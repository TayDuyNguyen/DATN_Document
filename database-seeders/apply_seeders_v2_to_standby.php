<?php
// Bootstrap Laravel
require 'd:/DATN/danangtrip-api/vendor/autoload.php';
$app = require_once 'd:/DATN/danangtrip-api/bootstrap/app.php';
$kernel = $app->make(Illuminate\Contracts\Console\Kernel::class);
$kernel->bootstrap();

use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Artisan;
use Illuminate\Support\Facades\Schema;

$v2Dir = "d:/DATN/DATN_Tài liệu/database-seeders/seeders_v2";

$allFiles = [
    // LAYER 1: BASE SYSTEM TABLES
    "base/01_categories.sql",
    "base/02_subcategories.sql",
    "base/03_tags.sql",
    "base/04_amenities.sql",
    "base/05_tour_categories.sql",
    "base/06_blog_categories.sql",
    "base/07_system_settings.sql",
    "base/08_admin_users.sql",
    "base/09_point_rules.sql",
    "base/10_landing_pages.sql",

    // LAYER 2: DEMO DATA (PART 1)
    "demo/01_demo_users.sql",
    "demo/02_promotions.sql",
    "demo/03_locations.sql",
    "demo/04_tours.sql",
    "demo/05_blog_posts.sql",
    "demo/06_bookings.sql",
    "demo/07_ratings.sql",

    // LAYER 3: TEST CHECKOUT (Contains User 101, required for notifications and cart)
    "test/03_test_checkout.sql",

    // LAYER 4: DEMO DATA (PART 2)
    "demo/08_notifications_activity.sql",
    "demo/09_chat_knowledge.sql",

    // LAYER 5: TEST DATA
    "test/01_test_cart.sql"
];

try {
    echo "=== Current active DB configuration ===\n";
    echo "Host: " . config('database.connections.pgsql.host') . "\n";
    echo "Database: " . config('database.connections.pgsql.database') . "\n";
    echo "Username: " . config('database.connections.pgsql.username') . "\n";
    echo "========================================\n\n";

    if (strpos(config('database.connections.pgsql.host'), 'aws-1-ap-southeast-1.pooler.supabase.com') === false) {
        throw new Exception("Error: Active host is NOT the Standby Backup database (Singapore pooler). Please double check .env!");
    }

    echo "Running migrate:fresh on Standby Backup Database...\n";
    Artisan::call('migrate:fresh', ['--force' => true]);
    echo Artisan::output() . "\n";

    echo "Start importing seeders_v2 SQL files...\n";
    
    foreach ($allFiles as $file) {
        $path = "$v2Dir/$file";
        if (file_exists($path)) {
            echo "Importing $file...\n";
            $sql = file_get_contents($path);
            $sql = str_replace([
                'ALTER TABLE tours DISABLE TRIGGER ALL;',
                'ALTER TABLE tours ENABLE TRIGGER ALL;',
                'ALTER TABLE locations DISABLE TRIGGER ALL;',
                'ALTER TABLE locations ENABLE TRIGGER ALL;',
                'ALTER TABLE blog_posts DISABLE TRIGGER ALL;',
                'ALTER TABLE blog_posts ENABLE TRIGGER ALL;',
                'ALTER TABLE "tours" DISABLE TRIGGER ALL;',
                'ALTER TABLE "tours" ENABLE TRIGGER ALL;',
                'ALTER TABLE "locations" DISABLE TRIGGER ALL;',
                'ALTER TABLE "locations" ENABLE TRIGGER ALL;',
                'ALTER TABLE "blog_posts" DISABLE TRIGGER ALL;',
                'ALTER TABLE "blog_posts" ENABLE TRIGGER ALL;'
            ], '', $sql);
            DB::unprepared($sql);
        } else {
            throw new Exception("File not found: $path");
        }
    }

    echo "\nResetting database sequences...\n";
    $resetPath = "d:/DATN/DATN_Tài liệu/database-seeders/67_reset_all_postgres_sequences.sql";
    if (file_exists($resetPath)) {
        DB::unprepared(file_get_contents($resetPath));
        echo "Sequences reset successfully.\n";
    }

    echo "\n=== Standby Backup Database updated successfully with seeders_v2! ===\n";

} catch (Throwable $e) {
    echo "\nERROR: " . $e->getMessage() . "\n";
    echo $e->getTraceAsString() . "\n";
}
