# Màn hình Xác thực Email (Verify Email Page)

## Phạm vi

- Route: `/verify-email` hoặc `/[locale]/verify-email`
- API liên quan: `/api/auth/verify-email` (POST), `/api/auth/resend-verification` (POST)
- Vai trò: Khách chưa đăng nhập (đang trong luồng đăng ký hoặc xác minh tài khoản).

## Điều kiện trước

- Người dùng vừa thực hiện đăng ký và có mã OTP gửi về Email.
- Môi trường: Local dev server (`http://localhost:3000`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_VERIFY_001 | OTP Input auto-focus | Kiểm tra tự động nhảy con trỏ khi nhập OTP | Màn hình xác thực mở sẵn | 1. Nhấp vào ô nhập OTP đầu tiên.<br>2. Nhập một chữ số bất kỳ. | Dữ liệu: `1` | Con trỏ tự động nhảy sang ô nhập thứ 2 mà không cần bấm Tab. | | | |
| 2 | TC_VERIFY_002 | Nhập thiếu ký tự | Gửi mã OTP chưa đủ số lượng ký tự | | 1. Chỉ nhập 4 chữ số vào ô OTP.<br>2. Nhấn nút "XÁC NHẬN". | OTP: `1234` | Hiển thị thông báo yêu cầu điền đầy đủ mã xác thực (ví dụ: cần 6 chữ số). | | | |
| 3 | TC_VERIFY_003 | Sai mã OTP | Nhập sai mã OTP | | 1. Nhập đủ 6 số nhưng sai mã gửi về email.<br>2. Nhấn nút "XÁC NHẬN". | OTP: `999999` | Gửi yêu cầu lên hệ thống và nhận phản hồi lỗi từ API. Hiển thị thông báo lỗi (ví dụ: "Mã xác thực không chính xác"). | | | |
| 4 | TC_VERIFY_004 | Xác thực thành công | Nhập đúng mã OTP xác thực | Tài khoản chưa xác thực có mã hợp lệ | 1. Nhập chính xác 6 chữ số OTP được gửi về Email.<br>2. Nhấn nút "XÁC NHẬN". | OTP: `[OTP từ Email]` | Xác thực thành công:<br>- Hiển thị thông báo xác thực thành công.<br>- Chuyển hướng người dùng sang trang Đăng nhập (`/login`) hoặc tự động đăng nhập đưa vào trang chủ. | | | |
| 5 | TC_VERIFY_005 | Gửi lại mã (Resend OTP) | Kiểm tra chức năng gửi lại mã và bộ đếm ngược thời gian | Mã cũ hết hạn hoặc không nhận được | Click nút "Gửi lại mã". | | - Hệ thống kích hoạt gửi lại mã OTP mới về Email.<br>- Nút "Gửi lại mã" bị vô hiệu hóa (disabled).<br>- Bộ đếm ngược thời gian (ví dụ: 60s) xuất hiện và đếm ngược về 0 trước khi cho phép bấm lại. | | | |

## Ghi chú

-
