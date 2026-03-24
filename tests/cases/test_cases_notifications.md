# Test Cases — NOTIFICATIONS (Thông báo)

> Base URL: `http://localhost:8000/api/v1`
> 🔐 User token cần thiết cho tất cả endpoints
> Bảng DB: `notifications` (fields: id, user_id, type, title, content, data, is_read, read_at, created_at)

---

## 1. GET /user/notifications — Danh sách thông báo

### ✅ TC01 — Lấy danh sách thành công
```http
GET /api/v1/user/notifications
```
- Expected: `200 OK`
- Verify: response có `data` là array, mỗi item có fields: `id`, `type`, `title`, `content`, `is_read`, `created_at`

### ✅ TC02 — Phân trang `per_page=5`
```http
GET /api/v1/user/notifications?page=1&per_page=5
```
- Expected: `200 OK`, `data` có tối đa 5 phần tử

### ✅ TC03 — Trang 2
```http
GET /api/v1/user/notifications?page=2&per_page=5
```
- Expected: `200 OK`

### ✅ TC03b — `per_page` vượt max
```http
GET /api/v1/user/notifications?per_page=200
```
- Expected: `200 OK` hoặc `422 Unprocessable`
- Nếu 422: backend validate đúng (`per_page` max 100)
- Nếu 200: verify số item trả về <= 100

### ✅ TC04 — Filter `is_read=0` (chưa đọc)
```http
GET /api/v1/user/notifications?is_read=0
```
- Expected: `200 OK`
- Verify: tất cả item trả về có `is_read = false` hoặc `0`

### ✅ TC05 — Filter `is_read=1` (đã đọc)
```http
GET /api/v1/user/notifications?is_read=1
```
- Expected: `200 OK`
- Verify: tất cả item trả về có `is_read = true` hoặc `1`

### ✅ TC06 — Sắp xếp mới nhất lên đầu
```http
GET /api/v1/user/notifications
```
- Expected: `200 OK`
- Verify: `created_at` của item đầu >= item cuối (DESC order)

### ❌ TC07 — Không có token
```http
GET /api/v1/user/notifications
```
- Expected: `401 Unauthorized`

---

## 2. PATCH /user/notifications/{id}/read — Đánh dấu đã đọc 1 thông báo

### ✅ TC08 — Đánh dấu đã đọc thành công (thông báo chưa đọc)
```http
PATCH /api/v1/user/notifications/{id_chua_doc}/read
```
- Expected: `200 OK`
- Verify: `is_read = true`, `read_at` không null

### ✅ TC09 — Đánh dấu đã đọc lại (thông báo đã đọc rồi — idempotent)
```http
PATCH /api/v1/user/notifications/{id_da_doc}/read
```
- Expected: `200 OK` (không lỗi, idempotent)
- Verify: `is_read` vẫn là `true`

### ❌ TC10 — ID không tồn tại
```http
PATCH /api/v1/user/notifications/99999/read
```
- Expected: `404 Not Found`

### ❌ TC11 — ID là chuỗi không hợp lệ
```http
PATCH /api/v1/user/notifications/abc/read
```
- Expected: `404 Not Found` hoặc `422 Unprocessable`

### ❌ TC12 — Đánh dấu thông báo của user khác
```http
PATCH /api/v1/user/notifications/{id_cua_user_khac}/read
```
- Expected: `403 Forbidden` hoặc `404 Not Found`

### ❌ TC13 — Không có token
```http
PATCH /api/v1/user/notifications/{id}/read
```
- Expected: `401 Unauthorized`

---

## 3. PATCH /user/notifications/read-all — Đánh dấu tất cả đã đọc

### ✅ TC14 — Đánh dấu tất cả đã đọc thành công
```http
PATCH /api/v1/user/notifications/read-all
```
- Expected: `200 OK`
- Verify: sau khi gọi, `GET /user/notifications?is_read=0` trả về `data = []`

### ✅ TC15 — Gọi khi không có thông báo chưa đọc (idempotent)
```http
PATCH /api/v1/user/notifications/read-all
```
- Expected: `200 OK` (không lỗi dù không có gì để cập nhật)

### ❌ TC16 — Không có token
```http
PATCH /api/v1/user/notifications/read-all
```
- Expected: `401 Unauthorized`

---

## 4. DELETE /user/notifications/{id} — Xóa thông báo

### ✅ TC17 — Xóa thông báo chưa đọc thành công
```http
DELETE /api/v1/user/notifications/{id_chua_doc}
```
- Expected: `200 OK` hoặc `204 No Content`
- Verify: GET lại ID đó → `404 Not Found`

### ✅ TC18 — Xóa thông báo đã đọc thành công
```http
DELETE /api/v1/user/notifications/{id_da_doc}
```
- Expected: `200 OK` hoặc `204 No Content`

### ❌ TC19 — Xóa ID không tồn tại
```http
DELETE /api/v1/user/notifications/99999
```
- Expected: `404 Not Found`

### ❌ TC20 — Xóa thông báo của user khác
```http
DELETE /api/v1/user/notifications/{id_cua_user_khac}
```
- Expected: `403 Forbidden` hoặc `404 Not Found`

### ❌ TC21 — Không có token
```http
DELETE /api/v1/user/notifications/{id}
```
- Expected: `401 Unauthorized`

---

## Tổng kết

| TC | API | Trường hợp | Expected |
|----|-----|-----------|----------|
| TC01 | GET /user/notifications | Lấy danh sách | 200 |
| TC02 | GET /user/notifications | Phân trang per_page=5 | 200 |
| TC03 | GET /user/notifications | Trang 2 | 200 |
| TC03b | GET /user/notifications | per_page vượt max | 200 |
| TC04 | GET /user/notifications | Filter is_read=0 | 200 |
| TC05 | GET /user/notifications | Filter is_read=1 | 200 |
| TC06 | GET /user/notifications | Sắp xếp mới nhất | 200 |
| TC07 | GET /user/notifications | Không có token | 401 |
| TC08 | PATCH .../read | Đánh dấu đã đọc (chưa đọc) | 200 |
| TC09 | PATCH .../read | Đánh dấu đã đọc lại (idempotent) | 200 |
| TC10 | PATCH .../read | ID không tồn tại | 404 |
| TC11 | PATCH .../read | ID không hợp lệ | 404/422 |
| TC12 | PATCH .../read | Thông báo của user khác | 403/404 |
| TC13 | PATCH .../read | Không có token | 401 |
| TC14 | PATCH /read-all | Đánh dấu tất cả đã đọc | 200 |
| TC15 | PATCH /read-all | Không có gì chưa đọc (idempotent) | 200 |
| TC16 | PATCH /read-all | Không có token | 401 |
| TC17 | DELETE .../{id} | Xóa thông báo chưa đọc | 200/204 |
| TC18 | DELETE .../{id} | Xóa thông báo đã đọc | 200/204 |
| TC19 | DELETE .../{id} | ID không tồn tại | 404 |
| TC20 | DELETE .../{id} | Thông báo của user khác | 403/404 |
| TC21 | DELETE .../{id} | Không có token | 401 |
