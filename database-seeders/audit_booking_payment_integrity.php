<?php

$missingPayments = DB::table('bookings as b')
    ->leftJoin('payments as p', 'p.booking_id', '=', 'b.id')
    ->whereNull('p.id')
    ->select([
        'b.id',
        'b.booking_code',
        'b.booking_status',
        'b.payment_status',
        'b.payment_method',
        'b.final_amount',
        'b.deposit_amount',
        'b.booked_at',
    ])
    ->orderBy('b.id')
    ->get();

$out = [
    'bookings_without_payment' => [
        'total' => $missingPayments->count(),
        'by_payment_status' => $missingPayments
            ->groupBy('payment_status')
            ->map(static fn ($rows) => $rows->count())
            ->all(),
        'by_booking_status' => $missingPayments
            ->groupBy('booking_status')
            ->map(static fn ($rows) => $rows->count())
            ->all(),
        'requires_payment_history' => $missingPayments
            ->whereIn('payment_status', ['success', 'refunded', 'failed'])
            ->values(),
        'pending_without_attempt' => $missingPayments
            ->where('payment_status', 'pending')
            ->values(),
        'unpaid_without_attempt' => $missingPayments
            ->where('payment_status', 'unpaid')
            ->values(),
    ],
    'status_mismatches' => [
        'booking_success_without_success_payment' => DB::table('bookings as b')
            ->where('b.payment_status', 'success')
            ->whereNotExists(static function ($query) {
                $query->selectRaw('1')
                    ->from('payments as p')
                    ->whereColumn('p.booking_id', 'b.id')
                    ->where('p.payment_status', 'success');
            })
            ->pluck('b.id'),
        'booking_refunded_without_refunded_payment' => DB::table('bookings as b')
            ->where('b.payment_status', 'refunded')
            ->whereNotExists(static function ($query) {
                $query->selectRaw('1')
                    ->from('payments as p')
                    ->whereColumn('p.booking_id', 'b.id')
                    ->where('p.payment_status', 'refunded');
            })
            ->pluck('b.id'),
        'successful_payments_without_paid_at' => DB::table('payments')
            ->where('payment_status', 'success')
            ->whereNull('paid_at')
            ->pluck('id'),
        'refunded_payments_without_refunded_at' => DB::table('payments')
            ->where('payment_status', 'refunded')
            ->whereNull('refunded_at')
            ->pluck('id'),
        'payment_amount_mismatch' => DB::table('payments as p')
            ->join('bookings as b', 'b.id', '=', 'p.booking_id')
            ->whereColumn('p.amount', '<>', 'b.final_amount')
            ->select('p.id', 'p.booking_id', 'p.amount', 'b.final_amount')
            ->get(),
    ],
];

echo json_encode($out, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
