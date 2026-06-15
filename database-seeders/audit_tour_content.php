<?php
// Bootstrap Laravel
require 'd:/DATN/danangtrip-api/vendor/autoload.php';
$app = require_once 'd:/DATN/danangtrip-api/bootstrap/app.php';
$kernel = $app->make(Illuminate\Contracts\Console\Kernel::class);
$kernel->bootstrap();

echo "==================================================\n";
echo "AUDITING TOUR CONTENT QUALITY & COMPLETENESS\n";
echo "==================================================\n\n";

$tours = DB::table('tours')->orderBy('id')->get();
$totalTours = count($tours);
echo "Total tours in database: $totalTours\n\n";

$issues = [
    'missing_desc' => [],
    'missing_short_desc' => [],
    'empty_itinerary' => [],
    'empty_inclusions' => [],
    'empty_exclusions' => [],
    'missing_start_time' => [],
    'missing_meeting_point' => [],
    'missing_duration' => [],
    'invalid_itinerary_json' => [],
    'invalid_inclusions_json' => [],
    'invalid_exclusions_json' => [],
    'missing_thumbnail' => [],
    'missing_images' => [],
    'invalid_images_json' => [],
    'zero_price_adult' => [],
    'english_or_placeholder_content' => []
];

foreach ($tours as $t) {
    $id = $t->id;
    $name = $t->name;
    
    // 1. Descriptions
    if (empty($t->description) || trim($t->description) === '') {
        $issues['missing_desc'][] = "$id: $name";
    }
    if (empty($t->short_desc) || trim($t->short_desc) === '') {
        $issues['missing_short_desc'][] = "$id: $name";
    }
    
    // 2. JSON Fields: Itinerary
    if (empty($t->itinerary) || $t->itinerary === '[]' || $t->itinerary === '{}') {
        $issues['empty_itinerary'][] = "$id: $name";
    } else {
        $decoded = json_decode($t->itinerary, true);
        if (json_last_error() !== JSON_ERROR_NONE) {
            $issues['invalid_itinerary_json'][] = "$id: $name (" . json_last_error_msg() . ")";
        }
    }
    
    // Inclusions
    if (empty($t->inclusions) || $t->inclusions === '[]' || $t->inclusions === '{}') {
        $issues['empty_inclusions'][] = "$id: $name";
    } else {
        $decoded = json_decode($t->inclusions, true);
        if (json_last_error() !== JSON_ERROR_NONE) {
            $issues['invalid_inclusions_json'][] = "$id: $name (" . json_last_error_msg() . ")";
        }
    }
    
    // Exclusions
    if (empty($t->exclusions) || $t->exclusions === '[]' || $t->exclusions === '{}') {
        $issues['empty_exclusions'][] = "$id: $name";
    } else {
        $decoded = json_decode($t->exclusions, true);
        if (json_last_error() !== JSON_ERROR_NONE) {
            $issues['invalid_exclusions_json'][] = "$id: $name (" . json_last_error_msg() . ")";
        }
    }
    
    // 3. Metadata
    if (empty($t->start_time)) {
        $issues['missing_start_time'][] = "$id: $name";
    }
    if (empty($t->meeting_point)) {
        $issues['missing_meeting_point'][] = "$id: $name";
    }
    if (empty($t->duration)) {
        $issues['missing_duration'][] = "$id: $name";
    }
    
    // 4. Images
    if (empty($t->thumbnail)) {
        $issues['missing_thumbnail'][] = "$id: $name";
    }
    if (empty($t->images) || $t->images === '[]') {
        $issues['missing_images'][] = "$id: $name";
    } else {
        $decoded = json_decode($t->images, true);
        if (json_last_error() !== JSON_ERROR_NONE) {
            $issues['invalid_images_json'][] = "$id: $name (" . json_last_error_msg() . ")";
        }
    }
    
    // 5. Prices
    if ($t->price_adult <= 0) {
        $issues['zero_price_adult'][] = "$id: $name (Price: {$t->price_adult})";
    }
    
    // 6. Language & Quality (check if description has placeholder English terms or is very short)
    if (!empty($t->description)) {
        // Detect english keywords or generic crawled descriptions like "Tour Da Nang, Ba Na Hills trong..."
        if (preg_match('/(tour.*hours.*tong hop tu nguon cong khai|website operator|source_url)/i', $t->description)) {
            $issues['english_or_placeholder_content'][] = "$id: $name (Has crawler review placeholders)";
        }
    }
}

// Print Report
echo "--- SUMMARY OF ISSUES ---\n";
foreach ($issues as $key => $list) {
    echo "  * " . strtoupper($key) . ": " . count($list) . " tours affected.\n";
}

echo "\n--- DETAILED AUDIT FINDINGS ---\n";

if (count($issues['english_or_placeholder_content']) > 0) {
    echo "\n⚠️ Tours with Crawler Placeholders/English Content (" . count($issues['english_or_placeholder_content']) . "):\n";
    foreach (array_slice($issues['english_or_placeholder_content'], 0, 15) as $item) {
        echo "   - $item\n";
    }
    if (count($issues['english_or_placeholder_content']) > 15) {
        echo "   ... and " . (count($issues['english_or_placeholder_content']) - 15) . " more tours.\n";
    }
}

if (count($issues['empty_itinerary']) > 0) {
    echo "\n⚠️ Tours with EMPTY Itinerary (" . count($issues['empty_itinerary']) . "):\n";
    foreach (array_slice($issues['empty_itinerary'], 0, 15) as $item) {
        echo "   - $item\n";
    }
    if (count($issues['empty_itinerary']) > 15) {
        echo "   ... and " . (count($issues['empty_itinerary']) - 15) . " more tours.\n";
    }
}

if (count($issues['empty_inclusions']) > 0) {
    echo "\n⚠️ Tours with EMPTY Inclusions (" . count($issues['empty_inclusions']) . "):\n";
    foreach (array_slice($issues['empty_inclusions'], 0, 15) as $item) {
        echo "   - $item\n";
    }
}

if (count($issues['missing_start_time']) > 0) {
    echo "\n⚠️ Tours with MISSING Start Time (" . count($issues['missing_start_time']) . "):\n";
    foreach (array_slice($issues['missing_start_time'], 0, 15) as $item) {
        echo "   - $item\n";
    }
}

if (count($issues['missing_meeting_point']) > 0) {
    echo "\n⚠️ Tours with MISSING Meeting Point (" . count($issues['missing_meeting_point']) . "):\n";
    foreach (array_slice($issues['missing_meeting_point'], 0, 15) as $item) {
        echo "   - $item\n";
    }
    if (count($issues['missing_meeting_point']) > 15) {
        echo "   ... and " . (count($issues['missing_meeting_point']) - 15) . " more tours.\n";
    }
}

if (count($issues['zero_price_adult']) > 0) {
    echo "\n⚠️ Tours with ZERO Price (" . count($issues['zero_price_adult']) . "):\n";
    foreach ($issues['zero_price_adult'] as $item) {
        echo "   - $item\n";
    }
}
