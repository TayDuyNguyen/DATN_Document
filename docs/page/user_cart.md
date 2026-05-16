# Màn hình User — Giỏ hàng tour

> Route đề xuất: `/cart`  
> Trạng thái: Planned  
> Tham khảo: travel.com.vn có icon/cart flow trong header và bundle.

---

## Mục tiêu

Cho phép khách lưu một hoặc nhiều tour/lịch khởi hành trước khi checkout.

---

## Thành phần giao diện

| Thành phần | Chức năng |
|---|---|
| Danh sách item | Tour, lịch, số khách, giá |
| Cập nhật số khách | Recalculate giá |
| Xóa item | Xóa khỏi giỏ |
| Mã giảm giá | Áp promotion/coupon nếu có |
| Tổng tiền | Subtotal, discount, final amount |
| Checkout | Chuyển sang nhập thông tin khách |

---

## API planned

| Method | Endpoint | Mục đích |
|---|---|---|
| GET | `/cart` | Lấy giỏ hàng |
| POST | `/cart/items` | Thêm tour vào giỏ |
| PUT | `/cart/items/{id}` | Cập nhật số khách |
| DELETE | `/cart/items/{id}` | Xóa item |
| POST | `/cart/checkout` | Chuyển giỏ thành booking |

---

## Ghi chú

Phase hiện tại có thể bỏ qua giỏ hàng và checkout trực tiếp từ tour detail. Chỉ nên làm cart khi muốn hỗ trợ nhiều item hoặc giữ chỗ tạm.

---

## Validation & States

| Hạng mục | Quy tắc |
|---|---|
| Session | Guest cart cần `X-Session-Id`; user đăng nhập ưu tiên `user_id` |
| Số khách | `quantity_adult >= 1`, `quantity_child >= 0`, `quantity_infant >= 0` |
| Sức chứa | Sau mỗi cập nhật số khách phải kiểm tra lại chỗ còn nhận của `tour_schedule_id` |
| Giá | Không tin giá từ client; subtotal/final amount lấy từ API calculate/checkout |
| Promotion | Mã giảm giá phải validate bằng `POST /promotions/validate` trước checkout |
| Item hết hạn | Nếu lịch khởi hành đã full/cancelled, disable checkout item và yêu cầu chọn lịch khác |
| Empty cart | Hiển thị CTA quay lại `/tours` hoặc landing `/du-lich-da-nang` |
| Checkout lỗi | Giữ item trong giỏ, hiển thị lỗi theo item hoặc theo promotion |
