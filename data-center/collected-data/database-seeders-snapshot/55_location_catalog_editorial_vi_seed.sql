-- DanangTrip location catalog editorial Vietnamese normalization
-- Purpose:
--   Fix unaccented/machine-translated location names and addresses.
--   Restore slug/name alignment, especially the shifted records after id 104.
--   Remap locations to the correct business category.
--   Replace English or mechanical descriptions with Vietnamese editorial copy.
-- Policy:
--   Match by slug, never by numeric id.
--   Preserve official international brand names where translation would be incorrect.

BEGIN;

WITH canonical(slug, canonical_name, category_id) AS (
    VALUES
        ('hoi-an-ancient-town', 'Phố cổ Hội An', 64),
        ('hoi-an-memories-land', 'Công viên Ấn tượng Hội An', 52),
        ('bay-mau-coconut-forest', 'Rừng dừa Bảy Mẫu', 61),
        ('tam-thanh-beach', 'Bãi biển Tam Thanh', 7),
        ('binh-minh-beach', 'Bãi biển Bình Minh', 7),
        ('dong-giang-heavens-gate', 'Cổng Trời Đông Giang', 58),
        ('furama-ariyana-complex', 'Quần thể Furama - Ariyana Đà Nẵng', 55),
        ('my-son-sanctuary', 'Thánh địa Mỹ Sơn', 8),
        ('ban-than-scenic-area', 'Ghềnh Bàn Than - Hòn Mang', 7),
        ('phu-ninh-lake', 'Hồ Phú Ninh', 57),
        ('thu-bon-river', 'Sông Thu Bồn', 7),
        ('an-bang-beach', 'Bãi biển An Bàng', 7),
        ('cu-lao-cham', 'Cù Lao Chàm', 59),
        ('dragon-bridge', 'Cầu Rồng', 7),
        ('han-river-bridge', 'Cầu Sông Hàn', 7),
        ('tran-thi-ly-bridge', 'Cầu Trần Thị Lý', 7),
        ('thuan-phuoc-bridge', 'Cầu Thuận Phước', 7),
        ('nguyen-van-troi-bridge', 'Cầu Nguyễn Văn Trỗi', 7),
        ('da-nang-cathedral', 'Nhà thờ Chính tòa Đà Nẵng', 11),
        ('linh-ung-pagoda', 'Chùa Linh Ứng Sơn Trà', 11),
        ('marble-mountains', 'Danh thắng Ngũ Hành Sơn', 9),
        ('nui-than-tai-park', 'Công viên Suối khoáng nóng Núi Thần Tài', 16),
        ('ba-na-hills', 'Sun World Bà Nà Hills', 16),
        ('cham-sculpture-museum', 'Bảo tàng Điêu khắc Chăm Đà Nẵng', 8),
        ('da-nang-museum', 'Bảo tàng Đà Nẵng', 8),
        ('da-nang-fine-arts-museum', 'Bảo tàng Mỹ thuật Đà Nẵng', 8),
        ('ho-chi-minh-museum', 'Bảo tàng Hồ Chí Minh - Chi nhánh Quân khu 5', 8),
        ('dong-dinh-museum', 'Bảo tàng Đồng Đình', 8),
        ('asia-park', 'Công viên Châu Á - Asia Park', 16),
        ('east-sea-park', 'Công viên Biển Đông', 10),
        ('apec-park', 'Công viên APEC', 10),
        ('29-3-park', 'Công viên 29/3', 10),
        ('banh-xeo-76', 'Bánh Xèo 76', 1),
        ('bun-bo-hue-ba-thuong', 'Bún Bò Huế Bà Thương', 1),
        ('que-xua-restaurant', 'Nhà hàng Quê Xưa', 1),
        ('shamballa-vegetarian', 'Nhà hàng chay Shamballa', 1),
        ('bep-cuon', 'Bếp Cuốn', 1),
        ('bun-rieu-cua-39', 'Bún Riêu Cua 39', 1),
        ('moc-restaurant', 'Nhà hàng Mộc', 1),
        ('la-maison-1888', 'La Maison 1888', 2),
        ('nen-danang', 'Nén Đà Nẵng', 2),
        ('pizza-4p-hoang-van-thu', 'Pizza 4P''s Hoàng Văn Thụ', 2),
        ('madam-lan', 'Nhà hàng Madame Lân', 1),
        ('waterfront-danang', 'Waterfront Đà Nẵng', 2),
        ('fat-fish-da-nang', 'Fatfish Đà Nẵng', 2),
        ('le-rendez-vous', 'Le Rendez-Vous', 2),
        ('red-sky-steakhouse', 'Red Sky Steakhouse', 2),
        ('burger-bros', 'Burger Bros', 2),
        ('sofia-restaurant', 'Nhà hàng Sofia', 1),
        ('blue-whale-restaurant', 'Blue Whale Restaurant', 2),
        ('my-casa', 'My Casa', 2),
        ('limoncello', 'Limoncello', 2),
        ('der-morgen-coffee', 'Der Morgen Coffee', 3),
        ('das-chill-coffee', 'Das-Chill Coffee', 3),
        ('trinh-cafe', 'Trịnh Cà Phê', 3),
        ('starbucks-bach-dang', 'Starbucks Bạch Đằng', 3),
        ('horizon-bar', 'Horizon Bar', 4),
        ('ador-coffee', 'ADOR Coffee', 3),
        ('trangcasa-cafe', 'Trangcasa Café', 3),
        ('dau-ngot-cafe', 'Đậu Ngọt Café', 3),
        ('danang-marriott-resort', 'Danang Marriott Resort & Spa', 5),
        ('melia-danang-resort', 'Meliá Danang Beach Resort', 5),
        ('new-world-hoiana', 'New World Hoiana Beach Resort', 5),
        ('muong-thanh-luxury', 'Mường Thanh Luxury Đà Nẵng', 6),
        ('monarque-hotel', 'Monarque Hotel Đà Nẵng', 6),
        ('tms-hotel-da-nang', 'TMS Hotel Đà Nẵng Beach', 6),
        ('haian-beach-hotel', 'HAIAN Beach Hotel & Spa', 6),
        ('the-blossom-resort', 'The Blossom Resort Island', 5),
        ('balcona-hotel', 'Balcona Hotel Đà Nẵng', 6),
        ('holiday-beach-hotel', 'Holiday Beach Danang Hotel & Resort', 6),
        ('intercontinental-resort', 'InterContinental Danang Sun Peninsula Resort', 5),
        ('sheraton-grand-resort', 'Sheraton Grand Danang Resort', 5),
        ('pullman-danang-resort', 'Pullman Danang Beach Resort', 5),
        ('novotel-han-river', 'Novotel Danang Premier Han River', 6),
        ('brilliant-hotel', 'Brilliant Hotel Đà Nẵng', 6),
        ('danang-new-year-2026', 'Lễ hội Chào năm mới Đà Nẵng 2026', 43),
        ('tet-festival-2026', 'Lễ hội Tết Đà Nẵng 2026', 43),
        ('festival-of-light', 'Lễ hội Ánh sáng Đà Nẵng', 43),
        ('da-nang-color-festival', 'Lễ hội Sắc màu Đà Nẵng', 43),
        ('quan-the-am-festival', 'Lễ hội Quán Thế Âm Ngũ Hành Sơn', 43),
        ('cau-ngu-festival', 'Lễ hội Cầu Ngư', 43),
        ('dragon-boat-racing', 'Lễ hội đua thuyền trên sông Hàn', 43),
        ('diff-festival', 'Lễ hội Pháo hoa Quốc tế Đà Nẵng', 43),
        ('han-market', 'Chợ Hàn', 14),
        ('con-market', 'Chợ Cồn', 14),
        ('helio-night-market', 'Chợ đêm Helio', 65),
        ('son-tra-night-market', 'Chợ đêm Sơn Trà', 65),
        ('an-thuong-night-market', 'Chợ đêm An Thượng', 65),
        ('lotte-mart-da-nang', 'Lotte Mart Đà Nẵng', 13),
        ('vincom-plaza-da-nang', 'Vincom Plaza Đà Nẵng', 13),
        ('go-da-nang', 'GO! Đà Nẵng', 13),
        ('highlands-coffee-bach-dang', 'Highlands Coffee Bạch Đằng', 3),
        ('phuc-long-coffee-tea', 'Phúc Long Coffee & Tea', 3),
        ('the-coffee-house-danang', 'The Coffee House Đà Nẵng', 3),
        ('cong-coffee-bach-dang', 'Cộng Cà Phê Bạch Đằng', 3),
        ('memory-lounge-danang', 'Memory Lounge Đà Nẵng', 4),
        ('brodard-tea-house', 'Brodard Tea House', 3),
        ('pullman-executive-lounge', 'Pullman Executive Lounge', 4),
        ('hilton-da-nang', 'Hilton Đà Nẵng', 6),
        ('four-points-sheraton-danang', 'Four Points by Sheraton Đà Nẵng', 6),
        ('quan-bun-co-ha', 'Quán bún cô Hà', 1),
        ('chua-lien-chieu', 'Chùa Liên Chiểu', 11),
        ('hue-imperial-city', 'Đại Nội Huế', 8),
        ('bai-bien-lang-co', 'Bãi biển Lăng Cô', 7),
        ('lang-co-beach', 'Bãi biển Lăng Cô', 7),
        ('hai-van-pass', 'Đèo Hải Vân', 9),
        ('vinwonders-nam-hoi-an', 'VinWonders Nam Hội An', 16),
        ('son-tra-peninsula', 'Bán đảo Sơn Trà', 7),
        ('tra-que-vegetable-village', 'Làng rau Trà Quế', 61),
        ('tam-giang-lagoon', 'Phá Tam Giang', 7),
        ('diem-luu-tru-nguyen-duc-chung', 'Điểm lưu trú Nguyễn Đức Chung', 6),
        ('4-seasons-danang-hostel', '4 Seasons Danang Hostel', 6)
)
UPDATE locations l
SET
    name = canonical.canonical_name,
    category_id = canonical.category_id,
    subcategory_id = NULL,
    updated_at = NOW()
FROM canonical
WHERE l.slug = canonical.slug;

-- Restore the records whose values were shifted to the next slug by the legacy id-based seed.
WITH corrected(slug, address, district, status) AS (
    VALUES
        ('lang-co-beach', 'Thị trấn Lăng Cô, huyện Phú Lộc, thành phố Huế', 'Phú Lộc', 'active'),
        ('hai-van-pass', 'Đèo Hải Vân, giáp ranh Đà Nẵng và thành phố Huế', 'Liên Chiểu', 'active'),
        ('vinwonders-nam-hoi-an', 'Đường Võ Chí Công, xã Bình Minh, huyện Thăng Bình, Quảng Nam', 'Thăng Bình', 'active'),
        ('son-tra-peninsula', 'Bán đảo Sơn Trà, quận Sơn Trà, Đà Nẵng', 'Sơn Trà', 'active'),
        ('tra-que-vegetable-village', 'Làng Trà Quế, phường Cẩm Hà, Hội An, Quảng Nam', 'Hội An', 'active'),
        ('tam-giang-lagoon', 'Phá Tam Giang, thành phố Huế', 'Huế', 'active'),
        ('hue-imperial-city', 'Đường 23 Tháng 8, phường Phú Hậu, thành phố Huế', 'Huế', 'pending_review'),
        ('bai-bien-lang-co', 'Thị trấn Lăng Cô, huyện Phú Lộc, thành phố Huế', 'Phú Lộc', 'pending_review'),
        ('diem-luu-tru-nguyen-duc-chung', '139 Nguyễn Đức Chung, Đà Nẵng', 'Đà Nẵng', 'pending_review'),
        ('4-seasons-danang-hostel', '69 Châu Thị Vĩnh Tế, quận Ngũ Hành Sơn, Đà Nẵng', 'Ngũ Hành Sơn', 'pending_review')
)
UPDATE locations l
SET
    address = corrected.address,
    district = corrected.district,
    status = corrected.status,
    updated_at = NOW()
FROM corrected
WHERE l.slug = corrected.slug;

-- Normalize common unaccented Vietnamese fragments in legacy addresses.
UPDATE locations
SET
    address = replace(
        replace(
            replace(
                replace(
                    replace(
                        replace(
                            replace(
                                replace(
                                    replace(
                                        replace(
                                            replace(
                                                replace(
                                                    replace(
                                                        replace(
                                                            replace(
                                                                replace(
                                                                    replace(
                                                                        replace(
                                                                            replace(address, 'Da Nang', 'Đà Nẵng'),
                                                                            'Danang', 'Đà Nẵng'
                                                                        ),
                                                                        'Vietnam', 'Việt Nam'
                                                                    ),
                                                                    'Quang Nam', 'Quảng Nam'
                                                                ),
                                                                'Duy Xuyen', 'Duy Xuyên'
                                                            ),
                                                            'Thang Binh', 'Thăng Bình'
                                                        ),
                                                        'Dong Giang', 'Đông Giang'
                                                    ),
                                                    'Nui Thanh', 'Núi Thành'
                                                ),
                                                'Phu Ninh', 'Phú Ninh'
                                            ),
                                            'Thuan Phuoc', 'Thuận Phước'
                                        ),
                                        'Nguyen Tri Phuong', 'Nguyễn Tri Phương'
                                    ),
                                    'Hung Vuong', 'Hùng Vương'
                                ),
                                'Ngo Quyen', 'Ngô Quyền'
                            ),
                            'Bach Dang', 'Bạch Đằng'
                        ),
                        'Phan Chau Trinh', 'Phan Châu Trinh'
                    ),
                    'Hoang Van Thu', 'Hoàng Văn Thụ'
                ),
                'An Thuong', 'An Thượng'
            ),
            'Truong Sa', 'Trường Sa'
        ),
        '2 Thang 9', '2 Tháng 9'
    ),
    district = replace(
        replace(
            replace(
                replace(district, 'Quang Nam', 'Quảng Nam'),
                'Thang Binh', 'Thăng Bình'
            ),
            'Da Nang', 'Đà Nẵng'
        ),
        ' District', ''
    ),
    updated_at = NOW();

-- Targeted address corrections that cannot be handled safely by global replacement.
WITH corrected(slug, address, district) AS (
    VALUES
        ('hoi-an-ancient-town', 'Phường Minh An, Hội An, Quảng Nam', 'Hội An'),
        ('hoi-an-memories-land', 'Cồn Hến, phường Cẩm An, Hội An, Quảng Nam', 'Hội An'),
        ('bay-mau-coconut-forest', 'Xã Cẩm Thanh, Hội An, Quảng Nam', 'Hội An'),
        ('tam-thanh-beach', 'Xã Tam Thanh, thành phố Tam Kỳ, Quảng Nam', 'Tam Kỳ'),
        ('binh-minh-beach', 'Xã Bình Minh, huyện Thăng Bình, Quảng Nam', 'Thăng Bình'),
        ('dong-giang-heavens-gate', 'Huyện Đông Giang, Quảng Nam', 'Đông Giang'),
        ('my-son-sanctuary', 'Xã Duy Phú, huyện Duy Xuyên, Quảng Nam', 'Duy Xuyên'),
        ('ban-than-scenic-area', 'Xã Tam Hải, huyện Núi Thành, Quảng Nam', 'Núi Thành'),
        ('phu-ninh-lake', 'Huyện Phú Ninh, Quảng Nam', 'Phú Ninh'),
        ('thu-bon-river', 'Hội An, Quảng Nam', 'Hội An'),
        ('an-bang-beach', 'Phường Cẩm An, Hội An, Quảng Nam', 'Hội An'),
        ('cu-lao-cham', 'Xã Tân Hiệp, Hội An, Quảng Nam', 'Hội An'),
        ('linh-ung-pagoda', 'Bãi Bụt, bán đảo Sơn Trà, Đà Nẵng', 'Sơn Trà'),
        ('cham-sculpture-museum', '02 đường 2 Tháng 9, quận Hải Châu, Đà Nẵng', 'Hải Châu'),
        ('asia-park', '01 Phan Đăng Lưu, quận Hải Châu, Đà Nẵng', 'Hải Châu'),
        ('29-3-park', 'Đường Điện Biên Phủ, quận Thanh Khê, Đà Nẵng', 'Thanh Khê'),
        ('banh-xeo-76', '85A Lê Văn Hưu, quận Ngũ Hành Sơn, Đà Nẵng', 'Ngũ Hành Sơn'),
        ('bun-bo-hue-ba-thuong', '23 Trần Quốc Toản, quận Hải Châu, Đà Nẵng', 'Hải Châu'),
        ('que-xua-restaurant', '116 Núi Thành, quận Hải Châu, Đà Nẵng', 'Hải Châu'),
        ('bep-cuon', '31 Trần Bạch Đằng, quận Ngũ Hành Sơn, Đà Nẵng', 'Ngũ Hành Sơn'),
        ('bun-rieu-cua-39', '39 Lê Hồng Phong, quận Hải Châu, Đà Nẵng', 'Hải Châu'),
        ('moc-restaurant', '26 Tô Hiến Thành, quận Sơn Trà, Đà Nẵng', 'Sơn Trà'),
        ('nen-danang', '16 Mỹ Đa Tây 2, quận Ngũ Hành Sơn, Đà Nẵng', 'Ngũ Hành Sơn'),
        ('pizza-4p-hoang-van-thu', '08 Hoàng Văn Thụ, quận Hải Châu, Đà Nẵng', 'Hải Châu'),
        ('le-rendez-vous', '20 Lý Thường Kiệt, quận Hải Châu, Đà Nẵng', 'Hải Châu'),
        ('sofia-restaurant', 'Lô 1-2 Phạm Văn Đồng, quận Sơn Trà, Đà Nẵng', 'Sơn Trà'),
        ('my-casa', '52 Võ Nghĩa, quận Sơn Trà, Đà Nẵng', 'Sơn Trà'),
        ('der-morgen-coffee', '07 Lê Hồng Phong, quận Hải Châu, Đà Nẵng', 'Hải Châu'),
        ('das-chill-coffee', '37 Trần Quý Cáp, quận Hải Châu, Đà Nẵng', 'Hải Châu'),
        ('trinh-cafe', '111 Nguyễn Hữu Thọ, quận Cẩm Lệ, Đà Nẵng', 'Cẩm Lệ'),
        ('trangcasa-cafe', '186 Phan Châu Trinh, quận Hải Châu, Đà Nẵng', 'Hải Châu'),
        ('dau-ngot-cafe', '92 Phan Châu Trinh, quận Hải Châu, Đà Nẵng', 'Hải Châu'),
        ('the-blossom-resort', 'Đường 2 Tháng 9, phường Hòa Cường Bắc, quận Hải Châu, Đà Nẵng', 'Hải Châu'),
        ('sheraton-grand-resort', '35 Trường Sa, quận Ngũ Hành Sơn, Đà Nẵng', 'Ngũ Hành Sơn'),
        ('da-nang-color-festival', 'Bãi biển Mỹ Khê, Đà Nẵng', 'Sơn Trà'),
        ('han-market', '119 Trần Phú, quận Hải Châu, Đà Nẵng', 'Hải Châu'),
        ('con-market', '290 Hùng Vương, quận Hải Châu, Đà Nẵng', 'Hải Châu'),
        ('helio-night-market', 'Đường 2 Tháng 9, quận Hải Châu, Đà Nẵng', 'Hải Châu'),
        ('son-tra-night-market', 'Đường Lý Nam Đế, quận Sơn Trà, Đà Nẵng', 'Sơn Trà'),
        ('an-thuong-night-market', 'Đường An Thượng 4, quận Ngũ Hành Sơn, Đà Nẵng', 'Ngũ Hành Sơn'),
        ('lotte-mart-da-nang', '06 Nại Nam, quận Hải Châu, Đà Nẵng', 'Hải Châu'),
        ('vincom-plaza-da-nang', '910A Ngô Quyền, quận Sơn Trà, Đà Nẵng', 'Sơn Trà'),
        ('go-da-nang', '255-257 Hùng Vương, quận Thanh Khê, Đà Nẵng', 'Thanh Khê')
)
UPDATE locations l
SET
    address = corrected.address,
    district = corrected.district,
    updated_at = NOW()
FROM corrected
WHERE l.slug = corrected.slug;

-- Replace all public summaries/descriptions with Vietnamese copy after taxonomy is corrected.
UPDATE locations
SET
    short_description = CASE
        WHEN category_id IN (1, 2, 36) THEN name || ' là địa điểm ẩm thực phù hợp để tham khảo khi khám phá Đà Nẵng và khu vực miền Trung.'
        WHEN category_id = 3 THEN name || ' là địa điểm cà phê, đồ uống phù hợp để nghỉ chân và gặp gỡ tại Đà Nẵng.'
        WHEN category_id = 4 THEN name || ' là không gian thư giãn, gặp gỡ và thưởng thức đồ uống tại Đà Nẵng.'
        WHEN category_id IN (5, 6, 56) THEN name || ' là cơ sở lưu trú phục vụ du khách tại Đà Nẵng và khu vực miền Trung.'
        WHEN category_id IN (13, 14, 15, 65, 75) THEN name || ' là địa điểm mua sắm, tham quan và trải nghiệm đời sống địa phương.'
        WHEN category_id = 43 THEN name || ' là sự kiện văn hóa, giải trí dành cho người dân và du khách.'
        WHEN category_id IN (8, 11, 12, 51, 52, 64) THEN name || ' là điểm tham quan văn hóa, lịch sử đáng chú ý tại miền Trung.'
        WHEN category_id IN (7, 9, 10, 16, 57, 58, 59, 61) THEN name || ' là điểm tham quan và trải nghiệm nổi bật trong hành trình khám phá miền Trung.'
        ELSE name || ' là địa điểm phục vụ nhu cầu tham quan và trải nghiệm của du khách.'
    END,
    description = CASE
        WHEN category_id IN (1, 2, 36) THEN name || ' cung cấp trải nghiệm ẩm thực cho người dân và du khách. Thông tin địa chỉ, mức giá, giờ hoạt động và dịch vụ cần được đối chiếu trước mỗi chuyến đi.'
        WHEN category_id = 3 THEN name || ' là điểm dừng chân dành cho khách muốn thưởng thức cà phê và đồ uống. Du khách nên kiểm tra giờ mở cửa và tình trạng hoạt động trước khi đến.'
        WHEN category_id = 4 THEN name || ' là địa điểm thư giãn và gặp gỡ tại Đà Nẵng. Thông tin chương trình, giờ hoạt động và quy định phục vụ có thể thay đổi theo thời điểm.'
        WHEN category_id IN (5, 6, 56) THEN name || ' cung cấp dịch vụ lưu trú cho du khách. Giá phòng, tiện nghi và chính sách nhận trả phòng cần được xác nhận trực tiếp với cơ sở trước khi đặt.'
        WHEN category_id IN (13, 14, 15, 65, 75) THEN name || ' là địa điểm mua sắm và trải nghiệm đời sống địa phương. Giờ hoạt động, gian hàng và dịch vụ có thể thay đổi theo ngày.'
        WHEN category_id = 43 THEN name || ' là hoạt động văn hóa, giải trí được tổ chức theo thời gian cụ thể. Du khách cần kiểm tra lịch chính thức, địa điểm và điều kiện tham dự trước khi đi.'
        WHEN category_id IN (8, 11, 12, 51, 52, 64) THEN name || ' mang giá trị văn hóa, lịch sử hoặc nghệ thuật của miền Trung. Khi tham quan, du khách nên tôn trọng quy định tại điểm đến và kiểm tra giờ mở cửa.'
        WHEN category_id IN (7, 9, 10, 16, 57, 58, 59, 61) THEN name || ' là điểm đến phù hợp để kết hợp trong lịch trình khám phá Đà Nẵng, Hội An, Quảng Nam và thành phố Huế. Thời tiết, vé tham quan và giờ hoạt động nên được kiểm tra trước chuyến đi.'
        ELSE name || ' là địa điểm được tổng hợp phục vụ tra cứu du lịch. Thông tin vận hành nên được xác minh trước khi sử dụng.'
    END,
    updated_at = NOW();

-- Keep unverified lodging outside the public catalog.
UPDATE locations
SET status = 'pending_review', updated_at = NOW()
WHERE slug IN ('diem-luu-tru-nguyen-duc-chung', '4-seasons-danang-hostel');

COMMIT;
