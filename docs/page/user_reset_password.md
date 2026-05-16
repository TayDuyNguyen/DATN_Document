# Màn hình User — Đặt lại mật khẩu

> Route UI: `/reset-password`  
> Quyền: Public  
> API: `POST /auth/reset-password`

---

## Mục tiêu

Cho phép người dùng đặt mật khẩu mới bằng token nhận từ email.

---

## Thành phần giao diện

| Khu vực | Thành phần | Ghi chú |
|---|---|---|
| Hidden/query | Token | Lấy từ URL hoặc form |
| Form | Email | Có thể lấy từ URL hoặc user nhập |
| Form | Mật khẩu mới | Bắt buộc |
| Form | Xác nhận mật khẩu | Phải khớp |
| Action chính | Đặt lại mật khẩu | Gọi API |
| Điều hướng phụ | Quay lại đăng nhập | Link `/login` |

---

## Luồng xử lý

1. Mở link reset từ email, đọc `token` và `email` nếu có.
2. User nhập mật khẩu mới và xác nhận.
3. Gọi `POST /auth/reset-password`.
4. Nếu thành công: hiển thị thông báo và chuyển `/login`.
5. Nếu token hết hạn/sai: hiển thị lỗi và link gửi lại yêu cầu quên mật khẩu.

---

## API sử dụng

| Method | Endpoint | Body | Mô tả |
|---|---|---|---|
| POST | `/auth/reset-password` | `token`, `email`, `password`, `password_confirmation` | Đặt lại mật khẩu |
