-- DanangTrip expired auth/runtime cleanup
-- Purpose:
--   Keep rebuild/incremental runs clean from stale authentication and runtime rows.
--   These rows are operational state, not curated catalog content.

BEGIN;

DELETE FROM password_reset_tokens
WHERE created_at IS NULL
   OR created_at < CURRENT_TIMESTAMP - INTERVAL '60 minutes';

DELETE FROM refresh_tokens
WHERE expires_at < CURRENT_TIMESTAMP;

DELETE FROM sessions
WHERE last_activity < EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - INTERVAL '24 hours'))::int;

DELETE FROM cache
WHERE expiration < EXTRACT(EPOCH FROM CURRENT_TIMESTAMP)::int;

DELETE FROM cache_locks
WHERE expiration < EXTRACT(EPOCH FROM CURRENT_TIMESTAMP)::int;

COMMIT;
