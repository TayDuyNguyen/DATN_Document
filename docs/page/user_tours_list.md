# Màn hình: Danh sách Tour

> Route: `/tours`
> Quyền: 🌐 Public — không cần đăng nhập
> Mô tả: Danh sách toàn bộ tour du lịch tại Đà Nẵng với filter theo danh mục, giá, thời lượng và sắp xếp.

---

## Layout tổng thể

```
┌─────────────────────────────────────────────────────────────┐
│  HEADER (dùng chung)                                        │
├─────────────────────────────────────────────────────────────┤
│  PAGE HERO: Tiêu đề + Breadcrumb                           │
├─────────────────────────────────────────────────────────────┤
│  CATEGORY TABS: Tất cả · Tham quan · Ẩm thực · ...        │
├─────────────────────────────────────────────────────────────┤
│  FILTER BAR: Giá · Thời lượng · Ngày · Sắp xếp            │
│              Active filter tags                             │
├──────────────────────────────────┬──────────────────────────┤
│  SIDEBAR (240px)                 │  MAIN CONTENT (flex-1)   │
│  - Danh mục tour (checkbox)      │  - Toolbar: Count + View │
│  - Khoảng giá (range slider)     │  - Grid / List cards     │
│  - Thời lượng (checkbox)         │  - Pagination            │
│  - Ngày khởi hành (date range)   │                          │
│  - Đánh giá (star filter)        │                          │
└──────────────────────────────────┴──────────────────────────┘
│  FOOTER (dùng chung)                                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 1. Page Hero

`bg linear-gradient(135deg, #FF6B35, #FF8F5C) py-48 text-center`

- Breadcrumb: `"Trang chủ / Tour" 13px white/70`
- Title: `"Tour Du lịch Đà Nẵng" 32px Inter 700 white`
- Subtitle: `"48 tour hấp dẫn đang chờ bạn khám phá" 16px white/80 mt-8`

---

## 2. Category Tabs

**API: `GET /tour-categories`**

`bg white border-b #E2E8F0 py-0`

`flex gap-0 overflow-x-auto max-w-1200px mx-auto`

- Tab "Tất cả": Active mặc định
- Mỗi tab: `flex items-center gap-8 px-20 py-16 cursor-pointer border-b-2 border-transparent`
  - Icon danh mục: `20px`
  - Tên: `14px Inter 500 #64748B`
  - Count: `"(12)" 12px #94A3B8`
- Active: `border-b-2 border-#FF6B35 text #FF6B35 font-600`
- Hover: `text #FF6B35`
- Click → filter `tour_category_id=`

---

## 3. Filter Bar (Mobile)

**Chỉ hiển thị trên mobile**

`bg white border-b #E2E8F0 py-12 overflow-x-auto`

`flex gap-8 px-16`

- Pill "Giá ▾" · Pill "Thời lượng ▾" · Pill "Ngày ▾" · Pill "Sắp xếp ▾"
- Button "Bộ lọc" icon `tune` → bottom sheet

**Active filter tags** (`flex gap-8 px-16 pb-12 overflow-x-auto`):
- Tag: `bg #FFE0D4 text #FF6B35 border rgba(255,107,53,0.2) radius-full px-10 py-4 12px Inter 500`
- Nút `×` xóa từng filter

---

## 4. Sidebar (Desktop)

`width 240px flex-shrink-0 sticky top-[header+tabs]`

**Card:** `bg white border #E2E8F0 radius-16 p-20`

### 4.1 Danh mục Tour

- Label: `"DANH MỤC" 11px uppercase #94A3B8 mb-12`
- Checkbox list (`space-y-10`):
  - Mỗi item: `flex items-center justify-between cursor-pointer`
    - Checkbox `16px accent-color #FF6B35`
    - Icon + Tên: `13px Inter 500 #1E293B`
    - Count: `12px #94A3B8` — e.g. "(12)"
  - Checked: label `color #FF6B35 font-600`

### 4.2 Khoảng giá

- Label: `"KHOẢNG GIÁ" 11px uppercase #94A3B8 mb-12 mt-20`
- Range slider dual-handle:
  - Track: `h-4px bg #E2E8F0 radius-full`
  - Fill: `bg #FF6B35`
  - Thumb: `16x16px bg #FF6B35 rounded-full border-2 white shadow`
- `flex justify-between mt-8`:
  - Min: `"0 đ" 12px #64748B`
  - Max: `"5.000.000 đ" 12px #64748B`
- Input range display: `"500.000 đ — 2.000.000 đ" 13px Inter 600 #1E293B text-center mt-8`

### 4.3 Thời lượng

- Label: `"THỜI LƯỢNG" 11px uppercase #94A3B8 mb-12 mt-20`
- Checkbox list:
  - ☐ Nửa ngày (< 4 giờ)
  - ☐ 1 ngày
  - ☐ 2 ngày 1 đêm
  - ☐ 3 ngày 2 đêm
  - ☐ Từ 4 ngày trở lên

### 4.4 Ngày khởi hành

- Label: `"NGÀY KHỞI HÀNH" 11px uppercase #94A3B8 mb-12 mt-20`
- `flex gap-8`:
  - Input "Từ ngày": `flex-1 border #E2E8F0 radius-8 px-10 py-8 12px`
  - Input "Đến ngày": `flex-1 border #E2E8F0 radius-8 px-10 py-8 12px`

### 4.5 Đánh giá

- Label: `"ĐÁNH GIÁ" 11px uppercase #94A3B8 mb-12 mt-20`
- Radio group:
  - ○ Tất cả
  - ○ ★★★★★ 5 sao trở lên
  - ○ ★★★★ 4 sao trở lên
  - ○ ★★★ 3 sao trở lên

### 4.6 Button Đặt lại

`border #E2E8F0 bg white text #64748B radius-10 py-10 full-width mt-20 13px 600`
hover `text #EF4444 border #EF4444`

---

## 5. Main Content

### 5.1 Toolbar

`flex justify-between items-center mb-20`

**Bên trái:**
- `"48 tour" 14px #64748B`

**Bên phải** (`flex items-center gap-12`):
- Select "Sắp xếp":
  - Phổ biến nhất · Đánh giá cao nhất · Giá thấp → cao · Giá cao → thấp · Mới nhất
  - `border #E2E8F0 radius-8 px-12 py-8 13px`
- View toggle (Grid / List):
  - Active: `bg #FFE0D4 border rgba(255,107,53,0.2) color #FF6B35 32x32px radius-8`
  - Inactive: `bg white border #E2E8F0 color #94A3B8`

### 5.2 Grid View

`grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-20`

Mỗi tour card:
- Thumbnail: `full-width h-220px object-cover radius-t-16 relative`
  - Badge nổi bật: `"⭐ NỔI BẬT" absolute top-12 left-12 bg #EFF6FF text #0066CC 11px 700 radius-full px-8 py-3`
  - Badge hot: `"🔥 HOT" absolute top-12 left-12 bg #FF6B35 text white 11px 700 radius-full px-8 py-3`
  - Badge giảm giá (nếu có): `"-15%" absolute top-12 right-12 bg #EF4444 text white 11px 700 radius-full px-8 py-3`
- Body (`p-16`):
  - Danh mục: `11px 600 bg #FFE0D4 text #FF6B35 radius-full px-8 py-2`
  - Tên: `16px Inter 600 #1E293B mt-8` max 2 lines
  - `flex items-center gap-12 mt-8`:
    - icon `schedule 14px #94A3B8` + thời lượng `12px #64748B`
    - icon `group 14px #94A3B8` + "Tối đa 20 người" `12px #64748B`
    - icon `location_on 14px #94A3B8` + điểm đến `12px #64748B`
  - `flex justify-between items-end mt-12 pt-12 border-t #F1F5F9`:
    - Left:
      - Rating: `★ 4.8` `12px #F59E0B` + `"(128)" 11px #94A3B8`
    - Right:
      - Giá gốc (nếu có giảm): `"1.000.000 đ" 12px #94A3B8 line-through`
      - Giá: `"850.000 đ" 16px Inter 700 #FF6B35`
      - `"/ người" 11px #94A3B8`
  - Button "Xem chi tiết" (full width, mt-12):
    `bg #FF6B35 text white radius-10 py-10 14px 600`
    hover `bg #E55A2B`
    → navigate `/tours/{slug}`
- hover: `shadow-card-hover transform translateY(-2px) transition-200ms`

### 5.3 List View

`flex flex-col gap-16`

Mỗi tour card (horizontal):
- `flex gap-16 bg white border #E2E8F0 radius-16 overflow-hidden hover shadow-card-hover`
- Thumbnail: `width 220px h-160px object-cover flex-shrink-0 relative`
  - Badges (same as grid)
- Body (`p-16 flex-1`):
  - `flex items-center gap-8 mb-6`:
    - Danh mục badge
    - Thời lượng: `12px #64748B` icon `schedule`
  - Tên: `18px Inter 600 #1E293B`
  - Mô tả ngắn: `13px #64748B mt-6` max 2 lines
  - `flex items-center gap-16 mt-8`:
    - icon `group 14px #94A3B8` + "Tối đa 20 người" `12px #64748B`
    - icon `location_on 14px #94A3B8` + điểm đến `12px #64748B`
  - `flex justify-between items-center mt-12`:
    - Rating: `★ 4.8 (128)` `13px #F59E0B`
    - `flex items-end gap-8`:
      - Giá gốc (nếu có): `"1.000.000 đ" 12px #94A3B8 line-through`
      - Giá: `"850.000 đ / người" 16px Inter 700 #FF6B35`
      - Button "Đặt ngay →": `bg #FF6B35 text white radius-8 px-16 py-8 13px 600`

### 5.4 Pagination

`flex justify-center items-center gap-8 mt-32`

- Prev · 1 · 2 · 3 · ... · 5 · Next
- Button: `32x32px border #E2E8F0 radius-8 bg white color #64748B`
- Active: `bg #FF6B35 text white border #FF6B35`

---

## 6. Empty State

`center py-64 text-center`

- SVG icon `tour 80px #E2E8F0`
- Title: `"Không tìm thấy tour nào" 20px Inter 600 #1E293B mt-16`
- Subtitle: `"Thử thay đổi bộ lọc để xem thêm kết quả" 14px #94A3B8 mt-8`
- Button "Xóa bộ lọc": `border #E2E8F0 bg white text #64748B radius-10 px-20 py-10 mt-16`

---

## 7. API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load danh sách | GET | `/tours?page=&per_page=12&sort=&order=` | Khi mount, đổi filter |
| Load danh mục (tabs + sidebar) | GET | `/tour-categories` | Khi mount |
| Filter danh mục | GET | `/tours?tour_category_id=` | Click tab / checkbox |
| Filter giá | GET | `/tours?price_min=&price_max=` | Drag range slider |
| Filter thời lượng | GET | `/tours?duration=` | Chọn checkbox |
| Filter ngày | GET | `/tours?available_from=&available_to=` | Chọn date range |
| Sắp xếp | GET | `/tours?sort=&order=` | Chọn select |

**Query params của `/tours`:**

| Param | Mô tả | Giá trị |
|-------|-------|---------|
| `tour_category_id` | ID danh mục tour | number |
| `price_min` | Giá tối thiểu | number |
| `price_max` | Giá tối đa | number |
| `duration` | Thời lượng | string |
| `available_from` | Ngày bắt đầu | ISO date |
| `available_to` | Ngày kết thúc | ISO date |
| `sort` | Trường sắp xếp | `booking_count` \| `avg_rating` \| `price_adult` \| `created_at` |
| `order` | Thứ tự | `asc` \| `desc` |
| `page` | Trang | number |
| `per_page` | Số item/trang | default 12 |
