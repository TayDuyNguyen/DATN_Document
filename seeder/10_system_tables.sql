-- DanangTrip Real Data Seeder: System Tables (100 rows each)
-- FILE: 10_system_tables.sql

-- 1. SESSIONS (Target 100)
INSERT INTO sessions (id, user_id, ip_address, user_agent, payload, last_activity)
SELECT 
    md5(i::text || 'session'), 
    (CASE WHEN i % 2 = 0 THEN (i % 90) + 1 ELSE NULL END), 
    '172.16.' || (i % 255) || '.' || (i % 100), 
    (CASE 
        WHEN i % 3 = 0 THEN 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        WHEN i % 3 = 1 THEN 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15'
        ELSE 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1'
    END), 
    'YTo0OntzOjY6Il90b2tlbiI7czo0MDoiRGZtclU3RWN6S0ZqN1VqTzR6R3Z6S0ZqN1VqTzR6R3Z6S0ZqN1VqTzQiO3M6OToiX3ByZXZpb3VzIjthOjE6e3M6MzoidXJsIjtzOjI3OiJodHRwOi8vbG9jYWxob3N0OjgwMDAvbG9naW4iO31zOjY6Il9mbGFzaCI7YToyOntzOjM6Im9sZCI7YTowOnt9czo0OiJuZXciO2E6MDp7fX1zOjM6InBocCI7YTowOnt9fQ==', 
    extract(epoch from (NOW() - (random() * INTERVAL '24 hours')))::int
FROM generate_series(1, 100) AS i;

-- 2. CACHE (Target 100)
INSERT INTO cache (key, value, expiration)
SELECT 
    'danangtrip_cache_' || i, 
    '{"data":"Sample serialized data for item ' || i || '"}', 
    extract(epoch from (NOW() + INTERVAL '1 hour'))::int
FROM generate_series(1, 100) AS i;

-- 3. JOBS (Target 100)
INSERT INTO jobs (id, queue, payload, attempts, available_at, created_at)
SELECT 
    i, 
    'default', 
    '{"uuid":"' || md5(i::text) || '","displayName":"App\\Jobs\\SendBookingEmail","job":"Illuminate\\Queue\\CallQueuedHandler@call","maxTries":null,"maxExceptions":null,"failOnTimeout":false,"backoff":null,"timeout":null,"retryUntil":null,"data":{"commandName":"App\\Jobs\\SendBookingEmail","command":"O:24:\"App\\Jobs\\SendBookingEmail\":1:{s:10:\"booking_id\";i:' || i || ';}"}}', 
    0, 
    extract(epoch from NOW())::int, 
    extract(epoch from NOW())::int
FROM generate_series(1, 100) AS i;

-- 4. REFRESH_TOKENS (Target 100)
INSERT INTO refresh_tokens (id, user_id, token, expires_at, created_at, updated_at)
SELECT 
    i, 
    (i % 90) + 1, 
    md5(i::text || 'refresh_secret_' || NOW()), 
    NOW() + INTERVAL '30 days', 
    NOW() - INTERVAL '1 day', 
    NOW()
FROM generate_series(1, 100) AS i;

-- 5. PASSWORD_RESET_TOKENS (Target 100)
INSERT INTO password_reset_tokens (email, token, created_at)
SELECT 
    u.email, 
    md5(u.email || 'reset_' || i), 
    NOW() - (i * INTERVAL '1 hour')
FROM generate_series(1, 100) AS i
JOIN users u ON u.id = (i % 90) + 1;

-- 6. CACHE_LOCKS (Target 100)
INSERT INTO cache_locks (key, owner, expiration)
SELECT 
    'booking_lock_' || i, 
    'worker_' || (i % 5), 
    extract(epoch from (NOW() + INTERVAL '5 minutes'))::int
FROM generate_series(1, 100) AS i;

-- 7. JOB_BATCHES (Target 100)
INSERT INTO job_batches (id, name, total_jobs, pending_jobs, failed_jobs, failed_job_ids, created_at)
SELECT 
    md5(i::text || 'batch_id'), 
    'Import Locations Batch ' || i, 
    50, 0, 0, '[]', 
    extract(epoch from (NOW() - INTERVAL '2 hours'))::int
FROM generate_series(1, 100) AS i;

-- 8. FAILED_JOBS (Target 100)
INSERT INTO failed_jobs (id, uuid, connection, queue, payload, exception, failed_at)
SELECT 
    i, 
    md5(i::text || 'uuid'), 
    'database', 
    'high', 
    '{"job":"ProcessPayment"}', 
    'GuzzleHttp\\Exception\\ConnectException: Connection refused in /var/www/html/vendor/guzzlehttp/guzzle/src/Handler/CurlHandler.php:210', 
    NOW() - (random() * INTERVAL '7 days')
FROM generate_series(1, 100) AS i;
