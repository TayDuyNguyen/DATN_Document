# Màn hình: Hóa đơn PDF

> Route: `/bookings/{id}/invoice`
> Quyền: 🔐 Cần đăng nhập
> Mô tả: Xem và tải hóa đơn PDF của đơn đặt tour.

---

## Ghi chú quan trọng

API `GET /user/bookings/{id}/invoice` trả về **file PDF trực tiếp** (không phải JSON).

Có 2 cách xử lý:

| Cách | Mô tả |
|------|-------|
| **Download trực tiếp** | Browser tự tải file PDF về máy |
| **Preview trong browser** | Mở PDF trong tab mới hoặc iframe |

---

## Không có màn riêng

Màn này **không có UI trang riêng** — chỉ là action trigger từ các màn khác:

| Từ đâu | Trigger | Hành động |
|--------|---------|-----------|
| `/bookings/{id}` | Click "In hóa đơn" | Download PDF hoặc mở tab mới |
| `/bookings` (list) | — | Không có nút trực tiếp |
| Email xác nhận | Link "Tải hóa đơn" | Download PDF |

---

## Loading State (khi đang tải PDF)

**Hiển thị overlay trên button "In hóa đơn":**

- Button: disabled · spinner `16px` · `"Đang tải hóa đơn..."` · `bg #3385D6`
- Duration: thường 1-3 giây

---

## Nội dung PDF (Layout hóa đơn)

Mặc dù không có UI trang, backend tạo PDF với layout sau:

```
┌─────────────────────────────────────────────────────────────┐
│  LOGO + Tên công ty                    HÓA ĐƠN ĐIỆN TỬ     │
│  Địa chỉ · Điện thoại · Email          Số: #BK-1008         │
│                                         Ngày: 06/04/2026    │
├─────────────────────────────────────────────────────────────┤
│  THÔNG TIN KHÁCH HÀNG                                       │
│  Họ tên · Email · Điện thoại                                │
├─────────────────────────────────────────────────────────────┤
│  CHI TIẾT DỊCH VỤ                                           │
│  Tên tour · Ngày KH · Số lượng · Đơn giá · Thành tiền      │
├─────────────────────────────────────────────────────────────┤
│  TỔNG CỘNG: 2.200.000 đ                                     │
│  Phương thức TT: MoMo                                       │
│  Trạng thái: Đã thanh toán                                  │
├─────────────────────────────────────────────────────────────┤
│  Cảm ơn quý khách · QR code đơn hàng                       │
└─────────────────────────────────────────────────────────────┘
```

---

## Error States

| Tình huống | Xử lý |
|-----------|-------|
| Đơn chưa thanh toán | Toast `"Hóa đơn chỉ có sau khi thanh toán thành công" bg #FEF3C7 text #F59E0B` |
| Lỗi server | Toast `"Không thể tải hóa đơn. Vui lòng thử lại." bg #FEE2E2 text #EF4444` |
| Không có quyền | Redirect `/login` |

---

## API Mapping

| Hành động | Method | Endpoint | Response |
|-----------|--------|----------|---------|
| Tải hóa đơn | GET | `/user/bookings/{id}/invoice` | `application/pdf` file |
