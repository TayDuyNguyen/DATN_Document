-- DanangTrip Real Data Seeder: Ratings, Favorites, Views, Search Logs, Contacts, Notifications
-- Normalized to current schema constraints

INSERT INTO ratings (
    id, user_id, location_id, tour_id, booking_id, score, comment, image_count, status,
    created_at, updated_at
) VALUES
(1, 3, 1, NULL, NULL, 5, 'Ba Na Hills rat an tuong. Khong khi trong lanh, dich vu tot.', 2, 'approved', '2024-05-02 09:00:00', NOW()),
(2, 4, 18, NULL, NULL, 5, 'Do an ngon, khong gian am cung, nhan vien nhiet tinh.', 1, 'approved', '2024-05-02 10:30:00', NOW()),
(3, 7, 3, NULL, NULL, 4, 'Chua Linh Ung dep va thanh tinh, view bien dep.', 0, 'approved', '2024-04-29 15:00:00', NOW()),
(4, 9, 5, NULL, NULL, 5, 'My Khe dep, cat min, nuoc trong.', 0, 'approved', '2024-04-28 06:00:00', NOW()),
(5, 10, 1, NULL, NULL, 3, 'Canh dep nhung gia ve cao vao cuoi tuan.', 0, 'approved', '2024-04-27 11:00:00', NOW());

INSERT INTO rating_images (id, rating_id, image_url, sort_order, created_at) VALUES
(1, 1, 'https://cdn.danangtrip.vn/ratings/rating1_img1.jpg', 1, NOW()),
(2, 1, 'https://cdn.danangtrip.vn/ratings/rating1_img2.jpg', 2, NOW()),
(3, 2, 'https://cdn.danangtrip.vn/ratings/rating2_img1.jpg', 1, NOW());

INSERT INTO favorites (id, user_id, location_id, tour_id, created_at) VALUES
(1, 3, 2, NULL, NOW()),
(2, 3, 3, NULL, NOW()),
(3, 4, 1, NULL, NOW()),
(4, 4, NULL, 1, NOW());

INSERT INTO views (id, user_id, location_id, tour_id, session_id, time_spent, created_at) VALUES
(1, 3, 1, NULL, 'sess_01', 300, NOW()),
(2, NULL, 2, NULL, 'sess_02', 120, NOW()),
(3, 4, NULL, 1, 'sess_03', 450, NOW());

INSERT INTO search_logs (id, user_id, session_id, query, results_count, filters, created_at) VALUES
(1, 3, 'sess_01', 'Sun World Ba Na Hills', 12, '{"category":"sightseeing"}', NOW()),
(2, NULL, 'sess_02', 'Cau Vang', 8, NULL, NOW()),
(3, 4, 'sess_03', 'Bai bien My Khe', 5, NULL, NOW()),
(4, NULL, 'sess_04', 'Mi Quang ngon', 15, '{"category":"dining"}', NOW()),
(5, 7, 'sess_05', 'Khach san ven bien Da Nang', 25, '{"price_max":2000000}', NOW());

INSERT INTO contacts (
    id, name, email, phone, subject, message, status, reply, created_at, updated_at
) VALUES
(1, 'Nguyen Van A', 'vana@gmail.com', '0901234567', 'Tu van tour gia dinh', 'Minh muon hoi gia tour Ba Na Hills cho doan 10 nguoi lon tuan sau.', 'new', NULL, NOW(), NOW()),
(2, 'Tran Thi B', 'thib@gmail.com', '0912345678', 'Hoi ve don tra khach', 'Tour Cu Lao Cham co don tai khach san khu Ngu Hanh Son khong?', 'processed', 'Da goi dien tu van.', NOW(), NOW());

INSERT INTO notifications (
    id, user_id, type, title, content, data, is_read, read_at, created_at
) VALUES
(1, 3, 'booking_status', 'Dat cho thanh cong', 'Don hang DT-240501-001 da duoc xac nhan.', '{"booking_id":1}', false, NULL, NOW()),
(2, 4, 'system', 'Uu dai he', 'Giam 10% khi dat tour Hoi An trong thang 5.', '{"discount_code":"SUMMER10"}', true, NOW(), NOW());
