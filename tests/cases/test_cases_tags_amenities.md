# Test Cases — TAGS & AMENITIES

> Base URL: `http://localhost:8000/api/v1`
> Branch: `feat/taynd/api-tags-amenities`
> 🌐 Public: GET endpoints | 🛡️ Admin token bắt buộc cho write endpoints

---

## 1. GET /tags — Danh sách tags (Public)

### ✅ TC01 — Lấy tất cả tags
```http
GET /api/v1/tags
```
- Expected: `200 OK`, mỗi item có `id`, `name`, `slug`, `type`

### ✅ TC02 — Filter `type=cuisine`
- Expected: `200 OK`, tất cả item có `type = cuisine`

### ✅ TC03 — Filter `type=service`
- Expected: `200 OK`, tất cả item có `type = service`

### ✅ TC04 — Filter `type=feature`
- Expected: `200 OK`

### ✅ TC05 — Filter `type=atmosphere`
- Expected: `200 OK`

### ✅ TC06 — Không cần token (public)
- Expected: `200 OK`

### ❌ TC07 — `type` sai giá trị → 422
```http
GET /api/v1/tags?type=invalid_type
```
- Expected: `200 OK` hoặc `422 Unprocessable`
- Note: tùy backend có validate enum hay không

---

## 2. GET /amenities — Danh sách tiện ích (Public)

### ✅ TC08 — Lấy tất cả amenities
```http
GET /api/v1/amenities
```
- Expected: `200 OK`, mỗi item có `id`, `name`, `icon`, `category`

### ✅ TC09 — Filter `category=connectivity`
- Expected: `200 OK`, tất cả item có `category = connectivity`

### ✅ TC10 — Filter `category=parking`
- Expected: `200 OK`

### ✅ TC11 — Filter `category=comfort`
- Expected: `200 OK`

### ✅ TC12 — Filter `category=payment`
- Expected: `200 OK`

### ✅ TC13 — Không cần token (public)
- Expected: `200 OK`

### ❌ TC14 — `category` sai giá trị → 422
```http
GET /api/v1/amenities?category=invalid_category
```
- Expected: `200 OK` hoặc `422 Unprocessable`
- Note: tùy backend có validate enum hay không

---

## 3. POST /admin/tags — Tạo tag (Admin)

### ✅ TC15 — Tạo tag đầy đủ fields
```json
{ "name": "Test Tag", "slug": "test-tag-{ts}", "type": "cuisine" }
```
- Expected: `200 OK` hoặc `201 Created`
- Verify: response có `id`, `name`, `slug`, `type`

### ✅ TC16 — Tạo tag không có `type` (optional)
```json
{ "name": "Tag No Type {ts}" }
```
- Expected: `200 OK` hoặc `201 Created`
- Note: `slug` tự sinh nếu không truyền

### ❌ TC17 — Thiếu `name` → 422
```json
{ "slug": "no-name", "type": "cuisine" }
```
- Expected: `422 Unprocessable`

### ❌ TC18 — `type` sai giá trị → 422
```json
{ "name": "Bad Type", "type": "invalid_type" }
```
- Expected: `422 Unprocessable`

### ❌ TC19 — `slug` trùng → 422/409
- Expected: `422 Unprocessable` hoặc `409 Conflict`

### ❌ TC20 — User thường bị 403
- Expected: `403 Forbidden`

### ❌ TC21 — Không có token → 401
- Expected: `401 Unauthorized`

---

## 4. PUT /admin/tags/{id} — Cập nhật tag (Admin)

### ✅ TC22 — Cập nhật `name`
```json
{ "name": "Updated Tag Name" }
```
- Expected: `200 OK`, `name` thay đổi

### ✅ TC23 — Cập nhật `type`
```json
{ "type": "service" }
```
- Expected: `200 OK`

### ✅ TC24 — Cập nhật `slug`
```json
{ "slug": "updated-slug-{ts}" }
```
- Expected: `200 OK`

### ❌ TC25 — ID không tồn tại → 404/422
```http
PUT /api/v1/admin/tags/99999
```
- Expected: `404 Not Found` hoặc `422 Unprocessable`

### ❌ TC26 — `type` sai giá trị → 422
```json
{ "type": "invalid_type" }
```
- Expected: `422 Unprocessable`

### ❌ TC27 — User thường bị 403
- Expected: `403 Forbidden`

### ❌ TC28 — Không có token → 401
- Expected: `401 Unauthorized`

---

## 5. DELETE /admin/tags/{id} — Xóa tag (Admin)

### ✅ TC29 — Xóa tag thành công
- Expected: `200 OK` hoặc `204 No Content`
- Verify: GET /tags không còn ID này

### ❌ TC30 — ID không tồn tại → 404/422
- Expected: `404 Not Found` hoặc `422 Unprocessable`

### ❌ TC31 — User thường bị 403
- Expected: `403 Forbidden`

### ❌ TC32 — Không có token → 401
- Expected: `401 Unauthorized`

---

## 6. POST /admin/amenities — Tạo tiện ích (Admin)

### ✅ TC33 — Tạo amenity đầy đủ fields
```json
{ "name": "Test Amenity {ts}", "icon": "fa-wifi", "category": "connectivity" }
```
- Expected: `200 OK` hoặc `201 Created`
- Verify: response có `id`, `name`, `icon`, `category`

### ✅ TC34 — Tạo amenity chỉ có `name` (optional fields)
```json
{ "name": "Minimal Amenity {ts}" }
```
- Expected: `200 OK` hoặc `201 Created`

### ❌ TC35 — Thiếu `name` → 422
```json
{ "icon": "fa-wifi", "category": "connectivity" }
```
- Expected: `422 Unprocessable`

### ❌ TC36 — `category` sai giá trị → 422
```json
{ "name": "Bad Category", "category": "invalid_category" }
```
- Expected: `422 Unprocessable`

### ❌ TC37 — User thường bị 403
- Expected: `403 Forbidden`

### ❌ TC38 — Không có token → 401
- Expected: `401 Unauthorized`

---

## 7. PUT /admin/amenities/{id} — Cập nhật tiện ích (Admin)

### ✅ TC39 — Cập nhật `name`
```json
{ "name": "Updated Amenity Name" }
```
- Expected: `200 OK`, `name` thay đổi

### ✅ TC40 — Cập nhật `icon`
```json
{ "icon": "fa-parking" }
```
- Expected: `200 OK`

### ✅ TC41 — Cập nhật `category`
```json
{ "category": "parking" }
```
- Expected: `200 OK`

### ❌ TC42 — ID không tồn tại → 404/422
- Expected: `404 Not Found` hoặc `422 Unprocessable`

### ❌ TC43 — `category` sai giá trị → 422
```json
{ "category": "invalid_category" }
```
- Expected: `422 Unprocessable`

### ❌ TC44 — User thường bị 403
- Expected: `403 Forbidden`

### ❌ TC45 — Không có token → 401
- Expected: `401 Unauthorized`

---

## 8. DELETE /admin/amenities/{id} — Xóa tiện ích (Admin)

### ✅ TC46 — Xóa amenity thành công
- Expected: `200 OK` hoặc `204 No Content`
- Verify: GET /amenities không còn ID này

### ❌ TC47 — ID không tồn tại → 404/422
- Expected: `404 Not Found` hoặc `422 Unprocessable`

### ❌ TC48 — User thường bị 403
- Expected: `403 Forbidden`

### ❌ TC49 — Không có token → 401
- Expected: `401 Unauthorized`

---

## Tổng kết

| TC | API | Trường hợp | Expected |
|----|-----|-----------|----------|
| TC01–TC07 | GET /tags | List, filter type, auth | 200/422 |
| TC08–TC14 | GET /amenities | List, filter category, auth | 200/422 |
| TC15–TC21 | POST /admin/tags | Create, validation, auth | 200/201/422/403/401 |
| TC22–TC28 | PUT /admin/tags/{id} | Update, validation, auth | 200/422/403/401 |
| TC29–TC32 | DELETE /admin/tags/{id} | Delete, auth | 200/204/403/401 |
| TC33–TC38 | POST /admin/amenities | Create, validation, auth | 200/201/422/403/401 |
| TC39–TC45 | PUT /admin/amenities/{id} | Update, validation, auth | 200/422/403/401 |
| TC46–TC49 | DELETE /admin/amenities/{id} | Delete, auth | 200/204/403/401 |

**Tổng: 49 test cases** — 22 happy path ✅ · 27 error case ❌
