<?php
// Bootstrap Laravel
require 'd:/DATN/danangtrip-api/vendor/autoload.php';
$app = require_once 'd:/DATN/danangtrip-api/bootstrap/app.php';
$kernel = $app->make(Illuminate\Contracts\Console\Kernel::class);
$kernel->bootstrap();

use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Artisan;

$v2Dir = "d:/DATN/DATN_Tài liệu/database-seeders/seeders_v2";
$locationsFile = "$v2Dir/demo/03_locations.sql";
$toursFile = "$v2Dir/demo/04_tours.sql";
$blogsFile = "$v2Dir/demo/05_blog_posts.sql";
$testFile = "$v2Dir/test/03_test_checkout.sql";
$chatOutFile = "$v2Dir/demo/09_chat_knowledge.sql";

// Helper for generic table dump
function dumpTableToSqlLocal($tableName, $query, $onConflict = '') {
    $rows = $query->get();
    if ($rows->isEmpty()) {
        return "-- No records in $tableName\n\n";
    }
    
    $columns = array_keys((array)$rows->first());
    $columnsList = implode(', ', array_map(fn($c) => "\"$c\"", $columns));
    
    $sql = "INSERT INTO \"$tableName\" ($columnsList) VALUES\n";
    $valueLines = [];
    foreach ($rows as $row) {
        $values = [];
        foreach ($columns as $col) {
            $val = $row->$col;
            if ($val === null) {
                $values[] = 'NULL';
            } elseif (is_bool($val)) {
                $values[] = $val ? 'true' : 'false';
            } elseif (is_int($val) || is_float($val)) {
                $values[] = $val;
            } else {
                $isJson = false;
                if (in_array($col, ['itinerary', 'inclusions', 'exclusions', 'images', 'opening_hours', 'metadata', 'headers', 'body', 'content_hash']) &&
                    (strpos($val, '[') === 0 || strpos($val, '{') === 0)) {
                    $isJson = true;
                }
                
                $escaped = str_replace("'", "''", $val);
                if ($isJson) {
                    $values[] = "'$escaped'::jsonb";
                } else {
                    $values[] = "'$escaped'";
                }
            }
        }
        $valueLines[] = "(" . implode(', ', $values) . ")";
    }
    $sql .= implode(",\n", $valueLines);
    if ($onConflict) {
        $sql .= "\n$onConflict;\n\n";
    } else {
        $sql .= ";\n\n";
    }
    return $sql;
}

try {
    DB::beginTransaction();
    echo "Transaction started.\n";
    
    // Truncate tables for a clean sync state inside the transaction
    echo "Truncating tours, locations and blog_posts inside transaction...\n";
    DB::unprepared("TRUNCATE TABLE tour_locations, tour_schedules, tours, locations, blog_post_categories, blog_posts, payments, booking_items, bookings CASCADE;");
    
    // Load static seeders
    $files = [$locationsFile, $toursFile, $blogsFile, $testFile];
    foreach ($files as $f) {
        if (file_exists($f)) {
            echo "Loading seeder: " . basename($f) . "...\n";
            $sql = file_get_contents($f);
            $sql = preg_replace('/^\s*BEGIN\s*;/i', '', $sql);
            $sql = preg_replace('/COMMIT\s*;\s*$/i', '', $sql);
            $sql = str_replace([
                'ALTER TABLE tours DISABLE TRIGGER ALL;',
                'ALTER TABLE tours ENABLE TRIGGER ALL;',
                'ALTER TABLE locations DISABLE TRIGGER ALL;',
                'ALTER TABLE locations ENABLE TRIGGER ALL;',
                'ALTER TABLE blog_posts DISABLE TRIGGER ALL;',
                'ALTER TABLE blog_posts ENABLE TRIGGER ALL;'
            ], '', $sql);
            DB::unprepared($sql);
        }
    }
    echo "All seeders loaded into transaction state.\n";
    
    // Run chatbot sync and embedding command
    echo "Running chatbot:sync-knowledge --embed ...\n";
    Artisan::call('chatbot:sync-knowledge', [
        '--embed' => true,
        '--force' => false // This ensures we only embed items with null embeddings (new/changed content)
    ]);
    echo Artisan::output();
    
    // Dump the updated chat_knowledge_base table to demo/09_chat_knowledge.sql
    echo "Exporting updated chatbot knowledge table to demo/09_chat_knowledge.sql...\n";
    $chatSql = "BEGIN;\n";
    $chatSql .= dumpTableToSqlLocal('chat_knowledge_base', DB::table('chat_knowledge_base')->orderBy('id'), "ON CONFLICT (id) DO NOTHING");
    $chatSql .= "SELECT setval(pg_get_serial_sequence('chat_knowledge_base', 'id'), GREATEST((SELECT COALESCE(MAX(id), 0) FROM chat_knowledge_base), 1), true);\n\n";
    $chatSql .= "COMMIT;\n";
    file_put_contents($chatOutFile, $chatSql);
    echo "Successfully updated demo/09_chat_knowledge.sql with new vector embeddings!\n";
    
} catch (Throwable $e) {
    echo "Error: " . $e->getMessage() . "\n";
    echo $e->getTraceAsString() . "\n";
} finally {
    DB::rollBack();
    echo "Transaction rolled back. Live database state is completely untouched.\n";
}
