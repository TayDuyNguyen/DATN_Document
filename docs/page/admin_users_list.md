# Màn hình: Danh sách Người dùng

> Route: `/admin/users`
> Quyền: 🛡️ Admin / Staff
> Mô tả: Quản lý tài khoản người dùng — filter, đổi role, khóa/mở khóa, xóa, xuất Excel.

---

## Layout tổng thể

```
┌─────────────────────────────────────────────────────────────────┐
│  HEADER: Breadcrumb + Tiêu đề + [Xuất Excel] [Thêm người dùng] │
├─────────────────────────────────────────────────────────────────┤
│  STATS ROW: [Tổng ND] [Đang HĐ] [Bị khóa] [Admin & Staff]      │
├─────────────────────────────────────────────────────────────────┤
│  FILTER BAR: Search + Role + Trạng thái + Lọc                   │
├─────────────────────────────────────────────────────────────────┤
│  TABLE TOOLBAR: Checkbox + Bulk actions + Per page              │
│  TABLE HEADER: ☐ | Người dùng | Role | Đơn hàng | ĐG |         │
│                Ngày tham gia | Trạng thái | Thao tác            │
│  TABLE BODY: rows                                               │
│  PAGINATION                                                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1. Page Header

| Element | Style |
|---------|-------|
| Breadcrumb | `12px Inter 500 #94A3B8` — "Người dùng / Danh sách Người dùng" |
| Title | `24px Inter 700 #1E293B` — "Danh sách Người dùng" |
| Subtitle | `14px Inter 400 #64748B` — "Quản lý tài khoản người dùng hệ thống" |
| Button "Xuất Excel" | `border #E2E8F0 bg white text #64748B radius-10 px-16 py-10` icon `download` | `GET /admin/users/export` |
| Button "Thêm người dùng" | `bg #0066CC text white radius-10 px-20 py-10 shadow` icon `add` | Navigate `/admin/users/create` |

---

## 2. Stats Row

`grid grid-cols-4 gap-4 mb-24`

| Thẻ | Icon | Icon bg | Value | Label | Value color |
|-----|------|---------|-------|-------|-------------|
| Tổng người dùng | `group` | `#EFF6FF` | `4.850` | "TỔNG NGƯỜI DÙNG" | `#1E293B` |
| Đang hoạt động | `check_circle` | `#D1FAE5` | `4.712` | "ĐANG HOẠT ĐỘNG" | `#10B981` |
| Bị khóa | `block` | `#FEE2E2` | `138` | "BỊ KHÓA" | `#EF4444` |
| Admin & Staff | `admin_panel_settings` | `#EEF2FF` | `8` | "ADMIN & STAFF" | `#6366F1` |

---

## 3. Filter Bar

**Card:** `bg white border #E2E8F0 radius-16 p-20 mb-24`

### Row 1 (`flex gap-3 flex-wrap`)

| Element | Width | Config |
|---------|-------|--------|
| Search | `flex-1 min-280px` | Placeholder "Tìm theo tên, email, username..." · debounce 300ms |
| Select Role | `160px` | Tất cả / Người dùng (user) / Staff (staff) / Admin (admin) |
| Select Trạng thái | `160px` | Tất cả / Đang hoạt động (active) / Bị khóa (banned) |
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
  - "Kích hoạt": `bg #D1FAE5 text #10B981 radius-8 px-12 py-6 12px 600`
  - "Khóa tài khoản": `bg #FEE2E2 text #EF4444`
  - "Xóa": `bg #FEE2E2 text #EF4444`

**Bên phải:**
- `"Hiển thị 1–10 / 4.850 người dùng" 13px #94A3B8`
- Select per_page: 10 / 20 / 50

### 4.2 Table Header

`bg #F8FAFC border-b #E2E8F0`
`th: px-16 py-12, 11px Inter 600, uppercase, letter-spacing 0.06em, #94A3B8`

| Cột | Width | Ghi chú |
|-----|-------|---------|
| ☐ | 40px | Checkbox |
| Người dùng | auto | Avatar + tên + email + username |
| Role | 110px | Badge clickable → dropdown |
| Đơn hàng | 100px | Sortable ↕ |
| Đánh giá | 90px | |
| Ngày tham gia | 140px | Sortable ↕ |
| Trạng thái | 120px | Badge clickable |
| Thao tác | 120px | Xem + Sửa + Khóa + Xóa |

### 4.3 Table Body

`border-b #F1F5F9 min-h-64px`
- Hover: `bg #F8FAFC transition-150ms`
- Selected: `bg #EFF6FF border-l-3 #0066CC`

#### Chi tiết từng cột

**Col Người dùng** (`flex items-center gap-12`):
- Avatar: `40x40px rounded-full border-2 #E2E8F0 object-cover`
  - Nếu không có ảnh: bg gradient initials · text white `14px 600`
- Right:
  - Full name: `14px Inter 600 #1E293B`
  - Email: `12px #94A3B8 max-1-line ellipsis`
  - Username: `11px #94A3B8` — e.g. "@nguyenvanan"

**Col Role** — badge pill `11px 700 rounded-full px-10 py-4` · click → dropdown:

| Role | Background | Text |
|------|-----------|------|
| admin | `#EEF2FF` | `#6366F1` "ADMIN" |
| staff | `#EFF6FF` | `#0066CC` "STAFF" |
| user | `#F1F5F9` | `#64748B` "USER" |

→ `PATCH /admin/users/{id}/role`

**Col Đơn hàng:**
- Value: `13px Inter 600 #1E293B` + `"đơn" 11px #94A3B8`

**Col Đánh giá:**
- Value: `13px Inter 600 #1E293B` + `"đánh giá" 11px #94A3B8`

**Col Ngày tham gia:**
- Date: `13px Inter 500 #1E293B` — e.g. "15/03/2026"
- Relative: `"3 tháng trước" 11px #94A3B8`

**Col Trạng thái** — badge pill `11px 700 rounded-full px-10 py-4` · click → toggle:

| Status | Background | Text |
|--------|-----------|------|
| active | `#D1FAE5` | `#10B981` "HOẠT ĐỘNG" |
| banned | `#FEE2E2` | `#EF4444` "BỊ KHÓA" |

→ `PATCH /admin/users/{id}/status`

**Col Thao tác** (`flex gap-4`):

| Button | Icon | Điều kiện | Hover | Action |
|--------|------|-----------|-------|--------|
| Xem | `visibility` | Luôn | `#0066CC` | `/admin/users/{id}` |
| Sửa | `edit` | Luôn | `#F59E0B` | `/admin/users/{id}/edit` |
| Khóa | `block` | status=active | `#EF4444` | `PATCH /admin/users/{id}/status { status: "banned" }` |
| Mở khóa | `lock_open` | status=banned | `#10B981` | `PATCH /admin/users/{id}/status { status: "active" }` |
| Xóa | `delete` | Luôn | `#EF4444` | Confirm → `DELETE /admin/users/{id}` |

Style chung: `28x28px bg #F8FAFC border #E2E8F0 radius-6 color #64748B`

### 4.4 Sample Data

| Người dùng | Role | Đơn | ĐG | Ngày TG | Status |
|-----------|------|-----|-----|---------|--------|
| Nguyễn Văn An · @nguyenvanan | USER | 12 | 5 | 15/03/2026 | HOẠT ĐỘNG |
| Trần Thị Bích · @tranbich | USER | 8 | 3 | 20/02/2026 | HOẠT ĐỘNG |
| Admin Duy Tây · @admin | ADMIN | 0 | 0 | 01/01/2026 | HOẠT ĐỘNG |
| Lê Minh Tuấn · @leminhtuan | USER | 2 | 1 | 10/03/2026 | BỊ KHÓA |
| Staff Hoa · @staffhoa | STAFF | 0 | 0 | 05/01/2026 | HOẠT ĐỘNG |

---

## 5. Dropdown Đổi Role (inline)

Khi click badge Role:
- Dropdown: `bg white border #E2E8F0 radius-10 shadow-modal w-140px`
- Mỗi option: `flex items-center gap-8 px-14 py-10 13px #1E293B` hover `bg #F8FAFC`
  - icon `person` + "Người dùng"
  - icon `support_agent` + "Staff"
  - icon `admin_panel_settings` + "Admin"
  - Option hiện tại: icon `check_circle 14px #0066CC` bên phải

**Confirm khi đổi lên Admin:**
- Dialog nhỏ: "Bạn có chắc muốn cấp quyền Admin cho người dùng này?"
- "Hủy" + "Xác nhận" `bg #0066CC`

---

## 6. Confirm Delete Dialog

**Modal:** `bg white radius-16 w-400px shadow-modal backdrop rgba(0,0,0,0.4)`

| Vùng | Nội dung |
|------|---------|
| Header | Icon `warning_amber 40x40 bg #FEE2E2 radius-10 color #EF4444` + "Xóa tài khoản này?" `16px 700 #1E293B` |
| Body | "Tài khoản của [Tên] sẽ bị xóa vĩnh viễn." `14px #64748B` + Warning `bg #FEF3C7 13px #92400E`: "⚠ Tất cả đơn hàng, đánh giá, yêu thích và thông báo của người dùng này sẽ bị xóa theo." |
| Footer | "Hủy" (ghost) + "Xóa tài khoản" `bg #EF4444 hover #DC2626` |

---

## 7. Empty State

`center py-64`:
- SVG icon `person_off 80x80px color #E2E8F0`
- Title: `"Không tìm thấy người dùng nào" 16px Inter 600 #1E293B`
- Subtitle: `"Thử thay đổi bộ lọc hoặc thêm người dùng mới" 14px #94A3B8`
- Button "Thêm người dùng": `bg #0066CC text white radius-10 px-20 py-10`

---

## 8. API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load danh sách | GET | `/admin/users?page=&per_page=&sort=&order=` | Khi mount, đổi filter |
| Tìm kiếm | GET | `/admin/users?q=` | Nhập search (debounce 300ms) |
| Filter role | GET | `/admin/users?role=` | Chọn select |
| Filter trạng thái | GET | `/admin/users?status=` | Chọn select |
| Đổi trạng thái | PATCH | `/admin/users/{id}/status` | Click badge / button khóa |
| Đổi role | PATCH | `/admin/users/{id}/role` | Chọn trong dropdown |
| Xóa người dùng | DELETE | `/admin/users/{id}` | Confirm dialog |
| Bulk kích hoạt | PATCH | `/admin/users/{id}/status` (loop) | Bulk action |
| Bulk khóa | PATCH | `/admin/users/{id}/status` (loop) | Bulk action |
| Bulk xóa | DELETE | `/admin/users/{id}` (loop) | Bulk action |
| Xuất Excel | GET | `/admin/users/export?role=&status=` | Click "Xuất Excel" |
