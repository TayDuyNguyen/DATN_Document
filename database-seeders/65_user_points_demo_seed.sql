INSERT INTO user_point_balances (
    user_id,
    available_points,
    lifetime_earned,
    lifetime_spent,
    created_at,
    updated_at
)
SELECT
    id,
    350,
    500,
    150,
    NOW(),
    NOW()
FROM users
WHERE email = 'duytayx8@gmail.com'
ON CONFLICT (user_id) DO UPDATE SET
    available_points = 350,
    lifetime_earned = GREATEST(user_point_balances.lifetime_earned, 500),
    lifetime_spent = GREATEST(user_point_balances.lifetime_spent, 150),
    updated_at = NOW();

DELETE FROM point_transactions
WHERE source_type = 'seed_demo'
  AND user_id IN (SELECT id FROM users WHERE email = 'duytayx8@gmail.com');

INSERT INTO point_transactions (
    user_id,
    type,
    points,
    balance_after,
    source_type,
    source_id,
    description,
    status,
    created_at,
    updated_at
)
SELECT id, 'earn', 10, 160, 'seed_demo', 1, 'Thanh toán đơn tour thành công', 'approved', NOW() - INTERVAL '10 days', NOW()
FROM users WHERE email = 'duytayx8@gmail.com'
UNION ALL
SELECT id, 'earn', 5, 165, 'seed_demo', 2, 'Đánh giá chất lượng được duyệt', 'approved', NOW() - INTERVAL '8 days', NOW()
FROM users WHERE email = 'duytayx8@gmail.com'
UNION ALL
SELECT id, 'earn', 20, 185, 'seed_demo', 3, 'Đề xuất địa điểm được duyệt', 'approved', NOW() - INTERVAL '5 days', NOW()
FROM users WHERE email = 'duytayx8@gmail.com'
UNION ALL
SELECT id, 'earn', 315, 500, 'seed_demo', 4, 'Điểm thưởng khởi tạo tài khoản demo loyalty', 'approved', NOW() - INTERVAL '2 days', NOW()
FROM users WHERE email = 'duytayx8@gmail.com'
UNION ALL
SELECT id, 'spend', -150, 350, 'seed_demo', 5, 'Đổi điểm lấy voucher giảm giá thử nghiệm', 'approved', NOW() - INTERVAL '1 day', NOW()
FROM users WHERE email = 'duytayx8@gmail.com';

INSERT INTO user_vouchers (
    user_id,
    point_reward_id,
    code,
    name,
    discount_type,
    discount_value,
    max_discount_amount,
    min_order_amount,
    expires_at,
    status,
    created_at,
    updated_at
)
SELECT
    u.id,
    pr.id,
    'DTV-DEMO-50K',
    'Voucher demo đổi điểm 50.000đ',
    'fixed',
    50000,
    NULL,
    300000,
    NOW() + INTERVAL '30 days',
    'active',
    NOW(),
    NOW()
FROM users u
JOIN point_rewards pr ON pr.code = 'P50K'
WHERE u.email = 'duytayx8@gmail.com'
ON CONFLICT (code) DO UPDATE SET
    user_id = EXCLUDED.user_id,
    point_reward_id = EXCLUDED.point_reward_id,
    name = EXCLUDED.name,
    discount_type = EXCLUDED.discount_type,
    discount_value = EXCLUDED.discount_value,
    max_discount_amount = EXCLUDED.max_discount_amount,
    min_order_amount = EXCLUDED.min_order_amount,
    expires_at = EXCLUDED.expires_at,
    used_at = NULL,
    status = 'active',
    updated_at = NOW();
