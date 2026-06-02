# Màn hình Cẩm nang du lịch Đà Nẵng (Danang Guide Landing Page)

## Phạm vi

- Route: `/du-lich-da-nang` hoặc `/[locale]/du-lich-da-nang`
- Vai trò: Khách vãng lai (Guest) / Người dùng đã đăng nhập (User).

## Điều kiện trước

- Môi trường: Local dev server (`http://localhost:3000`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_DNGUIDE_001 | Thông tin điểm đến | Kiểm tra hiển thị thông tin giới thiệu Đà Nẵng | Giao diện tải hoàn tất | Đọc nội dung giới thiệu chung về khí hậu, phương tiện di chuyển, thời điểm du lịch lý tưởng tại Đà Nẵng. | | Hiển thị đầy đủ nội dung, hình ảnh trực quan sinh động, bố cục đẹp mắt. | | | |
| 2 | TC_DNGUIDE_002 | Bản đồ địa điểm | Tương tác bản đồ số địa điểm gợi ý | | Click chọn các biểu tượng địa điểm vui chơi/ăn uống hiển thị trên bản đồ hướng dẫn du lịch Đà Nẵng. | | Hiển thị popover thông tin địa điểm tương ứng kèm khoảng cách hoặc hướng dẫn đi lại nhanh. | | | |
| 3 | TC_DNGUIDE_003 | Click Tour đi ngay | Xem danh sách các tour đề xuất cho kỳ nghỉ Đà Nẵng | | Click nút "Xem Tour du lịch Đà Nẵng" tại trang cẩm nang. | | Chuyển hướng thành công tới trang danh sách tour (`/tours`) đã được lọc sẵn địa điểm đến là Đà Nẵng. | | | |

## Ghi chú

-
