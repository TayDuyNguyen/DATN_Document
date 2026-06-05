# Database Table Coverage Audit - 2026-06-03

Scope:

- Document root: `D:\DATN\DATN_Tài liệu`
- API source of truth: `D:\DATN\danangtrip-api\database\migrations`
- DBML: `D:\DATN\DATN_Tài liệu\docs\database\database.dbml`
- Seed SQL: `D:\DATN\DATN_Tài liệu\database-seeders`

## Summary

The API currently creates 37 production tables through Laravel migrations.

DBML coverage was missing one API table:

| Table | Status before audit | Action |
| --- | --- | --- |
| `landing_pages` | Missing in DBML | Added to `docs/database/database.dbml` on 2026-06-03 |

The DBML also documents 4 crawler staging tables that are created by seed SQL, not Laravel migrations:

- `crawl_sources`
- `crawl_jobs`
- `crawl_items`
- `crawl_logs`

This is acceptable because crawler staging is managed from `database-seeders/11_crawl_staging_tables.sql`.

## Real Data Status

As of 2026-06-03, the only collected real-world dataset with traceable source evidence is the Overpass/OpenStreetMap crawler output:

| Dataset | Source | Count | Status | Trust level |
| --- | --- | ---: | --- | --- |
| `overpass-danang-pois.json` | OpenStreetMap via Overpass API | 942 | `pending_review` staging | Real source, not production-ready |
| `overpass-danang-pois-clean.json` | Quality-filtered Overpass output | 580 | `pending_review` staging | Best current real dataset |
| `overpass-danang-pois-rejected.json` | Quality-filtered rejected output | 360 | `rejected` | Not for production |
| `overpass-danang-pois-enriched.json` | Pexels image candidates added | 580 | image-enriched staging | Do not trust for current requirement because image links/candidates are not accepted |

Clean Overpass split:

| Entity | Count |
| --- | ---: |
| `location` | 180 |
| `restaurant` | 220 |
| `hotel` | 180 |

Important: `database-seeders/01` through `10`, plus `17_promotions_seed.sql` and `18_landing_pages_seed.sql`, should be treated as demo/test seed data unless each row has external source evidence. They are useful for development, but they are not fully collected real-world data.

## Seed Coverage

Production tables with migrations but no dedicated SQL seed touch found in `D:\DATN\DATN_Tài liệu\database-seeders`:

| Table | Need seed? | Decision |
| --- | --- | --- |
| `settings` | Already covered in API repo | `D:\DATN\danangtrip-api\database\seeders\SettingSeeder.php` is called by `DatabaseSeeder`. Optional: add SQL mirror only if the document seed workflow must be standalone. |
| `promotions` | Covered | Added `database-seeders/17_promotions_seed.sql` for booking/admin coupon testing. |
| `landing_pages` | Covered | Added `database-seeders/18_landing_pages_seed.sql` with text/config-only landing content. No images. |
| `cart_items` | Usually no | Keep as runtime/test data. Prefer factories or test setup instead of production seed. |

Laravel import status:

- `D:\DATN\danangtrip-api\database\seeders\SqlSeeder.php` imports `17_promotions_seed.sql` and `18_landing_pages_seed.sql`.
- `D:\DATN\danangtrip-api\database\seeders\Concerns\ImportsSeederSql.php` resolves the current document seed folder: `D:\DATN\DATN_Tài liệu\database-seeders`.

## Real Data Collection Classification

Need real data collection:

| Table | Why |
| --- | --- |
| `locations` | Core tourism places need real name, address, district, coordinates, description, category and source evidence. Current Overpass clean set can feed this after admin review. |
| `location_tags` | Should be derived from real location categories/tags after review. |
| `location_amenities` | Should be derived from real POI amenities/source tags after review. |
| `tours` | Tour products need real itinerary, price, schedule rules, inclusions/exclusions and source/vendor evidence. Current seed is demo-like. |
| `tour_schedules` | Needs real departure dates, availability, deadline and prices. Current seed is test data. |
| `tour_locations` | Should be linked from real tours to real locations. |
| `blog_posts` | Should be real travel guide/editorial content with source/author review, or original owned content. Current seed is demo content. |
| `blog_post_categories` | Derived from real blog content. |
| `landing_pages` | Needs text/config content for real SEO pages. Current seed is text-only starter content, not externally collected. |
| `promotions` | Needs real business-approved campaign data. Current seed is test/demo. |
| `ratings` | Needs real user reviews or controlled test-only data. Do not claim seed ratings are real. |
| `rating_images` | Needs reviewed working URLs/uploaded media. Current image candidates are not trusted. |
| `views` | Analytics/runtime data; collect from app runtime, not static seed. |
| `favorites` | User runtime data; collect from app runtime, not static seed. |
| `search_logs` | Search runtime data; collect from app runtime, not static seed. |
| `contacts` | Real inbound user messages; seed only for UI/testing. |

Seed-only or internal/system is enough:

| Table | Why |
| --- | --- |
| `categories` | Controlled taxonomy. Seed is fine. |
| `subcategories` | Controlled taxonomy. Seed is fine. |
| `tags` | Controlled taxonomy. Seed is fine, can be expanded after crawl review. |
| `amenities` | Controlled taxonomy. Seed is fine. |
| `tour_categories` | Controlled taxonomy. Seed is fine. |
| `blog_categories` | Controlled taxonomy. Seed is fine. |
| `users` | Demo/admin/test users only. Real users come from registration. |
| `settings` | Internal config. Laravel `SettingSeeder` is enough. |
| `cart_items` | Runtime cart data. Usually no production seed. |
| `bookings` | Runtime transaction data. Seed only for admin/testing. |
| `booking_items` | Runtime transaction data. Seed only for admin/testing. |
| `payments` | Runtime transaction data. Seed only for admin/testing. |
| `notifications` | Mostly runtime/system generated. Seed only for UI/testing. |
| `refresh_tokens` | Runtime auth data. No real seed needed. |
| `password_reset_tokens` | Runtime auth data. No real seed needed. |
| `sessions` | Runtime auth/session data. No real seed needed. |
| `cache`, `cache_locks`, `jobs`, `job_batches`, `failed_jobs` | Infrastructure/runtime tables. No real seed needed beyond technical testing. |
| `crawl_sources`, `crawl_jobs`, `crawl_items`, `crawl_logs` | Staging/operations tables. Populated by crawler jobs, not final business seed. |

## Crawl Direction

User requirement: crawl and collect DB data only, no image creation.

Use crawl only for:

- text content
- structured metadata
- FAQ/content blocks
- destination/tour guide copy
- URLs and source evidence
- normalized JSON staged in `crawl_items`

Do not run image enrichment:

```powershell
npm.cmd run enrich:pexels
```

Do not create:

- generated images
- downloaded images
- thumbnail candidates
- OG image candidates
- Pexels/Unsplash enrichment seed

Image columns in production tables should stay `NULL`, empty, or use already-approved existing URLs.

## Crawl4AI Recommendation

Use Crawl4AI only for text-heavy web extraction where the current Overpass crawler is not enough.

Good targets:

- travel guide pages
- FAQ pages
- itinerary articles
- destination landing content
- policy/help pages
- tables/lists that need conversion into structured JSON

Do not use Crawl4AI for:

- image scraping
- bypassing terms of service
- direct production inserts

Recommended flow:

```text
Crawl4AI/text source
  -> raw markdown/html evidence
  -> normalized JSON
  -> crawl_items pending_review
  -> admin review
  -> seed/update landing_pages, blog_posts, FAQs or guide content
```

## Next Data Tasks

1. Optional: create SQL mirror for `settings` only if the SQL seed package must be runnable without Laravel seeders.
2. Add a text-only crawler source for destination landing content if more external text is needed.
3. Keep Pexels/image enrichment disabled unless the requirement changes.
4. Keep `cart_items` as runtime/test data unless a dedicated cart integration test needs fixture rows.
