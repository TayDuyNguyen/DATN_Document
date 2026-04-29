-- DanangTrip Real Data Seeder: System Tables (100 rows each)
-- FILE: 10_system_tables.sql

-- 1. SESSIONS (Target 100)
INSERT INTO sessions (id, user_id, ip_address, user_agent, payload, last_activity)
SELECT 
    md5(i::text), 
    (i % 50) + 1, 
    '127.0.0.' || i, 
    'Mozilla/5.0...', 
    'base64_payload_example', 
    extract(epoch from now())::int
FROM generate_series(1, 100) AS i;

-- 2. CACHE (Target 100)
INSERT INTO cache (key, value, expiration)
SELECT 
    'cache_key_' || i, 
    'cache_value_' || i, 
    extract(epoch from now())::int + 3600
FROM generate_series(1, 100) AS i;

-- 3. JOBS (Target 100)
INSERT INTO jobs (id, queue, payload, attempts, available_at, created_at)
SELECT 
    i, 
    'default', 
    '{"job":"ExampleJob"}', 
    0, 
    extract(epoch from now())::int, 
    extract(epoch from now())::int
FROM generate_series(1, 100) AS i;

-- 4. REFRESH_TOKENS (Target 100)
INSERT INTO refresh_tokens (id, user_id, token, expires_at, created_at, updated_at)
SELECT 
    i, 
    (i % 50) + 1, 
    md5(i::text || 'secret'), 
    NOW() + INTERVAL '30 days', 
    NOW(), 
    NOW()
FROM generate_series(1, 100) AS i;

-- 5. PASSWORD_RESET_TOKENS (Target 100)
INSERT INTO password_reset_tokens (email, token, created_at)
SELECT 
    'user' || i || '@example.com', 
    md5(i::text || 'reset'), 
    NOW()
FROM generate_series(1, 100) AS i;

-- 6. CACHE_LOCKS (Target 100)
INSERT INTO cache_locks (key, owner, expiration)
SELECT 
    'lock_' || i, 
    'owner_' || i, 
    extract(epoch from now())::int + 60
FROM generate_series(1, 100) AS i;

-- 7. JOB_BATCHES (Target 100)
INSERT INTO job_batches (id, name, total_jobs, pending_jobs, failed_jobs, failed_job_ids, created_at)
SELECT 
    md5(i::text || 'batch'), 
    'Batch ' || i, 
    10, 0, 0, '[]', 
    extract(epoch from now())::int
FROM generate_series(1, 100) AS i;

-- 8. FAILED_JOBS (Target 100)
INSERT INTO failed_jobs (id, uuid, connection, queue, payload, exception, failed_at)
SELECT 
    i, 
    gen_random_uuid()::text, 
    'database', 
    'default', 
    '{}', 
    'Exception error ' || i, 
    NOW()
FROM generate_series(1, 100) AS i;
