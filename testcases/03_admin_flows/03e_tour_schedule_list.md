# Màn hình Danh sách Lịch khởi hành (Tour Schedules List Page)

## Phạm vi

- Route: `/admin/tours/[id]/schedules`
- API liên quan: Danh sách lịch khởi hành của tour, thống kê số lượng đặt chỗ trên mỗi chuyến khởi hành.
- Vai trò: Quản trị viên (Admin) / Nhân viên (Staff).

## Điều kiện trước

- Tài khoản: Đã đăng nhập vào trang quản trị bằng tài khoản Admin/Staff.
- Dữ liệu mẫu: Tour cụ thể tồn tại trong DB.
- Môi trường: Local dev server (`http://localhost:5173`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_AD_SCHEDLIST_001 | Calendar View | Xem lịch khởi hành dưới dạng Lịch tháng (Calendar View) | Trang danh sách mở sẵn | Bấm chọn tab "Xem dạng lịch" (Calendar View). | | Hiển thị bảng lịch tháng. Các ngày có lịch khởi hành hiển thị thẻ nhỏ chứa số lượng người đã đặt / số chỗ tối đa (Ví dụ: `12/20`). | | | |
| 2 | TC_AD_SCHEDLIST_002 | Bảng danh sách | Xem lịch khởi hành dạng bảng danh sách | | Bấm chọn tab "Xem dạng bảng" (List View). | | Bảng hiển thị các cột: Ngày khởi hành, Số khách tối đa, Số khách đã đặt, Trạng thái bán (Mở bán / Tạm đóng / Đã khóa), Thao tác. | | | |
| 3 | TC_AD_SCHEDLIST_003 | Xóa lịch khởi hành | Xóa lịch khởi hành của tour | Lịch khởi hành không có khách nào đặt chỗ | 1. Click nút "Xóa" tại dòng lịch trình.<br>2. Nhấn xác nhận. | | Lịch trình bị xóa khỏi danh sách. Nếu đã có khách hàng đặt chỗ, hệ thống chặn không cho xóa và hiển thị thông báo lỗi. | | | |

## Ghi chú

-
