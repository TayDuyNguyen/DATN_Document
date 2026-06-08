BEGIN;

-- Public location categories should only expose categories containing active content.
UPDATE categories c
SET status = CASE
        WHEN EXISTS (
            SELECT 1
            FROM locations l
            WHERE l.category_id = c.id
              AND l.status = 'active'
        ) THEN 'active'
        ELSE 'inactive'
    END,
    updated_at = CURRENT_TIMESTAMP;

-- Subcategories without active locations create empty public filters.
UPDATE subcategories s
SET status = CASE
        WHEN EXISTS (
            SELECT 1
            FROM locations l
            WHERE l.subcategory_id = s.id
              AND l.status = 'active'
        ) THEN 'active'
        ELSE 'inactive'
    END,
    updated_at = CURRENT_TIMESTAMP;

-- Public tour categories should only expose categories containing active tours.
UPDATE tour_categories tc
SET status = CASE
        WHEN EXISTS (
            SELECT 1
            FROM tours t
            WHERE t.tour_category_id = tc.id
              AND t.status = 'active'
        ) THEN 'active'
        ELSE 'inactive'
    END,
    updated_at = CURRENT_TIMESTAMP;

-- Blog categories have no status column. Remove only true orphans with no post relation.
DELETE FROM blog_categories bc
WHERE NOT EXISTS (
    SELECT 1
    FROM blog_post_categories bpc
    WHERE bpc.blog_category_id = bc.id
);

SELECT setval(
    pg_get_serial_sequence('blog_categories', 'id'),
    GREATEST((SELECT COALESCE(MAX(id), 1) FROM blog_categories), 1),
    true
);

COMMIT;
