# Màn hình User — Xem ảnh đánh giá

> Route UI: modal/lightbox trong chi tiết địa điểm hoặc chi tiết tour  
> Quyền: 🌐 Public xem ảnh đã duyệt; 🔐 User khi thao tác hữu ích/báo cáo nếu có  
> API: `GET /ratings/{id}/images`

---

## Mục tiêu

Cho phép người dùng xem toàn bộ ảnh đính kèm trong một đánh giá mà không phải rời khỏi màn chi tiết địa điểm/tour.

---

## Thành phần giao diện

| Thành phần | Chức năng |
|---|---|
| Thumbnail grid | Hiển thị tối đa 5 ảnh trong card đánh giá |
| Lightbox modal | Xem ảnh lớn, next/previous |
| Counter | Hiển thị `1 / total` |
| Close action | Đóng modal, quay lại vị trí đang đọc |

---

## API Mapping

| Hành động | Method | Endpoint | Trigger |
|---|---|---|---|
| Load ảnh đánh giá | GET | `/ratings/{id}/images` | Click thumbnail hoặc mở lightbox |

---

## Validation & Flow

| Rule | Mô tả |
|---|---|
| Chỉ ảnh hợp lệ | Chỉ hiển thị ảnh thuộc rating tồn tại và được phép xem |
| Empty state | Nếu rating không có ảnh, không hiển thị nút mở lightbox |
| Lỗi tải ảnh | Hiển thị placeholder và cho phép retry |
