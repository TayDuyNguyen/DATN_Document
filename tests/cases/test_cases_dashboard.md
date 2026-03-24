# Test Cases  ADMIN DASHBOARD & REPORTS

> Base URL: `http://localhost:8000/api/v1`
>  Admin token bắt buộc cho tất cả endpoints

---

## 1. GET /admin/dashboard  Tổng quan

###  TC01  Lấy dashboard thành công
```http
GET /api/v1/admin/dashboard
```
- Expected: `200 OK`
- Verify: response có các field thống kê tổng quan (users, locations, ratings, views)

###  TC02  Response có đủ các field cần thiết
- Expected: `200 OK`
- Verify: có ít nhất các field: `total_users`, `total_locations`, `total_ratings`, `total_views` (hoặc tên tương đương)

###  TC03  User thường không được truy cập
```http
GET /api/v1/admin/dashboard
```
- Expected: `403 Forbidden`

###  TC04  Không có token
```http
GET /api/v1/admin/dashboard
```
- Expected: `401 Unauthorized`

---

## 2. GET /admin/reports/locations  Thống kê địa điểm

###  TC05  Lấy thống kê không filter
```http
GET /api/v1/admin/reports/locations
```
- Expected: `200 OK`
- Verify: response có data thống kê theo category hoặc district

###  TC06  Filter `from` và `to` hợp lệ
```http
GET /api/v1/admin/reports/locations?from=2026-01-01&to=2026-03-31
```
- Expected: `200 OK`

###  TC07  Filter chỉ `from`
```http
GET /api/v1/admin/reports/locations?from=2026-01-01
```
- Expected: `200 OK`

###  TC08  Filter chỉ `to`
```http
GET /api/v1/admin/reports/locations?to=2026-03-31
```
- Expected: `200 OK`

###  TC09  `from` sai định dạng ngày
```http
GET /api/v1/admin/reports/locations?from=31-01-2026
```
- Expected: `422 Unprocessable`

###  TC10  `to` sai định dạng ngày
```http
GET /api/v1/admin/reports/locations?to=not-a-date
```
- Expected: `422 Unprocessable`

###  TC11  `from` > `to` (khoảng ngày ngược)
```http
GET /api/v1/admin/reports/locations?from=2026-12-31&to=2026-01-01
```
- Expected: `422 Unprocessable` hoặc `200 OK` với data rỗng

###  TC12  User thường không được truy cập
- Expected: `403 Forbidden`

###  TC13  Không có token
- Expected: `401 Unauthorized`

---

## 3. GET /admin/reports/ratings  Thống kê đánh giá

###  TC14  Lấy thống kê không filter
```http
GET /api/v1/admin/reports/ratings
```
- Expected: `200 OK`
- Verify: response có data thống kê theo thời gian

###  TC15  Filter `from` và `to`
```http
GET /api/v1/admin/reports/ratings?from=2026-01-01&to=2026-03-31
```
- Expected: `200 OK`

###  TC16  Filter `status=pending`
```http
GET /api/v1/admin/reports/ratings?status=pending
```
- Expected: `200 OK`

###  TC17  Filter `status=approved`
```http
GET /api/v1/admin/reports/ratings?status=approved
```
- Expected: `200 OK`

###  TC18  Filter `status=rejected`
```http
GET /api/v1/admin/reports/ratings?status=rejected
```
- Expected: `200 OK`

###  TC19  Kết hợp `from`, `to`, `status`
```http
GET /api/v1/admin/reports/ratings?from=2026-01-01&to=2026-03-31&status=approved
```
- Expected: `200 OK`

###  TC20  `status` sai giá trị
```http
GET /api/v1/admin/reports/ratings?status=invalid
```
- Expected: `422 Unprocessable`

###  TC21  `from` sai định dạng
```http
GET /api/v1/admin/reports/ratings?from=not-a-date
```
- Expected: `422 Unprocessable`

###  TC22  User thường không được truy cập
- Expected: `403 Forbidden`

###  TC23  Không có token
- Expected: `401 Unauthorized`

---

## 4. GET /admin/reports/users  Thống kê người dùng mới

###  TC24  Lấy thống kê không filter (năm hiện tại)
```http
GET /api/v1/admin/reports/users
```
- Expected: `200 OK`
- Verify: response có 12 tháng hoặc data theo tháng

###  TC25  Filter `year` hợp lệ
```http
GET /api/v1/admin/reports/users?year=2026
```
- Expected: `200 OK`
- Verify: data thuộc năm 2026

###  TC26  Filter `year` năm quá khứ
```http
GET /api/v1/admin/reports/users?year=2025
```
- Expected: `200 OK`

###  TC27  `year` không phải số
```http
GET /api/v1/admin/reports/users?year=abc
```
- Expected: `422 Unprocessable`

###  TC28  `year` quá nhỏ (vô lý)
```http
GET /api/v1/admin/reports/users?year=1900
```
- Expected: `422 Unprocessable` hoặc `200 OK` với data rỗng

###  TC29  User thường không được truy cập
- Expected: `403 Forbidden`

###  TC30  Không có token
- Expected: `401 Unauthorized`

---

## 5. GET /admin/reports/points  Thống kê giao dịch point

###  TC31  Lấy thống kê không filter
```http
GET /api/v1/admin/reports/points
```
- Expected: `200 OK`
- Verify: response có data thống kê giao dịch

###  TC32  Filter `from` và `to`
```http
GET /api/v1/admin/reports/points?from=2026-01-01&to=2026-03-31
```
- Expected: `200 OK`

###  TC33  Filter `type=purchase`
```http
GET /api/v1/admin/reports/points?type=purchase
```
- Expected: `200 OK`

###  TC34  Filter `type=spend`
```http
GET /api/v1/admin/reports/points?type=spend
```
- Expected: `200 OK`

###  TC35  Filter `type=bonus`
```http
GET /api/v1/admin/reports/points?type=bonus
```
- Expected: `200 OK`

###  TC36  Filter `type=refund`
```http
GET /api/v1/admin/reports/points?type=refund
```
- Expected: `200 OK`

###  TC37  Kết hợp `from`, `to`, `type`
```http
GET /api/v1/admin/reports/points?from=2026-01-01&to=2026-03-31&type=purchase
```
- Expected: `200 OK`

###  TC38  `type` sai giá trị
```http
GET /api/v1/admin/reports/points?type=invalid
```
- Expected: `422 Unprocessable`

###  TC39  `from` sai định dạng
```http
GET /api/v1/admin/reports/points?from=not-a-date
```
- Expected: `422 Unprocessable`

###  TC40  User thường không được truy cập
- Expected: `403 Forbidden`

###  TC41  Không có token
- Expected: `401 Unauthorized`

---

## Tổng kết

| TC | API | Trường hợp | Expected |
|----|-----|-----------|----------|
| TC01 | GET /admin/dashboard | Lấy tổng quan | 200 |
| TC02 | GET /admin/dashboard | Đủ fields | 200 |
| TC03 | GET /admin/dashboard | User thường | 403 |
| TC04 | GET /admin/dashboard | Không có token | 401 |
| TC05 | GET /admin/reports/locations | Không filter | 200 |
| TC06 | GET /admin/reports/locations | from + to | 200 |
| TC07 | GET /admin/reports/locations | Chỉ from | 200 |
| TC08 | GET /admin/reports/locations | Chỉ to | 200 |
| TC09 | GET /admin/reports/locations | from sai định dạng | 422 |
| TC10 | GET /admin/reports/locations | to sai định dạng | 422 |
| TC11 | GET /admin/reports/locations | from > to | 422/200 |
| TC12 | GET /admin/reports/locations | User thường | 403 |
| TC13 | GET /admin/reports/locations | Không có token | 401 |
| TC14 | GET /admin/reports/ratings | Không filter | 200 |
| TC15 | GET /admin/reports/ratings | from + to | 200 |
| TC16 | GET /admin/reports/ratings | status=pending | 200 |
| TC17 | GET /admin/reports/ratings | status=approved | 200 |
| TC18 | GET /admin/reports/ratings | status=rejected | 200 |
| TC19 | GET /admin/reports/ratings | Kết hợp filters | 200 |
| TC20 | GET /admin/reports/ratings | status sai | 422 |
| TC21 | GET /admin/reports/ratings | from sai định dạng | 422 |
| TC22 | GET /admin/reports/ratings | User thường | 403 |
| TC23 | GET /admin/reports/ratings | Không có token | 401 |
| TC24 | GET /admin/reports/users | Không filter | 200 |
| TC25 | GET /admin/reports/users | year=2026 | 200 |
| TC26 | GET /admin/reports/users | year quá khứ | 200 |
| TC27 | GET /admin/reports/users | year không phải số | 422 |
| TC28 | GET /admin/reports/users | year=1900 | 422/200 |
| TC29 | GET /admin/reports/users | User thường | 403 |
| TC30 | GET /admin/reports/users | Không có token | 401 |
| TC31 | GET /admin/reports/points | Không filter | 200 |
| TC32 | GET /admin/reports/points | from + to | 200 |
| TC33 | GET /admin/reports/points | type=purchase | 200 |
| TC34 | GET /admin/reports/points | type=spend | 200 |
| TC35 | GET /admin/reports/points | type=bonus | 200 |
| TC36 | GET /admin/reports/points | type=refund | 200 |
| TC37 | GET /admin/reports/points | Kết hợp filters | 200 |
| TC38 | GET /admin/reports/points | type sai | 422 |
| TC39 | GET /admin/reports/points | from sai định dạng | 422 |
| TC40 | GET /admin/reports/points | User thường | 403 |
| TC41 | GET /admin/reports/points | Không có token | 401 |
