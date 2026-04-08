# Màn hình: Báo cáo Doanh thu

> Route: `/admin/reports/revenue`
> Quyền: 🛡️ Admin / Staff
> Mô tả: Báo cáo thống kê doanh thu theo thời gian — biểu đồ xu hướng, top tour doanh thu cao, bảng chi tiết giao dịch và xuất Excel.

---

## Layout tổng thể

```
┌─────────────────────────────────────────────────────────────────┐
│  HEADER: Breadcrumb + Tiêu đề + [Xuất Excel]                    │
├─────────────────────────────────────────────────────────────────┤
│  FILTER BAR: Date range + Quick range + Cổng TT + Áp dụng      │
├─────────────────────────────────────────────────────────────────┤
│  STATS ROW: [Tổng DT] [DT trung bình/ngày] [Giao dịch] [Hoàn tiền] │
├─────────────────────────────────────────────────────────────────┤
│  HÀNG 1: [Line chart doanh thu] [Bar chart top 5 tour]          │
├─────────────────────────────────────────────────────────────────┤
│  HÀNG 2: [Bar chart theo cổng TT] [Pie chart phân bố]          │
├─────────────────────────────────────────────────────────────────┤
│  HÀNG 3: Bảng chi tiết giao dịch (paginate)                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1. Page Header

| Element | Style |
|---------|-------|
| Breadcrumb | `12px Inter 500 #94A3B8` — "Báo cáo / Báo cáo Doanh thu" |
| Title | `24px Inter 700 #1E293B` — "Báo cáo Doanh thu" |
| Subtitle | `14px Inter 400 #64748B` — "Thống kê và phân tích doanh thu hệ thống" |
| Button "Xuất Excel" | `border #E2E8F0 bg white text #64748B radius-10 px-16 py-10` icon `download` | `GET /admin/payments/export` với params hiện tại |

---

## 2. Filter Bar

**Card:** `bg white border #E2E8F0 radius-16 p-20 mb-24`

`flex gap-12 flex-wrap items-end`

| Element | Width | Config |
|---------|-------|--------|
| Date "Từ ngày" | `150px` | Input date · default: đầu tháng hiện tại |
| Date "Đến ngày" | `150px` | Input date · default: hôm nay |
| Quick range | `auto` | Pill buttons: "7 ngày" \| "30 ngày" \| "3 tháng" \| "Năm nay" |
| Select Cổng TT | `160px` | Tất cả / MoMo / VNPay / ZaloPay |
| Button "Áp dụng" | `auto` | `bg #0066CC text white radius-10 px-20 py-10` |

---

## 3. Stats Row

`grid grid-cols-4 gap-4 mb-24`

| Thẻ | Icon | Icon bg | Value | Label | Value color |
|-----|------|---------|-------|-------|-------------|
| Tổng doanh thu | `payments` | `#EEF2FF` | `2.45 tỷ đ` | "TỔNG DOANH THU" | `#6366F1` |
| DT trung bình/ngày | `trending_up` | `#D1FAE5` | `81.7 triệu đ` | "TB / NGÀY" | `#10B981` |
| Tổng giao dịch | `receipt` | `#EFF6FF` | `1.024` | "GIAO DỊCH" | `#0066CC` |
| Đã hoàn tiền | `currency_exchange` | `#FEE2E2` | `38.5 triệu đ` | "HOÀN TIỀN" | `#EF4444` |

Mỗi thẻ có trend badge:
- Tăng: `bg #D1FAE5 text #10B981 11px 600 radius-full px-8 py-2` "↑ +15.2%"
- Giảm: `bg #FEE2E2 text #EF4444` "↓ -2.1%"

---

## 4. Hàng 1 — Biểu đồ chính

`grid grid-cols-2 gap-24 mb-24`

### 4.1 Line Chart — Xu hướng doanh thu

**Card:** `bg white border #E2E8F0 radius-16 p-24`

**Card header** (`flex justify-between mb-20`):
- Left:
  - Title: `"Xu hướng doanh thu" 15px Inter 600 #1E293B`
  - Subtitle: `"TỔNG QUAN" 10px uppercase #94A3B8`
- Right:
  - Total: `"2.450.000.000 đ" 17px Inter 700 #10B981`
  - Sub-label: `"TỔNG KỲ BÁO CÁO" 10px uppercase #94A3B8`

**Period tabs** (`flex gap-4 mb-16`):
- "Ngày" | "Tuần" | "Tháng" — pill style
- Active: `bg #0066CC text white`

**Chart area** (`height 240px`):
- SVG line chart (API: `GET /admin/dashboard/revenue?period=day&from=&to=`)
- Area fill: `linear-gradient rgba(16,185,129,0.08) → transparent`
- Stroke: `#10B981 stroke-width 2.5px`
- Data points: `circle r=3.5 fill #10B981 stroke white`
- Y-axis: values formatted "100 Tr." / "75 Tr." etc.
- Tooltip: `bg white border #E2E8F0 radius-8 p-10 shadow`
  - Date + Revenue formatted

### 4.2 Bar Chart — Top 5 Tour doanh thu cao

**Card:** `bg white border #E2E8F0 radius-16 p-24`

**Card header:**
- Title: `"Top 5 Tour doanh thu cao" 15px Inter 600 #1E293B`

**Horizontal bar chart** (`height 240px`):
- 5 bars nằm ngang, mỗi bar:
  - Label bên trái: tên tour `12px Inter 500 #1E293B max-120px ellipsis`
  - Bar: `height 28px radius-r-6px`
    - Bar 1 (max): fill `#0066CC`
    - Bar 2: fill `#3385D6`
    - Bar 3: fill `#6699CC`
    - Bar 4: fill `#99BBDD`
    - Bar 5: fill `#CCDDEe`
  - Value bên phải: `12px Inter 700 #1E293B` — e.g. "520 triệu đ"
- Background track: `h-28px bg #F1F5F9 radius-6px`

---

## 5. Hàng 2 — Biểu đồ phụ

`grid grid-cols-2 gap-24 mb-24`

### 5.1 Bar Chart — Doanh thu theo cổng thanh toán

**Card:** `bg white border #E2E8F0 radius-16 p-24`

**Card header:**
- Title: `"Theo cổng thanh toán" 15px Inter 600 #1E293B`

**Vertical bar chart** (`height 200px`):
- 3 bars: MoMo · VNPay · ZaloPay
- Bar width: `64px radius-t-8px`
- Colors:
  - MoMo: `#FF6B35`
  - VNPay: `#0066CC`
  - ZaloPay: `#10B981`
- Value label above bar: `12px Inter 700` màu tương ứng
- X-axis label: `11px #94A3B8`
- Background track: full height `bg #F1F5F9 radius-8px`
- Hover: bar brightens 10% + tooltip

**Summary** (`mt-16 grid grid-cols-3 gap-8`):
- Mỗi item: `text-center`
  - Badge cổng: `11px 600 rounded-full px-8 py-3` màu tương ứng
  - Value: `14px Inter 700 #1E293B mt-4`
  - Percent: `11px #94A3B8`

### 5.2 Donut Chart — Phân bố doanh thu

**Card:** `bg white border #E2E8F0 radius-16 p-24`

**Card header:**
- Title: `"Phân bố doanh thu" 15px Inter 600 #1E293B`

**Donut chart** (`height 200px`):
- Segments theo cổng TT:
  - MoMo: `#FF6B35` — 45%
  - VNPay: `#0066CC` — 38%
  - ZaloPay: `#10B981` — 17%
- Center: `"2.45 tỷ" 20px Inter 700 #1E293B` + `"Tổng DT" 11px #94A3B8`

**Legend** (`grid grid-cols-1 gap-8 mt-16`):
- Mỗi item: `flex justify-between items-center`
  - Left: dot + label `12px #64748B`
  - Right: value `12px Inter 700 #1E293B` + percent `11px #94A3B8`

---

## 6. Hàng 3 — Bảng chi tiết giao dịch

**Card:** `bg white border #E2E8F0 radius-16 overflow-hidden`

**Card header** (`flex justify-between px-24 py-20 border-b #E2E8F0`):
- Title: `"Chi tiết giao dịch" 15px Inter 600 #1E293B`
- Right: `"1.024 giao dịch" 13px #94A3B8` + Button "Xuất Excel" ghost

**Table** (API: `GET /admin/reports/revenue-detail?from=&to=`):

`thead bg #F8FAFC` · `th: px-16 py-12, 11px uppercase #94A3B8`

| Cột | Width |
|-----|-------|
| Mã GD | 150px |
| Mã đơn | 110px |
| Khách hàng | 180px |
| Tour | auto |
| Cổng TT | 110px |
| Số tiền | 130px |
| Ngày GD | 130px |
| Trạng thái | 120px |

`tbody: border-b #F1F5F9 hover bg #F8FAFC`

- Mã GD: `13px Inter 700 #1E293B`
- Mã đơn: `13px Inter 600 #0066CC` hover underline → `/admin/bookings/{id}`
- Khách hàng: Avatar `24x24px` + Name `13px Inter 500 #1E293B`
- Tour: `13px #1E293B max-1-line ellipsis`
- Cổng TT: badge màu (MoMo/VNPay/ZaloPay)
- Số tiền: `13px Inter 700 #1E293B`
- Ngày GD: Date `13px #1E293B` + Time `11px #94A3B8`
- Trạng thái: badge (paid/pending/refunded/failed)

**Pagination** (`px-24 py-16 border-t #E2E8F0 bg #F8FAFC flex justify-between`):
- `"Hiển thị 1–10 / 1.024 giao dịch" 13px #64748B`
- Prev · 1 · 2 · ... · 103 · Next

---

## 7. API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load biểu đồ xu hướng | GET | `/admin/dashboard/revenue?period=day&from=&to=` | Khi mount, đổi filter/period |
| Load báo cáo + bảng | GET | `/admin/reports/revenue-detail?from=&to=` | Khi mount, đổi filter |
| Xuất Excel | GET | `/admin/payments/export?payment_gateway=&date_from=&date_to=` | Click "Xuất Excel" |
