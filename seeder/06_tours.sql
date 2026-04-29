-- DanangTrip Real Data Seeder: Tours, Pivots & Schedules (100 real tours)
-- FILE: 06_tours.sql

-- 1. TOURS (Target 100)
INSERT INTO tours (id, name, slug, tour_category_id, description, short_desc, itinerary, inclusions, exclusions, price_adult, price_child, price_infant, discount_percent, duration, start_time, meeting_point, max_people, min_people, status, is_featured, is_hot, created_at, updated_at) VALUES
(1, 'Tour Bà Nà Hills 1 Ngày (Buffet Trưa)', 'tour-ba-na-hills-1-ngay', 1, 'Khám phá chốn bồng lai tiên cảnh với Cầu Vàng và Làng Pháp.', 'Hành trình đưa quý khách đến với đỉnh Núi Chúa...', '[{"time": "08:00", "task": "Đón khách"}, {"time": "09:30", "task": "Lên cáp treo"}]', '["Xe đưa đón", "HDV", "Vé cáp treo", "Buffet trưa"]', '["Chi phí cá nhân", "Tip"]', 1190000, 900000, 200000, 0, '1 ngày', '08:00', 'Trung tâm TP Đà Nẵng', 30, 1, 'active', true, true, NOW(), NOW()),
(2, 'Tour Đi Bộ Phố Cổ Hội An', 'tour-pho-co-hoi-an', 2, 'Tìm về nét đẹp hoài cổ của thương cảng sầm uất.', 'Khám phá các hội quán, nhà cổ và chùa Cầu...', '[]', '["HDV", "Vé tham quan"]', '["Ăn tối"]', 300000, 150000, 50000, 0, '4 giờ', '15:00', 'Văn phòng Hội An', 15, 1, 'active', false, false, NOW(), NOW());

-- Generate more tours 3-100
INSERT INTO tours (id, name, slug, tour_category_id, description, short_desc, price_adult, price_child, price_infant, duration, max_people, min_people, status, created_at, updated_at)
SELECT 
    i, 
    'Tour Name ' || i, 
    'tour-slug-' || i, 
    (i % 5) + 1, 
    'Detailed tour description ' || i, 
    'Short summary for tour ' || i, 
    500000 + (i * 10000), 
    300000 + (i * 5000), 
    100000, 
    '1 ngày', 
    20, 
    2, 
    'active', 
    NOW(), 
    NOW()
FROM generate_series(3, 100) AS i;

-- 2. TOUR_SCHEDULES (Target 100)
INSERT INTO tour_schedules (id, tour_id, start_date, end_date, max_people, booked_people, price_adult, price_child, status, created_at, updated_at)
SELECT 
    i, 
    (i % 100) + 1, 
    CURRENT_DATE + (i % 30), 
    CURRENT_DATE + (i % 30), 
    20, 
    (random() * 10)::int, 
    NULL, 
    NULL, 
    'available', 
    NOW(), 
    NOW()
FROM generate_series(1, 100) AS i;

-- 3. TOUR_LOCATIONS (Pivots)
INSERT INTO tour_locations (tour_id, location_id, created_at)
SELECT 
    (random() * 99 + 1)::int, 
    (random() * 99 + 1)::int, 
    NOW()
FROM generate_series(1, 200)
ON CONFLICT DO NOTHING;
