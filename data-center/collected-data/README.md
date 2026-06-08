# Collected Data Snapshot

Folder này gom snapshot dữ liệu đã thu thập và seed hiện hành để dễ kiểm tra, đối chiếu và bàn giao.

## Nội dung

- `crawler-data-snapshot/`
  - bản sao các file `.json` và `.csv` từ `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data`
  - dùng để đối chiếu dữ liệu raw/normalized/review đã crawl
- `database-seeders-snapshot/`
  - bản sao các file `.sql`, `seed-manifest.json`, `apply_database_seeders.ps1` từ `D:\DATN\DATN_Tài liệu\database-seeders`
  - snapshot tại thời điểm dữ liệu đã được chuẩn hóa tiếng Việt có dấu, location đã được sửa theo slug/taxonomy, ratings đã được tăng volume/tính lại aggregate, có seed chốt lịch theo ngày hiện tại và cleanup runtime hết hạn

## Lưu ý vận hành

Nguồn chạy thật vẫn là:

- `D:\DATN\DATN_Tài liệu\database-seeders`
- `D:\DATN\DATN_Tài liệu\data-center\database-refresh`

Không chạy seed trực tiếp từ snapshot trừ khi cần phục hồi/tham chiếu. Để rebuild DB, dùng:

```powershell
powershell -ExecutionPolicy Bypass -File "D:\DATN\DATN_Tài liệu\data-center\database-refresh\RUN_REBUILD_DATABASE.ps1"
```

Để update DB hiện tại mà không xóa dữ liệu:

```powershell
powershell -ExecutionPolicy Bypass -File "D:\DATN\DATN_Tài liệu\data-center\database-refresh\RUN_INCREMENTAL_UPDATE.ps1"
```

Để chỉ kiểm tra chất lượng dữ liệu:

```powershell
powershell -ExecutionPolicy Bypass -File "D:\DATN\DATN_Tài liệu\data-center\database-refresh\RUN_AUDIT_DATABASE.ps1"
```
