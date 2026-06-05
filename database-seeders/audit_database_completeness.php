<?php

$out = [];

$statusCounts = static function (string $table, string $column = 'status'): array {
    return DB::table($table)
        ->select($column, DB::raw('count(*) as total'))
        ->groupBy($column)
        ->orderBy($column)
        ->pluck('total', $column)
        ->map(static fn ($value) => (int) $value)
        ->all();
};

$out['status_distributions'] = [
    'locations' => $statusCounts('locations'),
    'tours' => $statusCounts('tours'),
    'tour_schedules' => $statusCounts('tour_schedules'),
    'blog_posts' => $statusCounts('blog_posts'),
    'bookings' => [
        'booking_status' => $statusCounts('bookings', 'booking_status'),
        'payment_status' => $statusCounts('bookings', 'payment_status'),
    ],
    'payments' => $statusCounts('payments', 'payment_status'),
    'promotions' => $statusCounts('promotions'),
    'crawl_items' => $statusCounts('crawl_items'),
];

$out['user_roles'] = DB::table('users')
    ->select('role', DB::raw('count(*) as total'))
    ->groupBy('role')
    ->orderBy('role')
    ->pluck('total', 'role')
    ->map(static fn ($value) => (int) $value)
    ->all();

$out['relation_gaps'] = [
    'locations_without_tags' => DB::table('locations as l')
        ->leftJoin('location_tags as lt', 'lt.location_id', '=', 'l.id')
        ->whereNull('lt.location_id')
        ->count(),
    'locations_without_amenities' => DB::table('locations as l')
        ->leftJoin('location_amenities as la', 'la.location_id', '=', 'l.id')
        ->whereNull('la.location_id')
        ->count(),
    'tours_without_locations' => DB::table('tours as t')
        ->leftJoin('tour_locations as tl', 'tl.tour_id', '=', 't.id')
        ->whereNull('tl.tour_id')
        ->count(),
    'tours_without_schedules' => DB::table('tours as t')
        ->leftJoin('tour_schedules as ts', 'ts.tour_id', '=', 't.id')
        ->whereNull('ts.tour_id')
        ->count(),
    'blog_posts_without_categories' => DB::table('blog_posts as bp')
        ->leftJoin('blog_post_categories as bpc', 'bpc.post_id', '=', 'bp.id')
        ->whereNull('bpc.post_id')
        ->count(),
    'bookings_without_items' => DB::table('bookings as b')
        ->leftJoin('booking_items as bi', 'bi.booking_id', '=', 'b.id')
        ->whereNull('bi.booking_id')
        ->count(),
    'ratings_without_user' => DB::table('ratings as r')
        ->leftJoin('users as u', 'u.id', '=', 'r.user_id')
        ->whereNull('u.id')
        ->count(),
    'favorites_without_user' => DB::table('favorites as f')
        ->leftJoin('users as u', 'u.id', '=', 'f.user_id')
        ->whereNull('u.id')
        ->count(),
];

$out['content_quality'] = [
    'active_locations' => DB::table('locations')->where('status', 'active')->count(),
    'inactive_locations' => DB::table('locations')->where('status', 'inactive')->count(),
    'locations_missing_thumbnail' => DB::table('locations')
        ->where(static function ($query) {
            $query->whereNull('thumbnail')->orWhere('thumbnail', '');
        })
        ->count(),
    'active_location_duplicate_names' => DB::table('locations')
        ->where('status', 'active')
        ->select(DB::raw('lower(name) as normalized_name'))
        ->groupBy(DB::raw('lower(name)'))
        ->havingRaw('count(*) > 1')
        ->count(),
    'tours_missing_thumbnail' => DB::table('tours')
        ->where(static function ($query) {
            $query->whereNull('thumbnail')->orWhere('thumbnail', '');
        })
        ->count(),
    'tour_generic_slugs' => DB::table('tours')->where('slug', 'like', 'tour-real-variant-%')->count(),
    'blog_posts_missing_featured_image' => DB::table('blog_posts')
        ->where(static function ($query) {
            $query->whereNull('featured_image')->orWhere('featured_image', '');
        })
        ->count(),
];

$out['schedule_quality'] = [
    'future_available_schedules' => DB::table('tour_schedules')
        ->whereDate('start_date', '>=', now()->toDateString())
        ->where('status', 'available')
        ->count(),
    'past_open_booking_schedules' => DB::table('tour_schedules')
        ->whereDate('start_date', '<', now()->toDateString())
        ->where('booking_availability', 'open')
        ->count(),
    'overbooked_schedules' => DB::table('tour_schedules')
        ->whereColumn('booked_people', '>', 'max_people')
        ->count(),
    'schedules_missing_departure_code' => DB::table('tour_schedules')
        ->where(static function ($query) {
            $query->whereNull('departure_code')->orWhere('departure_code', '');
        })
        ->count(),
    'schedules_missing_departure_place' => DB::table('tour_schedules')
        ->where(static function ($query) {
            $query->whereNull('departure_place')->orWhere('departure_place', '');
        })
        ->count(),
];

$out['runtime_tables'] = [
    'jobs' => DB::table('jobs')->count(),
    'failed_jobs' => DB::table('failed_jobs')->count(),
    'job_batches' => DB::table('job_batches')->count(),
    'cache' => DB::table('cache')->count(),
    'cache_locks' => DB::table('cache_locks')->count(),
    'sessions' => DB::table('sessions')->count(),
    'password_reset_tokens' => DB::table('password_reset_tokens')->count(),
    'refresh_tokens' => DB::table('refresh_tokens')->count(),
];

$out['runtime_suspicion'] = [
    'failed_jobs_with_exception' => DB::table('failed_jobs')
        ->whereNotNull('exception')
        ->count(),
    'expired_password_reset_tokens' => DB::table('password_reset_tokens')
        ->where('created_at', '<', now()->subHours(24))
        ->count(),
    'expired_refresh_tokens' => Schema::hasColumn('refresh_tokens', 'expires_at')
        ? DB::table('refresh_tokens')->where('expires_at', '<', now())->count()
        : null,
];

echo json_encode($out, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
