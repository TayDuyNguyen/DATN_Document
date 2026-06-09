-- DanangTrip search log Vietnamese diacritics backfill
-- FILE: 60_search_logs_vietnamese_diacritics_seed.sql
-- Purpose:
--   Normalize public/admin search trend keywords so dashboard UI does not show
--   Vietnamese phrases without diacritics.

UPDATE search_logs
SET query = CASE query
    WHEN 've cap treo ba na' THEN 'vé cáp treo Bà Nà'
    WHEN 'quan an ngon hue' THEN 'quán ăn ngon Huế'
    WHEN 'tour mien trung 4 ngay 3 dem' THEN 'tour miền Trung 4 ngày 3 đêm'
    WHEN 'tour cu lao cham gia re' THEN 'tour Cù Lao Chàm giá rẻ'
    WHEN 'thoi gian rong phun lua' THEN 'thời gian Rồng phun lửa'
    WHEN 'khach san gan bien' THEN 'khách sạn gần biển'
    WHEN 'dac san hoi an' THEN 'đặc sản Hội An'
    WHEN 'tour ba na hills' THEN 'tour Bà Nà Hills'
    WHEN 'le hoi phao hoa da nang' THEN 'lễ hội pháo hoa Đà Nẵng'
    WHEN 'dia diem check in da nang' THEN 'địa điểm check-in Đà Nẵng'
    ELSE query
END
WHERE query IN (
    've cap treo ba na',
    'quan an ngon hue',
    'tour mien trung 4 ngay 3 dem',
    'tour cu lao cham gia re',
    'thoi gian rong phun lua',
    'khach san gan bien',
    'dac san hoi an',
    'tour ba na hills',
    'le hoi phao hoa da nang',
    'dia diem check in da nang'
);
