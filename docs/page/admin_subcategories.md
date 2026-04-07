# Màn hình: Danh mục con

> Route: `/admin/subcategories` (Tab 2 trong `/admin/categories`)
> Quyền: 🛡️ Admin / Staff
> Mô tả: Quản lý danh mục con của địa điểm — tab thứ 2 trong trang Danh mục Địa điểm. Hiển thị danh sách, tạo mới, chỉnh sửa, đổi trạng thái, xóa. Form inline bên phải.

---

## Layout tổng thể

```
┌─────────────────────────────────────────────────────────────┐
│  HEADER: (dùng chung với trang /admin/categories)           │
├─────────────────────────────────────────────────────────────┤
│  TAB BAR: [Danh mục] [Danh mục con ← active]               │
├─────────────────────────────────────────────────────────────┤
│  STATS ROW: [Tổng DM con] [Đang HĐ] [Tổng ĐĐ]             │
├──────────────────────────────────┬──────────────────────────┤
│  CỘT TRÁI (flex-1)               │  CỘT PHẢI (400px)        │
│                                  │  sticky top-24           │
│  Toolbar: Search + DM cha + TT   │  Form tạo / chỉnh sửa    │
│  Table: danh sách danh mục con   │  - DM cha, Tên, Slug     │
│  Footer: ghi chú drag & drop     │  - Mô tả, Thứ tự, TT    │
│                                  │  - Preview box           │
└──────────────────────────────────┴──────────────────────────┘
```

---

## 1. Tab Bar

`flex gap-0 bg white border #E2E8F0 radius-12 p-4 inline-flex mb-24`

| Tab | Style |
|-----|-------|
| Danh mục | Inactive: `bg transparent text #64748B px-16 py-8 13px 500` hover `text #0066CC` |
| Danh mục con | Active: `bg #0066CC text white radius-8 px-16 py-8 13px 600` |

---

## 2. Stats Row

`grid grid-cols-3 gap-4 mb-24`
Mỗi thẻ: `bg white border #E2E8F0 radius-12 p-16 flex items-center gap-12`

| Thẻ | Icon | Icon bg | Value | Label | Value color |
|-----|------|---------|-------|-------|-------------|
| Tổng danh mục con | `account_tree` | `#EFF6FF` | `24` | "TỔNG DANH MỤC CON" | `#1E293B` |
| Đang hoạt động | `check_circle` | `#D1FAE5` | `18` | "ĐANG HOẠT ĐỘNG" | `#10B981` |
| Tổng địa điểm | `location_on` | `#EEF2FF` | `124` | "TỔNG ĐỊA ĐIỂM" | `#6366F1` |

---

## 3. Cột trái — Danh sách

**Card:** `bg white border #E2E8F0 radius-16 overflow-hidden`

### 3.1 Toolbar

`flex justify-between items-center px-24 py-16 border-b #E2E8F0`

**Bên trái:**
- Search `width 220px`: icon `search` trái · placeholder "Tìm danh mục con..." · `border #E2E8F0 radius-8 px-10 py-8 pl-36 13px` · focus `border #0066CC`
- Select "Danh mục cha" `width 200px ml-8`: "Tất cả" + list từ `GET /categories`
- Select "Trạng thái" `width 140px ml-8`: Tất cả / Đang hoạt động / Tạm dừng

**Bên phải:** `"24 danh mục con" 13px #94A3B8`

### 3.2 Table Header

`bg #F8FAFC border-b #E2E8F0`
`th: px-16 py-12, 11px Inter 600, uppercase, letter-spacing 0.06em, #94A3B8`

| Cột | Width | Ghi chú |
|-----|-------|---------|
| # | 48px | Drag handle `drag_indicator` |
| Danh mục con | auto | Tên + icon + slug + mô tả |
| Thuộc danh mục | 160px | Badge danh mục cha |
| Số địa điểm | 110px | Count + mini bar |
| Thứ tự | 80px | Input inline |
| Trạng thái | 120px | Badge clickable |
| Thao tác | 100px | Sửa + Xóa |

### 3.3 Table Body

`border-b #F1F5F9 min-h-56px`
- Hover: `bg #F8FAFC transition-150ms`
- Row đang sửa: `bg #EFF6FF border-l-3 #0066CC`

#### Chi tiết từng cột

**Col # (Drag):** `13px Inter 500 #94A3B8` · icon `drag_indicator color #E2E8F0` hover `#94A3B8` cursor `grab`

**Col Danh mục con** (`flex items-center gap-12`):
- Icon container: `36x36px radius-8` bg màu danh mục cha (10% opacity) · icon/emoji `18px`
- Right:
  - Tên: `14px Inter 600 #1E293B`
  - Slug: `11px Inter 500 #94A3B8`
  - Mô tả: `12px #94A3B8 max-1-line ellipsis mt-2`

**Col Thuộc danh mục:**
- Badge: bg màu DM cha (10% opacity) · text màu DM cha · border màu DM cha (20% opacity)
- `radius-full px-10 py-4 11px Inter 600`
- e.g. `bg #EFF6FF text #0066CC border #B3D9FF` "🏖️ Bãi biển & Biển"

**Col Số địa điểm:**
- Value: `13px Inter 600 #1E293B`
- Mini bar: `h-3px bg #E2E8F0 radius-full w-48px mt-4` · fill `#0066CC` proportional

**Col Thứ tự:**
- Input number: `w-48px border #E2E8F0 radius-6 text-center 13px Inter 600 #1E293B py-4`
- Blur → auto save → `PUT /admin/subcategories/{id}`

**Col Trạng thái** — badge pill `11px 700 rounded-full px-10 py-4` · click → toggle:

| Status | Background | Text |
|--------|-----------|------|
| active | `#D1FAE5` | `#10B981` "ĐANG HOẠT ĐỘNG" |
| inactive | `#FEE2E2` | `#EF4444` "TẠM DỪNG" |

→ `PATCH /admin/subcategories/{id}/status`

**Col Thao tác** (`flex gap-4`):
- Sửa: `28x28px bg #F8FAFC border #E2E8F0 radius-6 color #64748B` hover `border #F59E0B color #F59E0B` → load data vào form phải
- Xóa: hover `border #EF4444 color #EF4444` → confirm → `DELETE /admin/subcategories/{id}`

### 3.4 Sample Data

| # | Tên | DM cha | Địa điểm | Thứ tự | Status |
|---|-----|--------|----------|--------|--------|
| 1 | Bãi biển Đà Nẵng | 🏖️ Bãi biển & Biển | 8 | 1 | ĐANG HOẠT ĐỘNG |
| 2 | Bãi biển Hội An | 🏖️ Bãi biển & Biển | 4 | 2 | ĐANG HOẠT ĐỘNG |
| 3 | Đền chùa | 🏛️ Di tích lịch sử | 6 | 1 | ĐANG HOẠT ĐỘNG |
| 4 | Bảo tàng | 🏛️ Di tích lịch sử | 3 | 2 | ĐANG HOẠT ĐỘNG |
| 5 | Quán ăn đường phố | 🍜 Ẩm thực | 12 | 1 | ĐANG HOẠT ĐỘNG |
| 6 | Nhà hàng hải sản | 🍜 Ẩm thực | 7 | 2 | TẠM DỪNG |

### 3.5 Card Footer

`px-24 py-12 border-t #E2E8F0 bg #F8FAFC radius-b-16`
- icon `drag_indicator #94A3B8` + `"Kéo thả để sắp xếp thứ tự" 12px #94A3B8`

---

## 4. Cột phải — Form tạo / chỉnh sửa

**Card:** `bg white border #E2E8F0 radius-16 p-24 sticky top-24`

### 4.1 Card Header

`flex justify-between items-center mb-20 pb-16 border-b #F1F5F9`

| Mode | Title | Badge |
|------|-------|-------|
| Tạo mới | "Thêm danh mục con" | `bg #D1FAE5 text #10B981` "MỚI" |
| Chỉnh sửa | "Chỉnh sửa danh mục con" | `bg #EFF6FF text #0066CC` "ĐANG SỬA" |

- Button `×`: `24x24px icon close color #94A3B8` hover `#1E293B` → reset form

### 4.2 Form Fields

`space-y-16`

| Field | Type | Bắt buộc | Config |
|-------|------|----------|--------|
| Danh mục cha | select | ✅ | Options từ `GET /categories` (chỉ active) · Khi sửa: disabled + badge DM cha hiện tại |
| Tên danh mục con | text | ✅ | placeholder "Ví dụ: Bãi biển Đà Nẵng" |
| Slug | text | — | placeholder "bai-bien-da-nang" · badge "Tự động" `bg #EFF6FF text #0066CC 11px` |
| Mô tả | textarea rows-3 | — | placeholder "Mô tả ngắn..." · resize-none |
| Thứ tự hiển thị | number | — | placeholder "1" · helper "Số nhỏ hơn hiển thị trước" |
| Trạng thái | toggle | — | ON `#0066CC`, OFF `#E2E8F0`, `40x22px` |

### 4.3 Preview Box

`mt-16 bg #F8FAFC border #E2E8F0 radius-12 p-16`

- Label: `"XEM TRƯỚC" 10px uppercase #94A3B8 mb-10`
- Preview item: `flex items-center gap-12`
  - Icon container: `40x40px radius-10` bg màu DM cha (10% opacity) · icon/emoji DM cha `20px`
  - Right:
    - Badge DM cha: `11px 600 radius-full px-8 py-2`
    - Tên: `14px Inter 600 #1E293B` (live update)
    - Slug: `12px #94A3B8` (live update)

### 4.4 Form Footer

`flex gap-8 mt-20 pt-16 border-t #F1F5F9`

| Button | Style | Action |
|--------|-------|--------|
| Hủy | `border #E2E8F0 bg white text #64748B radius-10 py-10 flex-1` hover `border #EF4444 text #EF4444` | Reset form |
| Lưu / Tạo | `bg #0066CC text white radius-10 py-10 flex-1 14px 600` hover `bg #004999` | POST (tạo) hoặc PUT (sửa) |

---

## 5. Confirm Delete Dialog

**Modal:** `bg white radius-16 w-400px shadow-modal backdrop rgba(0,0,0,0.4)`

| Vùng | Nội dung |
|------|---------|
| Header | Icon `warning_amber 40x40 bg #FEE2E2 radius-10 color #EF4444` + "Xóa danh mục con này?" `16px 700 #1E293B` |
| Body | "Danh mục con [Tên] sẽ bị xóa vĩnh viễn." `14px #64748B` + Warning `bg #FEF3C7 13px #92400E`: "⚠ Kiểm tra xem có địa điểm nào đang thuộc danh mục con này không. Nếu có, các địa điểm sẽ mất liên kết danh mục con." |
| Footer | "Hủy" (ghost) + "Xóa" `bg #EF4444 hover #DC2626` |

---

## 6. Empty State

`center py-64`:
- SVG icon `account_tree 80x80px color #E2E8F0`
- Title: `"Chưa có danh mục con nào" 16px Inter 600 #1E293B`
- Subtitle: `"Tạo danh mục con đầu tiên để phân loại địa điểm" 14px #94A3B8`
- Button "Thêm danh mục con": `bg #0066CC text white radius-10 px-20 py-10`

---

## 7. API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load danh mục cha (select) | GET | `/categories` | Khi mount |
| Tạo danh mục con | POST | `/admin/subcategories` | Submit form tạo mới |
| Cập nhật danh mục con | PUT | `/admin/subcategories/{id}` | Submit form chỉnh sửa |
| Đổi trạng thái | PATCH | `/admin/subcategories/{id}/status` | Click badge |
| Cập nhật thứ tự | PUT | `/admin/subcategories/{id}` | Blur input sort_order |
| Xóa danh mục con | DELETE | `/admin/subcategories/{id}` | Confirm dialog |
