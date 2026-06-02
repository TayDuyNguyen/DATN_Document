# Màn hình Gợi ý Tour & Địa điểm lân cận (Nearby Recommendations Page)

## Phạm vi

- Route: `/nearby` hoặc `/[locale]/nearby`
- API liên quan: Lấy danh sách tour/địa điểm theo tọa độ GPS bán kính gần nhất.
- Vai trò: Khách vãng lai (Guest) / Người dùng đã đăng nhập (User).

## Điều kiện trước

- Trình duyệt hỗ trợ định vị (Geolocation API).
- Môi trường: Local dev server (`http://localhost:3000`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_NEARBY_001 | Cho phép định vị (Allow GPS) | Cấp quyền định vị khi trang yêu cầu | Chưa cấp quyền định vị trước đó | 1. Mở trang `/nearby`.<br>2. Trình duyệt hiển thị pop-up yêu cầu quyền truy cập vị trí.<br>3. Bấm "Cho phép" (Allow). | | - Bản đồ tải vị trí hiện tại của người dùng.<br>- Renders danh sách tour/địa điểm được sắp xếp thứ tự theo khoảng cách từ gần nhất đến xa nhất. | | | |
| 2 | TC_NEARBY_002 | Từ chối định vị (Block GPS) | Từ chối cấp quyền định vị vị trí | Chưa cấp quyền định vị trước đó | 1. Mở trang `/nearby`.<br>2. Tại pop-up yêu cầu quyền vị trí của trình duyệt, chọn "Chặn/Từ chối" (Block/Deny). | | - Hệ thống hiển thị hộp thoại hoặc thông báo yêu cầu người dùng tự chọn một Điểm xuất phát / Vị trí trung tâm thủ công từ bản đồ hoặc ô tìm kiếm.<br>- Hiển thị dữ liệu mặc định (Ví dụ: Trung tâm Thành phố Đà Nẵng). | | | |
| 3 | TC_NEARBY_003 | Thay đổi bán kính lọc | Thay đổi bán kính tìm kiếm địa điểm xung quanh | Đã định vị thành công | Chọn thay đổi bán kính lọc trên thanh công cụ (Ví dụ: 2km, 5km, 10km). | Bán kính: `5km` | Danh sách tour/địa điểm lọc lại tức thì, chỉ hiển thị các kết quả nằm trong phạm vi bán kính 5km từ vị trí đang đứng. | | | |
| 4 | TC_NEARBY_004 | Click xem từ bản đồ | Click vào marker địa điểm trên Bản đồ | | Click chọn một ghim vị trí (Marker) bất kỳ trên bản đồ nhúng. | | Hiển thị thẻ tóm tắt (Tooltip/Infowindow) chứa ảnh đại diện, tên tour, khoảng cách thực tế (ví dụ: `Cách bạn 1.2 km`). Click tiếp sẽ điều hướng sang trang chi tiết của tour đó. | | | |

## Ghi chú

-
