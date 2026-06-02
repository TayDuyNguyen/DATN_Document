# Màn hình Quản lý Yêu cầu liên hệ & Phản hồi (Contacts Management)

## Phạm vi

- Route: `/admin/contacts`
- API liên quan: Xem danh sách liên hệ gửi từ Web client, đánh dấu đã xử lý (resolve/read), xóa thư liên hệ.
- Vai trò: Quản trị viên (Admin) / Nhân viên (Staff).

## Điều kiện trước

- Tài khoản: Đã đăng nhập vào trang quản trị bằng tài khoản Admin/Staff.
- Dữ liệu mẫu: Có tin nhắn/yêu cầu liên hệ được gửi từ form liên hệ của Web client.
- Môi trường: Local dev server (`http://localhost:5173`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_AD_CONT_001 | Danh sách liên hệ | Hiển thị hộp thư liên hệ | Có thư liên hệ trong DB | Mở trang Quản lý Liên hệ. | | Danh sách hiển thị các cột thông tin: Tên người gửi, Email, SĐT, Tiêu đề, Trạng thái (Chưa đọc / Đã xử lý), Ngày gửi. | | | |
| 2 | TC_AD_CONT_002 | Xem nội dung thư | Xem chi tiết nội dung tin nhắn liên hệ | | Click chọn dòng liên hệ hoặc nút "Xem" tại một dòng thư chưa đọc. | | - Mở cửa sổ popup hoặc trang chi tiết hiển thị toàn bộ nội dung tin nhắn của khách hàng.<br>- Thư tự động chuyển trạng thái từ "Chưa đọc" sang "Đã đọc" (Read) và biểu tượng thư thay đổi tương ứng. | | | |
| 3 | TC_AD_CONT_003 | Đánh dấu Đã xử lý (Resolve) | Cập nhật trạng thái xử lý liên hệ | Liên hệ ở trạng thái mới nhận | Click nút "Đánh dấu đã giải quyết" (Mark as Resolved) sau khi đã liên hệ hỗ trợ khách hàng qua điện thoại/email. | | Trạng thái chuyển sang "Đã xử lý" (Resolved). Badge trạng thái cập nhật màu sắc sang xanh lá cây. | | | |
| 4 | TC_AD_CONT_004 | Xóa liên hệ | Xóa tin nhắn liên hệ khỏi hệ thống | | 1. Click nút "Xóa" tại thư liên hệ bất kỳ.<br>2. Nhấn xác nhận xóa trên hộp thoại cảnh báo. | | Thư liên hệ bị loại bỏ hoàn toàn khỏi danh sách hộp thư của quản trị viên. | | | |

## Ghi chú

-
