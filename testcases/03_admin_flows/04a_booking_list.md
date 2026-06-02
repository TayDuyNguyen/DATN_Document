# Màn hình Danh sách Đặt chỗ (Booking List Page)

## Phạm vi

- Route: `/admin/bookings`
- API liên quan: Lấy danh sách toàn bộ các đơn đặt chỗ có phân trang, lọc và tìm kiếm.
- Vai trò: Quản trị viên (Admin) / Nhân viên (Staff).

## Điều kiện trước

- Tài khoản: Đã đăng nhập vào trang quản trị bằng tài khoản Admin/Staff.
- Môi trường: Local dev server (`http://localhost:5173`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_AD_BLIST_001 | Renders bảng | Renders bảng dữ liệu các đơn đặt chỗ | Có đơn đặt chỗ trong DB | Mở trang danh sách đặt chỗ. | | Hiển thị bảng gồm các cột: Mã đặt chỗ, Khách hàng, Tour, Số tiền, Phương thức thanh toán, Trạng thái đơn, Trạng thái thanh toán, Ngày đặt và Cột thao tác. | | | |
| 2 | TC_AD_BLIST_002 | Tìm kiếm đơn | Tìm đơn hàng theo Mã đặt chỗ hoặc Tên khách hàng | Có đơn hàng khớp | 1. Nhập Mã đơn vào ô tìm kiếm.<br>2. Nhấn Enter. | Mã đơn: `DNT12345` | Danh sách hiển thị chính xác đơn đặt chỗ có mã là `DNT12345`. | | | |
| 3 | TC_AD_BLIST_003 | Lọc trạng thái đơn | Lọc danh sách đặt chỗ theo Trạng thái | | Chọn bộ lọc trạng thái đơn (Pending, Confirmed, Completed, Cancelled). | Trạng thái: `Pending` | Chỉ hiển thị các đơn đặt tour đang chờ xử lý xác nhận từ quản trị viên. | | | |

## Ghi chú

-
