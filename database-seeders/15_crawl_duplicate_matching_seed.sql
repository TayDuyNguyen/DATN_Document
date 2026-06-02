-- DanangTrip Crawler Duplicate Matching Seed
-- FILE: 15_crawl_duplicate_matching_seed.sql
-- Purpose:
--   Mark crawled staging items that look duplicated with production locations.
--   This file does not publish data into production tables.

ALTER TABLE crawl_items
    ADD COLUMN IF NOT EXISTS duplicate_source_table VARCHAR(100) NULL,
    ADD COLUMN IF NOT EXISTS duplicate_source_id BIGINT NULL,
    ADD COLUMN IF NOT EXISTS duplicate_match_score NUMERIC(5,2) NULL,
    ADD COLUMN IF NOT EXISTS duplicate_reason TEXT NULL;

CREATE INDEX IF NOT EXISTS idx_crawl_items_duplicate_source
    ON crawl_items (duplicate_source_table, duplicate_source_id);

WITH source_row AS (
    SELECT id FROM crawl_sources WHERE name = 'overpass-danang-pois'
),
candidates AS (
    SELECT
        ci.id AS crawl_item_id,
        l.id AS location_id,
        ci.normalized_payload,
        l.slug AS location_slug,
        l.name AS location_name,
        (
            6371000 * 2 * asin(
                sqrt(
                    power(sin(radians(((ci.normalized_payload->>'latitude')::numeric - l.latitude) / 2)), 2)
                    + cos(radians(l.latitude))
                    * cos(radians((ci.normalized_payload->>'latitude')::numeric))
                    * power(sin(radians(((ci.normalized_payload->>'longitude')::numeric - l.longitude) / 2)), 2)
                )
            )
        ) AS distance_m
    FROM crawl_items ci
    JOIN source_row s ON s.id = ci.source_id
    JOIN locations l ON TRUE
    WHERE ci.status = 'pending_review'
      AND ci.normalized_payload ? 'latitude'
      AND ci.normalized_payload ? 'longitude'
      AND (ci.normalized_payload->>'latitude') ~ '^-?[0-9]+(\.[0-9]+)?$'
      AND (ci.normalized_payload->>'longitude') ~ '^-?[0-9]+(\.[0-9]+)?$'
),
ranked_matches AS (
    SELECT
        crawl_item_id,
        location_id,
        location_slug,
        location_name,
        distance_m,
        CASE
            WHEN lower(normalized_payload->>'slugCandidate') = lower(location_slug) THEN 100
            WHEN lower(regexp_replace(normalized_payload->>'name', '[^a-z0-9]+', '-', 'g')) = lower(location_slug) THEN 95
            WHEN distance_m <= 30 THEN 90
            WHEN distance_m <= 80 THEN 80
            WHEN distance_m <= 150 THEN 70
            ELSE 0
        END AS match_score,
        CASE
            WHEN lower(normalized_payload->>'slugCandidate') = lower(location_slug) THEN 'same_slug'
            WHEN lower(regexp_replace(normalized_payload->>'name', '[^a-z0-9]+', '-', 'g')) = lower(location_slug) THEN 'same_name_slug'
            WHEN distance_m <= 30 THEN 'same_coordinates_30m'
            WHEN distance_m <= 80 THEN 'near_coordinates_80m'
            WHEN distance_m <= 150 THEN 'near_coordinates_150m'
            ELSE 'not_duplicate'
        END AS match_reason,
        row_number() OVER (
            PARTITION BY crawl_item_id
            ORDER BY
                CASE
                    WHEN lower(normalized_payload->>'slugCandidate') = lower(location_slug) THEN 100
                    WHEN lower(regexp_replace(normalized_payload->>'name', '[^a-z0-9]+', '-', 'g')) = lower(location_slug) THEN 95
                    WHEN distance_m <= 30 THEN 90
                    WHEN distance_m <= 80 THEN 80
                    WHEN distance_m <= 150 THEN 70
                    ELSE 0
                END DESC,
                distance_m ASC
        ) AS rn
    FROM candidates
    WHERE lower(normalized_payload->>'slugCandidate') = lower(location_slug)
       OR lower(regexp_replace(normalized_payload->>'name', '[^a-z0-9]+', '-', 'g')) = lower(location_slug)
       OR distance_m <= 150
),
best_matches AS (
    SELECT *
    FROM ranked_matches
    WHERE rn = 1
      AND match_score >= 70
)
UPDATE crawl_items ci
SET duplicate_source_table = 'locations',
    duplicate_source_id = best.location_id,
    duplicate_match_score = best.match_score,
    duplicate_reason = best.match_reason || ': ' || best.location_name,
    normalized_payload = jsonb_set(
        jsonb_set(
            jsonb_set(
                COALESCE(ci.normalized_payload, '{}'::jsonb),
                '{duplicateProductionTable}',
                to_jsonb('locations'::text),
                true
            ),
            '{duplicateProductionId}',
            to_jsonb(best.location_id),
            true
        ),
        '{duplicateReason}',
        to_jsonb(best.match_reason || ': ' || best.location_name),
        true
    ),
    updated_at = NOW()
FROM best_matches best
WHERE ci.id = best.crawl_item_id;

INSERT INTO crawl_logs (job_id, level, message, context_json, created_at)
SELECT j.id,
       'INFO',
       'Applied production duplicate matching',
       jsonb_build_object(
           'source', 'overpass-danang-pois',
           'duplicate_table', 'locations',
           'min_match_score', 70,
           'max_distance_m', 150,
           'matched_count', (
               SELECT count(*)
               FROM crawl_items ci
               JOIN crawl_sources s ON s.id = ci.source_id
               WHERE s.name = 'overpass-danang-pois'
                 AND ci.duplicate_source_table = 'locations'
           )
       ),
       NOW()
FROM crawl_jobs j
JOIN crawl_sources s ON s.id = j.source_id
WHERE s.name = 'overpass-danang-pois'
ORDER BY j.id DESC
LIMIT 1;
