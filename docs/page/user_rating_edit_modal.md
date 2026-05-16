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

---

## Validation & Flow

| Hạng mục | Quy tắc |
|---|---|
| Quyền sửa | Chỉ chủ đánh giá được sửa; nếu API trả 403 thì đóng modal và hiển thị toast lỗi |
| Score | Bắt buộc từ 1 đến 5 sao |
| Comment | Khuyến nghị tối thiểu 10 ký tự nếu có nhập; trim trước khi submit |
| Ảnh | Tối đa 5 ảnh sau khi cộng ảnh cũ và ảnh mới; chỉ nhận định dạng ảnh hợp lệ |
| Submit | Disable button khi đang upload/submitting để tránh gửi lặp |
| Thành công | Cập nhật lại card đánh giá trong danh sách mà không reload toàn trang |
| Thất bại | Giữ nguyên dữ liệu form, hiển thị lỗi theo field nếu backend trả validation errors |
