# API List — Dự án Đà Nẵng Trip

> Base URL: `/api/v1`
> Auth: Laravel Sanctum (Bearer Token)
>
> **Ký hiệu:**
> - 🌐 Public — không cần đăng nhập
> - 🔐 User — cần đăng nhập (role: user hoặc admin)
> - 🛡️ Admin — chỉ admin mới truy cập được

---

## AUTH

| Method | Endpoint | Quyền | Mô tả |
|--------|----------|-------|-------|
| POST | `/auth/register` | 🌐 | Đăng ký tài khoản mới |
| POST | `/auth/login` | 🌐 | Đăng nhập, trả về Bearer token |
| POST | `/auth/logout` | 🔐 | Đăng xuất, thu hồi token |
| GET | `/auth/me` | 🔐 | Lấy thông tin user đang đăng nhập |
| POST | `/auth/refresh` | 🔐 | Làm mới token |
| POST | `/auth/forgot-password` | 🌐 | Gửi email reset mật khẩu |
| POST | `/auth/reset-password` | 🌐 | Đặt lại mật khẩu bằng token email |

---

## CATEGORIES & SUBCATEGORIES

| Method | Endpoint | Quyền | Mô tả |
|--------|----------|-------|-------|
| GET | `/categories` | 🌐 | Danh sách tất cả danh mục (kèm subcategories) |
| GET | `/categories/{id}` | 🌐 | Chi tiết 1 danh mục |
| POST | `/admin/categories` | 🛡️ | Tạo danh mục mới |
| PUT | `/admin/categories/{id}` | 🛡️ | Cập nhật danh mục |
| DELETE | `/admin/categories/{id}` | 🛡️ | Xóa danh mục |
| POST | `/admin/subcategories` | 🛡️ | Tạo danh mục con |
| PUT | `/admin/subcategories/{id}` | 🛡️ | Cập nhật danh mục con |
| DELETE | `/admin/subcategories/{id}` | 🛡️ | Xóa danh mục con |

---

## LOCATIONS (Địa điểm)

| Method | Endpoint | Quyền | Mô tả |
|--------|----------|-------|-------|
| GET | `/locations` | 🌐 | Danh sách địa điểm (filter, sort, paginate) |
| GET | `/locations/{slug}` | 🌐 | Chi tiết địa điểm theo slug |
| GET | `/locations/featured` | 🌐 | Danh sách địa điểm nổi bật |
| GET | `/locations/nearby` | 🌐 | Địa điểm gần vị trí hiện tại (lat, lng, radius) |
| GET | `/locations/{id}/ratings` | 🌐 | Danh sách đánh giá của địa điểm |
| POST | `/locations/{id}/view` | 🌐 | Ghi nhận lượt xem (kèm session_id) |
| POST | `/admin/locations` | 🛡️ | Tạo địa điểm mới |
| PUT | `/admin/locations/{id}` | 🛡️ | Cập nhật địa điểm |
| DELETE | `/admin/locations/{id}` | 🛡️ | Xóa địa điểm |
| PATCH | `/admin/locations/{id}/status` | 🛡️ | Đổi trạng thái (active/inactive) |
| PATCH | `/admin/locations/{id}/featured` | 🛡️ | Bật/tắt nổi bật |

> **Query params cho GET /locations:**
> `?category_id=1&district=Hải Châu&price_level=2&sort=avg_rating&order=desc&page=1&per_page=12`

---

## SEARCH (Tìm kiếm)

| Method | Endpoint | Quyền | Mô tả |
|--------|----------|-------|-------|
| GET | `/search` | 🌐 | Tìm kiếm địa điểm theo từ khóa |
| GET | `/search/suggestions` | 🌐 | Gợi ý tìm kiếm (autocomplete) |
| GET | `/search/popular` | 🌐 | Từ khóa tìm kiếm phổ biến |

---

## RATINGS (Đánh giá)

| Method | Endpoint | Quyền | Mô tả |
|--------|----------|-------|-------|
| POST | `/ratings` | 🔐 | Tạo đánh giá mới (trừ point nếu có ảnh) |
| PUT | `/ratings/{id}` | 🔐 | Sửa đánh giá của chính mình |
| DELETE | `/ratings/{id}` | 🔐 | Xóa đánh giá của chính mình |
| POST | `/ratings/{id}/helpful` | 🔐 | Đánh dấu đánh giá hữu ích |
| GET | `/admin/ratings` | 🛡️ | Danh sách đánh giá chờ duyệt / tất cả |
| PATCH | `/admin/ratings/{id}/approve` | 🛡️ | Duyệt đánh giá |
| PATCH | `/admin/ratings/{id}/reject` | 🛡️ | Từ chối đánh giá (kèm lý do) |

---

## FAVORITES (Yêu thích)

| Method | Endpoint | Quyền | Mô tả |
|--------|----------|-------|-------|
| GET | `/user/favorites` | 🔐 | Danh sách địa điểm đã lưu |
| POST | `/user/favorites` | 🔐 | Thêm địa điểm vào yêu thích |
| DELETE | `/user/favorites/{location_id}` | 🔐 | Xóa khỏi yêu thích |

---

## USER PROFILE

| Method | Endpoint | Quyền | Mô tả |
|--------|----------|-------|-------|
| GET | `/user/profile` | 🔐 | Xem thông tin cá nhân |
| PUT | `/user/profile` | 🔐 | Cập nhật thông tin cá nhân |
| POST | `/user/profile/avatar` | 🔐 | Upload ảnh đại diện |
| PUT | `/user/password` | 🔐 | Đổi mật khẩu |
| GET | `/user/ratings` | 🔐 | Lịch sử đánh giá của mình |

---

## POINTS (Điểm thưởng)

| Method | Endpoint | Quyền | Mô tả |
|--------|----------|-------|-------|
| GET | `/user/points` | 🔐 | Số dư point hiện tại |
| GET | `/user/points/transactions` | 🔐 | Lịch sử giao dịch point |
| POST | `/user/points/purchase` | 🔐 | Nạp point (thanh toán) |

---

## NOTIFICATIONS (Thông báo)

| Method | Endpoint | Quyền | Mô tả |
|--------|----------|-------|-------|
| GET | `/user/notifications` | 🔐 | Danh sách thông báo (paginate) |
| PATCH | `/user/notifications/{id}/read` | 🔐 | Đánh dấu đã đọc 1 thông báo |
| PATCH | `/user/notifications/read-all` | 🔐 | Đánh dấu tất cả đã đọc |
| DELETE | `/user/notifications/{id}` | 🔐 | Xóa thông báo |

---

## BLOG

| Method | Endpoint | Quyền | Mô tả |
|--------|----------|-------|-------|
| GET | `/blog` | 🌐 | Danh sách bài viết (paginate) |
| GET | `/blog/{slug}` | 🌐 | Chi tiết bài viết |
| GET | `/blog/categories` | 🌐 | Danh sách danh mục blog |
| POST | `/admin/blog` | 🛡️ | Tạo bài viết mới |
| PUT | `/admin/blog/{id}` | 🛡️ | Cập nhật bài viết |
| DELETE | `/admin/blog/{id}` | 🛡️ | Xóa bài viết |
| PATCH | `/admin/blog/{id}/publish` | 🛡️ | Xuất bản / ẩn bài viết |

---

## ADMIN — USERS

| Method | Endpoint | Quyền | Mô tả |
|--------|----------|-------|-------|
| GET | `/admin/users` | 🛡️ | Danh sách người dùng (filter, search) |
| GET | `/admin/users/{id}` | 🛡️ | Chi tiết người dùng |
| PATCH | `/admin/users/{id}/status` | 🛡️ | Kích hoạt / khóa tài khoản |
| PATCH | `/admin/users/{id}/role` | 🛡️ | Đổi role (user ↔ admin) |
| DELETE | `/admin/users/{id}` | 🛡️ | Xóa tài khoản |

---

## ADMIN — DASHBOARD & REPORTS

| Method | Endpoint | Quyền | Mô tả |
|--------|----------|-------|-------|
| GET | `/admin/dashboard` | 🛡️ | Tổng quan: số user, địa điểm, đánh giá, lượt xem |
| GET | `/admin/reports/locations` | 🛡️ | Thống kê địa điểm theo danh mục, quận |
| GET | `/admin/reports/ratings` | 🛡️ | Thống kê đánh giá theo thời gian |
| GET | `/admin/reports/users` | 🛡️ | Thống kê người dùng mới theo tháng |
| GET | `/admin/reports/points` | 🛡️ | Thống kê giao dịch point |

---

## TAGS & AMENITIES

| Method | Endpoint | Quyền | Mô tả |
|--------|----------|-------|-------|
| GET | `/tags` | 🌐 | Danh sách tất cả tags |
| GET | `/amenities` | 🌐 | Danh sách tất cả tiện ích |
| POST | `/admin/tags` | 🛡️ | Tạo tag mới |
| DELETE | `/admin/tags/{id}` | 🛡️ | Xóa tag |
| POST | `/admin/amenities` | 🛡️ | Tạo tiện ích mới |
| DELETE | `/admin/amenities/{id}` | 🛡️ | Xóa tiện ích |

---

## UPLOAD

| Method | Endpoint | Quyền | Mô tả |
|--------|----------|-------|-------|
| POST | `/upload/image` | 🔐 | Upload ảnh lên Cloudinary, trả về URL |

---

## Tổng kết

| Nhóm | Public 🌐 | User 🔐 | Admin 🛡️ |
|------|-----------|---------|----------|
| Auth | 4 | 3 | — |
| Categories | 2 | — | 6 |
| Locations | 5 | — | 5 |
| Search | 3 | — | — |
| Ratings | — | 4 | 3 |
| Favorites | — | 3 | — |
| Profile | — | 5 | — |
| Points | — | 3 | — |
| Notifications | — | 4 | — |
| Blog | 3 | — | 4 |
| Users | — | — | 5 |
| Dashboard | — | — | 5 |
| Tags & Amenities | 2 | — | 4 |
| Upload | — | 1 | — |
| **Tổng** | **19** | **23** | **32** |
