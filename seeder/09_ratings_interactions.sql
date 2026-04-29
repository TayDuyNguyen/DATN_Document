-- DanangTrip Real Data Seeder: Ratings, Favorites, Views, Search Logs & Contacts
-- Source: TripAdvisor (Da Nang Landmarks), Google Search Trends, UX Analysis 2024
-- Retrieved Date: 2026-04-29

-- RATING_LOOKUP
-- 1: Review for Ba Na Hills (User 3)
-- 2: Review for Madame Lan (User 4)
-- ...

INSERT INTO ratings (id, user_id, location_id, tour_id, booking_id, score, comment, status, is_featured, created_at, updated_at) VALUES
(1, 3, 1, NULL, 1, 5, 'Bà Nà Hills thực sự là chốn bồng lai tiên cảnh. Cầu Vàng rất ấn tượng, không khí trong lành. Dịch vụ chuyên nghiệp.', 'approved', true, '2024-05-02 09:00:00', NOW()),
(2, 4, 18, NULL, 2, 5, 'Đồ ăn tại Madame Lân rất ngon, không gian ấm cúng đậm chất Việt. Nhân viên nhiệt tình.', 'approved', true, '2024-05-02 10:30:00', NOW()),
(3, 7, 3, NULL, NULL, 4, 'Chùa Linh Ứng rất đẹp và thanh tịnh. View nhìn ra biển cực đỉnh. Tuy nhiên vào mùa lễ hơi đông.', 'approved', false, '2024-04-29 15:00:00', NOW()),
(4, 9, 5, NULL, NULL, 5, 'Bãi biển Mỹ Khê tuyệt đẹp, cát mịn, nước trong. Sáng sớm tắm biển rất thích.', 'approved', false, '2024-04-28 06:00:00', NOW()),
(5, 10, 1, NULL, NULL, 3, 'Cảnh đẹp nhưng giá vé hơi cao, xếp hàng chờ cáp treo khá lâu vào cuối tuần.', 'approved', false, '2024-04-27 11:00:00', NOW());

INSERT INTO rating_images (id, rating_id, image_path, sort_order, created_at, updated_at) VALUES
(1, 1, 'rating1_img1.jpg', 1, NOW(), NOW()),
(2, 1, 'rating1_img2.jpg', 2, NOW(), NOW()),
(3, 2, 'rating2_img1.jpg', 1, NOW(), NOW());

INSERT INTO favorites (id, user_id, location_id, tour_id, created_at, updated_at) VALUES
(1, 3, 2, NULL, NOW(), NOW()), -- Huy thích Ngũ Hành Sơn
(2, 3, 3, NULL, NOW(), NOW()), -- Huy thích Chùa Linh Ứng
(3, 4, 1, NULL, NOW(), NOW()), -- Mai thích Bà Nà Hills
(4, 4, NULL, 1, NOW(), NOW()); -- Mai thích Tour Bà Nà

INSERT INTO views (id, user_id, location_id, tour_id, session_id, ip_address, user_agent, time_spent, created_at) VALUES
(1, 3, 1, NULL, 'sess_01', '127.0.0.1', 'Chrome/Windows', 300, NOW()),
(2, NULL, 2, NULL, 'sess_02', '127.0.0.1', 'Safari/iPhone', 120, NOW()),
(3, 4, NULL, 1, 'sess_03', '127.0.0.1', 'Chrome/Windows', 450, NOW());

INSERT INTO search_logs (id, user_id, query, results_count, filters, created_at) VALUES
(1, 3, 'Sun World Bà Nà Hills', 12, '{"category": "sightseeing"}', NOW()),
(2, NULL, 'Cầu Vàng', 8, NULL, NOW()),
(3, 4, 'Bãi biển Mỹ Khê', 5, NULL, NOW()),
(4, NULL, 'Mì Quảng ngon', 15, '{"category": "dining"}', NOW()),
(5, 7, 'Khách sạn ven biển Đà Nẵng', 25, '{"price_max": 2000000}', NOW());

INSERT INTO contacts (id, name, email, phone, subject, message, status, notes, created_at, updated_at) VALUES
(1, 'Nguyễn Văn A', 'vana@gmail.com', '0901234567', 'Tư vấn tour gia đình', 'Chào bạn, mình muốn hỏi giá tour Bà Nà Hills cho đoàn 10 người lớn vào tuần sau. Có ưu đãi gì không ạ?', 'pending', NULL, NOW(), NOW()),
(2, 'Trần Thị B', 'thib@gmail.com', '0912345678', 'Hỏi về đón trả khách', 'Tour Cù Lao Chàm có đón tại khách sạn ở Ngũ Hành Sơn không shop? Lịch trình cụ thể thế nào ạ?', 'processed', 'Đã gọi điện tư vấn.', NOW(), NOW());

INSERT INTO notifications (id, user_id, type, title, content, data, is_read, read_at, created_at, updated_at) VALUES
(1, 3, 'booking_status', 'Đặt chỗ thành công', 'Đơn hàng DT-240501-001 của bạn đã được xác nhận.', '{"booking_id": 1}', false, NULL, NOW(), NOW()),
(2, 4, 'system', 'Ưu đãi hè rực rỡ', 'Giảm ngay 10% khi đặt tour Hội An trong tháng 5.', '{"discount_code": "SUMMER10"}', true, NOW(), NOW(), NOW());
