# Test Cases — PAYMENTS (Thanh toán)

> Base URL: `http://localhost:8000/api/v1`
> 🌐 Public: không cần token (webhook)
> 🔐 User token
> 🛡️ Admin token

---

## 1. POST /payments/callback — Webhook cổng thanh toán

### ✅ TC01 — Callback thành công (mock payload)
- body: payload giả lập từ gateway
- Expected: `200 OK`

### ✅ TC02 — Không cần token (public webhook)
- Expected: `200 OK` hoặc `422`

---

## 2. POST /payments/create — Tạo link thanh toán

### ✅ TC03 — Tạo link MoMo thành công
```json
{ "booking_id": 1, "payment_method": "momo" }
```
- Expected: `200 OK` hoặc `201 Created`
- Verify: response có `payment_url` hoặc `transaction_code`

### ✅ TC04 — Tạo link VNPay
```json
{ "booking_id": 1, "payment_method": "vnpay" }
```
- Expected: `200 OK` hoặc `201 Created`

### ✅ TC05 — Tạo link ZaloPay
```json
{ "booking_id": 1, "payment_method": "zalopay" }
```
- Expected: `200 OK` hoặc `201 Created`

### ❌ TC06 — Thiếu `booking_id`
- Expected: `422 Unprocessable`

### ❌ TC07 — Thiếu `payment_method`
- Expected: `422 Unprocessable`

### ❌ TC08 — `payment_method` sai giá trị
```json
{ "booking_id": 1, "payment_method": "paypal" }
```
- Expected: `422 Unprocessable`

### ❌ TC09 — `booking_id` không tồn tại
```json
{ "booking_id": 99999, "payment_method": "momo" }
```
- Expected: `404 Not Found` hoặc `422`

### ❌ TC10 — Không có token
- Expected: `401 Unauthorized`

---

## 3. GET /payments/status/{transaction_code} — Kiểm tra trạng thái

### ✅ TC11 — Kiểm tra trạng thái thành công
- Expected: `200 OK`
- Verify: response có `payment_status`, `transaction_code`

### ❌ TC12 — `transaction_code` không tồn tại
- Expected: `404 Not Found` hoặc `422`

### ❌ TC13 — Không có token
- Expected: `401 Unauthorized`

---

## 4. POST /payments/retry/{booking_code} — Thử lại thanh toán

### ✅ TC14 — Retry thành công
- Expected: `200 OK` hoặc `201 Created`
- Verify: response có `payment_url` hoặc `transaction_code`

### ❌ TC15 — `booking_code` không tồn tại
- Expected: `404 Not Found` hoặc `422`

### ❌ TC16 — Booking đã thanh toán (không cần retry)
- Expected: `422 Unprocessable` hoặc `400 Bad Request`

### ❌ TC17 — Không có token
- Expected: `401 Unauthorized`

---

## 5. GET /admin/payments — Danh sách giao dịch (Admin)

### ✅ TC18 — Lấy tất cả thành công
- Expected: `200 OK`
- Verify: mỗi item có `id`, `transaction_code`, `payment_status`, `amount`

### ✅ TC19 — Filter `payment_status=pending`
- Expected: `200 OK`

### ✅ TC20 — Filter `payment_status=success`
- Expected: `200 OK`

### ✅ TC21 — Filter `payment_status=failed`
- Expected: `200 OK`

### ✅ TC22 — Filter `payment_status=refunded`
- Expected: `200 OK`

### ✅ TC23 — Filter `payment_gateway=momo`
- Expected: `200 OK`

### ✅ TC24 — Filter `date_from` và `date_to`
- Expected: `200 OK`

### ✅ TC25 — Phân trang `per_page=5`
- Expected: `200 OK`

### ❌ TC26 — `payment_status` sai giá trị
- Expected: `422 Unprocessable`

### ❌ TC27 — `date_from` sai định dạng
- Expected: `422 Unprocessable`

### ❌ TC28 — User thường không được truy cập
- Expected: `403 Forbidden`

### ❌ TC29 — Không có token
- Expected: `401 Unauthorized`

---

## 6. GET /admin/payments/{id} — Chi tiết giao dịch (Admin)

### ✅ TC30 — Lấy chi tiết thành công
- Expected: `200 OK`
- Verify: có `transaction_code`, `booking`, `payment_gateway`

### ❌ TC31 — ID không tồn tại
- Expected: `404 Not Found` hoặc `422`

### ❌ TC32 — User thường không được truy cập
- Expected: `403 Forbidden`

### ❌ TC33 — Không có token
- Expected: `401 Unauthorized`

---

## 7. POST /admin/payments/{id}/refund — Hoàn tiền (Admin)

### ✅ TC34 — Hoàn tiền thành công
```json
{ "refund_reason": "Khach hang yeu cau hoan tien" }
```
- Expected: `200 OK`
- Verify: `payment_status = refunded`

### ❌ TC35 — Thiếu `refund_reason`
- Expected: `422 Unprocessable`

### ❌ TC36 — Hoàn tiền giao dịch chưa `success`
- Expected: `422 Unprocessable` hoặc `400 Bad Request`

### ❌ TC37 — ID không tồn tại
- Expected: `404 Not Found` hoặc `422`

### ❌ TC38 — User thường không được hoàn tiền
- Expected: `403 Forbidden`

### ❌ TC39 — Không có token
- Expected: `401 Unauthorized`

---

## 8. GET /admin/payments/export — Export Excel (Admin)

### ✅ TC40 — Export thành công
- Expected: `200 OK`
- Verify: Content-Type là CSV hoặc Excel

### ✅ TC41 — Export với filter
- Expected: `200 OK`

### ❌ TC42 — User thường không được export
- Expected: `403 Forbidden`

### ❌ TC43 — Không có token
- Expected: `401 Unauthorized`

---

## Tổng kết

| TC | API | Trường hợp | Expected |
|----|-----|-----------|----------|
| TC01-TC02 | POST /payments/callback | Webhook | 200/422 |
| TC03-TC05 | POST /payments/create | Tạo link | 200/201 |
| TC06-TC10 | POST /payments/create | Validation + auth | 422/401 |
| TC11 | GET /payments/status/{code} | Kiểm tra trạng thái | 200 |
| TC12-TC13 | GET /payments/status/{code} | 404/401 | 404/401 |
| TC14 | POST /payments/retry/{code} | Retry | 200/201 |
| TC15-TC17 | POST /payments/retry/{code} | Edge cases | 404/422/401 |
| TC18 | GET /admin/payments | Lấy tất cả | 200 |
| TC19-TC25 | GET /admin/payments | Filter + paginate | 200 |
| TC26-TC29 | GET /admin/payments | Validation + auth | 422/403/401 |
| TC30 | GET /admin/payments/{id} | Chi tiết | 200 |
| TC31-TC33 | GET /admin/payments/{id} | 404/403/401 | 404/403/401 |
| TC34 | POST /admin/payments/{id}/refund | Hoàn tiền | 200 |
| TC35-TC39 | POST /admin/payments/{id}/refund | Validation + auth | 422/403/401 |
| TC40-TC41 | GET /admin/payments/export | Export | 200 |
| TC42-TC43 | GET /admin/payments/export | Auth | 403/401 |
