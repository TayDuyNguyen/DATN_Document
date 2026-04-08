# Màn hình: Chi tiết Địa điểm

> Route: `/locations/{slug}`
> Quyền: 🌐 Public — không cần đăng nhập
> Mô tả: Xem đầy đủ thông tin địa điểm — ảnh, mô tả, bản đồ, tags, tiện ích, đánh giá và địa điểm lân cận.

---

## Layout tổng thể

```
┌─────────────────────────────────────────────────────────────┐
│  HEADER (dùng chung)                                        │
├─────────────────────────────────────────────────────────────┤
│  BREADCRUMB: Trang chủ / Địa điểm / Tên địa điểm           │
├─────────────────────────────────────────────────────────────┤
│  IMAGE GALLERY: Ảnh chính + Grid ảnh phụ                   │
├──────────────────────────────────┬──────────────────────────┤
│  LEFT COLUMN (flex-1)            │  RIGHT COLUMN (360px)    │
│                                  │  sticky top-24           │
│  - Tên + Badges + Actions        │  Card: Thông tin nhanh   │
│  - Thông tin cơ bản              │  - Giờ mở cửa            │
│  - Mô tả                         │  - Liên hệ               │
│  - Tags & Tiện ích               │  - Bản đồ mini           │
│  - Đánh giá                      │  - Button Yêu thích      │
│                                  │  - Button Chia sẻ        │
├─────────────────────────────────────────────────────────────┤
│  SECTION: Địa điểm lân cận                                  │
├─────────────────────────────────────────────────────────────┤
│  FOOTER (dùng chung)                                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 1. Breadcrumb

`py-12 border-b #E2E8F0`

`"Trang chủ / Địa điểm / Bãi biển Mỹ Khê" 13px #94A3B8`
- Mỗi phần là link hover `text #0066CC`
- Phần cuối: `text #1E293B font-500` (không phải link)

---

## 2. Image Gallery

**API: `GET /locations/{id}/images`**

`mb-32`

**Layout desktop:**
```
┌──────────────────────┬──────────┬──────────┐
│                      │  Ảnh 2   │  Ảnh 3   │
│      Ảnh chính       ├──────────┼──────────┤
│      (60% width)     │  Ảnh 4   │  Ảnh 5   │
│                      │          │ +X ảnh   │
└──────────────────────┴──────────┴──────────┘
```

- Ảnh chính: `h-400px object-cover radius-l-16`
- Ảnh phụ: `h-196px object-cover` (2 hàng × 2 cột)
- Ảnh cuối: overlay `bg rgba(0,0,0,0.5)` + text `"+5 ảnh" 16px white 600`
- Click bất kỳ ảnh → mở lightbox fullscreen

**Lightbox:**
- Backdrop `rgba(0,0,0,0.9)`
- Ảnh lớn center + Prev/Next arrows
- Thumbnail strip bên dưới
- Button đóng `×` top-right

---

## 3. Left Column

### 3.1 Tên + Badges + Actions

`flex justify-between items-start mb-20`

**Bên trái:**
- Tên: `28px Inter 700 #1E293B letter-spacing -0.3px`
- `flex items-center gap-8 mt-8`:
  - Badge danh mục: `bg màu-danh-mục/10 text màu-danh-mục 12px 600 radius-full px-10 py-4`
  - Badge quận: `bg #F1F5F9 text #64748B 12px 500 radius-full px-10 py-4`
  - Badge mức giá: `"Miễn phí"` hoặc `"$"` `12px 600 #0066CC`

**Bên phải** (`flex gap-8`):
- Button Yêu thích:
  - Chưa đăng nhập: icon `favorite_border` → redirect `/login`
  - Đã đăng nhập, chưa thích: icon `favorite_border #94A3B8` → `POST /user/favorites`
  - Đã thích: icon `favorite #EF4444` → `DELETE /user/favorites/{id}`
  - Style: `40x40px border #E2E8F0 radius-full bg white`
- Button Chia sẻ: icon `share #64748B` same style → Web Share API

### 3.2 Thông tin cơ bản

`flex flex-wrap gap-20 py-20 border-y #F1F5F9 mb-24`

| Icon | Label | Value |
|------|-------|-------|
| `location_on #0066CC` | Địa chỉ | Full address |
| `schedule #10B981` | Giờ mở cửa | "8:00 - 22:00" hoặc "Mở cửa 24/7" |
| `phone #F59E0B` | Điện thoại | Link `tel:` |
| `language #6366F1` | Website | Link truncate |
| `star #F59E0B` | Đánh giá | "4.8 · 96 đánh giá" |

- Mỗi item: `flex items-center gap-8`
  - Icon: `20px`
  - Value: `14px Inter 500 #1E293B`

### 3.3 Mô tả

`mb-24`

- Title: `"Giới thiệu" 18px Inter 600 #1E293B mb-12`
- Text: `15px Inter 400 #1E293B line-height 1.7`
- Nếu dài: hiện 4 dòng + Button "Xem thêm ▾" `13px #0066CC`
  → expand inline

### 3.4 Tags & Tiện ích

`mb-24`

**Tags:**
- Title: `"Tags" 16px Inter 600 #1E293B mb-12`
- `flex flex-wrap gap-8`:
  - Mỗi tag: `px-12 py-6 bg #F8FAFC border #E2E8F0 radius-full 13px Inter 500 #64748B`
  - hover `bg #EFF6FF border #B3D9FF text #0066CC cursor-pointer`
  - Click → navigate `/search?q={tag}`

**Tiện ích:**
- Title: `"Tiện ích" 16px Inter 600 #1E293B mb-12 mt-20`
- `grid grid-cols-2 md:grid-cols-3 gap-8`:
  - Mỗi amenity: `flex items-center gap-8 px-12 py-10 bg #F8FAFC border #E2E8F0 radius-10`
    - Icon `18px #0066CC`
    - Tên: `13px Inter 500 #1E293B`

### 3.5 Đánh giá

**API: `GET /locations/{id}/ratings?page=1&per_page=5`**
**API: `GET /locations/{id}/rating-stats`**

`mb-24`

**Rating Overview:**
`flex gap-32 py-24 bg #F8FAFC radius-16 px-24 mb-24`

Left — Big score:
- Score: `"4.8" 48px Inter 700 #1E293B`
- Stars: 5 icons `star 20px #F59E0B`
- Sub: `"96 đánh giá" 13px #94A3B8`

Right — Distribution:
- 5 rows (5★ → 1★): `flex items-center gap-8`
  - Label: `"5★" 12px #64748B w-20px`
  - Bar: `flex-1 h-6px bg #E2E8F0 radius-full` · fill `bg #F59E0B` proportional
  - Count: `"52" 12px #94A3B8 w-24px text-right`

**Button Viết đánh giá:**
- Chưa đăng nhập: `border #0066CC text #0066CC radius-10 px-20 py-10 14px 600 mb-20`
  → redirect `/login?redirect=/locations/{slug}`
- Đã đăng nhập + chưa đánh giá: same style → mở modal viết đánh giá
- Đã đánh giá: `border #E2E8F0 text #94A3B8 cursor-not-allowed` "Bạn đã đánh giá"

**Review List:**
- Mỗi review (`py-20 border-b #F1F5F9`):
  - Header: `flex justify-between items-start`
    - Left: Avatar `40x40px rounded-full` + Name `14px 600 #1E293B` + Date `12px #94A3B8`
    - Right: Stars `14px #F59E0B` + score `13px 600 #1E293B`
  - Comment: `14px #64748B line-height 1.6 mt-8`
  - Images (nếu có): `flex gap-8 mt-8` · `60x60px radius-8 object-cover`
  - Button "Hữu ích (12)": `flex items-center gap-4 mt-8 text-12 #94A3B8 cursor-pointer`
    hover `text #0066CC` → `POST /ratings/{id}/helpful` (🔐)

**Pagination đánh giá:**
`flex justify-center mt-16`
- Prev · 1 · 2 · 3 · Next (compact style)

---

## 4. Right Column (Sidebar sticky)

**Card:** `bg white border #E2E8F0 radius-16 p-20 sticky top-24`

### 4.1 Thông tin nhanh

`space-y-14`

| Icon | Label | Value |
|------|-------|-------|
| `location_on #0066CC` | Địa chỉ | Full address, 2 lines |
| `schedule #10B981` | Giờ mở cửa | "8:00 - 22:00" |
| `phone #F59E0B` | Điện thoại | Link `tel:` color `#0066CC` |
| `email #6366F1` | Email | Link `mailto:` color `#0066CC` |
| `language #EC4899` | Website | Link truncate color `#0066CC` |

### 4.2 Bản đồ mini

`mt-16 h-180px bg #F1F5F9 radius-12 overflow-hidden`

- iframe Google Maps với marker tại tọa độ
- Button "Xem bản đồ lớn hơn": `flex items-center gap-4 mt-8 text-13 #0066CC`
  icon `open_in_new` → mở Google Maps tab mới

### 4.3 Actions

`mt-16 space-y-8`

- Button "Yêu thích":
  - Chưa thích: `border #E2E8F0 bg white text #64748B radius-10 py-10 full-width` icon `favorite_border`
  - Đã thích: `bg #FEE2E2 border #EF4444 text #EF4444 radius-10 py-10 full-width` icon `favorite`
  - 🔐 Cần đăng nhập

- Button "Chia sẻ":
  `border #E2E8F0 bg white text #64748B radius-10 py-10 full-width` icon `share`
  → Web Share API

- Button "Chỉ đường":
  `bg #0066CC text white radius-10 py-10 full-width 14px 600` icon `directions`
  → mở Google Maps directions

---

## 5. Địa điểm Lân cận

**API: `GET /locations/{id}/nearby` (limit 6)**

`py-48 bg #F8FAFC`

- Title: `"Địa điểm lân cận" 22px Inter 700 #1E293B mb-24`

`grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-16`

Mỗi nearby card (compact):
- Thumbnail: `full-width h-120px object-cover radius-t-12`
- Body (`p-12`):
  - Tên: `13px Inter 600 #1E293B` max 1 line
  - Khoảng cách: `11px #94A3B8` — e.g. "1.2 km"
  - Rating: `★ 4.7` `11px #F59E0B`
- → navigate `/locations/{slug}`

---

## 6. Modal Viết Đánh giá (🔐)

**Trigger:** Click "Viết đánh giá"
**API:** `GET /ratings/check` → `POST /ratings`

`Modal center, backdrop rgba(0,0,0,0.5), w-500px`

- Header: `"Viết đánh giá" 18px Inter 600 #1E293B` + button `×`
- Stars selector: 5 stars lớn `32px` clickable · hover fill `#F59E0B`
- Textarea: `rows-4 border #E2E8F0 radius-10 px-14 py-12 14px` placeholder "Chia sẻ trải nghiệm của bạn..."
- Upload ảnh: `border dashed #E2E8F0 radius-10 p-16 text-center` (max 5 ảnh)
  → `POST /upload/images`
- Footer: "Hủy" (ghost) + "Gửi đánh giá" `bg #0066CC text white radius-10 px-20 py-10`

---

## 7. API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load chi tiết | GET | `/locations/{slug}` | Khi mount |
| Load ảnh | GET | `/locations/{id}/images` | Khi mount |
| Load đánh giá | GET | `/locations/{id}/ratings?page=1&per_page=5` | Khi mount |
| Load rating stats | GET | `/locations/{id}/rating-stats` | Khi mount |
| Load địa điểm lân cận | GET | `/locations/{id}/nearby` | Khi mount |
| Ghi nhận lượt xem | POST | `/locations/{id}/view` | Khi mount (1 lần) |
| Kiểm tra đã đánh giá (🔐) | GET | `/ratings/check?location_id={id}` | Khi mount + đã đăng nhập |
| Gửi đánh giá (🔐) | POST | `/ratings` | Submit modal |
| Toggle yêu thích (🔐) | POST/DELETE | `/user/favorites` | Click button yêu thích |
| Đánh dấu hữu ích (🔐) | POST | `/ratings/{id}/helpful` | Click "Hữu ích" |
| Upload ảnh đánh giá (🔐) | POST | `/upload/images` | Chọn ảnh trong modal |
