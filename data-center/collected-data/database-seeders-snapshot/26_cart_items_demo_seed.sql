-- DanangTrip Cart Items Demo Seeder
-- FILE: 26_cart_items_demo_seed.sql
-- Purpose:
--   Optional demo data for testing cart and checkout screens.
--   This is behavior/test data, not crawled real data.
--
-- Required before running:
--   1. 04_users.sql
--   2. 06_tours.sql and/or 20_approved_tour_staging_seed.sql

WITH demo_users AS (
    SELECT id, row_number() OVER (ORDER BY id) AS rn
    FROM users
    WHERE role IN ('customer', 'user')
    ORDER BY id
    LIMIT 5
),
available_schedules AS (
    SELECT
        ts.id AS tour_schedule_id,
        ts.tour_id,
        row_number() OVER (ORDER BY ts.start_date NULLS LAST, ts.id) AS rn
    FROM tour_schedules ts
    JOIN tours t ON t.id = ts.tour_id
    WHERE COALESCE(ts.status, 'available') IN ('available', 'open')
      AND COALESCE(t.status, 'active') IN ('active', 'open', 'pending_review')
    ORDER BY ts.start_date NULLS LAST, ts.id
    LIMIT 10
),
cart_rows AS (
    SELECT
        u.id AS user_id,
        s.tour_id,
        s.tour_schedule_id,
        CASE WHEN u.rn % 2 = 0 THEN 2 ELSE 1 END AS quantity_adult,
        CASE WHEN u.rn % 3 = 0 THEN 1 ELSE 0 END AS quantity_child,
        0 AS quantity_infant
    FROM demo_users u
    JOIN available_schedules s ON s.rn = u.rn
)
INSERT INTO cart_items (
    user_id,
    tour_id,
    tour_schedule_id,
    quantity_adult,
    quantity_child,
    quantity_infant,
    created_at,
    updated_at
)
SELECT
    user_id,
    tour_id,
    tour_schedule_id,
    quantity_adult,
    quantity_child,
    quantity_infant,
    NOW(),
    NOW()
FROM cart_rows
ON CONFLICT (user_id, tour_schedule_id) DO UPDATE SET
    quantity_adult = EXCLUDED.quantity_adult,
    quantity_child = EXCLUDED.quantity_child,
    quantity_infant = EXCLUDED.quantity_infant,
    updated_at = NOW();

