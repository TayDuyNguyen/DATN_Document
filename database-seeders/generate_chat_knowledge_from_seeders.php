<?php
/**
 * generate_chat_knowledge_from_seeders.php
 *
 * Load dữ liệu từ seeder files (165 tours, 112 locations, 118 blogs)
 * vào transaction tạm thời, chạy chatbot:sync-knowledge --embed để tạo vectors,
 * export ra demo/09_chat_knowledge.sql, rồi ROLLBACK (không đụng DB thật).
 *
 * Sau đó apply file SQL lên server.
 */

require 'd:/DATN/danangtrip-api/vendor/autoload.php';
$app = require_once 'd:/DATN/danangtrip-api/bootstrap/app.php';
$kernel = $app->make(Illuminate\Contracts\Console\Kernel::class);
$kernel->bootstrap();

use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Artisan;

$v2Dir = "d:/DATN/DATN_Tài liệu/database-seeders/seeders_v2";
$chatOutFile = "$v2Dir/demo/09_chat_knowledge.sql";

// Seeder files chứa toàn bộ dữ liệu (165 tours, 112 locations, 118 blogs)
$seederFiles = [
    "$v2Dir/demo/03_locations.sql",
    "$v2Dir/demo/04_tours.sql",
    "$v2Dir/demo/05_blog_posts.sql",
];

echo "=== GENERATE CHAT KNOWLEDGE FROM SEEDERS V2 ===\n";
echo "Host: " . config('database.connections.pgsql.host') . "\n";
echo "Seeder files:\n";
foreach ($seederFiles as $f) {
    $size = file_exists($f) ? round(filesize($f)/1024, 0) . " KB" : "NOT FOUND";
    echo "  " . basename($f) . " ($size)\n";
}
echo "================================================\n\n";

// Helper để load SQL file, strip BEGIN/COMMIT/TRIGGER statements
function loadSqlFile($path) {
    $sql = file_get_contents($path);
    $sql = preg_replace('/^\s*BEGIN\s*;/im', '', $sql);
    $sql = preg_replace('/COMMIT\s*;\s*$/im', '', $sql);
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
        'ALTER TABLE "blog_posts" ENABLE TRIGGER ALL;',
    ], '', $sql);
    return $sql;
}

// Helper export bảng sang SQL
function dumpTableToSql($tableName, $rows, $onConflict = '') {
    if ($rows->isEmpty()) return "-- No records in $tableName\n\n";

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
                // JSONB: metadata
                $jsonbCols = ['metadata'];
                $escaped = str_replace("'", "''", $val);
                if (in_array($col, $jsonbCols) && (strpos($val, '{') === 0 || strpos($val, '[') === 0)) {
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
    // === TRANSACTION: Load toàn bộ seeder data vào trạng thái tạm thời ===
    DB::beginTransaction();
    echo "Transaction started.\n";

    // Xóa dữ liệu hiện tại trong transaction (sẽ rollback sau)
    echo "Clearing tours, locations, blog_posts tables in transaction...\n";
    DB::unprepared("
        TRUNCATE TABLE
            tour_locations, tour_schedules, tours,
            locations,
            blog_post_categories, blog_posts
        CASCADE;
    ");

    // Load seeder files
    foreach ($seederFiles as $f) {
        if (!file_exists($f)) {
            throw new Exception("Seeder file not found: $f");
        }
        echo "Loading: " . basename($f) . "...\n";
        $sql = loadSqlFile($f);
        DB::unprepared($sql);
    }

    // Kiểm tra số lượng đã load
    $tourCount = DB::table('tours')->count();
    $locationCount = DB::table('locations')->count();
    $blogCount = DB::table('blog_posts')->count();
    echo "\nLoaded into transaction:\n";
    echo "  Tours: $tourCount\n";
    echo "  Locations: $locationCount\n";
    echo "  Blog posts: $blogCount\n\n";

    // === SYNC: Tạo chat knowledge records từ dữ liệu seeder ===
    echo "Step 1: Syncing chat knowledge from seeder data...\n";
    Artisan::call('chatbot:sync-knowledge', [
        '--force' => true,
        '--embed' => false,
    ]);
    echo Artisan::output() . "\n";

    $knowledgeCount = DB::table('chat_knowledge_base')->count();
    echo "Knowledge records created: $knowledgeCount\n\n";

    // === EMBED: Tạo vector embeddings ===
    echo "Step 2: Generating vector embeddings với Gemini API...\n";
    echo "(Mất khoảng 5-15 phút tùy số lượng records...)\n\n";

    Artisan::call('chatbot:sync-knowledge', [
        '--embed' => true,
        '--force' => false,
    ]);
    echo Artisan::output() . "\n";

    // Kiểm tra kết quả
    $withEmbedding = DB::table('chat_knowledge_base')->whereNotNull('embedding')->count();
    $withoutEmbedding = DB::table('chat_knowledge_base')->whereNull('embedding')->count();
    echo "Embedding results:\n";
    echo "  With embedding: $withEmbedding\n";
    echo "  Without embedding: $withoutEmbedding\n\n";

    // Retry nếu còn thiếu
    if ($withoutEmbedding > 0) {
        echo "Retrying embedding for $withoutEmbedding records...\n";
        Artisan::call('chatbot:sync-knowledge', ['--embed' => true, '--force' => false]);
        echo Artisan::output() . "\n";
        $withEmbedding = DB::table('chat_knowledge_base')->whereNotNull('embedding')->count();
        $withoutEmbedding = DB::table('chat_knowledge_base')->whereNull('embedding')->count();
        echo "After retry: with=$withEmbedding, without=$withoutEmbedding\n\n";
    }

    // === EXPORT: Ghi ra file SQL ===
    echo "Step 3: Exporting to $chatOutFile ...\n";
    $rows = DB::table('chat_knowledge_base')->orderBy('id')->get();

    $chatSql = "BEGIN;\n";
    $chatSql .= dumpTableToSql(
        'chat_knowledge_base',
        $rows,
        "ON CONFLICT (id) DO UPDATE SET\n" .
        "  \"title\" = EXCLUDED.\"title\",\n" .
        "  \"content\" = EXCLUDED.\"content\",\n" .
        "  \"metadata\" = EXCLUDED.\"metadata\",\n" .
        "  \"embedding\" = EXCLUDED.\"embedding\",\n" .
        "  \"embedding_model\" = EXCLUDED.\"embedding_model\",\n" .
        "  \"embedding_dimension\" = EXCLUDED.\"embedding_dimension\",\n" .
        "  \"content_hash\" = EXCLUDED.\"content_hash\",\n" .
        "  \"last_embedded_at\" = EXCLUDED.\"last_embedded_at\",\n" .
        "  \"updated_at\" = EXCLUDED.\"updated_at\""
    );
    $chatSql .= "SELECT setval(pg_get_serial_sequence('chat_knowledge_base', 'id'), GREATEST((SELECT COALESCE(MAX(id), 0) FROM chat_knowledge_base), 1), true);\n\n";
    $chatSql .= "COMMIT;\n";

    file_put_contents($chatOutFile, $chatSql);
    $fileSize = round(filesize($chatOutFile) / 1024, 1);
    echo "✓ Exported $knowledgeCount records ($fileSize KB) to file!\n\n";

    echo "=== EXPORT HOÀN THÀNH ===\n";
    echo "File: $chatOutFile\n";
    echo "Records: $knowledgeCount (with embedding: $withEmbedding)\n\n";

    // === APPLY LÊN SERVER ===
    echo "Step 4: Applying 09_chat_knowledge.sql lên server...\n";
    $sqlContent = file_get_contents($chatOutFile);
    $sqlContent = preg_replace('/^\s*BEGIN\s*;/im', '', $sqlContent);
    $sqlContent = preg_replace('/COMMIT\s*;\s*$/im', '', $sqlContent);
    DB::unprepared($sqlContent);
    echo "✓ Applied to server database!\n\n";

    echo "=== TẤT CẢ HOÀN THÀNH ===\n";
    echo "- File 09_chat_knowledge.sql đã cập nhật với dữ liệu từ seeder\n";
    echo "- Server database đã có vector embeddings mới nhất\n";

} catch (Throwable $e) {
    echo "\nERROR: " . $e->getMessage() . "\n";
    echo $e->getTraceAsString() . "\n";
} finally {
    DB::rollBack();
    echo "\nTransaction rolled back. Live DB không bị thay đổi.\n";
}
