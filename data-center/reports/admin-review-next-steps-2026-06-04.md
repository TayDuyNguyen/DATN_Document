# Admin Review Next Steps - 2026-06-04

## Current DB Status

Public relation coverage is clean:

| Check | Result |
| --- | ---: |
| locations_total | 333 |
| locations_active | 111 |
| locations_inactive | 222 |
| locations_without_tags | 0 |
| locations_without_amenities | 0 |
| tours_without_schedule | 0 |
| tours_without_location_mapping | 0 |
| published_blog_posts_without_category | 0 |
| promotions | 10 |
| landing_pages | 5 |
| crawl_items | 942 |
| crawl_published | 222 |
| crawl_pending_review | 360 |
| crawl_rejected | 360 |

## Inactive Locations

There are 222 crawl-published locations in `locations.status = inactive`.

Important:

- `inactive_with_thumbnail`: 0.
- `inactive_without_thumbnail`: 222.
- Do not bulk activate these rows before admin review.

Category split:

| Category | Count |
| --- | ---: |
| khach-san-homestay | 108 |
| am-thuc-dia-phuong | 75 |
| check-in-noi-tieng | 16 |
| bao-tang-di-tich | 7 |
| ca-phe-tra-sua | 6 |
| cong-vien-vuon-hoa | 6 |
| hang-dong-nui-non | 2 |
| cong-vien-nuoc | 2 |

Duplicate signal:

| Name | Count |
| --- | ---: |
| nha hang hancook | 3 |

Recommended handling:

1. Review duplicate group `nha hang hancook`.
2. Keep one canonical row.
3. Leave duplicate rows inactive or merge/delete manually after confirming source.
4. Add thumbnail/images only after legal source review.
5. Activate locations gradually by category.

## Pending Crawl Items

There are 360 `crawl_items.status = pending_review`.

Entity split:

| Entity | Count |
| --- | ---: |
| location | 147 |
| restaurant | 141 |
| hotel | 72 |

Category split:

| Category | Count |
| --- | ---: |
| check-in-noi-tieng | 100 |
| am-thuc-dia-phuong | 75 |
| khach-san-homestay | 71 |
| ca-phe-tra-sua | 67 |
| cong-vien-vuon-hoa | 23 |
| bao-tang-di-tich | 12 |
| hang-dong-nui-non | 11 |
| cong-vien-nuoc | 1 |

Recommended review order:

1. `check-in-noi-tieng`: highest user-facing travel value.
2. `am-thuc-dia-phuong`: useful for discovery, but needs duplicate/name cleanup.
3. `khach-san-homestay`: review carefully because many hotel records lack rich data.
4. `ca-phe-tra-sua`: review after restaurants.
5. Parks/museums/mountains/water parks: smaller batches, review manually.

## What Not To Do Automatically

- Do not activate all 222 inactive locations at once.
- Do not apply Pexels image candidates without image review.
- Do not publish the 360 pending crawl items without dedupe/quality review.
- Do not delete duplicate HanCook rows automatically unless admin confirms the canonical row.

## Best Next Action

Create an admin review CSV/export for the 222 inactive locations with:

- id
- slug
- name
- category
- district
- address
- latitude
- longitude
- source_url from `crawl_items`
- duplicate flag
- has_thumbnail
- recommended_action

