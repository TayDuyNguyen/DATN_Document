<?php

use Illuminate\Contracts\Console\Kernel;
use Illuminate\Support\Facades\DB;

$apiRoot = dirname(__DIR__, 2).DIRECTORY_SEPARATOR.'danangtrip-api';
require $apiRoot.DIRECTORY_SEPARATOR.'vendor'.DIRECTORY_SEPARATOR.'autoload.php';
$app = require $apiRoot.DIRECTORY_SEPARATOR.'bootstrap'.DIRECTORY_SEPARATOR.'app.php';
$app->make(Kernel::class)->bootstrap();

$apply = in_array('--apply', $argv, true);
$generatedAt = now();

$templateRows = DB::table('locations')
    ->where(function ($query): void {
        $query
            ->whereRaw("short_description ILIKE '%duoc thu thap tu OpenStreetMap%'")
            ->orWhereRaw("description ILIKE '%la diem du lieu du lich/dich vu%'");
    })
    ->orderBy('id')
    ->get();

$nameCorrections = [
    136 => 'Bảo tàng Quân khu 5',
    205 => 'Khách sạn Bốn Mùa',
    206 => 'Khách sạn Hải An',
    327 => 'Trung tâm Văn hóa - Thể thao quận Thanh Khê',
];

$addressReplacements = [
    'Ngu Hanh Son' => 'Ngũ Hành Sơn',
    'Trinh Cong Son' => 'Trịnh Công Sơn',
    'Luu Quang Vu' => 'Lưu Quang Vũ',
    'Nguyen Chi Thanh' => 'Nguyễn Chí Thanh',
    'Nguyen Duc' => 'Nguyễn Đức',
    'Ong Ich Khiem' => 'Ông Ích Khiêm',
    'Le Van Quy' => 'Lê Văn Quý',
    'An Don' => 'An Đồn',
    'Son Tra' => 'Sơn Trà',
    'Hai Chau' => 'Hải Châu',
    'Thanh Khe' => 'Thanh Khê',
    'Hoang Sa' => 'Hoàng Sa',
    'Da Nang' => 'Đà Nẵng',
    'Danang' => 'Đà Nẵng',
    'Duong ' => 'Đường ',
    'Quan ' => 'Quận ',
];

$rowsById = $templateRows->keyBy('id');
$extraIds = array_values(array_diff(array_keys($nameCorrections), $rowsById->keys()->all()));
if ($extraIds !== []) {
    $extraRows = DB::table('locations')->whereIn('id', $extraIds)->get();
    foreach ($extraRows as $row) {
        $rowsById->put($row->id, $row);
    }
}

$backupDirectory = dirname(__DIR__).DIRECTORY_SEPARATOR.'data-center'.DIRECTORY_SEPARATOR.'backups';
$reportDirectory = dirname(__DIR__).DIRECTORY_SEPARATOR.'data-center'.DIRECTORY_SEPARATOR.'reports';
foreach ([$backupDirectory, $reportDirectory] as $directory) {
    if (! is_dir($directory)) {
        mkdir($directory, 0777, true);
    }
}

$stamp = $generatedAt->format('Y-m-d-His');
$backupPath = $backupDirectory.DIRECTORY_SEPARATOR."locations-before-vietnamese-diacritics-{$stamp}.json";
$reportPath = $reportDirectory.DIRECTORY_SEPARATOR."location-vietnamese-diacritics-repair-{$stamp}.json";
$backupPayload = [
    'generated_at' => $generatedAt->toIso8601String(),
    'applied' => $apply,
    'rows' => $rowsById->values()->all(),
];
file_put_contents(
    $backupPath,
    json_encode($backupPayload, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE).PHP_EOL
);

$changes = [];
foreach ($rowsById as $row) {
    $newName = $nameCorrections[$row->id] ?? $row->name;
    $newAddress = normalizeAddress($row->address, $addressReplacements);
    $isTemplateRow = $templateRows->contains('id', $row->id);
    $newShortDescription = $row->short_description;
    $newDescription = $row->description;

    if ($isTemplateRow) {
        $newShortDescription = "{$newName} được thu thập từ OpenStreetMap và đang chờ biên tập. "
            .'Cần quản trị viên kiểm tra mô tả, hình ảnh và thông tin vận hành trước khi xuất bản.';
        $newDescription = "{$newName} là địa điểm du lịch hoặc dịch vụ tại Đà Nẵng, được thu thập "
            .'từ OpenStreetMap qua Overpass API. Bản ghi đang chờ duyệt và cần được kiểm tra nội dung, '
            .'hình ảnh, giờ mở cửa, giá và danh mục trước khi xuất bản trên DanangTrip.';
    }

    $updates = array_filter([
        'name' => $newName !== $row->name ? $newName : null,
        'address' => $newAddress !== $row->address ? $newAddress : null,
        'short_description' => $newShortDescription !== $row->short_description ? $newShortDescription : null,
        'description' => $newDescription !== $row->description ? $newDescription : null,
    ], static fn ($value): bool => $value !== null);

    if ($updates !== []) {
        $changes[] = [
            'id' => $row->id,
            'before' => [
                'name' => $row->name,
                'address' => $row->address,
                'short_description' => $row->short_description,
                'description' => $row->description,
            ],
            'after' => array_merge([
                'name' => $row->name,
                'address' => $row->address,
                'short_description' => $row->short_description,
                'description' => $row->description,
            ], $updates),
            'changed_columns' => array_keys($updates),
        ];
    }
}

if ($apply) {
    DB::transaction(static function () use ($changes): void {
        foreach ($changes as $change) {
            DB::table('locations')
                ->where('id', $change['id'])
                ->update(array_merge($change['after'], ['updated_at' => now()]));
        }
    });
}

$report = [
    'generated_at' => $generatedAt->toIso8601String(),
    'mode' => $apply ? 'apply' : 'dry-run',
    'backup_path' => $backupPath,
    'template_rows_found' => $templateRows->count(),
    'rows_changed' => count($changes),
    'changed_column_counts' => collect($changes)
        ->flatMap(static fn (array $change): array => $change['changed_columns'])
        ->countBy()
        ->all(),
    'changes' => $changes,
];
file_put_contents(
    $reportPath,
    json_encode($report, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE).PHP_EOL
);

echo json_encode([
    'mode' => $report['mode'],
    'template_rows_found' => $report['template_rows_found'],
    'rows_changed' => $report['rows_changed'],
    'changed_column_counts' => $report['changed_column_counts'],
    'backup_path' => $backupPath,
    'report_path' => $reportPath,
], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE).PHP_EOL;

function normalizeAddress(?string $address, array $replacements): ?string
{
    if ($address === null || trim($address) === '') {
        return $address;
    }

    return str_ireplace(array_keys($replacements), array_values($replacements), $address);
}
