<?php

$slugs = collect(json_decode(
    file_get_contents(
        'D:/DATN/DATN_Tài liệu/danangtrip-crawler/data/verified-real-tour-catalog-cloudinary-20260607.json'
    ),
    true,
    flags: JSON_THROW_ON_ERROR
))->pluck('slug')->values();

$existingTourIds = DB::table('tours')
    ->whereIn('slug', $slugs)
    ->pluck('id');

$payload = [
    'exported_at' => now()->toIso8601String(),
    'database' => DB::connection()->getDatabaseName(),
    'catalog_slugs' => $slugs,
    'existing_tours' => DB::table('tours')->whereIn('id', $existingTourIds)->orderBy('id')->get(),
    'existing_schedules' => DB::table('tour_schedules')
        ->whereIn('tour_id', $existingTourIds)
        ->orderBy('id')
        ->get(),
    'existing_locations' => DB::table('tour_locations')
        ->whereIn('tour_id', $existingTourIds)
        ->orderBy('id')
        ->get(),
];

$directory = 'D:/DATN/DATN_Tài liệu/data-center/backups';
$filename = $directory.'/verified-real-tour-import-before-'.now()->format('Ymd-His').'.json';

if (! is_dir($directory)) {
    mkdir($directory, 0775, true);
}

file_put_contents(
    $filename,
    json_encode($payload, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES)
);

echo json_encode([
    'backup_file' => $filename,
    'existing_tours' => count($payload['existing_tours']),
    'existing_schedules' => count($payload['existing_schedules']),
    'existing_locations' => count($payload['existing_locations']),
], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
