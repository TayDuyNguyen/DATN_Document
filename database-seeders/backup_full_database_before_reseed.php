<?php

$connection = DB::connection();

$tables = collect($connection->select("
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'public'
      AND table_type = 'BASE TABLE'
    ORDER BY table_name
"))->pluck('table_name');

$payload = [
    'exported_at' => now()->toIso8601String(),
    'database' => $connection->getDatabaseName(),
    'table_count' => $tables->count(),
    'tables' => [],
];

foreach ($tables as $table) {
    $payload['tables'][$table] = [
        'count' => DB::table($table)->count(),
        'rows' => DB::table($table)->get(),
    ];
}

$directory = 'D:/DATN/DATN_Tài liệu/data-center/backups';
$filename = $directory.'/full-database-before-reseed-'.now()->format('Ymd-His').'.json';

if (! is_dir($directory)) {
    mkdir($directory, 0775, true);
}

file_put_contents(
    $filename,
    json_encode($payload, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES)
);

echo json_encode([
    'backup_file' => $filename,
    'table_count' => $payload['table_count'],
    'row_counts' => collect($payload['tables'])
        ->map(static fn ($value) => $value['count'])
        ->all(),
], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
