# Data Inventory

## Tours

- Raw/normalized:
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\tour-crawl-raw.json`
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\tour-crawl-merged-normalized.json`
- Staging/review:
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\tour-staging-enriched.json`
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\tour-review-enriched.csv`
- Approved:
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\approved-tours-review.json`
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\approved-tour-locations-review.json`
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\approved-tour-schedules-review.json`
- Seed:
  - `D:\DATN\DATN_Tài liệu\database-seeders\20_approved_tour_staging_seed.sql`

## Locations / POI

- Raw/clean/enriched:
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\overpass-danang-pois.json`
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\overpass-danang-pois-clean.json`
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\overpass-danang-pois-enriched.json`
- Reports:
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\overpass-quality-report.json`
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\pexels-enrichment-report.json`
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\overpass-approval-batch1-report.json`
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\overpass-approval-batch2-weak-address-report.json`
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\overpass-approval-batch3-weak-address-services-report.json`
- Review:
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\overpass-approval-batch1-review.csv`
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\overpass-approval-batch2-weak-address-review.csv`
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\overpass-approval-batch3-weak-address-services-review.csv`
- Seeds:
  - `D:\DATN\DATN_Tài liệu\database-seeders\11_crawl_staging_tables.sql`
  - `D:\DATN\DATN_Tài liệu\database-seeders\12_overpass_danang_pois_seed.sql`
  - `D:\DATN\DATN_Tài liệu\database-seeders\13_overpass_quality_review_seed.sql`
  - `D:\DATN\DATN_Tài liệu\database-seeders\14_pexels_image_enrichment_seed.sql`
  - `D:\DATN\DATN_Tài liệu\database-seeders\15_crawl_duplicate_matching_seed.sql`
  - `D:\DATN\DATN_Tài liệu\database-seeders\21_approve_overpass_clean_batch1.sql`
  - `D:\DATN\DATN_Tài liệu\database-seeders\23_approve_overpass_weak_address_landmarks.sql`
  - `D:\DATN\DATN_Tài liệu\database-seeders\24_approve_overpass_weak_address_services.sql`
  - `D:\DATN\DATN_Tài liệu\database-seeders\16_crawl_publish_approved_locations.sql`

## Missing Tour Locations

- Candidates:
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\missing-location-candidates.json`
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\missing-locations-review.json`
- Approved:
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\approved-locations-review.json`

## Blog / Travel Guide

- Existing seed:
  - `D:\DATN\DATN_Tài liệu\database-seeders\07_blog_posts.sql`
- Crawl sources:
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\blog_guide_sources.json`
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\blog_guide_sources_batch4.json`
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\blog_guide_sources_batch5.json`
- Latest crawl:
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\blog-guides-batch3-raw.json`
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\blog-guides-batch3-normalized.json`
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\blog-guides-batch3-report.json`
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\blog-guides-batch4-clean-raw.json`
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\blog-guides-batch4-clean-normalized.json`
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\blog-guides-batch4-clean-report.json`
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\blog-guides-batch5-clean-raw.json`
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\blog-guides-batch5-clean-normalized.json`
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\blog-guides-batch5-clean-report.json`
- Staging/review:
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\blog-guides-staging.json`
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\blog-guides-staging-report.json`
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\blog-guides-review.csv`
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\blog-guides-review.json`
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\blog-guides-review-report.json`
- Approved/pending:
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\approved-blog-guides-review.csv`
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\approved-blog-guides-review.json`
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\pending-blog-guides-review.csv`
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\pending-blog-guides-review.json`
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\approved-blog-guides-seed-report.json`
- Seed:
  - `D:\DATN\DATN_Tài liệu\database-seeders\22_approved_blog_guides_seed.sql`
- Status:
  - Existing blog seed is demo-like content.
  - Batch 3 + batch 4 + batch 5 collected 23 source-backed text-only travel guide records.
  - 18 blog guide records are approved for draft seed.
  - 5 records remain pending because of redirect, deduped slug, or low text volume flags.
  - Seed `22` inserts approved records as `draft`, not `published`.
  - No images were generated.

## Landing FAQ

- Staging/review:
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\landing-faq-staging.json`
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\landing-faq-review.csv`
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\landing-faq-report.json`
- Seed:
  - `D:\DATN\DATN_Tài liệu\database-seeders\25_landing_faq_blocks_seed.sql`
- Status:
  - 4 landing groups.
  - 14 FAQ items.
  - Generated from source-backed guide staging.
  - No images were generated.
  - Updates `landing_pages.content_blocks`.

## Memory

- `D:\DATN\DATN_Tài liệu\danangtrip-crawler\memory.md`
