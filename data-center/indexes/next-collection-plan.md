# Next Collection Plan

## Priority 1: Blog / Travel Guide Text

Reason:

- Existing `07_blog_posts.sql` is demo-like.
- Batch 3 + 4 + 5 already collected 23 source-backed records.
- 18 records are approved for draft seed.
- The next step is editor rewrite or FAQ-specific collection, not more general guide crawling.

Target fields:

- title
- slug
- excerpt
- content_summary
- source_url
- source_name
- category_hint
- tags_hint
- status = pending_review

Rules:

- Do not copy long source text.
- Keep source_url for traceability.
- Rewrite/summarize facts into short DB-ready text.
- featured_image remains NULL unless using already approved URL.

## Priority 2: Pending Location Review

Reason:

- 277 Overpass candidates are approved across 3 batches.
- Remaining weak-address POIs are lower confidence.
- Need manual review or stricter external source verification, not auto approve all.

Approach:

- Prioritize tourist attractions and named restaurants/cafes.
- Keep weak hotel/unclear address pending.

## Priority 3: Manual Verification

- `Hoa Phu Thanh`
- `Nui Than Tai Hot Spring Park`

Need coordinate verification before approving location seed.
