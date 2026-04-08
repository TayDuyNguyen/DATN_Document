# Màn hình: Chi tiết Đơn đặt tour

> Route: `/bookings/{id}`
> Quyền: 🔐 Cần đăng nhập
> Mô tả: Xem đầy đủ thông tin đơn đặt tour — tour, lịch khởi hành, số lượng, thanh toán và trạng thái.

---

## Tái sử dụng từ màn Hồ sơ cá nhân

> Xem chi tiết layout tại `user_profile.md`

Giữ nguyên: Header · Sidebar (item "Đơn đặt tour" active) · Footer

---

## Breadcrumb

`py-12 border-b #E2E8F0`
`"Trang chủ / Đơn đặt tour / #BK-1008" 13px #94A3B8`

---

## Main Content

### 1. Page Header

`flex justify-between items-center mb-24`

**Bên trái:**
- `flex items-center gap-12`
  - Title: `"#BK-1008" 22px Inter 700 #1E293B`
  - Badge TT đơn: `11px 700 rounded-full px-10 py-4`
  - Badge TT thanh toán: `11px 700 rounded-full px-10 py-4`

**Bên phải** (`flex gap-8`):
- Button "In hóa đơn": `border #E2E8F0 bg white text #64748B radius-10 px-16 py-10` icon `print`
  → `GET /user/bookings/{id}/invoice` (PDF)
- Button "Hủy đơn" (nếu status=pending/confirmed):
  `border #FEE2E2 bg white text #EF4444 radius-10 px-16 py-10` icon `cancel`
  hover `bg #FEE2E2`
  → confirm dialog

---

### 2. Status Timeline

`bg white border #E2E8F0 radius-16 p-20 mb-20`

`flex justify-between items-center`

4 steps: Đặt tour → Xác nhận → Khởi hành → Hoàn tất

Mỗi step:
- Circle: `32x32px rounded-full flex items-center justify-center`
  - Done: `bg #10B981 text white` icon `check`
  - Active: `bg #0066CC text white` icon tương ứng
  - Pending: `bg #E2E8F0 text #94A3B8`
- Label: `12px Inter 500` bên dưới
  - Done/Active: `#1E293B`
  - Pending: `#94A3B8`
- Timestamp: `11px #94A3B8 mt-2`

Connector line: `flex-1 h-1px bg #E2E8F0 mx-8`
- Done: `bg #10B981`

---

### 3. Tour Info

`bg white border #E2E8F0 radius-16 overflow-hidden mb-20`

**Header** (`px-20 py-16 border-b #F1F5F9`):
- Title: `"Thông tin tour" 15px Inter 600 #1E293B`

**Body** (`flex gap-16 p-20`):
- Thumbnail: `100x100px radius-12 object-cover flex-shrink-0`
- Right:
  - Tên tour: `18px Inter 700 #1E293B`
  - Danh mục: `11px 600 bg #FFE0D4 text #FF6B35 radius-full px-8 py-2 mt-6`
  - `flex flex-wrap gap-16 mt-10`:
    - icon `calendar_today 14px #94A3B8` + "Ngày KH: 15/04/2026" `13px #64748B`
    - icon `access_time 14px #94A3B8` + "07:00" `13px #64748B`
    - icon `schedule 14px #94A3B8` + "1 ngày" `13px #64748B`
    - icon `flag 14px #94A3B8` + "Trước cổng Bà Nà Hills" `13px #64748B`
  - Button "Xem tour →": `13px #0066CC mt-10` hover underline
    → `/tours/{slug}`

---

### 4. Booking Details

`bg white border #E2E8F0 radius-16 p-20 mb-20`

**Title:** `"Chi tiết đặt chỗ" 15px Inter 600 #1E293B mb-16`

`grid grid-cols-2 gap-16`

Mỗi item: `flex flex-col gap-4`
- Label: `11px uppercase #94A3B8`
- Value: `14px Inter 500 #1E293B`

| Label | Value |
|-------|-------|
| MÃ ĐƠN HÀNG | "#BK-1008" `14px Inter 700 #0066CC` |
| NGÀY ĐẶT | "06/04/2026 14:30" |
| NGÀY KHỞI HÀNH | "15/04/2026" |
| SỐ LƯỢNG | "2 Người lớn · 1 Trẻ em" |
| GHI CHÚ | text hoặc "—" `italic #94A3B8` |
| PHƯƠNG THỨC TT | Badge MoMo/VNPay/ZaloPay |

---

### 5. Price Summary

`bg white border #E2E8F0 radius-16 p-20 mb-20`

**Title:** `"Tóm tắt thanh toán" 15px Inter 600 #1E293B mb-16`

`space-y-10 flex justify-between 13px`

- "Người lớn × 2": "1.700.000 đ" `#1E293B`
- "Trẻ em × 1": "500.000 đ" `#1E293B`
- Divider `1px #F1F5F9`
- "Giảm giá": "0 đ" `#10B981`
- Divider
- "TỔNG CỘNG": `"2.200.000 đ" 18px Inter 700 #FF6B35`

**TT thanh toán** (`mt-12 pt-12 border-t #F1F5F9 flex justify-between`):
- Label: `"Trạng thái thanh toán" 13px #94A3B8`
- Badge TT thanh toán

---

### 6. Customer Info

`bg white border #E2E8F0 radius-16 p-20 mb-20`

**Title:** `"Thông tin khách hàng" 15px Inter 600 #1E293B mb-16`

`space-y-12`

Mỗi item: `flex items-center gap-12`
- Icon container: `36x36px radius-8 bg #F8FAFC border #E2E8F0`
  - Icon: `18px #0066CC`
- Right: Label `11px #94A3B8` + Value `13px Inter 500 #1E293B`

| Icon | Label | Value |
|------|-------|-------|
| `person` | HỌ TÊN | "Nguyễn Văn An" |
| `email` | EMAIL | "nguyenvanan@gmail.com" |
| `phone` | ĐIỆN THOẠI | "0905 xxx xxx" |
| `location_on` | ĐỊA CHỈ | text hoặc "—" |

---

### 7. Action Buttons

`flex flex-col gap-8`

- "In hóa đơn PDF": `border #E2E8F0 bg white text #64748B radius-10 py-12 full-width 14px 600` icon `print`
  → `GET /user/bookings/{id}/invoice`

- "Đặt lại tour" (nếu completed/cancelled): `bg #FF6B35 text white radius-10 py-12 full-width 14px 600` icon `refresh`
  → `/tours/{slug}`

- "Viết đánh giá" (nếu completed + chưa đánh giá): `bg #0066CC text white radius-10 py-12 full-width 14px 600` icon `star`
  → mở modal viết đánh giá

- "Hủy đơn" (nếu pending/confirmed): `border #FEE2E2 bg white text #EF4444 radius-10 py-12 full-width 14px 600` icon `cancel`
  hover `bg #FEE2E2`
  → confirm dialog

---

### 8. Confirm Hủy đơn Dialog

`Modal w-440px backdrop rgba(0,0,0,0.4)`

- Header: icon `warning_amber 40x40 bg #FEE2E2 radius-10 color #EF4444`
  + `"Hủy đơn #BK-1008?" 16px 700 #1E293B`
- Body:
  - `"Đơn hàng sẽ bị hủy vĩnh viễn." 14px #64748B`
  - Textarea "Lý do hủy" (optional): `rows-3 border #E2E8F0 radius-10 px-14 py-10 14px`
  - Warning `bg #FEF3C7 radius-8 p-12 mt-8 13px #92400E`:
    "⚠ Chính sách hủy: Miễn phí trước 24 giờ. Sau đó mất 50% phí."
- Footer: "Đóng" (ghost) + "Xác nhận hủy" `bg #EF4444 hover #DC2626`

---

## API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load chi tiết | GET | `/user/bookings/{id}` | Khi mount |
| Hủy đơn | POST | `/user/bookings/{id}/cancel` | Confirm dialog |
| In hóa đơn | GET | `/user/bookings/{id}/invoice` | Click "In hóa đơn" |
