# DanangTrip Crawler

Standalone data collection system for DanangTrip.

This module is designed to collect tourism data, clean it, store raw evidence, and prepare it for admin review before publishing into the main DanangTrip application.

## Why This Exists

DanangTrip needs reliable real-world data:

- Tourist attractions
- Restaurants and cafes
- Hotels/stays
- Tours and schedules
- Travel guides
- FAQ content
- Ratings and coordinates
- Legal image references

This should not run directly inside `danangtrip-api`, because crawling is slow, failure-prone, and source-specific. The crawler should run as a separate worker/service and only send approved data to the main system.

## High-Level Workflow

```text
Source configuration
        |
        v
Crawler worker
        |
        v
Raw storage
        |
        v
Normalizer
        |
        v
Enrichment
        |
        v
Pending review
        |
        v
Admin approval
        |
        v
DanangTrip production tables
```

## Main Principle

Never write crawled data directly into production tables.

Correct flow:

```text
raw -> normalized -> pending_review -> approved -> published
```

This keeps bad, duplicate, copyrighted, or incomplete data away from the public website.

## Recommended Source Strategy

### 1. Google Places API

Use for real place data:

- Name
- Address
- Place ID
- Latitude/longitude
- Rating
- Review count
- Opening hours
- Place types

Best first use cases:

- Attractions in Da Nang
- Restaurants in Da Nang
- Cafes in Da Nang
- Hotels in Da Nang

### 2. Pexels / Unsplash API

Use for legal image candidates.

Do not copy images from Tripadvisor, Booking, Klook, Traveloka, random blogs, or Google Images unless license/permission is clear.

### 3. Crawl4AI / Firecrawl / Crawlee

Use for blog/FAQ/travel guide content.

Good targets:

- Travel tips
- Itinerary suggestions
- FAQ content
- Public tourism pages

Always check robots.txt and terms of service.

### 4. Crawlee + Playwright

Use for dynamic websites only when needed.

Use cases:

- Pages requiring JavaScript rendering
- Infinite scroll
- Click-to-load content
- Dynamic tour listings

## Proposed Database Staging Tables

Use staging tables first:

```text
crawl_sources
crawl_jobs
crawl_items
crawl_logs
```

Production tables such as `locations`, `tours`, `blog_posts`, `media` should only receive data after review/approval.

See `docs/schema.sql` for a starting schema.

## Folder Structure

```text
danangtrip-crawler/
  memory.md
  README.md
  package.json
  tsconfig.json
  .env.example
  data/
    .gitkeep
  docs/
    schema.sql
  src/
    cli/
      crawl.ts
    config/
      env.ts
    contracts/
      crawler.ts
    pipelines/
      locationPipeline.ts
    sources/
      mockPlacesSource.ts
    storage/
      fileStorage.ts
    utils/
      logger.ts
```

## Initial Development Flow

### Step 1: Install dependencies

```bash
npm install
```

### Step 2: Copy environment file

```bash
copy .env.example .env
```

On PowerShell:

```powershell
Copy-Item .env.example .env
```

### Step 3: Run dry crawl

```bash
npm run crawl:mock
```

Expected result:

- Read mock place data
- Normalize it
- Write JSON output into `data/crawl-items.json`

### Step 4: Run real Overpass crawl

```bash
npm run crawl:overpass
```

Expected result:

- Query Overpass API for Da Nang POIs.
- Normalize attractions, restaurants/cafes, hotels and parks.
- Write pending-review output into `data/overpass-danang-pois.json`.

Current tested result on 2026-05-31:

```text
total: 942
location: 218
restaurant: 483
hotel: 241
```

### Step 5: Implement image enrichment

Pexels enrichment is available after `PEXELS_API_KEY` is configured in local `.env`:

```text
npm.cmd run enrich:pexels
```

The crawler should store:

- Image URL
- Photographer name
- Pexels page URL
- Search keyword used
- License/source attribution

Current Pexels output files:

```text
data/overpass-danang-pois-enriched.json
data/pexels-enrichment-report.json
../database-seeders/14_pexels_image_enrichment_seed.sql
```

The first run enriches 80 clean items with 3 image candidates each. Increase `PEXELS_ENRICH_LIMIT` in `.env` only after checking image quality and API quota.

Current `.env` is configured for full resume:

```text
PEXELS_ENRICH_LIMIT=580
PEXELS_PHOTOS_PER_ITEM=3
PEXELS_REQUEST_DELAY_MS=750
PEXELS_STOP_ON_429=true
```

If Pexels returns `429 Too Many Requests`, run the same command again later. The script preserves existing images, skips already enriched items, and stops early on throttle.

### Step 6: Optional Google Places source

If Google Places API is available later:

```text
src/sources/googlePlacesSource.ts
```

Recommended search seeds:

```text
tourist attractions in Da Nang
restaurants in Da Nang
cafes in Da Nang
hotels in Da Nang
beaches in Da Nang
```

### Step 7: Add persistence

Two options:

1. Write to staging tables in the same PostgreSQL database used by `danangtrip-api`.
2. Write to a separate crawler database, then sync approved records later.

For the DATN project, option 1 is simpler if admin review screens are added to `danangtrip-admin`.

## Admin Review Flow

Later, add a screen in `danangtrip-admin`:

```text
/admin/crawl-items
```

Expected actions:

- View raw payload
- View normalized payload
- Detect duplicates
- Edit fields
- Approve
- Reject
- Publish to location/tour/blog tables

Statuses:

```text
raw
normalized
pending_review
approved
rejected
published
failed
```

## Data Quality Rules

Before approving a crawled item:

- Name must be human-readable.
- Address or coordinates must exist for locations.
- Category must be mapped.
- Images must have legal source.
- Pexels images are candidates and must be reviewed before publish.
- Duplicate detection must pass.
- Description should be reviewed or generated from approved source material.
- External source ID/URL must be kept.
- Text content in crawler outputs and SQL seed files must be Vietnamese without diacritics.
- Example text style: `Bao tang Da Nang`, `Duong Tran Phu`, `am thuc dia phuong`.

## Security and Compliance

- Do not store API keys in Git.
- Do not scrape protected/private data.
- Do not bypass paywalls, login walls, or anti-bot restrictions.
- Respect robots.txt and website terms.
- Do not copy copyrighted images without permission.
- Store source metadata for traceability.

## Roadmap

### Phase 1: Local scaffold

- Mock source
- Normalization pipeline
- JSON output
- Staging schema draft

### Phase 2: Real place crawl

- Google Places source
- PostgreSQL staging write
- Duplicate detection
- Crawl logs

### Phase 3: Admin review

- Admin list screen
- Detail screen
- Approve/reject/publish actions

### Phase 4: Image pipeline

- Pexels/Unsplash source
- Image candidate matching by place/category
- Manual approval

### Phase 5: Blog/FAQ knowledge

- Markdown crawler
- FAQ extractor
- Travel guide enrichment
- Optional RAG-ready content chunks

## Current Status

Implemented as of 2026-05-31:

- Overpass API crawler for Da Nang POIs.
- JSON file storage.
- Normalization pipeline.
- ASCII / Vietnamese-without-diacritics text policy.
- Quality filtering and dedupe.
- Pexels image enrichment for reviewed candidate data.
- SQL seed generation for crawler staging tables.

Current generated data:

```text
raw Overpass items: 942
clean pending-review items: 580
rejected items: 360
Pexels-enriched candidate items: 580
```

Recommended next step:

1. Add duplicate matching against existing `locations`, `restaurants`, and hotel/stay data before publishing.
2. Review Pexels image quality and raise `PEXELS_ENRICH_LIMIT` if the matches are acceptable.
3. Build `/admin/crawl-items` review screen to approve/reject/publish crawled data.
