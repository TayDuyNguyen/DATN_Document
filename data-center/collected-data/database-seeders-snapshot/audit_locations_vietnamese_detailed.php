<?php

$reportDir = 'D:/DATN/DATN_Tài liệu/data-center/reports';
if (! is_dir($reportDir)) {
    mkdir($reportDir, 0777, true);
}

$columns = [
    'name',
    'description',
    'short_description',
    'address',
    'district',
    'ward',
    'opening_hours',
];

$phrasePatterns = [
    'an hai bac',
    'an hai dong',
    'an hai tay',
    'ba na',
    'bai bien',
    'ban dao',
    'cam le',
    'cau rong',
    'cham museum',
    'chau thi vinh te',
    'cho han',
    'cho con',
    'cong vien',
    'cu lao cham',
    'da nang',
    'dac san',
    'dia chi',
    'dia diem',
    'dich vu',
    'du lich',
    'duong bach dang',
    'duong tran phu',
    'duy xuyen',
    'gio mo cua',
    'hai chau',
    'hai van',
    'hoa cuong',
    'hoa hai',
    'hoa khanh',
    'hoa minh',
    'hoa vang',
    'hoang van thu',
    'hoi an',
    'khach san',
    'kham pha',
    'khu du lich',
    'khu vui choi',
    'lien chieu',
    'ly nam de',
    'luu tru',
    'my an',
    'my khe',
    'my son',
    'ngu hanh son',
    'nguyen huu tho',
    'nguyen tri phuong',
    'ngo quyen',
    'nha hang',
    'noi tieng',
    'phu hop',
    'phuong an hai',
    'quan an',
    'son tra',
    'thanh khe',
    'thanh pho',
    'thang binh',
    'thong tin',
    'thua thien hue',
    'trai nghiem',
    'trung tam',
    'truong sa',
    'viet nam',
];

$wordPatterns = [
    'am thuc',
    'can duoc',
    'can kiem duyet',
    'cho du khach',
    'dang cho',
    'di chuyen',
    'diem den',
    'duoc biet den',
    'duoc thu thap',
    'duoc tong hop',
    'gan khu vuc',
    'khach tham quan',
    'khong gian',
    'nguon cong khai',
    'tai da nang',
    'tai hoi an',
    'tai hue',
    'thoi gian',
    'thuong hieu',
    'tien ich',
    'van hoa',
];

$normalize = static function ($value): string {
    if ($value === null) {
        return '';
    }

    if (is_array($value) || is_object($value)) {
        return json_encode($value, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES) ?: '';
    }

    $text = (string) $value;
    $decoded = json_decode($text, true);
    if (json_last_error() === JSON_ERROR_NONE && is_array($decoded)) {
        return json_encode($decoded, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES) ?: $text;
    }

    return $text;
};

$findMatches = static function (string $text, array $patterns): array {
    $matches = [];
    foreach ($patterns as $pattern) {
        if (preg_match('/(?<![a-z])'.preg_quote($pattern, '/').'(?![a-z])/iu', $text) === 1) {
            $matches[] = $pattern;
        }
    }

    return $matches;
};

$rows = DB::table('locations')
    ->select(array_merge(['id', 'status', 'slug'], $columns))
    ->orderBy('id')
    ->get();

$findings = [];
$byColumn = [];
$byStatus = [];
$brandOrForeignNames = [];

foreach ($rows as $row) {
    foreach ($columns as $column) {
        $text = trim(preg_replace('/\s+/u', ' ', strip_tags($normalize($row->{$column} ?? null))));
        if ($text === '') {
            continue;
        }

        $lower = mb_strtolower($text);
        $matches = array_values(array_unique(array_merge(
            $findMatches($lower, $phrasePatterns),
            $findMatches($lower, $wordPatterns)
        )));

        $asciiWords = [];
        preg_match_all('/(?<![\p{L}])[a-z]{3,}(?![\p{L}])/u', $lower, $asciiWordMatches);
        foreach ($asciiWordMatches[0] ?? [] as $word) {
            if (in_array($word, [
                'the', 'and', 'hotel', 'resort', 'hostel', 'homestay', 'cafe', 'coffee',
                'restaurant', 'spa', 'center', 'centre', 'club', 'lounge', 'house',
                'beach', 'park', 'garden', 'villa', 'museum', 'market', 'mall',
                'street', 'road', 'city', 'vietnam', 'danang',
            ], true)) {
                $asciiWords[] = $word;
            }
        }

        if ($column === 'name' && $asciiWords !== []) {
            $brandOrForeignNames[] = [
                'id' => $row->id,
                'status' => $row->status,
                'slug' => $row->slug,
                'value' => $text,
                'signals' => array_values(array_unique($asciiWords)),
            ];
        }

        if ($matches === []) {
            continue;
        }

        $finding = [
            'id' => $row->id,
            'status' => $row->status,
            'slug' => $row->slug,
            'column' => $column,
            'matched_unaccented_phrases' => $matches,
            'english_or_ascii_place_words' => array_values(array_unique($asciiWords)),
            'value' => $text,
        ];
        $findings[] = $finding;
        $byColumn[$column] = ($byColumn[$column] ?? 0) + 1;
        $byStatus[$row->status] = ($byStatus[$row->status] ?? 0) + 1;
    }
}

$report = [
    'generated_at' => now()->toIso8601String(),
    'rows_scanned' => $rows->count(),
    'columns_scanned' => $columns,
    'findings_total' => count($findings),
    'by_column' => $byColumn,
    'by_status' => $byStatus,
    'brand_or_foreign_names_total' => count($brandOrForeignNames),
    'brand_or_foreign_names' => $brandOrForeignNames,
    'findings' => $findings,
];

$reportPath = $reportDir.'/locations-vietnamese-detailed-audit-'.now()->format('Y-m-d-His').'.json';
file_put_contents(
    $reportPath,
    json_encode($report, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES)
);

echo json_encode([
    'report_path' => $reportPath,
    'rows_scanned' => $report['rows_scanned'],
    'findings_total' => $report['findings_total'],
    'by_column' => $report['by_column'],
    'by_status' => $report['by_status'],
    'brand_or_foreign_names_total' => $report['brand_or_foreign_names_total'],
], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
