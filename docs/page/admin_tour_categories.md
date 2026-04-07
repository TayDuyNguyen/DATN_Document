# Màn hình: Danh mục Tour

> Route: `/admin/tour-categories`
> Quyền: 🛡️ Admin / Staff
> Mô tả: Quản lý danh mục phân loại tour — xem danh sách, tạo mới, chỉnh sửa, đổi trạng thái, xóa. Form tạo/sửa hiển thị inline bên phải, không cần chuyển trang.

---

## Layout tổng thể

```
┌─────────────────────────────────────────────────────────────┐
│  HEADER: Breadcrumb + Tiêu đề + [Thêm danh mục]            │
├─────────────────────────────────────────────────────────────┤
│  STATS ROW: [Tổng DM] [Đang HĐ] [Tổng tour]                │
├──────────────────────────────────┬──────────────────────────┤
│  CỘT TRÁI (flex-1)               │  CỘT PHẢI (400px)        │
│                                  │  sticky top-24           │
│  Toolbar: Search + Filter        │  Form tạo / chỉnh sửa    │
│  Table: danh sách danh mục       │  - Tên, Slug, Icon       │
│  Footer: ghi chú drag & drop     │  - Màu nền, Mô tả        │
│                                  │  - Thứ tự, Trạng thái    │
│                                  │  - Preview box           │
└──────────────────────────────────┴──────────────────────────┘
```

---

## 1. Page Header

`flex justify-between items-start, mb 24px`

| Element | Style |
|---------|-------|
| Breadcrumb | `12px Inter 500 #94A3B8` — "Quản lý Tour / Danh mục Tour" |
| Title | `24px Inter 700 #1E293B` — "Danh mục Tour" |
| Subtitle | `14px Inter 400 #64748B` — "Quản lý các danh mục phân loại tour du lịch" |
| Button "Thêm danh mục" | `bg #0066CC text white radius-10 px-20 py-10 shadow` icon `add` → reset form về trạng thái tạo mới |

---

## 2. Stats Row

`grid grid-cols-3 gap-4 mb-24`
Mỗi thẻ: `bg white border #E2E8F0 radius-12 p-16 flex items-center gap-12`

| Thẻ | Icon | Icon bg | Value | Label | Value color |
|-----|------|---------|-------|-------|-------------|
| Tổng danh mục | `category` | `#EFF6FF` | `8` | "TỔNG DANH MỤC" | `#1E293B` |
| Đang hoạt động | `check_circle` | `#D1FAE5` | `6` | "ĐANG HOẠT ĐỘNG" | `#10B981` |
| Tổng tour | `inventory_2` | `#FEF3C7` | `48` | "TỔNG TOUR" | `#F59E0B` |

- Icon container: `36x36px radius-8`
- Label: `12px uppercase #94A3B8`
- Value: `20px Inter 700`

---

## 3. Cột trái — Danh sách danh mục

**Card:** `bg white border #E2E8F0 radius-16 overflow-hidden`

### 3.1 Toolbar

`flex justify-between items-center px-24 py-16 border-b #E2E8F0`

**Bên trái:**
- Search input `width 240px`: icon `search` trái `#94A3B8` · placeholder "Tìm danh mục..." · `border #E2E8F0 radius-8 px-10 py-8 pl-36 13px` · focus `border #0066CC`
- Select "Trạng thái" `width 140px ml-8`: Tất cả / Đang hoạt động / Tạm dừng · same style

**Bên phải:**
- Text `"8 danh mục" 13px #94A3B8`

### 3.2 Table Header

`bg #F8FAFC border-b #E2E8F0`
`th: px-16 py-12, 11px Inter 600, uppercase, letter-spacing 0.06em, #94A3B8`

| Cột | Width | Ghi chú |
|-----|-------|---------|
| # | 48px | Drag handle icon `drag_indicator` |
| Danh mục | auto | Tên + icon + slug + mô tả |
| Số tour | 100px | Count + mini bar |
| Thứ tự | 80px | Input number inline |
| Trạng thái | 120px | Badge clickable |
| Thao tác | 100px | Sửa + Xóa |

### 3.3 Table Body

`border-b #F1F5F9 min-h-60px`
- Hover: `bg #F8FAFC transition-150ms`
- Row đang sửa: `bg #EFF6FF border-l-3 border-#0066CC`

#### Chi tiết từng cột

**Col # (Drag)**
- `13px Inter 500 #94A3B8`
- Icon `drag_indicator` bên trái: `color #E2E8F0` hover `#94A3B8` cursor `grab`

**Col Danh mục** (`flex items-center gap-12`)
- Icon container: `40x40px radius-10` bg màu riêng từng danh mục
  - Icon/emoji `20px` ở giữa
- Right:
  - Tên: `14px Inter 600 #1E293B`
  - Slug: `11px Inter 500 #94A3B8` — e.g. `tham-quan`
  - Mô tả: `12px #94A3B8 max-1-line ellipsis mt-2`

**Col Số tour**
- Value: `13px Inter 600 #1E293B` — e.g. `12`
- Mini bar: `h-3px bg #E2E8F0 radius-full w-48px mt-4` · fill `#0066CC` proportional

**Col Thứ tự**
- Input number: `w-48px border #E2E8F0 radius-6 text-center 13px Inter 600 #1E293B py-4`
- Blur → auto save → `PUT /admin/tour-categories/{id}`

**Col Trạng thái**
- Badge pill `11px Inter 700 rounded-full px-10 py-4` · click → toggle

| Status | Background | Text |
|--------|-----------|------|
| active | `#D1FAE5` | `#10B981` "ĐANG HOẠT ĐỘNG" |
| inactive | `#FEE2E2` | `#EF4444` "TẠM DỪNG" |

→ `PATCH /admin/tour-categories/{id}/status`

**Col Thao tác** (`flex gap-4`)
- Sửa: `28x28px bg #F8FAFC border #E2E8F0 radius-6 color #64748B` hover `border #F59E0B color #F59E0B` → load data vào form phải
- Xóa: hover `border #EF4444 color #EF4444` → confirm dialog → `DELETE /admin/tour-categories/{id}`

### 3.4 Sample Data

| # | Danh mục | Số tour | Thứ tự | Trạng thái |
|---|----------|---------|--------|-----------|
| 1 | 🏖️ Tham quan | 12 | 1 | ĐANG HOẠT ĐỘNG |
| 2 | 🍜 Ẩm thực | 8 | 2 | ĐANG HOẠT ĐỘNG |
| 3 | 🏊 Thể thao & Mạo hiểm | 6 | 3 | ĐANG HOẠT ĐỘNG |
| 4 | 🎭 Văn hóa & Lịch sử | 9 | 4 | ĐANG HOẠT ĐỘNG |
| 5 | 🌿 Sinh thái | 5 | 5 | ĐANG HOẠT ĐỘNG |
| 6 | 🎉 Giải trí | 8 | 6 | TẠM DỪNG |

### 3.5 Card Footer

`px-24 py-12 border-t #E2E8F0 bg #F8FAFC radius-b-16`
- Icon `drag_indicator #94A3B8` + Text `"Kéo thả để sắp xếp thứ tự hiển thị" 12px #94A3B8`

---

## 4. Cột phải — Form tạo / chỉnh sửa

**Card:** `bg white border #E2E8F0 radius-16 p-24 sticky top-24`

### 4.1 Card Header

`flex justify-between items-center mb-20 pb-16 border-b #F1F5F9`

| Trạng thái form | Title | Badge |
|----------------|-------|-------|
| Tạo mới | "Thêm danh mục" `15px Inter 600 #1E293B` | `bg #D1FAE5 text #10B981` "MỚI" |
| Chỉnh sửa | "Chỉnh sửa danh mục" | `bg #EFF6FF text #0066CC` "ĐANG SỬA" |

- Button đóng `×`: `24x24px icon close color #94A3B8` hover `#1E293B` → reset form

### 4.2 Form Fields

`space-y-16`

**Tên danh mục** ✅:
- Input text · placeholder "Ví dụ: Tham quan & Du lịch"
- `border #E2E8F0 radius-10 px-14 py-10 14px Inter`

**Slug**:
- Input text · placeholder "tham-quan-du-lich"
- Helper: "Tự động tạo từ tên"
- Badge "Tự động" `absolute right-12 bg #EFF6FF text #0066CC 11px radius-6 px-8 py-2`

**Icon / Emoji**:
- `flex gap-8`:
  - Input emoji `w-80px text-center 20px py-10 border #E2E8F0 radius-10` · placeholder "🏖️"
  - Text "hoặc" `13px #94A3B8`
  - Input icon name `flex-1 px-14 py-10 border #E2E8F0 radius-10 13px` · placeholder "beach_access"
- Helper: "Nhập emoji hoặc tên icon Material Symbols"

**Màu nền icon**:
- `flex gap-8 flex-wrap`:
  - 8 color swatches: `28x28px rounded-full cursor-pointer`
    Colors: `#EFF6FF` `#FFE0D4` `#D1FAE5` `#FEF3C7` `#FEE2E2` `#EEF2FF` `#E0F2FE` `#FCE7F3`
  - Selected: `ring-2 ring-offset-2 ring-#0066CC`
  - Color picker input: `w-28 h-28 rounded-full border #E2E8F0 cursor-pointer`

**Mô tả**:
- Textarea `rows-3` · placeholder "Mô tả ngắn về danh mục..."
- `border #E2E8F0 radius-10 px-14 py-10 14px Inter resize-none`

**Thứ tự hiển thị**:
- Input number · placeholder "1"
- Helper: "Số nhỏ hơn hiển thị trước"

**Trạng thái**:
- `flex justify-between items-center`
- Label: `"Đang hoạt động" 14px #1E293B`
- Toggle: ON `#0066CC`, OFF `#E2E8F0`, `40x22px`

### 4.3 Preview Box

`mt-16 bg #F8FAFC border #E2E8F0 radius-12 p-16`

- Label: `"XEM TRƯỚC" 10px uppercase #94A3B8 mb-10`
- Preview item: `flex items-center gap-12`
  - Icon container: `44x44px radius-12` bg theo màu đã chọn · icon/emoji `22px` ở giữa
  - Right:
    - Tên: `14px Inter 600 #1E293B` (live update)
    - Slug: `12px #94A3B8` (live update)

### 4.4 Form Footer

`flex gap-8 mt-20 pt-16 border-t #F1F5F9`

| Button | Style | Action |
|--------|-------|--------|
| Hủy | `border #E2E8F0 bg white text #64748B radius-10 py-10 flex-1` hover `border #EF4444 text #EF4444` | Reset form về trạng thái tạo mới |
| Lưu / Tạo | `bg #0066CC text white radius-10 py-10 flex-1 14px 600` hover `bg #004999` | POST (tạo) hoặc PUT (sửa) |

---

## 5. Confirm Delete Dialog

**Trigger:** Click button Xóa
**Modal:** `bg white radius-16 w-400px shadow-modal center backdrop rgba(0,0,0,0.4)`

| Vùng | Nội dung |
|------|---------|
| Header | Icon `warning_amber 40x40 bg #FEE2E2 radius-10 color #EF4444` + Title "Xóa danh mục này?" `16px 700 #1E293B` |
| Body | Text xác nhận `14px #64748B` + Warning box `bg #FEF3C7 border warning radius-8 p-12 13px #92400E`: "⚠ Kiểm tra xem có tour nào đang thuộc danh mục này không. Nếu có, các tour sẽ mất liên kết danh mục." |
| Footer | "Hủy" (ghost) + "Xóa danh mục" `bg #EF4444 hover #DC2626` |

---

## 6. Empty State

Khi chưa có danh mục nào (`center py-64`):
- SVG icon `category 80x80px color #E2E8F0`
- Title: `"Chưa có danh mục nào" 16px Inter 600 #1E293B`
- Subtitle: `"Tạo danh mục đầu tiên để phân loại tour" 14px #94A3B8`
- Button "Thêm danh mục": `bg #0066CC text white radius-10 px-20 py-10`

---

## 7. API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load danh sách | GET | `/admin/tour-categories` | Khi mount |
| Tìm kiếm / filter | — | Client-side filter | Nhập search, chọn status |
| Tạo danh mục | POST | `/admin/tour-categories` | Submit form tạo mới |
| Cập nhật danh mục | PUT | `/admin/tour-categories/{id}` | Submit form chỉnh sửa |
| Cập nhật thứ tự | PUT | `/admin/tour-categories/{id}` | Blur input sort_order |
| Đổi trạng thái | PATCH | `/admin/tour-categories/{id}/status` | Click badge trạng thái |
| Xóa danh mục | DELETE | `/admin/tour-categories/{id}` | Confirm dialog |
