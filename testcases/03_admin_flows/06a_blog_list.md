# Màn hình Danh sách Bài viết (Blog Posts List Page)

## Phạm vi

- Route: `/admin/blog`
- API liên quan: Lấy danh sách toàn bộ các bài viết blog có bộ lọc chuyên mục và tìm kiếm.
- Vai trò: Quản trị viên (Admin) / Nhân viên (Staff).

## Điều kiện trước

- Tài khoản: Đã đăng nhập vào trang quản trị bằng tài khoản Admin/Staff.
- Môi trường: Local dev server (`http://localhost:5173`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_AD_BLOGLIST_001 | Renders bảng | Renders bảng dữ liệu các bài viết blog | Có bài viết trong DB | Mở trang danh sách bài viết. | | Hiển thị bảng gồm các cột: Tiêu đề, Chuyên mục, Tác giả, Lượt xem, Trạng thái (Bản nháp/Xuất bản), Ngày đăng, Thao tác. | | | |
| 2 | TC_AD_BLOGLIST_002 | Tìm kiếm nhanh | Tìm kiếm bài viết theo tiêu đề | Có bài viết khớp | 1. Nhập từ khóa tìm kiếm.<br>2. Nhấn Enter. | Từ khóa: `Ẩm thực Đà Nẵng` | Bảng cập nhật hiển thị các bài viết có tiêu đề chứa từ khóa `Ẩm thực Đà Nẵng`. | | | |
| 3 | TC_AD_BLOGLIST_003 | Lọc chuyên mục | Lọc danh sách bài viết theo chuyên mục | | Chọn chuyên mục bài viết từ dropdown bộ lọc. | Chuyên mục: `Kinh nghiệm` | Chỉ hiển thị các bài viết thuộc chuyên mục Kinh nghiệm. | | | |
| 4 | TC_AD_BLOGLIST_004 | Xóa bài viết | Xóa bài viết khỏi hệ thống | | 1. Click nút "Xóa" tại dòng bài viết.<br>2. Xác nhận xóa. | | Bài viết bị xóa khỏi hệ thống. Danh sách bài viết cập nhật lại tức thì. | | | |

## Ghi chú

-
