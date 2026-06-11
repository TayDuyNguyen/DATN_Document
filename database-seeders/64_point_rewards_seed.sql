INSERT INTO point_rewards (
    code,
    name,
    description,
    required_points,
    discount_type,
    discount_value,
    max_discount_amount,
    min_order_amount,
    expires_in_days,
    usage_limit_per_user,
    status,
    created_at,
    updated_at
)
VALUES
    ('P1KTEST', 'Voucher test đơn 0 đồng', 'Voucher kiểm thử giảm đúng 1.000đ cho tour test SePay giá 1.000đ. Khi áp dụng, đơn được xác nhận miễn phí và không tạo mã QR.', 1, 'fixed', 1000, NULL, 1000, 7, 20, 'active', NOW(), NOW()),
    ('P50K', 'Voucher đổi điểm 50.000đ', 'Đổi điểm loyalty thành voucher giảm 50.000đ cho đơn tour đủ điều kiện.', 100, 'fixed', 50000, NULL, 300000, 30, 1, 'active', NOW(), NOW()),
    ('P100K', 'Voucher đổi điểm 100.000đ', 'Đổi điểm loyalty thành voucher giảm 100.000đ cho đơn tour đủ điều kiện.', 200, 'fixed', 100000, NULL, 700000, 30, 1, 'active', NOW(), NOW()),
    ('P200K', 'Voucher đổi điểm 200.000đ', 'Phần thưởng dành cho người dùng tích cực đặt tour và đóng góp nội dung chất lượng.', 400, 'fixed', 200000, NULL, 1500000, 45, 1, 'active', NOW(), NOW()),
    ('P5', 'Voucher đổi điểm giảm 5%', 'Voucher giảm 5% cho đơn tour lớn, có giới hạn số tiền giảm tối đa.', 150, 'percent', 5, 150000, 500000, 30, 1, 'active', NOW(), NOW()),
    ('P10', 'Voucher đổi điểm giảm 10%', 'Voucher giảm 10% dành cho khách hàng thân thiết, có giới hạn số tiền giảm tối đa.', 300, 'percent', 10, 300000, 1000000, 30, 1, 'active', NOW(), NOW())
ON CONFLICT (code) DO UPDATE SET
    name = EXCLUDED.name,
    description = EXCLUDED.description,
    required_points = EXCLUDED.required_points,
    discount_type = EXCLUDED.discount_type,
    discount_value = EXCLUDED.discount_value,
    max_discount_amount = EXCLUDED.max_discount_amount,
    min_order_amount = EXCLUDED.min_order_amount,
    expires_in_days = EXCLUDED.expires_in_days,
    usage_limit_per_user = EXCLUDED.usage_limit_per_user,
    status = EXCLUDED.status,
    updated_at = NOW();
