# Màn hình Báo cáo thống kê & Doanh thu (Reports & Statistical Analytics)

## Phạm vi

- Route: `/admin/reports`
- API liên quan: Xuất dữ liệu thống kê doanh số, số lượng đơn đặt chỗ, tỷ lệ lấp đầy tour, xuất file báo cáo (Excel/PDF).
- Vai trò: Quản trị viên (Admin).

## Điều kiện trước

- Tài khoản: Đã đăng nhập với vai trò Admin.
- Dữ liệu mẫu: Hệ thống có lịch sử giao dịch và đặt tour qua nhiều tháng/năm.
- Môi trường: Local dev server (`http://localhost:5173`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_AD_REP_001 | Thống kê theo ngày | Kiểm tra lọc dữ liệu báo cáo theo khoảng thời gian tùy chọn | | 1. Click chọn bộ lọc Ngày bắt đầu - Ngày kết thúc.<br>2. Nhấn nút "Lọc" (Filter). | Từ ngày: `2026-05-01`<br>Tới ngày: `2026-05-31` | Toàn bộ dữ liệu tổng kết (Tổng doanh thu, Tổng đơn hàng, Số đơn hủy, Số khách đi tour) và biểu đồ thay đổi tương ứng chỉ hiển thị dữ liệu phát sinh trong tháng 5 năm 2026. | | | |
| 2 | TC_AD_REP_002 | Tour bán chạy nhất | Xem bảng xếp hạng các tour được đặt nhiều nhất (Top booked tours) | Hệ thống có dữ liệu đặt tour | Quan sát khu vực danh sách "Tour bán chạy nhất" (Top Tours). | | Danh sách hiển thị đúng thứ tự số lượng khách đặt giảm dần kèm theo cột doanh thu thu về từ mỗi tour. | | | |
| 3 | TC_AD_REP_003 | Xuất báo cáo (Export Excel) | Kiểm tra chức năng xuất file Excel báo cáo doanh thu | | Click vào nút "Xuất Excel" (Export Excel). | | - Tải xuống thành công file định dạng `.xlsx` hoặc `.xls`.<br>- Nội dung file Excel khớp chính xác các số liệu đang hiển thị trên giao diện thống kê của khoảng thời gian đã lọc. | | | |

## Ghi chú

-
