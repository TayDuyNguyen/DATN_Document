<?php

use Illuminate\Contracts\Console\Kernel;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schema;

$apiRoot = dirname(__DIR__, 2).DIRECTORY_SEPARATOR.'danangtrip-api';
require $apiRoot.DIRECTORY_SEPARATOR.'vendor'.DIRECTORY_SEPARATOR.'autoload.php';
$app = require $apiRoot.DIRECTORY_SEPARATOR.'bootstrap'.DIRECTORY_SEPARATOR.'app.php';
$app->make(Kernel::class)->bootstrap();

$apply = in_array('--apply', $argv, true);
$generatedAt = now();

$relationTables = [
    'booking_items' => 10000,
    'cart_items' => 100000,
    'ratings' => 1000,
    'favorites' => 100,
    'views' => 10,
];
$relationCounts = [];
foreach ($relationTables as $table => $weight) {
    if (! Schema::hasTable($table) || ! Schema::hasColumn($table, 'tour_id')) {
        continue;
    }
    $relationCounts[$table] = DB::table($table)
        ->whereNotNull('tour_id')
        ->selectRaw('tour_id, count(*) as aggregate')
        ->groupBy('tour_id')
        ->pluck('aggregate', 'tour_id')
        ->map(static fn ($count): int => (int) $count);
}

$tours = DB::table('tours')
    ->select([
        'id', 'name', 'slug', 'status', 'booking_availability', 'price_adult',
        'short_desc', 'description', 'duration', 'meeting_point',
        'itinerary', 'inclusions', 'exclusions',
    ])
    ->orderBy('id')
    ->get();

$groups = [];
foreach ($tours as $tour) {
    $nameKey = normalizeDuplicateText($tour->name);
    $contentFingerprint = hash('sha256', implode('|', [
        normalizeFingerprintValue($tour->short_desc),
        normalizeFingerprintValue($tour->description),
        normalizeFingerprintValue($tour->itinerary),
        normalizeFingerprintValue($tour->inclusions),
        normalizeFingerprintValue($tour->exclusions),
        normalizeFingerprintValue($tour->duration),
        normalizeFingerprintValue($tour->meeting_point),
    ]));
    $groups[$nameKey][$contentFingerprint][] = $tour;
}

$tourGroups = [];
$deactivateIds = [];
foreach ($groups as $nameGroups) {
    foreach ($nameGroups as $rows) {
        if (count($rows) < 2) {
            continue;
        }
        $ranked = [];
        foreach ($rows as $row) {
            $counts = [];
            $score = 0;
            foreach ($relationTables as $table => $weight) {
                $count = $relationCounts[$table]->get($row->id, 0) ?? 0;
                $counts[$table] = $count;
                $score += $count * $weight;
            }
            $ranked[] = [
                'row' => $row,
                'score' => $score,
                'relation_counts' => $counts,
            ];
        }
        usort($ranked, static function (array $left, array $right): int {
            $scoreCompare = $right['score'] <=> $left['score'];
            if ($scoreCompare !== 0) {
                return $scoreCompare;
            }

            return $left['row']->id <=> $right['row']->id;
        });

        $canonical = $ranked[0];
        $duplicates = array_slice($ranked, 1);
        $duplicateIds = array_map(static fn (array $item): int => $item['row']->id, $duplicates);
        array_push($deactivateIds, ...$duplicateIds);
        $tourGroups[] = [
            'name' => $canonical['row']->name,
            'canonical' => summarizeTourDecision($canonical),
            'deactivate' => array_map('summarizeTourDecision', $duplicates),
        ];
    }
}

$duplicateBlog = DB::table('blog_posts')->where('id', 105)->first();
$canonicalBlog = DB::table('blog_posts')->where('id', 103)->first();
$archiveBlog105 = $duplicateBlog !== null
    && $canonicalBlog !== null
    && normalizeFingerprintValue($duplicateBlog->excerpt) === normalizeFingerprintValue($canonicalBlog->excerpt)
    && normalizeFingerprintValue($duplicateBlog->content) === normalizeFingerprintValue($canonicalBlog->content);

$backupDirectory = dirname(__DIR__).DIRECTORY_SEPARATOR.'data-center'.DIRECTORY_SEPARATOR.'backups';
$reportDirectory = dirname(__DIR__).DIRECTORY_SEPARATOR.'data-center'.DIRECTORY_SEPARATOR.'reports';
foreach ([$backupDirectory, $reportDirectory] as $directory) {
    if (! is_dir($directory)) {
        mkdir($directory, 0777, true);
    }
}
$stamp = $generatedAt->format('Y-m-d-His');
$backupPath = $backupDirectory.DIRECTORY_SEPARATOR."catalog-before-duplicate-repair-{$stamp}.json";
$reportPath = $reportDirectory.DIRECTORY_SEPARATOR."duplicate-catalog-repair-{$stamp}.json";
$backup = [
    'generated_at' => $generatedAt->toIso8601String(),
    'mode' => $apply ? 'apply' : 'dry-run',
    'tours' => DB::table('tours')->whereIn('id', $deactivateIds)->orderBy('id')->get(),
    'blog_posts' => DB::table('blog_posts')->whereIn('id', [103, 105])->orderBy('id')->get(),
];
file_put_contents(
    $backupPath,
    json_encode($backup, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES).PHP_EOL
);

if ($apply) {
    DB::transaction(static function () use ($deactivateIds, $archiveBlog105): void {
        if ($deactivateIds !== []) {
            DB::table('tours')
                ->whereIn('id', $deactivateIds)
                ->update([
                    'status' => 'inactive',
                    'booking_availability' => 'sold_out',
                    'updated_at' => now(),
                ]);
        }
        if ($archiveBlog105) {
            DB::table('blog_posts')
                ->where('id', 105)
                ->update([
                    'status' => 'archived',
                    'updated_at' => now(),
                ]);
        }
    });
}

$seedPath = __DIR__.DIRECTORY_SEPARATOR.'48_deactivate_duplicate_catalog_seed.sql';
$idList = implode(', ', array_map('intval', $deactivateIds));
$seed = [
    '-- DanangTrip duplicate catalog visibility repair',
    '-- Keeps historical relations; does not delete tours or blog posts.',
    'BEGIN;',
    '',
    "UPDATE tours SET status = 'inactive', booking_availability = 'sold_out', updated_at = NOW()",
    "WHERE id IN ({$idList});",
    '',
];
if ($archiveBlog105) {
    $seed[] = "UPDATE blog_posts SET status = 'archived', updated_at = NOW() WHERE id = 105;";
    $seed[] = '';
}
$seed[] = 'COMMIT;';
$seed[] = '';
file_put_contents($seedPath, implode(PHP_EOL, $seed));

$report = [
    'generated_at' => $generatedAt->toIso8601String(),
    'mode' => $apply ? 'apply' : 'dry-run',
    'tour_duplicate_groups' => count($tourGroups),
    'canonical_tours_kept_active' => count($tourGroups),
    'tour_ids_deactivated' => $deactivateIds,
    'tour_count_deactivated' => count($deactivateIds),
    'blog_105_archived' => $archiveBlog105,
    'backup_path' => $backupPath,
    'seed_path' => $seedPath,
    'groups' => $tourGroups,
];
file_put_contents(
    $reportPath,
    json_encode($report, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES).PHP_EOL
);

echo json_encode([
    'mode' => $report['mode'],
    'tour_duplicate_groups' => $report['tour_duplicate_groups'],
    'canonical_tours_kept_active' => $report['canonical_tours_kept_active'],
    'tour_count_deactivated' => $report['tour_count_deactivated'],
    'blog_105_archived' => $report['blog_105_archived'],
    'backup_path' => $backupPath,
    'report_path' => $reportPath,
    'seed_path' => $seedPath,
], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE).PHP_EOL;

function normalizeDuplicateText(?string $value): string
{
    $value = mb_strtolower(trim((string) $value), 'UTF-8');
    $ascii = iconv('UTF-8', 'ASCII//TRANSLIT//IGNORE', $value);
    $ascii = $ascii === false ? $value : $ascii;

    return trim(preg_replace('/\s+/', ' ', preg_replace('/[^a-z0-9]+/', ' ', strtolower($ascii))));
}

function normalizeFingerprintValue(mixed $value): string
{
    if ($value === null) {
        return '';
    }
    if (! is_string($value)) {
        $value = json_encode($value, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    }

    return preg_replace('/\s+/u', ' ', trim((string) $value));
}

function summarizeTourDecision(array $item): array
{
    return [
        'id' => $item['row']->id,
        'name' => $item['row']->name,
        'slug' => $item['row']->slug,
        'price_adult' => $item['row']->price_adult,
        'status_before' => $item['row']->status,
        'booking_availability_before' => $item['row']->booking_availability,
        'selection_score' => $item['score'],
        'relation_counts' => $item['relation_counts'],
    ];
}
