# Màn hình Quản lý Khuyến mãi & Mã giảm giá (Promotions & Vouchers)

## Phạm vi

- Route: `/admin/promotions` (danh sách và biểu mẫu thêm/sửa)
- API liên quan: Thêm/Sửa/Xóa mã giảm giá (Vouchers), kiểm tra tính hợp lệ của mã giảm giá khi áp dụng.
- Vai trò: Quản trị viên (Admin) / Nhân viên (Staff).

## Điều kiện trước

- Tài khoản: Đã đăng nhập vào trang quản trị bằng tài khoản Admin/Staff.
- Môi trường: Local dev server (`http://localhost:5173`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_AD_PROM_001 | Thêm Voucher - Validate | Kiểm tra các trường bắt buộc khi tạo mã giảm giá | Màn hình Thêm mã giảm giá mở sẵn | Nhấn nút "Lưu" mà không điền thông tin. | | Hệ thống chặn lưu và hiển thị cảnh báo lỗi tại các trường bắt buộc: Mã giảm giá (Code), Loại giảm giá (Phần trăm / Số tiền cố định), Giá trị giảm giá, Ngày bắt đầu, Ngày kết thúc, Giới hạn lượt sử dụng. | | | |
| 2 | TC_AD_PROM_002 | Thêm Voucher thành công | Tạo mới mã giảm giá phần trăm thành công | | 1. Điền Mã giảm giá (ví dụ: `HELLOSUMMER`).<br>2. Chọn loại giảm giá là "Phần trăm".<br>3. Nhập giá trị giảm giá (ví dụ: `15`).<br>4. Chọn Ngày bắt đầu là ngày hiện tại, Ngày kết thúc là ngày trong tương lai.<br>5. Bấm "Lưu". | Mã: `HELLOSUMMER`<br>Loại: `%`<br>Giá trị: `15`<br>Giới hạn: `100` | Tạo thành công mã giảm giá. Mã hiển thị trong bảng danh sách và khách hàng có thể áp dụng mã giảm giá 15% này tại bước đặt tour trên Web client. | | | |
| 3 | TC_AD_PROM_003 | Loại giảm giá cố định | Tạo mới mã giảm giá theo số tiền cố định | | 1. Chọn loại giảm giá là "Số tiền cố định" (Fixed Amount).<br>2. Nhập giá trị giảm giá (ví dụ: `200000`).<br>3. Bấm "Lưu". | Loại: `Fixed`<br>Giá trị: `200,000đ` | Tạo mã giảm giá thành công. Khi khách hàng áp dụng mã này tại Web client, tổng hóa đơn sẽ được trừ trực tiếp `200,000đ`. | | | |
| 4 | TC_AD_PROM_004 | Validate Hạn dùng | Kiểm tra thiết lập ngày kết thúc nhỏ hơn ngày bắt đầu | | 1. Nhập Ngày bắt đầu là ngày hiện tại.<br>2. Nhập Ngày kết thúc là một ngày trong quá khứ.<br>3. Nhấn nút "Lưu". | Bắt đầu: `2026-06-01`<br>Kết thúc: `2026-05-30` | Hệ thống báo lỗi logic thời gian "Ngày kết thúc không được nhỏ hơn ngày bắt đầu", chặn không cho phép tạo mã giảm giá. | | | |
| 5 | TC_AD_PROM_005 | Trạng thái mã | Tắt kích hoạt hoạt động của mã giảm giá (Deactivate) | Mã giảm giá đang ở trạng thái Hoạt động (Active) | 1. Tìm mã giảm giá cần tắt kích hoạt trong bảng.<br>2. Bật tắt switch Trạng thái ở dòng tương ứng. | | Mã chuyển sang trạng thái "Không hoạt động" (Inactive). Khi áp dụng mã này trên Web client, hệ thống sẽ báo lỗi mã không hợp lệ hoặc đã hết hạn. | | | |
| 6 | TC_AD_PROM_006 | Xóa Voucher | Xóa mã giảm giá khỏi hệ thống | Mã giảm giá tồn tại | 1. Click nút "Xóa" trên dòng mã giảm giá.<br>2. Xác nhận xóa. | | Mã giảm giá bị xóa hoàn toàn khỏi hệ thống, danh sách cập nhật lại và không còn khả năng áp dụng mã này nữa. | | | |

## Ghi chú

-
