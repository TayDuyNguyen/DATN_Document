# Cloudinary Media Organization - 2026-06-09

## Mục tiêu

Chuẩn hóa toàn bộ ảnh DanangTrip về một namespace Cloudinary duy nhất:

`dmukxquza/danangtrip/...`

Không dùng link cũ dạng:

- `https://res.cloudinary.com/danangtrip/...`
- thư mục mẫu `samples/...`
- upload rời rạc không có entity id/slug trong public id

## Cấu trúc Cloudinary chính thức

```text
danangtrip/
  branding/
    logo/
    favicon/
    og/
  locations/
    {location_slug}/
      loc-{location_id}__{location_slug}__p01
      loc-{location_id}__{location_slug}__p02
  tours/
    {tour_slug}/
      tour-{tour_id}__{tour_slug}__p01
      tour-{tour_id}__{tour_slug}__p02
  blogs/
    {blog_slug}/
      blog-{blog_id}__{blog_slug}__p01
  users/
    {user_id}__{username}/
      avatar
  payments/
    sepay/
  landing-pages/
    {landing_slug}/
```

## Quy tắc đặt tên

- Public id phải chứa loại dữ liệu, id và slug để map ngược về DB.
- Tên file/local manifest dùng ASCII, không dấu.
- Nội dung tiếng Việt trong DB vẫn giữ UTF-8 có dấu.
- Không xóa ảnh Cloudinary nếu còn xuất hiện trong seed, DB backup, hoặc manifest hiện hành.

## Batch branding hiện hành

Manifest:

`D:\DATN\DATN_Tài liệu\data-center\media-assets\cloudinary-staging\branding\2026-06-09-branding-assets\manifest.csv`

Upload result:

| Setting | Cloudinary URL |
| --- | --- |
| `brand.logo` | `https://res.cloudinary.com/dmukxquza/image/upload/v1781012077/danangtrip/branding/logo/danangtrip-logo.png` |
| `brand.favicon` | `https://res.cloudinary.com/dmukxquza/image/upload/v1781012079/danangtrip/branding/favicon/danangtrip-favicon.png` |
| `seo.og_image` | `https://res.cloudinary.com/dmukxquza/image/upload/v1781012083/danangtrip/branding/og/danangtrip-og-image.jpg` |

Upload:

```powershell
cd D:\DATN\DATN_Tài liệu\danangtrip-crawler
.venv\Scripts\python.exe scripts\upload_cloudinary_assets.py --manifest "D:\DATN\DATN_Tài liệu\data-center\media-assets\cloudinary-staging\branding\2026-06-09-branding-assets\manifest.csv" --results "D:\DATN\DATN_Tài liệu\data-center\media-assets\cloudinary-staging\branding\2026-06-09-branding-assets\upload-results.csv" --results-json "D:\DATN\DATN_Tài liệu\data-center\media-assets\cloudinary-staging\branding\2026-06-09-branding-assets\upload-results.json"
```

## Dọn ảnh cũ

Luôn chạy dry-run trước:

```powershell
cd D:\DATN\DATN_Tài liệu\danangtrip-crawler
.venv\Scripts\python.exe scripts\manage_cloudinary_assets.py audit --prefix samples --used-url-roots "D:\DATN\danangtrip-api\database" "D:\DATN\DATN_Tài liệu\database-seeders" "D:\DATN\DATN_Tài liệu\data-center"
```

Chỉ khi báo cáo xác nhận không có seed đang dùng public id trong `samples`, mới chạy delete:

```powershell
cd D:\DATN\DATN_Tài liệu\danangtrip-crawler
.venv\Scripts\python.exe scripts\manage_cloudinary_assets.py delete-prefix --prefix samples --confirm samples
```

## Kết quả dọn Cloudinary

Đã audit prefix `samples`:

- Tổng asset: 53
- Asset được seed/tài liệu hiện hành tham chiếu: 0
- Asset không còn dùng: 53

Đã xóa prefix `samples` khỏi Cloudinary:

- Requested delete: 53
- Kết quả: 53 asset `deleted`
- Không xoá bất kỳ asset nào trong namespace `danangtrip/...`

Kiểm tra lại sau xoá:

- Prefix `samples`: 0 asset
