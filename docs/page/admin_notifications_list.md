# Màn hình: Danh sách Thông báo

> Route: `/admin/notifications`
> Quyền: 🛡️ Admin / Staff
> Mô tả: Xem toàn bộ thông báo hệ thống đã gửi đến người dùng — filter theo loại/user, xóa thông báo.

---

## Layout tổng thể

```
┌─────────────────────────────────────────────────────────────────┐
│  HEADER: Breadcrumb + Tiêu đề + [Gửi thông báo]                │
├─────────────────────────────────────────────────────────────────┤
│  STATS ROW: [Tổng TB] [Đã đọc] [Chưa đọc]                      │
├─────────────────────────────────────────────────────────────────┤
│  FILTER BAR: Search + Loại + User + Lọc                         │
├─────────────────────────────────────────────────────────────────┤
│  TABLE TOOLBAR: Checkbox + Bulk delete + Per page               │
│  TABLE: Người nhận | Nội dung | Loại | Thời gian | Đã đọc | ⚙  │
│  PAGINATION                                                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1. Page Header

| Element | Style |
|---------|-------|
| Breadcrumb | `12px Inter 500 #94A3B8` — "Thông báo / Danh sách Thông báo" |
| Title | `24px Inter 700 #1E293B` — "Danh sách Thông báo" |
| Subtitle | `14px Inter 400 #64748B` — "Quản lý thông báo hệ thống gửi đến người dùng" |
| Button "Gửi thông báo" | `bg #0066CC text white radius-10 px-20 py-10 shadow` icon `send` | Navigate `/admin/notifications/send` |

---

## 2. Stats Row

`grid grid-cols-3 gap-4 mb-24`

| Thẻ | Icon | Icon bg | Value | Label | Value color |
|-----|------|---------|-------|-------|-------------|
| Tổng thông báo | `notifications` | `#EFF6FF` | `1.248` | "TỔNG THÔNG BÁO" | `#1E293B` |
| Đã đọc | `mark_email_read` | `#D1FAE5` | `986` | "ĐÃ ĐỌC" | `#10B981` |
| Chưa đọc | `mark_email_unread` | `#FEF3C7` | `262` | "CHƯA ĐỌC" | `#F59E0B` |

---

## 3. Filter Bar

**Card:** `bg white border #E2E8F0 radius-16 p-20 mb-24`

### Row 1 (`flex gap-3 flex-wrap`)

| Element | Width | Config |
|---------|-------|--------|
| Search | `flex-1 min-280px` | Placeholder "Tìm theo tiêu đề, nội dung thông báo..." · debounce 300ms |
| Select Loại | `180px` | Tất cả / Đặt tour (booking) / Đánh giá (rating) / Hệ thống (system) / Khuyến mãi (promotion) |
| Select Trạng thái | `160px` | Tất cả / Đã đọc / Chưa đọc |
| Button Lọc | `auto` | `bg #0066CC text white radius-10 px-20 py-10` |
| Button Đặt lại | `auto` | Chỉ hiện khi có filter |

### Row 2 — Active filter tags
- Tag: `bg #EFF6FF text #0066CC border #B3D9FF radius-full px-10 py-4 12px Inter 500`

---

## 4. Table

**Card:** `bg white border #E2E8F0 radius-16 overflow-hidden`

### 4.1 Toolbar

`flex justify-between items-center px-24 py-16 border-b #E2E8F0`

**Bên trái:**
- Checkbox "Chọn tất cả"
- Khi có row được chọn: `"Đã chọn 3" 13px 600 #0066CC` + bulk action:
  - "Xóa tất cả": `bg #FEE2E2 text #EF4444 radius-8 px-12 py-6 12px 600`

**Bên phải:**
- `"Hiển thị 1–10 / 1.248 thông báo" 13px #94A3B8`
- Select per_page: 10 / 20 / 50

### 4.2 Table Header

`bg #F8FAFC border-b #E2E8F0`
`th: px-16 py-12, 11px Inter 600, uppercase, letter-spacing 0.06em, #94A3B8`

| Cột | Width | Ghi chú |
|-----|-------|---------|
| ☐ | 40px | Checkbox |
| Người nhận | 200px | Avatar + tên + email |
| Nội dung | auto | Tiêu đề + nội dung ngắn |
| Loại | 130px | Badge type |
| Thời gian | 140px | Sortable ↕ |
| Đã đọc | 100px | Badge |
| Thao tác | 80px | Xóa |

### 4.3 Table Body

`border-b #F1F5F9 min-h-60px`
- Hover: `bg #F8FAFC transition-150ms`
- Selected: `bg #EFF6FF border-l-3 #0066CC`
- Row chưa đọc: `bg #FFFBEB` (subtle yellow tint)

**Col Người nhận** (`flex items-center gap-10`):
- Avatar: `32x32px rounded-full border #E2E8F0`
- Name: `13px Inter 600 #1E293B`
- Email: `11px #94A3B8 max-1-line ellipsis`

**Col Nội dung** (`flex flex-col gap-2`):
- Tiêu đề: `13px Inter 600 #1E293B max-1-line ellipsis`
- Nội dung: `12px #94A3B8 max-1-line ellipsis`

**Col Loại** — badge `11px 600 rounded-full px-10 py-4`:

| Type | Background | Text |
|------|-----------|------|
| booking | `#EFF6FF` | `#0066CC` "ĐẶT TOUR" |
| rating | `#FEF3C7` | `#F59E0B` "ĐÁNH GIÁ" |
| system | `#F1F5F9` | `#64748B` "HỆ THỐNG" |
| promotion | `#FFE0D4` | `#FF6B35` "KHUYẾN MÃI" |

**Col Thời gian:**
- Date: `13px #1E293B` — e.g. "06/04/2026"
- Time: `11px #94A3B8` — e.g. "14:30"
- Relative: `"2 giờ trước" 11px #94A3B8`

**Col Đã đọc:**
- Đã đọc: icon `check_circle 16px #10B981`
- Chưa đọc: icon `radio_button_unchecked 16px #F59E0B`

**Col Thao tác:**
- Xóa: `28x28px bg #F8FAFC border #E2E8F0 radius-6 icon delete color #64748B`
  hover `border #EF4444 color #EF4444`
  → confirm → `DELETE /admin/notifications/{id}`

### 4.4 Sample Data

| Người nhận | Nội dung | Loại | Thời gian | Đã đọc |
|-----------|---------|------|---------|--------|
| Nguyễn Văn An | Đơn #BK-1008 đã được xác nhận | ĐẶT TOUR | 06/04 14:30 | ✓ |
| Trần Thị Bích | Đánh giá của bạn đã được duyệt | ĐÁNH GIÁ | 06/04 11:15 | ✗ |
| Lê Minh Tuấn | Đơn #BK-1006 đã hoàn thành | ĐẶT TOUR | 05/04 09:00 | ✓ |
| Phạm Thu Hà | Khuyến mãi mùa hè 2026 | KHUYẾN MÃI | 05/04 08:00 | ✗ |
| Hoàng Văn Đức | Cập nhật hệ thống | HỆ THỐNG | 04/04 10:00 | ✓ |

---

## 5. Pagination

`flex justify-between items-center px-24 py-16 border-t #E2E8F0 bg #F8FAFC radius-b-16`

- Trái: `"Hiển thị 1–10 trong tổng số 1.248 thông báo" 13px #64748B`
- Phải: Prev · 1 · 2 · ... · 125 · Next

---

## 6. Confirm Delete Dialog

**Modal:** `bg white radius-16 w-400px shadow-modal backdrop rgba(0,0,0,0.4)`

| Vùng | Nội dung |
|------|---------|
| Header | Icon `delete 40x40 bg #FEE2E2 radius-10 color #EF4444` + "Xóa thông báo này?" `16px 700 #1E293B` |
| Body | "Thông báo sẽ bị xóa vĩnh viễn." `14px #64748B` |
| Footer | "Hủy" (ghost) + "Xóa" `bg #EF4444 hover #DC2626` |

---

## 7. Empty State

`center py-64`:
- SVG icon `notifications_off 80x80px color #E2E8F0`
- Title: `"Không có thông báo nào" 16px Inter 600 #1E293B`
- Subtitle: `"Thử thay đổi bộ lọc hoặc gửi thông báo mới" 14px #94A3B8`
- Button "Gửi thông báo": `bg #0066CC text white radius-10 px-20 py-10`

---

## 8. API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load danh sách | GET | `/admin/notifications?page=&per_page=` | Khi mount, đổi filter |
| Tìm kiếm | GET | `/admin/notifications?search=` | Nhập search (debounce 300ms) |
| Filter loại | GET | `/admin/notifications?type=` | Chọn select |
| Filter trạng thái | GET | `/admin/notifications?user_id=` | Chọn user |
| Xóa 1 thông báo | DELETE | `/admin/notifications/{id}` | Confirm dialog |
| Bulk xóa | DELETE | `/admin/notifications/{id}` (loop) | Bulk action |
