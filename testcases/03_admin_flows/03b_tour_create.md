# Màn hình Thêm mới Tour (Create Tour Page)

## Phạm vi

- Route: `/admin/tours/create`
- API liên quan: Thêm tour mới, upload hình ảnh tour lên CDN/Server.
- Vai trò: Quản trị viên (Admin) / Nhân viên (Staff).

## Điều kiện trước

- Tài khoản: Đã đăng nhập vào trang quản trị bằng tài khoản Admin/Staff.
- Môi trường: Local dev server (`http://localhost:5173`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_AD_TCREATE_001 | Validate form trống | Kiểm tra validate các trường bắt buộc | Màn hình Thêm mới mở sẵn | Bấm "Lưu" mà không nhập thông tin. | | Hệ thống hiển thị cảnh báo lỗi màu đỏ tại các trường bắt buộc: Tên tour, Điểm xuất phát, Thời lượng, Giá người lớn, Danh mục. | | | |
| 2 | TC_AD_TCREATE_002 | Tải lên nhiều ảnh | Tải lên bộ sưu tập ảnh cho tour | | 1. Tại khu vực hình ảnh, chọn tải lên 3 file ảnh.<br>2. Nhấn tải lên. | Ảnh: `gallery1.jpg`, `gallery2.png` | Hiển thị thumbnail của các ảnh vừa tải lên. Có thể chọn một ảnh làm ảnh bìa chính (cover) và có nút để xóa ảnh lỗi. | | | |
| 3 | TC_AD_TCREATE_003 | Thiết lập hành trình | Thêm thông tin hành trình chi tiết (Itinerary Builder) | | 1. Bấm nút "Thêm ngày" trong phần lịch trình.<br>2. Nhập Tiêu đề ngày.<br>3. Nhập Nội dung chi tiết các điểm đi qua. | Ngày 1: "Đón sân bay - Bán đảo Sơn Trà" | Hành trình được lưu dưới cấu trúc mảng động, cho phép thêm nhiều ngày không giới hạn. | | | |
| 4 | TC_AD_TCREATE_004 | Thêm thành công | Tạo mới một tour hoàn chỉnh thành công | Thông tin hợp lệ | 1. Nhập đầy đủ thông tin bắt buộc.<br>2. Tải ảnh lên.<br>3. Thiết lập lịch trình.<br>4. Nhấn "Lưu". | Tên: "Tour Ngũ Hành Sơn - Hội An 1 Ngày" | - Tạo tour thành công.<br>- Hiển thị thông báo toast thành công.<br>- Chuyển hướng về trang danh sách tour.<br>- Tour mới xuất hiện ở đầu bảng. | | | |

## Ghi chú

-
