<?php
/**
 * generate_chat_knowledge_from_live_db.php
 *
 * Tạo vector embeddings từ DỮ LIỆU THỰC TẾ trong database hiện tại
 * (không dùng seeder file) và export ra demo/09_chat_knowledge.sql
 * rồi apply luôn lên server.
 *
 * API keys lấy từ .env: GEMINI_API_KEYS, GEMINI_EMBEDDING_MODEL
 */

require 'd:/DATN/danangtrip-api/vendor/autoload.php';
$app = require_once 'd:/DATN/danangtrip-api/bootstrap/app.php';
$kernel = $app->make(Illuminate\Contracts\Console\Kernel::class);
$kernel->bootstrap();

use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Artisan;
use Illuminate\Support\Facades\Config;

$chatOutFile = "d:/DATN/DATN_Tài liệu/database-seeders/seeders_v2/demo/09_chat_knowledge.sql";

echo "=== GENERATE CHAT KNOWLEDGE FROM LIVE DATABASE ===\n";
echo "Host: " . config('database.connections.pgsql.host') . "\n";
echo "Database: " . config('database.connections.pgsql.database') . "\n";
echo "Embedding model: " . config('services.gemini.embedding_model', env('GEMINI_EMBEDDING_MODEL')) . "\n";
echo "===================================================\n\n";

// --- Step 1: Kiểm tra dữ liệu hiện tại trong DB ---
$tourCount = DB::table('tours')->where('status', 'active')->count();
$locationCount = DB::table('locations')->where('status', 'active')->count();
$blogCount = DB::table('blog_posts')->where('status', 'published')->count();

echo "Dữ liệu trong DB hiện tại:\n";
echo "  Tours active: $tourCount\n";
echo "  Locations active: $locationCount\n";
echo "  Blog posts active: $blogCount\n\n";

// --- Step 2: Sync knowledge từ DB thực tế (xóa records cũ, tạo mới) ---
echo "Step 1: Sync chatbot knowledge từ live DB (--force để tái tạo tất cả)...\n";
Artisan::call('chatbot:sync-knowledge', [
    '--force' => true,   // force re-sync tất cả records
    '--embed' => false,  // chưa embed, làm sau
]);
$syncOutput = Artisan::output();
echo $syncOutput . "\n";

// --- Step 3: Generate embeddings cho tất cả records ---
echo "Step 2: Generating embeddings với Gemini API...\n";
echo "(Đây có thể mất vài phút tùy số lượng records...)\n\n";

Artisan::call('chatbot:sync-knowledge', [
    '--embed' => true,
    '--force' => false,  // chỉ embed những records chưa có embedding
]);
$embedOutput = Artisan::output();
echo $embedOutput . "\n";

// --- Step 4: Kiểm tra kết quả embedding ---
$totalKnowledge = DB::table('chat_knowledge_base')->count();
$withEmbedding = DB::table('chat_knowledge_base')->whereNotNull('embedding')->count();
$withoutEmbedding = DB::table('chat_knowledge_base')->whereNull('embedding')->count();

echo "=== Kết quả sau embedding ===\n";
echo "  Tổng records: $totalKnowledge\n";
echo "  Đã có embedding: $withEmbedding\n";
echo "  Chưa có embedding: $withoutEmbedding\n\n";

if ($withoutEmbedding > 0) {
    echo "CẢNH BÁO: Còn $withoutEmbedding records chưa có embedding!\n";
    echo "Thử chạy lại lần 2...\n";
    Artisan::call('chatbot:sync-knowledge', [
        '--embed' => true,
        '--force' => false,
    ]);
    echo Artisan::output() . "\n";

    $withoutEmbedding = DB::table('chat_knowledge_base')->whereNull('embedding')->count();
    echo "Sau lần 2: Chưa có embedding = $withoutEmbedding\n\n";
}

// --- Step 5: Export ra file SQL ---
echo "Step 3: Exporting to $chatOutFile ...\n";

function escapeForSql($val, $col) {
    if ($val === null) return 'NULL';
    if (is_bool($val)) return $val ? 'true' : 'false';
    if (is_int($val) || is_float($val)) return $val;

    // Embedding array - giữ nguyên format số
    if ($col === 'embedding' && strpos($val, '[') === 0) {
        $escaped = str_replace("'", "''", $val);
        return "'" . $escaped . "'";
    }

    // JSONB columns
    $jsonbCols = ['metadata'];
    if (in_array($col, $jsonbCols) && (strpos($val, '{') === 0 || strpos($val, '[') === 0)) {
        $escaped = str_replace("'", "''", $val);
        return "'" . $escaped . "'::jsonb";
    }

    // Normal string
    $escaped = str_replace("'", "''", $val);
    return "'" . $escaped . "'";
}

$rows = DB::table('chat_knowledge_base')->orderBy('id')->get();

if ($rows->isEmpty()) {
    echo "LỖI: Không có dữ liệu trong chat_knowledge_base!\n";
    exit(1);
}

$columns = array_keys((array)$rows->first());
$columnsList = implode(', ', array_map(fn($c) => "\"$c\"", $columns));

$chatSql = "BEGIN;\n";
$chatSql .= "INSERT INTO \"chat_knowledge_base\" ($columnsList) VALUES\n";

$valueLines = [];
foreach ($rows as $row) {
    $values = [];
    foreach ($columns as $col) {
        $values[] = escapeForSql($row->$col, $col);
    }
    $valueLines[] = "(" . implode(', ', $values) . ")";
}
$chatSql .= implode(",\n", $valueLines);
$chatSql .= "\nON CONFLICT (id) DO UPDATE SET\n";
$chatSql .= "  \"embedding\" = EXCLUDED.\"embedding\",\n";
$chatSql .= "  \"embedding_model\" = EXCLUDED.\"embedding_model\",\n";
$chatSql .= "  \"embedding_dimension\" = EXCLUDED.\"embedding_dimension\",\n";
$chatSql .= "  \"content_hash\" = EXCLUDED.\"content_hash\",\n";
$chatSql .= "  \"last_embedded_at\" = EXCLUDED.\"last_embedded_at\",\n";
$chatSql .= "  \"updated_at\" = EXCLUDED.\"updated_at\";\n\n";
$chatSql .= "SELECT setval(pg_get_serial_sequence('chat_knowledge_base', 'id'), GREATEST((SELECT COALESCE(MAX(id), 0) FROM chat_knowledge_base), 1), true);\n\n";
$chatSql .= "COMMIT;\n";

file_put_contents($chatOutFile, $chatSql);
$fileSize = round(filesize($chatOutFile) / 1024, 1);
echo "✓ Đã export $totalKnowledge records ($fileSize KB) vào file!\n";
echo "File: $chatOutFile\n\n";

echo "=== HOÀN THÀNH ===\n";
echo "File 09_chat_knowledge.sql đã được cập nhật với:\n";
echo "  - $withEmbedding records có vector embedding\n";
echo "  - Dữ liệu lấy từ live DB (không phải seeder)\n";
echo "  - Sẵn sàng để apply lên server\n";
