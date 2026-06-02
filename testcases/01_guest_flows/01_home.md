# Màn hình Trang chủ (Home Page)

## Phạm vi

- Route: `/` hoặc `/[locale]`
- API liên quan: Lấy danh sách tour nổi bật, danh sách danh mục tour, danh mục địa điểm.
- Vai trò: Khách vãng lai (Guest) / Người dùng đã đăng nhập (User).

## Điều kiện trước

- Tài khoản: Không bắt buộc đăng nhập.
- Dữ liệu mẫu: Có danh sách địa điểm nổi bật, danh mục tour, danh sách tour nổi bật/tuần trong database.
- Môi trường: Local dev server (`http://localhost:3000`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_HOME_001 | Header Navigation | Kiểm tra điều hướng các liên kết trên Header | Trang chủ hiển thị bình thường | Click lần lượt vào các mục: Tours (Tour), Places (Địa điểm), Blog, Contact (Liên hệ). | | Điều hướng chính xác đến các trang tương ứng (`/tours`, `/locations`, `/blog`, `/contact`) mà không bị lỗi. | | | |
| 2 | TC_HOME_002 | Language Toggle | Kiểm tra chuyển đổi ngôn ngữ (Vietnamese / English) | Trang chủ hiển thị bình thường | 1. Click vào nút chọn ngôn ngữ trên Header.<br>2. Chọn English hoặc Tiếng Việt. | | Toàn bộ giao diện (Header, Banner, các đề mục, Footer) thay đổi ngôn ngữ tương ứng. URL thay đổi từ `/vi/...` sang `/en/...` hoặc ngược lại. | | | |
| 3 | TC_HOME_003 | Search Bar | Kiểm tra tìm kiếm nhanh trên Banner chính | Có dữ liệu Tour tương ứng với từ khóa tìm kiếm | 1. Nhập từ khóa tìm kiếm (Ví dụ: "Bà Nà").<br>2. Chọn ngày đi (tùy chọn).<br>3. Click nút Tìm kiếm. | Từ khóa: "Bà Nà" | Chuyển hướng sang trang danh sách tour với từ khóa tìm kiếm trong URL và hiển thị danh sách các tour khớp với từ khóa. | | | |
| 4 | TC_HOME_004 | Categories Carousel | Kiểm tra danh mục địa điểm/tour khám phá | Có danh mục địa điểm trong database | 1. Di chuyển chuột qua lại trên danh mục.<br>2. Click chọn 1 danh mục bất kỳ. | Danh mục: "Biển" | Giao diện hiển thị hiệu ứng hover mượt mà. Khi click sẽ chuyển hướng tới trang danh sách tour đã lọc sẵn theo danh mục được chọn. | | | |
| 5 | TC_HOME_005 | Slider Điều hướng | Kiểm tra nút chuyển qua lại (Next/Prev) của Tour Nổi bật, Tour Hot trong tuần | Danh sách tour nhiều hơn số lượng hiển thị trên 1 màn hình | Click lần lượt nút Next (Mũi tên phải) và Prev (Mũi tên trái) tại mục "Tour Nổi Bật". | | Danh sách tour trượt sang phải/trái mượt mà. Khi hover vào nút có hiệu ứng đổi màu hồng (primary) và icon đổi thành màu trắng, nút bị disabled nếu ở đầu/cuối danh sách. | | | |
| 6 | TC_HOME_006 | Tour Card Click | Kiểm tra click vào card tour | Có danh sách tour hiển thị | Click vào hình ảnh hoặc tiêu đề của một tour card bất kỳ. | | Chuyển hướng thành công đến trang chi tiết của tour đó (`/tours/[slug]`). | | | |
| 7 | TC_HOME_007 | Responsive Layout (Mobile/Tablet) | Kiểm tra độ co giãn giao diện trên các thiết bị khác nhau | | Thu nhỏ trình duyệt về kích thước màn hình Mobile (< 768px) hoặc Tablet. | | Giao diện tự động thích ứng:<br>- Menu điều hướng chuyển thành icon Hamburger hoặc thu gọn chỉ hiển thị icon.<br>- Tên thương hiệu và slogan ẩn đi (dưới breakpoint `2xl`).<br>- Khoảng cách đệm (padding) co giãn hợp lý (cách lề 24px/32px/40px tùy kích thước). | | | |
| 8 | TC_HOME_008 | Footer Links | Kiểm tra các liên kết ở chân trang | Footer hiển thị bình thường | Click vào các liên kết chính sách, mạng xã hội (Facebook, Instagram), thông tin liên hệ ở Footer. | | Điều hướng chính xác tới các trang tương ứng hoặc các tài khoản mạng xã hội chính thức ở tab mới. | | | |

## Ghi chú

- Đảm bảo font chữ (Inter/Outfit) hiển thị sắc nét trên cả Chrome, Safari, Firefox.
