BEGIN;
INSERT INTO "point_rules" ("id", "action_key", "name", "description", "points", "max_per_day", "requires_approval", "status", "created_at", "updated_at") VALUES
(1, 'review_quality', 'Đánh giá chất lượng', 'Thưởng điểm khi người dùng viết đánh giá có nội dung hữu ích và được duyệt.', 5, 5, true, 'active', '2026-06-13 10:23:50', '2026-06-14 15:01:55'),
(2, 'review_with_image', 'Đánh giá kèm ảnh', 'Thưởng thêm khi đánh giá có ảnh thật, giúp nội dung đáng tin cậy hơn.', 3, 5, true, 'active', '2026-06-13 10:23:50', '2026-06-14 15:01:55'),
(3, 'content_helpful_received', 'Nội dung được đánh dấu hữu ích', 'Thưởng cho chủ đánh giá khi một người dùng khác đánh dấu nội dung là hữu ích. Không tính tự đánh dấu hoặc đánh dấu lặp.', 1, 10, false, 'active', '2026-06-13 10:23:50', '2026-06-14 15:01:55'),
(4, 'content_helpful_milestone_5', 'Đạt 5 lượt hữu ích', 'Thưởng một lần khi một đánh giá đạt đủ 5 lượt hữu ích hợp lệ.', 5, NULL, false, 'active', '2026-06-13 10:23:50', '2026-06-14 15:01:55'),
(5, 'content_helpful_milestone_10', 'Đạt 10 lượt hữu ích', 'Thưởng một lần khi một đánh giá đạt đủ 10 lượt hữu ích hợp lệ.', 10, NULL, false, 'active', '2026-06-13 10:23:50', '2026-06-14 15:01:55'),
(6, 'booking_paid', 'Thanh toán đơn tour thành công', 'Thưởng điểm loyalty khi đơn đặt tour được thanh toán thành công.', 10, NULL, false, 'active', '2026-06-13 10:23:50', '2026-06-14 15:01:55'),
(7, 'checkin_approved', 'Check-in được duyệt', 'Thưởng điểm khi người dùng check-in tại địa điểm và nội dung được xác nhận. Tạm tắt đến khi có luồng duyệt check-in.', 2, 10, true, 'inactive', '2026-06-13 10:23:50', '2026-06-14 15:01:55'),
(8, 'suggest_location_approved', 'Đề xuất địa điểm được duyệt', 'Thưởng điểm cao cho người dùng đóng góp địa điểm mới hợp lệ. Tạm tắt đến khi có luồng duyệt địa điểm người dùng đề xuất.', 20, 2, true, 'inactive', '2026-06-13 10:23:50', '2026-06-14 15:01:55')
ON CONFLICT (id) DO NOTHING;

INSERT INTO "point_rewards" ("id", "code", "name", "description", "required_points", "discount_type", "discount_value", "max_discount_amount", "min_order_amount", "expires_in_days", "usage_limit_per_user", "status", "created_at", "updated_at") VALUES
(1, 'P1KTEST', 'Voucher test đơn 0 đồng', 'Voucher kiểm thử giảm đúng 1.000đ cho tour test SePay giá 1.000đ. Khi áp dụng, đơn được xác nhận miễn phí và không tạo mã QR.', 1, 'fixed', '1000.00', NULL, '1000.00', 7, 20, 'active', '2026-06-13 10:23:50', '2026-06-14 15:01:56'),
(2, 'P50K', 'Voucher đổi điểm 50.000đ', 'Đổi điểm loyalty thành voucher giảm 50.000đ cho đơn tour đủ điều kiện.', 100, 'fixed', '50000.00', NULL, '300000.00', 30, 1, 'active', '2026-06-13 10:23:50', '2026-06-14 15:01:56'),
(3, 'P100K', 'Voucher đổi điểm 100.000đ', 'Đổi điểm loyalty thành voucher giảm 100.000đ cho đơn tour đủ điều kiện.', 200, 'fixed', '100000.00', NULL, '700000.00', 30, 1, 'active', '2026-06-13 10:23:50', '2026-06-14 15:01:56'),
(4, 'P200K', 'Voucher đổi điểm 200.000đ', 'Phần thưởng dành cho người dùng tích cực đặt tour và đóng góp nội dung chất lượng.', 400, 'fixed', '200000.00', NULL, '1500000.00', 45, 1, 'active', '2026-06-13 10:23:50', '2026-06-14 15:01:56'),
(5, 'P5', 'Voucher đổi điểm giảm 5%', 'Voucher giảm 5% cho đơn tour lớn, có giới hạn số tiền giảm tối đa.', 150, 'percent', '5.00', '150000.00', '500000.00', 30, 1, 'active', '2026-06-13 10:23:50', '2026-06-14 15:01:56'),
(6, 'P10', 'Voucher đổi điểm giảm 10%', 'Voucher giảm 10% dành cho khách hàng thân thiết, có giới hạn số tiền giảm tối đa.', 300, 'percent', '10.00', '300000.00', '1000000.00', 30, 1, 'active', '2026-06-13 10:23:50', '2026-06-14 15:01:56')
ON CONFLICT (id) DO NOTHING;

COMMIT;
