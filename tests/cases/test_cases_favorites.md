# Test Cases — FAVORITES (Yêu thích)

> Base URL: `http://localhost:8000/api/v1`
> 🔐 User token cần thiết cho tất cả endpoints

---

## 1. POST /user/favorites — Thêm vào yêu thích

### ✅ TC01 — Thêm thành công
```json
{ "location_id": 1 }
```
- Expected: `200 OK` hoặc `201 Created`
- Verify: `favorites` có record mới, `locations.favorite_count` tăng 1

### ❌ TC02 — Thêm trùng (đã có trong favorites)
```json
{ "location_id": 1 }
```
- Expected: `409 Conflict` hoặc `422 Unprocessable`

### ❌ TC03 — Thiếu `location_id`
```json
{}
```
- Expected: `422 Unprocessable`

### ❌ TC03b — `location_id` không phải số
```json
{ "location_id": "abc" }
```
- Expected: `422 Unprocessable`

### ❌ TC04 — `location_id` không tồn tại
```json
{ "location_id": 99999 }
```
- Expected: `422 Unprocessable` hoặc `404 Not Found`

### ❌ TC05 — Không có token
```json
{ "location_id": 1 }
```
- Expected: `401 Unauthorized`

---

## 2. GET /user/favorites — Danh sách yêu thích

### ✅ TC06 — Lấy danh sách thành công
```http
GET /api/v1/user/favorites
```
- Expected: `200 OK`, array locations kèm thông tin `categories`
- Verify: response item có field `location` và `category`

### ✅ TC07 — Phân trang `page` và `per_page`
```http
GET /api/v1/user/favorites?page=1&per_page=5
```
- Expected: `200 OK`, `data` có tối đa 5 phần tử

### ✅ TC08 — Danh sách rỗng (user chưa lưu gì)
```http
GET /api/v1/user/favorites
```
- Expected: `200 OK`, `data = []`

### ❌ TC09 — Không có token
```http
GET /api/v1/user/favorites
```
- Expected: `401 Unauthorized`

---

## 3. DELETE /user/favorites/{location_id} — Xóa khỏi yêu thích

### ✅ TC10 — Xóa thành công
```http
DELETE /api/v1/user/favorites/{location_id}
```
- Expected: `200 OK` hoặc `204 No Content`
- Verify: record bị xóa khỏi `favorites`, `locations.favorite_count` giảm 1

### ❌ TC11 — Xóa location không có trong favorites (ID không tồn tại)
```http
DELETE /api/v1/user/favorites/99999
```
- Expected: `404 Not Found` hoặc `422 Unprocessable`

### ❌ TC11b — Xóa location tồn tại trong DB nhưng chưa lưu vào favorites
```http
DELETE /api/v1/user/favorites/{location_id_chua_luu}
```
- Expected: `404 Not Found` hoặc `422 Unprocessable`

### ❌ TC12 — Xóa của người khác (location_id user khác đã lưu)
```http
DELETE /api/v1/user/favorites/{location_id}
```
- Expected: `403 Forbidden` hoặc `404 Not Found`

### ❌ TC13 — Không có token
```http
DELETE /api/v1/user/favorites/{location_id}
```
- Expected: `401 Unauthorized`

---

## Tổng kết

| TC | API | Trường hợp | Expected |
|----|-----|-----------|----------|
| TC01 | POST /user/favorites | Thêm thành công | 200/201 |
| TC02 | POST /user/favorites | Thêm trùng | 409/422 |
| TC03 | POST /user/favorites | Thiếu location_id | 422 |
| TC04 | POST /user/favorites | location_id không tồn tại | 404/422 |
| TC05 | POST /user/favorites | Không có token | 401 |
| TC06 | GET /user/favorites | Lấy danh sách | 200 |
| TC07 | GET /user/favorites | Phân trang | 200 |
| TC08 | GET /user/favorites | Danh sách rỗng | 200 |
| TC09 | GET /user/favorites | Không có token | 401 |
| TC10 | DELETE /user/favorites/{id} | Xóa thành công | 200/204 |
| TC11 | DELETE /user/favorites/{id} | Không có trong favorites | 404/422 |
| TC12 | DELETE /user/favorites/{id} | Xóa của người khác | 403/404 |
| TC13 | DELETE /user/favorites/{id} | Không có token | 401 |
