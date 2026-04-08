# Màn hình: Chi tiết Đơn hàng

> Route: `/admin/bookings/{id}`
> Quyền: 🛡️ Admin / Staff
> Mô tả: Xem toàn bộ thông tin chi tiết đơn đặt tour — thông tin khách hàng, tour, lịch khởi hành, thanh toán, lịch sử trạng thái. Thực hiện các hành động xác nhận, hủy, hoàn thành đơn.

---

## Layout tổng thể

```
┌─────────────────────────────────────────────────────────────────┐
│  HEADER: Breadcrumb + Mã đơn + Badges + [In HĐ] [Xác nhận]    │
├──────────────────────────────────────┬──────────────────────────┤
│  LEFT COLUMN (65%)                   │  RIGHT COLUMN (320px)    │
│                                      │  sticky top-24           │
│  Section 1: Thông tin đơn hàng       │  Card 1: Tóm tắt TT      │
│  Section 2: Thông tin khách hàng     │  Card 2: Thao tác        │
│  Section 3: Chi tiết tour đặt        │  Card 3: Thông tin nhanh │
│  Section 4: Lịch sử trạng thái       │                          │
└──────────────────────────────────────┴──────────────────────────┘
```

---

## 1. Page Header

`flex justify-between items-start, mb 24px`

### Bên trái

| Element | Style |
|---------|-------|
| Breadcrumb | `12px Inter 500 #94A3B8` — "Đơn hàng & Thanh toán / Danh sách Đơn hàng / #BK-1008" |
| Title + Badges | `flex items-center gap-12 mt-4` |
| Title | `24px Inter 700 #1E293B` — "#BK-1008" |
| Badge TT đơn | `11px 700 rounded-full px-10 py-4` theo status |
| Badge TT thanh toán | `11px 700 rounded-full px-10 py-4` theo payment_status |
| Subtitle | `13px Inter 400 #94A3B8` — "Đặt lúc 06/04/2026 14:30 · Cập nhật 06/04/2026 15:00" |

**Badge TT đơn:**
| Status | Background | Text |
|--------|-----------|------|
| pending | `#FEF3C7` | `#F59E0B` "CHỜ XÁC NHẬN" |
| confirmed | `#DBEAFE` | `#3B82F6` "ĐÃ XÁC NHẬN" |
| completed | `#D1FAE5` | `#10B981` "HOÀN TẤT" |
| cancelled | `#FEE2E2` | `#EF4444` "ĐÃ HỦY" |

**Badge TT thanh toán:**
| Status | Background | Text |
|--------|-----------|------|
| paid | `#D1FAE5` | `#10B981` "ĐÃ THANH TOÁN" |
| pending | `#FEF3C7` | `#F59E0B` "CHỜ THANH TOÁN" |
| refunded | `#EEF2FF` | `#6366F1` "HOÀN TIỀN" |

### Bên phải (`flex gap-3`)

| Button | Điều kiện | Style | Action |
|--------|-----------|-------|--------|
| In hóa đơn | Luôn hiện | `border #E2E8F0 bg white text #64748B radius-10 px-16 py-10` icon `print` | `GET /user/bookings/{id}/invoice` |
| Xác nhận | status=pending | `bg #10B981 text white radius-10 px-20 py-10` icon `check_circle` | `POST /admin/bookings/{id}/confirm` |

---

## 2. Left Column

### Section 1 — Thông tin đơn hàng

**Card:** `bg white border #E2E8F0 radius-16 p-24 mb-24`
**Section header:** Icon `receipt #0066CC bg #EFF6FF` + Title "Thông tin đơn hàng"

**Grid 2 cột, gap 20px:**
- Mỗi item: `flex flex-col gap-4`
  - Label: `11px uppercase #94A3B8`
  - Value: `14px Inter 500 #1E293B`

| Label | Value | Style đặc biệt |
|-------|-------|----------------|
| MÃ ĐƠN HÀNG | "#BK-1008" | `14px Inter 700 #0066CC` |
| NGÀY ĐẶT | "06/04/2026 14:30" | — |
| PHƯƠNG THỨC TT | "MoMo" / "VNPay" / "ZaloPay" | Badge màu tương ứng |
| MÃ GIAO DỊCH | "TXN-20260406-001" | `13px monospace #64748B` |
| GHI CHÚ | text hoặc "—" | `14px #64748B italic` |

**Badge phương thức thanh toán:**
| Method | Background | Text |
|--------|-----------|------|
| MoMo | `#FFE0D4` | `#FF6B35` |
| VNPay | `#EFF6FF` | `#0066CC` |
| ZaloPay | `#D1FAE5` | `#10B981` |

---

### Section 2 — Thông tin khách hàng

**Card:** `bg white border #E2E8F0 radius-16 p-24 mb-24`
**Section header:** Icon `person #10B981 bg #D1FAE5` + Title "Thông tin khách hàng"

`flex items-start gap-16`:
- Avatar: `56x56px rounded-full border-2 #E2E8F0 object-cover`
- Right (`flex-1`):
  - Name: `16px Inter 700 #1E293B`
  - `flex gap-16 mt-8`:
    - icon `email 16px #94A3B8` + email `13px #64748B` (link `mailto:`)
    - icon `phone 16px #94A3B8` + phone `13px #64748B` (link `tel:`)
  - `flex gap-16 mt-4`:
    - icon `location_on 16px #94A3B8` + address `13px #64748B`
  - Button "Xem hồ sơ khách hàng" (`mt-12`):
    `border #E2E8F0 bg white text #0066CC radius-8 px-14 py-8 icon open_in_new 13px 600`
    → `/admin/users/{user_id}`

---

### Section 3 — Chi tiết tour đặt

**Card:** `bg white border #E2E8F0 radius-16 overflow-hidden mb-24`

**Card header** (`px-24 py-20 border-b #E2E8F0`):
Icon `tour #F59E0B bg #FEF3C7` + Title "Chi tiết tour"

**Tour info** (`px-24 py-20 flex gap-16 border-b #E2E8F0`):
- Thumbnail: `80x80px radius-12 object-cover border #E2E8F0`
- Right:
  - Tên tour: `16px Inter 700 #1E293B`
  - Danh mục tag: `11px 600 bg #EFF6FF text #0066CC border #B3D9FF radius-full px-8 py-2 mt-4`
  - `flex gap-16 mt-8`:
    - icon `schedule 16px #94A3B8` + "1 ngày" `13px #64748B`
    - icon `location_on 16px #94A3B8` + "Bà Nà Hills" `13px #64748B`
  - Button "Xem tour" (`mt-8`):
    `border #E2E8F0 bg white text #0066CC radius-8 px-14 py-8 icon open_in_new 13px 600`
    → `/admin/tours/{tour_id}`

**Schedule info** (`px-24 py-16 bg #F8FAFC border-b #E2E8F0`):
- Label: `"LỊCH KHỞI HÀNH" 10px uppercase #94A3B8 mb-8`
- `flex gap-24`:
  - icon `event` + "Ngày KH: 15/04/2026" `13px Inter 600 #1E293B`
  - icon `event_available` + "Ngày KT: 15/04/2026" `13px #64748B`
  - icon `flag` + "Điểm tập trung: Trước cổng Bà Nà Hills" `13px #64748B`

**Quantity table** (`px-24 py-16`):

`thead bg #F8FAFC` · `th: 11px uppercase #94A3B8`

| Cột | Width |
|-----|-------|
| Loại | auto |
| Số lượng | 100px |
| Đơn giá | 130px |
| Thành tiền | 130px |

Rows:
- Người lớn | 2 | 850.000 đ | 1.700.000 đ
- Trẻ em | 1 | 500.000 đ | 500.000 đ
- Em bé | 0 | — | —

`tfoot border-t #E2E8F0`:
- "TỔNG CỘNG" `13px 700 #1E293B` | | | "2.200.000 đ" `16px Inter 700 #0066CC`

---

### Section 4 — Lịch sử trạng thái

**Card:** `bg white border #E2E8F0 radius-16 p-24 mb-24`
**Section header:** Icon `history #6366F1 bg #EEF2FF` + Title "Lịch sử trạng thái"

**Timeline** (`space-y-0`):
- Mỗi event: `flex gap-16`
  - Left: `flex flex-col items-center`
    - Dot: `10x10px rounded-full` màu theo status
    - Line: `flex-1 w-2px bg #E2E8F0 mx-auto` (không có ở event cuối)
  - Right: `pb-16` (trừ event cuối)
    - `flex justify-between items-start`
      - Left: Badge status + Note `13px #64748B mt-4`
      - Right: Timestamp `12px #94A3B8`

**Sample timeline** (mới nhất lên đầu):
| Dot | Status | Note | Time |
|-----|--------|------|------|
| `#10B981` | HOÀN TẤT | — | "06/04/2026 18:00" |
| `#3B82F6` | ĐÃ XÁC NHẬN | "Xác nhận bởi Admin Duy Tây" | "06/04/2026 15:00" |
| `#F59E0B` | CHỜ XÁC NHẬN | "Đơn hàng được tạo" | "06/04/2026 14:30" |

---

## 3. Right Column — Sidebar

### Card 1 — Tóm tắt thanh toán
`bg white border #E2E8F0 radius-16 p-20 mb-16`

Title: `"Tóm tắt thanh toán" 14px Inter 600 #1E293B mb-16`

Rows (`space-y-10 flex justify-between 13px`):
- "Người lớn (×2)": "1.700.000 đ" `#1E293B`
- "Trẻ em (×1)": "500.000 đ" `#1E293B`
- "Em bé (×0)": "0 đ" `#94A3B8`
- Divider `1px #F1F5F9`
- "Giảm giá": "0 đ" `#10B981`
- Divider
- "TỔNG CỘNG": "2.200.000 đ" `16px Inter 700 #0066CC`

Payment method (`mt-12 pt-12 border-t #F1F5F9 flex justify-between`):
- Label: `"Phương thức" 13px #94A3B8`
- Badge phương thức TT

---

### Card 2 — Thao tác
`bg white border #E2E8F0 radius-16 p-20 mb-16`

Title: `"Thao tác" 14px Inter 600 #1E293B mb-12`

**Buttons hiển thị theo điều kiện:**

| Button | Điều kiện | Style | Action |
|--------|-----------|-------|--------|
| Xác nhận đơn | status=pending | `bg #10B981 text white radius-10 py-10 full-width` icon `check_circle` | `POST /admin/bookings/{id}/confirm` |
| Hoàn thành đơn | status=confirmed | `bg #0066CC text white radius-10 py-10 full-width` icon `task_alt` | `POST /admin/bookings/{id}/complete` |
| Hủy đơn hàng | status=pending/confirmed | `border #FEE2E2 bg white text #EF4444 radius-10 py-10 full-width` icon `cancel` hover `bg #FEE2E2` | Confirm dialog → `POST /admin/bookings/{id}/cancel` |
| In hóa đơn | Luôn hiện | ghost style icon `print` | `GET /user/bookings/{id}/invoice` |
| Xem khách hàng | Luôn hiện | ghost style icon `person` | `/admin/users/{user_id}` |

Ghost style: `border #E2E8F0 bg white text #64748B radius-10 py-10 full-width 13px 600` hover `border #0066CC text #0066CC`

---

### Card 3 — Thông tin nhanh
`bg white border #E2E8F0 radius-16 p-20 mb-16`

Rows (`space-y-10 flex justify-between items-start 13px`):

| Label | Value |
|-------|-------|
| Mã đơn | "#BK-1008" `13px 700 #0066CC` |
| Ngày đặt | "06/04/2026 14:30" `#64748B` |
| Ngày KH | "15/04/2026" `#1E293B` |
| Số người | "2 NL · 1 TE · 0 EB" `#1E293B` |
| Tổng tiền | "2.200.000 đ" `13px 700 #1E293B` |
| Cập nhật | "06/04/2026 18:00" `#94A3B8` |

---

## 4. Confirm Dialogs

### Dialog Hủy đơn

**Modal:** `bg white radius-16 w-440px shadow-modal backdrop rgba(0,0,0,0.4)`

| Vùng | Nội dung |
|------|---------|
| Header | Icon `warning_amber 40x40 bg #FEE2E2 radius-10 color #EF4444` + "Hủy đơn hàng #BK-1008?" `16px 700 #1E293B` |
| Body | "Đơn hàng của [Tên khách] sẽ bị hủy." `14px #64748B` + Textarea "Lý do hủy" (optional) `rows-3 border #E2E8F0 radius-10 px-14 py-10` + Warning `bg #FEF3C7 13px #92400E`: "⚠ Khách hàng sẽ nhận được thông báo hủy đơn qua email." |
| Footer | "Đóng" (ghost) + "Xác nhận hủy" `bg #EF4444 hover #DC2626` |

### Dialog Hoàn thành đơn

**Modal:** `bg white radius-16 w-400px shadow-modal backdrop rgba(0,0,0,0.4)`

| Vùng | Nội dung |
|------|---------|
| Header | Icon `task_alt 40x40 bg #D1FAE5 radius-10 color #10B981` + "Hoàn thành đơn hàng?" `16px 700 #1E293B` |
| Body | "Xác nhận đơn #BK-1008 đã hoàn thành?" `14px #64748B` |
| Footer | "Đóng" (ghost) + "Xác nhận hoàn thành" `bg #10B981 hover #059669` |

---

## 5. API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load chi tiết | GET | `/admin/bookings/{id}` | Khi mount |
| Xác nhận đơn | POST | `/admin/bookings/{id}/confirm` | Click button / confirm dialog |
| Hủy đơn | POST | `/admin/bookings/{id}/cancel` | Confirm dialog hủy |
| Hoàn thành đơn | POST | `/admin/bookings/{id}/complete` | Confirm dialog hoàn thành |
| Đổi trạng thái | PATCH | `/admin/bookings/{id}/status` | Dự phòng |
| In hóa đơn | GET | `/user/bookings/{id}/invoice` | Click "In hóa đơn" |
