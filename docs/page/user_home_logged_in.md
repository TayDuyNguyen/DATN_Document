# Màn hình: Trang chủ (Đã đăng nhập)

> Route: `/`
> Quyền: 🔐 Đã đăng nhập
> Mô tả: Trang chủ với thêm section Gợi ý cá nhân dựa trên lịch sử xem, đặt tour và yêu thích.

---

## Tái sử dụng từ màn Trang chủ (Chưa đăng nhập)

> Xem chi tiết tại `user_home.md`

Giữ nguyên toàn bộ 10 sections:
1. Header
2. Hero Section
3. Stats Bar
4. Danh mục Địa điểm
5. Địa điểm Nổi bật
6. Danh mục Tour
7. Tour Nổi bật
8. Tour Hot
9. Bài viết Blog
10. Footer

---

## Điểm khác biệt khi đã đăng nhập

---

### 1. Header — Thay đổi auth buttons

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

---

### 2. Section mới: Gợi ý cho bạn

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

**Loading state** (khi đang fetch):
- 6 skeleton cards: `bg #E2E8F0 radius-16 h-180px animation pulse`

**Empty state** (nếu chưa có lịch sử):
- Không hiển thị section này
- Hoặc hiển thị với subtitle: `"Hãy khám phá để nhận gợi ý phù hợp"`
  + 6 cards địa điểm/tour phổ biến nhất thay thế

---

### 3. Section Địa điểm Nổi bật — Thêm toggle yêu thích

Khi đã đăng nhập, button yêu thích trên mỗi card địa điểm:
- Đã yêu thích: icon `favorite #EF4444` (filled)
- Chưa yêu thích: icon `favorite_border #94A3B8`
- Click → `POST /user/favorites` hoặc `DELETE /user/favorites/{id}`
- Toast: `"Đã thêm vào yêu thích" bg #D1FAE5 text #10B981` hoặc `"Đã xóa khỏi yêu thích"`

---

### 4. Dropdown Thông báo Mini

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
    - booking: `bg #EFF6FF` icon `shopping_cart #0066CC`
    - rating: `bg #FEF3C7` icon `star #F59E0B`
    - system: `bg #F1F5F9` icon `info #64748B`
  - Right:
    - Title: `13px Inter 600 #1E293B` max 1 line
    - Time: `11px #94A3B8 mt-2`
  - Unread dot: `w-8 h-8 bg #0066CC rounded-full flex-shrink-0 mt-4`

**Footer** (`px-16 py-12 text-center`):
- Link "Xem tất cả thông báo →": `13px #0066CC` → `/notifications`

---

## API Mapping (bổ sung so với Phần 1)

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load gợi ý cá nhân | GET | `/recommendations?limit=6` | Khi mount + đã đăng nhập |
| Load thông báo mini | GET | `/user/notifications?per_page=5` | Click icon thông báo |
| Đánh dấu tất cả đã đọc | PATCH | `/user/notifications/read-all` | Click trong dropdown |
| Toggle yêu thích | POST/DELETE | `/user/favorites` | Click icon yêu thích trên card |
| Đăng xuất | POST | `/auth/logout` | Click "Đăng xuất" trong dropdown |
