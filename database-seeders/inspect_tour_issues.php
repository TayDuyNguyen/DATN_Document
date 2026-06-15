<?php
// Bootstrap Laravel
require 'd:/DATN/danangtrip-api/vendor/autoload.php';
$app = require_once 'd:/DATN/danangtrip-api/bootstrap/app.php';
$kernel = $app->make(Illuminate\Contracts\Console\Kernel::class);
$kernel->bootstrap();

echo "=== INSPECTING DETAILED TOUR ISSUES (PHP FILTERING) ===\n\n";

$tours = DB::table('tours')->select('id', 'name', 'slug', 'inclusions', 'exclusions', 'meeting_point', 'duration')->get();

$emptyInclusions = [];
$emptyExclusions = [];
$emptyMeeting = [];

foreach ($tours as $t) {
    // Check inclusions
    $incVal = trim($t->inclusions);
    if (empty($incVal) || $incVal === '[]' || $incVal === '{}' || $incVal === 'null') {
        $emptyInclusions[] = $t;
    }
    
    // Check exclusions
    $excVal = trim($t->exclusions);
    if (empty($excVal) || $excVal === '[]' || $excVal === '{}' || $excVal === 'null') {
        $emptyExclusions[] = $t;
    }
    
    // Check meeting point
    $meetVal = trim($t->meeting_point);
    if (empty($meetVal) || $meetVal === 'null') {
        $emptyMeeting[] = $t;
    }
}

echo "Tours with empty inclusions (" . count($emptyInclusions) . "):\n";
foreach ($emptyInclusions as $t) {
    echo "  - ID {$t->id}: {$t->name} (slug: {$t->slug})\n";
}

echo "\nTours with empty exclusions (" . count($emptyExclusions) . "):\n";
foreach ($emptyExclusions as $t) {
    echo "  - ID {$t->id}: {$t->name} (slug: {$t->slug})\n";
}

echo "\nTours with empty meeting point (" . count($emptyMeeting) . "):\n";
foreach ($emptyMeeting as $t) {
    echo "  - ID {$t->id}: {$t->name} (slug: {$t->slug}, duration: {$t->duration})\n";
}
