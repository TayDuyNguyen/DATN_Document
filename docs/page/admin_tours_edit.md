# Màn hình: Chỉnh sửa Tour

> Route: `/admin/tours/{id}/edit`
> Quyền: 🛡️ Admin / Staff
> Mô tả: Form chỉnh sửa thông tin tour đã tồn tại. Tái sử dụng toàn bộ layout từ màn Tạo Tour, chỉ khác ở các điểm được ghi rõ bên dưới.

---

## Tái sử dụng từ màn Tạo Tour

> Xem chi tiết tại `admin_tours_create.md`

Giữ nguyên toàn bộ:
- Layout 2 cột (left form + right sidebar)
- Section 1: Thông tin cơ bản
- Section 2: Giá & Số lượng
- Section 3: Lịch khởi hành
- Section 4: Lịch trình (Itinerary builder)
- Section 5: Bao gồm & Không bao gồm
- Section 6: Hình ảnh & Media
- Design system, màu sắc, spacing

---

## Điểm khác biệt

---

### 1. Page Header

| Element | Tạo Tour | Chỉnh sửa Tour |
|---------|----------|----------------|
| Breadcrumb | ".../ Tạo mới" | ".../ Bà Nà Hills - Cầu Vàng / Chỉnh sửa" |
| Title | "Tạo Tour mới" | "Chỉnh sửa Tour" |
| Subtitle | "Điền đầy đủ thông tin..." | Tên tour hiện tại `14px Inter 500 #64748B` |
| Button Hủy | → `/admin/tours` | → `/admin/tours/{id}` (trang chi tiết) |
| Button phụ | "Lưu nháp" | "Xem trang" — icon `open_in_new` → mở `/tours/{slug}` tab mới |
| Button chính | "Tạo tour" | "Lưu thay đổi" → `PUT /admin/tours/{id}` |

---

### 2. Loading State

Khi fetch `GET /tours/{slug}` chưa xong:
- Toàn bộ form hiển thị skeleton loading
- Mỗi input: `skeleton bar h-10 bg #E2E8F0 radius-10 animation pulse`
- Sidebar cards: skeleton tương tự
- Header: spinner nhỏ + "Đang tải dữ liệu tour..." `13px #94A3B8`

---

### 3. Form Pre-filled

- Tất cả fields được điền sẵn từ response `GET /tours/{slug}`
- Slug field: hiển thị slug hiện tại, có thể sửa
  - Khi user thay đổi slug → hiện warning box:
    `bg #FEF3C7 border rgba(245,158,11,0.3) radius-8 p-12`
    icon `warning_amber #F59E0B` + text `13px #92400E`:
    "Thay đổi slug sẽ làm thay đổi URL của tour. Các link cũ sẽ không còn hoạt động."

---

### 4. Thumbnail & Ảnh hiện tại

**Thumbnail:**
- Hiển thị ảnh hiện tại thay vì empty upload zone
- Preview: `full-width h-160px object-cover radius-12`
- Bottom overlay thường trực (không cần hover):
  `bg rgba(0,0,0,0.5) p-8 radius-b-12`
  - Text "Ảnh hiện tại" `11px white opacity-70`
  - Button "Thay đổi": `bg white/20 text white border white/30 radius-6 px-10 py-4 12px 600`
    → click mở file picker → upload mới → replace

**Thư viện ảnh:**
- Hiển thị grid ảnh hiện có (pre-filled)
- Mỗi ảnh có nút xóa (×) góc trên phải
- Drag to reorder
- Upload zone vẫn hiển thị bên dưới để thêm ảnh mới
- Counter: "5/10 ảnh" `12px #94A3B8`

---

### 5. Sidebar — Card "Xuất bản"

**Thêm so với màn Tạo:**

Block "Thông tin" (trên buttons, sau divider):
- Label: "THÔNG TIN" `10px uppercase #94A3B8 mb-8`
- Rows (`flex justify-between 13px`):
  - "Ngày tạo": `#64748B` — e.g. "15/03/2026 09:30"
  - "Cập nhật lần cuối": `#64748B` — e.g. "01/04/2026 14:22"
  - "Tạo bởi": `#64748B` — e.g. "Admin Duy Tây"

**Buttons:**
| Button | Tạo Tour | Chỉnh sửa Tour |
|--------|----------|----------------|
| Chính | "Tạo tour" | "Lưu thay đổi" |
| Phụ | "Lưu nháp" | "Hủy thay đổi" → confirm nếu có thay đổi chưa lưu |

**Toggles:** Pre-set theo `is_featured` và `is_hot` hiện tại của tour.

---

### 6. Sidebar — Card "Checklist"

- Tất cả items Done (✓) vì đã có dữ liệu
- Progress bar: 100% hoặc theo field thực tế còn thiếu
- Thêm item: "Có lịch khởi hành"
  - Done: nếu tour đã có schedule
  - Pending: nếu chưa có schedule nào

---

### 7. Sidebar — Card mới: "Thao tác nhanh"

Thêm sau Card Checklist:
`bg white border #E2E8F0 radius-16 p-20 mb-16`

Title: "Thao tác nhanh" `14px Inter 600 #1E293B mb-12`

| Button | Icon | Hover | Action |
|--------|------|-------|--------|
| Xem lịch khởi hành | `calendar_month` | `border #0066CC text #0066CC` | Navigate `/admin/tour-schedules?tour_id={id}` |
| Xem đánh giá | `star` | `border #0066CC text #0066CC` | Navigate `/admin/ratings?tour_id={id}` |
| Nhân bản tour | `content_copy` | `border #0066CC text #0066CC` | Confirm → copy data → redirect tạo mới pre-filled |
| Xóa tour | `delete` | `bg #FEE2E2` | Confirm delete → `DELETE /admin/tours/{id}` → redirect `/admin/tours` |

Style chung: `border #E2E8F0 bg white text #64748B radius-10 py-10 full-width 13px 600`
Xóa tour: `border #FEE2E2 text #EF4444`

---

### 8. Unsaved Changes Guard

Khi navigate away hoặc click "Hủy thay đổi" khi có thay đổi chưa lưu:

Confirm dialog:
- Title: "Bỏ thay đổi?" `16px Inter 700 #1E293B`
- Body: "Bạn có thay đổi chưa được lưu. Nếu rời đi, các thay đổi sẽ bị mất."
  `14px #64748B`
- Footer:
  - "Tiếp tục chỉnh sửa": `bg #0066CC text white radius-10 px-20 py-10`
  - "Bỏ thay đổi": `border #E2E8F0 text #64748B radius-10` hover `text #EF4444 border #EF4444`

---

### 9. Submit States

| Tình huống | Xử lý |
|-----------|-------|
| Đang lưu | Button disabled · spinner · text "Đang lưu..." · `bg #3385D6 cursor-not-allowed` |
| Lưu thành công | Toast `bg #D1FAE5 text #10B981` "Cập nhật tour thành công!" · **ở lại trang edit** (không redirect) |
| Lưu thất bại | Toast `bg #FEE2E2 text #EF4444` "Có lỗi xảy ra. Vui lòng thử lại." · highlight field lỗi từ server |
| Field bắt buộc trống | Border `#EF4444` · error text `12px #EF4444` · scroll to first error |

---

## API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load dữ liệu tour | GET | `/tours/{slug}` | Khi mount (id từ URL params) |
| Load danh mục tour | GET | `/tour-categories` | Khi mount |
| Upload thumbnail mới | POST | `/upload/image` | Click "Thay đổi" ảnh đại diện |
| Upload ảnh thêm | POST | `/upload/images` | Thêm ảnh vào thư viện |
| Xóa ảnh Cloudinary | DELETE | `/upload/image` | Click xóa ảnh preview |
| Lưu thay đổi | PUT | `/admin/tours/{id}` | Submit form |
| Xóa tour | DELETE | `/admin/tours/{id}` | Confirm delete dialog |

**Body PUT /admin/tours/{id}:** (all fields optional — chỉ gửi fields đã thay đổi)
```json
{
  "name": "",
  "tour_category_id": "",
  "price_adult": "",
  "slug": "",
  "description": "",
  "short_desc": "",
  "itinerary": "",
  "inclusions": "",
  "exclusions": "",
  "price_child": "",
  "price_infant": "",
  "discount_percent": "",
  "duration": "",
  "start_time": "",
  "meeting_point": "",
  "max_people": "",
  "min_people": "",
  "available_from": "",
  "available_to": "",
  "thumbnail": "",
  "images": [],
  "video_url": "",
  "location_ids": [],
  "status": "",
  "is_featured": false,
  "is_hot": false
}
```
