# Màn hình: Danh sách Địa điểm

> Route: `/locations`
> Quyền: 🌐 Public — không cần đăng nhập
> Mô tả: Danh sách toàn bộ địa điểm du lịch tại Đà Nẵng với filter theo danh mục, quận, mức giá và sắp xếp.

---

## Layout tổng thể

```
┌─────────────────────────────────────────────────────────────┐
│  HEADER (dùng chung)                                        │
├─────────────────────────────────────────────────────────────┤
│  PAGE HERO: Tiêu đề + Breadcrumb + Mô tả ngắn              │
├─────────────────────────────────────────────────────────────┤
│  FILTER BAR: Danh mục · Quận · Mức giá · Sắp xếp           │
│              Active filter tags                             │
├──────────────────────────────────┬──────────────────────────┤
│  SIDEBAR (240px)                 │  MAIN CONTENT (flex-1)   │
│  - Danh mục (checkbox)           │  - Toolbar: Count + View │
│  - Quận (checkbox)               │  - Grid / List cards     │
│  - Mức giá (radio)               │  - Pagination            │
│  - Đánh giá (star filter)        │                          │
└──────────────────────────────────┴──────────────────────────┘
│  FOOTER (dùng chung)                                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 1. Page Hero

`bg linear-gradient(135deg, #0066CC, #3385D6) py-48 text-center`

- Breadcrumb: `"Trang chủ / Địa điểm" 13px white/70`
- Title: `"Khám phá Địa điểm Đà Nẵng" 32px Inter 700 white`
- Subtitle: `"124 địa điểm du lịch hấp dẫn đang chờ bạn" 16px white/80 mt-8`

---

## 2. Filter Bar (Mobile / Top)

**Chỉ hiển thị trên mobile, ẩn trên desktop (sidebar thay thế)**

`bg white border-b #E2E8F0 py-16 overflow-x-auto`

`flex gap-8 px-16`

- Pill "Tất cả danh mục ▾": dropdown danh mục
- Pill "Quận ▾": dropdown quận
- Pill "Mức giá ▾": dropdown giá
- Pill "Sắp xếp ▾": dropdown sắp xếp
- Button "Bộ lọc" icon `tune`: mở bottom sheet filter đầy đủ

**Active filter tags** (`flex gap-8 px-16 pb-12 overflow-x-auto`):
- Tag: `bg #EFF6FF text #0066CC border #B3D9FF radius-full px-10 py-4 12px Inter 500`
- Nút `×` xóa từng filter

---

## 3. Sidebar (Desktop)

`width 240px flex-shrink-0 sticky top-[header+filter]`

**Card:** `bg white border #E2E8F0 radius-16 p-20`

### 3.1 Danh mục

**API: `GET /categories`**

- Label: `"DANH MỤC" 11px uppercase #94A3B8 mb-12`
- Checkbox list (`space-y-10`):
  - Mỗi item: `flex items-center justify-between cursor-pointer`
    - Left: `flex items-center gap-8`
      - Checkbox `16px accent-color #0066CC`
      - Icon container `24x24px radius-6` bg màu danh mục + icon `14px`
      - Tên: `13px Inter 500 #1E293B`
    - Right: count `12px #94A3B8` — e.g. "(28)"
  - Checked: label `color #0066CC font-600`

### 3.2 Quận/Huyện

**API: `GET /locations/districts`**

- Label: `"QUẬN/HUYỆN" 11px uppercase #94A3B8 mb-12 mt-20`
- Checkbox list:
  - Hải Châu (18) · Sơn Trà (24) · Ngũ Hành Sơn (16) · Cẩm Lệ (12) · Thanh Khê (14) · Liên Chiểu (10)

### 3.3 Mức giá

- Label: `"MỨC GIÁ" 11px uppercase #94A3B8 mb-12 mt-20`
- Radio group (`space-y-8`):
  - ○ Tất cả
  - ○ Miễn phí
  - ○ Bình dân ($)
  - ○ Trung bình ($$)
  - ○ Cao cấp ($$$)
  - Radio: `accent-color #0066CC` · label `13px Inter 500 #1E293B`

### 3.4 Đánh giá

- Label: `"ĐÁNH GIÁ" 11px uppercase #94A3B8 mb-12 mt-20`
- Radio group:
  - ○ Tất cả
  - ○ ★★★★★ 5 sao trở lên
  - ○ ★★★★ 4 sao trở lên
  - ○ ★★★ 3 sao trở lên

### 3.5 Button Đặt lại

`border #E2E8F0 bg white text #64748B radius-10 py-10 full-width mt-20 13px 600`
hover `text #EF4444 border #EF4444`
→ reset tất cả filter

---

## 4. Main Content

### 4.1 Toolbar

`flex justify-between items-center mb-20`

**Bên trái:**
- `"Hiển thị 124 địa điểm" 14px #64748B`
- Khi có filter: `"(đang lọc)" 13px #0066CC`

**Bên phải** (`flex items-center gap-12`):
- Select "Sắp xếp":
  - Phổ biến nhất · Đánh giá cao nhất · Mới nhất · Tên A-Z
  - `border #E2E8F0 radius-8 px-12 py-8 13px`
- View toggle (Grid / List):
  - Active: `bg #EFF6FF border #B3D9FF color #0066CC 32x32px radius-8`
  - Inactive: `bg white border #E2E8F0 color #94A3B8`
  - Icons: `grid_view` | `view_list`

### 4.2 Grid View

`grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-20`

Mỗi location card:
- Thumbnail: `full-width h-200px object-cover radius-t-16`
  - Badge nổi bật (nếu is_featured): `"⭐ NỔI BẬT" absolute top-12 left-12 bg #0066CC text white 11px 700 radius-full px-8 py-3`
  - Button yêu thích: `absolute top-12 right-12 w-32 h-32 bg white/80 rounded-full icon favorite`
    - 🔐 Cần đăng nhập · Filled nếu đã yêu thích
- Body (`p-16`):
  - `flex items-center gap-8 mb-8`:
    - Danh mục badge: `11px 600 bg màu-danh-mục/10 text màu-danh-mục radius-full px-8 py-2`
    - Quận: `11px #94A3B8`
  - Tên: `16px Inter 600 #1E293B` max 1 line ellipsis
  - Địa chỉ: `12px #94A3B8 mt-4` icon `location_on 12px` max 1 line
  - `flex justify-between items-center mt-12 pt-12 border-t #F1F5F9`:
    - Rating: `flex items-center gap-4` · stars `#F59E0B` · `"4.8 (96)" 12px #64748B`
    - Mức giá: `"Miễn phí"` hoặc `"$"` `13px Inter 600 #0066CC`
- hover: `shadow-card-hover transform translateY(-2px) transition-200ms`
- → navigate `/locations/{slug}`

### 4.3 List View

`flex flex-col gap-16`

Mỗi location card (horizontal):
- `flex gap-16 bg white border #E2E8F0 radius-16 overflow-hidden hover shadow-card-hover`
- Thumbnail: `width 200px h-140px object-cover flex-shrink-0`
- Body (`p-16 flex-1`):
  - `flex items-center gap-8 mb-6`:
    - Danh mục badge
    - Quận badge
  - Tên: `17px Inter 600 #1E293B`
  - Địa chỉ: `13px #94A3B8 mt-4` icon `location_on`
  - Mô tả ngắn: `13px #64748B mt-8` max 2 lines
  - `flex justify-between items-center mt-12`:
    - Rating: `★ 4.8 (96)` `13px #F59E0B`
    - `flex items-center gap-12`:
      - Mức giá: `13px Inter 600 #0066CC`
      - Button "Xem chi tiết →": `border #0066CC text #0066CC radius-8 px-14 py-8 13px 600`
        hover `bg #0066CC text white`

### 4.4 Pagination

`flex justify-center items-center gap-8 mt-32`

- Prev · 1 · 2 · 3 · ... · 11 · Next
- Button: `32x32px border #E2E8F0 radius-8 bg white color #64748B`
- Active: `bg #0066CC text white border #0066CC`
- Hover: `border #0066CC color #0066CC`
- Disabled: `opacity-40 cursor-not-allowed`

---

## 5. Empty State

`center py-64 text-center`

- SVG icon `location_off 80x80px color #E2E8F0`
- Title: `"Không tìm thấy địa điểm nào" 20px Inter 600 #1E293B mt-16`
- Subtitle: `"Thử thay đổi bộ lọc để xem thêm kết quả" 14px #94A3B8 mt-8`
- Button "Xóa bộ lọc": `border #E2E8F0 bg white text #64748B radius-10 px-20 py-10 mt-16`

---

## 6. API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load danh sách | GET | `/locations?page=&per_page=12&sort=&order=` | Khi mount, đổi filter, đổi trang |
| Filter danh mục | GET | `/locations?category_id=` | Chọn checkbox danh mục |
| Filter quận | GET | `/locations?district=` | Chọn checkbox quận |
| Filter mức giá | GET | `/locations?price_level=` | Chọn radio mức giá |
| Sắp xếp | GET | `/locations?sort=&order=` | Chọn select sắp xếp |
| Load danh mục (sidebar) | GET | `/categories` | Khi mount |
| Load quận (sidebar) | GET | `/locations/districts` | Khi mount |
| Thêm yêu thích (🔐) | POST | `/user/favorites` | Click icon yêu thích khi chưa lưu |
| Xóa yêu thích (🔐) | DELETE | `/user/favorites` | Click icon yêu thích khi đã lưu |
| Kiểm tra yêu thích (🔐) | GET | `/user/favorites/check?location_id={id}` | Khi render card |

**Query params của `/locations`:**

| Param | Mô tả | Giá trị |
|-------|-------|---------|
| `category_id` | ID danh mục | number |
| `subcategory_id` | ID danh mục con | number |
| `district` | Quận/huyện | string |
| `price_level` | Mức giá | `free` \| `budget` \| `mid` \| `luxury` |
| `sort` | Trường sắp xếp | `view_count` \| `avg_rating` \| `created_at` \| `name` |
| `order` | Thứ tự | `asc` \| `desc` |
| `page` | Trang | number |
| `per_page` | Số item/trang | default 12 |
