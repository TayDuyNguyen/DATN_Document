# Màn hình Danh sách & Tìm kiếm Tour (Tour Catalog & Search Page)

## Phạm vi

- Route: `/tours` hoặc `/[locale]/tours`
- API liên quan: Lấy danh sách tour, tìm kiếm tour có phân trang và bộ lọc.
- Vai trò: Khách vãng lai (Guest) / Người dùng đã đăng nhập (User).

## Điều kiện trước

- Dữ liệu mẫu: Có danh sách tour thuộc nhiều danh mục, mức giá, địa điểm khác nhau trong database.
- Môi trường: Local dev server (`http://localhost:3000`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_TOURLIST_001 | Tìm kiếm theo từ khóa | Tìm kiếm tour bằng ô nhập từ khóa | Có tour chứa từ khóa | 1. Nhập từ khóa tìm kiếm vào ô tìm kiếm.<br>2. Nhấn Enter hoặc click icon Tìm kiếm. | Từ khóa: "Cù Lao Chàm" | Danh sách cập nhật và chỉ hiển thị các tour có tiêu đề hoặc mô tả chứa từ khóa "Cù Lao Chàm". URL cập nhật tham số query. | | | |
| 2 | TC_TOURLIST_002 | Lọc theo danh mục | Lọc danh sách tour theo danh mục | Có tour thuộc danh mục tương ứng | Tích chọn 1 hoặc nhiều danh mục ở sidebar bên trái (Ví dụ: "Tour trong ngày", "Tour nghỉ dưỡng"). | Danh mục: "Tour trong ngày" | Danh sách tour tự động tải lại và chỉ hiển thị các tour thuộc danh mục đã chọn. | | | |
| 3 | TC_TOURLIST_003 | Lọc theo địa điểm | Lọc danh sách tour theo địa điểm đến | Có tour thuộc địa điểm tương ứng | Tích chọn địa điểm đến ở phần bộ lọc (Ví dụ: "Hội An", "Bà Nà Hills"). | Địa điểm: "Hội An" | Danh sách hiển thị chính xác các tour đi qua hoặc xuất phát tại địa điểm đã chọn. | | | |
| 4 | TC_TOURLIST_004 | Lọc theo giá (Price Range) | Lọc danh sách tour theo khoảng giá | Có tour có mức giá trong khoảng lọc | Kéo slider chọn khoảng giá hoặc nhập mức giá tối thiểu - tối đa (Ví dụ: 500,000đ - 2,000,000đ). | Giá: 500,000đ - 2,000,000đ | Chỉ hiển thị các tour có giá người lớn (`price_adult`) nằm trong khoảng từ 500,000đ đến 2,000,000đ. | | | |
| 5 | TC_TOURLIST_005 | Lọc theo thời gian | Lọc danh sách tour theo số ngày đi | | Chọn thời lượng tour ở sidebar (Ví dụ: "1 ngày", "2 ngày 1 đêm", "3 ngày 2 đêm"). | Thời lượng: "1 ngày" | Giao diện hiển thị các tour có thời lượng đúng như đã chọn. | | | |
| 6 | TC_TOURLIST_006 | Sắp xếp (Sorting) | Sắp xếp danh sách tour theo các tiêu chí | Có danh sách tour hiển thị | Click vào dropdown Sắp xếp và chọn lần lượt:<br>- Giá: Thấp đến Cao<br>- Giá: Cao đến Thấp<br>- Đánh giá tốt nhất<br>- Mới nhất. | | Danh sách tour được sắp xếp lại tương ứng với tiêu chí đã chọn, giá cả hoặc thứ tự ngày tạo/đánh giá hiển thị đúng quy luật. | | | |
| 7 | TC_TOURLIST_007 | Xóa bộ lọc (Clear Filters) | Reset toàn bộ bộ lọc về mặc định | Đang bật các bộ lọc | Click nút "Xóa tất cả bộ lọc" ở đầu sidebar hoặc bộ lọc. | | Toàn bộ các lựa chọn (chọn địa điểm, danh mục, giá, thời lượng) được bỏ chọn. Danh sách hiển thị toàn bộ tour ban đầu. | | | |
| 8 | TC_TOURLIST_008 | Phân trang (Pagination) | Chuyển trang danh sách tour | Danh sách tour nhiều hơn số lượng hiển thị trên 1 trang | Click chọn trang 2 hoặc nút Tiếp theo (Next). | | Danh sách tour trang tiếp theo được tải lên. Trang cuộn mượt mà lên đầu trang, URL cập nhật tham số `page=2`. | | | |

## Ghi chú

- Đảm bảo khi không tìm thấy tour nào khớp với bộ lọc, hệ thống hiển thị thông điệp thông báo "Không tìm thấy kết quả phù hợp" kèm nút reset bộ lọc.
