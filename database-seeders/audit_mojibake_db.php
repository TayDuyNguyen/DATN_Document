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
    'tours' => ['name', 'short_desc', 'description', 'duration', 'meeting_point', 'itinerary', 'inclusions', 'exclusions'],
    'blog_posts' => ['title', 'excerpt', 'content'],
];

$patterns = [
    'replacement_character' => '/�/u',
    'utf8_as_latin1_vietnamese' => '/(?:Ã[\x{0080}-\x{00BF}]|áº|á»|Ä[\x{0080}-\x{00BF}]|Æ[\x{0080}-\x{00BF}])/u',
    'broken_smart_punctuation' => '/(?:â€|â€™|â€œ|â€“|â€”|â€¦)/u',
    'broken_bom' => '/(?:ï»¿|ï¿½)/u',
    'broken_emoji' => '/ðŸ/u',
    'c1_control' => '/[\x{0080}-\x{009F}]/u',
];

$output = [
    'generated_at' => now()->toIso8601String(),
    'rows_scanned' => 0,
    'field_values_scanned' => 0,
    'rows_with_findings' => 0,
    'findings' => [],
    'counts' => [],
];

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

    $rows = DB::table($table)->select(array_merge(['id'], $columns))->get();
    $output['rows_scanned'] += $rows->count();
    foreach ($rows as $row) {
        $rowHasFinding = false;
        foreach ($columns as $column) {
            $rawValue = $row->{$column};
            if ($rawValue === null || $rawValue === '') {
                continue;
            }
            $value = is_string($rawValue) ? $rawValue : json_encode($rawValue, JSON_UNESCAPED_UNICODE);
            if ($value === false) {
                continue;
            }
            $output['field_values_scanned']++;
            foreach ($patterns as $type => $pattern) {
                if (preg_match($pattern, $value) !== 1) {
                    continue;
                }
                $rowHasFinding = true;
                $output['counts'][$type] = ($output['counts'][$type] ?? 0) + 1;
                if (count($output['findings']) < 500) {
                    $output['findings'][] = [
                        'table' => $table,
                        'id' => $row->id,
                        'column' => $column,
                        'type' => $type,
                        'value' => mb_substr(preg_replace('/\s+/u', ' ', $value), 0, 500),
                    ];
                }
            }
        }
        if ($rowHasFinding) {
            $output['rows_with_findings']++;
        }
    }
}

$reportDirectory = dirname(__DIR__).DIRECTORY_SEPARATOR.'data-center'.DIRECTORY_SEPARATOR.'reports';
if (! is_dir($reportDirectory)) {
    mkdir($reportDirectory, 0777, true);
}
$reportPath = $reportDirectory.DIRECTORY_SEPARATOR.'mojibake-db-audit-'.now()->format('Y-m-d').'.json';
file_put_contents(
    $reportPath,
    json_encode($output, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE).PHP_EOL
);

echo json_encode([
    'report_path' => $reportPath,
    'rows_scanned' => $output['rows_scanned'],
    'field_values_scanned' => $output['field_values_scanned'],
    'rows_with_findings' => $output['rows_with_findings'],
    'counts' => $output['counts'],
], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE).PHP_EOL;
