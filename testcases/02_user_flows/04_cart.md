# Màn hình Giỏ hàng (Shopping Cart Page)

## Phạm vi

- Route: `/cart` hoặc `/[locale]/cart`
- API liên quan: Thêm vào giỏ hàng, cập nhật giỏ hàng, xóa khỏi giỏ hàng.
- Vai trò: Người dùng đã đăng nhập (User) / Lưu tạm trên local (Guest).

## Điều kiện trước

- Tài khoản: Đã đăng nhập.
- Dữ liệu mẫu: Có một số tour đã lưu vào giỏ hàng trước đó.
- Môi trường: Local dev server (`http://localhost:3000`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_CART_001 | Giỏ hàng rỗng | Hiển thị giỏ hàng khi không có sản phẩm nào | Giỏ hàng trống | Truy cập vào trang `/cart`. | | Hiển thị thông báo "Giỏ hàng của bạn đang trống" kèm theo nút điều hướng "Khám phá Tour ngay" quay về trang danh sách tour. | | | |
| 2 | TC_CART_002 | Xem giỏ hàng | Hiển thị danh sách sản phẩm trong giỏ hàng | Giỏ hàng có sản phẩm | Truy cập vào trang `/cart`. | | Hiển thị danh sách các tour đã thêm gồm các cột: Ảnh, Tên Tour, Ngày khởi hành, Số lượng khách (người lớn/trẻ em/em bé), Đơn giá, Thành tiền và cột chọn thanh toán. | | | |
| 3 | TC_CART_003 | Thay đổi số lượng | Tăng/giảm số lượng khách trực tiếp trong giỏ hàng | | Nhấn nút cộng (+)/trừ (-) tại cột Số lượng khách của một tour trong giỏ. | | Số lượng thay đổi, tiền của dòng sản phẩm đó cập nhật tức thì. Cột tổng tiền tạm tính ở góc phải thay đổi tương ứng. | | | |
| 4 | TC_CART_004 | Xóa sản phẩm | Xóa tour ra khỏi giỏ hàng | | 1. Click vào icon Thùng rác (Xóa) của một tour.<br>2. Nhấn xác nhận "Xóa" trên pop-up xác nhận. | | Tour bị loại bỏ khỏi giỏ hàng, danh sách giỏ hàng cập nhật lại và hiển thị thông báo toast xóa thành công. | | | |
| 5 | TC_CART_005 | Chọn thanh toán | Tích chọn tour muốn thanh toán | Giỏ hàng có nhiều tour | 1. Tích chọn checkbox ở đầu dòng của một vài tour.<br>2. Bỏ chọn một số tour. | | Chỉ những tour được tích chọn mới được tính vào Tổng tiền thanh toán ở hộp hóa đơn tạm tính bên phải. | | | |
| 6 | TC_CART_006 | Tiến hành đặt hàng | Đi tiếp sang trang đặt chỗ từ giỏ hàng | Đã chọn ít nhất 1 tour | Click nút "Tiến hành đặt chỗ" (Checkout) ở hộp hóa đơn. | | Chuyển hướng thành công sang trang Đặt tour (`/tours/[slug]/book` hoặc `/payment`) tương ứng với các tour đã chọn thanh toán trong giỏ. | | | |

## Ghi chú

-
