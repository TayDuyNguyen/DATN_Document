# Màn hình Thêm mới Địa điểm (Create Location Page)

## Phạm vi

- Route: `/admin/locations/create`
- API liên quan: Thêm địa điểm mới (POST `/api/locations`), tải hình ảnh đại diện địa điểm.
- Vai trò: Quản trị viên (Admin) / Nhân viên (Staff).

## Điều kiện trước

- Tài khoản: Đã đăng nhập vào trang quản trị bằng tài khoản Admin/Staff.
- Môi trường: Local dev server (`http://localhost:5173`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_AD_LOCCREATE_001 | Validate form trống | Kiểm tra validate các trường bắt buộc | Màn hình Thêm mới mở sẵn | Bấm "Lưu" mà không điền thông tin. | | Hệ thống chặn submit và báo lỗi tại các trường bắt buộc: Tên địa điểm, Mô tả ngắn, chọn Danh mục địa danh. | | | |
| 2 | TC_AD_LOCCREATE_002 | Thêm thành công | Kiểm tra luồng tạo một địa điểm du lịch mới thành công | Dữ liệu nhập hợp lệ | 1. Điền Tên địa điểm.<br>2. Nhập mô tả ngắn và mô tả chi tiết.<br>3. Chọn Danh mục địa điểm.<br>4. Tải lên hình ảnh.<br>5. Bấm "Lưu". | Tên: "Ngũ Hành Sơn"<br>Mô tả: "Quần thể 5 ngọn núi đá vôi..." | - Tạo thành công.<br>- Hiển thị toast thông báo thành công.<br>- Chuyển hướng về trang danh sách địa điểm.<br>- Địa điểm mới xuất hiện ở đầu bảng. | | | |

## Ghi chú

-
