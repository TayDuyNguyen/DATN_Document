# Màn hình Đổi mật khẩu (Password Change Form)

## Phạm vi

- Route: `/profile` hoặc `/settings` hoặc `/[locale]/settings` (phần đổi mật khẩu)
- API liên quan: Thay đổi mật khẩu (POST/PUT `/api/user/change-password`).
- Vai trò: Người dùng đã đăng nhập (User).

## Điều kiện trước

- Tài khoản: Đã đăng nhập vào hệ thống, mật khẩu hiện tại là `Password123!`.
- Môi trường: Local dev server (`http://localhost:3000`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_PWCHANGE_001 | Trường bắt buộc | Kiểm tra khi gửi form trống | Giao diện đổi mật khẩu hiển thị | Bấm nút "Cập nhật mật khẩu" mà không điền thông tin gì. | | Hệ thống chặn gửi form và hiển thị thông báo lỗi yêu cầu điền đầy đủ các trường mật khẩu. | | | |
| 2 | TC_PWCHANGE_002 | Đo độ mạnh mật khẩu | Kiểm tra bộ đo độ mạnh mật khẩu mới (Realtime Strength Meter) | | 1. Nhập mật khẩu mới ngắn.<br>2. Nhập thêm chữ hoa, số, ký tự đặc biệt từng bước một. | 1. `123`<br>2. `Abc12345!` | - Thanh đo độ mạnh hiển thị mức đỏ/Weak khi mật khẩu quá ngắn.<br>- Thanh đo chuyển sang cam/vàng/xanh lá kèm chữ Strong khi đáp ứng đủ tiêu chuẩn tối thiểu 8 ký tự, có chữ hoa, thường, số, ký tự đặc biệt. | | | |
| 3 | TC_PWCHANGE_003 | Khớp mật khẩu mới | Kiểm tra xác nhận mật khẩu mới không khớp | | 1. Nhập Mật khẩu hiện tại.<br>2. Nhập Mật khẩu mới hợp lệ.<br>3. Nhập Xác nhận mật khẩu mới không giống mật khẩu mới.<br>4. Nhấn "Cập nhật mật khẩu". | Current: `Password123!`<br>New: `NewPassword123!`<br>Confirm: `NewPassword123?` | Trình duyệt hoặc form hiển thị cảnh báo "Mật khẩu xác nhận không trùng khớp". Nút cập nhật bị vô hiệu hóa. | | | |
| 4 | TC_PWCHANGE_004 | Sai mật khẩu cũ | Nhập sai mật khẩu hiện tại | | 1. Nhập sai Mật khẩu hiện tại.<br>2. Nhập Mật khẩu mới hợp lệ và trùng khớp xác nhận.<br>3. Nhấn "Cập nhật mật khẩu". | Current: `WrongCurrent123`<br>New: `NewPassword123!`<br>Confirm: `NewPassword123!` | Phản hồi lỗi từ API. Form hiển thị lỗi ngay dưới ô nhập Mật khẩu hiện tại (ví dụ: "Mật khẩu hiện tại không chính xác"). | | | |
| 5 | TC_PWCHANGE_005 | Đổi thành công | Đổi mật khẩu thành công với thông tin đúng | Mật khẩu hiện tại đúng, mật khẩu mới thỏa mãn yêu cầu | 1. Nhập đúng Mật khẩu hiện tại.<br>2. Nhập Mật khẩu mới hợp lệ.<br>3. Nhập trùng khớp Xác nhận mật khẩu mới.<br>4. Nhấn "Cập nhật mật khẩu". | Current: `Password123!`<br>New: `NewPassword123!`<br>Confirm: `NewPassword123!` | Đổi thành công:<br>- Hiển thị toast thông báo đổi mật khẩu thành công.<br>- Form được dọn sạch dữ liệu.<br>- Lần đăng nhập tiếp theo bắt buộc dùng mật khẩu mới. | | | |

## Ghi chú

-
