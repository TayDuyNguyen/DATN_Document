-- DanangTrip ratings Vietnamese editorial and realistic volume seed
-- Purpose:
--   Normalize all review comments to Vietnamese with full diacritics.
--   Expand the catalog from 100 to about 600 approved ratings.
--   Keep a realistic 2-5 star distribution and recalculate aggregate counters.
-- Policy:
--   Deterministic user/target pairs, idempotent through unique constraints.
--   No fabricated rating images are added.

BEGIN;

-- Rewrite the legacy unaccented comments using varied Vietnamese copy.
UPDATE ratings
SET
    comment = CASE
        WHEN location_id IS NOT NULL THEN CASE (id % 12)
            WHEN 0 THEN 'Không gian dễ tìm, nhân viên hỗ trợ khá nhanh. Cuối tuần hơi đông nhưng trải nghiệm nhìn chung tốt.'
            WHEN 1 THEN 'Địa điểm sạch sẽ, thông tin chỉ dẫn rõ ràng và phù hợp cho gia đình có trẻ nhỏ.'
            WHEN 2 THEN 'Cảnh quan đẹp, có nhiều góc chụp ảnh. Nên đến sớm để tránh đông người và thời tiết nắng gắt.'
            WHEN 3 THEN 'Mức giá tương đối hợp lý so với khu vực. Chất lượng dịch vụ ổn và nhân viên thân thiện.'
            WHEN 4 THEN 'Vị trí thuận tiện, có thể kết hợp tham quan với các điểm gần đó trong cùng một buổi.'
            WHEN 5 THEN 'Trải nghiệm thực tế tốt hơn mong đợi. Không gian thoáng và được chăm sóc khá chỉn chu.'
            WHEN 6 THEN 'Địa điểm đáng ghé khi đến miền Trung. Nên kiểm tra giờ mở cửa trước khi di chuyển.'
            WHEN 7 THEN 'Phù hợp để đi cùng bạn bè. Một số thời điểm khá đông nên cần chủ động đặt chỗ.'
            WHEN 8 THEN 'Chất lượng ở mức khá, cảnh quan đẹp nhưng khu vực gửi xe và lối vào có thể thuận tiện hơn.'
            WHEN 9 THEN 'Đã đến vào ngày thường nên khá thoải mái. Nhân viên hướng dẫn nhiệt tình và dễ trao đổi.'
            WHEN 10 THEN 'Không gian có nét riêng, phù hợp để nghỉ chân và trải nghiệm văn hóa địa phương.'
            ELSE 'Nhìn chung là một địa điểm ổn. Giá, thời gian phục vụ và tiện ích nên được cập nhật thường xuyên hơn.'
        END
        ELSE CASE (id % 12)
            WHEN 0 THEN 'Lịch trình hợp lý, hướng dẫn viên nhiệt tình và hỗ trợ đoàn trong suốt chuyến đi.'
            WHEN 1 THEN 'Xe đón đúng giờ, các điểm tham quan được sắp xếp vừa sức và không quá vội.'
            WHEN 2 THEN 'Tour phù hợp cho gia đình. Bữa ăn ổn, hướng dẫn viên giải thích rõ ràng và thân thiện.'
            WHEN 3 THEN 'Cảnh đẹp và lịch trình đáng trải nghiệm. Thời gian tự do tại một số điểm hơi ngắn.'
            WHEN 4 THEN 'Khâu tổ chức khá chuyên nghiệp, thông tin trước chuyến đi đầy đủ và dễ hiểu.'
            WHEN 5 THEN 'Chi phí hợp lý so với các dịch vụ đi kèm. Tôi sẽ cân nhắc đặt lại khi có dịp.'
            WHEN 6 THEN 'Chuyến đi diễn ra thuận lợi, điểm đón dễ tìm và hướng dẫn viên xử lý tình huống tốt.'
            WHEN 7 THEN 'Trải nghiệm tổng thể tốt. Nếu lịch khởi hành sớm hơn một chút sẽ tránh được đông khách.'
            WHEN 8 THEN 'Nội dung tour đúng mô tả, phương tiện sạch và lịch trình có thời gian nghỉ phù hợp.'
            WHEN 9 THEN 'Một vài điểm dừng khá nhanh nhưng đoàn vẫn tham quan được các điểm chính trong chương trình.'
            WHEN 10 THEN 'Hướng dẫn viên am hiểu địa phương, nhiệt tình chụp ảnh và hỗ trợ các thành viên lớn tuổi.'
            ELSE 'Tour ở mức khá, dịch vụ ổn định. Nên thông báo chi tiết hơn về các khoản chi phí cá nhân.'
        END
    END,
    updated_at = NOW();

-- Protect the sequence after the original fixed-id seed.
SELECT setval(
    pg_get_serial_sequence('ratings', 'id'),
    GREATEST((SELECT COALESCE(MAX(id), 0) FROM ratings), 1),
    true
);

-- Guarantee at least one approved review for every active location.
WITH uncovered AS (
    SELECT l.id AS location_id
    FROM locations l
    WHERE l.status = 'active'
      AND NOT EXISTS (
          SELECT 1
          FROM ratings r
          WHERE r.location_id = l.id
            AND r.status = 'approved'
      )
),
coverage AS (
    SELECT
        uncovered.location_id,
        reviewer.user_id
    FROM uncovered
    CROSS JOIN LATERAL (
        SELECT u.id AS user_id
        FROM users u
        WHERE u.role = 'user'
          AND u.status = 'active'
          AND NOT EXISTS (
              SELECT 1
              FROM ratings r
              WHERE r.user_id = u.id
                AND r.location_id = uncovered.location_id
          )
        ORDER BY md5('location-coverage-' || uncovered.location_id::text || '-' || u.id::text)
        LIMIT 1
    ) reviewer
)
INSERT INTO ratings (
    user_id, location_id, tour_id, booking_id, score, comment, image_count,
    status, rejected_reason, approved_by, approved_at, helpful_count,
    created_at, updated_at
)
SELECT
    coverage.user_id,
    coverage.location_id,
    NULL,
    NULL,
    CASE WHEN coverage.location_id % 4 = 0 THEN 4 ELSE 5 END,
    'Địa điểm có thông tin tương đối rõ ràng, thuận tiện đưa vào lịch trình và đáng để trải nghiệm khi có dịp.',
    0,
    'approved',
    NULL,
    1,
    NOW() - ((coverage.location_id % 60) || ' days')::interval,
    coverage.location_id % 7,
    NOW() - ((coverage.location_id % 120) || ' days')::interval,
    NOW()
FROM coverage
ON CONFLICT DO NOTHING;

-- Guarantee at least one approved review for every active tour.
WITH uncovered AS (
    SELECT t.id AS tour_id
    FROM tours t
    WHERE t.status = 'active'
      AND NOT EXISTS (
          SELECT 1
          FROM ratings r
          WHERE r.tour_id = t.id
            AND r.status = 'approved'
      )
),
coverage AS (
    SELECT
        uncovered.tour_id,
        reviewer.user_id
    FROM uncovered
    CROSS JOIN LATERAL (
        SELECT u.id AS user_id
        FROM users u
        WHERE u.role = 'user'
          AND u.status = 'active'
          AND NOT EXISTS (
              SELECT 1
              FROM ratings r
              WHERE r.user_id = u.id
                AND r.tour_id = uncovered.tour_id
          )
        ORDER BY md5('tour-coverage-' || uncovered.tour_id::text || '-' || u.id::text)
        LIMIT 1
    ) reviewer
)
INSERT INTO ratings (
    user_id, location_id, tour_id, booking_id, score, comment, image_count,
    status, rejected_reason, approved_by, approved_at, helpful_count,
    created_at, updated_at
)
SELECT
    coverage.user_id,
    NULL,
    coverage.tour_id,
    NULL,
    CASE WHEN coverage.tour_id % 5 = 0 THEN 4 ELSE 5 END,
    'Lịch trình đúng mô tả, nhân viên hỗ trợ nhiệt tình và các điểm tham quan được sắp xếp khá hợp lý.',
    0,
    'approved',
    NULL,
    1,
    NOW() - ((coverage.tour_id % 60) || ' days')::interval,
    coverage.tour_id % 7,
    NOW() - ((coverage.tour_id % 120) || ' days')::interval,
    NOW()
FROM coverage
ON CONFLICT DO NOTHING;

-- Fill the location review catalog to a stable target.
WITH candidates AS (
    SELECT
        u.id AS user_id,
        l.id AS location_id,
        ROW_NUMBER() OVER (
            ORDER BY md5('location-rating-' || u.id::text || '-' || l.id::text)
        ) AS rn
    FROM users u
    CROSS JOIN locations l
    WHERE u.role = 'user'
      AND u.status = 'active'
      AND l.status = 'active'
      AND NOT EXISTS (
          SELECT 1
          FROM ratings r
          WHERE r.user_id = u.id
            AND r.location_id = l.id
      )
),
selected AS (
    SELECT *
    FROM candidates
    WHERE rn <= GREATEST(
        360 - (SELECT COUNT(*) FROM ratings WHERE location_id IS NOT NULL),
        0
    )
)
INSERT INTO ratings (
    user_id, location_id, tour_id, booking_id, score, comment, image_count,
    status, rejected_reason, approved_by, approved_at, helpful_count,
    created_at, updated_at
)
SELECT
    selected.user_id,
    selected.location_id,
    NULL,
    NULL,
    CASE
        WHEN selected.rn % 20 = 0 THEN 2
        WHEN selected.rn % 6 = 0 THEN 3
        WHEN selected.rn % 3 = 0 THEN 4
        ELSE 5
    END,
    CASE (selected.rn % 16)
        WHEN 0 THEN 'Không gian đẹp và dễ tìm. Cuối tuần khá đông nhưng nhân viên vẫn hỗ trợ nhiệt tình.'
        WHEN 1 THEN 'Địa điểm phù hợp cho gia đình, khu vực chung sạch sẽ và có nhiều góc chụp ảnh.'
        WHEN 2 THEN 'Trải nghiệm tốt, cảnh quan thực tế đẹp hơn hình. Nên đến vào buổi sáng để thoải mái hơn.'
        WHEN 3 THEN 'Giá cả chấp nhận được, dịch vụ nhanh và nhân viên giao tiếp lịch sự.'
        WHEN 4 THEN 'Vị trí thuận tiện để kết hợp thêm các điểm gần đó. Thời gian tham quan khoảng hai giờ là hợp lý.'
        WHEN 5 THEN 'Không gian thoáng, chỉ dẫn rõ ràng. Khu vực gửi xe có thể đông vào giờ cao điểm.'
        WHEN 6 THEN 'Mình đi ngày thường nên không phải chờ lâu. Trải nghiệm nhìn chung rất dễ chịu.'
        WHEN 7 THEN 'Địa điểm có nét đặc trưng riêng, phù hợp với người muốn tìm hiểu văn hóa địa phương.'
        WHEN 8 THEN 'Cảnh đẹp, vệ sinh khá tốt. Nên mang theo nước và chuẩn bị chống nắng nếu đi buổi trưa.'
        WHEN 9 THEN 'Nhân viên thân thiện và xử lý yêu cầu nhanh. Giá niêm yết tương đối rõ ràng.'
        WHEN 10 THEN 'Một điểm dừng đáng cân nhắc trong lịch trình. Không gian đông nhưng vẫn có trật tự.'
        WHEN 11 THEN 'Trải nghiệm ổn, dịch vụ đúng mô tả. Mình mong khu vực nghỉ chân được bổ sung thêm chỗ ngồi.'
        WHEN 12 THEN 'Phù hợp đi cùng nhóm bạn, nhiều góc đẹp và thuận tiện di chuyển bằng xe công nghệ.'
        WHEN 13 THEN 'Chất lượng khá đồng đều, không gian sạch và nhân viên hướng dẫn chu đáo.'
        WHEN 14 THEN 'Địa điểm nổi bật, dễ kết hợp trong hành trình khám phá Đà Nẵng và Hội An.'
        ELSE 'Tổng thể tốt nhưng cần cập nhật giờ hoạt động rõ hơn trên các kênh trực tuyến.'
    END,
    0,
    'approved',
    NULL,
    1,
    NOW() - ((selected.rn % 120) || ' days')::interval,
    selected.rn % 13,
    NOW() - ((selected.rn % 180) || ' days')::interval,
    NOW()
FROM selected
ON CONFLICT DO NOTHING;

-- Fill the tour review catalog to a stable target.
WITH candidates AS (
    SELECT
        u.id AS user_id,
        t.id AS tour_id,
        ROW_NUMBER() OVER (
            ORDER BY md5('tour-rating-' || u.id::text || '-' || t.id::text)
        ) AS rn
    FROM users u
    CROSS JOIN tours t
    WHERE u.role = 'user'
      AND u.status = 'active'
      AND t.status = 'active'
      AND NOT EXISTS (
          SELECT 1
          FROM ratings r
          WHERE r.user_id = u.id
            AND r.tour_id = t.id
      )
),
selected AS (
    SELECT *
    FROM candidates
    WHERE rn <= GREATEST(
        260 - (SELECT COUNT(*) FROM ratings WHERE tour_id IS NOT NULL),
        0
    )
)
INSERT INTO ratings (
    user_id, location_id, tour_id, booking_id, score, comment, image_count,
    status, rejected_reason, approved_by, approved_at, helpful_count,
    created_at, updated_at
)
SELECT
    selected.user_id,
    NULL,
    selected.tour_id,
    NULL,
    CASE
        WHEN selected.rn % 25 = 0 THEN 2
        WHEN selected.rn % 7 = 0 THEN 3
        WHEN selected.rn % 3 = 0 THEN 4
        ELSE 5
    END,
    CASE (selected.rn % 16)
        WHEN 0 THEN 'Xe đón đúng giờ, hướng dẫn viên nhiệt tình và lịch trình được tổ chức khá hợp lý.'
        WHEN 1 THEN 'Tour phù hợp cho gia đình, các điểm dừng vừa sức và thời gian nghỉ được bố trí tốt.'
        WHEN 2 THEN 'Thông tin trước chuyến đi rõ ràng. Hướng dẫn viên vui vẻ và hỗ trợ chụp ảnh cho đoàn.'
        WHEN 3 THEN 'Cảnh đẹp, lịch trình đúng mô tả. Thời gian tự do tại điểm chính có thể dài hơn một chút.'
        WHEN 4 THEN 'Dịch vụ ổn định, phương tiện sạch và tài xế chạy cẩn thận. Mức giá phù hợp.'
        WHEN 5 THEN 'Bữa ăn trong chương trình khá ngon, hướng dẫn viên giới thiệu nhiều thông tin hữu ích.'
        WHEN 6 THEN 'Khâu tổ chức chuyên nghiệp, điểm đón thuận tiện và đoàn khởi hành gần đúng giờ.'
        WHEN 7 THEN 'Một chuyến đi đáng nhớ. Lịch trình nhiều điểm nhưng không tạo cảm giác quá vội.'
        WHEN 8 THEN 'Tour đúng nội dung đã tư vấn. Nhân viên chăm sóc phản hồi nhanh trước ngày khởi hành.'
        WHEN 9 THEN 'Trải nghiệm tổng thể tốt, phù hợp với người lần đầu đến miền Trung.'
        WHEN 10 THEN 'Hướng dẫn viên am hiểu địa phương và hỗ trợ các thành viên lớn tuổi rất chu đáo.'
        WHEN 11 THEN 'Chuyến đi ổn nhưng một số điểm khá đông. Nên khởi hành sớm hơn vào cuối tuần.'
        WHEN 12 THEN 'Giá tour hợp lý so với vé tham quan và phương tiện đi kèm. Sẽ giới thiệu cho bạn bè.'
        WHEN 13 THEN 'Lịch trình dễ theo dõi, đoàn có đủ thời gian chụp ảnh và nghỉ ngơi tại các điểm chính.'
        WHEN 14 THEN 'Dịch vụ tốt, xe sạch và nhân viên thân thiện. Phần hướng dẫn chuẩn bị trước tour rất hữu ích.'
        ELSE 'Nội dung tour khá đầy đủ, tuy nhiên cần ghi rõ hơn các chi phí cá nhân không bao gồm.'
    END,
    0,
    'approved',
    NULL,
    1,
    NOW() - ((selected.rn % 120) || ' days')::interval,
    selected.rn % 11,
    NOW() - ((selected.rn % 180) || ' days')::interval,
    NOW()
FROM selected
ON CONFLICT DO NOTHING;

-- Recalculate location rating aggregates from approved reviews.
UPDATE locations l
SET
    avg_rating = aggregates.avg_score,
    review_count = aggregates.rating_count,
    updated_at = NOW()
FROM (
    SELECT
        location_id,
        ROUND(AVG(score)::numeric, 2) AS avg_score,
        COUNT(*)::integer AS rating_count
    FROM ratings
    WHERE location_id IS NOT NULL
      AND status = 'approved'
    GROUP BY location_id
) aggregates
WHERE l.id = aggregates.location_id;

UPDATE locations l
SET
    avg_rating = 0,
    review_count = 0,
    updated_at = NOW()
WHERE NOT EXISTS (
    SELECT 1
    FROM ratings r
    WHERE r.location_id = l.id
      AND r.status = 'approved'
);

-- Recalculate tour rating aggregates from approved reviews.
UPDATE tours t
SET
    rating_avg = aggregates.avg_score,
    rating_count = aggregates.rating_count,
    updated_at = NOW()
FROM (
    SELECT
        tour_id,
        ROUND(AVG(score)::numeric, 2) AS avg_score,
        COUNT(*)::integer AS rating_count
    FROM ratings
    WHERE tour_id IS NOT NULL
      AND status = 'approved'
    GROUP BY tour_id
) aggregates
WHERE t.id = aggregates.tour_id;

UPDATE tours t
SET
    rating_avg = 0,
    rating_count = 0,
    updated_at = NOW()
WHERE NOT EXISTS (
    SELECT 1
    FROM ratings r
    WHERE r.tour_id = t.id
      AND r.status = 'approved'
);

COMMIT;
