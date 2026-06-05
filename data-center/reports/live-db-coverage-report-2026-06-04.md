# Live DB Coverage Report - 2026-06-04

## Scope

- Project: `D:\DATN\danangtrip-api`
- DB connection from API `.env`:
  - `APP_ENV=local`
  - `DB_CONNECTION=pgsql`
  - `DB_HOST=aws-1-ap-northeast-1.pooler.supabase.com`
  - `DB_DATABASE=postgres`
- Commands run were read-only:
  - `php artisan migrate:status`
  - `php artisan tinker --execute ...` with `SELECT count(*)` checks.
- No migration, seed, insert, update, or delete was executed.

## Migration Status

All migrations currently in `danangtrip-api/database/migrations` are marked `Ran` on the configured database.

## Table Counts

| Table | Rows | Status |
| --- | ---: | --- |
| categories | 100 | ok |
| subcategories | 100 | ok |
| tags | 100 | ok |
| amenities | 100 | ok |
| tour_categories | 100 | ok |
| blog_categories | 101 | ok |
| locations | 101 | ok |
| location_tags | 223 | ok |
| location_amenities | 287 | ok |
| tours | 100 | ok |
| tour_schedules | 300 | ok |
| tour_locations | 169 | weak_relation |
| blog_posts | 105 | ok |
| blog_post_categories | 87 | weak_relation |
| promotions | 0 | missing_seed_on_live_db |
| landing_pages | 0 | missing_seed_on_live_db |
| settings | 23 | ok |
| users | 100 | ok |
| bookings | 105 | ok |
| booking_items | 158 | ok |
| payments | 74 | ok |
| cart_items | 2 | optional_demo |
| ratings | 97 | ok |
| rating_images | 101 | ok |
| favorites | 110 | ok |
| views | 137 | ok |
| search_logs | 221 | ok |
| contacts | 100 | ok |
| notifications | 101 | ok |

## Missing Tables On Live DB

The crawler staging tables do not exist on the configured database:

- `crawl_sources`
- `crawl_jobs`
- `crawl_items`
- `crawl_logs`

This means crawler staging seeds `11` to `15`, approval seeds `21`/`23`/`24`, publish seed `16`, and taxonomy backfill seed `27` have not been applied to this DB.

## Relation Gaps

| Check | Issue Count |
| --- | ---: |
| tours_without_schedule | 0 |
| tours_without_location_mapping | 14 |
| locations_without_tags | 1 |
| locations_without_amenities | 1 |
| blog_posts_without_category | 33 |
| crawl_sources_table_exists | 0 |
| crawl_items_table_exists | 0 |

## Notable Records

Tours without location mapping:

- `tour-hue-1-ngay`
- `tour-my-son`
- `tour-hai-van-lang-co`
- `tour-dem-hoi-an`
- `tour-ba-na-night`
- `tour-vinwonders-nam-hoi-an`
- `tour-trekking-son-tra`
- `tour-bach-ma`
- `tour-street-food-danang`
- `tour-tra-que-farmer`
- `tour-du-thuyen-song-han`
- `tour-tam-giang-sunset`
- `tour-ca-hue-song-huong`
- `tour-snorkeling-son-tra`

Location without tag/amenity:

- `quan-bun-co-ha-`

Blog posts without category:

- 33 published posts are missing `blog_post_categories` rows.
- One notable test record exists: `test-title-1143398745`.

## Recommended Next Steps

1. Apply missing live DB content seeds only after confirming this remote database is safe to modify:
   - `17_promotions_seed.sql`
   - `18_landing_pages_seed.sql`
   - `25_landing_faq_blocks_seed.sql`
2. Decide whether crawler staging belongs on this live DB:
   - If yes, apply `11` to `15`, approval seeds, then publish/backfill manually.
   - If no, keep crawler staging in a separate review DB.
3. Create a fix seed for:
   - 14 tours missing `tour_locations`.
   - 33 blog posts missing categories.
   - 1 location missing tag/amenity.
4. Remove or rename the test blog record `test-title-1143398745` if it should not be public.

## Follow-up Seed Prepared

Created local seed only, not applied to DB:

- `D:\DATN\DATN_Tài liệu\database-seeders\29_live_relation_gap_fix_seed.sql`

Purpose:

- Add missing destination locations by slug for Hue, Lang Co, Hai Van, VinWonders Nam Hoi An, Son Tra, Bach Ma, Tra Que, Tam Giang, Perfume River, and Han River.
- Add missing `tour_locations` mappings for the 14 tours reported above.
- Add missing `blog_post_categories` mappings for 32 real posts.
- Add tag/amenity for `quan-bun-co-ha-`.

The test post `test-title-1143398745` is intentionally not mapped; it should be reviewed or removed separately.

## Applied Fixes - 2026-06-04

The following seed files were applied to the configured Supabase DB after approval:

- `17_promotions_seed.sql`
- `18_landing_pages_seed.sql`
- `25_landing_faq_blocks_seed.sql`
- `29_live_relation_gap_fix_seed.sql`
- `30_live_relation_gap_fix_followup_seed.sql`
- `31_archive_test_blog_posts_seed.sql`

Final read-only coverage:

| Check | Result |
| --- | ---: |
| promotions | 10 |
| landing_pages | 5 |
| tours_without_schedule | 0 |
| tours_without_location_mapping | 0 |
| locations_without_tags | 0 |
| locations_without_amenities | 0 |
| published_blog_posts_without_category | 0 |
| all_blog_posts_without_category | 1 |
| archived_test_posts | 1 |
| locations | 111 |
| tour_locations | 192 |
| blog_post_categories | 119 |
| location_tags | 245 |
| location_amenities | 301 |

Notes:

- The only remaining blog post without category is the archived test post `test-title-1143398745`.
- Public/published data no longer has the relation gaps found earlier.
- Crawler staging tables are still not applied to this DB.

## Crawler Staging Applied - 2026-06-04

After user approval, crawler staging was applied to the configured Supabase DB.

Applied:

- `11_crawl_staging_tables.sql`
- `12_overpass_danang_pois_seed.sql`
- `13_overpass_quality_review_seed.sql`
- `15_crawl_duplicate_matching_seed.sql`
- `21_approve_overpass_clean_batch1.sql`
- `23_approve_overpass_weak_address_landmarks.sql`
- `24_approve_overpass_weak_address_services.sql`

Not applied:

- `14_pexels_image_enrichment_seed.sql`
- `16_crawl_publish_approved_locations.sql`
- `27_published_location_taxonomy_backfill.sql`

Reason:

- User requested DB/data collection, not new image work.
- Approved crawl records should remain in staging for review.
- No additional crawl records were published to production `locations`.

Final crawler staging coverage:

| Check | Result |
| --- | ---: |
| crawl_sources | 1 |
| crawl_jobs | 1 |
| crawl_items | 942 |
| crawl_logs | 6 |
| approved crawl_items | 222 |
| pending_review crawl_items | 360 |
| rejected crawl_items | 360 |
| hotel crawl_items | 241 |
| location crawl_items | 218 |
| restaurant crawl_items | 483 |

Implementation notes:

- `12_overpass_danang_pois_seed.sql` was fixed to include `created_at` and `updated_at` values in the generated `SELECT` rows.
- Approval seeds `21`, `23`, and `24` were fixed for PostgreSQL `UPDATE ... FROM` syntax by moving the target-table condition into `WHERE`.
- Public data checks remained clean after staging apply:
  - `tours_without_location_mapping = 0`
  - `locations_without_tags = 0`
  - `locations_without_amenities = 0`
  - `published_blog_posts_without_category = 0`

## Approved Crawl Items Published As Inactive - 2026-06-04

After user approval, approved crawler records were published to production `locations` with `status = inactive`.

Applied:

- `16_crawl_publish_approved_locations.sql`
- `27_published_location_taxonomy_backfill.sql`
- `32_published_location_minimum_amenity_backfill.sql`

Final coverage after publish:

| Check | Result |
| --- | ---: |
| locations_total | 333 |
| locations_active | 111 |
| locations_inactive | 222 |
| crawl_items_published | 222 |
| crawl_items_pending_review | 360 |
| crawl_items_rejected | 360 |
| published_locations_without_tags | 0 |
| published_locations_without_amenities | 0 |
| tours_without_location_mapping | 0 |
| published_blog_posts_without_category | 0 |
| location_tags | 721 |
| location_amenities | 676 |

Notes:

- No new crawl-published location was activated automatically.
- The 222 published crawl locations are ready for admin review/activation.
- `14_pexels_image_enrichment_seed.sql` remains unapplied.

## Final Taxonomy Cleanup - 2026-06-04

Applied:

- `33_hancook_location_taxonomy_fix.sql`

Reason:

- Two inactive HanCook crawl-published locations still had no tag/amenity after the generic backfill.
- Rows were not activated or deleted; only minimal relation rows were inserted.

Final check:

| Check | Result |
| --- | ---: |
| locations_without_tags | 0 |
| locations_without_amenities | 0 |
| tours_without_schedule | 0 |
| tours_without_location_mapping | 0 |
| published_blog_posts_without_category | 0 |
| promotions | 10 |
| landing_pages | 5 |
| crawl_items | 942 |
| crawl_published | 222 |
| crawl_pending_review | 360 |
| crawl_rejected | 360 |
