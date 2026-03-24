# Test Cases — ADMIN USERS (Quản lý người dùng)

> Base URL: `http://localhost:8000/api/v1`
> 🛡️ Admin token bắt buộc cho tất cả endpoints

---

## 1. GET /admin/users — Danh sách người dùng

### ✅ TC01 — Lấy danh sách thành công
```http
GET /api/v1/admin/users
```
- Expected: `200 OK`
- Verify: response có `data` là array, mỗi item có `id`, `email`, `username`, `role`, `status`

### ✅ TC02 — Phân trang `per_page=5`
```http
GET /api/v1/admin/users?page=1&per_page=5
```
- Expected: `200 OK`, `data` có tối đa 5 phần tử

### ✅ TC03 — Trang 2
```http
GET /api/v1/admin/users?page=2&per_page=5
```
- Expected: `200 OK`

### ✅ TC04 — Search theo tên `?q=`
```http
GET /api/v1/admin/users?q=user
```
- Expected: `200 OK`
- Verify: tất cả item có `full_name` hoặc `email` chứa "user"

### ✅ TC05 — Search không có kết quả
```http
GET /api/v1/admin/users?q=xyzkhongtontai999
```
- Expected: `200 OK`, `data = []`

### ✅ TC06 — Filter `role=user`
```http
GET /api/v1/admin/users?role=user
```
- Expected: `200 OK`
- Verify: tất cả item có `role = user`

### ✅ TC07 — Filter `role=admin`
```http
GET /api/v1/admin/users?role=admin
```
- Expected: `200 OK`
- Verify: tất cả item có `role = admin`

### ✅ TC08 — Filter `status=active`
```http
GET /api/v1/admin/users?status=active
```
- Expected: `200 OK`
- Verify: tất cả item có `status = active`

### ✅ TC09 — Filter `status=banned`
```http
GET /api/v1/admin/users?status=banned
```
- Expected: `200 OK`
- Verify: tất cả item có `status = banned`

### ✅ TC10 — Kết hợp filter `role=user&status=active`
```http
GET /api/v1/admin/users?role=user&status=active
```
- Expected: `200 OK`
- Verify: tất cả item có `role=user` và `status=active`

### ❌ TC11 — `role` sai giá trị
```http
GET /api/v1/admin/users?role=superadmin
```
- Expected: `422 Unprocessable`

### ❌ TC12 — `status` sai giá trị
```http
GET /api/v1/admin/users?status=suspended
```
- Expected: `422 Unprocessable`

### ❌ TC13 — `per_page` vượt max
```http
GET /api/v1/admin/users?per_page=200
```
- Expected: `200 OK` hoặc `422 Unprocessable`

### ❌ TC14 — User thường không được truy cập
```http
GET /api/v1/admin/users
```
- Expected: `403 Forbidden`

### ❌ TC15 — Không có token
```http
GET /api/v1/admin/users
```
- Expected: `401 Unauthorized`

---

## 2. GET /admin/users/{id} — Chi tiết người dùng

### ✅ TC16 — Lấy chi tiết thành công
```http
GET /api/v1/admin/users/{id_hop_le}
```
- Expected: `200 OK`
- Verify: có fields `id`, `email`, `username`, `full_name`, `role`, `status`, `created_at`
- Verify: có thống kê `ratings_count` hoặc `point_transactions_count` (COUNT)

### ✅ TC17 — Lấy chi tiết admin user
```http
GET /api/v1/admin/users/{id_admin}
```
- Expected: `200 OK`
- Verify: `role = admin`

### ❌ TC18 — ID không tồn tại
```http
GET /api/v1/admin/users/99999
```
- Expected: `404 Not Found` hoặc `422 Unprocessable` (backend validate ID qua FormRequest)

### ❌ TC19 — User thường không được truy cập
```http
GET /api/v1/admin/users/{id}
```
- Expected: `403 Forbidden`

### ❌ TC20 — Không có token
```http
GET /api/v1/admin/users/{id}
```
- Expected: `401 Unauthorized`

---

## 3. PATCH /admin/users/{id}/status — Kích hoạt / Khóa tài khoản

### ✅ TC21 — Ban user `active` → `banned`
```json
{ "status": "banned" }
```
- Expected: `200 OK`
- Verify: `status = banned`

### ✅ TC22 — Unban user `banned` → `active`
```json
{ "status": "active" }
```
- Expected: `200 OK`
- Verify: `status = active`

### ✅ TC23 — Set status giống hiện tại (idempotent)
```json
{ "status": "active" }
```
- Expected: `200 OK`

### ❌ TC24 — `status` sai giá trị
```json
{ "status": "suspended" }
```
- Expected: `422 Unprocessable`

### ❌ TC25 — Thiếu `status`
```json
{}
```
- Expected: `422 Unprocessable`

### ❌ TC26 — Admin tự ban chính mình
```json
{ "status": "banned" }
```
- Expected: `200 OK` hoặc `403 Forbidden` hoặc `422 Unprocessable`
- Nếu 200: backend chưa chặn self-action `[WARN]`
- Note: script tự restore lại `active` sau TC này

### ❌ TC27 — ID không tồn tại
```json
{ "status": "banned" }
```
- Expected: `404 Not Found` hoặc `422 Unprocessable` (backend validate ID qua FormRequest)

### ❌ TC28 — User thường không được đổi status
```json
{ "status": "banned" }
```
- Expected: `403 Forbidden`

### ❌ TC29 — Không có token
```json
{ "status": "banned" }
```
- Expected: `401 Unauthorized`

---

## 4. PATCH /admin/users/{id}/role — Đổi role

### ✅ TC30 — Đổi `user` → `admin`
```json
{ "role": "admin" }
```
- Expected: `200 OK`
- Verify: `role = admin`

### ✅ TC31 — Đổi `admin` → `user`
```json
{ "role": "user" }
```
- Expected: `200 OK`
- Verify: `role = user`

### ✅ TC32 — Set role giống hiện tại (idempotent)
```json
{ "role": "user" }
```
- Expected: `200 OK`

### ❌ TC33 — `role` sai giá trị
```json
{ "role": "superadmin" }
```
- Expected: `422 Unprocessable`

### ❌ TC34 — Thiếu `role`
```json
{}
```
- Expected: `422 Unprocessable`

### ❌ TC35 — Admin tự đổi role chính mình
```json
{ "role": "user" }
```
- Expected: `200 OK` hoặc `403 Forbidden` hoặc `422 Unprocessable`
- Nếu 200: backend chưa chặn self-action `[WARN]`
- Note: script tự restore lại `role=admin` ngay sau TC này để không mất quyền

### ❌ TC36 — ID không tồn tại
```json
{ "role": "admin" }
```
- Expected: `404 Not Found` hoặc `422 Unprocessable` hoặc `403 Forbidden`

### ❌ TC37 — User thường không được đổi role
```json
{ "role": "admin" }
```
- Expected: `403 Forbidden`

### ❌ TC38 — Không có token
```json
{ "role": "admin" }
```
- Expected: `401 Unauthorized`

---

## 5. DELETE /admin/users/{id} — Xóa tài khoản

### ✅ TC39 — Xóa user thành công
```http
DELETE /api/v1/admin/users/{id_user_test}
```
- Expected: `200 OK` hoặc `204 No Content`
- Verify: GET `/admin/users/{id}` → `404 Not Found`
- Verify: dữ liệu liên quan (ratings, favorites, notifications) bị CASCADE DELETE

### ❌ TC40 — Xóa ID không tồn tại
```http
DELETE /api/v1/admin/users/99999
```
- Expected: `404 Not Found`

### ❌ TC41 — Admin tự xóa chính mình
```http
DELETE /api/v1/admin/users/{admin_id}
```
- Expected: `403 Forbidden` hoặc `422 Unprocessable`

### ❌ TC42 — User thường không được xóa
```http
DELETE /api/v1/admin/users/{id}
```
- Expected: `403 Forbidden`

### ❌ TC43 — Không có token
```http
DELETE /api/v1/admin/users/{id}
```
- Expected: `401 Unauthorized`

---

## Tổng kết

| TC | API | Trường hợp | Expected |
|----|-----|-----------|----------|
| TC01 | GET /admin/users | Lấy danh sách | 200 |
| TC02 | GET /admin/users | Phân trang per_page=5 | 200 |
| TC03 | GET /admin/users | Trang 2 | 200 |
| TC04 | GET /admin/users | Search ?q= | 200 |
| TC05 | GET /admin/users | Search không có kết quả | 200 |
| TC06 | GET /admin/users | Filter role=user | 200 |
| TC07 | GET /admin/users | Filter role=admin | 200 |
| TC08 | GET /admin/users | Filter status=active | 200 |
| TC09 | GET /admin/users | Filter status=banned | 200 |
| TC10 | GET /admin/users | Kết hợp filter | 200 |
| TC11 | GET /admin/users | role sai giá trị | 422 |
| TC12 | GET /admin/users | status sai giá trị | 422 |
| TC13 | GET /admin/users | per_page vượt max | 200/422 |
| TC14 | GET /admin/users | User thường | 403 |
| TC15 | GET /admin/users | Không có token | 401 |
| TC16 | GET /admin/users/{id} | Chi tiết thành công | 200 |
| TC17 | GET /admin/users/{id} | Chi tiết admin user | 200 |
| TC18 | GET /admin/users/{id} | ID không tồn tại | 404 |
| TC19 | GET /admin/users/{id} | User thường | 403 |
| TC20 | GET /admin/users/{id} | Không có token | 401 |
| TC21 | PATCH .../status | active → banned | 200 |
| TC22 | PATCH .../status | banned → active | 200 |
| TC23 | PATCH .../status | Idempotent | 200 |
| TC24 | PATCH .../status | status sai | 422 |
| TC25 | PATCH .../status | Thiếu status | 422 |
| TC26 | PATCH .../status | Admin tự ban mình | 403/422 |
| TC27 | PATCH .../status | ID không tồn tại | 404 |
| TC28 | PATCH .../status | User thường | 403 |
| TC29 | PATCH .../status | Không có token | 401 |
| TC30 | PATCH .../role | user → admin | 200 |
| TC31 | PATCH .../role | admin → user | 200 |
| TC32 | PATCH .../role | Idempotent | 200 |
| TC33 | PATCH .../role | role sai | 422 |
| TC34 | PATCH .../role | Thiếu role | 422 |
| TC35 | PATCH .../role | Admin tự đổi role mình | 403/422 |
| TC36 | PATCH .../role | ID không tồn tại | 404 |
| TC37 | PATCH .../role | User thường | 403 |
| TC38 | PATCH .../role | Không có token | 401 |
| TC39 | DELETE /admin/users/{id} | Xóa thành công | 200/204 |
| TC40 | DELETE /admin/users/{id} | ID không tồn tại | 404 |
| TC41 | DELETE /admin/users/{id} | Admin tự xóa mình | 403/422 |
| TC42 | DELETE /admin/users/{id} | User thường | 403 |
| TC43 | DELETE /admin/users/{id} | Không có token | 401 |
