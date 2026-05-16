# Màn hình Admin — Quản lý khuyến mãi

> Route đề xuất: `/admin/promotions`  
> Trạng thái: Planned  
> Nghiệp vụ tham khảo: travel.com.vn có promotion/ưu đãi và quà tặng trong tour.

---

## Mục tiêu

Quản lý mã giảm giá, ưu đãi, quà tặng và điều kiện áp dụng cho tour/booking.

---

## Thành phần giao diện

| Thành phần | Chức năng |
|---|---|
| Danh sách promotion | Search/filter theo status, thời gian |
| Form tạo/sửa | Code, tên, mô tả, discount, gift |
| Điều kiện áp dụng | Tour, danh mục, giá trị đơn tối thiểu |
| Giới hạn | Số lượt dùng, thời gian hiệu lực |
| Thống kê | used_count, booking đã áp dụng |
| Trạng thái | active/inactive/expired |

---

## API planned

| Method | Endpoint | Mục đích |
|---|---|---|
| GET | `/admin/promotions` | Danh sách |
| GET | `/admin/promotions/{id}` | Chi tiết promotion để xem/sửa |
| POST | `/admin/promotions` | Tạo |
| PUT | `/admin/promotions/{id}` | Cập nhật |
| PATCH | `/admin/promotions/{id}/status` | Bật/tắt |
| DELETE | `/admin/promotions/{id}` | Xóa |
| GET | `/promotions` | Public lấy ưu đãi phù hợp tour/landing |
| POST | `/promotions/validate` | User kiểm tra mã |

---

## Rule nghiệp vụ

| Rule | Mô tả |
|---|---|
| Code unique | Không trùng mã giảm giá |
| Thời gian hiệu lực | Chỉ áp dụng trong `starts_at` - `ends_at` |
| Usage limit | Không vượt quá số lượt dùng |
| Min order | Chỉ áp dụng khi đơn đạt giá trị tối thiểu |
