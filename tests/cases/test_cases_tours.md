# Test Cases — TOURS

> Base URL: `http://localhost:8000/api/v1`
> Admin token cần thiết cho các API 🛡️

---

## 1. GET /tours — Danh sách tour

### ✅ TC01 — Không filter
```http
GET /api/v1/tours
```
- Expected: `200 OK`, trả về paginated list tours

### ✅ TC02 — Filter theo `tour_category_id`
```http
GET /api/v1/tours?tour_category_id=1
```
- Expected: `200 OK`, chỉ trả về tours thuộc category đó

### ✅ TC03 — Filter theo `price_min` và `price_max`
```http
GET /api/v1/tours?price_min=100000&price_max=500000
```
- Expected: `200 OK`, chỉ trả về tours trong khoảng giá

### ✅ TC04 — Filter theo `available_from` và `available_to`
```http
GET /api/v1/tours?available_from=2026-01-01&available_to=2026-12-31
```
- Expected: `200 OK`

### ✅ TC05 — Sort theo `price_adult` tăng dần
```http
GET /api/v1/tours?sort=price_adult&order=asc
```
- Expected: `200 OK`, tours sắp xếp theo giá tăng dần

### ✅ TC06 — Kết hợp filter + sort + paginate
```http
GET /api/v1/tours?tour_category_id=1&sort=price_adult&order=asc&page=1&per_page=12
```
- Expected: `200 OK`

### ❌ TC07 — `tour_category_id` không tồn tại
```http
GET /api/v1/tours?tour_category_id=99999
```
- Expected: `200 OK` trả về rỗng, hoặc `422`

### ❌ TC08 — `price_min` không phải số
```http
GET /api/v1/tours?price_min=abc
```
- Expected: `200 OK` hoặc `422`

---

## 2. GET /tours/featured — Tour nổi bật

### ✅ TC09 — Lấy danh sách nổi bật
```http
GET /api/v1/tours/featured
```
- Expected: `200 OK`, chỉ trả về tours có `is_featured=true`

### ✅ TC10 — Có limit
```http
GET /api/v1/tours/featured?limit=4
```
- Expected: `200 OK`, trả về tối đa 4 tours

---

## 3. GET /tours/hot — Tour hot

### ✅ TC11 — Lấy danh sách hot
```http
GET /api/v1/tours/hot
```
- Expected: `200 OK`, chỉ trả về tours có `is_hot=true`

### ✅ TC12 — Có limit
```http
GET /api/v1/tours/hot?limit=4
```
- Expected: `200 OK`

---

## 4. GET /tours/{slug} — Chi tiết tour

### ✅ TC13 — Slug hợp lệ
```http
GET /api/v1/tours/tour-tham-quan-da-nang
```
- Expected: `200 OK`, trả về đầy đủ thông tin tour kèm schedules

### ❌ TC14 — Slug không tồn tại
```http
GET /api/v1/tours/slug-khong-ton-tai-99999
```
- Expected: `404 Not Found`

---

## 5. GET /tours/{id}/schedules — Lịch khởi hành

### ✅ TC15 — ID hợp lệ
```http
GET /api/v1/tours/{id}/schedules
```
- Expected: `200 OK`, trả về list schedules có status=available

### ✅ TC16 — Filter theo khoảng ngày
```http
GET /api/v1/tours/{id}/schedules?from=2026-01-01&to=2026-12-31
```
- Expected: `200 OK`

### ❌ TC17 — ID không tồn tại
```http
GET /api/v1/tours/99999/schedules
```
- Expected: `404 Not Found` hoặc `422`

---

## 6. GET /tours/{id}/ratings — Đánh giá của tour

### ✅ TC18 — ID hợp lệ
```http
GET /api/v1/tours/{id}/ratings
```
- Expected: `200 OK`, trả về paginated list ratings approved

### ✅ TC19 — Có paginate
```http
GET /api/v1/tours/{id}/ratings?page=1&per_page=5
```
- Expected: `200 OK`

### ❌ TC20 — ID không tồn tại
```http
GET /api/v1/tours/99999/ratings
```
- Expected: `404 Not Found` hoặc `422`

---

## 7. GET /tours/{id}/rating-stats — Phân bố số sao

### ✅ TC21 — ID hợp lệ
```http
GET /api/v1/tours/{id}/rating-stats
```
- Expected: `200 OK`, trả về `{1: n, 2: n, 3: n, 4: n, 5: n}`

### ❌ TC22 — ID không tồn tại
```http
GET /api/v1/tours/99999/rating-stats
```
- Expected: `404 Not Found` hoặc `422`

---

## 8. POST /tours/{id}/check-availability — Kiểm tra còn chỗ

### ✅ TC23 — Còn chỗ
```json
{
  "schedule_id": 1,
  "quantity_adult": 2,
  "quantity_child": 1,
  "quantity_infant": 0
}
```
- Expected: `200 OK`, trả về `available: true/false`

### ❌ TC24 — Thiếu `schedule_id`
```json
{ "quantity_adult": 2 }
```
- Expected: `422 Unprocessable`

### ❌ TC25 — `schedule_id` không tồn tại
```json
{ "schedule_id": 99999, "quantity_adult": 2 }
```
- Expected: `404 Not Found` hoặc `422`

### ❌ TC26 — ID tour không tồn tại
```http
POST /api/v1/tours/99999/check-availability
```
- Expected: `404 Not Found` hoặc `422`

---

## 9. POST /admin/tours — Tạo tour mới

### ✅ TC27 — Đủ tất cả field hợp lệ
```json
{
  "name": "Tour Tham Quan Đà Nẵng",
  "slug": "tour-tham-quan-da-nang",
  "tour_category_id": 1,
  "description": "Mô tả chi tiết",
  "short_desc": "Mô tả ngắn",
  "price_adult": 500000,
  "price_child": 300000,
  "price_infant": 0,
  "duration": "1 ngày",
  "start_time": "07:00",
  "meeting_point": "Số 1 Trần Phú",
  "max_people": 20,
  "min_people": 2,
  "status": "active",
  "is_featured": false,
  "is_hot": false
}
```
- Expected: `201 Created`

### ✅ TC28 — Chỉ field bắt buộc
```json
{
  "name": "Tour Test TC28",
  "tour_category_id": 1,
  "price_adult": 300000,
  "status": "active"
}
```
- Expected: `201 Created`

### ❌ TC29 — Thiếu `name`
```json
{ "tour_category_id": 1, "price_adult": 300000, "status": "active" }
```
- Expected: `422 Unprocessable`

### ❌ TC30 — Thiếu `tour_category_id`
```json
{ "name": "Test", "price_adult": 300000, "status": "active" }
```
- Expected: `422 Unprocessable`

### ❌ TC31 — Thiếu `price_adult`
```json
{ "name": "Test", "tour_category_id": 1, "status": "active" }
```
- Expected: `422 Unprocessable`

### ❌ TC32 — `tour_category_id` không tồn tại
```json
{ "name": "Test", "tour_category_id": 99999, "price_adult": 300000, "status": "active" }
```
- Expected: `422 Unprocessable`

### ❌ TC33 — `status` sai giá trị
```json
{ "name": "Test", "tour_category_id": 1, "price_adult": 300000, "status": "unknown" }
```
- Expected: `422 Unprocessable`

### ❌ TC34 — `slug` trùng
- Expected: `422 Unprocessable`

### ❌ TC35 — Không có token
- Expected: `401 Unauthorized`

### ❌ TC36 — Token user thường
- Expected: `403 Forbidden`

---

## 10. PUT /admin/tours/{id} — Cập nhật tour

### ✅ TC37 — Cập nhật nhiều field
```json
{ "name": "Tour Updated", "description": "Mô tả mới", "status": "active" }
```
- Expected: `200 OK`

### ✅ TC38 — Cập nhật 1 field
```json
{ "status": "inactive" }
```
- Expected: `200 OK`

### ✅ TC39 — Cập nhật slug của chính nó (không báo trùng)
- Expected: `200 OK`

### ❌ TC40 — ID không tồn tại
```http
PUT /api/v1/admin/tours/99999
```
- Expected: `404 Not Found` hoặc `422`

### ❌ TC41 — `slug` trùng với tour khác
- Expected: `422 Unprocessable`

### ❌ TC42 — Không có token
- Expected: `401 Unauthorized`

### ❌ TC43 — Token user thường
- Expected: `403 Forbidden`

---

## 11. DELETE /admin/tours/{id} — Xóa tour

### ✅ TC44 — Xóa thành công
- Expected: `200 OK` hoặc `204 No Content`

### ❌ TC45 — ID không tồn tại
- Expected: `404 Not Found` hoặc `422`

### ❌ TC46 — Không có token
- Expected: `401 Unauthorized`

---

## 12. PATCH /admin/tours/{id}/status — Đổi trạng thái

### ✅ TC47 — Đổi sang `unavailable`
```json
{ "status": "unavailable" }
```
- Expected: `200 OK`

### ✅ TC48 — Đổi sang `available`
```json
{ "status": "available" }
```
- Expected: `200 OK`

### ✅ TC49 — Đổi sang `pending`
```json
{ "status": "pending" }
```
- Expected: `200 OK`

### ❌ TC50 — `status` sai giá trị
```json
{ "status": "unknown" }
```
- Expected: `422 Unprocessable`

### ❌ TC51 — ID không tồn tại
- Expected: `404 Not Found` hoặc `422`

### ❌ TC52 — Không có token
- Expected: `401 Unauthorized`

---

## 13. PATCH /admin/tours/{id}/featured — Bật/tắt nổi bật

### ✅ TC53 — Bật nổi bật
```json
{ "is_featured": true }
```
- Expected: `200 OK`

### ✅ TC54 — Tắt nổi bật
```json
{ "is_featured": false }
```
- Expected: `200 OK`

### ❌ TC55 — `is_featured` sai kiểu
```json
{ "is_featured": "yes" }
```
- Expected: `422 Unprocessable`

### ❌ TC56 — ID không tồn tại
- Expected: `404 Not Found` hoặc `422`

### ❌ TC57 — Không có token
- Expected: `401 Unauthorized`

---

## 14. PATCH /admin/tours/{id}/hot — Bật/tắt tour hot

### ✅ TC58 — Bật hot
```json
{ "is_hot": true }
```
- Expected: `200 OK`

### ✅ TC59 — Tắt hot
```json
{ "is_hot": false }
```
- Expected: `200 OK`

### ❌ TC60 — `is_hot` sai kiểu
```json
{ "is_hot": "yes" }
```
- Expected: `422 Unprocessable`

### ❌ TC61 — ID không tồn tại
- Expected: `404 Not Found` hoặc `422`

### ❌ TC62 — Không có token
- Expected: `401 Unauthorized`

---

## 15. GET /admin/tours/export — Export Excel

### ✅ TC63 — Export thành công
```http
GET /api/v1/admin/tours/export
```
- Expected: `200 OK`, file Excel

### ✅ TC64 — Export với filter
```http
GET /api/v1/admin/tours/export?status=active&tour_category_id=1
```
- Expected: `200 OK`

### ❌ TC65 — Không có token
- Expected: `401 Unauthorized`

---

## Tổng kết

| TC | API | Trường hợp | Expected |
|----|-----|-----------|----------|
| TC01 | GET /tours | Không filter | 200 |
| TC02 | GET /tours | Filter tour_category_id | 200 |
| TC03 | GET /tours | Filter price_min/max | 200 |
| TC04 | GET /tours | Filter available_from/to | 200 |
| TC05 | GET /tours | Sort price_adult asc | 200 |
| TC06 | GET /tours | Kết hợp filter + sort + page | 200 |
| TC07 | GET /tours | tour_category_id không tồn tại | 200/422 |
| TC08 | GET /tours | price_min không phải số | 200/422 |
| TC09 | GET /tours/featured | Lấy danh sách nổi bật | 200 |
| TC10 | GET /tours/featured | Có limit | 200 |
| TC11 | GET /tours/hot | Lấy danh sách hot | 200 |
| TC12 | GET /tours/hot | Có limit | 200 |
| TC13 | GET /tours/{slug} | Slug hợp lệ | 200 |
| TC14 | GET /tours/{slug} | Slug không tồn tại | 404 |
| TC15 | GET /tours/{id}/schedules | ID hợp lệ | 200 |
| TC16 | GET /tours/{id}/schedules | Filter ngày | 200 |
| TC17 | GET /tours/{id}/schedules | ID không tồn tại | 404/422 |
| TC18 | GET /tours/{id}/ratings | ID hợp lệ | 200 |
| TC19 | GET /tours/{id}/ratings | Có paginate | 200 |
| TC20 | GET /tours/{id}/ratings | ID không tồn tại | 404/422 |
| TC21 | GET /tours/{id}/rating-stats | ID hợp lệ | 200 |
| TC22 | GET /tours/{id}/rating-stats | ID không tồn tại | 404/422 |
| TC23 | POST /tours/{id}/check-availability | Còn chỗ | 200 |
| TC24 | POST /tours/{id}/check-availability | Thiếu schedule_id | 422 |
| TC25 | POST /tours/{id}/check-availability | schedule_id không tồn tại | 404/422 |
| TC26 | POST /tours/{id}/check-availability | tour ID không tồn tại | 404/422 |
| TC27 | POST /admin/tours | Đủ field | 201 |
| TC28 | POST /admin/tours | Chỉ field bắt buộc | 201 |
| TC29 | POST /admin/tours | Thiếu name | 422 |
| TC30 | POST /admin/tours | Thiếu tour_category_id | 422 |
| TC31 | POST /admin/tours | Thiếu price_adult | 422 |
| TC32 | POST /admin/tours | tour_category_id không tồn tại | 422 |
| TC33 | POST /admin/tours | status sai giá trị | 422 |
| TC34 | POST /admin/tours | slug trùng | 422 |
| TC35 | POST /admin/tours | Không có token | 401 |
| TC36 | POST /admin/tours | Token user thường | 403 |
| TC37 | PUT /admin/tours/{id} | Cập nhật nhiều field | 200 |
| TC38 | PUT /admin/tours/{id} | Cập nhật 1 field | 200 |
| TC39 | PUT /admin/tours/{id} | Cập nhật slug chính nó | 200 |
| TC40 | PUT /admin/tours/{id} | ID không tồn tại | 404/422 |
| TC41 | PUT /admin/tours/{id} | slug trùng | 422 |
| TC42 | PUT /admin/tours/{id} | Không có token | 401 |
| TC43 | PUT /admin/tours/{id} | Token user thường | 403 |
| TC44 | DELETE /admin/tours/{id} | Xóa thành công | 200/204 |
| TC45 | DELETE /admin/tours/{id} | ID không tồn tại | 404/422 |
| TC46 | DELETE /admin/tours/{id} | Không có token | 401 |
| TC47 | PATCH /admin/tours/{id}/status | Đổi sang unavailable | 200 |
| TC48 | PATCH /admin/tours/{id}/status | Đổi sang available | 200 |
| TC49 | PATCH /admin/tours/{id}/status | Đổi sang pending | 200 |
| TC50 | PATCH /admin/tours/{id}/status | status sai giá trị | 422 |
| TC51 | PATCH /admin/tours/{id}/status | ID không tồn tại | 404/422 |
| TC52 | PATCH /admin/tours/{id}/status | Không có token | 401 |
| TC53 | PATCH /admin/tours/{id}/featured | Bật nổi bật | 200 |
| TC54 | PATCH /admin/tours/{id}/featured | Tắt nổi bật | 200 |
| TC55 | PATCH /admin/tours/{id}/featured | is_featured sai kiểu | 422 |
| TC56 | PATCH /admin/tours/{id}/featured | ID không tồn tại | 404/422 |
| TC57 | PATCH /admin/tours/{id}/featured | Không có token | 401 |
| TC58 | PATCH /admin/tours/{id}/hot | Bật hot | 200 |
| TC59 | PATCH /admin/tours/{id}/hot | Tắt hot | 200 |
| TC60 | PATCH /admin/tours/{id}/hot | is_hot sai kiểu | 422 |
| TC61 | PATCH /admin/tours/{id}/hot | ID không tồn tại | 404/422 |
| TC62 | PATCH /admin/tours/{id}/hot | Không có token | 401 |
| TC63 | GET /admin/tours/export | Export thành công | 200 |
| TC64 | GET /admin/tours/export | Export với filter | 200 |
| TC65 | GET /admin/tours/export | Không có token | 401 |
