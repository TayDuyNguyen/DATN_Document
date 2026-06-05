-- DanangTrip Archive Test Blog Posts Seeder
-- FILE: 31_archive_test_blog_posts_seed.sql
-- Purpose:
--   Hide known test blog content from public data without deleting rows.

UPDATE blog_posts
SET status = 'archived',
    published_at = NULL,
    updated_at = NOW()
WHERE slug IN (
    'test-title-1143398745'
);

