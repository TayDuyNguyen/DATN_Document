# Tour & Blog Categories Audit - 2026-06-03

## Module

- Tables: `tour_categories`, `blog_categories`.
- Related content tables: `tours`, `blog_posts`, `blog_post_categories`.
- Seeder: `D:\DATN\DATN_Tài liệu\database-seeders\03_tour_blog_categories.sql`.
- Purpose: controlled taxonomy for tour listing, blog listing, homepage sections, search, and admin content management.

## Schema Coverage

`tour_categories` supports:

- `name`
- `slug`
- `description`
- `icon`
- `sort_order`
- `status`

`blog_categories` supports:

- `name`
- `slug`
- `description`

No schema change is required for the current crawler/data audit.

## Current Seed Status

`03_tour_blog_categories.sql` currently provides:

- 100 tour categories.
- 100 blog categories.

This should be treated as controlled taxonomy/config data, not crawled real-world data.

The seed is broad and includes many route/theme/season/activity categories. That is acceptable as product taxonomy, but it should not be counted as collected real data.

## Related Seed Data Status

Important distinction:

- `tour_categories` and `blog_categories`: keep as seed/config.
- `tours` and `blog_posts`: content/business data, should eventually be replaced or backed by real reviewed sources.

Observed related seeds:

- `06_tours.sql` contains 20 manually written tour-like rows and then generates rows 21-100 with SQL variation logic. Treat it as demo/dev seed, not verified real tour inventory.
- `07_blog_posts.sql` contains 100 English travel-guide style posts without per-row source URL/evidence. Treat it as demo/dev seed, not verified crawled content.

## Crawler Coverage

Current crawler evidence:

- No real tour inventory crawler is implemented yet.
- No real blog/travel-guide crawler is implemented yet.
- `danangtrip-crawler/README.md` recommends Crawl4AI / Firecrawl / Crawlee for blog/FAQ/travel guide content, but only after checking robots.txt and terms of service.
- Active instruction is database/text only; image generation/enrichment is disabled.

## Data Classification

Tables that should stay seed/config:

- `tour_categories`
- `blog_categories`

Tables that need real collection/review later:

- `tours`
- `tour_schedules`
- `tour_locations`
- `blog_posts`
- `blog_post_categories`

Reason:

- Categories are internal UX taxonomy.
- Tours are sellable products and need real prices, schedules, inclusions, exclusions, meeting points, and availability.
- Blog posts are content and need source/editorial evidence or original authored content.

## Decision

- Do not crawl `tour_categories` and `blog_categories` as independent real data tables.
- Keep `03_tour_blog_categories.sql` as controlled seed/config.
- Do not auto-generate category rows from external sites.
- Mark tour/blog content seeds as demo/dev until source evidence is added.
- Next real crawl target should be `tours`, not `tour_categories`.

## Recommended Real Data Sources Later

For tours:

- Official tour operator pages with permission or public product data.
- DanangTrip-owned operator data if available.
- Manual admin import from verified partner inventory.

For blogs/travel guides:

- DanangTrip-owned original content.
- Official tourism pages that allow referencing/summarization.
- Crawl4AI/Firecrawl/Crawlee only for text extraction after checking robots.txt and terms.

Do not copy full copyrighted tour/blog content into seed files.

## Gaps

- No source URL/external ID/evidence field exists in `tours` or `blog_posts` seeds.
- Generated tour rows 21-100 in `06_tours.sql` are synthetic.
- `07_blog_posts.sql` content is not tied to crawl sources.
- Blog categories have no `status` or `sort_order` in schema, unlike `tour_categories`.

## Next Work

Recommended next module: `tours`, `tour_schedules`, and `tour_locations`.

Reason:

- These are business-critical data tables.
- Current seed appears demo/synthetic.
- They need real partner/operator data or a reviewed crawl/import workflow.
