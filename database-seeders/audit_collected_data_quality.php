<?php

$blank = static fn (string $column): Closure => static function ($query) use ($column): void {
    $query->whereNull($column)->orWhere($column, '');
};

$out = [];

$out['columns'] = [
    'locations' => Schema::getColumnListing('locations'),
    'tours' => Schema::getColumnListing('tours'),
    'blog_posts' => Schema::getColumnListing('blog_posts'),
    'crawl_items' => Schema::getColumnListing('crawl_items'),
];

$out['locations'] = [
    'total' => DB::table('locations')->count(),
    'active' => DB::table('locations')->where('status', 'active')->count(),
    'inactive' => DB::table('locations')->where('status', 'inactive')->count(),
    'blank_name' => DB::table('locations')->where($blank('name'))->count(),
    'blank_address' => DB::table('locations')->where($blank('address'))->count(),
    'blank_district' => DB::table('locations')->where($blank('district'))->count(),
    'blank_description' => DB::table('locations')->where($blank('description'))->count(),
    'short_description_under_40' => DB::table('locations')
        ->whereRaw('char_length(trim(short_description)) < 40')
        ->count(),
    'description_under_100' => DB::table('locations')
        ->whereRaw('char_length(trim(description)) < 100')
        ->count(),
    'zero_coordinates' => DB::table('locations')
        ->where(static fn ($query) => $query->where('latitude', 0)->orWhere('longitude', 0))
        ->count(),
    'outside_danang_bbox' => DB::table('locations')
        ->where(static function ($query): void {
            $query->whereNotBetween('latitude', [15.85, 16.25])
                ->orWhereNotBetween('longitude', [107.95, 108.35]);
        })
        ->count(),
    'missing_thumbnail' => DB::table('locations')->where($blank('thumbnail'))->count(),
    'non_cloudinary_thumbnail' => DB::table('locations')
        ->whereNotNull('thumbnail')
        ->where('thumbnail', '<>', '')
        ->where('thumbnail', 'not like', 'https://res.cloudinary.com/%')
        ->count(),
    'empty_images' => DB::table('locations')
        ->whereRaw("images is null or images::text in ('[]', 'null', '\"\"')")
        ->count(),
    'invalid_price_range' => DB::table('locations')
        ->whereNotNull('price_min')
        ->whereNotNull('price_max')
        ->whereColumn('price_min', '>', 'price_max')
        ->count(),
    'duplicate_normalized_name_groups' => DB::table('locations')
        ->selectRaw("lower(regexp_replace(trim(name), '\\s+', ' ', 'g')) as normalized_name")
        ->groupByRaw("lower(regexp_replace(trim(name), '\\s+', ' ', 'g'))")
        ->havingRaw('count(*) > 1')
        ->count(),
    'near_duplicate_coordinate_groups' => DB::table('locations')
        ->selectRaw('round(latitude::numeric, 5) as lat, round(longitude::numeric, 5) as lng')
        ->groupByRaw('round(latitude::numeric, 5), round(longitude::numeric, 5)')
        ->havingRaw('count(*) > 1')
        ->count(),
];

$out['tours'] = [
    'total' => DB::table('tours')->count(),
    'blank_description' => DB::table('tours')->where($blank('description'))->count(),
    'description_under_150' => DB::table('tours')
        ->whereRaw('char_length(trim(description)) < 150')
        ->count(),
    'short_desc_under_40' => DB::table('tours')
        ->whereRaw('char_length(trim(short_desc)) < 40')
        ->count(),
    'missing_duration' => DB::table('tours')->where($blank('duration'))->count(),
    'missing_start_time' => DB::table('tours')->where($blank('start_time'))->count(),
    'missing_meeting_point' => DB::table('tours')->where($blank('meeting_point'))->count(),
    'missing_itinerary' => DB::table('tours')->whereRaw('itinerary is null or json_array_length(itinerary) = 0')->count(),
    'missing_inclusions' => DB::table('tours')->whereRaw('inclusions is null or json_array_length(inclusions) = 0')->count(),
    'missing_exclusions' => DB::table('tours')->whereRaw('exclusions is null or json_array_length(exclusions) = 0')->count(),
    'missing_images' => DB::table('tours')->whereRaw('images is null or json_array_length(images) = 0')->count(),
    'non_cloudinary_thumbnail' => DB::table('tours')
        ->whereNotNull('thumbnail')
        ->where('thumbnail', '<>', '')
        ->where('thumbnail', 'not like', 'https://res.cloudinary.com/%')
        ->count(),
    'invalid_people_range' => DB::table('tours')->whereColumn('min_people', '>', 'max_people')->count(),
    'zero_adult_price' => DB::table('tours')->where('price_adult', '<=', 0)->count(),
    'duplicate_normalized_name_groups' => DB::table('tours')
        ->selectRaw("lower(regexp_replace(trim(name), '\\s+', ' ', 'g')) as normalized_name")
        ->groupByRaw("lower(regexp_replace(trim(name), '\\s+', ' ', 'g'))")
        ->havingRaw('count(*) > 1')
        ->count(),
];

$out['blogs'] = [
    'total' => DB::table('blog_posts')->count(),
    'published' => DB::table('blog_posts')->where('status', 'published')->count(),
    'published_missing_excerpt' => DB::table('blog_posts')
        ->where('status', 'published')
        ->where($blank('excerpt'))
        ->count(),
    'published_content_under_500' => DB::table('blog_posts')
        ->where('status', 'published')
        ->whereRaw('char_length(trim(content)) < 500')
        ->count(),
    'published_missing_image' => DB::table('blog_posts')
        ->where('status', 'published')
        ->where($blank('featured_image'))
        ->count(),
    'published_non_cloudinary_image' => DB::table('blog_posts')
        ->where('status', 'published')
        ->whereNotNull('featured_image')
        ->where('featured_image', '<>', '')
        ->where('featured_image', 'not like', 'https://res.cloudinary.com/%')
        ->count(),
    'published_missing_published_at' => DB::table('blog_posts')
        ->where('status', 'published')
        ->whereNull('published_at')
        ->count(),
    'duplicate_normalized_title_groups' => DB::table('blog_posts')
        ->selectRaw("lower(regexp_replace(trim(title), '\\s+', ' ', 'g')) as normalized_title")
        ->groupByRaw("lower(regexp_replace(trim(title), '\\s+', ' ', 'g'))")
        ->havingRaw('count(*) > 1')
        ->count(),
];

$crawlColumns = collect($out['columns']['crawl_items']);
$crawl = DB::table('crawl_items');
$out['crawl'] = [
    'total' => (clone $crawl)->count(),
    'published' => (clone $crawl)->where('status', 'published')->count(),
    'pending_review' => (clone $crawl)->where('status', 'pending_review')->count(),
    'rejected' => (clone $crawl)->where('status', 'rejected')->count(),
];

foreach (['source_url', 'external_id', 'name', 'address', 'latitude', 'longitude'] as $column) {
    if ($crawlColumns->contains($column)) {
        $out['crawl']['missing_'.$column] = DB::table('crawl_items')
            ->where('status', 'pending_review')
            ->where(static function ($query) use ($column): void {
                $query->whereNull($column)->orWhere($column, '');
            })
            ->count();
    }
}

if ($crawlColumns->contains('raw_data')) {
    $out['crawl']['pending_missing_image_candidates'] = DB::table('crawl_items')
        ->where('status', 'pending_review')
        ->whereRaw("coalesce(raw_data->'imageUrls', '[]'::jsonb) = '[]'::jsonb")
        ->count();
}

echo json_encode($out, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
