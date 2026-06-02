# Màn hình Chỉnh sửa thông tin cá nhân (Profile Edit Page)

## Phạm vi

- Route: `/profile` hoặc `/settings` hoặc `/[locale]/profile`
- API liên quan: Lấy thông tin cá nhân, cập nhật thông tin cá nhân (PUT/PATCH `/api/user/profile`), upload avatar (POST `/api/user/avatar`).
- Vai trò: Người dùng đã đăng nhập (User).

## Điều kiện trước

- Tài khoản: Đã đăng nhập vào hệ thống bằng tài khoản người dùng hợp lệ.
- Môi trường: Local dev server (`http://localhost:3000`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_PROFILE_001 | Tải thông tin cũ | Đọc thông tin cá nhân hiện tại | Đăng nhập thành công | Truy cập trang Chỉnh sửa thông tin cá nhân. | | Tất cả các trường (Họ và tên, Số điện thoại, Ngày sinh, Giới tính, Thành phố) tự động điền sẵn (pre-fill) thông tin hiện có của người dùng. | | | |
| 2 | TC_PROFILE_002 | Đổi ảnh đại diện | Cập nhật ảnh đại diện (Avatar) | | 1. Di chuột lên ảnh đại diện và click vào icon máy ảnh.<br>2. Chọn một tệp hình ảnh có định dạng hợp lệ (JPG, PNG, JPEG). | File: `avatar.png` (2MB) | - Giao diện hiển thị loading trong lúc upload.<br>- Upload thành công: ảnh xem trước cập nhật ngay lập tức.<br>- Avatar trên Header thay đổi theo. | | | |
| 3 | TC_PROFILE_003 | Loại file Avatar | Lọc định dạng file avatar không hợp lệ | | 1. Chọn file không phải ảnh (Ví dụ: `.pdf`, `.docx`). | File: `document.pdf` | Hệ thống chặn hoặc báo lỗi không hỗ trợ định dạng file này. Không cho phép tải lên. | | | |
| 4 | TC_PROFILE_004 | Validate Họ và tên | Kiểm tra trường Họ và tên trống | | 1. Xóa sạch thông tin ở ô Họ tên.<br>2. Click nút "Lưu thay đổi". | Name: ` ` | Cảnh báo trường Họ tên không được để trống. Nút lưu bị vô hiệu hóa hoặc chặn gửi form. | | | |
| 5 | TC_PROFILE_005 | Validate SĐT | Kiểm tra định dạng số điện thoại không hợp lệ | | 1. Nhập số điện thoại chứa ký tự chữ hoặc không đúng độ dài. | Phone: `090abc`<br>hoặc `1234` | Hiển thị cảnh báo số điện thoại không hợp lệ ngay dưới ô nhập. | | | |
| 6 | TC_PROFILE_006 | Hủy thay đổi (Cancel/Reset) | Hủy các chỉnh sửa vừa nhập | Đã thay đổi một vài ô nhập liệu | Click nút "Hủy" (Cancel hoặc Reset). | | Toàn bộ dữ liệu trong form quay trở về trạng thái ban đầu khi chưa chỉnh sửa. Các thông báo lỗi (nếu có) bị xóa bỏ. | | | |
| 7 | TC_PROFILE_007 | Cập nhật thành công | Lưu thông tin chỉnh sửa hợp lệ thành công | Dữ liệu nhập hợp lệ | 1. Nhập thông tin thay đổi hợp lệ ở các trường.<br>2. Nhấn "Lưu thay đổi". | Name: `Nguyen Van B`<br>Phone: `0905123456`<br>Birthdate: `1998-10-15`<br>Gender: `male` | Lưu thành công:<br>- Hiển thị toast thông báo thành công.<br>- Dữ liệu mới được đồng bộ lên Header.<br>- Tải lại trang vẫn giữ thông tin mới. | | | |

## Ghi chú

-
