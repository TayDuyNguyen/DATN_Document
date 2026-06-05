<?php

$bookings = DB::table('bookings as b')
    ->leftJoin('payments as p', 'p.booking_id', '=', 'b.id')
    ->whereNull('p.id')
    ->where('b.booking_status', 'completed')
    ->where('b.payment_status', 'pending')
    ->select('b.*')
    ->orderBy('b.id')
    ->get();

$directory = 'D:/DATN/DATN_Tài liệu/data-center/backups';
$filename = $directory.'/booking-payment-backfill-'.now()->format('Ymd-His').'.json';

if (! is_dir($directory)) {
    mkdir($directory, 0775, true);
}

file_put_contents($filename, json_encode([
    'exported_at' => now()->toIso8601String(),
    'database' => DB::connection()->getDatabaseName(),
    'bookings' => $bookings,
], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES));

echo json_encode([
    'backup_file' => $filename,
    'bookings' => $bookings->count(),
], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
