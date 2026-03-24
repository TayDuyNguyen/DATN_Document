# Test Cases — POINTS (Điểm thưởng)

> Base URL: `http://localhost:8000/api/v1`
> 🔐 User token cần thiết cho tất cả endpoints

---

## 1. GET /user/points — Số dư point hiện tại

### ✅ TC01 — Lấy số dư thành công
- Expected: `200 OK`, response có `point_balance` (số nguyên >= 0)

### ✅ TC02 — Verify `point_balance` khớp với `/user/profile`
- Gọi `GET /user/profile` và `GET /user/points`, so sánh `point_balance`
- Expected: 2 giá trị phải bằng nhau

### ❌ TC03 — Không có token
- Expected: `401 Unauthorized`

---

## 2. GET /user/points/transactions — Lịch sử giao dịch

### ✅ TC04 — Lấy tất cả không filter
```http
GET /api/v1/user/points/transactions
```
- Expected: `200 OK`, array transactions có `id`, `type`, `amount`, `created_at`

### ✅ TC05 — Filter `type=purchase`
```http
GET /api/v1/user/points/transactions?type=purchase
```
- Expected: `200 OK`, tất cả record có `type = purchase`

### ✅ TC06 — Filter `type=spend`
```http
GET /api/v1/user/points/transactions?type=spend
```
- Expected: `200 OK`, tất cả record có `type = spend`

### ✅ TC07 — Filter `type=bonus`
```http
GET /api/v1/user/points/transactions?type=bonus
```
- Expected: `200 OK`, tất cả record có `type = bonus`

### ✅ TC08 — Filter `type=refund`
```http
GET /api/v1/user/points/transactions?type=refund
```
- Expected: `200 OK`, tất cả record có `type = refund`

### ✅ TC09 — Phân trang `per_page=5`
```http
GET /api/v1/user/points/transactions?page=1&per_page=5
```
- Expected: `200 OK`, `data` có tối đa 5 phần tử

### ✅ TC10 — Trang 2 (nếu có đủ data)
```http
GET /api/v1/user/points/transactions?page=2&per_page=5
```
- Expected: `200 OK`

### ❌ TC11 — `type` sai giá trị
```http
GET /api/v1/user/points/transactions?type=invalid
```
- Expected: `422 Unprocessable`

### ❌ TC12 — Không có token
- Expected: `401 Unauthorized`

---

## 3. POST /user/points/purchase — Nạp point

### ✅ TC13 — Nạp point với momo thành công
```json
{ "amount": 100, "payment_method": "momo" }
```
- Expected: `200 OK` hoặc `201 Created`
- Verify: `point_balance` tăng thêm `amount`, `point_transactions` có record mới `type=purchase`

### ✅ TC14 — Nạp point với vnpay
```json
{ "amount": 200, "payment_method": "vnpay" }
```
- Expected: `200 OK` hoặc `201 Created`

### ✅ TC15 — Nạp point với bank
```json
{ "amount": 500, "payment_method": "bank" }
```
- Expected: `200 OK` hoặc `201 Created`

### ✅ TC16 — Nạp số lượng nhỏ nhất hợp lệ
```json
{ "amount": 1, "payment_method": "momo" }
```
- Expected: `200 OK` hoặc `201 Created`

### ❌ TC17 — `amount` = 0
```json
{ "amount": 0, "payment_method": "momo" }
```
- Expected: `422 Unprocessable`

### ❌ TC18 — `amount` âm
```json
{ "amount": -100, "payment_method": "momo" }
```
- Expected: `422 Unprocessable`

### ❌ TC19 — `amount` không phải số
```json
{ "amount": "abc", "payment_method": "momo" }
```
- Expected: `422 Unprocessable`

### ❌ TC20 — `payment_method` sai giá trị
```json
{ "amount": 100, "payment_method": "paypal" }
```
- Expected: `422 Unprocessable`

### ❌ TC21 — Thiếu `amount`
```json
{ "payment_method": "momo" }
```
- Expected: `422 Unprocessable`

### ❌ TC22 — Thiếu `payment_method`
```json
{ "amount": 100 }
```
- Expected: `422 Unprocessable`

### ❌ TC23 — Body rỗng
```json
{}
```
- Expected: `422 Unprocessable`

### ❌ TC24 — Không có token
```json
{ "amount": 100, "payment_method": "momo" }
```
- Expected: `401 Unauthorized`

---

## Tổng kết

| TC | API | Trường hợp | Expected |
|----|-----|-----------|----------|
| TC01 | GET /user/points | Lấy số dư | 200 |
| TC02 | GET /user/points | Verify khớp profile | 200 |
| TC03 | GET /user/points | Không có token | 401 |
| TC04 | GET /user/points/transactions | Lấy tất cả | 200 |
| TC05 | GET /user/points/transactions | Filter purchase | 200 |
| TC06 | GET /user/points/transactions | Filter spend | 200 |
| TC07 | GET /user/points/transactions | Filter bonus | 200 |
| TC08 | GET /user/points/transactions | Filter refund | 200 |
| TC09 | GET /user/points/transactions | Phân trang per_page=5 | 200 |
| TC10 | GET /user/points/transactions | Trang 2 | 200 |
| TC11 | GET /user/points/transactions | type sai giá trị | 422 |
| TC12 | GET /user/points/transactions | Không có token | 401 |
| TC13 | POST /user/points/purchase | Nạp momo | 200/201 |
| TC14 | POST /user/points/purchase | Nạp vnpay | 200/201 |
| TC15 | POST /user/points/purchase | Nạp bank | 200/201 |
| TC16 | POST /user/points/purchase | amount nhỏ nhất (1) | 200/201 |
| TC17 | POST /user/points/purchase | amount = 0 | 422 |
| TC18 | POST /user/points/purchase | amount âm | 422 |
| TC19 | POST /user/points/purchase | amount không phải số | 422 |
| TC20 | POST /user/points/purchase | payment_method sai | 422 |
| TC21 | POST /user/points/purchase | Thiếu amount | 422 |
| TC22 | POST /user/points/purchase | Thiếu payment_method | 422 |
| TC23 | POST /user/points/purchase | Body rỗng | 422 |
| TC24 | POST /user/points/purchase | Không có token | 401 |
