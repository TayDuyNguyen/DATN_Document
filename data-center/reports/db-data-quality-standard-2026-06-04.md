# DB Data Quality Standard - 2026-06-04

## Goal

Make DanangTrip database reliable for demo, admin review, search/filter, and future production use.

## Quality Levels

### Level 1 - Safe Staging

Use for crawled/raw records.

Required:

- source table or source URL.
- external ID if available.
- raw payload.
- normalized payload.
- status: `pending_review`, `approved`, `rejected`, or `published`.
- no automatic public visibility.

Current tables:

- `crawl_sources`
- `crawl_jobs`
- `crawl_items`
- `crawl_logs`

### Level 2 - Review-Ready Production

Use for records inserted into production tables but not public yet.

Required:

- valid category.
- valid slug.
- valid latitude/longitude when location-based.
- tag and amenity relations.
- status: `inactive`.
- source trace from `crawl_items`.

Current example:

- 222 crawl-published `locations.status = inactive`.

### Level 3 - Public-Ready

Use only after admin/editor review.

Required:

- clean Vietnamese display name.
- no duplicate/canonical conflict.
- useful short description and description.
- legal thumbnail/images or intentionally image-less UI support.
- tag and amenity relations.
- correct category/subcategory.
- status: `active` or `published`.

## Current DB Health

Clean checks:

- `locations_without_tags = 0`.
- `locations_without_amenities = 0`.
- `tours_without_schedule = 0`.
- `tours_without_location_mapping = 0`.
- `published_blog_posts_without_category = 0`.
- `promotions = 10`.
- `landing_pages = 5`.

Remaining review work:

- 222 inactive locations need admin review before activation.
- 360 pending crawl items need manual review before any further publish.
- 222 inactive locations have no thumbnail yet.
- Pexels image candidates were intentionally not applied to live DB.

## Recommended Workflow

1. Review inactive location CSV:
   - `D:\DATN\DATN_Tài liệu\data-center\reports\inactive-locations-review-2026-06-04.csv`
2. Resolve duplicate names first.
3. Add or verify legal images for records selected for public use.
4. Activate only reviewed rows.
5. Review `pending_review` crawl items by category and publish in small batches.
6. Run coverage checks after every batch.

## Activation Rules

Do not activate a location if:

- duplicate_name_count > 1 and canonical row is not chosen.
- no clear address or coordinate confidence.
- name is generic, broken, or looks like crawl noise.
- it has no legal image and UI page requires image.
- category is wrong or too generic.

Can activate after review if:

- name is clear.
- source is traceable.
- category is correct.
- location has tag/amenity relations.
- image policy is satisfied or UI supports missing images.

## Crawl Rules

Only crawl more data when one of these is true:

- a production table is empty or below target.
- a specific screen lacks content.
- pending_review queue is depleted.
- current data lacks required fields after review.

Do not crawl more just because raw count is low for behavior tables:

- `bookings`
- `payments`
- `cart_items`
- `favorites`
- `views`
- `ratings`
- `notifications`

These are demo/user behavior data, not real crawl targets.

