# Test Cases  TAGS & AMENITIES

> Base URL: `http://localhost:8000/api/v1`
>  Public: không cần token
>  Admin token bắt buộc cho write endpoints

---

## 1. GET /tags  Danh sách tags (Public)

###  TC01  Lấy tất cả tags thành công
```http
GET /api/v1/tags
```
- Expected: `200 OK`
- Verify: response có `data` là array, mỗi item có `id`, `name`, `slug`, `type`

###  TC02  Filter `type=cuisine`
```http
GET /api/v1/tags?type=cuisine
```
- Expected: `200 OK`
- Verify: tất cả item có `type = cuisine`

###  TC03  Filter `type=service`
```http
GET /api/v1/tags?type=service
```
- Expected: `200 OK`
- Verify: tất cả item có `type = service`

###  TC04  Filter `type=feature`
```http
GET /api/v1/tags?type=feature
```
- Expected: `200 OK`

###  TC05  Filter `type=atmosphere`
```http
GET /api/v1/tags?type=atmosphere
```
- Expected: `200 OK`

###  TC06  Không cần token (public)
```http
GET /api/v1/tags
```
- Expected: `200 OK`

###  TC07  `type` sai giá trị
```http
GET /api/v1/tags?type=invalid
```
- Expected: `422 Unprocessable`

---

## 2. GET /amenities  Danh sách tiện ích (Public)

###  TC08  Lấy tất cả amenities thành công
```http
GET /api/v1/amenities
```
- Expected: `200 OK`
- Verify: mỗi item có `id`, `name`, `icon`, `category`

###  TC09  Filter `category=connectivity`
```http
GET /api/v1/amenities?category=connectivity
```
- Expected: `200 OK`
- Verify: tất cả item có `category = connectivity`

###  TC10  Filter `category=parking`
```http
GET /api/v1/amenities?category=parking
```
- Expected: `200 OK`

###  TC11  Filter `category=comfort`
```http
GET /api/v1/amenities?category=comfort
```
- Expected: `200 OK`

###  TC12  Filter `category=payment`
```http
GET /api/v1/amenities?category=payment
```
- Expected: `200 OK`

###  TC13  Không cần token (public)
```http
GET /api/v1/amenities
```
- Expected: `200 OK`

###  TC14  `category` sai giá trị
```http
GET /api/v1/amenities?category=invalid
```
- Expected: `422 Unprocessable`

---

## 3. POST /admin/tags  Tạo tag mới (Admin)

###  TC15  Tạo tag thành công với đầy đủ fields
```json
{ "name": "Test Tag", "slug": "test-tag", "type": "cuisine" }
```
- Expected: `200 OK` hoặc `201 Created`
- Verify: response có `id`, `name`, `slug`, `type`

###  TC16  Tạo tag không có `type` (optional)
```json
{ "name": "Tag No Type", "slug": "tag-no-type" }
```
- Expected: `200 OK` hoặc `201 Created`

###  TC17  Thiếu `name`
```json
{ "slug": "no-name" }
```
- Expected: `422 Unprocessable`

###  TC18  Thiếu `slug`
```json
{ "name": "No Slug" }
```
- Expected: `422 Unprocessable`

###  TC19  `name` trùng (đã tồn tại)
```json
{ "name": "Test Tag", "slug": "test-tag-2" }
```
- Expected: `422 Unprocessable` hoặc `409 Conflict`

###  TC20  `slug` trùng (đã tồn tại)
```json
{ "name": "Tag Unique Name", "slug": "test-tag" }
```
- Expected: `422 Unprocessable` hoặc `409 Conflict`

###  TC21  `type` sai giá trị
```json
{ "name": "Bad Type", "slug": "bad-type", "type": "invalid" }
```
- Expected: `422 Unprocessable`

###  TC22  User thường không được tạo tag
```json
{ "name": "User Tag", "slug": "user-tag" }
```
- Expected: `403 Forbidden`

###  TC23  Không có token
```json
{ "name": "No Token Tag", "slug": "no-token-tag" }
```
- Expected: `401 Unauthorized`

---

## 4. DELETE /admin/tags/{id}  Xóa tag (Admin)

###  TC24  Xóa tag thành công
```http
DELETE /api/v1/admin/tags/{id}
```
- Expected: `200 OK` hoặc `204 No Content`
- Verify: tag không còn trong GET /tags

###  TC25  Xóa ID không tồn tại
```http
DELETE /api/v1/admin/tags/99999
```
- Expected: `404 Not Found` hoặc `422 Unprocessable`

###  TC26  User thường không được xóa
```http
DELETE /api/v1/admin/tags/{id}
```
- Expected: `403 Forbidden`

###  TC27  Không có token
```http
DELETE /api/v1/admin/tags/{id}
```
- Expected: `401 Unauthorized`

---

## 5. POST /admin/amenities  Tạo tiện ích mới (Admin)

###  TC28  Tạo amenity thành công với đầy đủ fields
```json
{ "name": "Test Amenity", "icon": "fa-test", "category": "connectivity" }
```
- Expected: `200 OK` hoặc `201 Created`
- Verify: response có `id`, `name`, `icon`, `category`

###  TC29  Tạo amenity không có `icon` và `category` (optional)
```json
{ "name": "Amenity Minimal" }
```
- Expected: `200 OK` hoặc `201 Created`

###  TC30  Thiếu `name`
```json
{ "icon": "fa-test", "category": "connectivity" }
```
- Expected: `422 Unprocessable`

###  TC31  `name` trùng (đã tồn tại)
```json
{ "name": "Test Amenity" }
```
- Expected: `422 Unprocessable` hoặc `409 Conflict`

###  TC32  `category` sai giá trị
```json
{ "name": "Bad Category", "category": "invalid" }
```
- Expected: `422 Unprocessable`

###  TC33  User thường không được tạo amenity
```json
{ "name": "User Amenity" }
```
- Expected: `403 Forbidden`

###  TC34  Không có token
```json
{ "name": "No Token Amenity" }
```
- Expected: `401 Unauthorized`

---

## 6. DELETE /admin/amenities/{id}  Xóa tiện ích (Admin)

###  TC35  Xóa amenity thành công
```http
DELETE /api/v1/admin/amenities/{id}
```
- Expected: `200 OK` hoặc `204 No Content`
- Verify: amenity không còn trong GET /amenities

###  TC36  Xóa ID không tồn tại
```http
DELETE /api/v1/admin/amenities/99999
```
- Expected: `404 Not Found` hoặc `422 Unprocessable`

###  TC37  User thường không được xóa
```http
DELETE /api/v1/admin/amenities/{id}
```
- Expected: `403 Forbidden`

###  TC38  Không có token
```http
DELETE /api/v1/admin/amenities/{id}
```
- Expected: `401 Unauthorized`

---

## Tổng kết

| TC | API | Trường hợp | Expected |
|----|-----|-----------|----------|
| TC01 | GET /tags | Lấy tất cả | 200 |
| TC02 | GET /tags | Filter type=cuisine | 200 |
| TC03 | GET /tags | Filter type=service | 200 |
| TC04 | GET /tags | Filter type=feature | 200 |
| TC05 | GET /tags | Filter type=atmosphere | 200 |
| TC06 | GET /tags | Không cần token | 200 |
| TC07 | GET /tags | type sai giá trị | 422 |
| TC08 | GET /amenities | Lấy tất cả | 200 |
| TC09 | GET /amenities | Filter category=connectivity | 200 |
| TC10 | GET /amenities | Filter category=parking | 200 |
| TC11 | GET /amenities | Filter category=comfort | 200 |
| TC12 | GET /amenities | Filter category=payment | 200 |
| TC13 | GET /amenities | Không cần token | 200 |
| TC14 | GET /amenities | category sai giá trị | 422 |
| TC15 | POST /admin/tags | Tạo đầy đủ fields | 200/201 |
| TC16 | POST /admin/tags | Không có type | 200/201 |
| TC17 | POST /admin/tags | Thiếu name | 422 |
| TC18 | POST /admin/tags | Thiếu slug | 422 |
| TC19 | POST /admin/tags | name trùng | 422/409 |
| TC20 | POST /admin/tags | slug trùng | 422/409 |
| TC21 | POST /admin/tags | type sai | 422 |
| TC22 | POST /admin/tags | User thường | 403 |
| TC23 | POST /admin/tags | Không có token | 401 |
| TC24 | DELETE /admin/tags/{id} | Xóa thành công | 200/204 |
| TC25 | DELETE /admin/tags/{id} | ID không tồn tại | 404/422 |
| TC26 | DELETE /admin/tags/{id} | User thường | 403 |
| TC27 | DELETE /admin/tags/{id} | Không có token | 401 |
| TC28 | POST /admin/amenities | Tạo đầy đủ fields | 200/201 |
| TC29 | POST /admin/amenities | Chỉ có name | 200/201 |
| TC30 | POST /admin/amenities | Thiếu name | 422 |
| TC31 | POST /admin/amenities | name trùng | 422/409 |
| TC32 | POST /admin/amenities | category sai | 422 |
| TC33 | POST /admin/amenities | User thường | 403 |
| TC34 | POST /admin/amenities | Không có token | 401 |
| TC35 | DELETE /admin/amenities/{id} | Xóa thành công | 200/204 |
| TC36 | DELETE /admin/amenities/{id} | ID không tồn tại | 404/422 |
| TC37 | DELETE /admin/amenities/{id} | User thường | 403 |
| TC38 | DELETE /admin/amenities/{id} | Không có token | 401 |

