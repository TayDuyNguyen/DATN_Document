# Màn hình: Tạo Tour mới

> Route: `/admin/tours/create`
> Quyền: 🛡️ Admin / Staff
> Mô tả: Form tạo mới sản phẩm tour du lịch với đầy đủ thông tin, hình ảnh, giá và lịch trình.

---

## Layout tổng thể

```
┌─────────────────────────────────────────────────────────────────┐
│  HEADER: Breadcrumb + Tiêu đề + [Hủy] [Lưu nháp] [Tạo tour]   │
├──────────────────────────────────────┬──────────────────────────┤
│  LEFT COLUMN (65%)                   │  RIGHT COLUMN (320px)    │
│                                      │  sticky top-24           │
│  Section 1: Thông tin cơ bản         │  Card 1: Xuất bản        │
│  Section 2: Giá & Số lượng           │  Card 2: Checklist       │
│  Section 3: Lịch khởi hành           │  Card 3: Địa điểm LQ     │
│  Section 4: Lịch trình               │  Card 4: Hướng dẫn       │
│  Section 5: Bao gồm / Không bao gồm  │                          │
│  Section 6: Hình ảnh & Media         │                          │
└──────────────────────────────────────┴──────────────────────────┘
```

---

## 1. Page Header

`flex justify-between items-start, mb 24px`

### Bên trái
| Element | Style |
|---------|-------|
| Breadcrumb | `12px Inter 500 #94A3B8` — "Quản lý Tour / Danh sách Tour / Tạo mới" |
| Title | `24px Inter 700 #1E293B letter-spacing -0.3px` — "Tạo Tour mới" |
| Subtitle | `14px Inter 400 #64748B` — "Điền đầy đủ thông tin để thêm tour vào hệ thống" |

### Bên phải (`flex gap-3`)
| Button | Style | Action |
|--------|-------|--------|
| Hủy | `border #E2E8F0 bg white text #64748B radius-10 px-20 py-10` hover `border #EF4444 text #EF4444` | Navigate `/admin/tours` |
| Lưu nháp | `border #E2E8F0 bg white text #64748B radius-10 px-20 py-10` hover `border #0066CC text #0066CC` | Submit status=inactive |
| Tạo tour | `bg #0066CC text white radius-10 px-20 py-10 shadow` hover `bg #004999` | Submit `POST /admin/tours` |

---

## 2. Left Column — Form Sections

**Pattern chung mỗi section:**
- Card: `bg white border #E2E8F0 radius-16 p-24 mb-24`
- Section header: `flex items-center gap-10 mb-20 pb-16 border-b #F1F5F9`
  - Icon container: `32x32px radius-8`
  - Title: `15px Inter 600 #1E293B`
  - Subtitle: `13px #94A3B8`

---

### Section 1 — Thông tin cơ bản
`Icon: inventory_2 | color #0066CC | bg #EFF6FF`

| Field | Type | Bắt buộc | Config |
|-------|------|----------|--------|
| Tên tour | text | ✅ | placeholder "Ví dụ: Bà Nà Hills - Cầu Vàng 1 ngày" · col-span 2 |
| Slug | text | — | placeholder "ba-na-hills-cau-vang" · badge "Tự động" · col-span 2 |
| Danh mục tour | select | ✅ | options từ `GET /tour-categories` · col-span 1 |
| Thời lượng | text | ✅ | placeholder "1 ngày, 2 ngày 1 đêm" · icon schedule · col-span 1 |
| Mô tả ngắn | textarea rows-3 | ✅ | max 300 ký tự · counter "0/300" · col-span 2 |
| Mô tả chi tiết | textarea rows-6 | ✅ | helper "Hỗ trợ Markdown cơ bản" · col-span 2 |

---

### Section 2 — Giá & Số lượng
`Icon: payments | color #10B981 | bg #D1FAE5`

**Grid 3 cột:**

| Field | Type | Bắt buộc | Config |
|-------|------|----------|--------|
| Giá người lớn | number | ✅ | suffix "đ" · helper "Giá cơ bản / người lớn" |
| Giá trẻ em | number | — | suffix "đ" · helper "Để trống nếu không áp dụng" |
| Giá em bé | number | — | suffix "đ" · helper "Dưới 2 tuổi" |
| Giảm giá (%) | number | — | min 0 max 100 · suffix "%" |
| Giá sau giảm | number | — | disabled · bg #F8FAFC · text #0066CC 16px 700 · tự động tính · col-span 2 |
| Số người tối đa | number | — | icon group · helper "Tối đa / lịch khởi hành" |
| Số người tối thiểu | number | — | helper "Tối thiểu để tour khởi hành" |
| Giờ khởi hành | time | — | icon schedule |
| Điểm tập trung | text | — | icon location_on · col-span 3 |

---

### Section 3 — Lịch khởi hành
`Icon: calendar_month | color #F59E0B | bg #FEF3C7`

| Field | Type | Config |
|-------|------|--------|
| Ngày bắt đầu bán | date | helper "Ngày tour bắt đầu nhận đặt chỗ" |
| Ngày kết thúc bán | date | helper "Ngày tour ngừng nhận đặt chỗ" |

**Info box** (col-span 2):
- `bg #FEF3C7 border rgba(245,158,11,0.3) radius-10 p-14`
- Icon info `#F59E0B` + text `13px #92400E`:
  "Sau khi tạo tour, bạn có thể thêm các lịch khởi hành cụ thể tại mục Lịch khởi hành."
- Link "Xem hướng dẫn →" `13px 600 #0066CC`

---

### Section 4 — Lịch trình (Itinerary)
`Icon: route | color #6366F1 | bg #EEF2FF`

**Itinerary builder — mỗi ngày là 1 block:**
- Block header: `flex justify-between`
  - Badge "Ngày 1": `bg #EFF6FF text #0066CC 12px 700 radius-8 px-10 py-4`
  - Button xóa: icon `delete_outline` color `#94A3B8` hover `#EF4444`
- Textarea: `rows-4 border #E2E8F0 radius-10 resize-none full-width`
  placeholder: "07:00 - Tập trung tại điểm hẹn\n08:00 - Khởi hành..."

**Button "Thêm ngày"** (mt-12):
- `border dashed #B3D9FF bg #EFF6FF/50 text #0066CC radius-10 py-10 full-width 13px 600`
- icon add bên trái · hover `bg #EFF6FF`

---

### Section 5 — Bao gồm & Không bao gồm
`Icon: checklist | color #0891B2 | bg #E0F2FE`

**Grid 2 cột:**

| Cột | Label | Placeholder |
|-----|-------|-------------|
| Trái | Bao gồm (Inclusions) | "✓ Xe đưa đón\n✓ Hướng dẫn viên\n✓ Vé tham quan\n✓ Bữa trưa" |
| Phải | Không bao gồm (Exclusions) | "✗ Chi phí cá nhân\n✗ Đồ uống\n✗ Tip hướng dẫn viên" |

- Mỗi textarea: `rows-5`
- Helper: "Mỗi dòng = 1 mục"

---

### Section 6 — Hình ảnh & Media
`Icon: photo_library | color #EC4899 | bg #FCE7F3`

**Ảnh đại diện (Thumbnail)** ✅:
- Upload zone: `h-160px border-2 dashed #E2E8F0 radius-12 bg #F8FAFC flex-col center`
  - Icon `upload_file 40px #94A3B8`
  - Text "Kéo thả ảnh vào đây hoặc" `14px #64748B`
  - Button "Chọn ảnh": `bg #EFF6FF text #0066CC radius-8 px-16 py-8 13px 600`
  - Helper: "PNG, JPG, WEBP · Tối đa 5MB · Khuyến nghị 800x600px" `12px #94A3B8`
- Khi có ảnh: preview `h-160px object-cover radius-12`
  Overlay hover: button "Thay đổi" + "Xóa"
- API: `POST /upload/image`

**Thư viện ảnh**:
- Label + badge "Tối đa 10 ảnh" `bg #F1F5F9 text #64748B 11px`
- Upload zone: `h-100px` same dashed style
- Preview grid: `grid-cols-5 gap-8 mt-12`
  - Mỗi ảnh: `80x80px radius-8 object-cover border #E2E8F0`
  - Overlay hover: icon delete white, `bg rgba(0,0,0,0.5)`
  - Drag to reorder (cursor grab)
- API: `POST /upload/images`

**Video URL**:
- Input url · icon `play_circle` trái `#94A3B8`
- placeholder "https://youtube.com/watch?v=..."
- Helper: "Link YouTube hoặc Vimeo (tuỳ chọn)"

---

## 3. Right Column — Sidebar

### Card 1 — Xuất bản
`bg white border #E2E8F0 radius-16 p-20 mb-16`

**Trạng thái** (radio group):
| Option | Badge |
|--------|-------|
| ● Đang hoạt động (active) — default | `bg #D1FAE5 text #10B981` "Hiển thị công khai" |
| ○ Tạm dừng (inactive) | `bg #FEE2E2 text #EF4444` "Ẩn khỏi trang" |
| ○ Hết chỗ (sold_out) | `bg #FEF3C7 text #F59E0B` "Không nhận đặt" |

**Toggles:**
| Toggle | ON color | Label | Helper |
|--------|----------|-------|--------|
| Nổi bật | `#0066CC` | "Đánh dấu nổi bật" | "Hiển thị trong mục Tour nổi bật" |
| Hot 🔥 | `#FF6B35` | "Đánh dấu Hot" | "Hiển thị trong mục Tour Hot" |

**Buttons:**
- "Tạo tour": `bg #0066CC text white radius-10 py-12 full-width 14px 600 shadow`
- "Lưu nháp": `border #E2E8F0 bg white text #64748B radius-10 py-12 full-width mt-8`

---

### Card 2 — Checklist hoàn thiện
`bg white border #E2E8F0 radius-16 p-20 mb-16`

- Progress bar: `h-6px bg #E2E8F0 radius-full` · fill `bg #0066CC` dynamic width
- Label: "X% hoàn thành" `12px #64748B`

| Item | Trạng thái |
|------|-----------|
| Tên tour | Pending → Done khi điền |
| Danh mục tour | Pending → Done |
| Mô tả ngắn | Pending → Done |
| Mô tả chi tiết | Pending → Done |
| Giá người lớn | Pending → Done |
| Thời lượng | Pending → Done |
| Ảnh đại diện | Pending → Done |
| Lịch trình | Pending → Done |
| Bao gồm / Không bao gồm | Pending → Done |

- Done: icon `check_circle #10B981` + text `#64748B line-through`
- Pending: icon `radio_button_unchecked #E2E8F0` + text `#1E293B`

---

### Card 3 — Địa điểm liên quan
`bg white border #E2E8F0 radius-16 p-20 mb-16`

- Search input: `placeholder "Tìm địa điểm..." border #E2E8F0 radius-8 p-8 icon search`
- Selected list: mỗi item `flex gap-8 bg #F8FAFC border #E2E8F0 radius-8 p-8`
  - Thumbnail `32x32px radius-6`
  - Name `13px Inter 500 #1E293B flex-1`
  - Button xóa: icon close `#94A3B8` hover `#EF4444`
- Empty: "Chưa có địa điểm nào được chọn" `13px #94A3B8 text-center py-12`

---

### Card 4 — Hướng dẫn
`bg #EFF6FF border #B3D9FF radius-16 p-20`

- Title: "💡 Lưu ý" `13px Inter 600 #0066CC mb-12`
- Items: icon `arrow_right #0066CC` + `12px #1E293B`
  - "Tên tour nên ngắn gọn, dễ nhớ và có từ khóa"
  - "Ảnh đại diện quyết định 70% lượt click"
  - "Mô tả chi tiết lịch trình giúp tăng tỷ lệ đặt tour"
  - "Thêm lịch khởi hành sau khi tạo tour thành công"

---

## 4. Validation & States

| Tình huống | Xử lý |
|-----------|-------|
| Field bắt buộc trống | Border `#EF4444` · bg `rgba(239,68,68,0.04)` · error text `12px #EF4444` · scroll to first error |
| Submit thành công | Toast `bg #D1FAE5 text #10B981` "Tạo tour thành công!" · redirect `/admin/tours/{id}` |
| Submit thất bại | Toast `bg #FEE2E2 text #EF4444` "Có lỗi xảy ra. Vui lòng thử lại." |
| Đang submit | Button disabled · spinner · text "Đang tạo..." · `bg #3385D6` |

---

## 5. API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load danh mục tour | GET | `/tour-categories` | Khi mount |
| Upload thumbnail | POST | `/upload/image` | Chọn ảnh đại diện |
| Upload thư viện | POST | `/upload/images` | Chọn nhiều ảnh |
| Xóa ảnh Cloudinary | DELETE | `/upload/image` | Click xóa preview |
| Tạo tour | POST | `/admin/tours` | Submit form |

**Body POST /admin/tours:**
```json
{
  "name": "*",
  "tour_category_id": "*",
  "price_adult": "*",
  "slug": "",
  "description": "*",
  "short_desc": "*",
  "itinerary": "",
  "inclusions": "",
  "exclusions": "",
  "price_child": "",
  "price_infant": "",
  "discount_percent": "",
  "duration": "*",
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
  "status": "active",
  "is_featured": false,
  "is_hot": false
}
```
