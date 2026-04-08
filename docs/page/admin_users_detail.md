# Màn hình: Chi tiết Người dùng

> Route: `/admin/users/{id}`
> Quyền: 🛡️ Admin / Staff
> Mô tả: Xem toàn bộ thông tin người dùng — thông tin cá nhân, lịch sử đặt tour, đánh giá đã viết. Thực hiện khóa/mở khóa, đổi role, xóa tài khoản.

---

## Layout tổng thể

```
┌─────────────────────────────────────────────────────────────────┐
│  HEADER: Breadcrumb + Tên + Badges + [Sửa] [Khóa/Mở khóa]     │
├──────────────────────────────────────┬──────────────────────────┤
│  LEFT COLUMN (65%)                   │  RIGHT COLUMN (320px)    │
│                                      │  sticky top-24           │
│  Section 1: Thông tin cá nhân        │  Card 1: Thống kê        │
│  Section 2: Lịch sử đặt tour (table) │  Card 2: Tài khoản       │
│  Section 3: Đánh giá đã viết (list)  │  Card 3: Thao tác        │
└──────────────────────────────────────┴──────────────────────────┘
```

---

## 1. Page Header

`flex justify-between items-start, mb 24px`

### Bên trái

| Element | Style |
|---------|-------|
| Breadcrumb | `12px Inter 500 #94A3B8` — "Người dùng / Danh sách Người dùng / Nguyễn Văn An" |
| Title + Badges | `flex items-center gap-12 mt-4` |
| Title | `24px Inter 700 #1E293B` — tên người dùng |
| Badge Role | `11px 700 rounded-full px-10 py-4` |
| Badge Trạng thái | `11px 700 rounded-full px-10 py-4` |
| Subtitle | `13px Inter 400 #94A3B8` — "@nguyenvanan · Tham gia 15/03/2026" |

**Badge Role:**
| Role | Background | Text |
|------|-----------|------|
| admin | `#EEF2FF` | `#6366F1` "ADMIN" |
| staff | `#EFF6FF` | `#0066CC` "STAFF" |
| user | `#F1F5F9` | `#64748B` "USER" |

**Badge Trạng thái:**
| Status | Background | Text |
|--------|-----------|------|
| active | `#D1FAE5` | `#10B981` "HOẠT ĐỘNG" |
| banned | `#FEE2E2` | `#EF4444` "BỊ KHÓA" |

### Bên phải (`flex gap-3`)

| Button | Điều kiện | Style | Action |
|--------|-----------|-------|--------|
| Chỉnh sửa | Luôn | `border #E2E8F0 bg white text #64748B radius-10 px-16 py-10` icon `edit` | `/admin/users/{id}/edit` |
| Khóa tài khoản | status=active | `border #FEE2E2 bg white text #EF4444 radius-10 px-16 py-10` icon `block` | `PATCH /admin/users/{id}/status { status: "banned" }` |
| Mở khóa | status=banned | `bg #10B981 text white radius-10 px-16 py-10` icon `lock_open` | `PATCH /admin/users/{id}/status { status: "active" }` |

---

## 2. Left Column

### Section 1 — Thông tin cá nhân

**Card:** `bg white border #E2E8F0 radius-16 p-24 mb-24`
**Section header:** Icon `person #0066CC bg #EFF6FF` + Title "Thông tin cá nhân"

`flex items-start gap-20`:

**Left — Avatar block:**
- Avatar: `80x80px rounded-full border-3 #E2E8F0 object-cover`
- Không có ảnh: bg gradient initials · text white `24px 700`
- Badge role bên dưới: `centered mt-8`

**Right** (`flex-1 grid grid-cols-2 gap-16`):
- Mỗi item: `flex flex-col gap-4`
  - Label: `11px uppercase #94A3B8`
  - Value: `14px Inter 500 #1E293B`

| Label | Value | Style đặc biệt |
|-------|-------|----------------|
| HỌ VÀ TÊN | "Nguyễn Văn An" | — |
| USERNAME | "@nguyenvanan" | `14px monospace` |
| EMAIL | "nguyenvanan@gmail.com" | link `mailto:` color `#0066CC` |
| SỐ ĐIỆN THOẠI | "0905 xxx xxx" hoặc "—" | — |
| NGÀY SINH | "15/01/1995" hoặc "—" | — |
| GIỚI TÍNH | "Nam" hoặc "—" | — |
| THÀNH PHỐ | "Đà Nẵng" hoặc "—" | — |
| NGÀY THAM GIA | "15/03/2026 09:30" | — |
| CẬP NHẬT | "01/04/2026 14:22" | — |
| XÁC THỰC EMAIL | Badge | "ĐÃ XÁC THỰC" `bg #D1FAE5 text #10B981` hoặc "CHƯA XÁC THỰC" `bg #FEF3C7 text #F59E0B` |

---

### Section 2 — Lịch sử đặt tour

**Card:** `bg white border #E2E8F0 radius-16 overflow-hidden mb-24`

**Card header** (`flex justify-between px-24 py-20 border-b #E2E8F0`):
- Left: Icon `shopping_cart #F59E0B bg #FEF3C7` + Title "Lịch sử đặt tour"
- Right:
  - Badge "12 đơn": `bg #EFF6FF text #0066CC 12px 600 radius-full px-10 py-4`
  - Button "Xem tất cả →": `13px 600 #0066CC` hover underline → `/admin/bookings?user_id={id}`

**Table** (API: `GET /admin/users/{id}/bookings?page=1&per_page=5`):

`thead bg #F8FAFC` · `th: px-16 py-10, 11px uppercase #94A3B8`

| Cột | Width |
|-----|-------|
| Mã đơn | 110px |
| Tour | auto |
| Ngày đặt | 130px |
| Tổng tiền | 120px |
| Trạng thái | 120px |

`tbody: border-b #F1F5F9 hover bg #F8FAFC`

**Col Mã đơn:** `"#BK-1008" 13px Inter 700 #0066CC` hover underline → `/admin/bookings/{id}`

**Col Tour:** `13px Inter 500 #1E293B max-1-line ellipsis`

**Col Ngày đặt:** Date `13px #1E293B` + Time `11px #94A3B8`

**Col Tổng tiền:** `13px Inter 700 #1E293B`

**Col Trạng thái** — badge `11px 700 rounded-full px-8 py-3`:
| Status | Background | Text |
|--------|-----------|------|
| completed | `#D1FAE5` | `#10B981` "HOÀN TẤT" |
| confirmed | `#DBEAFE` | `#3B82F6` "ĐÃ XÁC NHẬN" |
| pending | `#FEF3C7` | `#F59E0B` "CHỜ XÁC NHẬN" |
| cancelled | `#FEE2E2` | `#EF4444` "ĐÃ HỦY" |

**Sample data:**
| Mã đơn | Tour | Ngày đặt | Tổng tiền | Status |
|--------|------|----------|-----------|--------|
| #BK-1008 | Bà Nà Hills | 06/04 14:30 | 2.450.000đ | HOÀN TẤT |
| #BK-1006 | Cù Lao Chàm | 05/04 09:00 | 3.600.000đ | ĐÃ XÁC NHẬN |
| #BK-1004 | Sơn Trà | 04/04 10:20 | 750.000đ | ĐÃ HỦY |

---

### Section 3 — Đánh giá đã viết

**Card:** `bg white border #E2E8F0 radius-16 overflow-hidden mb-24`

**Card header** (`flex justify-between px-24 py-20 border-b #E2E8F0`):
- Left: Icon `rate_review #6366F1 bg #EEF2FF` + Title "Đánh giá đã viết"
- Right:
  - Badge "5 đánh giá": `bg #EFF6FF text #0066CC 12px 600 radius-full px-10 py-4`
  - Button "Xem tất cả →": `13px 600 #0066CC` → `/admin/ratings?user_id={id}`

**Review mini list** (API: `GET /admin/users/{id}/ratings?page=1&per_page=3`):

Mỗi item (`px-24 py-14 border-b #F1F5F9 flex justify-between items-start`):

**Left** (`flex gap-12`):
- Thumbnail: `40x40px radius-8 object-cover border #E2E8F0`
- Right:
  - Tên tour/địa điểm: `13px Inter 500 #1E293B`
  - `flex items-center gap-8 mt-4`:
    - Stars: 5 icon `star 12px` filled `#F59E0B` / empty `#E2E8F0`
    - Score: `"4.8" 12px Inter 700 #1E293B`
    - Date: `"06/04/2026" 11px #94A3B8`

**Right** — Badge trạng thái `11px 700 rounded-full px-8 py-3`:
| Status | Background | Text |
|--------|-----------|------|
| approved | `#D1FAE5` | `#10B981` "ĐÃ DUYỆT" |
| pending | `#FEF3C7` | `#F59E0B` "CHỜ DUYỆT" |
| rejected | `#FEE2E2` | `#EF4444` "TỪ CHỐI" |

---

## 3. Right Column — Sidebar

### Card 1 — Thống kê
`bg white border #E2E8F0 radius-16 p-20 mb-16`

**Grid 2 cột, gap 12px:**
- Mỗi stat: `bg #F8FAFC border #E2E8F0 radius-10 p-12 text-center`
  - Value: `20px Inter 700 #1E293B`
  - Label: `11px uppercase #94A3B8 mt-2`

| Value | Label |
|-------|-------|
| "12" | "ĐƠN HÀNG" |
| "5" | "ĐÁNH GIÁ" |
| "8" | "YÊU THÍCH" |
| "2.450.000đ" color `#0066CC` | "TỔNG CHI" |

---

### Card 2 — Tài khoản
`bg white border #E2E8F0 radius-16 p-20 mb-16`

Rows (`space-y-12 flex justify-between items-start 13px`):

| Label | Value |
|-------|-------|
| Role | Badge role |
| Trạng thái | Badge status |
| Xác thực email | Badge xác thực |
| Ngày tham gia | "15/03/2026" `#64748B` |
| Đăng nhập cuối | "01/04/2026 14:22" `#64748B` |

---

### Card 3 — Thao tác
`bg white border #E2E8F0 radius-16 p-20 mb-16`

| Button | Style | Action |
|--------|-------|--------|
| Chỉnh sửa thông tin | `bg #0066CC text white radius-10 py-10 full-width shadow` icon `edit` | `/admin/users/{id}/edit` |
| Đổi role | ghost icon `admin_panel_settings` | Dropdown chọn role |
| Xem đơn hàng | ghost icon `shopping_cart` | `/admin/bookings?user_id={id}` |
| Xem đánh giá | ghost icon `rate_review` | `/admin/ratings?user_id={id}` |
| Khóa tài khoản (active) | `border #FEE2E2 text #EF4444` hover `bg #FEE2E2` icon `block` | `PATCH /admin/users/{id}/status` |
| Mở khóa (banned) | `bg #10B981 text white` icon `lock_open` | `PATCH /admin/users/{id}/status` |
| Xóa tài khoản | `border #FEE2E2 text #EF4444` hover `bg #FEE2E2` icon `delete` | Confirm → `DELETE /admin/users/{id}` |

Ghost style: `border #E2E8F0 bg white text #64748B radius-10 py-10 full-width 13px 600` hover `border #0066CC text #0066CC`

---

## 4. Confirm Delete Dialog

**Modal:** `bg white radius-16 w-400px shadow-modal backdrop rgba(0,0,0,0.4)`

| Vùng | Nội dung |
|------|---------|
| Header | Icon `warning_amber 40x40 bg #FEE2E2 radius-10 color #EF4444` + "Xóa tài khoản này?" `16px 700 #1E293B` |
| Body | "Tài khoản của [Tên] sẽ bị xóa vĩnh viễn." `14px #64748B` + Warning `bg #FEF3C7 13px #92400E`: "⚠ Tất cả đơn hàng, đánh giá, yêu thích và thông báo của người dùng này sẽ bị xóa theo." |
| Footer | "Hủy" (ghost) + "Xóa tài khoản" `bg #EF4444 hover #DC2626` |

---

## 5. API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load chi tiết | GET | `/admin/users/{id}` | Khi mount |
| Load đơn hàng | GET | `/admin/users/{id}/bookings?page=1&per_page=5` | Khi mount |
| Load đánh giá | GET | `/admin/users/{id}/ratings?page=1&per_page=3` | Khi mount |
| Đổi trạng thái | PATCH | `/admin/users/{id}/status` | Click button khóa/mở khóa |
| Đổi role | PATCH | `/admin/users/{id}/role` | Chọn trong dropdown |
| Xóa tài khoản | DELETE | `/admin/users/{id}` | Confirm dialog |
