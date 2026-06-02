# Màn hình Quên mật khẩu & Đặt lại mật khẩu (Forgot & Reset Password)

## Phạm vi

- Route: `/forgot-password`, `/reset-password`
- API liên quan: `/api/auth/forgot-password` (POST), `/api/auth/reset-password` (POST)
- Vai trò: Khách chưa đăng nhập (Guest).

## Điều kiện trước

- Môi trường: Local dev server (`http://localhost:3000`).

## Test cases

### Phần 1: Yêu cầu đặt lại mật khẩu (Forgot Password)

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_FORGOT_001 | Trường bắt buộc | Kiểm tra khi gửi Email rỗng | Màn hình quên mật khẩu mở sẵn | Click nút gửi mà không điền Email. | | Hiển thị thông báo yêu cầu nhập Email. | | | |
| 2 | TC_FORGOT_002 | Định dạng Email | Kiểm tra nhập email sai định dạng | | 1. Nhập email sai cú pháp.<br>2. Nhấn nút Gửi. | Email: `abc.com` | Hiển thị lỗi định dạng Email không hợp lệ. | | | |
| 3 | TC_FORGOT_003 | Email không tồn tại | Gửi yêu cầu với Email chưa đăng ký | | 1. Nhập email hợp lệ nhưng chưa từng đăng ký tài khoản.<br>2. Nhấn nút Gửi. | Email: `notfound@test.com` | Hiển thị lỗi "Email không tồn tại" hoặc thông báo gửi mã xác nhận thất bại tùy chính sách bảo mật API. | | | |
| 4 | TC_FORGOT_004 | Yêu cầu thành công | Gửi yêu cầu thành công với Email hợp lệ | Tài khoản tồn tại trong DB | 1. Nhập Email chính xác đã đăng ký.<br>2. Nhấn nút Gửi. | Email: `user@test.com` | Hiển thị thông báo thành công (ví dụ: "Đã gửi liên kết/mã đặt lại mật khẩu đến Email của bạn"). Người dùng nhận được mã xác nhận/OTP. | | | |

### Phần 2: Đặt lại mật khẩu mới (Reset Password)

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 5 | TC_RESET_001 | Mã OTP / Token | Kiểm tra khi mã OTP / Token đặt lại không hợp lệ hoặc hết hạn | Có trang Đặt lại mật khẩu | 1. Nhập mã OTP sai hoặc hết hạn.<br>2. Nhập mật khẩu mới hợp lệ.<br>3. Nhấn "ĐẶT LẠI MẬT KHẨU". | OTP: `123456`<br>Password: `NewPassword123!` | Hiển thị lỗi thông báo mã xác thực không chính xác hoặc đã hết hạn. | | | |
| 6 | TC_RESET_002 | Khớp mật khẩu | Kiểm tra Xác nhận mật khẩu không khớp mật khẩu mới | | 1. Nhập mã OTP hợp lệ.<br>2. Nhập Mật khẩu mới.<br>3. Nhập Xác nhận mật khẩu khác.<br>4. Nhấn "ĐẶT LẠI MẬT KHẨU". | Password: `NewPassword123!`<br>Confirm: `NewPassword123?` | Cảnh báo xác nhận mật khẩu không trùng khớp, không cho gửi form. | | | |
| 7 | TC_RESET_003 | Đặt lại mật khẩu thành công | Kiểm tra quy trình hoàn tất đặt lại mật khẩu | Đã có mã OTP hợp lệ | 1. Nhập đúng mã OTP.<br>2. Nhập mật khẩu mới và xác nhận mật khẩu trùng khớp.<br>3. Nhấn "ĐẶT LẠI MẬT KHẨU". | OTP: `[Mã đúng]`<br>Password: `NewPassword123!` | Đổi mật khẩu thành công:<br>- Hiển thị toast thông báo thành công.<br>- Chuyển hướng người dùng về trang Đăng nhập (`/login`). | | | |

## Ghi chú

-
