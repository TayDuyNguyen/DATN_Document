# Màn hình User — Đăng nhập

> Route UI: `/login`  
> Quyền: Public  
> API: `POST /auth/login`

---

## Mục tiêu

Cho phép người dùng đăng nhập bằng email và mật khẩu để sử dụng các chức năng cần tài khoản: đặt tour, thanh toán, yêu thích, đánh giá, thông báo, hồ sơ cá nhân.

---

## Thành phần giao diện

| Khu vực | Thành phần | Ghi chú |
|---|---|---|
| Form đăng nhập | Email | Bắt buộc, đúng định dạng email |
| Form đăng nhập | Mật khẩu | Bắt buộc, có nút ẩn/hiện mật khẩu |
| Action chính | Button Đăng nhập | Disabled khi form invalid/loading |
| Điều hướng phụ | Quên mật khẩu | Link `/forgot-password` |
| Điều hướng phụ | Đăng ký | Link `/register` |
| Feedback | Alert lỗi | Sai thông tin, tài khoản bị khóa, lỗi server |

---

## Luồng xử lý

1. User nhập email và mật khẩu.
2. Client validate dữ liệu bắt buộc.
3. Gọi `POST /auth/login`.
4. Nếu thành công: lưu access token, refresh token nếu API trả về, lưu user profile.
5. Điều hướng:
   - Nếu có `redirect` query: quay lại trang trước đó.
   - Nếu user role là `admin` hoặc `staff`: có thể chuyển `/admin/dashboard` nếu dùng chung frontend.
   - Mặc định chuyển `/`.
6. Nếu thất bại: hiển thị lỗi ngay dưới form.

---

## API sử dụng

| Method | Endpoint | Body | Mô tả |
|---|---|---|---|
| POST | `/auth/login` | `email`, `password` | Đăng nhập và nhận JWT |

---

## Trạng thái cần xử lý

| Trạng thái | Hiển thị |
|---|---|
| Loading | Button có spinner, không cho submit lại |
| Sai thông tin | Alert "Email hoặc mật khẩu không đúng" |
| Tài khoản bị khóa | Alert theo message API |
| Server error | Alert lỗi chung |
