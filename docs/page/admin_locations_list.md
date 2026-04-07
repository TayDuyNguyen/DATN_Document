# Màn hình: Danh sách Địa điểm

> Route: `/admin/locations`
> Quyền: 🛡️ Admin / Staff
> Mô tả: Quản lý toàn bộ địa điểm du lịch — filter, sort, đổi trạng thái, bật/tắt nổi bật, xóa, xuất Excel. Hỗ trợ cả chế độ xem List và Grid.

---

## Layout tổng thể

```
┌─────────────────────────────────────────────────────────────────┐
│  HEADER: Breadcrumb + Tiêu đề + [Xuất Excel] [Thêm Địa điểm]   │
├─────────────────────────────────────────────────────────────────┤
│  STATS ROW: [Tổng ĐĐ] [Đang HĐ] [Nổi bật] [Lượt xem]          │
├─────────────────────────────────────────────────────────────────┤
│  FILTER BAR: Search + Danh mục + Quận + Mức giá + Trạng thái   │
│              Active filter tags                                 │
├─────────────────────────────────────────────────────────────────┤
│  TABLE TOOLBAR: Checkbox + Bulk actions + View toggle + Per page│
│  TABLE HEADER: ☐ # | Địa điểm | Quận | Giá | 👁 | ❤ | ★ | TT | ⭐ | ⚙ │
│  TABLE BODY: rows                                               │
│  PAGINATION                                                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1. Page Header

`flex justify-between items-start, mb 24px`

| Element | Style |
|---------|-------|
| Breadcrumb | `12px Inter 500 #94A3B8` — "Quản lý Địa điểm / Danh sách Địa điểm" |
| Title | `24px Inter 700 #1E293B` — "Danh sách Địa điểm" |
| Subtitle | `14px Inter 400 #64748B` — "Quản lý toàn bộ địa điểm du lịch tại Đà Nẵng" |

**Buttons bên phải** (`flex gap-3`):

| Button | Style | Action |
|--------|-------|--------|
| Xuất Excel | `border #E2E8F0 bg white text #64748B radius-10 px-16 py-10` icon `download` hover `border #0066CC text #0066CC` | `GET /admin/locations/export` |
| Thêm Địa điểm | `bg #0066CC text white radius-10 px-20 py-10 shadow` icon `add` hover `bg #004999` | Navigate `/admin/locations/create` |

---

## 2. Stats Row

`grid grid-cols-4 gap-4 mb-24`
Mỗi thẻ: `bg white border #E2E8F0 radius-12 p-16 flex items-center gap-12`

| Thẻ | Icon | Icon bg | Value | Label | Value color |
|-----|------|---------|-------|-------|-------------|
| Tổng địa điểm | `location_on` | `#EFF6FF` | `124` | "TỔNG ĐỊA ĐIỂM" | `#1E293B` |
| Đang hoạt động | `check_circle` | `#D1FAE5` | `98` | "ĐANG HOẠT ĐỘNG" | `#10B981` |
| Nổi bật | `star` | `#FEF3C7` | `24` | "NỔI BẬT" | `#F59E0B` |
| Tổng lượt xem | `visibility` | `#EEF2FF` | `48.2K` | "LƯỢT XEM" | `#6366F1` |

---

## 3. Filter Bar

**Card:** `bg white border #E2E8F0 radius-16 p-20 mb-24`

### Row 1 (`flex gap-3 flex-wrap`)

| Element | Width | Config |
|---------|-------|--------|
| Search | `flex-1 min-280px` | Placeholder "Tìm theo tên địa điểm, địa chỉ..." · icon `search` · debounce 300ms |
| Select Danh mục | `180px` | "Tất cả danh mục" + list từ `GET /categories` |
| Select Quận | `180px` | Tất cả / Hải Châu / Sơn Trà / Ngũ Hành Sơn / Cẩm Lệ / Thanh Khê / Liên Chiểu |
| Select Mức giá | `150px` | Tất cả / Miễn phí / Bình dân ($) / Trung bình ($$) / Cao cấp ($$$) |
| Select Trạng thái | `150px` | Tất cả / Đang hoạt động / Tạm dừng |
| Button Lọc | `auto` | `bg #0066CC text white radius-10 px-20 py-10` |
| Button Đặt lại | `auto` | Chỉ hiện khi có filter · hover `text #EF4444 border #EF4444` |

### Row 2 — Active filter tags (khi có filter)
- Tag: `bg #EFF6FF text #0066CC border #B3D9FF radius-full px-10 py-4 12px Inter 500`
- Nút `×` xóa từng filter
- Ví dụ: `Danh mục: Bãi biển ×` · `Quận: Sơn Trà ×`

---

## 4. Table

**Card:** `bg white border #E2E8F0 radius-16 overflow-hidden`

### 4.1 Toolbar

`flex justify-between items-center px-24 py-16 border-b #E2E8F0`

**Bên trái:**
- Checkbox "Chọn tất cả"
- Khi có row được chọn: `"Đã chọn 3" 13px 600 #0066CC` + bulk actions:
  - "Kích hoạt": `bg #D1FAE5 text #10B981 radius-8 px-12 py-6 12px 600`
  - "Tạm dừng": `bg #FEF3C7 text #F59E0B`
  - "Xóa": `bg #FEE2E2 text #EF4444`

**Bên phải** (`flex items-center gap-8`):
- View toggle (List | Grid):
  - Active: `bg #EFF6FF border #B3D9FF color #0066CC 32x32px radius-8`
  - Inactive: `bg white border #E2E8F0 color #94A3B8`
  - Icons: `view_list` | `grid_view`
- `"Hiển thị 1–10 / 124 địa điểm" 13px #94A3B8`
- Select per_page: 10 / 20 / 50

### 4.2 Table Header

`bg #F8FAFC border-b #E2E8F0`
`th: px-16 py-12, 11px Inter 600, uppercase, letter-spacing 0.06em, #94A3B8`

| Cột | Width | Ghi chú |
|-----|-------|---------|
| ☐ | 40px | Checkbox |
| # | 48px | STT |
| Địa điểm | auto | Tên + thumbnail + địa chỉ + danh mục |
| Quận | 120px | |
| Mức giá | 100px | |
| Lượt xem | 100px | Sortable ↕ |
| Yêu thích | 100px | Sortable ↕ |
| Đánh giá | 100px | |
| Trạng thái | 120px | Badge clickable |
| Nổi bật | 80px | Toggle |
| Thao tác | 100px | |

### 4.3 Table Body

`border-b #F1F5F9 min-h-64px`
- Hover: `bg #F8FAFC transition-150ms`
- Selected: `bg #EFF6FF border-l-3 #0066CC`

#### Chi tiết từng cột

**Col Địa điểm** (`flex items-center gap-12`):
- Thumbnail: `56x56px radius-10 object-cover border #E2E8F0`
- Right:
  - Tên: `14px Inter 600 #1E293B` hover `#0066CC` cursor pointer · 1 line ellipsis
  - Địa chỉ: `11px Inter 400 #94A3B8` · icon `location_on 12px` trái · 1 line ellipsis · `mt-2`
  - Danh mục tag: `11px 600 bg #EFF6FF text #0066CC border #B3D9FF radius-full px-8 py-2 mt-4`

**Col Quận**:
- Badge: `11px Inter 600 bg #F1F5F9 text #64748B radius-full px-8 py-3`

**Col Mức giá**:
| Value | Text | Color |
|-------|------|-------|
| free | "Miễn phí" | `#10B981` |
| budget | "$" | `#64748B` |
| mid | "$$" | `#F59E0B` |
| luxury | "$$$" | `#FF6B35` |

`13px Inter 600`

**Col Lượt xem**:
- icon `visibility 14px #94A3B8` + value `13px Inter 600 #1E293B` — e.g. "1.2K"

**Col Yêu thích**:
- icon `favorite 14px #EF4444` + value `13px Inter 600 #1E293B` — e.g. "248"

**Col Đánh giá**:
- `"★ 4.7" 13px Inter 600 #1E293B` · star `#F59E0B`
- `"(96)" 11px #94A3B8`

**Col Trạng thái** — badge pill `11px 700 rounded-full px-10 py-4` · click → dropdown:

| Status | Background | Text |
|--------|-----------|------|
| active | `#D1FAE5` | `#10B981` "ĐANG HOẠT ĐỘNG" |
| inactive | `#FEE2E2` | `#EF4444` "TẠM DỪNG" |

→ `PATCH /admin/locations/{id}/status`

**Col Nổi bật**:
- Toggle: ON `#0066CC`, OFF `#E2E8F0`, `36x20px` · thumb `16px white`
- Tooltip: "Bật/tắt nổi bật"
- → `PATCH /admin/locations/{id}/featured`

**Col Thao tác** (`flex gap-4`):

| Button | Icon | Hover | Action |
|--------|------|-------|--------|
| Xem | `visibility` | `#0066CC` | `/admin/locations/{id}` |
| Sửa | `edit` | `#F59E0B` | `/admin/locations/{id}/edit` |
| Xóa | `delete` | `#EF4444` | Confirm → `DELETE /admin/locations/{id}` |

Style chung: `28x28px bg #F8FAFC border #E2E8F0 radius-6 color #64748B`

### 4.4 Sample Data

| # | Địa điểm | Quận | Giá | 👁 | ❤ | ★ | Status | Nổi bật |
|---|----------|------|-----|---|---|---|--------|---------|
| 1 | Bãi biển Mỹ Khê | Sơn Trà | Miễn phí | 12.4K | 1.2K | 4.8 | ĐANG HĐ | ON |
| 2 | Cầu Rồng | Hải Châu | Miễn phí | 8.6K | 856 | 4.7 | ĐANG HĐ | ON |
| 3 | Bà Nà Hills | Hòa Vang | $$$ | 6.2K | 624 | 4.9 | ĐANG HĐ | ON |
| 4 | Ngũ Hành Sơn | Ngũ Hành Sơn | $ | 3.8K | 312 | 4.6 | ĐANG HĐ | OFF |
| 5 | Chùa Linh Ứng | Sơn Trà | Miễn phí | 2.1K | 198 | 4.5 | TẠM DỪNG | OFF |

---

## 5. Grid View (khi chọn chế độ Grid)

`grid grid-cols-3 gap-4 p-16` (thay thế table)

Mỗi card:
- Thumbnail: `full-width h-160px object-cover radius-t-12`
- Body: `p-14`
  - Tên: `14px Inter 600 #1E293B`
  - Địa chỉ: `12px #94A3B8` icon `location_on`
  - `flex justify-between mt-8`: Badge danh mục + Badge trạng thái
  - `flex justify-between mt-8`:
    - `"★ 4.7 · 1.2K views" 12px #64748B`
    - Toggle nổi bật + action buttons (xem/sửa/xóa)

---

## 6. Pagination

`flex justify-between items-center px-24 py-16 border-t #E2E8F0 bg #F8FAFC radius-b-16`

- Trái: `"Hiển thị 1–10 trong tổng số 124 địa điểm" 13px #64748B`
- Phải: Prev · 1 · 2 · ... · 13 · Next
  - Button: `32x32px border #E2E8F0 radius-8 bg white color #64748B`
  - Active: `bg #0066CC text white border #0066CC`

---

## 7. Confirm Delete Dialog

**Modal:** `bg white radius-16 w-400px shadow-modal backdrop rgba(0,0,0,0.4)`

| Vùng | Nội dung |
|------|---------|
| Header | Icon `warning_amber 40x40 bg #FEE2E2 radius-10 color #EF4444` + "Xóa địa điểm này?" `16px 700 #1E293B` |
| Body | "Địa điểm [Tên] sẽ bị xóa vĩnh viễn." `14px #64748B` + Warning `bg #FEF3C7 13px #92400E`: "⚠ Tất cả đánh giá, lượt yêu thích và dữ liệu liên quan sẽ bị xóa theo." |
| Footer | "Hủy" (ghost) + "Xóa địa điểm" `bg #EF4444 hover #DC2626` |

---

## 8. Empty State

`center py-64`:
- SVG icon `location_off 80x80px color #E2E8F0`
- Title: `"Không tìm thấy địa điểm nào" 16px Inter 600 #1E293B`
- Subtitle: `"Thử thay đổi bộ lọc hoặc thêm địa điểm mới" 14px #94A3B8`
- Button "Thêm Địa điểm": `bg #0066CC text white radius-10 px-20 py-10`

---

## 9. API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load danh sách | GET | `/locations?page=&per_page=&sort=&order=` | Khi mount, đổi filter, đổi trang |
| Tìm kiếm | GET | `/locations?q=` | Nhập search (debounce 300ms) |
| Filter danh mục | GET | `/locations?category_id=` | Chọn select danh mục |
| Filter quận | GET | `/locations?district=` | Chọn select quận |
| Filter mức giá | GET | `/locations?price_level=` | Chọn select mức giá |
| Filter trạng thái | GET | `/locations?status=` | Chọn select trạng thái |
| Load danh mục (select) | GET | `/categories` | Khi mount |
| Đổi trạng thái | PATCH | `/admin/locations/{id}/status` | Click badge → chọn trạng thái |
| Bật/tắt nổi bật | PATCH | `/admin/locations/{id}/featured` | Toggle switch |
| Xóa 1 địa điểm | DELETE | `/admin/locations/{id}` | Confirm dialog |
| Bulk kích hoạt | PATCH | `/admin/locations/{id}/status` (loop) | Bulk action |
| Bulk tạm dừng | PATCH | `/admin/locations/{id}/status` (loop) | Bulk action |
| Bulk xóa | DELETE | `/admin/locations/{id}` (loop) | Bulk action |
| Xuất Excel | GET | `/admin/locations/export?category_id=&district=&status=` | Click "Xuất Excel" |
