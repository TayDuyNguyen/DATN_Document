<?php

$tables = [
    'failed_jobs',
    'job_batches',
    'cache_locks',
    'password_reset_tokens',
];

$payload = [
    'exported_at' => now()->toIso8601String(),
    'database' => DB::connection()->getDatabaseName(),
    'tables' => [],
];

foreach ($tables as $table) {
    $payload['tables'][$table] = DB::table($table)->orderBy(
        $table === 'cache_locks' ? 'key' : ($table === 'password_reset_tokens' ? 'email' : 'id')
    )->get();
}

$directory = 'D:/DATN/DATN_Tài liệu/data-center/backups';
$filename = $directory.'/runtime-cleanup-backup-'.now()->format('Ymd-His').'.json';

if (! is_dir($directory)) {
    mkdir($directory, 0775, true);
}

file_put_contents(
    $filename,
    json_encode($payload, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES)
);

echo json_encode([
    'backup_file' => $filename,
    'counts' => collect($payload['tables'])
        ->map(static fn ($rows) => count($rows))
        ->all(),
], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
