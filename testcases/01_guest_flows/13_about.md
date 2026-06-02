# Màn hình Giới thiệu (About Page)

## Phạm vi

- Route: `/about` hoặc `/[locale]/about`
- Vai trò: Khách vãng lai (Guest) / Người dùng đã đăng nhập (User).

## Điều kiện trước

- Môi trường: Local dev server (`http://localhost:3000`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_ABOUT_001 | Hiển thị thông tin | Kiểm tra hiển thị thông tin giới thiệu công ty | Giao diện tải hoàn tất | Đọc nội dung tiêu đề, giới thiệu sứ mệnh, tầm nhìn, và đội ngũ thành viên sáng lập DaNangTrip. | | Văn bản giới thiệu hiển thị rõ ràng, đúng chính tả, bố cục hình ảnh và text cân đối. | | | |
| 2 | TC_ABOUT_002 | Responsive layout | Kiểm tra hiển thị co giãn trên thiết bị di động | | Thu nhỏ màn hình về kích thước Mobile (< 768px). | | Bố cục dạng cột dọc hiển thị hợp lý, ảnh thành viên thu nhỏ đúng tỷ lệ, không bị lỗi tràn viền (overflow). | | | |

## Ghi chú

-
