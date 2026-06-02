# Màn hình Liên hệ (Contact Page)

## Phạm vi

- Route: `/contact` hoặc `/[locale]/contact`
- API liên quan: Gửi thông tin liên hệ / phản hồi về hệ thống.
- Vai trò: Khách vãng lai (Guest) / Người dùng đã đăng nhập (User).

## Điều kiện trước

- Môi trường: Local dev server (`http://localhost:3000`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_CONTACT_001 | Trường bắt buộc | Kiểm tra lỗi khi gửi form trống | Màn hình liên hệ hiển thị | Để trống tất cả các trường và nhấn nút "Gửi tin nhắn" (Submit). | | Form validator ngăn gửi đi và hiển thị lỗi màu đỏ dưới các trường bắt buộc (`Họ và tên`, `Email`, `Nội dung tin nhắn`). | | | |
| 2 | TC_CONTACT_002 | Định dạng Email | Kiểm tra lỗi khi nhập email sai định dạng | | 1. Điền Họ tên hợp lệ.<br>2. Điền Email không đúng định dạng.<br>3. Điền Nội dung tin nhắn hợp lệ.<br>4. Nhấn "Gửi tin nhắn". | Email: `vanatest` | Hiển thị thông báo lỗi "Email không đúng định dạng" ngay dưới ô Email. | | | |
| 3 | TC_CONTACT_003 | Gửi tin nhắn thành công | Kiểm tra luồng gửi liên hệ thành công | | 1. Nhập đầy đủ thông tin hợp lệ vào tất cả các trường.<br>2. Nhấn "Gửi tin nhắn". | Name: `Nguyen Van A`<br>Email: `vana@test.com`<br>Phone: `0901234567`<br>Subject: `Hỏi về tour Bà Nà`<br>Message: `Tôi muốn hỏi tour Bà Nà khởi hành ngày mai.` | Gửi thành công:<br>- Nút bấm hiển thị trạng thái loading "Đang gửi...".<br>- Sau đó, form biến mất và thay thế bằng thông báo thành công "Cảm ơn bạn đã liên hệ!".<br>- Có nút "Gửi tin nhắn khác". | | | |
| 4 | TC_CONTACT_004 | Gửi tin nhắn khác | Kiểm tra nút gửi tin nhắn khác sau khi thành công | Đã gửi tin nhắn thành công | Click nút "Gửi một tin nhắn khác" ở màn hình báo thành công. | | Màn hình quay trở lại giao diện form liên hệ ban đầu, tất cả các ô nhập liệu được làm sạch (clear) hoàn toàn để sẵn sàng nhập mới. | | | |
| 5 | TC_CONTACT_005 | Bản đồ & Info Card | Kiểm tra hiển thị thông tin địa chỉ và bản đồ | | Rà soát thông tin hotline, email hỗ trợ, bản đồ nhúng Google Map ở bên cạnh form liên hệ. | | - Các thông tin liên hệ hiển thị rõ ràng.<br>- Bản đồ Google Map tải thành công, có thể thu phóng, di chuyển bản đồ bình thường. | | | |

## Ghi chú

-
