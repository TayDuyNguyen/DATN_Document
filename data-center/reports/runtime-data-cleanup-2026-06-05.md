# Runtime Data Cleanup - 2026-06-05

## Backup

- File: `D:\DATN\DATN_Tài liệu\data-center\backups\runtime-cleanup-backup-20260605-142727.json`
- Backed up rows:
  - `failed_jobs`: 100
  - `job_batches`: 100
  - `cache_locks`: 100
  - `password_reset_tokens`: 100

The backup contains authentication/runtime data and must not be committed to a public repository.

## Applied cleanup

- Seed: `D:\DATN\DATN_Tài liệu\database-seeders\45_cleanup_stale_runtime_data.sql`
- Removed all seeded failed jobs, job batches and cache locks.
- Removed password reset tokens older than 24 hours.
- Preserved sessions, refresh tokens and all business data.

## Final audit

- `failed_jobs`: 0
- `job_batches`: 0
- `cache_locks`: 0
- `password_reset_tokens`: 0
- `sessions`: 101
- `refresh_tokens`: 168
- `expired_refresh_tokens`: 0
