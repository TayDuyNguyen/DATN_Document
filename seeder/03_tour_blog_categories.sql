-- DanangTrip Real Data Seeder: Tour & Blog Categories
-- Source: Vietravel, Saigontourist, VnExpress Travel, Kenh14
-- Retrieved Date: 2026-04-28

-- TOUR_CATEGORY_LOOKUP
-- Du lịch văn hóa -> 1, Du lịch sinh thái -> 2, Du lịch nghỉ dưỡng -> 3, Du lịch giải trí -> 4, Du lịch thể thao -> 5
-- Du lịch khám phá -> 6, Du lịch mạo hiểm -> 7, Du lịch MICE -> 8, Du lịch tâm linh -> 9, Du lịch biển đảo -> 10

INSERT INTO tour_categories (id, name, slug, description, icon, sort_order, status, created_at, updated_at) VALUES
(1, 'Du lịch văn hóa', 'du-lich-van-hoa', 'Khám phá di sản, di tích lịch sử và phong tục tập quán đặc sắc.', 'history', 1, 'active', NOW(), NOW()),
(2, 'Du lịch sinh thái', 'du-lich-sinh-thai', 'Tham quan và hòa mình vào thiên nhiên tại các vườn quốc gia.', 'eco', 2, 'active', NOW(), NOW()),
(3, 'Du lịch nghỉ dưỡng', 'du-lich-nghi-duong', 'Thư giãn tại các resort cao cấp, spa và dịch vụ chăm sóc sức khỏe.', 'pool', 3, 'active', NOW(), NOW()),
(4, 'Du lịch giải trí', 'du-lich-giai-tri', 'Trải nghiệm các hoạt động vui chơi tại công viên chủ đề.', 'celebration', 4, 'active', NOW(), NOW()),
(5, 'Du lịch thể thao', 'du-lich-the-thao', 'Kết hợp du lịch với các hoạt động thể thao như golf, marathon.', 'sports_soccer', 5, 'active', NOW(), NOW()),
(6, 'Du lịch khám phá', 'du-lich-kham-pha', 'Tìm hiểu những vùng đất mới và những nét văn hóa độc đáo.', 'explore', 6, 'active', NOW(), NOW()),
(7, 'Du lịch mạo hiểm', 'du-lich-mao-hiem', 'Các hoạt động kích thích như leo núi, trekking, thám hiểm hang động.', 'landscape', 7, 'active', NOW(), NOW()),
(8, 'Du lịch MICE', 'du-lich-mice', 'Du lịch kết hợp hội thảo, hội nghị và sự kiện doanh nghiệp.', 'groups', 8, 'active', NOW(), NOW()),
(9, 'Du lịch tâm linh', 'du-lich-tam-linh', 'Hành hương, thăm viếng các ngôi chùa và cơ sở tôn giáo.', 'church', 9, 'active', NOW(), NOW()),
(10, 'Du lịch biển đảo', 'du-lich-bien-dao', 'Nghỉ dưỡng và tham gia các hoạt động vui chơi tại các vùng biển.', 'beach_access', 10, 'active', NOW(), NOW());

-- BLOG_CATEGORY_LOOKUP
-- Điểm đến -> 1, Ẩm thực -> 2, Dấu chân -> 3, Tư vấn -> 4, Cẩm nang -> 5, Ảnh & Video -> 6, Check-in -> 7, Review -> 8

INSERT INTO blog_categories (id, name, slug, description, created_at, updated_at) VALUES
(1, 'Điểm đến', 'diem-den', 'Thông tin chi tiết, hình ảnh và đánh giá về các địa danh du lịch.', NOW(), NOW()),
(2, 'Ẩm thực', 'am-thuc-blog', 'Giới thiệu các món ăn đặc sản và địa chỉ quán ăn ngon.', NOW(), NOW()),
(3, 'Dấu chân', 'dau-chan', 'Chia sẻ trải nghiệm cá nhân và câu chuyện truyền cảm hứng.', NOW(), NOW()),
(4, 'Tư vấn', 'tu-van', 'Giải đáp thắc mắc và cung cấp mẹo hữu ích cho chuyến đi.', NOW(), NOW()),
(5, 'Cẩm nang', 'cam-nang', 'Hướng dẫn chi tiết về di chuyển, lưu trú và lịch trình.', NOW(), NOW()),
(6, 'Ảnh & Video', 'anh-video', 'Tổng hợp những khoảnh khắc đẹp về phong cảnh và con người.', NOW(), NOW()),
(7, 'Check-in', 'check-in-blog', 'Cập nhật địa điểm chụp ảnh hot và xu hướng du lịch mới.', NOW(), NOW()),
(8, 'Review', 'review', 'Đánh giá khách quan về chất lượng tour, khách sạn và nhà hàng.', NOW(), NOW());
