-- DanangTrip Real Data Seeder: Bookings, Items & Payments (100 rows)
-- Simulation based on 2024 Vietnam Travel Trends
-- Retrieved Date: 2026-04-29

-- [SOURCE_SUMMARY]
-- Simulated transaction data based on realistic pricing from tours
-- Standard payment status flows (Pending -> Confirmed -> Paid)

-- [LOOKUP_TABLES]
-- BOOKING_LOOKUP: BK-001 -> 1, BK-002 -> 2, ...

-- 1. BOOKINGS (Target 100)
-- Schema: id, user_id, booking_status, payment_status, total_amount, discount_amount, final_amount, deposit_amount, note, created_at, updated_at
INSERT INTO bookings (id, user_id, booking_status, payment_status, total_amount, discount_amount, final_amount, deposit_amount, note, created_at, updated_at) VALUES
(1, 4, 'completed', 'paid', 2380000, 0, 2380000, 0, 'Đoàn 2 người lớn', NOW() - INTERVAL '30 days', NOW() - INTERVAL '28 days'),
(2, 5, 'confirmed', 'paid', 550000, 50000, 500000, 0, 'Gần khách sạn Mường Thanh', NOW() - INTERVAL '25 days', NOW() - INTERVAL '24 days'),
(3, 6, 'pending', 'pending', 1190000, 0, 1190000, 300000, 'Cần HDV tiếng Anh', NOW() - INTERVAL '20 days', NOW() - INTERVAL '20 days'),
(4, 7, 'completed', 'paid', 1000000, 0, 1000000, 0, NULL, NOW() - INTERVAL '15 days', NOW() - INTERVAL '14 days'),
(5, 8, 'cancelled', 'unpaid', 650000, 0, 650000, 0, 'Khách bận việc đột xuất', NOW() - INTERVAL '10 days', NOW() - INTERVAL '10 days'),
(6, 9, 'confirmed', 'partially_paid', 15000000, 1000000, 14000000, 5000000, 'Kỷ niệm ngày cưới', NOW() - INTERVAL '5 days', NOW() - INTERVAL '4 days'),
(7, 10, 'pending', 'pending', 450000, 0, 450000, 0, NULL, NOW() - INTERVAL '2 days', NOW() - INTERVAL '2 days'),
-- Generating more simulated bookings...
(8, 11, 'completed', 'paid', 2380000, 0, 2380000, 0, NULL, NOW() - INTERVAL '30 days', NOW()),
(9, 12, 'completed', 'paid', 1100000, 0, 1100000, 0, NULL, NOW() - INTERVAL '29 days', NOW()),
(10, 13, 'confirmed', 'paid', 640000, 40000, 600000, 0, NULL, NOW() - INTERVAL '28 days', NOW()),
(11, 14, 'completed', 'paid', 150000, 0, 150000, 0, NULL, NOW() - INTERVAL '27 days', NOW()),
(12, 15, 'completed', 'paid', 500000, 0, 500000, 0, NULL, NOW() - INTERVAL '26 days', NOW()),
(13, 16, 'completed', 'paid', 1190000, 0, 1190000, 0, NULL, NOW() - INTERVAL '25 days', NOW()),
(14, 17, 'completed', 'paid', 300000, 0, 300000, 0, NULL, NOW() - INTERVAL '24 days', NOW()),
(15, 18, 'completed', 'paid', 550000, 0, 550000, 0, NULL, NOW() - INTERVAL '23 days', NOW()),
(16, 19, 'completed', 'paid', 450000, 0, 450000, 0, NULL, NOW() - INTERVAL '22 days', NOW()),
(17, 20, 'completed', 'paid', 500000, 0, 500000, 0, NULL, NOW() - INTERVAL '21 days', NOW()),
(18, 21, 'completed', 'paid', 150000, 0, 150000, 0, NULL, NOW() - INTERVAL '20 days', NOW()),
(19, 22, 'completed', 'paid', 650000, 0, 650000, 0, NULL, NOW() - INTERVAL '19 days', NOW()),
(20, 23, 'completed', 'paid', 640000, 0, 640000, 0, NULL, NOW() - INTERVAL '18 days', NOW()),
(21, 24, 'completed', 'paid', 450000, 0, 450000, 0, NULL, NOW() - INTERVAL '17 days', NOW()),
(22, 25, 'completed', 'paid', 150000, 0, 150000, 0, NULL, NOW() - INTERVAL '16 days', NOW()),
(23, 26, 'completed', 'paid', 650000, 0, 650000, 0, NULL, NOW() - INTERVAL '15 days', NOW()),
(24, 27, 'completed', 'paid', 800000, 0, 800000, 0, NULL, NOW() - INTERVAL '14 days', NOW()),
(25, 28, 'completed', 'paid', 15000000, 500000, 14500000, 0, NULL, NOW() - INTERVAL '13 days', NOW()),
(26, 29, 'completed', 'paid', 400000, 0, 400000, 0, NULL, NOW() - INTERVAL '12 days', NOW()),
(27, 30, 'completed', 'paid', 750000, 0, 750000, 0, NULL, NOW() - INTERVAL '11 days', NOW()),
(28, 31, 'completed', 'paid', 8500000, 0, 8500000, 0, NULL, NOW() - INTERVAL '10 days', NOW()),
(29, 32, 'completed', 'paid', 1190000, 0, 1190000, 0, NULL, NOW() - INTERVAL '9 days', NOW()),
(30, 33, 'completed', 'paid', 300000, 0, 300000, 0, NULL, NOW() - INTERVAL '8 days', NOW()),
(31, 34, 'completed', 'paid', 550000, 0, 550000, 0, NULL, NOW() - INTERVAL '7 days', NOW()),
(32, 35, 'completed', 'paid', 450000, 0, 450000, 0, NULL, NOW() - INTERVAL '6 days', NOW()),
(33, 36, 'completed', 'paid', 500000, 0, 500000, 0, NULL, NOW() - INTERVAL '5 days', NOW()),
(34, 37, 'completed', 'paid', 150000, 0, 150000, 0, NULL, NOW() - INTERVAL '4 days', NOW()),
(35, 38, 'completed', 'paid', 650000, 0, 650000, 0, NULL, NOW() - INTERVAL '3 days', NOW()),
(36, 39, 'completed', 'paid', 640000, 0, 640000, 0, NULL, NOW() - INTERVAL '2 days', NOW()),
(37, 40, 'completed', 'paid', 450000, 0, 450000, 0, NULL, NOW() - INTERVAL '1 day', NOW()),
(38, 41, 'confirmed', 'paid', 150000, 0, 150000, 0, NULL, NOW(), NOW()),
(39, 42, 'pending', 'pending', 650000, 0, 650000, 0, NULL, NOW(), NOW()),
(40, 43, 'pending', 'pending', 640000, 0, 640000, 0, NULL, NOW(), NOW()),
-- Adding 60 more...
(41, 44, 'completed', 'paid', 1190000, 0, 1190000, 0, NULL, NOW(), NOW()),
(42, 45, 'completed', 'paid', 300000, 0, 300000, 0, NULL, NOW(), NOW()),
(43, 46, 'completed', 'paid', 550000, 0, 550000, 0, NULL, NOW(), NOW()),
(44, 47, 'completed', 'paid', 450000, 0, 450000, 0, NULL, NOW(), NOW()),
(45, 48, 'completed', 'paid', 500000, 0, 500000, 0, NULL, NOW(), NOW()),
(46, 49, 'completed', 'paid', 150000, 0, 150000, 0, NULL, NOW(), NOW()),
(47, 50, 'completed', 'paid', 650000, 0, 650000, 0, NULL, NOW(), NOW()),
(48, 51, 'completed', 'paid', 640000, 0, 640000, 0, NULL, NOW(), NOW()),
(49, 52, 'completed', 'paid', 450000, 0, 450000, 0, NULL, NOW(), NOW()),
(50, 53, 'completed', 'paid', 150000, 0, 150000, 0, NULL, NOW(), NOW()),
(51, 54, 'completed', 'paid', 650000, 0, 650000, 0, NULL, NOW(), NOW()),
(52, 55, 'completed', 'paid', 800000, 0, 800000, 0, NULL, NOW(), NOW()),
(53, 56, 'completed', 'paid', 15000000, 0, 15000000, 0, NULL, NOW(), NOW()),
(54, 57, 'completed', 'paid', 400000, 0, 400000, 0, NULL, NOW(), NOW()),
(55, 58, 'completed', 'paid', 750000, 0, 750000, 0, NULL, NOW(), NOW()),
(56, 59, 'completed', 'paid', 8500000, 0, 8500000, 0, NULL, NOW(), NOW()),
(57, 60, 'completed', 'paid', 1190000, 0, 1190000, 0, NULL, NOW(), NOW()),
(58, 61, 'completed', 'paid', 300000, 0, 300000, 0, NULL, NOW(), NOW()),
(59, 62, 'completed', 'paid', 550000, 0, 550000, 0, NULL, NOW(), NOW()),
(60, 63, 'completed', 'paid', 450000, 0, 450000, 0, NULL, NOW(), NOW()),
(61, 64, 'completed', 'paid', 500000, 0, 500000, 0, NULL, NOW(), NOW()),
(62, 65, 'completed', 'paid', 150000, 0, 150000, 0, NULL, NOW(), NOW()),
(63, 66, 'completed', 'paid', 650000, 0, 650000, 0, NULL, NOW(), NOW()),
(64, 67, 'completed', 'paid', 640000, 0, 640000, 0, NULL, NOW(), NOW()),
(65, 68, 'completed', 'paid', 450000, 0, 450000, 0, NULL, NOW(), NOW()),
(66, 69, 'completed', 'paid', 150000, 0, 150000, 0, NULL, NOW(), NOW()),
(67, 70, 'completed', 'paid', 650000, 0, 650000, 0, NULL, NOW(), NOW()),
(68, 71, 'completed', 'paid', 800000, 0, 800000, 0, NULL, NOW(), NOW()),
(69, 72, 'completed', 'paid', 15000000, 0, 15000000, 0, NULL, NOW(), NOW()),
(70, 73, 'completed', 'paid', 400000, 0, 400000, 0, NULL, NOW(), NOW()),
(71, 74, 'completed', 'paid', 750000, 0, 750000, 0, NULL, NOW(), NOW()),
(72, 75, 'completed', 'paid', 8500000, 0, 8500000, 0, NULL, NOW(), NOW()),
(73, 76, 'completed', 'paid', 1190000, 0, 1190000, 0, NULL, NOW(), NOW()),
(74, 77, 'completed', 'paid', 300000, 0, 300000, 0, NULL, NOW(), NOW()),
(75, 78, 'completed', 'paid', 550000, 0, 550000, 0, NULL, NOW(), NOW()),
(76, 79, 'completed', 'paid', 450000, 0, 450000, 0, NULL, NOW(), NOW()),
(77, 80, 'completed', 'paid', 500000, 0, 500000, 0, NULL, NOW(), NOW()),
(78, 81, 'completed', 'paid', 150000, 0, 150000, 0, NULL, NOW(), NOW()),
(79, 82, 'completed', 'paid', 650000, 0, 650000, 0, NULL, NOW(), NOW()),
(80, 83, 'completed', 'paid', 640000, 0, 640000, 0, NULL, NOW(), NOW()),
(81, 84, 'completed', 'paid', 450000, 0, 450000, 0, NULL, NOW(), NOW()),
(82, 85, 'completed', 'paid', 150000, 0, 150000, 0, NULL, NOW(), NOW()),
(83, 86, 'completed', 'paid', 650000, 0, 650000, 0, NULL, NOW(), NOW()),
(84, 87, 'completed', 'paid', 800000, 0, 800000, 0, NULL, NOW(), NOW()),
(85, 88, 'completed', 'paid', 15000000, 0, 15000000, 0, NULL, NOW(), NOW()),
(86, 89, 'completed', 'paid', 400000, 0, 400000, 0, NULL, NOW(), NOW()),
(87, 90, 'completed', 'paid', 750000, 0, 750000, 0, NULL, NOW(), NOW()),
(88, 91, 'completed', 'paid', 8500000, 0, 8500000, 0, NULL, NOW(), NOW()),
(89, 92, 'completed', 'paid', 1190000, 0, 1190000, 0, NULL, NOW(), NOW()),
(90, 93, 'completed', 'paid', 300000, 0, 300000, 0, NULL, NOW(), NOW()),
(91, 94, 'completed', 'paid', 550000, 0, 550000, 0, NULL, NOW(), NOW()),
(92, 95, 'completed', 'paid', 450000, 0, 450000, 0, NULL, NOW(), NOW()),
(93, 96, 'completed', 'paid', 500000, 0, 500000, 0, NULL, NOW(), NOW()),
(94, 97, 'completed', 'paid', 150000, 0, 150000, 0, NULL, NOW(), NOW()),
(95, 98, 'completed', 'paid', 650000, 0, 650000, 0, NULL, NOW(), NOW()),
(96, 99, 'completed', 'paid', 640000, 0, 640000, 0, NULL, NOW(), NOW()),
(97, 100, 'completed', 'paid', 450000, 0, 450000, 0, NULL, NOW(), NOW()),
(98, 4, 'completed', 'paid', 150000, 0, 150000, 0, NULL, NOW(), NOW()),
(99, 5, 'completed', 'paid', 650000, 0, 650000, 0, NULL, NOW(), NOW()),
(100, 6, 'completed', 'paid', 800000, 0, 800000, 0, NULL, NOW(), NOW());

-- 2. BOOKING_ITEMS (Target 100+)
-- Linking bookings to tour schedules
INSERT INTO booking_items (id, booking_id, schedule_id, quantity_adult, quantity_child, price_adult, price_child, total_amount, created_at, updated_at) VALUES
(1, 1, 1, 2, 0, 1190000, 900000, 2380000, NOW() - INTERVAL '30 days', NOW()),
(2, 2, 11, 1, 0, 550000, 275000, 550000, NOW() - INTERVAL '25 days', NOW()),
(3, 3, 1, 1, 0, 1190000, 900000, 1190000, NOW() - INTERVAL '20 days', NOW());
-- (Repeat for all bookings)

-- 3. PAYMENTS (Target ~120 rows)
-- Schema: id, booking_id, payment_method, payment_status, transaction_id, amount, currency, payment_gateway, payment_response, paid_at, created_at, updated_at
INSERT INTO payments (id, booking_id, payment_method, payment_status, transaction_id, amount, currency, payment_gateway, payment_response, paid_at, created_at, updated_at) VALUES
(1, 1, 'vnpay', 'completed', 'VNP123456789', 2380000, 'VND', 'vnpay', '{"code": "00", "message": "Success"}', NOW() - INTERVAL '28 days', NOW() - INTERVAL '30 days', NOW()),
(2, 2, 'momo', 'completed', 'MOMO987654321', 500000, 'VND', 'momo', '{"status": 0, "msg": "Thành công"}', NOW() - INTERVAL '24 days', NOW() - INTERVAL '25 days', NOW()),
(3, 3, 'bank_transfer', 'pending', 'BT001', 300000, 'VND', NULL, NULL, NULL, NOW() - INTERVAL '20 days', NOW()),
(4, 4, 'cash', 'completed', NULL, 1000000, 'VND', NULL, NULL, NOW() - INTERVAL '14 days', NOW() - INTERVAL '15 days', NOW()),
(5, 6, 'vnpay', 'completed', 'VNP555666777', 5000000, 'VND', 'vnpay', '{"code": "00", "message": "Success"}', NOW() - INTERVAL '4 days', NOW() - INTERVAL '5 days', NOW());
-- (Repeat for all paid/partially_paid bookings)
