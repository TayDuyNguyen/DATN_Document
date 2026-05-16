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
- bg `rgba(255,255,255,0.2)` backdrop-blur(12px), radius 20px, px-16 py-10
- border `1px solid rgba(255,255,255,0.3)`

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

> API trả về tất cả categories, không hỗ trợ `limit`.
> Frontend tự slice lấy 6 cái đầu:
> ```typescript
> const categories = response.data
>   .filter(c => c.status === 'active')
>   .slice(0, 6);
> ```

`py-48 bg #F8FAFC`

- Section title: "Khám phá theo Danh mục" — `24px Inter 700 #1E293B`
- Subtitle: "Tìm địa điểm phù hợp với sở thích của bạn" — `14px #64748B`

**Icon grid** (`grid grid-cols-3 md:grid-cols-6 gap-16 mt-32`):
- Mỗi category card: `flex flex-col items-center gap-8 p-16 bg white radius-24 cursor-pointer`
  - Icon container: `48x48px radius-12` bg màu danh mục
  - Icon/emoji: `24px`
  - Tên: `13px Inter 600 #1E293B text-center`
  - shadow: `0 8px 30px rgba(0,0,0,0.08)`
  - hover: `transform scale-105 transition-200ms`
  - → navigate `/categories/{slug}/locations`

---

## 5. Địa điểm Nổi bật

**API: `GET /locations/featured?limit=8`**

> Hiển thị địa điểm nổi bật (`is_featured=true`).
> Để lọc theo danh mục (Ăn uống, Khách sạn...) dùng:
> ```
> GET /locations?category_id={id}&per_page=8&sort=avg_rating&order=desc
> ```
> hoặc:
> ```
> GET /categories/{slug}/locations?per_page=8
> ```

`py-48 bg white`

- Section header (`flex justify-between items-center mb-24`):
  - Title: "Địa điểm Nổi bật" — `24px Inter 700 #1E293B`
  - Link "Xem tất cả →" — `14px #0066CC` → `/locations`

**Horizontal scroll** (`flex gap-16 overflow-x-auto pb-8`):
- Mỗi location card (`width 280px flex-shrink-0`):
  - Thumbnail: `full-width h-180px object-cover radius-t-24`
  - Badge "NỔI BẬT": `absolute top-12 left-12 bg #0066CD text white 11px 700 radius-full px-8 py-3`
  - Button yêu thích: `absolute top-12 right-12 w-32 h-32 bg white/80 rounded-full` icon `favorite`
    - 🔐 Cần đăng nhập để toggle
  - Body (`p-16`):
    - Tên: `15px Inter 600 #1E293B`
    - Địa chỉ: `12px #94A3B8` icon `location_on`
    - `flex justify-between mt-8`:
      - Rating: `★ 4.8` `12px #F59E0B`
      - Giá: `"900.000 đ"` hoặc `"Miễn phí"` `12px #64748B`
  - shadow: `0 8px 30px rgba(0,0,0,0.08)` radius-b-24
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
  - Thumbnail: `full-width h-200px object-cover radius-t-24`
  - Badge "⭐ NỔI BẬT": `absolute top-12 left-12 bg #EFF6FF text #0066CD 11px 700 radius-full px-8 py-3`
  - Body (`p-16`):
    - Danh mục: `11px 600 bg #EFF6FF text #0066CD radius-full px-8 py-2`
    - Tên tour: `15px Inter 600 #1E293B mt-8` max 2 lines
    - `flex items-center gap-8 mt-8`:
      - icon `schedule 14px #94A3B8` + "1 ngày" `12px #64748B`
      - icon `group 14px #94A3B8` + "20 người" `12px #64748B`
    - `flex justify-between items-center mt-12 pt-12 border-t #F1F5F9`:
      - Rating: `★ 4.8 (128)` `12px #F59E0B`
      - Giá: "850.000 đ" `15px Inter 700 #0066CD`
  - Button "Đặt ngay" (full width, mt-12): `bg #0066CD text white radius-12 py-10 14px 600`
  - shadow: `0 8px 30px rgba(0,0,0,0.08)` radius-b-24
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
  - Thumbnail: `full-width h-180px object-cover radius-t-24`
  - Badge "🔥 HOT": `absolute top-12 left-12 bg #F97316 text white 11px 700 radius-full px-8 py-3`
  - Body (`p-16`):
    - Tên: `15px Inter 600 #1E293B`
    - `flex justify-between mt-8`:
      - Thời lượng: `12px #64748B`
      - Rating: `★ 4.8` `12px #F59E0B`
    - Giá: "850.000 đ / người" `14px Inter 700 #F97316 mt-8`
  - shadow: `0 8px 30px rgba(0,0,0,0.08)` radius-b-24
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
- Col 4: Thông tin liên hệ (planned `GET /config`; hiện dùng fallback hardcode hotline, email, địa chỉ)

**Bottom bar:** `border-t rgba(255,255,255,0.1) pt-24 flex justify-between`
- "© 2026 Đà Nẵng Trip. All rights reserved."
- Links: Chính sách · Điều khoản

---

## API Mapping

| Section | Method | Endpoint | Status | Ghi chú |
|---------|--------|----------|--------|---------|
| Thời tiết | GET | `/weather` | Planned | Chưa có route, ẩn widget hoặc dùng fallback |
| Thống kê | GET | `/statistics` | ✅ 200 | Hoạt động |
| Danh mục địa điểm | GET | `/categories` | ✅ 200 | Hoạt động |
| Địa điểm nổi bật | GET | `/locations/featured?limit=8` | ✅ 200 | Hoạt động |
| Danh mục tour | GET | `/tour-categories` | ✅ 200 | Hoạt động |
| Tour nổi bật | GET | `/tours/featured?limit=8` | ✅ 200 | Hoạt động |
| Tour hot | GET | `/tours/hot?limit=8` | ✅ 200 | Hoạt động |
| Blog mới nhất | GET | `/blog?page=1&per_page=3` | ✅ 200 | Hoạt động |
| Cấu hình | GET | `/config` | Planned | Chưa có route, footer dùng fallback hardcode |
| Gợi ý cá nhân (🔐) | GET | `/recommendations?limit=6` | ⚠️ 500 | Lỗi query tour_id trong views |
| Thêm yêu thích (🔐) | POST | `/user/favorites` | ✅ 200 | Hoạt động |
| Xóa yêu thích (🔐) | DELETE | `/user/favorites` | ✅ 200 | Hoạt động |

---

## Cấu trúc Response thực tế

---

### GET /statistics ✅

```json
{
  "code": 200,
  "data": {
    "total_users": 23,
    "total_locations": 158,
    "total_tours": 35,
    "total_ratings": 571,
    "total_views": 387297,
    "total_blog_posts": 10
  }
}
```

**TypeScript:**
```ts
interface Statistics {
  total_users: number;
  total_locations: number;
  total_tours: number;
  total_ratings: number;
  total_views: number;
  total_blog_posts: number;
}
// Truy cập: response.data
// Stats bar dùng: total_locations, total_tours, total_blog_posts
```

---

### GET /categories ✅

```json
{
  "code": 200,
  "data": [
    {
      "id": 1,
      "name": "Nhà hàng",
      "slug": "nha-hang",
      "icon": null,
      "description": null,
      "image": null,
      "sort_order": 0,
      "status": "active",
      "created_at": "2026-04-09T20:48:09.000000Z",
      "updated_at": "2026-04-09T20:48:09.000000Z",
      "subcategories": []
    }
  ]
}
```

**TypeScript:**
```ts
interface Category {
  id: number;
  name: string;
  slug: string;
  icon: string | null;
  description: string | null;
  image: string | null;
  sort_order: number;
  status: 'active' | 'inactive';
  created_at: string;
  updated_at: string;
  subcategories: SubCategory[];
}
// Truy cập: response.data (mảng trực tiếp)
// Navigate: /categories/{slug}/locations
```

---

### GET /locations/featured?limit=8 ✅

```json
{
  "code": 200,
  "data": [
    {
      "id": 99,
      "name": "Địa điểm Lữ, Kim and Thịnh",
      "slug": "dia-diem-lu-kim-and-thinh-69d60783f239d",
      "category_id": 13,
      "subcategory_id": 13,
      "description": "...",
      "short_description": "...",
      "address": "5 Phố Tiếp",
      "district": "Thanh Khê",
      "ward": "Phường 5",
      "latitude": "16.00288900",
      "longitude": "108.21702400",
      "phone": "...",
      "email": null,
      "website": null,
      "opening_hours": null,
      "price_min": null,
      "price_max": null,
      "price_level": 2,
      "thumbnail": "...",
      "images": [...],
      "video_url": null,
      "status": "active",
      "is_featured": true,
      "view_count": 4216,
      "favorite_count": 200,
      "avg_rating": "4.03",
      "review_count": 89,
      "created_at": "...",
      "updated_at": "..."
    }
  ]
}
```

**TypeScript:**
```ts
interface Location {
  id: number;
  name: string;
  slug: string;
  category_id: number;
  subcategory_id: number | null;
  description: string;
  short_description: string;
  address: string;
  district: string;
  ward: string | null;
  latitude: string;
  longitude: string;
  phone: string | null;
  email: string | null;
  website: string | null;
  opening_hours: string | null;
  price_min: number | null;
  price_max: number | null;
  price_level: number | null;  // 1-4
  thumbnail: string | null;
  images: string[] | null;
  video_url: string | null;
  status: 'active' | 'inactive';
  is_featured: boolean;
  view_count: number;
  favorite_count: number;
  avg_rating: string;   // parse: parseFloat(avg_rating)
  review_count: number;
  created_at: string;
  updated_at: string;
}
// Truy cập: response.data (mảng trực tiếp, KHÔNG phải response.data.data)
```

---

### GET /tour-categories ✅

```json
{
  "code": 200,
  "data": [
    {
      "id": 1,
      "name": "Tour Bà Nà Hills",
      "slug": "tour-ba-na-hills",
      "description": "Các tour thuộc nhóm Tour Bà Nà Hills...",
      "icon": "mountain",
      "sort_order": 0,
      "status": "active",
      "created_at": "2026-04-08T00:45:45.000000Z",
      "updated_at": "2026-04-08T00:45:45.000000Z"
    }
  ]
}
```

**TypeScript:**
```ts
interface TourCategory {
  id: number;
  name: string;
  slug: string;
  description: string;
  icon: string;
  sort_order: number;
  status: 'active' | 'inactive';
  created_at: string;
  updated_at: string;
}
// Truy cập: response.data (mảng trực tiếp)
```

---

### GET /tours/featured?limit=8 ✅

```json
{
  "code": 200,
  "data": [
    {
      "id": 6,
      "name": "Tour Suối Khoáng Nóng Núi Thần Tài",
      "slug": "tour-suoi-khoang-nong-nui-than-tai-69d607acecc9a",
      "tour_category_id": 4,
      "description": "...",
      "short_desc": "Khám phá vẻ đẹp của Đà Nẵng...",
      "itinerary": [
        {"time": "08:00", "activity": "Xe và HDV đón khách tại khách sạn"},
        {"time": "09:00", "activity": "Bắt đầu hành trình tham quan"}
      ],
      "inclusions": null,
      "exclusions": null,
      "price_adult": "500000",   // string
      "price_child": "300000",   // string
      "price_infant": "0",
      "discount_percent": 0,
      "duration": "1 ngày",
      "start_time": "08:00:00",
      "meeting_point": "...",
      "max_people": 20,
      "min_people": 1,
      "available_from": "2026-04-08",
      "available_to": "2026-12-31",
      "thumbnail": "...",
      "images": [...],
      "video_url": null,
      "location_ids": null,
      "status": "active",
      "is_featured": true,
      "is_hot": false,
      "view_count": 0,
      "booking_count": 4,
      "created_by": 1,
      "created_at": "...",
      "updated_at": "..."
    }
  ]
}
```

**TypeScript:**
```ts
interface Tour {
  id: number;
  name: string;
  slug: string;
  tour_category_id: number;
  description: string;
  short_desc: string | null;
  itinerary: Array<{time: string; activity: string}> | null;
  inclusions: string | null;
  exclusions: string | null;
  price_adult: string;    // parse: parseFloat(price_adult)
  price_child: string;
  price_infant: string;
  discount_percent: number;
  duration: string;
  start_time: string | null;
  meeting_point: string | null;
  max_people: number;
  min_people: number;
  available_from: string | null;
  available_to: string | null;
  thumbnail: string | null;
  images: string[] | null;
  video_url: string | null;
  location_ids: number[] | null;
  status: 'active' | 'inactive' | 'sold_out';
  is_featured: boolean;
  is_hot: boolean;
  view_count: number;
  booking_count: number;
  created_by: number | null;
  created_at: string;
  updated_at: string;
}
// Truy cập: response.data (mảng trực tiếp)
// GET /tours/hot trả về cùng cấu trúc
```

---

### GET /blog?page=1&per_page=3 ✅

```json
{
  "code": 200,
  "data": {
    "current_page": 1,
    "data": [
      {
        "id": 8,
        "title": "Top 5 quán cà phê làm việc yên tĩnh tại quận Hải Châu",
        "slug": "top-5-quan-ca-phe-lam-viec-yen-tinh-...",
        "excerpt": "Tenetur quam qui sit in rerum nostrum...",
        "content": "...",
        "featured_image": "...",
        "author_id": 1,
        "view_count": 4822,
        "status": "published",
        "published_at": "2026-04-08T00:45:45.000000Z",
        "created_at": "...",
        "updated_at": "...",
        "author": {
          "id": 1,
          "username": "admin",
          "full_name": "Admin",
          "avatar": null
        },
        "categories": [
          {"id": 1, "name": "Du lịch", "slug": "du-lich"}
        ]
      }
    ],
    "total": 10,
    "per_page": 3,
    "last_page": 4
  }
}
```

**TypeScript:**
```ts
interface BlogPost {
  id: number;
  title: string;
  slug: string;
  excerpt: string | null;
  content: string;
  featured_image: string | null;
  author_id: number;
  view_count: number;
  status: 'published' | 'draft' | 'archived';
  published_at: string | null;
  created_at: string;
  updated_at: string;
  author: { id: number; username: string; full_name: string; avatar: string | null; };
  categories: Array<{ id: number; name: string; slug: string; }>;
}
// Truy cập: response.data.data (mảng), response.data.total
```

---

### GET /weather — Planned

### GET /config — Planned

> Footer cần fallback hardcode thông tin liên hệ cho đến khi backend implement `/config`.

---

## Điểm khác biệt khi đã đăng nhập (🔐)

### Header — Thay đổi auth buttons

**Chưa đăng nhập:**
- Button "Đăng nhập" + Button "Đăng ký"

**Đã đăng nhập:**
- `flex items-center gap-16`
  - Badge thông báo: icon `notifications 22px #64748B` relative
    - Unread dot: `w-8 h-8 bg #EF4444 rounded-full absolute top-0 right-0 pulse`
    - Click → dropdown thông báo mini (5 thông báo gần nhất)
  - Avatar: `36x36px rounded-full border-2 #E2E8F0 object-cover cursor-pointer`
    - Click → dropdown menu:
      - "Hồ sơ của tôi" → `/profile`
      - "Đơn đặt tour" → `/bookings`
      - "Địa điểm yêu thích" → `/favorites`
      - "Thông báo" → `/notifications`
      - Divider
      - "Đăng xuất" → `POST /auth/logout`

### Section mới: Gợi ý cho bạn

**API: `GET /recommendations?limit=6`**

**Vị trí:** Chèn sau Section 4 (Danh mục Địa điểm), trước Section 5 (Địa điểm Nổi bật)

`py-48 bg white`

**Section header** (`flex justify-between items-center mb-24`):
- Left:
  - Title: `"Gợi ý cho bạn" 24px Inter 700 #1E293B`
  - Subtitle: `"Dựa trên lịch sử của bạn" 14px #94A3B8 mt-4`
- Right: Link "Xem thêm →" `14px #0066CC` → `/recommendations`

**Card grid** (`grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-16`):

Mỗi recommendation card (compact):
- `bg white border #E2E8F0 radius-16 overflow-hidden cursor-pointer`
  hover `shadow-card-hover transform translateY(-2px) transition-200ms`
- Thumbnail: `full-width h-120px object-cover`
  - Badge loại: `absolute top-8 left-8`
    - Địa điểm: `"📍" bg white/80 11px radius-full px-6 py-2`
    - Tour: `"🎫" bg white/80 11px radius-full px-6 py-2`
- Body (`p-12`):
  - Tên: `13px Inter 600 #1E293B` max 1 line ellipsis
  - `flex justify-between mt-6`:
    - Rating: `★ 4.8` `11px #F59E0B`
    - Giá/Mức giá: `11px #0066CC`
- → navigate `/locations/{slug}` hoặc `/tours/{slug}`

**Loading state:** 6 skeleton cards `bg #E2E8F0 radius-16 h-180px animation pulse`

**Empty state:** Không hiển thị section hoặc hiển thị với subtitle "Hãy khám phá để nhận gợi ý phù hợp" + 6 cards phổ biến nhất

### Section Địa điểm Nổi bật — Thêm toggle yêu thích

Khi đã đăng nhập, button yêu thích trên mỗi card:
- Đã yêu thích: icon `favorite #EF4444` (filled)
- Chưa yêu thích: icon `favorite_border #94A3B8`
- Click → `POST /user/favorites` hoặc `DELETE /user/favorites`
- Toast: `"Đã thêm vào yêu thích" bg #D1FAE5 text #10B981` hoặc `"Đã xóa khỏi yêu thích"`

### Dropdown Thông báo Mini

**Trigger:** Click icon thông báo trong header

`absolute top-full right-0 bg white border #E2E8F0 radius-16 shadow-modal w-360px z-50`

**Header** (`flex justify-between items-center px-16 py-12 border-b #F1F5F9`):
- `"Thông báo" 14px Inter 600 #1E293B`
- Button "Đánh dấu tất cả đã đọc": `12px #0066CC` → `PATCH /user/notifications/read-all`

**List** (5 thông báo gần nhất, `GET /user/notifications?per_page=5`):
- Mỗi item (`flex gap-12 px-16 py-12 border-b #F1F5F9 cursor-pointer`):
  hover `bg #F8FAFC`
  - Chưa đọc: `bg #EFF6FF`
  - Icon container: `36x36px radius-10 bg màu-loại flex-shrink-0`
  - Right: Title `13px Inter 600 #1E293B` max 1 line + Time `11px #94A3B8 mt-2`
  - Unread dot: `w-8 h-8 bg #0066CC rounded-full`

**Footer** (`px-16 py-12 text-center`):
- Link "Xem tất cả thông báo →": `13px #0066CC` → `/notifications`

### API Mapping (bổ sung khi đã đăng nhập)

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load gợi ý cá nhân | GET | `/recommendations?limit=6` | Khi mount + đã đăng nhập |
| Load thông báo mini | GET | `/user/notifications?per_page=5` | Click icon thông báo |
| Đánh dấu tất cả đã đọc | PATCH | `/user/notifications/read-all` | Click trong dropdown |
| Thêm yêu thích | POST | `/user/favorites` | Click icon yêu thích |
| Xóa yêu thích | DELETE | `/user/favorites` | Click icon yêu thích (đã lưu) |
| Đăng xuất | POST | `/auth/logout` | Click "Đăng xuất" |
