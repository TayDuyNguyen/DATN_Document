# Màn hình Tour theo Danh mục (Tours by Category Page)

## Phạm vi

- Route: `/tour-categories/[slug]/tours` hoặc `/[locale]/tour-categories/[slug]/tours`
- API liên quan: Danh sách tour được phân loại theo danh mục cụ thể (Ví dụ: "Tour hàng ngày", "Tour dài ngày").
- Vai trò: Khách vãng lai (Guest) / Người dùng đã đăng nhập (User).

## Điều kiện trước

- Dữ liệu mẫu: Có danh mục tour và các tour thuộc danh mục tương ứng hoạt động trong hệ thống.
- Môi trường: Local dev server (`http://localhost:3000`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_TOURCAT_001 | Tiêu đề trang | Hiển thị đúng tiêu đề danh mục tour đang chọn | | Truy cập trang danh mục tour (Ví dụ: `/tour-categories/tour-hang-ngay/tours`). | | Tiêu đề trang hiển thị đúng tên danh mục (Ví dụ: "Danh mục Tour: Tour Hằng Ngày"). | | | |
| 2 | TC_TOURCAT_002 | Lưới danh sách tour | Hiển thị chính xác các tour thuộc danh mục | Có tour trong danh mục | Quan sát lưới danh sách các tour hiển thị trên lưới. | | Chỉ hiển thị các card tour thuộc danh mục đã chọn. Các card tour hiển thị đầy đủ thông tin: Ảnh, Tên tour, Giá tiền, Đánh giá, Thời lượng. | | | |
| 3 | TC_TOURCAT_003 | Click Xem chi tiết | Click điều hướng xem chi tiết tour | | Click vào một card tour bất kỳ trong lưới. | | Chuyển hướng thành công tới trang chi tiết tour tương ứng (`/tours/[slug]`). | | | |

## Ghi chú

-
