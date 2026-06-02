# Màn hình Chỉnh sửa Lịch khởi hành (Edit Tour Schedule Page)

## Phạm vi

- Route: `/admin/tours/[id]/schedules/[schedule_id]/edit`
- API liên quan: Chi tiết lịch khởi hành, cập nhật lịch khởi hành (PUT `/api/schedules/[id]`).
- Vai trò: Quản trị viên (Admin) / Nhân viên (Staff).

## Điều kiện trước

- Tài khoản: Đã đăng nhập vào trang quản trị bằng tài khoản Admin/Staff.
- Dữ liệu mẫu: Lịch khởi hành cần sửa tồn tại trong DB.
- Môi trường: Local dev server (`http://localhost:5173`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_AD_SCHEDEDIT_001 | Tải thông tin cũ | Renders thông tin hiện có lên form chỉnh sửa | Màn hình sửa mở sẵn | Truy cập trang Sửa lịch khởi hành. | | Các trường (Ngày khởi hành, Số khách tối đa, Số khách đã đặt, Trạng thái) hiển thị chính xác thông tin hiện thời. | | | |
| 2 | TC_AD_SCHEDEDIT_002 | Thay đổi số chỗ tối đa | Chỉnh sửa số khách tối đa của lịch trình | | 1. Nhập Số khách tối đa mới lớn hơn số khách đã đặt.<br>2. Bấm "Cập nhật". | Max: `25` (cũ `20`) | Cập nhật thành công, số lượng chỗ tăng lên cho phép khách đặt thêm vé trên web client. | | | |
| 3 | TC_AD_SCHEDEDIT_003 | Đóng bán vé | Thay đổi trạng thái bán hàng sang khóa/đóng | | 1. Tại dropdown trạng thái, chọn "Tạm đóng" (Temporarily Closed).<br>2. Bấm "Cập nhật". | Trạng thái: `Closed` | Cập nhật thành công. Khách hàng trên Web client không thể click đặt chỗ vào ngày này nữa. | | | |

## Ghi chú

-
