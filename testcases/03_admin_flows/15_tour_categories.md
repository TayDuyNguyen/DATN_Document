# Màn hình Quản lý Danh mục Tour (Tour Categories Management)

## Phạm vi

- Route: `/admin/tours/categories`
- API liên quan: Thêm/Sửa/Xóa phân loại danh mục tour.
- Vai trò: Quản trị viên (Admin) / Nhân viên (Staff).

## Điều kiện trước

- Tài khoản: Đã đăng nhập vào trang quản trị bằng tài khoản Admin/Staff.
- Môi trường: Local dev server (`http://localhost:5173`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_AD_TOURCAT_001 | Danh sách danh mục | Hiển thị danh sách các danh mục tour | | Truy cập trang Quản lý Danh mục Tour. | | Renders bảng/lưới chứa các danh mục gồm: Tên danh mục (ví dụ: Tour Trong Ngày, Tour Dài Ngày), Slug, Mô tả ngắn, Icon hiển thị, Số lượng tour đang thuộc danh mục. | | | |
| 2 | TC_AD_TOURCAT_002 | Thêm danh mục - Validate | Kiểm tra trường bắt buộc khi tạo danh mục mới | Màn hình Thêm danh mục mở sẵn | Bấm "Lưu" mà không điền thông tin gì. | | Hệ thống báo lỗi trường Tên danh mục không được để trống. | | | |
| 3 | TC_AD_TOURCAT_003 | Thêm danh mục thành công | Tạo mới một danh mục tour thành công | Tên danh mục chưa tồn tại | 1. Nhập Tên danh mục.<br>2. Nhập Mô tả và chọn Icon đại diện.<br>3. Bấm "Lưu". | Tên: "Tour Du Thuyền"<br>Slug: `tour-du-thuyen` | Danh mục mới được tạo thành công, tự động tạo slug thân thiện, hiển thị trong danh sách và xuất hiện ở phần chọn danh mục khi thêm/sửa tour mới. | | | |
| 4 | TC_AD_TOURCAT_004 | Chỉnh sửa danh mục | Cập nhật thông tin danh mục tour | Danh mục cần sửa tồn tại | 1. Click nút "Sửa" tại dòng danh mục.<br>2. Thay đổi mô tả.<br>3. Nhấn "Cập nhật". | | Thông tin lưu lại thành công, cập nhật ngay lập tức giao diện. | | | |
| 5 | TC_AD_TOURCAT_005 | Xóa danh mục | Xóa danh mục tour khỏi hệ thống | Danh mục không chứa tour nào hoạt động | 1. Click nút "Xóa" tại danh mục.<br>2. Xác nhận xóa. | | Danh mục bị xóa khỏi hệ thống. Nếu danh mục đang có tour thuộc về nó, hệ thống báo lỗi chặn không cho xóa để tránh lỗi mồ côi dữ liệu. | | | |

## Ghi chú

-
