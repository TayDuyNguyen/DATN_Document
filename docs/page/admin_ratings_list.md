# Màn hình: Danh sách Đánh giá

> Route: `/admin/ratings`
> Quyền: 🛡️ Admin / Staff
> Mô tả: Duyệt và quản lý đánh giá của khách hàng cho địa điểm và tour. Dùng card list thay vì table truyền thống — mỗi đánh giá là 1 card với inline actions.

---

## Layout tổng thể

```
┌─────────────────────────────────────────────────────────────────┐
│  HEADER: Breadcrumb + Tiêu đề + [Xuất Excel]                    │
├─────────────────────────────────────────────────────────────────┤
│  STATS ROW: [Tổng ĐG] [Chờ duyệt ●] [Đã duyệt] [Đã từ chối]   │
├─────────────────────────────────────────────────────────────────┤
│  FILTER BAR: Search + Loại + Trạng thái + Số sao + Lọc         │
├─────────────────────────────────────────────────────────────────┤
│  TOOLBAR: Checkbox + Bulk actions + Per page                    │
│  CARD LIST: mỗi đánh giá = 1 card                              │
│  PAGINATION                                                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1. Page Header

| Element | Style |
|---------|-------|
| Breadcrumb | `12px Inter 500 #94A3B8` — "Đánh giá / Danh sách Đánh giá" |
| Title | `24px Inter 700 #1E293B` — "Danh sách Đánh giá" |
| Subtitle | `14px Inter 400 #64748B` — "Duyệt và quản lý đánh giá của khách hàng" |
| Button "Xuất Excel" | `border #E2E8F0 bg white text #64748B radius-10 px-16 py-10` icon `download` | `GET /admin/ratings/export` |

---

## 2. Stats Row

`grid grid-cols-4 gap-4 mb-24`

| Thẻ | Icon | Icon bg | Value | Label | Value color | Ghi chú |
|-----|------|---------|-------|-------|-------------|---------|
| Tổng đánh giá | `rate_review` | `#EFF6FF` | `1.024` | "TỔNG ĐÁNH GIÁ" | `#1E293B` | |
| Chờ duyệt | `pending` | `#FEF3C7` | `18` | "CHỜ DUYỆT" | `#F59E0B` | Pulse animation trên dot (urgent) |
| Đã duyệt | `check_circle` | `#D1FAE5` | `986` | "ĐÃ DUYỆT" | `#10B981` | |
| Đã từ chối | `cancel` | `#FEE2E2` | `20` | "ĐÃ TỪ CHỐI" | `#EF4444` | |

---

## 3. Filter Bar

**Card:** `bg white border #E2E8F0 radius-16 p-20 mb-24`

### Row 1 (`flex gap-3 flex-wrap`)

| Element | Width | Config |
|---------|-------|--------|
| Search | `flex-1 min-280px` | Placeholder "Tìm theo tên khách hàng, tên tour/địa điểm..." · debounce 300ms |
| Select Loại | `150px` | Tất cả / Địa điểm (location) / Tour (tour) |
| Select Trạng thái | `160px` | Tất cả / Chờ duyệt (pending) / Đã duyệt (approved) / Đã từ chối (rejected) |
| Select Số sao | `140px` | Tất cả / ★★★★★ 5 sao / ★★★★ 4 sao / ★★★ 3 sao / ★★ 2 sao / ★ 1 sao |
| Button Lọc | `auto` | `bg #0066CC text white radius-10 px-20 py-10` |
| Button Đặt lại | `auto` | Chỉ hiện khi có filter · hover `text #EF4444` |

### Row 2 — Active filter tags
- Tag: `bg #EFF6FF text #0066CC border #B3D9FF radius-full px-10 py-4 12px Inter 500`

---

## 4. Toolbar

`bg white border-b #E2E8F0 px-24 py-16 flex justify-between`

**Bên trái:**
- Checkbox "Chọn tất cả"
- Khi có item được chọn: `"Đã chọn 3" 13px 600 #0066CC` + bulk actions:
  - "Duyệt tất cả": `bg #D1FAE5 text #10B981 radius-8 px-12 py-6 12px 600`
  - "Từ chối tất cả": `bg #FEE2E2 text #EF4444`
  - "Xóa": `bg #FEE2E2 text #EF4444`

**Bên phải:**
- `"Hiển thị 1–10 / 1.024 đánh giá" 13px #94A3B8`
- Select per_page: 10 / 20 / 50

---

## 5. Review Card List

**Container:** `bg white border #E2E8F0 radius-b-16 overflow-hidden`

Mỗi card: `border-b #F1F5F9 px-24 py-20`
- Hover: `bg #F8FAFC transition-150ms`
- Selected: `bg #EFF6FF border-l-3 #0066CC`

### 5.1 Row 1 — Header (`flex justify-between items-start`)

**Bên trái** (`flex items-start gap-12`):
- Checkbox: `16px accent-color #0066CC flex-shrink-0 mt-2`
- Avatar: `40x40px rounded-full border-2 #E2E8F0 object-cover`
- Info:
  - Name: `14px Inter 600 #1E293B`
  - Stars + Score: `flex items-center gap-8 mt-2`
    - 5 icon `star` filled `#F59E0B` / empty `#E2E8F0` · size `14px`
    - Score: `"4.8" 13px Inter 700 #1E293B`
  - Date: `"06/04/2026 14:30" 12px #94A3B8 mt-2`

**Bên phải** (`flex items-center gap-8`):
- Badge loại (`11px 600 rounded-full px-8 py-3 flex items-center gap-4`):
  - location: `bg #EEF2FF text #6366F1 border rgba(99,102,241,0.2)` icon `location_on 12px` "Địa điểm"
  - tour: `bg #EFF6FF text #0066CC border #B3D9FF` icon `tour 12px` "Tour"
- Badge trạng thái (`11px 700 rounded-full px-10 py-4`):
  - pending: `bg #FEF3C7 text #F59E0B` "CHỜ DUYỆT"
  - approved: `bg #D1FAE5 text #10B981` "ĐÃ DUYỆT"
  - rejected: `bg #FEE2E2 text #EF4444` "ĐÃ TỪ CHỐI"

### 5.2 Row 2 — Target (`flex items-center gap-8 mt-10 ml-68`)
- Thumbnail: `32x32px radius-6 object-cover border #E2E8F0`
- Tên tour/địa điểm: `13px Inter 500 #1E293B`
- icon `chevron_right 14px #94A3B8`
- Link "Xem →": `12px #0066CC` hover underline → `/admin/locations/{id}` hoặc `/admin/tours/{id}`

### 5.3 Row 3 — Comment (`mt-10 ml-68`)
- Text: `14px Inter 400 #1E293B line-height 1.6`
- Max 3 lines, overflow hidden
- Nếu dài hơn: button "Xem thêm" `12px #0066CC` → expand inline

### 5.4 Row 4 — Images (`flex gap-8 mt-10 ml-68`, chỉ hiện nếu có ảnh)
- Mỗi ảnh: `64x64px radius-8 object-cover border #E2E8F0`
- Hover: scale 1.05, cursor pointer → lightbox

### 5.5 Row 5 — Rejected reason (`mt-8 ml-68`, chỉ hiện nếu status=rejected)
- `bg #FEE2E2 border rgba(239,68,68,0.2) radius-8 px-12 py-8`
- icon `info 14px #EF4444` + text `12px #EF4444`:
  "Lý do từ chối: [rejected_reason]"

### 5.6 Row 6 — Actions (`flex items-center gap-8 mt-12 ml-68`)

**Theo status:**

| Status | Buttons hiện |
|--------|-------------|
| pending | "Duyệt" (xanh) + "Từ chối" (đỏ outline) + "Xóa" (ghost) |
| approved | "Hủy duyệt" (ghost) + "Xóa" (ghost) |
| rejected | "Xóa" (ghost) |

**Button "Duyệt"** (status=pending):
- `bg #10B981 text white radius-8 px-14 py-7 13px 600` icon `check` · hover `bg #059669`
- → `PATCH /admin/ratings/{id}/approve`

**Button "Từ chối"** (status=pending):
- `border #FEE2E2 bg white text #EF4444 radius-8 px-14 py-7 13px 600` icon `close` · hover `bg #FEE2E2`
- → Mở inline reject form bên dưới

**Button "Hủy duyệt"** (status=approved):
- `border #E2E8F0 bg white text #64748B radius-8 px-14 py-7 13px 600` · hover `border #F59E0B text #F59E0B`
- → `PATCH /admin/ratings/{id}/reject`

**Button "Xóa"** (luôn hiện):
- `border #E2E8F0 bg white text #94A3B8 radius-8 px-14 py-7 13px 600` icon `delete` · hover `border #EF4444 text #EF4444`
- → Confirm dialog → `DELETE /admin/ratings/{id}`

**Helpful count** (`ml-auto`):
- icon `thumb_up 14px #94A3B8` + `"12 hữu ích" 12px #94A3B8`

---

## 6. Inline Reject Form

Hiện ngay bên dưới Row 6 khi click "Từ chối":
`bg #FEF3C7 border rgba(245,158,11,0.2) radius-10 p-14 mt-8 ml-68`

- Label: `"Lý do từ chối *" 12px Inter 600 #92400E mb-6`
- Textarea: `rows-2 placeholder "Nhập lý do từ chối..." border rgba(245,158,11,0.3) radius-8 px-12 py-8 13px bg white` · focus `border #F59E0B`
- `flex justify-end gap-8 mt-8`:
  - "Hủy": `border #E2E8F0 bg white text #64748B radius-8 px-12 py-6 12px`
  - "Xác nhận từ chối": `bg #F59E0B text white radius-8 px-12 py-6 12px 600`
    → `PATCH /admin/ratings/{id}/reject` · body: `{ rejected_reason }`

---

## 7. Pagination

`flex justify-between items-center px-24 py-16 border-t #E2E8F0 bg #F8FAFC radius-b-16`

- Trái: `"Hiển thị 1–10 trong tổng số 1.024 đánh giá" 13px #64748B`
- Phải: Prev · 1 · 2 · ... · 103 · Next

---

## 8. Confirm Delete Dialog

**Modal:** `bg white radius-16 w-400px shadow-modal backdrop rgba(0,0,0,0.4)`

| Vùng | Nội dung |
|------|---------|
| Header | Icon `delete 40x40 bg #FEE2E2 radius-10 color #EF4444` + "Xóa đánh giá này?" `16px 700 #1E293B` |
| Body | "Đánh giá của [Tên khách] sẽ bị xóa vĩnh viễn." `14px #64748B` |
| Footer | "Hủy" (ghost) + "Xóa đánh giá" `bg #EF4444 hover #DC2626` |

---

## 9. Empty State

`center py-64`:
- SVG icon `rate_review 80x80px color #E2E8F0`
- Title: `"Không tìm thấy đánh giá nào" 16px Inter 600 #1E293B`
- Subtitle: `"Thử thay đổi bộ lọc" 14px #94A3B8`

---

## 10. API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load danh sách | GET | `/admin/ratings?page=&per_page=&status=` | Khi mount, đổi filter |
| Tìm kiếm | GET | `/admin/ratings?search=` | Nhập search (debounce 300ms) |
| Filter loại | GET | `/admin/ratings?location_id=` hoặc `?tour_id=` | Chọn select loại |
| Filter trạng thái | GET | `/admin/ratings?status=` | Chọn select |
| Filter số sao | GET | `/admin/ratings?score=` | Chọn select |
| Duyệt đánh giá | PATCH | `/admin/ratings/{id}/approve` | Click "Duyệt" |
| Từ chối đánh giá | PATCH | `/admin/ratings/{id}/reject` | Submit inline reject form |
| Xóa đánh giá | DELETE | `/admin/ratings/{id}` | Confirm dialog |
| Bulk duyệt | PATCH | `/admin/ratings/{id}/approve` (loop) | Bulk action |
| Bulk từ chối | PATCH | `/admin/ratings/{id}/reject` (loop) | Bulk action |
| Bulk xóa | DELETE | `/admin/ratings/{id}` (loop) | Bulk action |
| Xuất Excel | GET | `/admin/ratings/export?status=&date_from=&date_to=` | Click "Xuất Excel" |
