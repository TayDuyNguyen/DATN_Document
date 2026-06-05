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
16. `16_crawl_publish_approved_locations.sql`
17. `17_promotions_seed.sql`
18. `18_landing_pages_seed.sql`
19. `19_settings_seed.sql`
20. `20_approved_tour_staging_seed.sql`
21. `21_approve_overpass_clean_batch1.sql`
22. `22_approved_blog_guides_seed.sql`
23. `23_approve_overpass_weak_address_landmarks.sql`
24. `24_approve_overpass_weak_address_services.sql`
25. `25_landing_faq_blocks_seed.sql`
26. `26_cart_items_demo_seed.sql` neu can test cart/checkout UI
27. `27_published_location_taxonomy_backfill.sql` sau khi publish location crawl
28. `28_seed_coverage_check.sql` chi de kiem tra, khong thay doi du lieu
29. `29_live_relation_gap_fix_seed.sql` neu live DB thieu mapping tour/blog/location taxonomy
30. `30_live_relation_gap_fix_followup_seed.sql` chay sau `29` de gan mapping cho destination moi
31. `31_archive_test_blog_posts_seed.sql` an cac bai blog test khoi public data
32. `32_published_location_minimum_amenity_backfill.sql` dam bao location publish tu crawl co amenity toi thieu
33. `33_hancook_location_taxonomy_fix.sql` bo sung taxonomy cho 2 location HanCook inactive con thieu
34. `34_update_location_images_from_cloudinary_seed.sql` cap nhat Cloudinary thumbnail/images cho inactive locations crawl-published
35. `35_hancook_duplicate_location_images_fix.sql` bo sung anh cho duplicate HanCook inactive
36. `36_update_active_location_images_from_cloudinary_seed.sql` cap nhat Cloudinary thumbnail/images cho active locations cu
37. `37_activate_curated_inactive_locations_batch1.sql` activate batch curated non-lodging inactive locations
38. `38_deactivate_memory_lounge_crawl_duplicate.sql` dua duplicate Memory Lounge crawl ve inactive
39. `39_tour_content_quality_backfill_seed.sql` backfill itinerary/inclusions/exclusions/start_time/meeting_point/price_infant cho tours
40. `40_update_tour_images_from_cloudinary_seed.sql` cap nhat Cloudinary thumbnail/images cho tours
41. `41_update_blog_featured_images_from_cloudinary_seed.sql` cap nhat Cloudinary featured_image cho published blog posts
42. `42_reject_duplicate_pending_crawl_items.sql` chuyen duplicate crawl_items pending_review sang rejected de don queue
43. `43_polish_generic_tour_slugs_seed.sql` sua ten lap chu Tour va thay `tour-real-variant-*` bang slug SEO duy nhat
44. `44_tour_schedule_operational_backfill.sql` bo sung departure code/place/deadline va dong booking lich qua khu

## Lenh mot dong

Thu muc nay da co manifest va script de chay seed theo thu tu:

- `seed-manifest.json`
- `apply_database_seeders.ps1`
- `audit_database_quality.ps1`
- `audit_database_quality.php`

Kiem tra DB hien tai:

```powershell
powershell -ExecutionPolicy Bypass -File "D:\DATN\DATN_Tài liệu\database-seeders\audit_database_quality.ps1"
```

Chay read-only coverage check:

```powershell
powershell -ExecutionPolicy Bypass -File "D:\DATN\DATN_Tài liệu\database-seeders\apply_database_seeders.ps1" -Mode Check
```

Cap nhat DB hien tai bang cac seed backfill moi nhat:

```powershell
powershell -ExecutionPolicy Bypass -File "D:\DATN\DATN_Tài liệu\database-seeders\apply_database_seeders.ps1" -Mode Incremental
```

Khoi tao DB moi sau khi da chay migration/fresh schema:

```powershell
powershell -ExecutionPolicy Bypass -File "D:\DATN\DATN_Tài liệu\database-seeders\apply_database_seeders.ps1" -Mode Full
```

Neu muon nap them du lieu demo cart:

```powershell
powershell -ExecutionPolicy Bypass -File "D:\DATN\DATN_Tài liệu\database-seeders\apply_database_seeders.ps1" -Mode Full -IncludeOptionalDemo
```

Luu y quan trong:

- `Mode Full` chi dung cho DB moi/DB da migrate fresh. Khong chay len DB da co du lieu vi cac seed dau co fixed `id`.
- `Mode Incremental` chi chay cac seed backfill hien tai (`34` den `40`) cho live DB hien co.
- Script dung Laravel `php artisan tinker`, nen se dung dung ket noi DB trong `D:\DATN\danangtrip-api\.env`.

Chi chay thu cong sau khi admin da duyet item:

- `16_crawl_publish_approved_locations.sql`
- `21_approve_overpass_clean_batch1.sql` neu muon approve batch Overpass sach truoc khi publish.

## Seed coverage check - 2026-06-03

Doi chieu voi migrations trong `D:\DATN\danangtrip-api\database\migrations`, cac bang production chua co SQL seed rieng trong thu muc tai lieu:

| Table | Nen seed khong? | Huong xu ly |
| --- | --- | --- |
| `settings` | Da co | `19_settings_seed.sql` la SQL mirror cua `D:\DATN\danangtrip-api\database\seeders\SettingSeeder.php` de seed doc lap voi Laravel. |
| `promotions` | Da co | `17_promotions_seed.sql` tao du lieu khuyen mai demo/thuc te de test admin va booking flow. |
| `landing_pages` | Da co | `18_landing_pages_seed.sql` tao seed text/config cho `/du-lich-da-nang`, landing theo dong tour, landing promotion. Khong tao anh. |
| `cart_items` | Tuy chon | `26_cart_items_demo_seed.sql` tao du lieu demo de test cart/checkout UI. Khong phai du lieu crawl. |

Crawler/staging tables da co seed va du lieu:

- `crawl_sources`
- `crawl_jobs`
- `crawl_items`
- `crawl_logs`

## Text-only crawl rule

Khi crawl tiep tuc thu thap DB, chi tao/stage du lieu text va structured JSON.

Khong chay:

```powershell
npm.cmd run enrich:pexels
```

Khong tao moi:

- image candidates
- generated images
- thumbnails
- OG images

Neu can gia tri cho cot anh (`hero_image`, `og_image`, `thumbnail`, `images`) thi de `NULL`, chuoi rong, hoac chi dung URL da duoc duyet san.

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
| `20_approved_tour_staging_seed.sql` | Seed staging/demo cho tour da crawl va duyet: locations lien quan, tours, tour_locations, tour_schedules. | 4 locations, 34 tours, 57 mappings, 136 schedules |
| `21_approve_overpass_clean_batch1.sql` | Duyet batch Overpass sach: high priority, co imageUrls, khong co qualityReasons, va bo qua duplicate tai runtime. | 242 candidates |
| `22_approved_blog_guides_seed.sql` | Seed draft blog guide source-backed da duyet, khong copy doan dai tu nguon va khong tao anh. | 18 posts |
| `23_approve_overpass_weak_address_landmarks.sql` | Duyet them landmark/location du lich ro rang chi bi fail `weak_address`; khong publish truc tiep. | 24 candidates |
| `24_approve_overpass_weak_address_services.sql` | Duyet them restaurant/hotel chi fail `weak_address` nhung co it nhat 2 tin hieu van hanh/source. | 11 candidates |
| `25_landing_faq_blocks_seed.sql` | Cap nhat FAQ text-only cho landing pages tu blog guide staging da co source_url. | 4 groups, 14 FAQ |
| `26_cart_items_demo_seed.sql` | Tao gio hang demo cho customer dau tien va tour schedule kha dung. | dynamic |
| `27_published_location_taxonomy_backfill.sql` | Gan tag/amenity cho location da publish tu crawl_items de ho tro loc/tim kiem UI. | dynamic |
| `28_seed_coverage_check.sql` | Bao cao count tung bang va cac issue relation sau khi seed. | read-only |
| `29_live_relation_gap_fix_seed.sql` | Bo sung location destination thieu va mapping tour/blog/location taxonomy tim thay tren live DB. | 10 locations + relation fix |
| `30_live_relation_gap_fix_followup_seed.sql` | Gan relation sau khi destination tu seed 29 da ton tai trong DB. | relation fix |
| `31_archive_test_blog_posts_seed.sql` | Chuyen known test blog posts sang `archived` va xoa `published_at`. | cleanup |
| `32_published_location_minimum_amenity_backfill.sql` | Gan amenity generic theo entity type cho crawl locations da publish nhung con trong amenity. | relation fix |
| `33_hancook_location_taxonomy_fix.sql` | Gan tag/amenity toi thieu cho 2 location HanCook inactive con thieu taxonomy. | relation fix |
| `44_tour_schedule_operational_backfill.sql` | Bo sung departure code/place/deadline va khoa booking lich qua khu. | 300 schedules |
| `45_cleanup_stale_runtime_data.sql` | Don failed jobs, job batches, cache locks va password reset token het han. | runtime cleanup |
| `46_completed_booking_payment_backfill.sql` | Tao payment success cho completed booking bi thieu payment va dong bo booking payment status. | 9 bookings |

Truoc khi apply seed 45 tren live DB, co the sao luu bang:

```powershell
php artisan tinker --execute "require 'D:/DATN/DATN_Tài liệu/database-seeders/backup_runtime_cleanup.php';"
```

Thong ke sau khi ap dung `13_overpass_quality_review_seed.sql`:

| Entity | So luong |
| --- | ---: |
| `location` pending review | 180 |
| `restaurant` pending review | 220 |
| `hotel` pending review | 180 |
| rejected | 360 |
