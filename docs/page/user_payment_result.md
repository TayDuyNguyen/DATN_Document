# Màn hình: Kết quả Thanh toán

> Route: `/payment/result`
> Quyền: 🔐 Cần đăng nhập
> Mô tả: Trang callback sau khi cổng thanh toán redirect về — kiểm tra trạng thái giao dịch và hiển thị kết quả.

---

## Ghi chú quan trọng

Màn này là **callback URL** mà cổng thanh toán (MoMo/VNPay/ZaloPay) redirect về sau khi user hoàn tất hoặc hủy thanh toán.

URL thường có dạng:
`/payment/result?transaction_code=TXN-001&status=success`
hoặc
`/payment/result?transaction_code=TXN-001&status=failed`

---

## Tái sử dụng từ màn Thanh toán

> Xem chi tiết tại `user_payment.md`

Màn này hiển thị **đúng 1 trong 3 trạng thái** từ `user_payment.md`:

| Trạng thái | Điều kiện | Xem tại |
|-----------|-----------|---------|
| Đang xử lý (Polling) | Vừa redirect về, chưa có kết quả | Section 4 |
| Thanh toán thành công | Polling trả về `status=paid` | Section 5 |
| Thanh toán thất bại | Polling trả về `status=failed` hoặc user cancel | Section 6 |

---

## Flow xử lý khi mount

```
1. Lấy transaction_code từ URL params
2. Gọi GET /payments/status/{transaction_code}
3. Nếu status=paid → hiển thị Thành công
4. Nếu status=failed/cancelled → hiển thị Thất bại
5. Nếu status=pending → bắt đầu polling mỗi 3s (tối đa 30s)
6. Nếu hết 30s vẫn pending → hiển thị Hết thời gian
```

---

## API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Kiểm tra trạng thái | GET | `/payments/status/{transaction_code}` | Khi mount + polling |
| Thử lại (nếu thất bại) | POST | `/payments/retry/{booking_code}` | Click "Thử lại" |
| Hủy đơn (nếu thất bại) | POST | `/user/bookings/{id}/cancel` | Click "Hủy đơn" |
