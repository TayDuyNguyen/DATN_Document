# Component: Modal Sửa đánh giá

> Loại: Modal component (không phải trang riêng)
> Quyền: 🔐 Cần đăng nhập
> Mô tả: Modal sửa đánh giá đã viết — pre-filled với dữ liệu hiện tại.

---

## Xuất hiện tại

| Màn hình | Trigger | Tham chiếu |
|---------|---------|-----------|
| Đánh giá của tôi | Click icon `edit` trên card | `user_my_ratings.md` Section 6 |

---

## Khác biệt so với Modal Viết đánh giá

> Xem chi tiết modal tại `user_rating_modal.md`

| Điểm | Viết mới | Sửa |
|------|---------|-----|
| Header title | "Viết đánh giá" | "Sửa đánh giá" |
| Stars | Trống | Pre-filled với score hiện tại |
| Textarea | Trống | Pre-filled với comment hiện tại |
| Ảnh | Trống | Hiển thị ảnh hiện có + upload thêm |
| Button submit | "Gửi đánh giá" | "Lưu thay đổi" |
| API | `POST /ratings` | `PUT /ratings/{id}` |

---

## API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Lưu thay đổi | PUT | `/ratings/{id}` | Submit modal |
| Upload ảnh thêm | POST | `/upload/images` | Chọn ảnh mới |
