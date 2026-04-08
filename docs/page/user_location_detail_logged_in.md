# Màn hình: Chi tiết Địa điểm (Đã đăng nhập)

> Route: `/locations/{slug}`
> Quyền: 🔐 Đã đăng nhập
> Mô tả: Chi tiết địa điểm với thêm tính năng yêu thích và viết đánh giá.

---

## Tái sử dụng từ màn Chi tiết Địa điểm (Chưa đăng nhập)

> Xem chi tiết tại `user_location_detail.md`

Giữ nguyên toàn bộ: gallery, mô tả, tags, tiện ích, bản đồ, địa điểm lân cận, sidebar.

---

## Điểm khác biệt khi đã đăng nhập

---

### 1. Button Yêu thích — Active state

**API khi mount: `GET /user/favorites/check/{location_id}`**

Khi mount trang → gọi API kiểm tra → cập nhật UI:

| Trạng thái | Icon | Style | Action |
|-----------|------|-------|--------|
| Chưa yêu thích | `favorite_border` | `border #E2E8F0 bg white color #94A3B8` | `POST /user/favorites` |
| Đã yêu thích | `favorite` | `border #EF4444 bg #FEE2E2 color #EF4444` | `DELETE /user/favorites/{id}` |

**Sau khi toggle:**
- Thêm: Toast `"Đã thêm vào yêu thích ❤️" bg #FEE2E2 text #EF4444` · icon đổi sang filled
- Xóa: Toast `"Đã xóa khỏi yêu thích" bg #F1F5F9 text #64748B` · icon đổi sang outline

Button yêu thích xuất hiện ở **2 vị trí**:
1. Header bên phải (Section 3.1)
2. Sidebar Card (Section 4.3)

---

### 2. Button Viết đánh giá — Unlock

**API khi mount: `GET /ratings/check?location_id={id}`**

| Trạng thái | Button | Action |
|-----------|--------|--------|
| Chưa đánh giá | `"Viết đánh giá" border #0066CC text #0066CC` | Mở modal viết đánh giá |
| Đã đánh giá | `"Bạn đã đánh giá" border #E2E8F0 text #94A3B8 cursor-not-allowed` | Disabled |

---

### 3. Modal Viết đánh giá (Unlock)

**Chỉ hiển thị khi đã đăng nhập + chưa đánh giá**

`Modal center w-500px backdrop rgba(0,0,0,0.5)`

**Header:** `"Viết đánh giá" 18px Inter 600 #1E293B` + button `×`

**Stars selector:**
`flex gap-8 justify-center my-16`
- 5 stars `36px` clickable
- Hover: fill từ trái → phải `#F59E0B`
- Selected: filled `#F59E0B`
- Label bên dưới: `"Tệ" / "Không tốt" / "Bình thường" / "Tốt" / "Tuyệt vời"` `13px #94A3B8`

**Textarea:**
`rows-4 border #E2E8F0 radius-10 px-14 py-12 14px full-width`
placeholder "Chia sẻ trải nghiệm của bạn về địa điểm này..."
counter `"0/500" 11px #94A3B8 text-right mt-4`

**Upload ảnh:**
`border-2 dashed #E2E8F0 radius-10 p-16 text-center cursor-pointer mt-4`
hover `border #0066CC bg #EFF6FF`
- icon `add_photo_alternate 32px #94A3B8`
- Text `"Thêm ảnh (tối đa 5)" 13px #64748B mt-8`
- Preview grid khi có ảnh: `grid-cols-5 gap-8 mt-8`
  - Mỗi ảnh: `60x60px radius-8 object-cover` + nút `×` xóa
- API: `POST /upload/images`

**Footer:**
`flex justify-end gap-12 mt-16 pt-16 border-t #F1F5F9`
- "Hủy": `border #E2E8F0 bg white text #64748B radius-10 px-20 py-10`
- "Gửi đánh giá": `bg #0066CC text white radius-10 px-20 py-10 14px 600`
  disabled khi chưa chọn sao: `bg #E2E8F0 text #94A3B8`
  → `POST /ratings` · body: `{ location_id, score, comment, images[], booking_id }`

---

### 4. Đánh dấu đánh giá Hữu ích

**Chỉ hiển thị khi đã đăng nhập**

Mỗi review có button:
- Chưa đánh dấu: `"Hữu ích (12)" 12px #94A3B8` icon `thumb_up_outlined`
  hover `text #0066CC`
- Đã đánh dấu: `"Hữu ích (13)" 12px #0066CC` icon `thumb_up` (filled)
- → `POST /ratings/{id}/helpful`

---

## API Mapping (bổ sung)

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Kiểm tra đã yêu thích | GET | `/user/favorites/check/{location_id}` | Khi mount |
| Thêm yêu thích | POST | `/user/favorites` | Click button yêu thích |
| Xóa yêu thích | DELETE | `/user/favorites/{location_id}` | Click button yêu thích (đã thích) |
| Kiểm tra đã đánh giá | GET | `/ratings/check?location_id={id}` | Khi mount |
| Gửi đánh giá | POST | `/ratings` | Submit modal |
| Upload ảnh đánh giá | POST | `/upload/images` | Chọn ảnh trong modal |
| Đánh dấu hữu ích | POST | `/ratings/{id}/helpful` | Click "Hữu ích" |
