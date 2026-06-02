# Màn hình Quản lý Danh mục Địa điểm (Location Categories Management)

## Phạm vi

- Route: `/admin/locations/categories`
- API liên quan: Thêm/Sửa/Xóa phân loại danh mục địa danh/địa điểm.
- Vai trò: Quản trị viên (Admin) / Nhân viên (Staff).

## Điều kiện trước

- Tài khoản: Đã đăng nhập vào trang quản trị bằng tài khoản Admin/Staff.
- Môi trường: Local dev server (`http://localhost:5173`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_AD_LOCCAT_001 | Danh sách danh mục | Hiển thị danh sách các danh mục địa điểm | | Truy cập trang Quản lý Danh mục Địa điểm. | | Renders bảng chứa các danh mục gồm: Tên danh mục (ví dụ: Bãi biển, Di tích lịch sử, Đền chùa), Slug, Mô tả ngắn, Số lượng địa điểm đang thuộc danh mục này. | | | |
| 2 | TC_AD_LOCCAT_002 | Thêm danh mục thành công | Tạo mới một danh mục địa điểm thành công | Tên danh mục chưa tồn tại | 1. Nhập Tên danh mục.<br>2. Nhập Mô tả ngắn.<br>3. Bấm "Lưu". | Tên: "Khu Vui Chơi"<br>Slug: `khu-vui-choi` | Danh mục mới được tạo thành công, xuất hiện ở bảng danh sách và hiển thị ở dropdown khi tạo/sửa địa điểm mới. | | | |
| 3 | TC_AD_LOCCAT_003 | Chỉnh sửa danh mục | Cập nhật thông tin danh mục địa điểm | Danh mục cần sửa tồn tại | 1. Click nút "Sửa" tại danh mục.<br>2. Sửa thông tin mô tả.<br>3. Nhấn "Cập nhật". | | Lưu thành công thông tin mới. | | | |
| 4 | TC_AD_LOCCAT_004 | Xóa danh mục | Xóa danh mục địa điểm khỏi hệ thống | Danh mục không chứa địa điểm nào | 1. Click nút "Xóa" tại danh mục.<br>2. Xác nhận xóa. | | Danh mục bị xóa khỏi hệ thống. Nếu danh mục đang chứa địa danh liên kết, hệ thống báo lỗi không cho xóa. | | | |

## Ghi chú

-
