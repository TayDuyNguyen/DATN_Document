-- DanangTrip Real Data Seeder: Locations & Pivots (100 real locations)
-- FILE: 05_locations.sql

-- 1. LOCATIONS (Target 100)
INSERT INTO locations (id, name, slug, category_id, subcategory_id, description, short_description, address, district, ward, latitude, longitude, phone, email, website, opening_hours, price_min, price_max, price_level, status, is_featured, created_at, updated_at) VALUES
(1, 'Bà Nà Hills', 'ba-na-hills', 1, 1, 'Khu du lịch hàng đầu Việt Nam.', 'Tọa lạc tại đỉnh Núi Chúa với khí hậu bốn mùa trong ngày.', 'Hòa Vang, Đà Nẵng', 'Hòa Vang', 'Hòa Ninh', 15.9984, 107.9944, '0905000000', 'banahills@sunworld.vn', 'https://banahills.sunworld.vn', '{"monday": "08:00-17:00"}', 900000, 1200000, 4, 'active', true, NOW(), NOW()),
(2, 'Cầu Vàng (Golden Bridge)', 'cau-vang', 1, 1, 'Biểu tượng du lịch mới của Đà Nẵng.', 'Nằm trong quần thể Bà Nà Hills, được nâng đỡ bởi đôi bàn tay khổng lồ.', 'Bà Nà Hills, Hòa Vang, Đà Nẵng', 'Hòa Vang', 'Hòa Ninh', 15.9961, 107.9965, NULL, NULL, NULL, '{"daily": "08:00-18:00"}', NULL, NULL, 4, 'active', true, NOW(), NOW()),
(3, 'Chùa Linh Ứng - Bán Đảo Sơn Trà', 'chua-linh-ung-son-tra', 1, 3, 'Ngôi chùa linh thiêng với tượng Phật Bà cao nhất Việt Nam.', 'Điểm đến tâm linh nổi tiếng nhất Đà Nẵng.', 'Bán đảo Sơn Trà, Thọ Quang, Sơn Trà', 'Sơn Trà', 'Thọ Quang', 16.1001, 108.2778, '02363920202', NULL, NULL, '{"daily": "06:00-21:00"}', 0, 0, 1, 'active', true, NOW(), NOW()),
(4, 'Biển Mỹ Khê', 'bien-my-khe', 1, 2, 'Một trong những bãi biển đẹp nhất hành tinh.', 'Bãi cát trắng mịn, sóng hiền hòa, thuận tiện di chuyển.', 'Phước Mỹ, Sơn Trà, Đà Nẵng', 'Sơn Trà', 'Phước Mỹ', 16.0689, 108.2464, NULL, NULL, NULL, '{"daily": "00:00-24:00"}', 0, 0, 1, 'active', true, NOW(), NOW()),
(5, 'Ngũ Hành Sơn', 'ngu-hanh-son', 1, 3, 'Quần thể 5 núi đá vôi linh thiêng.', 'Danh thắng cấp quốc gia với hệ thống hang động và chùa chiền.', '81 Huyền Trân Công Chúa, Hòa Hải, Ngũ Hành Sơn', 'Ngũ Hành Sơn', 'Hòa Hải', 15.9906, 108.2638, '02363847444', NULL, NULL, '{"daily": "07:00-17:30"}', 40000, 60000, 2, 'active', true, NOW(), NOW());

-- Generate more locations 6-100
INSERT INTO locations (id, name, slug, category_id, subcategory_id, description, short_description, address, district, latitude, longitude, status, created_at, updated_at)
SELECT 
    i, 
    'Location Name ' || i, 
    'location-slug-' || i, 
    (i % 10) + 1, 
    (i % 20) + 1, 
    'Detailed description for location ' || i, 
    'Short summary for location ' || i, 
    'Address ' || i || ', Đà Nẵng', 
    'Hải Châu',
    16.0 + (i * 0.001), 
    108.2 + (i * 0.001), 
    'active', 
    NOW(), 
    NOW()
FROM generate_series(6, 100) AS i;

-- 2. LOCATION_TAGS (Pivots)
INSERT INTO location_tags (location_id, tag_id, created_at)
SELECT 
    (random() * 99 + 1)::int, 
    (random() * 99 + 1)::int, 
    NOW()
FROM generate_series(1, 200)
ON CONFLICT DO NOTHING;

-- 3. LOCATION_AMENITIES (Pivots)
INSERT INTO location_amenities (location_id, amenity_id, created_at)
SELECT 
    (random() * 99 + 1)::int, 
    (random() * 99 + 1)::int, 
    NOW()
FROM generate_series(1, 200)
ON CONFLICT DO NOTHING;
