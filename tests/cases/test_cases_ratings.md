# Test Cases — RATINGS (Đánh giá)

> Base URL: `http://localhost:8000/api/v1`
> 🔐 User token cần thiết cho POST/PUT/DELETE ratings
> 🛡️ Admin token cần thiết cho GET/PATCH /admin/ratings

---

## 1. POST /ratings — Tạo đánh giá mới

### ✅ TC01 — Đủ field, không có ảnh
```json
{ "location_id": 1, "score": 5, "comment": "Rất ngon, sẽ quay lại!" }
```
- Expected: `201 Created`, `status = pending`

### ✅ TC02 — Chỉ field bắt buộc (không comment, không ảnh)
```json
{ "location_id": 1, "score": 3 }
```
- Expected: `201 Created`

### ✅ TC03 — Kèm ảnh (multipart/form-data, 1 file)
- body: `location_id=1`, `score=4`, `comment=OK`, `images[]=<file.jpg>`
- Expected: `201 Created`, `rating_images` có 1 record

### ✅ TC04 — Kèm ảnh tối đa (5 files)
- body: `location_id=1`, `score=4`, `images[]=<5 files>`
- Expected: `201 Created`, `rating_images` có 5 records

### ❌ TC05 — Thiếu `location_id`
```json
{ "score": 4, "comment": "OK" }
```
- Expected: `422 Unprocessable`, lỗi `location_id required`

### ❌ TC06 — Thiếu `score`
```json
{ "location_id": 1, "comment": "OK" }
```
- Expected: `422 Unprocessable`, lỗi `score required`

### ❌ TC07 — `score` ngoài khoảng 1-5
```json
{ "location_id": 1, "score": 6 }
```
- Expected: `422 Unprocessable`, lỗi `score phải từ 1 đến 5`

### ❌ TC08 — `location_id` không tồn tại
```json
{ "location_id": 99999, "score": 4 }
```
- Expected: `422 Unprocessable`, lỗi foreign key

### ❌ TC09 — User đánh giá trùng địa điểm đã đánh giá
```json
{ "location_id": 1, "score": 5, "comment": "Lần 2" }
```
- Expected: `422 Unprocessable`, lỗi `đã đánh giá địa điểm này`

### ❌ TC10 — Kèm quá 5 ảnh
- body: `location_id=1`, `score=4`, `images[]=<6 files>`
- Expected: `422 Unprocessable`, lỗi `tối đa 5 ảnh`

### ❌ TC11 — Không có token
```json
{ "location_id": 1, "score": 4 }
```
- Expected: `401 Unauthorized`

---

## 2. PUT /ratings/{id} — Sửa đánh giá

### ✅ TC12 — Sửa `score` và `comment`
```json
{ "score": 4, "comment": "Cập nhật lại nhận xét" }
```
- Expected: `200 OK`, dữ liệu được cập nhật

### ✅ TC13 — Chỉ sửa `score`
```json
{ "score": 2 }
```
- Expected: `200 OK`

### ❌ TC14 — Sửa đánh giá của người khác
- Expected: `403 Forbidden`

### ❌ TC15 — Sửa đánh giá đã được duyệt (`approved`)
- Expected: `422 Unprocessable`, lỗi `không thể sửa bài đã duyệt`

### ❌ TC16 — `score` ngoài khoảng 1-5
```json
{ "score": 0 }
```
- Expected: `422 Unprocessable`

### ❌ TC17 — ID không tồn tại
```http
PUT /api/v1/ratings/99999
```
- Expected: `404 Not Found`

### ❌ TC18 — Không có token
- Expected: `401 Unauthorized`

---

## 3. DELETE /ratings/{id} — Xóa đánh giá

### ✅ TC19 — Xóa đánh giá của chính mình (status pending)
- Expected: `200 OK` hoặc `204 No Content`
- Verify: `ratings` xóa record, `rating_images` cascade xóa, `locations.review_count` không đổi (chưa approved)

### ❌ TC20 — Xóa đánh giá của người khác
- Expected: `403 Forbidden`

### ❌ TC21 — Xóa đánh giá đã được duyệt (`approved`)
- Expected: `422 Unprocessable`, lỗi `không thể xóa bài đã duyệt`

### ❌ TC22 — ID không tồn tại
```http
DELETE /api/v1/ratings/99999
```
- Expected: `404 Not Found`

### ❌ TC23 — Không có token
- Expected: `401 Unauthorized`

---

## 4. POST /ratings/{id}/helpful — Đánh dấu hữu ích

> **Lưu ý:** Backend implement one-way helpful (không toggle). Gọi lần 2 trả `409 Conflict`.

### ✅ TC24 — Đánh dấu hữu ích thành công
- Expected: `200 OK`, `helpful_count` tăng 1
- Note: Nếu user đã mark trước đó, backend trả `409` (one-way, không unmark)

### ✅ TC25 — Gọi lần 2 (đã mark rồi)
- Expected: `200 OK` (nếu toggle) hoặc `409 Conflict` (nếu one-way)

### ❌ TC26 — ID không tồn tại
```http
POST /api/v1/ratings/99999/helpful
```
- Expected: `404 Not Found`

### ❌ TC27 — Không có token
- Expected: `401 Unauthorized`

---

## 5. GET /admin/ratings — Danh sách đánh giá (Admin)

### ✅ TC28 — Lấy tất cả không filter
```http
GET /api/v1/admin/ratings
```
- Expected: `200 OK`, array ratings kèm `user`, `location`, `rating_images`

### ✅ TC29 — Filter `status=pending`
```http
GET /api/v1/admin/ratings?status=pending
```
- Expected: `200 OK`, tất cả kết quả có `status = pending`

### ✅ TC30 — Filter `status=approved`
```http
GET /api/v1/admin/ratings?status=approved
```
- Expected: `200 OK`, tất cả kết quả có `status = approved`

### ✅ TC31 — Filter `location_id`
```http
GET /api/v1/admin/ratings?location_id=1
```
- Expected: `200 OK`, tất cả kết quả có `location_id = 1`

### ✅ TC32 — Phân trang
```http
GET /api/v1/admin/ratings?page=1&per_page=5
```
- Expected: `200 OK`, `data` có tối đa 5 phần tử

### ❌ TC33 — `status` sai giá trị
```http
GET /api/v1/admin/ratings?status=unknown
```
- Expected: `422 Unprocessable`

### ❌ TC34 — Không có token
- Expected: `401 Unauthorized`

### ❌ TC35 — Token user thường
- Expected: `403 Forbidden`

---

## 6. PATCH /admin/ratings/{id}/approve — Duyệt đánh giá

### ✅ TC36 — Duyệt đánh giá `pending` thành công
- Expected: `200 OK`
- Verify:
  - `ratings.status = approved`, `approved_by`, `approved_at` được set
  - `locations.avg_rating` và `review_count` được cập nhật
  - `users.point_balance` bị trừ (`point_cost`)
  - `point_transactions` có 1 record mới type=`spend`
  - `notifications` có 1 record mới type=`rating_approved`

### ❌ TC37 — Duyệt đánh giá đã `approved`
- Expected: `422 Unprocessable`, lỗi `đã được duyệt rồi`

### ❌ TC38 — Duyệt đánh giá đã `rejected`
- Expected: `422 Unprocessable`, lỗi `đã bị từ chối`

### ❌ TC39 — ID không tồn tại
```http
PATCH /api/v1/admin/ratings/99999/approve
```
- Expected: `404 Not Found`

### ❌ TC40 — Không có token
- Expected: `401 Unauthorized`

### ❌ TC41 — Token user thường
- Expected: `403 Forbidden`

---

## 7. PATCH /admin/ratings/{id}/reject — Từ chối đánh giá

### ✅ TC42 — Từ chối đánh giá `pending` thành công
```json
{ "rejected_reason": "Nội dung không phù hợp" }
```
- Expected: `200 OK`
- Verify:
  - `ratings.status = rejected`, `rejected_reason` được lưu
  - `notifications` có 1 record mới type=`rating_rejected`
  - `users.point_balance` KHÔNG thay đổi

### ❌ TC43 — Thiếu `rejected_reason`
```json
{}
```
- Expected: `422 Unprocessable`, lỗi `rejected_reason required`

### ❌ TC44 — Từ chối đánh giá đã `approved`
- Expected: `422 Unprocessable`, lỗi `không thể từ chối bài đã duyệt`

### ❌ TC45 — ID không tồn tại
```http
PATCH /api/v1/admin/ratings/99999/reject
```
- Expected: `404 Not Found`

### ❌ TC46 — Không có token
- Expected: `401 Unauthorized`

### ❌ TC47 — Token user thường
- Expected: `403 Forbidden`

---

## Tổng kết

| TC | API | Trường hợp | Expected |
|----|-----|-----------|----------|
| TC01 | POST /ratings | Đủ field, không ảnh | 201 |
| TC02 | POST /ratings | Chỉ field bắt buộc | 201 |
| TC03 | POST /ratings | Kèm 1 ảnh | 201 |
| TC04 | POST /ratings | Kèm 5 ảnh (max) | 201 |
| TC05 | POST /ratings | Thiếu location_id | 422 |
| TC06 | POST /ratings | Thiếu score | 422 |
| TC07 | POST /ratings | score ngoài 1-5 | 422 |
| TC08 | POST /ratings | location_id không tồn tại | 422 |
| TC09 | POST /ratings | Đánh giá trùng | 422 |
| TC10 | POST /ratings | Quá 5 ảnh | 422 |
| TC11 | POST /ratings | Không có token | 401 |
| TC12 | PUT /ratings/{id} | Sửa score & comment | 200 |
| TC13 | PUT /ratings/{id} | Chỉ sửa score | 200 |
| TC14 | PUT /ratings/{id} | Sửa của người khác | 403 |
| TC15 | PUT /ratings/{id} | Bài đã approved | 422 |
| TC16 | PUT /ratings/{id} | score ngoài 1-5 | 422 |
| TC17 | PUT /ratings/{id} | ID không tồn tại | 404 |
| TC18 | PUT /ratings/{id} | Không có token | 401 |
| TC19 | DELETE /ratings/{id} | Xóa thành công | 200/204 |
| TC20 | DELETE /ratings/{id} | Xóa của người khác | 403 |
| TC21 | DELETE /ratings/{id} | Bài đã approved | 422 |
| TC22 | DELETE /ratings/{id} | ID không tồn tại | 404 |
| TC23 | DELETE /ratings/{id} | Không có token | 401 |
| TC24 | POST /ratings/{id}/helpful | Đánh dấu hữu ích | 200 |
| TC25 | POST /ratings/{id}/helpful | Toggle bỏ đánh dấu | 200 |
| TC26 | POST /ratings/{id}/helpful | ID không tồn tại | 404 |
| TC27 | POST /ratings/{id}/helpful | Không có token | 401 |
| TC28 | GET /admin/ratings | Lấy tất cả | 200 |
| TC29 | GET /admin/ratings | Filter pending | 200 |
| TC30 | GET /admin/ratings | Filter approved | 200 |
| TC31 | GET /admin/ratings | Filter location_id | 200 |
| TC32 | GET /admin/ratings | Phân trang | 200 |
| TC33 | GET /admin/ratings | status sai giá trị | 422 |
| TC34 | GET /admin/ratings | Không có token | 401 |
| TC35 | GET /admin/ratings | Token user thường | 403 |
| TC36 | PATCH /admin/ratings/{id}/approve | Duyệt thành công | 200 |
| TC37 | PATCH /admin/ratings/{id}/approve | Đã approved | 422 |
| TC38 | PATCH /admin/ratings/{id}/approve | Đã rejected | 422 |
| TC39 | PATCH /admin/ratings/{id}/approve | ID không tồn tại | 404 |
| TC40 | PATCH /admin/ratings/{id}/approve | Không có token | 401 |
| TC41 | PATCH /admin/ratings/{id}/approve | Token user thường | 403 |
| TC42 | PATCH /admin/ratings/{id}/reject | Từ chối thành công | 200 |
| TC43 | PATCH /admin/ratings/{id}/reject | Thiếu rejected_reason | 422 |
| TC44 | PATCH /admin/ratings/{id}/reject | Bài đã approved | 422 |
| TC45 | PATCH /admin/ratings/{id}/reject | ID không tồn tại | 404 |
| TC46 | PATCH /admin/ratings/{id}/reject | Không có token | 401 |
| TC47 | PATCH /admin/ratings/{id}/reject | Token user thường | 403 |
