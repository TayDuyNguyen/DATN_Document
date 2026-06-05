<?php

$out = [];

$out['category_coverage'] = [
    'location_categories_total' => DB::table('categories')->count(),
    'location_categories_used' => DB::table('locations')->distinct('category_id')->count('category_id'),
    'location_categories_unused' => DB::table('categories as c')
        ->leftJoin('locations as l', 'l.category_id', '=', 'c.id')
        ->whereNull('l.id')
        ->count(),
    'subcategories_total' => DB::table('subcategories')->count(),
    'subcategories_used' => DB::table('locations')
        ->whereNotNull('subcategory_id')
        ->distinct('subcategory_id')
        ->count('subcategory_id'),
    'tour_categories_total' => DB::table('tour_categories')->count(),
    'tour_categories_used' => DB::table('tours')->distinct('tour_category_id')->count('tour_category_id'),
    'tour_categories_unused' => DB::table('tour_categories as tc')
        ->leftJoin('tours as t', 't.tour_category_id', '=', 'tc.id')
        ->whereNull('t.id')
        ->count(),
    'blog_categories_total' => DB::table('blog_categories')->count(),
    'blog_categories_used' => DB::table('blog_post_categories')
        ->distinct('blog_category_id')
        ->count('blog_category_id'),
    'blog_categories_unused' => DB::table('blog_categories as bc')
        ->leftJoin('blog_post_categories as bpc', 'bpc.blog_category_id', '=', 'bc.id')
        ->whereNull('bpc.id')
        ->count(),
];

$out['engagement_coverage'] = [
    'ratings' => DB::table('ratings')->count(),
    'rating_images' => DB::table('rating_images')->count(),
    'favorites' => DB::table('favorites')->count(),
    'views' => DB::table('views')->count(),
    'search_logs' => DB::table('search_logs')->count(),
    'notifications' => DB::table('notifications')->count(),
    'contacts' => DB::table('contacts')->count(),
    'locations_with_ratings' => DB::table('ratings')
        ->whereNotNull('location_id')
        ->distinct('location_id')
        ->count('location_id'),
    'tours_with_ratings' => DB::table('ratings')
        ->whereNotNull('tour_id')
        ->distinct('tour_id')
        ->count('tour_id'),
    'users_with_bookings' => DB::table('bookings')
        ->whereNotNull('user_id')
        ->distinct('user_id')
        ->count('user_id'),
    'users_with_favorites' => DB::table('favorites')
        ->distinct('user_id')
        ->count('user_id'),
];

$out['commercial_coverage'] = [
    'active_promotions' => DB::table('promotions')->where('status', 'active')->count(),
    'usable_future_promotions' => DB::table('promotions')
        ->where('status', 'active')
        ->where(static function ($query) {
            $query->whereNull('ends_at')->orWhere('ends_at', '>=', now());
        })
        ->count(),
    'landing_pages' => DB::table('landing_pages')->count(),
    'bookings' => DB::table('bookings')->count(),
    'booking_items' => DB::table('booking_items')->count(),
    'payments' => DB::table('payments')->count(),
    'bookings_without_payment_record' => DB::table('bookings as b')
        ->leftJoin('payments as p', 'p.booking_id', '=', 'b.id')
        ->whereNull('p.id')
        ->count(),
];

$out['specific_gaps'] = [
    'blog_without_category' => DB::table('blog_posts as bp')
        ->leftJoin('blog_post_categories as bpc', 'bpc.post_id', '=', 'bp.id')
        ->whereNull('bpc.id')
        ->select('bp.id', 'bp.title', 'bp.slug', 'bp.status')
        ->get(),
    'past_open_booking_schedule_ids' => DB::table('tour_schedules')
        ->whereDate('start_date', '<', now()->toDateString())
        ->where('booking_availability', 'open')
        ->orderBy('start_date')
        ->limit(20)
        ->pluck('id'),
];

echo json_encode($out, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
