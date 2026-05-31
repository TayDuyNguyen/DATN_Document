# DanangTrip Crawler Memory

Last updated: 2026-05-31

## Purpose

This folder defines the first version of a standalone data collection system for DanangTrip.

The crawler must collect real tourism data for Da Nang, normalize it, keep raw evidence, and push only reviewed/approved data into the main DanangTrip database later.

## Current Decision

Build the crawler as a separate service/module, not inside `danangtrip-api`.

Reason:

- Crawling can be slow and unstable.
- It needs retries, logs, and source-specific logic.
- The public API should not be blocked by crawl jobs.
- Admin users should review data before publishing.

## Target Data

Priority data types:

1. Locations: attractions, beaches, bridges, temples, markets, landmarks.
2. Restaurants and cafes.
3. Hotels and stays.
4. Tours and schedules.
5. Blog/FAQ/travel guide content.
6. Legal image references from official APIs such as Pexels/Unsplash or owned assets.

## Source Priority

Initial priority:

1. Google Places API for real places, coordinates, ratings, opening hours, and place IDs.
2. Pexels/Unsplash API for reusable image candidates.
3. Crawl4AI/Firecrawl or Crawlee for tourism blog/FAQ content.
4. Crawlee + Playwright for dynamic websites only when allowed by robots.txt and terms.

Avoid copying copyrighted images or scraping private/protected content.

## Architecture Decision

Pipeline:

```text
Source config
  -> Crawler worker
  -> Raw item storage
  -> Normalizer
  -> Enrichment
  -> Pending review
  -> Admin approval
  -> Publish to DanangTrip tables
```

The first implementation is a Node.js/TypeScript scaffold.

Expected future runtime:

- Node.js 20+
- TypeScript
- Crawlee + Playwright for website crawling
- Google Places API client/fetch for official place data
- PostgreSQL or DanangTrip API integration for persistence

## Current Folder Status

Created as a scaffold under:

`D:\DATN\DATN_Document\danangtrip-crawler`

Important files:

- `README.md`: detailed concept, workflow, setup, and roadmap.
- `memory.md`: this memory file for future AI/agent continuity.
- `package.json`: initial npm scripts and dependency plan.
- `.env.example`: environment variables needed later.
- `src/`: initial TypeScript scaffold.
- `data/`: local JSON output for early dry-run testing.
- `docs/schema.sql`: proposed staging database tables.

## Verification Status

Initial scaffold was installed and tested on 2026-05-31.

Commands run:

```powershell
npm.cmd install
npm.cmd run typecheck
npm.cmd run crawl:mock
```

Result:

- Dependencies installed successfully.
- TypeScript typecheck passed.
- Mock crawl completed successfully.
- Output generated at `data/crawl-items.json` with 2 pending-review location items.

Real Overpass crawl was implemented and tested on 2026-05-31.

Commands run:

```powershell
npm.cmd run typecheck
npm.cmd run crawl:overpass
```

Result:

- TypeScript typecheck passed.
- Overpass API crawl completed successfully.
- Output generated at `data/overpass-danang-pois.json`.
- Total normalized pending-review items: 942.
- Entity split:
  - `location`: 218
  - `restaurant`: 483
  - `hotel`: 241
- Category split:
  - `check-in-noi-tieng`: 145
  - `hang-dong-nui-non`: 15
  - `bao-tang-di-tich`: 24
  - `cong-vien-nuoc`: 4
  - `ca-phe-tra-sua`: 251
  - `am-thuc-dia-phuong`: 233
  - `khach-san-homestay`: 240
  - `cong-vien-vuon-hoa`: 30

Notes:

- Data comes from OpenStreetMap via Overpass API.
- All output items are still `pending_review`.
- No Pexels image enrichment was run because no `PEXELS_API_KEY` has been provided yet.
- Next step should be duplicate/quality filtering before generating SQL seed or inserting staging rows.

Quality filtering was implemented and tested on 2026-05-31.

Command:

```powershell
npm.cmd run filter:overpass
```

Generated files:

- `data/overpass-danang-pois-clean.json`
- `data/overpass-danang-pois-rejected.json`
- `data/overpass-quality-report.json`
- `../database-seeders/13_overpass_quality_review_seed.sql`

Result:

- Input items: 942
- Unique after dedupe: 940
- Clean pending-review items: 580
- Rejected items: 360
- Clean split:
  - `location`: 180
  - `restaurant`: 220
  - `hotel`: 180

Next step:

1. Add Pexels image enrichment when `PEXELS_API_KEY` is available.
2. Add duplicate matching against existing `locations`.
3. Build admin review screen for `crawl_items`.

Vietnamese without diacritics policy was enforced on 2026-05-31.

Changes:

- Added `src/utils/text.ts` with `toAsciiText`.
- Normalized Overpass source fields, curated source payloads, normalized payloads, and raw payload strings to ASCII.
- Added `npm.cmd run seed:overpass` to regenerate `../database-seeders/12_overpass_danang_pois_seed.sql`.
- Regenerated Overpass crawl data, clean/rejected data, quality report, and SQL seed files.

Verification:

- `npm.cmd run typecheck` passed.
- `npm.cmd run crawl:overpass` returned 942 items.
- `npm.cmd run seed:overpass` wrote 942 staging items.
- `npm.cmd run filter:overpass` returned 580 clean items and 360 rejected items.
- `rg -n "[^\x00-\x7F]"` returned no matches for the main Overpass JSON outputs and SQL seed files.

Current text rule:

- Data content for crawler output and database seed must be Vietnamese without diacritics.
- Example: `Bao tang Da Nang`, `Duong Tran Phu`, `am thuc dia phuong`.
- Keep IDs, slugs, source names, and technical keys ASCII.

Pexels image enrichment was implemented and tested on 2026-05-31.

Command:

```powershell
npm.cmd run enrich:pexels
```

Generated files:

- `data/overpass-danang-pois-enriched.json`
- `data/pexels-enrichment-report.json`
- `../database-seeders/14_pexels_image_enrichment_seed.sql`

Result:

- Input clean items: 580
- Enrichment limit for first run: 80
- Photos per item: 3
- Enriched items: 80
- Items with images: 80
- Failures: 0

Full enrichment was attempted after setting `PEXELS_ENRICH_LIMIT=580`, but Pexels returned `429 Too Many Requests`.

Current result after resume-safe rerun:

- Total clean items: 580
- Total items with Pexels images: 472
- Remaining items without Pexels images: 108
- Last run stopped on throttle at `Nha tro Tan Canh`.
- `../database-seeders/14_pexels_image_enrichment_seed.sql` currently updates only the 472 items that have image candidates.

Notes:

- `PEXELS_API_KEY` is stored only in local `.env` and must not be committed.
- `.gitignore` was added to ignore `.env` and `node_modules/`.
- Pexels images are candidates only. Admin review is still required because search results may be close but not always exact for each place.
- The enrichment script is now resume-safe: it preserves existing images, skips already enriched items, and stops early when Pexels throttles requests.

## Implementation Guardrails

- Do not publish crawled data directly into production tables.
- Always store raw payload first.
- Preserve source URL/API ID/external ID for traceability.
- Add duplicate detection before approval.
- Admin review is required before publishing.
- Keep each source adapter isolated.
- Keep logs detailed enough to debug source failures.

## Next Recommended Steps

1. Install dependencies when the user is ready:
   `npm install`
2. Implement Google Places source first.
3. Add database connection or DanangTrip API write adapter.
4. Create admin screen/API for `crawl_items` review.
5. Add image source adapter with legal image APIs.
6. Add blog/FAQ crawler after place pipeline is stable.

## Open Questions

- Should staging data be written directly to the same PostgreSQL database as `danangtrip-api`, or to a separate crawler database first?
- Which image source is preferred: owned images, Pexels, Unsplash, or manual upload?
- Should AI enrichment use local model, Gemini/OpenAI API, or manual admin editing first?
