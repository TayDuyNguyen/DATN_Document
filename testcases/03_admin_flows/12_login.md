# Màn hình Đăng nhập Quản trị (Admin Login)

## Phạm vi

- Route: `/admin/login` hoặc `/admin/auth`
- API liên quan: Đăng nhập quản trị viên (POST `/api/auth/admin/login`).
- Vai trò: Quản trị viên (Admin) / Nhân viên (Staff).

## Điều kiện trước

- Tài khoản: Đã có tài khoản Admin/Staff đăng ký trong hệ thống.
- Môi trường: Local dev server (`http://localhost:5173`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_AD_LOGIN_001 | Validate form trống | Báo lỗi khi không điền Email/Mật khẩu | Màn hình đăng nhập quản trị mở sẵn | Click nút "ĐĂNG NHẬP" mà không nhập dữ liệu. | | Trình duyệt hoặc validator chặn lại và báo lỗi yêu cầu điền tài khoản và mật khẩu. | | | |
| 2 | TC_AD_LOGIN_002 | Sai tài khoản/mật khẩu | Đăng nhập với thông tin tài khoản không chính xác | | 1. Nhập email hoặc mật khẩu không tồn tại/không đúng.<br>2. Nhấn "ĐĂNG NHẬP". | Email: `wrongadmin@test.com`<br>Password: `123456` | Giao diện hiển thị thông báo lỗi màu đỏ rõ ràng (ví dụ: "Tài khoản hoặc mật khẩu không chính xác"). | | | |
| 3 | TC_AD_LOGIN_003 | Đăng nhập thành công | Đăng nhập thành công với tài khoản Admin hợp lệ | Tài khoản có vai trò là Admin trong DB | 1. Nhập chính xác Email của Admin.<br>2. Nhập chính xác Mật khẩu.<br>3. Nhấn "ĐĂNG NHẬP". | Email: `admin@danangtrip.vn`<br>Password: `Admin123!` | Đăng nhập thành công:<br>- Lưu token xác thực vào cookies/localStorage.<br>- Chuyển hướng người dùng vào trang Dashboard quản trị chính (`/admin/dashboard`). | | | |
| 4 | TC_AD_LOGIN_004 | Chặn truy cập (Staff) | Kiểm tra đăng nhập với tài khoản không có quyền Admin/Staff | Tài khoản khách hàng thông thường | 1. Nhập Email của tài khoản khách hàng thông thường.<br>2. Nhập mật khẩu chính xác.<br>3. Nhấn "ĐĂNG NHẬP". | Email: `customer@test.com`<br>Password: `Customer123!` | Đăng nhập thất bại, hệ thống báo lỗi không có quyền truy cập (ví dụ: "Tài khoản của bạn không có quyền truy cập trang quản trị"). | | | |
| 5 | TC_AD_LOGIN_005 | Route Guard (Bảo vệ tuyến đường) | Chặn truy cập Dashboard trực tiếp khi chưa đăng nhập | Chưa đăng nhập | Nhập trực tiếp đường dẫn `/admin/dashboard` trên thanh địa chỉ trình duyệt rồi nhấn Enter. | | Hệ thống tự động phát hiện chưa có token hợp lệ, chặn truy cập và chuyển hướng người dùng ngay lập tức quay về màn hình đăng nhập quản trị (`/admin/login`). | | | |

## Ghi chú

-
