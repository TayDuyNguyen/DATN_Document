# Màn hình: Tạo Địa điểm mới

> Route: `/admin/locations/create`
> Quyền: 🛡️ Admin / Staff
> Mô tả: Form tạo mới địa điểm du lịch với đầy đủ thông tin, hình ảnh, vị trí bản đồ, tags và tiện ích.

---

## Layout tổng thể

```
┌─────────────────────────────────────────────────────────────────┐
│  HEADER: Breadcrumb + Tiêu đề + [Hủy] [Lưu nháp] [Tạo ĐĐ]    │
├──────────────────────────────────────┬──────────────────────────┤
│  LEFT COLUMN (65%)                   │  RIGHT COLUMN (320px)    │
│                                      │  sticky top-24           │
│  Section 1: Thông tin cơ bản         │  Card 1: Xuất bản        │
│  Section 2: Liên hệ & Giờ mở cửa    │  Card 2: Checklist       │
│  Section 3: Vị trí bản đồ            │  Card 3: Hướng dẫn       │
│  Section 4: Hình ảnh & Media         │                          │
│  Section 5: Tags                     │                          │
│  Section 6: Tiện ích (Amenities)     │                          │
└──────────────────────────────────────┴──────────────────────────┘
```

---

## 1. Page Header

`flex justify-between items-start, mb 24px`

| Element | Style |
|---------|-------|
| Breadcrumb | `12px Inter 500 #94A3B8` — "Quản lý Địa điểm / Danh sách Địa điểm / Tạo mới" |
| Title | `24px Inter 700 #1E293B letter-spacing -0.3px` — "Tạo Địa điểm mới" |
| Subtitle | `14px Inter 400 #64748B` — "Điền đầy đủ thông tin để thêm địa điểm vào hệ thống" |

**Buttons bên phải** (`flex gap-3`):

| Button | Style | Action |
|--------|-------|--------|
| Hủy | `border #E2E8F0 bg white text #64748B radius-10 px-20 py-10` hover `border #EF4444 text #EF4444` | Navigate `/admin/locations` |
| Lưu nháp | `border #E2E8F0 bg white text #64748B radius-10 px-20 py-10` hover `border #0066CC text #0066CC` | Submit `status=inactive` |
| Tạo địa điểm | `bg #0066CC text white radius-10 px-20 py-10 shadow 14px 600` hover `bg #004999` | Submit `POST /admin/locations` |

---

## 2. Left Column — Form Sections

**Pattern chung mỗi section:**
- Card: `bg white border #E2E8F0 radius-16 p-24 mb-24`
- Header: `flex items-center gap-10 mb-20 pb-16 border-b #F1F5F9`
  - Icon container: `32x32px radius-8`
  - Title: `15px Inter 600 #1E293B`
  - Subtitle: `13px #94A3B8`

---

### Section 1 — Thông tin cơ bản
`Icon: info | color #0066CC | bg #EFF6FF`

`grid grid-cols-2 gap-20`

| Field | Type | Bắt buộc | Col | Config |
|-------|------|----------|-----|--------|
| Tên địa điểm | text | ✅ | 2 | placeholder "Ví dụ: Bãi biển Mỹ Khê" |
| Slug | text | — | 2 | placeholder "bai-bien-my-khe" · badge "Tự động" `absolute right-12 bg #EFF6FF text #0066CC 11px radius-6` · helper "Tự động tạo từ tên. Dùng cho URL." |
| Danh mục | select | ✅ | 1 | options từ `GET /categories` · khi chọn → load danh mục con |
| Danh mục con | select | — | 1 | disabled khi chưa chọn danh mục · placeholder "Chọn danh mục con (tuỳ chọn)" |
| Quận/Huyện | select | ✅ | 1 | Hải Châu / Sơn Trà / Ngũ Hành Sơn / Cẩm Lệ / Thanh Khê / Liên Chiểu |
| Mức giá | select | — | 1 | Miễn phí (free) / Bình dân ($) / Trung bình ($$) / Cao cấp ($$$) |
| Mô tả ngắn | textarea rows-3 | ✅ | 2 | max 200 ký tự · counter "0/200" `11px #94A3B8 bottom-right` |
| Mô tả chi tiết | textarea rows-6 | ✅ | 2 | helper "Hỗ trợ Markdown cơ bản" |

---

### Section 2 — Liên hệ & Giờ mở cửa
`Icon: contact_phone | color #10B981 | bg #D1FAE5`

`grid grid-cols-2 gap-20`

| Field | Type | Bắt buộc | Col | Config |
|-------|------|----------|-----|--------|
| Địa chỉ | text | ✅ | 2 | placeholder "Số nhà, tên đường, phường/xã..." · icon `location_on` trái `#94A3B8` |
| Số điện thoại | tel | — | 1 | placeholder "0905 xxx xxx" · icon `phone` trái |
| Email | email | — | 1 | placeholder "contact@example.com" · icon `email` trái |
| Website | url | — | 2 | placeholder "https://example.com" · icon `language` trái |
| Giờ mở cửa | textarea rows-3 | — | 2 | placeholder "Thứ 2 - Thứ 6: 8:00 - 17:00\nThứ 7 - CN: 8:00 - 20:00" · helper "Nhập giờ mở cửa theo từng ngày" |
| Giá tối thiểu | number | — | 1 | suffix "đ" `absolute right-14 14px #64748B` |
| Giá tối đa | number | — | 1 | suffix "đ" · helper "Để trống nếu miễn phí" |

---

### Section 3 — Vị trí trên bản đồ
`Icon: map | color #F59E0B | bg #FEF3C7`
`Subtitle: "Nhập tọa độ để hiển thị trên bản đồ"`

`grid grid-cols-2 gap-20`

| Field | Type | Bắt buộc | Col | Config |
|-------|------|----------|-----|--------|
| Vĩ độ (Latitude) | number | ✅ | 1 | step 0.000001 · placeholder "16.0544" · helper "Ví dụ: 16.0544 (Đà Nẵng)" |
| Kinh độ (Longitude) | number | ✅ | 1 | step 0.000001 · placeholder "108.2022" · helper "Ví dụ: 108.2022 (Đà Nẵng)" |

**Map preview** (`col-span-2`):
- Container: `h-200px bg #F1F5F9 border #E2E8F0 radius-12`
- Placeholder: icon `map_outlined 48px #E2E8F0` + text `"Nhập tọa độ để xem vị trí" 14px #94A3B8 centered`
- Khi có tọa độ: hiển thị static map / iframe Google Maps

**Button "Lấy vị trí hiện tại"** (`col-span-2 inline-flex`):
- `border #E2E8F0 bg white icon my_location text #64748B 13px radius-8 px-14 py-8`
- hover `border #0066CC text #0066CC`

---

### Section 4 — Hình ảnh & Media
`Icon: photo_library | color #6366F1 | bg #EEF2FF`

**Ảnh đại diện (Thumbnail)** ✅:
- Upload zone: `h-160px border-2 dashed #E2E8F0 radius-12 bg #F8FAFC flex-col center gap-8`
  - icon `upload_file 40px #94A3B8`
  - Text `"Kéo thả ảnh vào đây hoặc" 14px #64748B`
  - Button "Chọn ảnh": `bg #EFF6FF text #0066CC radius-8 px-16 py-8 13px 600`
  - Helper: `"PNG, JPG, WEBP · Tối đa 5MB · Khuyến nghị 800x600px" 12px #94A3B8`
- Khi có ảnh: preview `h-160px object-cover radius-12`
  Overlay hover: button "Thay đổi" + "Xóa"
- API: `POST /upload/image`

**Thư viện ảnh** (`mt-20`):
- Label + badge `"Tối đa 10 ảnh" bg #F1F5F9 text #64748B 11px`
- Upload zone: `h-100px` same dashed style
- Preview grid: `grid-cols-5 gap-8 mt-12`
  - Mỗi ảnh: `80x80px radius-8 object-cover border #E2E8F0`
  - Overlay hover: icon `delete white bg rgba(0,0,0,0.5)`
  - Drag to reorder (cursor grab)
- API: `POST /upload/images`

**Video URL** (`mt-20`):
- Input url · icon `play_circle` trái `#94A3B8`
- placeholder `"https://youtube.com/watch?v=..."`
- Helper: `"Link YouTube hoặc Vimeo (tuỳ chọn)"`

---

### Section 5 — Tags
`Icon: label | color #EC4899 | bg #FCE7F3`
`Subtitle: "Gắn nhãn để dễ tìm kiếm và lọc"`

Load từ `GET /tags` — group theo type:

| Group | Type value |
|-------|-----------|
| Ẩm thực | cuisine |
| Dịch vụ | service |
| Đặc điểm | feature |
| Không khí | atmosphere |

Mỗi group: label `11px uppercase #94A3B8 mb-8` + tags `flex flex-wrap gap-8`

**Tag style:**
- Unselected: `border #E2E8F0 bg white text #64748B radius-full px-12 py-6 13px 500` hover `border #0066CC text #0066CC`
- Selected: `bg #EFF6FF border #B3D9FF text #0066CC 13px 600` icon `check_small` trái

---

### Section 6 — Tiện ích (Amenities)
`Icon: checklist | color #0891B2 | bg #E0F2FE`
`Subtitle: "Các tiện ích có tại địa điểm"`

Load từ `GET /amenities` — group theo category:

| Group | Category value |
|-------|---------------|
| Kết nối | connectivity |
| Đỗ xe | parking |
| Tiện nghi | comfort |
| Thanh toán | payment |

Mỗi group: label `11px uppercase #94A3B8` + items `grid-cols-3 gap-8`

**Item style:**
- Unselected: `flex items-center gap-8 border #E2E8F0 radius-10 px-14 py-10 bg white cursor-pointer` · icon `18px #64748B` + text `13px #64748B` · hover `border #0066CC`
- Selected: `bg #EFF6FF border #B3D9FF text #0066CC` · icon `check_circle 16px #0066CC` bên phải

---

## 3. Right Column — Sidebar

### Card 1 — Xuất bản
`bg white border #E2E8F0 radius-16 p-20 mb-16`

**Trạng thái** (radio group `flex-col gap-10`):
| Option | Badge |
|--------|-------|
| ● Đang hoạt động (active) — default | `bg #D1FAE5 text #10B981` "Hiển thị công khai" |
| ○ Tạm dừng (inactive) | `bg #FEE2E2 text #EF4444` "Ẩn khỏi trang" |

**Toggle Nổi bật** (`flex justify-between items-center py-12 border-t #F1F5F9`):
- Label: `"Đánh dấu nổi bật" 14px #1E293B` + `"Hiển thị trong mục địa điểm nổi bật" 12px #94A3B8`
- Toggle: ON `#0066CC`, OFF `#E2E8F0`, `40x22px`

**Buttons:**
- "Tạo địa điểm": `bg #0066CC text white radius-10 py-12 full-width 14px 600 shadow`
- "Lưu nháp": `border #E2E8F0 bg white text #64748B radius-10 py-12 full-width mt-8`

---

### Card 2 — Checklist hoàn thiện
`bg white border #E2E8F0 radius-16 p-20 mb-16`

- Progress bar: `h-6px bg #E2E8F0 radius-full` · fill `bg #0066CC` dynamic
- Label: `"X% hoàn thành" 12px #64748B`

| Item | Trạng thái |
|------|-----------|
| Tên địa điểm | Pending → Done khi điền |
| Danh mục | Pending → Done |
| Quận/Huyện | Pending → Done |
| Mô tả ngắn | Pending → Done |
| Địa chỉ | Pending → Done |
| Tọa độ | Pending → Done |
| Ảnh đại diện | Pending → Done |
| Thư viện ảnh | Pending → Done |
| Tags | Pending → Done |
| Tiện ích | Pending → Done |

- Done: icon `check_circle #10B981` + text `#64748B line-through`
- Pending: icon `radio_button_unchecked #E2E8F0` + text `#1E293B`

---

### Card 3 — Hướng dẫn
`bg #EFF6FF border #B3D9FF radius-16 p-20`

- Title: `"💡 Lưu ý" 13px Inter 600 #0066CC mb-12`
- Items: icon `arrow_right #0066CC` + `12px #1E293B`
  - "Tên và mô tả nên rõ ràng, dễ tìm kiếm"
  - "Ảnh đại diện nên có tỷ lệ 4:3 hoặc 16:9"
  - "Tọa độ chính xác giúp hiển thị đúng trên bản đồ"
  - "Gắn tags và tiện ích giúp người dùng tìm kiếm dễ hơn"

---

## 4. Validation & States

| Tình huống | Xử lý |
|-----------|-------|
| Field bắt buộc trống | Border `#EF4444` · bg `rgba(239,68,68,0.04)` · error text `12px #EF4444` · scroll to first error |
| Đang submit | Button disabled · spinner · "Đang tạo..." · `bg #3385D6 cursor-not-allowed` |
| Thành công | Toast `bg #D1FAE5 text #10B981` "Tạo địa điểm thành công!" · redirect `/admin/locations/{id}` |
| Thất bại | Toast `bg #FEE2E2 text #EF4444` "Có lỗi xảy ra. Vui lòng thử lại." |

---

## 5. API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load danh mục | GET | `/categories` | Khi mount |
| Load danh mục con | GET | `/categories/{id}` | Khi chọn danh mục |
| Load tags | GET | `/tags` | Khi mount |
| Load amenities | GET | `/amenities` | Khi mount |
| Upload thumbnail | POST | `/upload/image` | Chọn ảnh đại diện |
| Upload thư viện | POST | `/upload/images` | Chọn nhiều ảnh |
| Xóa ảnh Cloudinary | DELETE | `/upload/image` | Click xóa preview |
| Tạo địa điểm | POST | `/admin/locations` | Submit form |

**Body POST /admin/locations:**
```json
{
  "name": "*",
  "category_id": "*",
  "description": "*",
  "short_description": "*",
  "address": "*",
  "district": "*",
  "latitude": "*",
  "longitude": "*",
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
  "status": "active",
  "is_featured": false
}
```
