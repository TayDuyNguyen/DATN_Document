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
14. `14_pexels_image_enrichment_seed.sql`
15. `15_crawl_duplicate_matching_seed.sql`

Chi chay thu cong sau khi admin da duyet item:

16. `16_crawl_publish_approved_locations.sql`

## Ghi chu

- Khong doi thu tu so dau file neu cac file con phu thuoc khoa ngoai.
- Neu them seed moi, dat so thu tu tiep theo va mo ta ly do trong commit.
- Toan bo noi dung seed phai dung ASCII / tieng Viet khong dau. Khong de lai ky tu co dau hoac loi encoding mojibake.
- Du lieu crawl tu Overpass duoc nap vao bang staging `crawl_items` voi `status = pending_review`, khong ghi thang vao `locations`.
- Can admin/agent loc trung, kiem tra ten-dia chi-toa do-anh truoc khi publish sang bang chinh.
- `16_crawl_publish_approved_locations.sql` chi publish item co `status = approved`, khong bi trung production, va publish vao `locations.status = inactive` de admin bat active sau.

## Chuan hoa encoding

Da chuan hoa cac file `01` den `10` ve ASCII / tieng Viet khong dau bang:

```powershell
cd D:\DATN\DATN_Document\danangtrip-crawler
npm.cmd run normalize:seeders
```

Lenh kiem tra:

```powershell
rg -n "[^\x00-\x7F]" D:\DATN\DATN_Document\database-seeders
```

Neu khong co output nghia la seed dang sach ky tu non-ASCII.

## Du lieu crawl hien co

| File | Noi dung | So luong |
| --- | --- | ---: |
| `11_crawl_staging_tables.sql` | Tao bang staging `crawl_sources`, `crawl_jobs`, `crawl_items`, `crawl_logs`. | - |
| `12_overpass_danang_pois_seed.sql` | Import POI Da Nang tu OpenStreetMap/Overpass vao `crawl_items`. | 942 |
| `13_overpass_quality_review_seed.sql` | Danh dau ban ghi dat chat luong la `pending_review`, ban ghi can loai la `rejected`. | 940 |
| `14_pexels_image_enrichment_seed.sql` | Gan 3 anh Pexels ung vien cho tung item clean. | 580 |
| `15_crawl_duplicate_matching_seed.sql` | Danh dau item staging co kha nang trung voi bang `locations`. | dynamic |
| `16_crawl_publish_approved_locations.sql` | Publish item da approve sang `locations` o trang thai `inactive`. | dynamic |

Thong ke sau khi ap dung `13_overpass_quality_review_seed.sql`:

| Entity | So luong |
| --- | ---: |
| `location` pending review | 180 |
| `restaurant` pending review | 220 |
| `hotel` pending review | 180 |
| rejected | 360 |
