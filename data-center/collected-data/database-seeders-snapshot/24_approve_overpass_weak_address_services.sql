-- DanangTrip Overpass weak-address service approval
-- FILE: 24_approve_overpass_weak_address_services.sql
-- Purpose: approve selected restaurants/hotels that only failed weak_address but have strong operational signals.
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
        ('osm-node-5485445021'),
        ('osm-node-6109158033'),
        ('osm-node-4805182821'),
        ('osm-node-4352266089'),
        ('osm-node-4430018990'),
        ('osm-way-1109970012'),
        ('osm-node-5484764821'),
        ('osm-node-4352266389'),
        ('osm-node-5864570785'),
        ('osm-node-5271605921'),
        ('osm-node-4401223296')
),
updated AS (
    UPDATE crawl_items ci
    SET status = 'approved',
        reviewed_at = NOW(),
        normalized_payload = jsonb_set(
            jsonb_set(
                COALESCE(ci.normalized_payload, '{}'::jsonb),
                '{approvalBatch}',
                to_jsonb('overpass-weak-address-services'::text),
                true
            ),
            '{approvalPolicy}',
            to_jsonb('services_with_two_or_more_operational_signals'::text),
            true
        ),
        updated_at = NOW()
    FROM source_row s, approved_external_ids a
    WHERE ci.source_id = s.id
      AND a.external_id = ci.external_id
      AND ci.status = 'pending_review'
      AND ci.duplicate_source_id IS NULL
      AND ci.entity_type IN ('restaurant', 'hotel')
    RETURNING ci.id, ci.entity_type
)
INSERT INTO crawl_logs (job_id, level, message, context_json, created_at)
SELECT j.id,
       'INFO',
       'Approved Overpass weak-address service batch',
       jsonb_build_object(
           'source', 'overpass-danang-pois',
           'approval_batch', 'overpass-weak-address-services',
           'approved_count', (SELECT count(*) FROM updated),
           'restaurant_count', (SELECT count(*) FROM updated WHERE entity_type = 'restaurant'),
           'hotel_count', (SELECT count(*) FROM updated WHERE entity_type = 'hotel'),
           'note', 'Only service records with at least two operational/source signals are approved.'
       ),
       NOW()
FROM crawl_jobs j
JOIN source_row s ON s.id = j.source_id
ORDER BY j.id DESC
LIMIT 1;
