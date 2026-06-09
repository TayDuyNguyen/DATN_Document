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
    'ratings' => ['comment'],
    'search_logs' => ['query'],
];

$phrases = [
    'dac san hoi an',
    'duoc thu thap',
    'duoc tong hop',
    'dia diem check in da nang',
    'can duyet',
    'du lieu nay',
    'diem du lich',
    'dich vu',
    'gio mo cua',
    'huong dan',
    'kham pha',
    'khach san',
    'lich trinh',
    'le hoi phao hoa da nang',
    'mien trung',
    'noi dung',
    'quan an ngon hue',
    'thanh pho',
    'tham quan',
    'thoi gian rong phun lua',
    'thong tin',
    'tour ba na hills',
    'tour cu lao cham gia re',
    'tour mien trung',
    'trai nghiem',
    've cap treo ba na',
];

$tokens = array_flip([
    'an', 'ba', 'bao', 'ban', 'bien', 'bieu', 'can', 'cang', 'cap', 'cham',
    'check', 'chieu', 'chi', 'chon', 'chuyen', 'cong', 'cua', 'danh', 'dat',
    'dich', 'diem', 'dieu', 'doi', 'don',
    'du', 'dua', 'duoc', 'duong', 'gia', 'gio', 'gioi', 'gom', 'hanh', 'hoat',
    'hoi', 'hue', 'huong', 'khach', 'kham', 'khong', 'khu', 'lich', 'lieu',
    'luu', 'mien', 'mo', 'mua', 'na', 'ngam', 'ngay', 'nghiem', 'nguoi',
    'nguon', 'noi', 'phao', 'phong', 'phun', 'quan', 'quy', 're', 'rong',
    'san', 'thanh', 'tham', 'thoi', 'thong', 'thu', 'tieng', 'tinh', 'tong',
    'tour', 'trai', 'treo', 'trinh', 'trong', 'tu', 'van', 've', 'viet',
    'voi', 'vu',
]);

$hasVietnameseDiacritics = static fn (string $value): bool =>
    preg_match(
        '/[ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠƯ'
        .'àáâãèéêìíòóôõùúăđĩũơư'
        .'ẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀẾỂỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪỬỮỰỲỴỶỸÝ'
        .'ạảấầẩẫậắằẳẵặẹẻẽềếểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹý]/u',
        $value
    ) === 1;

$looksUnaccentedVietnamese = static function (string $value) use (
    $phrases,
    $tokens,
    $hasVietnameseDiacritics
): bool {
    if ($hasVietnameseDiacritics($value)) {
        return false;
    }
    $lower = mb_strtolower($value);
    foreach ($phrases as $phrase) {
        if (str_contains($lower, $phrase)) {
            return true;
        }
    }
    preg_match_all('/[a-z]+/', $lower, $matches);
    $words = $matches[0] ?? [];
    if ($words === []) {
        return false;
    }
    $score = count(array_filter($words, static fn (string $word): bool => isset($tokens[$word])));

    return $score >= 3 && ($score / count($words)) >= 0.18;
};

$output = [
    'generated_at' => now()->toIso8601String(),
    'tables' => [],
    'totals' => [
        'rows_scanned' => 0,
        'rows_with_unaccented_vietnamese' => 0,
        'field_values_unaccented' => 0,
        'field_values_accented' => 0,
    ],
    'examples' => [],
    'examples_by_column' => [],
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
    $tableResult = [
        'rows_scanned' => $rows->count(),
        'rows_with_unaccented_vietnamese' => 0,
        'field_values_unaccented' => 0,
        'field_values_accented' => 0,
        'by_column' => [],
    ];

    foreach ($rows as $row) {
        $rowHasIssue = false;
        foreach ($columns as $column) {
            $rawValue = $row->{$column};
            if ($rawValue === null || $rawValue === '') {
                continue;
            }
            $value = is_string($rawValue) ? $rawValue : json_encode($rawValue, JSON_UNESCAPED_UNICODE);
            if ($value === false) {
                continue;
            }
            $tableResult['by_column'][$column] ??= [
                'unaccented' => 0,
                'accented' => 0,
            ];
            if ($looksUnaccentedVietnamese($value)) {
                $rowHasIssue = true;
                $tableResult['field_values_unaccented']++;
                $tableResult['by_column'][$column]['unaccented']++;
                $columnKey = $table.'.'.$column;
                $output['examples_by_column'][$columnKey] ??= [];
                if (count($output['examples_by_column'][$columnKey]) < 20) {
                    $output['examples_by_column'][$columnKey][] = [
                        'id' => $row->id,
                        'value' => mb_substr(preg_replace('/\s+/u', ' ', $value), 0, 500),
                    ];
                }
                if (count($output['examples']) < 200) {
                    $output['examples'][] = [
                        'table' => $table,
                        'id' => $row->id,
                        'column' => $column,
                        'value' => mb_substr(preg_replace('/\s+/u', ' ', $value), 0, 500),
                    ];
                }
            } elseif ($hasVietnameseDiacritics($value)) {
                $tableResult['field_values_accented']++;
                $tableResult['by_column'][$column]['accented']++;
            }
        }
        if ($rowHasIssue) {
            $tableResult['rows_with_unaccented_vietnamese']++;
        }
    }

    $output['tables'][$table] = $tableResult;
    $output['totals']['rows_scanned'] += $tableResult['rows_scanned'];
    $output['totals']['rows_with_unaccented_vietnamese'] += $tableResult['rows_with_unaccented_vietnamese'];
    $output['totals']['field_values_unaccented'] += $tableResult['field_values_unaccented'];
    $output['totals']['field_values_accented'] += $tableResult['field_values_accented'];
}

$json = json_encode($output, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
$reportDirectory = dirname(__DIR__).DIRECTORY_SEPARATOR.'data-center'.DIRECTORY_SEPARATOR.'reports';
if (! is_dir($reportDirectory)) {
    mkdir($reportDirectory, 0777, true);
}
$reportPath = $reportDirectory.DIRECTORY_SEPARATOR.'vietnamese-diacritics-db-audit-'.now()->format('Y-m-d').'.json';
file_put_contents($reportPath, $json.PHP_EOL);

echo json_encode([
    'report_path' => $reportPath,
    'generated_at' => $output['generated_at'],
    'totals' => $output['totals'],
    'tables' => $output['tables'],
], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE).PHP_EOL;
