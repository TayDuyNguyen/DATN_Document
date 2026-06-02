# Màn hình Cài đặt hệ thống & Thông tin quản trị (System & Admin Settings)

## Phạm vi

- Route: `/admin/settings`
- API liên quan: Thay đổi cấu hình hệ thống (tắt/bật cổng thanh toán, tỷ lệ hoa hồng, thông tin liên hệ chính thức, đổi mật khẩu admin).
- Vai trò: Quản trị viên (Admin).

## Điều kiện trước

- Tài khoản: Đã đăng nhập với vai trò Admin.
- Môi trường: Local dev server (`http://localhost:5173`).

## Test cases

### Phần 1: Thông tin cấu hình hệ thống (General Settings)

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_AD_SET_001 | Thông tin công ty | Thay đổi thông tin liên hệ chính thức hiển thị ra ngoài Web client | | 1. Thay đổi số điện thoại hotline hỗ trợ và email liên hệ.<br>2. Nhấn nút "Lưu cài đặt". | Hotline: `1900 8888`<br>Email: `support@danangtrip.vn` | - Lưu thành công.<br>- Toàn bộ thông tin hotline và email mới lập tức được đồng bộ hiển thị chính xác trên Header / Footer của trang Web client. | | | |
| 2 | TC_AD_SET_002 | Bật tắt cổng thanh toán | Kích hoạt hoặc hủy kích hoạt các cổng thanh toán trực tuyến | Có cấu hình cổng VNPay, PayOS | 1. Tắt switch kích hoạt cổng VNPay hoặc PayOS.<br>2. Nhấn nút "Lưu cài đặt". | | - Lưu thành công.<br>- Khi khách hàng đặt tour tại Web client, phương thức thanh toán vừa bị tắt sẽ không còn hiển thị ở danh sách lựa chọn thanh toán nữa. | | | |

### Phần 2: Tài khoản quản trị cá nhân (Admin Profile)

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3 | TC_AD_SET_003 | Thay đổi thông tin cá nhân | Thay đổi Họ tên, email, số điện thoại của tài khoản Admin hiện tại | | 1. Đổi tên hiển thị Admin.<br>2. Nhấn nút "Lưu thay đổi". | Name: `Administrator V2` | Thông tin thay đổi thành công, tên hiển thị trên thanh điều hướng góc phải Header cập nhật tức thì. | | | |
| 4 | TC_AD_SET_004 | Đổi mật khẩu | Đổi mật khẩu quản trị viên | Mật khẩu cũ chính xác | 1. Nhập Mật khẩu hiện tại.<br>2. Nhập Mật khẩu mới và Xác nhận mật khẩu mới trùng khớp.<br>3. Click "Đổi mật khẩu". | Current: `Admin123!`<br>New: `NewAdmin123!`<br>Confirm: `NewAdmin123!` | Đổi mật khẩu thành công. Lần đăng nhập quản trị tiếp theo bắt buộc phải dùng mật khẩu mới này. | | | |

## Ghi chú

-
