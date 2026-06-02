# Màn hình Thanh toán & Kết quả Thanh toán (Payment & Result Page)

## Phạm vi

- Route: `/payment`, `/payment/result` hoặc `/[locale]/payment/result`
- API liên quan: Kiểm tra trạng thái đơn hàng (get booking status), xử lý webhook thanh toán thành công/thất bại, thanh toán lại (retry payment).
- Vai trò: Người dùng đã đặt tour thành công và chờ thanh toán (User).

## Điều kiện trước

- Người dùng đã hoàn thành form Đặt tour và được chuyển hướng tới cổng thanh toán hoặc trang kết quả đơn hàng.
- Môi trường: Local dev server (`http://localhost:3000`).

## Test cases

### Phần 1: Giao diện cổng thanh toán bên thứ ba (Sandbox)

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_PAYMENT_001 | Thanh toán thành công | Hoàn thành thanh toán trên cổng sandbox (PayOS/VNPay) | Chuyển hướng thành công sang trang thanh toán sandbox | 1. Nhập thông tin thẻ test/tài khoản test.<br>2. Xác nhận thanh toán thành công.<br>3. Chờ chuyển hướng quay về web. | VNPay: Thẻ test quốc tế hoặc thẻ nội địa NCB cung cấp sẵn. | Cổng thanh toán chuyển hướng về trang `/payment/result?booking_code=...&status=success` (hoặc tương đương). Hệ thống cập nhật trạng thái đơn hàng thành "Đã thanh toán" (Paid). Renders thẻ thông báo xanh báo "Thanh toán thành công". | | | |
| 2 | TC_PAYMENT_002 | Hủy thanh toán | Người dùng hủy thanh toán giữa chừng trên cổng sandbox | | 1. Tại trang thanh toán sandbox, nhấn nút "Hủy" hoặc quay lại.<br>2. Chờ chuyển hướng về web. | | Hệ thống chuyển về trang `/payment/result` với trạng thái báo "Thanh toán không thành công" hoặc "Đã hủy". Renders thẻ cảnh báo màu đỏ. | | | |

### Phần 2: Trang kết quả thanh toán trên DaNangTrip (/payment/result)

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3 | TC_PAYMENT_003 | Renders thông tin đơn hàng | Renders thông tin hóa đơn khi thanh toán thành công | | Truy cập trang kết quả thanh toán thành công của đơn hàng. | | Hiển thị đầy đủ:<br>- Mã đơn hàng (`booking_code`).<br>- Tên tour, ngày xuất phát, số lượng khách.<br>- Tổng tiền đã trả.<br>- Phương thức thanh toán.<br>- Thông báo: Vé điện tử đã gửi về Email. | | | |
| 4 | TC_PAYMENT_004 | Nút Đặt lại thanh toán (Retry Payment) | Thử thanh toán lại đối với đơn hàng chưa thanh toán thành công | Trạng thái đơn hàng là chưa thanh toán (unpaid/cancelled) | Click nút "Thử thanh toán lại" (Retry Payment) hiển thị ở trang kết quả thất bại. | | Hệ thống khởi tạo lại phiên thanh toán mới với cổng thanh toán đã chọn và chuyển hướng người dùng sang trang thanh toán tương ứng. | | | |
| 5 | TC_PAYMENT_005 | Hướng dẫn Chuyển khoản | Renders thông tin chuyển khoản đối với phương thức Bank Transfer | Chọn phương thức thanh toán là Chuyển khoản | Xem giao diện kết quả đặt tour sau khi chọn Chuyển khoản ngân hàng. | | Hiển thị bảng chi tiết:<br>- Số tài khoản ngân hàng nhận.<br>- Tên ngân hàng, Tên chủ tài khoản.<br>- Nội dung chuyển khoản bắt buộc (Ví dụ: `DNT12345`).<br>- Mã QR thanh toán nhanh (nếu có). | | | |

## Ghi chú

-
