# Màn hình Quản lý Danh mục Bài viết (Blog Categories Management)

## Phạm vi

- Route: `/admin/blog/categories`
- API liên quan: Thêm/Sửa/Xóa phân loại bài viết blog.
- Vai trò: Quản trị viên (Admin) / Nhân viên (Staff).

## Điều kiện trước

- Tài khoản: Đã đăng nhập vào trang quản trị bằng tài khoản Admin/Staff.
- Môi trường: Local dev server (`http://localhost:5173`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_AD_BLOGCAT_001 | Danh sách danh mục | Hiển thị danh sách các chuyên mục bài viết | | Truy cập trang Quản lý Danh mục Bài viết. | | Renders bảng chứa các chuyên mục bài viết gồm: Tên chuyên mục (ví dụ: Kinh nghiệm du lịch, Ẩm thực Đà Nẵng, Tin tức sự kiện), Slug, Mô tả ngắn, Số lượng bài viết đang thuộc chuyên mục này. | | | |
| 2 | TC_AD_BLOGCAT_002 | Thêm danh mục thành công | Tạo mới một chuyên mục bài viết thành công | Tên chuyên mục chưa tồn tại | 1. Nhập Tên chuyên mục.<br>2. Nhập Mô tả.<br>3. Bấm "Lưu". | Tên: "Cẩm Nang Ăn Uống"<br>Slug: `cam-nang-an-uong` | Chuyên mục mới được tạo thành công, xuất hiện ở bảng danh sách và hiển thị ở phần chọn chuyên mục khi tạo/sửa bài viết blog mới. | | | |
| 3 | TC_AD_BLOGCAT_003 | Chỉnh sửa danh mục | Cập nhật thông tin chuyên mục bài viết | Chuyên mục cần sửa tồn tại | 1. Click nút "Sửa" chuyên mục.<br>2. Sửa thông tin.<br>3. Nhấn "Cập nhật". | | Lưu thành công thông tin mới. | | | |
| 4 | TC_AD_BLOGCAT_004 | Xóa danh mục | Xóa chuyên mục bài viết khỏi hệ thống | Chuyên mục không chứa bài viết nào | 1. Click nút "Xóa" chuyên mục.<br>2. Xác nhận xóa. | | Chuyên mục bị xóa khỏi hệ thống. Nếu chuyên mục đang chứa bài viết hoạt động, hệ thống báo lỗi không cho xóa. | | | |

## Ghi chú

-
