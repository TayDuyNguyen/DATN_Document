# DanangTrip Database Refresh

Folder này là điểm chạy một lệnh cho database DanangTrip.

## Rebuild từ đầu

Chỉ dùng khi muốn xóa toàn bộ dữ liệu DB hiện tại, chạy lại migration và seed mới nhất:

```powershell
powershell -ExecutionPolicy Bypass -File "D:\DATN\DATN_Tài liệu\data-center\database-refresh\RUN_REBUILD_DATABASE.ps1"
```

Script sẽ:

- backup DB hiện tại vào `D:\DATN\DATN_Tài liệu\data-center\backups`
- chạy `php artisan migrate:fresh --force`
- chạy full seed manifest trong `D:\DATN\DATN_Tài liệu\database-seeders`
- chạy sync trạng thái lịch tour theo ngày hiện tại
- chạy audit chất lượng dữ liệu
- chạy test schedule backend

## Update DB hiện tại

Dùng khi không muốn xóa DB, chỉ áp dụng seed backfill/polish mới nhất:

```powershell
powershell -ExecutionPolicy Bypass -File "D:\DATN\DATN_Tài liệu\data-center\database-refresh\RUN_INCREMENTAL_UPDATE.ps1"
```

Lưu ý: seed tour thật có lịch rolling theo ngày hiện tại. Khi chạy sau một tuần mới, DB có thể có thêm lịch tương lai mới cho 30 tour đã xác minh; các lịch cũ sẽ bị khóa booking, không còn mở bán sai ngày. Không tạo duplicate cùng `tour_id + start_date`.

## Chỉ audit

```powershell
powershell -ExecutionPolicy Bypass -File "D:\DATN\DATN_Tài liệu\data-center\database-refresh\RUN_AUDIT_DATABASE.ps1"
```

Script audit cũng chạy `php artisan tour-schedules:sync-availability` trước khi kiểm tra để không còn lịch đã qua ngày/deadline nhưng vẫn mở booking.
Ngoài audit toàn DB, script còn chạy `audit_locations_vietnamese_detailed.php` để bắt các cụm tiếng Việt không dấu trộn trong tên, địa chỉ và mô tả địa điểm; tên thương hiệu quốc tế được thống kê riêng.

## Canonical data locations

- SQL seed chính: `D:\DATN\DATN_Tài liệu\database-seeders`
- Raw/normalized crawler data: `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data`
- Media/Cloudinary staging: `D:\DATN\DATN_Tài liệu\data-center\media-assets`
- Reports: `D:\DATN\DATN_Tài liệu\data-center\reports`
- Backups: `D:\DATN\DATN_Tài liệu\data-center\backups`

Seed cuối hiện tại:

- `51_database_quality_polish_seed.sql`
- `52_public_vietnamese_content_seed.sql`
- `53_tour_schedule_current_date_guard_seed.sql`
- `54_cleanup_expired_auth_runtime_seed.sql`
- `55_location_catalog_editorial_vi_seed.sql`
- `56_ratings_editorial_vi_and_volume_seed.sql`

Các seed này phải nằm cuối manifest để dữ liệu sau rebuild giữ quan hệ đầy đủ, media đầy đủ, không mojibake, location đúng slug/taxonomy, public text và bình luận đánh giá là tiếng Việt có dấu, rating aggregate đồng bộ, lịch tour đúng theo ngày hiện tại và runtime không giữ token/session hết hạn.
