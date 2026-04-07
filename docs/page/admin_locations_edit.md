# Màn hình: Chỉnh sửa Địa điểm

> Route: `/admin/locations/{id}/edit`
> Quyền: 🛡️ Admin / Staff
> Mô tả: Form chỉnh sửa địa điểm đã tồn tại. Tái sử dụng toàn bộ layout từ màn Tạo Địa điểm. Tags và Amenities được auto-save ngay khi click, không cần submit form.

---

## Tái sử dụng từ màn Tạo Địa điểm

> Xem chi tiết tại `admin_locations_create.md`

Giữ nguyên toàn bộ:
- Layout 2 cột (left 65% + right sidebar 320px)
- Section 1: Thông tin cơ bản
- Section 2: Liên hệ & Giờ mở cửa
- Section 3: Vị trí bản đồ
- Section 4: Hình ảnh & Media
- Section 5: Tags
- Section 6: Tiện ích (Amenities)
- Design system, màu sắc, spacing

---

## Điểm khác biệt

---

### 1. Page Header

| Element | Tạo Địa điểm | Chỉnh sửa Địa điểm |
|---------|-------------|-------------------|
| Breadcrumb | ".../ Tạo mới" | ".../ Bãi biển Mỹ Khê / Chỉnh sửa" |
| Title | "Tạo Địa điểm mới" | "Chỉnh sửa Địa điểm" |
| Subtitle | "Điền đầy đủ thông tin..." | Tên địa điểm `14px Inter 500 #64748B` |
| Button Hủy | → `/admin/locations` | → `/admin/locations/{id}` (chi tiết) |
| Button phụ | "Lưu nháp" | "Xem trang" — icon `open_in_new` → `/locations/{slug}` tab mới |
| Button chính | "Tạo địa điểm" | "Lưu thay đổi" → `PUT /admin/locations/{id}` |

---

### 2. Loading State

Khi fetch `GET /locations/{slug}` chưa xong:
- Skeleton loading toàn bộ form: `h-10 bg #E2E8F0 radius-10 animation pulse`
- Spinner nhỏ + `"Đang tải dữ liệu..." 13px #94A3B8`

---

### 3. Form Pre-filled

- Tất cả fields điền sẵn từ response `GET /locations/{slug}`
- Slug field: khi user thay đổi → warning box bên dưới:
  - `bg #FEF3C7 border rgba(245,158,11,0.3) radius-8 p-12`
  - icon `warning_amber #F59E0B` + text `13px #92400E`:
    "Thay đổi slug sẽ làm thay đổi URL của địa điểm. Các link cũ sẽ không còn hoạt động."

---

### 4. Section 4 — Hình ảnh: Pre-filled

**Thumbnail:**
- Hiển thị ảnh hiện tại thay vì empty upload zone
- Preview: `full-width h-160px object-cover radius-12`
- Bottom overlay thường trực: `bg rgba(0,0,0,0.5) p-8 radius-b-12`
  - Text `"Ảnh hiện tại" 11px white opacity-70`
  - Button "Thay đổi": `bg white/20 text white border white/30 radius-6 px-10 py-4 12px 600`
    → click mở file picker → upload mới → replace

**Thư viện ảnh:**
- Grid ảnh hiện có (pre-filled)
- Mỗi ảnh có nút xóa `×` góc trên phải
- Drag to reorder
- Upload zone vẫn hiển thị bên dưới để thêm ảnh mới
- Counter: `"4/10 ảnh" 12px #94A3B8`

---

### 5. Section 5 — Tags: Auto-save

- Tags đã gán hiển thị ở trạng thái Selected (xanh)
- **Không cần submit form** — auto-save ngay khi click:
  - Click tag unselected → `POST /admin/locations/{id}/tags` · body: `{ tag_ids: [id] }`
  - Click tag selected → `DELETE /admin/locations/{id}/tags/{tagId}`
- Sau mỗi auto-save: toast nhỏ `"Đã lưu" bg #D1FAE5 text #10B981 12px` bottom-right, auto-dismiss 2s

---

### 6. Section 6 — Tiện ích: Auto-save

- Amenities đã gán hiển thị ở trạng thái Selected
- **Không cần submit form** — auto-save ngay khi click:
  - Click unselected → `POST /admin/locations/{id}/amenities` · body: `{ amenity_ids: [id] }`
  - Click selected → `DELETE /admin/locations/{id}/amenities/{amenityId}`
- Sau mỗi auto-save: toast nhỏ tương tự Tags

---

### 7. Sidebar — Card "Xuất bản"

**Thêm block "Thông tin"** (trên buttons, `border-t #F1F5F9 pt-16`):
- Label: `"THÔNG TIN" 10px uppercase #94A3B8 mb-8`

| Label | Value | Style |
|-------|-------|-------|
| Ngày tạo | "15/03/2026 09:30" | `flex justify-between 13px #64748B` |
| Cập nhật lần cuối | "01/04/2026 14:22" | same |
| Lượt xem | "1.248 lượt" | same |
| Yêu thích | "248 lượt" | same |

**Buttons:**
| Button | Tạo | Chỉnh sửa |
|--------|-----|-----------|
| Chính | "Tạo địa điểm" | "Lưu thay đổi" |
| Phụ | "Lưu nháp" | "Hủy thay đổi" → confirm nếu có thay đổi chưa lưu |

**Toggles:** Pre-set theo `status` và `is_featured` hiện tại.

---

### 8. Sidebar — Card "Checklist"

- Tất cả items Done (✓) vì đã có dữ liệu
- Progress bar: 100% hoặc theo field thực tế còn thiếu

---

### 9. Sidebar — Card mới: "Thao tác nhanh"

Thêm sau Card Checklist:
`bg white border #E2E8F0 radius-16 p-20 mb-16`

Title: `"Thao tác nhanh" 14px Inter 600 #1E293B mb-12`

| Button | Icon | Hover | Action |
|--------|------|-------|--------|
| Xem đánh giá | `star` | `border #0066CC text #0066CC` | `/admin/ratings?location_id={id}` |
| Xem địa điểm lân cận | `near_me` | `border #0066CC text #0066CC` | `/locations/{id}/nearby` tab mới |
| Xóa địa điểm | `delete` | `bg #FEE2E2` | Confirm → `DELETE /admin/locations/{id}` → redirect `/admin/locations` |

Ghost style: `border #E2E8F0 bg white text #64748B radius-10 py-10 full-width 13px 600`
Xóa: `border #FEE2E2 text #EF4444`

---

### 10. Confirm Delete Dialog

**Modal:** `bg white radius-16 w-400px shadow-modal backdrop rgba(0,0,0,0.4)`

| Vùng | Nội dung |
|------|---------|
| Header | Icon `warning_amber 40x40 bg #FEE2E2 radius-10 color #EF4444` + "Xóa địa điểm này?" `16px 700 #1E293B` |
| Body | "Địa điểm [Tên] sẽ bị xóa vĩnh viễn." `14px #64748B` + Warning `bg #FEF3C7 13px #92400E`: "⚠ Tất cả đánh giá, lượt yêu thích, tags và tiện ích liên quan sẽ bị xóa theo." |
| Footer | "Hủy" (ghost) + "Xóa địa điểm" `bg #EF4444 hover #DC2626` |

---

### 11. Unsaved Changes Guard

Khi navigate away khi có thay đổi form chưa lưu:

| Button | Style | Action |
|--------|-------|--------|
| Tiếp tục chỉnh sửa | `bg #0066CC text white radius-10` | Đóng dialog |
| Bỏ thay đổi | `border #E2E8F0 text #64748B` hover `text #EF4444` | Navigate away |

> Tags và Amenities được auto-save ngay khi click → không bị ảnh hưởng bởi guard này.

---

### 12. Submit States

| Tình huống | Xử lý |
|-----------|-------|
| Đang lưu | Button disabled · spinner · "Đang lưu..." · `bg #3385D6 cursor-not-allowed` |
| Lưu thành công | Toast `bg #D1FAE5 text #10B981` "Cập nhật địa điểm thành công!" · ở lại trang edit |
| Lưu thất bại | Toast `bg #FEE2E2 text #EF4444` "Có lỗi xảy ra. Vui lòng thử lại." |
| Xóa thành công | Toast `bg #D1FAE5 text #10B981` "Đã xóa địa điểm." · redirect `/admin/locations` |

---

## API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load dữ liệu | GET | `/locations/{slug}` | Khi mount |
| Load danh mục | GET | `/categories` | Khi mount |
| Load tags | GET | `/tags` | Khi mount |
| Load amenities | GET | `/amenities` | Khi mount |
| Upload thumbnail mới | POST | `/upload/image` | Click "Thay đổi" ảnh |
| Upload ảnh thêm | POST | `/upload/images` | Thêm ảnh thư viện |
| Xóa ảnh Cloudinary | DELETE | `/upload/image` | Click xóa ảnh preview |
| Thêm tag | POST | `/admin/locations/{id}/tags` | Click tag unselected |
| Xóa tag | DELETE | `/admin/locations/{id}/tags/{tagId}` | Click tag selected |
| Thêm amenity | POST | `/admin/locations/{id}/amenities` | Click amenity unselected |
| Xóa amenity | DELETE | `/admin/locations/{id}/amenities/{amenityId}` | Click amenity selected |
| Lưu thay đổi | PUT | `/admin/locations/{id}` | Submit form |
| Xóa địa điểm | DELETE | `/admin/locations/{id}` | Confirm delete dialog |

**Body PUT /admin/locations/{id}:** (all optional)
```json
{
  "name": "",
  "category_id": "",
  "description": "",
  "short_description": "",
  "address": "",
  "district": "",
  "latitude": "",
  "longitude": "",
  "subcategory_id": "",
  "slug": "",
  "phone": "",
  "email": "",
  "website": "",
  "opening_hours": "",
  "price_min": "",
  "price_max": "",
  "price_level": "",
  "thumbnail": "",
  "images": [],
  "video_url": "",
  "status": "",
  "is_featured": false
}
```
