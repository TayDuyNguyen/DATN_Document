-- DanangTrip Real Data Seeder: Bookings, Items & Payments
-- Source: Simulated based on Vietnam Travel Trends 2024 (Outbox Consulting, Vietravel)
-- Retrieved Date: 2026-04-29

-- BOOKING_LOOKUP
-- 1: DT-240501-001 (User 3 - Huy Le)
-- 2: DT-240501-002 (User 4 - Mai Pham)
-- 3: DT-240502-001 (User 7 - Khoa Phan)

INSERT INTO bookings (id, booking_code, user_id, customer_name, customer_email, customer_phone, customer_address, note, total_amount, deposit_amount, payment_method, payment_status, booking_status, created_at, updated_at) VALUES
(1, 'DT-240501-001', 3, 'Lê Minh Huy', 'huy.le@gmail.com', '0321456789', 'Hồ Chí Minh', 'Đón tại khách sạn Novotel.', 2420000.00, 1210000.00, 'vnpay_qr', 'partially_paid', 'confirmed', '2024-04-28 10:00:00', NOW()),
(2, 'DT-240501-002', 4, 'Phạm Ngọc Mai', 'mai.pham@yahoo.com', '0702345678', 'Đà Nẵng', 'Yêu cầu món chay cho bữa trưa.', 900000.00, 900000.00, 'momo', 'paid', 'confirmed', '2024-04-29 08:30:00', NOW()),
(3, 'DT-240502-001', 7, 'Phan Trọng Khoa', 'khoa.phan@hotmail.com', '0966778899', 'Đà Nẵng', NULL, 1300000.00, 0.00, 'bank_transfer', 'unpaid', 'pending', '2024-04-29 14:00:00', NOW()),
(4, 'DT-240502-002', NULL, 'Nguyễn Văn B', 'b.nguyen@test.com', '0988776655', 'Hà Nội', 'Khách vãng lai.', 650000.00, 650000.00, 'vnpay_qr', 'paid', 'completed', '2024-04-25 09:00:00', NOW());

INSERT INTO booking_items (id, booking_id, tour_id, tour_schedule_id, quantity_adult, quantity_child, quantity_infant, unit_price_adult, unit_price_child, unit_price_infant, subtotal, travel_date, status, created_at, updated_at) VALUES
(1, 1, 1, 1, 2, 0, 0, 1210000.00, 950000.00, 0.00, 2420000.00, '2024-05-01', 'confirmed', '2024-04-28 10:00:00', NOW()),
(2, 2, 2, 4, 2, 0, 0, 450000.00, 225000.00, 0.00, 900000.00, '2024-05-01', 'confirmed', '2024-04-29 08:30:00', NOW()),
(3, 3, 3, 6, 2, 0, 0, 650000.00, 325000.00, 100000.00, 1300000.00, '2024-05-01', 'pending', '2024-04-29 14:00:00', NOW()),
(4, 4, 3, 6, 1, 0, 0, 650000.00, 325000.00, 100000.00, 650000.00, '2024-04-27', 'completed', '2024-04-25 09:00:00', NOW());

INSERT INTO payments (id, booking_id, transaction_code, amount, payment_status, gateway, paid_at, gateway_response, created_at, updated_at) VALUES
(1, 1, 'VNP202404281005', 1210000.00, 'success', 'vnpay', '2024-04-28 10:05:00', '{"status": "00", "msg": "Success"}', NOW(), NOW()),
(2, 2, 'MM202404290835', 900000.00, 'success', 'momo', '2024-04-29 08:35:00', '{"status": 0, "msg": "Successful"}', NOW(), NOW()),
(4, 4, 'VNP202404250910', 650000.00, 'success', 'vnpay', '2024-04-25 09:10:00', '{"status": "00", "msg": "Success"}', NOW(), NOW());
