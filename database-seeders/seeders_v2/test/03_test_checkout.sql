BEGIN;
INSERT INTO "users" ("id", "username", "email", "password", "full_name", "avatar", "phone", "birthdate", "gender", "city", "role", "status", "email_verified_at", "last_login_at", "created_at", "updated_at") VALUES
(101, 'duytayx8', 'duytayx8@gmail.com', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'Nguyễn Duy Tây DUT', NULL, '0364061026', '2004-09-02', 'male', 'Đà Nẵng', 'user', 'active', '2026-06-13 10:23:49', NULL, '2026-06-13 10:23:49', '2026-06-14 15:01:55')
ON CONFLICT (email) DO UPDATE SET username = EXCLUDED.username, full_name = EXCLUDED.full_name, phone = EXCLUDED.phone, birthdate = EXCLUDED.birthdate, gender = EXCLUDED.gender, city = EXCLUDED.city, role = EXCLUDED.role, status = EXCLUDED.status, email_verified_at = COALESCE(users.email_verified_at, EXCLUDED.email_verified_at), updated_at = NOW();

INSERT INTO "tours" ("id", "name", "slug", "tour_category_id", "description", "short_desc", "itinerary", "inclusions", "exclusions", "price_adult", "price_child", "price_infant", "discount_percent", "duration", "start_time", "meeting_point", "max_people", "min_people", "available_from", "available_to", "thumbnail", "images", "video_url", "status", "booking_availability", "is_featured", "is_hot", "view_count", "booking_count", "rating_count", "rating_avg", "created_by", "created_at", "updated_at") VALUES
(165, 'Tour Test Thanh Toán SePay 1.000đ', 'tour-test-thanh-toan-sepay-1000', 1, 'Tour thử nghiệm thanh toán SePay VietQR cho DanangTrip. Dữ liệu được tạo riêng để kiểm tra quy trình đặt tour, tạo mã QR chuyển khoản, nhận IPN và cập nhật trạng thái đơn hàng. Nội dung, lịch trình và hình ảnh mô phỏng theo một tour vận hành thật nhưng giá cố định chỉ 1.000đ để test an toàn.', 'Tour test thanh toán SePay VietQR giá 1.000đ, có lịch khởi hành mở bán và hình ảnh đầy đủ.', '[
        {"time":"08:00","activity":"Đón khách tại trung tâm Đà Nẵng hoặc điểm hẹn đã đăng ký."},
        {"time":"08:30","activity":"Hướng dẫn nhanh quy trình check-in tour và xác nhận thông tin đặt chỗ."},
        {"time":"09:00","activity":"Di chuyển tham quan Cầu Vàng và khu làng Pháp Bà Nà Hills."},
        {"time":"11:30","activity":"Nghỉ ngơi, chụp ảnh và dùng nước suối theo tiêu chuẩn tour."},
        {"time":"13:30","activity":"Tự do trải nghiệm khu vui chơi, quảng trường và các điểm check-in nổi bật."},
        {"time":"15:30","activity":"Tập trung đoàn, quay về Đà Nẵng và kết thúc chương trình test."}
    ]'::jsonb, '[
        "Xe đưa đón theo chương trình",
        "Hướng dẫn viên hỗ trợ trong suốt hành trình",
        "Nước suối 1 chai/khách",
        "Bảo hiểm du lịch cơ bản",
        "Hỗ trợ xác nhận thanh toán SePay VietQR"
    ]'::jsonb, '[
        "Chi phí cá nhân ngoài chương trình",
        "Ăn uống ngoài phần đã nêu",
        "Vé hoặc dịch vụ phát sinh không nằm trong gói test"
    ]'::jsonb, '1000.00', '1000.00', '0.00', 0, '1 ngày', '08:00', 'Trung tâm Đà Nẵng / điểm hẹn DanangTrip', 30, 1, '2026-06-14', '2026-12-11', 'https://res.cloudinary.com/dmukxquza/image/upload/v1780804744/danangtrip/tours/vmtravel-central-003-ba-na-hills-tour-from-da-nang-1-day-tour-deluxe-group-tour/tour-004__vmtravel-central-003-ba-na-hills-tour-from-da-nang-1-day-tour-deluxe-group-tour__p01__vmtravel-bana-hills-big-group-tour.jpg', '[
        "https://res.cloudinary.com/dmukxquza/image/upload/v1780804744/danangtrip/tours/vmtravel-central-003-ba-na-hills-tour-from-da-nang-1-day-tour-deluxe-group-tour/tour-004__vmtravel-central-003-ba-na-hills-tour-from-da-nang-1-day-tour-deluxe-group-tour__p01__vmtravel-bana-hills-big-group-tour.jpg",
        "https://res.cloudinary.com/dmukxquza/image/upload/v1780804747/danangtrip/tours/vmtravel-central-003-ba-na-hills-tour-from-da-nang-1-day-tour-deluxe-group-tour/tour-004__vmtravel-central-003-ba-na-hills-tour-from-da-nang-1-day-tour-deluxe-group-tour__p02__vmtravel-bana-hills-in-december.jpg",
        "https://res.cloudinary.com/dmukxquza/image/upload/v1780804750/danangtrip/tours/vmtravel-central-003-ba-na-hills-tour-from-da-nang-1-day-tour-deluxe-group-tour/tour-004__vmtravel-central-003-ba-na-hills-tour-from-da-nang-1-day-tour-deluxe-group-tour__p03__vmtravel-bana-hill-tour-from-hoi-an.jpg"
    ]'::jsonb, NULL, 'active', 'open', true, true, 128, 0, 1, '4.00', 101, '2026-06-13 10:23:49', '2026-06-15 00:49:30')
ON CONFLICT (id) DO UPDATE SET
    name = EXCLUDED.name,
    slug = EXCLUDED.slug,
    tour_category_id = EXCLUDED.tour_category_id,
    description = EXCLUDED.description,
    short_desc = EXCLUDED.short_desc,
    itinerary = EXCLUDED.itinerary,
    inclusions = EXCLUDED.inclusions,
    exclusions = EXCLUDED.exclusions,
    price_adult = EXCLUDED.price_adult,
    price_child = EXCLUDED.price_child,
    price_infant = EXCLUDED.price_infant,
    discount_percent = EXCLUDED.discount_percent,
    duration = EXCLUDED.duration,
    start_time = EXCLUDED.start_time,
    meeting_point = EXCLUDED.meeting_point,
    max_people = EXCLUDED.max_people,
    min_people = EXCLUDED.min_people,
    thumbnail = EXCLUDED.thumbnail,
    images = EXCLUDED.images,
    status = EXCLUDED.status,
    updated_at = NOW();

INSERT INTO "tour_locations" ("id", "tour_id", "location_id", "created_at") VALUES
(305, 165, 23, '2026-06-13 10:23:49') ON CONFLICT (tour_id, location_id) DO NOTHING;

INSERT INTO "tour_schedules" (id, tour_id, start_date, end_date, max_people, booked_people, price_adult, price_child, price_infant, status, booking_availability, departure_code, departure_place, booking_deadline, created_at, updated_at) VALUES
(1377, 165, CURRENT_DATE + (-1), CURRENT_DATE + (-1), 30, 0, 1000.00, 1000.00, 0.00, 'available', 'open', 'TEST-SEPAY-' || to_char(CURRENT_DATE + (-1), 'YYYYMMDD'), 'Trung tâm Đà Nẵng / điểm hẹn DanangTrip', (CURRENT_DATE + (-1))::timestamp - interval '20 hours', NOW(), NOW()),
(1385, 165, CURRENT_DATE + (0), CURRENT_DATE + (0), 30, 0, 1000.00, 1000.00, 0.00, 'available', 'open', 'TEST-SEPAY-' || to_char(CURRENT_DATE + (0), 'YYYYMMDD'), 'Trung tâm Đà Nẵng / điểm hẹn DanangTrip', (CURRENT_DATE + (0))::timestamp - interval '20 hours', NOW(), NOW()),
(1378, 165, CURRENT_DATE + (1), CURRENT_DATE + (1), 30, 2, 1000.00, 1000.00, 0.00, 'available', 'open', 'TEST-SEPAY-' || to_char(CURRENT_DATE + (1), 'YYYYMMDD'), 'Trung tâm Đà Nẵng / điểm hẹn DanangTrip', (CURRENT_DATE + (1))::timestamp - interval '20 hours', NOW(), NOW()),
(1386, 165, CURRENT_DATE + (2), CURRENT_DATE + (2), 30, 0, 1000.00, 1000.00, 0.00, 'available', 'open', 'TEST-SEPAY-' || to_char(CURRENT_DATE + (2), 'YYYYMMDD'), 'Trung tâm Đà Nẵng / điểm hẹn DanangTrip', (CURRENT_DATE + (2))::timestamp - interval '20 hours', NOW(), NOW()),
(1379, 165, CURRENT_DATE + (3), CURRENT_DATE + (3), 30, 0, 1000.00, 1000.00, 0.00, 'available', 'open', 'TEST-SEPAY-' || to_char(CURRENT_DATE + (3), 'YYYYMMDD'), 'Trung tâm Đà Nẵng / điểm hẹn DanangTrip', (CURRENT_DATE + (3))::timestamp - interval '20 hours', NOW(), NOW()),
(1387, 165, CURRENT_DATE + (4), CURRENT_DATE + (4), 30, 0, 1000.00, 1000.00, 0.00, 'available', 'open', 'TEST-SEPAY-' || to_char(CURRENT_DATE + (4), 'YYYYMMDD'), 'Trung tâm Đà Nẵng / điểm hẹn DanangTrip', (CURRENT_DATE + (4))::timestamp - interval '20 hours', NOW(), NOW()),
(1380, 165, CURRENT_DATE + (5), CURRENT_DATE + (5), 30, 0, 1000.00, 1000.00, 0.00, 'available', 'open', 'TEST-SEPAY-' || to_char(CURRENT_DATE + (5), 'YYYYMMDD'), 'Trung tâm Đà Nẵng / điểm hẹn DanangTrip', (CURRENT_DATE + (5))::timestamp - interval '20 hours', NOW(), NOW()),
(1388, 165, CURRENT_DATE + (6), CURRENT_DATE + (6), 30, 0, 1000.00, 1000.00, 0.00, 'available', 'open', 'TEST-SEPAY-' || to_char(CURRENT_DATE + (6), 'YYYYMMDD'), 'Trung tâm Đà Nẵng / điểm hẹn DanangTrip', (CURRENT_DATE + (6))::timestamp - interval '20 hours', NOW(), NOW()),
(1381, 165, CURRENT_DATE + (8), CURRENT_DATE + (8), 30, 0, 1000.00, 1000.00, 0.00, 'available', 'open', 'TEST-SEPAY-' || to_char(CURRENT_DATE + (8), 'YYYYMMDD'), 'Trung tâm Đà Nẵng / điểm hẹn DanangTrip', (CURRENT_DATE + (8))::timestamp - interval '20 hours', NOW(), NOW()),
(1389, 165, CURRENT_DATE + (9), CURRENT_DATE + (9), 30, 0, 1000.00, 1000.00, 0.00, 'available', 'open', 'TEST-SEPAY-' || to_char(CURRENT_DATE + (9), 'YYYYMMDD'), 'Trung tâm Đà Nẵng / điểm hẹn DanangTrip', (CURRENT_DATE + (9))::timestamp - interval '20 hours', NOW(), NOW()),
(1382, 165, CURRENT_DATE + (12), CURRENT_DATE + (12), 30, 0, 1000.00, 1000.00, 0.00, 'available', 'open', 'TEST-SEPAY-' || to_char(CURRENT_DATE + (12), 'YYYYMMDD'), 'Trung tâm Đà Nẵng / điểm hẹn DanangTrip', (CURRENT_DATE + (12))::timestamp - interval '20 hours', NOW(), NOW()),
(1390, 165, CURRENT_DATE + (13), CURRENT_DATE + (13), 30, 0, 1000.00, 1000.00, 0.00, 'available', 'open', 'TEST-SEPAY-' || to_char(CURRENT_DATE + (13), 'YYYYMMDD'), 'Trung tâm Đà Nẵng / điểm hẹn DanangTrip', (CURRENT_DATE + (13))::timestamp - interval '20 hours', NOW(), NOW()),
(1383, 165, CURRENT_DATE + (19), CURRENT_DATE + (19), 30, 0, 1000.00, 1000.00, 0.00, 'available', 'open', 'TEST-SEPAY-' || to_char(CURRENT_DATE + (19), 'YYYYMMDD'), 'Trung tâm Đà Nẵng / điểm hẹn DanangTrip', (CURRENT_DATE + (19))::timestamp - interval '20 hours', NOW(), NOW()),
(1391, 165, CURRENT_DATE + (20), CURRENT_DATE + (20), 30, 0, 1000.00, 1000.00, 0.00, 'available', 'open', 'TEST-SEPAY-' || to_char(CURRENT_DATE + (20), 'YYYYMMDD'), 'Trung tâm Đà Nẵng / điểm hẹn DanangTrip', (CURRENT_DATE + (20))::timestamp - interval '20 hours', NOW(), NOW()),
(1384, 165, CURRENT_DATE + (26), CURRENT_DATE + (26), 30, 0, 1000.00, 1000.00, 0.00, 'available', 'open', 'TEST-SEPAY-' || to_char(CURRENT_DATE + (26), 'YYYYMMDD'), 'Trung tâm Đà Nẵng / điểm hẹn DanangTrip', (CURRENT_DATE + (26))::timestamp - interval '20 hours', NOW(), NOW()),
(1392, 165, CURRENT_DATE + (27), CURRENT_DATE + (27), 30, 0, 1000.00, 1000.00, 0.00, 'available', 'open', 'TEST-SEPAY-' || to_char(CURRENT_DATE + (27), 'YYYYMMDD'), 'Trung tâm Đà Nẵng / điểm hẹn DanangTrip', (CURRENT_DATE + (27))::timestamp - interval '20 hours', NOW(), NOW())
ON CONFLICT (id) DO UPDATE SET
    start_date = EXCLUDED.start_date,
    end_date = EXCLUDED.end_date,
    departure_code = EXCLUDED.departure_code,
    booking_deadline = EXCLUDED.booking_deadline,
    updated_at = NOW();

INSERT INTO "bookings" ("id", "booking_code", "user_id", "customer_name", "customer_email", "customer_phone", "customer_address", "customer_note", "total_amount", "discount_amount", "final_amount", "deposit_amount", "payment_method", "payment_status", "booking_status", "cancellation_reason", "booked_at", "confirmed_at", "cancelled_at", "completed_at", "created_at", "updated_at", "promotion_id", "user_voucher_id") VALUES
(125, 'BOOK-JU80GZ2U', 101, 'Nguyễn Duy Tây DUT', 'duytayx8@gmail.com', '0364061026', 'Đà Nẵng', NULL, '2000.00', '0.00', '2000.00', '0.00', 'sepay', 'success', 'confirmed', NULL, '2026-06-14 21:51:40', '2026-06-14 22:09:01', NULL, NULL, '2026-06-14 21:51:40', '2026-06-14 22:09:02', NULL, NULL)
ON CONFLICT (id) DO UPDATE SET booking_status = EXCLUDED.booking_status, payment_status = EXCLUDED.payment_status, updated_at = NOW();

INSERT INTO "booking_items" ("id", "booking_id", "tour_id", "tour_schedule_id", "item_type", "item_name", "travel_date", "quantity_adult", "quantity_child", "quantity_infant", "unit_price_adult", "unit_price_child", "unit_price_infant", "subtotal", "status", "created_at", "updated_at") VALUES
(178, 125, 165, 1378, 'tour', 'Tour Test Thanh Toán SePay 1.000đ', '2026-06-16', 2, 0, 0, '1000', '1000', '0', '2000', 'active', '2026-06-14 21:51:40', '2026-06-14 21:51:40')
ON CONFLICT (id) DO NOTHING;

INSERT INTO "payments" ("id", "booking_id", "transaction_code", "amount", "payment_method", "payment_status", "payment_gateway", "gateway_response", "paid_at", "refunded_at", "refund_reason", "created_at", "updated_at") VALUES
(104, 125, 'PAY-MXZMF8QPGU', '2000.00', 'sepay', 'pending', 'sepay', '{"checkout":{"provider":"sepay","merchant_id":"SP-LIVE-ND974396","environment":"production","transaction_code":"PAY-MXZMF8QPGU","booking_code":"BOOK-JU80GZ2U","amount":2000,"currency":"VND","transfer_content":"DNT BOOK-JU80GZ2U","qr_content":"DNT BOOK-JU80GZ2U","qr_image_url":"https:\/\/img.vietqr.io\/image\/MB-0364061026-compact2.png?amount=2000&addInfo=DNT%20BOOK-JU80GZ2U&accountName=NGUYEN%20DUY%20TAY","return_url":"https:\/\/danangtrip-web.vercel.app\/payment\/result?transaction_code=PAY-MXZMF8QPGU&booking_code=BOOK-JU80GZ2U","bank":{"bank_code":"MB","account_no":"0364061026","account_name":"NGUYEN DUY TAY"}}}', NULL, NULL, NULL, '2026-06-14 21:51:47', '2026-06-14 21:51:47'),
(105, 125, 'PAY-E5EYB3TLRO', '2000.00', 'sepay', 'success', 'sepay', '{"provider":"sepay","reference":"FT26166778594058","payload":{"gateway":"MBBank","transactionDate":"2026-06-14 22:08:00","accountNumber":"0364061026","subAccount":null,"code":null,"content":"DNT BOOKJU80GZ2U   Ma giao dich  Trace707482 Trace 707482","transferType":"in","description":"BankAPINotify DNT BOOKJU80GZ2U   Ma giao dich  Trace707482 Trace 707482","transferAmount":2000,"referenceCode":"FT26166778594058","accumulated":0,"id":63373748}}', '2026-06-14 22:09:01', NULL, NULL, '2026-06-14 22:08:16', '2026-06-14 22:09:01')
ON CONFLICT (id) DO UPDATE SET payment_status = EXCLUDED.payment_status, updated_at = NOW();

INSERT INTO "ratings" ("id", "user_id", "location_id", "tour_id", "booking_id", "score", "comment", "image_count", "status", "rejected_reason", "approved_by", "approved_at", "helpful_count", "created_at", "updated_at", "is_new") VALUES
(621, 44, NULL, 165, NULL, 4, 'Một vài điểm dừng khá nhanh nhưng đoàn vẫn tham quan được các điểm chính trong chương trình.', 0, 'approved', NULL, 1, '2026-04-30 15:02:45', 4, '2026-04-30 15:02:45', '2026-06-14 15:03:23', true)
ON CONFLICT (id) DO NOTHING;

-- No records in rating_images

SELECT setval(pg_get_serial_sequence('users', 'id'), GREATEST((SELECT MAX(id) FROM users), 1), true);
SELECT setval(pg_get_serial_sequence('tours', 'id'), GREATEST((SELECT MAX(id) FROM tours), 1), true);
SELECT setval(pg_get_serial_sequence('tour_schedules', 'id'), GREATEST((SELECT MAX(id) FROM tour_schedules), 1), true);
SELECT setval(pg_get_serial_sequence('bookings', 'id'), GREATEST((SELECT COALESCE(MAX(id), 1) FROM bookings), 1), true);
SELECT setval(pg_get_serial_sequence('booking_items', 'id'), GREATEST((SELECT COALESCE(MAX(id), 1) FROM booking_items), 1), true);
SELECT setval(pg_get_serial_sequence('payments', 'id'), GREATEST((SELECT COALESCE(MAX(id), 1) FROM payments), 1), true);
SELECT setval(pg_get_serial_sequence('ratings', 'id'), GREATEST((SELECT COALESCE(MAX(id), 1) FROM ratings), 1), true);
SELECT setval(pg_get_serial_sequence('rating_images', 'id'), GREATEST((SELECT COALESCE(MAX(id), 1) FROM rating_images), 1), true);

COMMIT;
