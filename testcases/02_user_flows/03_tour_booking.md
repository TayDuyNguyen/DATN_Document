# Màn hình Đặt Tour (Tour Booking Page)

## Phạm vi

- Route: `/tours/[slug]/book` hoặc `/[locale]/tours/[slug]/book`
- API liên quan: Kiểm tra tình trạng chỗ trống (availability check), tính giá tạm thời (calculate booking), tạo đơn đặt tour (create booking).
- Vai trò: Người dùng đã đăng nhập (User).

## Điều kiện trước

- Tài khoản: Đã đăng nhập vào hệ thống.
- Dữ liệu mẫu: Tour tồn tại, có lịch trình khởi hành còn chỗ trong database.
- Môi trường: Local dev server (`http://localhost:3000`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_BOOKING_001 | Thông tin Lịch khởi hành | Hiển thị và thay đổi ngày khởi hành | Lịch khởi hành có sẵn trong DB | 1. Mở màn hình đặt tour.<br>2. Chọn ngày khởi hành từ dropdown. | | Dropdown hiển thị danh sách ngày xuất phát hợp lệ cùng số ghế còn lại. Khi chọn 1 ngày, thông tin tóm tắt và giá tạm tính được cập nhật. | | | |
| 2 | TC_BOOKING_002 | Điền từ hồ sơ | Tự động lấy thông tin từ Profile | Hồ sơ cá nhân có đầy đủ Name, Phone, Email, City | Click liên kết "Điền từ hồ sơ cá nhân" (Fill from profile). | | Các trường Họ và tên, Email, Số điện thoại, Địa chỉ tự động điền đúng thông tin của tài khoản hiện tại. | | | |
| 3 | TC_BOOKING_003 | Validate liên hệ | Kiểm tra định dạng Email/SĐT liên hệ | | 1. Thay đổi Email sai cú pháp.<br>2. Nhập SĐT sai độ dài.<br>3. Bấm nút đặt tour. | Email: `vana` / Phone: `123` | Hệ thống báo lỗi định dạng Email và SĐT không hợp lệ ở phần thông tin liên hệ. | | | |
| 4 | TC_BOOKING_004 | Đếm số lượng khách | Thay đổi số lượng khách vượt quá số chỗ trống còn lại | Lịch khởi hành còn 3 chỗ trống | 1. Tăng số lượng người lớn và trẻ em lên tổng số là 4 người.<br>2. Quan sát thông báo. | Adults: 3, Children: 1 | Hệ thống hiển thị cảnh báo quá tải số chỗ còn lại ("Chỉ còn lại X chỗ trống") và tự động điều chỉnh số lượng khách về mức tối đa cho phép. | | | |
| 5 | TC_BOOKING_005 | Điều khoản dịch vụ | Kiểm tra yêu cầu đồng ý điều khoản | Chưa tích chọn checkbox đồng ý điều khoản | 1. Nhập đầy đủ thông tin hợp lệ.<br>2. Bỏ chọn checkbox "Tôi đồng ý với điều khoản dịch vụ...".<br>3. Nhấn "Tiếp tục thanh toán". | | Hệ thống chặn gửi đơn đặt và hiển thị lỗi "Bạn phải đồng ý với điều khoản dịch vụ trước khi tiếp tục". | | | |
| 6 | TC_BOOKING_006 | Chọn phương thức thanh toán | Kiểm tra việc lựa chọn phương thức thanh toán | Các cổng thanh toán được cấu hình trong admin | Click chọn lần lượt các phương thức thanh toán hiển thị: PayOS, VNPay, Chuyển khoản ngân hàng. | | Phương thức thanh toán được chọn sáng lên, cập nhật giá trị trường `payment_method` trong dữ liệu gửi đi. | | | |
| 7 | TC_BOOKING_007 | Tạo booking thành công | Đặt tour thành công với thanh toán trực tuyến | Thông tin hợp lệ, chọn VNPay/PayOS | 1. Nhập đầy đủ thông tin hợp lệ.<br>2. Chọn phương thức thanh toán trực tuyến (PayOS hoặc VNPay).<br>3. Tích đồng ý điều khoản.<br>4. Nhấn "Tiếp tục thanh toán". | | Đặt thành công:<br>- Hiển thị toast đặt tour thành công.<br>- Hệ thống gọi API thanh toán và tự động chuyển hướng người dùng sang trang thanh toán sandbox của VNPay / PayOS. | | | |
| 8 | TC_BOOKING_008 | Tạo booking thành công | Đặt tour thành công với Chuyển khoản ngân hàng | Thông tin hợp lệ, chọn Bank Transfer | 1. Nhập đầy đủ thông tin hợp lệ.<br>2. Chọn phương thức "Chuyển khoản ngân hàng".<br>3. Tích đồng ý điều khoản.<br>4. Nhấn "Tiếp tục thanh toán". | | Đặt thành công:<br>- Tạo đơn thành công.<br>- Chuyển hướng người dùng về trang Kết quả đặt tour (`/payment/result`) kèm mã đơn hàng `booking_code` và thông tin số tài khoản chuyển khoản. | | | |

## Ghi chú

-
