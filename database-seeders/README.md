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
45. `45_cleanup_stale_runtime_data.sql` don du lieu runtime het han
46. `46_completed_booking_payment_backfill.sql` dong bo payment cho booking completed
47. `47_canonical_display_text_utf8_seed.sql` khoi phuc display text UTF-8 da audit
48. `48_deactivate_duplicate_catalog_seed.sql` dong cac ban sao catalog nhung giu lich su
49. `49_verified_real_tours_seed.sql` upsert 30 tour that da xac minh, anh Cloudinary, mapping diem den va lich tuong lai
50. `50_verified_real_tours_editorial_vi_seed.sql` bien tap tieng Viet va active 30 tour that da duyet
51. `51_database_quality_polish_seed.sql` fix audit cuoi: relation gaps, thumbnail/image thieu, draft blog, duplicate departure_code va text khong dau
52. `52_public_vietnamese_content_seed.sql` chot public-facing content sang tieng Viet co dau tren locations/tours/blog/landing/promotions
53. `53_tour_schedule_current_date_guard_seed.sql` khoa booking cac lich da qua ngay/deadline/full/cancelled va dong bo tour availability theo ngay hien tai
54. `54_cleanup_expired_auth_runtime_seed.sql` don password reset token, refresh token, session/cache runtime da het han
55. `55_location_catalog_editorial_vi_seed.sql` sua toan bo location theo slug: ten/dia chi/mo ta tieng Viet, taxonomy va cac ban ghi bi lech noi dung
56. `56_ratings_editorial_vi_and_volume_seed.sql` sua binh luan danh gia co dau, tang volume danh gia va tinh lai rating aggregate
57. `57_recent_operational_activity_seed.sql` tao luong hoat dong demo gan day
58. `58_public_taxonomy_visibility_seed.sql` an taxonomy public rong
59. `59_ratings_admin_read_state_seed.sql` khoi tao trang thai Moi/Da xem cho ratings
60. `60_search_logs_vietnamese_diacritics_seed.sql` chuan hoa search trends sang tieng Viet co dau
61. `61_dashboard_search_activity_seed.sql` bo sung log tim kiem/click/zero-result gan day cho dashboard admin

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
- `Mode Incremental` chạy các seed backfill hiện hành và kết thúc bằng lớp chốt dữ liệu vận hành/search `61`.
- Script dung Laravel `php artisan tinker`, nen se dung dung ket noi DB trong `D:\DATN\danangtrip-api\.env`.
- `47_canonical_display_text_utf8_seed.sql` phải chạy sau các seed legacy để dữ liệu hiển thị giữ đầy đủ dấu tiếng Việt; các seed `48-56` là lớp chốt chất lượng sau canonical text.

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
- Nội dung hiển thị bằng tiếng Việt phải dùng UTF-8 và đầy đủ dấu. Chỉ slug, URL, tên file và định danh kỹ thuật dùng ASCII.
- Du lieu crawl tu Overpass duoc nap vao bang staging `crawl_items` voi `status = pending_review`, khong ghi thang vao `locations`.
- Can admin/agent loc trung, kiem tra ten-dia chi-toa do-anh truoc khi publish sang bang chinh.
- `16_crawl_publish_approved_locations.sql` chi publish item co `status = approved`, khong bi trung production, va publish vao `locations.status = inactive` de admin bat active sau.

## Chuẩn hóa encoding

Các file SQL phải được lưu bằng UTF-8. Kiểm tra lỗi mojibake và tiếng Việt không dấu bằng:

```powershell
cd D:\DATN\DATN_Tài liệu\danangtrip-crawler
.venv\Scripts\python.exe scripts\audit_vietnamese_diacritics.py
.venv\Scripts\python.exe scripts\audit_mojibake.py

cd D:\DATN\DATN_Tài liệu\database-seeders
php audit_vietnamese_diacritics_db.php
php audit_mojibake_db.php
```

Không dùng kiểm tra “chỉ ASCII” cho nội dung hiển thị vì cách này làm mất dấu tiếng Việt.
Không chạy `normalize:seeders` trên seed UTF-8 hiện hành vì script legacy này loại bỏ dấu.

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
| `47_canonical_display_text_utf8_seed.sql` | Khôi phục các trường hiển thị UTF-8 từ database đã audit sạch; chạy cuối full/incremental. | 1,139 rows |
| `48_deactivate_duplicate_catalog_seed.sql` | Giữ một tour active cho mỗi nhóm nội dung trùng, đóng các bản sao và archive blog Copy; không xóa lịch sử. | 60 tours + 1 blog |
| `49_verified_real_tours_seed.sql` | Upsert catalog tour thật đã xác minh; giữ inactive chờ duyệt, dùng ảnh Cloudinary và sinh lịch tương lai. | 30 tours + 46 mappings + 240 schedules |
| `50_verified_real_tours_editorial_vi_seed.sql` | Cập nhật tiêu đề, mô tả, itinerary/inclusions/exclusions tiếng Việt và chuyển 30 tour thật sang active. | 30 tours active |
| `55_location_catalog_editorial_vi_seed.sql` | Chuẩn hóa nội dung, địa chỉ và taxonomy location theo slug ổn định. | 112 locations |
| `56_ratings_editorial_vi_and_volume_seed.sql` | Chuẩn hóa đánh giá tiếng Việt, tăng độ phủ và đồng bộ rating aggregate. | 620 ratings |
| `57_recent_operational_activity_seed.sql` | Tạo luồng hoạt động demo gần đây, sửa pending cũ và đồng bộ bộ đếm engagement/booking. | 24 bookings + activity rolling |
| `58_public_taxonomy_visibility_seed.sql` | Ẩn taxonomy public rỗng và xóa blog category mồ côi không có quan hệ. | dynamic |
| `59_ratings_admin_read_state_seed.sql` | Khởi tạo trạng thái Mới/Đã xem cho rating lịch sử đúng một lần, không ghi đè thao tác admin khi chạy incremental. | dynamic |
| `60_search_logs_vietnamese_diacritics_seed.sql` | Chuẩn hóa từ khóa search logs sang tiếng Việt có dấu cho dashboard search trends. | dynamic |
| `61_dashboard_search_activity_seed.sql` | Bổ sung search logs gần đây có keyword, click item và zero-result để 4 panel search dashboard có dữ liệu kiểm thử. | dynamic |

Seed `57` chỉ mô phỏng hoạt động vận hành, không phải dữ liệu khách hàng thật. Các bản ghi do seed tạo có prefix `DEMO-ACT-` hoặc `demo-activity-` để nhận diện và chạy lặp không tăng số lượng ngoài kiểm soát.

Kiểm tra riêng độ mới và tính nhất quán hoạt động:

```powershell
cd D:\DATN\danangtrip-api
php artisan tinker --execute "require 'D:/DATN/DATN_Tài liệu/database-seeders/audit_operational_activity.php';"
```

Cập nhật toàn bộ seed incremental, lịch tour, audit và test:

```powershell
powershell -ExecutionPolicy Bypass -File "D:\DATN\DATN_Tài liệu\data-center\database-refresh\RUN_INCREMENTAL_UPDATE.ps1"
```

Seed `49` được tái sinh bằng:

```powershell
cd D:\DATN\DATN_Tài liệu\danangtrip-crawler
.venv\Scripts\python.exe scripts\generate_verified_real_tour_seed.py
```

Seed `49` tạo lịch rolling theo `CURRENT_DATE` cho tour thật đã xác minh. Chạy lại vào tuần mới có thể thêm lịch tương lai mới, nhưng không tạo duplicate cùng `tour_id + start_date`; seed `53` và command `tour-schedules:sync-availability` sẽ khóa booking cho lịch đã qua ngày/deadline.

Seed `50` được tái sinh bằng:

```powershell
cd D:\DATN\DATN_Tài liệu\danangtrip-crawler
.venv\Scripts\python.exe scripts\generate_verified_real_tour_editorial_seed.py
```

Trước khi áp dụng seed `49`, backup các tour cùng slug bằng:

```powershell
cd D:\DATN\danangtrip-api
php artisan tinker --execute "require 'D:/DATN/DATN_Tài liệu/database-seeders/backup_verified_real_tour_import.php';"
```

Seed `47` được tái sinh bằng:

```powershell
cd D:\DATN\DATN_Tài liệu\database-seeders
php generate_canonical_display_text_seed.php
```

Các JSON crawl `raw` và SQL cũ trước ngày 2026-06-07 được xem là artifact lịch sử. Không dùng chúng làm nguồn nội dung hiển thị cuối cùng nếu chưa qua pipeline UTF-8 và audit dấu tiếng Việt.

Kiểm tra duplicate catalog:

```powershell
cd D:\DATN\DATN_Tài liệu\database-seeders
php audit_duplicate_entities.php
```

Không xóa tour đã có booking, rating, favorite, view hoặc schedule. Duplicate catalog phải được chuyển `inactive` để giữ nguyên lịch sử giao dịch.

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
