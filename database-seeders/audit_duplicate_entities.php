<?php

use Illuminate\Contracts\Console\Kernel;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schema;

$apiRoot = dirname(__DIR__, 2).DIRECTORY_SEPARATOR.'danangtrip-api';
require $apiRoot.DIRECTORY_SEPARATOR.'vendor'.DIRECTORY_SEPARATOR.'autoload.php';
$app = require $apiRoot.DIRECTORY_SEPARATOR.'bootstrap'.DIRECTORY_SEPARATOR.'app.php';
$app->make(Kernel::class)->bootstrap();

$locations = DB::table('locations')
    ->select([
        'id', 'name', 'slug', 'address', 'district', 'latitude', 'longitude',
        'category_id', 'status', 'thumbnail', 'created_at',
    ])
    ->orderBy('id')
    ->get()
    ->all();
$tours = DB::table('tours')
    ->select([
        'id', 'name', 'slug', 'tour_category_id', 'duration', 'price_adult',
        'meeting_point', 'status', 'thumbnail', 'created_at', 'short_desc',
        'description', 'itinerary', 'inclusions', 'exclusions',
    ])
    ->orderBy('id')
    ->get()
    ->all();
$tourRelationTables = [
    'booking_items',
    'tour_schedules',
    'ratings',
    'favorites',
    'views',
    'cart_items',
    'tour_locations',
];
$tourRelationCounts = [];
foreach ($tourRelationTables as $table) {
    if (! Schema::hasTable($table) || ! Schema::hasColumn($table, 'tour_id')) {
        continue;
    }
    $tourRelationCounts[$table] = DB::table($table)
        ->whereNotNull('tour_id')
        ->selectRaw('tour_id, count(*) as aggregate')
        ->groupBy('tour_id')
        ->pluck('aggregate', 'tour_id')
        ->map(static fn ($count): int => (int) $count);
}
foreach ($tours as $tour) {
    $tour->content_fingerprint = hash('sha256', implode('|', [
        normalizeFingerprintValue($tour->short_desc),
        normalizeFingerprintValue($tour->description),
        normalizeFingerprintValue($tour->itinerary),
        normalizeFingerprintValue($tour->inclusions),
        normalizeFingerprintValue($tour->exclusions),
        normalizeFingerprintValue($tour->duration),
        normalizeFingerprintValue($tour->meeting_point),
    ]));
    $tour->relation_counts = [];
    foreach ($tourRelationCounts as $table => $counts) {
        $tour->relation_counts[$table] = $counts->get($tour->id, 0);
    }
}
$blogs = DB::table('blog_posts')
    ->select([
        'id', 'title', 'slug', 'excerpt', 'content', 'status', 'featured_image',
        'published_at', 'created_at',
    ])
    ->orderBy('id')
    ->get()
    ->all();
$blogCategoryIds = DB::table('blog_post_categories')
    ->select(['post_id', 'blog_category_id'])
    ->orderBy('post_id')
    ->get()
    ->groupBy('post_id')
    ->map(static fn ($rows): array => $rows->pluck('blog_category_id')->map(
        static fn ($id): int => (int) $id
    )->all());
foreach ($blogs as $blog) {
    $blog->category_ids = $blogCategoryIds->get($blog->id, []);
    $blog->excerpt_fingerprint = hash('sha256', normalizeFingerprintValue($blog->excerpt ?? ''));
    $blog->content_fingerprint = hash('sha256', normalizeFingerprintValue($blog->content ?? ''));
}

$locationPairs = compareLocations($locations);
$tourPairs = compareTours($tours);
$blogPairs = compareBlogs($blogs);

$report = [
    'generated_at' => now()->toIso8601String(),
    'thresholds' => [
        'location_high' => 'same normalized name, or <= 20 m with name similarity >= 0.80',
        'location_review' => '<= 80 m with name similarity >= 0.65, or same normalized address with similarity >= 0.65',
        'tour_high' => 'same normalized name',
        'tour_review' => 'name similarity >= 0.88 with matching category/duration/price signals',
        'blog_high' => 'same normalized title',
        'blog_review' => 'title similarity >= 0.90',
    ],
    'totals' => [
        'locations' => count($locations),
        'tours' => count($tours),
        'blog_posts' => count($blogs),
        'location_pairs' => count($locationPairs),
        'tour_pairs' => count($tourPairs),
        'blog_pairs' => count($blogPairs),
    ],
    'summary' => [
        'location_high' => countByConfidence($locationPairs, 'high'),
        'location_review' => countByConfidence($locationPairs, 'review'),
        'tour_high' => countByConfidence($tourPairs, 'high'),
        'tour_review' => countByConfidence($tourPairs, 'review'),
        'blog_high' => countByConfidence($blogPairs, 'high'),
        'blog_review' => countByConfidence($blogPairs, 'review'),
    ],
    'locations' => $locationPairs,
    'tours' => $tourPairs,
    'blog_posts' => $blogPairs,
    'policy' => [
        'automatic_merge' => false,
        'coordinates_alone_are_not_duplicate_proof' => true,
        'review_relations_before_delete' => true,
    ],
];

$reportDirectory = dirname(__DIR__).DIRECTORY_SEPARATOR.'data-center'.DIRECTORY_SEPARATOR.'reports';
if (! is_dir($reportDirectory)) {
    mkdir($reportDirectory, 0777, true);
}
$reportPath = $reportDirectory.DIRECTORY_SEPARATOR.'duplicate-entities-audit-'.now()->format('Y-m-d').'.json';
file_put_contents(
    $reportPath,
    json_encode($report, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES).PHP_EOL
);

echo json_encode([
    'report_path' => $reportPath,
    'totals' => $report['totals'],
    'summary' => $report['summary'],
], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE).PHP_EOL;

function compareLocations(array $rows): array
{
    $pairs = [];
    $count = count($rows);
    for ($i = 0; $i < $count; $i++) {
        for ($j = $i + 1; $j < $count; $j++) {
            $left = $rows[$i];
            $right = $rows[$j];
            $leftName = normalizeText($left->name);
            $rightName = normalizeText($right->name);
            $nameSimilarity = similarity($leftName, $rightName);
            $sameName = $leftName !== '' && $leftName === $rightName;
            $leftAddress = normalizeText($left->address);
            $rightAddress = normalizeText($right->address);
            $sameAddress = $leftAddress !== '' && $leftAddress === $rightAddress;
            $distance = haversineMeters(
                nullableFloat($left->latitude),
                nullableFloat($left->longitude),
                nullableFloat($right->latitude),
                nullableFloat($right->longitude)
            );

            $confidence = null;
            $reasons = [];
            if ($sameName) {
                $confidence = 'high';
                $reasons[] = 'same_normalized_name';
            }
            if ($distance !== null && $distance <= 20 && $nameSimilarity >= 0.80) {
                $confidence = 'high';
                $reasons[] = 'near_20m_similar_name';
            }
            if ($confidence === null && $distance !== null && $distance <= 80 && $nameSimilarity >= 0.65) {
                $confidence = 'review';
                $reasons[] = 'near_80m_similar_name';
            }
            if ($confidence === null && $sameAddress && $nameSimilarity >= 0.65) {
                $confidence = 'review';
                $reasons[] = 'same_address_similar_name';
            }
            if ($confidence === null) {
                continue;
            }

            $pairs[] = [
                'confidence' => $confidence,
                'reasons' => $reasons,
                'name_similarity' => round($nameSimilarity, 4),
                'distance_m' => $distance === null ? null : round($distance, 2),
                'same_category' => $left->category_id === $right->category_id,
                'left' => summarizeLocation($left),
                'right' => summarizeLocation($right),
            ];
        }
    }

    return sortPairs($pairs);
}

function compareTours(array $rows): array
{
    $pairs = [];
    $count = count($rows);
    for ($i = 0; $i < $count; $i++) {
        for ($j = $i + 1; $j < $count; $j++) {
            $left = $rows[$i];
            $right = $rows[$j];
            $leftName = normalizeText($left->name);
            $rightName = normalizeText($right->name);
            $nameSimilarity = similarity($leftName, $rightName);
            $sameName = $leftName !== '' && $leftName === $rightName;
            $sameCategory = $left->tour_category_id === $right->tour_category_id;
            $sameDuration = normalizeText($left->duration) === normalizeText($right->duration);
            $priceRatio = priceRatio($left->price_adult, $right->price_adult);
            $sameContent = $left->content_fingerprint === $right->content_fingerprint;

            $confidence = null;
            $reasons = [];
            if ($sameName) {
                $confidence = 'high';
                $reasons[] = 'same_normalized_name';
            } elseif (
                $nameSimilarity >= 0.88
                && $sameCategory
                && ($sameDuration || $priceRatio >= 0.90)
            ) {
                $confidence = 'review';
                $reasons[] = 'similar_name_matching_product_signals';
            }
            if ($confidence === null) {
                continue;
            }

            $pairs[] = [
                'confidence' => $confidence,
                'reasons' => $reasons,
                'name_similarity' => round($nameSimilarity, 4),
                'same_category' => $sameCategory,
                'same_duration' => $sameDuration,
                'same_content' => $sameContent,
                'price_ratio' => round($priceRatio, 4),
                'left' => summarizeTour($left),
                'right' => summarizeTour($right),
            ];
        }
    }

    return sortPairs($pairs);
}

function compareBlogs(array $rows): array
{
    $pairs = [];
    $count = count($rows);
    for ($i = 0; $i < $count; $i++) {
        for ($j = $i + 1; $j < $count; $j++) {
            $left = $rows[$i];
            $right = $rows[$j];
            $leftTitle = normalizeText($left->title);
            $rightTitle = normalizeText($right->title);
            $titleSimilarity = similarity($leftTitle, $rightTitle);
            $sameTitle = $leftTitle !== '' && $leftTitle === $rightTitle;

            if (! $sameTitle && $titleSimilarity < 0.90) {
                continue;
            }
            $pairs[] = [
                'confidence' => $sameTitle ? 'high' : 'review',
                'reasons' => [$sameTitle ? 'same_normalized_title' : 'similar_title'],
                'title_similarity' => round($titleSimilarity, 4),
                'shared_category' => array_intersect($left->category_ids, $right->category_ids) !== [],
                'same_excerpt' => $left->excerpt_fingerprint === $right->excerpt_fingerprint,
                'same_content' => $left->content_fingerprint === $right->content_fingerprint,
                'left' => summarizeBlog($left),
                'right' => summarizeBlog($right),
            ];
        }
    }

    return sortPairs($pairs);
}

function normalizeText(?string $value): string
{
    $value = mb_strtolower(trim((string) $value), 'UTF-8');
    $ascii = iconv('UTF-8', 'ASCII//TRANSLIT//IGNORE', $value);
    $ascii = $ascii === false ? $value : $ascii;
    $ascii = preg_replace('/[^a-z0-9]+/', ' ', strtolower($ascii));

    return trim(preg_replace('/\s+/', ' ', $ascii));
}

function similarity(string $left, string $right): float
{
    if ($left === '' || $right === '') {
        return 0.0;
    }
    if ($left === $right) {
        return 1.0;
    }
    $maxLength = max(strlen($left), strlen($right));
    if ($maxLength === 0) {
        return 1.0;
    }

    return max(0.0, 1.0 - (levenshtein($left, $right) / $maxLength));
}

function haversineMeters(?float $lat1, ?float $lng1, ?float $lat2, ?float $lng2): ?float
{
    if ($lat1 === null || $lng1 === null || $lat2 === null || $lng2 === null) {
        return null;
    }
    $earthRadius = 6371000.0;
    $latDelta = deg2rad($lat2 - $lat1);
    $lngDelta = deg2rad($lng2 - $lng1);
    $a = sin($latDelta / 2) ** 2
        + cos(deg2rad($lat1)) * cos(deg2rad($lat2)) * sin($lngDelta / 2) ** 2;

    return $earthRadius * 2 * atan2(sqrt($a), sqrt(1 - $a));
}

function nullableFloat(mixed $value): ?float
{
    return $value === null || $value === '' ? null : (float) $value;
}

function priceRatio(mixed $left, mixed $right): float
{
    $left = (float) $left;
    $right = (float) $right;
    if ($left <= 0 || $right <= 0) {
        return 0.0;
    }

    return min($left, $right) / max($left, $right);
}

function summarizeLocation(object $row): array
{
    return [
        'id' => $row->id,
        'name' => $row->name,
        'slug' => $row->slug,
        'address' => $row->address,
        'district' => $row->district,
        'latitude' => $row->latitude,
        'longitude' => $row->longitude,
        'category_id' => $row->category_id,
        'status' => $row->status,
        'has_thumbnail' => $row->thumbnail !== null && $row->thumbnail !== '',
    ];
}

function summarizeTour(object $row): array
{
    return [
        'id' => $row->id,
        'name' => $row->name,
        'slug' => $row->slug,
        'tour_category_id' => $row->tour_category_id,
        'duration' => $row->duration,
        'price_adult' => $row->price_adult,
        'meeting_point' => $row->meeting_point,
        'status' => $row->status,
        'has_thumbnail' => $row->thumbnail !== null && $row->thumbnail !== '',
        'relation_counts' => $row->relation_counts,
    ];
}

function summarizeBlog(object $row): array
{
    return [
        'id' => $row->id,
        'title' => $row->title,
        'slug' => $row->slug,
        'category_ids' => $row->category_ids,
        'status' => $row->status,
        'has_featured_image' => $row->featured_image !== null && $row->featured_image !== '',
        'published_at' => $row->published_at,
    ];
}

function sortPairs(array $pairs): array
{
    usort($pairs, static function (array $left, array $right): int {
        $confidenceOrder = ['high' => 0, 'review' => 1];
        $confidenceCompare = ($confidenceOrder[$left['confidence']] ?? 9)
            <=> ($confidenceOrder[$right['confidence']] ?? 9);
        if ($confidenceCompare !== 0) {
            return $confidenceCompare;
        }
        $leftScore = $left['name_similarity'] ?? $left['title_similarity'] ?? 0;
        $rightScore = $right['name_similarity'] ?? $right['title_similarity'] ?? 0;

        return $rightScore <=> $leftScore;
    });

    return $pairs;
}

function countByConfidence(array $pairs, string $confidence): int
{
    return count(array_filter(
        $pairs,
        static fn (array $pair): bool => $pair['confidence'] === $confidence
    ));
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
