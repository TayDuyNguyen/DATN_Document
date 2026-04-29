-- DanangTrip Real Data Seeder: Ratings & Interactions (100 rows each for 7 tables)
-- FILE: 09_ratings_interactions.sql

-- 1. RATINGS (Target 100)
INSERT INTO ratings (id, user_id, tour_id, score, comment, status, created_at, updated_at) VALUES
(1, 3, 1, 5, 'Chuyến đi tuyệt vời!', 'approved', NOW(), NOW()),
(2, 6, 1, 4, 'Hơi đông khách.', 'approved', NOW(), NOW());

INSERT INTO ratings (id, user_id, location_id, score, comment, status, created_at, updated_at) VALUES
(3, 3, 1, 5, 'Bà Nà rất đẹp!', 'approved', NOW(), NOW());

-- Generate more ratings 4-100
INSERT INTO ratings (id, user_id, tour_id, score, comment, status, created_at, updated_at)
SELECT 
    i, 
    (i % 50) + 1, 
    (i % 50) + 1, 
    (random() * 2 + 3)::int, 
    'Review comment ' || i, 
    'approved', 
    NOW(), 
    NOW()
FROM generate_series(4, 100) AS i;

-- 2. RATING_IMAGES (Target 100)
INSERT INTO rating_images (id, rating_id, image_url, sort_order, created_at)
SELECT 
    i, 
    (i % 100) + 1, 
    'https://picsum.photos/seed/' || i || '/800/600', 
    0, 
    NOW()
FROM generate_series(1, 100) AS i;

-- 3. FAVORITES (Target 100)
INSERT INTO favorites (id, user_id, tour_id, created_at)
SELECT 
    i, 
    (i % 50) + 1, 
    (i % 50) + 1, 
    NOW()
FROM generate_series(1, 100) AS i;

-- 4. VIEWS (Target 100)
INSERT INTO views (id, user_id, tour_id, session_id, time_spent, created_at)
SELECT 
    i, 
    (i % 50) + 1, 
    (i % 50) + 1, 
    'sess_' || i, 
    (random() * 300)::int, 
    NOW()
FROM generate_series(1, 100) AS i;

-- 5. SEARCH_LOGS (Target 100)
INSERT INTO search_logs (id, user_id, session_id, query, results_count, created_at)
SELECT 
    i, 
    (i % 50) + 1, 
    'sess_' || i, 
    'query ' || i, 
    (random() * 20)::int, 
    NOW()
FROM generate_series(1, 100) AS i;

-- 6. CONTACTS (Target 100)
INSERT INTO contacts (id, name, email, phone, subject, message, status, created_at, updated_at)
SELECT 
    i, 
    'Contact ' || i, 
    'contact' || i || '@example.com', 
    '0905' || LPAD(i::text, 6, '0'), 
    'Subject ' || i, 
    'Message content ' || i, 
    'new', 
    NOW(), 
    NOW()
FROM generate_series(1, 100) AS i;

-- 7. NOTIFICATIONS (Target 100)
INSERT INTO notifications (id, user_id, type, title, content, is_read, created_at)
SELECT 
    i, 
    (i % 50) + 1, 
    'system', 
    'Notification ' || i, 
    'Content for notification ' || i, 
    false, 
    NOW()
FROM generate_series(1, 100) AS i;
