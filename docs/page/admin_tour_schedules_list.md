# Màn hình: Lịch khởi hành

> Route: `/admin/tour-schedules`
> Quyền: 🛡️ Admin / Staff
> Mô tả: Xem toàn bộ lịch khởi hành của tất cả tour — filter theo tour/trạng thái/ngày, đổi trạng thái, xóa.

---

## Layout tổng thể

```
┌─────────────────────────────────────────────────────────────┐
│  HEADER: Breadcrumb + Tiêu đề + [Thêm lịch]                │
├─────────────────────────────────────────────────────────────┤
│  STATS ROW: [Tổng lịch] [Còn chỗ] [Đầy chỗ] [Đã hủy]      │
├─────────────────────────────────────────────────────────────┤
│  FILTER BAR: Search + Tour + Trạng thái + Date range + Lọc  │
│              Active filter tags                             │
├─────────────────────────────────────────────────────────────┤
│  TABLE TOOLBAR: Checkbox + Bulk actions + Per page          │
│  TABLE HEADER: ☐ # | Tour | Ngày KH | Ngày KT | Giá | Đặt/Max | TT | ⚙ │
│  TABLE BODY: rows                                           │
│  PAGINATION                                                 │
└─────────────────────────────────────────────────────────────┘
```

---

## 1. Page Header

`flex justify-between items-start, mb 24px`

| Element | Style |
|---------|-------|
| Breadcrumb | `12px Inter 500 #94A3B8` — "Quản lý Tour / Lịch khởi hành" |
| Title | `24px Inter 700 #1E293B` — "Lịch khởi hành" |
| Subtitle | `14px Inter 400 #64748B` — "Quản lý toàn bộ lịch khởi hành của các tour" |
| Button "Thêm lịch" | `bg #0066CC text white radius-10 px-20 py-10 shadow` icon `add` → mở modal chọn tour → `/admin/tours/{id}/schedules/create` |

---

## 2. Stats Row

`grid grid-cols-4 gap-4 mb-24`
Mỗi thẻ: `bg white border #E2E8F0 radius-12 p-16 flex items-center gap-12`

| Thẻ | Icon | Icon bg | Value | Label | Value color |
|-----|------|---------|-------|-------|-------------|
| Tổng lịch | `calendar_month` | `#EFF6FF` | `24` | "TỔNG LỊCH" | `#1E293B` |
| Còn chỗ | `event_available` | `#D1FAE5` | `18` | "CÒN CHỖ" | `#10B981` |
| Đầy chỗ | `event_busy` | `#FEE2E2` | `4` | "ĐẦY CHỖ" | `#EF4444` |
| Đã hủy | `cancel` | `#F1F5F9` | `2` | "ĐÃ HỦY" | `#94A3B8` |

---

## 3. Filter Bar

**Card:** `bg white border #E2E8F0 radius-16 p-20 mb-24`

### Row 1 (`flex gap-3 flex-wrap`)

| Element | Width | Config |
|---------|-------|--------|
| Search | `flex-1 min-280px` | Placeholder "Tìm theo tên tour..." · icon search · debounce 300ms |
| Select Tour | `220px` | "Tất cả tour" + list tour · pre-selected nếu có `?tour_id` từ URL |
| Select Trạng thái | `160px` | Tất cả / Còn chỗ / Đầy chỗ / Đã hủy |
| Date "Từ ngày" | `150px` | Input date · icon `calendar_today` |
| Date "Đến ngày" | `150px` | Input date |
| Button Lọc | `auto` | `bg #0066CC text white radius-10 px-20 py-10` |
| Button Đặt lại | `auto` | Chỉ hiện khi có filter · hover `text #EF4444 border #EF4444` |

### Row 2 — Active filter tags (khi có filter)
- Tag: `bg #EFF6FF text #0066CC border #B3D9FF radius-full px-10 py-4 12px Inter 500`
- Nút `×` xóa từng filter
- Ví dụ: `Tour: Bà Nà Hills ×` · `Trạng thái: Còn chỗ ×`

> Khi navigate từ trang chi tiết tour với `?tour_id=X`: pre-select tour đó và hiện tag filter

---

## 4. Table

**Card:** `bg white border #E2E8F0 radius-16 overflow-hidden`

### 4.1 Toolbar

`flex justify-between items-center px-24 py-16 border-b #E2E8F0`

**Bên trái:**
- Checkbox "Chọn tất cả"
- Khi có row được chọn: `"Đã chọn 3" 13px 600 #0066CC` + bulk actions:
  - "Kích hoạt": `bg #D1FAE5 text #10B981 radius-8 px-12 py-6 12px 600`
  - "Hủy lịch": `bg #FEE2E2 text #EF4444`

**Bên phải:**
- `"Hiển thị 1–10 / 24 lịch" 13px #94A3B8`
- Select per_page: 10 / 20 / 50

### 4.2 Table Header

`bg #F8FAFC border-b #E2E8F0`
`th: px-16 py-12, 11px Inter 600, uppercase, letter-spacing 0.06em, #94A3B8`

| Cột | Width | Ghi chú |
|-----|-------|---------|
| ☐ | 40px | Checkbox |
| # | 48px | STT |
| Tour | auto | Tên + thumbnail + danh mục |
| Ngày KH | 130px | Sortable ↕ |
| Ngày KT | 130px | |
| Giá riêng | 120px | Override price |
| Đã đặt / Max | 130px | Progress bar |
| Trạng thái | 120px | Badge clickable |
| Thao tác | 100px | |

### 4.3 Table Body

`border-b #F1F5F9 min-h-60px`
- Hover: `bg #F8FAFC transition-150ms`
- Selected: `bg #EFF6FF border-l-3 #0066CC`

#### Chi tiết từng cột

**Col Tour** (`flex items-center gap-12`):
- Thumbnail: `44x44px radius-8 object-cover border #E2E8F0`
- Tên tour: `14px Inter 600 #1E293B` hover `#0066CC` cursor pointer → `/admin/tours/{id}`
- Danh mục tag: `11px 600 bg #EFF6FF text #0066CC border #B3D9FF radius-full px-8 py-2 mt-2`

**Col Ngày KH**:
- Date: `13px Inter 600 #1E293B` — e.g. "15/04/2026"
- Thứ: `11px #94A3B8` — e.g. "Thứ Tư"
- Ngày đã qua: text `#94A3B8` (muted)
- Trong 7 ngày tới: badge "SẮP TỚI" `bg #EFF6FF text #0066CC 10px 600 radius-full px-6 py-1 ml-6`

**Col Ngày KT**: `13px Inter 400 #64748B`

**Col Giá riêng**:
- Có giá: `13px Inter 700 #FF6B35` — e.g. "900.000 đ"
- Không có: `13px #94A3B8 italic` — "Theo tour"

**Col Đã đặt / Max**:
- Text: `"12 / 20" 13px Inter 600 #1E293B`
- Progress bar: `h-4px bg #E2E8F0 radius-full w-80px mt-4`
  - 0–60%: fill `#0066CC`
  - 61–89%: fill `#F59E0B`
  - 90–100%: fill `#EF4444`
- Full: text `#EF4444`

**Col Trạng thái** — badge pill `11px 700 rounded-full px-10 py-4` · click → dropdown inline:

| Status | Background | Text |
|--------|-----------|------|
| available | `#D1FAE5` | `#10B981` "CÒN CHỖ" |
| full | `#FEE2E2` | `#EF4444` "ĐẦY CHỖ" |
| cancelled | `#F1F5F9` | `#94A3B8` "ĐÃ HỦY" |

→ `PATCH /admin/tour-schedules/{id}/status`

**Col Thao tác** (`flex gap-4`):

| Button | Icon | Hover | Action |
|--------|------|-------|--------|
| Xem tour | `visibility` | `#0066CC` | `/admin/tours/{id}` |
| Sửa lịch | `edit` | `#F59E0B` | `/admin/tour-schedules/{id}/edit` |
| Xóa | `delete` | `#EF4444` | Confirm → `DELETE /admin/tour-schedules/{id}` |

Style chung: `28x28px bg #F8FAFC border #E2E8F0 radius-6 color #64748B`

### 4.4 Sample Data

| # | Tour | Ngày KH | Ngày KT | Giá | Đặt/Max | Status |
|---|------|---------|---------|-----|---------|--------|
| 1 | Bà Nà Hills - Cầu Vàng | 15/04/2026 Thứ Tư | 15/04/2026 | Theo tour | 12/20 | CÒN CHỖ |
| 2 | Bà Nà Hills - Cầu Vàng | 22/04/2026 Thứ Ba | 22/04/2026 | 900.000đ | 20/20 | ĐẦY CHỖ |
| 3 | Hội An - Show Ký ức | 18/04/2026 Thứ Sáu | 18/04/2026 | Theo tour | 8/15 | CÒN CHỖ |
| 4 | Cù Lao Chàm | 20/04/2026 CN | 20/04/2026 | 1.300.000đ | 0/12 | CÒN CHỖ |
| 5 | Ngũ Hành Sơn | 10/03/2026 Thứ Hai | 10/03/2026 | Theo tour | 10/10 | ĐÃ HỦY |

---

## 5. Pagination

`flex justify-between items-center px-24 py-16 border-t #E2E8F0 bg #F8FAFC radius-b-16`

- Trái: `"Hiển thị 1–10 trong tổng số 24 lịch" 13px #64748B`
- Phải: Prev · 1 · 2 · 3 · Next
  - Button: `32x32px border #E2E8F0 radius-8 bg white color #64748B`
  - Active: `bg #0066CC text white border #0066CC`

---

## 6. Confirm Delete Dialog

**Modal:** `bg white radius-16 w-400px shadow-modal backdrop rgba(0,0,0,0.4)`

| Vùng | Nội dung |
|------|---------|
| Header | Icon `warning_amber 40x40 bg #FEE2E2 radius-10 color #EF4444` + "Xóa lịch khởi hành này?" `16px 700 #1E293B` |
| Body | "Lịch [ngày] của tour [tên] sẽ bị xóa vĩnh viễn." `14px #64748B` + Warning box `bg #FEF3C7`: "⚠ Nếu đã có đơn đặt cho lịch này, hãy hủy các đơn trước khi xóa." |
| Footer | "Hủy" (ghost) + "Xóa lịch" `bg #EF4444 hover #DC2626` |

---

## 7. Empty State

`center py-64`:
- SVG icon `calendar_month 80x80px color #E2E8F0`
- Title: `"Không có lịch khởi hành nào" 16px Inter 600 #1E293B`
- Subtitle: `"Thử thay đổi bộ lọc hoặc thêm lịch mới" 14px #94A3B8`
- Button "Thêm lịch": `bg #0066CC text white radius-10 px-20 py-10`

---

## 8. API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load danh sách | GET | `/admin/tour-schedules?page=&per_page=&sort=&order=` | Khi mount, đổi filter, đổi trang |
| Filter theo tour | GET | `/admin/tour-schedules?tour_id=` | Chọn select Tour |
| Filter theo status | GET | `/admin/tour-schedules?status=` | Chọn select Trạng thái |
| Filter theo ngày | GET | `/admin/tour-schedules?from=&to=` | Chọn date range |
| Tìm kiếm | GET | `/admin/tour-schedules?q=` | Nhập search (debounce 300ms) |
| Đổi trạng thái | PATCH | `/admin/tour-schedules/{id}/status` | Click badge → chọn trạng thái |
| Bulk hủy | PATCH | `/admin/tour-schedules/{id}/status` (loop) | Bulk action "Hủy lịch" |
| Xóa lịch | DELETE | `/admin/tour-schedules/{id}` | Confirm dialog |
