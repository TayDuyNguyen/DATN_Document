# Flow màn hình theo benchmark travel.com.vn

> Ngày cập nhật: 13/05/2026  
> Nguồn tham khảo: `https://travel.com.vn/du-lich-da-nang.aspx` và bundle public của travel.com.vn.  
> Mục tiêu: định nghĩa flow màn hình DanangTrip nên đi theo để bán tour Đà Nẵng chuyên nghiệp hơn.

---

## 1. Nghiệp vụ quan sát được

| Nghiệp vụ | Chi tiết |
|---|---|
| Landing tour theo điểm đến | Trang SEO riêng cho Đà Nẵng, mô tả điểm đến, danh sách tour liên quan |
| Menu sản phẩm | Du lịch trong nước, nước ngoài, dòng tour, MICE, loyalty, liên hệ |
| Dòng tour | Cao cấp, tiết kiệm, tiêu chuẩn, giá tốt |
| Tour card | Ảnh, tên tour, tuyến điểm, khách sạn/sao, hãng bay, giá, ưu đãi, nút đặt |
| Bộ lọc tour | Điểm khởi hành, điểm đến, dòng tour, loại tour, khoảng giá, ngày khởi hành |
| Lịch khởi hành | Ngày đi, số chỗ, giá người lớn/trẻ em/em bé |
| Giỏ hàng | Có icon cart và route/bundle liên quan cart |
| Booking flow | booking-check, order-booking, booking-success, booking-fail |
| Payment flow | payment-process, payment-success |
| Dịch vụ mở rộng | flight, hotel, flight-hotel, visa, promotion |

---

## 2. Flow user đề xuất cho DanangTrip

### 2.1 Landing tour theo điểm đến

File nên có: `user_destination_tour_landing.md`  
Route đề xuất: `/du-lich-da-nang` hoặc `/destinations/da-nang/tours`

Chức năng:

| Chức năng | Mô tả |
|---|---|
| Hero SEO | Tên điểm đến, mô tả ngắn, ảnh đại diện |
| Search nhanh | Từ khóa, điểm khởi hành, ngày khởi hành |
| Bộ lọc | Dòng tour, khoảng giá, thời lượng, phương tiện, khách sạn |
| Danh sách tour | Tour card có giá, lịch, số chỗ, ưu đãi |
| Sort | Đề xuất, giá thấp nhất, ngày gần nhất, bán chạy |
| Nội dung SEO | Giới thiệu Đà Nẵng, điểm nổi bật, FAQ |
| CTA hỗ trợ | Hotline, chat/liên hệ tư vấn |

API hiện có có thể dùng:

| API | Mục đích |
|---|---|
| `GET /tours` | Danh sách tour |
| `GET /tour-categories` | Danh mục/dòng tour hiện tại |
| `GET /tours/featured` | Tour nổi bật |
| `GET /search` | Tìm tour |

API nên bổ sung sau:

| API | Mục đích |
|---|---|
| `GET /landing-pages/{slug}` | Nội dung SEO landing |
| `GET /tours/filters` | Metadata filter: điểm khởi hành, dòng tour, khoảng giá |

### 2.2 Danh sách tour nâng cao

File hiện có: `user_tours_list.md`  
Route hiện có: `/tours`

Cần cập nhật thêm:

| Chức năng | Mô tả |
|---|---|
| Filter điểm khởi hành | `departure_from` |
| Filter điểm đến | `departure_to` hoặc category/destination |
| Filter dòng tour | standard/saving/premium/best_price |
| Filter phương tiện | flight/car/train/mixed |
| Filter khách sạn | 3/4/5 sao |
| Filter ngày đi | `available_from`, `available_to` |
| Badge ưu đãi | Tour có promotion/gift |
| Hiển thị số chỗ | Dựa vào lịch khởi hành gần nhất |

### 2.3 Chi tiết tour nâng cao

File hiện có: `user_tour_detail.md`  
Route hiện có: `/tours/{slug}`

Cần cập nhật thêm tab/section:

| Section | Chức năng |
|---|---|
| Tổng quan | Tên tour, mã tour, tuyến điểm, dòng tour, phương tiện, khách sạn |
| Lịch khởi hành | Danh sách ngày đi, ngày về, giá, số chỗ còn nhận |
| Giá tour | Người lớn, trẻ em, em bé, phụ thu nếu có |
| Lịch trình | Theo ngày, điểm tham quan, bữa ăn, khách sạn |
| Dịch vụ bao gồm | Vé tham quan, xe, hướng dẫn viên, ăn uống, khách sạn |
| Không bao gồm | Chi phí cá nhân, thuế/phụ phí nếu có |
| Điều kiện đặt/hủy | Deadline, chính sách hoàn/hủy |
| Ưu đãi | Coupon, quà tặng, show/event đi kèm |
| Tour liên quan | Cùng điểm đến/dòng tour |

### 2.4 Chọn lịch và kiểm tra chỗ

File nên có: `user_tour_departure_select.md`  
Route đề xuất: modal trong `/tours/{slug}` hoặc `/tours/{slug}/departures`

Chức năng:

| Chức năng | Mô tả |
|---|---|
| Chọn ngày khởi hành | Dựa vào `tour_schedules` |
| Hiển thị chỗ còn nhận | `max_people - booked_people - locked_people` |
| Chọn số khách | Người lớn, trẻ em, em bé |
| Tính giá tạm | Gọi calculate/check availability |
| Giữ chỗ tạm | Planned nếu có cart/checkout timeout |

API hiện có:

| API | Mục đích |
|---|---|
| `GET /tours/{id}/schedules` | Lấy lịch khởi hành |
| `POST /tours/{id}/check-availability` | Kiểm tra còn chỗ |
| `POST /bookings/calculate` | Tính tiền |

### 2.5 Giỏ hàng

File nên có: `user_cart.md`  
Route đề xuất: `/cart`  
Trạng thái: planned nếu muốn giống travel.com.vn.

Chức năng:

| Chức năng | Mô tả |
|---|---|
| Danh sách tour đã chọn | Tour, lịch khởi hành, số khách, giá |
| Cập nhật số khách | Recalculate giá |
| Xóa item | Remove khỏi cart |
| Áp mã giảm giá | Planned promotions |
| Checkout | Chuyển sang nhập thông tin khách |

Nếu chưa làm giỏ hàng, có thể checkout trực tiếp từ chi tiết tour như hiện tại.

### 2.6 Checkout đặt tour

File hiện có: `user_tour_booking.md`  
Route hiện có: `/tours/{slug}/book`

Cần cập nhật thêm:

| Bước | Chức năng |
|---|---|
| 1. Kiểm tra đơn | Tour, lịch, số khách, giá |
| 2. Thông tin người liên hệ | Họ tên, email, phone, địa chỉ, ghi chú |
| 3. Danh sách hành khách | Họ tên, loại khách, ngày sinh, giấy tờ nếu cần |
| 4. Mã giảm giá | Nhập coupon/promotion nếu có |
| 5. Điều khoản | Checkbox đồng ý điều kiện tour/chính sách dữ liệu |
| 6. Tạo booking | Gọi API booking |

### 2.7 Thanh toán

File hiện có: `user_payment.md`, `user_payment_result.md`  
Route hiện có: `/payment`, `/payment/result`

Cần cập nhật thêm:

| Chức năng | Mô tả |
|---|---|
| Chọn phương thức | VNPay/MoMo/ZaloPay/chuyển khoản nếu hỗ trợ |
| Hiển thị countdown | Thời hạn thanh toán booking |
| Trạng thái xử lý | payment-process |
| Thành công | booking-success/payment-success |
| Thất bại | booking-fail/payment-fail, retry |
| Tra cứu giao dịch | Theo `transaction_code` |

### 2.8 Tra cứu booking

File hiện có: `user_booking_by_code.md`  
Route hiện có: `/bookings/code/{booking_code}`

Cần cập nhật thêm:

| Chức năng | Mô tả |
|---|---|
| Nhập mã booking | Cho user tìm lại đơn |
| Xác thực quyền | Nếu user đăng nhập, chỉ xem booking của mình |
| Gửi lại thanh toán | Với đơn chưa thanh toán |
| Tải hóa đơn | Nếu booking hợp lệ |

---

## 3. Flow admin đề xuất

### 3.1 Quản lý tour nâng cao

File cần cập nhật: `admin_tours_create.md`, `admin_tours_edit.md`, `admin_tours_detail.md`

Thêm field/chức năng:

| Nhóm | Field/chức năng |
|---|---|
| Định danh | `tour_code`, slug |
| Phân loại | tour category, tour line, tour type |
| Tuyến tour | departure_from, departure_to, danh sách địa điểm |
| Dịch vụ | transport_type, airline, hotel_rating, service_standard |
| Giá | adult/child/infant, discount, promotion |
| SEO | seo title, description, landing content |
| Chính sách | included, excluded, cancellation policy, note |

### 3.2 Quản lý lịch khởi hành nâng cao

File cần cập nhật: `admin_tour_schedules_list.md`, `admin_tour_schedules_create.md`, `admin_tour_schedules_edit.md`

Thêm field/chức năng:

| Chức năng | Mô tả |
|---|---|
| Mã lịch | departure_code |
| Nơi khởi hành | departure_place |
| Hạn nhận khách | booking_deadline |
| Chỗ còn nhận | max - booked - locked |
| Giá riêng theo lịch | adult/child/infant override |
| Trạng thái | available/full/cancelled |
| Lý do trạng thái | status_reason |

### 3.3 Quản lý khuyến mãi

File nên có: `admin_promotions.md`  
Route đề xuất: `/admin/promotions`

Chức năng:

| Chức năng | Mô tả |
|---|---|
| Danh sách promotion | Filter theo status/time |
| Tạo/sửa promotion | code, name, discount, gift, thời gian |
| Gán tour/category | Apply theo tour hoặc dòng tour |
| Giới hạn sử dụng | usage_limit, min_order_amount |
| Theo dõi sử dụng | used_count, booking áp dụng |

### 3.4 Quản lý booking nâng cao

File cần cập nhật: `admin_bookings_detail.md`

Thêm section:

| Section | Chức năng |
|---|---|
| Người liên hệ | customer_name/email/phone |
| Danh sách hành khách | adult/child/infant, ngày sinh, giấy tờ |
| Giá & khuyến mãi | subtotal, discount, final_amount |
| Timeline trạng thái | pending/confirmed/cancelled/completed |
| Payment timeline | pending/success/failed/refunded |
| Ghi chú nội bộ | Admin note |

### 3.5 Quản lý cấu hình website

File nên có: `admin_site_settings.md`  
Route đề xuất: `/admin/settings`

Chức năng:

| Chức năng | Mô tả |
|---|---|
| Hotline/email/địa chỉ | Footer/contact |
| Logo/social | Header/footer |
| Payment methods | Bật/tắt VNPay/MoMo/ZaloPay |
| SEO mặc định | title, description |
| Policy links | Chính sách riêng tư, điều khoản sử dụng |

---

## 4. Tổng hợp màn cần thêm/cập nhật

| Ưu tiên | Màn | Trạng thái |
|---|---|---|
| Cao | `user_destination_tour_landing.md` | Thêm mới |
| Cao | `user_tour_departure_select.md` | Thêm mới hoặc modal trong detail |
| Cao | `user_tour_booking.md` | Cập nhật passenger/promotion/terms |
| Cao | `admin_tours_create/edit/detail` | Cập nhật field tour code, dòng tour, dịch vụ |
| Cao | `admin_tour_schedules_*` | Cập nhật mã lịch, hạn nhận khách, chỗ còn nhận |
| Trung bình | `admin_promotions.md` | Thêm mới |
| Trung bình | `admin_site_settings.md` | Thêm mới |
| Trung bình | `user_cart.md` | Planned nếu làm cart |
| Thấp | flight/hotel/visa pages | Planned phase sau |

---

## 5. Flow triển khai khuyến nghị

1. Chuẩn hóa tour listing/detail theo mã tour, lịch khởi hành, số chỗ, dòng tour.
2. Bổ sung checkout có danh sách hành khách.
3. Bổ sung promotion/coupon cơ bản.
4. Bổ sung settings để thay thế hardcode hotline/footer.
5. Sau khi core booking ổn, mới làm cart và combo flight/hotel/visa.
