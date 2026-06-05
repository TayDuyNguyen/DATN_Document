# Data Readiness Report - 2026-06-03

## Summary

DanangTrip now has source-backed staging data for the main demo surfaces:

- Locations/POI.
- Tours.
- Tour schedules.
- Blog/travel guide drafts.

No SQL has been applied to the database in this workflow. No API/admin/web code was changed.

## Location / POI

Source:

- OpenStreetMap / Overpass.
- Pexels URL candidates were already attached in the existing enrichment seed, but no new image assets were generated in the latest work.

Approval status:

- Batch 1 clean approval: 242 candidates.
- Batch 2 weak-address landmarks: 24 candidates.
- Batch 3 weak-address services: 11 candidates.
- Total approved staging candidates: 277.

Breakdown:

- Batch 1:
  - hotel: 131.
  - location: 15.
  - restaurant: 96.
- Batch 2:
  - selected landmarks/location only: 24.
- Batch 3:
  - restaurant: 10.
  - hotel: 1.

Still pending:

- 141 weak-address location records remain pending after landmark filtering.
- 162 weak-address restaurant/hotel records remain pending after service-signal filtering.
- Generic viewpoints, small parks, low-signal cafes, and low-signal hotels should not be auto-approved.

Seed files:

- `21_approve_overpass_clean_batch1.sql`
- `23_approve_overpass_weak_address_landmarks.sql`
- `24_approve_overpass_weak_address_services.sql`
- `16_crawl_publish_approved_locations.sql`

Publish note:

- `21`, `23`, and `24` only approve staging rows.
- `16` publishes approved rows into `locations.status = inactive`.
- Admin must activate records after review.

## Tours

Approved staging:

- New locations related to tours: 4.
- Tours: 34.
- Tour-location mappings: 57.
- Tour schedules: 136.

Pending:

- 2 fallback locations still need coordinate review:
  - Hoa Phu Thanh.
  - Nui Than Tai Hot Spring Park.
- 2 generic tours were rejected.

Seed file:

- `20_approved_tour_staging_seed.sql`

Publish note:

- Tour seed inserts records as review/staging data, not final production content.

## Blog / Travel Guide

Collected:

- 23 source-backed text-only guide records.
- 18 approved for draft seed.
- 5 pending due to redirect, duplicate slug, missing facts, or low text volume.

Approved draft topics include:

- Da Nang.
- Hoi An.
- Hue.
- Da Nang itinerary.
- Ba Na Hills.
- Marble Mountains.
- My Son.
- Da Nang food.
- Hai Van Pass.
- Son Tra Peninsula.
- Da Nang beaches.
- Airport/arrival transport.
- Transport within Vietnam.
- Plan your trip.
- Hoi An to Hue over Hai Van Pass.
- Da Nang insider/practical guide.

Seed file:

- `22_approved_blog_guides_seed.sql`

Publish note:

- Inserts as `draft`.
- `featured_image = NULL`.
- Content is short rewritten draft text, not copied long source text.
- Editor should rewrite/expand before setting `published`.

## Landing FAQ

Generated:

- 4 landing FAQ groups.
- 14 FAQ items.

Target landing pages:

- `du-lich-da-nang`.
- `cam-nang-du-lich-mien-trung`.
- `tour-ba-na-hills`.
- `tour-son-tra-ngu-hanh-son`.

Seed file:

- `25_landing_faq_blocks_seed.sql`

Publish note:

- Updates `landing_pages.content_blocks`.
- FAQ content is text-only and source-backed from existing guide staging.
- No images were generated.
- Review before public use.

## Recommended Seed Order

Base:

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

Crawler location staging:

1. `11_crawl_staging_tables.sql`
2. `12_overpass_danang_pois_seed.sql`
3. `13_overpass_quality_review_seed.sql`
4. `14_pexels_image_enrichment_seed.sql`
5. `15_crawl_duplicate_matching_seed.sql`
6. `21_approve_overpass_clean_batch1.sql`
7. `23_approve_overpass_weak_address_landmarks.sql`
8. `24_approve_overpass_weak_address_services.sql`
9. `16_crawl_publish_approved_locations.sql`

Additional draft/staging:

- Tours: `20_approved_tour_staging_seed.sql`
- Blog guides: `22_approved_blog_guides_seed.sql`
- Landing FAQ: `25_landing_faq_blocks_seed.sql`

## Readiness Decision

Recommended next action:

- Ready to publish location staging into DB as `inactive` if you want admin review inside the app.
- Ready to seed tour staging/demo.
- Ready to seed blog guide drafts.

Do not auto-publish as public/active yet.

Reasons:

- Location data still needs admin activation.
- Pexels image URLs are candidates, not guaranteed final production media.
- Blog guide drafts are intentionally short and need editor rewrite before public use.
- Some tour fields are inferred/defaulted and should be checked before selling.

## What Is Still Missing

High priority:

- Admin review/publish workflow for `crawl_items`.
- Manual coordinate review for Hoa Phu Thanh and Nui Than Tai Hot Spring Park.
- Final editor-ready Vietnamese content for blog guides.

Medium priority:

- Continue collecting FAQ-specific Q/A content.
- Review remaining 303 weak-address POIs manually or with stricter external source verification.
- Replace candidate image URLs with approved stable media later.

Low priority / seed only:

- Ratings.
- Favorites.
- Views.
- Bookings.
- Payments.
- Cart items.
- Notifications.
