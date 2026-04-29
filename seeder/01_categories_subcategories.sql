-- DanangTrip Real Data Seeder: Categories & Subcategories
-- Source: Official Tourism Portals (danangfantasticity.com), Wiki, Local Travel Guides
-- Retrieved Date: 2026-04-28

-- CATEGORY_LOOKUP
-- Tham quan -> 1
-- Ẩm thực -> 2
-- Lưu trú -> 3
-- Giải trí -> 4
-- Mua sắm -> 5

INSERT INTO categories (id, name, slug, icon, description, image, sort_order, status, created_at, updated_at) VALUES
(1, 'Tham quan', 'tham-quan', 'landmark', 'Các địa điểm danh lam thắng cảnh, di tích lịch sử và văn hóa tại Đà Nẵng.', 'https://danangfantasticity.com/wp-content/uploads/2023/01/sightseeing.jpg', 1, 'active', NOW(), NOW()),
(2, 'Ẩm thực', 'am-thuc', 'restaurant', 'Khám phá thế giới ẩm thực phong phú từ đặc sản địa phương đến ẩm thực quốc tế.', 'https://danangfantasticity.com/wp-content/uploads/2023/01/dining.jpg', 2, 'active', NOW(), NOW()),
(3, 'Lưu trú', 'luu-tru', 'hotel', 'Danh sách khách sạn, resort và homestay chất lượng tại Đà Nẵng.', 'https://danangfantasticity.com/wp-content/uploads/2023/01/accommodation.jpg', 3, 'active', NOW(), NOW()),
(4, 'Giải trí', 'giai-tri', 'celebration', 'Các hoạt động vui chơi giải trí, công viên chủ đề và show diễn đặc sắc.', 'https://danangfantasticity.com/wp-content/uploads/2023/01/entertainment.jpg', 4, 'active', NOW(), NOW()),
(5, 'Mua sắm', 'mua-sam', 'shopping_bag', 'Địa điểm mua sắm từ chợ truyền thống đến các trung tâm thương mại hiện đại.', 'https://danangfantasticity.com/wp-content/uploads/2023/01/shopping.jpg', 5, 'active', NOW(), NOW());

-- SUBCATEGORY_LOOKUP
-- Di tích lịch sử -> 1 (cat: 1)
-- Thắng cảnh thiên nhiên -> 2 (cat: 1)
-- Bảo tàng & Văn hóa -> 3 (cat: 1)
-- Công trình kiến trúc -> 4 (cat: 1)
-- Điểm tâm linh -> 5 (cat: 1)
-- Đặc sản Đà Nẵng -> 6 (cat: 2)
-- Nhà hàng -> 7 (cat: 2)
-- Quán ăn đường phố -> 8 (cat: 2)
-- Cà phê & Bar -> 9 (cat: 2)
-- Khách sạn -> 10 (cat: 3)
-- Resort -> 11 (cat: 3)
-- Homestay & Villa -> 12 (cat: 3)
-- Khu vui chơi -> 13 (cat: 4)
-- Show diễn -> 14 (cat: 4)
-- Spa & Massage -> 15 (cat: 4)
-- Chợ truyền thống -> 16 (cat: 5)
-- Trung tâm thương mại -> 17 (cat: 5)

INSERT INTO subcategories (id, category_id, name, slug, description, sort_order, status, created_at, updated_at) VALUES
(1, 1, 'Di tích lịch sử', 'di-tich-lich-su', 'Các địa danh mang đậm dấu ấn lịch sử dân tộc.', 1, 'active', NOW(), NOW()),
(2, 1, 'Thắng cảnh thiên nhiên', 'thang-canh-thien-nhien', 'Núi non, hang động và bãi biển tuyệt đẹp.', 2, 'active', NOW(), NOW()),
(3, 1, 'Bảo tàng & Văn hóa', 'bao-tang-van-hoa', 'Nơi lưu giữ giá trị nghệ thuật và lịch sử.', 3, 'active', NOW(), NOW()),
(4, 1, 'Công trình kiến trúc', 'cong-trinh-kien-truc', 'Những biểu tượng kiến trúc độc đáo của thành phố.', 4, 'active', NOW(), NOW()),
(5, 1, 'Điểm tâm linh', 'diem-tam-linh', 'Chùa chiền và các địa điểm tín ngưỡng.', 5, 'active', NOW(), NOW()),
(6, 2, 'Đặc sản Đà Nẵng', 'dac-san-da-nang', 'Mì Quảng, bánh tráng cuốn thịt heo, hải sản...', 1, 'active', NOW(), NOW()),
(7, 2, 'Nhà hàng', 'nha-hang', 'Không gian ẩm thực từ bình dân đến cao cấp.', 2, 'active', NOW(), NOW()),
(8, 2, 'Quán ăn đường phố', 'quan-an-duong-pho', 'Trải nghiệm văn hóa ẩm thực lề đường đặc trưng.', 3, 'active', NOW(), NOW()),
(9, 2, 'Cà phê & Bar', 'ca-phe-bar', 'Thưởng thức đồ uống và không gian chill.', 4, 'active', NOW(), NOW()),
(10, 3, 'Khách sạn', 'khach-san', 'Từ tiêu chuẩn đến 5 sao sang trọng.', 1, 'active', NOW(), NOW()),
(11, 3, 'Resort', 'resort', 'Khu nghỉ dưỡng ven biển đẳng cấp.', 2, 'active', NOW(), NOW()),
(12, 3, 'Homestay & Villa', 'homestay-villa', 'Không gian nghỉ ngơi ấm cúng và riêng tư.', 3, 'active', NOW(), NOW()),
(13, 4, 'Khu vui chơi', 'khu-vui-choi', 'Các công viên chủ đề và điểm giải trí gia đình.', 1, 'active', NOW(), NOW()),
(14, 4, 'Show diễn', 'show-dien', 'Các chương trình nghệ thuật biểu diễn đặc sắc.', 2, 'active', NOW(), NOW()),
(15, 4, 'Spa & Massage', 'spa-massage', 'Thư giãn và chăm sóc sức khỏe.', 3, 'active', NOW(), NOW()),
(16, 5, 'Chợ truyền thống', 'cho-truyen-thong', 'Chợ Hàn, chợ Cồn và các khu chợ địa phương.', 1, 'active', NOW(), NOW()),
(17, 5, 'Trung tâm thương mại', 'trung-tam-thuong-mai', 'Vincom, Lotte Mart và các mall hiện đại.', 2, 'active', NOW(), NOW());
