-- DanangTrip Real Data Seeder: System Tables (Laravel Technical Data)
-- Source: Laravel Standard Operational Patterns
-- Retrieved Date: 2026-04-29

-- 1. SESSIONS
INSERT INTO sessions (id, user_id, ip_address, user_agent, payload, last_activity) VALUES
('sess_v8k5K1m2n3o4p5q6r7s8t9u0v1w2x3y4z5a6b7c8', 1, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36', 'YTo0OntzOjY6Il90b2tlbiI7czo0MDoidjhrNUsxbTJuM280cDVxNnI3czh0OXUwdjF3MngzeTR6NWE2YjdjOCI7czo5OiJfcHJldmlvdXMiO2E6MTp7czozOiJ1cmwiO3M6MjE6Imh0dHA6Ly9sb2NhbGhvc3QvaG9tZSI7fXM6NzoiX2ZsYXNoIjthOjI6e3M6Mzoib2xkIjthOjA6e31zOjM6Im5ldyI7YTowOnt9fXM6NToibG9naW4iO3M6MToiMSI7fQ==', 1714350000),
('sess_m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2', 3, '192.168.1.15', 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1', 'YTo0OntzOjY6Il90b2tlbiI7czo0MDoibTNpNG81cDZxN3I4czl0MHUxdjJ3M3g0eTV6NmE3YjhjOWQwZTFmMiI7czo5OiJfcHJldmlvdXMiO2E6MTp7czozOiJ1cmwiO3M6MjQ6Imh0dHA6Ly9sb2NhbGhvc3QvYm9va2luZyI7fXM6NzoiX2ZsYXNoIjthOjI6e3M6Mzoib2xkIjthOjA6e31zOjM6Im5ldyI7YTowOnt9fXM6NToibG9naW4iO3M6MToiMyI7fQ==', 1714355000);

-- 2. PASSWORD_RESET_TOKENS
INSERT INTO password_reset_tokens (email, token, created_at) VALUES
('huy.le@gmail.com', 'a6b7c8d9e0f1g2h3i4j5k6l7m8n9o0p1q2r3s4t5u6v7w8x9y0z1a2b3c4d5e6f7', NOW());

-- 3. JOBS
INSERT INTO jobs (id, queue, payload, attempts, reserved_at, available_at, created_at) VALUES
(1, 'default', '{"uuid":"550e8400-e29b-41d4-a716-446655440000","displayName":"App\\Jobs\\SendBookingConfirmation","job":"Illuminate\\Queue\\CallQueuedHandler@call","data":{"bookingId":1}}', 0, NULL, 1714360000, 1714360000),
(2, 'notifications', '{"uuid":"720e8400-e29b-41d4-a716-446655440001","displayName":"App\\Jobs\\ProcessPaymentWebhook","job":"Illuminate\\Queue\\CallQueuedHandler@call","data":{"transactionCode":"VNP202404281005"}}', 1, NULL, 1714360500, 1714360000);

-- 4. FAILED_JOBS
INSERT INTO failed_jobs (id, uuid, connection, queue, payload, exception, failed_at) VALUES
(1, '990e8400-e29b-41d4-a716-446655440002', 'database', 'default', '{"displayName":"App\\Jobs\\UpdateExchangeRate"}', 'Illuminate\Http\Client\ConnectionException: Connection timed out after 5000ms', NOW());

-- 5. CACHE
INSERT INTO cache ("key", value, expiration) VALUES
('danangtrip_cache_v1:site_settings', 'a:2:{s:9:"site_name";s:10:"DanangTrip";s:12:"contact_mail";s:20:"info@danangtrip.vn";}', 1716940800),
('danangtrip_cache_v1:popular_tours_ids', 'a:3:{i:0;i:1;i:1;i:2;i:2;i:4;}', 1714425600);

-- 6. CACHE_LOCKS
INSERT INTO cache_locks ("key", owner, expiration) VALUES
('danangtrip_cache_v1:booking_lock_1', 'user_3', 1714361000);
