# Màn hình: Chi tiết Bài viết Blog

> Route: `/admin/blog-posts/{id}`
> Quyền: 🛡️ Admin / Staff
> Mô tả: Màn hình hiển thị chi tiết bài viết blog, thông tin tác giả, danh mục, số lượt xem và hỗ trợ các thao tác đổi trạng thái nhanh, nhân bản hoặc xóa bài viết.

---

## Bố cục Giao diện

Bố cục trang chia thành 2 phần chính:
- **Trái (Left - 70%):** Banner ảnh đại diện, Tiêu đề bài viết, Slug, Mô tả ngắn (Excerpt), và Khung nội dung HTML đã căn chỉnh Typography.
- **Phải (Right - 30%):** Sidebar chứa khối Thao tác nhanh (Xem thử, Sửa, Nhân bản, Xóa), Khối Trạng thái xuất bản (Đã xuất bản, Bản nháp, Lưu trữ), Tác giả bài viết, và các thông tin Metadata (Lượt xem, Ngày tạo, Ngày cập nhật, Danh mục liên kết).

---

## Chi tiết các Khối Chức năng

### 1. Sticky Header
- Nút quay lại: Quay lại `/admin/blog-posts`.
- Breadcrumb: `Blog / Danh sách bài viết / Chi tiết`.
- Hành động nhanh: Nút "Chỉnh sửa" di chuyển sang trang edit, Trình chọn trạng thái xuất bản, nút "Xem bài viết" mở tab mới.

### 2. Nội dung Bài viết (Left Column)
- **Ảnh đại diện:** Chiều cao `320px` với hiệu ứng zoom nhẹ, bo góc tròn `24px` và phủ gradient mờ. Có hình ảnh fallback nếu bài viết không có ảnh.
- **Tiêu đề:** Font chữ đậm `text-2xl font-black text-slate-900`.
- **Slug Box:** Chứa slug dạng mã hóa URL thân thiện, hỗ trợ nút "Sao chép" (Copy to Clipboard) kèm hiệu ứng thông báo.
- **Mô tả ngắn (Excerpt):** Nằm trong hộp Alert màu xám nhẹ bo tròn, làm nổi bật tóm tắt nội dung.
- **Khung nội dung (HTML Body):** Renders nội dung bài viết dạng HTML, cấu hình tối ưu với các thẻ headings (`h1`, `h2`, `h3`), quotes (`blockquote`), danh sách, bảng biểu và ảnh hiển thị rộng tối đa 100%.

### 3. Sidebar thông tin (Right Column)

#### Card: Thao tác nhanh
- **Xem bài viết:** Icon `open_in_new`. Mở link `http://localhost:3000/blog/{slug}` trên tab mới (chỉ khả dụng khi bài viết đã xuất bản).
- **Chỉnh sửa bài viết:** Chuyển hướng đến màn sửa `/admin/blog-posts/edit/{id}`.
- **Nhân bản:** Copy dữ liệu hiện tại sang màn tạo bài viết mới.
- **Xóa:** Hiển thị Dialog xác nhận xóa vĩnh viễn bài viết.

#### Card: Trạng thái & Metadata
- **Trạng thái:** Nút dropdown đổi trạng thái nhanh trực tiếp ngay trên trang chi tiết (Nháp / Xuất bản / Lưu trữ).
- **Metadata Grid:**
  - Tác giả: Hiển thị avatar và tên đầy đủ tác giả bài viết.
  - Ngày tạo / Ngày cập nhật: Định dạng thời gian rõ ràng `HH:MM DD/MM/YYYY`.
  - Lượt xem: Thống kê số lượt xem thực tế từ backend.
  - Danh mục: Các tag danh mục hiển thị dạng badge màu sắc nổi bật.

---

## Thiết kế trạng thái UI

| Trạng thái | Giao diện | Hành động |
|---|---|---|
| **Đang tải (Loading)** | Hiển thị Skeleton animation mô phỏng chính xác khung xương tiêu đề, ảnh đại diện, nội dung bài viết và sidebar. | Vô hiệu hóa tạm thời các nút bấm. |
| **Không tìm thấy (404)** | Hộp cảnh báo đỏ cao cấp `"Không tìm thấy bài viết"`, nút quay về danh sách. | N/A |
| **Đổi trạng thái thành công** | Toast Sonner thông báo `"Cập nhật trạng thái bài viết thành công"`. | Refresh lại cache TanStack Query để đồng bộ toàn bộ view. |

---

## Đặc tả API Tương tác

| Tên chức năng | Method | Endpoint | Payload |
|---|---|---|---|
| Tải bài viết | GET | `/admin/blog-posts/{id}` | N/A |
| Thay đổi trạng thái | PATCH | `/admin/blog-posts/{id}/status` | `{ "status": "draft\|published\|archived" }` |
| Xóa bài viết | DELETE | `/admin/blog-posts/{id}` | N/A |
