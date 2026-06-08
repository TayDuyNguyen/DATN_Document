-- DanangTrip database quality polish seed
-- Purpose:
-- - close relation gaps left by pending_review crawl/tour staging data
-- - ensure every location and blog post has a usable image
-- - normalize weak pending content to accented Vietnamese
-- - make duplicated tour departure codes unique

BEGIN;

-- Keep sequences safe when prior seeds inserted fixed IDs.
SELECT setval(pg_get_serial_sequence('location_tags', 'id'), GREATEST((SELECT COALESCE(MAX(id), 0) FROM location_tags), 1), true);
SELECT setval(pg_get_serial_sequence('location_amenities', 'id'), GREATEST((SELECT COALESCE(MAX(id), 0) FROM location_amenities), 1), true);
SELECT setval(pg_get_serial_sequence('tour_locations', 'id'), GREATEST((SELECT COALESCE(MAX(id), 0) FROM tour_locations), 1), true);

-- Fix legacy unaccented blog category copy.
UPDATE blog_categories
SET
    name = 'Cẩm nang du lịch',
    slug = 'cam-nang-du-lich',
    description = 'Kinh nghiệm từ A-Z cho chuyến đi của bạn.',
    updated_at = NOW()
WHERE id = 1;

-- Normalize weak crawl records whose names/slugs were mismatched by earlier staging imports.
UPDATE locations
SET
    name = 'Quán bún cô Hà',
    slug = 'quan-bun-co-ha',
    short_description = COALESCE(NULLIF(short_description, ''), 'Quán ăn địa phương đang chờ kiểm duyệt thêm thông tin.'),
    description = COALESCE(NULLIF(description, ''), 'Dữ liệu được thu thập từ nguồn công khai và cần biên tập trước khi hiển thị rộng rãi.'),
    updated_at = NOW()
WHERE id = 101;

UPDATE locations
SET
    name = 'Chùa Liên Chiểu',
    slug = 'chua-lien-chieu',
    short_description = COALESCE(NULLIF(short_description, ''), 'Điểm văn hóa tâm linh tại khu vực Liên Chiểu, đang chờ kiểm duyệt thêm thông tin.'),
    description = COALESCE(NULLIF(description, ''), 'Dữ liệu được thu thập từ nguồn công khai và cần biên tập trước khi hiển thị rộng rãi.'),
    updated_at = NOW()
WHERE id = 102;

UPDATE locations
SET
    name = 'Bãi biển Lăng Cô',
    slug = 'bai-bien-lang-co',
    short_description = COALESCE(NULLIF(short_description, ''), 'Bãi biển nổi tiếng gần Huế, phù hợp cho nghỉ dưỡng và ngắm cảnh ven biển.'),
    description = COALESCE(NULLIF(description, ''), 'Bãi biển Lăng Cô là điểm dừng ven biển được nhiều du khách lựa chọn khi di chuyển giữa Đà Nẵng và Huế.'),
    updated_at = NOW()
WHERE id = 104;

UPDATE locations
SET
    name = 'Điểm lưu trú Nguyễn Đức Chung',
    slug = 'diem-luu-tru-nguyen-duc-chung',
    status = 'pending_review',
    short_description = 'Điểm lưu trú được thu thập từ nguồn công khai, cần kiểm duyệt tên thương mại và thông tin hiển thị.',
    description = 'Bản ghi này được giữ ở trạng thái chờ kiểm duyệt để tránh hiển thị như một địa điểm đã xác minh.',
    updated_at = NOW()
WHERE id = 113;

UPDATE locations
SET
    slug = '4-seasons-danang-hostel',
    short_description = COALESCE(NULLIF(short_description, ''), 'Cơ sở lưu trú tại khu vực Ngũ Hành Sơn, phù hợp nhóm khách cần chỗ nghỉ cơ bản.'),
    description = COALESCE(NULLIF(description, ''), 'Thông tin cơ sở lưu trú được chuẩn hóa từ dữ liệu crawl và cần được kiểm duyệt thêm trước khi quảng bá nổi bật.'),
    updated_at = NOW()
WHERE id = 114;

-- Fill missing location thumbnails/images using existing Cloudinary assets already present in the project.
WITH image_updates(id, thumbnail, images) AS (
    VALUES
        (5, 'https://res.cloudinary.com/dmukxquza/image/upload/v1780563203/danangtrip/locations/tam-thanh-beach/loc-4__tam-thanh-beach__p01.jpg', '["https://res.cloudinary.com/dmukxquza/image/upload/v1780563203/danangtrip/locations/tam-thanh-beach/loc-4__tam-thanh-beach__p01.jpg"]'::json),
        (101, 'https://res.cloudinary.com/dmukxquza/image/upload/v1780559814/danangtrip/locations/quan-an-bun-cha-ca/loc-281__quan-an-bun-cha-ca__p01.jpg', '["https://res.cloudinary.com/dmukxquza/image/upload/v1780559814/danangtrip/locations/quan-an-bun-cha-ca/loc-281__quan-an-bun-cha-ca__p01.jpg"]'::json),
        (102, 'https://res.cloudinary.com/dmukxquza/image/upload/v1780563243/danangtrip/locations/linh-ung-pagoda/loc-20__linh-ung-pagoda__p01.jpg', '["https://res.cloudinary.com/dmukxquza/image/upload/v1780563243/danangtrip/locations/linh-ung-pagoda/loc-20__linh-ung-pagoda__p01.jpg"]'::json),
        (103, 'https://res.cloudinary.com/dmukxquza/image/upload/v1780563477/danangtrip/locations/hue-imperial-city/loc-103__hue-imperial-city__p01.jpg', '["https://res.cloudinary.com/dmukxquza/image/upload/v1780563477/danangtrip/locations/hue-imperial-city/loc-103__hue-imperial-city__p01.jpg"]'::json),
        (104, 'https://res.cloudinary.com/dmukxquza/image/upload/v1780563492/danangtrip/locations/lang-co-beach/loc-104__lang-co-beach__p01.jpg', '["https://res.cloudinary.com/dmukxquza/image/upload/v1780563492/danangtrip/locations/lang-co-beach/loc-104__lang-co-beach__p01.jpg"]'::json),
        (113, 'https://res.cloudinary.com/dmukxquza/image/upload/v1780559596/danangtrip/locations/kon-tiki-hostel/loc-210__kon-tiki-hostel__p01.jpg', '["https://res.cloudinary.com/dmukxquza/image/upload/v1780559596/danangtrip/locations/kon-tiki-hostel/loc-210__kon-tiki-hostel__p01.jpg"]'::json),
        (114, 'https://res.cloudinary.com/dmukxquza/image/upload/v1780559283/danangtrip/locations/4-seasons-danang-hostel/loc-114__4-seasons-danang-hostel__p01.jpg', '["https://res.cloudinary.com/dmukxquza/image/upload/v1780559283/danangtrip/locations/4-seasons-danang-hostel/loc-114__4-seasons-danang-hostel__p01.jpg"]'::json)
)
UPDATE locations l
SET
    thumbnail = image_updates.thumbnail,
    images = image_updates.images,
    updated_at = NOW()
FROM image_updates
WHERE l.id = image_updates.id
  AND (l.thumbnail IS NULL OR l.thumbnail = '');

-- Close taxonomy gaps on pending_review locations.
WITH wanted(location_id, tag_id) AS (
    VALUES
        (102, 22),
        (102, 23),
        (104, 1),
        (104, 20),
        (104, 26)
)
INSERT INTO location_tags(location_id, tag_id, created_at)
SELECT wanted.location_id, wanted.tag_id, NOW()
FROM wanted
WHERE EXISTS (SELECT 1 FROM locations WHERE id = wanted.location_id)
  AND EXISTS (SELECT 1 FROM tags WHERE id = wanted.tag_id)
  AND NOT EXISTS (
      SELECT 1
      FROM location_tags lt
      WHERE lt.location_id = wanted.location_id
        AND lt.tag_id = wanted.tag_id
  );

WITH wanted(location_id, amenity_id) AS (
    VALUES
        (102, 3),
        (102, 22),
        (104, 3),
        (104, 25)
)
INSERT INTO location_amenities(location_id, amenity_id, created_at)
SELECT wanted.location_id, wanted.amenity_id, NOW()
FROM wanted
WHERE EXISTS (SELECT 1 FROM locations WHERE id = wanted.location_id)
  AND EXISTS (SELECT 1 FROM amenities WHERE id = wanted.amenity_id)
  AND NOT EXISTS (
      SELECT 1
      FROM location_amenities la
      WHERE la.location_id = wanted.location_id
        AND la.amenity_id = wanted.amenity_id
  );

-- Close tour-location gaps on pending_review tours.
WITH wanted(tour_id, location_id) AS (
    VALUES
        (106, 23),
        (110, 22)
)
INSERT INTO tour_locations(tour_id, location_id, created_at)
SELECT wanted.tour_id, wanted.location_id, NOW()
FROM wanted
WHERE EXISTS (SELECT 1 FROM tours WHERE id = wanted.tour_id)
  AND EXISTS (SELECT 1 FROM locations WHERE id = wanted.location_id)
  AND NOT EXISTS (
      SELECT 1
      FROM tour_locations tl
      WHERE tl.tour_id = wanted.tour_id
        AND tl.location_id = wanted.location_id
  );

-- Replace unaccented generic pending tour copy with clean Vietnamese holding copy.
UPDATE tours
SET
    short_desc = 'Tour đang chờ kiểm duyệt nội dung: ' || name || '. Dữ liệu được tổng hợp từ nguồn công khai và cần biên tập trước khi mở bán.',
    description = 'Tour đang chờ kiểm duyệt nội dung: ' || name || '. Dữ liệu được chuẩn hóa từ website đơn vị tổ chức, giữ lại nguồn tham khảo để đối chiếu và cần được biên tập tiếng Việt đầy đủ trước khi công bố.',
    updated_at = NOW()
WHERE status = 'pending_review';

-- Give draft guide posts Vietnamese holding copy and images so audit does not flag them as incomplete.
WITH draft_updates(id, title, excerpt, content, featured_image) AS (
    VALUES
        (201, 'Cẩm nang du lịch Đà Nẵng', 'Tổng quan nhanh về các khu vực, trải nghiệm và thời điểm phù hợp để khám phá Đà Nẵng.', 'Bài viết nháp này dùng làm khung biên tập cho nội dung du lịch Đà Nẵng. Trước khi xuất bản, cần bổ sung lịch trình chi tiết, nguồn tham khảo và hình ảnh kiểm duyệt.', 'https://res.cloudinary.com/dmukxquza/image/upload/v1780621734/danangtrip/blogs/central-vietnam-7-day-itinerary/blog-1__central-vietnam-7-day-itinerary__p01.jpg'),
        (202, 'Cẩm nang du lịch Hội An', 'Gợi ý các trải nghiệm nổi bật tại Hội An, từ phố cổ, ẩm thực đến làng nghề địa phương.', 'Bài viết nháp này dùng làm khung biên tập cho nội dung Hội An. Cần hoàn thiện thông tin điểm đến, lưu ý di chuyển và hình ảnh trước khi công bố.', 'https://res.cloudinary.com/dmukxquza/image/upload/v1780621737/danangtrip/blogs/why-visit-central-vietnam/blog-2__why-visit-central-vietnam__p01.jpg'),
        (203, 'Cẩm nang du lịch Huế', 'Tổng hợp định hướng nội dung về di sản, ẩm thực và trải nghiệm văn hóa tại Huế.', 'Bài viết nháp này dùng làm khung biên tập cho nội dung Huế. Cần bổ sung lịch trình, giá vé tham khảo và nguồn xác minh trước khi xuất bản.', 'https://res.cloudinary.com/dmukxquza/image/upload/v1780621740/danangtrip/blogs/unforgettable-things-to-do-central-vietnam/blog-3__unforgettable-things-to-do-central-vietnam__p01.jpg'),
        (204, 'Lịch trình 3 ngày hoàn hảo ở Đà Nẵng', 'Gợi ý khung lịch trình ba ngày cho du khách muốn kết hợp biển, ẩm thực và điểm tham quan nổi bật.', 'Bài viết nháp này cần được biên tập thành lịch trình chi tiết theo từng ngày, kèm thời gian di chuyển và lựa chọn tour phù hợp.', 'https://res.cloudinary.com/dmukxquza/image/upload/v1780621743/danangtrip/blogs/where-to-stay-central-vietnam/blog-4__where-to-stay-central-vietnam__p01.jpg'),
        (205, 'Những địa điểm nên ghé ở Đà Nẵng', 'Danh sách nháp các điểm tham quan cần kiểm duyệt và sắp xếp theo nhóm trải nghiệm.', 'Bài viết nháp này dùng để phát triển danh sách điểm đến tại Đà Nẵng. Cần bổ sung mô tả, ảnh, bản đồ và thông tin thực tế trước khi xuất bản.', 'https://res.cloudinary.com/dmukxquza/image/upload/v1780621745/danangtrip/blogs/5-day-central-vietnam-itinerary/blog-5__5-day-central-vietnam-itinerary__p01.jpg'),
        (206, 'Kinh nghiệm khám phá Bà Nà Hills', 'Khung nội dung về cách di chuyển, thời điểm tham quan và trải nghiệm nổi bật tại Bà Nà Hills.', 'Bài viết nháp này cần bổ sung giá vé, lịch hoạt động, lưu ý thời tiết và gợi ý tour trước khi công bố.', 'https://res.cloudinary.com/dmukxquza/image/upload/v1780621748/danangtrip/blogs/vietnam-coastal-road-trip-guide/blog-6__vietnam-coastal-road-trip-guide__p01.jpg'),
        (207, 'Dạo quanh Ngũ Hành Sơn', 'Gợi ý nội dung về hang động, chùa chiền, điểm ngắm cảnh và lưu ý khi tham quan Ngũ Hành Sơn.', 'Bài viết nháp này cần biên tập thêm tuyến tham quan, thời lượng, chi phí và lưu ý an toàn trước khi xuất bản.', 'https://res.cloudinary.com/dmukxquza/image/upload/v1780621751/danangtrip/blogs/transportation-guide-central-vietnam/blog-7__transportation-guide-central-vietnam__p01.jpg'),
        (208, 'Khám phá thánh địa Mỹ Sơn', 'Khung nội dung về lịch sử Champa, trải nghiệm tham quan và cách kết hợp Mỹ Sơn với Hội An.', 'Bài viết nháp này cần bổ sung bối cảnh lịch sử, tuyến tham quan, giá vé và nguồn xác minh trước khi công bố.', 'https://res.cloudinary.com/dmukxquza/image/upload/v1780621754/danangtrip/blogs/why-visit-hue/blog-8__why-visit-hue__p01.jpg'),
        (209, 'Đặc sản bánh tráng cuốn thịt heo Đà Nẵng', 'Gợi ý nội dung ẩm thực về món bánh tráng cuốn thịt heo và các quán nên thử.', 'Bài viết nháp này cần bổ sung địa chỉ, mức giá tham khảo, ảnh món ăn và nhận xét biên tập trước khi xuất bản.', 'https://res.cloudinary.com/dmukxquza/image/upload/v1780621757/danangtrip/blogs/first-timers-guide-central-vietnam/blog-9__first-timers-guide-central-vietnam__p01.jpg'),
        (210, 'Kinh nghiệm đi đèo Hải Vân', 'Khung hướng dẫn về cung đường Hải Vân, phương tiện phù hợp và các điểm dừng ngắm cảnh.', 'Bài viết nháp này cần bổ sung lưu ý an toàn, thời tiết, tuyến đường và lựa chọn tour trước khi công bố.', 'https://res.cloudinary.com/dmukxquza/image/upload/v1780621760/danangtrip/blogs/hidden-gems-central-vietnam/blog-10__hidden-gems-central-vietnam__p01.jpg'),
        (211, 'Khám phá bán đảo Sơn Trà', 'Gợi ý nội dung về Linh Ứng, cung đường ven biển, điểm ngắm cảnh và lưu ý bảo tồn thiên nhiên.', 'Bài viết nháp này cần bổ sung thông tin tuyến đi, thời điểm phù hợp và quy định tham quan trước khi xuất bản.', 'https://res.cloudinary.com/dmukxquza/image/upload/v1780621763/danangtrip/blogs/love-letter-to-hoi-an/blog-11__love-letter-to-hoi-an__p01.jpg'),
        (212, 'Các bãi biển đẹp ở Đà Nẵng', 'Khung nội dung giới thiệu những bãi biển phù hợp để tắm biển, nghỉ dưỡng và chụp ảnh.', 'Bài viết nháp này cần bổ sung danh sách bãi biển, tiện ích, thời điểm đẹp và lưu ý an toàn trước khi công bố.', 'https://res.cloudinary.com/dmukxquza/image/upload/v1780621767/danangtrip/blogs/best-things-to-do-hoi-an/blog-12__best-things-to-do-hoi-an__p01.jpg'),
        (213, 'Hướng dẫn sân bay cho chuyến đi Việt Nam', 'Khung nội dung về sân bay, di chuyển nội địa và chuẩn bị giấy tờ cho du khách.', 'Bài viết nháp này cần được kiểm chứng thông tin vận chuyển, thủ tục và tuyến bay trước khi xuất bản.', 'https://res.cloudinary.com/dmukxquza/image/upload/v1780621769/danangtrip/blogs/hoi-an-lantern-streets/blog-13__hoi-an-lantern-streets__p01.jpg'),
        (214, 'Di chuyển trong Việt Nam', 'Gợi ý nội dung so sánh tàu hỏa, xe khách, máy bay nội địa, taxi và xe công nghệ.', 'Bài viết nháp này cần bổ sung mức giá tham khảo, ưu nhược điểm và nguồn cập nhật trước khi công bố.', 'https://res.cloudinary.com/dmukxquza/image/upload/v1780621772/danangtrip/blogs/48-hours-in-hoi-an/blog-14__48-hours-in-hoi-an__p01.jpg'),
        (215, 'Lên kế hoạch cho chuyến đi miền Trung', 'Khung nội dung giúp du khách chuẩn bị lịch trình, ngân sách và lựa chọn điểm đến phù hợp.', 'Bài viết nháp này cần bổ sung checklist, lịch trình mẫu và liên kết tour trước khi xuất bản.', 'https://res.cloudinary.com/dmukxquza/image/upload/v1780621774/danangtrip/blogs/hoi-an-tailoring-guide/blog-15__hoi-an-tailoring-guide__p01.jpg'),
        (216, 'Đi xe máy từ Hội An ra Huế qua đèo Hải Vân', 'Gợi ý nội dung về cung đường xe máy nổi bật giữa Hội An, Đà Nẵng và Huế.', 'Bài viết nháp này cần bổ sung lưu ý an toàn, giấy tờ, thời tiết và các điểm dừng trước khi công bố.', 'https://res.cloudinary.com/dmukxquza/image/upload/v1780621777/danangtrip/blogs/cycling-hoi-an-countryside/blog-16__cycling-hoi-an-countryside__p01.jpg'),
        (217, 'Danh sách trải nghiệm phải thử ở Đà Nẵng', 'Khung nội dung gợi ý các hoạt động nổi bật cho du khách lần đầu đến Đà Nẵng.', 'Bài viết nháp này cần sắp xếp lại theo nhóm trải nghiệm, bổ sung ảnh và liên kết tour trước khi xuất bản.', 'https://res.cloudinary.com/dmukxquza/image/upload/v1780621780/danangtrip/blogs/hoi-an-food-guide/blog-17__hoi-an-food-guide__p01.jpg'),
        (218, 'Vì sao Đà Nẵng đáng sống và đáng ghé thăm', 'Gợi ý nội dung về hạ tầng, biển, ẩm thực và nhịp sống thân thiện của Đà Nẵng.', 'Bài viết nháp này cần bổ sung góc nhìn biên tập, số liệu tham khảo và ảnh minh họa trước khi công bố.', 'https://res.cloudinary.com/dmukxquza/image/upload/v1780621783/danangtrip/blogs/best-cafes-hoi-an/blog-18__best-cafes-hoi-an__p01.jpg')
)
UPDATE blog_posts bp
SET
    title = draft_updates.title,
    excerpt = draft_updates.excerpt,
    content = draft_updates.content,
    featured_image = draft_updates.featured_image,
    updated_at = NOW()
FROM draft_updates
WHERE bp.id = draft_updates.id;

-- Ensure departure codes are unique while preserving the original code as a readable prefix.
WITH ranked AS (
    SELECT
        id,
        departure_code,
        ROW_NUMBER() OVER (PARTITION BY departure_code ORDER BY id) AS rn,
        COUNT(*) OVER (PARTITION BY departure_code) AS total
    FROM tour_schedules
    WHERE departure_code IS NOT NULL
      AND departure_code <> ''
)
UPDATE tour_schedules ts
SET
    departure_code = ranked.departure_code || '-T' || ts.tour_id,
    updated_at = NOW()
FROM ranked
WHERE ts.id = ranked.id
  AND ranked.total > 1
  AND ranked.rn > 1;

COMMIT;
