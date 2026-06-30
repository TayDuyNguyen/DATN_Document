-- PostgreSQL Auto-Increment Sequence Reset Script
-- Purpose: Reset all sequence generators to their max ID to avoid unique constraint violations after seeding.
-- Run this script in your database editor (e.g. pgAdmin, DBeaver, Supabase SQL Editor) if you get 500 errors during inserts.

BEGIN;

SELECT setval(pg_get_serial_sequence('users', 'id'), GREATEST((SELECT COALESCE(MAX(id), 1) FROM users), 1), true);
SELECT setval(pg_get_serial_sequence('tours', 'id'), GREATEST((SELECT COALESCE(MAX(id), 1) FROM tours), 1), true);
SELECT setval(pg_get_serial_sequence('tour_schedules', 'id'), GREATEST((SELECT COALESCE(MAX(id), 1) FROM tour_schedules), 1), true);
SELECT setval(pg_get_serial_sequence('bookings', 'id'), GREATEST((SELECT COALESCE(MAX(id), 1) FROM bookings), 1), true);
SELECT setval(pg_get_serial_sequence('booking_items', 'id'), GREATEST((SELECT COALESCE(MAX(id), 1) FROM booking_items), 1), true);
SELECT setval(pg_get_serial_sequence('payments', 'id'), GREATEST((SELECT COALESCE(MAX(id), 1) FROM payments), 1), true);
SELECT setval(pg_get_serial_sequence('payment_receipts', 'id'), GREATEST((SELECT COALESCE(MAX(id), 1) FROM payment_receipts), 1), true);
SELECT setval(pg_get_serial_sequence('refund_requests', 'id'), GREATEST((SELECT COALESCE(MAX(id), 1) FROM refund_requests), 1), true);
SELECT setval(pg_get_serial_sequence('notifications', 'id'), GREATEST((SELECT COALESCE(MAX(id), 1) FROM notifications), 1), true);
SELECT setval(pg_get_serial_sequence('ratings', 'id'), GREATEST((SELECT COALESCE(MAX(id), 1) FROM ratings), 1), true);
SELECT setval(pg_get_serial_sequence('point_transactions', 'id'), GREATEST((SELECT COALESCE(MAX(id), 1) FROM point_transactions), 1), true);
SELECT setval(pg_get_serial_sequence('user_vouchers', 'id'), GREATEST((SELECT COALESCE(MAX(id), 1) FROM user_vouchers), 1), true);
SELECT setval(pg_get_serial_sequence('user_point_balances', 'id'), GREATEST((SELECT COALESCE(MAX(id), 1) FROM user_point_balances), 1), true);
SELECT setval(pg_get_serial_sequence('locations', 'id'), GREATEST((SELECT COALESCE(MAX(id), 1) FROM locations), 1), true);
SELECT setval(pg_get_serial_sequence('blog_posts', 'id'), GREATEST((SELECT COALESCE(MAX(id), 1) FROM blog_posts), 1), true);
SELECT setval(pg_get_serial_sequence('favorites', 'id'), GREATEST((SELECT COALESCE(MAX(id), 1) FROM favorites), 1), true);
SELECT setval(pg_get_serial_sequence('search_logs', 'id'), GREATEST((SELECT COALESCE(MAX(id), 1) FROM search_logs), 1), true);
SELECT setval(pg_get_serial_sequence('views', 'id'), GREATEST((SELECT COALESCE(MAX(id), 1) FROM views), 1), true);

COMMIT;
