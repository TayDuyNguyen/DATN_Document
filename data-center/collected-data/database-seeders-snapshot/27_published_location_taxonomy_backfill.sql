-- DanangTrip Published Location Taxonomy Backfill
-- FILE: 27_published_location_taxonomy_backfill.sql
-- Purpose:
--   Add tags and amenities to locations published from approved crawl_items.
--   This improves filtering/search UI without changing source crawl payloads.
--
-- Required before running:
--   1. 02_tags_amenities.sql
--   2. 11_crawl_staging_tables.sql
--   3. 16_crawl_publish_approved_locations.sql

WITH published AS (
    SELECT
        ci.id AS crawl_item_id,
        ci.entity_type,
        ci.raw_payload,
        ci.normalized_payload,
        l.id AS location_id,
        l.price_level
    FROM crawl_items ci
    JOIN locations l ON l.id = ci.published_entity_id
    WHERE ci.published_entity_type = 'locations'
      AND ci.published_entity_id IS NOT NULL
),
tag_rules AS (
    SELECT location_id, 'check-in-dep' AS slug FROM published WHERE entity_type = 'location'
    UNION ALL
    SELECT location_id, 'view-dep' FROM published WHERE entity_type = 'location'
    UNION ALL
    SELECT location_id, 'local-culture' FROM published
    WHERE normalized_payload->>'categorySlug' IN ('bao-tang-di-tich', 'check-in-noi-tieng')
    UNION ALL
    SELECT location_id, 'history' FROM published
    WHERE normalized_payload->>'categorySlug' = 'bao-tang-di-tich'
    UNION ALL
    SELECT location_id, 'am-thuc-bien' FROM published
    WHERE entity_type = 'restaurant'
      AND lower(COALESCE(raw_payload #>> '{osmTags,cuisine}', '')) LIKE '%seafood%'
    UNION ALL
    SELECT location_id, 'mon-an-dac-san' FROM published
    WHERE entity_type = 'restaurant'
    UNION ALL
    SELECT location_id, 'binh-dan' FROM published
    WHERE entity_type = 'restaurant' AND COALESCE(price_level, 3) <= 2
    UNION ALL
    SELECT location_id, 'cao-cap' FROM published
    WHERE entity_type IN ('hotel', 'restaurant') AND COALESCE(price_level, 0) >= 4
    UNION ALL
    SELECT location_id, 'gan-bien' FROM published
    WHERE lower(COALESCE(normalized_payload->>'district', '')) IN ('son tra', 'ngu hanh son')
    UNION ALL
    SELECT location_id, 'trung-tam-thanh-pho' FROM published
    WHERE lower(COALESCE(normalized_payload->>'district', '')) IN ('hai chau', 'thanh khe')
    UNION ALL
    SELECT location_id, 'gia-dinh' FROM published
    WHERE entity_type IN ('location', 'hotel')
),
tag_candidates AS (
    SELECT DISTINCT tr.location_id, t.id AS tag_id
    FROM tag_rules tr
    JOIN tags t ON t.slug = tr.slug
),
inserted_tags AS (
    INSERT INTO location_tags (location_id, tag_id, created_at)
    SELECT tc.location_id, tc.tag_id, NOW()
    FROM tag_candidates tc
    WHERE NOT EXISTS (
        SELECT 1
        FROM location_tags lt
        WHERE lt.location_id = tc.location_id
          AND lt.tag_id = tc.tag_id
    )
    RETURNING location_id
),
amenity_rules AS (
    SELECT location_id, 'free-wifi' AS amenity_name FROM published
    WHERE raw_payload #>> '{osmTags,internet_access}' IN ('wlan', 'wifi', 'yes')
       OR raw_payload #>> '{osmTags,wifi}' IN ('yes', 'free')
    UNION ALL
    SELECT location_id, 'Cho dau xe mien phi' FROM published
    WHERE raw_payload #>> '{osmTags,parking}' IN ('yes', 'street_side', 'surface')
       OR raw_payload #>> '{osmTags,amenity}' = 'parking'
    UNION ALL
    SELECT location_id, 'Le tan 24h' FROM published
    WHERE entity_type = 'hotel'
    UNION ALL
    SELECT location_id, 'Nha hang' FROM published
    WHERE entity_type IN ('restaurant', 'hotel')
    UNION ALL
    SELECT location_id, 'Ho tro dat tour' FROM published
    WHERE entity_type IN ('location', 'hotel')
    UNION ALL
    SELECT location_id, 'Ban do du lich' FROM published
    WHERE entity_type = 'location'
    UNION ALL
    SELECT location_id, 'Dich vu gui do' FROM published
    WHERE entity_type = 'hotel'
    UNION ALL
    SELECT location_id, 'Dich vu don phong hang ngay' FROM published
    WHERE entity_type = 'hotel'
),
amenity_candidates AS (
    SELECT DISTINCT ar.location_id, a.id AS amenity_id
    FROM amenity_rules ar
    JOIN amenities a ON a.name = ar.amenity_name OR a.icon = ar.amenity_name
),
inserted_amenities AS (
    INSERT INTO location_amenities (location_id, amenity_id, created_at)
    SELECT ac.location_id, ac.amenity_id, NOW()
    FROM amenity_candidates ac
    WHERE NOT EXISTS (
        SELECT 1
        FROM location_amenities la
        WHERE la.location_id = ac.location_id
          AND la.amenity_id = ac.amenity_id
    )
    RETURNING location_id
)
INSERT INTO crawl_logs (job_id, level, message, context_json, created_at)
SELECT j.id,
       'INFO',
       'Backfilled taxonomy for published crawl locations',
       jsonb_build_object(
           'target_tables', jsonb_build_array('location_tags', 'location_amenities'),
           'tag_rows_inserted', (SELECT COUNT(*) FROM inserted_tags),
           'amenity_rows_inserted', (SELECT COUNT(*) FROM inserted_amenities)
       ),
       NOW()
FROM crawl_jobs j
ORDER BY j.id DESC
LIMIT 1;

