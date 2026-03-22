# Test Cases — CATEGORIES & SUBCATEGORIES

> Base URL: `http://localhost:8000/api/v1`
> Admin token cần thiết cho các API 🛡️

---

## 1. GET /categories — Danh sách danh mục

### ✅ TC01 — Lấy danh sách thành công
```http
GET /api/v1/categories
```
- Expected: `200 OK`, trả về array categories kèm subcategories

---

## 2. GET /categories/{id} — Chi tiết danh mục

### ✅ TC02 — ID hợp lệ
```http
GET /api/v1/categories/1
```
- Expected: `200 OK`, trả về object category

### ❌ TC03 — ID không tồn tại
```http
GET /api/v1/categories/99999
```
- Expected: `404 Not Found`

### ❌ TC04 — ID không phải số
```http
GET /api/v1/categories/abc
```
- Expected: `404 Not Found` hoặc `422 Unprocessable`

---

## 3. POST /admin/categories — Tạo danh mục

### ✅ TC05 — Đủ tất cả field hợp lệ
```json
{
  "name": "Ăn uống",
  "slug": "an-uong",
  "icon": "fa-utensils",
  "description": "Nhà hàng, quán ăn, cà phê tại Đà Nẵng",
  "image": "(file)",
  "sort_order": 1,
  "status": "active"
}
```
- Expected: `201 Created`

### ✅ TC06 — Chỉ truyền field bắt buộc
```json
{
  "name": "Khách sạn",
  "status": "active"
}
```
- Expected: `201 Created`, slug tự sinh từ name

### ❌ TC07 — Thiếu `name`
```json
{
  "status": "active"
}
```
- Expected: `422 Unprocessable`, lỗi validation `name required`

### ❌ TC08 — Thiếu `status`
```json
{
  "name": "Du lịch"
}
```
- Expected: `422 Unprocessable`, lỗi validation `status required`

### ❌ TC09 — `slug` trùng với danh mục đã có
```json
{
  "name": "Ăn uống 2",
  "slug": "an-uong",
  "status": "active"
}
```
- Expected: `422 Unprocessable`, lỗi `slug has already been taken`

### ❌ TC10 — `status` sai giá trị
```json
{
  "name": "Test",
  "status": "unknown"
}
```
- Expected: `422 Unprocessable`, lỗi `status must be active or inactive`

### ❌ TC11 — Không có token
```json
{
  "name": "Test",
  "status": "active"
}
```
- Expected: `401 Unauthorized`

### ❌ TC12 — Token của user thường (không phải admin)
```json
{
  "name": "Test",
  "status": "active"
}
```
- Expected: `403 Forbidden`

---

## 4. PUT /admin/categories/{id} — Cập nhật danh mục

### ✅ TC13 — Cập nhật hợp lệ
```json
{
  "name": "Ăn uống & Đồ uống",
  "slug": "an-uong-do-uong",
  "status": "active"
}
```
- Expected: `200 OK`

### ✅ TC14 — Chỉ cập nhật 1 field
```json
{
  "status": "inactive"
}
```
- Expected: `200 OK`, chỉ field đó thay đổi

### ❌ TC15 — ID không tồn tại
```http
PUT /api/v1/admin/categories/99999
```
- Expected: `404 Not Found`

### ❌ TC16 — `slug` trùng với danh mục khác
```json
{
  "slug": "an-uong"
}
```
- Expected: `422 Unprocessable`, lỗi `slug has already been taken`

### ❌ TC17 — Không có token
- Expected: `401 Unauthorized`

---

## 5. DELETE /admin/categories/{id} — Xóa danh mục

### ✅ TC18 — Xóa danh mục không có địa điểm nào
```http
DELETE /api/v1/admin/categories/1
```
- Expected: `200 OK` hoặc `204 No Content`

### ❌ TC19 — Xóa danh mục đang có địa điểm liên kết
- Expected: `422 Unprocessable` hoặc `409 Conflict`, không cho xóa

### ❌ TC20 — ID không tồn tại
```http
DELETE /api/v1/admin/categories/99999
```
- Expected: `404 Not Found`

### ❌ TC21 — Không có token
- Expected: `401 Unauthorized`

---

## 6. POST /admin/subcategories — Tạo danh mục con

### ✅ TC22 — Đủ field hợp lệ
```json
{
  "category_id": 1,
  "name": "Hải sản",
  "slug": "hai-san",
  "description": "Nhà hàng hải sản tươi sống",
  "sort_order": 1,
  "status": "active"
}
```
- Expected: `201 Created`

### ✅ TC23 — Chỉ field bắt buộc
```json
{
  "category_id": 1,
  "name": "Quán cà phê",
  "status": "active"
}
```
- Expected: `201 Created`

### ❌ TC24 — Thiếu `category_id`
```json
{
  "name": "Hải sản",
  "status": "active"
}
```
- Expected: `422 Unprocessable`

### ❌ TC25 — `category_id` không tồn tại
```json
{
  "category_id": 99999,
  "name": "Hải sản",
  "status": "active"
}
```
- Expected: `422 Unprocessable`, lỗi foreign key

### ❌ TC26 — `slug` trùng
```json
{
  "category_id": 1,
  "name": "Hải sản 2",
  "slug": "hai-san",
  "status": "active"
}
```
- Expected: `422 Unprocessable`

### ❌ TC27 — Không có token
- Expected: `401 Unauthorized`

---

## 7. PUT /admin/subcategories/{id} — Cập nhật danh mục con

### ✅ TC28 — Cập nhật hợp lệ
```json
{
  "name": "Hải sản cao cấp",
  "status": "active"
}
```
- Expected: `200 OK`

### ✅ TC29 — Chuyển sang category khác
```json
{
  "category_id": 2
}
```
- Expected: `200 OK`

### ❌ TC30 — ID không tồn tại
```http
PUT /api/v1/admin/subcategories/99999
```
- Expected: `404 Not Found`

### ❌ TC31 — Không có token
- Expected: `401 Unauthorized`

---

## 8. DELETE /admin/subcategories/{id} — Xóa danh mục con

### ✅ TC32 — Xóa subcategory không có địa điểm
```http
DELETE /api/v1/admin/subcategories/1
```
- Expected: `200 OK` hoặc `204 No Content`

### ❌ TC33 — Xóa subcategory đang có địa điểm liên kết
- Expected: `422 Unprocessable` hoặc `409 Conflict`

### ❌ TC34 — ID không tồn tại
```http
DELETE /api/v1/admin/subcategories/99999
```
- Expected: `404 Not Found`

### ❌ TC35 — Không có token
- Expected: `401 Unauthorized`

---

## Tổng kết

| TC | API | Trường hợp | Expected |
|----|-----|-----------|----------|
| TC01 | GET /categories | Thành công | 200 |
| TC02 | GET /categories/{id} | ID hợp lệ | 200 |
| TC03 | GET /categories/{id} | ID không tồn tại | 404 |
| TC04 | GET /categories/{id} | ID không phải số | 404/422 |
| TC05 | POST /admin/categories | Đủ field | 201 |
| TC06 | POST /admin/categories | Chỉ field bắt buộc | 201 |
| TC07 | POST /admin/categories | Thiếu name | 422 |
| TC08 | POST /admin/categories | Thiếu status | 422 |
| TC09 | POST /admin/categories | Slug trùng | 422 |
| TC10 | POST /admin/categories | Status sai giá trị | 422 |
| TC11 | POST /admin/categories | Không có token | 401 |
| TC12 | POST /admin/categories | Token user thường | 403 |
| TC13 | PUT /admin/categories/{id} | Cập nhật hợp lệ | 200 |
| TC14 | PUT /admin/categories/{id} | Cập nhật 1 field | 200 |
| TC15 | PUT /admin/categories/{id} | ID không tồn tại | 404 |
| TC16 | PUT /admin/categories/{id} | Slug trùng | 422 |
| TC17 | PUT /admin/categories/{id} | Không có token | 401 |
| TC18 | DELETE /admin/categories/{id} | Xóa thành công | 200/204 |
| TC19 | DELETE /admin/categories/{id} | Có địa điểm liên kết | 422/409 |
| TC20 | DELETE /admin/categories/{id} | ID không tồn tại | 404 |
| TC21 | DELETE /admin/categories/{id} | Không có token | 401 |
| TC22 | POST /admin/subcategories | Đủ field | 201 |
| TC23 | POST /admin/subcategories | Chỉ field bắt buộc | 201 |
| TC24 | POST /admin/subcategories | Thiếu category_id | 422 |
| TC25 | POST /admin/subcategories | category_id không tồn tại | 422 |
| TC26 | POST /admin/subcategories | Slug trùng | 422 |
| TC27 | POST /admin/subcategories | Không có token | 401 |
| TC28 | PUT /admin/subcategories/{id} | Cập nhật hợp lệ | 200 |
| TC29 | PUT /admin/subcategories/{id} | Chuyển category | 200 |
| TC30 | PUT /admin/subcategories/{id} | ID không tồn tại | 404 |
| TC31 | PUT /admin/subcategories/{id} | Không có token | 401 |
| TC32 | DELETE /admin/subcategories/{id} | Xóa thành công | 200/204 |
| TC33 | DELETE /admin/subcategories/{id} | Có địa điểm liên kết | 422/409 |
| TC34 | DELETE /admin/subcategories/{id} | ID không tồn tại | 404 |
| TC35 | DELETE /admin/subcategories/{id} | Không có token | 401 |
