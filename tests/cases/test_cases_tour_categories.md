# Test Cases — TOUR CATEGORIES (Danh mục tour)

> Base URL: `http://localhost:8000/api/v1`
> 🌐 Public: không cần token
> 🛡️ Admin token bắt buộc cho write endpoints

---

## 1. GET /tour-categories — Danh sách danh mục (Public)

### ✅ TC01 — Lấy danh sách thành công
- Expected: `200 OK`
- Verify: mỗi item có `id`, `name`, `slug`, `status`

### ✅ TC02 — Chỉ trả về `status=active`
- Expected: `200 OK`
- Verify: tất cả item có `status = active`

### ✅ TC03 — Không cần token (public)
- Expected: `200 OK`

---

## 2. GET /tour-categories/{slug}/tours — Tour theo danh mục (Public)

### ✅ TC04 — Lấy tour theo slug thành công
- Expected: `200 OK`
- Verify: tất cả tour thuộc đúng category

### ✅ TC05 — Phân trang `per_page=5`
- Expected: `200 OK`, `data` có tối đa 5 phần tử

### ✅ TC06 — Sort `price_adult asc`
- Expected: `200 OK`

### ✅ TC07 — Không cần token
- Expected: `200 OK`

### ❌ TC08 — Slug không tồn tại
- Expected: `404 Not Found` hoặc `200` với data rỗng

---

## 3. GET /admin/tour-categories — Danh sách admin (Admin)

### ✅ TC09 — Lấy tất cả (kể cả inactive)
- Expected: `200 OK`

### ✅ TC10 — Filter `status=active`
- Expected: `200 OK`
- Verify: tất cả item có `status = active`

### ✅ TC11 — Filter `status=inactive`
- Expected: `200 OK`

### ✅ TC12 — Phân trang `per_page=5`
- Expected: `200 OK`

### ❌ TC13 — `status` sai giá trị
- Expected: `422 Unprocessable`

### ❌ TC14 — User thường không được truy cập
- Expected: `403 Forbidden`

### ❌ TC15 — Không có token
- Expected: `401 Unauthorized`

---

## 4. POST /admin/tour-categories — Tạo danh mục (Admin)

### ✅ TC16 — Tạo thành công với đầy đủ fields
```json
{
  "name": "Tour Test Category",
  "slug": "tour-test-category",
  "description": "Mo ta danh muc test",
  "icon": "fa-map",
  "sort_order": 99,
  "status": "active"
}
```
- Expected: `200 OK` hoặc `201 Created`
- Verify: response có `id`, `name`, `slug`

### ✅ TC17 — Tạo chỉ với `name` (các field khác optional)
```json
{ "name": "Tour Minimal Category" }
```
- Expected: `200 OK` hoặc `201 Created`

### ❌ TC18 — Thiếu `name`
```json
{ "slug": "no-name", "status": "active" }
```
- Expected: `422 Unprocessable`

### ❌ TC19 — `name` trùng (đã tồn tại)
- Expected: `422 Unprocessable` hoặc `409 Conflict`

### ❌ TC20 — `slug` trùng (đã tồn tại)
- Expected: `422 Unprocessable` hoặc `409 Conflict`

### ❌ TC21 — `status` sai giá trị
```json
{ "name": "Test", "status": "invalid" }
```
- Expected: `422 Unprocessable`

### ❌ TC22 — User thường không được tạo
- Expected: `403 Forbidden`

### ❌ TC23 — Không có token
- Expected: `401 Unauthorized`

---

## 5. PUT /admin/tour-categories/{id} — Cập nhật (Admin)

### ✅ TC24 — Cập nhật `name` thành công
```json
{ "name": "Updated Category Name" }
```
- Expected: `200 OK`
- Verify: `name` thay đổi trong response

### ✅ TC25 — Cập nhật `description`
```json
{ "description": "Mo ta moi" }
```
- Expected: `200 OK`

### ✅ TC26 — Cập nhật `sort_order`
```json
{ "sort_order": 5 }
```
- Expected: `200 OK`

### ❌ TC27 — ID không tồn tại
- Expected: `404 Not Found` hoặc `422`

### ❌ TC28 — `status` sai giá trị
```json
{ "status": "invalid" }
```
- Expected: `422 Unprocessable`

### ❌ TC29 — User thường không được cập nhật
- Expected: `403 Forbidden`

### ❌ TC30 — Không có token
- Expected: `401 Unauthorized`

---

## 6. DELETE /admin/tour-categories/{id} — Xóa (Admin)

### ✅ TC31 — Xóa danh mục không có tour thành công
- Expected: `200 OK` hoặc `204 No Content`
- Verify: GET `/tour-categories` không còn item này

### ❌ TC32 — Xóa danh mục đang có tour (FK constraint)
- Expected: `400 Bad Request` hoặc `422 Unprocessable` hoặc `409 Conflict`
- Note: backend trả `400` với message `Cannot delete category with associated tours`

### ❌ TC33 — ID không tồn tại
- Expected: `404 Not Found` hoặc `422`

### ❌ TC34 — User thường không được xóa
- Expected: `403 Forbidden`

### ❌ TC35 — Không có token
- Expected: `401 Unauthorized`

---

## 7. PATCH /admin/tour-categories/{id}/status — Đổi trạng thái (Admin)

### ✅ TC36 — Đổi sang `inactive`
```json
{ "status": "inactive" }
```
- Expected: `200 OK`
- Verify: `status = inactive`

### ✅ TC37 — Đổi sang `active`
```json
{ "status": "active" }
```
- Expected: `200 OK`
- Verify: `status = active`

### ✅ TC38 — Idempotent (set lại status giống hiện tại)
```json
{ "status": "active" }
```
- Expected: `200 OK`

### ❌ TC39 — `status` sai giá trị
```json
{ "status": "pending" }
```
- Expected: `422 Unprocessable`

### ❌ TC40 — Thiếu `status`
```json
{}
```
- Expected: `422 Unprocessable`

### ❌ TC41 — ID không tồn tại
- Expected: `404 Not Found` hoặc `422`

### ❌ TC42 — User thường không được đổi status
- Expected: `403 Forbidden`

### ❌ TC43 — Không có token
- Expected: `401 Unauthorized`

---

## Tổng kết

| TC | API | Trường hợp | Expected |
|----|-----|-----------|----------|
| TC01 | GET /tour-categories | Lấy danh sách | 200 |
| TC02 | GET /tour-categories | Chỉ active | 200 |
| TC03 | GET /tour-categories | Không cần token | 200 |
| TC04 | GET /tour-categories/{slug}/tours | Tour theo slug | 200 |
| TC05 | GET /tour-categories/{slug}/tours | Phân trang | 200 |
| TC06 | GET /tour-categories/{slug}/tours | Sort | 200 |
| TC07 | GET /tour-categories/{slug}/tours | Không cần token | 200 |
| TC08 | GET /tour-categories/{slug}/tours | Slug không tồn tại | 404/200 |
| TC09 | GET /admin/tour-categories | Lấy tất cả | 200 |
| TC10 | GET /admin/tour-categories | Filter active | 200 |
| TC11 | GET /admin/tour-categories | Filter inactive | 200 |
| TC12 | GET /admin/tour-categories | Phân trang | 200 |
| TC13 | GET /admin/tour-categories | status sai | 422 |
| TC14 | GET /admin/tour-categories | User thường | 403 |
| TC15 | GET /admin/tour-categories | Không có token | 401 |
| TC16 | POST /admin/tour-categories | Tạo đầy đủ | 200/201 |
| TC17 | POST /admin/tour-categories | Chỉ name | 200/201 |
| TC18 | POST /admin/tour-categories | Thiếu name | 422 |
| TC19 | POST /admin/tour-categories | name trùng | 422/409 |
| TC20 | POST /admin/tour-categories | slug trùng | 422/409 |
| TC21 | POST /admin/tour-categories | status sai | 422 |
| TC22 | POST /admin/tour-categories | User thường | 403 |
| TC23 | POST /admin/tour-categories | Không có token | 401 |
| TC24 | PUT /admin/tour-categories/{id} | Cập nhật name | 200 |
| TC25 | PUT /admin/tour-categories/{id} | Cập nhật description | 200 |
| TC26 | PUT /admin/tour-categories/{id} | Cập nhật sort_order | 200 |
| TC27 | PUT /admin/tour-categories/{id} | ID không tồn tại | 404/422 |
| TC28 | PUT /admin/tour-categories/{id} | status sai | 422 |
| TC29 | PUT /admin/tour-categories/{id} | User thường | 403 |
| TC30 | PUT /admin/tour-categories/{id} | Không có token | 401 |
| TC31 | DELETE /admin/tour-categories/{id} | Xóa thành công | 200/204 |
| TC32 | DELETE /admin/tour-categories/{id} | Có tour (FK) | 400/422/409 |
| TC33 | DELETE /admin/tour-categories/{id} | ID không tồn tại | 404/422 |
| TC34 | DELETE /admin/tour-categories/{id} | User thường | 403 |
| TC35 | DELETE /admin/tour-categories/{id} | Không có token | 401 |
| TC36 | PATCH .../status | inactive | 200 |
| TC37 | PATCH .../status | active | 200 |
| TC38 | PATCH .../status | Idempotent | 200 |
| TC39 | PATCH .../status | status sai | 422 |
| TC40 | PATCH .../status | Thiếu status | 422 |
| TC41 | PATCH .../status | ID không tồn tại | 404/422 |
| TC42 | PATCH .../status | User thường | 403 |
| TC43 | PATCH .../status | Không có token | 401 |
