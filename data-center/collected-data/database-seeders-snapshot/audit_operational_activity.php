<?php

$windows = [7, 30, 90];
$activityTables = [
    'bookings' => 'booked_at',
    'payments' => 'created_at',
    'favorites' => 'created_at',
    'views' => 'created_at',
    'search_logs' => 'created_at',
    'notifications' => 'created_at',
    'ratings' => 'created_at',
    'contacts' => 'created_at',
];

$out = [
    'generated_at' => now()->toIso8601String(),
    'activity_windows' => [],
    'latest_activity' => [],
];

foreach ($activityTables as $table => $column) {
    $out['latest_activity'][$table] = DB::table($table)->max($column);

    foreach ($windows as $days) {
        $out['activity_windows'][$days . '_days'][$table] = DB::table($table)
            ->where($column, '>=', now()->subDays($days))
            ->count();
    }
}

$out['user_activity'] = [
    'active_users' => DB::table('users')->where('status', 'active')->count(),
    'users_never_logged_in' => DB::table('users')->whereNull('last_login_at')->count(),
    'users_logged_in_last_30_days' => DB::table('users')
        ->where('last_login_at', '>=', now()->subDays(30))
        ->count(),
    'users_with_recent_favorites' => DB::table('favorites')
        ->where('created_at', '>=', now()->subDays(30))
        ->distinct('user_id')
        ->count('user_id'),
    'users_with_recent_searches' => DB::table('search_logs')
        ->whereNotNull('user_id')
        ->where('created_at', '>=', now()->subDays(30))
        ->distinct('user_id')
        ->count('user_id'),
];

$out['engagement_distribution'] = [
    'locations_with_views' => DB::table('views')
        ->whereNotNull('location_id')
        ->distinct('location_id')
        ->count('location_id'),
    'active_locations_without_views' => DB::table('locations as l')
        ->where('l.status', 'active')
        ->whereNotExists(static function ($query) {
            $query->selectRaw('1')
                ->from('views as v')
                ->whereColumn('v.location_id', 'l.id');
        })
        ->count(),
    'locations_with_favorites' => DB::table('favorites')
        ->whereNotNull('location_id')
        ->distinct('location_id')
        ->count('location_id'),
    'active_locations_without_favorites' => DB::table('locations as l')
        ->where('l.status', 'active')
        ->whereNotExists(static function ($query) {
            $query->selectRaw('1')
                ->from('favorites as f')
                ->whereColumn('f.location_id', 'l.id');
        })
        ->count(),
    'active_tours_with_views' => DB::table('views as v')
        ->join('tours as t', 't.id', '=', 'v.tour_id')
        ->where('t.status', 'active')
        ->distinct('t.id')
        ->count('t.id'),
    'active_tours_without_views' => DB::table('tours as t')
        ->where('t.status', 'active')
        ->whereNotExists(static function ($query) {
            $query->selectRaw('1')
                ->from('views as v')
                ->whereColumn('v.tour_id', 't.id');
        })
        ->count(),
    'active_tours_with_favorites' => DB::table('favorites as f')
        ->join('tours as t', 't.id', '=', 'f.tour_id')
        ->where('t.status', 'active')
        ->distinct('t.id')
        ->count('t.id'),
    'active_tours_without_favorites' => DB::table('tours as t')
        ->where('t.status', 'active')
        ->whereNotExists(static function ($query) {
            $query->selectRaw('1')
                ->from('favorites as f')
                ->whereColumn('f.tour_id', 't.id');
        })
        ->count(),
];

$out['counter_integrity'] = [
    'location_view_count_mismatches' => DB::table('locations as l')
        ->whereRaw('l.view_count <> (SELECT COUNT(*) FROM views v WHERE v.location_id = l.id)')
        ->count(),
    'location_favorite_count_mismatches' => DB::table('locations as l')
        ->whereRaw('l.favorite_count <> (SELECT COUNT(*) FROM favorites f WHERE f.location_id = l.id)')
        ->count(),
    'tour_view_count_mismatches' => DB::table('tours as t')
        ->whereRaw('t.view_count <> (SELECT COUNT(*) FROM views v WHERE v.tour_id = t.id)')
        ->count(),
    'tour_booking_count_mismatches' => DB::table('tours as t')
        ->whereRaw(
            "t.booking_count <> (
                SELECT COUNT(*)
                FROM booking_items bi
                JOIN bookings b ON b.id = bi.booking_id
                WHERE bi.tour_id = t.id
                  AND b.booking_status <> 'cancelled'
            )"
        )
        ->count(),
];

$out['commercial_health'] = [
    'recent_bookings_30_days' => DB::table('bookings')
        ->where('booked_at', '>=', now()->subDays(30))
        ->count(),
    'recent_successful_payments_30_days' => DB::table('payments')
        ->where('payment_status', 'success')
        ->where('paid_at', '>=', now()->subDays(30))
        ->count(),
    'stale_pending_bookings_over_7_days' => DB::table('bookings')
        ->where('booking_status', 'pending')
        ->where('booked_at', '<', now()->subDays(7))
        ->count(),
    'completed_bookings_without_completed_at' => DB::table('bookings')
        ->where('booking_status', 'completed')
        ->whereNull('completed_at')
        ->count(),
    'confirmed_bookings_without_confirmed_at' => DB::table('bookings')
        ->where('booking_status', 'confirmed')
        ->whereNull('confirmed_at')
        ->count(),
    'cancelled_bookings_without_cancelled_at' => DB::table('bookings')
        ->where('booking_status', 'cancelled')
        ->whereNull('cancelled_at')
        ->count(),
];

$out['notification_health'] = [
    'unread_notifications' => DB::table('notifications')->where('is_read', false)->count(),
    'read_without_read_at' => DB::table('notifications')
        ->where('is_read', true)
        ->whereNull('read_at')
        ->count(),
    'unread_with_read_at' => DB::table('notifications')
        ->where('is_read', false)
        ->whereNotNull('read_at')
        ->count(),
];

echo json_encode($out, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
