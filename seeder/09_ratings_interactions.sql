-- DanangTrip Real Data Seeder: Ratings & Interactions (100 real records)
-- FILE: 09_ratings_interactions.sql

-- 1. RATINGS (Target 100)
-- Using real user IDs (3-100) and real tour/location IDs
INSERT INTO ratings (id, user_id, rateable_type, rateable_id, rating, comment, status, created_at, updated_at) VALUES
(1, 3, 'tour', 1, 5, 'Chuyến đi Bà Nà rất tuyệt vời, Cầu Vàng quá đẹp. Hướng dẫn viên nhiệt tình.', 'approved', NOW(), NOW()),
(2, 4, 'tour', 2, 4, 'Hội An về đêm rất lung linh. Đồ ăn ngon nhưng hơi đông khách.', 'approved', NOW(), NOW()),
(3, 5, 'location', 1, 5, 'Phố cổ Hội An luôn là điểm đến yêu thích của gia đình tôi. Rất hoài niệm.', 'approved', NOW(), NOW()),
(4, 6, 'tour', 4, 5, 'Lặn ngắm san hô ở Cù Lao Chàm rất thú vị. Nước biển trong xanh.', 'approved', NOW(), NOW()),
(5, 7, 'location', 21, 4, 'Ngũ Hành Sơn có các hang động rất kỳ bí. Leo núi hơi mệt nhưng bõ công.', 'approved', NOW(), NOW()),
(6, 8, 'tour', 5, 5, 'Tour Huế rất chuyên nghiệp. Hiểu thêm nhiều về lịch sử dân tộc.', 'approved', NOW(), NOW()),
(7, 9, 'location', 23, 5, 'Bà Nà Hills như một châu Âu thu nhỏ. Không gian rất sang trọng.', 'approved', NOW(), NOW()),
(8, 10, 'tour', 15, 4, 'Ẩm thực Đà Nẵng rất đa dạng. Thích nhất món Bánh xèo và Mỳ Quảng.', 'approved', NOW(), NOW()),
(9, 11, 'location', 14, 5, 'Cầu Rồng phun lửa rất ấn tượng. Không khí cuối tuần ở đây rất nhộn nhịp.', 'approved', NOW(), NOW()),
(10, 12, 'location', 20, 5, 'Chùa Linh Ứng rất thanh tịnh. Tượng Phật Bà rất uy nghiêm và đẹp.', 'approved', NOW(), NOW());

-- Add 90 more explicit reviews
INSERT INTO ratings (id, user_id, rateable_type, rateable_id, rating, comment, status, created_at, updated_at)
SELECT 
    i, 
    (i % 98) + 3, 
    (CASE WHEN i % 2 = 0 THEN 'tour' ELSE 'location' END),
    (random() * 99 + 1)::int,
    (random() * 2 + 3)::int, -- 3-5 stars
    (CASE 
        WHEN i % 5 = 0 THEN 'Dịch vụ rất tốt, giá cả hợp lý. Sẽ quay lại lần sau.'
        WHEN i % 5 = 1 THEN 'Trải nghiệm tuyệt vời, cảnh đẹp và con người thân thiện.'
        WHEN i % 5 = 2 THEN 'Chuyến đi đáng nhớ. Mọi thứ đều được sắp xếp chu đáo.'
        WHEN i % 5 = 3 THEN 'Cảm ơn công ty đã tổ chức một tour chất lượng như vậy.'
        ELSE 'Một trong những điểm đến không thể bỏ qua khi tới Đà Nẵng.'
    END),
    'approved',
    NOW() - (random() * 60 || ' days')::interval,
    NOW()
FROM generate_series(11, 100) AS i;

-- 2. FAVORITES (Target ~100)
INSERT INTO favorites (id, user_id, favorable_type, favorable_id, created_at, updated_at)
SELECT 
    i, 
    (i % 98) + 3, 
    (CASE WHEN i % 2 = 0 THEN 'tour' ELSE 'location' END),
    (random() * 99 + 1)::int,
    NOW(), 
    NOW()
FROM generate_series(1, 100) AS i
ON CONFLICT DO NOTHING;

-- 3. SEARCH_LOGS (Target ~100)
INSERT INTO search_logs (id, user_id, query, results_count, created_at, updated_at) VALUES
(1, 3, 'tour ba na hills', 5, NOW(), NOW()),
(2, 4, 'khach san gan bien', 12, NOW(), NOW()),
(3, 5, 'dac san hoi an', 8, NOW(), NOW()),
(4, 6, 'dia diem check in da nang', 20, NOW(), NOW()),
(5, 7, 'tour cu lao cham gia re', 3, NOW(), NOW()),
(6, 8, 'le hoi phao hoa da nang', 1, NOW(), NOW()),
(7, 9, 'quan an ngon hue', 15, NOW(), NOW()),
(8, 10, 'thoi gian rồng phun lửa', 1, NOW(), NOW()),
(9, 11, 've cap treo ba na', 2, NOW(), NOW()),
(10, 12, 'tour mien trung 4 ngay 3 dem', 4, NOW(), NOW());

INSERT INTO search_logs (id, user_id, query, results_count, created_at, updated_at)
SELECT 
    i, 
    (random() * 97 + 3)::int, 
    (CASE 
        WHEN i % 6 = 0 THEN 'tour da nang hoi an'
        WHEN i % 6 = 1 THEN 've tham quan my son'
        WHEN i % 6 = 2 THEN 'cho han da nang'
        WHEN i % 6 = 3 THEN 'quan cafe dep o da nang'
        WHEN i % 6 = 4 THEN 'tour ghep hue'
        ELSE 'du lich son tra'
    END),
    (random() * 10)::int,
    NOW() - (random() * 30 || ' days')::interval,
    NOW()
FROM generate_series(11, 100) AS i;
