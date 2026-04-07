# Test Cases — TOUR SCHEDULES (Lịch khởi hành)

> Base URL: `http://localhost:8000/api/v1`
> 🛡️ Admin token bắt buộc cho tất cả endpoints

---

## 1. GET /admin/tour-schedules — Danh sách lịch

### ✅ TC01 — Lấy tất cả thành công
- Expected: `200 OK`
- Verify: mỗi item có `id`, `tour_id`, `start_date`, `end_date`, `status`

### ✅ TC02 — Filter `tour_id`
- Expected: `200 OK`
- Verify: tất cả item có `tour_id` đúng

### ✅ TC03 — Filter `status=available`
- Expected: `200 OK`

### ✅ TC04 — Filter `status=full`
- Expected: `200 OK`

### ✅ TC05 — Filter `status=cancelled`
- Expected: `200 OK`

### ✅ TC06 — Filter `from` và `to` (khoảng ngày)
- Expected: `200 OK`

### ✅ TC07 — Phân trang `per_page=5`
- Expected: `200 OK`, tối đa 5 items

### ❌ TC08 — `status` sai giá trị
- Expected: `422 Unprocessable`

### ❌ TC09 — `from` sai định dạng ngày
- Expected: `200 OK` hoặc `422 Unprocessable`
- Note: backend có thể không validate format ngày filter

### ❌ TC10 — User thường không được truy cập
- Expected: `403 Forbidden`

### ❌ TC11 — Không có token
- Expected: `401 Unauthorized`

---

## 2. GET /admin/tour-schedules/{id} — Chi tiết lịch

### ✅ TC12 — Lấy chi tiết thành công
- Expected: `200 OK`
- Verify: có `id`, `tour_id`, `start_date`, `end_date`, `max_people`, `status`

### ❌ TC13 — ID không tồn tại
- Expected: `404 Not Found` hoặc `422`

### ❌ TC14 — User thường không được truy cập
- Expected: `403 Forbidden`

### ❌ TC15 — Không có token
- Expected: `401 Unauthorized`

---

## 3. POST /admin/tours/{id}/schedules — Thêm lịch khởi hành

### ✅ TC16 — Tạo lịch thành công với đầy đủ fields
```json
{
  "start_date": "2026-07-01",
  "end_date": "2026-07-02",
  "max_people": 20,
  "price_adult": 600000,
  "price_child": 400000,
  "price_infant": 0,
  "status": "available"
}
```
- Expected: `200 OK` hoặc `201 Created`

### ✅ TC17 — Tạo lịch chỉ với fields bắt buộc
```json
{ "start_date": "2026-08-01", "end_date": "2026-08-02", "max_people": 10, "price_adult": 500000 }
```
- Expected: `200 OK` hoặc `201 Created`
- Note: backend bắt buộc `price_adult`

### ❌ TC18 — Thiếu `start_date`
- Expected: `422 Unprocessable`

### ❌ TC19 — Thiếu `end_date`
- Expected: `422 Unprocessable`

### ❌ TC20 — Thiếu `max_people`
- Expected: `422 Unprocessable`

### ❌ TC21 — `end_date` trước `start_date`
- Expected: `422 Unprocessable`

### ❌ TC22 — `start_date` trùng với lịch đã có (unique constraint)
- Expected: `422 Unprocessable` hoặc `409 Conflict`

### ❌ TC23 — `status` sai giá trị
- Expected: `422 Unprocessable`

### ❌ TC24 — Tour ID không tồn tại
- Expected: `404 Not Found` hoặc `422`

### ❌ TC25 — User thường không được tạo
- Expected: `403 Forbidden`

### ❌ TC26 — Không có token
- Expected: `401 Unauthorized`

---

## 4. PUT /admin/tour-schedules/{id} — Cập nhật lịch

### ✅ TC27 — Cập nhật `max_people`
- Expected: `200 OK`

### ✅ TC28 — Cập nhật `price_adult`
- Expected: `200 OK`

### ✅ TC29 — Cập nhật `end_date`
- Expected: `200 OK`

### ❌ TC30 — ID không tồn tại
- Expected: `404 Not Found` hoặc `422`

### ❌ TC31 — `end_date` trước `start_date`
- Expected: `200 OK` hoặc `422 Unprocessable`
- Note: backend có thể không validate end_date > start_date khi PUT

### ❌ TC32 — User thường không được cập nhật
- Expected: `403 Forbidden`

### ❌ TC33 — Không có token
- Expected: `401 Unauthorized`

---

## 5. DELETE /admin/tour-schedules/{id} — Xóa lịch

### ✅ TC34 — Xóa lịch không có booking thành công
- Expected: `200 OK` hoặc `204 No Content`

### ❌ TC35 — ID không tồn tại
- Expected: `404 Not Found` hoặc `422`

### ❌ TC36 — User thường không được xóa
- Expected: `403 Forbidden`

### ❌ TC37 — Không có token
- Expected: `401 Unauthorized`

---

## 6. PATCH /admin/tour-schedules/{id}/status — Đổi trạng thái

### ✅ TC38 — Đổi sang `full`
- Expected: `200 OK`

### ✅ TC39 — Đổi sang `cancelled`
- Expected: `200 OK`

### ✅ TC40 — Đổi sang `available`
- Expected: `200 OK`

### ❌ TC41 — `status` sai giá trị
- Expected: `422 Unprocessable`

### ❌ TC42 — Thiếu `status`
- Expected: `422 Unprocessable`

### ❌ TC43 — ID không tồn tại
- Expected: `404 Not Found` hoặc `422`

### ❌ TC44 — User thường không được đổi status
- Expected: `403 Forbidden`

### ❌ TC45 — Không có token
- Expected: `401 Unauthorized`

---

## Tổng kết

| TC | API | Trường hợp | Expected |
|----|-----|-----------|----------|
| TC01 | GET /admin/tour-schedules | Lấy tất cả | 200 |
| TC02 | GET /admin/tour-schedules | Filter tour_id | 200 |
| TC03 | GET /admin/tour-schedules | Filter available | 200 |
| TC04 | GET /admin/tour-schedules | Filter full | 200 |
| TC05 | GET /admin/tour-schedules | Filter cancelled | 200 |
| TC06 | GET /admin/tour-schedules | Filter from/to | 200 |
| TC07 | GET /admin/tour-schedules | Phân trang | 200 |
| TC08 | GET /admin/tour-schedules | status sai | 422 |
| TC09 | GET /admin/tour-schedules | from sai định dạng | 422 |
| TC10 | GET /admin/tour-schedules | User thường | 403 |
| TC11 | GET /admin/tour-schedules | Không có token | 401 |
| TC12 | GET /admin/tour-schedules/{id} | Chi tiết | 200 |
| TC13 | GET /admin/tour-schedules/{id} | ID không tồn tại | 404/422 |
| TC14 | GET /admin/tour-schedules/{id} | User thường | 403 |
| TC15 | GET /admin/tour-schedules/{id} | Không có token | 401 |
| TC16 | POST /admin/tours/{id}/schedules | Tạo đầy đủ | 200/201 |
| TC17 | POST /admin/tours/{id}/schedules | Chỉ bắt buộc | 200/201 |
| TC18 | POST /admin/tours/{id}/schedules | Thiếu start_date | 422 |
| TC19 | POST /admin/tours/{id}/schedules | Thiếu end_date | 422 |
| TC20 | POST /admin/tours/{id}/schedules | Thiếu max_people | 422 |
| TC21 | POST /admin/tours/{id}/schedules | end_date < start_date | 422 |
| TC22 | POST /admin/tours/{id}/schedules | start_date trùng | 422/409 |
| TC23 | POST /admin/tours/{id}/schedules | status sai | 422 |
| TC24 | POST /admin/tours/{id}/schedules | Tour không tồn tại | 404/422 |
| TC25 | POST /admin/tours/{id}/schedules | User thường | 403 |
| TC26 | POST /admin/tours/{id}/schedules | Không có token | 401 |
| TC27 | PUT /admin/tour-schedules/{id} | Cập nhật max_people | 200 |
| TC28 | PUT /admin/tour-schedules/{id} | Cập nhật price_adult | 200 |
| TC29 | PUT /admin/tour-schedules/{id} | Cập nhật end_date | 200 |
| TC30 | PUT /admin/tour-schedules/{id} | ID không tồn tại | 404/422 |
| TC31 | PUT /admin/tour-schedules/{id} | end_date < start_date | 422 |
| TC32 | PUT /admin/tour-schedules/{id} | User thường | 403 |
| TC33 | PUT /admin/tour-schedules/{id} | Không có token | 401 |
| TC34 | DELETE /admin/tour-schedules/{id} | Xóa thành công | 200/204 |
| TC35 | DELETE /admin/tour-schedules/{id} | ID không tồn tại | 404/422 |
| TC36 | DELETE /admin/tour-schedules/{id} | User thường | 403 |
| TC37 | DELETE /admin/tour-schedules/{id} | Không có token | 401 |
| TC38 | PATCH .../status | full | 200 |
| TC39 | PATCH .../status | cancelled | 200 |
| TC40 | PATCH .../status | available | 200 |
| TC41 | PATCH .../status | status sai | 422 |
| TC42 | PATCH .../status | Thiếu status | 422 |
| TC43 | PATCH .../status | ID không tồn tại | 404/422 |
| TC44 | PATCH .../status | User thường | 403 |
| TC45 | PATCH .../status | Không có token | 401 |
