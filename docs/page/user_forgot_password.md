# Màn hình User — Quên mật khẩu

> Route UI: `/forgot-password`  
> Quyền: Public  
> API: `POST /auth/forgot-password`

---

## Mục tiêu

Cho phép người dùng yêu cầu gửi email đặt lại mật khẩu.

---

## Thành phần giao diện

| Khu vực | Thành phần | Ghi chú |
|---|---|---|
| Form | Email | Bắt buộc, đúng định dạng |
| Action chính | Gửi link đặt lại mật khẩu | Gọi API |
| Điều hướng phụ | Quay lại đăng nhập | Link `/login` |
| Feedback | Thông báo đã gửi | Không nên tiết lộ email có tồn tại hay không |

---

## Luồng xử lý

1. User nhập email.
2. Client validate email.
3. Gọi `POST /auth/forgot-password`.
4. Hiển thị thông báo kiểm tra email nếu API trả về thành công.
5. Nếu lỗi validation/server: hiển thị lỗi phù hợp.

---

## API sử dụng

| Method | Endpoint | Body | Mô tả |
|---|---|---|---|
| POST | `/auth/forgot-password` | `email` | Gửi email reset mật khẩu |
