INSERT INTO point_rules (
    action_key,
    name,
    description,
    points,
    max_per_day,
    requires_approval,
    status,
    created_at,
    updated_at
)
VALUES
    ('review_quality', 'Đánh giá chất lượng', 'Thưởng điểm khi người dùng viết đánh giá có nội dung hữu ích và được duyệt.', 5, 5, true, 'active', NOW(), NOW()),
    ('review_with_image', 'Đánh giá kèm ảnh', 'Thưởng thêm khi đánh giá có ảnh thật, giúp nội dung đáng tin cậy hơn.', 3, 5, true, 'active', NOW(), NOW()),
    ('content_helpful_received', 'Nội dung được đánh dấu hữu ích', 'Thưởng cho chủ đánh giá khi một người dùng khác đánh dấu nội dung là hữu ích. Không tính tự đánh dấu hoặc đánh dấu lặp.', 1, 10, false, 'active', NOW(), NOW()),
    ('content_helpful_milestone_5', 'Đạt 5 lượt hữu ích', 'Thưởng một lần khi một đánh giá đạt đủ 5 lượt hữu ích hợp lệ.', 5, NULL, false, 'active', NOW(), NOW()),
    ('content_helpful_milestone_10', 'Đạt 10 lượt hữu ích', 'Thưởng một lần khi một đánh giá đạt đủ 10 lượt hữu ích hợp lệ.', 10, NULL, false, 'active', NOW(), NOW()),
    ('booking_paid', 'Thanh toán đơn tour thành công', 'Thưởng điểm loyalty khi đơn đặt tour được thanh toán thành công.', 10, NULL, false, 'active', NOW(), NOW()),
    ('checkin_approved', 'Check-in được duyệt', 'Thưởng điểm khi người dùng check-in tại địa điểm và nội dung được xác nhận. Tạm tắt đến khi có luồng duyệt check-in.', 2, 10, true, 'inactive', NOW(), NOW()),
    ('suggest_location_approved', 'Đề xuất địa điểm được duyệt', 'Thưởng điểm cao cho người dùng đóng góp địa điểm mới hợp lệ. Tạm tắt đến khi có luồng duyệt địa điểm người dùng đề xuất.', 20, 2, true, 'inactive', NOW(), NOW())
ON CONFLICT (action_key) DO UPDATE SET
    name = EXCLUDED.name,
    description = EXCLUDED.description,
    points = EXCLUDED.points,
    max_per_day = EXCLUDED.max_per_day,
    requires_approval = EXCLUDED.requires_approval,
    status = EXCLUDED.status,
    updated_at = NOW();
