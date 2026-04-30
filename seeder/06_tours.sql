-- DanangTrip Real Data Seeder: Tours, Pivots & Schedules (100 real tours)
-- FILE: 06_tours.sql

-- 1. TOURS (Target 100)
INSERT INTO tours (id, name, slug, tour_category_id, description, short_desc, itinerary, inclusions, exclusions, price_adult, price_child, price_infant, discount_percent, duration, start_time, meeting_point, max_people, min_people, status, is_featured, is_hot, created_at, updated_at) VALUES
(1, 'Tour Bà Nà Hills 1 Ngày (Buffet Trưa)', 'tour-ba-na-hills-1-ngay', 1, 'Khám phá chốn bồng lai tiên cảnh với Cầu Vàng, Làng Pháp và hệ thống cáp treo đạt nhiều kỷ lục thế giới.', 'Hành trình đưa quý khách đến với đỉnh Núi Chúa - Đà Nẵng.', '[{"time": "08:00", "task": "Đón khách tại trung tâm Đà Nẵng"}, {"time": "09:30", "task": "Check-in Cầu Vàng"}, {"time": "12:00", "task": "Ăn trưa Buffet"}, {"time": "15:30", "task": "Rời Bà Nà"}]', '["Xe đưa đón đời mới", "Hướng dẫn viên", "Vé cáp treo", "Buffet trưa 100 món"]', '["Nước uống trong bữa ăn", "Chi phí cá nhân", "Tip cho HDV"]', 1250000, 950000, 250000, 5, '1 ngày', '08:00', 'Văn phòng Đà Nẵng / Khách sạn trung tâm', 45, 2, 'active', true, true, NOW(), NOW()),
(2, 'Tour Phố Cổ Hội An & Rừng Dừa Bảy Mẫu', 'tour-hoi-an-rung-dua', 2, 'Trải nghiệm chèo thúng tại rừng dừa Bảy Mẫu và khám phá vẻ đẹp hoài cổ của phố cổ Hội An về đêm.', 'Kết hợp trải nghiệm sông nước và văn hóa phố cổ.', '[{"time": "14:00", "task": "Đón khách"}, {"time": "15:00", "task": "Tham quan Rừng dừa"}, {"time": "17:30", "task": "Dạo phố cổ Hội An"}, {"time": "21:00", "task": "Trở về Đà Nẵng"}]', '["Xe đưa đón", "Vé tham quan", "Chèo thúng", "Ăn tối đặc sản Hội An"]', '["Đồ uống", "Ổ khóa tình yêu"]', 750000, 550000, 150000, 0, '7 giờ', '14:00', 'Đà Nẵng / Hội An', 30, 2, 'active', true, false, NOW(), NOW()),
(3, 'Tour Ngũ Hành Sơn & Chùa Linh Ứng Sơn Trà', 'tour-ngu-hanh-son-son-tra', 5, 'Hành trình tâm linh khám phá các hang động kỳ bí tại Ngũ Hành Sơn và chiêm bái Phật Bà tại Sơn Trà.', 'Tour tâm linh nửa ngày ngắm cảnh biển Đà Nẵng.', '[{"time": "08:00", "task": "Tham quan Chùa Linh Ứng"}, {"time": "10:00", "task": "Khám phá Ngũ Hành Sơn"}, {"time": "12:00", "task": "Kết thúc tour"}]', '["Xe du lịch", "HDV nhiệt tình", "Nước suối", "Vé tham quan"]', '["Ăn trưa", "Chi phí cá nhân"]', 450000, 250000, 0, 0, '4 giờ', '08:00', 'Đà Nẵng', 20, 2, 'active', false, false, NOW(), NOW()),
(4, 'Tour Cù Lao Chàm Lặn Ngắm San Hô', 'tour-cu-lao-cham', 3, 'Chuyến đi biển đảo hấp dẫn với các hoạt động tắm biển, lặn ngắm san hô và thưởng thức hải sản tươi ngon.', 'Thiên đường biển đảo Cù Lao Chàm.', '[{"time": "08:30", "task": "Cano cao tốc đi đảo"}, {"time": "10:00", "task": "Lặn ngắm san hô"}, {"time": "12:00", "task": "Ăn trưa hải sản"}, {"time": "14:30", "task": "Về lại đất liền"}]', '["Cano cao tốc", "Kính lặn", "Ăn trưa", "Bảo hiểm du lịch"]', '["Lặn bình khí", "Phí môi trường quốc tế"]', 650000, 450000, 100000, 10, '1 ngày', '08:00', 'Cảng Cửa Đại', 35, 4, 'active', true, true, NOW(), NOW()),
(5, 'Tour Cố Đô Huế 1 Ngày từ Đà Nẵng', 'tour-hue-1-ngay', 5, 'Vượt đèo Hải Vân đến với cố đô Huế, tham quan Đại Nội, chùa Thiên Mụ và các lăng tẩm uy nghiêm.', 'Hành trình di sản cố đô miền Trung.', '[{"time": "07:30", "task": "Khởi hành qua hầm Hải Vân"}, {"time": "10:30", "task": "Tham quan Đại Nội"}, {"time": "12:00", "task": "Ăn trưa đặc sản Huế"}, {"time": "15:00", "task": "Tham quan Lăng Khải Định"}]', '["Xe đưa đón", "HDV", "Vé tham quan các điểm", "Ăn trưa"]', '["Chi phí cá nhân"]', 1050000, 750000, 200000, 0, '1 ngày', '07:30', 'Đà Nẵng', 40, 2, 'active', true, false, NOW(), NOW()),
(6, 'Tour Thánh Địa Mỹ Sơn nửa ngày', 'tour-my-son', 5, 'Tìm hiểu về văn hóa Champa cổ đại qua quần thể đền tháp Mỹ Sơn - Di sản văn hóa thế giới.', 'Khám phá bí ẩn tháp Chàm.', '[{"time": "08:00", "task": "Khởi hành"}, {"time": "09:30", "task": "Tham quan Mỹ Sơn"}, {"time": "11:00", "task": "Xem múa Apsara"}, {"time": "13:00", "task": "Về lại Hội An"}]', '["Xe vận chuyển", "HDV", "Vé tham quan", "Xem biểu diễn văn nghệ"]', '["Ăn trưa", "Tip"]', 550000, 400000, 100000, 0, '5 giờ', '08:00', 'Đà Nẵng / Hội An', 25, 2, 'active', false, false, NOW(), NOW()),
(7, 'Tour Đà Nẵng City - Những Cây Cầu', 'tour-city-danang', 1, 'Hành trình check-in những biểu tượng hiện đại của Đà Nẵng: Cầu Rồng, Cầu Tình Yêu, Bảo tàng Chăm.', 'Tour khám phá thành phố đáng sống.', '[{"time": "08:00", "task": "Bảo tàng Chăm"}, {"time": "10:00", "task": "Cầu Rồng & Cầu Tình Yêu"}, {"time": "11:30", "task": "Chợ Hàn"}]', '["Xe du lịch", "HDV", "Vé bảo tàng", "Nước uống"]', '["Ăn trưa"]', 350000, 200000, 0, 0, '4 giờ', '08:30', 'Đà Nẵng', 15, 2, 'active', false, false, NOW(), NOW()),
(8, 'Tour Đèo Hải Vân & Lăng Cô - Ô tô', 'tour-hai-van-lang-co', 3, 'Trải nghiệm cung đường đèo đẹp nhất Việt Nam và thư giãn tại vịnh biển Lăng Cô thơ mộng.', 'Ngắm nhìn "Thiên hạ đệ nhất hùng quan".', '[]', '["Xe du lịch", "HDV", "Ăn trưa hải sản"]', '["Dịch vụ biển"]', 850000, 600000, 150000, 0, '1 ngày', '08:00', 'Đà Nẵng', 20, 2, 'active', false, false, NOW(), NOW()),
(9, 'Tour Đêm Phố Cổ Hội An & Ăn Tối', 'tour-dem-hoi-an', 6, 'Dạo bước phố đèn lồng, thả đèn hoa đăng và thưởng thức các món ăn đặc sản nổi tiếng của Hội An.', 'Lãng mạn phố cổ về đêm.', '[]', '["Xe đưa đón", "Ăn tối", "Thả hoa đăng"]', '["Mua sắm cá nhân"]', 600000, 450000, 100000, 0, '5 giờ', '16:00', 'Đà Nẵng', 25, 2, 'active', false, true, NOW(), NOW()),
(10, 'Tour Bà Nà Hills Đêm (Sun World Night)', 'tour-ba-na-night', 1, 'Trải nghiệm Bà Nà Hills lung linh về đêm với Buffet tối, rượu vang và các show diễn đặc sắc.', 'Bà Nà huyền ảo buổi đêm.', '[]', '["Cáp treo khứ hồi", "Ăn tối Buffet", "Rượu vang/Bia"]', '["Các trò chơi có phí"]', 950000, 750000, 200000, 0, '1 ngày', '15:30', 'Cáp treo Bà Nà', 50, 1, 'active', false, true, NOW(), NOW()),
(11, 'Tour VinWonders Nam Hội An Full Day', 'tour-vinwonders-nam-hoi-an', 1, 'Vui chơi không giới hạn tại VinWonders Nam Hội An với Safari, Công viên nước và Đảo văn hóa.', 'Thế giới giải trí đa sắc màu.', '[]', '["Xe bus đón tiễn", "Vé vào cổng", "Ăn trưa set menu"]', '["Mua sắm", "Chi phí khác"]', 900000, 700000, 150000, 0, '1 ngày', '09:00', 'Đà Nẵng / Hội An', 50, 1, 'active', false, false, NOW(), NOW()),
(12, 'Tour Suối Khoáng Nóng Thần Tài Relax', 'tour-nui-than-tai', 4, 'Thư giãn tuyệt đối với dịch vụ tắm khoáng, tắm bùn và khu vui chơi nước giữa núi rừng.', 'Nghỉ dưỡng và chăm sóc sức khỏe.', '[]', '["Xe đưa đón", "Vé cổng", "Buffet trưa"]', '["Tắm bùn/Tắm sả", "Phòng nghỉ"]', 850000, 650000, 150000, 0, '1 ngày', '08:30', 'Đà Nẵng', 30, 2, 'active', false, false, NOW(), NOW()),
(13, 'Tour Trekking Bán Đảo Sơn Trà', 'tour-trekking-son-tra', 7, 'Thám hiểm rừng già Sơn Trà, tìm kiếm voọc chà vá chân nâu và chinh phục đỉnh Bàn Cờ.', 'Thử thách thiên nhiên Sơn Trà.', '[]', '["HDV thám hiểm", "Gậy trekking", "Ăn nhẹ", "Nước suối"]', '["Vận chuyển"]', 700000, 700000, 0, 0, '6 giờ', '06:00', 'Sơn Trà', 10, 2, 'active', false, false, NOW(), NOW()),
(14, 'Tour Khám Phá Bạch Mã National Park', 'tour-bach-ma', 7, 'Trekking rừng quốc gia Bạch Mã, ngắm thác Đỗ Quyên và ngắm toàn cảnh vịnh Lăng Cô từ Hải Vọng Đài.', 'Hành trình chinh phục đỉnh Bạch Mã.', '[]', '["Xe đưa đón", "HDV chuyên tuyến", "Ăn trưa picnic", "Vé cổng"]', '["Dụng cụ cá nhân"]', 1100000, 850000, 200000, 0, '1 ngày', '07:30', 'Đà Nẵng / Huế', 15, 2, 'active', false, false, NOW(), NOW()),
(15, 'Street Food Tour Đà Nẵng bằng Xe Máy', 'tour-street-food-danang', 6, 'Ngồi sau xe máy cùng HDV địa phương len lỏi vào các ngõ ngách thưởng thức 5-7 món ăn đặc sản.', 'Khám phá ẩm thực Đà Nẵng như người bản địa.', '[]', '["Xe máy & Xăng", "Tất cả đồ ăn thức uống", "HDV địa phương"]', '["Tip"]', 650000, 650000, 0, 0, '4 giờ', '18:00', 'Khách sạn trung tâm', 10, 1, 'active', false, true, NOW(), NOW()),
(16, 'Tour Làm Nông Dân Làng Rau Trà Quế', 'tour-tra-que-farmer', 5, 'Học cách xới đất, trồng rau, tưới nước và tự tay chế biến món ăn từ rau sạch Trà Quế.', 'Một ngày làm nông dân Hội An.', '[]', '["Phí tham quan", "HDV nông dân", "Ăn trưa gia đình"]', '["Đưa đón"]', 500000, 350000, 100000, 0, '4 giờ', '08:30', 'Làng Trà Quế', 12, 1, 'active', false, false, NOW(), NOW()),
(17, 'Tour Du Thuyền Sông Hàn & Xem Rồng Phun Lửa', 'tour-du-thuyen-song-han', 1, 'Ngắm nhìn thành phố ánh sáng từ giữa lòng sông và xem Cầu Rồng phun lửa, phun nước vào tối cuối tuần.', 'Buổi tối lãng mạn trên sông Hàn.', '[]', '["Vé du thuyền", "Nước uống", "Bảo hiểm"]', '["Ăn tối trên thuyền"]', 200000, 150000, 50000, 0, '2 giờ', '19:30', 'Bến tàu Bạch Đằng', 80, 1, 'active', false, false, NOW(), NOW()),
(18, 'Tour Đầm Phá Tam Giang & Sunset', 'tour-tam-giang-sunset', 3, 'Khám phá hệ sinh thái đầm phá nước lợ, chèo thuyền Kayak và ngắm hoàng hôn tuyệt đẹp.', 'Hoàng hôn rực rỡ trên phá Tam Giang.', '[]', '["Xe đưa đón", "Thuyền tham quan", "Ăn tối hải sản"]', '["Chi phí khác"]', 750000, 550000, 150000, 0, '6 giờ', '14:30', 'Huế', 20, 2, 'active', false, false, NOW(), NOW()),
(19, 'Tour Ca Huế Trên Sông Hương & Ngắm Thành Phố', 'tour-ca-hue-song-huong', 5, 'Thưởng thức loại hình nghệ thuật di sản phi vật thể và thả đèn hoa đăng cầu may trên sông Hương.', 'Văn hóa cố đô đặc sắc.', '[]', '["Thuyền rồng", "Nghệ nhân biểu diễn", "Hoa đăng"]', '["Ăn tối"]', 150000, 100000, 0, 0, '2 giờ', '19:00', 'Bến Tòa Khâm', 30, 1, 'active', false, false, NOW(), NOW()),
(20, 'Tour Snorkeling Bán Đảo Sơn Trà', 'tour-snorkeling-son-tra', 7, 'Đi tàu gỗ ra các hòn đảo nhỏ quanh bán đảo Sơn Trà để lặn ngắm san hô và câu cá.', 'Khám phá đại dương Sơn Trà.', '[]', '["Tàu gỗ du lịch", "Thiết bị lặn", "Ăn trưa trên tàu"]', '["Dịch vụ tắm nước ngọt"]', 600000, 450000, 100000, 0, '6 giờ', '08:30', 'Cảng Tiên Sa', 25, 4, 'active', false, false, NOW(), NOW());

-- Generate more tours 21-100 (Variations of above with different durations/options)
INSERT INTO tours (id, name, slug, tour_category_id, description, short_desc, price_adult, price_child, price_infant, duration, max_people, min_people, status, created_at, updated_at)
SELECT 
    i, 
    'Tour ' || (CASE WHEN i % 5 = 0 THEN 'Cao Cấp ' WHEN i % 5 = 1 THEN 'Tiết Kiệm ' ELSE 'Khám Phá ' END) || t.name,
    'tour-real-variant-' || i,
    t.tour_category_id,
    'Trải nghiệm ' || (CASE WHEN i % 5 = 0 THEN 'sang trọng ' ELSE 'chuyên sâu ' END) || 'hơn của ' || t.description,
    t.short_desc,
    t.price_adult * (1 + (random() * 0.2)),
    t.price_child * (1 + (random() * 0.1)),
    t.price_infant,
    t.duration,
    t.max_people,
    t.min_people,
    'active',
    NOW(),
    NOW()
FROM generate_series(21, 100) AS i
JOIN tours t ON t.id = (i % 20) + 1;

-- 2. TOUR_SCHEDULES (Target ~200)
INSERT INTO tour_schedules (id, tour_id, start_date, end_date, max_people, booked_people, price_adult, price_child, status, created_at, updated_at)
SELECT 
    i, 
    (i % 100) + 1, 
    CURRENT_DATE + (i / 100 * 7) + (i % 7) + 1, -- Avoid today
    CURRENT_DATE + (i / 100 * 7) + (i % 7) + 1, 
    20, 
    (random() * 5)::int, 
    NULL, 
    NULL, 
    'available', 
    NOW(), 
    NOW()
FROM generate_series(1, 300) AS i;

-- 3. TOUR_LOCATIONS (Pivots)
INSERT INTO tour_locations (tour_id, location_id, created_at) VALUES
(1, 23, NOW()), (1, 31, NOW()), -- Ba Na Hills, APEC Park
(2, 1, NOW()), (2, 3, NOW()), -- Ancient Town, Coconut Forest
(3, 21, NOW()), (3, 20, NOW()), -- Marble Mt, Linh Ung
(4, 13, NOW()), -- Cu Lao Cham
(7, 14, NOW()), (7, 15, NOW()), (7, 16, NOW()), -- Bridges
(12, 22, NOW()); -- Than Tai
-- Randomly link others
INSERT INTO tour_locations (tour_id, location_id, created_at)
SELECT 
    t.id, 
    (random() * 99 + 1)::int, 
    NOW()
FROM tours t
CROSS JOIN generate_series(1, 2)
WHERE t.id > 20
ON CONFLICT DO NOTHING;

-- 4. TOUR_TAGS (Pivots)
INSERT INTO tour_tags (tour_id, tag_id, created_at)
SELECT 
    t.id, 
    (random() * 29 + 1)::int, 
    NOW()
FROM tours t
CROSS JOIN generate_series(1, 3)
ON CONFLICT DO NOTHING;

-- 5. TOUR_AMENITIES (Pivots)
INSERT INTO tour_amenities (tour_id, amenity_id, created_at)
SELECT 
    t.id, 
    (random() * 19 + 1)::int, 
    NOW()
FROM tours t
CROSS JOIN generate_series(1, 3)
ON CONFLICT DO NOTHING;
