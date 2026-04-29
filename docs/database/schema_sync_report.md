# DanangTrip Database Schema Sync Report

- Sync date: `2026-04-29`
- API source of truth: [`d:/DATN/danangtrip-api/database/migrations`](d:/DATN/danangtrip-api/database/migrations)
- Docs synchronized:
  - [`sql.dbml`](d:/DATN/DATN_Tài liệu/docs/database/sql.dbml)
  - [`database.sql`](d:/DATN/DATN_Tài liệu/docs/database/database.sql)
  - [`sql.dbdiagram`](d:/DATN/DATN_Tài liệu/docs/database/sql.dbdiagram)

## Migration verification

Command run in [`d:/DATN/danangtrip-api`](d:/DATN/danangtrip-api):

```powershell
php artisan migrate:fresh
```

Result: `DONE` (all migrations completed successfully).

## Current table set (33)

1. users
2. password_reset_tokens
3. sessions
4. cache
5. cache_locks
6. jobs
7. job_batches
8. failed_jobs
9. categories
10. subcategories
11. tags
12. amenities
13. locations
14. location_tags
15. location_amenities
16. search_logs
17. notifications
18. blog_categories
19. blog_posts
20. blog_post_categories
21. tour_categories
22. tours
23. tour_schedules
24. bookings
25. booking_items
26. payments
27. contacts
28. favorites
29. views
30. ratings
31. rating_images
32. refresh_tokens
33. tour_locations

## Notes

- PHP startup warning about `imagick` was shown but did **not** block migrations.
- If you want strict CI-style verification, run additionally:

```powershell
php artisan migrate:fresh --seed
```
