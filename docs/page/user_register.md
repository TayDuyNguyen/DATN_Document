# Màn hình User — Đăng ký

> Route UI: `/register`  
> Quyền: Public  
> API: `POST /auth/register`

---

## Mục tiêu

Cho phép khách tạo tài khoản mới để đặt tour, lưu yêu thích, đánh giá và nhận thông báo.

---

## Thành phần giao diện

| Khu vực | Thành phần | Ghi chú |
|---|---|---|
| Form đăng ký | Họ tên | `full_name`, bắt buộc |
| Form đăng ký | Tên đăng nhập | `username`, bắt buộc, không trùng |
| Form đăng ký | Email | Bắt buộc, đúng định dạng |
| Form đăng ký | Mật khẩu | Bắt buộc |
| Form đăng ký | Xác nhận mật khẩu | Phải khớp mật khẩu |
| Action chính | Button Đăng ký | Disabled khi form invalid/loading |
| Điều hướng phụ | Đã có tài khoản | Link `/login` |

---

## Luồng xử lý

1. User nhập thông tin đăng ký.
2. Client validate email, mật khẩu, xác nhận mật khẩu.
3. Gọi `POST /auth/register`.
4. Nếu thành công: hiển thị thông báo tạo tài khoản thành công.
5. Điều hướng sang `/verify-email` nếu hệ thống yêu cầu xác thực email, hoặc `/login` nếu cần đăng nhập lại.
6. Nếu thất bại: hiển thị lỗi trùng email/username hoặc lỗi validation.

---

## API sử dụng

| Method | Endpoint | Body | Mô tả |
|---|---|---|---|
| POST | `/auth/register` | `username`, `email`, `password`, `password_confirmation`, `full_name` | Tạo tài khoản mới |

---

## Trạng thái cần xử lý

| Trạng thái | Hiển thị |
|---|---|
| Loading | Button có spinner |
| Email/username trùng | Hiển thị lỗi tại field tương ứng |
| Mật khẩu không khớp | Hiển thị lỗi tại field xác nhận |
| Thành công | Toast/alert và điều hướng |
