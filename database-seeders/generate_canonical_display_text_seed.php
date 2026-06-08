<?php

use Illuminate\Contracts\Console\Kernel;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schema;

$apiRoot = dirname(__DIR__, 2).DIRECTORY_SEPARATOR.'danangtrip-api';
require $apiRoot.DIRECTORY_SEPARATOR.'vendor'.DIRECTORY_SEPARATOR.'autoload.php';
$app = require $apiRoot.DIRECTORY_SEPARATOR.'bootstrap'.DIRECTORY_SEPARATOR.'app.php';
$app->make(Kernel::class)->bootstrap();

$displayColumns = [
    'categories' => ['name'],
    'subcategories' => ['name'],
    'tags' => ['name'],
    'amenities' => ['name'],
    'tour_categories' => ['name', 'description'],
    'blog_categories' => ['name', 'description'],
    'locations' => ['name', 'address', 'district', 'short_description', 'description'],
    'tours' => [
        'name',
        'short_desc',
        'description',
        'duration',
        'meeting_point',
        'itinerary',
        'inclusions',
        'exclusions',
    ],
    'blog_posts' => ['title', 'excerpt', 'content'],
];

$outputPath = __DIR__.DIRECTORY_SEPARATOR.'47_canonical_display_text_utf8_seed.sql';
$pdo = DB::connection()->getPdo();
$lines = [
    '-- DanangTrip canonical UTF-8 display text seed',
    '-- Generated from the audited live database on '.now()->toIso8601String(),
    '-- Run last in a full rebuild. It does not modify slugs, URLs, identifiers, relations, prices, or statuses.',
    '',
    'BEGIN;',
    '',
];
$tableCounts = [];

foreach ($displayColumns as $table => $wantedColumns) {
    if (! Schema::hasTable($table)) {
        continue;
    }

    $columns = array_values(array_filter(
        $wantedColumns,
        static fn (string $column): bool => Schema::hasColumn($table, $column)
    ));
    if ($columns === []) {
        continue;
    }

    $rows = DB::table($table)->select(array_merge(['id'], $columns))->orderBy('id')->get();
    $tableCounts[$table] = $rows->count();
    $lines[] = "-- {$table}: {$rows->count()} rows";

    foreach ($rows as $row) {
        $assignments = [];
        foreach ($columns as $column) {
            $value = $row->{$column};
            if ($value === null) {
                $assignments[] = "\"{$column}\" = NULL";
                continue;
            }

            if (! is_string($value)) {
                $value = json_encode($value, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
            }
            $assignments[] = "\"{$column}\" = ".$pdo->quote($value);
        }

        $lines[] = sprintf(
            'UPDATE "%s" SET %s WHERE "id" = %d;',
            $table,
            implode(', ', $assignments),
            $row->id
        );
    }
    $lines[] = '';
}

$lines[] = 'COMMIT;';
$lines[] = '';
file_put_contents($outputPath, implode(PHP_EOL, $lines));

echo json_encode([
    'output_path' => $outputPath,
    'tables' => $tableCounts,
    'rows' => array_sum($tableCounts),
], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE).PHP_EOL;
