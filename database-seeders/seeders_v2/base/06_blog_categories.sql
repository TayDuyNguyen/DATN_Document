BEGIN;
INSERT INTO "blog_categories" ("id", "name", "slug", "description", "created_at", "updated_at", "sort_order") VALUES
(1, 'Cẩm nang du lịch', 'cam-nang-du-lich', 'Kinh nghiệm từ A-Z cho chuyến đi của bạn.', '2026-06-13 10:19:12', '2026-06-13 10:20:59', 0),
(2, 'Review Ẩm Thực', 'review-am-thuc', 'Những quán ăn ngon nức tiếng không thể bỏ qua.', '2026-06-13 10:19:12', '2026-06-13 10:19:12', 0),
(3, 'Địa Điểm Check-in', 'dia-diem-check-in', 'Tổng hợp những tọa độ sống ảo cực chất.', '2026-06-13 10:19:12', '2026-06-13 10:19:12', 0),
(4, 'Tin Tức Du Lịch', 'tin-tuc-du-lich', 'Cập nhật các sự kiện, lễ hội mới nhất.', '2026-06-13 10:19:12', '2026-06-13 10:19:12', 0),
(5, 'Lịch Trình Gợi Ý', 'lich-trinh-goi-y', 'Gợi ý lịch trình 3 ngày 2 đêm, 4 ngày 3 đêm.', '2026-06-13 10:19:12', '2026-06-13 10:19:12', 0),
(6, 'Văn Hóa & Lịch Sử', 'van-hoa-lich-su', 'Tìm hiểu về nguồn gốc và truyền thống địa phương.', '2026-06-13 10:19:12', '2026-06-13 10:19:12', 0),
(8, 'Review Khách Sạn', 'review-khach-san', 'Đánh giá chân thực về nơi lưu trú.', '2026-06-13 10:19:12', '2026-06-13 10:19:12', 0),
(16, 'Du Lịch Gia Đình', 'family-travel-tips', 'Mẹo nhỏ khi có trẻ em và người già đi cùng.', '2026-06-13 10:19:12', '2026-06-13 10:19:12', 0),
(17, 'Hẹn Hò Lãng Mạn', 'romantic-date', 'Những điểm đến dành riêng cho các cặp đôi.', '2026-06-13 10:19:12', '2026-06-13 10:19:12', 0),
(22, 'Cẩm Nang Hội An', 'hoi-an-guide', 'Chuyên sâu về phố cổ và vùng ven.', '2026-06-13 10:19:12', '2026-06-13 10:19:12', 0),
(23, 'Cẩm Nang Huế', 'hue-guide', 'Chuyên sâu về cố đô và các lăng tẩm.', '2026-06-13 10:19:12', '2026-06-13 10:19:12', 0),
(24, 'Cẩm Nang Đà Nẵng', 'danang-guide', 'Chuyên sâu về thành phố đáng sống nhất.', '2026-06-13 10:19:12', '2026-06-13 10:19:12', 0),
(30, 'Phương Tiện Di Chuyển', 'transport-guide', 'Thuê xe máy, Grab hay xe buýt?', '2026-06-13 10:19:12', '2026-06-13 10:19:12', 0),
(41, 'Chợ & Mua Sắm', 'market-shopping', 'Trải nghiệm mua sắm tại chợ truyền thống.', '2026-06-13 10:19:12', '2026-06-13 10:19:12', 0),
(47, 'Góc Review Homestay', 'homestay-review', 'Ấm cúng như ở nhà.', '2026-06-13 10:19:12', '2026-06-13 10:19:12', 0),
(55, 'Hướng Dẫn Đi Bà Nà Hills', 'ba-na-hills-tips', 'Làm sao để không bị lạc và chơi hết các trò?', '2026-06-13 10:19:12', '2026-06-13 10:19:12', 0),
(61, 'Cẩm Nang Quà Lưu Niệm', 'souvenir-guide', 'Những món đồ ý nghĩa nên mua.', '2026-06-13 10:19:12', '2026-06-13 10:19:12', 0),
(64, 'Review Các Bãi Biển', 'beach-review', 'Mỹ Khê, Non Nước hay Thanh Khê?', '2026-06-13 10:19:12', '2026-06-13 10:19:12', 0),
(81, 'Kinh Nghiệm Đi Thánh Địa Mỹ Sơn', 'my-son-tips', 'Hành trình tìm về quá khứ.', '2026-06-13 10:19:12', '2026-06-13 10:19:12', 0)
ON CONFLICT (id) DO NOTHING;

COMMIT;
