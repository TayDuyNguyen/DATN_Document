# Test Cases — LOCATIONS

> Base URL: `http://localhost:8000/api/v1`
> Admin token cần thiết cho các API 🛡️

---

## 1. GET /locations — Danh sách địa điểm

### ✅ TC01 — Lấy danh sách không filter
```http
GET /api/v1/locations
```
- Expected: `200 OK`, trả về paginated list locations

### ✅ TC02 — Filter theo `category_id`
```http
GET /api/v1/locations?category_id=1
```
- Expected: `200 OK`, chỉ trả về locations thuộc category đó

### ✅ TC03 — Filter theo `district`
```http
GET /api/v1/locations?district=Hải Châu
```
- Expected: `200 OK`, chỉ trả về locations thuộc quận Hải Châu

### ✅ TC04 — Filter theo `price_level`
```http
GET /api/v1/locations?price_level=2
```
- Expected: `200 OK`, chỉ trả về locations có price_level=2

### ✅ TC05 — Sort theo `avg_rating` giảm dần
```http
GET /api/v1/locations?sort=avg_rating&order=desc
```
- Expected: `200 OK`, locations sắp xếp theo điểm đánh giá cao nhất

### ✅ TC06 — Kết hợp nhiều filter + sort + paginate
```http
GET /api/v1/locations?category_id=1&district=Hải Châu&price_level=2&sort=avg_rating&order=desc&page=1&per_page=12
```
- Expected: `200 OK`, kết quả đúng với tất cả filter

### ❌ TC07 — `category_id` không tồn tại
```http
GET /api/v1/locations?category_id=99999
```
- Expected: `200 OK` trả về array rỗng, hoặc `404/422`

### ❌ TC08 — `price_level` sai giá trị
```http
GET /api/v1/locations?price_level=99
```
- Expected: `200 OK` trả về rỗng, hoặc `422 Unprocessable`

---

## 2. GET /locations/featured — Địa điểm nổi bật

### ✅ TC09 — Lấy danh sách nổi bật
```http
GET /api/v1/locations/featured
```
- Expected: `200 OK`, chỉ trả về locations có `is_featured=true`

---

## 3. GET /locations/nearby — Địa điểm gần vị trí

### ✅ TC10 — Tọa độ hợp lệ
```http
GET /api/v1/locations/nearby?lat=16.0544&lng=108.2022&radius=5
```
- Expected: `200 OK`, trả về locations trong bán kính 5km

### ✅ TC11 — Không truyền `radius` (dùng default)
```http
GET /api/v1/locations/nearby?lat=16.0544&lng=108.2022
```
- Expected: `200 OK`, dùng radius mặc định

### ❌ TC12 — Thiếu `lat`
```http
GET /api/v1/locations/nearby?lng=108.2022
```
- Expected: `422 Unprocessable`

### ❌ TC13 — Thiếu `lng`
```http
GET /api/v1/locations/nearby?lat=16.0544
```
- Expected: `422 Unprocessable`

### ❌ TC14 — `lat`/`lng` không phải số
```http
GET /api/v1/locations/nearby?lat=abc&lng=xyz
```
- Expected: `422 Unprocessable`

---

## 4. GET /locations/{slug} — Chi tiết địa điểm

### ✅ TC15 — Slug hợp lệ
```http
GET /api/v1/locations/nha-hang-be-man
```
- Expected: `200 OK`, trả về đầy đủ thông tin địa điểm

### ❌ TC16 — Slug không tồn tại
```http
GET /api/v1/locations/slug-khong-ton-tai
```
- Expected: `404 Not Found`

---

## 5. GET /locations/{id}/ratings — Đánh giá của địa điểm

### ✅ TC17 — ID hợp lệ, có ratings
```http
GET /api/v1/locations/1/ratings
```
- Expected: `200 OK`, trả về paginated list ratings đã approved

### ✅ TC18 — ID hợp lệ, chưa có rating nào
```http
GET /api/v1/locations/{new_id}/ratings
```
- Expected: `200 OK`, trả về array rỗng

### ❌ TC19 — ID không tồn tại
```http
GET /api/v1/locations/99999/ratings
```
- Expected: `404 Not Found`

---

## 6. POST /locations/{id}/view — Ghi nhận lượt xem

### ✅ TC20 — Guest ghi nhận lượt xem (có session_id)
```json
{
  "session_id": "sess_abc123"
}
```
- Expected: `200 OK`, view_count tăng

### ✅ TC21 — User đã đăng nhập ghi nhận lượt xem
```json
{
  "session_id": "sess_abc123"
}
```
- Headers: `Authorization: Bearer {user_token}`
- Expected: `200 OK`, ghi nhận kèm user_id

### ❌ TC22 — ID location không tồn tại
```http
POST /api/v1/locations/99999/view
```
- Expected: `404 Not Found`

### ❌ TC23 — Thiếu `session_id`
```json
{}
```
- Expected: `422 Unprocessable` hoặc `200 OK` nếu backend optional

---

## 7. POST /admin/locations — Tạo địa điểm mới

### ✅ TC24 — Đủ tất cả field hợp lệ
```json
{
  "name": "Nhà hàng Bé Mặn",
  "category_id": 1,
  "subcategory_id": 1,
  "description": "Nhà hàng hải sản nổi tiếng",
  "short_description": "Hải sản tươi sống",
  "address": "123 Trần Phú",
  "district": "Hải Châu",
  "latitude": 16.0544,
  "longitude": 108.2022,
  "phone": "0236123456",
  "price_min": 100000,
  "price_max": 500000,
  "price_level": 2,
  "status": "active",
  "is_featured": false
}
```
- Expected: `201 Created`

### ✅ TC25 — Chỉ field bắt buộc
```json
{
  "name": "Quán Cà Phê Test",
  "category_id": 1,
  "address": "456 Lê Duẩn",
  "district": "Hải Châu",
  "status": "active"
}
```
- Expected: `201 Created`

### ❌ TC26 — Thiếu `name`
```json
{
  "category_id": 1,
  "address": "123 Trần Phú",
  "district": "Hải Châu",
  "status": "active"
}
```
- Expected: `422 Unprocessable`

### ❌ TC27 — Thiếu `category_id`
```json
{
  "name": "Test",
  "address": "123 Trần Phú",
  "district": "Hải Châu",
  "status": "active"
}
```
- Expected: `422 Unprocessable`

### ❌ TC28 — `category_id` không tồn tại
```json
{
  "name": "Test",
  "category_id": 99999,
  "address": "123 Trần Phú",
  "district": "Hải Châu",
  "status": "active"
}
```
- Expected: `422 Unprocessable`

### ❌ TC29 — `district` sai giá trị
```json
{
  "name": "Test",
  "category_id": 1,
  "address": "123 Trần Phú",
  "district": "Quận không tồn tại",
  "status": "active"
}
```
- Expected: `422 Unprocessable`

### ❌ TC30 — `price_level` sai giá trị (ngoài 1-4)
```json
{
  "name": "Test",
  "category_id": 1,
  "address": "123 Trần Phú",
  "district": "Hải Châu",
  "price_level": 99,
  "status": "active"
}
```
- Expected: `422 Unprocessable`

### ❌ TC31 — `slug` trùng
```json
{
  "name": "Test",
  "slug": "slug-da-ton-tai",
  "category_id": 1,
  "address": "123 Trần Phú",
  "district": "Hải Châu",
  "status": "active"
}
```
- Expected: `422 Unprocessable`

### ❌ TC32 — Không có token
- Expected: `401 Unauthorized`

### ❌ TC33 — Token user thường
- Expected: `403 Forbidden`

---

## 8. PUT /admin/locations/{id} — Cập nhật địa điểm

### ✅ TC34 — Cập nhật hợp lệ nhiều field
```json
{
  "name": "Nhà hàng Bé Mặn Updated",
  "description": "Mô tả mới",
  "status": "active"
}
```
- Expected: `200 OK`

### ✅ TC35 — Cập nhật 1 field
```json
{
  "status": "inactive"
}
```
- Expected: `200 OK`

### ❌ TC36 — ID không tồn tại
```http
PUT /api/v1/admin/locations/99999
```
- Expected: `404 Not Found`

### ❌ TC37 — `slug` trùng với location khác
```json
{
  "slug": "slug-cua-location-khac"
}
```
- Expected: `422 Unprocessable`

### ❌ TC38 — Không có token
- Expected: `401 Unauthorized`

---

## 9. DELETE /admin/locations/{id} — Xóa địa điểm

### ✅ TC39 — Xóa thành công
```http
DELETE /api/v1/admin/locations/{id}
```
- Expected: `200 OK` hoặc `204 No Content`

### ❌ TC40 — ID không tồn tại
```http
DELETE /api/v1/admin/locations/99999
```
- Expected: `404 Not Found`

### ❌ TC41 — Không có token
- Expected: `401 Unauthorized`

---

## 10. PATCH /admin/locations/{id}/status — Đổi trạng thái

### ✅ TC42 — Đổi sang `inactive`
```json
{
  "status": "inactive"
}
```
- Expected: `200 OK`

### ✅ TC43 — Đổi sang `active`
```json
{
  "status": "active"
}
```
- Expected: `200 OK`

### ❌ TC44 — `status` sai giá trị
```json
{
  "status": "unknown"
}
```
- Expected: `422 Unprocessable`

### ❌ TC45 — ID không tồn tại
```http
PATCH /api/v1/admin/locations/99999/status
```
- Expected: `404 Not Found`

### ❌ TC46 — Không có token
- Expected: `401 Unauthorized`

---

## 11. PATCH /admin/locations/{id}/featured — Bật/tắt nổi bật

### ✅ TC47 — Bật nổi bật
```json
{
  "is_featured": true
}
```
- Expected: `200 OK`

### ✅ TC48 — Tắt nổi bật
```json
{
  "is_featured": false
}
```
- Expected: `200 OK`

### ❌ TC49 — `is_featured` sai kiểu dữ liệu
```json
{
  "is_featured": "yes"
}
```
- Expected: `422 Unprocessable`

### ❌ TC50 — ID không tồn tại
```http
PATCH /api/v1/admin/locations/99999/featured
```
- Expected: `404 Not Found`

### ❌ TC51 — Không có token
- Expected: `401 Unauthorized`

---

## Tổng kết

| TC | API | Trường hợp | Expected |
|----|-----|-----------|----------|
| TC01 | GET /locations | Không filter | 200 |
| TC02 | GET /locations | Filter category_id | 200 |
| TC03 | GET /locations | Filter district | 200 |
| TC04 | GET /locations | Filter price_level | 200 |
| TC05 | GET /locations | Sort avg_rating desc | 200 |
| TC06 | GET /locations | Kết hợp filter + sort + page | 200 |
| TC07 | GET /locations | category_id không tồn tại | 200/404/422 |
| TC08 | GET /locations | price_level sai giá trị | 200/422 |
| TC09 | GET /locations/featured | Lấy danh sách nổi bật | 200 |
| TC10 | GET /locations/nearby | Tọa độ hợp lệ | 200 |
| TC11 | GET /locations/nearby | Không có radius | 200 |
| TC12 | GET /locations/nearby | Thiếu lat | 422 |
| TC13 | GET /locations/nearby | Thiếu lng | 422 |
| TC14 | GET /locations/nearby | lat/lng không phải số | 422 |
| TC15 | GET /locations/{slug} | Slug hợp lệ | 200 |
| TC16 | GET /locations/{slug} | Slug không tồn tại | 404 |
| TC17 | GET /locations/{id}/ratings | Có ratings | 200 |
| TC18 | GET /locations/{id}/ratings | Chưa có rating | 200 |
| TC19 | GET /locations/{id}/ratings | ID không tồn tại | 404 |
| TC20 | POST /locations/{id}/view | Guest có session_id | 200 |
| TC21 | POST /locations/{id}/view | User đã đăng nhập | 200 |
| TC22 | POST /locations/{id}/view | ID không tồn tại | 404 |
| TC23 | POST /locations/{id}/view | Thiếu session_id | 422/200 |
| TC24 | POST /admin/locations | Đủ field | 201 |
| TC25 | POST /admin/locations | Chỉ field bắt buộc | 201 |
| TC26 | POST /admin/locations | Thiếu name | 422 |
| TC27 | POST /admin/locations | Thiếu category_id | 422 |
| TC28 | POST /admin/locations | category_id không tồn tại | 422 |
| TC29 | POST /admin/locations | district sai giá trị | 422 |
| TC30 | POST /admin/locations | price_level sai giá trị | 422 |
| TC31 | POST /admin/locations | slug trùng | 422 |
| TC32 | POST /admin/locations | Không có token | 401 |
| TC33 | POST /admin/locations | Token user thường | 403 |
| TC34 | PUT /admin/locations/{id} | Cập nhật nhiều field | 200 |
| TC35 | PUT /admin/locations/{id} | Cập nhật 1 field | 200 |
| TC36 | PUT /admin/locations/{id} | ID không tồn tại | 404 |
| TC37 | PUT /admin/locations/{id} | slug trùng | 422 |
| TC38 | PUT /admin/locations/{id} | Không có token | 401 |
| TC39 | DELETE /admin/locations/{id} | Xóa thành công | 200/204 |
| TC40 | DELETE /admin/locations/{id} | ID không tồn tại | 404 |
| TC41 | DELETE /admin/locations/{id} | Không có token | 401 |
| TC42 | PATCH /admin/locations/{id}/status | Đổi sang inactive | 200 |
| TC43 | PATCH /admin/locations/{id}/status | Đổi sang active | 200 |
| TC44 | PATCH /admin/locations/{id}/status | status sai giá trị | 422 |
| TC45 | PATCH /admin/locations/{id}/status | ID không tồn tại | 404 |
| TC46 | PATCH /admin/locations/{id}/status | Không có token | 401 |
| TC47 | PATCH /admin/locations/{id}/featured | Bật nổi bật | 200 |
| TC48 | PATCH /admin/locations/{id}/featured | Tắt nổi bật | 200 |
| TC49 | PATCH /admin/locations/{id}/featured | is_featured sai kiểu | 422 |
| TC50 | PATCH /admin/locations/{id}/featured | ID không tồn tại | 404 |
| TC51 | PATCH /admin/locations/{id}/featured | Không có token | 401 |
