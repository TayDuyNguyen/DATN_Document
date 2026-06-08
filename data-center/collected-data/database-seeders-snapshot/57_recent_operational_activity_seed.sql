BEGIN;

-- Earlier catalog/demo seeds use explicit IDs, so sequences must be repaired before inserts.
SELECT setval(
    pg_get_serial_sequence('bookings', 'id'),
    GREATEST((SELECT COALESCE(MAX(id), 1) FROM bookings), 1),
    true
);
SELECT setval(
    pg_get_serial_sequence('booking_items', 'id'),
    GREATEST((SELECT COALESCE(MAX(id), 1) FROM booking_items), 1),
    true
);
SELECT setval(
    pg_get_serial_sequence('payments', 'id'),
    GREATEST((SELECT COALESCE(MAX(id), 1) FROM payments), 1),
    true
);
SELECT setval(
    pg_get_serial_sequence('favorites', 'id'),
    GREATEST((SELECT COALESCE(MAX(id), 1) FROM favorites), 1),
    true
);
SELECT setval(
    pg_get_serial_sequence('views', 'id'),
    GREATEST((SELECT COALESCE(MAX(id), 1) FROM views), 1),
    true
);

-- Mark legacy stale pending bookings as either confirmed or expired.
UPDATE bookings
SET booking_status = 'confirmed',
    confirmed_at = COALESCE(confirmed_at, booked_at + INTERVAL '2 hours'),
    updated_at = CURRENT_TIMESTAMP
WHERE booking_status = 'pending'
  AND payment_status = 'success'
  AND booked_at < CURRENT_TIMESTAMP - INTERVAL '7 days';

UPDATE bookings
SET booking_status = 'cancelled',
    cancellation_reason = COALESCE(cancellation_reason, 'Đơn đặt tour đã hết thời gian thanh toán.'),
    cancelled_at = COALESCE(cancelled_at, booked_at + INTERVAL '24 hours'),
    updated_at = CURRENT_TIMESTAMP
WHERE booking_status = 'pending'
  AND payment_status IN ('pending', 'unpaid')
  AND booked_at < CURRENT_TIMESTAMP - INTERVAL '7 days';

-- Refresh account activity to support realistic personalization and admin dashboards.
UPDATE users
SET last_login_at = CURRENT_TIMESTAMP
    - ((id * 7) % 45) * INTERVAL '1 day'
    - ((id * 13) % 18) * INTERVAL '1 hour',
    updated_at = CURRENT_TIMESTAMP
WHERE status = 'active';

-- Stable, rerunnable recent booking set backed by real active tours and future schedules.
WITH ranked_users AS (
    SELECT
        id,
        full_name,
        email,
        phone,
        city,
        ROW_NUMBER() OVER (ORDER BY id) AS row_num
    FROM users
    WHERE status = 'active'
      AND role = 'user'
),
ranked_schedules AS (
    SELECT
        ts.id AS schedule_id,
        ts.tour_id,
        ts.start_date,
        t.name AS tour_name,
        t.price_adult,
        t.price_child,
        ROW_NUMBER() OVER (ORDER BY ts.start_date, ts.id) AS row_num
    FROM tour_schedules ts
    JOIN tours t ON t.id = ts.tour_id
    WHERE ts.start_date >= CURRENT_DATE + INTERVAL '2 days'
      AND ts.status = 'available'
      AND ts.booking_availability = 'open'
      AND t.status = 'active'
      AND t.booking_availability = 'open'
),
source AS (
    SELECT
        gs AS seed_no,
        u.id AS user_id,
        u.full_name,
        u.email,
        COALESCE(NULLIF(u.phone, ''), '0905000000') AS phone,
        COALESCE(NULLIF(u.city, ''), 'Đà Nẵng') AS city,
        s.schedule_id,
        s.tour_id,
        s.start_date,
        s.tour_name,
        s.price_adult,
        s.price_child,
        1 + (gs % 3) AS adult_count,
        CASE WHEN gs % 4 = 0 THEN 1 ELSE 0 END AS child_count,
        CASE
            WHEN gs BETWEEN 15 AND 21
                THEN CURRENT_TIMESTAMP
                    - (gs - 15) * INTERVAL '1 day'
                    - ((gs * 11) % 12) * INTERVAL '1 hour'
            ELSE CURRENT_TIMESTAMP
                - ((gs * 17) % 29) * INTERVAL '1 day'
                - ((gs * 11) % 20) * INTERVAL '1 hour'
        END AS booked_at
    FROM generate_series(1, 24) gs
    JOIN ranked_users u
      ON u.row_num = 1 + ((gs * 5 - 1) % (SELECT COUNT(*) FROM ranked_users))
    JOIN ranked_schedules s
      ON s.row_num = 1 + ((gs * 7 - 1) % (SELECT COUNT(*) FROM ranked_schedules))
),
booking_source AS (
    SELECT
        *,
        price_adult * adult_count + price_child * child_count AS total_amount,
        CASE WHEN seed_no % 5 = 0 THEN 100000 ELSE 0 END AS discount_amount,
        CASE
            WHEN seed_no <= 14 THEN 'confirmed'
            WHEN seed_no <= 21 THEN 'pending'
            ELSE 'cancelled'
        END AS booking_status,
        CASE
            WHEN seed_no <= 14 THEN 'success'
            WHEN seed_no <= 18 THEN 'pending'
            ELSE 'unpaid'
        END AS payment_status,
        CASE seed_no % 4
            WHEN 0 THEN 'VNPAY'
            WHEN 1 THEN 'MOMO'
            WHEN 2 THEN 'CREDIT_CARD'
            ELSE 'CASH'
        END AS payment_method
    FROM source
)
INSERT INTO bookings (
    booking_code,
    user_id,
    customer_name,
    customer_email,
    customer_phone,
    customer_address,
    customer_note,
    total_amount,
    discount_amount,
    final_amount,
    deposit_amount,
    payment_method,
    payment_status,
    booking_status,
    cancellation_reason,
    booked_at,
    confirmed_at,
    cancelled_at,
    completed_at,
    created_at,
    updated_at
)
SELECT
    'DEMO-ACT-' || LPAD(seed_no::text, 3, '0'),
    user_id,
    full_name,
    email,
    phone,
    city,
    CASE WHEN seed_no % 6 = 0 THEN 'Ưu tiên chỗ ngồi thuận tiện cho gia đình.' ELSE NULL END,
    total_amount,
    discount_amount,
    GREATEST(total_amount - discount_amount, 0),
    CASE WHEN payment_status = 'success' THEN GREATEST(total_amount - discount_amount, 0) ELSE 0 END,
    payment_method,
    payment_status,
    booking_status,
    CASE WHEN booking_status = 'cancelled' THEN 'Khách thay đổi kế hoạch chuyến đi.' ELSE NULL END,
    booked_at,
    CASE WHEN booking_status = 'confirmed' THEN booked_at + INTERVAL '2 hours' ELSE NULL END,
    CASE WHEN booking_status = 'cancelled' THEN booked_at + INTERVAL '1 day' ELSE NULL END,
    NULL,
    booked_at,
    CURRENT_TIMESTAMP
FROM booking_source
ON CONFLICT (booking_code) DO UPDATE SET
    user_id = EXCLUDED.user_id,
    customer_name = EXCLUDED.customer_name,
    customer_email = EXCLUDED.customer_email,
    customer_phone = EXCLUDED.customer_phone,
    customer_address = EXCLUDED.customer_address,
    customer_note = EXCLUDED.customer_note,
    total_amount = EXCLUDED.total_amount,
    discount_amount = EXCLUDED.discount_amount,
    final_amount = EXCLUDED.final_amount,
    deposit_amount = EXCLUDED.deposit_amount,
    payment_method = EXCLUDED.payment_method,
    payment_status = EXCLUDED.payment_status,
    booking_status = EXCLUDED.booking_status,
    cancellation_reason = EXCLUDED.cancellation_reason,
    booked_at = EXCLUDED.booked_at,
    confirmed_at = EXCLUDED.confirmed_at,
    cancelled_at = EXCLUDED.cancelled_at,
    completed_at = EXCLUDED.completed_at,
    created_at = EXCLUDED.created_at,
    updated_at = CURRENT_TIMESTAMP;

-- Enforce the intended recent lifecycle even if a previous run changed stale statuses.
UPDATE bookings
SET booking_status = 'confirmed',
    payment_status = 'success',
    confirmed_at = booked_at + INTERVAL '2 hours',
    cancelled_at = NULL,
    cancellation_reason = NULL,
    deposit_amount = final_amount,
    updated_at = CURRENT_TIMESTAMP
WHERE booking_code BETWEEN 'DEMO-ACT-001' AND 'DEMO-ACT-014';

UPDATE bookings
SET booking_status = 'pending',
    payment_status = CASE
        WHEN booking_code BETWEEN 'DEMO-ACT-015' AND 'DEMO-ACT-018' THEN 'pending'
        ELSE 'unpaid'
    END,
    booked_at = CURRENT_TIMESTAMP
        - (SUBSTRING(booking_code FROM '[0-9]+$')::integer - 15) * INTERVAL '1 day'
        - ((SUBSTRING(booking_code FROM '[0-9]+$')::integer * 11) % 12) * INTERVAL '1 hour',
    confirmed_at = NULL,
    cancelled_at = NULL,
    cancellation_reason = NULL,
    deposit_amount = 0,
    created_at = CURRENT_TIMESTAMP
        - (SUBSTRING(booking_code FROM '[0-9]+$')::integer - 15) * INTERVAL '1 day'
        - ((SUBSTRING(booking_code FROM '[0-9]+$')::integer * 11) % 12) * INTERVAL '1 hour',
    updated_at = CURRENT_TIMESTAMP
WHERE booking_code BETWEEN 'DEMO-ACT-015' AND 'DEMO-ACT-021';

UPDATE bookings
SET booking_status = 'cancelled',
    payment_status = 'unpaid',
    confirmed_at = NULL,
    cancelled_at = booked_at + INTERVAL '1 day',
    cancellation_reason = 'Khách thay đổi kế hoạch chuyến đi.',
    deposit_amount = 0,
    updated_at = CURRENT_TIMESTAMP
WHERE booking_code BETWEEN 'DEMO-ACT-022' AND 'DEMO-ACT-024';

DELETE FROM booking_items
WHERE booking_id IN (
    SELECT id
    FROM bookings
    WHERE booking_code LIKE 'DEMO-ACT-%'
);

WITH ranked_schedules AS (
    SELECT
        ts.id AS schedule_id,
        ts.tour_id,
        ts.start_date,
        t.name AS tour_name,
        t.price_adult,
        t.price_child,
        ROW_NUMBER() OVER (ORDER BY ts.start_date, ts.id) AS row_num
    FROM tour_schedules ts
    JOIN tours t ON t.id = ts.tour_id
    WHERE ts.start_date >= CURRENT_DATE + INTERVAL '2 days'
      AND ts.status = 'available'
      AND ts.booking_availability = 'open'
      AND t.status = 'active'
      AND t.booking_availability = 'open'
),
source AS (
    SELECT
        gs AS seed_no,
        s.*,
        1 + (gs % 3) AS adult_count,
        CASE WHEN gs % 4 = 0 THEN 1 ELSE 0 END AS child_count
    FROM generate_series(1, 24) gs
    JOIN ranked_schedules s
      ON s.row_num = 1 + ((gs * 7 - 1) % (SELECT COUNT(*) FROM ranked_schedules))
)
INSERT INTO booking_items (
    booking_id,
    tour_id,
    tour_schedule_id,
    item_type,
    item_name,
    travel_date,
    quantity_adult,
    quantity_child,
    quantity_infant,
    unit_price_adult,
    unit_price_child,
    unit_price_infant,
    subtotal,
    status,
    created_at,
    updated_at
)
SELECT
    b.id,
    s.tour_id,
    s.schedule_id,
    'tour',
    s.tour_name,
    s.start_date,
    s.adult_count,
    s.child_count,
    0,
    s.price_adult,
    s.price_child,
    0,
    s.price_adult * s.adult_count + s.price_child * s.child_count,
    CASE b.booking_status
        WHEN 'confirmed' THEN 'confirmed'
        WHEN 'cancelled' THEN 'cancelled'
        ELSE 'pending'
    END,
    b.booked_at,
    CURRENT_TIMESTAMP
FROM source s
JOIN bookings b
  ON b.booking_code = 'DEMO-ACT-' || LPAD(s.seed_no::text, 3, '0');

DELETE FROM payments
WHERE transaction_code LIKE 'DEMO-ACT-PAY-%';

INSERT INTO payments (
    booking_id,
    transaction_code,
    amount,
    payment_method,
    payment_status,
    payment_gateway,
    gateway_response,
    paid_at,
    refunded_at,
    refund_reason,
    created_at,
    updated_at
)
SELECT
    b.id,
    'DEMO-ACT-PAY-' || LPAD(SUBSTRING(b.booking_code FROM '[0-9]+$'), 3, '0'),
    b.final_amount,
    b.payment_method,
    'success',
    CASE
        WHEN b.payment_method = 'CASH' THEN 'CASH'
        ELSE b.payment_method
    END,
    '{"source":"recent_operational_activity_seed","environment":"demo"}'::json,
    b.booked_at + INTERVAL '15 minutes',
    NULL,
    NULL,
    b.booked_at + INTERVAL '10 minutes',
    CURRENT_TIMESTAMP
FROM bookings b
WHERE b.booking_code LIKE 'DEMO-ACT-%'
  AND b.payment_status = 'success';

INSERT INTO payments (
    booking_id,
    transaction_code,
    amount,
    payment_method,
    payment_status,
    payment_gateway,
    gateway_response,
    paid_at,
    refunded_at,
    refund_reason,
    created_at,
    updated_at
)
SELECT
    b.id,
    'PENDING-ATTEMPT-' || b.id,
    GREATEST(b.deposit_amount, b.final_amount),
    b.payment_method,
    'pending',
    CASE
        WHEN b.payment_method = 'CASH' THEN 'CASH'
        ELSE b.payment_method
    END,
    '{"source":"recent_operational_activity_seed","state":"awaiting_payment"}'::json,
    NULL,
    NULL,
    NULL,
    b.booked_at + INTERVAL '5 minutes',
    CURRENT_TIMESTAMP
FROM bookings b
WHERE b.booking_status <> 'cancelled'
  AND b.payment_status = 'pending'
  AND NOT EXISTS (
      SELECT 1 FROM payments p WHERE p.booking_id = b.id
  )
ON CONFLICT (transaction_code) DO UPDATE SET
    amount = EXCLUDED.amount,
    payment_method = EXCLUDED.payment_method,
    payment_status = EXCLUDED.payment_status,
    payment_gateway = EXCLUDED.payment_gateway,
    gateway_response = EXCLUDED.gateway_response,
    paid_at = NULL,
    refunded_at = NULL,
    refund_reason = NULL,
    created_at = EXCLUDED.created_at,
    updated_at = CURRENT_TIMESTAMP;

-- Guarantee that every active catalog item has at least one favorite.
INSERT INTO favorites (user_id, location_id, tour_id, created_at)
SELECT
    u.id,
    l.id,
    NULL,
    CURRENT_TIMESTAMP - ((l.id * 5) % 30) * INTERVAL '1 day'
FROM locations l
JOIN LATERAL (
    SELECT id
    FROM users
    WHERE role = 'user' AND status = 'active'
    ORDER BY id
    OFFSET ((l.id * 7) % (SELECT COUNT(*) FROM users WHERE role = 'user' AND status = 'active'))
    LIMIT 1
) u ON true
WHERE l.status = 'active'
  AND NOT EXISTS (
      SELECT 1 FROM favorites f WHERE f.location_id = l.id
  )
ON CONFLICT DO NOTHING;

INSERT INTO favorites (user_id, location_id, tour_id, created_at)
SELECT
    u.id,
    NULL,
    t.id,
    CURRENT_TIMESTAMP - ((t.id * 3) % 30) * INTERVAL '1 day'
FROM tours t
JOIN LATERAL (
    SELECT id
    FROM users
    WHERE role = 'user' AND status = 'active'
    ORDER BY id
    OFFSET ((t.id * 11) % (SELECT COUNT(*) FROM users WHERE role = 'user' AND status = 'active'))
    LIMIT 1
) u ON true
WHERE t.status = 'active'
  AND NOT EXISTS (
      SELECT 1 FROM favorites f WHERE f.tour_id = t.id
  )
ON CONFLICT DO NOTHING;

UPDATE favorites
SET created_at = CURRENT_TIMESTAMP
    - ((id * 7) % 45) * INTERVAL '1 day'
    - ((id * 3) % 20) * INTERVAL '1 hour';

-- Regenerate a bounded, identifiable view stream for all active catalog items.
DELETE FROM views WHERE session_id LIKE 'demo-activity-%';

INSERT INTO views (user_id, location_id, tour_id, session_id, time_spent, created_at)
SELECT
    CASE WHEN gs % 4 = 0 THEN NULL ELSE u.id END,
    l.id,
    NULL,
    'demo-activity-location-' || l.id || '-' || gs,
    35 + ((l.id * 17 + gs * 31) % 420),
    CURRENT_TIMESTAMP
        - ((l.id * 3 + gs * 5) % 30) * INTERVAL '1 day'
        - ((l.id + gs * 7) % 20) * INTERVAL '1 hour'
FROM locations l
CROSS JOIN generate_series(1, 3) gs
JOIN LATERAL (
    SELECT id
    FROM users
    WHERE role = 'user' AND status = 'active'
    ORDER BY id
    OFFSET ((l.id * 5 + gs) % (SELECT COUNT(*) FROM users WHERE role = 'user' AND status = 'active'))
    LIMIT 1
) u ON true
WHERE l.status = 'active';

INSERT INTO views (user_id, location_id, tour_id, session_id, time_spent, created_at)
SELECT
    CASE WHEN gs % 4 = 0 THEN NULL ELSE u.id END,
    NULL,
    t.id,
    'demo-activity-tour-' || t.id || '-' || gs,
    50 + ((t.id * 19 + gs * 37) % 540),
    CURRENT_TIMESTAMP
        - ((t.id * 5 + gs * 3) % 30) * INTERVAL '1 day'
        - ((t.id + gs * 11) % 20) * INTERVAL '1 hour'
FROM tours t
CROSS JOIN generate_series(1, 3) gs
JOIN LATERAL (
    SELECT id
    FROM users
    WHERE role = 'user' AND status = 'active'
    ORDER BY id
    OFFSET ((t.id * 7 + gs) % (SELECT COUNT(*) FROM users WHERE role = 'user' AND status = 'active'))
    LIMIT 1
) u ON true
WHERE t.status = 'active';

-- Refresh existing interaction streams without multiplying records.
UPDATE search_logs
SET created_at = CURRENT_TIMESTAMP
    - ((id * 11) % 45) * INTERVAL '1 day'
    - ((id * 7) % 20) * INTERVAL '1 hour';

UPDATE notifications
SET created_at = CURRENT_TIMESTAMP
        - ((id * 13) % 45) * INTERVAL '1 day'
        - ((id * 5) % 20) * INTERVAL '1 hour',
    is_read = (id % 3 <> 0),
    read_at = CASE
        WHEN id % 3 <> 0
            THEN CURRENT_TIMESTAMP
                - ((id * 13) % 45) * INTERVAL '1 day'
                - ((id * 5) % 20) * INTERVAL '1 hour'
                + INTERVAL '3 hours'
        ELSE NULL
    END;

UPDATE contacts
SET created_at = CURRENT_TIMESTAMP
        - ((id * 17) % 60) * INTERVAL '1 day'
        - ((id * 3) % 20) * INTERVAL '1 hour',
    updated_at = CURRENT_TIMESTAMP;

-- Counters shown by APIs must reflect the underlying interaction rows.
UPDATE locations l
SET view_count = (SELECT COUNT(*) FROM views v WHERE v.location_id = l.id),
    favorite_count = (SELECT COUNT(*) FROM favorites f WHERE f.location_id = l.id),
    updated_at = CURRENT_TIMESTAMP;

UPDATE tours t
SET view_count = (SELECT COUNT(*) FROM views v WHERE v.tour_id = t.id),
    booking_count = (
        SELECT COUNT(*)
        FROM booking_items bi
        JOIN bookings b ON b.id = bi.booking_id
        WHERE bi.tour_id = t.id
          AND b.booking_status <> 'cancelled'
    ),
    updated_at = CURRENT_TIMESTAMP;

SELECT setval(
    pg_get_serial_sequence('bookings', 'id'),
    GREATEST((SELECT COALESCE(MAX(id), 1) FROM bookings), 1),
    true
);
SELECT setval(
    pg_get_serial_sequence('booking_items', 'id'),
    GREATEST((SELECT COALESCE(MAX(id), 1) FROM booking_items), 1),
    true
);
SELECT setval(
    pg_get_serial_sequence('payments', 'id'),
    GREATEST((SELECT COALESCE(MAX(id), 1) FROM payments), 1),
    true
);
SELECT setval(
    pg_get_serial_sequence('favorites', 'id'),
    GREATEST((SELECT COALESCE(MAX(id), 1) FROM favorites), 1),
    true
);
SELECT setval(
    pg_get_serial_sequence('views', 'id'),
    GREATEST((SELECT COALESCE(MAX(id), 1) FROM views), 1),
    true
);

COMMIT;
