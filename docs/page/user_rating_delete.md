# Component: Xóa đánh giá (Confirm Dialog)

> Loại: Confirm dialog (không phải trang riêng)
> Quyền: 🔐 Cần đăng nhập
> Mô tả: Dialog xác nhận xóa đánh giá đã viết.

---

## Xuất hiện tại

| Màn hình | Trigger | Tham chiếu |
|---------|---------|-----------|
| Đánh giá của tôi | Click icon `delete` trên card | `user_my_ratings.md` Section 7 |

---

## Dialog

`Modal w-400px backdrop rgba(0,0,0,0.4)`

- Header: icon `delete 40x40 bg #FEE2E2 radius-10 color #EF4444`
  + `"Xóa đánh giá này?" 16px 700 #1E293B`
- Body: `"Đánh giá sẽ bị xóa vĩnh viễn." 14px #64748B`
- Footer:
  - "Hủy": ghost
  - "Xóa": `bg #EF4444 text white radius-10 px-20 py-10` hover `#DC2626`
    → `DELETE /ratings/{id}` → xóa card khỏi list với animation

---

## API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Xóa đánh giá | DELETE | `/ratings/{id}` | Confirm dialog |

---

## Validation & Flow

| Hạng mục | Quy tắc |
|---|---|
| Quyền xóa | Chỉ chủ đánh giá được xóa; admin xóa dùng endpoint admin riêng nếu có |
| Confirm | Bắt buộc confirm trước khi gọi API; không xóa trực tiếp từ click đầu tiên |
| Optimistic update | Có thể ẩn card tạm thời nhưng phải rollback nếu API lỗi |
| Thành công | Xóa card khỏi danh sách, cập nhật tổng số đánh giá/rating stats nếu đang ở detail |
| Thất bại | Hiển thị toast lỗi, giữ card đánh giá nguyên trạng |
| Đánh giá đã bị xóa | Nếu API trả 404, remove card khỏi UI và thông báo dữ liệu đã thay đổi |
