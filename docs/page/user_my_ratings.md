# Màn hình: Đánh giá của tôi

> Route: `/profile/ratings`
> Quyền: 🔐 Cần đăng nhập
> Mô tả: Xem toàn bộ đánh giá đã viết cho địa điểm và tour, với tùy chọn sửa và xóa.

---

## Tái sử dụng từ màn Hồ sơ cá nhân

> Xem chi tiết layout tại `user_profile.md`

Giữ nguyên: Header · Breadcrumb · Sidebar (item "Đánh giá của tôi" active) · Footer

---

## Main Content

### 1. Page Header

`flex justify-between items-center mb-24`

- Title: `"Đánh giá của tôi" 20px Inter 700 #1E293B`
- Count: `"5 đánh giá" 14px #94A3B8`

### 2. Filter Tabs

`flex gap-0 border-b #E2E8F0 mb-24`

| Tab | Label |
|-----|-------|
| Tất cả | "Tất cả (5)" |
| Địa điểm | "Địa điểm (3)" |
| Tour | "Tour (2)" |

- Active: `border-b-2 border-#0066CC text #0066CC 14px 600`
- Inactive: `text #64748B 14px 500` hover `text #0066CC`

### 3. Rating Card List

**API: `GET /user/ratings?status=&page=1&per_page=10`**

`flex flex-col gap-16`

Mỗi rating card:
`bg white border #E2E8F0 radius-16 p-20`

**Card header** (`flex justify-between items-start mb-16`):

**Bên trái** (`flex gap-12`):
- Thumbnail: `56x56px radius-10 object-cover border #E2E8F0 flex-shrink-0`
- Right:
  - `flex items-center gap-8 mb-4`:
    - Badge loại: `11px 600 rounded-full px-8 py-3`
      - Địa điểm: `bg #EEF2FF text #6366F1` icon `location_on 12px`
      - Tour: `bg #EFF6FF text #0066CC` icon `tour 12px`
    - Tên địa điểm/tour: `14px Inter 600 #1E293B`
      hover `color #0066CC` cursor pointer
      → `/locations/{slug}` hoặc `/tours/{slug}`
  - Stars: 5 icons `star 16px` filled `#F59E0B` / empty `#E2E8F0`
  - Ngày đánh giá: `12px #94A3B8 mt-4`

**Bên phải** (`flex items-center gap-8`):
- Badge trạng thái `11px 700 rounded-full px-8 py-3`:
  - approved: `bg #D1FAE5 text #10B981` "ĐÃ DUYỆT"
  - pending: `bg #FEF3C7 text #F59E0B` "CHỜ DUYỆT"
  - rejected: `bg #FEE2E2 text #EF4444` "TỪ CHỐI"
- Button sửa: `28x28px border #E2E8F0 radius-6 bg white` icon `edit 16px #64748B`
  hover `border #F59E0B color #F59E0B`
  → mở modal sửa đánh giá
- Button xóa: `28x28px border #E2E8F0 radius-6 bg white` icon `delete 16px #64748B`
  hover `border #EF4444 color #EF4444`
  → confirm xóa → `DELETE /ratings/{id}`

**Card body:**

Comment: `14px #1E293B line-height 1.6`
- Nếu dài: max 3 lines + "Xem thêm" `12px #0066CC`

Images (nếu có): `flex gap-8 mt-12`
- Mỗi ảnh: `64x64px radius-8 object-cover border #E2E8F0 cursor-pointer`
  → lightbox

**Rejected reason** (nếu status=rejected):
`bg #FEE2E2 border rgba(239,68,68,0.2) radius-8 px-12 py-8 mt-12`
- icon `info 14px #EF4444` + `"Lý do từ chối: [reason]" 12px #EF4444`

**Card footer** (`flex items-center gap-16 mt-12 pt-12 border-t #F1F5F9`):
- icon `thumb_up 14px #94A3B8` + `"12 người thấy hữu ích" 12px #94A3B8`
- `·`
- Ngày tạo: `12px #94A3B8`

### 4. Pagination

`flex justify-center mt-24`
- Prev · 1 · 2 · Next

### 5. Empty State

`center py-64 text-center`

- SVG icon `rate_review 80px #E2E8F0`
- Title: `"Chưa có đánh giá nào" 18px Inter 600 #1E293B mt-16`
- Subtitle: `"Hãy đặt tour và chia sẻ trải nghiệm của bạn!" 14px #94A3B8 mt-8`
- Button "Khám phá Tour": `bg #FF6B35 text white radius-10 px-24 py-12 14px 600 mt-16`
  → `/tours`

### 6. Modal Sửa đánh giá

**Trigger:** Click button sửa

`Modal center w-500px backdrop rgba(0,0,0,0.5)`

- Header: `"Sửa đánh giá" 18px Inter 600 #1E293B` + button `×`
- Stars selector: 5 stars `32px` clickable · pre-filled với score hiện tại
- Textarea: `rows-4 border #E2E8F0 radius-10 px-14 py-12 14px` pre-filled với comment
  counter `"X/500" 11px #94A3B8 text-right mt-4`
- Ảnh hiện có: `flex gap-8 mt-8`
  - Mỗi ảnh: `60x60px radius-8 object-cover` + nút `×` xóa
- Upload thêm ảnh: `border dashed #E2E8F0 radius-8 p-12 text-center cursor-pointer`
  `"Thêm ảnh" 12px #64748B` icon `add_photo_alternate`
- Footer: "Hủy" (ghost) + "Lưu thay đổi" `bg #0066CC text white radius-10 px-20 py-10`
  → `PUT /ratings/{id}`

### 7. Confirm Xóa đánh giá

`Modal w-400px`

- Header: icon `delete 40x40 bg #FEE2E2 radius-10 color #EF4444`
  + `"Xóa đánh giá này?" 16px 700 #1E293B`
- Body: `"Đánh giá sẽ bị xóa vĩnh viễn." 14px #64748B`
- Footer: "Hủy" (ghost) + "Xóa" `bg #EF4444 hover #DC2626`
  → `DELETE /ratings/{id}`

---

## API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load danh sách | GET | `/user/ratings?page=1&per_page=10` | Khi mount, đổi tab |
| Filter loại | GET | `/user/ratings?type=location` hoặc `?type=tour` | Click tab |
| Sửa đánh giá | PUT | `/ratings/{id}` | Submit modal sửa |
| Xóa đánh giá | DELETE | `/ratings/{id}` | Confirm dialog |
| Upload ảnh | POST | `/upload/images` | Chọn ảnh trong modal |
