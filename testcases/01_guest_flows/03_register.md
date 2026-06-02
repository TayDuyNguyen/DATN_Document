# Màn hình Đăng ký (Register Page)

## Phạm vi

- Route: `/register` hoặc `/[locale]/register`
- API liên quan: `/api/auth/register` (POST)
- Vai trò: Khách chưa đăng nhập (Guest).

## Điều kiện trước

- Môi trường: Local dev server (`http://localhost:3000`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_REGISTER_001 | Trường bắt buộc | Kiểm tra lỗi khi gửi form trống | Màn hình đăng ký mở sẵn | Để trống toàn bộ thông tin và nhấn "ĐĂNG KÝ". | | Hiển thị cảnh báo điền đầy đủ các trường bắt buộc (`name`, `email`, `password`, `confirmPassword`). | | | |
| 2 | TC_REGISTER_002 | Họ và tên | Kiểm tra trường Họ và tên quá ngắn hoặc rỗng | | 1. Nhập Họ và tên dưới 2 ký tự.<br>2. Nhập các trường khác hợp lệ.<br>3. Nhấn "ĐĂNG KÝ". | Name: `A` | Hiển thị thông báo lỗi yêu cầu Họ tên tối thiểu 2 ký tự hoặc không được để trống. | | | |
| 3 | TC_REGISTER_003 | Validate Email | Kiểm tra định dạng Email không hợp lệ | | 1. Nhập email sai định dạng.<br>2. Nhập các trường khác hợp lệ.<br>3. Nhấn "ĐĂNG KÝ". | Email: `user@test` | Hiển thị thông báo lỗi Email không đúng định dạng. | | | |
| 4 | TC_REGISTER_004 | Độ mạnh mật khẩu | Kiểm tra mật khẩu yếu (Không đủ ký tự hoặc thiếu loại ký tự) | | 1. Nhập mật khẩu dưới 8 ký tự.<br>2. Nhập các trường khác hợp lệ.<br>3. Nhấn "ĐĂNG KÝ". | Password: `12345`<br>Confirm: `12345` | Hiển thị lỗi độ mạnh mật khẩu (yêu cầu tối thiểu 8 ký tự, bao gồm chữ hoa, chữ thường, số, ký tự đặc biệt). | | | |
| 5 | TC_REGISTER_005 | Khớp mật khẩu | Kiểm tra Xác nhận mật khẩu không khớp | | 1. Nhập Mật khẩu hợp lệ.<br>2. Nhập Xác nhận mật khẩu khác với Mật khẩu đã nhập.<br>3. Nhấn "ĐĂNG KÝ". | Password: `Password123!`<br>Confirm: `Password123?` | Chặn gửi form và hiển thị cảnh báo xác nhận mật khẩu không trùng khớp. | | | |
| 6 | TC_REGISTER_006 | Trùng Email | Đăng ký với Email đã tồn tại trong hệ thống | Có tài khoản `exist@test.com` trong hệ thống | 1. Nhập Họ tên hợp lệ.<br>2. Nhập Email đã tồn tại.<br>3. Nhập mật khẩu hợp lệ.<br>4. Nhấn "ĐĂNG KÝ". | Email: `exist@test.com`<br>Password: `Password123!` | Nhận phản hồi lỗi từ API. Hiển thị thông báo lỗi (ví dụ: "Email đã được sử dụng") ở khung thông báo lỗi. | | | |
| 7 | TC_REGISTER_007 | Đăng ký thành công | Kiểm tra đăng ký thành công với thông tin hợp lệ | Email chưa tồn tại | 1. Nhập đầy đủ thông tin hợp lệ ở tất cả các trường.<br>2. Nhấn "ĐĂNG KÝ". | Name: `Nguyen Van A`<br>Email: `newuser@test.com`<br>Password: `Password123!` | Đăng ký thành công:<br>- Hiển thị toast thông báo thành công.<br>- Chuyển hướng người dùng sang màn hình Đăng nhập (`/login`) hoặc tự động gửi email kích hoạt tài khoản. | | | |
| 8 | TC_REGISTER_008 | Link điều hướng | Kiểm tra nút chuyển sang màn hình Đăng nhập | | Click vào liên kết "Đăng nhập ngay". | | Chuyển hướng chính xác đến trang Đăng nhập (`/login`). | | | |

## Ghi chú

-
