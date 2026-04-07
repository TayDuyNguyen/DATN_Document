# Màn hình: Chi tiết Địa điểm

> Route: `/admin/locations/{id}`
> Quyền: 🛡️ Admin / Staff
> Mô tả: Xem toàn bộ thông tin chi tiết của một địa điểm — mô tả, liên hệ, bản đồ, tags, tiện ích, đánh giá. Có thể đổi trạng thái và bật/tắt nổi bật trực tiếp trên trang này.

---

## Layout tổng thể

```
┌─────────────────────────────────────────────────────────────────┐
│  HEADER: Breadcrumb + Tên ĐĐ + Badges + [Xem trang] [Sửa]     │
├──────────────────────────────────────┬──────────────────────────┤
│  LEFT COLUMN (65%)                   │  RIGHT COLUMN (320px)    │
│                                      │  sticky top-24           │
│  Section 1: Hero ảnh + Info bar      │  Card 1: Thông tin nhanh │
│  Section 2: Mô tả (tab)              │  Card 2: Thống kê        │
│  Section 3: Thông tin liên hệ        │  Card 3: Cài đặt hiển thị│
│  Section 4: Vị trí bản đồ            │  Card 4: Thao tác        │
│  Section 5: Tags & Tiện ích          │                          │
│  Section 6: Đánh giá                 │                          │
└──────────────────────────────────────┴──────────────────────────┘
```

---

## 1. Page Header

`flex justify-between items-start, mb 24px`

### Bên trái

| Element | Style |
|---------|-------|
| Breadcrumb | `12px Inter 500 #94A3B8` — "Quản lý Địa điểm / Danh sách Địa điểm / Bãi biển Mỹ Khê" |
| Title + Badges | `flex items-center gap-12 mt-4` |
| Title | `24px Inter 700 #1E293B` — tên địa điểm từ API |
| Badge trạng thái | `11px 700 rounded-full px-10 py-4` |
| Badge Nổi bật | `bg #EFF6FF text #0066CC border #B3D9FF` "⭐ NỔI BẬT" (chỉ hiện nếu is_featured) |
| Subtitle | `13px Inter 400 #94A3B8` — "Sơn Trà · Bãi biển · Tạo lúc 15/03/2026" |

**Badge trạng thái:**
| Status | Background | Text |
|--------|-----------|------|
| active | `#D1FAE5` | `#10B981` "ĐANG HOẠT ĐỘNG" |
| inactive | `#FEE2E2` | `#EF4444` "TẠM DỪNG" |

### Bên phải (`flex gap-3`)

| Button | Style | Action |
|--------|-------|--------|
| Xem trang | `border #E2E8F0 bg white text #64748B radius-10 px-16 py-10` icon `open_in_new` | Mở `/locations/{slug}` tab mới |
| Chỉnh sửa | `bg #0066CC text white radius-10 px-20 py-10 shadow` icon `edit` | Navigate `/admin/locations/{id}/edit` |

---

## 2. Left Column

### Section 1 — Hero: Ảnh & Info bar

**Card:** `bg white border #E2E8F0 radius-16 overflow-hidden mb-24`

**Image gallery** (`height 320px, position relative`):
- Main image: `full-width h-320px object-cover`
  (API: `GET /locations/{id}/images` → ảnh đầu tiên)
- Thumbnail strip (`absolute bottom-0 full-width`):
  - `bg rgba(0,0,0,0.5) backdrop-blur-sm px-16 py-12 flex gap-8 overflow-x-auto`
  - Mỗi thumbnail: `56x56px radius-8 object-cover border-2 border-transparent`
  - Active: `border-2 border-white`
- Badge đếm ảnh (`absolute top-12 right-12`):
  - `bg rgba(0,0,0,0.5) text white 12px 600 radius-8 px-10 py-4` — "1 / 6 ảnh"

**Info bar** (`px-24 py-20 flex gap-24 flex-wrap border-t #F1F5F9`):

| Icon | Color | Value | Label |
|------|-------|-------|-------|
| `location_on` | `#0066CC` | "Sơn Trà" | "Quận" |
| `category` | `#10B981` | "Bãi biển" | "Danh mục" |
| `attach_money` | `#F59E0B` | "Miễn phí" | "Mức giá" |
| `schedule` | `#6366F1` | "6:00 - 22:00" | "Giờ mở cửa" |
| `phone` | `#EC4899` | "0905 xxx xxx" | "Điện thoại" |

- Mỗi item: `flex items-center gap-8`
  - Icon: `20px`
  - Value: `14px Inter 600 #1E293B`
  - Label: `11px uppercase #94A3B8 display-block`

---

### Section 2 — Mô tả

**Card:** `bg white border #E2E8F0 radius-16 p-24 mb-24`
**Section header:** Icon `description #0066CC bg #EFF6FF` + Title "Mô tả địa điểm"

**Tab bar** (`flex border-b #E2E8F0 mb-20`):
- "Mô tả ngắn" | "Mô tả chi tiết"
- Active: `border-b-2 border-#0066CC text #0066CC 14px 600`
- Inactive: `text #64748B 14px 500` hover `text #0066CC`

**Content:** `15px Inter 400 #1E293B line-height 1.7 white-space pre-wrap`

---

### Section 3 — Thông tin liên hệ

**Card:** `bg white border #E2E8F0 radius-16 p-24 mb-24`
**Section header:** Icon `contact_phone #10B981 bg #D1FAE5` + Title "Thông tin liên hệ"

**Grid 2 cột, gap 16px:**
- Mỗi item: `flex items-start gap-12`
  - Icon container: `36x36px radius-8 bg #F8FAFC border #E2E8F0` · icon `18px color #0066CC`
  - Right: Label `11px uppercase #94A3B8` + Value `14px Inter 500 #1E293B`

| Icon | Label | Value |
|------|-------|-------|
| `location_on` | "ĐỊA CHỈ" | Full address |
| `phone` | "ĐIỆN THOẠI" | Phone (link `tel:`) |
| `email` | "EMAIL" | Email (link `mailto:`, color `#0066CC`) |
| `language` | "WEBSITE" | URL (link, truncate, color `#0066CC`) |
| `schedule` | "GIỜ MỞ CỬA" | `white-space pre-wrap` |
| `payments` | "KHOẢNG GIÁ" | "Miễn phí" hoặc "50.000 - 200.000 đ" |

---

### Section 4 — Vị trí bản đồ

**Card:** `bg white border #E2E8F0 radius-16 p-24 mb-24`
**Section header:** Icon `map #F59E0B bg #FEF3C7` + Title "Vị trí trên bản đồ"

**Map container** (`h-280px radius-12 overflow-hidden border #E2E8F0`):
- Có tọa độ: iframe Google Maps với marker
- Không có tọa độ: icon `map 48px #E2E8F0` + text `"Chưa có tọa độ" 14px #94A3B8 centered`

**Coordinates row** (`mt-12 flex gap-16`):
- `"Vĩ độ: 16.0544" 13px Inter 500 #64748B`
- `"Kinh độ: 108.2022" 13px Inter 500 #64748B`
- Button "Mở Google Maps": icon `open_in_new` text `#0066CC 13px 600`
  → `maps.google.com?q=lat,lng` tab mới

---

### Section 5 — Tags & Tiện ích

**Card:** `bg white border #E2E8F0 radius-16 p-24 mb-24`
**Section header:** Icon `label #EC4899 bg #FCE7F3` + Title "Tags & Tiện ích"

**Sub-section Tags** (`mb-20`):
- Label: `"TAGS" 11px uppercase #94A3B8 mb-10`
- `flex flex-wrap gap-8`:
  - Tag: `bg #EFF6FF border #B3D9FF text #0066CC radius-full px-12 py-6 13px 600`
  - Không có: `"Chưa có tags" 13px #94A3B8 italic`

**Sub-section Tiện ích**:
- Label: `"TIỆN ÍCH" 11px uppercase #94A3B8 mb-10`
- `grid-cols-3 gap-8`:
  - Item: `flex items-center gap-8 bg #F8FAFC border #E2E8F0 radius-10 px-14 py-10`
    - Icon `18px #0066CC` + Text `13px #1E293B`
  - Không có: `"Chưa có tiện ích" 13px #94A3B8 italic`

---

### Section 6 — Đánh giá

**Card:** `bg white border #E2E8F0 radius-16 overflow-hidden mb-24`

**Card header** (`flex justify-between px-24 py-20 border-b #E2E8F0`):
- Left: Icon `star #F59E0B bg #FEF3C7` + Title "Đánh giá"
- Right: Button "Xem tất cả →" `13px 600 #0066CC` hover underline
  → `/admin/ratings?location_id={id}`

**Rating overview** (`px-24 py-20 flex gap-32 border-b #E2E8F0`):

Left — Big score:
- Score: `"4.8" 48px Inter 700 #1E293B`
- Stars: 5 icons `star 20px #F59E0B`
- Sub: `"(96 đánh giá)" 13px #94A3B8`

Right — Distribution (API: `GET /locations/{id}/rating-stats`):
- 5 rows (5★ → 1★): `flex items-center gap-8`
  - Label: `"5★" 12px #64748B w-20px`
  - Bar: `flex-1 h-6px bg #E2E8F0 radius-full` · Fill: `bg #F59E0B` width proportional
  - Count: `"52" 12px #94A3B8 w-24px text-right`

**Review list** (API: `GET /locations/{id}/ratings?page=1&per_page=3`):
- 3 đánh giá gần nhất
- Mỗi review (`px-24 py-16 border-b #F1F5F9`):
  - Header: `flex justify-between`
    - Left: Avatar `36x36px rounded-full` + Name `14px 600 #1E293B` + Date `12px #94A3B8`
    - Right: Stars + score `13px 600 #1E293B`
  - Comment: `14px #64748B line-height 1.6 mt-8`
  - Images (nếu có): `flex gap-8 mt-8` · `60x60px radius-8 object-cover border #E2E8F0`
  - Status badge:
    - "CHỜ DUYỆT": `bg #FEF3C7 text #F59E0B`
    - "ĐÃ TỪ CHỐI": `bg #FEE2E2 text #EF4444`

---

## 3. Right Column — Sidebar

### Card 1 — Thông tin nhanh
`bg white border #E2E8F0 radius-16 p-20 mb-16`

Title: `"Thông tin địa điểm" 14px Inter 600 #1E293B mb-16`

Info rows (`space-y-12 flex justify-between items-start`):

| Label | Value |
|-------|-------|
| Danh mục | Badge `bg #EFF6FF text #0066CC` |
| Danh mục con | Text hoặc "—" |
| Quận | "Sơn Trà" |
| Mức giá | "$" hoặc "Miễn phí" |
| Tọa độ | `"16.0544, 108.2022" 12px monospace` |
| Ngày tạo | "15/03/2026 09:30" |
| Cập nhật | "01/04/2026 14:22" |

---

### Card 2 — Thống kê
`bg white border #E2E8F0 radius-16 p-20 mb-16`

**Grid 2 cột, gap 12px:**
- Mỗi stat: `bg #F8FAFC border #E2E8F0 radius-10 p-12 text-center`
  - Value: `20px Inter 700 #1E293B`
  - Label: `11px uppercase #94A3B8 mt-2`

| Value | Label |
|-------|-------|
| "12.4K" | "LƯỢT XEM" |
| "★ 4.8" color `#F59E0B` | "ĐÁNH GIÁ" |
| "1.2K" | "YÊU THÍCH" |
| "96" | "BÌNH LUẬN" |

---

### Card 3 — Cài đặt hiển thị
`bg white border #E2E8F0 radius-16 p-20 mb-16`

**Trạng thái** (`flex justify-between items-center mb-12`):
- Label: `"Trạng thái" 14px #1E293B`
- Dropdown badge: `"ĐANG HOẠT ĐỘNG ▾" bg #D1FAE5 text #10B981 radius-8 px-10 py-6 12px 700`
  - Click → dropdown: Đang hoạt động | Tạm dừng
  - → `PATCH /admin/locations/{id}/status`

**Toggle Nổi bật** (`flex justify-between items-center py-12 border-t #F1F5F9`):
- Left: `"Địa điểm nổi bật" 14px #1E293B` + `"Hiển thị trong mục nổi bật" 12px #94A3B8`
- Toggle: ON `#0066CC`, OFF `#E2E8F0`, `40x22px`
- → `PATCH /admin/locations/{id}/featured`

---

### Card 4 — Thao tác
`bg white border #E2E8F0 radius-16 p-20 mb-16`

| Button | Style | Action |
|--------|-------|--------|
| Chỉnh sửa địa điểm | `bg #0066CC text white radius-10 py-10 full-width shadow` icon `edit` | `/admin/locations/{id}/edit` |
| Xem đánh giá | ghost style icon `star` | `/admin/ratings?location_id={id}` |
| Xem địa điểm lân cận | ghost style icon `near_me` | `/locations/{id}/nearby` tab mới |
| Xóa địa điểm | `border #FEE2E2 text #EF4444` hover `bg #FEE2E2` icon `delete` | Confirm → `DELETE /admin/locations/{id}` → redirect `/admin/locations` |

Ghost style: `border #E2E8F0 bg white text #64748B radius-10 py-10 full-width 13px 600` hover `border #0066CC text #0066CC`

---

## 4. Confirm Delete Dialog

**Modal:** `bg white radius-16 w-400px shadow-modal backdrop rgba(0,0,0,0.4)`

| Vùng | Nội dung |
|------|---------|
| Header | Icon `warning_amber 40x40 bg #FEE2E2 radius-10 color #EF4444` + "Xóa địa điểm này?" `16px 700 #1E293B` |
| Body | "Địa điểm [Tên] sẽ bị xóa vĩnh viễn." `14px #64748B` + Warning `bg #FEF3C7 13px #92400E`: "⚠ Tất cả đánh giá, lượt yêu thích, tags và tiện ích liên quan sẽ bị xóa theo." |
| Footer | "Hủy" (ghost) + "Xóa địa điểm" `bg #EF4444 hover #DC2626` |

---

## 5. API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load chi tiết | GET | `/locations/{slug}` | Khi mount |
| Load ảnh | GET | `/locations/{id}/images` | Khi mount |
| Load đánh giá | GET | `/locations/{id}/ratings?page=1&per_page=3` | Khi mount |
| Load rating stats | GET | `/locations/{id}/rating-stats` | Khi mount |
| Đổi trạng thái | PATCH | `/admin/locations/{id}/status` | Click dropdown trạng thái |
| Bật/tắt nổi bật | PATCH | `/admin/locations/{id}/featured` | Toggle |
| Xóa địa điểm | DELETE | `/admin/locations/{id}` | Confirm dialog |
