# Màn hình: Danh sách Bài viết Blog

> Route: `/blog`
> Quyền: 🌐 Public — không cần đăng nhập
> Mô tả: Danh sách bài viết blog du lịch Đà Nẵng với filter theo danh mục và phân trang.

---

## Layout tổng thể

```
┌─────────────────────────────────────────────────────────────┐
│  HEADER (dùng chung)                                        │
├─────────────────────────────────────────────────────────────┤
│  PAGE HERO: Tiêu đề + Breadcrumb                           │
├─────────────────────────────────────────────────────────────┤
│  CATEGORY TABS: Tất cả · Tham quan · Ẩm thực · ...        │
├──────────────────────────────────┬──────────────────────────┤
│  MAIN CONTENT (flex-1)           │  SIDEBAR (300px)         │
│  - Featured post (bài nổi bật)   │  - Danh mục blog         │
│  - Grid bài viết                 │  - Bài viết phổ biến     │
│  - Pagination                    │  - Tags cloud            │
└──────────────────────────────────┴──────────────────────────┘
│  FOOTER (dùng chung)                                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 1. Page Hero

`bg linear-gradient(135deg, #1E293B, #475569) py-48 text-center`

- Breadcrumb: `"Trang chủ / Blog" 13px white/70`
- Title: `"Cẩm nang Du lịch Đà Nẵng" 32px Inter 700 white`
- Subtitle: `"Khám phá những bài viết hữu ích về du lịch Đà Nẵng" 16px white/80 mt-8`

---

## 2. Category Tabs

**API: `GET /blog/categories`**

`bg white border-b #E2E8F0`

`flex gap-0 overflow-x-auto max-w-1200px mx-auto`

- Tab "Tất cả": Active mặc định
- Mỗi tab: `px-20 py-16 cursor-pointer border-b-2 border-transparent 14px Inter 500 #64748B`
- Active: `border-b-2 border-#0066CC text #0066CC font-600`
- Hover: `text #0066CC`
- Click → filter `category_id=`

---

## 3. Main Content

### 3.1 Featured Post (Bài nổi bật)

**Bài đầu tiên trong response** — hiển thị lớn hơn

`mb-32`

`flex gap-24 bg white border #E2E8F0 radius-16 overflow-hidden hover shadow-card-hover`

- Thumbnail: `width 50% h-300px object-cover flex-shrink-0`
- Body (`p-24 flex-1 flex flex-col justify-center`):
  - Danh mục: `11px 600 bg #EFF6FF text #0066CC radius-full px-10 py-4`
  - Tiêu đề: `24px Inter 700 #1E293B mt-12` max 2 lines
  - Excerpt: `14px #64748B mt-8 line-height 1.6` max 3 lines
  - `flex items-center gap-12 mt-16`:
    - Avatar `28x28px rounded-full border #E2E8F0`
    - Tên tác giả: `13px Inter 500 #1E293B`
    - `·` separator
    - Ngày: `13px #94A3B8`
    - `·` separator
    - Lượt xem: icon `visibility 14px #94A3B8` + `"1.2K" 13px #94A3B8`
  - Button "Đọc ngay →": `bg #0066CC text white radius-10 px-20 py-10 14px 600 mt-16 inline-flex`
    → navigate `/blog/{slug}`

### 3.2 Grid Bài viết

**API: `GET /blog?page=1&per_page=9&category_id=`**

`grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-20`

Mỗi blog card:
- Thumbnail: `full-width h-200px object-cover radius-t-16 relative`
  - Danh mục badge: `absolute top-12 left-12 bg white/90 backdrop-blur-sm text #0066CC 11px 600 radius-full px-8 py-3`
- Body (`p-16`):
  - Tiêu đề: `16px Inter 600 #1E293B` max 2 lines
    hover `color #0066CC`
  - Excerpt: `13px #64748B mt-6` max 2 lines
  - `flex items-center justify-between mt-12 pt-12 border-t #F1F5F9`:
    - Left: `flex items-center gap-8`
      - Avatar `24x24px rounded-full border #E2E8F0`
      - Tên: `12px Inter 500 #64748B`
    - Right: `flex items-center gap-12`
      - Ngày: `12px #94A3B8`
      - icon `visibility 13px #94A3B8` + `"856" 12px #94A3B8`
- hover: `shadow-card-hover transform translateY(-2px) transition-200ms`
- → navigate `/blog/{slug}`

### 3.3 Pagination

`flex justify-center items-center gap-8 mt-32`

- Prev · 1 · 2 · 3 · ... · 6 · Next
- Button: `32x32px border #E2E8F0 radius-8 bg white color #64748B`
- Active: `bg #0066CC text white border #0066CC`

---

## 4. Sidebar

`width 300px flex-shrink-0`

### 4.1 Danh mục Blog

**API: `GET /blog/categories`**

**Card:** `bg white border #E2E8F0 radius-16 p-20 mb-16`

- Title: `"Danh mục" 16px Inter 600 #1E293B mb-16`
- List (`space-y-4`):
  - Mỗi item: `flex justify-between items-center px-12 py-10 radius-8 cursor-pointer`
    hover `bg #EFF6FF`
    - Left: `flex items-center gap-8`
      - icon `folder 16px #0066CC`
      - Tên: `13px Inter 500 #1E293B`
    - Right: count `12px #94A3B8 bg #F1F5F9 radius-full px-8 py-2`
  - Active (danh mục đang chọn): `bg #EFF6FF` · tên `color #0066CC font-600`
  - Click → filter `category_id=`

### 4.2 Bài viết phổ biến

**Card:** `bg white border #E2E8F0 radius-16 p-20 mb-16`

- Title: `"Bài viết phổ biến" 16px Inter 600 #1E293B mb-16`
- List 5 bài (`space-y-12`):
  - Mỗi item: `flex gap-12 cursor-pointer`
    hover `opacity-80`
    - Thumbnail: `64x64px radius-8 object-cover flex-shrink-0`
    - Right:
      - Tiêu đề: `13px Inter 600 #1E293B` max 2 lines
      - `flex items-center gap-8 mt-4`:
        - Ngày: `11px #94A3B8`
        - icon `visibility 12px #94A3B8` + views `11px #94A3B8`
    - → navigate `/blog/{slug}`

### 4.3 Tags Cloud

**Card:** `bg white border #E2E8F0 radius-16 p-20`

- Title: `"Tags" 16px Inter 600 #1E293B mb-16`
- `flex flex-wrap gap-8`:
  - Mỗi tag: `px-12 py-6 bg #F8FAFC border #E2E8F0 radius-full 12px Inter 500 #64748B cursor-pointer`
    hover `bg #EFF6FF border #B3D9FF text #0066CC`
  - Click → navigate `/search?q={tag}&type=blog`

---

## 5. Empty State

`center py-64 text-center`

- SVG icon `article 80px #E2E8F0`
- Title: `"Chưa có bài viết nào" 20px Inter 600 #1E293B mt-16`
- Subtitle: `"Thử chọn danh mục khác" 14px #94A3B8 mt-8`
- Button "Xem tất cả": `border #E2E8F0 bg white text #64748B radius-10 px-20 py-10 mt-16`
  → reset filter

---

## 6. API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load bài viết | GET | `/blog?page=1&per_page=9` | Khi mount, đổi trang |
| Load danh mục | GET | `/blog/categories` | Khi mount |
| Filter danh mục | GET | `/blog?category_id=` | Click tab / sidebar |
| Đổi trang | GET | `/blog?page=` | Click pagination |

**Query params của `/blog`:**

| Param | Mô tả | Giá trị |
|-------|-------|---------|
| `category_id` | ID danh mục blog | number |
| `page` | Trang | number |
| `per_page` | Số bài/trang | default 9 |
