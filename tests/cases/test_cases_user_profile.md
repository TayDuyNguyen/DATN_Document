# Test Cases — USER PROFILE (Hồ sơ cá nhân)

> Base URL: `http://localhost:8000/api/v1`
> 🔐 User token cần thiết cho tất cả endpoints

---

## 1. GET /user/profile — Xem thông tin cá nhân

### ✅ TC01 — Lấy profile thành công
- Expected: `200 OK`, có các field `id`, `full_name`, `email`, `phone`, `birthdate`, `gender`, `city`, `avatar`

### ❌ TC02 — Không có token
- Expected: `401 Unauthorized`

---

## 2. PUT /user/profile — Cập nhật thông tin cá nhân

### ✅ TC03 — Cập nhật đầy đủ field
```json
{ "full_name": "Nguyen Van A", "phone": "0901234567", "birthdate": "1995-06-15", "gender": "male", "city": "Da Nang" }
```
- Expected: `200 OK`, dữ liệu được cập nhật

### ✅ TC04 — Cập nhật một field
```json
{ "full_name": "Ten Moi" }
```
- Expected: `200 OK`

### ✅ TC05 — Cập nhật với body rỗng (không thay đổi gì)
```json
{}
```
- Expected: `200 OK`

### ❌ TC06 — `phone` sai định dạng
```json
{ "phone": "abc123" }
```
- Expected: `422 Unprocessable`
- Note: Backend hiện chưa validate format phone (trả 200) — cần thêm rule `regex` trong `UpdateProfileRequest`

### ❌ TC07 — `birthdate` sai định dạng
```json
{ "birthdate": "15/06/1995" }
```
- Expected: `422 Unprocessable`

### ❌ TC08 — `gender` sai giá trị
```json
{ "gender": "unknown" }
```
- Expected: `422 Unprocessable`

### ❌ TC09 — Không có token
- Expected: `401 Unauthorized`

---

## 3. POST /user/profile/avatar — Upload ảnh đại diện

### ✅ TC10 — Upload JPEG thành công (< 2MB)
- body: `avatar=<file.jpg>`
- Expected: `200 OK`, response có `avatar` URL mới

### ✅ TC11 — Upload PNG thành công
- body: `avatar=<file.png>`
- Expected: `200 OK`

### ❌ TC12 — Thiếu file `avatar`
- body: `{}`
- Expected: `422 Unprocessable`

### ❌ TC13 — File không phải ảnh (txt, pdf...)
- body: `avatar=<file.txt>`
- Expected: `422 Unprocessable`

### ❌ TC14 — File quá 2MB
- body: `avatar=<file > 2MB>`
- Expected: `422 Unprocessable` (Laravel) hoặc `413 Request Entity Too Large` (Nginx)
- Note: `413` là Nginx chặn trước khi vào Laravel do `client_max_body_size` — cần tăng config Nginx nếu muốn Laravel validate và trả 422

### ❌ TC15 — Không có token
- Expected: `401 Unauthorized`

---

## 4. PUT /user/password — Đổi mật khẩu

### ✅ TC16 — Đổi mật khẩu thành công
```json
{ "current_password": "password", "password": "NewPass123!", "password_confirmation": "NewPass123!" }
```
- Expected: `200 OK`
- Verify: đăng nhập lại với mật khẩu mới thành công

### ❌ TC17 — `current_password` sai
```json
{ "current_password": "wrongpass", "password": "NewPass123!", "password_confirmation": "NewPass123!" }
```
- Expected: `422 Unprocessable` hoặc `400 Bad Request`

### ❌ TC18 — `password` và `password_confirmation` không khớp
```json
{ "current_password": "password", "password": "NewPass123!", "password_confirmation": "DifferentPass!" }
```
- Expected: `422 Unprocessable`

### ❌ TC19 — `password` quá ngắn (< 8 ký tự)
```json
{ "current_password": "password", "password": "123", "password_confirmation": "123" }
```
- Expected: `422 Unprocessable`

### ❌ TC20 — Thiếu `current_password`
```json
{ "password": "NewPass123!", "password_confirmation": "NewPass123!" }
```
- Expected: `422 Unprocessable`

### ❌ TC21 — Không có token
- Expected: `401 Unauthorized`

---

## 5. GET /user/ratings — Lịch sử đánh giá

### ✅ TC22 — Lấy tất cả không filter
```http
GET /api/v1/user/ratings
```
- Expected: `200 OK`, array ratings kèm `location`, `rating_images`

### ✅ TC23 — Filter `status=pending`
```http
GET /api/v1/user/ratings?status=pending
```
- Expected: `200 OK`, tất cả kết quả có `status = pending`

### ✅ TC24 — Filter `status=approved`
```http
GET /api/v1/user/ratings?status=approved
```
- Expected: `200 OK`, tất cả kết quả có `status = approved`

### ✅ TC25 — Filter `status=rejected`
```http
GET /api/v1/user/ratings?status=rejected
```
- Expected: `200 OK`, tất cả kết quả có `status = rejected`

### ✅ TC26 — Phân trang
```http
GET /api/v1/user/ratings?page=1&per_page=5
```
- Expected: `200 OK`, `data` có tối đa 5 phần tử

### ❌ TC27 — `status` sai giá trị
```http
GET /api/v1/user/ratings?status=invalid
```
- Expected: `422 Unprocessable`

### ❌ TC28 — Không có token
- Expected: `401 Unauthorized`

---

## Tổng kết

| TC | API | Trường hợp | Expected |
|----|-----|-----------|----------|
| TC01 | GET /user/profile | Lấy profile | 200 |
| TC02 | GET /user/profile | Không có token | 401 |
| TC03 | PUT /user/profile | Cập nhật đầy đủ | 200 |
| TC04 | PUT /user/profile | Cập nhật 1 field | 200 |
| TC05 | PUT /user/profile | Body rỗng | 200 |
| TC06 | PUT /user/profile | phone sai định dạng | 422 |
| TC07 | PUT /user/profile | birthdate sai định dạng | 422 |
| TC08 | PUT /user/profile | gender sai giá trị | 422 |
| TC09 | PUT /user/profile | Không có token | 401 |
| TC10 | POST /user/profile/avatar | Upload JPEG | 200 |
| TC11 | POST /user/profile/avatar | Upload PNG | 200 |
| TC12 | POST /user/profile/avatar | Thiếu file | 422 |
| TC13 | POST /user/profile/avatar | File không phải ảnh | 422 |
| TC14 | POST /user/profile/avatar | File > 2MB | 422 |
| TC15 | POST /user/profile/avatar | Không có token | 401 |
| TC16 | PUT /user/password | Đổi mật khẩu thành công | 200 |
| TC17 | PUT /user/password | current_password sai | 400/422 |
| TC18 | PUT /user/password | password không khớp | 422 |
| TC19 | PUT /user/password | password quá ngắn | 422 |
| TC20 | PUT /user/password | Thiếu current_password | 422 |
| TC21 | PUT /user/password | Không có token | 401 |
| TC22 | GET /user/ratings | Lấy tất cả | 200 |
| TC23 | GET /user/ratings | Filter pending | 200 |
| TC24 | GET /user/ratings | Filter approved | 200 |
| TC25 | GET /user/ratings | Filter rejected | 200 |
| TC26 | GET /user/ratings | Phân trang | 200 |
| TC27 | GET /user/ratings | status sai giá trị | 422 |
| TC28 | GET /user/ratings | Không có token | 401 |
