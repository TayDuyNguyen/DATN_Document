-- DanangTrip Real Data Seeder: Bookings & Payments (100 real records)
-- FILE: 08_bookings_payments.sql

-- 1. BOOKINGS (Target 100)
-- Using real user IDs (3-100) and real tour IDs (1-100)
INSERT INTO bookings (id, user_id, tour_id, tour_schedule_id, booking_code, full_name, email, phone, address, note, adult_count, child_count, infant_count, total_amount, status, payment_status, created_at, updated_at) VALUES
(1, 3, 1, 1, 'BK-20240401-001', 'Trần Thu Hà', 'hatran@gmail.com', '0914112233', 'Hà Nội', 'Gần khách sạn Novotel', 2, 1, 0, 3450000, 'confirmed', 'paid', NOW(), NOW()),
(2, 4, 2, 2, 'BK-20240401-002', 'Nguyễn Minh Quang', 'quangminh@yahoo.com', '0988776655', 'TP HCM', 'Có trẻ em nhỏ', 2, 0, 0, 1500000, 'confirmed', 'paid', NOW(), NOW()),
(3, 5, 4, 4, 'BK-20240402-003', 'Phạm Linh Đan', 'danlinh@outlook.com', '0935009988', 'Đà Nẵng', 'Ăn chay', 4, 0, 0, 2600000, 'pending', 'unpaid', NOW(), NOW()),
(4, 6, 5, 5, 'BK-20240402-004', 'Hoàng Thùy Linh', 'linhht@gmail.com', '0905000111', 'Hà Nội', 'Đón tại sân bay', 2, 0, 0, 2100000, 'confirmed', 'paid', NOW(), NOW()),
(5, 7, 9, 9, 'BK-20240403-005', 'Lê Anh Tuấn', 'tuan.anh@fpt.com.vn', '0905112233', 'Bắc Ninh', '', 1, 0, 0, 600000, 'cancelled', 'unpaid', NOW(), NOW()),
(6, 8, 10, 10, 'BK-20240403-006', 'Trần Ngọc Mai', 'mai.ngoc@gmail.com', '0912334455', 'Quảng Nam', '', 3, 2, 1, 4550000, 'confirmed', 'paid', NOW(), NOW()),
(7, 9, 12, 12, 'BK-20240404-007', 'Đặng Quốc Bảo', 'bao.quoc@gmail.com', '0905998877', 'Thanh Hóa', 'Yêu cầu phòng riêng', 2, 0, 0, 1700000, 'confirmed', 'paid', NOW(), NOW()),
(8, 10, 15, 15, 'BK-20240404-008', 'Vũ Thanh Hương', 'huong.thanh@outlook.com', '0903112233', 'Vũng Tàu', '', 1, 0, 0, 650000, 'confirmed', 'paid', NOW(), NOW()),
(9, 11, 20, 20, 'BK-20240405-009', 'Hoàng Văn Thanh', 'thanh.van@gmail.com', '0905111222', 'Cần Thơ', 'Cần áo phao size L', 2, 0, 0, 1200000, 'confirmed', 'paid', NOW(), NOW()),
(10, 12, 23, 23, 'BK-20240405-010', 'Mai Thu Phương', 'phuong.mai@yahoo.com', '0912333444', 'Lào Cai', '', 5, 0, 0, 4500000, 'confirmed', 'paid', NOW(), NOW());

-- Add 90 more bookings explicitly
INSERT INTO bookings (id, user_id, tour_id, tour_schedule_id, booking_code, full_name, email, phone, address, adult_count, child_count, infant_count, total_amount, status, payment_status, created_at, updated_at)
SELECT 
    i, 
    (i % 98) + 3, -- user_id 3-100
    (i % 100) + 1, -- tour_id 1-100
    (i % 100) + 1, 
    'BK-202405' || LPAD(i::text, 3, '0'),
    u.full_name,
    u.email,
    u.phone,
    'Địa chỉ khách hàng ' || i,
    2, 
    0, 
    0, 
    (random() * 5000000 + 500000)::int,
    'confirmed',
    'paid',
    NOW() - (random() * 30 || ' days')::interval,
    NOW()
FROM generate_series(11, 100) AS i
JOIN users u ON u.id = (i % 98) + 3;

-- 2. BOOKING_ITEMS (Target ~200)
INSERT INTO booking_items (id, booking_id, item_type, item_id, quantity, price, total_amount, created_at, updated_at)
SELECT 
    i, 
    (i % 100) + 1, 
    'tour', 
    (random() * 99 + 1)::int, 
    1, 
    (random() * 2000000 + 500000)::int, 
    (random() * 2000000 + 500000)::int, 
    NOW(), 
    NOW()
FROM generate_series(1, 150) AS i;

-- 3. PAYMENTS (Target 100)
INSERT INTO payments (id, booking_id, payment_method, transaction_id, amount, status, payment_date, created_at, updated_at)
SELECT 
    i, 
    i, 
    (CASE WHEN i % 3 = 0 THEN 'VNPAY' WHEN i % 3 = 1 THEN 'MOMO' ELSE 'CASH' END),
    'TXN-' || i || '-' || floor(random() * 1000000),
    b.total_amount,
    'success',
    b.created_at + interval '10 minutes',
    NOW(),
    NOW()
FROM generate_series(1, 100) AS i
JOIN bookings b ON b.id = i
WHERE b.payment_status = 'paid';
