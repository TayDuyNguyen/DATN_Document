# Màn hình User — Chọn lịch khởi hành tour

> Route đề xuất: modal trong `/tours/{slug}` hoặc `/tours/{slug}/departures`  
> Quyền: Public/User  
> API: `GET /tours/{id}/schedules`, `POST /tours/{id}/check-availability`, `POST /bookings/calculate`

---

## Mục tiêu

Cho phép khách chọn đúng ngày khởi hành, số lượng khách và kiểm tra còn chỗ trước khi đặt tour.

---

## Thành phần giao diện

| Thành phần | Chức năng |
|---|---|
| Danh sách lịch | Ngày đi, ngày về, giá, trạng thái |
| Badge chỗ còn nhận | Hiển thị số chỗ còn lại |
| Stepper số khách | Người lớn, trẻ em, em bé |
| Giá tạm tính | Tính theo lịch và số khách |
| Button tiếp tục | Chuyển sang `/tours/{slug}/book` |
| Trạng thái full | Disable lịch hết chỗ |

---

## API sử dụng

| Method | Endpoint | Mục đích |
|---|---|---|
| GET | `/tours/{id}/schedules` | Lấy lịch khởi hành |
| POST | `/tours/{id}/check-availability` | Kiểm tra chỗ |
| POST | `/bookings/calculate` | Tính tổng tiền |

---

## Rule nghiệp vụ

| Rule | Mô tả |
|---|---|
| Người lớn | Bắt buộc ít nhất 1 |
| Trẻ em/em bé | Có thể bằng 0 |
| Chỗ còn nhận | `max_people - booked_people` hiện tại; phase sau trừ thêm `locked_people` |
| Hết hạn đặt | Nếu có `booking_deadline`, không cho chọn lịch quá hạn |
