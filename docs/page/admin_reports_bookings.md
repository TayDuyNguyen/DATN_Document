# Màn hình: Báo cáo Đơn hàng

> Route: `/admin/reports/bookings`
> Quyền: 🛡️ Admin / Staff
> Mô tả: Báo cáo thống kê đơn hàng theo thời gian — biểu đồ xu hướng, phân bố trạng thái, bảng chi tiết và xuất Excel.

---

## Layout tổng thể

```
┌─────────────────────────────────────────────────────────────────┐
│  HEADER: Breadcrumb + Tiêu đề + [Xuất Excel]                    │
├─────────────────────────────────────────────────────────────────┤
│  FILTER BAR: Date range + Trạng thái + Trạng thái TT + Lọc     │
├─────────────────────────────────────────────────────────────────┤
│  STATS ROW: [Tổng đơn] [Hoàn tất] [Đã hủy] [Doanh thu]        │
├─────────────────────────────────────────────────────────────────┤
│  HÀNG 1: [Line chart xu hướng đơn hàng] [Pie chart trạng thái] │
├─────────────────────────────────────────────────────────────────┤
│  HÀNG 2: Bảng chi tiết đơn hàng (paginate)                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1. Page Header

| Element | Style |
|---------|-------|
| Breadcrumb | `12px Inter 500 #94A3B8` — "Báo cáo / Báo cáo Đơn hàng" |
| Title | `24px Inter 700 #1E293B` — "Báo cáo Đơn hàng" |
| Subtitle | `14px Inter 400 #64748B` — "Thống kê và phân tích đơn đặt tour" |
| Button "Xuất Excel" | `border #E2E8F0 bg white text #64748B radius-10 px-16 py-10` icon `download` | `GET /admin/bookings/export` với params hiện tại |

---

## 2. Filter Bar

**Card:** `bg white border #E2E8F0 radius-16 p-20 mb-24`

`flex gap-12 flex-wrap items-end`

| Element | Width | Config |
|---------|-------|--------|
| Date "Từ ngày" | `150px` | Input date · default: đầu tháng hiện tại |
| Date "Đến ngày" | `150px` | Input date · default: hôm nay |
| Quick range | `auto` | Pill buttons: "7 ngày" \| "30 ngày" \| "3 tháng" \| "Năm nay" · Active: `bg #0066CC text white` · Inactive: `bg #F1F5F9 text #64748B` |
| Select Trạng thái đơn | `170px` | Tất cả / pending / confirmed / completed / cancelled |
| Select Trạng thái TT | `170px` | Tất cả / pending / paid / refunded |
| Button "Áp dụng" | `auto` | `bg #0066CC text white radius-10 px-20 py-10` |

---

## 3. Stats Row

`grid grid-cols-4 gap-4 mb-24`

| Thẻ | Icon | Icon bg | Value | Label | Value color |
|-----|------|---------|-------|-------|-------------|
| Tổng đơn hàng | `shopping_cart` | `#EFF6FF` | `1.248` | "TỔNG ĐƠN HÀNG" | `#1E293B` |
| Hoàn tất | `check_circle` | `#D1FAE5` | `936` | "HOÀN TẤT" | `#10B981` |
| Đã hủy | `cancel` | `#FEE2E2` | `124` | "ĐÃ HỦY" | `#EF4444` |
| Doanh thu | `payments` | `#EEF2FF` | `2.45 tỷ đ` | "DOANH THU" | `#6366F1` |

Mỗi thẻ có thêm trend badge (`mt-8`):
- Tăng: `bg #D1FAE5 text #10B981 11px 600 radius-full px-8 py-2` "↑ +12.5% so với kỳ trước"
- Giảm: `bg #FEE2E2 text #EF4444` "↓ -3.2%"

---

## 4. Hàng 1 — Biểu đồ

`grid grid-cols-2 gap-24 mb-24`

### 4.1 Line Chart — Xu hướng đơn hàng

**Card:** `bg white border #E2E8F0 radius-16 p-24`

**Card header** (`flex justify-between mb-20`):
- Left: Title `"Xu hướng đơn hàng" 15px Inter 600 #1E293B` + Subtitle `"THEO NGÀY/TUẦN/THÁNG" 10px uppercase #94A3B8`
- Right: Tab group "Ngày" | "Tuần" | "Tháng" — same pill style as filter

**Chart area** (`height 240px`):
- SVG line chart
- Y-axis labels: `10px #94A3B8`
- Horizontal grid lines: `1px solid #F1F5F9`
- Line stroke: `#0066CC stroke-width 2.5px stroke-linecap round`
- Area fill: `linear-gradient rgba(0,102,204,0.08) → transparent`
- Data points: `circle r=3.5 fill #0066CC stroke white stroke-width 2`
- Tooltip on hover: `bg white border #E2E8F0 radius-8 p-10 shadow 12px Inter 500 #1E293B`
- X-axis labels: `10px #94A3B8`

**Legend** (`flex gap-16 mt-12 justify-center`):
- `#0066CC dot` + "Tổng đơn" `11px #64748B`

### 4.2 Pie/Donut Chart — Phân bố trạng thái

**Card:** `bg white border #E2E8F0 radius-16 p-24`

**Card header:**
- Title: `"Phân bố trạng thái" 15px Inter 600 #1E293B`

**Chart area** (`height 240px, flex items-center justify-center`):
- Donut chart, inner radius 60%, outer radius 100%
- Segments:
  - Hoàn tất: `#10B981` — 75%
  - Đã xác nhận: `#3B82F6` — 10%
  - Chờ xác nhận: `#F59E0B` — 8%
  - Đã hủy: `#EF4444` — 7%
- Center text: `"1.248" 24px Inter 700 #1E293B` + `"Tổng đơn" 12px #94A3B8`
- Hover segment: opacity 0.8 + tooltip

**Legend** (`grid grid-cols-2 gap-8 mt-16`):
- Mỗi item: `flex items-center gap-8`
  - Dot `10x10px rounded-full` màu segment
  - Label `12px #64748B` + Value `12px Inter 600 #1E293B` + Percent `11px #94A3B8`

---

## 5. Hàng 2 — Bảng chi tiết

**Card:** `bg white border #E2E8F0 radius-16 overflow-hidden`

**Card header** (`flex justify-between px-24 py-20 border-b #E2E8F0`):
- Title: `"Chi tiết đơn hàng" 15px Inter 600 #1E293B`
- Right: `"1.248 đơn hàng" 13px #94A3B8` + Button "Xuất Excel" ghost style

**Table** (API: `GET /admin/reports/bookings` với params filter):

`thead bg #F8FAFC` · `th: px-16 py-12, 11px uppercase #94A3B8`

| Cột | Width |
|-----|-------|
| Mã đơn | 110px |
| Khách hàng | 180px |
| Tour | auto |
| Ngày đặt | 130px |
| Tổng tiền | 120px |
| TT đơn | 120px |
| TT thanh toán | 130px |

`tbody: border-b #F1F5F9 hover bg #F8FAFC`

- Mã đơn: `13px Inter 700 #0066CC` hover underline → `/admin/bookings/{id}`
- Khách hàng: Avatar `24x24px` + Name `13px Inter 500 #1E293B`
- Tour: `13px #1E293B max-1-line ellipsis`
- Ngày đặt: `13px #1E293B` + Time `11px #94A3B8`
- Tổng tiền: `13px Inter 700 #1E293B`
- TT đơn + TT thanh toán: badge pill (same style as admin_bookings_list.md)

**Pagination** (`px-24 py-16 border-t #E2E8F0 bg #F8FAFC flex justify-between`):
- `"Hiển thị 1–10 / 1.248 đơn" 13px #64748B`
- Prev · 1 · 2 · ... · 125 · Next

---

## 6. API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load báo cáo + bảng | GET | `/admin/reports/bookings?from=&to=&status=&payment_status=` | Khi mount, đổi filter |
| Xuất Excel | GET | `/admin/bookings/export?from=&to=&status=&payment_status=` | Click "Xuất Excel" |
