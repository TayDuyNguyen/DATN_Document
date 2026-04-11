# Test Cases — NOTIFICATIONS (Thông báo)

> Base URL: `http://localhost:8000/api/v1`
> Branch: `feat/taynd/api-notifications`
> 🔐 User token | 🛡️ Admin token
> Bảng DB: `notifications` (id, user_id, type, title, content, data, is_read, read_at, created_at)

---

## 1. GET /user/notifications — Danh sách thông báo

### ✅ TC01 — Lấy danh sách thành công
```http
GET /api/v1/user/notifications
Authorization: Bearer {user_token}
```
- Expected: `200 OK`
- Verify: `data` là array, mỗi item có fields: `id`, `type`, `title`, `content`, `is_read`, `created_at`

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
- Verify: `created_at` item đầu >= item cuối (DESC order)

### ✅ TC07 — `per_page` vượt max
```http
GET /api/v1/user/notifications?per_page=200
```
- Expected: `200 OK` hoặc `422 Unprocessable`
- Nếu 200: verify số item trả về <= 100

### ❌ TC08 — Không có token
```http
GET /api/v1/user/notifications
```
- Expected: `401 Unauthorized`

---

## 2. GET /user/notifications/unread-count — Số thông báo chưa đọc

### ✅ TC09 — Lấy unread count thành công
```http
GET /api/v1/user/notifications/unread-count
Authorization: Bearer {user_token}
```
- Expected: `200 OK`
- Verify: response có field `count` (hoặc `unread_count`) là số nguyên >= 0

### ✅ TC10 — Count khớp với danh sách chưa đọc
```http
GET /api/v1/user/notifications/unread-count
GET /api/v1/user/notifications?is_read=0
```
- Expected: `200 OK`
- Verify: `count` từ unread-count == tổng số item từ filter `is_read=0`

### ✅ TC11 — Count = 0 sau khi mark all read
```http
PATCH /api/v1/user/notifications/read-all
GET  /api/v1/user/notifications/unread-count
```
- Expected: `200 OK`, `count = 0`

### ❌ TC12 — Không có token
```http
GET /api/v1/user/notifications/unread-count
```
- Expected: `401 Unauthorized`

---

## 3. PATCH /user/notifications/{id}/read — Đánh dấu đã đọc 1 thông báo

### ✅ TC13 — Đánh dấu đã đọc thành công (thông báo chưa đọc)
```http
PATCH /api/v1/user/notifications/{id_chua_doc}/read
Authorization: Bearer {user_token}
```
- Expected: `200 OK`
- Verify: `is_read = true`, `read_at` không null

### ✅ TC14 — Đánh dấu đã đọc lại (idempotent)
```http
PATCH /api/v1/user/notifications/{id_da_doc}/read
```
- Expected: `200 OK` (không lỗi)
- Verify: `is_read` vẫn là `true`

### ❌ TC15 — ID không tồn tại
```http
PATCH /api/v1/user/notifications/99999/read
```
- Expected: `404 Not Found` hoặc `422 Unprocessable`

### ❌ TC16 — ID không hợp lệ (chuỗi)
```http
PATCH /api/v1/user/notifications/abc/read
```
- Expected: `404 Not Found` hoặc `422 Unprocessable`

### ❌ TC17 — Đánh dấu thông báo của user khác
```http
PATCH /api/v1/user/notifications/{id_cua_user_khac}/read
Authorization: Bearer {user1_token}
```
- Expected: `403 Forbidden` hoặc `404 Not Found`

### ❌ TC18 — Không có token
```http
PATCH /api/v1/user/notifications/{id}/read
```
- Expected: `401 Unauthorized`

---

## 4. PATCH /user/notifications/read-all — Đánh dấu tất cả đã đọc

### ✅ TC19 — Đánh dấu tất cả đã đọc thành công
```http
PATCH /api/v1/user/notifications/read-all
Authorization: Bearer {user_token}
```
- Expected: `200 OK`
- Verify: sau khi gọi, `GET /user/notifications?is_read=0` trả về `data = []`
- Verify: `GET /user/notifications/unread-count` trả về `count = 0`

### ✅ TC20 — Gọi khi không có thông báo chưa đọc (idempotent)
```http
PATCH /api/v1/user/notifications/read-all
```
- Expected: `200 OK` (không lỗi dù không có gì để cập nhật)

### ❌ TC21 — Không có token
```http
PATCH /api/v1/user/notifications/read-all
```
- Expected: `401 Unauthorized`

---

## 5. DELETE /user/notifications/{id} — Xóa thông báo (user)

### ✅ TC22 — Xóa thông báo chưa đọc thành công
```http
DELETE /api/v1/user/notifications/{id_chua_doc}
Authorization: Bearer {user_token}
```
- Expected: `200 OK` hoặc `204 No Content`
- Verify: GET lại ID đó → `404 Not Found`

### ✅ TC23 — Xóa thông báo đã đọc thành công
```http
DELETE /api/v1/user/notifications/{id_da_doc}
```
- Expected: `200 OK` hoặc `204 No Content`

### ❌ TC24 — Xóa ID không tồn tại
```http
DELETE /api/v1/user/notifications/99999
```
- Expected: `404 Not Found` hoặc `422 Unprocessable`

### ❌ TC25 — Xóa thông báo của user khác
```http
DELETE /api/v1/user/notifications/{id_cua_user_khac}
Authorization: Bearer {user1_token}
```
- Expected: `403 Forbidden` hoặc `404 Not Found`

### ❌ TC26 — Không có token
```http
DELETE /api/v1/user/notifications/{id}
```
- Expected: `401 Unauthorized`

---

## 6. GET /admin/notifications — Danh sách thông báo hệ thống

### ✅ TC27 — Lấy tất cả thông báo
```http
GET /api/v1/admin/notifications
Authorization: Bearer {admin_token}
```
- Expected: `200 OK`
- Verify: `data` là array, có thông báo của nhiều user

### ✅ TC28 — Filter theo `user_id`
```http
GET /api/v1/admin/notifications?user_id={id}
```
- Expected: `200 OK`
- Verify: tất cả item có `user_id` khớp

### ✅ TC29 — Filter theo `type`
```http
GET /api/v1/admin/notifications?type=booking
```
- Expected: `200 OK`
- Verify: tất cả item có `type = booking`

### ✅ TC30 — Phân trang `per_page=10`
```http
GET /api/v1/admin/notifications?page=1&per_page=10
```
- Expected: `200 OK`, `data` có tối đa 10 phần tử

### ❌ TC31 — User thường bị 403
```http
GET /api/v1/admin/notifications
Authorization: Bearer {user_token}
```
- Expected: `403 Forbidden`

### ❌ TC32 — Không có token
```http
GET /api/v1/admin/notifications
```
- Expected: `401 Unauthorized`

---

## 7. POST /admin/notifications/send — Gửi thông báo đến 1 user

### ✅ TC33 — Gửi đầy đủ fields
```http
POST /api/v1/admin/notifications/send
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "user_id": 1,
  "type": "system",
  "title": "Thông báo test",
  "content": "Nội dung thông báo",
  "data": { "url": "/tours/1" }
}
```
- Expected: `200 OK` hoặc `201 Created`
- Verify: notification xuất hiện trong `GET /user/notifications` của user đó

### ✅ TC34 — Gửi chỉ fields bắt buộc (không có `content`, `data`)
```http
{
  "user_id": 1,
  "type": "system",
  "title": "Thông báo tối giản"
}
```
- Expected: `200 OK` hoặc `201 Created`

### ❌ TC35 — Thiếu `user_id`
```json
{ "type": "system", "title": "Test" }
```
- Expected: `422 Unprocessable`

### ❌ TC36 — Thiếu `type`
```json
{ "user_id": 1, "title": "Test" }
```
- Expected: `422 Unprocessable`

### ❌ TC37 — Thiếu `title`
```json
{ "user_id": 1, "type": "system" }
```
- Expected: `422 Unprocessable`

### ❌ TC38 — `user_id` không tồn tại
```json
{ "user_id": 99999, "type": "system", "title": "Test" }
```
- Expected: `404 Not Found` hoặc `422 Unprocessable`

### ❌ TC39 — User thường bị 403
```http
POST /api/v1/admin/notifications/send
Authorization: Bearer {user_token}
```
- Expected: `403 Forbidden`

### ❌ TC40 — Không có token
- Expected: `401 Unauthorized`

---

## 8. POST /admin/notifications/send-all — Gửi thông báo đến tất cả user

### ✅ TC41 — Gửi đầy đủ fields
```http
POST /api/v1/admin/notifications/send-all
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "type": "system",
  "title": "Thông báo toàn hệ thống",
  "content": "Nội dung broadcast",
  "data": {}
}
```
- Expected: `200 OK` hoặc `201 Created`
- Verify: nhiều user nhận được thông báo

### ✅ TC42 — Gửi chỉ fields bắt buộc
```json
{ "type": "system", "title": "Broadcast tối giản" }
```
- Expected: `200 OK` hoặc `201 Created`

### ❌ TC43 — Thiếu `type`
```json
{ "title": "Test broadcast" }
```
- Expected: `422 Unprocessable`

### ❌ TC44 — Thiếu `title`
```json
{ "type": "system" }
```
- Expected: `422 Unprocessable`

### ❌ TC45 — User thường bị 403
```http
POST /api/v1/admin/notifications/send-all
Authorization: Bearer {user_token}
```
- Expected: `403 Forbidden`

### ❌ TC46 — Không có token
- Expected: `401 Unauthorized`

---

## 9. DELETE /admin/notifications/{id} — Xóa thông báo (admin)

### ✅ TC47 — Admin xóa thông báo thành công
```http
DELETE /api/v1/admin/notifications/{id}
Authorization: Bearer {admin_token}
```
- Expected: `200 OK` hoặc `204 No Content`
- Verify: GET lại ID đó → `404 Not Found`

### ❌ TC48 — ID không tồn tại
```http
DELETE /api/v1/admin/notifications/99999
```
- Expected: `404 Not Found` hoặc `422 Unprocessable`

### ❌ TC49 — User thường bị 403
```http
DELETE /api/v1/admin/notifications/{id}
Authorization: Bearer {user_token}
```
- Expected: `403 Forbidden`

### ❌ TC50 — Không có token
```http
DELETE /api/v1/admin/notifications/{id}
```
- Expected: `401 Unauthorized`

---

## Tổng kết

| TC | API | Trường hợp | Expected |
|----|-----|-----------|----------|
| TC01 | GET /user/notifications | Lấy danh sách | 200 |
| TC02 | GET /user/notifications | Phân trang per_page=5 | 200 |
| TC03 | GET /user/notifications | Trang 2 | 200 |
| TC04 | GET /user/notifications | Filter is_read=0 | 200 |
| TC05 | GET /user/notifications | Filter is_read=1 | 200 |
| TC06 | GET /user/notifications | Sắp xếp mới nhất | 200 |
| TC07 | GET /user/notifications | per_page vượt max | 200/422 |
| TC08 | GET /user/notifications | Không có token | 401 |
| TC09 | GET /user/notifications/unread-count | Lấy count | 200 |
| TC10 | GET /user/notifications/unread-count | Count khớp danh sách | 200 |
| TC11 | GET /user/notifications/unread-count | Count=0 sau read-all | 200 |
| TC12 | GET /user/notifications/unread-count | Không có token | 401 |
| TC13 | PATCH .../{id}/read | Đánh dấu đã đọc | 200 |
| TC14 | PATCH .../{id}/read | Idempotent | 200 |
| TC15 | PATCH .../{id}/read | ID không tồn tại | 404/422 |
| TC16 | PATCH .../{id}/read | ID không hợp lệ | 404/422 |
| TC17 | PATCH .../{id}/read | Thông báo user khác | 403/404 |
| TC18 | PATCH .../{id}/read | Không có token | 401 |
| TC19 | PATCH /read-all | Đánh dấu tất cả đã đọc | 200 |
| TC20 | PATCH /read-all | Idempotent | 200 |
| TC21 | PATCH /read-all | Không có token | 401 |
| TC22 | DELETE /user/notifications/{id} | Xóa chưa đọc | 200/204 |
| TC23 | DELETE /user/notifications/{id} | Xóa đã đọc | 200/204 |
| TC24 | DELETE /user/notifications/{id} | ID không tồn tại | 404/422 |
| TC25 | DELETE /user/notifications/{id} | Thông báo user khác | 403/404 |
| TC26 | DELETE /user/notifications/{id} | Không có token | 401 |
| TC27 | GET /admin/notifications | Lấy tất cả | 200 |
| TC28 | GET /admin/notifications | Filter user_id | 200 |
| TC29 | GET /admin/notifications | Filter type | 200 |
| TC30 | GET /admin/notifications | Phân trang | 200 |
| TC31 | GET /admin/notifications | User thường | 403 |
| TC32 | GET /admin/notifications | Không có token | 401 |
| TC33 | POST /admin/notifications/send | Đầy đủ fields | 200/201 |
| TC34 | POST /admin/notifications/send | Chỉ fields bắt buộc | 200/201 |
| TC35 | POST /admin/notifications/send | Thiếu user_id | 422 |
| TC36 | POST /admin/notifications/send | Thiếu type | 422 |
| TC37 | POST /admin/notifications/send | Thiếu title | 422 |
| TC38 | POST /admin/notifications/send | user_id không tồn tại | 404/422 |
| TC39 | POST /admin/notifications/send | User thường | 403 |
| TC40 | POST /admin/notifications/send | Không có token | 401 |
| TC41 | POST /admin/notifications/send-all | Đầy đủ fields | 200/201 |
| TC42 | POST /admin/notifications/send-all | Chỉ fields bắt buộc | 200/201 |
| TC43 | POST /admin/notifications/send-all | Thiếu type | 422 |
| TC44 | POST /admin/notifications/send-all | Thiếu title | 422 |
| TC45 | POST /admin/notifications/send-all | User thường | 403 |
| TC46 | POST /admin/notifications/send-all | Không có token | 401 |
| TC47 | DELETE /admin/notifications/{id} | Admin xóa thành công | 200/204 |
| TC48 | DELETE /admin/notifications/{id} | ID không tồn tại | 404/422 |
| TC49 | DELETE /admin/notifications/{id} | User thường | 403 |
| TC50 | DELETE /admin/notifications/{id} | Không có token | 401 |

**Tổng: 50 test cases** — 25 happy path ✅ · 25 error case ❌
