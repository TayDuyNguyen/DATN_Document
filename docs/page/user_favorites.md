# Màn hình: Địa điểm Yêu thích

> Route: `/favorites`
> Quyền: 🔐 Cần đăng nhập
> Mô tả: Danh sách địa điểm đã lưu yêu thích với tùy chọn xóa và điều hướng đến chi tiết.

---

## Tái sử dụng từ màn Hồ sơ cá nhân

> Xem chi tiết layout tại `user_profile.md`

Giữ nguyên: Header · Breadcrumb · Sidebar (item "Địa điểm yêu thích" active) · Footer

---

## Main Content

### 1. Page Header

`flex justify-between items-center mb-24`

- Title: `"Địa điểm yêu thích" 20px Inter 700 #1E293B`
- Count: `"8 địa điểm" 14px #94A3B8`

### 2. View Toggle + Sort

`flex justify-between items-center mb-20`

**Bên trái:** View toggle (Grid / List)
- Active: `bg #EFF6FF border #B3D9FF color #0066CC 32x32px radius-8`
- Inactive: `bg white border #E2E8F0 color #94A3B8`

**Bên phải:** Select "Sắp xếp"
- Mới thêm nhất · Cũ nhất · Tên A-Z · Đánh giá cao nhất
- `border #E2E8F0 radius-8 px-12 py-8 13px`

### 3. Grid View

**API: `GET /user/favorites?page=1&per_page=12`**

`grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-20`

Mỗi favorite card:
- Thumbnail: `full-width h-200px object-cover radius-t-16 relative`
  - Button xóa yêu thích: `absolute top-12 right-12 w-36 h-36 bg white/90 rounded-full flex items-center justify-center`
    icon `favorite #EF4444` (filled)
    hover: `bg #FEE2E2` · icon scale 1.1
    Click → confirm xóa → `DELETE /user/favorites/{location_id}`
- Body (`p-16`):
  - `flex items-center gap-8 mb-8`:
    - Danh mục badge
    - Quận: `11px #94A3B8`
  - Tên: `16px Inter 600 #1E293B` max 1 line
  - Địa chỉ: `12px #94A3B8 mt-4` icon `location_on 12px`
  - `flex justify-between items-center mt-12 pt-12 border-t #F1F5F9`:
    - Rating: `★ 4.8 (96)` `12px #F59E0B`
    - Mức giá: `"Miễn phí"` hoặc `"$"` `13px #0066CC`
  - Button "Xem chi tiết" (full width, mt-12):
    `border #0066CC text #0066CC radius-10 py-10 14px 600`
    hover `bg #0066CC text white`
    → `/locations/{slug}`
- hover: `shadow-card-hover transform translateY(-2px) transition-200ms`

### 4. List View

`flex flex-col gap-12`

Mỗi card (horizontal):
- `flex gap-16 bg white border #E2E8F0 radius-16 overflow-hidden hover shadow-card`
- Thumbnail: `width 160px h-120px object-cover flex-shrink-0`
- Body (`p-16 flex-1`):
  - `flex justify-between items-start`:
    - Left: Tên `16px Inter 600 #1E293B`
    - Right: Button xóa icon `favorite #EF4444 20px` hover `scale-110`
  - Địa chỉ: `12px #94A3B8 mt-4` icon `location_on`
  - `flex items-center gap-16 mt-8`:
    - Rating: `★ 4.8` `12px #F59E0B`
    - Mức giá: `12px #0066CC`
    - Danh mục badge
  - Button "Xem chi tiết →": `13px #0066CC mt-8` hover underline

### 5. Pagination

`flex justify-center mt-24`
- Prev · 1 · 2 · Next

### 6. Empty State

`center py-64 text-center`

- SVG icon `favorite_border 80px #E2E8F0`
- Title: `"Chưa có địa điểm yêu thích" 18px Inter 600 #1E293B mt-16`
- Subtitle: `"Hãy khám phá và lưu những địa điểm bạn thích!" 14px #94A3B8 mt-8`
- Button "Khám phá Địa điểm": `bg #0066CC text white radius-10 px-24 py-12 14px 600 mt-16`
  → `/locations`

### 7. Confirm Xóa yêu thích

**Inline toast** (không dùng modal — UX nhanh hơn):

Khi click icon xóa:
- Hiện toast bottom: `bg #1E293B text white radius-10 px-16 py-12 flex items-center gap-12`
  - Text: `"Đã xóa khỏi yêu thích" 13px white`
  - Button "Hoàn tác": `13px #0066CC` (trong 5 giây)
    → `POST /user/favorites` (thêm lại)
  - Auto-dismiss sau 5 giây
- Card bị xóa khỏi grid với animation `opacity 0 → scale 0.8 → remove`

---

## API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load danh sách | GET | `/user/favorites?page=1&per_page=12` | Khi mount, đổi trang |
| Xóa yêu thích | DELETE | `/user/favorites/{location_id}` | Click icon xóa |
| Hoàn tác xóa | POST | `/user/favorites` | Click "Hoàn tác" trong toast |
