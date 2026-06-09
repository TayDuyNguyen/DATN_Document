-- DanangTrip test checkout seed.
-- Purpose: stable user and 1,000 VND tour for SePay/VietQR payment testing.

BEGIN;

SELECT setval(pg_get_serial_sequence('users', 'id'), GREATEST((SELECT COALESCE(MAX(id), 1) FROM users), 1), true);
SELECT setval(pg_get_serial_sequence('tours', 'id'), GREATEST((SELECT COALESCE(MAX(id), 1) FROM tours), 1), true);
SELECT setval(pg_get_serial_sequence('tour_schedules', 'id'), GREATEST((SELECT COALESCE(MAX(id), 1) FROM tour_schedules), 1), true);
SELECT setval(pg_get_serial_sequence('bookings', 'id'), GREATEST((SELECT COALESCE(MAX(id), 1) FROM bookings), 1), true);
SELECT setval(pg_get_serial_sequence('booking_items', 'id'), GREATEST((SELECT COALESCE(MAX(id), 1) FROM booking_items), 1), true);
SELECT setval(pg_get_serial_sequence('payments', 'id'), GREATEST((SELECT COALESCE(MAX(id), 1) FROM payments), 1), true);

INSERT INTO users (
    username, email, password, full_name, phone, birthdate, gender, city,
    role, status, email_verified_at, created_at, updated_at
) VALUES (
    'duytayx8',
    'duytayx8@gmail.com',
    '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi',
    'Nguyễn Duy Tây DUT',
    '0364061026',
    '2004-09-02',
    'male',
    'Đà Nẵng',
    'user',
    'active',
    NOW(),
    NOW(),
    NOW()
)
ON CONFLICT (email) DO UPDATE SET
    username = EXCLUDED.username,
    full_name = EXCLUDED.full_name,
    phone = EXCLUDED.phone,
    birthdate = EXCLUDED.birthdate,
    gender = EXCLUDED.gender,
    city = EXCLUDED.city,
    role = EXCLUDED.role,
    status = EXCLUDED.status,
    email_verified_at = COALESCE(users.email_verified_at, EXCLUDED.email_verified_at),
    updated_at = NOW();

INSERT INTO tours (
    name, slug, tour_category_id, description, short_desc, itinerary, inclusions,
    exclusions, price_adult, price_child, price_infant, discount_percent, duration,
    start_time, meeting_point, max_people, min_people, available_from, available_to,
    thumbnail, images, video_url, status, booking_availability, is_featured, is_hot,
    view_count, booking_count, rating_count, rating_avg, created_by, created_at, updated_at
)
SELECT
    'Tour Test Thanh Toán SePay 1.000đ',
    'tour-test-thanh-toan-sepay-1000',
    COALESCE(
        (SELECT id FROM tour_categories WHERE slug = 'tour-ba-na-hills' LIMIT 1),
        (SELECT id FROM tour_categories ORDER BY sort_order, id LIMIT 1)
    ),
    'Tour thử nghiệm thanh toán SePay VietQR cho DanangTrip. Dữ liệu được tạo riêng để kiểm tra quy trình đặt tour, tạo mã QR chuyển khoản, nhận IPN và cập nhật trạng thái đơn hàng. Nội dung, lịch trình và hình ảnh mô phỏng theo một tour vận hành thật nhưng giá cố định chỉ 1.000đ để test an toàn.',
    'Tour test thanh toán SePay VietQR giá 1.000đ, có lịch khởi hành mở bán và hình ảnh đầy đủ.',
    '[
        {"time":"08:00","activity":"Đón khách tại trung tâm Đà Nẵng hoặc điểm hẹn đã đăng ký."},
        {"time":"08:30","activity":"Hướng dẫn nhanh quy trình check-in tour và xác nhận thông tin đặt chỗ."},
        {"time":"09:00","activity":"Di chuyển tham quan Cầu Vàng và khu làng Pháp Bà Nà Hills."},
        {"time":"11:30","activity":"Nghỉ ngơi, chụp ảnh và dùng nước suối theo tiêu chuẩn tour."},
        {"time":"13:30","activity":"Tự do trải nghiệm khu vui chơi, quảng trường và các điểm check-in nổi bật."},
        {"time":"15:30","activity":"Tập trung đoàn, quay về Đà Nẵng và kết thúc chương trình test."}
    ]'::json,
    '[
        "Xe đưa đón theo chương trình",
        "Hướng dẫn viên hỗ trợ trong suốt hành trình",
        "Nước suối 1 chai/khách",
        "Bảo hiểm du lịch cơ bản",
        "Hỗ trợ xác nhận thanh toán SePay VietQR"
    ]'::json,
    '[
        "Chi phí cá nhân ngoài chương trình",
        "Ăn uống ngoài phần đã nêu",
        "Vé hoặc dịch vụ phát sinh không nằm trong gói test"
    ]'::json,
    1000,
    1000,
    0,
    0,
    '1 ngày',
    '08:00',
    'Trung tâm Đà Nẵng / điểm hẹn DanangTrip',
    30,
    1,
    CURRENT_DATE,
    CURRENT_DATE + INTERVAL '180 days',
    'https://res.cloudinary.com/dmukxquza/image/upload/v1780804744/danangtrip/tours/vmtravel-central-003-ba-na-hills-tour-from-da-nang-1-day-tour-deluxe-group-tour/tour-004__vmtravel-central-003-ba-na-hills-tour-from-da-nang-1-day-tour-deluxe-group-tour__p01__vmtravel-bana-hills-big-group-tour.jpg',
    '[
        "https://res.cloudinary.com/dmukxquza/image/upload/v1780804744/danangtrip/tours/vmtravel-central-003-ba-na-hills-tour-from-da-nang-1-day-tour-deluxe-group-tour/tour-004__vmtravel-central-003-ba-na-hills-tour-from-da-nang-1-day-tour-deluxe-group-tour__p01__vmtravel-bana-hills-big-group-tour.jpg",
        "https://res.cloudinary.com/dmukxquza/image/upload/v1780804747/danangtrip/tours/vmtravel-central-003-ba-na-hills-tour-from-da-nang-1-day-tour-deluxe-group-tour/tour-004__vmtravel-central-003-ba-na-hills-tour-from-da-nang-1-day-tour-deluxe-group-tour__p02__vmtravel-bana-hills-in-december.jpg",
        "https://res.cloudinary.com/dmukxquza/image/upload/v1780804750/danangtrip/tours/vmtravel-central-003-ba-na-hills-tour-from-da-nang-1-day-tour-deluxe-group-tour/tour-004__vmtravel-central-003-ba-na-hills-tour-from-da-nang-1-day-tour-deluxe-group-tour__p03__vmtravel-bana-hill-tour-from-hoi-an.jpg"
    ]'::json,
    NULL,
    'active',
    'open',
    true,
    true,
    128,
    0,
    5,
    4.80,
    (SELECT id FROM users WHERE email = 'duytayx8@gmail.com' LIMIT 1),
    NOW(),
    NOW()
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
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
    available_from = EXCLUDED.available_from,
    available_to = EXCLUDED.available_to,
    thumbnail = EXCLUDED.thumbnail,
    images = EXCLUDED.images,
    status = EXCLUDED.status,
    booking_availability = EXCLUDED.booking_availability,
    is_featured = EXCLUDED.is_featured,
    is_hot = EXCLUDED.is_hot,
    rating_count = EXCLUDED.rating_count,
    rating_avg = EXCLUDED.rating_avg,
    created_by = EXCLUDED.created_by,
    updated_at = NOW();

INSERT INTO tour_locations (tour_id, location_id, created_at)
SELECT t.id, l.id, NOW()
FROM tours t
JOIN locations l ON l.id IN (19, 23)
WHERE t.slug = 'tour-test-thanh-toan-sepay-1000'
ON CONFLICT (tour_id, location_id) DO NOTHING;

WITH test_tour AS (
    SELECT id, price_adult, price_child, price_infant
    FROM tours
    WHERE slug = 'tour-test-thanh-toan-sepay-1000'
),
future_dates AS (
    SELECT
        test_tour.*,
        (CURRENT_DATE + (day_offset || ' days')::interval)::date AS start_date,
        row_number() OVER () AS rn
    FROM test_tour
    CROSS JOIN (VALUES (1), (3), (5), (7), (10), (14), (21), (28)) AS offsets(day_offset)
)
INSERT INTO tour_schedules (
    tour_id, start_date, end_date, max_people, booked_people, price_adult,
    price_child, price_infant, status, booking_availability, departure_code,
    departure_place, booking_deadline, created_at, updated_at
)
SELECT
    id,
    start_date,
    start_date,
    30,
    0,
    price_adult,
    price_child,
    price_infant,
    'available',
    'open',
    'TEST-SEPAY-' || to_char(start_date, 'YYYYMMDD'),
    'Trung tâm Đà Nẵng / điểm hẹn DanangTrip',
    start_date::timestamp - INTERVAL '12 hours',
    NOW(),
    NOW()
FROM future_dates
ON CONFLICT (tour_id, start_date) DO UPDATE SET
    end_date = EXCLUDED.end_date,
    max_people = EXCLUDED.max_people,
    price_adult = EXCLUDED.price_adult,
    price_child = EXCLUDED.price_child,
    price_infant = EXCLUDED.price_infant,
    status = EXCLUDED.status,
    booking_availability = EXCLUDED.booking_availability,
    departure_code = EXCLUDED.departure_code,
    departure_place = EXCLUDED.departure_place,
    booking_deadline = EXCLUDED.booking_deadline,
    updated_at = NOW();

SELECT setval(pg_get_serial_sequence('users', 'id'), GREATEST((SELECT MAX(id) FROM users), 1), true);
SELECT setval(pg_get_serial_sequence('tours', 'id'), GREATEST((SELECT MAX(id) FROM tours), 1), true);
SELECT setval(pg_get_serial_sequence('tour_schedules', 'id'), GREATEST((SELECT MAX(id) FROM tour_schedules), 1), true);
SELECT setval(pg_get_serial_sequence('bookings', 'id'), GREATEST((SELECT COALESCE(MAX(id), 1) FROM bookings), 1), true);
SELECT setval(pg_get_serial_sequence('booking_items', 'id'), GREATEST((SELECT COALESCE(MAX(id), 1) FROM booking_items), 1), true);
SELECT setval(pg_get_serial_sequence('payments', 'id'), GREATEST((SELECT COALESCE(MAX(id), 1) FROM payments), 1), true);

COMMIT;
