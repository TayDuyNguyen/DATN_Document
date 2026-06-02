# Màn hình Thông báo của tôi (User Notifications Page)

## Phạm vi

- Route: `/profile/notifications` hoặc `/[locale]/profile/notifications`
- API liên quan: Lấy danh sách thông báo gửi riêng cho user, đánh dấu thông báo đã đọc.
- Vai trò: Người dùng đã đăng nhập (User).

## Điều kiện trước

- Tài khoản: Đã đăng nhập vào hệ thống.
- Môi trường: Local dev server (`http://localhost:3000`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_US_NOTIF_001 | Danh sách thông báo | Hiển thị hộp thư thông báo cá nhân | Có thông báo trong DB | Truy cập trang `/profile/notifications`. | | Danh sách hiển thị các thông báo (khuyến mãi, cập nhật đơn hàng, thanh toán) với tiêu đề, tóm tắt nội dung, thời gian nhận. Các thông báo chưa đọc được highlight màu nền nhạt hoặc có dấu chấm xanh. | | | |
| 2 | TC_US_NOTIF_002 | Đọc thông báo | Nhấp xem nội dung chi tiết thông báo | Có thông báo chưa đọc | Click vào tiêu đề một thông báo chưa đọc. | | - Nội dung thông báo hiển thị chi tiết.<br>- Trạng thái đổi thành "Đã đọc", dấu chấm xanh hoặc highlight biến mất.<br>- Số đếm thông báo chưa đọc trên quả chuông Header giảm đi 1. | | | |
| 3 | TC_US_NOTIF_003 | Đánh dấu tất cả đã đọc | Đánh dấu nhanh tất cả thông báo là đã đọc | Có nhiều thông báo chưa đọc | Click nút "Đánh dấu tất cả là đã đọc" ở đầu danh sách. | | Toàn bộ thông báo chuyển trạng thái đã đọc cùng một lúc. Icon chuông trên Header không còn hiển thị số đếm chưa đọc. | | | |
| 4 | TC_US_NOTIF_004 | Xóa thông báo | Xóa thông báo khỏi danh sách | | Click icon Thùng rác/Xóa tại dòng thông báo. | | Thông báo bị xóa vĩnh viễn khỏi danh sách hiển thị của người dùng. | | | |

## Ghi chú

-
