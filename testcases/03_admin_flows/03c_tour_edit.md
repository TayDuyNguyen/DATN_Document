# Màn hình Chỉnh sửa Tour (Edit Tour Page)

## Phạm vi

- Route: `/admin/tours/[id]/edit`
- API liên quan: Chi tiết tour du lịch, cập nhật tour du lịch (PUT `/api/tours/[id]`).
- Vai trò: Quản trị viên (Admin) / Nhân viên (Staff).

## Điều kiện trước

- Tài khoản: Đã đăng nhập vào trang quản trị bằng tài khoản Admin/Staff.
- Dữ liệu mẫu: Tour cần sửa tồn tại trong DB.
- Môi trường: Local dev server (`http://localhost:5173`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_AD_TEDIT_001 | Tải thông tin cũ | Renders thông tin hiện có của tour lên biểu mẫu | Màn hình sửa mở sẵn | Truy cập trang Chỉnh sửa của tour du lịch. | | Tất cả các ô nhập liệu (Tên, Mô tả, Lịch trình, Giá cả, Ảnh đại diện, FAQ) điền sẵn đúng thông tin của tour hiện tại. | | | |
| 2 | TC_AD_TEDIT_002 | Thay đổi thông tin | Chỉnh sửa tên và cập nhật mức giá của tour | | 1. Thay đổi Tên tour.<br>2. Thay đổi Giá người lớn.<br>3. Bấm "Cập nhật". | Giá: `600,000` | Cập nhật thành công, lưu thông tin mới vào database và hiển thị toast báo thành công. | | | |
| 3 | TC_AD_TEDIT_003 | Quản lý hình ảnh | Thêm/Xóa hình ảnh hiện tại của tour | | 1. Click nút "Xóa" tại 1 hình ảnh cũ.<br>2. Chọn tải lên 1 hình ảnh mới.<br>3. Bấm "Cập nhật". | | Ảnh cũ bị loại bỏ, ảnh mới được tải lên và lưu làm tài nguyên của tour thành công. | | | |

## Ghi chú

-
