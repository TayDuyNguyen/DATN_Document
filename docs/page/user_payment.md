# Màn hình: Thanh toán

> Route: `/payment`
> Quyền: 🔐 Cần đăng nhập
> Mô tả: Xử lý thanh toán sau khi đặt tour — tạo link thanh toán, redirect sang cổng thanh toán, kiểm tra trạng thái và thử lại nếu thất bại.

---

## Layout tổng thể

```
┌─────────────────────────────────────────────────────────────┐
│  HEADER (minimal — logo + step indicator)                  │
├─────────────────────────────────────────────────────────────┤
│  PROGRESS STEPS: 1. Thông tin ✓ → 2. Thanh toán → 3. XN   │
├─────────────────────────────────────────────────────────────┤
│  CENTER CONTENT (max-width 560px, mx-auto)                 │
│  [Trạng thái động theo flow]                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 1. Header Minimal

`bg white border-b #E2E8F0 py-16 px-24 flex justify-between items-center`

- Logo bên trái
- `"Thanh toán an toàn" 14px #64748B` icon `lock 16px #10B981` bên trái
- Progress steps (same style as booking page, step 2 active)

---

## 2. Trạng thái: Đang tạo link thanh toán

**Trigger:** Vào trang sau khi submit form đặt tour → tự động gọi `POST /payments/create`

`center py-64 text-center`

- Spinner `48px #0066CC animate-spin mx-auto`
- Title: `"Đang tạo link thanh toán..." 18px Inter 600 #1E293B mt-16`
- Subtitle: `"Vui lòng không đóng trang này" 14px #94A3B8 mt-8`

---

## 3. Trạng thái: Chờ thanh toán (Redirect)

**Trigger:** Sau khi tạo link thành công → hiển thị trước khi redirect

`center py-32 text-center max-w-480px mx-auto`

**Payment info card:**
`bg white border #E2E8F0 radius-16 p-24 mb-24`

- Logo cổng TT (MoMo/VNPay/ZaloPay): `64x64px mx-auto mb-16`
- Title: `"Thanh toán qua MoMo" 20px Inter 700 #1E293B`
- Amount: `"2.200.000 đ" 32px Inter 700 #FF6B35 mt-8`
- Mã đơn: `"#BK-1008" 13px #94A3B8 mt-4`

**Countdown redirect:**
`bg #EFF6FF border #B3D9FF radius-10 p-14 mt-16 flex items-center gap-8`
- icon `info 18px #0066CC`
- Text: `"Tự động chuyển đến trang thanh toán sau 3 giây..." 13px #0066CC`
- Progress bar: `h-2px bg #B3D9FF radius-full mt-8` · fill `bg #0066CC` animate 0→100% trong 3s

**Buttons:**
- "Thanh toán ngay": `bg #0066CC text white radius-12 py-14 full-width 15px 600 mt-16`
  → redirect đến payment gateway URL
- "Hủy thanh toán": `border #E2E8F0 bg white text #64748B radius-12 py-12 full-width mt-8 13px`
  → navigate `/bookings/{id}` (trang chi tiết đơn)

---

## 4. Trạng thái: Đang xử lý (Polling)

**Trigger:** Sau khi user quay lại từ cổng thanh toán (callback URL)

`center py-64 text-center`

- Spinner `48px #F59E0B animate-spin mx-auto`
- Title: `"Đang xác nhận thanh toán..." 18px Inter 600 #1E293B mt-16`
- Subtitle: `"Hệ thống đang kiểm tra giao dịch của bạn" 14px #94A3B8 mt-8`

**Polling:** `GET /payments/status/{transaction_code}` mỗi 3 giây (tối đa 30 giây)

---

## 5. Trạng thái: Thanh toán thành công

**Trigger:** Polling trả về `status=paid`

`center py-32 text-center max-w-480px mx-auto`

- Confetti animation (optional)
- SVG icon `check_circle 80px #10B981 mx-auto`
- Title: `"Thanh toán thành công!" 24px Inter 700 #1E293B mt-16`
- Subtitle: `"Đơn đặt tour của bạn đã được xác nhận" 14px #64748B mt-8`

**Booking summary card:**
`bg white border #E2E8F0 radius-16 p-20 mt-24 text-left`

`space-y-12 flex justify-between 13px`

| Label | Value |
|-------|-------|
| Mã đơn | `"#BK-1008" 13px Inter 700 #0066CC` |
| Tour | Tên tour `13px #1E293B` |
| Ngày khởi hành | "15/04/2026" `13px #1E293B` |
| Số người | "2 NL · 1 TE" `13px #1E293B` |
| Tổng tiền | `"2.200.000 đ" 14px Inter 700 #FF6B35` |
| Phương thức TT | Badge MoMo/VNPay/ZaloPay |

**Buttons:**
- "Xem chi tiết đơn hàng": `bg #0066CC text white radius-12 py-12 px-24 14px 600 mt-20`
  → navigate `/bookings/{id}`
- "Về trang chủ": `border #E2E8F0 bg white text #64748B radius-12 py-12 px-24 mt-8`
  → navigate `/`

**Email confirmation note:**
`flex items-center gap-8 mt-16 justify-center`
icon `email 16px #10B981` + `"Email xác nhận đã được gửi đến nguyenvanan@gmail.com" 12px #64748B`

---

## 6. Trạng thái: Thanh toán thất bại

**Trigger:** Polling trả về `status=failed` hoặc user cancel tại cổng TT

`center py-32 text-center max-w-480px mx-auto`

- SVG icon `error 80px #EF4444 mx-auto`
- Title: `"Thanh toán thất bại" 22px Inter 700 #1E293B mt-16`
- Error message (dynamic):
  - Hủy: `"Bạn đã hủy giao dịch thanh toán." 14px #64748B mt-8`
  - Thất bại: `"Giao dịch không thành công. Vui lòng thử lại." 14px #64748B mt-8`
  - Hết hạn: `"Phiên thanh toán đã hết hạn." 14px #64748B mt-8`

**Retry card:**
`bg #FEF3C7 border rgba(245,158,11,0.2) radius-12 p-16 mt-20`
- `"Đơn hàng #BK-1008 vẫn được giữ trong 15 phút" 13px #92400E`
- Countdown: `"Còn 12:34" 16px Inter 700 #F59E0B mt-4`

**Buttons:**
- "Thử thanh toán lại": `bg #FF6B35 text white radius-12 py-14 full-width 15px 600 mt-16`
  → `POST /payments/retry/{booking_code}` → redirect sang cổng TT
- "Đổi phương thức thanh toán": `border #E2E8F0 bg white text #64748B radius-12 py-12 full-width mt-8`
  → navigate `/tours/{slug}/book` (quay lại form đặt tour)
- "Hủy đơn hàng": `text #EF4444 13px mt-8 cursor-pointer` hover underline
  → `POST /user/bookings/{id}/cancel`

---

## 7. Trạng thái: Hết thời gian polling

**Trigger:** Sau 30 giây polling không có kết quả

`center py-32 text-center max-w-480px mx-auto`

- SVG icon `hourglass_empty 80px #F59E0B mx-auto`
- Title: `"Đang xử lý giao dịch" 20px Inter 600 #1E293B mt-16`
- Subtitle: `"Giao dịch đang được xử lý. Chúng tôi sẽ thông báo kết quả qua email." 14px #64748B mt-8 text-center`

**Buttons:**
- "Kiểm tra trạng thái": `bg #0066CC text white radius-12 py-12 px-24 14px 600 mt-20`
  → gọi lại `GET /payments/status/{transaction_code}`
- "Xem đơn hàng của tôi": `border #E2E8F0 bg white text #64748B radius-12 py-12 px-24 mt-8`
  → navigate `/bookings`

---

## 8. API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Tạo link thanh toán | POST | `/payments/create` | Khi mount (từ booking form) |
| Kiểm tra trạng thái | GET | `/payments/status/{transaction_code}` | Polling mỗi 3s sau callback |
| Thử lại thanh toán | POST | `/payments/retry/{booking_code}` | Click "Thử thanh toán lại" |
| Hủy đơn (nếu thất bại) | POST | `/user/bookings/{id}/cancel` | Click "Hủy đơn hàng" |

**Body POST /payments/create:**
```json
{
  "booking_id": "*",
  "payment_method": "*"
}
```

**Body POST /payments/retry/{booking_code}:** (không cần body)
