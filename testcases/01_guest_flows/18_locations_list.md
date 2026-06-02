# Màn hình Danh sách Địa điểm du lịch (Destinations Catalog Page)

## Phạm vi

- Route: `/locations` hoặc `/[locale]/locations`
- API liên quan: Lấy danh sách toàn bộ các địa danh/địa điểm du lịch du lịch nổi bật.
- Vai trò: Khách vãng lai (Guest) / Người dùng đã đăng nhập (User).

## Điều kiện trước

- Dữ liệu mẫu: Có danh sách địa điểm trong database.
- Môi trường: Local dev server (`http://localhost:3000`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_LOCLIST_001 | Danh sách địa danh | Xem danh sách toàn bộ địa điểm du lịch | | Truy cập trang `/locations`. | | Hiển thị danh sách các địa danh nổi tiếng dưới dạng Grid. Mỗi card địa điểm có hình ảnh, tên địa danh, số lượng tour đang khai thác tại đây. | | | |
| 2 | TC_LOCLIST_002 | Tìm kiếm địa danh | Tìm nhanh địa điểm theo từ khóa | | 1. Nhập từ khóa tìm kiếm địa danh.<br>2. Nhấn nút Tìm kiếm hoặc Enter. | Từ khóa: "Ngũ Hành Sơn" | Danh sách lọc nhanh chỉ hiển thị card địa danh Ngũ Hành Sơn. | | | |
| 3 | TC_LOCLIST_003 | Click Địa danh | Xem thông tin chi tiết địa danh | | Click chọn một card địa điểm trong danh sách. | | Chuyển hướng thành công tới trang chi tiết địa điểm đó (`/locations/[slug]`). | | | |

## Ghi chú

-
