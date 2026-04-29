-- DanangTrip Real Data Seeder: Bookings, Booking Items & Payments
-- Normalized to current schema (bookings/booking_items/payments)

INSERT INTO bookings (
    id, booking_code, user_id, customer_name, customer_email, customer_phone, customer_address, customer_note,
    total_amount, discount_amount, final_amount, deposit_amount,
    payment_method, payment_status, booking_status, booked_at, created_at, updated_at
) VALUES
(1, 'DT-240501-001', 3, 'Le Minh Huy', 'huy.le@gmail.com', '0321456789', 'Ho Chi Minh', 'Don tai khach san Novotel.', 2420000.00, 0.00, 2420000.00, 1210000.00, 'vnpay_qr', 'partially_paid', 'confirmed', '2024-04-28 10:00:00', '2024-04-28 10:00:00', NOW()),
(2, 'DT-240501-002', 4, 'Pham Ngoc Mai', 'mai.pham@yahoo.com', '0702345678', 'Da Nang', 'Yeu cau mon chay cho bua trua.', 900000.00, 0.00, 900000.00, 900000.00, 'momo', 'success', 'confirmed', '2024-04-29 08:30:00', '2024-04-29 08:30:00', NOW()),
(3, 'DT-240502-001', 7, 'Phan Trong Khoa', 'khoa.phan@hotmail.com', '0966778899', 'Da Nang', NULL, 1300000.00, 0.00, 1300000.00, 0.00, 'bank_transfer', 'unpaid', 'pending', '2024-04-29 14:00:00', '2024-04-29 14:00:00', NOW()),
(4, 'DT-240502-002', NULL, 'Nguyen Van B', 'b.nguyen@test.com', '0988776655', 'Ha Noi', 'Khach vang lai.', 650000.00, 0.00, 650000.00, 650000.00, 'vnpay_qr', 'success', 'completed', '2024-04-25 09:00:00', '2024-04-25 09:00:00', NOW());

INSERT INTO booking_items (
    id, booking_id, tour_id, tour_schedule_id, item_type, item_name, travel_date,
    quantity_adult, quantity_child, quantity_infant,
    unit_price_adult, unit_price_child, unit_price_infant, subtotal,
    status, created_at, updated_at
) VALUES
(1, 1, 1, 1, 'tour', 'Tour Ba Na Hills 1 ngay (Ghep doan)', '2024-05-01', 2, 0, 0, 1210000.00, 950000.00, 0.00, 2420000.00, 'confirmed', '2024-04-28 10:00:00', NOW()),
(2, 2, 2, 4, 'tour', 'Tour Ngu Hanh Son - Hoi An (Chieu toi)', '2024-05-01', 2, 0, 0, 450000.00, 225000.00, 0.00, 900000.00, 'confirmed', '2024-04-29 08:30:00', NOW()),
(3, 3, 3, 6, 'tour', 'Tour Cu Lao Cham 1 ngay (Snorkeling)', '2024-05-01', 2, 0, 0, 650000.00, 325000.00, 100000.00, 1300000.00, 'pending', '2024-04-29 14:00:00', NOW()),
(4, 4, 3, 6, 'tour', 'Tour Cu Lao Cham 1 ngay (Snorkeling)', '2024-04-27', 1, 0, 0, 650000.00, 325000.00, 100000.00, 650000.00, 'completed', '2024-04-25 09:00:00', NOW());

INSERT INTO payments (
    id, booking_id, transaction_code, amount, payment_method, payment_status, payment_gateway,
    paid_at, gateway_response, created_at, updated_at
) VALUES
(1, 1, 'VNP202404281005', 1210000.00, 'vnpay_qr', 'success', 'vnpay', '2024-04-28 10:05:00', '{"status":"00","msg":"Success"}', NOW(), NOW()),
(2, 2, 'MM202404290835', 900000.00, 'momo', 'success', 'momo', '2024-04-29 08:35:00', '{"status":0,"msg":"Successful"}', NOW(), NOW()),
(4, 4, 'VNP202404250910', 650000.00, 'vnpay_qr', 'success', 'vnpay', '2024-04-25 09:10:00', '{"status":"00","msg":"Success"}', NOW(), NOW());
