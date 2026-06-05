# Collection Status - 2026-06-03

## Centralization

- Created central folder: `D:\DATN\DATN_Tài liệu\data-center`
- This folder is an index/manifest center, not a destructive file move.
- Original crawler and seeder paths remain unchanged so scripts still work.

## Latest Blog Guide Crawl

- Source config: `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\blog_guide_sources.json`
- Raw output: `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\blog-guides-batch3-raw.json`
- Normalized output: `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\blog-guides-batch3-normalized.json`
- Report: `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\blog-guides-batch3-report.json`
- Batch 4 source config: `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\blog_guide_sources_batch4.json`
- Batch 4 normalized output: `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\blog-guides-batch4-clean-normalized.json`
- Batch 5 source config: `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\blog_guide_sources_batch5.json`
- Batch 5 normalized output: `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\blog-guides-batch5-clean-normalized.json`
- Merged staging: `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\blog-guides-staging.json`
- Review CSV: `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\blog-guides-review.csv`

Result:

- Total source-backed records in staging: 23.
- Batch 3 success: 9/9.
- Batch 4 success: 7/7.
- Batch 5 success: 7/7.
- Failures: 0.
- Mode: text-only, no generated images.
- Status of records: pending_review.
- Records with review flags: 5.
- Approved for draft seed: 18.
- Pending: 5.
- Draft seed: `D:\DATN\DATN_Tài liệu\database-seeders\22_approved_blog_guides_seed.sql`

Collected topics:

- Da Nang.
- Hoi An.
- Hue.
- 3 perfect days in Danang.
- Must-visit places in Da Nang.
- Ba Na Hills.
- Marble Mountains.
- My Son.
- Da Nang pork rolls / local food.
- Hai Van Pass.
- Son Tra Peninsula.
- Da Nang beaches.
- Da Nang mountain tourism.
- Airport/arrival transport.
- Transport within Vietnam.
- Plan your trip.
- Hoi An to Hue via Hai Van Pass.
- Da Nang insider/practical guide.

## Next Work

- Edit/rewrite the 12 draft blog guide records before publishing.
- Review the 4 pending flagged records.
- Decide whether `22_approved_blog_guides_seed.sql` supplements or later replaces part of `07_blog_posts.sql`.
- Continue pending POI review after batch 2:
  - Batch 2 approved 24 selected weak-address landmarks.
  - Batch 3 approved 11 selected weak-address restaurant/hotel records with at least 2 operational/source signals.
  - Restaurants/hotels with weak address remain pending.
  - Generic viewpoints and minor parks remain pending.
