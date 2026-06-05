# Seed Run Order

## Base Project Seeds

1. `01_categories_subcategories.sql`
2. `02_tags_amenities.sql`
3. `03_tour_blog_categories.sql`
4. `04_users.sql`
5. `05_locations.sql`
6. `06_tours.sql`
7. `07_blog_posts.sql`
8. `08_bookings_payments.sql`
9. `09_ratings_interactions.sql`
10. `10_system_tables.sql`
11. `19_settings_seed.sql`

## Crawler Staging / Location POI

1. `11_crawl_staging_tables.sql`
2. `12_overpass_danang_pois_seed.sql`
3. `13_overpass_quality_review_seed.sql`
4. `14_pexels_image_enrichment_seed.sql`
5. `15_crawl_duplicate_matching_seed.sql`
6. `21_approve_overpass_clean_batch1.sql`
7. `23_approve_overpass_weak_address_landmarks.sql`
8. `24_approve_overpass_weak_address_services.sql`
9. `16_crawl_publish_approved_locations.sql`
10. `27_published_location_taxonomy_backfill.sql`

Note: `16` publishes into `locations.status = inactive`; `27` only adds tags/amenities for published crawl locations.

## Tour Staging

1. Run base categories/users/locations first.
2. Run `20_approved_tour_staging_seed.sql`.

Note: tour records are `pending_review` staging/demo records.

## Blog Guide Drafts

1. Run `03_tour_blog_categories.sql`.
2. Run `04_users.sql`.
3. Run `22_approved_blog_guides_seed.sql`.

Note: blog guide records are inserted as `draft` and need editing before publish.

## Landing FAQ Blocks

1. Run `18_landing_pages_seed.sql`.
2. Run `25_landing_faq_blocks_seed.sql`.

Note: FAQ blocks update `landing_pages.content_blocks` and should be reviewed before public use.

## Optional Cart Demo

1. Run `04_users.sql`.
2. Run `06_tours.sql` and/or `20_approved_tour_staging_seed.sql`.
3. Run `26_cart_items_demo_seed.sql`.

Note: cart rows are behavior/test data for checkout UI, not real crawled data.

## Final Coverage Check

1. Run all selected seed files first.
2. Run `28_seed_coverage_check.sql`.

Note: this file is read-only and reports table counts plus common relation gaps.
