# Màn hình Chỉnh sửa Địa điểm (Edit Location Page)

## Phạm vi

- Route: `/admin/locations/edit/:id`
- API liên quan: Chi tiết địa điểm, cập nhật địa điểm (PUT `/api/locations/[id]`).
- Vai trò: Quản trị viên (Admin) / Nhân viên (Staff).

## Điều kiện trước

- Tài khoản: Đã đăng nhập vào trang quản trị bằng tài khoản Admin/Staff.
- Dữ liệu mẫu: Địa điểm cần sửa tồn tại trong DB.
- Môi trường: Local dev server (`http://localhost:5173`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_AD_LOCEDIT_001 | Tải thông tin cũ | Renders thông tin hiện tại của địa điểm lên form | Màn hình sửa mở sẵn | Truy cập trang Chỉnh sửa của địa điểm. | | Các trường (Tên, Mô tả ngắn, Mô tả chi tiết, Danh mục, Ảnh bìa) điền sẵn đúng thông tin của địa điểm này. | | | |
| 2 | TC_AD_LOCEDIT_002 | Thay đổi thông tin | Chỉnh sửa mô tả chi tiết địa điểm | | 1. Sửa nội dung Mô tả chi tiết.<br>2. Thay đổi hình ảnh đại diện.<br>3. Bấm "Cập nhật". | | Cập nhật thành công, lưu thông tin mới vào database và hiển thị toast báo thành công. | | | |

## Ghi chú

-
