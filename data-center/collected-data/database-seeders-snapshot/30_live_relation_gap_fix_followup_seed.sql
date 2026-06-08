-- DanangTrip Live Relation Gap Fix Follow-up Seeder
-- FILE: 30_live_relation_gap_fix_followup_seed.sql
-- Purpose:
--   Follow-up for seed 29 after newly inserted destination locations exist.
--   It only inserts missing relation rows and does not overwrite data.

WITH tour_location_rules AS (
    SELECT *
    FROM (VALUES
        ('tour-hue-1-ngay', 'hue-imperial-city'),
        ('tour-hue-1-ngay', 'perfume-river'),
        ('tour-hue-1-ngay', 'lang-co-beach'),
        ('tour-hai-van-lang-co', 'hai-van-pass'),
        ('tour-hai-van-lang-co', 'lang-co-beach'),
        ('tour-vinwonders-nam-hoi-an', 'vinwonders-nam-hoi-an'),
        ('tour-bach-ma', 'bach-ma-national-park'),
        ('tour-bach-ma', 'lang-co-beach'),
        ('tour-tam-giang-sunset', 'tam-giang-lagoon'),
        ('tour-ca-hue-song-huong', 'perfume-river'),
        ('tour-ca-hue-song-huong', 'hue-imperial-city'),
        ('tour-snorkeling-son-tra', 'son-tra-peninsula')
    ) AS v(tour_slug, location_slug)
),
inserted_tour_locations AS (
    INSERT INTO tour_locations (tour_id, location_id, created_at)
    SELECT t.id, l.id, NOW()
    FROM tour_location_rules r
    JOIN tours t ON t.slug = r.tour_slug
    JOIN locations l ON l.slug = r.location_slug
    ON CONFLICT (tour_id, location_id) DO NOTHING
    RETURNING id
),
blog_category_rules AS (
    SELECT *
    FROM (VALUES
        ('why-visit-central-vietnam', 'danang-guide'),
        ('first-timers-guide-central-vietnam', 'danang-guide'),
        ('falling-in-love-with-vietnam', 'danang-guide'),
        ('travel-memories-central-vietnam', 'danang-guide'),
        ('authentic-travel-vietnam', 'danang-guide'),
        ('surprising-central-vietnam', 'danang-guide'),
        ('must-visit-central-vietnam-southeast-asia', 'danang-guide')
    ) AS v(post_slug, category_slug)
),
inserted_blog_categories AS (
    INSERT INTO blog_post_categories (post_id, blog_category_id)
    SELECT bp.id, bc.id
    FROM blog_category_rules r
    JOIN blog_posts bp ON bp.slug = r.post_slug
    JOIN blog_categories bc ON bc.slug = r.category_slug
    ON CONFLICT (post_id, blog_category_id) DO NOTHING
    RETURNING id
),
location_tag_rules AS (
    SELECT *
    FROM (VALUES
        ('hue-imperial-city', 'history'),
        ('hue-imperial-city', 'local-culture'),
        ('lang-co-beach', 'gan-bien'),
        ('lang-co-beach', 'view-dep'),
        ('hai-van-pass', 'view-dep'),
        ('hai-van-pass', 'adventure'),
        ('vinwonders-nam-hoi-an', 'kids-friendly'),
        ('vinwonders-nam-hoi-an', 'entertainment'),
        ('son-tra-peninsula', 'adventure'),
        ('son-tra-peninsula', 'view-dep'),
        ('bach-ma-national-park', 'adventure'),
        ('bach-ma-national-park', 'eco-friendly'),
        ('tra-que-vegetable-village', 'local-culture'),
        ('tra-que-vegetable-village', 'learning'),
        ('tam-giang-lagoon', 'view-dep'),
        ('tam-giang-lagoon', 'local-culture'),
        ('perfume-river', 'local-culture'),
        ('perfume-river', 'view-song'),
        ('han-river', 'view-song'),
        ('han-river', 'trung-tam-thanh-pho')
    ) AS v(location_slug, tag_slug)
),
inserted_location_tags AS (
    INSERT INTO location_tags (location_id, tag_id, created_at)
    SELECT l.id, t.id, NOW()
    FROM location_tag_rules r
    JOIN locations l ON l.slug = r.location_slug
    JOIN tags t ON t.slug = r.tag_slug
    ON CONFLICT (location_id, tag_id) DO NOTHING
    RETURNING id
),
location_amenity_rules AS (
    SELECT *
    FROM (VALUES
        ('quan-bun-co-ha-', 'on-site-restaurant'),
        ('hue-imperial-city', 'tourist-map'),
        ('hue-imperial-city', 'tour-desk'),
        ('lang-co-beach', 'tourist-map'),
        ('hai-van-pass', 'tourist-map'),
        ('vinwonders-nam-hoi-an', 'tour-desk'),
        ('son-tra-peninsula', 'tourist-map'),
        ('son-tra-peninsula', 'tour-desk'),
        ('bach-ma-national-park', 'tourist-map'),
        ('bach-ma-national-park', 'tour-desk'),
        ('tra-que-vegetable-village', 'tourist-map'),
        ('tam-giang-lagoon', 'tourist-map'),
        ('perfume-river', 'tourist-map'),
        ('han-river', 'tourist-map')
    ) AS v(location_slug, amenity_icon)
),
inserted_location_amenities AS (
    INSERT INTO location_amenities (location_id, amenity_id, created_at)
    SELECT l.id, a.id, NOW()
    FROM location_amenity_rules r
    JOIN locations l ON l.slug = r.location_slug
    JOIN amenities a ON a.icon = r.amenity_icon
    ON CONFLICT (location_id, amenity_id) DO NOTHING
    RETURNING id
)
SELECT
    (SELECT COUNT(*) FROM inserted_tour_locations) AS inserted_tour_locations,
    (SELECT COUNT(*) FROM inserted_blog_categories) AS inserted_blog_categories,
    (SELECT COUNT(*) FROM inserted_location_tags) AS inserted_location_tags,
    (SELECT COUNT(*) FROM inserted_location_amenities) AS inserted_location_amenities;

