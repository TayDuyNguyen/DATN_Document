-- ============================================================
-- DanangTrip Seeders v2 – MASTER SCRIPT
-- FILE: run_all_seeders.sql
-- Mục đích: Chạy tất cả seeder theo thứ tự khóa ngoại đúng
-- Dành cho: DB MỚI sau khi chạy migrations
-- KHÔNG dùng cho DB đã có dữ liệu (dùng incremental thay thế)
-- ============================================================
--
-- Cách chạy (psql):
--   psql $DATABASE_URL -f run_all_seeders.sql
--
-- Hoặc qua Laravel:
--   php artisan tinker --execute="DB::statement(file_get_contents('...'));"
--
-- ============================================================

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

\echo '=== DanangTrip Seeders v2 - Full Seed ==='
\echo ''

-- ────────────────────────────────────────────────────────────
-- LAYER 1: BASE SYSTEM TABLES (No Foreign Keys or Independent)
-- ────────────────────────────────────────────────────────────
\echo '[1/21] Seeding categories...'
\i base/01_categories.sql

\echo '[2/21] Seeding subcategories...'
\i base/02_subcategories.sql

\echo '[3/21] Seeding tags...'
\i base/03_tags.sql

\echo '[4/21] Seeding amenities...'
\i base/04_amenities.sql

\echo '[5/21] Seeding tour_categories...'
\i base/05_tour_categories.sql

\echo '[6/21] Seeding blog_categories...'
\i base/06_blog_categories.sql

\echo '[7/21] Seeding system settings...'
\i base/07_system_settings.sql

\echo '[8/21] Seeding admin users...'
\i base/08_admin_users.sql

\echo '[9/21] Seeding point rules...'
\i base/09_point_rules.sql

\echo '[10/21] Seeding landing pages...'
\i base/10_landing_pages.sql

-- ────────────────────────────────────────────────────────────
-- LAYER 2: DEMO DATA (Depends on BASE LAYER)
-- ────────────────────────────────────────────────────────────
\echo ''
\echo '=== DEMO LAYER ==='

\echo '[11/21] Seeding demo users...'
\i demo/01_demo_users.sql

\echo '[12/21] Seeding promotions...'
\i demo/02_promotions.sql

\echo '[13/21] Seeding locations (enriched with Cloudinary images & diacritics)...'
\i demo/03_locations.sql

\echo '[14/21] Seeding tours (schedules & locations linked)...'
\i demo/04_tours.sql

\echo '[15/21] Seeding blog posts (categories & featured images linked)...'
\i demo/05_blog_posts.sql

\echo '[16/21] Seeding bookings & payment transactions...'
\i demo/06_bookings.sql

\echo '[17/21] Seeding ratings, reviews & favorites...'
\i demo/07_ratings.sql

\echo '[18/22] Seeding notifications, points, views & search logs activity...'
\i demo/08_notifications_activity.sql

\echo '[19/22] Seeding chatbot knowledge base...'
\i demo/09_chat_knowledge.sql

-- ────────────────────────────────────────────────────────────
-- LAYER 3: TEST DATA & INTEGRITY VERIFICATION
-- ────────────────────────────────────────────────────────────
\echo ''
\echo '=== TEST & INTEGRITY LAYER ==='

\echo '[20/22] Seeding test cart items...'
\i test/01_test_cart.sql

\echo '[21/22] Seeding test checkout (1,000đ SePay VietQR test tour)...'
\i test/03_test_checkout.sql

\echo '[22/22] Running coverage & integrity checks...'
\i test/02_coverage_check.sql

\echo ''
\echo '=== Seed hoàn tất! ==='
