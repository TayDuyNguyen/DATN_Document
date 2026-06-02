# Màn hình Quản lý & Gửi Thông báo (System Notifications Management)

## Phạm vi

- Route: `/admin/notifications`, `/admin/notifications/send`
- API liên quan: Danh sách lịch sử thông báo hệ thống, tạo và gửi thông báo đẩy (push notifications / system alerts) tới người dùng.
- Vai trò: Quản trị viên (Admin).

## Điều kiện trước

- Tài khoản: Đã đăng nhập với vai trò Admin.
- Môi trường: Local dev server (`http://localhost:5173`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_AD_NOTIF_001 | Danh sách thông báo | Xem lịch sử các thông báo hệ thống đã gửi | | Truy cập trang Quản lý Thông báo. | | Renders bảng danh sách thông báo đã gửi gồm: Tiêu đề, Nội dung tóm tắt, Đối tượng nhận (Tất cả / Cá nhân), Trạng thái gửi, Ngày gửi, Người gửi. | | | |
| 2 | TC_AD_NOTIF_002 | Gửi thông báo - Validate | Kiểm tra nhập trống các trường bắt buộc khi soạn thông báo mới | Màn hình Gửi thông báo mới mở sẵn | Nhấn nút "Gửi thông báo" mà không nhập thông tin. | | Hệ thống chặn gửi và báo lỗi tại các trường bắt buộc: Tiêu đề, Nội dung, Đối tượng nhận. | | | |
| 3 | TC_AD_NOTIF_003 | Gửi thông báo toàn hệ thống | Gửi thông báo tới tất cả người dùng hoạt động | | 1. Nhập Tiêu đề.<br>2. Nhập Nội dung.<br>3. Chọn Đối tượng nhận là "Tất cả người dùng" (All Users).<br>4. Nhập đường dẫn liên kết (tùy chọn).<br>5. Bấm "Gửi thông báo". | Tiêu đề: "Khuyến mãi hè 2026"<br>Nội dung: "Giảm giá 10% các tour biển..." | - Gửi thành công và thông báo toast thành công.<br>- Toàn bộ tài khoản khách hàng khi đăng nhập trên Web client sẽ nhận được thông báo mới này ở icon quả chuông trên Header. | | | |
| 4 | TC_AD_NOTIF_004 | Gửi thông báo cá nhân | Gửi thông báo hướng tới một người dùng cụ thể | Tài khoản nhận tồn tại | 1. Soạn nội dung thông báo.<br>2. Chọn Đối tượng nhận là "Người dùng cụ thể" (Specific User).<br>3. Tìm kiếm và chọn người dùng nhận qua Email.<br>4. Bấm "Gửi thông báo". | Email nhận: `user@test.com` | - Gửi thành công.<br>- Chỉ duy nhất tài khoản `user@test.com` nhận được thông báo này khi truy cập Web client. Các tài khoản khác không nhận được. | | | |

## Ghi chú

-
