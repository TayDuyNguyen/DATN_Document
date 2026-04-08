# Màn hình: Chi tiết Đơn đặt theo Mã đơn

> Route: `/bookings/code/{booking_code}`
> Quyền: 🔐 Cần đăng nhập
> Mô tả: Xem chi tiết đơn đặt tour bằng mã đơn hàng (booking_code). Thường dùng khi user click link từ email xác nhận.

---

## Tái sử dụng hoàn toàn từ màn Chi tiết Đơn đặt

> Xem chi tiết tại `user_booking_detail.md`

Layout, sections và tất cả components giống hệt màn `/bookings/{id}`.

---

## Điểm khác biệt duy nhất

### 1. API khác

| Màn 7.2 | Màn 7.3 |
|---------|---------|
| `GET /user/bookings/{id}` | `GET /user/bookings/code/{booking_code}` |
| URL param: `id` (number) | URL param: `booking_code` (string, e.g. "BK-1008") |

### 2. Breadcrumb

`"Trang chủ / Đơn đặt tour / BK-1008" 13px #94A3B8`
(dùng booking_code thay vì id)

### 3. Use case chính

Màn này được truy cập từ:
- Link trong **email xác nhận đặt tour**: `danangtrip.vn/bookings/code/BK-1008`
- Link trong **email thông báo** từ hệ thống
- User tìm kiếm đơn bằng mã đơn

---

## API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load chi tiết | GET | `/user/bookings/code/{booking_code}` | Khi mount |
| Hủy đơn | POST | `/user/bookings/{id}/cancel` | Confirm dialog (dùng id từ response) |
| In hóa đơn | GET | `/user/bookings/{id}/invoice` | Click "In hóa đơn" (dùng id từ response) |
