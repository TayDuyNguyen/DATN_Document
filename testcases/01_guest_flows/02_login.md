# Màn hình Đăng nhập (Login Page)

## Phạm vi

- Route: `/login` hoặc `/[locale]/login`
- API liên quan: `/api/auth/login` (POST)
- Vai trò: Khách chưa đăng nhập (Guest).

## Điều kiện trước

- Tài khoản: Đã có tài khoản đăng ký trước trong database (ví dụ: `user@test.com` mật khẩu `Password123!`).
- Môi trường: Local dev server (`http://localhost:3000`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_LOGIN_001 | Trường bắt buộc | Kiểm tra thông báo lỗi khi để trống tất cả các trường | Màn hình đăng nhập mở sẵn | 1. Để trống Email và Mật khẩu.<br>2. Click nút "ĐĂNG NHẬP". | | Trình duyệt ngăn submit do thuộc tính `required` hoặc hiển thị thông báo yêu cầu nhập Email / Password. | | | |
| 2 | TC_LOGIN_002 | Validate Email | Kiểm tra định dạng Email không hợp lệ | Màn hình đăng nhập mở sẵn | 1. Nhập email sai định dạng.<br>2. Nhập mật khẩu hợp lệ.<br>3. Click nút "ĐĂNG NHẬP". | Email: `testinvalidemail`<br>Password: `12345678` | Hiển thị cảnh báo định dạng Email không hợp lệ từ input validation của trình duyệt hoặc form validator. | | | |
| 3 | TC_LOGIN_003 | Đăng nhập thất bại | Đăng nhập với tài khoản chưa đăng ký | Màn hình đăng nhập mở sẵn | 1. Nhập Email chưa đăng ký.<br>2. Nhập Mật khẩu bất kỳ.<br>3. Click nút "ĐĂNG NHẬP". | Email: `nonexistent@test.com`<br>Password: `Password123!` | Hiển thị hộp thoại hoặc thông báo lỗi màu đỏ (ví dụ: "Tài khoản hoặc mật khẩu không chính xác"). | | | |
| 4 | TC_LOGIN_004 | Đăng nhập thất bại | Đăng nhập với mật khẩu sai | Tài khoản tồn tại trong DB | 1. Nhập Email hợp lệ đã tồn tại.<br>2. Nhập Mật khẩu sai.<br>3. Click nút "ĐĂNG NHẬP". | Email: `user@test.com`<br>Password: `WrongPass123` | Hiển thị thông báo lỗi (ví dụ: "Tài khoản hoặc mật khẩu không chính xác"). Không cho phép đăng nhập. | | | |
| 5 | TC_LOGIN_005 | Đăng nhập thành công | Kiểm tra đăng nhập thành công và chuyển hướng | Tài khoản tồn tại trong DB | 1. Nhập Email và Mật khẩu hợp lệ.<br>2. Click nút "ĐĂNG NHẬP". | Email: `user@test.com`<br>Password: `Password123!` | Đăng nhập thành công:<br>- Lưu token vào cookies/localStorage.<br>- Trạng thái tài khoản đổi thành Avatar và hiển thị trên Header.<br>- Chuyển hướng về Trang chủ hoặc callbackUrl. | | | |
| 6 | TC_LOGIN_006 | Hiển thị Mật khẩu | Kiểm tra tính năng ẩn/hiện mật khẩu | Màn hình đăng nhập mở sẵn | 1. Nhập mật khẩu vào ô Mật khẩu.<br>2. Click vào icon con mắt (Show/Hide) ở góc phải ô nhập. | | Mật khẩu chuyển đổi hiển thị giữa ký tự dấu chấm `●●●●` và văn bản tường minh. | | | |
| 7 | TC_LOGIN_007 | Remember Me | Kiểm tra chức năng "Ghi nhớ tôi" | | 1. Nhập tài khoản hợp lệ.<br>2. Tích chọn checkbox "Ghi nhớ tôi".<br>3. Đăng nhập thành công.<br>4. Tắt trình duyệt, mở lại trang. | | Trạng thái đăng nhập vẫn được duy trì, người dùng không cần đăng nhập lại. | | | |
| 8 | TC_LOGIN_008 | Social Login | Kiểm tra nút Đăng nhập qua Google / Facebook | | Click lần lượt vào nút Google và Facebook. | | Hiển thị trang đăng nhập liên kết của Google / Facebook để người dùng chọn tài khoản. | | | |
| 9 | TC_LOGIN_009 | Navigation Links | Kiểm tra liên kết Đăng ký và Quên mật khẩu | | Click vào liên kết "Đăng ký ngay" và "Quên mật khẩu?". | | Chuyển hướng chính xác đến trang tương ứng (`/register` và `/forgot-password`). | | | |

## Ghi chú

- Đảm bảo layout panel phía bên trái (hình nền gradient chuyển động) ẩn đi trên thiết bị Mobile và hiển thị rõ ràng trên màn hình Desktop.
