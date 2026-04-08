# Component: Modal Viết đánh giá

> Loại: Modal component (không phải trang riêng)
> Quyền: 🔐 Cần đăng nhập
> Mô tả: Modal viết đánh giá dùng chung cho cả địa điểm và tour.

---

## Xuất hiện tại

| Màn hình | Trigger | Tham chiếu |
|---------|---------|-----------|
| Chi tiết Địa điểm | Click "Viết đánh giá" | `user_location_detail_logged_in.md` Section 3 |
| Chi tiết Tour | Click "Viết đánh giá" | `user_tour_detail.md` Section 3.6 |
| Lịch sử đặt tour | Click "Đánh giá" trên card | `user_bookings_list.md` |

---

## Điều kiện hiển thị

**Trước khi mở modal:**
`GET /ratings/check?location_id={id}` hoặc `GET /ratings/check?tour_id={id}`

| Kết quả | Hành động |
|---------|-----------|
| Chưa đánh giá | Hiện button "Viết đánh giá" → mở modal |
| Đã đánh giá | Button disabled "Bạn đã đánh giá" |
| Chưa đăng nhập | Redirect `/login?redirect=...` |

---

## Modal Layout

`Modal center w-500px backdrop rgba(0,0,0,0.5) radius-16`

**Header** (`flex justify-between items-center p-20 border-b #F1F5F9`):
- Left: `flex items-center gap-12`
  - Thumbnail: `40x40px radius-8 object-cover`
  - Tên địa điểm/tour: `14px Inter 600 #1E293B`
- Right: button `×` `24x24px color #94A3B8` hover `#1E293B`

**Body** (`p-20 space-y-16`):

**Stars selector:**
`flex gap-8 justify-center`
- 5 stars `36px` clickable
- Hover: fill từ trái → phải `#F59E0B`
- Selected: filled `#F59E0B`
- Label bên dưới: `"Tệ" / "Không tốt" / "Bình thường" / "Tốt" / "Tuyệt vời"` `12px #94A3B8`
- Chưa chọn: `"Chọn số sao *" 12px #EF4444`

**Textarea:**
`rows-4 border #E2E8F0 radius-10 px-14 py-12 14px Inter full-width`
placeholder "Chia sẻ trải nghiệm của bạn..."
focus: `border #0066CC`
counter: `"0/500" 11px #94A3B8 text-right mt-4`

**Upload ảnh** (tối đa 5):
`border-2 dashed #E2E8F0 radius-10 p-14 text-center cursor-pointer`
hover `border #0066CC bg #EFF6FF`
- icon `add_photo_alternate 28px #94A3B8`
- Text `"Thêm ảnh (tối đa 5)" 12px #64748B mt-6`

Preview grid khi có ảnh: `grid-cols-5 gap-8 mt-8`
- Mỗi ảnh: `60x60px radius-8 object-cover relative`
  - Nút `×`: `absolute top-2 right-2 w-16 h-16 bg rgba(0,0,0,0.5) rounded-full text white 10px`

**Footer** (`flex justify-end gap-12 p-20 border-t #F1F5F9`):
- "Hủy": `border #E2E8F0 bg white text #64748B radius-10 px-20 py-10`
- "Gửi đánh giá": `bg #0066CC text white radius-10 px-20 py-10 14px 600`
  disabled khi chưa chọn sao: `bg #E2E8F0 text #94A3B8 cursor-not-allowed`

---

## Submit States

| Tình huống | Xử lý |
|-----------|-------|
| Đang gửi | Button disabled · spinner |
| Thành công | Đóng modal · Toast `"Đánh giá đã được gửi và đang chờ duyệt" bg #D1FAE5 text #10B981` · Cập nhật UI button → "Bạn đã đánh giá" |
| Thất bại | Toast `bg #FEE2E2 text #EF4444` "Có lỗi xảy ra." |

---

## API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Kiểm tra đã đánh giá | GET | `/ratings/check?location_id=` hoặc `?tour_id=` | Khi mount trang chứa modal |
| Upload ảnh | POST | `/upload/images` | Chọn ảnh |
| Gửi đánh giá | POST | `/ratings` | Submit modal |

**Body POST /ratings:**
```json
{
  "score": "*",
  "comment": "",
  "images": [],
  "location_id": "hoặc",
  "tour_id": "*",
  "booking_id": ""
}
```
