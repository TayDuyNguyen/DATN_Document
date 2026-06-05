-- DanangTrip Seed Coverage Check
-- FILE: 28_seed_coverage_check.sql
-- Purpose:
--   Read-only checks after running migrations and seed SQL.
--   This file does not insert, update, or delete data.

WITH table_counts AS (
    SELECT 'taxonomy' AS group_name, 'categories' AS table_name, COUNT(*)::bigint AS row_count FROM categories
    UNION ALL SELECT 'taxonomy', 'subcategories', COUNT(*)::bigint FROM subcategories
    UNION ALL SELECT 'taxonomy', 'tags', COUNT(*)::bigint FROM tags
    UNION ALL SELECT 'taxonomy', 'amenities', COUNT(*)::bigint FROM amenities
    UNION ALL SELECT 'taxonomy', 'tour_categories', COUNT(*)::bigint FROM tour_categories
    UNION ALL SELECT 'taxonomy', 'blog_categories', COUNT(*)::bigint FROM blog_categories

    UNION ALL SELECT 'content', 'locations', COUNT(*)::bigint FROM locations
    UNION ALL SELECT 'content', 'tours', COUNT(*)::bigint FROM tours
    UNION ALL SELECT 'content', 'tour_schedules', COUNT(*)::bigint FROM tour_schedules
    UNION ALL SELECT 'content', 'tour_locations', COUNT(*)::bigint FROM tour_locations
    UNION ALL SELECT 'content', 'blog_posts', COUNT(*)::bigint FROM blog_posts
    UNION ALL SELECT 'content', 'blog_post_categories', COUNT(*)::bigint FROM blog_post_categories
    UNION ALL SELECT 'content', 'promotions', COUNT(*)::bigint FROM promotions
    UNION ALL SELECT 'content', 'landing_pages', COUNT(*)::bigint FROM landing_pages

    UNION ALL SELECT 'relations', 'location_tags', COUNT(*)::bigint FROM location_tags
    UNION ALL SELECT 'relations', 'location_amenities', COUNT(*)::bigint FROM location_amenities

    UNION ALL SELECT 'users', 'users', COUNT(*)::bigint FROM users

    UNION ALL SELECT 'commerce_demo', 'bookings', COUNT(*)::bigint FROM bookings
    UNION ALL SELECT 'commerce_demo', 'booking_items', COUNT(*)::bigint FROM booking_items
    UNION ALL SELECT 'commerce_demo', 'payments', COUNT(*)::bigint FROM payments
    UNION ALL SELECT 'commerce_demo', 'cart_items', COUNT(*)::bigint FROM cart_items

    UNION ALL SELECT 'engagement_demo', 'ratings', COUNT(*)::bigint FROM ratings
    UNION ALL SELECT 'engagement_demo', 'rating_images', COUNT(*)::bigint FROM rating_images
    UNION ALL SELECT 'engagement_demo', 'favorites', COUNT(*)::bigint FROM favorites
    UNION ALL SELECT 'engagement_demo', 'views', COUNT(*)::bigint FROM views
    UNION ALL SELECT 'engagement_demo', 'search_logs', COUNT(*)::bigint FROM search_logs
    UNION ALL SELECT 'engagement_demo', 'contacts', COUNT(*)::bigint FROM contacts
    UNION ALL SELECT 'engagement_demo', 'notifications', COUNT(*)::bigint FROM notifications

    UNION ALL SELECT 'system', 'settings', COUNT(*)::bigint FROM settings
    UNION ALL SELECT 'system', 'sessions', COUNT(*)::bigint FROM sessions
    UNION ALL SELECT 'system', 'cache', COUNT(*)::bigint FROM cache
    UNION ALL SELECT 'system', 'jobs', COUNT(*)::bigint FROM jobs
    UNION ALL SELECT 'system', 'failed_jobs', COUNT(*)::bigint FROM failed_jobs
    UNION ALL SELECT 'system', 'refresh_tokens', COUNT(*)::bigint FROM refresh_tokens

    UNION ALL SELECT 'crawl_staging', 'crawl_sources', COUNT(*)::bigint FROM crawl_sources
    UNION ALL SELECT 'crawl_staging', 'crawl_jobs', COUNT(*)::bigint FROM crawl_jobs
    UNION ALL SELECT 'crawl_staging', 'crawl_items', COUNT(*)::bigint FROM crawl_items
    UNION ALL SELECT 'crawl_staging', 'crawl_logs', COUNT(*)::bigint FROM crawl_logs
)
SELECT
    group_name,
    table_name,
    row_count,
    CASE
        WHEN table_name IN ('cart_items', 'sessions', 'cache', 'jobs', 'failed_jobs', 'refresh_tokens') THEN 'optional_runtime'
        WHEN row_count = 0 THEN 'missing_or_not_seeded'
        ELSE 'ok'
    END AS coverage_status
FROM table_counts
ORDER BY group_name, table_name;

-- Relation quality checks.
SELECT
    'published_crawl_locations_without_tags' AS check_name,
    COUNT(*)::bigint AS issue_count
FROM locations l
JOIN crawl_items ci ON ci.published_entity_type = 'locations'
                  AND ci.published_entity_id = l.id
LEFT JOIN location_tags lt ON lt.location_id = l.id
WHERE lt.location_id IS NULL;

SELECT
    'published_crawl_locations_without_amenities' AS check_name,
    COUNT(*)::bigint AS issue_count
FROM locations l
JOIN crawl_items ci ON ci.published_entity_type = 'locations'
                  AND ci.published_entity_id = l.id
LEFT JOIN location_amenities la ON la.location_id = l.id
WHERE la.location_id IS NULL;

SELECT
    'approved_crawl_items_not_published' AS check_name,
    COUNT(*)::bigint AS issue_count
FROM crawl_items
WHERE status = 'approved'
  AND duplicate_source_id IS NULL
  AND entity_type IN ('location', 'restaurant', 'hotel')
  AND published_entity_id IS NULL;

SELECT
    'inactive_published_locations_waiting_admin_activation' AS check_name,
    COUNT(*)::bigint AS issue_count
FROM locations l
JOIN crawl_items ci ON ci.published_entity_type = 'locations'
                  AND ci.published_entity_id = l.id
WHERE l.status = 'inactive';

SELECT
    'tours_without_schedule' AS check_name,
    COUNT(*)::bigint AS issue_count
FROM tours t
LEFT JOIN tour_schedules ts ON ts.tour_id = t.id
WHERE ts.id IS NULL;

SELECT
    'tours_without_location_mapping' AS check_name,
    COUNT(*)::bigint AS issue_count
FROM tours t
LEFT JOIN tour_locations tl ON tl.tour_id = t.id
WHERE tl.id IS NULL;

