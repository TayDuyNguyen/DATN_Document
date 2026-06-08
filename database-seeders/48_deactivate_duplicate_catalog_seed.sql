-- DanangTrip duplicate catalog visibility repair
-- Keeps historical relations; does not delete tours or blog posts.
BEGIN;

UPDATE tours SET status = 'inactive', booking_availability = 'sold_out', updated_at = NOW()
WHERE id IN (81, 21, 41, 42, 62, 22, 23, 63, 83, 44, 24, 84, 25, 85, 45, 26, 66, 86, 67, 47, 27, 68, 28, 88, 69, 89, 29, 30, 70, 90, 71, 91, 31, 72, 52, 92, 53, 33, 73, 74, 94, 54, 35, 75, 95, 56, 96, 36, 77, 37, 57, 98, 38, 58, 39, 59, 79, 40, 80, 100);

UPDATE blog_posts SET status = 'archived', updated_at = NOW() WHERE id = 105;

COMMIT;
