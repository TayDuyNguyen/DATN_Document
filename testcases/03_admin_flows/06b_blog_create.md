# Màn hình Thêm mới Bài viết (Create Blog Post Page)

## Phạm vi

- Route: `/admin/blog/create`
- API liên quan: Thêm bài viết mới (POST `/api/blog`), tải hình ảnh bìa bài viết.
- Vai trò: Quản trị viên (Admin) / Nhân viên (Staff).

## Điều kiện trước

- Tài khoản: Đã đăng nhập vào trang quản trị bằng tài khoản Admin/Staff.
- Môi trường: Local dev server (`http://localhost:5173`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_AD_BLOGCREATE_001 | Validate form trống | Kiểm tra validate các trường bắt buộc | Màn hình Thêm mới mở sẵn | Bấm "Lưu" hoặc "Xuất bản" mà không điền thông tin. | | Hệ thống chặn submit và báo lỗi tại các trường bắt buộc: Tiêu đề, Chuyên mục, Ảnh bìa, Nội dung bài viết. | | | |
| 2 | TC_AD_BLOGCREATE_002 | Trình soạn thảo Rich Text | Nhập nội dung định dạng bài viết | | 1. Nhập văn bản vào trình soạn thảo WYSIWYG.<br>2. Thử định dạng tiêu đề phụ H2, H3, chữ in đậm và chèn liên kết. | | Định dạng hiển thị chính xác trong khung soạn thảo và lưu trữ cấu trúc HTML/Markdown tương thích gửi lên server. | | | |
| 3 | TC_AD_BLOGCREATE_003 | Lưu bản nháp (Draft) | Tạo bài viết ở trạng thái Bản nháp | Dữ liệu hợp lệ | 1. Điền thông tin bài viết.<br>2. Tại dropdown trạng thái, chọn "Bản nháp" (Draft).<br>3. Nhấn "Lưu". | | Bài viết được lưu thành công nhưng không hiển thị công khai ở Web client. | | | |
| 4 | TC_AD_BLOGCREATE_004 | Xuất bản (Publish) | Tạo và xuất bản bài viết hiển thị ra web | Dữ liệu hợp lệ | 1. Điền thông tin bài viết.<br>2. Tại dropdown trạng thái, chọn "Xuất bản" (Published).<br>3. Nhấn "Xuất bản". | Tiêu đề: "Ăn gì ở Đà Nẵng: Top 10 món ngon..." | Bài viết tạo thành công và xuất hiện tức thì trên trang danh sách cẩm nang công cộng phía Web client. | | | |

## Ghi chú

-
