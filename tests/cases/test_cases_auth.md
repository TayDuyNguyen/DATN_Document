# Test Cases — AUTH (Xác thực)

> Base URL: `http://localhost:8000/api/v1`
> 🌐 Public — không cần token
> 🔐 Cần Bearer token

---

## 1. POST /auth/register — Đăng ký

### ✅ TC01 — Đăng ký thành công đầy đủ field
```json
{
  "username": "testuser_01",
  "email": "testuser01@example.com",
  "password": "Password123!",
  "password_confirmation": "Password123!",
  "full_name": "Test User 01"
}
```
- Expected: `201 Created`, response có `token` hoặc `user`

### ❌ TC02 — Email đã tồn tại
```json
{ "username": "newuser", "email": "user1@example.com", "password": "Password123!", "password_confirmation": "Password123!", "full_name": "New User" }
```
- Expected: `422 Unprocessable`, lỗi `email already taken`

### ❌ TC03 — Username đã tồn tại
```json
{ "username": "user1", "email": "brand_new@example.com", "password": "Password123!", "password_confirmation": "Password123!", "full_name": "New User" }
```
- Expected: `422 Unprocessable`, lỗi `username already taken`

### ❌ TC04 — `password` và `password_confirmation` không khớp
```json
{ "username": "newuser2", "email": "newuser2@example.com", "password": "Password123!", "password_confirmation": "Different123!", "full_name": "New User" }
```
- Expected: `422 Unprocessable`

### ❌ TC05 — `password` quá ngắn (< 8 ký tự)
```json
{ "username": "newuser3", "email": "newuser3@example.com", "password": "123", "password_confirmation": "123", "full_name": "New User" }
```
- Expected: `422 Unprocessable`

### ❌ TC06 — Email sai định dạng
```json
{ "username": "newuser4", "email": "not-an-email", "password": "Password123!", "password_confirmation": "Password123!", "full_name": "New User" }
```
- Expected: `422 Unprocessable`

### ❌ TC07 — Thiếu `email`
```json
{ "username": "newuser5", "password": "Password123!", "password_confirmation": "Password123!", "full_name": "New User" }
```
- Expected: `422 Unprocessable`

### ❌ TC08 — Thiếu `username`
```json
{ "email": "newuser6@example.com", "password": "Password123!", "password_confirmation": "Password123!", "full_name": "New User" }
```
- Expected: `422 Unprocessable`

### ❌ TC09 — Thiếu `full_name`
```json
{ "username": "newuser7", "email": "newuser7@example.com", "password": "Password123!", "password_confirmation": "Password123!" }
```
- Expected: `422 Unprocessable`

### ❌ TC10 — Body rỗng
```json
{}
```
- Expected: `422 Unprocessable`

---

## 2. POST /auth/login — Đăng nhập

### ✅ TC11 — Đăng nhập thành công
```json
{ "email": "user1@example.com", "password": "password" }
```
- Expected: `200 OK`, response có `token` (Bearer)

### ✅ TC12 — Đăng nhập với email vừa đăng ký (TC01)
```json
{ "email": "testuser01@example.com", "password": "Password123!" }
```
- Expected: `200 OK`, có token

### ❌ TC13 — Sai mật khẩu
```json
{ "email": "user1@example.com", "password": "wrongpassword" }
```
- Expected: `401 Unauthorized` hoặc `422 Unprocessable`

### ❌ TC14 — Email không tồn tại
```json
{ "email": "notexist@example.com", "password": "password" }
```
- Expected: `401 Unauthorized` hoặc `422 Unprocessable`

### ❌ TC15 — Thiếu `email`
```json
{ "password": "password" }
```
- Expected: `422 Unprocessable`

### ❌ TC16 — Thiếu `password`
```json
{ "email": "user1@example.com" }
```
- Expected: `422 Unprocessable`

### ❌ TC17 — Email sai định dạng
```json
{ "email": "not-an-email", "password": "password" }
```
- Expected: `422 Unprocessable`

### ❌ TC18 — Body rỗng
```json
{}
```
- Expected: `422 Unprocessable`

---

## 3. POST /auth/logout — Đăng xuất

### ✅ TC19 — Đăng xuất thành công
- header: `Authorization: Bearer {valid_token}`
- Expected: `200 OK`
- Verify: token bị thu hồi, gọi lại `/auth/me` với token cũ → `401`

### ❌ TC20 — Không có token
- Expected: `401 Unauthorized`

### ❌ TC21 — Token không hợp lệ (random string)
- header: `Authorization: Bearer invalid_token_string`
- Expected: `401 Unauthorized`

---

## 4. GET /auth/me — Thông tin user hiện tại

### ✅ TC22 — Lấy thông tin thành công
- header: `Authorization: Bearer {valid_token}`
- Expected: `200 OK`, có `id`, `email`, `username`, `full_name`, `role`

### ❌ TC23 — Không có token
- Expected: `401 Unauthorized`

### ❌ TC24 — Token đã bị thu hồi (sau logout)
- Expected: `401 Unauthorized`

### ❌ TC25 — Token sai định dạng
- header: `Authorization: Bearer abc.def.ghi`
- Expected: `401 Unauthorized`

---

## 5. POST /auth/refresh — Làm mới token

### ✅ TC26 — Refresh token thành công
- header: `Authorization: Bearer {valid_token}`
- Expected: `200 OK`, response có token mới
- Verify: token mới khác token cũ, token mới dùng được

### ❌ TC27 — Không có token
- Expected: `401 Unauthorized`

### ❌ TC28 — Token đã bị thu hồi
- Expected: `401 Unauthorized`

---

## 6. POST /auth/forgot-password — Quên mật khẩu

### ✅ TC29 — Gửi email thành công (email tồn tại)
```json
{ "email": "user1@example.com" }
```
- Expected: `200 OK`, message xác nhận đã gửi email

### ✅ TC30 — Email không tồn tại trong hệ thống
```json
{ "email": "notexist@example.com" }
```
- Expected: `200 OK` (không tiết lộ email có tồn tại hay không — security best practice)

### ❌ TC31 — Email sai định dạng
```json
{ "email": "not-an-email" }
```
- Expected: `422 Unprocessable`

### ❌ TC32 — Thiếu `email`
```json
{}
```
- Expected: `422 Unprocessable`

---

## 7. POST /auth/reset-password — Đặt lại mật khẩu

### ✅ TC33 — Reset thành công (cần token hợp lệ từ email)
```json
{ "token": "<valid_reset_token>", "email": "user1@example.com", "password": "NewPass123!", "password_confirmation": "NewPass123!" }
```
- Expected: `200 OK`
- Verify: đăng nhập với mật khẩu mới thành công

### ❌ TC34 — Token không hợp lệ
```json
{ "token": "invalid_token_xyz", "email": "user1@example.com", "password": "NewPass123!", "password_confirmation": "NewPass123!" }
```
- Expected: `422 Unprocessable` hoặc `400 Bad Request`

### ❌ TC35 — Token đúng nhưng email không khớp
```json
{ "token": "<valid_reset_token>", "email": "other@example.com", "password": "NewPass123!", "password_confirmation": "NewPass123!" }
```
- Expected: `422 Unprocessable`

### ❌ TC36 — `password` và `password_confirmation` không khớp
```json
{ "token": "<valid_reset_token>", "email": "user1@example.com", "password": "NewPass123!", "password_confirmation": "Different!" }
```
- Expected: `422 Unprocessable`

### ❌ TC37 — `password` quá ngắn
```json
{ "token": "<valid_reset_token>", "email": "user1@example.com", "password": "123", "password_confirmation": "123" }
```
- Expected: `422 Unprocessable`

### ❌ TC38 — Thiếu `token`
```json
{ "email": "user1@example.com", "password": "NewPass123!", "password_confirmation": "NewPass123!" }
```
- Expected: `422 Unprocessable`

### ❌ TC39 — Thiếu `email`
```json
{ "token": "<valid_reset_token>", "password": "NewPass123!", "password_confirmation": "NewPass123!" }
```
- Expected: `422 Unprocessable`

---

## Tổng kết

| TC | API | Trường hợp | Expected |
|----|-----|-----------|----------|
| TC01 | POST /auth/register | Đăng ký thành công | 201 |
| TC02 | POST /auth/register | Email đã tồn tại | 422 |
| TC03 | POST /auth/register | Username đã tồn tại | 422 |
| TC04 | POST /auth/register | password không khớp | 422 |
| TC05 | POST /auth/register | password quá ngắn | 422 |
| TC06 | POST /auth/register | Email sai định dạng | 422 |
| TC07 | POST /auth/register | Thiếu email | 422 |
| TC08 | POST /auth/register | Thiếu username | 422 |
| TC09 | POST /auth/register | Thiếu full_name | 422 |
| TC10 | POST /auth/register | Body rỗng | 422 |
| TC11 | POST /auth/login | Đăng nhập thành công | 200 |
| TC12 | POST /auth/login | Đăng nhập user mới đăng ký | 200 |
| TC13 | POST /auth/login | Sai mật khẩu | 401/422 |
| TC14 | POST /auth/login | Email không tồn tại | 401/422 |
| TC15 | POST /auth/login | Thiếu email | 422 |
| TC16 | POST /auth/login | Thiếu password | 422 |
| TC17 | POST /auth/login | Email sai định dạng | 422 |
| TC18 | POST /auth/login | Body rỗng | 422 |
| TC19 | POST /auth/logout | Đăng xuất thành công | 200 |
| TC20 | POST /auth/logout | Không có token | 401 |
| TC21 | POST /auth/logout | Token không hợp lệ | 401 |
| TC22 | GET /auth/me | Lấy thông tin thành công | 200 |
| TC23 | GET /auth/me | Không có token | 401 |
| TC24 | GET /auth/me | Token đã bị thu hồi | 401 |
| TC25 | GET /auth/me | Token sai định dạng | 401 |
| TC26 | POST /auth/refresh | Refresh thành công | 200 |
| TC27 | POST /auth/refresh | Không có token | 401 |
| TC28 | POST /auth/refresh | Token đã bị thu hồi | 401 |
| TC29 | POST /auth/forgot-password | Email tồn tại | 200 |
| TC30 | POST /auth/forgot-password | Email không tồn tại | 200 |
| TC31 | POST /auth/forgot-password | Email sai định dạng | 422 |
| TC32 | POST /auth/forgot-password | Thiếu email | 422 |
| TC33 | POST /auth/reset-password | Reset thành công | 200 |
| TC34 | POST /auth/reset-password | Token không hợp lệ | 400/422 |
| TC35 | POST /auth/reset-password | Email không khớp token | 422 |
| TC36 | POST /auth/reset-password | password không khớp | 422 |
| TC37 | POST /auth/reset-password | password quá ngắn | 422 |
| TC38 | POST /auth/reset-password | Thiếu token | 422 |
| TC39 | POST /auth/reset-password | Thiếu email | 422 |
