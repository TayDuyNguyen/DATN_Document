# Màn hình Danh sách Địa điểm (Location List Page)

## Phạm vi

- Route: `/admin/locations`
- API liên quan: Lấy danh sách toàn bộ các địa danh/địa điểm du lịch có lọc và tìm kiếm.
- Vai trò: Quản trị viên (Admin) / Nhân viên (Staff).

## Điều kiện trước

- Tài khoản: Đã đăng nhập vào trang quản trị bằng tài khoản Admin/Staff.
- Môi trường: Local dev server (`http://localhost:5173`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_AD_LOCLIST_001 | Renders bảng | Renders bảng dữ liệu các địa điểm | Có địa điểm trong DB | Mở trang danh sách địa điểm. | | Hiển thị bảng gồm các cột: Tên địa điểm, Mô tả ngắn, Danh mục, Hình ảnh đại diện, Trạng thái (Hoạt động/Tạm ẩn), Thao tác. | | | |
| 2 | TC_AD_LOCLIST_002 | Tìm kiếm địa danh | Tìm nhanh địa điểm theo từ khóa | Có địa điểm khớp | 1. Nhập từ khóa tìm kiếm.<br>2. Nhấn Enter. | Từ khóa: `Bán đảo Sơn Trà` | Bảng cập nhật và chỉ hiển thị địa danh Bán đảo Sơn Trà. | | | |
| 3 | TC_AD_LOCLIST_003 | Xóa địa danh | Xóa địa danh khỏi hệ thống | Địa điểm không có tour liên kết | 1. Click nút "Xóa" tại dòng địa điểm.<br>2. Xác nhận xóa. | | Địa điểm bị xóa khỏi hệ thống. Nếu địa danh này đang thuộc hành trình của một tour du lịch nào đó, hệ thống chặn lại và báo lỗi. | | | |

## Ghi chú

-
