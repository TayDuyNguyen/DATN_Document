# Màn hình Admin — Chi tiết giao dịch

> Route UI: `/admin/payments/{id}`  
> Quyền: Admin/Staff  
> API: `GET /admin/payments/{id}`, `POST /admin/payments/{id}/refund`

---

## Mục tiêu

Cho phép quản trị viên kiểm tra chi tiết giao dịch, đối chiếu với đơn đặt tour và thực hiện hoàn tiền khi đủ điều kiện.

---

## Thành phần giao diện

| Khu vực | Thành phần | Chức năng |
|---|---|---|
| Header | Mã giao dịch, trạng thái | Badge trạng thái: pending/success/failed/refunded |
| Thông tin thanh toán | Số tiền, gateway, method, transaction_code | Đối chiếu với cổng thanh toán |
| Thông tin đơn hàng | Booking code, khách hàng, tour, lịch khởi hành | Link sang `/admin/bookings/{id}` |
| Timeline | Các mốc tạo, thanh toán, callback, hoàn tiền | Giúp truy vết xử lý |
| Action | Hoàn tiền | Gọi `POST /admin/payments/{id}/refund` |
| Modal hoàn tiền | Lý do hoàn tiền | Field `refund_reason`, bắt buộc |

---

## API sử dụng

| Method | Endpoint | Mô tả |
|---|---|---|
| GET | `/admin/payments/{id}` | Lấy chi tiết giao dịch |
| POST | `/admin/payments/{id}/refund` | Hoàn tiền giao dịch |

---

## Điều kiện action

| Action | Điều kiện hiển thị |
|---|---|
| Hoàn tiền | Giao dịch thành công, chưa refunded, đơn hàng còn có thể hoàn |
| Xem đơn hàng | Luôn hiển thị nếu payment có booking |
