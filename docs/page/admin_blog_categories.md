# Màn hình: Danh mục Blog

> Route: `/admin/blog-categories`
> Quyền: 🛡️ Admin / Staff
> Mô tả: Quản lý danh mục blog — xem danh sách, tạo mới, chỉnh sửa, xóa. Form tạo/sửa hiển thị inline bên phải. Không có toggle trạng thái (blog categories luôn active).

---

## Layout tổng thể

```
┌─────────────────────────────────────────────────────────────────┐
│  HEADER: Breadcrumb + Tiêu đề + [Thêm danh mục]                │
├─────────────────────────────────────────────────────────────────┤
│  STATS ROW: [Tổng DM] [Tổng bài viết]                          │
├──────────────────────────────────┬──────────────────────────────┤
│  CỘT TRÁI (flex-1)               │  CỘT PHẢI (380px)            │
│                                  │  sticky top-24               │
│  Toolbar: Search + count         │  Form tạo / chỉnh sửa        │
│  Table: danh sách danh mục       │  - Tên, Slug, Mô tả          │
│  Footer                          │  - Preview box               │
└──────────────────────────────────┴──────────────────────────────┘
```

---

## 1. Page Header

| Element | Style |
|---------|-------|
| Breadcrumb | `12px Inter 500 #94A3B8` — "Blog / Danh mục Blog" |
| Title | `24px Inter 700 #1E293B` — "Danh mục Blog" |
| Subtitle | `14px Inter 400 #64748B` — "Quản lý danh mục phân loại bài viết blog" |
| Button "Thêm danh mục" | `bg #0066CC text white radius-10 px-20 py-10 shadow` icon `add` → reset form về tạo mới |

---

## 2. Stats Row

`grid grid-cols-2 gap-4 mb-24`

| Thẻ | Icon | Icon bg | Value | Label | Value color |
|-----|------|---------|-------|-------|-------------|
| Tổng danh mục | `folder` | `#EFF6FF` | `8` | "TỔNG DANH MỤC" | `#1E293B` |
| Tổng bài viết | `article` | `#D1FAE5` | `48` | "TỔNG BÀI VIẾT" | `#10B981` |

---

## 3. Cột trái — Danh sách

**Card:** `bg white border #E2E8F0 radius-16 overflow-hidden`

### 3.1 Toolbar

`flex justify-between items-center px-24 py-16 border-b #E2E8F0`

- Search `width 240px`: icon `search` trái · placeholder "Tìm danh mục..." · `border #E2E8F0 radius-8 px-10 py-8 pl-36 13px` · focus `border #0066CC`
- Text `"8 danh mục" 13px #94A3B8`

### 3.2 Table Header

`bg #F8FAFC border-b #E2E8F0`
`th: px-16 py-12, 11px Inter 600, uppercase, letter-spacing 0.06em, #94A3B8`

| Cột | Width | Ghi chú |
|-----|-------|---------|
| # | 48px | Drag handle `drag_indicator` |
| Danh mục | auto | Tên + slug + mô tả |
| Số bài viết | 120px | Count + mini bar |
| Thao tác | 100px | Sửa + Xóa |

### 3.3 Table Body

`border-b #F1F5F9 min-h-56px`
- Hover: `bg #F8FAFC transition-150ms`
- Row đang sửa: `bg #EFF6FF border-l-3 #0066CC`

**Col # (Drag):**
- `13px Inter 500 #94A3B8`
- icon `drag_indicator color #E2E8F0` hover `#94A3B8` cursor `grab`

**Col Danh mục** (`flex items-center gap-12`):
- Icon container: `36x36px radius-8 bg #EFF6FF`
  - icon `folder 18px #0066CC` ở giữa
- Right:
  - Tên: `14px Inter 600 #1E293B`
  - Slug: `11px Inter 500 #94A3B8` — e.g. `tham-quan`
  - Mô tả: `12px #94A3B8 max-1-line ellipsis mt-2`

**Col Số bài viết:**
- Value: `13px Inter 600 #1E293B` — e.g. `12`
- Mini bar: `h-3px bg #E2E8F0 radius-full w-48px mt-4` · fill `#0066CC` proportional

**Col Thao tác** (`flex gap-4`):
- Sửa: `28x28px bg #F8FAFC border #E2E8F0 radius-6 color #64748B` hover `border #F59E0B color #F59E0B` → load data vào form phải
- Xóa: hover `border #EF4444 color #EF4444` → confirm → `DELETE /admin/blog-categories/{id}`

### 3.4 Sample Data

| # | Danh mục | Số bài |
|---|----------|--------|
| 1 | 🏖️ Tham quan | 12 |
| 2 | 🍜 Ẩm thực | 8 |
| 3 | 🌿 Sinh thái | 6 |
| 4 | 🎭 Văn hóa | 9 |
| 5 | 🎉 Sự kiện | 5 |
| 6 | 💡 Mẹo du lịch | 8 |

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
| Tạo mới | "Thêm danh mục" `15px Inter 600 #1E293B` | `bg #D1FAE5 text #10B981` "MỚI" |
| Chỉnh sửa | "Chỉnh sửa danh mục" | `bg #EFF6FF text #0066CC` "ĐANG SỬA" |

- Button `×`: `24x24px icon close color #94A3B8` hover `#1E293B` → reset form

### 4.2 Form Fields

`space-y-16`

| Field | Type | Bắt buộc | Config |
|-------|------|----------|--------|
| Tên danh mục | text | ✅ | placeholder "Ví dụ: Tham quan & Du lịch" |
| Slug | text | — | placeholder "tham-quan-du-lich" · badge "Tự động" `bg #EFF6FF text #0066CC 11px` · helper "Tự động tạo từ tên" |
| Mô tả | textarea rows-3 | — | placeholder "Mô tả ngắn về danh mục..." · resize-none |

### 4.3 Preview Box

`mt-16 bg #F8FAFC border #E2E8F0 radius-12 p-16`

- Label: `"XEM TRƯỚC" 10px uppercase #94A3B8 mb-10`
- Preview item: `flex items-center gap-12`
  - Icon container: `40x40px radius-10 bg #EFF6FF` · icon `folder 20px #0066CC`
  - Right:
    - Tên: `14px Inter 600 #1E293B` (live update)
    - Slug: `12px #94A3B8` (live update)
    - Mô tả: `12px #94A3B8 mt-2` (live update, max 1 line)

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
| Header | Icon `warning_amber 40x40 bg #FEE2E2 radius-10 color #EF4444` + "Xóa danh mục này?" `16px 700 #1E293B` |
| Body | "Danh mục [Tên] sẽ bị xóa vĩnh viễn." `14px #64748B` + Warning `bg #FEF3C7 13px #92400E`: "⚠ Các bài viết thuộc danh mục này sẽ mất liên kết danh mục." |
| Footer | "Hủy" (ghost) + "Xóa danh mục" `bg #EF4444 hover #DC2626` |

---

## 6. Empty State

`center py-64`:
- SVG icon `folder_off 80x80px color #E2E8F0`
- Title: `"Chưa có danh mục nào" 16px Inter 600 #1E293B`
- Subtitle: `"Tạo danh mục đầu tiên để phân loại bài viết" 14px #94A3B8`
- Button "Thêm danh mục": `bg #0066CC text white radius-10 px-20 py-10`

---

## 7. API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load danh sách | GET | `/admin/blog-categories` | Khi mount |
| Tạo danh mục | POST | `/admin/blog-categories` | Submit form tạo mới |
| Cập nhật danh mục | PUT | `/admin/blog-categories/{id}` | Submit form chỉnh sửa |
| Xóa danh mục | DELETE | `/admin/blog-categories/{id}` | Confirm dialog |
