# Màn hình Admin — Báo cáo người dùng

> Route UI: `/admin/reports/users`  
> Quyền: Admin/Staff  
> API: `GET /admin/reports/users`, `GET /admin/users/export`

---

## Mục tiêu

Theo dõi tăng trưởng người dùng, phân bổ trạng thái/role và hỗ trợ xuất dữ liệu phục vụ báo cáo.

---

## Bộ lọc

| Bộ lọc | Mô tả |
|---|---|
| Năm | Mặc định năm hiện tại |
| Khoảng ngày | Dùng nếu API hỗ trợ `from`, `to` |
| Role | user/staff/admin |
| Status | active/banned |

---

## Thành phần giao diện

| Khu vực | Thành phần | Chức năng |
|---|---|---|
| KPI | Tổng user, user mới, tỉ lệ active | Xem nhanh sức khỏe hệ thống |
| Chart | User mới theo tháng | Dữ liệu từ `GET /admin/reports/users` |
| Chart phụ | Phân bố role/status | Hiển thị nếu API trả dữ liệu |
| Bảng | Tháng, user mới, tổng lũy kế | So sánh theo thời gian |
| Action | Export | Gọi `GET /admin/users/export` |

---

## API sử dụng

| Method | Endpoint | Mô tả |
|---|---|---|
| GET | `/admin/reports/users` | Báo cáo user mới theo tháng/năm |
| GET | `/admin/users/export` | Xuất danh sách user |

---

## Validation & States

| Hạng mục | Quy tắc |
|---|---|
| Year | Chỉ nhận năm dạng 4 chữ số, không lớn hơn năm hiện tại |
| Role/status filter | Nếu bổ sung filter, chỉ nhận role/status có trong hệ thống |
| Empty chart | Nếu chưa có user mới, chart vẫn hiển thị đủ 12 tháng với giá trị 0 |
| Export | File export phải dùng cùng `year`, `role`, `status` đang chọn |
| Permission | Chỉ admin/staff được xem; thiếu quyền chuyển 403 |
