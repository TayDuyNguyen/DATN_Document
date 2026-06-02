# Màn hình Lịch khởi hành mở rộng (Tour Departures Calendar Page)

## Phạm vi

- Route: `/tours/[slug]/departures` hoặc `/[locale]/tours/[slug]/departures`
- API liên quan: Lấy toàn bộ lịch khởi hành trong tháng/năm của một tour cụ thể, kiểm tra tình trạng số ghế còn trống.
- Vai trò: Khách vãng lai (Guest) / Người dùng đã đăng nhập (User).

## Điều kiện trước

- Dữ liệu mẫu: Tour có lịch khởi hành được thiết lập trong nhiều tháng tới.
- Môi trường: Local dev server (`http://localhost:3000`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_DEPART_001 | Renders Calendar | Hiển thị lịch khởi hành dạng lịch tháng (Calendar View) | Trang chi tiết lịch khởi hành mở sẵn | Xem giao diện lịch tháng hiển thị. | | Renders bảng lịch của tháng hiện tại. Các ngày có lịch khởi hành được highlight (ví dụ: khoanh tròn hồng hoặc có dấu hiệu riêng), hiển thị giá tiền và số chỗ còn lại trực tiếp trên ô ngày. | | | |
| 2 | TC_DEPART_002 | Chuyển tháng (Next/Prev Month) | Kiểm tra nút chuyển qua lại các tháng | | Click nút mũi tên chuyển sang tháng sau hoặc quay lại tháng trước. | | Lịch chuyển tháng mượt mà, tải dữ liệu lịch khởi hành của tháng mới từ API tương ứng. | | | |
| 3 | TC_DEPART_003 | Hover xem nhanh | Xem nhanh thông tin khi di chuột vào ô ngày | | Di chuột (hover) vào ngày có lịch khởi hành. | | Hiển thị một tooltip nhỏ chứa thông tin: Tình trạng (Còn chỗ / Sắp đầy / Hết chỗ), số người đã đặt, giá người lớn/trẻ em chi tiết. | | | |
| 4 | TC_DEPART_004 | Click chọn ngày đặt | Click chọn ngày đi từ lịch để tiến hành đặt tour | | Click chọn vào một ngày còn chỗ trống trên lịch. | | Chuyển hướng người dùng sang trang biểu mẫu đặt tour (`/tours/[slug]/book?schedule_id=...`) với tham số ngày đi được chọn sẵn. | | | |

## Ghi chú

-
