# Màn hình: Chi tiết Tour

> Route: `/admin/tours/{id}`
> Quyền: 🛡️ Admin / Staff
> Mô tả: Xem toàn bộ thông tin chi tiết của một tour — mô tả, giá, lịch trình, lịch khởi hành, đánh giá. Có thể thao tác nhanh đổi trạng thái, bật/tắt nổi bật/hot, xóa tour ngay trên trang này.

---

## Layout tổng thể

```
┌─────────────────────────────────────────────────────────────────┐
│  HEADER: Breadcrumb + Tên tour + Badges + [Xem trang] [Sửa]    │
├──────────────────────────────────────┬──────────────────────────┤
│  LEFT COLUMN (65%)                   │  RIGHT COLUMN (320px)    │
│                                      │  sticky top-24           │
│  Section 1: Hero ảnh + Info bar      │  Card 1: Thông tin nhanh │
│  Section 2: Mô tả (tab)              │  Card 2: Thống kê        │
│  Section 3: Bảng giá                 │  Card 3: Cài đặt hiển thị│
│  Section 4: Lịch trình               │  Card 4: Thao tác        │
│  Section 5: Bao gồm / Không bao gồm  │                          │
│  Section 6: Lịch khởi hành (table)   │                          │
│  Section 7: Đánh giá                 │                          │
└──────────────────────────────────────┴──────────────────────────┘
```

---

## 1. Page Header

`flex justify-between items-start, mb 24px`

### Bên trái
| Element | Style |
|---------|-------|
| Breadcrumb | `12px Inter 500 #94A3B8` — "Quản lý Tour / Danh sách Tour / Bà Nà Hills - Cầu Vàng" |
| Title + Badges | `flex items-center gap-12 mt-4` |
| Title | `24px Inter 700 #1E293B` — tên tour từ API |
| Badge trạng thái | `11px 700 rounded-full px-10 py-4` — theo status hiện tại |
| Badge Nổi bật | `bg #EFF6FF text #0066CC border #B3D9FF` — "⭐ NỔI BẬT" (chỉ hiện nếu is_featured) |
| Badge Hot | `bg #FFE0D4 text #FF6B35 border rgba(255,107,53,0.2)` — "🔥 HOT" (chỉ hiện nếu is_hot) |
| Subtitle | `13px Inter 400 #94A3B8` — "TOUR-001 · Tham quan · Tạo lúc 15/03/2026" |

**Badge trạng thái:**
| Status | Background | Text |
|--------|-----------|------|
| active | `#D1FAE5` | `#10B981` "ĐANG HOẠT ĐỘNG" |
| inactive | `#FEE2E2` | `#EF4444` "TẠM DỪNG" |
| sold_out | `#FEF3C7` | `#F59E0B` "HẾT CHỖ" |

### Bên phải (`flex gap-3`)
| Button | Style | Action |
|--------|-------|--------|
| Xem trang | `border #E2E8F0 bg white text #64748B radius-10 px-16 py-10` icon `open_in_new` | Mở `/tours/{slug}` tab mới |
| Chỉnh sửa | `bg #0066CC text white radius-10 px-20 py-10 shadow` icon `edit` | Navigate `/admin/tours/{id}/edit` |

---

## 2. Left Column

### Section 1 — Hero: Ảnh & Info bar

**Card:** `bg white border #E2E8F0 radius-16 overflow-hidden mb-24`

**Image gallery** (`height 320px, position relative`):
- Main image: `full-width h-320px object-cover`
- Thumbnail strip (`absolute bottom-0 full-width`):
  - `bg rgba(0,0,0,0.5) backdrop-blur-sm px-16 py-12 flex gap-8 overflow-x-auto`
  - Mỗi thumbnail: `56x56px radius-8 object-cover border-2 border-transparent`
  - Active: `border-2 border-white`
- Badge đếm ảnh (`absolute top-12 right-12`):
  - `bg rgba(0,0,0,0.5) text white 12px 600 radius-8 px-10 py-4` — "1 / 8 ảnh"

**Info bar** (`px-24 py-20 flex gap-24 flex-wrap border-t #F1F5F9`):

| Icon | Color | Value | Label |
|------|-------|-------|-------|
| `schedule` | `#0066CC` | "1 ngày" | "Thời lượng" |
| `group` | `#10B981` | "20 người" | "Tối đa" |
| `location_on` | `#F59E0B` | "Bà Nà Hills" | "Điểm đến" |
| `access_time` | `#6366F1` | "07:00" | "Giờ khởi hành" |
| `flag` | `#EC4899` | "2 người" | "Tối thiểu" |

- Mỗi item: `flex items-center gap-8`
  - Icon: `20px`
  - Value: `14px Inter 600 #1E293B`
  - Label: `11px uppercase #94A3B8 display-block`

---

### Section 2 — Mô tả

**Card:** `bg white border #E2E8F0 radius-16 p-24 mb-24`
**Section header:** Icon `description #0066CC bg #EFF6FF` + Title "Mô tả tour"

**Tab bar** (`flex border-b #E2E8F0 mb-20`):
- "Mô tả ngắn" | "Mô tả chi tiết"
- Active: `border-b-2 border-#0066CC text #0066CC 14px 600`
- Inactive: `text #64748B 14px 500` hover `text #0066CC`

**Content:**
- `15px Inter 400 #1E293B line-height 1.7 white-space pre-wrap`

---

### Section 3 — Bảng giá

**Card:** `bg white border #E2E8F0 radius-16 p-24 mb-24`
**Section header:** Icon `payments #10B981 bg #D1FAE5` + Title "Bảng giá"

**Grid 3 cột, gap 16px:**

| Card | Label | Màu value |
|------|-------|-----------|
| Người lớn | "NGƯỜI LỚN" | `#1E293B` |
| Trẻ em | "TRẺ EM" | `#1E293B` hoặc `#10B981` nếu miễn phí |
| Em bé | "EM BÉ" | `#10B981` "Miễn phí" |

- Mỗi price card: `bg #F8FAFC border #E2E8F0 radius-12 p-16 text-center`
  - Label: `11px uppercase #94A3B8`
  - Price: `22px Inter 700`
  - Sub: `"/ người" 12px #94A3B8`

**Discount row** (chỉ hiện nếu `discount_percent > 0`, `mt-16`):
- `bg #FFE0D4 border rgba(255,107,53,0.2) radius-10 px-16 py-12 flex justify-between items-center`
- Left: icon `local_offer #FF6B35` + "Đang giảm 15%" `14px 600 #FF6B35`
- Right: "Giá gốc: 1.000.000 đ" `13px #94A3B8 line-through`

---

### Section 4 — Lịch trình

**Card:** `bg white border #E2E8F0 radius-16 p-24 mb-24`
**Section header:** Icon `route #6366F1 bg #EEF2FF` + Title "Lịch trình"

**Timeline** (`space-y-0`):
- Mỗi ngày: `flex gap-16`
  - Left: `flex flex-col items-center`
    - Badge "Ngày 1": `28x28px bg #EFF6FF text #0066CC 12px 700 rounded-full flex-shrink-0`
    - Line nối: `flex-1 w-2px bg #E2E8F0 mx-auto` (không có ở ngày cuối)
  - Right: `pb-24` (trừ ngày cuối)
    - Content: `14px Inter 400 #1E293B line-height 1.7 white-space pre-wrap`

---

### Section 5 — Bao gồm & Không bao gồm

**Card:** `bg white border #E2E8F0 radius-16 p-24 mb-24`
**Section header:** Icon `checklist #0891B2 bg #E0F2FE` + Title "Dịch vụ"

**Grid 2 cột, gap 24px:**

| Cột | Label | Icon | Icon color |
|-----|-------|------|-----------|
| Trái | "✓ Bao gồm" `13px 600 #10B981` | `check_circle 16px` | `#10B981` |
| Phải | "✗ Không bao gồm" `13px 600 #EF4444` | `cancel 16px` | `#EF4444` |

- Mỗi item: `flex gap-8` · Text: `14px #1E293B`

---

### Section 6 — Lịch khởi hành

**Card:** `bg white border #E2E8F0 radius-16 overflow-hidden mb-24`

**Card header** (`flex justify-between px-24 py-20 border-b #E2E8F0`):
- Left: Icon `calendar_month #F59E0B bg #FEF3C7` + Title "Lịch khởi hành"
- Right:
  - Badge "5 lịch": `bg #EFF6FF text #0066CC 12px 600 radius-full px-10 py-4`
  - Button "Thêm lịch": `bg #0066CC text white radius-8 px-14 py-8 13px 600` icon `add`
    → Navigate `/admin/tours/{id}/schedules/create`

**Table** (API: `GET /tours/{id}/schedules`):

`thead: bg #F8FAFC, th: px-16 py-10, 11px uppercase #94A3B8`

| Cột | Width | Nội dung |
|-----|-------|---------|
| Ngày khởi hành | 140px | `14px Inter 600 #1E293B` |
| Ngày kết thúc | 140px | `14px Inter 400 #64748B` |
| Giá (override) | 120px | Có giá riêng: `13px 700 #FF6B35` · Không: `13px #94A3B8` "Theo tour" |
| Đã đặt / Tối đa | 130px | "12 / 20" `13px 600 #1E293B` + mini progress bar `h-3px mt-4 w-64px` |
| Trạng thái | 120px | Badge pill |
| Thao tác | 80px | Button sửa + xóa |

**Badge trạng thái lịch:**
| Status | Background | Text |
|--------|-----------|------|
| available | `#D1FAE5` | `#10B981` "CÒN CHỖ" |
| full | `#FEE2E2` | `#EF4444` "ĐẦY CHỖ" |
| cancelled | `#F1F5F9` | `#94A3B8` "ĐÃ HỦY" |

**Progress bar màu:**
- Bình thường: fill `#0066CC`
- Full (booked = max): fill `#EF4444`

**Thao tác:**
- Sửa: `28x28px bg #F8FAFC border #E2E8F0 radius-6` icon `edit` hover `#F59E0B`
  → `/admin/tour-schedules/{id}/edit`
- Xóa: icon `delete` hover `#EF4444` → confirm → `DELETE /admin/tour-schedules/{id}`

**Sample data:**
| Ngày KH | Ngày KT | Giá | Đặt/Max | Status |
|---------|---------|-----|---------|--------|
| 15/04/2026 | 15/04/2026 | Theo tour | 12/20 | CÒN CHỖ |
| 22/04/2026 | 22/04/2026 | 900.000đ | 20/20 | ĐẦY CHỖ |
| 01/05/2026 | 01/05/2026 | Theo tour | 0/20 | CÒN CHỖ |

---

### Section 7 — Đánh giá

**Card:** `bg white border #E2E8F0 radius-16 overflow-hidden mb-24`

**Card header** (`flex justify-between px-24 py-20 border-b #E2E8F0`):
- Left: Icon `star #F59E0B bg #FEF3C7` + Title "Đánh giá"
- Right: Button "Xem tất cả →" `13px 600 #0066CC` hover underline
  → Navigate `/admin/ratings?tour_id={id}`

**Rating overview** (`px-24 py-20 flex gap-32 border-b #E2E8F0`):

Left — Big score:
- Score: `"4.8" 48px Inter 700 #1E293B`
- Stars: 5 icons `star 20px #F59E0B`
- Sub: `"(128 đánh giá)" 13px #94A3B8`

Right — Distribution (API: `GET /tours/{id}/rating-stats`):
- 5 rows (5★ → 1★), mỗi row: `flex items-center gap-8`
  - Label: `"5★" 12px #64748B w-20px`
  - Bar: `flex-1 h-6px bg #E2E8F0 radius-full` · Fill: `bg #F59E0B` width proportional
  - Count: `"64" 12px #94A3B8 w-24px text-right`

**Review list** (API: `GET /tours/{id}/ratings?page=1&per_page=3`):
- Hiển thị 3 đánh giá gần nhất
- Mỗi review (`px-24 py-16 border-b #F1F5F9`):
  - Header: `flex justify-between`
    - Left: Avatar `36x36px rounded-full` + Name `14px 600 #1E293B` + Date `12px #94A3B8`
    - Right: Stars + score `13px 600 #1E293B`
  - Comment: `14px #64748B line-height 1.6 mt-8`
  - Images (nếu có): `flex gap-8 mt-8` · Mỗi ảnh: `60x60px radius-8 object-cover border #E2E8F0`
  - Status badge (nếu pending/rejected):
    - "CHỜ DUYỆT": `bg #FEF3C7 text #F59E0B`
    - "ĐÃ TỪ CHỐI": `bg #FEE2E2 text #EF4444`

---

## 3. Right Column — Sidebar

### Card 1 — Thông tin nhanh
`bg white border #E2E8F0 radius-16 p-20 mb-16`

Title: `"Thông tin tour" 14px Inter 600 #1E293B mb-16`

Info rows (`space-y-12, flex justify-between items-start`):
- Label: `13px #94A3B8`
- Value: `13px Inter 500 #1E293B text-right`

| Label | Value |
|-------|-------|
| Mã tour | "TOUR-001" |
| Danh mục | Badge `bg #EFF6FF text #0066CC` "Tham quan" |
| Thời lượng | "1 ngày" |
| Giờ khởi hành | "07:00" |
| Điểm tập trung | "Trước cổng Bà Nà Hills" (max 2 lines) |
| Ngày bắt đầu bán | "01/03/2026" |
| Ngày kết thúc bán | "31/12/2026" |
| Ngày tạo | "15/03/2026 09:30" |
| Cập nhật | "01/04/2026 14:22" |
| Tạo bởi | "Admin Duy Tây" |

---

### Card 2 — Thống kê
`bg white border #E2E8F0 radius-16 p-20 mb-16`

Title: `"Thống kê" 14px Inter 600 #1E293B mb-16`

**Grid 2 cột, gap 12px:**
- Mỗi stat: `bg #F8FAFC border #E2E8F0 radius-10 p-12 text-center`
  - Value: `20px Inter 700 #1E293B`
  - Label: `11px uppercase #94A3B8 mt-2`

| Value | Label |
|-------|-------|
| "428" | "LƯỢT BÁN" |
| "★ 4.8" color `#F59E0B` | "ĐÁNH GIÁ" |
| "5" | "LỊCH CÒN" |
| "2.450" | "LƯỢT XEM" |

---

### Card 3 — Cài đặt hiển thị
`bg white border #E2E8F0 radius-16 p-20 mb-16`

Title: `"Cài đặt hiển thị" 14px Inter 600 #1E293B mb-16`

**Trạng thái** (`flex justify-between items-center mb-12`):
- Label: `"Trạng thái" 14px #1E293B`
- Dropdown badge: `"ĐANG HOẠT ĐỘNG ▾" bg #D1FAE5 text #10B981 radius-8 px-10 py-6 12px 700`
  - Click → dropdown: Đang hoạt động | Tạm dừng | Hết chỗ
  - → `PATCH /admin/tours/{id}/status`

**Toggle Nổi bật** (`flex justify-between items-center py-12 border-t #F1F5F9`):
- Left: `"Tour nổi bật" 14px #1E293B` + `"Hiển thị trong mục nổi bật" 12px #94A3B8`
- Toggle: ON `#0066CC`, OFF `#E2E8F0`, `40x22px`
- → `PATCH /admin/tours/{id}/featured`

**Toggle Hot** (`flex justify-between items-center py-12 border-t #F1F5F9`):
- Left: `"Tour Hot 🔥" 14px #1E293B` + `"Hiển thị trong mục Hot" 12px #94A3B8`
- Toggle: ON `#FF6B35`, OFF `#E2E8F0`
- → `PATCH /admin/tours/{id}/hot`

---

### Card 4 — Thao tác
`bg white border #E2E8F0 radius-16 p-20 mb-16`

Title: `"Thao tác" 14px Inter 600 #1E293B mb-12`

| Button | Style | Action |
|--------|-------|--------|
| Chỉnh sửa tour | `bg #0066CC text white radius-10 py-10 full-width shadow` icon `edit` | `/admin/tours/{id}/edit` |
| Thêm lịch khởi hành | ghost style icon `add` | `/admin/tours/{id}/schedules/create` |
| Xem đánh giá | ghost style icon `star` | `/admin/ratings?tour_id={id}` |
| Nhân bản tour | ghost style icon `content_copy` | Confirm → copy data |
| Xóa tour | `border #FEE2E2 text #EF4444` hover `bg #FEE2E2` icon `delete` | Confirm → `DELETE /admin/tours/{id}` → redirect `/admin/tours` |

Ghost style: `border #E2E8F0 bg white text #64748B radius-10 py-10 full-width 13px 600` hover `border #0066CC text #0066CC`

---

## 4. API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load chi tiết tour | GET | `/tours/{slug}` | Khi mount |
| Load lịch khởi hành | GET | `/tours/{id}/schedules` | Khi mount |
| Load đánh giá | GET | `/tours/{id}/ratings?page=1&per_page=3` | Khi mount |
| Load rating stats | GET | `/tours/{id}/rating-stats` | Khi mount |
| Đổi trạng thái | PATCH | `/admin/tours/{id}/status` | Click dropdown trạng thái |
| Bật/tắt nổi bật | PATCH | `/admin/tours/{id}/featured` | Toggle |
| Bật/tắt hot | PATCH | `/admin/tours/{id}/hot` | Toggle |
| Xóa tour | DELETE | `/admin/tours/{id}` | Confirm dialog |
| Xóa lịch | DELETE | `/admin/tour-schedules/{id}` | Confirm trong bảng lịch |

---

## Validation & States

| Hạng mục | Quy tắc |
|---|---|
| Load detail | Nếu `GET /tours/{slug}` trả 404, hiển thị trạng thái "Tour không tồn tại" và CTA quay lại danh sách |
| Đổi trạng thái tour | `active`, `inactive`, `sold_out`; không cho chuyển `sold_out` nếu vẫn còn lịch `available` còn chỗ mà chưa có xác nhận |
| Xóa tour | Bắt buộc confirm; nếu tour đã có booking thì API nên từ chối hoặc chỉ cho chuyển `inactive` |
| Toggle nổi bật/hot | Optimistic update được phép nhưng phải rollback nếu API lỗi |
| Xóa lịch | Không cho xóa lịch đã có booking; đề xuất chuyển `status=cancelled` thay vì delete cứng |
| Ratings rỗng | Hiển thị "Chưa có đánh giá" và vẫn giữ card rating stats |
| Schedules rỗng | Hiển thị CTA "Thêm lịch khởi hành" nếu user có quyền |
