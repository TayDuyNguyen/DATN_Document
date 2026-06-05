-- DanangTrip deactivate Memory Lounge crawl duplicate
-- FILE: 38_deactivate_memory_lounge_crawl_duplicate.sql
-- Purpose:
--   Keep curated Memory Lounge id 96 active and move crawl duplicate id 221 back to inactive.

UPDATE locations
SET status = 'inactive',
    updated_at = NOW()
WHERE id = 221
  AND slug = 'memory-lounge'
  AND status = 'active';
