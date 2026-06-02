# Màn hình Chỉnh sửa Bài viết (Edit Blog Post Page)

## Phạm vi

- Route: `/admin/blog-posts/edit/:id`
- API liên quan: Chi tiết bài viết, cập nhật bài viết (PUT `/api/blog/[id]`).
- Vai trò: Quản trị viên (Admin) / Nhân viên (Staff).

## Điều kiện trước

- Tài khoản: Đã đăng nhập vào trang quản trị bằng tài khoản Admin/Staff.
- Dữ liệu mẫu: Bài viết cần sửa tồn tại trong DB.
- Môi trường: Local dev server (`http://localhost:5173`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_AD_BLOGEDIT_001 | Tải thông tin cũ | Renders nội dung bài viết hiện tại lên form | Màn hình sửa mở sẵn | Truy cập trang Chỉnh sửa của bài viết. | | Các trường (Tiêu đề, Chuyên mục, Ảnh bìa, Trình soạn thảo nội dung) điền sẵn đúng thông tin của bài viết này. | | | |
| 2 | TC_AD_BLOGEDIT_002 | Thay đổi nội dung | Chỉnh sửa và cập nhật bài viết | | 1. Sửa Tiêu đề bài viết.<br>2. Sửa nội dung văn bản trong trình soạn thảo.<br>3. Thay đổi hình ảnh bìa.<br>4. Nhấn "Cập nhật". | | Cập nhật thành công, lưu thông tin mới vào database và hiển thị toast báo thành công. Web client hiển thị nội dung mới. | | | |

## Ghi chú

-
