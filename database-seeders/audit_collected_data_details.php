<?php

$out = [];

$out['location_length_distribution'] = [
    'description_min' => DB::table('locations')->min(DB::raw('char_length(trim(description))')),
    'description_avg' => round((float) DB::table('locations')->avg(DB::raw('char_length(trim(description))')), 1),
    'description_max' => DB::table('locations')->max(DB::raw('char_length(trim(description))')),
    'short_min' => DB::table('locations')->min(DB::raw('char_length(trim(short_description))')),
    'short_avg' => round((float) DB::table('locations')->avg(DB::raw('char_length(trim(short_description))')), 1),
    'short_max' => DB::table('locations')->max(DB::raw('char_length(trim(short_description))')),
];

$out['short_active_locations'] = DB::table('locations')
    ->where('status', 'active')
    ->whereRaw('char_length(trim(description)) < 100')
    ->orderByRaw('char_length(trim(description))')
    ->limit(30)
    ->get(['id', 'name', 'address', 'district', 'description']);

$out['locations_outside_bbox'] = DB::table('locations')
    ->where(static function ($query): void {
        $query->whereNotBetween('latitude', [15.85, 16.25])
            ->orWhereNotBetween('longitude', [107.95, 108.35]);
    })
    ->orderBy('id')
    ->get(['id', 'name', 'status', 'address', 'latitude', 'longitude']);

$out['duplicate_location_names'] = DB::table('locations')
    ->selectRaw("lower(regexp_replace(trim(name), '\\s+', ' ', 'g')) as normalized_name, count(*) as total, json_agg(json_build_object('id', id, 'name', name, 'status', status, 'address', address, 'lat', latitude, 'lng', longitude) order by id) as rows")
    ->groupByRaw("lower(regexp_replace(trim(name), '\\s+', ' ', 'g'))")
    ->havingRaw('count(*) > 1')
    ->get();

$out['duplicate_location_coordinates'] = DB::table('locations')
    ->selectRaw("round(latitude::numeric, 5) as lat, round(longitude::numeric, 5) as lng, count(*) as total, json_agg(json_build_object('id', id, 'name', name, 'status', status) order by id) as rows")
    ->groupByRaw('round(latitude::numeric, 5), round(longitude::numeric, 5)')
    ->havingRaw('count(*) > 1')
    ->orderByDesc('total')
    ->get();

$out['tour_length_distribution'] = [
    'description_min' => DB::table('tours')->min(DB::raw('char_length(trim(description))')),
    'description_avg' => round((float) DB::table('tours')->avg(DB::raw('char_length(trim(description))')), 1),
    'description_max' => DB::table('tours')->max(DB::raw('char_length(trim(description))')),
    'short_min' => DB::table('tours')->min(DB::raw('char_length(trim(short_desc))')),
    'short_avg' => round((float) DB::table('tours')->avg(DB::raw('char_length(trim(short_desc))')), 1),
    'short_max' => DB::table('tours')->max(DB::raw('char_length(trim(short_desc))')),
];

$out['duplicate_tour_names'] = DB::table('tours')
    ->selectRaw("lower(regexp_replace(trim(name), '\\s+', ' ', 'g')) as normalized_name, count(*) as total, json_agg(json_build_object('id', id, 'name', name, 'slug', slug, 'price', price_adult, 'duration', duration) order by id) as rows")
    ->groupByRaw("lower(regexp_replace(trim(name), '\\s+', ' ', 'g'))")
    ->havingRaw('count(*) > 1')
    ->orderByDesc('total')
    ->get();

$out['tour_samples'] = DB::table('tours')
    ->orderBy('id')
    ->limit(20)
    ->get(['id', 'name', 'slug', 'description', 'short_desc', 'duration', 'price_adult']);

$out['blog_length_distribution'] = [
    'content_min' => DB::table('blog_posts')->where('status', 'published')->min(DB::raw('char_length(trim(content))')),
    'content_avg' => round((float) DB::table('blog_posts')->where('status', 'published')->avg(DB::raw('char_length(trim(content))')), 1),
    'content_max' => DB::table('blog_posts')->where('status', 'published')->max(DB::raw('char_length(trim(content))')),
];

$out['short_blog_samples'] = DB::table('blog_posts')
    ->where('status', 'published')
    ->whereRaw('char_length(trim(content)) < 500')
    ->orderByRaw('char_length(trim(content))')
    ->limit(20)
    ->selectRaw('id, title, slug, char_length(trim(content)) as content_length, content')
    ->get();

$out['crawl_provenance'] = [
    'published_with_entity_link' => DB::table('crawl_items')
        ->where('status', 'published')
        ->whereNotNull('published_entity_id')
        ->count(),
    'published_without_entity_link' => DB::table('crawl_items')
        ->where('status', 'published')
        ->whereNull('published_entity_id')
        ->count(),
    'pending_with_duplicate_match' => DB::table('crawl_items')
        ->where('status', 'pending_review')
        ->whereNotNull('duplicate_source_id')
        ->count(),
    'pending_payload_missing_address' => DB::table('crawl_items')
        ->where('status', 'pending_review')
        ->whereRaw("coalesce(normalized_payload->>'address', '') = ''")
        ->count(),
    'pending_payload_missing_coordinates' => DB::table('crawl_items')
        ->where('status', 'pending_review')
        ->whereRaw("coalesce(normalized_payload->>'latitude', '') = '' or coalesce(normalized_payload->>'longitude', '') = ''")
        ->count(),
    'pending_payload_missing_images' => DB::table('crawl_items')
        ->where('status', 'pending_review')
        ->whereRaw("coalesce(normalized_payload->'imageUrls', '[]'::jsonb) = '[]'::jsonb")
        ->count(),
];

echo json_encode($out, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
