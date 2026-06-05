# Full Database Data Sufficiency Audit - 2026-06-05

## Verdict

The database has enough data for:

- Graduation project demonstration
- Public web browsing flows
- Admin management flows
- Tour search/detail/booking demonstrations
- Blog/content demonstrations
- User interaction and reporting demonstrations

It is structurally clean enough for the graduation project and initial deployment preparation.

Main reasons:

- Master category tables are over-seeded but underused.
- Ratings cover only a subset of locations and tours.

Tour schedule metadata and booking availability were normalized on 2026-06-05.

## Complete table counts

| Table | Rows | Assessment |
| --- | ---: | --- |
| amenities | 100 | More than enough; only active usage matters |
| blog_categories | 101 | Excessive; 77 unused |
| blog_post_categories | 119 | Sufficient |
| blog_posts | 105 | Sufficient |
| booking_items | 158 | Sufficient for demo |
| bookings | 105 | Sufficient for demo |
| cache | 126 | Runtime data; should not be evaluated as business seed |
| cache_locks | 100 | Suspicious seeded/stale runtime data |
| cart_items | 2 | Fine; cart is runtime/temporary |
| categories | 100 | Excessive; only 11 used |
| contacts | 100 | Sufficient for admin demo |
| crawl_items | 942 | Large enough |
| crawl_jobs | 1 | Fine for one imported crawl batch |
| crawl_logs | 8 | Fine |
| crawl_sources | 1 | Fine if Overpass is the current main source |
| failed_jobs | 100 | Should be cleaned; not valid business data |
| favorites | 110 | Sufficient for demo |
| job_batches | 100 | Suspicious seeded/runtime data |
| jobs | 0 | Normal when queue is empty |
| landing_pages | 5 | Sufficient |
| location_amenities | 680 | Good relation coverage |
| location_tags | 725 | Good relation coverage |
| locations | 333 | More than enough |
| migrations | 42 | Normal |
| notifications | 101 | Sufficient for demo |
| password_reset_tokens | 100 | Expired/stale runtime data; should be cleaned |
| payments | 74 | Sufficient for demo |
| promotions | 10 | Sufficient |
| rating_images | 101 | Sufficient for demo |
| ratings | 97 | Moderate; coverage remains limited |
| refresh_tokens | 168 | Runtime authentication data |
| search_logs | 221 | Sufficient for analytics demo |
| sessions | 101 | Runtime data |
| settings | 23 | Sufficient |
| subcategories | 100 | Seeded but unused |
| tags | 100 | More than enough |
| tour_categories | 100 | Excessive; only 7 used |
| tour_locations | 192 | Good |
| tour_schedules | 300 | More than enough |
| tours | 100 | More than enough |
| users | 100 | Sufficient for demo |
| views | 137 | Sufficient for demo |

## Public content quality

- Locations:
  - Total: 333
  - Active: 221
  - Inactive/manual review: 112
  - Missing thumbnail: 0
  - Active duplicate name groups: 0
  - Without tags: 0
  - Without amenities: 0
- Tours:
  - Total/active: 100
  - Missing thumbnail/content: 0
  - Without schedules: 0
  - Without location mapping: 0
  - Generic slugs: 0
- Blogs:
  - Published: 104
  - Archived test post: 1
  - Missing content/excerpt/image: 0
  - Published posts without category: 0
- Promotions:
  - Active and currently usable: 8
- Landing pages:
  - Total: 5

## Category utilization

| Master data | Total | Used | Unused |
| --- | ---: | ---: | ---: |
| Location categories | 100 | 11 | 89 |
| Subcategories | 100 | 0 | 100 |
| Tour categories | 100 | 7 | 93 |
| Blog categories | 101 | 24 | 77 |

Assessment:

- The database has many category rows, but this is quantity without useful coverage.
- The UI should hide empty categories.
- Subcategories are currently not integrated into location data.
- For a cleaner production DB, unused generic categories should be archived or removed after confirming no code depends on fixed IDs.

## Tour schedule status

- Total schedules: 300
- Future available schedules: 158
- Future schedules open for booking: 156
- Past schedules open for booking: 0
- Past schedules closed as sold out: 142
- Overbooked schedules: 0
- Missing `departure_code`: 0
- Missing `departure_place`: 0
- Missing `booking_deadline`: 0

Completed:

1. Generated a unique departure code for every schedule.
2. Backfilled departure place from the tour meeting point.
3. Added booking deadlines 12 hours before departure.
4. Closed booking for past schedules.

## Engagement coverage

- Ratings: 97
- Locations with ratings: 35/333
- Tours with ratings: 41/100
- Favorites: 110
- Users with favorites: 100/100
- Users with bookings: 99/100
- Search logs: 221
- Views: 137

Assessment:

- Enough for UI/admin demonstrations.
- Not statistically realistic for recommendation/ranking algorithms.
- If recommendation quality matters, add ratings for at least 80 active locations and 70 tours.

## Booking and payment coverage

- Bookings: 105
- Booking items: 158
- Payments: 83
- Bookings without a payment record: 25

Booking status:

- Pending: 32
- Confirmed: 26
- Completed: 27
- Cancelled: 20

Payment status on bookings:

- Success: 69
- Pending: 16
- Refunded: 9
- Unpaid: 11

Assessment:

- Distribution is good for admin and reporting demonstrations.
- Nine completed bookings missing payment history were backfilled on 2026-06-05.
- The remaining 25 bookings without payment records are valid:
  - 11 cancelled and unpaid.
  - 14 pending payment without a recorded payment attempt.
- No success/refunded booking is missing the corresponding payment status.
- Payment amounts and paid/refunded timestamps pass the integrity audit.

## Crawl data

- Total: 942
- Published: 222
- Pending review: 258
- Rejected: 462

Assessment:

- Enough source data has already been collected.
- More crawling is not currently necessary.
- Remaining pending rows lack image candidates and mostly have weak address data.

## Runtime cleanup

- `failed_jobs`: 0
- `job_batches`: 0
- `cache_locks`: 0
- `password_reset_tokens`: 0

Completed on 2026-06-05 using:

- Backup: `data-center/backups/runtime-cleanup-backup-20260605-142727.json`
- Seed: `database-seeders/45_cleanup_stale_runtime_data.sql`

Sessions and refresh tokens were intentionally preserved.

## Final priority order

1. Decide whether to integrate subcategories or archive unused master categories.
2. Improve rating coverage only if recommendations/ranking are important.
3. Keep 112 inactive locations and 258 crawl items in manual review; do not auto-publish.
