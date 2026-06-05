<?php

$out = [
    'total' => DB::table('tour_schedules')->count(),
    'missing_departure_code' => DB::table('tour_schedules')
        ->where(static function ($query) {
            $query->whereNull('departure_code')->orWhere('departure_code', '');
        })
        ->count(),
    'missing_departure_place' => DB::table('tour_schedules')
        ->where(static function ($query) {
            $query->whereNull('departure_place')->orWhere('departure_place', '');
        })
        ->count(),
    'missing_booking_deadline' => DB::table('tour_schedules')
        ->whereNull('booking_deadline')
        ->count(),
    'duplicate_departure_code_groups' => DB::table('tour_schedules')
        ->select('departure_code')
        ->groupBy('departure_code')
        ->havingRaw('count(*) > 1')
        ->count(),
    'past_open_booking' => DB::table('tour_schedules')
        ->whereDate('start_date', '<', now()->toDateString())
        ->where('booking_availability', 'open')
        ->count(),
    'past_sold_out_booking' => DB::table('tour_schedules')
        ->whereDate('start_date', '<', now()->toDateString())
        ->where('booking_availability', 'sold_out')
        ->count(),
    'future_open_booking' => DB::table('tour_schedules')
        ->whereDate('start_date', '>=', now()->toDateString())
        ->where('status', 'available')
        ->where('booking_availability', 'open')
        ->count(),
    'deadline_not_before_departure' => DB::table('tour_schedules as ts')
        ->join('tours as t', 't.id', '=', 'ts.tour_id')
        ->whereRaw(
            "ts.booking_deadline >= (ts.start_date::text || ' ' || COALESCE(NULLIF(t.start_time, ''), '07:30'))::timestamp"
        )
        ->count(),
];

echo json_encode($out, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
