BEGIN;

-- Rebuild only deterministic demo notifications. Runtime notifications created
-- by normal application flows are retained.
DELETE FROM notifications
WHERE data ->> 'seed_source' = 'database_seeder';

-- Every active customer receives a concise system welcome notification.
INSERT INTO notifications (
    user_id, type, title, content, data, is_read, read_at, created_at
)
SELECT
    u.id,
    'system',
    'Chào mừng bạn đến với DanangTrip',
    'Khám phá tour, địa điểm, bài viết và quản lý hành trình ngay trong tài khoản của bạn.',
    jsonb_build_object(
        'seed_source', 'database_seeder',
        'seed_key', 'welcome-' || u.id,
        'url', '/profile'
    ),
    true,
    CURRENT_TIMESTAMP - INTERVAL '1 day',
    CURRENT_TIMESTAMP - INTERVAL '2 days'
FROM users u
WHERE u.role = 'user'
  AND u.status = 'active';

-- A current promotion keeps the notification center useful even for users who
-- have not placed an order yet.
INSERT INTO notifications (
    user_id, type, title, content, data, is_read, read_at, created_at
)
SELECT
    u.id,
    'promotion',
    'Ưu đãi dành cho hành trình tiếp theo',
    'Kiểm tra các mã giảm giá đang hoạt động trước khi đặt tour để nhận mức giá phù hợp nhất.',
    jsonb_build_object(
        'seed_source', 'database_seeder',
        'seed_key', 'promotion-' || u.id,
        'url', '/tours'
    ),
    false,
    NULL,
    CURRENT_TIMESTAMP - ((u.id % 18) + 1) * INTERVAL '1 hour'
FROM users u
WHERE u.role = 'user'
  AND u.status = 'active';

-- Payment confirmations: retain at most the two most recent successful
-- payments per customer.
WITH paid_bookings AS (
    SELECT
        b.*,
        ROW_NUMBER() OVER (
            PARTITION BY b.user_id
            ORDER BY COALESCE(b.confirmed_at, b.updated_at, b.created_at) DESC, b.id DESC
        ) AS row_number
    FROM bookings b
    WHERE b.user_id IS NOT NULL
      AND b.payment_status = 'success'
)
INSERT INTO notifications (
    user_id, type, title, content, data, is_read, read_at, created_at
)
SELECT
    b.user_id,
    'booking_payment_confirmed',
    'Thanh toán thành công',
    'Thanh toán cho đơn ' || b.booking_code || ' đã được xác nhận với số tiền '
        || TO_CHAR(b.final_amount, 'FM999G999G999G990') || ' đồng.',
    jsonb_build_object(
        'seed_source', 'database_seeder',
        'seed_key', 'payment-' || b.id,
        'booking_id', b.id,
        'booking_code', b.booking_code,
        'amount', b.final_amount
    ),
    b.row_number > 1,
    CASE
        WHEN b.row_number > 1
            THEN COALESCE(b.confirmed_at, b.updated_at, b.created_at) + INTERVAL '2 hours'
        ELSE NULL
    END,
    COALESCE(b.confirmed_at, b.updated_at, b.created_at)
FROM paid_bookings b
WHERE b.row_number <= 2;

-- Latest meaningful booking status per customer.
WITH ranked_bookings AS (
    SELECT
        b.*,
        ROW_NUMBER() OVER (
            PARTITION BY b.user_id, b.booking_status
            ORDER BY b.updated_at DESC, b.id DESC
        ) AS row_number
    FROM bookings b
    WHERE b.user_id IS NOT NULL
      AND b.booking_status IN ('confirmed', 'cancelled', 'completed')
)
INSERT INTO notifications (
    user_id, type, title, content, data, is_read, read_at, created_at
)
SELECT
    b.user_id,
    CASE b.booking_status
        WHEN 'confirmed' THEN 'booking_confirmed'
        WHEN 'cancelled' THEN 'booking_cancelled'
        ELSE 'booking_completed'
    END,
    CASE b.booking_status
        WHEN 'confirmed' THEN 'Đơn tour đã được xác nhận'
        WHEN 'cancelled' THEN 'Đơn tour đã được hủy'
        ELSE 'Hành trình đã hoàn thành'
    END,
    CASE b.booking_status
        WHEN 'confirmed'
            THEN 'Đơn ' || b.booking_code || ' đã được xác nhận. Bạn có thể xem lại thông tin hành trình trong chi tiết đơn.'
        WHEN 'cancelled'
            THEN 'Đơn ' || b.booking_code || ' đã được hủy'
                || CASE
                    WHEN NULLIF(BTRIM(b.cancellation_reason), '') IS NOT NULL
                        THEN '. Lý do: ' || b.cancellation_reason
                    ELSE '.'
                END
        ELSE 'Cảm ơn bạn đã đồng hành cùng DanangTrip trong đơn ' || b.booking_code || '.'
    END,
    jsonb_build_object(
        'seed_source', 'database_seeder',
        'seed_key', 'booking-status-' || b.id || '-' || b.booking_status,
        'booking_id', b.id,
        'booking_code', b.booking_code,
        'booking_status', b.booking_status
    ),
    b.updated_at < CURRENT_TIMESTAMP - INTERVAL '2 days',
    CASE
        WHEN b.updated_at < CURRENT_TIMESTAMP - INTERVAL '2 days'
            THEN b.updated_at + INTERVAL '3 hours'
        ELSE NULL
    END,
    b.updated_at
FROM ranked_bookings b
WHERE b.row_number = 1;

-- Recent ratings, including the target information used by the profile page.
WITH ranked_ratings AS (
    SELECT
        r.*,
        COALESCE(t.name, l.name, 'nội dung trên DanangTrip') AS target_name,
        ROW_NUMBER() OVER (
            PARTITION BY r.user_id
            ORDER BY r.created_at DESC, r.id DESC
        ) AS row_number
    FROM ratings r
    LEFT JOIN tours t ON t.id = r.tour_id
    LEFT JOIN locations l ON l.id = r.location_id
    WHERE r.status IN ('approved', 'rejected')
)
INSERT INTO notifications (
    user_id, type, title, content, data, is_read, read_at, created_at
)
SELECT
    r.user_id,
    CASE WHEN r.status = 'approved' THEN 'rating_approved' ELSE 'rating_rejected' END,
    CASE WHEN r.status = 'approved' THEN 'Đánh giá đã được ghi nhận' ELSE 'Đánh giá chưa được chấp nhận' END,
    CASE
        WHEN r.status = 'approved'
            THEN 'Đánh giá ' || r.score || ' sao của bạn về ' || r.target_name || ' đã được ghi nhận.'
        ELSE 'Đánh giá của bạn về ' || r.target_name || ' chưa được chấp nhận'
            || CASE
                WHEN NULLIF(BTRIM(r.rejected_reason), '') IS NOT NULL
                    THEN '. Lý do: ' || r.rejected_reason
                ELSE '.'
            END
    END,
    jsonb_build_object(
        'seed_source', 'database_seeder',
        'seed_key', 'rating-' || r.id || '-' || r.status,
        'rating_id', r.id,
        'tour_id', r.tour_id,
        'location_id', r.location_id,
        'score', r.score,
        'status', r.status
    ),
    r.row_number > 1,
    CASE WHEN r.row_number > 1 THEN r.created_at + INTERVAL '2 hours' ELSE NULL END,
    r.created_at
FROM ranked_ratings r
WHERE r.row_number <= 2;

-- Mirror the latest point ledger entries into user-facing notifications. The
-- point transaction remains the source of truth for balances.
WITH ranked_points AS (
    SELECT
        pt.*,
        ROW_NUMBER() OVER (
            PARTITION BY pt.user_id
            ORDER BY pt.created_at DESC, pt.id DESC
        ) AS row_number
    FROM point_transactions pt
    WHERE pt.status = 'approved'
)
INSERT INTO notifications (
    user_id, type, title, content, data, is_read, read_at, created_at
)
SELECT
    pt.user_id,
    CASE WHEN pt.type = 'spend' THEN 'point_voucher_redeemed' ELSE 'point_earned' END,
    CASE WHEN pt.type = 'spend' THEN 'Đổi điểm thành công' ELSE 'Bạn vừa nhận được điểm thưởng' END,
    CASE
        WHEN pt.type = 'spend'
            THEN 'Bạn đã sử dụng ' || ABS(pt.points) || ' điểm. ' || COALESCE(pt.description, '')
        ELSE 'Bạn được cộng ' || pt.points || ' điểm. ' || COALESCE(pt.description, '')
    END,
    jsonb_build_object(
        'seed_source', 'database_seeder',
        'seed_key', 'point-' || pt.id,
        'transaction_id', pt.id,
        'action_key', pt.action_key,
        'points', pt.points,
        'balance_after', pt.balance_after,
        'source_type', pt.source_type,
        'source_id', pt.source_id
    ),
    pt.row_number > 1,
    CASE WHEN pt.row_number > 1 THEN pt.created_at + INTERVAL '1 hour' ELSE NULL END,
    pt.created_at
FROM ranked_points pt
WHERE pt.row_number <= 3;

SELECT setval(
    pg_get_serial_sequence('notifications', 'id'),
    GREATEST((SELECT COALESCE(MAX(id), 1) FROM notifications), 1),
    true
);

COMMIT;
