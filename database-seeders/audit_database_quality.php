<?php

$out = [];

foreach ([
    'locations',
    'categories',
    'location_tags',
    'location_amenities',
    'tours',
    'tour_schedules',
    'tour_locations',
    'tour_categories',
    'blog_posts',
    'blog_categories',
    'promotions',
    'landing_pages',
    'crawl_items',
    'bookings',
    'booking_items',
    'payments',
    'users',
] as $table) {
    $out[$table] = Schema::hasTable($table) ? DB::table($table)->count() : null;
}

$out['locations_active'] = DB::table('locations')->where('status', 'active')->count();
$out['locations_inactive'] = DB::table('locations')->where('status', 'inactive')->count();
$out['locations_missing_thumbnail'] = DB::table('locations')
    ->where(function ($query) {
        $query->whereNull('thumbnail')->orWhere('thumbnail', '');
    })
    ->count();
$out['active_location_duplicate_lower_name_groups'] = DB::table('locations')
    ->where('status', 'active')
    ->select(DB::raw('lower(name) as n'))
    ->groupBy(DB::raw('lower(name)'))
    ->havingRaw('count(*) > 1')
    ->count();

$out['tours_missing_cloudinary_thumbnail'] = DB::table('tours')
    ->where(function ($query) {
        $query->whereNull('thumbnail')
            ->orWhere('thumbnail', '')
            ->orWhere('thumbnail', 'not like', 'https://res.cloudinary.com/%');
    })
    ->count();
foreach (['itinerary', 'inclusions', 'exclusions', 'images'] as $field) {
    $out['tours_missing_or_empty_' . $field] = DB::table('tours')
        ->whereRaw("$field is null or json_array_length($field) = 0")
        ->count();
}
$out['tours_without_schedule'] = DB::table('tours as t')
    ->leftJoin('tour_schedules as s', 's.tour_id', '=', 't.id')
    ->whereNull('s.id')
    ->count();
$out['tours_without_location_mapping'] = DB::table('tours as t')
    ->leftJoin('tour_locations as tl', 'tl.tour_id', '=', 't.id')
    ->whereNull('tl.id')
    ->count();

$out['blog_missing_excerpt'] = DB::table('blog_posts')
    ->where(function ($query) {
        $query->whereNull('excerpt')->orWhere('excerpt', '');
    })
    ->count();
$out['blog_missing_content'] = DB::table('blog_posts')
    ->where(function ($query) {
        $query->whereNull('content')->orWhere('content', '');
    })
    ->count();
$out['blog_missing_featured_image'] = DB::table('blog_posts')
    ->where(function ($query) {
        $query->whereNull('featured_image')->orWhere('featured_image', '');
    })
    ->count();
$out['published_blog_missing_featured_image'] = DB::table('blog_posts')
    ->where('status', 'published')
    ->where(function ($query) {
        $query->whereNull('featured_image')->orWhere('featured_image', '');
    })
    ->count();

$out['crawl_pending_review'] = DB::table('crawl_items')->where('status', 'pending_review')->count();
$out['crawl_published'] = DB::table('crawl_items')->where('status', 'published')->count();
$out['crawl_rejected'] = DB::table('crawl_items')->where('status', 'rejected')->count();

echo json_encode($out, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
