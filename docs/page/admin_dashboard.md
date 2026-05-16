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

## Cấu trúc Response thực tế từng API

---

### 1. GET /admin/dashboard/stats

```
GET /admin/dashboard/stats
```

```json
{
  "code": 200,
  "message": "Success",
  "data": {
    "total_users": 23,        // int — tổng số user
    "total_tours": 35,        // int — tổng số tour
    "total_bookings": 38,     // int — tổng số đơn hàng
    "total_revenue": 0        // number — tổng doanh thu (VNĐ)
  }
}
```

**Khai báo TypeScript:**
```ts
interface DashboardStats {
  total_users: number;
  total_tours: number;
  total_bookings: number;
  total_revenue: number;
}
// Truy cập: response.data
```

⚠️ **Thiếu:** `total_tours_sold`, `pending_ratings`, `new_contacts` — cần gọi thêm:
- `GET /admin/ratings?status=pending` → `response.data.total`
- `GET /admin/contacts?status=new` → `response.data.total`

---

### 2. GET /admin/dashboard/revenue

**Hôm nay** (`period=day`, `from=to`):
```
GET /admin/dashboard/revenue?period=day&from=2026-04-17&to=2026-04-17
```
```json
{
  "code": 200,
  "data": {
    "period": "day",
    "from": "2026-04-17",
    "to": "2026-04-17",
    "stats": [
      { "period": "00:00", "total_revenue": "0",            "transaction_count": 0 },
      { "period": "01:00", "total_revenue": "3135000.00",   "transaction_count": 1 },
      { "period": "02:00", "total_revenue": "0",            "transaction_count": 0 },
      "... 24 items (00:00 → 23:00)"
    ]
  }
}
```
⚠️ Khi `from = to` (cùng 1 ngày): `stats[].period` là **giờ** dạng `"HH:00"` (24 items)

**Tuần/Tháng này** (`period=week` hoặc `period=month`):
```
GET /admin/dashboard/revenue?period=week&from=2026-04-13&to=2026-04-17
```
```json
{
  "data": {
    "stats": [
      { "period": "2026-04-13", "total_revenue": "0",           "transaction_count": 0 },
      { "period": "2026-04-16", "total_revenue": "15450000.00", "transaction_count": 7 },
      { "period": "2026-04-17", "total_revenue": "15580000.00", "transaction_count": 7 }
    ]
  }
}
```
`stats[].period` là ngày `"YYYY-MM-DD"`, fill đủ các ngày thiếu = 0

**Năm này** (`period=year`):
```json
{
  "data": {
    "stats": [
      { "period": "2026-04", "total_revenue": "31030000.00", "transaction_count": 14 }
    ]
  }
}
```
`stats[].period` là tháng `"YYYY-MM"`

**Khai báo TypeScript:**
```ts
interface RevenueItem {
  period: string;
  // Khi period=day & from=to: "HH:00" (giờ trong ngày)
  // Khi period=day/week:      "YYYY-MM-DD"
  // Khi period=month/year:    "YYYY-MM"
  // Khi period=year (range):  "YYYY"
  total_revenue: string;     // parse: parseFloat(total_revenue)
  transaction_count: number;
}
interface RevenueData {
  period: 'day' | 'week' | 'month' | 'year';
  from: string | null;
  to: string | null;
  stats: RevenueItem[];      // đã được fill đủ các khoảng thiếu = 0
}
// Truy cập: response.data.stats
// Trục X: item.period | Trục Y: parseFloat(item.total_revenue)
```

---

### 3. GET /admin/dashboard/booking-trend

```
GET /admin/dashboard/booking-trend?days=7
```

```json
{
  "code": 200,
  "message": "Success",
  "data": {
    "days": "7",               // string — số ngày (dù truyền number)
    "stats": [
      {
        "date": "2026-04-10",  // string — "YYYY-MM-DD"
        "count": 8             // int — tổng số đơn trong ngày
      }
    ]
  }
}
```

**Khai báo TypeScript:**
```ts
interface BookingTrendItem { date: string; count: number; }
interface BookingTrendData { days: string; stats: BookingTrendItem[]; }
// Truy cập: response.data.stats → vẽ bar chart
```

⚠️ **Thiếu breakdown:** Chỉ có `count` tổng, không có `completed/confirmed/pending/cancelled`.
Không vẽ được stacked bar — chỉ vẽ bar chart đơn. Backend cần bổ sung nếu muốn stacked.

---

### 4. GET /admin/dashboard/user-growth

```
GET /admin/dashboard/user-growth?year=2026
```

```json
{
  "code": 200,
  "message": "Success",
  "data": {
    "year": "2026",            // string — năm (dù truyền number)
    "stats": [
      {
        "month": "4",          // string — số tháng "1"–"12"
        "count": 23            // int — số user mới trong tháng
      }
    ]
  }
}
```

**Khai báo TypeScript:**
```ts
interface UserGrowthItem { month: string; count: number; }
interface UserGrowthData { year: string; stats: UserGrowthItem[]; }
// Truy cập: response.data.stats → vẽ area chart
// Lưu ý: month là string "1"–"12", map sang "Tháng 1"–"Tháng 12"
```

---

### 5. GET /admin/dashboard/top-tours

```
GET /admin/dashboard/top-tours?limit=5
```

```json
{
  "code": 200,
  "message": "Success",
  "data": [
    {
      "id": 8,                          // int
      "name": "Phượt đỉnh Đèo Hải Vân", // string
      "slug": "phuot-dinh-deo-hai-van-...", // string
      "booking_count": 7,               // int — số lượt đặt
      "total_revenue": "16575000"       // string — cần parseFloat()
    }
  ]
}
```

**Khai báo TypeScript:**
```ts
interface TopTourItem {
  id: number;
  name: string;
  slug: string;
  booking_count: number;
  total_revenue: string; // parse: parseFloat(total_revenue)
}
// Truy cập: response.data (mảng trực tiếp, KHÔNG phải response.data.data)
```

⚠️ **Thiếu:** `thumbnail`, `avg_rating`, `status` — backend cần bổ sung.

---

### 6. GET /admin/dashboard/top-locations

```
GET /admin/dashboard/top-locations?limit=5
```

```json
{
  "code": 200,
  "message": "Success",
  "data": [
    {
      "id": 109,                        // int
      "name": "Địa điểm Ung-Đinh",      // string
      "slug": "dia-diem-ung-dinh-...",  // string
      "district": "Thanh Khê",          // string
      "favorite_count": 200,            // int
      "view_count": 4216,               // int
      "avg_rating": "4.03",             // string — cần parseFloat()
      "review_count": 89                // int
    }
  ]
}
```

**Khai báo TypeScript:**
```ts
interface TopLocationItem {
  id: number;
  name: string;
  slug: string;
  district: string;
  favorite_count: number;
  view_count: number;
  avg_rating: string; // parse: parseFloat(avg_rating)
  review_count: number;
}
// Truy cập: response.data (mảng trực tiếp)
```

---

### 7. GET /admin/bookings

```
GET /admin/bookings?page=1&per_page=8&sort=booked_at&order=desc
```

```json
{
  "code": 200,
  "message": "Bookings retrieved successfully.",
  "data": {
    "current_page": 1,
    "data": [
      {
        "id": 38,
        "booking_code": "BOOK-FGLZE5HE",   // string
        "user_id": 2,
        "customer_name": "Test User",        // string
        "customer_email": "test@example.com",
        "customer_phone": "0901234567",
        "customer_address": null,
        "customer_note": null,
        "total_amount": "1500000.00",        // string — cần parseFloat()
        "discount_amount": "75000.00",       // string
        "final_amount": "1425000.00",        // string — số tiền thực trả
        "deposit_amount": "0.00",            // string
        "payment_method": "cash",            // string: "cash"|"momo"|"vnpay"|"zalopay"
        "payment_status": "pending",         // string: "pending"|"paid"|"refunded"
        "booking_status": "cancelled",       // string: "pending"|"confirmed"|"completed"|"cancelled"
        "cancellation_reason": "Admin huy",  // string|null
        "booked_at": "2026-04-10T03:53:51.000000Z",   // ISO datetime
        "confirmed_at": null,                // ISO datetime|null
        "cancelled_at": "2026-04-10T03:53:57.000000Z", // ISO datetime|null
        "completed_at": null,                // ISO datetime|null
        "created_at": "2026-04-10T03:53:51.000000Z",
        "updated_at": "2026-04-10T03:53:57.000000Z",
        "user": {
          "id": 2,
          "username": "user1",
          "email": "user1@example.com",
          "full_name": "Nguyen Van A",
          "avatar": "avatars/abc.png"        // string — relative path
        }
      }
    ],
    "total": 38,          // int — tổng số đơn
    "per_page": 8,        // int
    "last_page": 5,       // int — tổng số trang
    "from": 1,
    "to": 8
  }
}
```

**Khai báo TypeScript:**
```ts
interface BookingUser { id: number; username: string; email: string; full_name: string; avatar: string; }
interface Booking {
  id: number;
  booking_code: string;
  user_id: number;
  customer_name: string;
  customer_email: string;
  customer_phone: string;
  customer_address: string | null;
  customer_note: string | null;
  total_amount: string;
  discount_amount: string;
  final_amount: string;
  deposit_amount: string;
  payment_method: string;
  payment_status: 'pending' | 'paid' | 'refunded';
  booking_status: 'pending' | 'confirmed' | 'completed' | 'cancelled';
  cancellation_reason: string | null;
  booked_at: string;
  confirmed_at: string | null;
  cancelled_at: string | null;
  completed_at: string | null;
  created_at: string;
  updated_at: string;
  user: BookingUser;
}
interface BookingListResponse {
  current_page: number;
  data: Booking[];
  total: number;
  per_page: number;
  last_page: number;
}
// Truy cập: response.data.data (mảng), response.data.total, response.data.last_page
```

---

### 8. GET /admin/reports/bookings

```
GET /admin/reports/bookings?from=2026-01-01&to=2026-12-31
```

```json
{
  "code": 200,
  "message": "Success",
  "data": [
    {
      "date": "2026-03-11",              // string — "YYYY-MM-DD"
      "booking_status": "cancelled",     // string
      "payment_status": "paid",          // string
      "count": 1,                        // int
      "total_amount": "2960000.00"       // string
    }
  ]
}
```

**Khai báo TypeScript:**
```ts
interface BookingReportItem {
  date: string;
  booking_status: string;
  payment_status: string;
  count: number;
  total_amount: string;
}
// Truy cập: response.data (mảng trực tiếp)
```

---

### 9. GET /admin/reports/ratings

```
GET /admin/reports/ratings?from=2026-01-01&to=2026-12-31
```

```json
{
  "code": 200,
  "message": "Success",
  "data": [
    {
      "date": "2026-01-08",    // string — "YYYY-MM-DD"
      "status": "approved",    // string: "approved"|"pending"|"rejected"
      "count": 2               // int
    }
  ]
}
```

**Khai báo TypeScript:**
```ts
interface RatingReportItem {
  date: string;
  status: 'approved' | 'pending' | 'rejected';
  count: number;
}
// Truy cập: response.data (mảng trực tiếp)
```

---

### 10. GET /admin/reports/users

```
GET /admin/reports/users?year=2026
```

```json
{
  "code": 200,
  "message": "Success",
  "data": {
    "year": "2026",
    "stats": [
      { "month": "4", "count": 23 }
    ]
  }
}
```

Cấu trúc giống `user-growth` — dùng `data.stats`.

---

### 11. GET /admin/reports/revenue-detail

```
GET /admin/reports/revenue-detail?from=2026-01-01&to=2026-12-31
```

```json
{
  "code": 200,
  "message": "Success",
  "data": []
}
```

⚠️ Hiện trả mảng rỗng — chưa có dữ liệu hoặc backend chưa implement đầy đủ.

---

## Tổng hợp tất cả API của màn Dashboard

| # | API | Method | Vị trí sử dụng | Gọi lúc | Key response |
|---|-----|--------|----------------|---------|-------------|
| 1 | `/admin/dashboard/stats` | GET | Hàng 1, Hàng 2, Hàng 4 (cột phải) | Khi load trang | `data.total_users/tours/bookings/revenue` |
| 2 | `/admin/dashboard/revenue` | GET | Hàng 3 — line chart | Khi load + đổi tab period | `data.stats[]` → `{date, revenue}` |
| 3 | `/admin/dashboard/booking-trend` | GET | Hàng 3 — bar chart | Khi load + đổi tab days | `data.stats[]` → `{date, count}` |
| 4 | `/admin/dashboard/user-growth` | GET | Hàng 4 — area chart | Khi load trang | `data.stats[]` → `{month, count}` |
| 5 | `/admin/dashboard/top-tours` | GET | Hàng 5 — bảng top tour | Khi load trang | `data[]` → `{id, name, booking_count, total_revenue}` |
| 6 | `/admin/bookings` | GET | Hàng 5 — bảng đơn hàng | Khi load + filter/phân trang | `data.data[]` → booking objects |
| 7 | `/admin/ratings?status=pending` | GET | Hàng 2 — thẻ đánh giá chờ | Khi load trang | `meta.total` hoặc `data.total` |
| 8 | `/admin/contacts?status=new` | GET | Hàng 2 — thẻ liên hệ mới | Khi load trang | `meta.total` hoặc `data.total` |

> **Tổng: 8 API** — `/admin/dashboard/stats` phục vụ 3 vị trí, chỉ gọi 1 lần.
> API 7 và 8 cần thêm nếu backend chưa trả `pending_ratings`/`new_contacts` trong stats.

## Dữ liệu thực tế hiện tại (2026-04-17)

| Tab | Doanh thu | Giao dịch |
|-----|-----------|-----------|
| Hôm nay (17/04) | **15.580.000 VNĐ** | 7 GD (theo giờ 01:00–13:00) |
| Tuần này (13–17/04) | **31.030.000 VNĐ** | 14 GD (16/04 + 17/04) |
| Tháng này (04/2026) | **31.030.000 VNĐ** | 14 GD |
| Năm này (2026) | **31.030.000 VNĐ** | 14 GD (tháng 04) |

**Trạng thái đơn hàng:** pending=9 · confirmed=20 · completed=8 · cancelled=14 (tổng 51)

**Tăng trưởng người dùng:** 23 users tất cả trong tháng 4/2026

---

- Nút **"Làm mới"** ở header → gọi lại toàn bộ 6 API trên.
- Nút **"Xuất báo cáo"** → gọi `GET /admin/bookings/export` hoặc `GET /admin/payments/export`.
- Các tab filter (period, days, status) → chỉ gọi lại API tương ứng, không reload toàn trang.
- Phân trang bảng đơn hàng → gọi lại `GET /admin/bookings` với `page` mới.
- Tất cả API yêu cầu header `Authorization: Bearer {token}` (role admin/staff).

---

## Validation & States

| Hạng mục | Quy tắc |
|---|---|
| Date range | `from <= to`; không cho chọn khoảng ngày tương lai nếu báo cáo chỉ tính dữ liệu đã phát sinh |
| Period | Chỉ nhận `day`, `week`, `month`, `year`; mặc định `day` khi giá trị không hợp lệ |
| Days filter | `booking-trend.days` chỉ nhận số nguyên dương, khuyến nghị tối đa 365 |
| Limit top list | `limit` tối thiểu 1, tối đa 20; mặc định 5 hoặc 10 theo API |
| Empty chart | Nếu API trả mảng rỗng, hiển thị biểu đồ rỗng kèm text "Chưa có dữ liệu trong khoảng thời gian này" |
| API lỗi | Giữ layout dashboard, từng card lỗi hiển thị retry riêng, không làm trắng toàn màn |
| Permission | Nếu role không phải admin/staff, chuyển 403 thay vì gọi API dashboard |
