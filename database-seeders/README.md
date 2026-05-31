# Database Seeders

Thu muc nay chua cac file SQL seed data theo thu tu khoi tao.

## Thu tu nap de xuat

1. `01_categories_subcategories.sql`
2. `02_tags_amenities.sql`
3. `03_tour_blog_categories.sql`
4. `04_users.sql`
5. `05_locations.sql`
6. `06_tours.sql`
7. `07_blog_posts.sql`
8. `08_bookings_payments.sql`
9. `09_ratings_interactions.sql`
10. `10_system_tables.sql`
11. `11_crawl_staging_tables.sql`
12. `12_overpass_danang_pois_seed.sql`
13. `13_overpass_quality_review_seed.sql`

## Ghi chu

- Khong doi thu tu so dau file neu cac file con phu thuoc khoa ngoai.
- Neu them seed moi, dat so thu tu tiep theo va mo ta ly do trong commit.
- Du lieu crawl tu Overpass duoc nap vao bang staging `crawl_items` voi `status = pending_review`, khong ghi thang vao `locations`.
- Can admin/agent loc trung, kiem tra ten-dia chi-toa do-anh truoc khi publish sang bang chinh.

## Du lieu crawl hien co

| File | Noi dung | So luong |
| --- | --- | ---: |
| `11_crawl_staging_tables.sql` | Tao bang staging `crawl_sources`, `crawl_jobs`, `crawl_items`, `crawl_logs`. | - |
| `12_overpass_danang_pois_seed.sql` | Import POI Da Nang tu OpenStreetMap/Overpass vao `crawl_items`. | 942 |
| `13_overpass_quality_review_seed.sql` | Danh dau ban ghi dat chat luong la `pending_review`, ban ghi can loai la `rejected`. | 940 |

Thong ke sau khi ap dung `13_overpass_quality_review_seed.sql`:

| Entity | So luong |
| --- | ---: |
| `location` pending review | 180 |
| `restaurant` pending review | 220 |
| `hotel` pending review | 180 |
| rejected | 360 |
