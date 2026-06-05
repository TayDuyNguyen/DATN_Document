# Categories & Subcategories Audit - 2026-06-03

## Module

- Tables: `categories`, `subcategories`.
- Seeder: `D:\DATN\DATN_Tài liệu\database-seeders\01_categories_subcategories.sql`.
- Purpose: controlled taxonomy for locations, restaurants, hotels, tours, search filters, and UI navigation.

## Schema Coverage

`categories` supports:

- `name`
- `slug`
- `icon`
- `description`
- `image`
- `sort_order`
- `status`

`subcategories` supports:

- `category_id`
- `name`
- `slug`
- `description`
- `sort_order`
- `status`

No schema change is required for the current crawler pipeline.

## Data Classification

This module should be treated as seed/config data, not a table that must be crawled row-by-row.

Reason:

- Categories are product taxonomy, not external real-world entities.
- Stable slugs are required by crawler mapping and API filters.
- Crawling categories directly from the web would create unstable naming and inconsistent UI navigation.

## Current Seed Status

`01_categories_subcategories.sql` currently provides:

- 100 categories.
- 100 subcategories.
- Active statuses and stable slugs.

This seed can stay as a controlled taxonomy seed. It does not need source URL/external ID per row like `locations`.

## Crawler Mapping Coverage

The Overpass crawler currently maps clean POIs into these category slugs:

- `cong-vien-nuoc`: 3.
- `bao-tang-di-tich`: 19.
- `check-in-noi-tieng`: 116.
- `cong-vien-vuon-hoa`: 29.
- `hang-dong-nui-non`: 13.
- `am-thuc-dia-phuong`: 148.
- `ca-phe-tra-sua`: 73.
- `khach-san-homestay`: 179.

These slugs are present in the controlled category seed, so the current `locations` publish SQL can resolve category IDs without adding new categories.

## Decision

- Do not crawl `categories` and `subcategories` as real data tables.
- Keep them as seed/config tables.
- Only update them manually when product taxonomy changes.
- Do not auto-generate new category rows from raw crawl tags.

## Gaps

- The seed is broad and contains many non-tourism/business categories. This is acceptable for a directory-style city app, but may be too wide for a focused travel-only product.
- Some subcategories are not used by current Overpass data.
- If the app focuses only on Da Nang tourism, the category list should later be reduced to fewer curated categories for cleaner UX.

## Next Work

Recommended next module: `tags` and `amenities`.

Reason:

- They are also controlled taxonomy/support data.
- They connect directly to `locations` via `location_tags` and `location_amenities`.
- They should likely stay seed/config too, but need audit before real-data collection continues.
