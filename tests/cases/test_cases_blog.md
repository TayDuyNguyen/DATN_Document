# Test Cases — BLOG (Bài viết)

> Base URL: `http://localhost:8000/api/v1`
> Branch: `feat/taynd/api-blog`
> 🌐 Public | 🛡️ Admin token bắt buộc cho write operations

---

## 1. GET /blog — Danh sách bài viết (Public)

### ✅ TC01 — Lấy danh sách thành công
```http
GET /api/v1/blog
```
- Expected: `200 OK`, `data` là array, mỗi item có `id`, `title`, `slug`, `excerpt`, `status`, `published_at`

### ✅ TC02 — Chỉ trả về bài `published`
- Expected: `200 OK`, tất cả item có `status = published`

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

### ✅ TC05 — Filter theo `category_id`
```http
GET /api/v1/blog?category_id=1
```
- Expected: `200 OK`

### ✅ TC06 — `category_id` không có bài nào
```http
GET /api/v1/blog?category_id=99999
```
- Expected: `200 OK` (data=[]) hoặc `422 Unprocessable`

### ❌ TC07 — `category_id` không phải số
```http
GET /api/v1/blog?category_id=abc
```
- Expected: `422 Unprocessable`

### ✅ TC08 — `per_page` vượt max
```http
GET /api/v1/blog?per_page=200
```
- Expected: `200 OK` hoặc `422 Unprocessable`

### ✅ TC09 — Không cần token (public)
- Expected: `200 OK`

---

## 2. GET /blog/{slug} — Chi tiết bài viết (Public)

### ✅ TC10 — Lấy chi tiết thành công
```http
GET /api/v1/blog/{slug_hop_le}
```
- Expected: `200 OK`, có `id`, `title`, `slug`, `content`, `view_count`, `published_at`

### ✅ TC11 — `view_count` tăng sau mỗi lần xem
- Expected: `200 OK`, `view_count` lần 2 >= lần 1

### ✅ TC12 — Không cần token (public)
- Expected: `200 OK`

### ❌ TC13 — Slug không tồn tại
```http
GET /api/v1/blog/slug-khong-ton-tai-xyz-999
```
- Expected: `404 Not Found`

### ❌ TC14 — Bài viết `draft` không hiển thị public
- Expected: `404 Not Found` hoặc `403 Forbidden`

---

## 3. GET /blog/categories — Danh mục blog (Public)

### ✅ TC15 — Lấy danh sách danh mục thành công
```http
GET /api/v1/blog/categories
```
- Expected: `200 OK`, mỗi item có `id`, `name`, `slug`

### ✅ TC16 — Không cần token (public)
- Expected: `200 OK`

---

## 4. GET /admin/blog-posts — Danh sách bài viết (Admin)

### ✅ TC17 — Lấy tất cả (kể cả draft)
```http
GET /api/v1/admin/blog-posts
Authorization: Bearer {admin_token}
```
- Expected: `200 OK`, có cả bài `draft` và `published`

### ✅ TC18 — Filter `status=draft`
```http
GET /api/v1/admin/blog-posts?status=draft
```
- Expected: `200 OK`, tất cả item có `status=draft`

### ✅ TC19 — Filter `status=published`
```http
GET /api/v1/admin/blog-posts?status=published
```
- Expected: `200 OK`

### ✅ TC20 — Filter `category_id`
```http
GET /api/v1/admin/blog-posts?category_id=1
```
- Expected: `200 OK`

### ✅ TC21 — Phân trang
```http
GET /api/v1/admin/blog-posts?page=1&per_page=5
```
- Expected: `200 OK`, `data` có tối đa 5 phần tử

### ❌ TC22 — User thường bị 403
- Expected: `403 Forbidden`

### ❌ TC23 — Không có token → 401
- Expected: `401 Unauthorized`

---

## 5. POST /admin/blog-posts — Tạo bài viết (Admin)

### ✅ TC24 — Tạo bài viết `draft`
```json
{ "title": "Bài viết test draft", "content": "Nội dung", "status": "draft" }
```
- Expected: `200 OK` hoặc `201 Created`
- Verify: `slug` tự sinh từ `title`, `status=draft`

### ✅ TC25 — Tạo bài viết `published`
```json
{ "title": "Bài viết published", "content": "Nội dung", "status": "published" }
```
- Expected: `200 OK` hoặc `201 Created`
- Verify: `published_at` không null

### ✅ TC26 — Tạo với đầy đủ fields
```json
{
  "title": "Bài viết đầy đủ",
  "content": "Nội dung chi tiết",
  "excerpt": "Tóm tắt",
  "featured_image": "https://example.com/image.jpg",
  "category_ids": [1],
  "status": "draft"
}
```
- Expected: `200 OK` hoặc `201 Created`

### ✅ TC27 — Tạo với nhiều `category_ids`
```json
{ "title": "Test", "content": "Test", "category_ids": [1, 2], "status": "draft" }
```
- Expected: `200 OK` hoặc `201 Created`

### ❌ TC28 — Thiếu `title`
```json
{ "content": "Nội dung", "status": "draft" }
```
- Expected: `422 Unprocessable`

### ❌ TC29 — Thiếu `content`
```json
{ "title": "Tiêu đề", "status": "draft" }
```
- Expected: `422 Unprocessable`

### ❌ TC30 — `status` sai giá trị
```json
{ "title": "Test", "content": "Test", "status": "invalid_status" }
```
- Expected: `422 Unprocessable`

### ❌ TC31 — `category_ids` chứa ID không tồn tại
```json
{ "title": "Test", "content": "Test", "category_ids": [99999], "status": "draft" }
```
- Expected: `422 Unprocessable` hoặc `404 Not Found`

### ❌ TC32 — User thường bị 403
- Expected: `403 Forbidden`

### ❌ TC33 — Không có token → 401
- Expected: `401 Unauthorized`

---

## 6. GET /admin/blog-posts/{id} — Chi tiết bài viết (Admin)

### ✅ TC34 — Lấy chi tiết thành công
```http
GET /api/v1/admin/blog-posts/{id}
```
- Expected: `200 OK`, có đầy đủ fields kể cả `content`

### ❌ TC35 — ID không tồn tại
```http
GET /api/v1/admin/blog-posts/99999
```
- Expected: `404 Not Found` hoặc `422 Unprocessable`

### ❌ TC36 — Không có token → 401
- Expected: `401 Unauthorized`

---

## 7. PUT /admin/blog-posts/{id} — Cập nhật bài viết (Admin)

### ✅ TC37 — Cập nhật `title`
```json
{ "title": "Tiêu đề đã cập nhật" }
```
- Expected: `200 OK`, `title` thay đổi

### ✅ TC38 — Cập nhật `content`
```json
{ "content": "Nội dung mới" }
```
- Expected: `200 OK`

### ✅ TC39 — Cập nhật `category_ids` (sync)
```json
{ "category_ids": [2] }
```
- Expected: `200 OK`

### ❌ TC40 — ID không tồn tại
- Expected: `404 Not Found` hoặc `422 Unprocessable`

### ❌ TC41 — `status` sai giá trị
```json
{ "status": "invalid_status" }
```
- Expected: `422 Unprocessable`

### ❌ TC42 — User thường bị 403
- Expected: `403 Forbidden`

### ❌ TC43 — Không có token → 401
- Expected: `401 Unauthorized`

---

## 8. DELETE /admin/blog-posts/{id} — Xóa bài viết (Admin)

### ✅ TC44 — Xóa thành công
```http
DELETE /api/v1/admin/blog-posts/{id}
```
- Expected: `200 OK` hoặc `204 No Content`
- Verify: GET `/blog/{slug}` → `404 Not Found`

### ❌ TC45 — ID không tồn tại
- Expected: `404 Not Found` hoặc `422 Unprocessable`

### ❌ TC46 — User thường bị 403
- Expected: `403 Forbidden`

### ❌ TC47 — Không có token → 401
- Expected: `401 Unauthorized`

---

## 9. PATCH /admin/blog-posts/{id}/status — Đổi trạng thái (Admin)

### ✅ TC48 — Draft → Published
```json
{ "status": "published" }
```
- Expected: `200 OK`, `status=published`, `published_at` không null

### ✅ TC49 — Published → Draft
```json
{ "status": "draft" }
```
- Expected: `200 OK`, `status=draft`

### ✅ TC50 — Published → Archived
```json
{ "status": "archived" }
```
- Expected: `200 OK`, `status=archived`

### ✅ TC51 — Idempotent (published → published)
```json
{ "status": "published" }
```
- Expected: `200 OK`

### ❌ TC52 — `status` sai giá trị
```json
{ "status": "invalid_status" }
```
- Expected: `422 Unprocessable`

### ❌ TC53 — Thiếu `status`
```json
{}
```
- Expected: `422 Unprocessable`

### ❌ TC54 — ID không tồn tại
- Expected: `404 Not Found` hoặc `422 Unprocessable`

### ❌ TC55 — User thường bị 403
- Expected: `403 Forbidden`

### ❌ TC56 — Không có token → 401
- Expected: `401 Unauthorized`

---

## 10. Admin Blog Categories CRUD

### ✅ TC57 — GET /admin/blog-categories — Lấy danh sách
- Expected: `200 OK`

### ✅ TC58 — POST /admin/blog-categories — Tạo danh mục
```json
{ "name": "Danh mục test", "description": "Mô tả" }
```
- Expected: `200 OK` hoặc `201 Created`

### ✅ TC59 — PUT /admin/blog-categories/{id} — Cập nhật
```json
{ "name": "Danh mục đã cập nhật" }
```
- Expected: `200 OK`

### ❌ TC60 — POST thiếu `name` → 422
- Expected: `422 Unprocessable`

### ✅ TC61 — DELETE /admin/blog-categories/{id} — Xóa
- Expected: `200 OK` hoặc `204 No Content`

### ❌ TC62 — DELETE ID không tồn tại → 404/422
- Expected: `404 Not Found` hoặc `422 Unprocessable`

### ❌ TC63 — User thường bị 403
- Expected: `403 Forbidden`

### ❌ TC64 — Không có token → 401
- Expected: `401 Unauthorized`

---

## Tổng kết

| TC | API | Trường hợp | Expected |
|----|-----|-----------|----------|
| TC01–TC09 | GET /blog | List, filter, paginate, public | 200/422 |
| TC10–TC14 | GET /blog/{slug} | Detail, view_count, draft, 404 | 200/404 |
| TC15–TC16 | GET /blog/categories | Public list | 200 |
| TC17–TC23 | GET /admin/blog-posts | Admin list, filter, auth | 200/403/401 |
| TC24–TC33 | POST /admin/blog-posts | Create, validation, auth | 200/201/422/403/401 |
| TC34–TC36 | GET /admin/blog-posts/{id} | Detail, 404, auth | 200/404/401 |
| TC37–TC43 | PUT /admin/blog-posts/{id} | Update, validation, auth | 200/422/403/401 |
| TC44–TC47 | DELETE /admin/blog-posts/{id} | Delete, 404, auth | 200/204/403/401 |
| TC48–TC56 | PATCH .../status | Status transitions, validation | 200/422/403/401 |
| TC57–TC64 | Admin blog-categories | CRUD, auth | 200/201/422/403/401 |

**Tổng: 64 test cases** — 30 happy path ✅ · 34 error case ❌
