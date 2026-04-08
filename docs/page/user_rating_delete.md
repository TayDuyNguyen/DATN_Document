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
