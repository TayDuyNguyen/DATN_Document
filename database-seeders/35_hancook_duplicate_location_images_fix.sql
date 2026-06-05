-- DanangTrip HanCook Duplicate Location Image Fix
-- FILE: 35_hancook_duplicate_location_images_fix.sql
-- Purpose:
--   Fill missing Cloudinary images for duplicate inactive HanCook crawl rows.
--   These rows represent the same crawled venue family as location id 236.

WITH image_row(thumbnail, images) AS (
    VALUES (
        'https://res.cloudinary.com/dmukxquza/image/upload/v1780559673/danangtrip/locations/nha-hang-hancook/loc-236__nha-hang-hancook__p01.jpg',
        '["https://res.cloudinary.com/dmukxquza/image/upload/v1780559673/danangtrip/locations/nha-hang-hancook/loc-236__nha-hang-hancook__p01.jpg"]'::json
    )
)
UPDATE locations l
SET thumbnail = image_row.thumbnail,
    images = image_row.images,
    updated_at = NOW()
FROM image_row
WHERE l.id IN (237, 238)
  AND l.status = 'inactive';
