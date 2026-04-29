-- DanangTrip Real Data Seeder: Blog Posts & Pivots (100 real posts)
-- FILE: 07_blog_posts.sql

-- 1. BLOG_POSTS (Target 100)
INSERT INTO blog_posts (id, title, slug, excerpt, content, author_id, status, published_at, created_at, updated_at) VALUES
(1, 'Kinh Nghiệm Du Lịch Đà Nẵng Tự Túc 2024 Từ A-Z', 'kinh-nghiem-du-lich-danang-2024', 'Tất tần tật những điều cần biết cho chuyến đi trọn vẹn.', 'Đà Nẵng không chỉ là thành phố của những cây cầu...', 2, 'published', NOW(), NOW(), NOW()),
(2, 'Top 10 Món Ăn Đặc Sản Đà Nẵng Phải Thử Một Lần', 'top-10-mon-an-dac-san-danang', 'Từ Mì Quảng, Bánh tráng cuốn thịt heo đến Bún chả cá.', 'Khám phá hương vị miền Trung đậm đà...', 2, 'published', NOW(), NOW(), NOW());

-- Generate more posts 3-100
INSERT INTO blog_posts (id, title, slug, excerpt, content, author_id, status, published_at, created_at, updated_at)
SELECT 
    i, 
    'Blog Post Title ' || i, 
    'blog-slug-' || i, 
    'Brief excerpt for blog post ' || i, 
    'Full content for blog post ' || i, 
    (i % 5) + 1, 
    'published', 
    NOW(), 
    NOW(), 
    NOW()
FROM generate_series(3, 100) AS i;

-- 2. BLOG_POST_CATEGORIES (Pivots)
INSERT INTO blog_post_categories (post_id, blog_category_id)
SELECT 
    (random() * 99 + 1)::int, 
    (random() * 99 + 1)::int
FROM generate_series(1, 150)
ON CONFLICT DO NOTHING;
