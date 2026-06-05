# Tags & Amenities Audit - 2026-06-03

## Module

- Tables: `tags`, `amenities`.
- Pivot tables: `location_tags`, `location_amenities`.
- Seeder: `D:\DATN\DATN_Tài liệu\database-seeders\02_tags_amenities.sql`.
- Purpose: controlled filters, labels, facility lists, and admin-managed metadata for locations.

## Schema Coverage

`tags` supports:

- `name`
- `slug`
- `type`

`amenities` supports:

- `name`
- `icon`
- `category`

`location_tags` supports:

- `location_id`
- `tag_id`

`location_amenities` supports:

- `location_id`
- `amenity_id`

No schema change is required for the current crawler pipeline.

## Current Seed Status

`02_tags_amenities.sql` currently provides:

- 100 tags.
- 100 amenities.

This seed should be treated as controlled taxonomy/config data.

It is not fake business/location data in the same way as demo `locations`; however, it is broad and product-defined, so it should not be counted as crawled real-world records.

## Crawler Coverage

The current Overpass crawler stores useful source tags in staging:

- `normalized_payload.categories`
- `raw_payload.osmTags`

Examples of OSM fields available in crawl payload:

- `tourism`
- `amenity`
- `historic`
- `leisure`
- `natural`
- `cuisine`
- `opening_hours`
- `website`
- `contact:*`
- `addr:*`

Current production publish behavior:

- `16_crawl_publish_approved_locations.sql` publishes approved rows into `locations`.
- It does not attach rows into `location_tags`.
- It does not attach rows into `location_amenities`.

This is the right default for now because tag/amenity mapping from raw OSM fields has not been reviewed.

## Data Classification

Tables that should stay seed/config:

- `tags`
- `amenities`

Tables that should be populated only after reviewed location publish or admin action:

- `location_tags`
- `location_amenities`

Reason:

- Tags and amenities are product UX filters.
- OSM fields are noisy and inconsistent.
- Auto-attaching tags/amenities without mapping rules can make search/filter results incorrect.

## Recommended Mapping Rules

Safe candidates that can be implemented later after review:

- `internet_access=yes|wlan` -> amenity `Wifi mien phi` or tag `strong-wifi`.
- `parking=*` -> amenity `Cho dau xe mien phi` only if value clearly indicates parking availability.
- `wheelchair=yes|limited` -> amenity `Loi di cho nguoi khuyet tat`.
- `opening_hours=24/7` -> tag `open-247` or amenity `Le tan 24h` depending on entity type.
- `takeaway=yes` -> tag `takeaway`.
- `delivery=yes` -> tag `delivery`.
- `outdoor_seating=yes` -> tag `outdoor-seating`.
- `cuisine=*` -> food tags only after cuisine vocabulary is normalized.

These rules should be added as a separate reviewed mapping step, not mixed into the first production publish.

## Decision

- Do not crawl `tags` and `amenities` as independent real data tables.
- Keep `02_tags_amenities.sql` as controlled seed/config.
- Do not automatically create new tag or amenity rows from OSM tags.
- Do not automatically attach `location_tags` or `location_amenities` during `16_crawl_publish_approved_locations.sql` yet.
- Add a dedicated mapping/review workflow later if the admin wants OSM-derived filters.

## Gaps

- No reviewed mapping file currently exists from OSM tags to `tags` / `amenities`.
- Existing `02_tags_amenities.sql` has broad hotel/service amenities that may not apply to every location type.
- Some seed tag names are English while most product labels are Vietnamese without diacritics.
- Pivot data should not be trusted unless it comes from admin review or a deterministic mapping rule.

## Next Work

Recommended next module: `tour_categories` and `blog_categories`.

Reason:

- They are also taxonomy/config tables.
- They determine whether tour/blog content needs real crawl or controlled seed only.
