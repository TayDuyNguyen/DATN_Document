# Màn hình: Báo cáo Đánh giá

> Route: `/admin/reports/ratings`
> Quyền: 🛡️ Admin / Staff
> Mô tả: Báo cáo thống kê đánh giá theo thời gian — xu hướng, phân bố số sao, trạng thái duyệt, bảng chi tiết và xuất Excel.

---

## Layout tổng thể

```
┌─────────────────────────────────────────────────────────────────┐
│  HEADER: Breadcrumb + Tiêu đề + [Xuất Excel]                    │
├─────────────────────────────────────────────────────────────────┤
│  FILTER BAR: Date range + Quick range + Trạng thái + Loại       │
├─────────────────────────────────────────────────────────────────┤
│  STATS ROW: [Tổng ĐG] [Chờ duyệt] [Đã duyệt] [Điểm TB]        │
├─────────────────────────────────────────────────────────────────┤
│  HÀNG 1: [Line chart xu hướng] [Bar chart phân bố số sao]       │
├─────────────────────────────────────────────────────────────────┤
│  HÀNG 2: [Donut chart trạng thái] [Bar chart loại ĐG]           │
├─────────────────────────────────────────────────────────────────┤
│  HÀNG 3: Bảng chi tiết đánh giá (paginate)                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1. Page Header

| Element | Style |
|---------|-------|
| Breadcrumb | `12px Inter 500 #94A3B8` — "Báo cáo / Báo cáo Đánh giá" |
| Title | `24px Inter 700 #1E293B` — "Báo cáo Đánh giá" |
| Subtitle | `14px Inter 400 #64748B` — "Thống kê và phân tích đánh giá của khách hàng" |
| Button "Xuất Excel" | `border #E2E8F0 bg white text #64748B radius-10 px-16 py-10` icon `download` | `GET /admin/ratings/export` với params hiện tại |

---

## 2. Filter Bar

**Card:** `bg white border #E2E8F0 radius-16 p-20 mb-24`

`flex gap-12 flex-wrap items-end`

| Element | Width | Config |
|---------|-------|--------|
| Date "Từ ngày" | `150px` | Input date · default: đầu tháng hiện tại |
| Date "Đến ngày" | `150px` | Input date · default: hôm nay |
| Quick range | `auto` | Pill buttons: "7 ngày" \| "30 ngày" \| "3 tháng" \| "Năm nay" |
| Select Trạng thái | `160px` | Tất cả / Chờ duyệt (pending) / Đã duyệt (approved) / Từ chối (rejected) |
| Select Loại | `150px` | Tất cả / Địa điểm (location) / Tour (tour) |
| Button "Áp dụng" | `auto` | `bg #0066CC text white radius-10 px-20 py-10` |

---

## 3. Stats Row

`grid grid-cols-4 gap-4 mb-24`

| Thẻ | Icon | Icon bg | Value | Label | Value color |
|-----|------|---------|-------|-------|-------------|
| Tổng đánh giá | `rate_review` | `#EFF6FF` | `1.024` | "TỔNG ĐÁNH GIÁ" | `#1E293B` |
| Chờ duyệt | `pending` | `#FEF3C7` | `18` | "CHỜ DUYỆT" | `#F59E0B` |
| Đã duyệt | `check_circle` | `#D1FAE5` | `986` | "ĐÃ DUYỆT" | `#10B981` |
| Điểm trung bình | `star` | `#FEF3C7` | `4.7 ★` | "ĐIỂM TRUNG BÌNH" | `#F59E0B` |

Mỗi thẻ có trend badge:
- Tăng: `bg #D1FAE5 text #10B981 11px 600 radius-full px-8 py-2` "↑ +8.3%"
- Giảm: `bg #FEE2E2 text #EF4444` "↓ -1.2%"

---

## 4. Hàng 1 — Biểu đồ chính

`grid grid-cols-2 gap-24 mb-24`

### 4.1 Line Chart — Xu hướng đánh giá

**Card:** `bg white border #E2E8F0 radius-16 p-24`

**Card header** (`flex justify-between mb-20`):
- Left:
  - Title: `"Xu hướng đánh giá" 15px Inter 600 #1E293B`
  - Subtitle: `"THEO NGÀY/TUẦN/THÁNG" 10px uppercase #94A3B8`
- Right: Period tabs "Ngày" | "Tuần" | "Tháng"

**Chart area** (`height 240px`):
- SVG line chart với 2 lines:
  - Line 1 — Tổng đánh giá: stroke `#0066CC stroke-width 2.5px`
    area fill `rgba(0,102,204,0.06)`
  - Line 2 — Đã duyệt: stroke `#10B981 stroke-width 2px stroke-dasharray 4,2`
- Y-axis labels: `10px #94A3B8`
- Grid lines: `1px solid #F1F5F9`
- Tooltip: date + tổng + đã duyệt

**Legend** (`flex gap-16 mt-12 justify-center`):
- `#0066CC dot` + "Tổng đánh giá" `11px #64748B`
- `#10B981 dot dashed` + "Đã duyệt" `11px #64748B`

### 4.2 Bar Chart — Phân bố số sao

**Card:** `bg white border #E2E8F0 radius-16 p-24`

**Card header:**
- Title: `"Phân bố số sao" 15px Inter 600 #1E293B`
- Right: `"Điểm TB: 4.7 ★" 14px Inter 700 #F59E0B`

**Horizontal bar chart** (`height 240px`):
- 5 rows (5★ → 1★):
  - Label: `"5 ★" 13px Inter 600 #1E293B w-32px`
  - Bar: `height 24px radius-r-6px`
    - 5★: fill `#10B981`
    - 4★: fill `#3B82F6`
    - 3★: fill `#F59E0B`
    - 2★: fill `#FF6B35`
    - 1★: fill `#EF4444`
  - Count: `12px Inter 600 #1E293B ml-8` — e.g. "512"
  - Percent: `11px #94A3B8` — e.g. "(50%)"
- Background track: `h-24px bg #F1F5F9 radius-6px`

---

## 5. Hàng 2 — Biểu đồ phụ

`grid grid-cols-2 gap-24 mb-24`

### 5.1 Donut Chart — Phân bố trạng thái duyệt

**Card:** `bg white border #E2E8F0 radius-16 p-24`

**Card header:**
- Title: `"Trạng thái duyệt" 15px Inter 600 #1E293B`

**Donut chart** (`height 200px`):
- Segments:
  - Đã duyệt: `#10B981` — 96.3%
  - Chờ duyệt: `#F59E0B` — 1.8%
  - Từ chối: `#EF4444` — 1.9%
- Center: `"1.024" 20px Inter 700 #1E293B` + `"Tổng ĐG" 11px #94A3B8`

**Legend** (`grid grid-cols-1 gap-8 mt-16`):
- Mỗi item: `flex justify-between items-center`
  - Left: dot + label `12px #64748B`
  - Right: count `12px Inter 700 #1E293B` + percent `11px #94A3B8`

### 5.2 Bar Chart — Đánh giá theo loại

**Card:** `bg white border #E2E8F0 radius-16 p-24`

**Card header:**
- Title: `"Theo loại địa điểm/tour" 15px Inter 600 #1E293B`

**Grouped bar chart** (`height 200px`):
- 2 nhóm: Địa điểm · Tour
- Mỗi nhóm có 2 bars:
  - Tổng: `#0066CC`
  - Đã duyệt: `#10B981`
- Bar width: `40px radius-t-6px`
- X-axis: "Địa điểm" | "Tour" `11px #94A3B8`
- Value label above: `11px Inter 700` màu tương ứng

**Summary** (`mt-16 grid grid-cols-2 gap-8`):
- Địa điểm: `"624 đánh giá · TB 4.8 ★" 12px #64748B`
- Tour: `"400 đánh giá · TB 4.6 ★" 12px #64748B`

---

## 6. Hàng 3 — Bảng chi tiết đánh giá

**Card:** `bg white border #E2E8F0 radius-16 overflow-hidden`

**Card header** (`flex justify-between px-24 py-20 border-b #E2E8F0`):
- Title: `"Chi tiết đánh giá" 15px Inter 600 #1E293B`
- Right: `"1.024 đánh giá" 13px #94A3B8` + Button "Xuất Excel" ghost

**Table** (API: `GET /admin/reports/ratings?from=&to=&status=`):

`thead bg #F8FAFC` · `th: px-16 py-12, 11px uppercase #94A3B8`

| Cột | Width |
|-----|-------|
| Người dùng | 180px |
| Địa điểm / Tour | auto |
| Loại | 100px |
| Số sao | 100px |
| Trạng thái | 120px |
| Ngày tạo | 130px |

`tbody: border-b #F1F5F9 hover bg #F8FAFC`

- Người dùng: Avatar `24x24px` + Name `13px Inter 500 #1E293B`
- Địa điểm/Tour: `13px #1E293B max-1-line ellipsis` + link `#0066CC` hover underline
- Loại: badge `11px 600 rounded-full px-8 py-3`
  - location: `bg #EEF2FF text #6366F1` "ĐỊA ĐIỂM"
  - tour: `bg #EFF6FF text #0066CC` "TOUR"
- Số sao: `flex items-center gap-4`
  - Stars: filled `#F59E0B` / empty `#E2E8F0` · size `14px`
  - Score: `13px Inter 700 #1E293B`
- Trạng thái: badge (approved/pending/rejected)
- Ngày tạo: Date `13px #1E293B` + Time `11px #94A3B8`

**Pagination** (`px-24 py-16 border-t #E2E8F0 bg #F8FAFC flex justify-between`):
- `"Hiển thị 1–10 / 1.024 đánh giá" 13px #64748B`
- Prev · 1 · 2 · ... · 103 · Next

---

## 7. API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load báo cáo + bảng | GET | `/admin/reports/ratings?from=&to=&status=` | Khi mount, đổi filter |
| Xuất Excel | GET | `/admin/ratings/export?status=&date_from=&date_to=` | Click "Xuất Excel" |
