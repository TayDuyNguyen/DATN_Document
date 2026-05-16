# Màn hình Admin — Báo cáo địa điểm

> Route UI: `/admin/reports/locations`  
> Quyền: Admin/Staff  
> API: `GET /admin/reports/locations`, `GET /admin/locations/export`

---

## Mục tiêu

Đánh giá hiệu quả nội dung địa điểm dựa trên lượt xem, yêu thích, đánh giá và phân bổ theo danh mục/quận.

---

## Bộ lọc

| Bộ lọc | Mô tả |
|---|---|
| Khoảng ngày | Lọc theo thời gian nếu API hỗ trợ |
| Danh mục | Lọc theo `category_id` |
| Quận/huyện | Lọc theo `district` |
| Trạng thái | active/inactive |

---

## Thành phần giao diện

| Khu vực | Thành phần | Chức năng |
|---|---|---|
| KPI | Tổng địa điểm, active, nổi bật | Tổng quan nội dung |
| Chart | Địa điểm theo danh mục/quận | Nhìn phân bổ dữ liệu |
| Bảng top | Top lượt xem | Dựa trên `view_count` hoặc bảng `views` |
| Bảng top | Top yêu thích | Dựa trên `favorite_count` hoặc bảng `favorites` |
| Bảng top | Top đánh giá cao | Dựa trên `avg_rating`, `review_count` |
| Action | Export | Gọi `GET /admin/locations/export` |

---

## API sử dụng

| Method | Endpoint | Mô tả |
|---|---|---|
| GET | `/admin/reports/locations` | Báo cáo địa điểm |
| GET | `/admin/locations/export` | Xuất danh sách địa điểm |

---

## Validation & States

| Hạng mục | Quy tắc |
|---|---|
| Date range | `from <= to`; mặc định 30 ngày gần nhất nếu không truyền filter |
| Category | `category_id` phải tồn tại trong `GET /categories`; nếu không hợp lệ thì bỏ filter |
| District | Chỉ nhận district có trong `GET /locations/districts` |
| Status | Chỉ nhận `active`, `inactive` hoặc bỏ trống |
| Empty data | Nếu không có địa điểm trong khoảng lọc, hiển thị empty chart/table và vẫn cho export |
| Export | Export dùng cùng bộ lọc với màn hiện tại để tránh lệch số liệu |
