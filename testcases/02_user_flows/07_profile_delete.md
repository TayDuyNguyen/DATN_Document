# Màn hình Xóa tài khoản (Delete Account Page)

## Phạm vi

- Route: `/profile/delete` hoặc `/[locale]/profile/delete`
- API liên quan: Xóa tài khoản người dùng (DELETE `/api/user/account`).
- Vai trò: Người dùng đã đăng nhập (User).

## Điều kiện trước

- Tài khoản: Đã đăng nhập vào hệ thống.
- Môi trường: Local dev server (`http://localhost:3000`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_ACCDELETE_001 | Ràng buộc đơn hàng hoạt động | Chặn xóa tài khoản khi đang có đơn hàng chờ đi hoặc chưa xử lý xong | Người dùng đang có đơn hàng ở trạng thái Pending hoặc Confirmed | Truy cập trang Xóa tài khoản. | | - Hệ thống hiển thị banner cảnh báo: "Bạn không thể xóa tài khoản vì đang có đơn đặt chỗ hoạt động".<br>- Checkbox xác nhận và ô nhập mật khẩu bị khóa (disabled).<br>- Có liên kết "Xem đơn hàng của tôi" dẫn về lịch sử đơn hàng. | | | |
| 2 | TC_ACCDELETE_002 | Đồng ý điều kiện | Kiểm tra yêu cầu tích chọn checkbox đồng ý chịu hệ quả | Người dùng không có đơn hàng hoạt động | 1. Điền mật khẩu chính xác.<br>2. Bỏ trống checkbox xác nhận.<br>3. Bấm "Xóa tài khoản". | Mật khẩu: `Password123!` | Chặn gửi yêu cầu, hiển thị lỗi "Bạn phải tích chọn đồng ý với các điều khoản xóa tài khoản". Nút gửi bị disabled. | | | |
| 3 | TC_ACCDELETE_003 | Kiểm tra mật khẩu | Kiểm tra yêu cầu nhập mật khẩu xác minh | | 1. Tích chọn checkbox xác nhận.<br>2. Để trống ô mật khẩu.<br>3. Bấm "Xóa tài khoản". | | Hệ thống yêu cầu nhập mật khẩu để tiếp tục. | | | |
| 4 | TC_ACCDELETE_004 | Nhập sai mật khẩu | Nhập mật khẩu xác minh không chính xác | | 1. Tích chọn checkbox xác nhận.<br>2. Nhập mật khẩu sai.<br>3. Bấm "Xóa tài khoản".<br>4. Xác nhận tiếp tục ở Modal. | Mật khẩu: `WrongPassword123` | Modal đóng, hiển thị thông báo lỗi "Mật khẩu xác thực không chính xác" ngay dưới ô nhập mật khẩu. Tài khoản không bị xóa. | | | |
| 5 | TC_ACCDELETE_005 | Modal xác nhận | Hiển thị hộp thoại cảnh báo cấp 2 (Confirmation Modal) | | 1. Tích chọn checkbox xác nhận.<br>2. Nhập mật khẩu chính xác.<br>3. Bấm "Xóa tài khoản". | Mật khẩu: `Password123!` | Hiển thị pop-up cảnh báo màu đỏ giữa màn hình yêu cầu xác nhận lần cuối: "Hành động này không thể hoàn tác. Bạn có chắc chắn?". | | | |
| 6 | TC_ACCDELETE_006 | Xác nhận xóa thành công | Hoàn tất quy trình xóa tài khoản | Mật khẩu đúng, đã tích chọn, bấm xác nhận ở Modal | 1. Thực hiện các bước điền form hợp lệ.<br>2. Tại Modal cảnh báo, click "Xác nhận xóa". | | Xóa tài khoản thành công:<br>- Token bị hủy bỏ, tự động đăng xuất người dùng.<br>- Hiển thị toast thông báo xóa tài khoản thành công.<br>- Chuyển hướng người dùng về Trang chủ (`/`). | | | |

## Ghi chú

-
