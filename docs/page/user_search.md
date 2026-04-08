# Màn hình: Tìm kiếm

> Route: `/search`
> Quyền: 🌐 Public — không cần đăng nhập
> Mô tả: Tìm kiếm địa điểm và tour du lịch với full-text search, autocomplete, từ khóa phổ biến và xu hướng.

---

## Layout tổng thể

```
┌─────────────────────────────────────────────────────────────┐
│  HEADER (dùng chung)                                        │
├─────────────────────────────────────────────────────────────┤
│  SEARCH BAR: Input lớn + Select loại + Button Tìm          │
├─────────────────────────────────────────────────────────────┤
│  FILTER BAR: Danh mục · Quận · Giá · Sắp xếp              │
│              Active filter tags                             │
├─────────────────────────────────────────────────────────────┤
│  [Khi chưa nhập] POPULAR & TRENDING                        │
│  - Từ khóa phổ biến                                        │
│  - Xu hướng tìm kiếm                                       │
│                                                             │
│  [Khi đang nhập] AUTOCOMPLETE DROPDOWN                     │
│                                                             │
│  [Khi có kết quả] RESULTS                                  │
│  - Tab: Tất cả · Địa điểm · Tour                           │
│  - Grid kết quả + Pagination                               │
│                                                             │
│  [Khi không có kết quả] EMPTY STATE                        │
├─────────────────────────────────────────────────────────────┤
│  FOOTER (dùng chung)                                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 1. Search Bar

`bg white border-b #E2E8F0 py-24 sticky top-[header-height]`

`flex gap-12 items-center max-w-800px mx-auto`

**Input tìm kiếm** (`flex-1`):
- `border #E2E8F0 radius-12 px-16 py-14 pl-48 16px Inter #1E293B`
- icon `search 20px #94A3B8` absolute left-16
- placeholder "Tìm địa điểm, tour du lịch..."
- focus: `border #0066CC ring rgba(0,102,204,0.15)`
- Khi có text: button `×` clear absolute right-16

**Select "Loại"** (`width 140px`):
- Options: Tất cả · Địa điểm · Tour
- `border #E2E8F0 radius-12 px-14 py-14 14px Inter`

**Button "Tìm kiếm"**:
- `bg #0066CC text white radius-12 px-24 py-14 15px Inter 600`
- icon `search` bên trái
- hover `bg #004999`
- → gọi `GET /search?q=...&type=...`

---

## 2. Autocomplete Dropdown

**Hiển thị khi:** user đang nhập (debounce 300ms), ẩn khi blur hoặc submit

**API: `GET /search/suggestions?q={query}&limit=5`**

`absolute top-full left-0 right-0 bg white border #E2E8F0 radius-12 shadow-modal mt-4 z-50 overflow-hidden`

**Cấu trúc dropdown:**

Section "Địa điểm" (nếu có):
- Label: `"ĐỊA ĐIỂM" 10px uppercase #94A3B8 px-16 py-8 bg #F8FAFC`
- Mỗi item: `flex items-center gap-12 px-16 py-12 hover bg #F8FAFC cursor-pointer`
  - icon `location_on 18px #0066CC`
  - Tên: `14px Inter 500 #1E293B` (highlight phần match với query)
  - Địa chỉ: `12px #94A3B8`

Section "Tour" (nếu có):
- Label: `"TOUR" 10px uppercase #94A3B8 px-16 py-8 bg #F8FAFC`
- Mỗi item: `flex items-center gap-12 px-16 py-12 hover bg #F8FAFC cursor-pointer`
  - icon `tour 18px #FF6B35`
  - Tên: `14px Inter 500 #1E293B`
  - Giá: `12px #94A3B8`

Footer dropdown:
- `px-16 py-10 border-t #F1F5F9 flex items-center gap-8 cursor-pointer hover bg #F8FAFC`
- icon `search 16px #0066CC` + `"Tìm kiếm '[query]'" 13px #0066CC`

---

## 3. Filter Bar

**Hiển thị khi:** có kết quả tìm kiếm

`bg white border-b #E2E8F0 py-16`

`flex gap-12 flex-wrap items-center max-w-1200px mx-auto`

| Filter | Width | Config |
|--------|-------|--------|
| Select Danh mục | `160px` | "Tất cả danh mục" + list từ `GET /categories` |
| Select Quận | `150px` | Tất cả / Hải Châu / Sơn Trà / Ngũ Hành Sơn / Cẩm Lệ / Thanh Khê / Liên Chiểu |
| Select Giá | `140px` | Tất cả / Miễn phí / $ / $$ / $$$ |
| Select Sắp xếp | `160px` | Liên quan nhất / Mới nhất / Đánh giá cao / Phổ biến nhất |
| Button Đặt lại | `auto` | Chỉ hiện khi có filter · hover `text #EF4444` |

**Active filter tags** (`flex gap-8 mt-12`):
- Tag: `bg #EFF6FF text #0066CC border #B3D9FF radius-full px-10 py-4 12px Inter 500`
- Nút `×` xóa từng filter

---

## 4. Trạng thái: Chưa nhập (Default)

**Hiển thị khi:** query rỗng, chưa search

`max-w-800px mx-auto py-32`

### 4.1 Từ khóa phổ biến

**API: `GET /search/popular?limit=10&days=30`**

- Title: "Tìm kiếm phổ biến" — `16px Inter 600 #1E293B mb-16`
- `flex flex-wrap gap-8`:
  - Mỗi keyword: `px-14 py-8 bg #F8FAFC border #E2E8F0 radius-full 13px Inter 500 #64748B cursor-pointer`
    hover `bg #EFF6FF border #B3D9FF text #0066CC`
  - icon `trending_up 14px #94A3B8` bên trái
  - Click → điền vào search input + submit

### 4.2 Xu hướng tìm kiếm

**API: `GET /search/trending?limit=10`**

- Title: "Đang hot 🔥" — `16px Inter 600 #1E293B mb-16 mt-32`
- `flex flex-wrap gap-8`:
  - Mỗi keyword: `px-14 py-8 bg #FFE0D4 border rgba(255,107,53,0.2) radius-full 13px Inter 500 #FF6B35 cursor-pointer`
    hover `bg #FF6B35 text white`
  - icon `local_fire_department 14px #FF6B35` bên trái

### 4.3 Lịch sử tìm kiếm (🔐 Đã đăng nhập)

**API: `GET /user/search-history?limit=5`**

- Title: "Tìm kiếm gần đây" — `16px Inter 600 #1E293B mb-16 mt-32`
- `flex flex-col gap-4`:
  - Mỗi item: `flex justify-between items-center px-14 py-10 bg #F8FAFC radius-10 cursor-pointer`
    hover `bg #EFF6FF`
    - Left: icon `history 16px #94A3B8` + keyword `13px #1E293B`
    - Right: icon `close 14px #94A3B8` hover `#EF4444` → xóa item
  - Click → điền vào search input + submit
- Button "Xóa lịch sử": `12px #EF4444` → `DELETE /user/search-history`

---

## 5. Trạng thái: Có kết quả

**API: `GET /search?q=&type=&category_id=&district=&price_min=&price_max=&sort=&order=&page=&per_page=&session_id=`**

### 5.1 Result Header

`flex justify-between items-center mb-24`

- Left: `"Tìm thấy 48 kết quả cho '[query]'" 16px Inter 600 #1E293B`
- Right: Select "Sắp xếp" (nếu chưa có trong filter bar)

### 5.2 Tab Bar

`flex gap-0 border-b #E2E8F0 mb-24`

| Tab | Style |
|-----|-------|
| Tất cả (48) | Active: `border-b-2 #0066CC text #0066CC 14px 600` |
| Địa điểm (32) | Inactive: `text #64748B 14px 500` hover `text #0066CC` |
| Tour (16) | Inactive |

- Click tab → filter `type=location` hoặc `type=tour`

### 5.3 Result Grid

**Tab "Tất cả" / "Địa điểm":**

`grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-20`

Mỗi location card:
- Thumbnail: `full-width h-180px object-cover radius-t-16`
- Badge loại: `"ĐỊA ĐIỂM" bg #EEF2FF text #6366F1 11px 600 radius-full px-8 py-3 absolute top-12 left-12`
- Button yêu thích: `absolute top-12 right-12` (🔐)
- Body (`p-16`):
  - Tên: `15px Inter 600 #1E293B` — highlight từ khóa match
  - Địa chỉ: `12px #94A3B8` icon `location_on`
  - `flex justify-between mt-8`:
    - Rating: `★ 4.8` `12px #F59E0B`
    - Mức giá: `$` `12px #64748B`
- → navigate `/locations/{slug}`

**Tab "Tour":**

Mỗi tour card:
- Thumbnail: `full-width h-180px object-cover radius-t-16`
- Badge: `"TOUR" bg #EFF6FF text #0066CC 11px 600 radius-full px-8 py-3 absolute top-12 left-12`
- Body (`p-16`):
  - Tên: `15px Inter 600 #1E293B` — highlight từ khóa match
  - `flex items-center gap-8 mt-4`:
    - icon `schedule 14px #94A3B8` + thời lượng `12px #64748B`
  - `flex justify-between mt-8`:
    - Rating: `★ 4.8 (128)` `12px #F59E0B`
    - Giá: "850.000 đ" `14px Inter 700 #0066CC`
- → navigate `/tours/{slug}`

### 5.4 Pagination

`flex justify-center mt-32`

- Prev · 1 · 2 · 3 · ... · Next
- Button: `32x32px border #E2E8F0 radius-8 bg white color #64748B`
- Active: `bg #0066CC text white border #0066CC`

---

## 6. Trạng thái: Không có kết quả

`center py-64 max-w-400px mx-auto text-center`

- SVG icon `search_off 80x80px color #E2E8F0`
- Title: `"Không tìm thấy kết quả nào" 20px Inter 600 #1E293B mt-16`
- Subtitle: `"Thử tìm với từ khóa khác hoặc xem các gợi ý bên dưới" 14px #94A3B8 mt-8`
- Button "Xóa bộ lọc": `border #E2E8F0 bg white text #64748B radius-10 px-20 py-10 mt-16`

**Gợi ý từ khóa phổ biến** (bên dưới empty state):
- Hiển thị lại Section 4.1 (Từ khóa phổ biến)

---

## 7. API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Tìm kiếm | GET | `/search?q=&type=&...` | Submit form / Enter |
| Autocomplete | GET | `/search/suggestions?q=&limit=5` | Nhập text (debounce 300ms) |
| Từ khóa phổ biến | GET | `/search/popular?limit=10&days=30` | Khi mount (query rỗng) |
| Xu hướng | GET | `/search/trending?limit=10` | Khi mount (query rỗng) |
| Lịch sử tìm kiếm (🔐) | GET | `/user/search-history?limit=5` | Khi mount + đã đăng nhập |
| Xóa lịch sử (🔐) | DELETE | `/user/search-history` | Click "Xóa lịch sử" |
| Load danh mục (filter) | GET | `/categories` | Khi mount |

**Query params của `/search`:**

| Param | Mô tả | Nguồn |
|-------|-------|-------|
| `q` | Từ khóa tìm kiếm | Search input |
| `type` | `location` hoặc `tour` | Select loại / Tab |
| `category_id` | ID danh mục | Filter danh mục |
| `district` | Quận/huyện | Filter quận |
| `price_min` | Giá tối thiểu | Filter giá |
| `price_max` | Giá tối đa | Filter giá |
| `sort` | Trường sắp xếp | Select sắp xếp |
| `order` | `asc` hoặc `desc` | Select sắp xếp |
| `page` | Trang hiện tại | Pagination |
| `per_page` | Số kết quả/trang | Mặc định 12 |
| `session_id` | ID phiên (tracking) | Auto-generate |
