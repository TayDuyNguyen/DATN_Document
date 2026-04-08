# Màn hình: Đặt Tour

> Route: `/tours/{slug}/book`
> Quyền: 🔐 Cần đăng nhập
> Mô tả: Form đặt tour — chọn lịch khởi hành, số lượng người, thông tin khách hàng và phương thức thanh toán.

---

## Layout tổng thể

```
┌─────────────────────────────────────────────────────────────┐
│  HEADER (minimal — logo + tên tour)                        │
├─────────────────────────────────────────────────────────────┤
│  PROGRESS STEPS: 1. Thông tin → 2. Thanh toán → 3. Xác nhận│
├──────────────────────────────────┬──────────────────────────┤
│  FORM (flex-1)                   │  ORDER SUMMARY (360px)   │
│  Step 1:                         │  sticky top-24           │
│  - Chọn lịch khởi hành           │  - Ảnh + Tên tour        │
│  - Số lượng người                │  - Lịch đã chọn          │
│  - Thông tin khách hàng          │  - Số lượng              │
│  - Ghi chú                       │  - Bảng tính giá         │
│  - Phương thức thanh toán        │  - Chính sách hủy        │
│  - Button Tiếp tục               │                          │
└──────────────────────────────────┴──────────────────────────┘
│  FOOTER minimal                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 1. Header Minimal

`bg white border-b #E2E8F0 py-16 px-24 flex justify-between items-center`

- Logo bên trái
- Tên tour: `"Đặt tour: Bà Nà Hills - Cầu Vàng" 14px Inter 500 #64748B` (truncate)
- Button "← Quay lại": `13px #0066CC` → navigate `/tours/{slug}`

---

## 2. Progress Steps

`bg white border-b #E2E8F0 py-16`

`flex justify-center gap-0 max-w-600px mx-auto`

| Step | Label | State |
|------|-------|-------|
| 1 | Thông tin đặt tour | Active: `bg #0066CC text white` |
| → | | Connector line |
| 2 | Thanh toán | Pending: `bg #E2E8F0 text #94A3B8` |
| → | | |
| 3 | Xác nhận | Pending |

Mỗi step: `flex items-center gap-8`
- Circle: `28x28px rounded-full flex items-center justify-center 13px Inter 700`
  - Active: `bg #0066CC text white`
  - Done: `bg #10B981 text white` icon `check`
  - Pending: `bg #E2E8F0 text #94A3B8`
- Label: `13px Inter 500`
  - Active: `#0066CC font-600`
  - Done: `#10B981`
  - Pending: `#94A3B8`

---

## 3. Form — Step 1: Thông tin đặt tour

**Card:** `bg white border #E2E8F0 radius-16 p-24 mb-20`

### 3.1 Chọn lịch khởi hành

- Section title: `"Chọn ngày khởi hành" 16px Inter 600 #1E293B mb-16`

**Calendar picker:**
`border #E2E8F0 radius-12 p-16`

- Header: `flex justify-between items-center mb-12`
  - `"Tháng 4, 2026" 15px Inter 600 #1E293B`
  - Prev/Next: `28x28px border #E2E8F0 radius-8 bg white color #64748B`

- Grid 7 cột (Thứ 2 → CN):
  - Header: `"T2 T3 T4 T5 T6 T7 CN" 11px #94A3B8 text-center`
  - Mỗi ngày: `32x32px rounded-full flex items-center justify-center 13px cursor-pointer`
    - Có lịch: `hover bg #EFF6FF text #0066CC`
    - Đã chọn: `bg #0066CC text white`
    - Hết chỗ: `text #94A3B8 line-through cursor-not-allowed`
    - Ngày qua: `text #E2E8F0 cursor-not-allowed`
    - Hôm nay: `border border-#0066CC text #0066CC`

**Thông tin lịch đã chọn** (hiện sau khi chọn):
`bg #FFF5F0 border rgba(255,107,53,0.2) radius-10 p-14 mt-12 flex justify-between items-center`
- Left:
  - `"15/04/2026 (Thứ Tư)" 14px Inter 600 #1E293B`
  - `"Còn 8/20 chỗ" 12px #10B981 mt-2`
- Right: Progress bar `w-80px h-4px bg #E2E8F0 radius-full` · fill `bg #FF6B35` 40%

---

### 3.2 Số lượng người

**Card:** `bg white border #E2E8F0 radius-16 p-24 mb-20`

- Section title: `"Số lượng người" 16px Inter 600 #1E293B mb-16`

**Counter rows** (`space-y-16`):

Mỗi loại:
`flex justify-between items-center py-12 border-b #F1F5F9`

| Loại | Giá | Min | Max |
|------|-----|-----|-----|
| Người lớn | 850.000 đ/người | 1 | max_people |
| Trẻ em (5-12 tuổi) | 500.000 đ/người | 0 | max_people |
| Em bé (< 5 tuổi) | Miễn phí | 0 | max_people |

- Left:
  - Label: `14px Inter 600 #1E293B`
  - Giá: `12px #94A3B8`
- Right: `flex items-center gap-16`
  - Button `-`: `32x32px border #E2E8F0 radius-full bg white 18px #64748B`
    disabled: `opacity-40 cursor-not-allowed`
    hover: `border #0066CC color #0066CC`
  - Count: `18px Inter 700 #1E293B w-32px text-center`
  - Button `+`: `32x32px bg #0066CC text white rounded-full 18px`
    disabled: `bg #E2E8F0 cursor-not-allowed`
    hover: `bg #004999`

**Tổng tạm tính** (realtime, API: `POST /bookings/calculate`):
`bg #F8FAFC border #E2E8F0 radius-10 p-14 mt-16`
- Rows (`space-y-8 flex justify-between 13px`):
  - "Người lớn × 2": "1.700.000 đ"
  - "Trẻ em × 1": "500.000 đ"
- Divider `1px #E2E8F0`
- "TỔNG CỘNG": `"2.200.000 đ" 18px Inter 700 #FF6B35`

---

### 3.3 Thông tin khách hàng

**Card:** `bg white border #E2E8F0 radius-16 p-24 mb-20`

- Section title: `"Thông tin khách hàng" 16px Inter 600 #1E293B mb-16`
- Note: `"Thông tin này dùng để liên hệ và xác nhận đặt tour" 13px #94A3B8 mb-16`

**Pre-fill từ profile** (nếu đã đăng nhập):
`bg #EFF6FF border #B3D9FF radius-10 p-12 mb-16 flex justify-between items-center`
- `"Điền từ hồ sơ của bạn" 13px #0066CC`
- Button "Điền ngay": `13px 600 #0066CC` → auto-fill fields

**Grid 2 cột** (`grid grid-cols-2 gap-16`):

| Field | Type | Bắt buộc | Col |
|-------|------|----------|-----|
| Họ và tên | text | ✅ | 2 |
| Email | email | ✅ | 1 |
| Số điện thoại | tel | ✅ | 1 |
| Địa chỉ | text | — | 2 |

**Ghi chú** (full width):
- Textarea `rows-3` · placeholder "Yêu cầu đặc biệt, dị ứng thức ăn, v.v..."

---

### 3.4 Phương thức thanh toán

**Card:** `bg white border #E2E8F0 radius-16 p-24 mb-20`

- Section title: `"Phương thức thanh toán" 16px Inter 600 #1E293B mb-16`

**Radio group** (`space-y-12`):

Mỗi option: `flex items-center gap-12 p-16 border-2 radius-12 cursor-pointer`
- Unselected: `border #E2E8F0 bg white`
- Selected: `border #0066CC bg #EFF6FF`

| Option | Logo | Label |
|--------|------|-------|
| MoMo | Logo MoMo | "Ví MoMo" |
| VNPay | Logo VNPay | "VNPay" |
| ZaloPay | Logo ZaloPay | "ZaloPay" |

- Left: Radio `16px accent-color #0066CC` + Logo `32x32px` + Label `14px Inter 600 #1E293B`
- Right: Badge `"Phổ biến" bg #D1FAE5 text #10B981 11px 600 radius-full px-8 py-2` (MoMo)

---

### 3.5 Điều khoản & Button

**Checkbox:**
`flex items-start gap-8 mb-20`
- Checkbox `16px accent-color #0066CC`
- Label: `13px #64748B` "Tôi đồng ý với [Điều khoản sử dụng](link) và [Chính sách hủy tour](link)"

**Button "Tiếp tục thanh toán":**
`bg #FF6B35 text white radius-12 py-14 full-width 16px Inter 600`
icon `arrow_forward` bên phải
hover `bg #E55A2B`
shadow `0 4px 12px rgba(255,107,53,0.25)`
disabled khi chưa chọn đủ thông tin: `bg #E2E8F0 text #94A3B8 cursor-not-allowed`

→ Submit `POST /bookings` → navigate `/payment`

---

## 4. Order Summary (Sidebar)

**Card:** `bg white border #E2E8F0 radius-16 p-20 sticky top-24`

### 4.1 Tour info

`flex gap-12 mb-16 pb-16 border-b #F1F5F9`
- Thumbnail: `80x80px radius-10 object-cover`
- Right:
  - Tên: `14px Inter 600 #1E293B` max 2 lines
  - Danh mục: `11px bg #FFE0D4 text #FF6B35 radius-full px-8 py-2`
  - Thời lượng: `12px #94A3B8 mt-4` icon `schedule`

### 4.2 Chi tiết đặt

`space-y-10 mb-16 pb-16 border-b #F1F5F9`

| Label | Value |
|-------|-------|
| Ngày khởi hành | "15/04/2026" hoặc "Chưa chọn" `#94A3B8` |
| Giờ khởi hành | "07:00" |
| Điểm tập trung | "Trước cổng Bà Nà Hills" |
| Người lớn | "× 2" |
| Trẻ em | "× 1" |

`13px flex justify-between` · Label `#94A3B8` · Value `#1E293B`

### 4.3 Bảng giá

`bg #F8FAFC radius-10 p-14 mb-16`

`space-y-8 flex justify-between 13px`
- "Người lớn × 2": "1.700.000 đ"
- "Trẻ em × 1": "500.000 đ"
- Divider
- "TỔNG CỘNG": `"2.200.000 đ" 16px Inter 700 #FF6B35`

### 4.4 Chính sách hủy

`bg #FEF3C7 border rgba(245,158,11,0.2) radius-10 p-12`

- icon `info 16px #F59E0B`
- Text `12px #92400E line-height 1.5`:
  "Hủy miễn phí trước 24 giờ. Hủy trong vòng 24 giờ mất 50% phí."

---

## 5. API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Tính giá realtime | POST | `/bookings/calculate` | Thay đổi số lượng người |
| Đặt tour | POST | `/bookings` | Submit form |

**Body POST /bookings/calculate:**
```json
{
  "tour_id": "*",
  "tour_schedule_id": "*",
  "quantity_adult": "*",
  "quantity_child": 0,
  "quantity_infant": 0
}
```

**Body POST /bookings:**
```json
{
  "tour_id": "*",
  "tour_schedule_id": "*",
  "quantity_adult": "*",
  "quantity_child": 0,
  "quantity_infant": 0,
  "customer_name": "*",
  "customer_email": "*",
  "customer_phone": "*",
  "customer_address": "",
  "customer_note": "",
  "payment_method": "*"
}
```
