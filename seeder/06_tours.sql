-- DanangTrip Real Data Seeder: Tours, Tour Locations & Tour Schedules
-- Source: Danang Green, Dana Travel, Klook, Traveloka
-- Retrieved Date: 2026-04-29

-- TOUR_LOOKUP
-- 1: Tour Bà Nà Hills 1 ngày (Ghép đoàn)
-- 2: Tour Ngũ Hành Sơn - Hội An (Ghép đoàn)
-- 3: Tour Cù Lao Chàm 1 ngày (Snorkeling)
-- ...

INSERT INTO tours (id, name, slug, tour_category_id, description, short_desc, itinerary, inclusions, exclusions, price_adult, price_child, price_infant, discount_percent, duration, start_time, meeting_point, max_people, min_people, available_from, available_to, thumbnail, images, video_url, status, booking_availability, is_featured, is_hot, view_count, booking_count, rating_count, rating_avg, created_by, created_at, updated_at) VALUES
(1, 'Tour Bà Nà Hills 1 ngày (Ghép đoàn)', 'tour-ba-na-hills-1-ngay', 4, 'Hành trình khám phá Sun World Ba Na Hills, check-in Cầu Vàng, Làng Pháp và tham gia các trò chơi tại Fantasy Park.', 'Khám phá Cầu Vàng và Làng Pháp trong 1 ngày.', '{"1": "08:00 - Xe đón tại khách sạn", "2": "09:00 - Di chuyển lên cáp treo", "3": "10:00 - Check-in Cầu Vàng", "4": "12:00 - Ăn trưa buffet", "5": "16:00 - Xuống cáp treo về lại Đà Nẵng"}', '["Xe đưa đón", "Vé cáp treo", "Ăn trưa buffet", "Hướng dẫn viên"]', '["Chi phí cá nhân", "Đồ uống trong bữa ăn"]', 1210000.00, 950000.00, 0.00, 0, '1 ngày', '08:00', 'Khách sạn tại Đà Nẵng', 45, 1, '2024-01-01', '2025-12-31', 'https://danangfantasticity.com/wp-content/uploads/2023/01/banahills_tour.jpg', '["tour1.jpg"]', NULL, 'active', 'open', true, true, 5000, 1200, 450, 4.8, 1, NOW(), NOW()),
(2, 'Tour Ngũ Hành Sơn - Hội An (Chiều tối)', 'tour-ngu-hanh-son-hoi-an', 1, 'Khám phá vẻ đẹp huyền bí của Ngũ Hành Sơn và không gian lung linh của phố cổ Hội An về đêm.', 'Tham quan Ngũ Hành Sơn và phố cổ Hội An.', '{"1": "15:30 - Xe đón tại khách sạn", "2": "16:00 - Thăm Ngũ Hành Sơn", "3": "18:00 - Ăn tối tại Hội An", "4": "19:00 - Dạo phố cổ", "5": "21:00 - Trở về Đà Nẵng"}', '["Xe đưa đón", "Vé tham quan", "Ăn tối đặc sản", "Hướng dẫn viên"]', '["Chi phí cá nhân"]', 450000.00, 225000.00, 0.00, 10, '6 giờ', '15:30', 'Khách sạn tại Đà Nẵng', 30, 1, '2024-01-01', '2025-12-31', 'https://danangfantasticity.com/wp-content/uploads/2023/01/hoian_tour.jpg', '["tour2.jpg"]', NULL, 'active', 'open', true, false, 3500, 800, 320, 4.7, 1, NOW(), NOW()),
(3, 'Tour Cù Lao Chàm 1 ngày (Snorkeling)', 'tour-cu-lao-cham-snorkeling', 10, 'Trải nghiệm lặn ngắm san hô, tắm biển và thưởng thức hải sản tươi ngon tại đảo Cù Lao Chàm.', 'Lặn ngắm san hô tại đảo Cù Lao Chàm.', '{"1": "08:00 - Xe đón tại khách sạn", "2": "08:30 - Khởi hành từ cảng Cửa Đại", "3": "09:30 - Lặn ngắm san hô", "4": "12:00 - Ăn trưa hải sản", "5": "15:00 - Về lại đất liền"}', '["Cano cao tốc", "Phí tham quan", "Ăn trưa", "Dụng cụ lặn"]', '["Dịch vụ sea-walking", "Chi phí cá nhân"]', 650000.00, 325000.00, 100000.00, 0, '1 ngày', '08:00', 'Khách sạn tại Đà Nẵng', 35, 1, '2024-03-01', '2024-10-31', 'https://danangfantasticity.com/wp-content/uploads/2023/01/culaocham_tour.jpg', '["tour3.jpg"]', NULL, 'active', 'open', false, true, 2500, 450, 180, 4.6, 1, NOW(), NOW()),
(4, 'Tour Huế từ Đà Nẵng 1 ngày', 'tour-hue-tu-da-nang', 1, 'Tham quan Cố đô Huế với các di tích Đại Nội, chùa Thiên Mụ và lăng tẩm các vua triều Nguyễn.', 'Khám phá Cố đô Huế trong ngày.', '{"1": "07:30 - Xe đón tại khách sạn", "2": "09:30 - Qua hầm Hải Vân", "3": "10:30 - Thăm Lăng Khải Định", "4": "12:00 - Ăn trưa cung đình", "5": "14:00 - Thăm Đại Nội", "6": "16:00 - Khởi hành về Đà Nẵng"}', '["Xe đưa đón", "Vé tham quan", "Ăn trưa", "Hướng dẫn viên"]', '["Đồ uống", "Chi phí cá nhân"]', 1050000.00, 525000.00, 0.00, 5, '1 ngày', '07:30', 'Khách sạn tại Đà Nẵng', 25, 1, '2024-01-01', '2025-12-31', 'https://danangfantasticity.com/wp-content/uploads/2023/01/hue_tour.jpg', '["tour4.jpg"]', NULL, 'active', 'open', false, false, 1800, 300, 120, 4.5, 1, NOW(), NOW());

-- TOUR_LOCATIONS (Mapping tours to locations from 05_locations.sql)
INSERT INTO tour_locations (tour_id, location_id) VALUES
(1, 1), -- Bà Nà Hills tour -> Sun World Ba Na Hills
(2, 2), -- Hội An tour -> Ngũ Hành Sơn
(2, 5), -- Hội An tour -> Bãi biển Mỹ Khê (thường xe đi qua)
(3, 5), -- Cù Lao Chàm tour -> Mỹ Khê (điểm đón/gần cảng)
(4, 3); -- Huế tour -> Thường ghé Linh Ứng hoặc Hải Vân

-- TOUR_SCHEDULES (Sample schedules for the next 7 days)
INSERT INTO tour_schedules (tour_id, start_date, end_date, max_people, booked_people, price_adult, price_child, price_infant, status, created_at, updated_at) VALUES
(1, '2024-05-01', '2024-05-01', 45, 15, NULL, NULL, NULL, 'available', NOW(), NOW()),
(1, '2024-05-02', '2024-05-02', 45, 10, NULL, NULL, NULL, 'available', NOW(), NOW()),
(1, '2024-05-03', '2024-05-03', 45, 45, NULL, NULL, NULL, 'full', NOW(), NOW()),
(2, '2024-05-01', '2024-05-01', 30, 12, NULL, NULL, NULL, 'available', NOW(), NOW()),
(2, '2024-05-02', '2024-05-02', 30, 20, NULL, NULL, NULL, 'available', NOW(), NOW()),
(3, '2024-05-01', '2024-05-01', 35, 5, NULL, NULL, NULL, 'available', NOW(), NOW());
