# Màn hình: Admin Dashboard

> Route: `/admin/dashboard`
> Quyền: 🛡️ Admin / Staff
> Mô tả: Trang tổng quan quản trị — hiển thị thống kê, biểu đồ và dữ liệu gần đây của toàn hệ thống.

---

## Layout tổng quan

```
┌─────────────────────────────────────────────────────────┐
│  HEADER: Tiêu đề + nút Làm mới + nút Xuất báo cáo      │
├─────────────────────────────────────────────────────────┤
│  HÀNG 1: [Doanh thu] [Đơn hàng] [Người dùng]           │  ← 3 thẻ thống kê chính
├─────────────────────────────────────────────────────────┤
│  HÀNG 2: [Tour đã bán] [Đánh giá chờ] [Liên hệ mới]   │  ← 3 thẻ thống kê phụ
├─────────────────────────────────────────────────────────┤
│  HÀNG 3: [Line chart doanh thu] [Bar chart đặt tour]    │  ← 2 biểu đồ
├─────────────────────────────────────────────────────────┤
│  HÀNG 4: [Area chart người dùng] [Bar chart trạng thái] │  ← 2 biểu đồ
├─────────────────────────────────────────────────────────┤
│  HÀNG 5: [Bảng Top 5 tour bán chạy]                    │  ← full width
│          [Bảng Đơn hàng gần đây]                        │  ← full width
└─────────────────────────────────────────────────────────┘
```

---

## Chi tiết từng vị trí & API tương ứng

---

### HÀNG 1 — Thẻ thống kê chính (3 cột)

> Tất cả 3 thẻ gọi chung **1 request duy nhất**:
> `GET /admin/dashboard/stats`

| Vị trí | Trường dữ liệu | Hiển thị |
|--------|---------------|----------|
| Thẻ 1 — Tổng doanh thu | `total_revenue` | Số tiền VNĐ, badge % tăng trưởng |
| Thẻ 2 — Tổng đơn hàng | `total_bookings` | Số đơn, badge % tăng trưởng |
| Thẻ 3 — Tổng người dùng | `total_users` | Số user, badge % tăng trưởng |

```
API: GET /admin/dashboard/stats
Response dùng: total_revenue, total_bookings, total_users
```

---

### HÀNG 2 — Thẻ thống kê phụ (3 cột)

> Cũng lấy từ cùng request `GET /admin/dashboard/stats`

| Vị trí | Trường dữ liệu | Hiển thị |
|--------|---------------|----------|
| Thẻ 4 — Tour đã bán | `total_tours_sold` | Số lượt tour đã bán |
| Thẻ 5 — Đánh giá chờ duyệt | `pending_ratings` | Số đánh giá status=pending |
| Thẻ 6 — Liên hệ mới | `new_contacts` | Số liên hệ status=new |

```
API: GET /admin/dashboard/stats
Response dùng: total_tours_sold, pending_ratings, new_contacts
```

> **Lưu ý:** Nếu backend chưa trả `pending_ratings` và `new_contacts` trong stats,
> có thể gọi thêm:
> - `GET /admin/ratings?status=pending` → đếm `total` trong meta
> - `GET /admin/contacts?status=new` → đếm `total` trong meta

---

### HÀNG 3 — Biểu đồ (2 cột)

#### Cột trái — Line chart "Doanh thu theo ngày"

```
API: GET /admin/dashboard/revenue?period=day&from=2026-03-01&to=2026-04-06
```

| Query param | Giá trị | Mô tả |
|-------------|---------|-------|
| `period` | `day` \| `week` \| `month` \| `year` | Điều khiển bởi tab filter |
| `from` | ISO date | Ngày bắt đầu |
| `to` | ISO date | Ngày kết thúc |

Response dùng: mảng `[{ date, revenue }]` để vẽ line chart.
Tab filter "Ngày/Tuần/Tháng/Năm" thay đổi `period` → gọi lại API.

#### Cột phải — Stacked bar chart "Xu hướng đặt tour"

```
API: GET /admin/dashboard/booking-trend?days=30
```

| Query param | Giá trị | Mô tả |
|-------------|---------|-------|
| `days` | `7` \| `30` \| `90` | Điều khiển bởi tab "7 ngày / 30 ngày / 90 ngày" |

Response dùng: mảng `[{ date, completed, confirmed, pending, cancelled }]`
để vẽ stacked bar chart.

---

### HÀNG 4 — Biểu đồ (2 cột)

#### Cột trái — Area chart "Tăng trưởng người dùng"

```
API: GET /admin/dashboard/user-growth?year=2026
```

| Query param | Giá trị | Mô tả |
|-------------|---------|-------|
| `year` | số năm | Mặc định năm hiện tại |

Response dùng: mảng `[{ month/week, new_users, total_users }]`
để vẽ area chart theo tuần/tháng.

#### Cột phải — Vertical bar chart "Trạng thái đơn hàng"

```
API: GET /admin/dashboard/stats
```

Response dùng: breakdown `booking_status` gồm:
`completed_count`, `confirmed_count`, `pending_count`, `cancelled_count`

> Cùng request với Hàng 1 & 2 — không cần gọi thêm.

---

### HÀNG 5 — Bảng dữ liệu (full width, xếp dọc)

#### Bảng 1 — Top 5 Tour bán chạy

```
API: GET /admin/dashboard/top-tours?limit=5&from=2026-03-01&to=2026-04-06
```

| Query param | Giá trị | Mô tả |
|-------------|---------|-------|
| `limit` | `5` | Số tour hiển thị |
| `from` | ISO date | Lọc theo khoảng thời gian (tuỳ chọn) |
| `to` | ISO date | Lọc theo khoảng thời gian (tuỳ chọn) |

Cột hiển thị: Rank · Tên tour + thumbnail · Lượt bán · Doanh thu · Đánh giá · Trạng thái

#### Bảng 2 — Đơn hàng gần đây

```
API: GET /admin/bookings?page=1&per_page=8&sort=booked_at&order=desc
```

| Query param | Giá trị | Mô tả |
|-------------|---------|-------|
| `page` | `1` | Trang đầu |
| `per_page` | `8` | Số dòng hiển thị |
| `sort` | `booked_at` | Sắp xếp theo ngày đặt |
| `order` | `desc` | Mới nhất lên đầu |
| `status` | `pending` \| `confirmed` \| `cancelled` | Filter tab trạng thái (tuỳ chọn) |

Cột hiển thị: Mã đơn · Khách hàng · Tour · Ngày đặt · Trạng thái · Tổng tiền · Thao tác

---

## Tổng hợp tất cả API của màn Dashboard

| # | API | Method | Vị trí sử dụng | Gọi lúc |
|---|-----|--------|----------------|---------|
| 1 | `/admin/dashboard/stats` | GET | Hàng 1, Hàng 2, Hàng 4 (cột phải) | Khi load trang |
| 2 | `/admin/dashboard/revenue` | GET | Hàng 3 — line chart | Khi load + khi đổi tab period |
| 3 | `/admin/dashboard/booking-trend` | GET | Hàng 3 — bar chart | Khi load + khi đổi tab days |
| 4 | `/admin/dashboard/user-growth` | GET | Hàng 4 — area chart | Khi load trang |
| 5 | `/admin/dashboard/top-tours` | GET | Hàng 5 — bảng top tour | Khi load trang |
| 6 | `/admin/bookings` | GET | Hàng 5 — bảng đơn hàng | Khi load + khi filter/phân trang |

> **Tổng: 6 API** — trong đó `/admin/dashboard/stats` phục vụ 3 vị trí khác nhau,
> chỉ cần gọi 1 lần duy nhất khi load trang.

---

## Ghi chú kỹ thuật

- Nút **"Làm mới"** ở header → gọi lại toàn bộ 6 API trên.
- Nút **"Xuất báo cáo"** → gọi `GET /admin/bookings/export` hoặc `GET /admin/payments/export`.
- Các tab filter (period, days, status) → chỉ gọi lại API tương ứng, không reload toàn trang.
- Phân trang bảng đơn hàng → gọi lại `GET /admin/bookings` với `page` mới.
- Tất cả API yêu cầu header `Authorization: Bearer {token}` (role admin/staff).
