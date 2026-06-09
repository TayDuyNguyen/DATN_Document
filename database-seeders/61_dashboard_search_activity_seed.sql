-- DanangTrip dashboard search activity seed
-- FILE: 61_dashboard_search_activity_seed.sql
-- Purpose:
--   Ensure admin dashboard search panels have recent keyword, click, trend and
--   zero-result activity using real catalog titles/slugs.

BEGIN;

DELETE FROM search_logs
WHERE session_id LIKE 'demo-dashboard-search-%';

SELECT setval(
    pg_get_serial_sequence('search_logs', 'id'),
    GREATEST((SELECT COALESCE(MAX(id), 1) FROM search_logs), 1),
    true
);

WITH active_users AS (
    SELECT id, ROW_NUMBER() OVER (ORDER BY id) AS row_num
    FROM users
    WHERE role = 'user' AND status = 'active'
),
catalog_clicks AS (
    SELECT *
    FROM (
        VALUES
            (1, 'Công viên Ấn tượng Hội An', 'hoi-an-memories-land', 'location', 'suggestion_click', 7),
            (2, 'Cầu Trần Thị Lý', 'tran-thi-ly-bridge', 'location', 'result_click', 6),
            (3, 'Bếp Cuốn', 'bep-cuon', 'location', 'result_click', 6),
            (4, 'Nhà hàng Sofia', 'sofia-restaurant', 'location', 'trending_click', 5),
            (5, 'Tour Ngũ Hành Sơn & Chùa Linh Ứng Sơn Trà', 'tour-ngu-hanh-son-son-tra', 'tour', 'result_click', 5),
            (6, 'Tour Thánh Địa Mỹ Sơn nửa ngày', 'tour-my-son', 'tour', 'suggestion_click', 4)
    ) AS item(seed_no, clicked_title, clicked_slug, clicked_type, event_name, click_count)
),
click_rows AS (
    SELECT
        c.seed_no,
        gs AS repeat_no,
        c.clicked_title,
        c.clicked_slug,
        c.clicked_type,
        c.event_name,
        CASE c.clicked_type
            WHEN 'location' THEN c.clicked_title
            ELSE 'tour bán chạy Đà Nẵng'
        END AS query_text,
        CURRENT_TIMESTAMP
            - ((c.seed_no + gs) % 6) * INTERVAL '1 day'
            - ((c.seed_no * 3 + gs) % 10) * INTERVAL '1 hour' AS created_at
    FROM catalog_clicks c
    CROSS JOIN LATERAL generate_series(1, c.click_count) gs
),
keyword_rows AS (
    SELECT *
    FROM (
        VALUES
            (1, 'quán ăn ngon Huế', 18, 4),
            (2, 'đặc sản Hội An', 12, 4),
            (3, 'khách sạn gần biển', 10, 3),
            (4, 'thời gian Rồng phun lửa', 8, 3),
            (5, 'tour miền Trung 4 ngày 3 đêm', 9, 3)
    ) AS item(seed_no, query_text, results_count, search_count)
),
keyword_search_rows AS (
    SELECT
        k.seed_no,
        gs AS repeat_no,
        k.query_text,
        k.results_count,
        CURRENT_TIMESTAMP
            - ((k.seed_no + gs) % 7) * INTERVAL '1 day'
            - ((k.seed_no * 5 + gs) % 12) * INTERVAL '1 hour' AS created_at
    FROM keyword_rows k
    CROSS JOIN LATERAL generate_series(1, k.search_count) gs
),
zero_rows AS (
    SELECT *
    FROM (
        VALUES
            (1, 'chạy ngay đi', 2),
            (2, 'tour Đà Nẵng bằng trực thăng', 1),
            (3, 'khách sạn trong Cầu Rồng', 1)
    ) AS item(seed_no, query_text, search_count)
),
zero_search_rows AS (
    SELECT
        z.seed_no,
        gs AS repeat_no,
        z.query_text,
        CURRENT_TIMESTAMP
            - ((z.seed_no + gs) % 5) * INTERVAL '1 day'
            - ((z.seed_no * 7 + gs) % 8) * INTERVAL '1 hour' AS created_at
    FROM zero_rows z
    CROSS JOIN LATERAL generate_series(1, z.search_count) gs
)
INSERT INTO search_logs (user_id, session_id, query, results_count, filters, created_at)
SELECT
    u.id,
    'demo-dashboard-search-keyword-' || k.seed_no || '-' || k.repeat_no,
    k.query_text,
    k.results_count,
    jsonb_build_object('type', 'all', 'source', 'dashboard_search_activity_seed'),
    k.created_at
FROM keyword_search_rows k
JOIN active_users u
  ON u.row_num = 1 + ((k.seed_no * 11 + k.repeat_no) % (SELECT COUNT(*) FROM active_users))
UNION ALL
SELECT
    u.id,
    'demo-dashboard-search-click-' || c.seed_no || '-' || c.repeat_no,
    c.query_text,
    CASE c.clicked_type WHEN 'location' THEN 12 ELSE 8 END,
    jsonb_build_object(
        'event', c.event_name,
        'type', 'all',
        'clicked_title', c.clicked_title,
        'clicked_slug', c.clicked_slug,
        'clicked_type', c.clicked_type,
        'source', 'dashboard_search_activity_seed'
    ),
    c.created_at
FROM click_rows c
JOIN active_users u
  ON u.row_num = 1 + ((c.seed_no * 13 + c.repeat_no) % (SELECT COUNT(*) FROM active_users))
UNION ALL
SELECT
    u.id,
    'demo-dashboard-search-zero-' || z.seed_no || '-' || z.repeat_no,
    z.query_text,
    0,
    jsonb_build_object('type', 'all', 'source', 'dashboard_search_activity_seed'),
    z.created_at
FROM zero_search_rows z
JOIN active_users u
  ON u.row_num = 1 + ((z.seed_no * 17 + z.repeat_no) % (SELECT COUNT(*) FROM active_users));

SELECT setval(
    pg_get_serial_sequence('search_logs', 'id'),
    GREATEST((SELECT COALESCE(MAX(id), 1) FROM search_logs), 1),
    true
);

COMMIT;
