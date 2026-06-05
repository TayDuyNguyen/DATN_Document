# Locations Real Data Audit - 2026-06-03

## Module

- Table/module: `locations` / destinations.
- Related staging tables: `crawl_sources`, `crawl_jobs`, `crawl_items`, `crawl_logs`.
- Related production relations: `location_tags`, `location_amenities`, `tour_locations`, `ratings`, `favorites`, `views`.

## Production Schema Coverage

The current `locations` production schema supports the main fields needed by the crawler:

- Identity: `name`, `slug`, `category_id`, `subcategory_id`.
- Content: `description`, `short_description`, `address`, `district`, `ward`.
- Map: `latitude`, `longitude`.
- Contact/source details: `phone`, `email`, `website`, `opening_hours`.
- Commerce/display: `price_min`, `price_max`, `price_level`, `thumbnail`, `images`, `video_url`.
- Moderation: `status`, `is_featured`, `created_by`.
- Metrics: `avg_rating`, `review_count`, `view_count`, `favorite_count`.

No schema change is required for the current Overpass staging pipeline.

## Existing Seed Status

`D:\DATN\DATN_Tài liệu\database-seeders\05_locations.sql` should be treated as development/demo seed data, not verified production data.

Reasons:

- It has no per-row crawl source, source URL, external ID, or collected timestamp.
- It mixes Da Nang with nearby tourism areas such as Hoi An, Quang Nam, Hue, and Ba Na Hills.
- It can be useful for UI/API development because many related seed files depend on location IDs, but it is not enough evidence for "real collected data".

Keep it temporarily for local development and relationship testing. Do not count it as verified collected data.

## Real Data Collected

Source: OpenStreetMap / Overpass API.

Files:

- `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\overpass-danang-pois.json`
- `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\overpass-danang-pois-clean.json`
- `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\overpass-danang-pois-rejected.json`
- `D:\DATN\DATN_Tài liệu\database-seeders\12_overpass_danang_pois_seed.sql`
- `D:\DATN\DATN_Tài liệu\database-seeders\13_overpass_quality_review_seed.sql`
- `D:\DATN\DATN_Tài liệu\database-seeders\15_crawl_duplicate_matching_seed.sql`
- `D:\DATN\DATN_Tài liệu\database-seeders\16_crawl_publish_approved_locations.sql`

Collected counts:

- Raw normalized POIs: 942.
- Clean pending-review POIs: 580.
- Rejected POIs: 360.
- Clean split:
  - `location`: 180.
  - `restaurant`: 220.
  - `hotel`: 180.

Current production import status:

- Published production `locations`: 0 from this audit action.
- Staged crawler data: ready through `CrawlerSeeder`.
- Production publish is intentionally gated by admin review and `16_crawl_publish_approved_locations.sql`.

## Image Status

The Pexels enrichment output is not trusted for production right now.

Reasons:

- The user confirmed the current seed image URLs are not reliable.
- Pexels search results are candidates only and may not represent the exact place.
- External images require manual/legal review before production use.

Decision:

- `14_pexels_image_enrichment_seed.sql` is not part of the automatic `CrawlerSeeder` flow.
- `16_crawl_publish_approved_locations.sql` does not require Pexels images.
- Locations should be published without external image candidates unless reviewed manually.

## Pipeline Decision

Automatic crawler seeding should import:

1. `11_crawl_staging_tables.sql`
2. `12_overpass_danang_pois_seed.sql`
3. `13_overpass_quality_review_seed.sql`
4. `15_crawl_duplicate_matching_seed.sql`

Manual/admin-only publish:

1. Review `crawl_items.status = 'pending_review'`.
2. Mark accepted records as `approved`.
3. Run `16_crawl_publish_approved_locations.sql`.
4. Published rows enter `locations` with `status = 'inactive'`.
5. Admin activates final rows after checking content, duplicates, and images.

## Gaps

- Overpass data often lacks phone, website, opening hours, ward, rating, price, and full address.
- Real image evidence is still missing.
- Existing production/demo seed `05_locations.sql` should not be used as collected-data proof.
- Admin review API/UI is still required before safe publish.

## Next Work

Before moving this module to production:

1. Build or expose an admin review screen/API for `crawl_items`.
2. Review the 580 clean records.
3. Approve only verified records.
4. Publish approved rows into `locations`.
5. Add reviewed/manual image assets or use a trusted image source with explicit evidence.

Recommended next table/module after this: `restaurants` and `hotels` are already included in the same Overpass crawl as entity types, but they currently publish into `locations`. If the system needs separate production tables for restaurants/hotels, audit that schema before publishing those entity types.
