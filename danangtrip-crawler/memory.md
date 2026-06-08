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
- Total items with Pexels images: 580
- Remaining items without Pexels images: 0
- Last successful full resume run: 2026-06-01
- `../database-seeders/14_pexels_image_enrichment_seed.sql` currently updates all 580 clean items that have image candidates.

Notes:

- `PEXELS_API_KEY` is stored only in local `.env` and must not be committed.
- `.gitignore` was added to ignore `.env` and `node_modules/`.
- Pexels images are candidates only. Admin review is still required because search results may be close but not always exact for each place.
- The enrichment script is now resume-safe: it preserves existing images, skips already enriched items, and stops early when Pexels throttles requests.

Duplicate matching and controlled publish seeds were added on 2026-06-01.

Generated files:

- `../database-seeders/15_crawl_duplicate_matching_seed.sql`
- `../database-seeders/16_crawl_publish_approved_locations.sql`

Behavior:

- `15_crawl_duplicate_matching_seed.sql` adds production duplicate metadata columns to `crawl_items` and matches staging records against production `locations` by slug/name slug and GPS distance up to 150m.
- `16_crawl_publish_approved_locations.sql` publishes only `crawl_items.status = 'approved'`, skips records with `duplicate_source_id`, inserts into `locations.status = 'inactive'`, and marks staging rows as `published`.
- `16_crawl_publish_approved_locations.sql` is not imported automatically. It should be run only after admin review.
- `danangtrip-api/database/seeders/CrawlerSeeder.php` now imports 11, 12, 13, 14, and 15 so staging, quality, images, and duplicate metadata are prepared together.

Database seeder encoding was normalized on 2026-06-01.

Command:

```powershell
npm.cmd run normalize:seeders
```

Result:

- `01_categories_subcategories.sql` through `09_ratings_interactions.sql` were changed.
- `10_system_tables.sql` already had no non-ASCII content.
- `rg -n "[^\x00-\x7F]" D:\DATN\DATN_Document\database-seeders` returned no matches.
- Added `scripts/normalize-database-seeders.mjs` and package script `normalize:seeders`.

Rule:

- All SQL seed files must remain ASCII / Vietnamese without diacritics.
- If old data has mojibake such as `NhÃ  hÃ ng`, run `npm.cmd run normalize:seeders` before committing.

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

## 2026-06-03 - locations / destinations audit

### Cong viec da lam

- Doc lai prompt lam viec: moi thao tac lien quan den crawl/data/seed/schema/data check phai cap nhat memory.
- Kiem tra `locations` trong `danangtrip-api`: migration, model, controller, repository va quy trinh seed crawler.
- Doi chieu du lieu that hien co trong `danangtrip-crawler` voi seed hien co trong `database-seeders`.
- Phan loai `05_locations.sql` la seed dev/demo, khong tinh la du lieu crawl co bang chung nguon.
- Cap nhat `CrawlerSeeder.php` de import dung pipeline staging khong dung anh Pexels tu dong.
- Cap nhat `16_crawl_publish_approved_locations.sql` de bo yeu cau bat buoc voi `14_pexels_image_enrichment_seed.sql`.
- Tao audit doc: `docs/locations-real-data-audit-2026-06-03.md`.

### Bang/module

- `locations`
- Related staging: `crawl_sources`, `crawl_jobs`, `crawl_items`, `crawl_logs`

### Nguon du lieu

- Real source: OpenStreetMap / Overpass API.
- Existing dev source: `05_locations.sql` only for local UI/API testing.
- Image source Pexels: khong tin cay cho production theo yeu cau hien tai, khong tinh la du lieu that hop le.

### Ket qua

- So ban ghi raw da thu thap: 942.
- So ban ghi hop le can review: 580.
- So ban ghi bi loai: 360.
- Clean split:
  - `location`: 180.
  - `restaurant`: 220.
  - `hotel`: 180.
- So ban ghi production `locations` da publish trong lan nay: 0.
- Ly do chua publish: can admin review, duplicate check, va kich hoat thu cong.

### Files da thay doi

- `D:\DATN\danangtrip-api\database\seeders\CrawlerSeeder.php`
- `D:\DATN\DATN_Tài liệu\database-seeders\16_crawl_publish_approved_locations.sql`
- `D:\DATN\DATN_Tài liệu\danangtrip-crawler\docs\locations-real-data-audit-2026-06-03.md`
- `D:\DATN\DATN_Tài liệu\danangtrip-crawler\memory.md`

### Pipeline hien tai

- Automatic crawler seed:
  1. `11_crawl_staging_tables.sql`
  2. `12_overpass_danang_pois_seed.sql`
  3. `13_overpass_quality_review_seed.sql`
  4. `15_crawl_duplicate_matching_seed.sql`
- Manual/admin-only publish:
  - `16_crawl_publish_approved_locations.sql`
- Khong auto import:
  - `14_pexels_image_enrichment_seed.sql`

### Van de

- `05_locations.sql` la seed demo/dev, khong co source URL/external ID/collected timestamp cho tung dong.
- Pexels image candidates khong dang tin de dua vao production.
- Overpass thieu nhieu truong nhu phone, website, opening_hours, ward, rating, price, dia chi day du.
- Can man/API admin review `crawl_items` truoc khi publish.
- Lenh shell kiem tra thoi gian/PHP lint bi runner sandbox loi `CreateProcessAsUserW failed: 1312`, nen chua verify bang command duoc trong lan nay.

### Viec tiep theo

- Hoan thien review/publish workflow cho `locations`.
- Review 580 clean records trong `crawl_items`.
- Chi approve ban ghi da xac minh.
- Publish bang `16_crawl_publish_approved_locations.sql`.
- Them anh that da review thu cong hoac dung nguon anh co bang chung ro rang.

## 2026-06-03 - categories / subcategories audit

### Cong viec da lam

- Kiem tra schema `categories` va `subcategories` trong `danangtrip-api`.
- Kiem tra seed `01_categories_subcategories.sql`.
- Doi chieu category slug ma Overpass crawler dang sinh ra voi taxonomy hien co.
- Tao audit doc: `docs/categories-subcategories-audit-2026-06-03.md`.

### Bang/module

- `categories`
- `subcategories`

### Nguon du lieu

- Controlled seed/config: `01_categories_subcategories.sql`.
- Crawler reference: `overpass-quality-report.json` va mapping trong `overpassDanangPoisSource.ts`.

### Ket qua

- So ban ghi can crawl that: 0.
- So ban ghi seed/config hien co: 100 categories, 100 subcategories.
- So category slug Overpass clean data dang dung: 8.
- Clean category mapping:
  - `cong-vien-nuoc`: 3.
  - `bao-tang-di-tich`: 19.
  - `check-in-noi-tieng`: 116.
  - `cong-vien-vuon-hoa`: 29.
  - `hang-dong-nui-non`: 13.
  - `am-thuc-dia-phuong`: 148.
  - `ca-phe-tra-sua`: 73.
  - `khach-san-homestay`: 179.

### Quyet dinh

- `categories` va `subcategories` khong nen crawl nhu bang du lieu that.
- Day la taxonomy san pham, can on dinh slug de UI, API filter va crawler mapping khong bi vo.
- Giu seed hien tai lam controlled taxonomy.
- Khong auto sinh category moi tu raw crawl tags.

### Files da thay doi

- `D:\DATN\DATN_Tài liệu\danangtrip-crawler\docs\categories-subcategories-audit-2026-06-03.md`
- `D:\DATN\DATN_Tài liệu\danangtrip-crawler\memory.md`

### Van de

- Seed category rat rong, phu hop city directory hon la travel-only app.
- Neu san pham chi tap trung du lich Da Nang, nen tinh gon category sau khi chot UX.
- Mot so subcategory chua duoc crawler dung toi.

### Viec tiep theo

- Audit tiep `tags` va `amenities`.
- Xac dinh tag/amenity nao la seed/config, tag nao co the lay tu OSM tags.

## 2026-06-03 - tags / amenities audit

### Cong viec da lam

- Kiem tra schema `tags`, `amenities`, `location_tags`, `location_amenities`.
- Kiem tra seed `02_tags_amenities.sql`.
- Kiem tra crawler Overpass hien dang luu OSM tags vao `normalized_payload.categories` va `raw_payload.osmTags`.
- Xac dinh publish SQL hien chua gan auto vao pivot `location_tags` / `location_amenities`.
- Tao audit doc: `docs/tags-amenities-audit-2026-06-03.md`.

### Bang/module

- `tags`
- `amenities`
- `location_tags`
- `location_amenities`

### Nguon du lieu

- Controlled seed/config: `02_tags_amenities.sql`.
- Real source reference in staging: OpenStreetMap / Overpass fields inside `raw_payload.osmTags`.

### Ket qua

- So ban ghi `tags` can crawl that doc lap: 0.
- So ban ghi `amenities` can crawl that doc lap: 0.
- So ban ghi seed/config hien co: 100 tags, 100 amenities.
- So pivot production da tao tu crawler trong lan nay: 0.

### Quyet dinh

- `tags` va `amenities` la controlled taxonomy/config, khong crawl nhu entity that.
- `location_tags` va `location_amenities` chi nen gan sau admin review hoac mapping rule da kiem chung.
- Khong auto tao tag/amenity moi tu OSM tags.
- Khong sua `16_crawl_publish_approved_locations.sql` de auto gan tag/amenity trong giai doan nay.

### Mapping co the lam sau

- `internet_access=yes|wlan` -> Wifi.
- `parking=*` -> Parking neu gia tri ro rang.
- `wheelchair=yes|limited` -> Accessibility.
- `opening_hours=24/7` -> Open 24/7.
- `takeaway=yes` -> Takeaway.
- `delivery=yes` -> Delivery.
- `outdoor_seating=yes` -> Outdoor seating.
- `cuisine=*` -> Food tags sau khi normalize vocabulary.

### Files da thay doi

- `D:\DATN\DATN_Tài liệu\danangtrip-crawler\docs\tags-amenities-audit-2026-06-03.md`
- `D:\DATN\DATN_Tài liệu\danangtrip-crawler\memory.md`

### Van de

- Chua co reviewed mapping file tu OSM tags sang `tags` / `amenities`.
- Seed amenities hoi nghieng ve hotel/service, khong phu hop tat ca loai location.
- Mot so label trong seed dang tieng Anh trong khi da so seed dung Vietnamese ASCII.
- Neu auto gan sai tag/amenity, filter UI se sai.

### Viec tiep theo

- Audit tiep `tour_categories` va `blog_categories`.
- Sau do moi xac dinh bang nao can crawl content that: tours, blog_posts, ratings, promotions, landing_pages.

## 2026-06-03 - tour_categories / blog_categories audit

### Cong viec da lam

- Kiem tra schema `tour_categories` va `blog_categories`.
- Kiem tra seed `03_tour_blog_categories.sql`.
- Kiem tra quan he voi `tours`, `blog_posts`, `blog_post_categories`.
- Kiem tra seed lien quan `06_tours.sql` va `07_blog_posts.sql` de phan biet taxonomy voi content/business data.
- Tao audit doc: `docs/tour-blog-categories-audit-2026-06-03.md`.

### Bang/module

- `tour_categories`
- `blog_categories`

### Nguon du lieu

- Controlled seed/config: `03_tour_blog_categories.sql`.
- Related demo seed evidence:
  - `06_tours.sql`
  - `07_blog_posts.sql`
- Crawler README: de xuat Crawl4AI / Firecrawl / Crawlee cho blog/FAQ/travel guide sau khi check robots.txt/terms.

### Ket qua

- So ban ghi `tour_categories` can crawl that doc lap: 0.
- So ban ghi `blog_categories` can crawl that doc lap: 0.
- So ban ghi seed/config hien co: 100 tour categories, 100 blog categories.
- So tour/blog real records da crawl trong lan nay: 0.

### Quyet dinh

- `tour_categories` va `blog_categories` la taxonomy/config, khong crawl nhu bang du lieu that.
- Giu `03_tour_blog_categories.sql` lam controlled seed.
- Khong auto tao category moi tu external sites.
- `06_tours.sql` va `07_blog_posts.sql` khong duoc tinh la du lieu that co bang chung nguon.

### Bang can thu thap that sau

- `tours`
- `tour_schedules`
- `tour_locations`
- `blog_posts`
- `blog_post_categories`

### Files da thay doi

- `D:\DATN\DATN_Tài liệu\danangtrip-crawler\docs\tour-blog-categories-audit-2026-06-03.md`
- `D:\DATN\DATN_Tài liệu\danangtrip-crawler\memory.md`

### Van de

- `06_tours.sql` co 20 tour viet tay va sinh dong 21-100 bang variation SQL, nen la demo/dev seed.
- `07_blog_posts.sql` co 100 bai style travel guide tieng Anh, khong co source URL/evidence tung dong.
- Chua co crawler/import workflow rieng cho tour inventory.
- Chua co crawler/import workflow rieng cho blog/travel guide content.
- `blog_categories` schema chua co `status` / `sort_order` nhu `tour_categories`.

### Viec tiep theo

- Audit tiep `tours`, `tour_schedules`, `tour_locations`.
- Xac dinh du lieu tour nao can lay tu doi tac/operator va du lieu nao chi nen seed demo.

## 2026-06-03 - locations image candidate enrichment

### Cong viec da lam

- Cai dependency crawler bang `npm install`.
- Chay crawl that Overpass cho `locations` bang `npm run crawl:overpass`.
- Chay lai quality filter bang `npm run filter:overpass`.
- Chay Pexels enrichment bang `npm run enrich:pexels`.
- Chay lai SQL staging raw bang `npm run seed:overpass`.
- Kiem tra nhanh 30 URL anh Pexels mau bang HEAD request.
- Cap nhat `.env.example` de them `PEXELS_REQUEST_DELAY_MS` va `PEXELS_STOP_ON_429`.

### Bang/module

- `locations`
- staging: `crawl_sources`, `crawl_jobs`, `crawl_items`, `crawl_logs`
- image candidates stored in `crawl_items.normalized_payload.imageUrls` and `crawl_items.raw_payload.imageCandidates` through seed `14_pexels_image_enrichment_seed.sql`

### Nguon du lieu

- Places/text: OpenStreetMap / Overpass API.
- Image candidate provider: Pexels API.
- Active mode: database/text + image URL candidates only, khong generate/tai anh ve production.

### Ket qua crawl/filter

- Raw Overpass items: 942.
- Unique after dedupe: 940.
- Clean pending-review items: 580.
- Rejected items: 360.
- Clean split:
  - `location`: 180.
  - `restaurant`: 220.
  - `hotel`: 180.

### Ket qua anh

- Input clean items: 580.
- Pexels limit: 580.
- Photos per item: 3.
- Request delay: 750ms.
- Selected missing items: 0.
- Newly enriched items: 0.
- Total items with image candidates: 580.
- Failures: 0.
- Throttled: false.
- Quick URL health sample: checked 30, ok 30, fail 0.

Note:

- `selectedMissingItems = 0` vi file enriched truoc do da co du 580 item co Pexels candidates, script resume-safe nen khong goi moi cho cac item da co anh.
- Anh Pexels van chi la candidates, can admin review phu hop noi dung va license/attribution truoc khi publish.

### Files da thay doi / tao lai

- `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\overpass-danang-pois.json`
- `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\overpass-danang-pois-clean.json`
- `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\overpass-danang-pois-rejected.json`
- `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\overpass-quality-report.json`
- `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\overpass-danang-pois-enriched.json`
- `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\pexels-enrichment-report.json`
- `D:\DATN\DATN_Tài liệu\database-seeders\12_overpass_danang_pois_seed.sql`
- `D:\DATN\DATN_Tài liệu\database-seeders\13_overpass_quality_review_seed.sql`
- `D:\DATN\DATN_Tài liệu\database-seeders\14_pexels_image_enrichment_seed.sql`
- `D:\DATN\DATN_Tài liệu\danangtrip-crawler\.env.example`
- `D:\DATN\DATN_Tài liệu\danangtrip-crawler\package-lock.json`
- `D:\DATN\DATN_Tài liệu\danangtrip-crawler\memory.md`

### Van de

- Pexels candidates co the dung ve mat URL nhung chua chac dung chinh xac dia diem.
- Khong duoc publish thang anh vao `locations.thumbnail` / `locations.images` neu chua review.
- User da paste Pexels API key trong chat; neu key tung bi lo cong khai thi nen rotate/regenerate.

### Viec tiep theo

- Neu muon refresh anh that su thay vi dung cache enriched, can them option force refresh vao script Pexels hoac xoa file enriched co kiem soat.
- Them workflow admin review image candidates.
- Sau khi review, moi publish approved locations va approved images vao production.

## 2026-06-03 - Python venv setup for crawler-only work

### Cong viec da lam

- Tao Python venv tai `D:\DATN\DATN_Tài liệu\danangtrip-crawler\.venv`.
- Them `.venv/` vao `.gitignore`.
- Cai dependency crawl co ban trong venv:
  - `httpx`
  - `beautifulsoup4`
  - `lxml`
  - `python-dotenv`
  - `pydantic`
- Verify import trong venv thanh cong voi output `venv-ok`.
- Tao `requirements.txt` de tai lap moi truong venv.

### Bang/module

- Chua crawl bang moi trong buoc nay.
- Muc tieu tiep theo hop ly: `tours`, `tour_schedules`, `tour_locations`.

### Nguon du lieu

- Chua co source tour hop le duoc user cung cap.

### Ket qua

- Venv ready: yes.
- Packages installed: yes.
- New records collected: 0.
- Files changed:
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\.gitignore`
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\requirements.txt`
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\memory.md`

### Van de

- Pip log co loi hien thi Unicode do duong dan co chu `Tài liệu`, nhung package da cai thanh cong.
- De crawl `tours` that, can source URL/API/doi tac hop le. Khong nen tu lay tour tu Klook/Traveloka/Booking/Tripadvisor neu khong co quyen/terms ro rang.

### Viec tiep theo

- User can bo sung source tour hop le:
  - URL danh sach tour cua doi tac/operator.
  - Hoac file CSV/Excel inventory tour.
  - Hoac API endpoint/credential neu co.
- Sau khi co source, crawler se chi ghi data ve file staging JSON/SQL, khong sua API/admin.

## 2026-06-03 - tours crawl batch 1 via Python venv

### Cong viec da lam

- Tao file source config `data/tour_sources.json`.
- Tao Python crawler `scripts/crawl_tours.py`.
- Chay crawler bang venv:
  - `.venv\Scripts\python.exe scripts\crawl_tours.py --max-pages-per-source 35 --delay-ms 750`
- Crawler co kiem tra robots.txt co ban, discover sitemap/home links, crawl HTML public, extract facts, image candidate URLs, va source URL.
- Khong sua API/admin.
- Khong publish DB.
- Khong copy nguyen van mo ta dai; chi tao `summary` rewrite ngan va giu facts/source.

### Bang/module

- `tours`
- future related tables:
  - `tour_schedules`
  - `tour_locations`

### Nguon du lieu

- `https://dacotours.com/`
- `https://hoiandaytrip.com/`
- `https://dananglocaltours.com/`
- `https://danangtourscity.com/`
- `https://venusvietnamtravel.com/`
- `https://vmtravel.com/`
- `https://vietnamadventuretour.com.vn/tour-category/da-nang-tours/`

### Ket qua

- Raw tour records collected: 242.
- Normalized tour records: 242.
- Records with `sourceUrl`: 242.
- Records with price: 186.
- Records with duration: 187.
- Records with image candidates: 236.
- By source:
  - `dacotours`: 35.
  - `hoiandaytrip`: 35.
  - `dananglocaltours`: 32.
  - `danangtourscity`: 35.
  - `venusvietnamtravel`: 35.
  - `vmtravel`: 35.
  - `vietnamadventuretour`: 35.

### Files da tao / thay doi

- `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\tour_sources.json`
- `D:\DATN\DATN_Tài liệu\danangtrip-crawler\scripts\crawl_tours.py`
- `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\tour-crawl-raw.json`
- `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\tour-crawl-normalized.json`
- `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\tour-crawl-report.json`
- `D:\DATN\DATN_Tài liệu\danangtrip-crawler\memory.md`

### Van de

- Day moi la JSON staging, chua phai seed DB.
- Image chi la candidate URL tu source page, can review license/permission truoc khi dung production.
- Mot so tour khong extract duoc price/duration do website format khac nhau.
- Warning `XMLParsedAsHTMLWarning` xuat hien khi parse mot so XML/sitemap bang parser HTML, khong lam hong ket qua batch.
- Chua map sang `tour_category_id`, `tour_locations`, `tour_schedules`.

### Viec tiep theo

- Tao audit chat luong tour batch 1.
- Neu muon dua vao seed DB, can buoc normalize schema sang:
  - `tours`
  - `tour_schedules`
  - `tour_locations`
- Can mapping category va location:
  - category theo destination/theme.
  - location link theo dia danh trong itinerary/destination.

## 2026-06-03 - tours staging normalization batch 1

### Cong viec da lam

- Tao script `scripts/normalize_tours.py` de chuan hoa `data/tour-crawl-normalized.json` sang schema staging gan voi bang `tours`.
- Doc migration moi nhat cua API cho cac bang:
  - `tours`
  - `tour_schedules`
  - `tour_locations`
- Doc seed category hien co trong `database-seeders/03_tour_blog_categories.sql` de map category slug.
- Khong sua API/admin/web.
- Khong publish DB.

### Ket qua staging sach

- Raw crawl input: 242 records.
- Tour staging output: 17 records.
- Rejected/not staging: 225 records.
- Output files:
  - `data/tour-staging.json`
  - `data/tour-staging-report.json`

### Coverage trong `tour-staging.json`

- With price: 13/17.
- With duration: 16/17.
- With images: 17/17.
- With itinerary: 7/17.
- With destinations: 17/17.

### By category

- `tour-ba-na-hills`: 9.
- `tour-hoi-an`: 8.

### By source

- `dacotours`: 1.
- `dananglocaltours`: 5.
- `danangtourscity`: 1.
- `hoiandaytrip`: 2.
- `venusvietnamtravel`: 6.
- `vmtravel`: 2.

### Rule da ap dung

- Chi dua vao staging cac trang co tin hieu tour/detail ro rang.
- Loai blog/listicle/guide/category/tag/homepage/news.
- Loai private transfer, ticket/news/free entrance, gia placeholder `From $0`.
- Loai tour ngoai pham vi Da Nang, Hoi An, Hue, Ba Na, My Son, Cham Island.
- Anh chi la candidate URL tu source page, can review quyen su dung truoc production.
- Long description la rewritten summary ngan, khong copy nguyen van noi dung dai.
- Tat ca record staging de `status = inactive` va can manual review truoc khi seed/publish.

### Van de con lai

- Mot so tour thieu gia hoac duration do website format khac nhau.
- Category hien moi map duoc manh vao `tour-ba-na-hills` va `tour-hoi-an`.
- Chua tao SQL seed.
- Chua tao mapping `tour_locations` va `tour_schedules`.

### Viec tiep theo

- Neu can nhieu tour hon, crawl tiep bang source URL chinh xac la trang category/detail tour, khong crawl homepage rong.
- Neu chuan bi seed DB, can tao buoc review:
  - bo sung gia/duration cho record thieu.
  - gan `tour_category_id` theo DB thuc te.
  - map dia diem sang `tour_locations`.
  - tao lich trinh/co ngay trong `tour_schedules` neu can.

## 2026-06-03 - tours crawl batch 2 page-links

### Cong viec da lam

- Cap nhat `scripts/crawl_tours.py`:
  - them `--source-file`.
  - them `--output-prefix`.
  - them `--discover-mode` voi cac mode:
    - `sitemap`
    - `page-links`
    - `exact`
- Tao source batch 2:
  - `data/tour_sources_batch2.json`
- Tao script merge:
  - `scripts/merge_tour_crawls.py`
- Chay batch 2 bang venv voi mode `page-links`, khong quet sitemap toan site:
  - `.venv\Scripts\python.exe scripts\crawl_tours.py --source-file data\tour_sources_batch2.json --output-prefix tour-crawl-batch2-pagelinks --discover-mode page-links --max-pages-per-source 25 --delay-ms 750`
- Merge batch 1 + batch 2:
  - `data/tour-crawl-merged-normalized.json`
- Normalize merged va cap nhat canonical staging:
  - `data/tour-staging.json`
  - `data/tour-staging-report.json`
- Khong sua API/admin/web.
- Khong publish DB.

### Ket qua batch 2

- Batch 2 page-links raw: 240.
- Batch 2 page-links normalized unique: 164.
- Merged normalized unique: 365.
- Final staging clean: 36.
- Final rejected/not staging: 329.

### Coverage final `tour-staging.json`

- With price: 31/36.
- With duration: 35/36.
- With images: 36/36.
- With itinerary: 19/36.
- With destinations: 36/36.

### By category final

- `tour-ba-na-hills`: 13.
- `tour-hoi-an`: 23.

### By source final

- `dacotours`: 1.
- `dananglocaltours`: 5.
- `dananglocaltours_basket_boat`: 5.
- `danangtourscity`: 1.
- `hoiandaytrip`: 2.
- `hoiandaytrip_bana`: 2.
- `venus_cham_island`: 4.
- `venusvietnamtravel`: 6.
- `vietnamadventure_danang`: 2.
- `vmtravel`: 2.
- `vmtravel_danang_shore`: 4.
- `vmtravel_hue_shore`: 2.

### Files moi / cap nhat

- `data/tour_sources_batch2.json`
- `data/tour-crawl-batch2-raw.json`
- `data/tour-crawl-batch2-normalized.json`
- `data/tour-crawl-batch2-report.json`
- `data/tour-crawl-batch2-pagelinks-raw.json`
- `data/tour-crawl-batch2-pagelinks-normalized.json`
- `data/tour-crawl-batch2-pagelinks-report.json`
- `data/tour-crawl-merged-normalized.json`
- `data/tour-staging.json`
- `data/tour-staging-report.json`
- `data/tour-staging-merged.json`
- `data/tour-staging-merged-report.json`
- `scripts/crawl_tours.py`
- `scripts/merge_tour_crawls.py`
- `scripts/normalize_tours.py`

### Chat luong va can review

- `tour-staging.json` hien la file staging moi nhat de review.
- Van de con lai:
  - 5 tour thieu price.
  - 1 tour thieu duration.
  - Mot so nguon co gia/duration chung cua website, can review truoc khi seed production.
  - Anh van la candidate URL tu source, can review quyen su dung truoc production.
- Chua tao SQL seed.
- Chua tao mapping `tour_locations`.
- Chua tao mapping `tour_schedules`.

### Huong tiep theo

- Nen crawl tiep bang exact/page-links voi URL detail/category chinh xac hon neu muon tang so tour.
- Neu chuyen sang seed DB, buoc tiep theo la tao `tour-review.csv/json` de duyet 36 tour:
  - approve/reject.
  - fix price/duration.
  - gan category/location.
  - sau do moi sinh SQL seed.

## 2026-06-03 - tours review files

### Cong viec da lam

- Tao script `scripts/build_tour_review.py`.
- Sua parser gia trong `scripts/normalize_tours.py` de doc duoc VND dang `1.190.000 VND`.
- Chay lai normalize tu `data/tour-crawl-merged-normalized.json`.
- Tao file review cho 36 tour staging:
  - `data/tour-review.json`
  - `data/tour-review.csv`
  - `data/tour-review-report.json`
- Khong sua API/admin/web.
- Khong tao SQL seed.
- Khong publish DB.

### Ket qua review

- Total review items: 36.
- Pending review: 36.
- Approve for seed mac dinh: `false`.
- Missing price: 4.
- Missing duration: 1.
- Missing itinerary: 17.
- Missing inclusions: 7.
- Few images: 0.

### Y nghia file review

- `tour-review.csv` dung de duyet nhanh bang Excel/Google Sheets.
- `tour-review.json` dung cho AI/doc pipeline xu ly tiep.
- Moi record co:
  - `review_id`
  - `review_status`
  - `approve_for_seed`
  - `reject_reason`
  - `fix_notes`
  - facts crawl duoc
  - `review_flags`
  - `source_url`

### Viec tiep theo

- Duyet 36 tour trong `tour-review.csv/json`.
- Sua cac record co flag:
  - `missing_price`
  - `missing_duration`
  - `missing_itinerary`
  - `missing_inclusions`
- Sau khi co record `approve_for_seed = true`, moi tao SQL seed cho:
  - `tours`
  - `tour_locations`
  - `tour_schedules` neu can.

## 2026-06-03 - tours context enrichment

### Cong viec da lam

- Tao script `scripts/enrich_tour_context.py`.
- Muc dich: bo sung truong thieu theo ngu canh nhung khong ghi de du lieu crawl that.
- Input:
  - `data/tour-staging.json`
- Output:
  - `data/tour-staging-enriched.json`
  - `data/tour-staging-enriched-report.json`
  - `data/tour-review-enriched.json`
  - `data/tour-review-enriched.csv`
  - `data/tour-review-enriched-report.json`
- Cap nhat `scripts/build_tour_review.py` de xuat cot `inferred_fields`.
- Khong sua API/admin/web.
- Khong tao SQL seed.
- Khong publish DB.

### Nguyen tac enrichment

- Khong ghi de gia tri crawl that.
- Chi dien truong dang thieu.
- Moi truong suy luan duoc ghi vao `inferred_fields`.
- Moi gia tri suy luan co:
  - `confidence`
  - `method`
  - `basis`
  - `requires_manual_review = true`
- Ban enriched khong duoc xem la production-safe neu chua duyet thu cong.

### Ket qua

- Total tours: 36.
- Items with inferred fields: 4.
- Inferred field count: 5.
- Missing price sau enrichment: 0.
- Missing duration sau enrichment: 0.
- Missing itinerary van con: 17.
- Missing inclusions van con: 7.

### Truong da suy luan

- `Bach Ma National Park Tour From Da Nang`: estimated `price_adult = 1100000 VND`.
- `Hoa Phu Thanh waterfall sliding daily tour`: estimated `price_adult = 1150000 VND`, estimated `duration = 1 day`.
- `Son Tra Peninsula - Marble Mountains - Hoian Daily Tour`: estimated `price_adult = 1175000 VND`.
- `Cam Thanh Coconut Jungle Muslim Tour`: estimated `price_adult = 1225000 VND`.

### Viec tiep theo

- Duyet `data/tour-review-enriched.csv`.
- Neu chap nhan gia/duration suy luan thi chuyen `approve_for_seed = true`.
- Neu khong chap nhan, dien `reject_reason` hoac `fix_notes`.
- Chi tao seed tu record da approve.

## 2026-06-03 - tour location mapping review

### Cong viec da lam

- Doc migration `tour_locations`: bang pivot gom `tour_id`, `location_id`, `created_at`.
- Doc seed `05_locations.sql` de xac dinh cac location da co san:
  - `hoi-an-ancient-town` id hint 1.
  - `bay-mau-coconut-forest` id hint 3.
  - `my-son-sanctuary` id hint 8.
  - `cu-lao-cham` id hint 13.
  - `linh-ung-pagoda` id hint 20.
  - `marble-mountains` id hint 21.
  - `ba-na-hills` id hint 23.
- Tao script `scripts/build_tour_location_review.py`.
- Tao script `scripts/build_missing_location_candidates.py`.
- Chay mapping tu `data/tour-staging-enriched.json`.
- Khong sua API/admin/web.
- Khong tao SQL seed.
- Khong publish DB.

### Files da tao / cap nhat

- `data/tour-location-review.json`
- `data/tour-location-review.csv`
- `data/tour-location-review-report.json`
- `data/missing-location-candidates.json`
- `data/missing-location-candidates.csv`
- `data/missing-location-candidates-report.json`
- `scripts/build_tour_location_review.py`
- `scripts/build_missing_location_candidates.py`

### Ket qua mapping

- Tour count: 36.
- Mapping rows: 61.
- Rows map duoc vao location seed hien co: 44.
- Rows can tao location seed truoc: 15.
- Tour unmatched location: 2.
- Approved for seed mac dinh: 0.

### Missing location seed candidates

- `bach-ma-national-park`: 1 tour.
- `chan-may-port`: 3 tour.
- `hoa-phu-thanh`: 1 tour.
- `hue-imperial-city`: 4 tour.
- `nui-than-tai-hot-spring-park`: 1 tour.
- `tien-sa-port`: 5 tour.

### Tour chua map duoc location

- `The best quality Daily Group Tour package in Vietnam`
- `Vietnam Luxury Tour - Experience your trip with 5-star class`

Hai tour nay qua chung chung, nen reject hoac crawl detail hon truoc khi seed.

### Viec tiep theo

- Duyet `data/tour-location-review.csv`.
- Duyet `data/missing-location-candidates.csv`.
- Neu chap nhan missing location, tao seed location truoc.
- Sau khi co location id that va tour duoc approve, moi sinh seed `tour_locations`.

## 2026-06-03 - missing locations crawl

### Cong viec da lam

- Thu thap 6 location con thieu cho mapping `tour_locations`.
- Tao source config:
  - `data/missing_location_sources.json`
- Tao crawler:
  - `scripts/crawl_missing_locations.py`
- Chay crawler bang Python venv:
  - `.venv\Scripts\python.exe scripts\crawl_missing_locations.py --source-file data\missing_location_sources.json --output-prefix missing-locations --delay-ms 1200`
- Khong crawl anh.
- Khong sua API/admin/web.
- Khong tao SQL seed.
- Khong publish DB.

### Output

- `data/missing-locations-crawl.json`
- `data/missing-locations-review.json`
- `data/missing-locations-review.csv`
- `data/missing-locations-report.json`

### Ket qua

- Total locations: 6.
- From Nominatim/OpenStreetMap: 4.
- From curated fallback context: 2.
- With coordinates: 6.
- Pending review: 6.
- Approved for location seed: 0.

### Location da thu thap

- `bach-ma-national-park`
  - Source: Nominatim/OpenStreetMap.
  - Coordinates: 16.2157265, 107.8533926.
  - Review flag: `low_nominatim_importance`.
- `chan-may-port`
  - Source: Nominatim/OpenStreetMap.
  - Coordinates: 16.3240874, 108.0249266.
  - Review flag: `low_nominatim_importance`.
- `hoa-phu-thanh`
  - Source: curated fallback context.
  - Coordinates: 15.9998, 107.9834.
  - Reference URLs:
    - `https://hoiandaytrip.com/hoa-phu-thanh-tourist-area/`
    - `https://indanang.vn/en/listing/hoa-phu-thanh-tourist-area/`
  - Review flags:
    - `used_curated_fallback`
    - `manual_coordinate_review_required`
- `hue-imperial-city`
  - Source: Nominatim/OpenStreetMap.
  - Coordinates: 16.4689726, 107.5781266.
- `nui-than-tai-hot-spring-park`
  - Source: curated fallback context.
  - Coordinates: 15.9946, 107.9872.
  - Reference URLs:
    - `https://vietnamtourism.gov.vn/en/post/10543`
    - `https://www.originvietnam.com/destinations/nui-than-tai-hot-spring-park/`
  - Review flags:
    - `used_curated_fallback`
    - `manual_coordinate_review_required`
- `tien-sa-port`
  - Source: Nominatim/OpenStreetMap.
  - Coordinates: 16.119709, 108.2171737.
  - Review flag: `low_nominatim_importance`.

### Viec tiep theo

- Duyet `data/missing-locations-review.csv`.
- Neu chap nhan 6 location nay, tao SQL seed cho bang `locations` truoc.
- Sau khi seed `locations`, moi seed `tour_locations`.

## 2026-06-03 - tour schedules review

### Cong viec da lam

- Doc migration moi nhat cua bang `tour_schedules`.
- Schema can ho tro:
  - `tour_id`
  - `start_date`
  - `end_date`
  - `max_people`
  - `booked_people`
  - `price_adult`
  - `price_child`
  - `price_infant`
  - `status`
  - `booking_availability`
  - `departure_code`
  - `departure_place`
  - `booking_deadline`
- Tao script:
  - `scripts/build_tour_schedule_review.py`
- Input:
  - `data/tour-staging-enriched.json`
- Output:
  - `data/tour-schedule-review.json`
  - `data/tour-schedule-review.csv`
  - `data/tour-schedule-review-report.json`
- Khong sua API/admin/web.
- Khong tao SQL seed.
- Khong publish DB.

### Ket qua

- Tour count: 36.
- Schedule rows: 144.
- Date window:
  - start: `2026-06-04`.
  - days: 30.
- Schedules per tour: 4.
- Pending review: 144.
- Approved for seed: 0.
- Schedule patterns:
  - `daily`: 132 rows.
  - `weekend`: 12 rows.
- Start time sources:
  - `default`: 100 rows.
  - `rule`: 44 rows.
- Rows with review flags: 144.

### Nguyen tac

- Khong coi schedule nay la du lieu that 100%.
- Day la schedule staging/review de demo booking.
- `approve_for_seed` mac dinh la false.
- `start_time_source` giup phan biet:
  - `default`: mac dinh 08:00.
  - `rule`: suy luan theo tu khoa afternoon/night/half-day.
- Da bo parse gio tu itinerary/inclusions de tranh lay nham gio trong lich trinh.

### Viec tiep theo

- Duyet `data/tour-schedule-review.csv`.
- Chi approve schedule cua tour da duoc approve.
- Neu can seed DB, thu tu seed nen la:
  - `locations`
  - `tours`
  - `tour_locations`
  - `tour_schedules`

## 2026-06-03 - approved review decisions

### Cong viec da lam

- Tao script `scripts/apply_review_decisions.py`.
- Sinh file review da duyet rieng, khong ghi de file review goc.
- Khong tao SQL seed.
- Khong publish DB.
- Khong sua API/admin/web.

### Files da tao

- `data/approved-locations-review.json`
- `data/approved-locations-review.csv`
- `data/approved-tours-review.json`
- `data/approved-tours-review.csv`
- `data/approved-tour-locations-review.json`
- `data/approved-tour-locations-review.csv`
- `data/approved-tour-schedules-review.json`
- `data/approved-tour-schedules-review.csv`
- `data/approved-review-report.json`

### Ket qua duyet

- Locations:
  - total: 6.
  - approved: 4.
  - pending: 2.
  - rejected: 0.
- Tours:
  - total: 36.
  - approved: 34.
  - rejected: 2.
  - pending: 0.
- Tour locations:
  - total: 61.
  - approved: 57.
  - rejected: 2.
  - pending: 2.
- Tour schedules:
  - total: 144.
  - approved: 136.
  - rejected: 8.
  - pending: 0.

### Tour bi reject

- `The best quality Daily Group Tour package in Vietnam`
- `Vietnam Luxury Tour - Experience your trip with 5-star class`

Ly do: package chung chung, khong du cu the de seed thanh tour rieng.

### Location con pending

- `Hoa Phu Thanh`
- `Nui Than Tai Hot Spring Park`

Ly do: dung curated fallback coordinates, can manual coordinate review truoc khi approve location seed.

### Rule duyet

- Tour duoc approve neu co price, duration, image va khong phai generic package.
- Location duoc approve neu lay duoc tu Nominatim/OpenStreetMap va co coordinates.
- Tour-location duoc approve neu parent tour approved va location da co seed hoac missing location da approved.
- Schedule duoc approve neu parent tour approved.

### Viec tiep theo

- Neu muon tao seed, nen tao SQL seed theo thu tu:
  - `locations` cho 4 location approved.
  - `tours` cho 34 tour approved.
  - `tour_locations` cho 57 mapping approved.
  - `tour_schedules` cho 136 schedule approved.
- Rieng `Hoa Phu Thanh` va `Nui Than Tai Hot Spring Park` nen xac minh toa do truoc khi seed.

## 2026-06-03 - approved staging SQL seed

### Cong viec da lam

- Tao script `scripts/generate_approved_staging_seed.py`.
- Sinh SQL seed staging tu cac file `data/approved-*.json`.
- Khong apply SQL vao database.
- Khong sua API/admin/web.
- Da doi JSON literal sang `::json` de khop migration PostgreSQL hien tai.
- Da kiem tra nhanh SQL:
  - Khong con `;\nON CONFLICT`.
  - Khong con `::jsonb`.
  - Co 4 lenh `INSERT INTO` va 4 lenh `ON CONFLICT`.

### File da tao/cap nhat

- `D:\DATN\DATN_Tài liệu\database-seeders\20_approved_tour_staging_seed.sql`
- `data/approved-staging-seed-report.json`

### Ket qua seed staging

- New locations approved: 4.
- Tours approved: 34.
- Tour-location mappings approved: 57.
- Tour schedules approved: 136.

### Luu y chat luong du lieu

- Day la seed staging/demo, cac ban ghi dang de `pending_review` de admin duyet truoc khi public.
- Images hien la URL nguon crawl duoc, chua download thanh file local.
- 2 location con pending vi dung curated fallback coordinates:
  - `Hoa Phu Thanh`.
  - `Nui Than Tai Hot Spring Park`.
- 2 tour generic da bi reject:
  - `The best quality Daily Group Tour package in Vietnam`.
  - `Vietnam Luxury Tour - Experience your trip with 5-star class`.

### Bang tiep theo nen thu thap du lieu that

- `locations`: can mo rong du lieu dia diem that va anh dia diem hoat dong.
- `location_images`/`location amenities` neu schema/seed dang thieu anh va tien ich.
- `blog_posts`: can noi dung bai viet that neu app co man cam nang/blog.
- `promotions`: co the seed noi bo, khong bat buoc crawl that.
- `ratings`, `favorites`, `views`, `bookings`, `payments`, `cart_items`, `notifications`: nen seed demo/noi bo, khong crawl that.

## 2026-06-03 - overpass clean batch 1 approval seed

### Cong viec da lam

- Tao script `scripts/generate_overpass_location_approval_seed.py`.
- Sinh SQL approval batch 1 cho Overpass staging items.
- Khong publish vao production `locations`.
- Khong apply SQL vao database.
- Khong sua API/admin/web.

### Files da tao/cap nhat

- `D:\DATN\DATN_Tài liệu\database-seeders\21_approve_overpass_clean_batch1.sql`
- `data/overpass-approval-batch1-review.csv`
- `data/overpass-approval-batch1-report.json`
- Cap nhat `D:\DATN\DATN_Tài liệu\database-seeders\README.md`

### Rule duyet batch 1

- Chi approve item tu source `overpass-danang-pois`.
- Chi approve `entityType` trong:
  - `location`
  - `restaurant`
  - `hotel`
- Chi approve item:
  - `status = pending_review`
  - `reviewPriority = high`
  - co `imageUrls`
  - khong co `qualityReasons`
- SQL runtime van bo qua duplicate bang dieu kien `duplicate_source_id IS NULL`.

### Ket qua

- Approved candidates: 242.
- By entity:
  - hotel: 131.
  - location: 15.
  - restaurant: 96.
- Pending con lai: 338.
- Ly do pending chinh: `weak_address`.

### Thu tu chay SQL neu muon publish vao DB

1. `11_crawl_staging_tables.sql`
2. `12_overpass_danang_pois_seed.sql`
3. `13_overpass_quality_review_seed.sql`
4. `14_pexels_image_enrichment_seed.sql`
5. `15_crawl_duplicate_matching_seed.sql`
6. `21_approve_overpass_clean_batch1.sql`
7. `16_crawl_publish_approved_locations.sql`

Sau buoc 7, ban ghi publish vao `locations.status = inactive`, van can admin bat active truoc khi hien thi cong khai.

## 2026-06-03 - data center va blog guide crawl batch 3

### Cong viec da lam

- Tao data center trung tam tai `D:\DATN\DATN_Tài liệu\data-center`.
- Khong di chuyen file goc de tranh lam hong script crawler/seed dang dung duong dan hien tai.
- Data center la noi AI mo dau tien de doc inventory, thu tu seed va ke hoach thu thap tiep.
- Tao crawler text-only cho blog/travel guide: `scripts/crawl_blog_guides.py`.
- Tao source config: `data/blog_guide_sources.json`.
- Chay crawl bang venv.
- Khong tao anh.
- Khong sua API/admin/web.
- Khong apply SQL vao database.

### Files data center

- `D:\DATN\DATN_Tài liệu\data-center\README.md`
- `D:\DATN\DATN_Tài liệu\data-center\indexes\data-inventory.md`
- `D:\DATN\DATN_Tài liệu\data-center\indexes\seed-run-order.md`
- `D:\DATN\DATN_Tài liệu\data-center\indexes\next-collection-plan.md`
- `D:\DATN\DATN_Tài liệu\data-center\reports\collection-status-2026-06-03.md`

### Blog guide crawl batch 3

- Raw output: `data/blog-guides-batch3-raw.json`
- Normalized output: `data/blog-guides-batch3-normalized.json`
- Report: `data/blog-guides-batch3-report.json`
- Total sources: 9.
- Success: 9.
- Failures: 0.
- Status: all records `pending_review`.
- `featured_image`: null.

### Topics da thu thap

- Da Nang.
- Hoi An.
- Hue.
- 3 perfect days in Danang.
- Must-visit places in Da Nang.
- Ba Na Hills.
- Marble Mountains.
- My Son.
- Da Nang pork rolls / local food.

### Viec tiep theo

- Tao review CSV/SQL staging cho blog guide records.
- Sau khi duyet, quyet dinh thay the hoac bo sung `07_blog_posts.sql`.
- Tiep tuc xu ly 338 Overpass POI pending do `weak_address`.

## 2026-06-03 - blog guide crawl batch 4 va merge staging

### Cong viec da lam

- Them source config batch 4: `data/blog_guide_sources_batch4.json`.
- Chay crawler text-only cho Danang Fantasticity official sources.
- Cai tien `scripts/crawl_blog_guides.py`:
  - strip HTML trong text/meta.
  - loai boilerplate copyright/license/newsletter/gallery.
- Re-run batch 3 clean va batch 4 clean.
- Tao script merge: `scripts/merge_blog_guides.py`.
- Tao script review: `scripts/build_blog_guide_review.py`.
- Khong tao anh.
- Khong apply SQL vao database.
- Khong sua API/admin/web.

### Files moi/cap nhat

- `data/blog_guide_sources_batch4.json`
- `data/blog-guides-batch3-clean-raw.json`
- `data/blog-guides-batch3-clean-normalized.json`
- `data/blog-guides-batch3-clean-report.json`
- `data/blog-guides-batch4-clean-raw.json`
- `data/blog-guides-batch4-clean-normalized.json`
- `data/blog-guides-batch4-clean-report.json`
- `data/blog-guides-staging.json`
- `data/blog-guides-staging-report.json`
- `data/blog-guides-review.csv`
- `data/blog-guides-review.json`
- `data/blog-guides-review-report.json`
- Cap nhat `D:\DATN\DATN_Tài liệu\data-center\indexes\data-inventory.md`
- Cap nhat `D:\DATN\DATN_Tài liệu\data-center\reports\collection-status-2026-06-03.md`

### Ket qua

- Blog guide staging total: 16.
- Status: all `pending_review`.
- Records with review flags: 4.
- By category hint:
  - `am-thuc`: 1.
  - `bien`: 1.
  - `cam-nang-da-nang`: 3.
  - `cam-nang-hoi-an`: 1.
  - `cam-nang-hue`: 1.
  - `diem-den`: 7.
  - `lich-trinh`: 2.

### Chu de moi batch 4

- Hai Van Pass.
- Son Tra Peninsula.
- Da Nang Beaches.
- My Son Sanctuary.
- 3 perfect days in Danang.
- Da Nang mountain tourism.

### Viec tiep theo

- Duyet `data/blog-guides-review.csv`.
- Tao SQL seed rieng cho blog guide approved, khong ghi de `07_blog_posts.sql` cho den khi duyet xong.
- Hoac tiep tuc crawl blog batch 5 neu can them chu de am thuc/kinh nghiem/FAQ.

## 2026-06-03 - approved blog guide draft seed

### Cong viec da lam

- Tao script `scripts/generate_approved_blog_guide_seed.py`.
- Duyet tu dong blog guide theo rule an toan:
  - approve record khong co `review_flags`.
  - giu pending record co `redirected_source_url` hoac `deduped_slug`.
- Sinh SQL seed rieng, khong ghi de `07_blog_posts.sql`.
- Seed insert blog records voi `status = draft`, `published_at = NULL`.
- Seed khong tao anh, `featured_image = NULL`.
- Da sua generator de:
  - excerpt la text rewrite ngan.
  - content la draft rewrite ngan.
  - khong copy doan dai tu source.
  - output SQL la ASCII.
- Khong apply SQL vao database.
- Khong sua API/admin/web.

### Files moi/cap nhat

- `D:\DATN\DATN_Tài liệu\database-seeders\22_approved_blog_guides_seed.sql`
- `data/approved-blog-guides-review.csv`
- `data/approved-blog-guides-review.json`
- `data/pending-blog-guides-review.csv`
- `data/pending-blog-guides-review.json`
- `data/approved-blog-guides-seed-report.json`
- Cap nhat `D:\DATN\DATN_Tài liệu\database-seeders\README.md`
- Cap nhat data-center inventory, seed order va collection status report.

### Ket qua

- Blog guide staging total: 16.
- Approved for draft seed: 12.
- Pending: 4.
- Seed ID range: 201-212.
- Blog categories mapped:
  - `cam-nang-da-nang` -> 24.
  - `cam-nang-hoi-an` -> 22.
  - `cam-nang-hue` -> 23.
  - `lich-trinh` -> 5.
  - `diem-den` -> 3.
  - `bien` -> 64.
  - `am-thuc` -> 2.

### Pending blog records

- `My Son Sanctuary` - `redirected_source_url`.
- `3 perfect days in Danang` - `deduped_slug`, `redirected_source_url`.
- `Da Nang’s Mountain Tourism – A Return to Origin in the Truong Son Range` - `redirected_source_url`.
- `Hai Van Pass` legacy - `deduped_slug`.

### Viec tiep theo

- Neu can nhap DB: chay `22_approved_blog_guides_seed.sql` sau `03_tour_blog_categories.sql` va `04_users.sql`.
- Sau khi seed, admin/editor can bien tap 12 bai draft truoc khi chuyen `published`.
- Co the tiep tuc crawl batch 5 cho FAQ, am thuc, kinh nghiem di chuyen, thoi tiet/mua du lich.

## 2026-06-03 - blog practical guide crawl batch 5

### Cong viec da lam

- Tao source config batch 5: `data/blog_guide_sources_batch5.json`.
- Crawl practical guide/FAQ-like topics text-only.
- Merge batch 3 + batch 4 + batch 5 vao `data/blog-guides-staging.json`.
- Rebuild review CSV/JSON.
- Rebuild `22_approved_blog_guides_seed.sql`.
- Cap nhat category map cho:
  - `di-chuyen` -> blog category id 30.
  - `kinh-nghiem` -> blog category id 1.
  - `thoi-tiet` -> blog category id 11.
- SQL seed van la ASCII, rewrite ngan, status `draft`, khong tao anh.
- Khong apply SQL vao database.
- Khong sua API/admin/web.

### Files moi/cap nhat

- `data/blog_guide_sources_batch5.json`
- `data/blog-guides-batch5-clean-raw.json`
- `data/blog-guides-batch5-clean-normalized.json`
- `data/blog-guides-batch5-clean-report.json`
- `data/blog-guides-staging.json`
- `data/blog-guides-staging-report.json`
- `data/blog-guides-review.csv`
- `data/blog-guides-review.json`
- `data/blog-guides-review-report.json`
- `data/approved-blog-guides-review.csv`
- `data/approved-blog-guides-review.json`
- `data/pending-blog-guides-review.csv`
- `data/pending-blog-guides-review.json`
- `data/approved-blog-guides-seed-report.json`
- `D:\DATN\DATN_Tài liệu\database-seeders\22_approved_blog_guides_seed.sql`

### Ket qua

- Blog guide staging total: 23.
- Approved for draft seed: 18.
- Pending: 5.
- Batch 5 success: 7/7.
- Batch 5 topics:
  - airport/arrival transport.
  - transport within Vietnam.
  - plan your trip.
  - motorbiking Hoi An to Hue over Hai Van Pass.
  - Da Nang insider list.
  - Da Nang livable city/practical guide.
  - Da Nang weather page.

### Pending moi

- `Post` from `danangfantasticity-weather-da-nang` bi `missing_facts`, `low_text_volume`.

### Viec tiep theo

- Neu tiep tuc thu thap: nen crawl FAQ rieng tu nguon co cau hoi/tra loi ro rang hoac tao FAQ staging tu cac blog practical guides da co.
- Neu muon lam DB seed tiep: tao seed FAQ/landing content tu 18 blog draft sau khi bien tap.
- Con phan data lon tiep theo la xu ly 338 Overpass POI pending do `weak_address`.

## 2026-06-03 - overpass weak-address landmark approval batch 2

### Cong viec da lam

- Tao script `scripts/generate_overpass_weak_address_approval_seed.py`.
- Loc 338 Overpass pending `weak_address`, chi xu ly nhom `location`.
- Khong approve nha hang/khach san weak-address trong batch nay.
- Khong approve generic viewpoint/park nho/ten mo ho.
- Tao SQL approval batch 2 chi update staging `crawl_items.status = approved`.
- Khong publish vao production `locations`.
- Khong apply SQL vao database.
- Khong sua API/admin/web.

### Files moi/cap nhat

- `D:\DATN\DATN_Tài liệu\database-seeders\23_approve_overpass_weak_address_landmarks.sql`
- `data/overpass-approval-batch2-weak-address-review.csv`
- `data/overpass-approval-batch2-weak-address-report.json`
- Cap nhat `database-seeders/README.md`.
- Cap nhat data-center inventory, seed order va collection status report.

### Rule duyet batch 2

- Source: `overpass-danang-pois`.
- `entityType = location`.
- `qualityReasons = ['weak_address']`.
- Co image candidates.
- `qualityScore >= 88`.
- Ten nam trong allowlist landmark/du lich ro rang.
- SQL runtime van bo qua duplicate bang dieu kien `duplicate_source_id IS NULL`.

### Ket qua

- Candidate location weak-address: 165.
- Approved selected landmarks: 24.
- Pending location weak-address con lai: 141.
- Approved by category:
  - `check-in-noi-tieng`: 15.
  - `bao-tang-di-tich`: 3.
  - `cong-vien-nuoc`: 2.
  - `cong-vien-vuon-hoa`: 2.
  - `hang-dong-nui-non`: 2.

### Mot so approved landmarks

- Ngu Hanh Son.
- Cau Rong.
- Bai bien My Khe.
- Cau Vang.
- Deo Hai Van.
- Nui Son Tra.
- Sun World Ba Na Hills.
- Cau Tran Thi Ly.
- Bai tam Non Nuoc.
- Ban Co Peak.
- Bao tang Ho Chi Minh.
- Bao tang Quan khu 5.
- Cau Song Han.
- Cau Thuan Phuoc.
- Cong Vien APEC.
- Cong vien Bien Dong.

### Thu tu SQL neu muon publish location vao DB

1. `11_crawl_staging_tables.sql`
2. `12_overpass_danang_pois_seed.sql`
3. `13_overpass_quality_review_seed.sql`
4. `14_pexels_image_enrichment_seed.sql`
5. `15_crawl_duplicate_matching_seed.sql`
6. `21_approve_overpass_clean_batch1.sql`
7. `23_approve_overpass_weak_address_landmarks.sql`
8. `16_crawl_publish_approved_locations.sql`

Sau buoc 8, locations duoc publish voi `status = inactive`, van can admin active sau.

## 2026-06-03 - overpass weak-address service approval batch 3

### Cong viec da lam

- Tao script `scripts/generate_overpass_service_weak_address_approval_seed.py`.
- Xu ly nhom restaurant/hotel con `weak_address`.
- Chi approve record co it nhat 2 tin hieu van hanh/source:
  - `website`
  - `contact:website`
  - `phone`
  - `contact:phone`
  - `opening_hours`
  - `cuisine`
- Khong approve cac quan/cafe/hotel chi co ten va toa do.
- Tao SQL approval batch 3 chi update staging `crawl_items.status = approved`.
- Khong publish vao production `locations`.
- Khong apply SQL vao database.
- Khong sua API/admin/web.

### Files moi/cap nhat

- `D:\DATN\DATN_Tài liệu\database-seeders\24_approve_overpass_weak_address_services.sql`
- `data/overpass-approval-batch3-weak-address-services-review.csv`
- `data/overpass-approval-batch3-weak-address-services-report.json`
- Cap nhat `database-seeders/README.md`.
- Cap nhat data-center inventory, seed order va collection status report.

### Ket qua

- Candidate restaurant/hotel weak-address: 173.
- Approved: 11.
- Pending: 162.
- Approved by entity:
  - restaurant: 10.
  - hotel: 1.
- Approved by category:
  - `am-thuc-dia-phuong`: 9.
  - `ca-phe-tra-sua`: 1.
  - `khach-san-homestay`: 1.

### Approved services

- Lam Vien Restaurant.
- Monsieur Crepes.
- Suon Nuong Cao Boi.
- Babylon Steakgarden.
- LUNA pub.
- Tru Vu Tra Quan.
- Bun cha ca 109.
- Burger Bros.
- Quan Chay Hang Ngay.
- Xuan Toi.
- Mercure Hotels.

### Tong approval Overpass hien tai

- Batch 1 clean approval: 242.
- Batch 2 weak-address landmarks: 24.
- Batch 3 weak-address services: 11.
- Total approved candidates: 277.

### Thu tu SQL neu muon publish location vao DB

1. `11_crawl_staging_tables.sql`
2. `12_overpass_danang_pois_seed.sql`
3. `13_overpass_quality_review_seed.sql`
4. `14_pexels_image_enrichment_seed.sql`
5. `15_crawl_duplicate_matching_seed.sql`
6. `21_approve_overpass_clean_batch1.sql`
7. `23_approve_overpass_weak_address_landmarks.sql`
8. `24_approve_overpass_weak_address_services.sql`
9. `16_crawl_publish_approved_locations.sql`

Sau buoc 9, locations duoc publish voi `status = inactive`, van can admin active sau.

## 2026-06-03 - data readiness report

### Cong viec da lam

- Tao report tong hop trang thai du lieu:
  - `D:\DATN\DATN_Tài liệu\data-center\reports\data-readiness-report-2026-06-03.md`
- Cap nhat data-center README va next collection plan.
- Khong apply SQL vao database.
- Khong sua API/admin/web.

### Ket luan readiness

- Locations/POI:
  - Total approved staging candidates: 277.
  - Nen publish vao DB o `locations.status = inactive` neu muon review trong admin/app.
  - Khong nen auto active/public.
- Tours:
  - 34 tours, 57 mappings, 136 schedules da co seed staging.
  - Can admin review cac field inferred/default truoc khi ban that.
- Blog guides:
  - 23 source-backed records.
  - 18 approved draft seed.
  - Can editor rewrite/expand truoc khi publish.

### Viec tiep theo khuyen nghi

- Neu muon dua vao DB: chay SQL theo seed order trong `data-center/indexes/seed-run-order.md`.
- Neu tiep tuc thu thap: nen crawl FAQ-specific Q/A, khong can crawl them general guide luc nay.
- Neu muon nang chat luong location: review manual remaining weak-address POIs hoac xac minh bang source ngoai.

## 2026-06-03 - landing FAQ staging and seed

### Cong viec da lam

- Kiem tra schema va xac dinh khong co bang `faqs` rieng.
- Chon noi luu FAQ phu hop: `landing_pages.content_blocks`.
- Tao script `scripts/generate_landing_faq_seed.py`.
- Tao FAQ staging tu cac blog/travel guide source-backed da crawl.
- Sinh JSON/CSV review va SQL seed rieng.
- Khong tao anh.
- Khong apply SQL vao database.
- Khong sua API/admin/web.

### Files moi/cap nhat

- `data/landing-faq-staging.json`
- `data/landing-faq-review.csv`
- `data/landing-faq-report.json`
- `D:\DATN\DATN_Tài liệu\database-seeders\25_landing_faq_blocks_seed.sql`
- Cap nhat `database-seeders/README.md`.
- Cap nhat data-center inventory, seed order va readiness report.

### Ket qua

- Landing FAQ groups: 4.
- FAQ items: 14.
- Target landing pages:
  - `du-lich-da-nang`
  - `cam-nang-du-lich-mien-trung`
  - `tour-ba-na-hills`
  - `tour-son-tra-ngu-hanh-son`

### Luu y

- Seed `25_landing_faq_blocks_seed.sql` update `landing_pages.content_blocks`.
- Nen chay sau `18_landing_pages_seed.sql`.
- Noi dung FAQ la draft-review text, can editor/admin duyet truoc khi public.
- Seed output ASCII, text-only, co source_urls trong content_blocks.

## 2026-06-03 - database seed coverage cleanup

### Cong viec da lam

- Kiem tra lai migrations va `database-seeders` de tim bang con thieu seed.
- Tao SQL mirror cho `settings` de bo seed co the chay doc lap ngoai Laravel seeder.
- Tao seed demo tuy chon cho `cart_items` de test cart/checkout UI.
- Tao seed backfill taxonomy cho location da publish tu `crawl_items` sang `location_tags` va `location_amenities`.
- Cap nhat `database-seeders/README.md` voi thu tu seed moi.
- Khong apply SQL vao database.
- Khong sua API/admin/web.

### Files moi/cap nhat

- `D:\DATN\DATN_Tài liệu\database-seeders\19_settings_seed.sql`
- `D:\DATN\DATN_Tài liệu\database-seeders\26_cart_items_demo_seed.sql`
- `D:\DATN\DATN_Tài liệu\database-seeders\27_published_location_taxonomy_backfill.sql`
- `D:\DATN\DATN_Tài liệu\database-seeders\README.md`
- `D:\DATN\DATN_Tài liệu\danangtrip-crawler\memory.md`

### Thu tu chay khuyen nghi cho cac file moi

1. `19_settings_seed.sql` sau `18_landing_pages_seed.sql` hoac bat ky luc nao sau khi migration `settings` da chay.
2. `26_cart_items_demo_seed.sql` chi khi can test cart/checkout UI, sau `04_users.sql` va tour schedules.
3. `27_published_location_taxonomy_backfill.sql` sau khi da publish location crawl bang `16_crawl_publish_approved_locations.sql`.

### Luu y

- `cart_items` la behavior/test seed, khong phai du lieu crawl that.
- `27_published_location_taxonomy_backfill.sql` chi xu ly locations da co `crawl_items.published_entity_id`, nen khong tao du lieu moi trong `locations`.
- Mapping tag/amenity dung rule bao thu; admin van nen review filter UI sau khi seed.

## 2026-06-03 - read-only seed coverage check

### Cong viec da lam

- Tao SQL check read-only de kiem tra so dong tung bang sau khi chay seed.
- Them cac check relation quan trong:
  - published crawl locations thieu tags.
  - published crawl locations thieu amenities.
  - approved crawl items chua publish.
  - inactive published locations can admin active.
  - tours thieu schedule.
  - tours thieu location mapping.
- Cap nhat README va seed-run-order.
- Khong apply SQL vao database.
- Khong sua API/admin/web.

### File moi/cap nhat

- `D:\DATN\DATN_Tài liệu\database-seeders\28_seed_coverage_check.sql`
- `D:\DATN\DATN_Tài liệu\database-seeders\README.md`
- `D:\DATN\DATN_Tài liệu\data-center\indexes\seed-run-order.md`
- `D:\DATN\DATN_Tài liệu\danangtrip-crawler\memory.md`

### Cach dung

- Chay `28_seed_coverage_check.sql` sau khi da chay migration va cac seed can dung.
- Ket qua `missing_or_not_seeded` chi can xu ly voi bang nghiep vu; cac bang `optional_runtime` co the rong trong dev/test.

## 2026-06-04 - live DB coverage check

### Cong viec da lam

- Kiem tra live DB theo `.env` cua `D:\DATN\danangtrip-api`.
- DB dang tro toi Supabase remote:
  - `DB_CONNECTION=pgsql`
  - `DB_HOST=aws-1-ap-northeast-1.pooler.supabase.com`
  - `DB_DATABASE=postgres`
- Chay read-only:
  - `php artisan migrate:status`
  - `php artisan tinker --execute` voi cac query `SELECT count(*)`.
- Khong apply migration.
- Khong chay seed.
- Khong insert/update/delete.

### Ket qua chinh

- Tat ca migrations hien co deu `Ran`.
- `promotions`: 0 row.
- `landing_pages`: 0 row.
- Crawler staging tables chua ton tai tren DB:
  - `crawl_sources`
  - `crawl_jobs`
  - `crawl_items`
  - `crawl_logs`
- `tours_without_location_mapping`: 14.
- `blog_posts_without_category`: 33.
- `locations_without_tags`: 1.
- `locations_without_amenities`: 1.

### File report

- `D:\DATN\DATN_Tài liệu\data-center\reports\live-db-coverage-report-2026-06-04.md`

### Viec tiep theo

- Xac nhan DB remote co duoc phep ghi hay khong truoc khi apply seed.
- Neu duoc phep ghi, uu tien seed:
  - `17_promotions_seed.sql`
  - `18_landing_pages_seed.sql`
  - `25_landing_faq_blocks_seed.sql`
- Tao fix seed cho:
  - 14 tours thieu `tour_locations`.
  - 33 blog posts thieu category.
  - 1 location thieu tag/amenity.

## 2026-06-04 - live relation gap fix seed prepared

### Cong viec da lam

- Dung query read-only lay danh sach ban ghi thieu mapping tren live DB.
- Doi chieu voi seed/crawler data local da co.
- Khong crawl network them vi du lieu can thiet da co trong local crawl/review outputs.
- Tao seed fix relation rieng, chua apply vao DB.

### File moi/cap nhat

- `D:\DATN\DATN_Tài liệu\database-seeders\29_live_relation_gap_fix_seed.sql`
- `D:\DATN\DATN_Tài liệu\database-seeders\README.md`
- `D:\DATN\DATN_Tài liệu\data-center\reports\live-db-coverage-report-2026-06-04.md`
- `D:\DATN\DATN_Tài liệu\danangtrip-crawler\memory.md`

### Noi dung seed 29

- Them 10 destination locations thieu:
  - Hue Imperial City.
  - Lang Co Beach.
  - Hai Van Pass.
  - VinWonders Nam Hoi An.
  - Son Tra Peninsula.
  - Bach Ma National Park.
  - Tra Que Vegetable Village.
  - Tam Giang Lagoon.
  - Perfume River.
  - Han River.
- Them mapping `tour_locations` cho 14 tours thieu mapping.
- Them mapping `blog_post_categories` cho 32 bai viet that.
- Them tag/amenity cho `quan-bun-co-ha-`.

### Luu y

- Blog post `test-title-1143398745` khong duoc map category trong seed 29 vi la test content, can review/xoa rieng.
- Seed 29 chi insert missing rows voi `ON CONFLICT DO NOTHING`.
- Chua apply seed vao Supabase/live DB.

## 2026-06-04 - live DB seed fixes applied

### Cong viec da lam

- Sau khi user duyet, apply seed vao Supabase DB dang cau hinh trong `.env`.
- Apply:
  - `17_promotions_seed.sql`
  - `18_landing_pages_seed.sql`
  - `25_landing_faq_blocks_seed.sql`
  - `29_live_relation_gap_fix_seed.sql`
  - `30_live_relation_gap_fix_followup_seed.sql`
  - `31_archive_test_blog_posts_seed.sql`
- Chay coverage read-only sau apply.

### Ket qua cuoi

- `promotions`: 10.
- `landing_pages`: 5.
- `tours_without_schedule`: 0.
- `tours_without_location_mapping`: 0.
- `locations_without_tags`: 0.
- `locations_without_amenities`: 0.
- `published_blog_posts_without_category`: 0.
- `all_blog_posts_without_category`: 1.
- `archived_test_posts`: 1.
- `locations`: 111.
- `tour_locations`: 192.
- `blog_post_categories`: 119.
- `location_tags`: 245.
- `location_amenities`: 301.

### Luu y

- Ban ghi blog duy nhat con thieu category la `test-title-1143398745`, da chuyen sang `archived`.
- Crawler staging tables van chua apply vao Supabase DB:
  - `crawl_sources`
  - `crawl_jobs`
  - `crawl_items`
  - `crawl_logs`
- PHP local van can cai/bat extension `intl` neu muon dung `php artisan db:show --counts`.
- PHP local dang canh bao thieu `imagick`, khong anh huong cac query DB vua chay.

## 2026-06-04 - crawler staging applied to live DB

### Cong viec da lam

- Sau khi user duyet, apply crawler staging vao Supabase DB dang cau hinh.
- Apply:
  - `11_crawl_staging_tables.sql`
  - `12_overpass_danang_pois_seed.sql`
  - `13_overpass_quality_review_seed.sql`
  - `15_crawl_duplicate_matching_seed.sql`
  - `21_approve_overpass_clean_batch1.sql`
  - `23_approve_overpass_weak_address_landmarks.sql`
  - `24_approve_overpass_weak_address_services.sql`
- Khong apply:
  - `14_pexels_image_enrichment_seed.sql`
  - `16_crawl_publish_approved_locations.sql`
  - `27_published_location_taxonomy_backfill.sql`
- Khong publish them vao production `locations`.

### Sua loi seed truoc khi apply

- `12_overpass_danang_pois_seed.sql` bi thieu gia tri cho `created_at`, `updated_at` trong `INSERT INTO crawl_items`.
- Da sua co hoc 942 dong `pending_review AS status` de them:
  - `NOW() AS created_at`
  - `NOW() AS updated_at`
- `21_approve_overpass_clean_batch1.sql`, `23_approve_overpass_weak_address_landmarks.sql`, `24_approve_overpass_weak_address_services.sql` bi loi PostgreSQL `UPDATE ... FROM` khi tham chieu target table trong `JOIN ON`.
- Da sua thanh `FROM source_row s, approved_external_ids a` va dua `a.external_id = ci.external_id` xuong `WHERE`.

### Ket qua cuoi

- `crawl_sources`: 1.
- `crawl_jobs`: 1.
- `crawl_items`: 942.
- `crawl_logs`: 6.
- Status split:
  - `approved`: 222.
  - `pending_review`: 360.
  - `rejected`: 360.
- Entity split:
  - `hotel`: 241.
  - `location`: 218.
  - `restaurant`: 483.

### Public DB van sach

- `promotions`: 10.
- `landing_pages`: 5.
- `tours_without_location_mapping`: 0.
- `locations_without_tags`: 0.
- `locations_without_amenities`: 0.
- `published_blog_posts_without_category`: 0.

### Luu y

- Approved crawl records van nam trong staging, chua publish.
- Neu muon dua approved staging sang `locations`, can chay `16_crawl_publish_approved_locations.sql` sau khi admin review lai.
- Vi khong apply `14_pexels_image_enrichment_seed.sql`, staging approved count thap hon report offline co image candidates.

## 2026-06-04 - approved crawl items published inactive

### Cong viec da lam

- Sau khi user duyet, publish `crawl_items.status = approved` sang production `locations`.
- Apply:
  - `16_crawl_publish_approved_locations.sql`
  - `27_published_location_taxonomy_backfill.sql`
  - `32_published_location_minimum_amenity_backfill.sql`
- Khong apply:
  - `14_pexels_image_enrichment_seed.sql`
- Khong auto active location moi.

### Ket qua cuoi

- `locations_total`: 333.
- `locations_active`: 111.
- `locations_inactive`: 222.
- `crawl_items_published`: 222.
- `crawl_items_pending_review`: 360.
- `crawl_items_rejected`: 360.
- `published_locations_without_tags`: 0.
- `published_locations_without_amenities`: 0.
- `tours_without_location_mapping`: 0.
- `published_blog_posts_without_category`: 0.
- `location_tags`: 721.
- `location_amenities`: 676.

### Luu y

- 222 location moi tu crawl dang `inactive`, can admin review/active thu cong truoc khi public.
- Vi khong apply Pexels enrichment, nhieu location crawl moi co the chua co image candidates.
- Seed `32_published_location_minimum_amenity_backfill.sql` duoc tao de dam bao UI filter khong gap location published thieu amenity.

## 2026-06-04 - final taxonomy cleanup

### Cong viec da lam

- Kiem tra lai DB sau publish.
- Phat hien 2 location inactive HanCook con thieu tag/amenity:
  - `nha-hang-hancook-crawl-215`.
  - `nha-hang-hancook-crawl-216`.
- Tao va apply `33_hancook_location_taxonomy_fix.sql`.
- Khong active, khong xoa 2 location nay.

### Ket qua cuoi

- `locations_total`: 333.
- `locations_active`: 111.
- `locations_inactive`: 222.
- `locations_without_tags`: 0.
- `locations_without_amenities`: 0.
- `tours_without_schedule`: 0.
- `tours_without_location_mapping`: 0.
- `published_blog_posts_without_category`: 0.
- `promotions`: 10.
- `landing_pages`: 5.
- `crawl_items`: 942.
- `crawl_published`: 222.
- `crawl_pending_review`: 360.
- `crawl_rejected`: 360.

### Viec con lai khong phai thieu DB

- Admin review 222 `inactive` locations va quyet dinh active/reject/merge duplicate.
- Review 360 `pending_review` crawl_items neu muon tiep tuc publish them.
- Chua apply `14_pexels_image_enrichment_seed.sql`, nen anh Pexels candidate van khong co trong live DB.

## 2026-06-04 - admin review audit

### Cong viec da lam

- Kiem tra lai phan con lai sau khi database relation da sach.
- Xac dinh 222 `locations.status = inactive` deu chua co thumbnail.
- Xac dinh duplicate signal trong inactive locations:
  - `nha hang hancook`: 3 rows.
- Xac dinh 360 `crawl_items.status = pending_review` con can review.
- Tao report next steps cho admin.

### File moi

- `D:\DATN\DATN_Tài liệu\data-center\reports\admin-review-next-steps-2026-06-04.md`

### Ket luan

- DB khong con thieu schema/seed/relation chinh.
- Viec con lai la admin review/activation/image/duplicate workflow.
- Khong nen bulk active 222 inactive locations vi 0/222 co thumbnail va co duplicate signal.

## 2026-06-04 - inactive location review export and quality standard

### Cong viec da lam

- Xuat CSV review cho 222 `locations.status = inactive`.
- File CSV moi:
  - `D:\DATN\DATN_Tài liệu\data-center\reports\inactive-locations-review-2026-06-04.csv`
- Tao tai lieu chuan chat luong data:
  - `D:\DATN\DATN_Tài liệu\data-center\reports\db-data-quality-standard-2026-06-04.md`

### Ket luan

- De DB that chuan, khong nen crawl them ngay.
- Nen review 222 inactive locations theo CSV, xu ly duplicate, anh, source, category roi moi active.
- `pending_review` crawl items chi nen publish theo batch nho sau khi duyet.

## 2026-06-04 - media asset download for Cloudinary staging

### Cong viec da lam

- Tao script:
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\scripts\export_media_assets.py`
- Tao naming standard:
  - `D:\DATN\DATN_Tài liệu\data-center\reports\media-asset-naming-standard-2026-06-04.md`
- Export DB published inactive locations:
  - `D:\DATN\DATN_Tài liệu\data-center\media-assets\db-published-locations.json`
- Tai anh Pexels candidate batch 1:
  - target: 222 `locations.status = inactive`.
  - photos per location: 1.
  - downloaded: 222.
  - failed: 0.
  - total size: about 85.6 MB.
- Tao Cloudinary prep doc:
  - `D:\DATN\DATN_Tài liệu\data-center\reports\cloudinary-upload-prep-2026-06-04.md`

### Folder asset

- `D:\DATN\DATN_Tài liệu\data-center\media-assets\cloudinary-staging\locations\2026-06-04-overpass-published-inactive`

### Files quan trong

- `originals\`: anh da tai.
- `manifest.csv`: map anh voi DB/source/cloudinary_public_id.
- `manifest.json`: manifest may doc.
- `summary.json`: ket qua download.

### Naming convention

- Local file:
  - `loc-{location_id}__{location_slug}__{external_id}__p01__pexels-{photo_id}.jpg`
- Cloudinary public ID:
  - `danangtrip/locations/{location_slug}/loc-{location_id}__{location_slug}__p01`

### Cloudinary upload va DB image update - 2026-06-04

- Da upload 222/222 anh Pexels candidate len Cloudinary.
- Upload result parts:
  - `upload-results-part-001.csv/json`: 50 uploaded, 0 failed.
  - `upload-results-part-002.csv/json`: 50 uploaded, 0 failed.
  - `upload-results-part-003.csv/json`: 50 uploaded, 0 failed.
  - `upload-results-part-004.csv/json`: 50 uploaded, 0 failed.
  - `upload-results-part-005.csv/json`: 22 uploaded, 0 failed.
- Da merge thanh:
  - `upload-results.csv`: 222 rows, 222 uploaded, 0 failed.
  - `upload-results.json`: 222 rows.
- Da tao va apply seed:
  - `D:\DATN\DATN_Tài liệu\database-seeders\34_update_location_images_from_cloudinary_seed.sql`
  - `D:\DATN\DATN_Tài liệu\database-seeders\35_hancook_duplicate_location_images_fix.sql`
- Ket qua DB sau apply:
  - `locations.total`: 333.
  - `locations.active`: 111.
  - `locations.inactive`: 222.
  - `locations.thumbnail` Cloudinary total: 224.
  - `inactive locations with Cloudinary thumbnail`: 222/222.
  - `inactive locations missing thumbnail`: 0.

### Luu y

- Anh da co Cloudinary URL va da map vao `locations.thumbnail` / `locations.images` cho toan bo 222 inactive locations.
- `id 237` va `id 238` la duplicate HanCook crawl rows, da dung chung anh Cloudinary cua `id 236`.
- Can review chat luong anh theo tung place trong admin/web vi Pexels candidates co the dung theo category/Da Nang nhung khong chac dung 100% tung dia diem.

### Active location image completion - 2026-06-04

- Van de phat hien:
  - `active locations`: 111.
  - `active locations missing thumbnail`: 109.
- Da export 109 active locations thieu thumbnail:
  - `D:\DATN\DATN_Tài liệu\data-center\media-assets\db-active-missing-thumbnail-locations.json`
- Da them script:
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\scripts\export_active_location_media_assets.py`
- Da tai anh Pexels candidate:
  - output: `D:\DATN\DATN_Tài liệu\data-center\media-assets\cloudinary-staging\locations\2026-06-04-active-missing-thumbnail`
  - found: 109/109.
  - downloaded: 109/109.
  - failed: 0.
- Da upload Cloudinary:
  - unique uploaded locations: 109/109.
  - location `34` upload loi do Cloudinary context co ky tu emoji trong photographer; da sanitize context trong `upload_cloudinary_assets.py` va retry thanh cong.
- Da tao va apply seed:
  - `D:\DATN\DATN_Tài liệu\database-seeders\36_update_active_location_images_from_cloudinary_seed.sql`
- Ket qua DB sau apply:
  - `locations`: 333.
  - `active`: 111.
  - `inactive`: 222.
  - `locations_missing_thumbnail`: 0.
  - `active_missing_thumbnail`: 0.
  - `inactive_missing_thumbnail`: 0.
  - `active_cloudinary_thumbnail`: 111/111.
  - `inactive_cloudinary_thumbnail`: 222/222.
- Report moi:
  - `D:\DATN\DATN_Tài liệu\data-center\reports\db-completion-next-steps-2026-06-04.md`

### Inactive location activation batch 1 - 2026-06-04

- Da audit 222 inactive locations:
  - input: `D:\DATN\DATN_Tài liệu\data-center\reports\inactive-locations-quality-input-2026-06-04.json`
  - quality CSV: `D:\DATN\DATN_Tài liệu\data-center\reports\inactive-locations-quality-review-2026-06-04.csv`
- Da tao activation batch 1:
  - CSV: `D:\DATN\DATN_Tài liệu\data-center\reports\inactive-locations-activate-batch1-2026-06-04.csv`
  - seed: `D:\DATN\DATN_Tài liệu\database-seeders\37_activate_curated_inactive_locations_batch1.sql`
- Tieu chi batch 1:
  - activate non-lodging categories: `am-thuc-dia-phuong`, `ca-phe-tra-sua`, `check-in-noi-tieng`, `bao-tang-di-tich`, `cong-vien-vuon-hoa`, `cong-vien-nuoc`, `hang-dong-nui-non`.
  - excluded: `khach-san-homestay`, duplicate HanCook rows, manual-review rows.
- Da apply seed `37`: active tang tu 111 len 222.
- Phat hien duplicate active `Memory Lounge`:
  - kept curated row `id=96`, `slug=memory-lounge-danang`, active.
  - deactivated crawl duplicate `id=221`, `slug=memory-lounge`.
  - seed: `D:\DATN\DATN_Tài liệu\database-seeders\38_deactivate_memory_lounge_crawl_duplicate.sql`
- Final sau batch 1:
  - `locations.total`: 333.
  - `locations.active`: 221.
  - `locations.inactive`: 112.
  - `active_missing_thumbnail`: 0.
  - `inactive_missing_thumbnail`: 0.
  - `active_duplicate_lower_name_groups`: 0.
  - `inactive_duplicate_lower_name_groups`: 1.
- Report:
  - `D:\DATN\DATN_Tài liệu\data-center\reports\inactive-location-activation-batch1-2026-06-04.md`

### Tour quality completion - 2026-06-04

- Da audit 100 tours:
  - input: `D:\DATN\DATN_Tài liệu\data-center\reports\tours-quality-input-2026-06-04.json`
  - sample: `D:\DATN\DATN_Tài liệu\data-center\reports\tours-quality-sample-2026-06-04.json`
- Van de ban dau:
  - `missing_start_time`: 80.
  - `missing_meeting_point`: 80.
  - `missing_thumbnail`: 100.
  - `missing_or_empty_itinerary`: 93.
  - `missing_or_empty_inclusions`: 80.
  - `missing_or_empty_exclusions`: 80.
  - `missing_or_empty_images`: 100.
  - `missing_or_zero_price_infant`: 25.
- Da them scripts:
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\scripts\generate_tour_quality_seed.py`
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\scripts\export_tour_media_assets.py`
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\scripts\generate_tour_image_update_seed.py`
- Da tao va apply seeds:
  - `D:\DATN\DATN_Tài liệu\database-seeders\39_tour_content_quality_backfill_seed.sql`
  - `D:\DATN\DATN_Tài liệu\database-seeders\40_update_tour_images_from_cloudinary_seed.sql`
- Tour media:
  - folder: `D:\DATN\DATN_Tài liệu\data-center\media-assets\cloudinary-staging\tours\2026-06-04-tour-missing-thumbnail`
  - downloaded: 100/100.
  - uploaded Cloudinary: 100/100.
- Final audit:
  - `tours_total`: 100.
  - `missing_description`: 0.
  - `missing_short_desc`: 0.
  - `missing_duration`: 0.
  - `missing_start_time`: 0.
  - `missing_meeting_point`: 0.
  - `missing_thumbnail`: 0.
  - `missing_or_empty_itinerary`: 0.
  - `missing_or_empty_inclusions`: 0.
  - `missing_or_empty_exclusions`: 0.
  - `missing_or_empty_images`: 0.
  - `missing_or_zero_price_adult`: 0.
  - `missing_or_zero_price_child`: 0.
  - `missing_or_zero_price_infant`: 0.
  - `missing_or_zero_max_people`: 0.
  - `missing_or_zero_min_people`: 0.
  - `without_schedule`: 0.
  - `without_location_mapping`: 0.
  - `missing_cloudinary_thumbnail`: 0.
- Report:
  - `D:\DATN\DATN_Tài liệu\data-center\reports\tour-quality-completion-2026-06-04.md`
- Luu y:
  - Mot so tour co slug generic `tour-real-variant-*`; du lieu da du field va anh nhung nen review/rename truoc demo production neu hien thi public.

### Database system audit and one-command seed runner - 2026-06-05

- Da tao manifest va script mot lenh:
  - `D:\DATN\DATN_Tài liệu\database-seeders\seed-manifest.json`
  - `D:\DATN\DATN_Tài liệu\database-seeders\apply_database_seeders.ps1`
  - `D:\DATN\DATN_Tài liệu\database-seeders\audit_database_quality.ps1`
  - `D:\DATN\DATN_Tài liệu\database-seeders\audit_database_quality.php`
- Lenh audit DB:
  - `powershell -ExecutionPolicy Bypass -File "D:\DATN\DATN_Tài liệu\database-seeders\audit_database_quality.ps1"`
- Lenh cap nhat DB hien tai bang seed backfill moi:
  - `powershell -ExecutionPolicy Bypass -File "D:\DATN\DATN_Tài liệu\database-seeders\apply_database_seeders.ps1" -Mode Incremental`
- Lenh khoi tao DB moi sau migration/fresh schema:
  - `powershell -ExecutionPolicy Bypass -File "D:\DATN\DATN_Tài liệu\database-seeders\apply_database_seeders.ps1" -Mode Full`
- Da test thanh cong:
  - `audit_database_quality.ps1`
  - `apply_database_seeders.ps1 -Mode Check`
- Live DB audit 2026-06-05:
  - `locations`: 333.
  - `locations_active`: 221.
  - `locations_inactive`: 112.
  - `locations_missing_thumbnail`: 0.
  - `active_location_duplicate_lower_name_groups`: 0.
  - `tours`: 100.
  - `tours_missing_cloudinary_thumbnail`: 0.
  - `tours_missing_or_empty_itinerary`: 0.
  - `tours_missing_or_empty_inclusions`: 0.
  - `tours_missing_or_empty_exclusions`: 0.
  - `tours_missing_or_empty_images`: 0.
  - `tours_without_schedule`: 0.
  - `tours_without_location_mapping`: 0.
  - `blog_posts`: 105.
  - `published_blog_missing_featured_image`: 102.
  - `crawl_pending_review`: 360.
  - `crawl_published`: 222.
  - `crawl_rejected`: 360.
- Con thieu chinh:
  - 360 crawl items con `pending_review`.
  - 112 inactive locations con review queue.
- Report:
  - `D:\DATN\DATN_Tài liệu\data-center\reports\database-system-audit-2026-06-05.md`

### Blog featured image completion - 2026-06-05

- Da xu ly gap blog media:
  - exported: `D:\DATN\DATN_Tài liệu\data-center\reports\blog-posts-missing-featured-image-2026-06-05.json`
  - media folder: `D:\DATN\DATN_Tài liệu\data-center\media-assets\cloudinary-staging\blogs\2026-06-05-blog-missing-featured-image`
  - downloaded: 102/102.
  - uploaded Cloudinary: 102/102.
- Da them scripts:
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\scripts\export_blog_media_assets.py`
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\scripts\generate_blog_image_update_seed.py`
- Da tao va apply seed:
  - `D:\DATN\DATN_Tài liệu\database-seeders\41_update_blog_featured_images_from_cloudinary_seed.sql`
- Da cap nhat:
  - `D:\DATN\DATN_Tài liệu\database-seeders\seed-manifest.json`
  - `D:\DATN\DATN_Tài liệu\database-seeders\README.md`
  - `D:\DATN\DATN_Tài liệu\data-center\reports\database-system-audit-2026-06-05.md`
- Final audit blog:
  - `blog_posts`: 105.
  - `blog_missing_excerpt`: 0.
  - `blog_missing_content`: 0.
  - `blog_missing_featured_image`: 0.
  - `published_blog_missing_featured_image`: 0.
- Report:
  - `D:\DATN\DATN_Tài liệu\data-center\reports\blog-featured-image-completion-2026-06-05.md`
- Con lai khong phai gap media/content bat buoc:
  - `crawl_pending_review`: 360.
  - `locations_inactive`: 112.

### Inactive locations review queue audit - 2026-06-05

- Da export 112 inactive locations:
  - `D:\DATN\DATN_Tài liệu\data-center\reports\inactive-locations-review-input-2026-06-05.json`
- Da export all location names de check duplicate voi active:
  - `D:\DATN\DATN_Tài liệu\data-center\reports\all-location-names-for-duplicate-check-2026-06-05.json`
- Da tao review queue:
  - `D:\DATN\DATN_Tài liệu\data-center\reports\inactive-locations-review-2026-06-05.csv`
  - `D:\DATN\DATN_Tài liệu\data-center\reports\inactive-locations-review-2026-06-05.json`
- Ket qua:
  - `manual_lodging_review`: 107.
  - `duplicate_keep_inactive`: 4.
  - `hold`: 1.
  - `activate_candidate`: 0.
- Khong tao/apply seed activate nao.
- Ly do:
  - `Memory Lounge` id `221` trong inactive la duplicate cua active curated row id `96`.
  - Phan lon con lai la `khach-san-homestay`/lodging can review thu cong truoc khi public.
  - HanCook rows van la duplicate/manual-review.
- Report:
  - `D:\DATN\DATN_Tài liệu\data-center\reports\inactive-location-review-queue-2026-06-05.md`

### Crawl pending review audit - 2026-06-05

- Da export 360 crawl_items pending_review:
  - `D:\DATN\DATN_Tài liệu\data-center\reports\crawl-items-pending-review-input-2026-06-05.json`
  - sample: `D:\DATN\DATN_Tài liệu\data-center\reports\crawl-items-pending-review-sample-2026-06-05.json`
- Da tao review CSV/JSON:
  - `D:\DATN\DATN_Tài liệu\data-center\reports\crawl-items-pending-review-2026-06-05.csv`
  - `D:\DATN\DATN_Tài liệu\data-center\reports\crawl-items-pending-review-2026-06-05.json`
- Initial classification:
  - `manual_review`: 258.
  - `duplicate_reject_or_link`: 102.
- Reason counters:
  - `missing_image_candidate`: 360.
  - `weak_address`: 309.
  - `duplicate_match`: 102.
  - `lodging_manual_review`: 73.
- Da tao va apply seed:
  - `D:\DATN\DATN_Tài liệu\database-seeders\42_reject_duplicate_pending_crawl_items.sql`
- Seed 42:
  - chuyen pending rows co `duplicate_source_id IS NOT NULL` sang `rejected`.
  - khong delete data.
  - khong publish tu dong.
- Final crawl state:
  - `crawl_items`: 942.
  - `crawl_pending_review`: 258.
  - `crawl_published`: 222.
  - `crawl_rejected`: 462.
- Da cap nhat:
  - `D:\DATN\DATN_Tài liệu\database-seeders\seed-manifest.json`
  - `D:\DATN\DATN_Tài liệu\database-seeders\README.md`
  - `D:\DATN\DATN_Tài liệu\data-center\reports\database-system-audit-2026-06-05.md`
- Report:
  - `D:\DATN\DATN_Tài liệu\data-center\reports\crawl-pending-review-audit-2026-06-05.md`
- Con lai:
  - 258 pending rows deu thieu image candidate, nhieu row weak address; khong nen auto publish.

### Tour generic slug polish - 2026-06-05

- Da audit 80 tours co slug `tour-real-variant-*`:
  - `D:\DATN\DATN_Tài liệu\data-center\reports\generic-tour-slugs-input-2026-06-05.json`
- Da them generator:
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\scripts\generate_tour_slug_polish_seed.py`
- Da tao review mapping:
  - `D:\DATN\DATN_Tài liệu\data-center\reports\generic-tour-slugs-polish-2026-06-05.json`
- Da tao va apply seed:
  - `D:\DATN\DATN_Tài liệu\database-seeders\43_polish_generic_tour_slugs_seed.sql`
- Thay doi:
  - xoa lap wording nhu `Tour Kham Pha Tour ...`.
  - thay slug `tour-real-variant-*` bang slug SEO theo ten.
  - giu nguyen price, schedule, location mappings, content va media.
- Final audit:
  - `tours_total`: 100.
  - `generic_slug_tours`: 0.
  - `variant_name_tours`: 0.
  - `duplicate_slug_groups`: 0.
  - `missing_thumbnail`: 0.
  - `without_schedule`: 0.
  - `without_location_mapping`: 0.
- Da cap nhat:
  - `D:\DATN\DATN_Tài liệu\database-seeders\seed-manifest.json`
  - `D:\DATN\DATN_Tài liệu\database-seeders\README.md`
- Report:
  - `D:\DATN\DATN_Tài liệu\data-center\reports\tour-slug-polish-completion-2026-06-05.md`

### Full database data sufficiency audit - 2026-06-05

- Da audit toan bo 44 bang live DB.
- Scripts:
  - `D:\DATN\DATN_Tài liệu\database-seeders\audit_all_table_counts.php`
  - `D:\DATN\DATN_Tài liệu\database-seeders\audit_database_completeness.php`
  - `D:\DATN\DATN_Tài liệu\database-seeders\audit_database_coverage.php`
- Ket luan:
  - du data cho DATN/demo va flow web/admin/API.
  - chua phai production-clean DB.
- Public content:
  - locations: 333 total, 221 active, missing thumbnail 0, active duplicate 0.
  - tours: 100, missing content/media/relation 0.
  - blogs: 104 published, missing content/media 0.
  - promotions active usable: 8.
  - landing pages: 5.
- Master data usage:
  - location categories: 100 total, 11 used, 89 unused.
  - subcategories: 100 total, 0 used.
  - tour categories: 100 total, 7 used, 93 unused.
  - blog categories: 101 total, 24 used, 77 unused.
- Tour schedule gaps:
  - total: 300.
  - future available: 158.
  - past still available: 142.
  - missing departure_code: 300.
  - missing departure_place: 300.
- Runtime/test cleanup gaps:
  - failed_jobs: 100.
  - job_batches: 100.
  - cache_locks: 100.
  - password_reset_tokens: 100 expired.
- Engagement:
  - ratings: 97.
  - locations with ratings: 35/333.
  - tours with ratings: 41/100.
- Report:
  - `D:\DATN\DATN_Tài liệu\data-center\reports\full-database-data-sufficiency-audit-2026-06-05.md`
- Next priority:
  - fix tour schedule departure metadata/past status.
  - clean runtime/test tables.

### Tour schedule operational backfill - 2026-06-05

- Da tao va apply seed:
  - `D:\DATN\DATN_Tài liệu\database-seeders\44_tour_schedule_operational_backfill.sql`
- Da chuan hoa toan bo 300 lich khoi hanh:
  - `departure_code`: `DNT-YYYYMMDD-T{tour_id}-S{schedule_id}`.
  - `departure_place`: lay tu `tours.meeting_point`, fallback `Trung tam Da Nang`.
  - `booking_deadline`: 12 gio truoc thoi diem khoi hanh.
  - lich qua khu giu `status=available` theo enum hien tai, nhung chuyen `booking_availability=sold_out`.
  - lich da du suc chua chuyen `booking_availability=sold_out`.
- Final audit:
  - total: 300.
  - missing departure code/place/deadline: 0.
  - duplicate departure code groups: 0.
  - past open booking: 0.
  - past sold out booking: 142.
  - future open booking: 156.
  - deadline not before departure: 0.
- Da cap nhat:
  - `D:\DATN\DATN_Tài liệu\database-seeders\seed-manifest.json`
  - `D:\DATN\DATN_Tài liệu\database-seeders\README.md`
  - `D:\DATN\DATN_Tài liệu\database-seeders\audit_database_completeness.php`
- Report:
  - `D:\DATN\DATN_Tài liệu\data-center\reports\tour-schedule-operational-backfill-2026-06-05.md`
- Next priority:
  - don du lieu runtime/test sau khi duoc phe duyet rieng vi thao tac co xoa du lieu.

### Runtime data cleanup - 2026-06-05

- Da backup truoc khi xoa:
  - `D:\DATN\DATN_Tài liệu\data-center\backups\runtime-cleanup-backup-20260605-142727.json`
- Da tao va apply:
  - `D:\DATN\DATN_Tài liệu\database-seeders\45_cleanup_stale_runtime_data.sql`
- Ket qua:
  - `failed_jobs`: 100 -> 0.
  - `job_batches`: 100 -> 0.
  - `cache_locks`: 100 -> 0.
  - `password_reset_tokens`: 100 -> 0.
- Khong xoa:
  - `sessions`: 101.
  - `refresh_tokens`: 168, expired: 0.
  - booking, payment va business data.
- Audit:
  - `D:\DATN\DATN_Tài liệu\database-seeders\audit_runtime_cleanup.php`
- Report:
  - `D:\DATN\DATN_Tài liệu\data-center\reports\runtime-data-cleanup-2026-06-05.md`
- Next priority:
  - kiem tra 34 bookings khong co payment record.
  - quyet dinh integrate subcategories hay archive master categories khong dung.

### Booking-payment integrity backfill - 2026-06-05

- Initial audit:
  - bookings without payment: 34.
  - valid cancelled/unpaid: 11.
  - valid pending without payment attempt: 14.
  - invalid completed/pending without payment: 9.
- Da backup:
  - `D:\DATN\DATN_Tài liệu\data-center\backups\booking-payment-backfill-20260605-145913.json`
- Da tao va apply:
  - `D:\DATN\DATN_Tài liệu\database-seeders\46_completed_booking_payment_backfill.sql`
- Final audit:
  - payments: 83.
  - bookings without payment: 25, deu hop le theo trang thai.
  - success/refunded booking thieu payment tuong ung: 0.
  - payment amount mismatch: 0.
  - success payment thieu paid_at: 0.
  - refunded payment thieu refunded_at: 0.
- Audit:
  - `D:\DATN\DATN_Tài liệu\database-seeders\audit_booking_payment_integrity.php`
- Report:
  - `D:\DATN\DATN_Tài liệu\data-center\reports\booking-payment-integrity-backfill-2026-06-05.md`
- API fix:
  - `BookingService::completeBooking()` da lock booking row trong transaction.
  - neu da co success payment thi tai su dung, khong tao trung.
  - neu chua co thi tao ADMIN success payment history.
  - rollback neu update booking that bai.
  - tests: 37 passed, 140 assertions.
  - PHPStan: no errors.
  - Pint: passed.
- Next priority:
  - quyet dinh integrate subcategories hay archive master categories khong dung.

### Collected data quality audit - 2026-06-06

- Ket luan:
  - du cho DATN/demo.
  - chua dat production-grade content.
- Locations:
  - 333 total, 221 active.
  - 222/222 published crawl items co production entity link.
  - missing core fields/images/relations: 0.
  - 107 active descriptions duoi 100 ky tu.
  - 94 active short descriptions duoi 40 ky tu.
  - 2 duplicate normalized name groups.
  - 7 shared coordinate groups, phan lon la co-located event/attraction.
  - 13 locations ngoai Da Nang bbox nhung chu yeu la Hoi An/Quang Nam/Hue, co the hop le theo pham vi mien Trung.
- Tours:
  - 100 live rows, IDs 1-100.
  - crawled operator tours IDs 101+ chua nam trong live DB.
  - chi 40 distinct names.
  - 20 duplicate name groups va 20 duplicate description groups.
  - 100/100 descriptions duoi 150 ky tu.
  - 80 prices co phan thap phan VND giong synthetic variants.
  - ket luan: live tours chu yeu la demo/variant seed.
- Blogs:
  - 104 published.
  - 101 posts duoi 500 content characters.
  - post 102 chi co `chay quá`.
  - posts 103, 104, 105 trung noi dung hoan toan.
  - ket luan: blog chu yeu la teaser/placeholder.
- Crawl staging:
  - 258 pending deu thieu image candidates, giu manual review.
- Reports:
  - `D:\DATN\DATN_Tài liệu\data-center\reports\collected-data-quality-audit-2026-06-06.md`
- Audit scripts:
  - `D:\DATN\DATN_Tài liệu\database-seeders\audit_collected_data_quality.php`
  - `D:\DATN\DATN_Tài liệu\database-seeders\audit_collected_data_details.php`
- Next priority:
  - thay/archive 80 synthetic tour variants bang reviewed real operator tours.
  - rewrite/unpublish 101 short blog posts va archive 2/3 duplicate long posts.
  - enrich 107 short active location descriptions.

### Tour replacement readiness gate - 2026-06-06

- Da audit lai 36 crawler tours bang production quality gate moi.
- Tieu chi:
  - source URL bat buoc.
  - price/duration khong duoc inferred.
  - itinerary >= 3.
  - inclusions/exclusions >= 2.
  - images >= 2.
  - duration phai hop ly voi route va itinerary.
  - image relevance can manual review.
- Ket qua:
  - ready for manual publish: 4.
  - needs recrawl: 32.
- Blocking reasons:
  - incomplete itinerary: 17.
  - suspicious duration: 14.
  - incomplete exclusions: 8.
  - incomplete inclusions: 7.
  - inferred core field: 4.
- Chua replace 80 synthetic live tours:
  - 4 tour that chua du duy tri catalog.
  - replace luc nay se lam giam coverage nghiem trong.
- Script:
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\scripts\audit_tour_publish_readiness.py`
- Outputs:
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\tour-publish-readiness.json`
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\tour-publish-readiness.csv`
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\tour-publish-readiness-report.json`
- Report:
  - `D:\DATN\DATN_Tài liệu\data-center\reports\tour-replacement-readiness-2026-06-06.md`
- Next priority:
  - recrawl 32 failed source URLs.
  - rerun strict gate.
  - chi tao replacement seed khi du unique real tours.

### Targeted tour recrawl - 2026-06-06

- Da crawl lai dung 32 failed source URLs bang `.venv`.
- Command:
  - `scripts/crawl_tours.py --discover-mode exact`.
- Network result:
  - requested: 32.
  - collected: 32.
  - failures: 0.
  - robots skipped: 0.
- Sau normalize/enrich:
  - staging: 32.
  - direct price: 28.
  - direct duration: 31.
  - with itinerary: 15.
  - inferred core fields: 4.
- Strict gate sau recrawl:
  - ready: 0.
  - needs recrawl/parser fix: 32.
- Ket luan:
  - crawl lai khong sua duoc quality.
  - root cause la parser duration va section extraction theo layout website.
  - khong apply vao live DB.
- Outputs:
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\tour-recrawl-20260606-raw.json`
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\tour-recrawl-20260606-normalized.json`
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\tour-recrawl-readiness-20260606.json`
- Next priority:
  - sua parser theo operator: Danang Local Tours, Venus Vietnam Travel, VM Travel, Dacotours.
  - rerun normalize va strict gate, khong can crawl lai neu raw HTML facts da du.

### Automatic tour schedule closure - 2026-06-06

- Da them command:
  - `php artisan tour-schedules:sync-availability`
- Da them scheduler:
  - chay moi 15 phut.
  - `withoutOverlapping(10)`.
- Quy tac dong booking:
  - start_date da qua.
  - booking_deadline da qua.
  - booked_people >= max_people.
  - schedule status cancelled.
- Lan chay dau:
  - closed 41 schedules.
- Lan chay thu hai:
  - closed 0 schedules, idempotent.
- Final audit:
  - past open booking: 0.
  - open past deadline: 0.
  - open full: 0.
  - open cancelled: 0.
  - future open: 115.
- Verification:
  - tests: 36 passed, 136 assertions.
  - PHPStan: no errors.
  - Pint: passed.
- Production requirement:
  - server phai chay `php artisan schedule:run` moi phut hoac quan ly `php artisan schedule:work`.
- Report:
  - `D:\DATN\DATN_Tài liệu\data-center\reports\tour-schedule-automatic-closure-2026-06-06.md`
- Next priority:
  - quyet dinh integrate subcategories hay archive master categories khong dung.

### Tour parser v3 and strict image audit - 2026-06-07

- Da sua `scripts/crawl_tours.py`:
  - parser itinerary/service theo layout Venus Vietnam Travel.
  - parser duration/detail itinerary theo layout VM Travel.
  - gioi han section theo heading, khong doc xuyen sang section/footer.
  - uu tien `og:image` va gallery co token lien quan truc tiep den ten tour.
  - loai logo, icon, placeholder, TripAdvisor, branding va anh tour lien quan khac.
- Da sua `scripts/audit_tour_publish_readiness.py`:
  - anh sai ngu canh la blocking error.
  - tour co duration <= 2 hours va itinerary >= 3 la suspicious.
- Parser v2:
  - 30 detail rows.
  - 11 rows qua text gate.
  - deep review phat hien anh menu/logo/tour khac, nen khong publish.
- Parser v3 strict image gate:
  - requested: 32 URLs.
  - collected: 28 URLs.
  - 4 temporary DNS failures.
  - normalized detail rows: 27.
  - ready for manual publish: 4.
  - blocked: 23.
- 4 ready candidates:
  - Ba Na Hills And Golden Bridge Tour From Tien Sa Port.
  - Da Nang City Tour From Tien Sa Port - Explore and Shopping.
  - My Son Sanctuary Tour From Tien Sa Port - Explore Now.
  - Hue Imperial Tour from Chan May Port: Best Shore Excursions.
- Moi ready candidate co:
  - direct source URL.
  - direct price va duration.
  - itinerary, inclusions, exclusions day du.
  - 8 anh source-relevant.
- Blocking reasons:
  - insufficient images: 14.
  - suspicious duration: 9.
  - irrelevant images: 9.
  - incomplete inclusions: 7.
  - incomplete exclusions: 7.
  - incomplete itinerary: 6.
  - inferred core field: 4.
- Khong ghi DB va khong tao replacement seed.
- Report:
  - `D:\DATN\DATN_Tài liệu\data-center\reports\tour-replacement-readiness-2026-06-06.md`
- Next priority:
  - dung Pexels/Cloudinary de bo sung anh cho Venus chi sau khi manual match destination.
  - bo qua category/listing pages cua Dacotours va Vietnam Adventure Tour.
  - crawl them detail pages VM Travel de dat it nhat 30-50 real tours truoc khi replace synthetic catalog.

### Verified real tour catalog reached 30 rows - 2026-06-07

- Da scan sitemap VM Travel:
  - discovered: 1623 URLs.
  - loc detail tour mien Trung moi: 26 URLs.
  - crawl thanh cong: 26/26.
- Da phat hien va sua loi gia:
  - parser cu lay `From $30` tu menu/header.
  - parser moi doc `.table-price-tour`.
  - vi du gia that: Ba Na $65, golf 4 ngay $425, Hue bicycle $60.
  - neu VM Travel co price table nhung khong co numeric price thi khong fallback.
  - them `suspicious_price` gate.
- Da sua image relevance:
  - cho phep token ngan co y nghia nhu Hue, Hoi An, DMZ.
  - audit ca image alt, khong chi URL.
- Da dieu chinh completeness gate theo noi dung:
  - mot exclusion ro rang duoc chap nhan.
  - itinerary 2 section dai duoc chap nhan neu tong noi dung >= 350 ky tu.
- Da recrawl 5 VM Travel old-ready URLs bang price parser moi:
  - 5/5 pass.
  - 0 inferred core fields.
- Da enrichment Pexels cho 4 Venus candidates:
  - 12 image candidates.
  - luu provider page, photographer, photo id va query.
  - manual visual review approved 2 tour:
    - Ba Na Hills Golden Bridge.
    - Cham Island snorkeling/coral.
- Final verified catalog:
  - total: 30.
  - unique source URLs: 30.
  - direct prices: 30.
  - direct durations: 30.
  - itinerary/inclusions/exclusions: 30/30.
  - at least 2 images: 30/30.
  - source images: 28.
  - source primary + visually reviewed Pexels: 2.
  - database written: no.
- Outputs:
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\verified-real-tour-catalog-20260607.json`
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\verified-real-tour-catalog-20260607-report.json`
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data\venus-tour-pexels-enriched-20260607-manifest.json`
- Script:
  - `scripts/discover_vmtravel_tours.py`
  - `scripts/enrich_tour_images_pexels.py`
  - `scripts/build_verified_real_tour_catalog.py`
- Next priority:
  - download full-resolution media theo naming convention.
  - tao Cloudinary manifest.
  - editorial review title/summary.
  - chi sau do moi generate database replacement seed.

### Verified tour media downloaded and staged - 2026-06-07

- Input:
  - `data/verified-real-tour-catalog-20260607.json`
- Naming:
  - `tour-{catalog_index}__{slug}__p{index}__{provider}-{external_id}.{ext}`
- Cloudinary public ID:
  - `danangtrip/tours/{slug}/{file_stem}`
- Download result:
  - tours: 30.
  - requested slots: 90.
  - downloaded: 89.
  - failed: 1.
  - bytes: 68,012,203.
  - tours with >= 2 local images: 30.
  - tours with all 3 images: 29.
- Integrity:
  - unique SHA-256: 78.
  - duplicate content mappings: 11.
  - duplicates are not included in upload manifest.
  - tour media map points duplicate slots to canonical public ID.
- Failed source:
  - Da Nang to Hue Day Trip by Heritage Train via Hai Van Pass.
  - one 2026 source image failed DNS/download.
  - tour still has 2 downloaded images and remains complete.
- Output:
  - `D:\DATN\DATN_Tài liệu\data-center\media-assets\cloudinary-staging\tours\2026-06-07-verified-real-tours`
- Files:
  - `manifest.json`
  - `manifest.csv`
  - `upload-manifest.json`
  - `upload-manifest.csv`
  - `tour-media-map.json`
  - `summary.json`
- Upload-ready unique assets:
  - 78.
- Cloudinary uploaded:
  - no.
- Database written:
  - no.
- Next priority:
  - run Cloudinary upload with `upload-manifest.csv` when approved.
  - use upload results plus `tour-media-map.json` to build final media URLs.
  - editorial title/summary review before database replacement seed.

### Verified tour media uploaded to Cloudinary - 2026-06-07

- Upload manifest:
  - 78 unique assets.
- First upload:
  - uploaded: 75.
  - failed: 3.
  - all 3 failures belonged to the long Venus Ba Na Hills public ID.
- Fix:
  - shortened path to `danangtrip/tours/bana-hills-afternoon-night/...`.
- Retry:
  - uploaded: 3/3.
- Final Cloudinary status:
  - unique assets uploaded: 78/78.
  - mapped image slots: 89.
  - unmapped source slots: 1.
  - tours with Cloudinary media: 30/30.
  - tours with >= 2 Cloudinary images: 30/30.
  - tours with all 3 images: 29/30.
- HTTP verification:
  - checked 78 unique secure URLs.
  - valid image responses: 78/78.
  - failures: 0.
- Final catalog:
  - `data/verified-real-tour-catalog-cloudinary-20260607.json`
- Final media map:
  - `data-center/media-assets/cloudinary-staging/tours/2026-06-07-verified-real-tours/cloudinary-tour-media-map.json`
- Cloudinary summary:
  - `data-center/media-assets/cloudinary-staging/tours/2026-06-07-verified-real-tours/cloudinary-summary.json`
- Database written:
  - no.
- Next priority:
  - editorial cleanup title and Vietnamese summaries.
  - map categories/destinations.
  - generate reviewable replacement seed.
  - apply only after explicit approval.

### Vietnamese diacritics audit - 2026-06-07

- Scope:
  - crawler JSON/CSV artifacts.
  - database seeder SQL files.
  - production-facing display columns in the current API database.
- File audit:
  - files scanned: 276.
  - files with likely unaccented Vietnamese: 86.
  - likely unaccented Vietnamese values: 17,658.
  - accented Vietnamese values: 997.
- Database audit:
  - rows scanned: 1,139.
  - rows with likely unaccented Vietnamese: 223.
  - likely unaccented field values: 475.
  - confirmed accented field values: 1,507.
- Main database issue:
  - `locations`: 222/333 rows affected.
  - `short_description`: 222 unaccented values.
  - `description`: 222 unaccented values.
  - `name`: 4 unaccented values.
  - `address`: 26 unaccented values.
- Healthy database areas:
  - `tours`: 0 unaccented values detected.
  - taxonomy tables: no confirmed issue.
  - `categories.name` id 73 is a detector false positive: `Vé tham quan & Show`.
- Policy:
  - keep slugs, URLs, file names, Cloudinary public IDs, and technical identifiers ASCII.
  - do not classify valid English source text as Vietnamese missing diacritics.
  - repair display text through reviewed source regeneration, not blind accent insertion.
- Reports:
  - `data-center/reports/vietnamese-diacritics-audit-2026-06-07.json`
  - `data-center/reports/vietnamese-diacritics-audit-2026-06-07.csv`
  - `data-center/reports/vietnamese-diacritics-db-audit-2026-06-07.json`
- Database written:
  - no.
- Next priority:
  - replace the 222 generated `locations` description templates with reviewed Vietnamese text.
  - normalize the 4 location names and 26 addresses.
  - change seeder/crawler generation policy so new Vietnamese display text preserves diacritics.

### Vietnamese diacritics repair applied - 2026-06-07

- Root cause fixed:
  - location pipeline no longer converts display fields to ASCII.
  - Overpass and curated sources preserve UTF-8/NFC text.
  - only slugs and technical identifiers are converted to ASCII.
  - crawler and seeder documentation no longer requires unaccented Vietnamese.
- Live database repair:
  - 222 generated `locations` rows updated in one transaction.
  - 222 `short_description` values rewritten with Vietnamese diacritics.
  - 222 `description` values rewritten with Vietnamese diacritics.
  - 222 addresses normalized, including `Da Nang` to `Đà Nẵng`.
  - 4 confirmed location names corrected.
- Safety:
  - pre-change backup:
    - `data-center/backups/locations-before-vietnamese-diacritics-2026-06-07-150018.json`
  - applied-change report:
    - `data-center/reports/location-vietnamese-diacritics-repair-2026-06-07-150018.json`
- Post-repair database audit:
  - rows scanned: 1,139.
  - rows with likely unaccented Vietnamese: 0.
  - unaccented field values: 0.
  - accented field values: 2,357.
  - final report:
    - `data-center/reports/vietnamese-diacritics-db-audit-2026-06-07.json`
- Historical artifact audit:
  - files scanned: 276.
  - old files with likely unaccented Vietnamese: 86.
  - old values flagged: 17,658.
  - these are mainly immutable crawl snapshots and generated SQL from the former ASCII policy.
  - do not use the old artifacts as production display content; regenerate canonical artifacts with the fixed pipeline.
- Verification:
  - TypeScript typecheck passed.
  - Python compile check passed.
  - PHP syntax checks passed.
- Known environment warning:
  - PHP reports missing optional `imagick`; it did not affect the database repair or audit.

### Canonical UTF-8 rebuild guard - 2026-06-07

- Added:
  - `database-seeders/47_canonical_display_text_utf8_seed.sql`.
  - generator: `database-seeders/generate_canonical_display_text_seed.php`.
- Coverage:
  - 9 production-facing tables.
  - 1,139 rows.
  - 2,355 accented Vietnamese values detected.
  - 0 unaccented Vietnamese values detected.
- Seed order:
  - seed `47` is last in both `full` and `incremental_current_live`.
  - this prevents old ASCII-era seeds from leaving unaccented display text after rebuild.
- Artifact lifecycle:
  - `data-center/artifact-lifecycle.json`.
  - raw crawl snapshots remain immutable evidence.
  - normalized/generated artifacts must be regenerated with the UTF-8 pipeline.
  - production display text is canonical from the audited database and seed `47`.
- Overpass recrawl:
  - attempted with `overpass-api.de` and `overpass.kumi.systems`.
  - both failed at network fetch on 2026-06-07.
  - existing snapshot was unchanged and separately backed up.

### Mojibake and UTF-8 audit - 2026-06-07

- File scope:
  - crawler data.
  - database seeders.
  - data-center text artifacts.
- File result:
  - files scanned: 352.
  - invalid UTF-8 files: 0.
  - files with mojibake: 0.
  - strong mojibake signals: 0.
- Database result:
  - rows scanned: 1,139.
  - display field values scanned: 3,580.
  - rows with mojibake: 0.
- Reports:
  - `data-center/reports/mojibake-audit-2026-06-07.json`.
  - `data-center/reports/mojibake-audit-2026-06-07.csv`.
  - `data-center/reports/mojibake-db-audit-2026-06-07.json`.
- Tools:
  - `danangtrip-crawler/scripts/audit_mojibake.py`.
  - `database-seeders/audit_mojibake_db.php`.
- Detector policy:
  - only strong encoding corruption signals are reported.
  - valid standalone Vietnamese characters such as `Â` and `Ã` are not treated as errors.
  - audit tools and their generated reports are excluded from self-scanning.
- Data changed:
  - no repair was required.

### Duplicate catalog audit and repair - 2026-06-07

- Scope:
  - 333 locations.
  - 100 tours.
  - 105 blog posts.
- Initial findings:
  - locations: 4 high-confidence pairs and 22 review pairs.
  - tours: 20 exact-content groups, 4 rows per group, 80 affected tours.
  - blogs: post 105 was an exact content copy of post 103.
- Location decision:
  - Memory Lounge duplicate was already handled correctly: id 96 active, id 221 inactive.
  - HanCook rows 236, 237, and 238 are separate branches at different addresses; they were not merged.
  - lodging rows with similar names or shared street-level addresses remain review-only.
- Tour decision:
  - all 120 duplicate pairs had identical product content.
  - duplicate tours had 123 booking item references plus schedules, ratings, favorites, views, cart, and location mappings.
  - no tour row or relation was deleted.
  - one canonical tour per group remains active, selected by cart/booking/engagement usage.
  - 60 duplicate tours were changed to `inactive` and `booking_availability = sold_out`.
- Blog decision:
  - blog 105 `(Copy)` changed from `published` to `archived`.
  - blog 103 remains published.
- Final public catalog:
  - tours active: 40.
  - tours inactive: 60.
  - active duplicate tour pairs: 0.
  - published duplicate blog pairs: 0.
  - active high-confidence duplicate location pairs: 0.
- Safety:
  - backup: `data-center/backups/catalog-before-duplicate-repair-2026-06-07-155801.json`.
  - apply report: `data-center/reports/duplicate-catalog-repair-2026-06-07-155801.json`.
  - audit report: `data-center/reports/duplicate-entities-audit-2026-06-07.json`.
  - persistent rebuild seed: `database-seeders/48_deactivate_duplicate_catalog_seed.sql`.
- Tools:
  - `database-seeders/audit_duplicate_entities.php`.
  - `database-seeders/repair_duplicate_catalog.php`.
- Verification:
  - seed manifest Check passed.
  - no active/published duplicate pairs remain.

### Data tooling moved out of API - 2026-06-07

- Removed:
  - `danangtrip-api/tools`.
  - six PHP wrapper files used only for data audit, repair, and seed generation.
- Canonical location for data tooling:
  - `D:\DATN\DATN_Tài liệu\database-seeders`.
  - `D:\DATN\DATN_Tài liệu\danangtrip-crawler\scripts`.
- API boundary:
  - `danangtrip-api` contains application/runtime code only.
  - data scripts may bootstrap the API to reuse Laravel configuration and database connectivity, but their files, reports, backups, and generated seeds remain under `DATN_Tài liệu`.
- Unrelated API changes preserved:
  - `routes/console.php`.
  - `app/Console`.
  - `app/Services/TourScheduleAvailabilityService.php`.
  - `tests/Unit/SyncTourScheduleAvailabilityTest.php`.

### Verified real tour catalog imported - 2026-06-07

- Canonical catalog:
  - `data/verified-real-tour-catalog-cloudinary-20260607.json`.
- Database seed:
  - `database-seeders/49_verified_real_tours_seed.sql`.
- Generator:
  - `danangtrip-crawler/scripts/generate_verified_real_tour_seed.py`.
- Pre-import backup:
  - `data-center/backups/verified-real-tour-import-before-20260607-162522.json`.
- API schema adjustment:
  - `danangtrip-api/database/migrations/2026_06_07_000001_expand_tour_thumbnail_url.php`.
  - changes `tours.thumbnail` from `varchar(255)` to `text` for verified Cloudinary URLs.
- Imported:
  - tours: 30.
  - tour-location mappings: 46.
  - future schedules: 240.
  - Cloudinary thumbnails: 30/30.
- Safety:
  - all imported tours remain `inactive`.
  - existing tours, bookings, ratings, schedules, and relations were not deleted.
  - seed upserts by slug and is idempotent.
  - second seed run remained 30 tours, 46 mappings, and 240 schedules.
- Quality verification:
  - missing required content: 0.
  - tours without location mapping: 0.
  - duplicate imported slugs: 0.
  - Vietnamese missing-diacritic findings: 0.
  - mojibake findings: 0.
  - duplicate catalog audit did not add new duplicate groups.
- Editorial status:
  - source titles and detailed itinerary/service facts remain in English where supplied by operators.
  - Vietnamese summary/description is normalized and accented.
  - admin/editor review is still required before changing status to `active`.

### Verified real tour editorial activation - 2026-06-07

- User approved activating the verified real tours.
- Added:
  - `database-seeders/50_verified_real_tours_editorial_vi_seed.sql`.
  - `danangtrip-crawler/scripts/generate_verified_real_tour_editorial_seed.py`.
- Applied to database:
  - updated only the 30 verified real tour slugs from the Cloudinary catalog.
  - converted public-facing title, description, short description, itinerary, inclusions, and exclusions to Vietnamese.
  - set `status = active`.
  - preserved prices, Cloudinary media, tour-location mappings, schedules, and booking availability.
- Final counts:
  - verified real tours in DB: 30.
  - active verified real tours: 30.
  - Cloudinary thumbnails: 30/30.
  - missing required content: 0.
  - future open schedules for verified tours: 240.
  - tours without location mapping: 0.
  - total active tours in DB: 70.
- Quality checks after activation:
  - Vietnamese missing-diacritic findings: 0.
  - mojibake findings: 0.
  - duplicate audit: no new duplicate tour groups introduced.
- Note:
  - duplicate audit still reports 120 old high-confidence tour pairs from the legacy seed catalog; these were already handled by deactivating duplicate legacy tours.

### Full database rebuild with latest seeds - 2026-06-07

- User requested deleting current database data and reseeding with the newest dataset.
- Backup before destructive rebuild:
  - `D:\DATN\DATN_Tài liệu\data-center\backups\full-database-before-reseed-20260607-192341.json`.
  - backed up 42 tables.
- Fixed seed issues before final rebuild:
  - `database-seeders/05_locations.sql`: escaped apostrophes in SQL text values.
  - `database-seeders/07_blog_posts.sql`: escaped apostrophes in English blog content.
  - `database-seeders/46_completed_booking_payment_backfill.sql`: synced `payments.id` sequence before backfill inserts.
- Final rebuild flow:
  - ran `php artisan migrate:fresh --force` in `D:\DATN\danangtrip-api`.
  - ran `database-seeders/apply_database_seeders.ps1 -Mode Full`.
  - applied seed files `01` through `50` successfully.
- Final core counts:
  - users: 100.
  - locations: 112.
  - active locations: 108.
  - tours: 164.
  - active tours: 70.
  - tour schedules: 676.
  - blog posts: 118.
  - bookings: 100.
  - payments: 78.
  - crawl items: 942.
- Quality verification after rebuild:
  - mojibake audit: 0 rows with findings.
  - active tour duplicate names: 0.
  - booking-payment audit: no success/refund/payment amount mismatches.
  - schedule audit: no missing departure code/place/deadline, no past open booking schedules, no deadline-after-departure issues.
  - `php artisan test tests\Unit\SyncTourScheduleAvailabilityTest.php`: passed.
- Remaining polish items:
  - 2 locations without tags.
  - 2 locations without amenities.
  - 2 tours without location mapping.
  - 7 active locations missing thumbnail.
  - 18 draft blog posts missing featured image.
  - Vietnamese diacritic audit still flags 53 rows, mostly 34 pending/staging tours and 18 draft blog posts.
  - schedule audit reports 16 duplicate departure code groups.
  - PHP startup still warns that `imagick` extension is missing; it did not block migration, seeding, or tests.

### Database quality polish seed applied - 2026-06-07

- Added and applied:
  - `database-seeders/51_database_quality_polish_seed.sql`.
- Manifest updated:
  - `51_database_quality_polish_seed.sql` is included in both `full` and `incremental_current_live`.
- Documentation updated:
  - `database-seeders/README.md` now lists seed `51` as the final quality polish layer.
- Fixes included:
  - normalized unaccented legacy blog category id `1`.
  - normalized weak crawl location names/slugs for ids `101`, `102`, `104`, `113`, `114`.
  - filled missing thumbnails/images for location ids `5`, `101`, `102`, `103`, `104`, `113`, `114`.
  - added missing location tags and amenities for pending locations `102` and `104`.
  - added missing tour-location mappings for pending tours `106` and `110`.
  - replaced unaccented generic pending tour copy with accented Vietnamese holding copy.
  - added Vietnamese titles/excerpts/content and featured images for draft blog posts `201-218`.
  - made duplicated `tour_schedules.departure_code` values unique.
- Final verification:
  - relation gaps: all 0.
  - missing location thumbnails: 0.
  - missing tour thumbnails: 0.
  - missing blog featured images: 0.
  - Vietnamese missing-diacritic findings: 0.
  - mojibake findings: 0.
  - duplicate active tour names: 0.
  - duplicate active location names: 0.
  - duplicate schedule departure code groups: 0.
  - `php artisan test tests\Unit\SyncTourScheduleAvailabilityTest.php`: passed.
- Final core counts:
  - users: 100.
  - locations: 112.
  - tours: 164.
  - tour_schedules: 706 after rerunning incremental seed; seed `49` uses rolling future schedules and does not duplicate the same `tour_id + start_date`.
  - blog_posts: 118.
  - bookings: 100.
  - payments: 78.
  - crawl_items: 942.
- Remaining non-blocking warning:
  - PHP startup still warns that `imagick` extension is missing.

### Public Vietnamese content and one-command database refresh - 2026-06-08

- User requested a full data audit: public content must be Vietnamese with full diacritics, collected data should be centralized, and the database should be rerunnable with one command.
- Added and applied:
  - `database-seeders/52_public_vietnamese_content_seed.sql`.
  - `database-seeders/53_tour_schedule_current_date_guard_seed.sql`.
- Manifest updated:
  - seeds `52` and `53` are included in both `full` and `incremental_current_live`.
- New operating folder:
  - `D:\DATN\DATN_Tài liệu\data-center\database-refresh`.
  - one-command rebuild: `RUN_REBUILD_DATABASE.ps1`.
  - one-command incremental update: `RUN_INCREMENTAL_UPDATE.ps1`.
  - one-command audit: `RUN_AUDIT_DATABASE.ps1`.
- Collected data snapshot folder:
  - `D:\DATN\DATN_Tài liệu\data-center\collected-data`.
  - contains crawler data snapshot and database seeders snapshot for handoff/reference.
- Final audit after applying seed `53` and syncing schedule availability:
  - public Vietnamese content findings: 0.
  - unaccented Vietnamese DB findings: 0.
  - mojibake findings: 0.
  - relation gaps: all 0.
  - active locations missing thumbnail: 0.
  - tours missing thumbnail: 0.
  - blog posts missing featured image: 0.
  - past open booking schedules: 0.
  - duplicate departure code groups: 0.
- Current core counts:
  - locations: 112 total, 107 active, 5 pending_review.
  - tours: 164 total, 70 active, 60 inactive, 34 pending_review.
  - tour_schedules: 676.
  - blog_posts: 118 total, 100 published, 18 draft.
  - bookings: 100.
  - payments: 78.
  - crawl_items: 942 total, 222 approved, 258 pending_review, 462 rejected.
- Remaining non-blocking warning:
  - PHP startup still warns that `imagick` extension is missing; it does not block seed, audit, or schedule sync.

### Expired runtime cleanup and publication backlog audit - 2026-06-08

- Added and applied:
  - `database-seeders/54_cleanup_expired_auth_runtime_seed.sql`.
  - `database-seeders/audit_publication_backlog.php`.
- Manifest updated:
  - seed `54` is included at the end of both `full` and `incremental_current_live`.
- Final runtime audit:
  - expired password reset tokens: 0.
  - expired refresh tokens: 0.
  - failed jobs: 0.
  - cache locks: 0.
- Publication backlog report:
  - `D:\DATN\DATN_Tài liệu\data-center\reports\publication-backlog-2026-06-08-103953.json`.
  - locations pending_review: 5.
  - tours pending_review: 34.
  - blog posts draft: 18.
- Important decision:
  - Pending/draft records were not auto-published because they require editorial/admin approval.
  - Public/active data remains clean and audit-ready.

### Detailed location Vietnamese and taxonomy repair - 2026-06-08

- User reported remaining unaccented Vietnamese in location content.
- Root cause:
  - previous audits skipped mixed accented/unaccented fields;
  - seed `52` used legacy id-based normalization, producing mechanical names and shifted content for slugs after id `104`;
  - many locations had incorrect categories, such as attractions under food and hotels under coffee.
- Added and applied:
  - `database-seeders/55_location_catalog_editorial_vi_seed.sql`.
  - `database-seeders/audit_locations_vietnamese_detailed.php`.
- Seed `55` behavior:
  - matches locations by stable `slug`, not numeric id;
  - normalizes Vietnamese place names and addresses;
  - preserves official international brand names;
  - remaps location categories;
  - restores correct values for `lang-co-beach`, `hai-van-pass`, `vinwonders-nam-hoi-an`, `son-tra-peninsula`, `tra-que-vegetable-village`, and `tam-giang-lagoon`;
  - replaces English/mechanical short descriptions and descriptions with Vietnamese editorial copy;
  - moves unverified `4-seasons-danang-hostel` to `pending_review`.
- Manifest:
  - seed `55` is last in both `full` and `incremental_current_live`.
- Final verification:
  - detailed location findings: 0 across 112 rows.
  - public Vietnamese content findings: 0.
  - unaccented Vietnamese field values across DB: 0.
  - mojibake findings: 0.
  - relation gaps: 0.
  - 26 official brand/foreign names are tracked separately and are not treated as Vietnamese spelling errors.

### Latest incremental database refresh verified - 2026-06-08

- Seeder integrity check:
  - 55 SQL files total.
  - 53 full seeds, 1 optional demo seed, 1 read-only coverage check.
  - no empty files.
  - no missing manifest files.
  - no duplicate manifest entries.
  - final full/incremental seed: `55_location_catalog_editorial_vi_seed.sql`.
- Ran:
  - `data-center/database-refresh/RUN_INCREMENTAL_UPDATE.ps1`.
  - `database-seeders/apply_database_seeders.ps1 -Mode Check`.
- Incremental result:
  - all 22 incremental seeds applied successfully.
  - schedule availability sync completed.
  - public Vietnamese findings: 0.
  - detailed location Vietnamese findings: 0.
  - unaccented Vietnamese DB fields: 0.
  - mojibake findings: 0.
  - relation gaps: 0.
  - missing public media: 0.
  - past open schedules: 0.
  - duplicate departure codes: 0.
  - schedule unit test: passed.
- Current catalog state:
  - locations: 112 total, 106 active, 6 pending_review.
  - tours: 164 total, 70 active, 60 inactive, 34 pending_review.
  - tour schedules: 706.
  - blog posts: 118 total, 100 published, 18 draft.
- Remaining non-blocking environment warning:
  - PHP `imagick` extension is not installed.

### Ratings Vietnamese normalization and realistic volume - 2026-06-08

- User reported that rating comments were still unaccented and requested more reviews for realism.
- Root cause:
  - the original `09_ratings_interactions.sql` contained 100 generic unaccented comments;
  - ratings were limited to 3-5 stars and only 50 location plus 50 tour reviews.
- Added and applied:
  - `database-seeders/56_ratings_editorial_vi_and_volume_seed.sql`.
  - `database-seeders/audit_ratings_quality.php`.
- Seed `56` behavior:
  - rewrites all legacy comments to natural Vietnamese with diacritics;
  - maintains a stable idempotent target of 360 location ratings and 260 tour ratings;
  - guarantees every active location and active tour has at least one approved rating;
  - uses a realistic 2-5 star distribution;
  - recalculates `locations.avg_rating`, `locations.review_count`, `tours.rating_avg`, and `tours.rating_count`;
  - does not add fabricated rating images.
- Final ratings state:
  - total: 620 approved ratings.
  - overall average: 4.33.
  - 2 stars: 23.
  - 3 stars: 99.
  - 4 stars: 148.
  - 5 stars: 350.
  - active locations without ratings: 0.
  - active tours without ratings: 0.
  - unaccented comments: 0.
  - duplicate user-location groups: 0.
  - duplicate user-tour groups: 0.
  - aggregate mismatches: 0.
- Idempotency verified:
  - rerunning seed `56` keeps the total at 620.

### Recent operational activity and counter integrity - 2026-06-08

- Operational audit found that all activity except ratings stopped on 2026-04-30:
  - 0 bookings, payments, favorites, views, searches, notifications, and contacts in the previous 30 days;
  - 100/100 users had no `last_login_at`;
  - 27 stale pending bookings;
  - 185 location/tour counter mismatches;
  - active catalog coverage gaps for views and favorites.
- Added and applied:
  - `database-seeders/57_recent_operational_activity_seed.sql`;
  - `database-seeders/audit_operational_activity.php`.
- Seed `57` behavior:
  - labels generated activity with `DEMO-ACT-` and `demo-activity-`;
  - creates a stable set of 24 recent bookings using active tours and future schedules;
  - creates success and pending payment histories;
  - refreshes login, favorite, view, search, notification, and contact timelines;
  - guarantees every active location and active tour has views and favorites;
  - closes or confirms legacy stale pending bookings;
  - recalculates location/tour view, favorite, and booking counters;
  - repairs PostgreSQL sequences before inserting.
- Final operational state:
  - activity in the last 7 days: 12 bookings, 8 payment attempts, 32 favorites, 109 views, 14 searches, 15 notifications, 38 ratings, 11 contacts;
  - activity in the last 30 days: 24 bookings, 18 payment attempts, 146 favorites, 525 views, 66 searches, 67 notifications, 126 ratings, 49 contacts;
  - users never logged in: 0;
  - stale pending bookings: 0;
  - active locations/tours without views or favorites: 0;
  - location/tour counter mismatches: 0;
  - booking/payment hard mismatches: 0.
- Idempotency verified:
  - rerunning seed `57` keeps totals at 124 bookings, 103 payments, 219 favorites, and 628 views.
- Seed `57` is included in both `full` and `incremental_current_live`.

### Public taxonomy visibility cleanup - 2026-06-08

- Public APIs returned every active taxonomy record, including:
  - 77 location categories without locations;
  - 88 tour categories without tours;
  - 100 subcategories without assigned locations;
  - 81 orphan blog categories.
- Added and applied `database-seeders/58_public_taxonomy_visibility_seed.sql`.
- Behavior:
  - location categories without active locations become inactive;
  - tour categories without active tours become inactive;
  - subcategories without active locations become inactive;
  - blog categories are deleted only when they have no `blog_post_categories` relation.
- This prevents empty categories from appearing on the home page and filter panels while preserving taxonomy used by content.

### Rating admin read tracking - 2026-06-08

- Added Laravel `ratings.is_new` support for admin-only read tracking.
- Added `database-seeders/59_ratings_admin_read_state_seed.sql`.
- Historical initialization:
  - ratings from the latest 7 days are marked new;
  - older ratings are marked viewed;
  - a private settings marker ensures later incremental runs never reset an admin's viewed state.
- New customer ratings continue to use the database default `is_new = true`.
- Public rating visibility still depends only on `status`; `is_new` never affects the public site.
