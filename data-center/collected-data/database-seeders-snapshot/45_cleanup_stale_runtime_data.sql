BEGIN;

DELETE FROM failed_jobs;
DELETE FROM job_batches;
DELETE FROM cache_locks;

DELETE FROM password_reset_tokens
WHERE created_at < CURRENT_TIMESTAMP - INTERVAL '24 hours';

COMMIT;
