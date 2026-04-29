-- DanangTrip Real Data Seeder: Bookings & Payments (100 rows each)
-- FILE: 08_bookings_payments.sql

-- 1. BOOKINGS (Target 100)
INSERT INTO bookings (id, booking_code, user_id, customer_name, customer_email, customer_phone, total_amount, discount_amount, final_amount, deposit_amount, payment_method, payment_status, booking_status, booked_at, created_at, updated_at) VALUES
(1, 'BK20240601001', 3, 'Trần Thu Hà', 'hatran@gmail.com', '0914112233', 2090000, 100000, 1990000, 0, 'vnpay', 'success', 'confirmed', NOW(), NOW(), NOW()),
(2, 'BK20240605002', 6, 'Hoàng Thùy Linh', 'linhht@gmail.com', '0905000111', 640000, 0, 640000, 0, 'momo', 'success', 'confirmed', NOW(), NOW(), NOW());

-- Generate more bookings 3-100
INSERT INTO bookings (id, booking_code, user_id, customer_name, customer_email, customer_phone, total_amount, discount_amount, final_amount, deposit_amount, payment_method, payment_status, booking_status, booked_at, created_at, updated_at)
SELECT 
    i, 
    'BK' || i || 'X', 
    (i % 50) + 1, 
    'Customer ' || i, 
    'customer' || i || '@example.com', 
    '0905' || LPAD(i::text, 6, '0'), 
    1000000, 0, 1000000, 0, 'vnpay', 'success', 'confirmed', NOW(), NOW(), NOW()
FROM generate_series(3, 100) AS i;

-- 2. BOOKING_ITEMS (Target 100)
INSERT INTO booking_items (id, booking_id, tour_id, tour_schedule_id, item_type, item_name, travel_date, quantity_adult, quantity_child, quantity_infant, unit_price_adult, unit_price_child, unit_price_infant, subtotal, status, created_at, updated_at)
SELECT 
    i, 
    i, 
    (i % 50) + 1, 
    i, 
    'tour', 
    'Tour Name ' || i, 
    CURRENT_DATE + 7, 
    2, 0, 0, 
    500000, 300000, 100000, 
    1000000, 
    'pending', 
    NOW(), 
    NOW()
FROM generate_series(1, 100) AS i;

-- 3. PAYMENTS (Target 100)
INSERT INTO payments (id, booking_id, transaction_code, amount, payment_method, payment_status, payment_gateway, paid_at, created_at, updated_at)
SELECT 
    i, 
    i, 
    'TR' || i || 'VNP', 
    1000000, 
    'vnpay', 
    'success', 
    'vnpay', 
    NOW(), 
    NOW(), 
    NOW()
FROM generate_series(1, 100) AS i;
