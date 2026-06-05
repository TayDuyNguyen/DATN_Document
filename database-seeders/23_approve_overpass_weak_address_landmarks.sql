-- DanangTrip Overpass weak-address landmark approval
-- FILE: 23_approve_overpass_weak_address_landmarks.sql
-- Purpose: approve selected tourism landmarks that only failed weak_address.
-- Required before running:
--   1. 11_crawl_staging_tables.sql
--   2. 12_overpass_danang_pois_seed.sql
--   3. 13_overpass_quality_review_seed.sql
--   4. 14_pexels_image_enrichment_seed.sql
--   5. 15_crawl_duplicate_matching_seed.sql
-- This file only updates crawl_items to approved. Run 16 after approval if publishing is desired.

WITH source_row AS (
    SELECT id FROM crawl_sources WHERE name = 'overpass-danang-pois'
),
approved_external_ids(external_id) AS (
    VALUES
        ('osm-relation-8552348'),
        ('osm-way-694831926'),
        ('osm-relation-19000664'),
        ('osm-way-683416736'),
        ('osm-node-1036552571'),
        ('osm-node-11161070775'),
        ('osm-node-1623183649'),
        ('osm-relation-16028838'),
        ('osm-node-12647208262'),
        ('osm-node-13687068650'),
        ('osm-node-13846529850'),
        ('osm-way-359114064'),
        ('osm-node-5273998823'),
        ('osm-node-10154412164'),
        ('osm-way-630377259'),
        ('osm-way-1204900824'),
        ('osm-node-1538334281'),
        ('osm-way-303341669'),
        ('osm-way-118691767'),
        ('osm-node-5276547123'),
        ('osm-node-7276380289'),
        ('osm-node-5273999121'),
        ('osm-way-675604354'),
        ('osm-way-149699484')
),
updated AS (
    UPDATE crawl_items ci
    SET status = 'approved',
        reviewed_at = NOW(),
        normalized_payload = jsonb_set(
            jsonb_set(
                COALESCE(ci.normalized_payload, '{}'::jsonb),
                '{approvalBatch}',
                to_jsonb('overpass-weak-address-landmarks'::text),
                true
            ),
            '{approvalPolicy}',
            to_jsonb('selected_landmarks_with_weak_address_only'::text),
            true
        ),
        updated_at = NOW()
    FROM source_row s, approved_external_ids a
    WHERE ci.source_id = s.id
      AND a.external_id = ci.external_id
      AND ci.status = 'pending_review'
      AND ci.duplicate_source_id IS NULL
      AND ci.entity_type = 'location'
    RETURNING ci.id, ci.entity_type
)
INSERT INTO crawl_logs (job_id, level, message, context_json, created_at)
SELECT j.id,
       'INFO',
       'Approved Overpass weak-address landmark batch',
       jsonb_build_object(
           'source', 'overpass-danang-pois',
           'approval_batch', 'overpass-weak-address-landmarks',
           'approved_count', (SELECT count(*) FROM updated),
           'note', 'Only selected location landmarks are approved; restaurants/hotels and generic viewpoints remain pending.'
       ),
       NOW()
FROM crawl_jobs j
JOIN source_row s ON s.id = j.source_id
ORDER BY j.id DESC
LIMIT 1;
