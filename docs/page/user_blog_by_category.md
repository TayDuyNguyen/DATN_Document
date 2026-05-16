# Màn hình: Blog theo Danh mục

> Route: `/blog?category_id={id}`
> Quyền: 🌐 Public — không cần đăng nhập
> Mô tả: Danh sách bài viết được lọc theo danh mục. Đây là cùng trang với màn Danh sách Bài viết (`/blog`), chỉ khác ở query param `category_id`.

---

## Tái sử dụng hoàn toàn từ màn Danh sách Bài viết

> Xem chi tiết tại `user_blog_list.md`

Không có sự khác biệt về layout hay component.

---

## Điểm khác biệt duy nhất

### 1. Category Tab active

Tab tương ứng với `category_id` được highlight active:
- `border-b-2 border-#0066CC text #0066CC font-600`
- Tab "Tất cả" không active

### 2. Sidebar — Danh mục active

Item danh mục tương ứng được highlight:
- `bg #EFF6FF` · tên `color #0066CC font-600`

### 3. Result count

Toolbar bên trái:
- `"8 bài viết trong [Tên danh mục]" 14px #64748B`
- Thay vì `"86 bài viết"`

### 4. Featured Post

Bài đầu tiên của danh mục đó (không phải bài đầu tiên toàn bộ blog).

---

## Cách điều hướng đến màn này

| Từ đâu | Action | URL |
|--------|--------|-----|
| Category tabs (blog list) | Click tab | `/blog?category_id=1` |
| Sidebar danh mục (blog list) | Click item | `/blog?category_id=1` |
| Sidebar danh mục (blog detail) | Click item | `/blog?category_id=1` |
| Tags trên bài viết | Click tag | `/blog?category_id=1` |
| Trang chủ | Click "Xem tất cả" danh mục | `/blog?category_id=1` |

---

## API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load bài viết theo danh mục | GET | `/blog?category_id={id}&page=1&per_page=9` | Khi mount với category_id |
| Load danh mục | GET | `/blog/categories` | Khi mount |
| Đổi trang | GET | `/blog?category_id={id}&page=` | Click pagination |

---

## Validation & States

| Hạng mục | Quy tắc |
|---|---|
| Category id | Bắt buộc là số hoặc id hợp lệ từ `GET /blog/categories` |
| Category không tồn tại | Hiển thị 404 category và CTA về `/blog` |
| Empty list | Hiển thị "Chưa có bài viết trong danh mục này" và danh sách danh mục khác |
| Pagination | `page >= 1`; nếu vượt tổng trang, quay về trang cuối hợp lệ |
| SEO | Title/meta lấy theo tên danh mục; fallback "Cẩm nang du lịch Đà Nẵng" |
