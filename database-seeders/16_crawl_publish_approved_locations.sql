-- DanangTrip Crawler Publish Approved Locations
-- FILE: 16_crawl_publish_approved_locations.sql
-- Purpose:
--   Publish only admin-approved, non-duplicate crawl items into production locations.
--   This file is intentionally not imported by CrawlerSeeder automatically.
--
-- Required before running:
--   1. 11_crawl_staging_tables.sql
--   2. 12_overpass_danang_pois_seed.sql
--   3. 13_overpass_quality_review_seed.sql
--   4. 15_crawl_duplicate_matching_seed.sql
--   5. Admin/user has manually changed selected crawl_items.status to 'approved'.
-- Optional:
--   - 14_pexels_image_enrichment_seed.sql can add external image candidates, but
--     it is not required and should not be trusted without manual review.

WITH source_row AS (
    SELECT id FROM crawl_sources WHERE name = 'overpass-danang-pois'
),
approved_items AS (
    SELECT ci.*
    FROM crawl_items ci
    JOIN source_row s ON s.id = ci.source_id
    WHERE ci.status = 'approved'
      AND ci.duplicate_source_id IS NULL
      AND ci.entity_type IN ('location', 'restaurant', 'hotel')
),
prepared AS (
    SELECT
        ai.id AS crawl_item_id,
        ai.entity_type,
        COALESCE(NULLIF(ai.normalized_payload->>'name', ''), 'Da Nang Place') AS name,
        COALESCE(NULLIF(ai.normalized_payload->>'slugCandidate', ''), 'crawl-item-' || ai.id) AS slug_base,
        COALESCE(NULLIF(ai.normalized_payload->>'description', ''), 'Du lieu duoc thu thap tu nguon cong khai va da duoc duyet truoc khi publish.') AS description,
        COALESCE(NULLIF(ai.normalized_payload->>'shortDescription', ''), 'Du lieu du lich Da Nang da duoc duyet.') AS short_description,
        COALESCE(NULLIF(ai.normalized_payload->>'address', ''), 'Da Nang') AS address,
        COALESCE(NULLIF(ai.normalized_payload->>'district', ''), 'Da Nang') AS district,
        (ai.normalized_payload->>'latitude')::numeric AS latitude,
        (ai.normalized_payload->>'longitude')::numeric AS longitude,
        NULLIF(ai.raw_payload #>> '{osmTags,contact:phone}', '') AS phone,
        COALESCE(NULLIF(ai.raw_payload #>> '{osmTags,website}', ''), NULLIF(ai.raw_payload #>> '{osmTags,contact:website}', '')) AS website,
        NULLIF(ai.raw_payload #>> '{osmTags,opening_hours}', '') AS opening_hours_text,
        COALESCE(ai.normalized_payload->'imageUrls', '[]'::jsonb) AS image_urls,
        COALESCE(NULLIF(ai.normalized_payload->>'categorySlug', ''), 'check-in-noi-tieng') AS category_slug
    FROM approved_items ai
    WHERE ai.normalized_payload ? 'latitude'
      AND ai.normalized_payload ? 'longitude'
      AND (ai.normalized_payload->>'latitude') ~ '^-?[0-9]+(\.[0-9]+)?$'
      AND (ai.normalized_payload->>'longitude') ~ '^-?[0-9]+(\.[0-9]+)?$'
),
mapped AS (
    SELECT
        p.*,
        c.id AS category_id,
        CASE
            WHEN p.entity_type = 'hotel' THEN 4
            WHEN p.entity_type = 'restaurant' THEN 3
            ELSE 1
        END AS price_level,
        COALESCE(p.image_urls->>0, NULL) AS thumbnail,
        CASE
            WHEN p.opening_hours_text IS NULL THEN NULL::jsonb
            ELSE jsonb_build_object('raw', p.opening_hours_text)
        END AS opening_hours_json
    FROM prepared p
    JOIN categories c ON c.slug = p.category_slug
),
slugged AS (
    SELECT
        m.*,
        row_number() OVER (PARTITION BY m.slug_base ORDER BY m.crawl_item_id) AS slug_rn
    FROM mapped m
),
inserted AS (
    INSERT INTO locations (
        name,
        slug,
        category_id,
        description,
        short_description,
        address,
        district,
        latitude,
        longitude,
        phone,
        website,
        opening_hours,
        price_level,
        thumbnail,
        images,
        status,
        is_featured,
        created_at,
        updated_at
    )
    SELECT
        m.name,
        CASE
            WHEN m.slug_rn > 1 OR EXISTS (SELECT 1 FROM locations l WHERE l.slug = m.slug_base)
                THEN m.slug_base || '-crawl-' || m.crawl_item_id
            ELSE m.slug_base
        END,
        m.category_id,
        m.description,
        left(m.short_description, 500),
        left(m.address, 255),
        left(m.district, 50),
        m.latitude,
        m.longitude,
        left(m.phone, 20),
        left(m.website, 255),
        m.opening_hours_json,
        m.price_level,
        left(m.thumbnail, 255),
        m.image_urls,
        'inactive',
        false,
        NOW(),
        NOW()
    FROM slugged m
    RETURNING id, slug
)
UPDATE crawl_items ci
SET status = 'published',
    published_entity_type = 'locations',
    published_entity_id = inserted.id,
    updated_at = NOW()
FROM inserted
WHERE ci.status = 'approved'
  AND (
      ci.normalized_payload->>'slugCandidate' = inserted.slug
      OR inserted.slug = (ci.normalized_payload->>'slugCandidate') || '-crawl-' || ci.id
  );

INSERT INTO crawl_logs (job_id, level, message, context_json, created_at)
SELECT j.id,
       'INFO',
       'Published approved crawl items to locations',
       jsonb_build_object(
           'source', 'overpass-danang-pois',
           'target_table', 'locations',
           'published_status', 'inactive',
           'note', 'Published rows require final admin activation.'
       ),
       NOW()
FROM crawl_jobs j
JOIN crawl_sources s ON s.id = j.source_id
WHERE s.name = 'overpass-danang-pois'
ORDER BY j.id DESC
LIMIT 1;
