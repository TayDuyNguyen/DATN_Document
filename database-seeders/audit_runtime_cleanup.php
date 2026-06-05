<?php

$tables = [
    'failed_jobs',
    'job_batches',
    'cache_locks',
    'password_reset_tokens',
];

$out = [];

foreach ($tables as $table) {
    $out[$table] = [
        'columns' => Schema::getColumnListing($table),
        'count' => DB::table($table)->count(),
    ];
}

$out['ranges'] = [
    'failed_jobs' => DB::table('failed_jobs')
        ->selectRaw('min(failed_at) as min_at, max(failed_at) as max_at')
        ->first(),
    'job_batches' => DB::table('job_batches')
        ->selectRaw('min(created_at) as min_at, max(created_at) as max_at')
        ->first(),
    'password_reset_tokens' => DB::table('password_reset_tokens')
        ->selectRaw('min(created_at) as min_at, max(created_at) as max_at')
        ->first(),
];

echo json_encode($out, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
