# Màn hình Trang chủ Quản trị (Admin Dashboard)

## Phạm vi

- Route: `/admin` hoặc `/admin/dashboard`
- API liên quan: Lấy thống kê tổng quan (số lượng tour, người dùng, tổng doanh thu, số đơn đặt chỗ mới), danh sách đặt chỗ gần đây.
- Vai trò: Quản trị viên (Admin) / Nhân viên (Staff).

## Điều kiện trước

- Tài khoản: Đã đăng nhập vào trang quản trị bằng tài khoản Admin/Staff.
- Dữ liệu mẫu: Hệ thống đã có giao dịch thanh toán, đơn đặt chỗ, người dùng hoạt động và các tour.
- Môi trường: Local dev server (`http://localhost:5173`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_AD_DASH_001 | Sidebar Navigation | Kiểm tra điều hướng menu Sidebar bên trái | Màn hình Dashboard mở sẵn | Click lần lượt các mục trên Sidebar: Dashboard, Quản lý Tour, Quản lý Đặt chỗ, Quản lý Người dùng, Quản lý Địa điểm, Bài viết/Blog, Khuyến mãi, Phản hồi, Đánh giá, Báo cáo, Cài đặt. | | - Mỗi mục điều hướng chính xác đến Route tương ứng.<br>- Menu hiện tại được highlight/active nổi bật.<br>- Sidebar có thể thu gọn/mở rộng (collapse) mượt mà. | | | |
| 2 | TC_AD_DASH_002 | Thẻ thống kê (Stats Cards) | Kiểm tra hiển thị các chỉ số thống kê tổng quan | | Xem các thẻ hiển thị: Tổng doanh thu, Số người dùng, Tổng số Tour, Tổng đơn hàng. | | - Các số liệu hiển thị chính xác (ví dụ doanh thu hiển thị theo định dạng tiền tệ: `12,500,000đ`).<br>- Có hiển thị tỷ lệ tăng/giảm so với tháng trước (ví dụ: `+12%`). | | | |
| 3 | TC_AD_DASH_003 | Biểu đồ doanh thu | Kiểm tra hiển thị biểu đồ doanh thu và bộ lọc | Có dữ liệu doanh thu các tháng | 1. Di chuột lên các cột/đường trên biểu đồ.<br>2. Thay đổi bộ lọc thời gian (Tuần này, Tháng này, Năm nay). | | - Biểu đồ vẽ đúng và hiển thị tooltip thông tin chi tiết số tiền khi hover vào từng điểm dữ liệu.<br>- Biểu đồ cập nhật lại dữ liệu ngay sau khi đổi bộ lọc thời gian. | | | |
| 4 | TC_AD_DASH_004 | Đơn hàng gần đây | Kiểm tra danh sách đơn đặt chỗ mới nhất | Hệ thống có đơn đặt tour mới | Xem bảng "Đơn đặt chỗ gần đây" (Recent Bookings) ở cuối trang Dashboard. | | - Hiển thị tối đa 5-10 đơn hàng mới nhất với các thông tin: Mã đơn, Khách hàng, Tour, Tổng tiền, Trạng thái, Ngày đặt.<br>- Trạng thái đơn được hiển thị bằng badge màu sắc tương ứng (ví dụ: Chờ thanh toán - Vàng, Đã xác nhận - Xanh dương, Hoàn thành - Xanh lá, Đã hủy - Đỏ). | | | |
| 5 | TC_AD_DASH_005 | Điều hướng từ Đơn hàng gần đây | Kiểm tra chuyển hướng chi tiết từ bảng gần đây | Bảng đơn hàng gần đây hiển thị | Click vào nút "Xem" hoặc mã đơn hàng trên bảng Đơn đặt chỗ gần đây. | | Chuyển hướng thành công sang màn hình Chi tiết Đặt chỗ (`/admin/bookings/detail/:id`) tương ứng. | | | |
| 6 | TC_AD_DASH_006 | Notification Bell | Kiểm tra thông báo nhanh từ Header | Có thông báo mới | Click vào icon quả chuông trên Header. | | Mở popover danh sách các thông báo mới nhất (ví dụ: "Có đơn đặt chỗ mới", "Có đánh giá mới"). Click vào thông báo sẽ dẫn đến trang chi tiết xử lý tương ứng. | | | |

## Ghi chú

-
