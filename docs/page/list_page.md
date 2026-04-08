# Danh sách màn hình — Admin Panel

> Route prefix: `/admin`
> Auth: JWT Bearer Token — role: admin | staff

---

## Sidebar chính thức

```
📊  Bảng điều khiển

🎫  Quản lý Tour
    ├── Danh sách Tour
    ├── Danh mục Tour
    └── Lịch khởi hành

📍  Quản lý Địa điểm
    ├── Danh sách Địa điểm
    └── Danh mục & Danh mục con

🛒  Đơn hàng & Thanh toán
    ├── Đơn hàng
    └── Giao dịch

⭐  Đánh giá

👥  Người dùng

📝  Blog
    ├── Bài viết
    └── Danh mục Blog

🏷️  Tags & Tiện ích

🔔  Thông báo

📬  Liên hệ

📈  Báo cáo
    ├── Đơn hàng
    ├── Doanh thu
    ├── Đánh giá
    └── Người dùng
```

---

## Chi tiết từng màn hình

---

### 1. BẢNG ĐIỀU KHIỂN

| # | Màn hình | Route | Loại | API sử dụng |
|---|----------|-------|------|-------------|
| 1.1 | Tổng quan Dashboard | `/admin/dashboard` | Trang đơn | `GET /admin/dashboard/stats` `GET /admin/dashboard/revenue` `GET /admin/dashboard/booking-trend` `GET /admin/dashboard/user-growth` `GET /admin/dashboard/top-tours` `GET /admin/dashboard/top-locations` `GET /admin/bookings` |

---

### 2. QUẢN LÝ TOUR

| # | Màn hình | Route | Loại | API sử dụng |
|---|----------|-------|------|-------------|
| 2.1 | Danh sách Tour | `/admin/tours` | List + filter + paginate | `GET /tours` `PATCH /admin/tours/{id}/status` `PATCH /admin/tours/{id}/featured` `PATCH /admin/tours/{id}/hot` `DELETE /admin/tours/{id}` |
| 2.2 | Tạo Tour | `/admin/tours/create` | Form | `POST /admin/tours` `GET /tour-categories` `POST /upload/images` |
| 2.3 | Chỉnh sửa Tour | `/admin/tours/{id}/edit` | Form | `GET /tours/{slug}` `PUT /admin/tours/{id}` `POST /upload/images` |
| 2.4 | Chi tiết Tour | `/admin/tours/{id}` | Detail | `GET /tours/{slug}` `GET /tours/{id}/schedules` `GET /tours/{id}/ratings` `GET /tours/{id}/rating-stats` |
| 2.5 | Danh mục Tour | `/admin/tour-categories` | List | `GET /admin/tour-categories` `PATCH /admin/tour-categories/{id}/status` `DELETE /admin/tour-categories/{id}` |
| 2.6 | Tạo Danh mục Tour | `/admin/tour-categories/create` | Form | `POST /admin/tour-categories` |
| 2.7 | Chỉnh sửa Danh mục Tour | `/admin/tour-categories/{id}/edit` | Form | `PUT /admin/tour-categories/{id}` |
| 2.8 | Lịch khởi hành | `/admin/tour-schedules` | List + filter | `GET /admin/tour-schedules` `PATCH /admin/tour-schedules/{id}/status` `DELETE /admin/tour-schedules/{id}` |
| 2.9 | Thêm Lịch khởi hành | `/admin/tours/{id}/schedules/create` | Form | `POST /admin/tours/{id}/schedules` |
| 2.10 | Chỉnh sửa Lịch khởi hành | `/admin/tour-schedules/{id}/edit` | Form | `GET /admin/tour-schedules/{id}` `PUT /admin/tour-schedules/{id}` |

---

### 3. QUẢN LÝ ĐỊA ĐIỂM

| # | Màn hình | Route | Loại | API sử dụng |
|---|----------|-------|------|-------------|
| 3.1 | Danh sách Địa điểm | `/admin/locations` | List + filter + paginate | `GET /locations` `PATCH /admin/locations/{id}/status` `PATCH /admin/locations/{id}/featured` `DELETE /admin/locations/{id}` `GET /admin/locations/export` |
| 3.2 | Tạo Địa điểm | `/admin/locations/create` | Form | `POST /admin/locations` `GET /categories` `GET /tags` `GET /amenities` `POST /upload/images` |
| 3.3 | Chỉnh sửa Địa điểm | `/admin/locations/{id}/edit` | Form | `GET /locations/{slug}` `PUT /admin/locations/{id}` `POST /admin/locations/{id}/tags` `POST /admin/locations/{id}/amenities` `POST /upload/images` |
| 3.4 | Chi tiết Địa điểm | `/admin/locations/{id}` | Detail | `GET /locations/{slug}` `GET /locations/{id}/ratings` `GET /locations/{id}/rating-stats` `GET /locations/{id}/images` |
| 3.5 | Danh mục Địa điểm | `/admin/categories` | List | `GET /categories` `PATCH /admin/categories/{id}/status` `DELETE /admin/categories/{id}` |
| 3.6 | Tạo Danh mục | `/admin/categories/create` | Form | `POST /admin/categories` `POST /upload/image` |
| 3.7 | Chỉnh sửa Danh mục | `/admin/categories/{id}/edit` | Form | `GET /categories/{id}` `PUT /admin/categories/{id}` |
| 3.8 | Danh mục con | `/admin/subcategories` | List (tab trong trang Danh mục) | `GET /categories` `POST /admin/subcategories` `PUT /admin/subcategories/{id}` `DELETE /admin/subcategories/{id}` `PATCH /admin/subcategories/{id}/status` |

---

### 4. ĐƠN HÀNG & THANH TOÁN

| # | Màn hình | Route | Loại | API sử dụng |
|---|----------|-------|------|-------------|
| 4.1 | Danh sách Đơn hàng | `/admin/bookings` | List + filter + paginate | `GET /admin/bookings` `GET /admin/bookings/export` |
| 4.2 | Chi tiết Đơn hàng | `/admin/bookings/{id}` | Detail + actions | `GET /admin/bookings/{id}` `POST /admin/bookings/{id}/confirm` `POST /admin/bookings/{id}/cancel` `POST /admin/bookings/{id}/complete` `PATCH /admin/bookings/{id}/status` |
| 4.3 | Danh sách Giao dịch | `/admin/payments` | List + filter + paginate | `GET /admin/payments` `GET /admin/payments/export` |
| 4.4 | Chi tiết Giao dịch | `/admin/payments/{id}` | Detail + actions | `GET /admin/payments/{id}` `POST /admin/payments/{id}/refund` |

---

### 5. ĐÁNH GIÁ

| # | Màn hình | Route | Loại | API sử dụng |
|---|----------|-------|------|-------------|
| 5.1 | Danh sách Đánh giá | `/admin/ratings` | List + filter + inline actions | `GET /admin/ratings` `PATCH /admin/ratings/{id}/approve` `PATCH /admin/ratings/{id}/reject` `DELETE /admin/ratings/{id}` `GET /admin/ratings/export` |

---

### 6. NGƯỜI DÙNG

| # | Màn hình | Route | Loại | API sử dụng |
|---|----------|-------|------|-------------|
| 6.1 | Danh sách Người dùng | `/admin/users` | List + filter + paginate | `GET /admin/users` `PATCH /admin/users/{id}/status` `PATCH /admin/users/{id}/role` `DELETE /admin/users/{id}` `GET /admin/users/export` |
| 6.2 | Chi tiết Người dùng | `/admin/users/{id}` | Detail | `GET /admin/users/{id}` `GET /admin/users/{id}/bookings` `GET /admin/users/{id}/ratings` |
| 6.3 | Tạo Người dùng | `/admin/users/create` | Form | `POST /admin/users` |
| 6.4 | Chỉnh sửa Người dùng | `/admin/users/{id}/edit` | Form | `PUT /admin/users/{id}` |

---

### 7. BLOG

| # | Màn hình | Route | Loại | API sử dụng |
|---|----------|-------|------|-------------|
| 7.1 | Danh sách Bài viết | `/admin/blog-posts` | List + filter + paginate | `GET /admin/blog-posts` `PATCH /admin/blog-posts/{id}/status` `DELETE /admin/blog-posts/{id}` |
| 7.2 | Tạo Bài viết | `/admin/blog-posts/create` | Form (rich text editor) | `POST /admin/blog-posts` `GET /admin/blog-categories` `POST /upload/image` `POST /upload/images` |
| 7.3 | Chỉnh sửa Bài viết | `/admin/blog-posts/{id}/edit` | Form | `GET /admin/blog-posts/{id}` `PUT /admin/blog-posts/{id}` `POST /upload/image` |
| 7.4 | Danh mục Blog | `/admin/blog-categories` | List | `GET /admin/blog-categories` `POST /admin/blog-categories` `PUT /admin/blog-categories/{id}` `DELETE /admin/blog-categories/{id}` |

---

### 8. TAGS & TIỆN ÍCH

| # | Màn hình | Route | Loại | API sử dụng |
|---|----------|-------|------|-------------|
| 8.1 | Tags | `/admin/tags` | List + inline CRUD (tab 1) | `GET /tags` `POST /admin/tags` `PUT /admin/tags/{id}` `DELETE /admin/tags/{id}` |
| 8.2 | Tiện ích (Amenities) | `/admin/amenities` | List + inline CRUD (tab 2) | `GET /amenities` `POST /admin/amenities` `PUT /admin/amenities/{id}` `DELETE /admin/amenities/{id}` |

> Có thể gộp 2 tab vào 1 trang `/admin/tags-amenities`

---

### 9. THÔNG BÁO

| # | Màn hình | Route | Loại | API sử dụng |
|---|----------|-------|------|-------------|
| 9.1 | Danh sách Thông báo | `/admin/notifications` | List + filter | `GET /admin/notifications` `DELETE /admin/notifications/{id}` |
| 9.2 | Gửi Thông báo | `/admin/notifications/send` | Form | `POST /admin/notifications/send` `POST /admin/notifications/send-all` `GET /admin/users` *(chọn user)* |

---

### 10. LIÊN HỆ

| # | Màn hình | Route | Loại | API sử dụng |
|---|----------|-------|------|-------------|
| 10.1 | Danh sách Liên hệ | `/admin/contacts` | List + filter + paginate | `GET /admin/contacts` `DELETE /admin/contacts/{id}` `GET /admin/contacts/export` |
| 10.2 | Chi tiết & Trả lời | `/admin/contacts/{id}` | Detail + form reply | `GET /admin/contacts/{id}` `POST /admin/contacts/{id}/reply` `DELETE /admin/contacts/{id}` |

---

### 11. BÁO CÁO

| # | Màn hình | Route | Loại | API sử dụng |
|---|----------|-------|------|-------------|
| 11.1 | Báo cáo Đơn hàng | `/admin/reports/bookings` | Chart + table + export | `GET /admin/reports/bookings` `GET /admin/bookings/export` |
| 11.2 | Báo cáo Doanh thu | `/admin/reports/revenue` | Chart + table + export | `GET /admin/reports/revenue-detail` `GET /admin/dashboard/revenue` `GET /admin/payments/export` |
| 11.3 | Báo cáo Đánh giá | `/admin/reports/ratings` | Chart + table + export | `GET /admin/reports/ratings` `GET /admin/ratings/export` |
| 11.4 | Báo cáo Người dùng | `/admin/reports/users` | Chart + export | `GET /admin/reports/users` `GET /admin/users/export` |

---

## Tổng số màn hình

| # | Nhóm | Số màn | Ghi chú |
|---|------|--------|---------|
| 1 | Bảng điều khiển | 1 | |
| 2 | Quản lý Tour | 10 | List · Create · Edit · Detail · Danh mục · Lịch |
| 3 | Quản lý Địa điểm | 8 | List · Create · Edit · Detail · Danh mục · Danh mục con |
| 4 | Đơn hàng & Thanh toán | 4 | Đơn hàng · Giao dịch (mỗi loại: list + detail) |
| 5 | Đánh giá | 1 | List + inline approve/reject |
| 6 | Người dùng | 4 | List · Detail · Create · Edit |
| 7 | Blog | 4 | Bài viết (list/create/edit) · Danh mục |
| 8 | Tags & Tiện ích | 2 | Tags · Amenities (hoặc 1 trang 2 tab) |
| 9 | Thông báo | 2 | List · Gửi thông báo |
| 10 | Liên hệ | 2 | List · Detail/Reply |
| 11 | Báo cáo | 4 | Đơn hàng · Doanh thu · Đánh giá · Người dùng |
| | **Tổng** | **42** | |
