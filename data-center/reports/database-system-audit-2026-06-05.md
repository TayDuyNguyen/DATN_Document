# DanangTrip Database System Audit - 2026-06-05

## Data locations

- SQL seed source of truth:
  - `D:\DATN\DATN_Tài liệu\database-seeders`
- Crawler scripts and memory:
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler`
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\memory.md`
- Data center reports/manifests/media:
  - `D:\DATN\DATN_Tài liệu\data-center`
- Cloudinary/local media staging:
  - `D:\DATN\DATN_Tài liệu\data-center\media-assets`

## One-command scripts

- Audit current DB:
  - `D:\DATN\DATN_Tài liệu\database-seeders\audit_database_quality.ps1`
- Apply DB seeders by manifest:
  - `D:\DATN\DATN_Tài liệu\database-seeders\apply_database_seeders.ps1`
- Seed manifest:
  - `D:\DATN\DATN_Tài liệu\database-seeders\seed-manifest.json`

## Commands

Audit DB:

```powershell
powershell -ExecutionPolicy Bypass -File "D:\DATN\DATN_Tài liệu\database-seeders\audit_database_quality.ps1"
```

Apply latest incremental backfills to current DB:

```powershell
powershell -ExecutionPolicy Bypass -File "D:\DATN\DATN_Tài liệu\database-seeders\apply_database_seeders.ps1" -Mode Incremental
```

Apply all seeders to a new empty/migrated DB:

```powershell
powershell -ExecutionPolicy Bypass -File "D:\DATN\DATN_Tài liệu\database-seeders\apply_database_seeders.ps1" -Mode Full
```

## Live DB audit result

- `locations`: 333
- `locations_active`: 221
- `locations_inactive`: 112
- `locations_missing_thumbnail`: 0
- `active_location_duplicate_lower_name_groups`: 0
- `categories`: 100
- `location_tags`: 725
- `location_amenities`: 680
- `tours`: 100
- `tour_schedules`: 300
- `tour_locations`: 192
- `tour_categories`: 100
- `tours_missing_cloudinary_thumbnail`: 0
- `tours_missing_or_empty_itinerary`: 0
- `tours_missing_or_empty_inclusions`: 0
- `tours_missing_or_empty_exclusions`: 0
- `tours_missing_or_empty_images`: 0
- `tours_without_schedule`: 0
- `tours_without_location_mapping`: 0
- `blog_posts`: 105
- `blog_categories`: 101
- `blog_missing_excerpt`: 0
- `blog_missing_content`: 0
- `blog_missing_featured_image`: 0
- `published_blog_missing_featured_image`: 0
- `promotions`: 10
- `landing_pages`: 5
- `crawl_items`: 942
- `crawl_pending_review`: 258
- `crawl_published`: 222
- `crawl_rejected`: 462
- `bookings`: 105
- `booking_items`: 158
- `payments`: 74
- `users`: 100

## Remaining gaps

1. Crawl review queue remains.
   - 258 `crawl_items` are still `pending_review`.
   - Duplicate pending rows were rejected by seed `42`.
   - Remaining pending rows should not be auto-published because they lack image candidates and many have weak address signals.

2. Inactive locations remain for review.
   - 112 inactive locations remain.
   - They are mostly lodging/homestay/hotel or manual-review/duplicate candidates.

3. Some tour slugs are generic.
   - Rows such as `tour-real-variant-*` now have complete data and Cloudinary media, but should be manually renamed/reviewed before a polished production demo.

## Current conclusion

The operational DB is now usable for app/demo flows:

- Locations are media-complete.
- Active locations have no duplicate name groups.
- Tours are media/content/schedule/location-complete.
- Published blogs are content/media-complete.
- Promotions and landing pages exist.

The next best improvement is manual review of the remaining crawl/location queues.
