# Test Cases — BOOKINGS (Đặt tour)

> Base URL: `http://localhost:8000/api/v1`
> 🔐 User token bắt buộc cho user endpoints
> 🛡️ Admin token bắt buộc cho admin endpoints

---

## 1. POST /bookings/calculate — Tính tổng tiền

### ✅ TC01 — Tính tiền thành công (người lớn)
```json
{ "tour_id": 1, "tour_schedule_id": 1, "quantity_adult": 2, "quantity_child": 0, "quantity_infant": 0 }
```
- Expected: `200 OK`
- Verify: response có `total_amount`, `breakdown`

### ✅ TC02 — Tính tiền với cả 3 loại khách
```json
{ "tour_id": 1, "tour_schedule_id": 1, "quantity_adult": 2, "quantity_child": 1, "quantity_infant": 1 }
```
- Expected: `200 OK`

### ❌ TC03 — Thiếu `tour_id`
- Expected: `422 Unprocessable`

### ❌ TC04 — Thiếu `tour_schedule_id`
- Expected: `422 Unprocessable`

### ❌ TC05 — Thiếu `quantity_adult`
- Expected: `422 Unprocessable`

### ❌ TC06 — `quantity_adult = 0` (không có người lớn)
- Expected: `422 Unprocessable`

### ❌ TC07 — `tour_schedule_id` không tồn tại
- Expected: `404 Not Found` hoặc `422`

### ❌ TC08 — Không có token
- Expected: `401 Unauthorized`

---

## 2. POST /bookings — Đặt tour mới

### ✅ TC09 — Đặt tour thành công đầy đủ fields
```json
{
  "tour_id": 1, "tour_schedule_id": 1,
  "quantity_adult": 2, "quantity_child": 0, "quantity_infant": 0,
  "customer_name": "Nguyen Van A", "customer_email": "test@example.com",
  "customer_phone": "0901234567", "customer_address": "123 Da Nang",
  "customer_note": "Yeu cau dac biet", "payment_method": "momo"
}
```
- Expected: `200 OK` hoặc `201 Created`
- Verify: response có `booking_code`, `booking_status=pending`

### ✅ TC10 — Đặt tour chỉ với fields bắt buộc
- Expected: `200 OK` hoặc `201 Created`

### ❌ TC11 — Thiếu `customer_name`
- Expected: `422 Unprocessable`

### ❌ TC12 — Thiếu `customer_email`
- Expected: `422 Unprocessable`

### ❌ TC13 — Thiếu `customer_phone`
- Expected: `422 Unprocessable`

### ❌ TC14 — Thiếu `payment_method`
- Expected: `422 Unprocessable`

### ❌ TC15 — `customer_email` sai định dạng
- Expected: `422 Unprocessable`

### ❌ TC16 — `payment_method` sai giá trị
- Expected: `422 Unprocessable`

### ❌ TC17 — `tour_schedule_id` đã full (hết chỗ)
- Expected: `422 Unprocessable` hoặc `409 Conflict`

### ❌ TC18 — Không có token
- Expected: `401 Unauthorized`

---

## 3. GET /user/bookings — Lịch sử đặt tour

### ✅ TC19 — Lấy danh sách thành công
- Expected: `200 OK`
- Verify: mỗi item có `id`, `booking_code`, `booking_status`, `final_amount`

### ✅ TC20 — Filter `status=pending`
- Expected: `200 OK`

### ✅ TC21 — Filter `status=confirmed`
- Expected: `200 OK`

### ✅ TC22 — Filter `status=cancelled`
- Expected: `200 OK`

### ✅ TC23 — Phân trang `per_page=5`
- Expected: `200 OK`

### ❌ TC24 — `status` sai giá trị
- Expected: `422 Unprocessable`

### ❌ TC25 — Không có token
- Expected: `401 Unauthorized`

---

## 4. GET /user/bookings/{id} — Chi tiết đơn theo ID

### ✅ TC26 — Lấy chi tiết thành công
- Expected: `200 OK`
- Verify: có `booking_code`, `booking_items`, `payments`

### ❌ TC27 — ID không tồn tại
- Expected: `404 Not Found` hoặc `422`

### ❌ TC28 — Xem đơn của người khác
- Expected: `403 Forbidden` hoặc `404 Not Found`

### ❌ TC29 — Không có token
- Expected: `401 Unauthorized`

---

## 5. GET /user/bookings/code/{booking_code} — Chi tiết theo mã đơn

### ✅ TC30 — Lấy chi tiết theo booking_code thành công
- Expected: `200 OK`

### ❌ TC31 — booking_code không tồn tại
- Expected: `404 Not Found` hoặc `422`

### ❌ TC32 — Không có token
- Expected: `401 Unauthorized`

---

## 6. GET /user/bookings/{id}/invoice — Xuất hóa đơn PDF

### ✅ TC33 — Xuất hóa đơn thành công
- Expected: `200 OK`
- Verify: Content-Type là `application/pdf` hoặc `application/octet-stream`

### ❌ TC34 — ID không tồn tại
- Expected: `404 Not Found` hoặc `422`

### ❌ TC35 — Không có token
- Expected: `401 Unauthorized`

---

## 7. POST /user/bookings/{id}/cancel — Hủy đơn

### ✅ TC36 — Hủy đơn `pending` thành công
```json
{ "cancellation_reason": "Thay doi ke hoach" }
```
- Expected: `200 OK`
- Verify: `booking_status = cancelled`

### ❌ TC37 — Hủy đơn đã `confirmed` (không cho phép)
- Expected: `422 Unprocessable` hoặc `400 Bad Request`

### ❌ TC38 — Hủy đơn đã `cancelled`
- Expected: `422 Unprocessable`

### ❌ TC39 — Hủy đơn của người khác
- Expected: `403 Forbidden` hoặc `404 Not Found`

### ❌ TC40 — ID không tồn tại
- Expected: `404 Not Found` hoặc `422`

### ❌ TC41 — Không có token
- Expected: `401 Unauthorized`

---

## 8. GET /admin/bookings — Danh sách đơn hàng (Admin)

### ✅ TC42 — Lấy tất cả thành công
- Expected: `200 OK`

### ✅ TC43 — Filter `status=pending`
- Expected: `200 OK`

### ✅ TC44 — Filter `payment_status=pending`
- Expected: `200 OK`
- Note: PaymentStatus enum: `pending`, `paid`, `failed`, `refunded` (không có `unpaid`)

### ✅ TC45 — Filter `date_from` và `date_to`
- Expected: `200 OK`

### ✅ TC46 — Search theo tên/email khách
- Expected: `200 OK`

### ✅ TC47 — Phân trang `per_page=5`
- Expected: `200 OK`

### ❌ TC48 — `status` sai giá trị
- Expected: `422 Unprocessable`

### ❌ TC49 — User thường không được truy cập
- Expected: `403 Forbidden`

### ❌ TC50 — Không có token
- Expected: `401 Unauthorized`

---

## 9. GET /admin/bookings/{id} — Chi tiết đơn (Admin)

### ✅ TC51 — Lấy chi tiết thành công
- Expected: `200 OK`
- Verify: có `booking_items`, `payments`, `user`

### ❌ TC52 — ID không tồn tại
- Expected: `404 Not Found` hoặc `422`

### ❌ TC53 — User thường không được truy cập
- Expected: `403 Forbidden`

### ❌ TC54 — Không có token
- Expected: `401 Unauthorized`

---

## 10. PATCH /admin/bookings/{id}/status — Cập nhật trạng thái

### ✅ TC55 — Đổi sang `confirmed`
```json
{ "booking_status": "confirmed" }
```
- Expected: `200 OK`

### ✅ TC56 — Đổi sang `completed`
```json
{ "booking_status": "completed" }
```
- Expected: `200 OK`

### ✅ TC57 — Đổi sang `cancelled`
```json
{ "booking_status": "cancelled" }
```
- Expected: `200 OK`

### ❌ TC58 — `booking_status` sai giá trị
- Expected: `422 Unprocessable`

### ❌ TC59 — Thiếu `booking_status`
- Expected: `422 Unprocessable`

### ❌ TC60 — ID không tồn tại
- Expected: `404 Not Found` hoặc `422`

### ❌ TC61 — Không có token
- Expected: `401 Unauthorized`

---

## 11. POST /admin/bookings/{id}/confirm — Xác nhận đơn

### ✅ TC62 — Xác nhận đơn `pending` thành công
- Expected: `200 OK`
- Verify: `booking_status = confirmed`, `confirmed_at` không null

### ❌ TC63 — Xác nhận đơn đã `confirmed` (idempotent hoặc lỗi)
- Expected: `200 OK` hoặc `422`

### ❌ TC64 — ID không tồn tại
- Expected: `404 Not Found` hoặc `422`

### ❌ TC65 — Không có token
- Expected: `401 Unauthorized`

---

## 12. POST /admin/bookings/{id}/cancel — Hủy đơn (Admin)

### ✅ TC66 — Hủy đơn thành công
```json
{ "cancellation_reason": "Khach hang yeu cau huy" }
```
- Expected: `200 OK`
- Verify: `booking_status = cancelled`

### ❌ TC67 — Hủy đơn đã `cancelled`
- Expected: `422 Unprocessable`

### ❌ TC68 — ID không tồn tại
- Expected: `404 Not Found` hoặc `422`

### ❌ TC69 — Không có token
- Expected: `401 Unauthorized`

---

## 13. POST /admin/bookings/{id}/complete — Hoàn thành đơn

### ✅ TC70 — Hoàn thành đơn `confirmed` thành công
- Expected: `200 OK`
- Verify: `booking_status = completed`

### ❌ TC71 — Hoàn thành đơn chưa `confirmed`
- Expected: `422 Unprocessable`

### ❌ TC72 — ID không tồn tại
- Expected: `404 Not Found` hoặc `422`

### ❌ TC73 — Không có token
- Expected: `401 Unauthorized`

---

## 14. GET /admin/bookings/export — Export Excel

### ✅ TC74 — Export thành công
- Expected: `200 OK`
- Verify: Content-Type là CSV hoặc Excel

### ✅ TC75 — Export với filter
- Expected: `200 OK`

### ❌ TC76 — User thường không được export
- Expected: `403 Forbidden`

### ❌ TC77 — Không có token
- Expected: `401 Unauthorized`

---

## Tổng kết

| TC | API | Trường hợp | Expected |
|----|-----|-----------|----------|
| TC01 | POST /bookings/calculate | Tính tiền thành công | 200 |
| TC02 | POST /bookings/calculate | 3 loại khách | 200 |
| TC03-TC08 | POST /bookings/calculate | Validation + auth | 422/401 |
| TC09 | POST /bookings | Đặt thành công | 200/201 |
| TC10 | POST /bookings | Chỉ bắt buộc | 200/201 |
| TC11-TC18 | POST /bookings | Validation + auth | 422/401 |
| TC19 | GET /user/bookings | Lấy danh sách | 200 |
| TC20-TC23 | GET /user/bookings | Filter + paginate | 200 |
| TC24-TC25 | GET /user/bookings | Validation + auth | 422/401 |
| TC26 | GET /user/bookings/{id} | Chi tiết | 200 |
| TC27-TC29 | GET /user/bookings/{id} | 404/403/401 | 404/403/401 |
| TC30 | GET /user/bookings/code/{code} | Chi tiết theo code | 200 |
| TC31-TC32 | GET /user/bookings/code/{code} | 404/401 | 404/401 |
| TC33 | GET /user/bookings/{id}/invoice | Xuất PDF | 200 |
| TC34-TC35 | GET /user/bookings/{id}/invoice | 404/401 | 404/401 |
| TC36 | POST /user/bookings/{id}/cancel | Hủy pending | 200 |
| TC37-TC41 | POST /user/bookings/{id}/cancel | Validation + auth | 422/403/401 |
| TC42 | GET /admin/bookings | Lấy tất cả | 200 |
| TC43-TC47 | GET /admin/bookings | Filter + paginate | 200 |
| TC48-TC50 | GET /admin/bookings | Validation + auth | 422/403/401 |
| TC51 | GET /admin/bookings/{id} | Chi tiết | 200 |
| TC52-TC54 | GET /admin/bookings/{id} | 404/403/401 | 404/403/401 |
| TC55-TC57 | PATCH .../status | Đổi trạng thái | 200 |
| TC58-TC61 | PATCH .../status | Validation + auth | 422/401 |
| TC62 | POST .../confirm | Xác nhận | 200 |
| TC63-TC65 | POST .../confirm | Edge cases | 200/422/401 |
| TC66 | POST .../cancel | Hủy (admin) | 200 |
| TC67-TC69 | POST .../cancel | Edge cases | 422/401 |
| TC70 | POST .../complete | Hoàn thành | 200 |
| TC71-TC73 | POST .../complete | Edge cases | 422/401 |
| TC74-TC75 | GET /admin/bookings/export | Export | 200 |
| TC76-TC77 | GET /admin/bookings/export | Auth | 403/401 |
