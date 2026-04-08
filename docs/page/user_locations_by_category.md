# Màn hình: Địa điểm theo Danh mục

> Route: `/categories/{slug}/locations`
> Quyền: 🌐 Public — không cần đăng nhập
> Mô tả: Danh sách địa điểm được lọc theo danh mục cụ thể. Tái sử dụng layout từ màn Danh sách Địa điểm, chỉ khác ở hero và context filter.

---

## Tái sử dụng từ màn Danh sách Địa điểm

> Xem chi tiết tại `user_locations_list.md`

Giữ nguyên:
- Filter bar (mobile)
- Sidebar (desktop): Quận · Mức giá · Đánh giá
- Main content: Toolbar + Grid/List view + Pagination
- Empty state
- Footer

---

## Điểm khác biệt

---

### 1. Page Hero

**API: `GET /categories/{id}`** — load thông tin danh mục

`py-48 text-center` bg màu danh mục (gradient)

- Breadcrumb: `"Trang chủ / Địa điểm / [Tên danh mục]" 13px white/70`
- Icon danh mục: `64x64px radius-16 bg white/20` icon/emoji `32px`
- Title: `"[Tên danh mục]" 32px Inter 700 white` — e.g. "Bãi biển & Biển"
- Subtitle: `"28 địa điểm" 16px white/80 mt-8`
- Mô tả danh mục (nếu có): `14px white/70 mt-4 max-w-500px mx-auto`

---

### 2. Sidebar — Bỏ filter Danh mục

Sidebar **không có** checkbox Danh mục (vì đã filter theo danh mục rồi).

Chỉ giữ:
- Quận/Huyện (checkbox)
- Mức giá (radio)
- Đánh giá (radio)
- Button Đặt lại

---

### 3. Danh mục con (Sub-categories)

**Thêm mới — hiển thị trên main content, trước toolbar**

Nếu danh mục có subcategories:

`flex gap-8 overflow-x-auto mb-20`

- Pill "Tất cả" (active mặc định): `bg #0066CC text white radius-full px-16 py-8 13px 600`
- Mỗi subcategory: `bg white border #E2E8F0 text #64748B radius-full px-16 py-8 13px 500`
  hover `border #0066CC text #0066CC`
  Click → filter `subcategory_id=` trong query

---

### 4. Breadcrumb

`py-12 border-b #E2E8F0`

`"Trang chủ / Địa điểm / Bãi biển & Biển" 13px #94A3B8`

---

### 5. Result count

Toolbar bên trái:
- `"28 địa điểm trong [Tên danh mục]" 14px #64748B`

---

## API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load thông tin danh mục | GET | `/categories/{id}` | Khi mount |
| Load địa điểm theo danh mục | GET | `/categories/{slug}/locations?page=&per_page=12&sort=&order=` | Khi mount, đổi filter |
| Filter quận | GET | `/categories/{slug}/locations?district=` | Chọn checkbox quận |
| Filter mức giá | GET | `/categories/{slug}/locations?price_level=` | Chọn radio mức giá |
| Filter danh mục con | GET | `/categories/{slug}/locations?subcategory_id=` | Click pill subcategory |
| Sắp xếp | GET | `/categories/{slug}/locations?sort=&order=` | Chọn select sắp xếp |
| Toggle yêu thích (🔐) | POST/DELETE | `/user/favorites` | Click icon yêu thích |
