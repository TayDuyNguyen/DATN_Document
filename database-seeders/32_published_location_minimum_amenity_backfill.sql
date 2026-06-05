-- DanangTrip Published Location Minimum Amenity Backfill
-- FILE: 32_published_location_minimum_amenity_backfill.sql
-- Purpose:
--   Ensure published crawl locations have at least one amenity for UI filters.
--   This seed uses conservative generic amenities by entity type.

WITH published AS (
    SELECT
        ci.entity_type,
        l.id AS location_id
    FROM crawl_items ci
    JOIN locations l ON l.id = ci.published_entity_id
    WHERE ci.published_entity_type = 'locations'
      AND ci.published_entity_id IS NOT NULL
),
missing AS (
    SELECT p.*
    FROM published p
    LEFT JOIN location_amenities la ON la.location_id = p.location_id
    WHERE la.location_id IS NULL
),
rules AS (
    SELECT location_id, 'tourist-map' AS amenity_icon
    FROM missing
    WHERE entity_type = 'location'
    UNION ALL
    SELECT location_id, 'tour-desk'
    FROM missing
    WHERE entity_type = 'location'
    UNION ALL
    SELECT location_id, 'on-site-restaurant'
    FROM missing
    WHERE entity_type = 'restaurant'
    UNION ALL
    SELECT location_id, 'tourist-map'
    FROM missing
    WHERE entity_type = 'restaurant'
    UNION ALL
    SELECT location_id, 'reception-24h'
    FROM missing
    WHERE entity_type = 'hotel'
    UNION ALL
    SELECT location_id, 'luggage-storage'
    FROM missing
    WHERE entity_type = 'hotel'
)
INSERT INTO location_amenities (location_id, amenity_id, created_at)
SELECT DISTINCT r.location_id, a.id, NOW()
FROM rules r
JOIN amenities a ON a.icon = r.amenity_icon
ON CONFLICT (location_id, amenity_id) DO NOTHING;

