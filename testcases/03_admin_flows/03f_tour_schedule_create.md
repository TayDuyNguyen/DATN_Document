# Màn hình Thêm lịch khởi hành (Create Tour Schedule Page)

## Phạm vi

- Route: `/admin/tours/[id]/schedules/create`
- API liên quan: Thêm lịch khởi hành mới cho một tour (POST `/api/tours/[id]/schedules`).
- Vai trò: Quản trị viên (Admin) / Nhân viên (Staff).

## Điều kiện trước

- Tài khoản: Đã đăng nhập vào trang quản trị bằng tài khoản Admin/Staff.
- Môi trường: Local dev server (`http://localhost:5173`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_AD_SCHEDCREATE_001 | Validate form trống | Kiểm tra validate các trường bắt buộc | Màn hình Thêm lịch mở sẵn | Bấm "Lưu" mà không điền thông tin. | | Hệ thống chặn submit và báo lỗi tại các trường Ngày khởi hành, Số người tối đa. | | | |
| 2 | TC_AD_SCHEDCREATE_002 | Ngày khởi hành quá khứ | Kiểm tra chặn chọn ngày khởi hành ở quá khứ | | 1. Chọn Ngày khởi hành là một ngày trước ngày hiện tại.<br>2. Nhập số khách tối đa.<br>3. Bấm "Lưu". | Ngày: `2026-05-01` (trong quá khứ) | Hệ thống báo lỗi Ngày khởi hành phải là ngày trong tương lai, chặn không cho tạo. | | | |
| 3 | TC_AD_SCHEDCREATE_003 | Thêm lịch thành công | Tạo mới một lịch khởi hành thành công | | 1. Chọn ngày đi hợp lệ (tương lai).<br>2. Nhập số lượng khách tối đa.<br>3. Chọn trạng thái hoạt động (Mở bán - open).<br>4. Nhấn "Lưu". | Date: `2026-07-20`<br>Max: `15 người` | Tạo thành công, lịch khởi hành mới hiển thị trên bảng quản trị và được mở bán ở Web client. | | | |

## Ghi chú

-
