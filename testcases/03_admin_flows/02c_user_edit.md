# Màn hình Chỉnh sửa Người dùng (Edit User Page)

## Phạm vi

- Route: `/admin/users/edit/:id`
- API liên quan: Lấy chi tiết thông tin người dùng, cập nhật thông tin người dùng (PUT `/api/users/[id]`).
- Vai trò: Quản trị viên (Admin).

## Điều kiện trước

- Tài khoản: Đã đăng nhập vào trang quản trị bằng tài khoản Admin.
- Dữ liệu mẫu: Tài khoản cần sửa tồn tại trong DB.
- Môi trường: Local dev server (`http://localhost:5173`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_AD_UEDIT_001 | Tải thông tin | Kiểm tra hiển thị thông tin cũ của người dùng | Màn hình sửa mở sẵn | Truy cập trang Chỉnh sửa của người dùng. | | Tất cả các ô nhập liệu (Họ tên, Email, Số điện thoại, Vai trò) hiển thị đúng thông tin hiện có của tài khoản này. | | | |
| 2 | TC_AD_UEDIT_002 | Thay đổi thông tin | Chỉnh sửa và cập nhật thông tin cá nhân | | 1. Đổi Họ tên mới.<br>2. Nhập số điện thoại mới.<br>3. Bấm "Cập nhật". | Name: `Nguyen Van A V2`<br>Phone: `0901234567` | - Lưu thành công.<br>- Hiển thị thông báo toast thành công.<br>- Quay lại danh sách và kiểm tra thông tin mới đã được cập nhật. | | | |
| 3 | TC_AD_UEDIT_003 | Thay đổi Vai trò (Role) | Thay đổi phân quyền tài khoản | | 1. Tại dropdown Vai trò, chọn vai trò mới (từ Nhân viên sang Admin).<br>2. Nhấn "Cập nhật". | | Cập nhật thành công. Quyền hạn của tài khoản này thay đổi tương ứng khi đăng nhập lại. | | | |

## Ghi chú

-
