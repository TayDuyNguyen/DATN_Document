# Màn hình: Danh sách Thông báo

> Route: `/notifications`
> Quyền: 🔐 Cần đăng nhập
> Mô tả: Xem toàn bộ thông báo hệ thống — đánh dấu đã đọc, xóa thông báo.

---

## Tái sử dụng từ màn Hồ sơ cá nhân

> Xem chi tiết layout tại `user_profile.md`

Giữ nguyên: Header · Breadcrumb · Sidebar (item "Thông báo" active) · Footer

---

## Main Content

### 1. Page Header

`flex justify-between items-center mb-24`

**Bên trái:**
- Title: `"Thông báo" 20px Inter 700 #1E293B`
- Badge unread: `"3 chưa đọc" bg #FEE2E2 text #EF4444 12px 600 radius-full px-10 py-4 ml-8`
  (API: `GET /user/notifications/unread-count`)

**Bên phải:**
- Button "Đánh dấu tất cả đã đọc": `border #E2E8F0 bg white text #0066CC radius-10 px-16 py-10 13px 600`
  hover `bg #EFF6FF`
  → `PATCH /user/notifications/read-all`
  → Ẩn button khi unread = 0

### 2. Filter Tabs

`flex gap-0 border-b #E2E8F0 mb-24`

| Tab | Label |
|-----|-------|
| Tất cả | "Tất cả" |
| Chưa đọc | "Chưa đọc (3)" |

- Active: `border-b-2 border-#0066CC text #0066CC 14px 600`
- Inactive: `text #64748B 14px 500` hover `text #0066CC`
- Click "Chưa đọc" → filter `is_read=0`

### 3. Notification List

**API: `GET /user/notifications?is_read=&page=1&per_page=20`**

`flex flex-col gap-0`

Mỗi notification item:
`flex gap-16 px-20 py-16 border-b #F1F5F9 cursor-pointer`
hover `bg #F8FAFC`

- Chưa đọc: `bg #EFF6FF` · left border `border-l-3 #0066CC`
- Đã đọc: `bg white`

**Layout:**

**Left — Icon container** (`40x40px radius-12 flex-shrink-0`):
- bg và icon theo loại:

| Type | bg | Icon | Color |
|------|-----|------|-------|
| booking | `#EFF6FF` | `shopping_cart` | `#0066CC` |
| rating | `#FEF3C7` | `star` | `#F59E0B` |
| system | `#F1F5F9` | `info` | `#64748B` |
| promotion | `#FFE0D4` | `local_offer` | `#FF6B35` |

**Middle (flex-1)**:
- Title: `14px Inter 600 #1E293B` (chưa đọc) hoặc `14px Inter 500 #64748B` (đã đọc)
- Content: `13px #94A3B8 mt-2` max 2 lines
- Time: `11px #94A3B8 mt-4` — e.g. "2 giờ trước"

**Right (`flex items-center gap-8`)**:
- Unread dot: `w-8 h-8 bg #0066CC rounded-full` (chỉ hiện khi chưa đọc)
- Button xóa: `24x24px border #E2E8F0 radius-6 bg white` icon `close 14px #94A3B8`
  hover `border #EF4444 color #EF4444`
  → `DELETE /user/notifications/{id}`

**Click vào item:**
- Đánh dấu đã đọc: `PATCH /user/notifications/{id}/read`
- Navigate đến trang liên quan (nếu có `data.url`):
  - booking: `/bookings/{id}`
  - rating: `/locations/{slug}` hoặc `/tours/{slug}`
  - system: không navigate

### 4. Load More / Pagination

`flex justify-center mt-16`

- Button "Tải thêm": `border #E2E8F0 bg white text #64748B radius-10 px-20 py-10 13px 600`
  → load page tiếp theo (infinite scroll hoặc button)
- Hoặc Pagination: Prev · 1 · 2 · Next

### 5. Empty State

`center py-64 text-center`

- SVG icon `notifications_none 80px #E2E8F0`
- Title (dynamic):
  - Tab "Tất cả": `"Chưa có thông báo nào" 18px Inter 600 #1E293B mt-16`
  - Tab "Chưa đọc": `"Bạn đã đọc hết thông báo! 🎉" 18px Inter 600 #1E293B mt-16`
- Subtitle: `"Các thông báo về đơn hàng, đánh giá sẽ xuất hiện ở đây" 14px #94A3B8 mt-8`

---

## API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load danh sách | GET | `/user/notifications?is_read=&page=1&per_page=20` | Khi mount, đổi tab |
| Load unread count | GET | `/user/notifications/unread-count` | Khi mount |
| Đánh dấu 1 đã đọc | PATCH | `/user/notifications/{id}/read` | Click vào item |
| Đánh dấu tất cả đã đọc | PATCH | `/user/notifications/read-all` | Click button header |
| Xóa thông báo | DELETE | `/user/notifications/{id}` | Click button xóa |
