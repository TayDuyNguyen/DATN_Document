-- ============================================================
-- DanangTrip Seeders v2 – TEST
-- FILE: test/02_coverage_check.sql
-- Mục đích: Kiểm tra số lượng bản ghi sau khi seed (read-only)
-- Phân loại: TEST (không thay đổi dữ liệu, chỉ đọc)
-- Nguồn: 28_seed_coverage_check.sql
-- Chạy bằng: psql -f test/02_coverage_check.sql
-- ============================================================

-- ─── Đếm bản ghi từng bảng ───────────────────────────────────
SELECT 'categories'         AS table_name, COUNT(*) AS row_count FROM categories
UNION ALL
SELECT 'subcategories',     COUNT(*) FROM subcategories
UNION ALL
SELECT 'tags',              COUNT(*) FROM tags
UNION ALL
SELECT 'amenities',         COUNT(*) FROM amenities
UNION ALL
SELECT 'tour_categories',   COUNT(*) FROM tour_categories
UNION ALL
SELECT 'blog_categories',   COUNT(*) FROM blog_categories
UNION ALL
SELECT 'settings',          COUNT(*) FROM settings
UNION ALL
SELECT 'users',             COUNT(*) FROM users
UNION ALL
SELECT 'locations',         COUNT(*) FROM locations
UNION ALL
SELECT 'tours',             COUNT(*) FROM tours
UNION ALL
SELECT 'tour_schedules',    COUNT(*) FROM tour_schedules
UNION ALL
SELECT 'blog_posts',        COUNT(*) FROM blog_posts
UNION ALL
SELECT 'bookings',          COUNT(*) FROM bookings
UNION ALL
SELECT 'payments',          COUNT(*) FROM payments
UNION ALL
SELECT 'ratings',           COUNT(*) FROM ratings
UNION ALL
SELECT 'promotions',        COUNT(*) FROM promotions
UNION ALL
SELECT 'landing_pages',     COUNT(*) FROM landing_pages
ORDER BY table_name;

-- ─── Kiểm tra FK integrity ────────────────────────────────────
SELECT 'tours orphan category' AS check_name, COUNT(*) AS issues
FROM tours t
WHERE t.tour_category_id IS NOT NULL
  AND NOT EXISTS (SELECT 1 FROM tour_categories tc WHERE tc.id = t.tour_category_id)

UNION ALL

SELECT 'bookings orphan tour', COUNT(*)
FROM bookings b
WHERE NOT EXISTS (SELECT 1 FROM tours t WHERE t.id = b.tour_id)

UNION ALL

SELECT 'ratings orphan user', COUNT(*)
FROM ratings r
WHERE NOT EXISTS (SELECT 1 FROM users u WHERE u.id = r.user_id)

UNION ALL

SELECT 'tour_schedules orphan tour', COUNT(*)
FROM tour_schedules ts
WHERE NOT EXISTS (SELECT 1 FROM tours t WHERE t.id = ts.tour_id);

-- ─── Kiểm tra tiếng Việt không dấu ──────────────────────────
-- Tìm categories còn ASCII không dấu
SELECT 'categories missing diacritics' AS check_name, id, name
FROM categories
WHERE name ~ '[Aa]m [Tt]huc|[Nn]ha [Hh]ang|[Kk]hach [Ss]an|[Dd]ia [Pp]huong'
LIMIT 10;

-- ─── Tours thiếu thông tin quan trọng ────────────────────────
SELECT 'tours missing price_child' AS check_name, COUNT(*) AS issues
FROM tours
WHERE status = 'active' AND (price_child IS NULL OR price_child = 0)

UNION ALL

SELECT 'tours missing start_time', COUNT(*)
FROM tours
WHERE status = 'active' AND start_time IS NULL

UNION ALL

SELECT 'tours missing description', COUNT(*)
FROM tours
WHERE status = 'active' AND (description IS NULL OR LENGTH(description) < 50);
