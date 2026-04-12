# Test Cases — CONTACTS (Liên hệ)

> Base URL: `http://localhost:8000/api/v1`
> Branch: `feat/taynd/api-contacts`
> 🌐 Public: POST /contacts | 🛡️ Admin token cho tất cả /admin/contacts

---

## 1. POST /contacts — Gửi form liên hệ (Public)

### ✅ TC01 — Gửi đầy đủ fields
```json
{ "name": "Nguyen Van A", "email": "test@example.com", "phone": "0901234567", "subject": "Hoi ve tour", "message": "Toi muon hoi ve tour Ba Na Hills" }
```
- Expected: `200 OK` hoặc `201 Created`
- Verify: response có `id` hoặc message thành công

### ✅ TC02 — Gửi chỉ fields bắt buộc (không có phone, subject)
```json
{ "name": "Nguyen Van B", "email": "test2@example.com", "message": "Noi dung lien he" }
```
- Expected: `200 OK` hoặc `201 Created`

### ✅ TC03 — Không cần token (public)
- Expected: `200 OK` hoặc `201 Created`

### ❌ TC04 — Thiếu `name` → 422
```json
{ "email": "test@example.com", "message": "Noi dung" }
```
- Expected: `422 Unprocessable`

### ❌ TC05 — Thiếu `email` → 422
```json
{ "name": "Test", "message": "Noi dung" }
```
- Expected: `422 Unprocessable`

### ❌ TC06 — Thiếu `message` → 422
```json
{ "name": "Test", "email": "test@example.com" }
```
- Expected: `422 Unprocessable`

### ❌ TC07 — `email` sai định dạng → 422
```json
{ "name": "Test", "email": "not-an-email", "message": "Noi dung" }
```
- Expected: `422 Unprocessable`

### ❌ TC08 — `message` quá ngắn (nếu có min length)
```json
{ "name": "Test", "email": "test@example.com", "message": "Hi" }
```
- Expected: `200 OK` hoặc `422 Unprocessable`

---

## 2. GET /admin/contacts — Danh sách liên hệ (Admin)

### ✅ TC09 — Lấy tất cả liên hệ
```http
GET /api/v1/admin/contacts
Authorization: Bearer {admin_token}
```
- Expected: `200 OK`, `data` là array, mỗi item có `id`, `name`, `email`, `message`, `status`

### ✅ TC10 — Filter `status=new`
```http
GET /api/v1/admin/contacts?status=new
```
- Expected: `200 OK`, tất cả item có `status = new`

### ✅ TC11 — Filter `status=read`
```http
GET /api/v1/admin/contacts?status=read
```
- Expected: `200 OK`

### ✅ TC12 — Filter `status=replied`
```http
GET /api/v1/admin/contacts?status=replied
```
- Expected: `200 OK`

### ✅ TC13 — Phân trang `per_page=5`
```http
GET /api/v1/admin/contacts?page=1&per_page=5
```
- Expected: `200 OK`, `data` có tối đa 5 phần tử

### ❌ TC14 — `status` sai giá trị → 422
```http
GET /api/v1/admin/contacts?status=invalid_status
```
- Expected: `422 Unprocessable`

### ❌ TC15 — User thường bị 403
- Expected: `403 Forbidden`

### ❌ TC16 — Không có token → 401
- Expected: `401 Unauthorized`

---

## 3. GET /admin/contacts/{id} — Chi tiết liên hệ (Admin)

### ✅ TC17 — Lấy chi tiết thành công
```http
GET /api/v1/admin/contacts/{id}
```
- Expected: `200 OK`, có đầy đủ fields
- Verify: `status` tự động chuyển sang `read` sau khi xem

### ✅ TC18 — Status tự động chuyển sang `read`
- Gọi GET lần 2 → verify `status = read`

### ❌ TC19 — ID không tồn tại → 404/422
```http
GET /api/v1/admin/contacts/99999
```
- Expected: `404 Not Found` hoặc `422 Unprocessable`

### ❌ TC20 — User thường bị 403
- Expected: `403 Forbidden`

### ❌ TC21 — Không có token → 401
- Expected: `401 Unauthorized`

---

## 4. POST /admin/contacts/{id}/reply — Trả lời liên hệ (Admin)

### ✅ TC22 — Trả lời thành công
```json
{ "reply": "Cam on ban da lien he. Chung toi se phan hoi trong 24h." }
```
- Expected: `200 OK`
- Verify: `status = replied`, `reply` không null, `replied_at` không null

### ✅ TC23 — Trả lời lần 2 (backend không cho override)
```json
{ "reply": "Noi dung tra loi moi" }
```
- Expected: `200 OK` hoặc `400 Bad Request`
- Note: backend có thể không cho phép reply lần 2 → trả `400 "already replied"`

### ❌ TC24 — Thiếu `reply` → 422
```json
{}
```
- Expected: `422 Unprocessable`

### ❌ TC25 — `reply` rỗng → 422
```json
{ "reply": "" }
```
- Expected: `422 Unprocessable`

### ❌ TC26 — ID không tồn tại → 404/422
- Expected: `404 Not Found` hoặc `422 Unprocessable`

### ❌ TC27 — User thường bị 403
- Expected: `403 Forbidden`

### ❌ TC28 — Không có token → 401
- Expected: `401 Unauthorized`

---

## 5. DELETE /admin/contacts/{id} — Xóa liên hệ (Admin)

### ✅ TC29 — Xóa thành công
- Expected: `200 OK` hoặc `204 No Content`
- Verify: GET lại ID đó → `404 Not Found`

### ❌ TC30 — ID không tồn tại → 404/422
- Expected: `404 Not Found` hoặc `422 Unprocessable`

### ❌ TC31 — User thường bị 403
- Expected: `403 Forbidden`

### ❌ TC32 — Không có token → 401
- Expected: `401 Unauthorized`

---

## 6. GET /admin/contacts/export — Export Excel (Admin)

### ✅ TC33 — Export tất cả
```http
GET /api/v1/admin/contacts/export
```
- Expected: `200 OK`
- Verify: `Content-Type` là `application/vnd.openxmlformats...` (Excel)

### ✅ TC34 — Export filter `status=new`
```http
GET /api/v1/admin/contacts/export?status=new
```
- Expected: `200 OK`

### ✅ TC35 — Export filter `status=replied`
- Expected: `200 OK`

### ❌ TC36 — `status` sai giá trị → 422
- Expected: `422 Unprocessable`

### ❌ TC37 — User thường bị 403
- Expected: `403 Forbidden`

### ❌ TC38 — Không có token → 401
- Expected: `401 Unauthorized`

---

## Tổng kết

| TC | API | Trường hợp | Expected |
|----|-----|-----------|----------|
| TC01–TC08 | POST /contacts | Submit form, validation | 200/201/422 |
| TC09–TC16 | GET /admin/contacts | List, filter, paginate, auth | 200/422/403/401 |
| TC17–TC21 | GET /admin/contacts/{id} | Detail, auto-read, auth | 200/404/403/401 |
| TC22–TC28 | POST /admin/contacts/{id}/reply | Reply, validation, auth | 200/422/403/401 |
| TC29–TC32 | DELETE /admin/contacts/{id} | Delete, auth | 200/204/403/401 |
| TC33–TC38 | GET /admin/contacts/export | Export, filter, auth | 200/422/403/401 |

**Tổng: 38 test cases** — 17 happy path ✅ · 21 error case ❌
