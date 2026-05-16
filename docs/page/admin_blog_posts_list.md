# Màn hình: Danh sách Bài viết Blog

> Route: `/admin/blog-posts`
> Quyền: 🛡️ Admin / Staff
> Mô tả: Quản lý nội dung blog — filter, đổi trạng thái (xuất bản/nháp/lưu trữ), xóa bài viết.

---

## Layout tổng thể

```
┌─────────────────────────────────────────────────────────────────┐
│  HEADER: Breadcrumb + Tiêu đề + [Thêm bài viết]                │
├─────────────────────────────────────────────────────────────────┤
│  STATS ROW: [Tổng BV] [Đã XB] [Bản nháp] [Lưu trữ]            │
├─────────────────────────────────────────────────────────────────┤
│  FILTER BAR: Search + Danh mục + Trạng thái + Lọc              │
├─────────────────────────────────────────────────────────────────┤
│  TABLE TOOLBAR: Checkbox + Bulk actions + Per page              │
│  TABLE HEADER: ☐ | Bài viết | Danh mục | 👁 | Ngày tạo |       │
│                Ngày XB | Trạng thái | Thao tác                  │
│  TABLE BODY: rows                                               │
│  PAGINATION                                                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1. Page Header

| Element | Style |
|---------|-------|
| Breadcrumb | `12px Inter 500 #94A3B8` — "Blog / Danh sách Bài viết" |
| Title | `24px Inter 700 #1E293B` — "Danh sách Bài viết" |
| Subtitle | `14px Inter 400 #64748B` — "Quản lý nội dung blog du lịch Đà Nẵng" |
| Button "Thêm bài viết" | `bg #0066CC text white radius-10 px-20 py-10 shadow` icon `add` | Navigate `/admin/blog-posts/create` |

---

## 2. Stats Row

`grid grid-cols-4 gap-4 mb-24`

| Thẻ | Icon | Icon bg | Value | Label | Value color |
|-----|------|---------|-------|-------|-------------|
| Tổng bài viết | `article` | `#EFF6FF` | `48` | "TỔNG BÀI VIẾT" | `#1E293B` |
| Đã xuất bản | `check_circle` | `#D1FAE5` | `32` | "ĐÃ XUẤT BẢN" | `#10B981` |
| Bản nháp | `edit_note` | `#FEF3C7` | `12` | "BẢN NHÁP" | `#F59E0B` |
| Lưu trữ | `archive` | `#F1F5F9` | `4` | "LƯU TRỮ" | `#94A3B8` |

---

## 3. Filter Bar

**Card:** `bg white border #E2E8F0 radius-16 p-20 mb-24`

### Row 1 (`flex gap-3 flex-wrap`)

| Element | Width | Config |
|---------|-------|--------|
| Search | `flex-1 min-280px` | Placeholder "Tìm theo tiêu đề bài viết..." · debounce 300ms |
| Select Danh mục | `180px` | "Tất cả" + list từ `GET /admin/blog-categories` |
| Select Trạng thái | `160px` | Tất cả / Đã xuất bản (published) / Bản nháp (draft) / Lưu trữ (archived) |
| Button Lọc | `auto` | `bg #0066CC text white radius-10 px-20 py-10` |
| Button Đặt lại | `auto` | Chỉ hiện khi có filter · hover `text #EF4444` |

### Row 2 — Active filter tags
- Tag: `bg #EFF6FF text #0066CC border #B3D9FF radius-full px-10 py-4 12px Inter 500`

---

## 4. Table

**Card:** `bg white border #E2E8F0 radius-16 overflow-hidden`

### 4.1 Toolbar

`flex justify-between items-center px-24 py-16 border-b #E2E8F0`

**Bên trái:**
- Checkbox "Chọn tất cả"
- Khi có row được chọn: `"Đã chọn 3" 13px 600 #0066CC` + bulk actions:
  - "Xuất bản": `bg #D1FAE5 text #10B981 radius-8 px-12 py-6 12px 600`
  - "Lưu trữ": `bg #F1F5F9 text #64748B`
  - "Xóa": `bg #FEE2E2 text #EF4444`

**Bên phải:**
- `"Hiển thị 1–10 / 48 bài viết" 13px #94A3B8`
- Select per_page: 10 / 20 / 50

### 4.2 Table Header

`bg #F8FAFC border-b #E2E8F0`
`th: px-16 py-12, 11px Inter 600, uppercase, letter-spacing 0.06em, #94A3B8`

| Cột | Width | Ghi chú |
|-----|-------|---------|
| ☐ | 40px | Checkbox |
| Bài viết | auto | Thumbnail + tiêu đề + excerpt + tác giả |
| Danh mục | 140px | Badge(s) |
| Lượt xem | 100px | Sortable ↕ |
| Ngày tạo | 130px | Sortable ↕ |
| Ngày xuất bản | 140px | |
| Trạng thái | 120px | Badge clickable |
| Thao tác | 100px | |

### 4.3 Table Body

`border-b #F1F5F9 min-h-72px`
- Hover: `bg #F8FAFC transition-150ms`
- Selected: `bg #EFF6FF border-l-3 #0066CC`

#### Chi tiết từng cột

**Col Bài viết** (`flex items-start gap-12`):
- Featured image: `64x48px radius-8 object-cover border #E2E8F0 flex-shrink-0`
- Right:
  - Tiêu đề: `14px Inter 600 #1E293B max-1-line ellipsis` hover `#0066CC` cursor pointer → `/admin/blog-posts/{id}`
  - Excerpt: `12px #94A3B8 max-2-lines ellipsis mt-2`
  - `flex items-center gap-8 mt-4`:
    - Avatar tác giả: `18x18px rounded-full border #E2E8F0`
    - Tên tác giả: `11px Inter 500 #64748B`

**Col Danh mục** (`flex flex-wrap gap-4`):
- Badge: `bg #EFF6FF text #0066CC border #B3D9FF radius-full px-8 py-2 11px 600`
- Nếu > 2: badge `"+1 more" bg #F1F5F9 text #94A3B8`

**Col Lượt xem:**
- icon `visibility 14px #94A3B8` + value `13px Inter 600 #1E293B` — e.g. "1.2K"

**Col Ngày tạo:**
- Date: `13px #1E293B` + Time: `11px #94A3B8`

**Col Ngày xuất bản:**
- Đã xuất bản: `"15/03/2026" 13px #1E293B`
- Chưa xuất bản: `"—" 13px #94A3B8`
- Lên lịch: `"20/04/2026" 13px #F59E0B` + badge "LÊN LỊCH" `bg #FEF3C7 text #F59E0B 10px radius-full px-6 py-1 ml-4`

**Col Trạng thái** — badge pill `11px 700 rounded-full px-10 py-4` · click → dropdown:

| Status | Background | Text |
|--------|-----------|------|
| published | `#D1FAE5` | `#10B981` "ĐÃ XUẤT BẢN" |
| draft | `#FEF3C7` | `#F59E0B` "BẢN NHÁP" |
| archived | `#F1F5F9` | `#94A3B8` "LƯU TRỮ" |

→ `PATCH /admin/blog-posts/{id}/status`

**Col Thao tác** (`flex gap-4`):

| Button | Icon | Hover | Action |
|--------|------|-------|--------|
| Xem | `visibility` | `#0066CC` | `/admin/blog-posts/{id}` |
| Sửa | `edit` | `#F59E0B` | `/admin/blog-posts/{id}/edit` |
| Xóa | `delete` | `#EF4444` | Confirm → `DELETE /admin/blog-posts/{id}` |

Style chung: `28x28px bg #F8FAFC border #E2E8F0 radius-6 color #64748B`

### 4.4 Sample Data

| Bài viết | Danh mục | 👁 | Ngày tạo | Ngày XB | Status |
|---------|---------|---|---------|---------|--------|
| Khám phá Bà Nà Hills | Tham quan | 2.4K | 15/03 09:30 | 15/03/2026 | ĐÃ XUẤT BẢN |
| Top 10 quán ăn Đà Nẵng | Ẩm thực | 1.8K | 20/03 14:00 | 20/03/2026 | ĐÃ XUẤT BẢN |
| Hướng dẫn du lịch Hội An | Tham quan | 0 | 01/04 10:00 | — | BẢN NHÁP |
| Mùa hè ở Cù Lao Chàm | Sinh thái | 0 | 02/04 08:00 | 20/04 LÊN LỊCH | BẢN NHÁP |
| Lễ hội pháo hoa 2025 | Sự kiện | 856 | 10/01 09:00 | 10/01/2026 | LƯU TRỮ |

---

## 5. Pagination

`flex justify-between items-center px-24 py-16 border-t #E2E8F0 bg #F8FAFC radius-b-16`

- Trái: `"Hiển thị 1–10 trong tổng số 48 bài viết" 13px #64748B`
- Phải: Prev · 1 · 2 · ... · 5 · Next

---

## 6. Confirm Delete Dialog

**Modal:** `bg white radius-16 w-400px shadow-modal backdrop rgba(0,0,0,0.4)`

| Vùng | Nội dung |
|------|---------|
| Header | Icon `warning_amber 40x40 bg #FEE2E2 radius-10 color #EF4444` + "Xóa bài viết này?" `16px 700 #1E293B` |
| Body | "Bài viết [Tiêu đề] sẽ bị xóa vĩnh viễn." `14px #64748B` + Warning `bg #FEF3C7 13px #92400E`: "⚠ Tất cả danh mục liên kết sẽ bị gỡ theo." |
| Footer | "Hủy" (ghost) + "Xóa bài viết" `bg #EF4444 hover #DC2626` |

---

## 7. Empty State

`center py-64`:
- SVG icon `article 80x80px color #E2E8F0`
- Title: `"Không tìm thấy bài viết nào" 16px Inter 600 #1E293B`
- Subtitle: `"Thử thay đổi bộ lọc hoặc tạo bài viết mới" 14px #94A3B8`
- Button "Thêm bài viết": `bg #0066CC text white radius-10 px-20 py-10`

---

## 8. API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load danh sách | GET | `/admin/blog-posts?page=&per_page=&sort=&order=` | Khi mount, đổi filter |
| Tìm kiếm | GET | `/admin/blog-posts?search=` | Nhập search (debounce 300ms) |
| Filter danh mục | GET | `/admin/blog-posts?category_id=` | Chọn select |
| Filter trạng thái | GET | `/admin/blog-posts?status=` | Chọn select |
| Load danh mục (select) | GET | `/admin/blog-categories` | Khi mount |
| Đổi trạng thái | PATCH | `/admin/blog-posts/{id}/status` | Click badge → chọn trạng thái |
| Bulk xuất bản | PATCH | `/admin/blog-posts/{id}/status` (loop) | Bulk action |
| Bulk lưu trữ | PATCH | `/admin/blog-posts/{id}/status` (loop) | Bulk action |
| Bulk xóa | DELETE | `/admin/blog-posts/{id}` (loop) | Bulk action |
| Xóa 1 bài | DELETE | `/admin/blog-posts/{id}` | Confirm dialog |

---

## Validation & States

| Hạng mục | Quy tắc |
|---|---|
| Search | Debounce tối thiểu 300ms, trim keyword trước khi gọi API |
| Status filter | Chỉ nhận `draft`, `published`, `archived` hoặc bỏ trống |
| Category filter | `category_id` phải tồn tại trong `GET /admin/blog-categories` |
| Bulk action | Chỉ bật khi có ít nhất 1 bài được chọn; confirm trước bulk delete |
| Đổi trạng thái | Khi publish nếu thiếu title/content thì API trả validation và UI hiển thị lỗi |
| Empty state | Phân biệt "chưa có bài viết" và "không có kết quả theo bộ lọc" |
