# Test Cases — ADMIN DASHBOARD & REPORTS

> Base URL: `http://localhost:8000/api/v1`
> Branch: `feat/taynd/api-admin-dashboard`
> 🛡️ Admin token bắt buộc cho tất cả endpoints

---

## 1. GET /admin/dashboard/stats — Tổng quan

### ✅ TC01 — Lấy stats thành công
```http
GET /api/v1/admin/dashboard/stats
Authorization: Bearer {admin_token}
```
- Expected: `200 OK`
- Verify: có các field `total_users`, `total_tours`, `total_bookings`, `total_revenue`

### ❌ TC02 — User thường bị 403
- Expected: `403 Forbidden`

### ❌ TC03 — Không có token → 401
- Expected: `401 Unauthorized`

---

## 2. GET /admin/dashboard/revenue — Thống kê doanh thu

### ✅ TC05 — Lấy revenue mặc định
```http
GET /api/v1/admin/dashboard/revenue
```
- Expected: `200 OK`, `data` là array theo thời gian

### ✅ TC06 — Filter `period=day`
```http
GET /api/v1/admin/dashboard/revenue?period=day
```
- Expected: `200 OK`

### ✅ TC07 — Filter `period=week`
```http
GET /api/v1/admin/dashboard/revenue?period=week
```
- Expected: `200 OK`

### ✅ TC08 — Filter `period=month`
```http
GET /api/v1/admin/dashboard/revenue?period=month
```
- Expected: `200 OK`

### ✅ TC09 — Filter `period=year`
```http
GET /api/v1/admin/dashboard/revenue?period=year
```
- Expected: `200 OK`

### ✅ TC10 — Filter `from` và `to`
```http
GET /api/v1/admin/dashboard/revenue?from=2026-01-01&to=2026-12-31
```
- Expected: `200 OK`

### ❌ TC11 — `period` sai giá trị → 422
```http
GET /api/v1/admin/dashboard/revenue?period=invalid
```
- Expected: `422 Unprocessable`

### ❌ TC12 — `from` sai định dạng → 422
```http
GET /api/v1/admin/dashboard/revenue?from=31-01-2026
```
- Expected: `422 Unprocessable`

### ❌ TC13 — User thường bị 403
- Expected: `403 Forbidden`

### ❌ TC14 — Không có token → 401
- Expected: `401 Unauthorized`

---

## 3. GET /admin/dashboard/top-tours — Top tour bán chạy

### ✅ TC15 — Lấy top tours mặc định
```http
GET /api/v1/admin/dashboard/top-tours
```
- Expected: `200 OK`, `data` là array, mỗi item có `id`, `name`

### ✅ TC16 — Giới hạn `limit=5`
```http
GET /api/v1/admin/dashboard/top-tours?limit=5
```
- Expected: `200 OK`, `data` có tối đa 5 phần tử

### ✅ TC17 — Filter `from` và `to`
```http
GET /api/v1/admin/dashboard/top-tours?from=2026-01-01&to=2026-12-31
```
- Expected: `200 OK`

### ❌ TC18 — `limit` không phải số → 422
```http
GET /api/v1/admin/dashboard/top-tours?limit=abc
```
- Expected: `422 Unprocessable`

### ❌ TC19 — User thường bị 403
- Expected: `403 Forbidden`

### ❌ TC20 — Không có token → 401
- Expected: `401 Unauthorized`

---

## 4. GET /admin/dashboard/top-locations — Top địa điểm

### ✅ TC21 — Lấy top locations mặc định
```http
GET /api/v1/admin/dashboard/top-locations
```
- Expected: `200 OK`, `data` là array, mỗi item có `id`, `name`

### ✅ TC22 — Giới hạn `limit=5`
```http
GET /api/v1/admin/dashboard/top-locations?limit=5
```
- Expected: `200 OK`, `data` có tối đa 5 phần tử

### ❌ TC23 — `limit` không phải số → 422
- Expected: `422 Unprocessable`

### ❌ TC24 — User thường bị 403
- Expected: `403 Forbidden`

### ❌ TC25 — Không có token → 401
- Expected: `401 Unauthorized`

---

## 5. GET /admin/dashboard/user-growth — Tăng trưởng người dùng

### ✅ TC26 — Lấy user growth năm hiện tại
```http
GET /api/v1/admin/dashboard/user-growth
```
- Expected: `200 OK`
- Verify: data theo tháng (12 phần tử hoặc tương đương)

### ✅ TC27 — Filter `year=2026`
```http
GET /api/v1/admin/dashboard/user-growth?year=2026
```
- Expected: `200 OK`

### ✅ TC28 — Filter `year` năm quá khứ
```http
GET /api/v1/admin/dashboard/user-growth?year=2025
```
- Expected: `200 OK`

### ❌ TC29 — `year` không phải số → 422
```http
GET /api/v1/admin/dashboard/user-growth?year=abc
```
- Expected: `422 Unprocessable`

### ❌ TC30 — User thường bị 403
- Expected: `403 Forbidden`

### ❌ TC31 — Không có token → 401
- Expected: `401 Unauthorized`

---

## 6. GET /admin/dashboard/booking-trend — Xu hướng đặt tour

### ✅ TC32 — Lấy booking trend mặc định (30 ngày)
```http
GET /api/v1/admin/dashboard/booking-trend
```
- Expected: `200 OK`, `data` là array theo ngày

### ✅ TC33 — Filter `days=7`
```http
GET /api/v1/admin/dashboard/booking-trend?days=7
```
- Expected: `200 OK`

### ✅ TC34 — Filter `days=90`
```http
GET /api/v1/admin/dashboard/booking-trend?days=90
```
- Expected: `200 OK`

### ❌ TC35 — `days` âm → 422
```http
GET /api/v1/admin/dashboard/booking-trend?days=-1
```
- Expected: `422 Unprocessable`

### ❌ TC36 — `days` không phải số → 422
```http
GET /api/v1/admin/dashboard/booking-trend?days=abc
```
- Expected: `422 Unprocessable`

### ❌ TC37 — User thường bị 403
- Expected: `403 Forbidden`

### ❌ TC38 — Không có token → 401
- Expected: `401 Unauthorized`

---

## 7. GET /admin/reports/bookings — Báo cáo đơn hàng

### ✅ TC39 — Lấy báo cáo không filter
```http
GET /api/v1/admin/reports/bookings
```
- Expected: `200 OK`

### ✅ TC40 — Filter `from` và `to`
```http
GET /api/v1/admin/reports/bookings?from=2026-01-01&to=2026-12-31
```
- Expected: `200 OK`

### ✅ TC41 — Filter `status=confirmed`
```http
GET /api/v1/admin/reports/bookings?status=confirmed
```
- Expected: `200 OK`

### ✅ TC42 — Filter `payment_status=paid`
```http
GET /api/v1/admin/reports/bookings?payment_status=paid
```
- Expected: `200 OK`

### ✅ TC43 — Kết hợp tất cả filters
```http
GET /api/v1/admin/reports/bookings?from=2026-01-01&to=2026-12-31&status=confirmed&payment_status=paid
```
- Expected: `200 OK`

### ❌ TC44 — `status` sai giá trị → 422
```http
GET /api/v1/admin/reports/bookings?status=invalid
```
- Expected: `422 Unprocessable`

### ❌ TC45 — `from` sai định dạng → 422
- Expected: `422 Unprocessable`

### ❌ TC46 — User thường bị 403
- Expected: `403 Forbidden`

### ❌ TC47 — Không có token → 401
- Expected: `401 Unauthorized`

---

## 8. GET /admin/reports/ratings — Thống kê đánh giá

### ✅ TC48 — Lấy báo cáo không filter
```http
GET /api/v1/admin/reports/ratings
```
- Expected: `200 OK`

### ✅ TC49 — Filter `from` và `to`
```http
GET /api/v1/admin/reports/ratings?from=2026-01-01&to=2026-12-31
```
- Expected: `200 OK`

### ✅ TC50 — Filter `status=approved`
```http
GET /api/v1/admin/reports/ratings?status=approved
```
- Expected: `200 OK`

### ✅ TC51 — Filter `status=pending`
- Expected: `200 OK`

### ✅ TC52 — Filter `status=rejected`
- Expected: `200 OK`

### ❌ TC53 — `status` sai giá trị → 422
- Expected: `422 Unprocessable`

### ❌ TC54 — `from` sai định dạng → 422
- Expected: `422 Unprocessable`

### ❌ TC55 — User thường bị 403
- Expected: `403 Forbidden`

### ❌ TC56 — Không có token → 401
- Expected: `401 Unauthorized`

---

## 9. GET /admin/reports/users — Thống kê người dùng mới

### ✅ TC57 — Lấy báo cáo năm hiện tại
```http
GET /api/v1/admin/reports/users
```
- Expected: `200 OK`, data theo tháng

### ✅ TC58 — Filter `year=2026`
```http
GET /api/v1/admin/reports/users?year=2026
```
- Expected: `200 OK`

### ✅ TC59 — Filter `year` năm quá khứ
```http
GET /api/v1/admin/reports/users?year=2025
```
- Expected: `200 OK`

### ❌ TC60 — `year` không phải số → 422
- Expected: `422 Unprocessable`

### ❌ TC61 — User thường bị 403
- Expected: `403 Forbidden`

### ❌ TC62 — Không có token → 401
- Expected: `401 Unauthorized`

---

## 10. GET /admin/reports/revenue-detail — Doanh thu chi tiết theo tour

### ✅ TC63 — Lấy báo cáo không filter
```http
GET /api/v1/admin/reports/revenue-detail
```
- Expected: `200 OK`

### ✅ TC64 — Filter `from` và `to`
```http
GET /api/v1/admin/reports/revenue-detail?from=2026-01-01&to=2026-12-31
```
- Expected: `200 OK`

### ❌ TC65 — `from` sai định dạng → 422
- Expected: `422 Unprocessable`

### ❌ TC66 — User thường bị 403
- Expected: `403 Forbidden`

### ❌ TC67 — Không có token → 401
- Expected: `401 Unauthorized`

---

## Tổng kết

| TC | API | Trường hợp | Expected |
|----|-----|-----------|----------|
| TC01–TC03 | GET /admin/dashboard/stats | Stats, fields, auth | 200/403/401 |
| TC04–TC13 | GET /admin/dashboard/revenue | Revenue, period, date, auth | 200/422/403/401 |
| TC14–TC19 | GET /admin/dashboard/top-tours | Top tours, limit, date, auth | 200/422/403/401 |
| TC20–TC24 | GET /admin/dashboard/top-locations | Top locations, limit, auth | 200/422/403/401 |
| TC25–TC30 | GET /admin/dashboard/user-growth | User growth, year, auth | 200/422/403/401 |
| TC31–TC37 | GET /admin/dashboard/booking-trend | Booking trend, days, auth | 200/422/403/401 |
| TC38–TC46 | GET /admin/reports/bookings | Bookings report, filters, auth | 200/422/403/401 |
| TC47–TC55 | GET /admin/reports/ratings | Ratings report, filters, auth | 200/422/403/401 |
| TC56–TC61 | GET /admin/reports/users | Users report, year, auth | 200/422/403/401 |
| TC62–TC66 | GET /admin/reports/revenue-detail | Revenue detail, date, auth | 200/422/403/401 |

**Tổng: 66 test cases** — 33 happy path ✅ · 33 error case ❌
