-- DanangTrip Real Data Seeder: Tags & Amenities
-- Source: Traveloka, Booking.com, Local Travel Portals
-- Retrieved Date: 2026-04-28

-- TAG_LOOKUP
-- Nghỉ dưỡng -> 1, Du lịch biển -> 2, Du lịch bụi -> 3, Du lịch tâm linh -> 4, Du lịch văn hóa -> 5, Du lịch sinh thái -> 6
-- Gia đình -> 7, Cặp đôi -> 8, Nhóm bạn -> 9, Đi một mình -> 10
-- Gần biển -> 11, Trung tâm -> 12, Yên tĩnh -> 13, Sang trọng -> 14, Giá rẻ -> 15, View đẹp -> 16
-- Sống ảo -> 17, Khám phá -> 18, Trải nghiệm -> 19, Chữa lành -> 20, Ẩm thực -> 21, Check-in -> 22

INSERT INTO tags (id, name, slug, type, created_at, updated_at) VALUES
(1, 'Nghỉ dưỡng', 'nghi-duong', 'vibe', NOW(), NOW()),
(2, 'Du lịch biển', 'du-lich-bien', 'landscape', NOW(), NOW()),
(3, 'Du lịch bụi', 'du-lich-bui', 'audience', NOW(), NOW()),
(4, 'Du lịch tâm linh', 'du-lich-tam-linh', 'activity', NOW(), NOW()),
(5, 'Du lịch văn hóa', 'du-lich-van-hoa', 'activity', NOW(), NOW()),
(6, 'Du lịch sinh thái', 'du-lich-sinh-thai', 'landscape', NOW(), NOW()),
(7, 'Gia đình', 'gia-dinh', 'audience', NOW(), NOW()),
(8, 'Cặp đôi', 'cap-doi', 'audience', NOW(), NOW()),
(9, 'Nhóm bạn', 'nhom-ban', 'audience', NOW(), NOW()),
(10, 'Đi một mình', 'di-mot-minh', 'audience', NOW(), NOW()),
(11, 'Gần biển', 'gan-bien', 'landscape', NOW(), NOW()),
(12, 'Trung tâm thành phố', 'trung-tam-thanh-pho', 'landscape', NOW(), NOW()),
(13, 'Yên tĩnh', 'yen-tinh', 'vibe', NOW(), NOW()),
(14, 'Sang trọng', 'sang-trong', 'vibe', NOW(), NOW()),
(15, 'Giá rẻ', 'gia-re', 'vibe', NOW(), NOW()),
(16, 'View đẹp', 'view-dep', 'landscape', NOW(), NOW()),
(17, 'Sống ảo', 'song-ao', 'activity', NOW(), NOW()),
(18, 'Khám phá', 'kham-pha', 'activity', NOW(), NOW()),
(19, 'Trải nghiệm', 'trai-nghiem', 'activity', NOW(), NOW()),
(20, 'Chữa lành', 'chua-lanh', 'vibe', NOW(), NOW()),
(21, 'Ẩm thực', 'am-thuc-tag', 'activity', NOW(), NOW()),
(22, 'Check-in', 'check-in', 'activity', NOW(), NOW());

-- AMENITY_LOOKUP
-- Wifi -> 1, Hồ bơi -> 2, Gym -> 3, Spa -> 4, Nhà hàng -> 5, Bãi đỗ xe -> 6, Đưa đón sân bay -> 7, Bãi biển riêng -> 8
-- Máy sấy tóc -> 9, Điều hòa -> 10, Tivi -> 11, Minibar -> 12, Két sắt -> 13, Bình đun nước -> 14, Dép -> 15, Áo choàng -> 16

INSERT INTO amenities (id, name, icon, category, created_at, updated_at) VALUES
(1, 'Wifi miễn phí', 'wifi', 'connectivity', NOW(), NOW()),
(2, 'Hồ bơi', 'pool', 'comfort', NOW(), NOW()),
(3, 'Phòng tập Gym', 'fitness_center', 'comfort', NOW(), NOW()),
(4, 'Spa & Massage', 'spa', 'comfort', NOW(), NOW()),
(5, 'Nhà hàng & Bar', 'restaurant', 'food', NOW(), NOW()),
(6, 'Bãi đỗ xe', 'local_parking', 'connectivity', NOW(), NOW()),
(7, 'Đưa đón sân bay', 'airport_shuttle', 'connectivity', NOW(), NOW()),
(8, 'Bãi biển riêng', 'beach_access', 'landscape', NOW(), NOW()),
(9, 'Máy sấy tóc', 'hair_dryer', 'bathroom', NOW(), NOW()),
(10, 'Điều hòa nhiệt độ', 'ac_unit', 'comfort', NOW(), NOW()),
(11, 'Tivi truyền hình cáp', 'tv', 'comfort', NOW(), NOW()),
(12, 'Tủ lạnh mini bar', 'kitchen', 'comfort', NOW(), NOW()),
(13, 'Két sắt an toàn', 'lock', 'comfort', NOW(), NOW()),
(14, 'Ấm đun nước', 'coffee_maker', 'comfort', NOW(), NOW()),
(15, 'Dép đi trong phòng', 'checkroom', 'bathroom', NOW(), NOW()),
(16, 'Áo choàng tắm', 'checkroom', 'bathroom', NOW(), NOW()),
(17, 'Bàn chải & Kem đánh răng', 'cleaning_services', 'bathroom', NOW(), NOW()),
(18, 'Dầu gội & Sữa tắm', 'soap', 'bathroom', NOW(), NOW()),
(19, 'Sân tennis', 'sports_tennis', 'comfort', NOW(), NOW()),
(20, 'Câu lạc bộ trẻ em', 'child_care', 'comfort', NOW(), NOW()),
(21, 'Thanh toán thẻ', 'credit_card', 'payment', NOW(), NOW()),
(22, 'Phòng họp', 'meeting_room', 'business', NOW(), NOW());
