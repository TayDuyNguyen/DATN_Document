# Màn hình Danh sách Người dùng (User List Page)

## Phạm vi

- Route: `/admin/users`
- API liên quan: Lấy danh sách người dùng, thay đổi trạng thái hoạt động (Kích hoạt/Khóa).
- Vai trò: Quản trị viên (Admin).

## Điều kiện trước

- Tài khoản: Đã đăng nhập vào trang quản trị bằng tài khoản Admin.
- Môi trường: Local dev server (`http://localhost:5173`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_AD_ULIST_001 | Renders bảng | Renders bảng dữ liệu người dùng | Danh sách người dùng có trong DB | Mở màn hình danh sách người dùng. | | Renders bảng danh sách đầy đủ các cột: Họ tên, Email, Số điện thoại, Vai trò (Admin/Staff/Customer), Trạng thái, Ngày tạo và Cột hành động. | | | |
| 2 | TC_AD_ULIST_002 | Tìm kiếm nhanh | Tìm kiếm người dùng theo tên hoặc email | Có người dùng khớp | 1. Nhập từ khóa tìm kiếm.<br>2. Nhấn Enter. | Từ khóa: `staff@danangtrip` | Bảng tự động cập nhật chỉ hiển thị các dòng chứa từ khóa `staff@danangtrip`. | | | |
| 3 | TC_AD_ULIST_003 | Lọc Vai trò | Lọc người dùng theo vai trò (Role) | Có người dùng ở các vai trò | Chọn vai trò từ bộ lọc dropdown. | Vai trò: `Nhân viên` | Bảng hiển thị chính xác danh sách tài khoản thuộc vai trò Nhân viên. | | | |
| 4 | TC_AD_ULIST_004 | Khóa tài khoản | Tắt kích hoạt hoạt động tài khoản người dùng | Tài khoản đang ở trạng thái Hoạt động | 1. Click switch/nút "Khóa" ở cột trạng thái của tài khoản.<br>2. Nhấn xác nhận ở dialog cảnh báo. | | - Trạng thái đổi thành "Đã khóa" (Blocked).<br>- Tài khoản này bị chặn đăng nhập ở cả Web client và Admin. | | | |
| 5 | TC_AD_ULIST_005 | Mở khóa tài khoản | Kích hoạt lại tài khoản đã khóa | Tài khoản đang ở trạng thái Đã khóa | 1. Click switch/nút "Kích hoạt" trên dòng tài khoản.<br>2. Nhấn xác nhận. | | Trạng thái chuyển thành "Hoạt động" (Active). Tài khoản đăng nhập lại bình thường. | | | |

## Ghi chú

-
