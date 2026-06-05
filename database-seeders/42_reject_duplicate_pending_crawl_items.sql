-- DanangTrip reject duplicate pending crawl items
-- FILE: 42_reject_duplicate_pending_crawl_items.sql
-- Purpose:
--   Clean pending review queue by rejecting crawl items already matched to existing production/staging records.
--   This does not delete data and does not affect published rows.

UPDATE crawl_items
SET status = 'rejected',
    reviewed_at = NOW(),
    duplicate_reason = COALESCE(duplicate_reason, 'Rejected from pending review because duplicate_source_id is already matched.'),
    updated_at = NOW()
WHERE status = 'pending_review'
  AND duplicate_source_id IS NOT NULL;
