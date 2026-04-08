# Màn hình: Chỉnh sửa Bài viết Blog

> Route: `/admin/blog-posts/{id}/edit`
> Quyền: 🛡️ Admin / Staff
> Mô tả: Form chỉnh sửa bài viết blog đã tồn tại. Tái sử dụng toàn bộ layout từ màn Tạo Bài viết.

---

## Tái sử dụng từ màn Tạo Bài viết

> Xem chi tiết tại `admin_blog_posts_create.md`

Giữ nguyên:
- Layout 2 cột (left 65% + right sidebar 320px)
- Field Tiêu đề · Slug · Excerpt · Rich text editor
- Sidebar: Card Xuất bản · Card Danh mục · Card Ảnh đại diện · Card Hướng dẫn
- Design system, màu sắc, spacing

---

## Điểm khác biệt

---

### 1. Page Header

| Element | Tạo | Chỉnh sửa |
|---------|-----|-----------|
| Breadcrumb | ".../ Tạo mới" | ".../ Khám phá Bà Nà Hills / Chỉnh sửa" |
| Title | "Tạo Bài viết mới" | "Chỉnh sửa Bài viết" |
| Subtitle | "Viết và xuất bản..." | Tiêu đề bài viết `14px Inter 500 #64748B` |
| Button Hủy | → `/admin/blog-posts` | → `/admin/blog-posts/{id}` |
| Button phụ | "Lưu nháp" | "Xem bài viết" — icon `open_in_new` → `/blog/{slug}` tab mới |
| Button chính | "Xuất bản" | "Lưu thay đổi" → `PUT /admin/blog-posts/{id}` |

---

### 2. Loading State

Khi fetch `GET /admin/blog-posts/{id}` chưa xong:
- Skeleton loading: tiêu đề `h-8 bg #E2E8F0 radius-8 w-3/4` · editor area `h-400px bg #E2E8F0 radius-10`
- Spinner nhỏ + `"Đang tải bài viết..." 13px #94A3B8`

---

### 3. Form Pre-filled

- Tiêu đề: điền sẵn
- Slug: điền sẵn · khi thay đổi → warning box:
  - `bg #FEF3C7 border rgba(245,158,11,0.3) radius-8 p-10 mt-6`
  - icon `warning_amber #F59E0B` + text `12px #92400E`:
    "Thay đổi slug sẽ làm thay đổi URL bài viết. Các link cũ sẽ không còn hoạt động."
- Excerpt: điền sẵn
- Rich text editor: load nội dung HTML hiện tại
- Danh mục: pre-checked theo categories hiện tại
- Ảnh đại diện: hiển thị ảnh hiện tại (không phải empty upload zone)

---

### 4. Ảnh đại diện Pre-filled

Thay empty upload zone bằng:
- Preview: `full-width h-160px object-cover radius-12`
- Bottom overlay thường trực: `bg rgba(0,0,0,0.5) p-8 radius-b-12`
  - Text `"Ảnh hiện tại" 11px white opacity-70`
  - Button "Thay đổi": `bg white/20 text white border white/30 radius-6 px-10 py-4 12px 600`
    → click mở file picker → `POST /upload/image` → replace

---

### 5. Sidebar — Card "Xuất bản"

- Radio trạng thái: pre-selected theo status hiện tại
- Nếu status=published: hiện thêm info:
  - `"Đã xuất bản lúc: 15/03/2026 09:30" 12px #64748B`
- Nếu status=scheduled: date+time picker pre-filled với `published_at`

**Thêm block "Thông tin"** (trên buttons, `border-t #F1F5F9 pt-16`):
- Label: `"THÔNG TIN" 10px uppercase #94A3B8 mb-8`

| Label | Value |
|-------|-------|
| Ngày tạo | "15/03/2026 09:30" `13px #64748B` |
| Cập nhật | "01/04/2026 14:22" `13px #64748B` |
| Tác giả | "Admin Duy Tây" `13px #64748B` |
| Lượt xem | "2.4K lượt" `13px #0066CC` |

**Buttons:**
| Button | Tạo | Chỉnh sửa |
|--------|-----|-----------|
| Chính | "Xuất bản" | "Lưu thay đổi" |
| Phụ | "Lưu nháp" | "Hủy thay đổi" → confirm nếu có thay đổi chưa lưu |

---

### 6. Sidebar — Card mới: "Thao tác nhanh"

Thêm sau Card Ảnh đại diện:
`bg white border #E2E8F0 radius-16 p-20 mb-16`

Title: `"Thao tác nhanh" 14px Inter 600 #1E293B mb-12`

| Button | Icon | Hover | Action |
|--------|------|-------|--------|
| Xem bài viết | `open_in_new` | `border #0066CC text #0066CC` | `/blog/{slug}` tab mới |
| Nhân bản bài viết | `content_copy` | `border #0066CC text #0066CC` | Confirm → copy → redirect tạo mới pre-filled |
| Xóa bài viết | `delete` | `bg #FEE2E2` | Confirm → `DELETE /admin/blog-posts/{id}` → redirect `/admin/blog-posts` |

Ghost style: `border #E2E8F0 bg white text #64748B radius-10 py-10 full-width 13px 600`
Xóa: `border #FEE2E2 text #EF4444`

---

### 7. Unsaved Changes Guard

Khi navigate away khi có thay đổi chưa lưu:

| Button | Style | Action |
|--------|-------|--------|
| Tiếp tục chỉnh sửa | `bg #0066CC text white radius-10` | Đóng dialog |
| Bỏ thay đổi | `border #E2E8F0 text #64748B` hover `text #EF4444` | Navigate away |

---

### 8. Submit States

| Tình huống | Xử lý |
|-----------|-------|
| Đang lưu | Button disabled · spinner · "Đang lưu..." · `bg #3385D6` |
| Lưu thành công | Toast `bg #D1FAE5 text #10B981` "Cập nhật bài viết thành công!" · ở lại trang edit |
| Thất bại | Toast `bg #FEE2E2 text #EF4444` "Có lỗi xảy ra." |
| Xóa thành công | Toast `bg #D1FAE5 text #10B981` "Đã xóa bài viết." · redirect `/admin/blog-posts` |

---

## API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load bài viết | GET | `/admin/blog-posts/{id}` | Khi mount |
| Load danh mục | GET | `/admin/blog-categories` | Khi mount |
| Upload ảnh đại diện mới | POST | `/upload/image` | Click "Thay đổi" ảnh |
| Upload ảnh inline editor | POST | `/upload/image` | Click icon ảnh trong toolbar |
| Lưu thay đổi | PUT | `/admin/blog-posts/{id}` | Submit form |
| Xóa bài viết | DELETE | `/admin/blog-posts/{id}` | Confirm dialog |

**Body PUT /admin/blog-posts/{id}:** (all optional)
```json
{
  "title": "",
  "content": "",
  "excerpt": "",
  "featured_image": "",
  "category_ids": [],
  "status": "",
  "published_at": ""
}
```
