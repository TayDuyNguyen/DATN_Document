# Test Cases — BLOG (Bài viết)

> Base URL: `http://localhost:8000/api/v1`
> 🌐 Public: không cần token
> 🔐 User token
> 🛡️ Admin token bắt buộc

---

## 1. GET /blog — Danh sách bài viết (Public)

### ✅ TC01 — Lấy danh sách thành công
```http
GET /api/v1/blog
```
- Expected: `200 OK`
- Verify: response có `data` là array, mỗi item có `id`, `title`, `slug`, `excerpt`, `status`, `published_at`

### ✅ TC02 — Chỉ trả về bài `published`
```http
GET /api/v1/blog
```
- Expected: `200 OK`
- Verify: tất cả item có `status = published`

### ✅ TC03 — Phân trang `per_page=5`
```http
GET /api/v1/blog?page=1&per_page=5
```
- Expected: `200 OK`, `data` có tối đa 5 phần tử

### ✅ TC04 — Trang 2
```http
GET /api/v1/blog?page=2&per_page=5
```
- Expected: `200 OK`

### ✅ TC05 — Filter theo `category_id` hợp lệ
```http
GET /api/v1/blog?category_id=1
```
- Expected: `200 OK`
- Verify: tất cả item thuộc category_id=1

### ✅ TC06 — Filter `category_id` không có bài nào
```http
GET /api/v1/blog?category_id=99999
```
- Expected: `200 OK` hoặc `422 Unprocessable`
- Nếu 200: `data = []`
- Nếu 422: backend validate `category_id` phải tồn tại trong DB

### ❌ TC07 — `category_id` không phải số
```http
GET /api/v1/blog?category_id=abc
```
- Expected: `422 Unprocessable`

### ✅ TC08 — `per_page` vượt max 100
```http
GET /api/v1/blog?per_page=200
```
- Expected: `200 OK` hoặc `422 Unprocessable`
- Nếu 200: verify số item <= 100

### ✅ TC09 — Không cần token (public)
```http
GET /api/v1/blog
```
- Expected: `200 OK` (không cần Authorization header)

---

## 2. GET /blog/{slug} — Chi tiết bài viết (Public)

### ✅ TC10 — Lấy chi tiết thành công
```http
GET /api/v1/blog/{slug_hop_le}
```
- Expected: `200 OK`
- Verify: có fields `id`, `title`, `slug`, `content`, `author`, `view_count`, `published_at`

### ✅ TC11 — `view_count` tăng sau mỗi lần xem
```http
GET /api/v1/blog/{slug} (gọi 2 lần)
```
- Expected: `200 OK`
- Verify: `view_count` lần 2 >= lần 1

### ✅ TC12 — Không cần token (public)
```http
GET /api/v1/blog/{slug}
```
- Expected: `200 OK` (không cần Authorization header)

### ❌ TC13 — Slug không tồn tại
```http
GET /api/v1/blog/slug-khong-ton-tai-xyz-999
```
- Expected: `404 Not Found`

### ❌ TC14 — Bài viết `draft` không hiển thị public
```http
GET /api/v1/blog/{slug_bai_draft}
```
- Expected: `404 Not Found` hoặc `403 Forbidden`

---

## 3. GET /blog/categories — Danh mục blog (Public)

### ✅ TC15 — Lấy danh sách danh mục thành công
```http
GET /api/v1/blog/categories
```
- Expected: `200 OK`
- Verify: mỗi item có `id`, `name`, `slug`

### ✅ TC16 — Không cần token (public)
```http
GET /api/v1/blog/categories
```
- Expected: `200 OK`

---

## 4. POST /admin/blog — Tạo bài viết (Admin)

### ✅ TC17 — Tạo bài viết `draft` thành công
```json
{
  "title": "Bài viết test draft",
  "content": "Nội dung bài viết test đầy đủ",
  "category_ids": [1],
  "status": "draft"
}
```
- Expected: `200 OK` hoặc `201 Created`
- Verify: response có `id`, `slug` tự sinh từ `title`, `status=draft`

### ✅ TC18 — Tạo bài viết `published` thành công
```json
{
  "title": "Bài viết test published",
  "content": "Nội dung bài viết published",
  "category_ids": [1],
  "status": "published"
}
```
- Expected: `200 OK` hoặc `201 Created`
- Verify: `status=published`, `published_at` không null

### ✅ TC19 — Tạo với đầy đủ fields
```json
{
  "title": "Bài viết đầy đủ fields",
  "content": "Nội dung chi tiết",
  "excerpt": "Tóm tắt ngắn",
  "featured_image": "https://example.com/image.jpg",
  "category_ids": [1],
  "status": "draft"
}
```
- Expected: `200 OK` hoặc `201 Created`

### ✅ TC20 — Tạo với nhiều `category_ids`
```json
{
  "title": "Bài viết nhiều danh mục",
  "content": "Nội dung",
  "category_ids": [1, 2],
  "status": "draft"
}
```
- Expected: `200 OK` hoặc `201 Created`
- Verify: bài viết thuộc cả 2 category

### ❌ TC21 — Thiếu `title`
```json
{ "content": "Nội dung", "status": "draft" }
```
- Expected: `422 Unprocessable`

### ❌ TC22 — Thiếu `content`
```json
{ "title": "Tiêu đề", "status": "draft" }
```
- Expected: `422 Unprocessable`

### ❌ TC23 — `status` sai giá trị
```json
{ "title": "Test", "content": "Test", "status": "invalid" }
```
- Expected: `422 Unprocessable`

### ❌ TC24 — `category_ids` chứa ID không tồn tại
```json
{ "title": "Test", "content": "Test", "category_ids": [99999], "status": "draft" }
```
- Expected: `422 Unprocessable` hoặc `404 Not Found`

### ❌ TC25 — User thường không được tạo bài (403)
```json
{ "title": "Test", "content": "Test", "status": "draft" }
```
- Expected: `403 Forbidden`

### ❌ TC26 — Không có token
```json
{ "title": "Test", "content": "Test", "status": "draft" }
```
- Expected: `401 Unauthorized`

---

## 5. PUT /admin/blog/{id} — Cập nhật bài viết (Admin)

### ✅ TC27 — Cập nhật `title` thành công
```json
{ "title": "Tiêu đề đã cập nhật" }
```
- Expected: `200 OK`
- Verify: `title` thay đổi trong response

### ✅ TC28 — Cập nhật `content` thành công
```json
{ "content": "Nội dung mới đã cập nhật" }
```
- Expected: `200 OK`

### ✅ TC29 — Cập nhật `category_ids` (sync)
```json
{ "category_ids": [2] }
```
- Expected: `200 OK`
- Verify: category cũ bị xóa, category mới được gán

### ✅ TC30 — Cập nhật `category_ids = []` (xóa hết category)
```json
{ "category_ids": [] }
```
- Expected: `200 OK` hoặc `422 Unprocessable`

### ❌ TC31 — ID không tồn tại
```json
{ "title": "Test" }
```
- Expected: `404 Not Found`

### ❌ TC32 — `status` sai giá trị
```json
{ "status": "invalid" }
```
- Expected: `422 Unprocessable`

### ❌ TC33 — User thường không được cập nhật
```json
{ "title": "Test" }
```
- Expected: `403 Forbidden`

### ❌ TC34 — Không có token
```json
{ "title": "Test" }
```
- Expected: `401 Unauthorized`

---

## 6. DELETE /admin/blog/{id} — Xóa bài viết (Admin)

### ✅ TC35 — Xóa bài viết thành công
```http
DELETE /api/v1/admin/blog/{id}
```
- Expected: `200 OK` hoặc `204 No Content`
- Verify: GET `/blog/{slug}` → `404 Not Found`

### ❌ TC36 — Xóa ID không tồn tại
```http
DELETE /api/v1/admin/blog/99999
```
- Expected: `404 Not Found`

### ❌ TC37 — User thường không được xóa
```http
DELETE /api/v1/admin/blog/{id}
```
- Expected: `403 Forbidden`

### ❌ TC38 — Không có token
```http
DELETE /api/v1/admin/blog/{id}
```
- Expected: `401 Unauthorized`

---

## 7. PATCH /admin/blog/{id}/publish — Xuất bản / Ẩn bài viết (Admin)

### ✅ TC39 — Xuất bản bài `draft` → `published`
```json
{ "status": "published" }
```
- Expected: `200 OK`
- Verify: `status=published`, `published_at` không null

### ✅ TC40 — Ẩn bài `published` → `draft`
```json
{ "status": "draft" }
```
- Expected: `200 OK`
- Verify: `status=draft`

### ✅ TC41 — Publish lại bài đã published (idempotent)
```json
{ "status": "published" }
```
- Expected: `200 OK`

### ❌ TC42 — `status` sai giá trị
```json
{ "status": "archived" }
```
- Expected: `422 Unprocessable`

### ❌ TC43 — Thiếu `status`
```json
{}
```
- Expected: `422 Unprocessable`

### ❌ TC44 — ID không tồn tại
```json
{ "status": "published" }
```
- Expected: `404 Not Found`

### ❌ TC45 — User thường không được publish
```json
{ "status": "published" }
```
- Expected: `403 Forbidden`

### ❌ TC46 — Không có token
```json
{ "status": "published" }
```
- Expected: `401 Unauthorized`

---

## Tổng kết

| TC | API | Trường hợp | Expected |
|----|-----|-----------|----------|
| TC01 | GET /blog | Lấy danh sách | 200 |
| TC02 | GET /blog | Chỉ trả published | 200 |
| TC03 | GET /blog | Phân trang per_page=5 | 200 |
| TC04 | GET /blog | Trang 2 | 200 |
| TC05 | GET /blog | Filter category_id | 200 |
| TC06 | GET /blog | category_id không có bài / không tồn tại | 200/422 |
| TC07 | GET /blog | category_id không phải số | 422 |
| TC08 | GET /blog | per_page vượt max | 200/422 |
| TC09 | GET /blog | Không cần token | 200 |
| TC10 | GET /blog/{slug} | Chi tiết thành công | 200 |
| TC11 | GET /blog/{slug} | view_count tăng | 200 |
| TC12 | GET /blog/{slug} | Không cần token | 200 |
| TC13 | GET /blog/{slug} | Slug không tồn tại | 404 |
| TC14 | GET /blog/{slug} | Bài draft | 404/403 |
| TC15 | GET /blog/categories | Lấy danh mục | 200 |
| TC16 | GET /blog/categories | Không cần token | 200 |
| TC17 | POST /admin/blog | Tạo draft | 200/201 |
| TC18 | POST /admin/blog | Tạo published | 200/201 |
| TC19 | POST /admin/blog | Đầy đủ fields | 200/201 |
| TC20 | POST /admin/blog | Nhiều category_ids | 200/201 |
| TC21 | POST /admin/blog | Thiếu title | 422 |
| TC22 | POST /admin/blog | Thiếu content | 422 |
| TC23 | POST /admin/blog | status sai | 422 |
| TC24 | POST /admin/blog | category_ids không tồn tại | 422/404 |
| TC25 | POST /admin/blog | User thường | 403 |
| TC26 | POST /admin/blog | Không có token | 401 |
| TC27 | PUT /admin/blog/{id} | Cập nhật title | 200 |
| TC28 | PUT /admin/blog/{id} | Cập nhật content | 200 |
| TC29 | PUT /admin/blog/{id} | Cập nhật category_ids | 200 |
| TC30 | PUT /admin/blog/{id} | category_ids rỗng | 200/422 |
| TC31 | PUT /admin/blog/{id} | ID không tồn tại | 404 |
| TC32 | PUT /admin/blog/{id} | status sai | 422 |
| TC33 | PUT /admin/blog/{id} | User thường | 403 |
| TC34 | PUT /admin/blog/{id} | Không có token | 401 |
| TC35 | DELETE /admin/blog/{id} | Xóa thành công | 200/204 |
| TC36 | DELETE /admin/blog/{id} | ID không tồn tại | 404 |
| TC37 | DELETE /admin/blog/{id} | User thường | 403 |
| TC38 | DELETE /admin/blog/{id} | Không có token | 401 |
| TC39 | PATCH .../publish | Draft → Published | 200 |
| TC40 | PATCH .../publish | Published → Draft | 200 |
| TC41 | PATCH .../publish | Idempotent | 200 |
| TC42 | PATCH .../publish | status sai | 422 |
| TC43 | PATCH .../publish | Thiếu status | 422 |
| TC44 | PATCH .../publish | ID không tồn tại | 404 |
| TC45 | PATCH .../publish | User thường | 403 |
| TC46 | PATCH .../publish | Không có token | 401 |
