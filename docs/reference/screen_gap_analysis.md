# Rà soát hiện trạng tài liệu màn hình

> Cập nhật: 14/05/2026  
> Phạm vi: `docs/page` và `screen`  
> Mục tiêu: kiểm tra tài liệu từng màn có khớp danh sách màn tổng, API hiện có, API planned và prototype màn hình hay không.

---

## 1. Kết luận

Tài liệu màn hình hiện đã đủ để làm flow nghiệp vụ cho DanangTrip:

| Khu vực | Trạng thái |
|---|---|
| Admin core screens | Đủ file mô tả cho dashboard, tour, địa điểm, booking, payment, rating, user, blog, notification, contact, report |
| User core screens | Đủ file mô tả cho auth, home, search, location, tour, booking, payment, profile, favorite, rating, notification |
| Planned screens theo travel.com.vn | Đã có file mô tả cho landing tour, chọn lịch khởi hành, cart, admin promotions, admin settings, admin landing pages |
| API planned | Đã đánh dấu rõ bằng `planned` hoặc `Planned`, không ghi như API đã có |
| Endpoint yêu thích | Đã chuẩn hóa về query/body `location_id` hoặc `tour_id`, không dùng path cũ xóa theo id favorite |
| Admin booking actions | Đã chuẩn hóa về `PATCH /admin/bookings/{id}/status`; route action riêng chỉ là planned |
| Prototype trong `screen` | Đã đối chiếu với `docs/page`; còn thiếu một số màn auth/user booking/blog/tour/admin report |
| API orphan | Đã có tài liệu chủ sở hữu cho toàn bộ endpoint trong `docs/api`; endpoint kỹ thuật được gom vào `system_runtime_endpoints.md` |
| DB planned | Đã bổ sung DBML cho landing pages, settings, promotions, cart, passengers và timeline |
| Chuẩn hóa page docs | 89/89 file màn/chức năng đã có API mapping hợp lệ, validation/state và flow rõ ràng |

---

## 2. Danh sách tổng

| File | Vai trò | Trạng thái |
|---|---|---|
| `list_page.md` | Danh sách màn Admin | Chuẩn, tổng 48 màn gồm planned |
| `list_page_user.md` | Danh sách màn User | Chuẩn, tổng 43 màn gồm planned |
| `travel_com_benchmark_flow.md` | Flow tham khảo travel.com.vn | Giữ làm tài liệu nghiệp vụ nền |

---

## 3. Màn planned đã có file

| Màn | File | Trạng thái API |
|---|---|---|
| Landing tour Đà Nẵng | `user_destination_tour_landing.md` | Planned một phần |
| Chọn lịch khởi hành | `user_tour_departure_select.md` | Dùng API hiện có + planned field |
| Giỏ hàng tour | `user_cart.md` | Planned |
| Quản lý khuyến mãi | `admin_promotions.md` | Planned |
| Cấu hình website | `admin_site_settings.md` | Planned |
| Quản lý landing pages | `admin_landing_pages.md` | Planned |

---

## 4. Điểm cần lưu ý khi triển khai code

| Hạng mục | Ghi chú |
|---|---|
| `/config`, `/weather`, `/health` | Đang planned trong API docs; frontend cần fallback. `/health` thuộc `system_runtime_endpoints.md` |
| `/user/search-history` | Planned; màn search có thể hiển thị section khi API sẵn sàng |
| `/user/account` | Planned; màn xóa tài khoản đã đánh dấu planned |
| `/cart/*` | Planned; chưa bắt buộc nếu checkout trực tiếp từ tour |
| Promotions | Planned; DBML đã có `promotions`, `promotion_targets`, `booking_promotions` |
| Landing pages | Planned; DBML đã có `landing_pages`, trước mắt có thể hardcode landing `/du-lich-da-nang` |
| Booking passengers/timeline | Planned; đã gắn vào màn chi tiết booking user/admin và DBML có bảng tương ứng |

---

## 5. Tiêu chuẩn tài liệu màn

Mỗi file màn nên có tối thiểu:

1. Route UI.
2. Quyền truy cập.
3. API sử dụng.
4. Mục tiêu màn.
5. Thành phần giao diện chính.
6. Luồng xử lý hoặc rule nghiệp vụ.
7. Trạng thái planned nếu API/database chưa có.

Các file mới tạo gần đây đã theo format này. Một số file cũ dài hơn và có chi tiết UI style, vẫn dùng được cho triển khai frontend.

Kết quả kiểm tra tự động sau chuẩn hóa:

```text
PAGE_TOTAL=89
PAGE_PASS=89
NEED_FIX=0
ORPHAN_COUNT=0
```

---

## 6. Đối chiếu prototype `screen`

File phân loại prototype đã được cập nhật tại:

- `screen/4_Others/00-Bang_Phan_Loai_Man_Hinh.md`
- `screen/4_Others/01-Screen_To_Docs_Mapping.md`

Kết luận đối chiếu:

| Khu vực | Trạng thái |
|---|---|
| Guest/Public | Đã có home, search, locations, tours, blog list, contact; thiếu auth, blog detail/category, tour category/departure |
| User | Đã có verify email, profile, favorites, booking list/detail, booking/payment, notifications, ratings; thiếu home logged-in riêng, booking by code, invoice, một số rating actions |
| Admin | Đã có dashboard, tour, location, user, booking, payment, rating, blog, notification, contact; thiếu report ratings/locations/users và các màn planned |
| Planned | Cart, promotions, site settings, landing pages vẫn giữ planned, chưa bắt buộc có prototype nếu API/database chưa hoàn chỉnh |

Các nghiệp vụ cũ như "Bài đăng của tôi", "Lịch sử hoạt động", "Nạp Point", "Quản lý Point" đã bị loại khỏi danh sách chuẩn triển khai trong tài liệu `screen`.
