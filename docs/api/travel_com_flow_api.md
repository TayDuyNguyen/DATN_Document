# API flow theo benchmark travel.com.vn

> Ngày cập nhật: 13/05/2026  
> Nguồn tham khảo: `https://travel.com.vn/du-lich-da-nang.aspx` và bundle public của travel.com.vn.  
> Mục tiêu: định nghĩa API cần có để DanangTrip đi theo flow bán tour tương tự, phân biệt API hiện có và API planned.

---

## 1. Mapping flow với API hiện tại

| Flow | API hiện có | Trạng thái |
|---|---|---|
| Landing/list tour Đà Nẵng | `GET /tours`, `GET /tours/featured`, `GET /tour-categories` | Đã có |
| Search/filter tour | `GET /search`, `GET /tours` | Đã có nền tảng, thiếu filter nâng cao |
| Chi tiết tour | `GET /tours/{slug}` | Đã có |
| Lịch khởi hành | `GET /tours/{id}/schedules` | Đã có |
| Kiểm tra chỗ | `POST /tours/{id}/check-availability` | Đã có |
| Tính giá | `POST /bookings/calculate` | Đã có |
| Tạo booking | `POST /bookings` | Đã có |
| Thanh toán | `POST /payments/create`, `GET /payments/status/{transaction_code}`, `POST /payments/retry/{booking_code}` | Đã có |
| Callback payment | `POST /payments/callback` | Đã có |
| Lịch sử booking | `GET /user/bookings`, `GET /user/bookings/{id}` | Đã có |
| Tra cứu theo mã | `GET /user/bookings/code/{booking_code}` | Đã có |
| Hóa đơn | `GET /user/bookings/{id}/invoice` | Đã có |
| Admin quản lý booking | `GET /admin/bookings`, `PATCH /admin/bookings/{id}/status` | Đã có |
| Admin quản lý payment | `GET /admin/payments`, `POST /admin/payments/{id}/refund` | Đã có |

---

## 2. API nên bổ sung Phase 1

### 2.1 Landing page

| Method | Endpoint | Quyền | Mục đích |
|---|---|---|---|
| GET | `/landing-pages/{slug}` | Public | Lấy nội dung SEO/hero/FAQ/filter mặc định cho landing điểm đến |
| GET | `/admin/landing-pages` | Admin | Quản lý landing pages |
| POST | `/admin/landing-pages` | Admin | Tạo landing page |
| PUT | `/admin/landing-pages/{id}` | Admin | Sửa landing page |
| PATCH | `/admin/landing-pages/{id}/status` | Admin | Publish/unpublish |

### 2.2 Tour filters metadata

| Method | Endpoint | Quyền | Mục đích |
|---|---|---|---|
| GET | `/tours/filters` | Public | Trả về điểm khởi hành, điểm đến, dòng tour, khoảng giá, duration, transport |

Response gợi ý:

```json
{
  "departure_from": ["Đà Nẵng", "Hồ Chí Minh", "Hà Nội", "Cần Thơ"],
  "departure_to": ["Đà Nẵng", "Hội An", "Huế", "Phong Nha"],
  "tour_lines": ["standard", "saving", "premium", "best_price"],
  "transport_types": ["flight", "car", "train", "mixed"],
  "hotel_ratings": [3, 4, 5],
  "price_range": { "min": 0, "max": 10000000 }
}
```

### 2.3 Passenger manifest

| Method | Endpoint | Quyền | Mục đích |
|---|---|---|---|
| GET | `/user/bookings/{id}/passengers` | User | Xem danh sách hành khách |
| PUT | `/user/bookings/{id}/passengers` | User | Cập nhật hành khách trước khi booking confirmed |
| GET | `/admin/bookings/{id}/passengers` | Admin | Admin xem danh sách hành khách |

Có thể gộp passengers vào `POST /bookings` trong phase đầu:

```json
{
  "tour_id": 1,
  "tour_schedule_id": 10,
  "quantity_adult": 2,
  "quantity_child": 1,
  "payment_method": "vnpay",
  "customer_name": "Nguyen Van A",
  "customer_email": "a@example.com",
  "customer_phone": "0900000000",
  "passengers": [
    { "passenger_type": "adult", "full_name": "Nguyen Van A", "birthdate": "1990-01-01" },
    { "passenger_type": "adult", "full_name": "Tran Thi B", "birthdate": "1992-01-01" },
    { "passenger_type": "child", "full_name": "Nguyen Van C", "birthdate": "2018-01-01" }
  ]
}
```

### 2.4 Promotions/coupons

| Method | Endpoint | Quyền | Mục đích |
|---|---|---|---|
| GET | `/promotions` | Public | Danh sách ưu đãi đang active |
| POST | `/promotions/validate` | User | Kiểm tra mã giảm giá cho booking/cart |
| GET | `/admin/promotions` | Admin | Danh sách promotion |
| POST | `/admin/promotions` | Admin | Tạo promotion |
| PUT | `/admin/promotions/{id}` | Admin | Cập nhật |
| PATCH | `/admin/promotions/{id}/status` | Admin | Bật/tắt |
| DELETE | `/admin/promotions/{id}` | Admin | Xóa |

### 2.5 Site settings

| Method | Endpoint | Quyền | Mục đích |
|---|---|---|---|
| GET | `/config` | Public | Hotline, email, địa chỉ, social, logo, payment methods |
| GET | `/admin/settings` | Admin | Xem cấu hình |
| PUT | `/admin/settings` | Admin | Cập nhật cấu hình |

---

## 3. API nên bổ sung Phase 2

### 3.1 Cart

| Method | Endpoint | Quyền | Mục đích |
|---|---|---|---|
| GET | `/cart` | Public/User | Lấy giỏ hàng theo user/session |
| POST | `/cart/items` | Public/User | Thêm tour schedule vào giỏ |
| PUT | `/cart/items/{id}` | Public/User | Cập nhật số khách |
| DELETE | `/cart/items/{id}` | Public/User | Xóa item |
| POST | `/cart/checkout` | User | Chuyển cart thành booking |

### 3.2 Booking timeline

| Method | Endpoint | Quyền | Mục đích |
|---|---|---|---|
| GET | `/user/bookings/{id}/timeline` | User | Timeline đơn của mình |
| GET | `/admin/bookings/{id}/timeline` | Admin | Timeline đầy đủ cho admin |

### 3.3 Admin action routes

Hiện tại dùng `PATCH /admin/bookings/{id}/status`. Nếu muốn API rõ theo action:

| Method | Endpoint | Quyền | Mục đích |
|---|---|---|---|
| POST | `/admin/bookings/{id}/confirm` | Admin | Xác nhận đơn |
| POST | `/admin/bookings/{id}/cancel` | Admin | Hủy đơn |
| POST | `/admin/bookings/{id}/complete` | Admin | Hoàn thành đơn |

### 3.4 Combo service planned

| Method | Endpoint | Quyền | Mục đích |
|---|---|---|---|
| GET | `/flights/search` | Public | Planned quote vé máy bay |
| GET | `/hotels/search` | Public | Planned khách sạn |
| GET | `/flight-hotels/search` | Public | Planned combo flight-hotel |
| GET | `/visa/products` | Public | Planned dịch vụ visa |

---

## 4. Thay đổi cần cập nhật trong API hiện có

### 4.1 `GET /tours`

Nên hỗ trợ thêm query:

| Query | Mục đích |
|---|---|
| `departure_from` | Lọc điểm khởi hành |
| `departure_to` | Lọc điểm đến |
| `tour_line` | Lọc dòng tour |
| `tour_type` | domestic/international/combo |
| `transport_type` | flight/car/train/mixed |
| `hotel_rating` | 3/4/5 sao |
| `promotion` | Tour đang có ưu đãi |

### 4.2 `GET /tours/{slug}`

Nên trả thêm:

| Field | Mục đích |
|---|---|
| `tour_code` | Mã tour |
| `tour_line` | Dòng tour |
| `transport_type`, `airline` | Phương tiện/hãng |
| `hotel_rating` | Tiêu chuẩn khách sạn |
| `policy` | Điều kiện booking/hủy |
| `promotions` | Ưu đãi áp dụng |
| `related_tours` | Tour liên quan |

### 4.3 `GET /tours/{id}/schedules`

Nên trả thêm:

| Field | Mục đích |
|---|---|
| `departure_code` | Mã lịch |
| `departure_place` | Nơi khởi hành |
| `remaining_people` | Chỗ còn nhận |
| `booking_deadline` | Hạn nhận khách |
| `status_reason` | Lý do full/cancelled |

### 4.4 `POST /bookings`

Nên hỗ trợ thêm:

| Field | Mục đích |
|---|---|
| `passengers[]` | Danh sách hành khách |
| `promotion_code` | Mã giảm giá |
| `accepted_terms` | Đồng ý điều khoản |

---

## 5. Thứ tự API nên làm

1. Mở rộng `GET /tours`, `GET /tours/{slug}`, `GET /tours/{id}/schedules`.
2. Thêm passenger manifest trong booking.
3. Thêm promotions/coupons.
4. Thêm `/config` và admin settings.
5. Thêm landing pages.
6. Sau cùng mới thêm cart và combo flight/hotel/visa.
