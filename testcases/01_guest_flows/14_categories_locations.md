# Màn hình Địa điểm theo Danh mục (Locations by Category Page)

## Phạm vi

- Route: `/categories/[slug]/locations` hoặc `/[locale]/categories/[slug]/locations`
- API liên quan: Lấy danh sách địa danh thuộc một phân loại danh mục cụ thể (Ví dụ: Danh mục "Bãi biển", "Di tích lịch sử").
- Vai trò: Khách vãng lai (Guest) / Người dùng đã đăng nhập (User).

## Điều kiện trước

- Dữ liệu mẫu: Có danh mục địa điểm và các địa điểm liên kết thuộc danh mục đó.
- Môi trường: Local dev server (`http://localhost:3000`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_CATLOC_001 | Tiêu đề danh mục | Renders đúng tiêu đề danh mục đang chọn | | Truy cập trang danh mục địa danh (Ví dụ: `/categories/bien-da-nang/locations`). | | Tiêu đề trang hiển thị đúng danh mục được chọn (Ví dụ: "Địa điểm: Biển Đà Nẵng"). | | | |
| 2 | TC_CATLOC_002 | Danh sách địa điểm | Renders danh sách địa điểm thuộc danh mục | Có địa danh thuộc danh mục | Xem các card địa điểm hiển thị trên lưới (Grid). | | Chỉ hiển thị các địa danh được gắn nhãn danh mục đã chọn. Mỗi card địa danh hiển thị đầy đủ hình ảnh, tên và mô tả ngắn. | | | |
| 3 | TC_CATLOC_003 | Click Địa danh | Click xem chi tiết địa danh từ danh sách | | Click chọn một địa điểm trong danh sách. | | Chuyển hướng thành công sang trang chi tiết của địa danh đó (`/locations/[slug]`). | | | |

## Ghi chú

-
