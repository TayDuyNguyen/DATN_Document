# Màn hình User — Landing tour theo điểm đến

> Route đề xuất: `/du-lich-da-nang` hoặc `/destinations/da-nang/tours`  
> Quyền: Public  
> Tham khảo: travel.com.vn có landing riêng cho `du-lich-da-nang.aspx`

---

## Mục tiêu

Tạo trang bán tour theo điểm đến Đà Nẵng, vừa phục vụ SEO vừa giúp khách lọc và chọn tour nhanh.

---

## Thành phần giao diện

| Khu vực | Thành phần | Chức năng |
|---|---|---|
| Hero | Tên điểm đến, ảnh, mô tả ngắn | Giới thiệu Đà Nẵng |
| Search box | Từ khóa, điểm khởi hành, ngày đi | Tìm nhanh tour |
| Filter bar | Dòng tour, giá, thời lượng, phương tiện, khách sạn | Lọc danh sách tour |
| Sort | Đề xuất, giá thấp nhất, ngày gần nhất, bán chạy | Sắp xếp kết quả |
| Tour list | Card tour | Ảnh, mã tour, tuyến điểm, giá, số chỗ, ưu đãi |
| SEO content | Mô tả điểm đến, FAQ | Tăng chất lượng landing |
| Support CTA | Hotline, liên hệ tư vấn | Chuyển đổi khách hàng |

---

## API sử dụng

| API | Trạng thái | Mục đích |
|---|---|---|
| `GET /tours` | Đã có | Danh sách tour |
| `GET /tours/featured` | Đã có | Tour nổi bật |
| `GET /tour-categories` | Đã có | Dòng/danh mục tour |
| `GET /search` | Đã có | Tìm kiếm tour |
| `GET /landing-pages/{slug}` | Planned | Nội dung SEO landing |
| `GET /tours/filters` | Planned | Metadata bộ lọc |

---

## Bộ lọc cần có

| Filter | Nguồn dữ liệu |
|---|---|
| Điểm khởi hành | `departure_from` planned |
| Điểm đến | `departure_to` planned |
| Dòng tour | `tour_line` hoặc `tour_categories` |
| Khoảng giá | `price_adult` |
| Ngày khởi hành | `tour_schedules.start_date` |
| Thời lượng | `duration` |
| Phương tiện | `transport_type` planned |
| Khách sạn | `hotel_rating` planned |

---

## Ghi chú triển khai

- Phase đầu có thể dùng `GET /tours?tour_category_id=&price_min=&price_max=&available_from=&available_to=`.
- Các filter chưa có DB/API thì chỉ hiển thị sau khi được bổ sung vào API và schema chính `docs/database/database.dbml`.

---

## Validation & States

| Hạng mục | Quy tắc |
|---|---|
| Landing slug | `slug` phải là slug hợp lệ; nếu `GET /landing-pages/{slug}` chưa có hoặc chưa publish thì dùng nội dung fallback hardcode |
| Khoảng giá | `price_min <= price_max`; giá âm tự reset về rỗng |
| Ngày khởi hành | `available_from <= available_to`; không mặc định chọn ngày quá khứ |
| Danh mục tour | `tour_category_id` phải tồn tại trong `GET /tour-categories` |
| Filter planned | `departure_from`, `departure_to`, `transport_type`, `hotel_rating` chỉ hiển thị khi API filter metadata đã sẵn sàng |
| Empty tour list | Hiển thị gợi ý nới bộ lọc và CTA xem tất cả tour |
| SEO fallback | Nếu landing API lỗi, vẫn render meta/title mặc định cho Đà Nẵng |
