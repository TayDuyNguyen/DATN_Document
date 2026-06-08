<?php

$reportDir = 'D:/DATN/DATN_Tài liệu/data-center/reports';
if (! is_dir($reportDir)) {
    mkdir($reportDir, 0777, true);
}

$vietnameseAccentPattern = '/[ăâđêôơưáàảãạắằẳẵặấầẩẫậéèẻẽẹếềểễệíìỉĩịóòỏõọốồổỗộớờởỡợúùủũụứừửữựýỳỷỹỵĂÂĐÊÔƠƯÁÀẢÃẠẮẰẲẴẶẤẦẨẪẬÉÈẺẼẸẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌỐỒỔỖỘỚỜỞỠỢÚÙỦŨỤỨỪỬỮỰÝỲỶỸỴ]/u';
$unaccentedVietnamesePattern = '/\b(da nang|hoi an|hue|du lich|am thuc|dia diem|kinh nghiem|cam nang|lich trinh|van hoa|khach san|nha hang|bai bien|tour|chuyen di|tham quan|di chuyen|nghi duong|gia dinh|huong dan|mien trung|ngu hanh son|son tra|ba na|hai van|my son)\b/iu';
$englishPattern = '/\b(the|and|or|why|how|best|guide|travel|traveler|travelling|trip|tour|tours|city|beach|bridge|mountain|mountains|village|food|cafe|hotel|resort|local|from|with|what|where|when|day|days|perfect|ultimate|things|visit|visiting|destination|itinerary|experience|experiences|culture|history|central|vietnam)\b/i';

$configs = [
    'categories' => ['columns' => ['name', 'description'], 'status_column' => 'status'],
    'subcategories' => ['columns' => ['name', 'description'], 'status_column' => 'status'],
    'tags' => ['columns' => ['name']],
    'amenities' => ['columns' => ['name', 'category']],
    'tour_categories' => ['columns' => ['name', 'description'], 'status_column' => 'status'],
    'blog_categories' => ['columns' => ['name', 'description']],
    'locations' => ['columns' => ['name', 'description', 'short_description', 'address', 'district', 'ward'], 'status_column' => 'status'],
    'tours' => ['columns' => ['name', 'description', 'short_desc', 'duration', 'meeting_point', 'itinerary', 'inclusions', 'exclusions'], 'status_column' => 'status'],
    'blog_posts' => ['columns' => ['title', 'excerpt', 'content'], 'status_column' => 'status'],
    'landing_pages' => ['columns' => ['title', 'intro', 'seo_title', 'seo_description', 'content_blocks'], 'status_column' => 'status'],
    'promotions' => ['columns' => ['name', 'description'], 'status_column' => 'status'],
    'ratings' => ['columns' => ['comment'], 'status_column' => 'status'],
];

$normalizeText = static function ($value): string {
    if ($value === null) {
        return '';
    }

    if (is_array($value) || is_object($value)) {
        return json_encode($value, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES) ?: '';
    }

    $text = (string) $value;
    $decoded = json_decode($text, true);
    if (json_last_error() === JSON_ERROR_NONE && (is_array($decoded) || is_object($decoded))) {
        return json_encode($decoded, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES) ?: $text;
    }

    return $text;
};

$isMostlyUrlOrCode = static function (string $text): bool {
    $trimmed = trim($text);
    if ($trimmed === '') {
        return true;
    }

    if (preg_match('/^https?:\/\//i', $trimmed)) {
        return true;
    }

    if (preg_match('/^[a-z0-9_\-\/:.#?=&]+$/i', $trimmed) && ! preg_match('/\s/', $trimmed)) {
        return true;
    }

    return false;
};

$findings = [];
$scannedRows = 0;
$scannedFields = 0;

foreach ($configs as $table => $config) {
    if (! Schema::hasTable($table)) {
        continue;
    }

    $columns = array_values(array_filter($config['columns'], static fn ($column) => Schema::hasColumn($table, $column)));
    if ($columns === []) {
        continue;
    }

    $idColumn = Schema::hasColumn($table, 'id') ? 'id' : null;
    $statusColumn = $config['status_column'] ?? null;
    $select = array_merge($idColumn ? [$idColumn] : [], $statusColumn && Schema::hasColumn($table, $statusColumn) ? [$statusColumn] : [], $columns);

    DB::table($table)
        ->select($select)
        ->orderBy($idColumn ?: $columns[0])
        ->chunk(200, function ($rows) use (&$findings, &$scannedRows, &$scannedFields, $table, $columns, $idColumn, $statusColumn, $normalizeText, $isMostlyUrlOrCode, $vietnameseAccentPattern, $unaccentedVietnamesePattern, $englishPattern): void {
            foreach ($rows as $row) {
                $scannedRows++;
                foreach ($columns as $column) {
                    $text = $normalizeText($row->{$column} ?? null);
                    $clean = trim(preg_replace('/\s+/u', ' ', strip_tags($text)));

                    if ($clean === '' || $isMostlyUrlOrCode($clean)) {
                        continue;
                    }

                    $scannedFields++;
                    $wordCount = preg_match_all('/[\p{L}\p{N}]+/u', $clean);
                    $hasAccent = preg_match($vietnameseAccentPattern, $clean) === 1;
                    $hasUnaccentedVietnamese = preg_match($unaccentedVietnamesePattern, $clean) === 1;
                    $hasEnglishSignal = preg_match($englishPattern, $clean) === 1;
                    $isLocationBrandName = $table === 'locations' && $column === 'name';

                    $reason = null;
                    if ($isLocationBrandName) {
                        // Location names may be official international brands. The dedicated
                        // detailed location audit checks unaccented Vietnamese place names.
                        $reason = null;
                    } elseif ($hasUnaccentedVietnamese && ! $hasAccent) {
                        $reason = 'unaccented_vietnamese';
                    } elseif ($wordCount >= 4 && $hasEnglishSignal && ! $hasAccent) {
                        $reason = 'english_or_non_vietnamese';
                    } elseif ($wordCount >= 8 && ! $hasAccent) {
                        $reason = 'long_text_without_vietnamese_accents';
                    }

                    if ($reason !== null) {
                        $findings[] = [
                            'table' => $table,
                            'id' => $idColumn ? $row->{$idColumn} : null,
                            'status' => $statusColumn && isset($row->{$statusColumn}) ? $row->{$statusColumn} : null,
                            'column' => $column,
                            'reason' => $reason,
                            'sample' => mb_substr($clean, 0, 240),
                        ];
                    }
                }
            }
        });
}

$summary = [
    'generated_at' => now()->toIso8601String(),
    'rows_scanned' => $scannedRows,
    'fields_scanned' => $scannedFields,
    'findings_total' => count($findings),
    'by_table' => collect($findings)->groupBy('table')->map->count()->all(),
    'by_reason' => collect($findings)->groupBy('reason')->map->count()->all(),
    'findings' => $findings,
];

$reportPath = $reportDir.'/public-vietnamese-content-audit-'.now()->format('Y-m-d-His').'.json';
file_put_contents($reportPath, json_encode($summary, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES));

echo json_encode([
    'report_path' => $reportPath,
    'rows_scanned' => $summary['rows_scanned'],
    'fields_scanned' => $summary['fields_scanned'],
    'findings_total' => $summary['findings_total'],
    'by_table' => $summary['by_table'],
    'by_reason' => $summary['by_reason'],
], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
