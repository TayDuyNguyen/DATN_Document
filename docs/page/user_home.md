# Màn hình: Trang chủ

> Route: `/`
> Quyền: 🌐 Public — không cần đăng nhập
> Mô tả: Landing page tổng hợp — giới thiệu địa điểm nổi bật, tour nổi bật, tour hot, blog mới nhất, thống kê và thời tiết Đà Nẵng.

---

## Layout tổng thể

```
┌─────────────────────────────────────────────────────────────┐
│  HEADER: Logo + Nav + Search bar + [Đăng nhập] [Đăng ký]   │
│          (hoặc Avatar + Thông báo nếu đã đăng nhập)        │
├─────────────────────────────────────────────────────────────┤
│  HERO SECTION: Banner + Search lớn + Thời tiết             │
├─────────────────────────────────────────────────────────────┤
│  STATS BAR: Tổng địa điểm · Tổng tour · Tổng bài viết      │
├─────────────────────────────────────────────────────────────┤
│  SECTION: Danh mục địa điểm (icon grid)                    │
├─────────────────────────────────────────────────────────────┤
│  SECTION: Địa điểm nổi bật (horizontal scroll)             │
├─────────────────────────────────────────────────────────────┤
│  SECTION: Danh mục tour (tab filter)                       │
├─────────────────────────────────────────────────────────────┤
│  SECTION: Tour nổi bật (card grid)                         │
├─────────────────────────────────────────────────────────────┤
│  SECTION: Tour Hot 🔥 (horizontal scroll)                  │
├─────────────────────────────────────────────────────────────┤
│  SECTION: Bài viết blog mới nhất                           │
├─────────────────────────────────────────────────────────────┤
│  FOOTER: Thông tin liên hệ + Links + Copyright             │
└─────────────────────────────────────────────────────────────┘
```

---

## 1. Header

**Sticky top, bg white, shadow khi scroll**

- Logo "Đà Nẵng Trip" bên trái
- Navigation: Trang chủ · Địa điểm · Tour · Blog · Liên hệ
- Search bar mini (icon search + placeholder "Tìm kiếm...")
  → click mở trang `/search`
- Bên phải:
  - Chưa đăng nhập: Button "Đăng nhập" + Button "Đăng ký"
  - Đã đăng nhập: Avatar + Badge thông báo chưa đọc + Dropdown menu

---

## 2. Hero Section

**Full-width, height 500px, background ảnh Đà Nẵng**

- Overlay gradient `rgba(0,0,0,0.4)`
- Tiêu đề lớn: "Khám phá Đà Nẵng" — 48px bold white
- Subtitle: "Tìm kiếm địa điểm và tour du lịch tuyệt vời" — 18px white
- Search box lớn (flex row):
  - Input "Bạn muốn đi đâu?" — flex-1
  - Select "Loại" (Địa điểm / Tour)
  - Button "Tìm kiếm" → navigate `/search?q=...`

**Widget thời tiết** (absolute bottom-right của hero):
- API: `GET /weather`
- Hiển thị: icon thời tiết + nhiệt độ + mô tả
- e.g. "☀️ 32°C · Nắng đẹp"
- bg `rgba(255,255,255,0.15)` backdrop-blur, radius 12px, px-16 py-10

---

## 3. Stats Bar

**API: `GET /statistics`**

`flex justify-center gap-48 py-24 bg white border-b #E2E8F0`

| Stat | Icon | Value | Label |
|------|------|-------|-------|
| Địa điểm | `location_on` | `124+` | "Địa điểm" |
| Tour | `tour` | `48+` | "Tour du lịch" |
| Bài viết | `article` | `86+` | "Bài viết" |

- Mỗi item: `flex items-center gap-8`
- Value: `28px Inter 700 #0066CC`
- Label: `14px #64748B`

---

## 4. Danh mục Địa điểm

**API: `GET /categories`**

`py-48 bg #F8FAFC`

- Section title: "Khám phá theo Danh mục" — `24px Inter 700 #1E293B`
- Subtitle: "Tìm địa điểm phù hợp với sở thích của bạn" — `14px #64748B`

**Icon grid** (`grid grid-cols-3 md:grid-cols-6 gap-16 mt-32`):
- Mỗi category card: `flex flex-col items-center gap-8 p-16 bg white radius-16 border #E2E8F0 cursor-pointer`
  - Icon container: `48x48px radius-12` bg màu danh mục
  - Icon/emoji: `24px`
  - Tên: `13px Inter 600 #1E293B text-center`
  - hover: `shadow-card-hover transform scale-105 transition-200ms`
  - → navigate `/categories/{slug}/locations`

---

## 5. Địa điểm Nổi bật

**API: `GET /locations/featured?limit=8`**

`py-48 bg white`

- Section header (`flex justify-between items-center mb-24`):
  - Title: "Địa điểm Nổi bật" — `24px Inter 700 #1E293B`
  - Link "Xem tất cả →" — `14px #0066CC` → `/locations`

**Horizontal scroll** (`flex gap-16 overflow-x-auto pb-8`):
- Mỗi location card (`width 280px flex-shrink-0`):
  - Thumbnail: `full-width h-180px object-cover radius-t-16`
  - Badge "NỔI BẬT": `absolute top-12 left-12 bg #0066CC text white 11px 700 radius-full px-8 py-3`
  - Button yêu thích: `absolute top-12 right-12 w-32 h-32 bg white/80 rounded-full` icon `favorite`
    - 🔐 Cần đăng nhập để toggle
  - Body (`p-16`):
    - Tên: `15px Inter 600 #1E293B`
    - Địa chỉ: `12px #94A3B8` icon `location_on`
    - `flex justify-between mt-8`:
      - Rating: `★ 4.8` `12px #F59E0B`
      - Mức giá: `$` hoặc `Miễn phí` `12px #64748B`
  - → navigate `/locations/{slug}`

---

## 6. Danh mục Tour

**API: `GET /tour-categories`**

`py-32 bg #F8FAFC`

- Section title: "Danh mục Tour" — `20px Inter 700 #1E293B`

**Tab pills** (`flex gap-8 overflow-x-auto`):
- Mỗi tab: `px-16 py-8 radius-full 13px Inter 600 cursor-pointer`
- Active: `bg #0066CC text white`
- Inactive: `bg white border #E2E8F0 text #64748B` hover `border #0066CC text #0066CC`
- Click → filter tour section bên dưới hoặc navigate `/tour-categories/{slug}/tours`

---

## 7. Tour Nổi bật

**API: `GET /tours/featured?limit=8`**

`py-48 bg #F8FAFC`

- Section header (`flex justify-between items-center mb-24`):
  - Title: "Tour Nổi bật" — `24px Inter 700 #1E293B`
  - Link "Xem tất cả →" → `/tours`

**Card grid** (`grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-20`):
- Mỗi tour card:
  - Thumbnail: `full-width h-200px object-cover radius-t-16`
  - Badge "⭐ NỔI BẬT": `absolute top-12 left-12 bg #EFF6FF text #0066CC 11px 700 radius-full px-8 py-3`
  - Body (`p-16`):
    - Danh mục: `11px 600 bg #EFF6FF text #0066CC radius-full px-8 py-2`
    - Tên tour: `15px Inter 600 #1E293B mt-8` max 2 lines
    - `flex items-center gap-8 mt-8`:
      - icon `schedule 14px #94A3B8` + "1 ngày" `12px #64748B`
      - icon `group 14px #94A3B8` + "20 người" `12px #64748B`
    - `flex justify-between items-center mt-12 pt-12 border-t #F1F5F9`:
      - Rating: `★ 4.8 (128)` `12px #F59E0B`
      - Giá: "850.000 đ" `15px Inter 700 #0066CC`
  - Button "Đặt ngay" (full width, mt-12): `bg #0066CC text white radius-10 py-10 14px 600`
    → navigate `/tours/{slug}`

---

## 8. Tour Hot 🔥

**API: `GET /tours/hot?limit=8`**

`py-48 bg white`

- Section header:
  - Title: "Tour Hot 🔥" — `24px Inter 700 #1E293B`
  - Subtitle: "Được đặt nhiều nhất tuần này" — `14px #64748B`
  - Link "Xem tất cả →" → `/tours?type=hot`

**Horizontal scroll** (`flex gap-16 overflow-x-auto pb-8`):
- Mỗi tour card (`width 300px flex-shrink-0`):
  - Thumbnail: `full-width h-180px object-cover radius-t-16`
  - Badge "🔥 HOT": `absolute top-12 left-12 bg #FF6B35 text white 11px 700 radius-full px-8 py-3`
  - Body (`p-16`):
    - Tên: `15px Inter 600 #1E293B`
    - `flex justify-between mt-8`:
      - Thời lượng: `12px #64748B`
      - Rating: `★ 4.8` `12px #F59E0B`
    - Giá: "850.000 đ / người" `14px Inter 700 #FF6B35 mt-8`
  - → navigate `/tours/{slug}`

---

## 9. Bài viết Blog mới nhất

**API: `GET /blog?page=1&per_page=3`**

`py-48 bg #F8FAFC`

- Section header:
  - Title: "Cẩm nang Du lịch" — `24px Inter 700 #1E293B`
  - Link "Xem tất cả →" → `/blog`

**Card grid** (`grid grid-cols-1 md:grid-cols-3 gap-20`):
- Mỗi blog card:
  - Featured image: `full-width h-200px object-cover radius-t-16`
  - Body (`p-16`):
    - Danh mục: `11px 600 bg #EFF6FF text #0066CC radius-full px-8 py-2`
    - Tiêu đề: `16px Inter 600 #1E293B mt-8` max 2 lines
    - Excerpt: `13px #64748B mt-8` max 2 lines
    - `flex justify-between items-center mt-12 pt-12 border-t #F1F5F9`:
      - Tác giả: Avatar `20x20px` + Name `12px #64748B`
      - Ngày: `12px #94A3B8`
  - → navigate `/blog/{slug}`

---

## 10. Footer

`bg #1E293B text white py-48`

**Grid 4 cột:**
- Col 1: Logo + Mô tả ngắn + Social links
- Col 2: Khám phá (links: Địa điểm · Tour · Blog)
- Col 3: Hỗ trợ (links: Liên hệ · FAQ · Điều khoản)
- Col 4: Thông tin liên hệ (từ `GET /config`: hotline, email, địa chỉ)

**Bottom bar:** `border-t rgba(255,255,255,0.1) pt-24 flex justify-between`
- "© 2026 Đà Nẵng Trip. All rights reserved."
- Links: Chính sách · Điều khoản

---

## API Mapping

| Section | Method | Endpoint | Ghi chú |
|---------|--------|----------|---------|
| Thời tiết | GET | `/weather` | Widget hero |
| Thống kê | GET | `/statistics` | Stats bar |
| Danh mục địa điểm | GET | `/categories` | Icon grid |
| Địa điểm nổi bật | GET | `/locations/featured?limit=8` | Horizontal scroll |
| Danh mục tour | GET | `/tour-categories` | Tab pills |
| Tour nổi bật | GET | `/tours/featured?limit=8` | Card grid |
| Tour hot | GET | `/tours/hot?limit=8` | Horizontal scroll |
| Blog mới nhất | GET | `/blog?page=1&per_page=3` | Card grid |
| Cấu hình | GET | `/config` | Footer info |
| Gợi ý cá nhân (🔐) | GET | `/recommendations?limit=6` | Chỉ khi đã đăng nhập |
| Toggle yêu thích (🔐) | POST/DELETE | `/user/favorites` | Inline trên card địa điểm |
