# Màn hình Thêm mới Người dùng (Create User Page)

## Phạm vi

- Route: `/admin/users/create`
- API liên quan: Thêm tài khoản người dùng mới (POST `/api/users`).
- Vai trò: Quản trị viên (Admin).

## Điều kiện trước

- Tài khoản: Đã đăng nhập vào trang quản trị bằng tài khoản Admin.
- Môi trường: Local dev server (`http://localhost:5173`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_AD_UCREATE_001 | Validate form trống | Kiểm tra validate các trường bắt buộc | Màn hình Thêm mới mở sẵn | Bấm nút "Lưu" mà không điền thông tin. | | Hệ thống chặn submit và hiển thị lỗi validate tại các trường bắt buộc: Họ tên, Email, Mật khẩu, Vai trò. | | | |
| 2 | TC_AD_UCREATE_002 | Định dạng Email | Kiểm tra validate định dạng email | | 1. Điền Họ tên hợp lệ.<br>2. Nhập Email sai cú pháp.<br>3. Bấm "Lưu". | Email: `invalidemail` | Hiển thị lỗi thông báo định dạng Email không hợp lệ. | | | |
| 3 | TC_AD_UCREATE_003 | Trùng Email | Thêm người dùng với Email đã tồn tại | Email đã có trong hệ thống | 1. Điền đầy đủ thông tin.<br>2. Nhập Email trùng.<br>3. Bấm "Lưu". | Email: `exist@test.com` | Nhận phản hồi lỗi từ API. Form hiển thị cảnh báo Email đã được sử dụng. | | | |
| 4 | TC_AD_UCREATE_004 | Thêm thành công | Kiểm tra luồng thêm người dùng hợp lệ thành công | Email chưa tồn tại | 1. Nhập Họ tên.<br>2. Nhập Email mới.<br>3. Nhập mật khẩu.<br>4. Chọn vai trò (Staff/Nhân viên).<br>5. Bấm "Lưu". | Name: `Tran Van C`<br>Email: `tranc@test.com`<br>Password: `Pass123!` | Tạo thành công:<br>- Hiển thị toast thông báo thành công.<br>- Chuyển hướng về trang danh sách người dùng.<br>- Tài khoản mới xuất hiện trong danh sách. | | | |

## Ghi chú

-
