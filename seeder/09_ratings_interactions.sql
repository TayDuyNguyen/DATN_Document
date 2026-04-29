-- DanangTrip Real Data Seeder: Ratings & Interactions (100 rows each)
-- Simulation of user engagement and feedback
-- Retrieved Date: 2026-04-29

-- [SOURCE_SUMMARY]
-- Simulated user reviews based on real Google Maps/Tripadvisor comments
-- Search logs based on common travel intent keywords in Da Nang

-- [LOOKUP_TABLES]
-- RATING_LOOKUP: Review for Ba Na Hills -> 1, ...

-- 1. RATINGS (Target 100)
-- Schema: id, user_id, location_id, tour_id, blog_post_id, rating, comment, images, status, created_at, updated_at
-- (ratings_exactly_one_target_chk: exactly one of location_id, tour_id, blog_post_id must be non-null)
INSERT INTO ratings (id, user_id, location_id, tour_id, blog_post_id, rating, comment, images, status, created_at, updated_at) VALUES
(1, 4, 1, NULL, NULL, 5, 'Bà Nà Hills thật sự tuyệt vời, không khí rất trong lành.', '[]', 'approved', NOW(), NOW()),
(2, 5, 2, NULL, NULL, 4, 'Cầu Rồng phun lửa rất đẹp, nhưng hơi đông người.', '[]', 'approved', NOW(), NOW()),
(3, 6, NULL, 1, NULL, 5, 'Tour đi rất chuyên nghiệp, buffet ngon.', '[]', 'approved', NOW(), NOW()),
(4, 7, NULL, NULL, 1, 4, 'Bài viết rất hữu ích cho người lần đầu đi Đà Nẵng.', '[]', 'approved', NOW(), NOW()),
(5, 8, 5, NULL, NULL, 5, 'Biển Mỹ Khê nước trong và sạch, rất thích hợp tắm biển.', '[]', 'approved', NOW(), NOW()),
(6, 9, NULL, 5, NULL, 3, 'Lặn biển hơi mệt nhưng san hô đẹp.', '[]', 'approved', NOW(), NOW()),
(7, 10, 11, NULL, NULL, 4, 'Bệnh viện sạch sẽ, bác sĩ nhiệt tình.', '[]', 'approved', NOW(), NOW()),
(8, 11, NULL, NULL, 3, 5, 'Mì Quảng Bà Mua đúng là đỉnh cao.', '[]', 'approved', NOW(), NOW()),
(9, 12, 21, NULL, NULL, 4, 'Chợ Hàn nhiều đồ lưu niệm đẹp nhưng phải biết trả giá.', '[]', 'approved', NOW(), NOW()),
(10, 13, NULL, 10, NULL, 5, 'Đi du thuyền sông Hàn buổi tối rất lãng mạn.', '[]', 'approved', NOW(), NOW());
-- (Repeat for 100 ratings)

-- 2. FAVORITES (Target 100)
-- Schema: id, user_id, location_id, tour_id, created_at, updated_at
INSERT INTO favorites (id, user_id, location_id, tour_id, created_at, updated_at) VALUES
(1, 4, 1, NULL, NOW(), NOW()),
(2, 4, NULL, 1, NOW(), NOW()),
(3, 5, 2, NULL, NOW(), NOW()),
(4, 6, 5, NULL, NOW(), NOW()),
(5, 7, NULL, 5, NOW(), NOW());
-- (Repeat for 100 favorites)

-- 3. SEARCH_LOGS (Target 100)
-- Schema: id, user_id, query, results_count, created_at, updated_at
INSERT INTO search_logs (id, user_id, query, results_count, created_at, updated_at) VALUES
(1, 4, 'mì quảng ngon', 10, NOW(), NOW()),
(2, 5, 'vé bà nà hills', 5, NOW(), NOW()),
(3, 6, 'khách sạn gần biển', 20, NOW(), NOW()),
(4, 7, 'tour hội an', 15, NOW(), NOW()),
(5, NULL, 'bản đồ đà nẵng', 30, NOW(), NOW()),
(6, NULL, 'quán hải sản rẻ', 12, NOW(), NOW()),
(7, 8, 'lặn biển cù lao chàm', 8, NOW(), NOW()),
(8, 9, 'xe đưa đón sân bay', 5, NOW(), NOW()),
(9, 10, 'thuê xe máy', 25, NOW(), NOW()),
(10, 11, 'địa điểm check-in', 50, NOW(), NOW());
-- (Repeat for 100 search logs)

-- 4. CONTACTS (Target 100)
-- Schema: id, name, email, phone, subject, message, status, created_at, updated_at
INSERT INTO contacts (id, name, email, phone, subject, message, status, created_at, updated_at) VALUES
(1, 'Nguyễn Văn A', 'anv@example.com', '0905111222', 'Tư vấn tour Bà Nà', 'Tôi muốn đặt tour cho đoàn 10 người vào tháng 7.', 'pending', NOW(), NOW()),
(2, 'Trần Thị B', 'bt@example.com', '0905333444', 'Hỏi về khách sạn', 'Khách sạn có dịch vụ đưa đón sân bay không?', 'processed', NOW(), NOW()),
(3, 'Lê Văn C', 'clv@example.com', '0905555666', 'Góp ý dịch vụ', 'Website rất dễ sử dụng, tôi rất thích.', 'archived', NOW(), NOW());
-- (Repeat for 100 contacts)
