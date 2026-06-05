-- DanangTrip HanCook Location Taxonomy Fix
-- FILE: 33_hancook_location_taxonomy_fix.sql
-- Purpose:
--   Add minimal taxonomy for inactive HanCook crawl locations left without
--   tag/amenity after publish backfill. Does not activate or delete rows.

WITH target_locations AS (
    SELECT id
    FROM locations
    WHERE slug IN (
        'nha-hang-hancook-crawl-215',
        'nha-hang-hancook-crawl-216'
    )
),
tag_rules AS (
    SELECT tl.id AS location_id, t.id AS tag_id
    FROM target_locations tl
    JOIN tags t ON t.slug IN ('mon-an-dac-san', 'binh-dan')
),
amenity_rules AS (
    SELECT tl.id AS location_id, a.id AS amenity_id
    FROM target_locations tl
    JOIN amenities a ON a.icon IN ('on-site-restaurant', 'tourist-map')
)
INSERT INTO location_tags (location_id, tag_id, created_at)
SELECT location_id, tag_id, NOW()
FROM tag_rules
ON CONFLICT (location_id, tag_id) DO NOTHING;

WITH target_locations AS (
    SELECT id
    FROM locations
    WHERE slug IN (
        'nha-hang-hancook-crawl-215',
        'nha-hang-hancook-crawl-216'
    )
),
amenity_rules AS (
    SELECT tl.id AS location_id, a.id AS amenity_id
    FROM target_locations tl
    JOIN amenities a ON a.icon IN ('on-site-restaurant', 'tourist-map')
)
INSERT INTO location_amenities (location_id, amenity_id, created_at)
SELECT location_id, amenity_id, NOW()
FROM amenity_rules
ON CONFLICT (location_id, amenity_id) DO NOTHING;

