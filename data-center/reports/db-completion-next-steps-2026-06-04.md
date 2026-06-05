# DanangTrip DB Completion Report - 2026-06-04

## Current database state

- `locations`: 333
- `locations.active`: 111
- `locations.inactive`: 222
- `locations_missing_thumbnail`: 0
- `active_missing_thumbnail`: 0
- `inactive_missing_thumbnail`: 0
- `locations_missing_address`: 0
- `locations_missing_description`: 0
- `categories`: 100
- `location_tags`: 725
- `location_amenities`: 680
- `tours`: 100
- `tour_schedules`: 300
- `blog_posts`: 105
- `promotions`: 10
- `landing_pages`: 5
- `crawl_items`: 942

## Media work completed

- Exported 109 active locations missing thumbnails:
  - `D:\DATN\DATN_Tài liệu\data-center\media-assets\db-active-missing-thumbnail-locations.json`
- Downloaded 109/109 Pexels image candidates:
  - `D:\DATN\DATN_Tài liệu\data-center\media-assets\cloudinary-staging\locations\2026-06-04-active-missing-thumbnail`
- Uploaded 109/109 active location images to Cloudinary.
- Generated and applied:
  - `D:\DATN\DATN_Tài liệu\database-seeders\36_update_active_location_images_from_cloudinary_seed.sql`

## Duplicate review

Remaining duplicate normalized-name groups: 2.

These are not urgent public data blockers because duplicate rows are inactive except one active Memory Lounge row.

- `Memory Lounge`
  - `id=96`, `slug=memory-lounge-danang`, `status=active`
  - `id=221`, `slug=memory-lounge`, `status=inactive`
- `Nha hang HanCook`
  - `id=236`, `slug=nha-hang-hancook`, `status=inactive`
  - `id=237`, `slug=nha-hang-hancook-crawl-215`, `status=inactive`
  - `id=238`, `slug=nha-hang-hancook-crawl-216`, `status=inactive`

## Recommended next work

1. Admin review for 222 inactive locations.
   - Approve only rows with good name, address, category, image, and coordinates.
   - Keep weak restaurants/homestays inactive until manually reviewed.

2. Visual QA for Cloudinary image candidates.
   - Pexels images are category/context matched, not guaranteed exact-place photos.
   - Replace any image that looks wrong before production demo.

3. Tour data quality pass.
   - Verify every tour has schedule, linked destinations, valid price range, and Cloudinary image.
   - Replace any fake or generic tour descriptions with rewritten source-backed content.

4. Blog/content cleanup.
   - Ensure only real guide posts are published.
   - Keep test/demo content archived or draft.

5. Final DB QA seed/report.
   - Add a reusable SQL check for missing media, missing relations, duplicate names, inactive/public counts, and review queue size.
