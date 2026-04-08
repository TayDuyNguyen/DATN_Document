# Màn hình: Tour theo Danh mục

> Route: `/tour-categories/{slug}/tours`
> Quyền: 🌐 Public — không cần đăng nhập
> Mô tả: Danh sách tour được lọc theo danh mục tour cụ thể. Tái sử dụng layout từ màn Danh sách Tour, chỉ khác ở hero và context.

---

## Tái sử dụng từ màn Danh sách Tour

> Xem chi tiết tại `user_tours_list.md`

Giữ nguyên:
- Filter bar (mobile)
- Sidebar (desktop): Khoảng giá · Thời lượng · Ngày khởi hành · Đánh giá
- Main content: Toolbar + Grid/List view + Pagination
- Empty state
- Footer

---

## Điểm khác biệt

---

### 1. Page Hero

**Dùng thông tin từ response `GET /tour-categories/{slug}/tours`** (header của response hoặc gọi thêm API danh mục)

`py-48 text-center` bg màu danh mục tour (gradient)

- Breadcrumb: `"Trang chủ / Tour / [Tên danh mục]" 13px white/70`
- Icon danh mục: `64x64px radius-16 bg white/20` icon/emoji `32px`
- Title: `"[Tên danh mục]" 32px Inter 700 white` — e.g. "Tour Tham quan"
- Subtitle: `"12 tour" 16px white/80 mt-8`
- Mô tả danh mục (nếu có): `14px white/70 mt-4 max-w-500px mx-auto`

---

### 2. Category Tabs

**Bỏ** category tabs (vì đã ở trong danh mục rồi).

Thay bằng breadcrumb navigation:
`flex items-center gap-8 py-12 border-b #E2E8F0 max-w-1200px mx-auto px-24`
- "← Tất cả Tour" `13px #0066CC` hover underline → `/tours`
- `·` separator
- Tên danh mục hiện tại: `13px Inter 600 #1E293B`

---

### 3. Sidebar — Bỏ filter Danh mục

Sidebar **không có** checkbox Danh mục tour.

Chỉ giữ:
- Khoảng giá (range slider)
- Thời lượng (checkbox)
- Ngày khởi hành (date range)
- Đánh giá (radio)
- Button Đặt lại

---

### 4. Result count

Toolbar bên trái:
- `"12 tour trong [Tên danh mục]" 14px #64748B`

---

### 5. Breadcrumb

`py-12 border-b #E2E8F0`
`"Trang chủ / Tour / Tham quan" 13px #94A3B8`

---

## API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load tour theo danh mục | GET | `/tour-categories/{slug}/tours?page=&per_page=12&sort=&order=` | Khi mount, đổi filter |
| Filter giá | GET | `/tour-categories/{slug}/tours?price_min=&price_max=` | Drag range slider |
| Filter thời lượng | GET | `/tour-categories/{slug}/tours?duration=` | Chọn checkbox |
| Filter ngày | GET | `/tour-categories/{slug}/tours?available_from=&available_to=` | Chọn date range |
| Sắp xếp | GET | `/tour-categories/{slug}/tours?sort=&order=` | Chọn select |
