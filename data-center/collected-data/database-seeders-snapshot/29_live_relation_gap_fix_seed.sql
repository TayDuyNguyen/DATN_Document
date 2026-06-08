-- DanangTrip Live Relation Gap Fix Seeder
-- FILE: 29_live_relation_gap_fix_seed.sql
-- Purpose:
--   Fill relation gaps found in the 2026-06-04 live DB coverage check.
--   This seed is conservative: it uses slugs, inserts only missing rows,
--   and does not delete or overwrite existing data.
--
-- Source basis:
--   - Existing base seeds: 01, 02, 03, 05, 06, 07.
--   - Existing crawler/review outputs under danangtrip-crawler/data.
--   - Nominatim/OpenStreetMap reviewed location records already stored locally.

WITH category_ref AS (
    SELECT id FROM categories WHERE slug = 'check-in-noi-tieng'
),
new_locations AS (
    SELECT *
    FROM (VALUES
        ('hue-imperial-city', 'Hue Imperial City', 'Imperial Citadel, Hue, Vietnam', 'Hue', 16.46897260, 107.57812660, 'Hue Imperial City is a core heritage stop for Hue day tours from Da Nang.', 'Former royal citadel of Hue, collected from local crawler review data.'),
        ('lang-co-beach', 'Lang Co Beach', 'Lang Co, Hue, Vietnam', 'Hue', 16.22690000, 108.07450000, 'Lang Co Beach is a scenic stop between Da Nang and Hue.', 'Coastal stop commonly used on Hai Van Pass and Hue tour itineraries.'),
        ('hai-van-pass', 'Hai Van Pass', 'Hai Van Pass, Da Nang - Hue, Vietnam', 'Da Nang / Hue', 16.20000000, 108.13330000, 'Hai Van Pass is a scenic mountain road between Da Nang and Hue.', 'Mountain pass used by sightseeing and transfer tours.'),
        ('vinwonders-nam-hoi-an', 'VinWonders Nam Hoi An', 'Binh Minh, Thang Binh, Quang Nam, Vietnam', 'Quang Nam', 15.83400000, 108.33800000, 'VinWonders Nam Hoi An is a theme park and family entertainment destination.', 'Family theme park destination near Hoi An.'),
        ('son-tra-peninsula', 'Son Tra Peninsula', 'Son Tra Peninsula, Da Nang, Vietnam', 'Da Nang', 16.11670000, 108.28330000, 'Son Tra Peninsula is a nature and coastal sightseeing area in Da Nang.', 'Nature, viewpoints, snorkeling and trekking destination in Da Nang.'),
        ('bach-ma-national-park', 'Bach Ma National Park', 'Bach Ma National Park, Hue, Vietnam', 'Hue', 16.21572650, 107.85339260, 'Bach Ma National Park is a trekking and nature destination between Da Nang and Hue.', 'National park destination collected from Nominatim/OpenStreetMap review data.'),
        ('tra-que-vegetable-village', 'Tra Que Vegetable Village', 'Tra Que, Hoi An, Quang Nam, Vietnam', 'Hoi An', 15.89930000, 108.33730000, 'Tra Que Vegetable Village is an agricultural experience destination near Hoi An.', 'Farming and local food experience village.'),
        ('tam-giang-lagoon', 'Tam Giang Lagoon', 'Tam Giang Lagoon, Hue, Vietnam', 'Hue', 16.60000000, 107.63330000, 'Tam Giang Lagoon is a sunset, boat and seafood experience destination in Hue.', 'Large brackish lagoon used by sunset and eco tours.'),
        ('perfume-river', 'Perfume River', 'Perfume River, Hue, Vietnam', 'Hue', 16.46900000, 107.58000000, 'Perfume River is the main cultural river of Hue.', 'River destination for Hue music and evening boat experiences.'),
        ('han-river', 'Han River', 'Han River, Da Nang, Vietnam', 'Da Nang', 16.07000000, 108.22500000, 'Han River is the central river corridor of Da Nang.', 'River cruise and evening sightseeing route in Da Nang.')
    ) AS v(slug, name, address, district, latitude, longitude, short_description, description)
),
inserted_locations AS (
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
        price_level,
        avg_rating,
        review_count,
        view_count,
        favorite_count,
        status,
        is_featured,
        created_at,
        updated_at
    )
    SELECT
        nl.name,
        nl.slug,
        cr.id,
        nl.description,
        nl.short_description,
        nl.address,
        nl.district,
        nl.latitude,
        nl.longitude,
        1,
        0,
        0,
        0,
        0,
        'active',
        false,
        NOW(),
        NOW()
    FROM new_locations nl
    CROSS JOIN category_ref cr
    ON CONFLICT (slug) DO NOTHING
    RETURNING id
),
tour_location_rules AS (
    SELECT *
    FROM (VALUES
        ('tour-hue-1-ngay', 'hue-imperial-city'),
        ('tour-hue-1-ngay', 'perfume-river'),
        ('tour-hue-1-ngay', 'lang-co-beach'),
        ('tour-my-son', 'my-son-sanctuary'),
        ('tour-hai-van-lang-co', 'hai-van-pass'),
        ('tour-hai-van-lang-co', 'lang-co-beach'),
        ('tour-dem-hoi-an', 'hoi-an-ancient-town'),
        ('tour-dem-hoi-an', 'thu-bon-river'),
        ('tour-ba-na-night', 'ba-na-hills'),
        ('tour-vinwonders-nam-hoi-an', 'vinwonders-nam-hoi-an'),
        ('tour-trekking-son-tra', 'son-tra-peninsula'),
        ('tour-trekking-son-tra', 'linh-ung-pagoda'),
        ('tour-bach-ma', 'bach-ma-national-park'),
        ('tour-bach-ma', 'lang-co-beach'),
        ('tour-street-food-danang', 'han-market'),
        ('tour-street-food-danang', 'con-market'),
        ('tour-street-food-danang', 'son-tra-night-market'),
        ('tour-tra-que-farmer', 'tra-que-vegetable-village'),
        ('tour-tra-que-farmer', 'hoi-an-ancient-town'),
        ('tour-du-thuyen-song-han', 'han-river'),
        ('tour-du-thuyen-song-han', 'dragon-bridge'),
        ('tour-du-thuyen-song-han', 'han-river-bridge'),
        ('tour-tam-giang-sunset', 'tam-giang-lagoon'),
        ('tour-ca-hue-song-huong', 'perfume-river'),
        ('tour-ca-hue-song-huong', 'hue-imperial-city'),
        ('tour-snorkeling-son-tra', 'son-tra-peninsula'),
        ('tour-snorkeling-son-tra', 'tien-sa-port')
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
        ('central-vietnam-7-day-itinerary', 'lich-trinh-goi-y'),
        ('why-visit-central-vietnam', 'cam-nang-du-lich'),
        ('where-to-stay-central-vietnam', 'review-khach-san'),
        ('5-day-central-vietnam-itinerary', 'lich-trinh-goi-y'),
        ('first-timers-guide-central-vietnam', 'cam-nang-du-lich'),
        ('best-things-to-do-hoi-an', 'hoi-an-guide'),
        ('48-hours-in-hoi-an', 'hoi-an-guide'),
        ('where-to-stay-hoi-an', 'review-khach-san'),
        ('ba-na-hills-golden-bridge-guide', 'ba-na-hills-tips'),
        ('da-nang-travel-base', 'danang-guide'),
        ('da-nang-weekend-itinerary', 'lich-trinh-goi-y'),
        ('luxury-hotels-da-nang', 'review-khach-san'),
        ('da-nang-family-travel-guide', 'family-travel-tips'),
        ('2-days-in-hue-itinerary', 'hue-guide'),
        ('hue-history-tour-itinerary', 'hue-guide'),
        ('where-to-stay-hue-guide', 'review-khach-san'),
        ('central-vietnam-markets-guide', 'market-shopping'),
        ('central-vietnam-souvenir-guide', 'souvenir-guide'),
        ('3-days-in-da-nang-itinerary', 'lich-trinh-goi-y'),
        ('2-days-in-hoi-an-itinerary', 'hoi-an-guide'),
        ('2-days-in-hue-itinerary-guide', 'hue-guide'),
        ('1-week-central-vietnam-planner', 'lich-trinh-goi-y'),
        ('luxury-travel-central-vietnam', 'review-khach-san'),
        ('family-travel-guide-vietnam', 'family-travel-tips'),
        ('my-son-sanctuary-tour-guide', 'my-son-tips'),
        ('falling-in-love-with-vietnam', 'cam-nang-du-lich'),
        ('romantic-travel-guide-vietnam', 'romantic-date'),
        ('travel-memories-central-vietnam', 'cam-nang-du-lich'),
        ('vietnam-homestay-experience', 'homestay-review'),
        ('authentic-travel-vietnam', 'cam-nang-du-lich'),
        ('surprising-central-vietnam', 'cam-nang-du-lich'),
        ('must-visit-central-vietnam-southeast-asia', 'cam-nang-du-lich')
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
        ('quan-bun-co-ha-', 'mon-an-dac-san'),
        ('quan-bun-co-ha-', 'binh-dan')
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
        ('quan-bun-co-ha-', 'Nha hang')
    ) AS v(location_slug, amenity_name)
),
inserted_location_amenities AS (
    INSERT INTO location_amenities (location_id, amenity_id, created_at)
    SELECT l.id, a.id, NOW()
    FROM location_amenity_rules r
    JOIN locations l ON l.slug = r.location_slug
    JOIN amenities a ON a.name = r.amenity_name
    ON CONFLICT (location_id, amenity_id) DO NOTHING
    RETURNING id
)
SELECT
    (SELECT COUNT(*) FROM inserted_locations) AS inserted_locations,
    (SELECT COUNT(*) FROM inserted_tour_locations) AS inserted_tour_locations,
    (SELECT COUNT(*) FROM inserted_blog_categories) AS inserted_blog_categories,
    (SELECT COUNT(*) FROM inserted_location_tags) AS inserted_location_tags,
    (SELECT COUNT(*) FROM inserted_location_amenities) AS inserted_location_amenities;

