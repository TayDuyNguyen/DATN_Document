# API List — Dự án Đà Nẵng Trip

> Base URL: `/api/v1`
> Auth: Laravel Sanctum (Bearer Token)
>
> **Ký hiệu:**
> - 🌐 Public — không cần đăng nhập
> - 🔐 User — cần đăng nhập (role: user hoặc admin)
> - 🛡️ Admin — chỉ admin mới truy cập được
> - `*` = bắt buộc
> - **Bảng chính** = bảng bị đọc/ghi trực tiếp | *bảng phụ* = bảng join/liên quan

---

## AUTH
> 🌿 Branch: `feat/taynd/api-auth`
> 💬 `feat(auth): register, login, logout, refresh token, forgot/reset password via email`

| Method | Endpoint | Quyền | Mô tả | Request | Bảng DB |
|--------|----------|-------|-------|---------|---------|
| POST | `/auth/register` | 🌐 | Đăng ký tài khoản mới | body: `username`* `email`* `password`* `password_confirmation`* `full_name`* | **users** (INSERT) |
| POST | `/auth/login` | 🌐 | Đăng nhập, trả về Bearer token | body: `email`* `password`* | **users** (SELECT) |
| POST | `/auth/logout` | 🔐 | Đăng xuất, thu hồi token | header: `Authorization: Bearer {token}` | **personal_access_tokens** (DELETE) |
| GET | `/auth/me` | 🔐 | Lấy thông tin user đang đăng nhập | header: `Authorization: Bearer {token}` | **users** (SELECT) |
| POST | `/auth/refresh` | 🔐 | Làm mới token | header: `Authorization: Bearer {token}` | **personal_access_tokens** (UPDATE) |
| POST | `/auth/forgot-password` | 🌐 | Gửi email reset mật khẩu | body: `email`* | **users** (SELECT), **password_reset_tokens** (INSERT) |
| POST | `/auth/reset-password` | 🌐 | Đặt lại mật khẩu bằng token email | body: `token`* `email`* `password`* `password_confirmation`* | **users** (UPDATE), **password_reset_tokens** (DELETE) |

---

## CATEGORIES & SUBCATEGORIES
> 🌿 Branch: `feat/taynd/api-categories`
> 💬 `feat(categories): CRUD categories & subcategories, admin only write, public read`

| Method | Endpoint | Quyền | Mô tả | Request | Bảng DB |
|--------|----------|-------|-------|---------|---------|
| GET | `/categories` | 🌐 | Danh sách tất cả danh mục (kèm subcategories) | — | **categories** (SELECT), *subcategories* (JOIN) |
| GET | `/categories/{id}` | 🌐 | Chi tiết 1 danh mục | path: `id` | **categories** (SELECT), *subcategories* (JOIN) |
| POST | `/admin/categories` | 🛡️ | Tạo danh mục mới | body: `name`* `slug`* `icon` `description` `image` `sort_order` `status` | **categories** (INSERT) |
| PUT | `/admin/categories/{id}` | 🛡️ | Cập nhật danh mục | path: `id`, body: *(same as POST, all optional)* | **categories** (UPDATE) |
| DELETE | `/admin/categories/{id}` | 🛡️ | Xóa danh mục | path: `id` | **categories** (DELETE), *subcategories*, *locations* (CHECK FK) |
| POST | `/admin/subcategories` | 🛡️ | Tạo danh mục con | body: `category_id`* `name`* `slug`* `description` `sort_order` `status` | **subcategories** (INSERT), *categories* (CHECK FK) |
| PUT | `/admin/subcategories/{id}` | 🛡️ | Cập nhật danh mục con | path: `id`, body: *(same as POST, all optional)* | **subcategories** (UPDATE) |
| DELETE | `/admin/subcategories/{id}` | 🛡️ | Xóa danh mục con | path: `id` | **subcategories** (DELETE), *locations* (CHECK FK) |

---

## LOCATIONS (Địa điểm)
> 🌿 Branch: `feat/taynd/api-locations`
> 💬 `feat(locations): list/detail/featured/nearby, track views, admin CRUD & toggle status/featured`

| Method | Endpoint | Quyền | Mô tả | Request | Bảng DB |
|--------|----------|-------|-------|---------|---------|
| GET | `/locations` | 🌐 | Danh sách địa điểm (filter, sort, paginate) | `?category_id &subcategory_id &district &price_level &sort &order &page &per_page` | **locations** (SELECT), *categories*, *subcategories* (JOIN) |
| GET | `/locations/{slug}` | 🌐 | Chi tiết địa điểm theo slug | path: `slug` | **locations** (SELECT), *categories*, *subcategories*, *tags*, *amenities* (JOIN) |
| GET | `/locations/featured` | 🌐 | Danh sách địa điểm nổi bật | `?limit` (default: 8) | **locations** (SELECT WHERE is_featured=1) |
| GET | `/locations/nearby` | 🌐 | Địa điểm gần vị trí hiện tại | `?lat`* `&lng`* `&radius` (km, default: 5) | **locations** (SELECT, tính khoảng cách theo lat/lng) |
| GET | `/locations/{id}/ratings` | 🌐 | Danh sách đánh giá của địa điểm | path: `id`, `?page &per_page` | **ratings** (SELECT), *users* (JOIN), *rating_images* (JOIN) |
| POST | `/locations/{id}/view` | 🌐 | Ghi nhận lượt xem | path: `id`, body: `session_id` | **views** (INSERT), **locations** (UPDATE view_count) |
| POST | `/admin/locations` | 🛡️ | Tạo địa điểm mới | body: `name`* `category_id`* `address`* `district`* `latitude`* `longitude`* `subcategory_id slug description short_description phone email website opening_hours price_min price_max price_level thumbnail images video_url status is_featured` | **locations** (INSERT), *categories*, *subcategories* (CHECK FK) |
| PUT | `/admin/locations/{id}` | 🛡️ | Cập nhật địa điểm | path: `id`, body: *(same as POST, all optional)* | **locations** (UPDATE) |
| DELETE | `/admin/locations/{id}` | 🛡️ | Xóa địa điểm | path: `id` | **locations** (DELETE), *ratings*, *favorites*, *views*, *location_tags*, *location_amenities* (CASCADE) |
| PATCH | `/admin/locations/{id}/status` | 🛡️ | Đổi trạng thái (active/inactive) | path: `id`, body: `status`* (`active`\|`inactive`) | **locations** (UPDATE status) |
| PATCH | `/admin/locations/{id}/featured` | 🛡️ | Bật/tắt nổi bật | path: `id`, body: `is_featured`* (bool) | **locations** (UPDATE is_featured) |

---

## SEARCH (Tìm kiếm)
> 🌿 Branch: `feat/taynd/api-search`
> 💬 `feat(search): full-text search, autocomplete suggestions, popular keywords`

| Method | Endpoint | Quyền | Mô tả | Request | Bảng DB |
|--------|----------|-------|-------|---------|---------|
| GET | `/search` | 🌐 | Tìm kiếm địa điểm theo từ khóa | `?q`* `&category_id &subcategory_id &district &price_level &price_min &price_max &rating_min &tag &sort &order &page &per_page` (max: 100) `&session_id` | **locations** (SELECT FULLTEXT), *categories*, *subcategories*, *tags* (JOIN), **search_logs** (INSERT) |
| GET | `/search/suggestions` | 🌐 | Gợi ý tìm kiếm (autocomplete) | `?q`* `&limit` (default: 5, max: 20) | **locations** (SELECT LIKE name) |
| GET | `/search/popular` | 🌐 | Từ khóa tìm kiếm phổ biến | `?limit` (default: 10, max: 50) `&days` (default: 30) | **search_logs** (SELECT GROUP BY query, ORDER BY count) |

---

## RATINGS (Đánh giá)
> 🌿 Branch: `feat/taynd/api-ratings`
> 💬 `feat(ratings): user submit/edit/delete review, mark helpful, admin approve/reject with point deduction`

| Method | Endpoint | Quyền | Mô tả | Request | Bảng DB |
|--------|----------|-------|-------|---------|---------|
| POST | `/ratings` | 🔐 | Tạo đánh giá mới (trừ point nếu có ảnh) | body: `location_id`* `score`* (1-5) `comment` `images[]` (max 5 files) | **ratings** (INSERT), *rating_images* (INSERT nếu có ảnh), *locations* (CHECK FK) |
| PUT | `/ratings/{id}` | 🔐 | Sửa đánh giá của chính mình | path: `id`, body: `score` `comment` `images[]` | **ratings** (UPDATE), *rating_images* (INSERT/DELETE) |
| DELETE | `/ratings/{id}` | 🔐 | Xóa đánh giá của chính mình | path: `id` | **ratings** (DELETE), *rating_images* (CASCADE), *locations* (UPDATE avg_rating, review_count) |
| POST | `/ratings/{id}/helpful` | 🔐 | Đánh dấu đánh giá hữu ích | path: `id` | **ratings** (UPDATE helpful_count) |
| GET | `/admin/ratings` | 🛡️ | Danh sách đánh giá chờ duyệt / tất cả | `?status` (`pending`\|`approved`\|`rejected`) `&location_id &page &per_page` | **ratings** (SELECT), *users*, *locations*, *rating_images* (JOIN) |
| PATCH | `/admin/ratings/{id}/approve` | 🛡️ | Duyệt đánh giá | path: `id` | **ratings** (UPDATE status, approved_by, approved_at), **locations** (UPDATE avg_rating, review_count), **users** (UPDATE point_balance), **point_transactions** (INSERT), **notifications** (INSERT) |
| PATCH | `/admin/ratings/{id}/reject` | 🛡️ | Từ chối đánh giá (kèm lý do) | path: `id`, body: `rejected_reason`* | **ratings** (UPDATE status, rejected_reason), **notifications** (INSERT) |

---

## FAVORITES (Yêu thích)
> 🌿 Branch: `feat/taynd/api-favorites`
> 💬 `feat(favorites): user save/unsave locations, list saved locations`

| Method | Endpoint | Quyền | Mô tả | Request | Bảng DB |
|--------|----------|-------|-------|---------|---------|
| GET | `/user/favorites` | 🔐 | Danh sách địa điểm đã lưu | `?page &per_page` | **favorites** (SELECT), *locations*, *categories* (JOIN) |
| POST | `/user/favorites` | 🔐 | Thêm địa điểm vào yêu thích | body: `location_id`* | **favorites** (INSERT), **locations** (UPDATE favorite_count) |
| DELETE | `/user/favorites/{location_id}` | 🔐 | Xóa khỏi yêu thích | path: `location_id` | **favorites** (DELETE), **locations** (UPDATE favorite_count) |

---

## USER PROFILE
> 🌿 Branch: `feat/taynd/api-user-profile`
> 💬 `feat(profile): view/update profile, upload avatar, change password, rating history`

| Method | Endpoint | Quyền | Mô tả | Request | Bảng DB |
|--------|----------|-------|-------|---------|---------|
| GET | `/user/profile` | 🔐 | Xem thông tin cá nhân | — | **users** (SELECT) |
| PUT | `/user/profile` | 🔐 | Cập nhật thông tin cá nhân | body: `full_name` `phone` `birthdate` `gender` `city` | **users** (UPDATE) |
| POST | `/user/profile/avatar` | 🔐 | Upload ảnh đại diện | body: `avatar`* (file, image/jpeg\|png, max 2MB) | **users** (UPDATE avatar) |
| PUT | `/user/password` | 🔐 | Đổi mật khẩu | body: `current_password`* `password`* `password_confirmation`* | **users** (UPDATE password) |
| GET | `/user/ratings` | 🔐 | Lịch sử đánh giá của mình | `?status` (`pending`\|`approved`\|`rejected`) `&page &per_page` | **ratings** (SELECT), *locations*, *rating_images* (JOIN) |

---

## POINTS (Điểm thưởng)
> 🌿 Branch: `feat/taynd/api-points`
> 💬 `feat(points): check balance, transaction history, purchase points`

| Method | Endpoint | Quyền | Mô tả | Request | Bảng DB |
|--------|----------|-------|-------|---------|---------|
| GET | `/user/points` | 🔐 | Số dư point hiện tại | — | **users** (SELECT point_balance) |
| GET | `/user/points/transactions` | 🔐 | Lịch sử giao dịch point | `?type` (`purchase`\|`spend`\|`bonus`\|`refund`) `&page &per_page` | **point_transactions** (SELECT) |
| POST | `/user/points/purchase` | 🔐 | Nạp point (thanh toán) | body: `amount`* (số point) `payment_method`* (`momo`\|`vnpay`\|`bank`) | **point_transactions** (INSERT), **users** (UPDATE point_balance) |

---

## NOTIFICATIONS (Thông báo)
> 🌿 Branch: `feat/taynd/api-notifications`
> 💬 `feat(notifications): list, mark read, mark all read, delete notification`

| Method | Endpoint | Quyền | Mô tả | Request | Bảng DB |
|--------|----------|-------|-------|---------|---------|
| GET | `/user/notifications` | 🔐 | Danh sách thông báo (paginate) | `?is_read` (bool) `&page &per_page` | **notifications** (SELECT) |
| PATCH | `/user/notifications/{id}/read` | 🔐 | Đánh dấu đã đọc 1 thông báo | path: `id` | **notifications** (UPDATE is_read, read_at) |
| PATCH | `/user/notifications/read-all` | 🔐 | Đánh dấu tất cả đã đọc | — | **notifications** (UPDATE WHERE user_id AND is_read=0) |
| DELETE | `/user/notifications/{id}` | 🔐 | Xóa thông báo | path: `id` | **notifications** (DELETE) |

---

## BLOG
> 🌿 Branch: `feat/taynd/api-blog`
> 💬 `feat(blog): public list/detail/categories, admin CRUD & publish/unpublish posts`

| Method | Endpoint | Quyền | Mô tả | Request | Bảng DB |
|--------|----------|-------|-------|---------|---------|
| GET | `/blog` | 🌐 | Danh sách bài viết (paginate) | `?category_id &page &per_page` | **blog_posts** (SELECT), *users*, *blog_categories* (JOIN) |
| GET | `/blog/{slug}` | 🌐 | Chi tiết bài viết | path: `slug` | **blog_posts** (SELECT, UPDATE view_count), *users*, *blog_categories* (JOIN) |
| GET | `/blog/categories` | 🌐 | Danh sách danh mục blog | — | **blog_categories** (SELECT) |
| POST | `/admin/blog` | 🛡️ | Tạo bài viết mới | body: `title`* `content`* `excerpt` `featured_image` `category_ids[]` `status` (`draft`\|`published`) `published_at` | **blog_posts** (INSERT), **blog_post_categories** (INSERT) |
| PUT | `/admin/blog/{id}` | 🛡️ | Cập nhật bài viết | path: `id`, body: *(same as POST, all optional)* | **blog_posts** (UPDATE), *blog_post_categories* (SYNC) |
| DELETE | `/admin/blog/{id}` | 🛡️ | Xóa bài viết | path: `id` | **blog_posts** (DELETE), *blog_post_categories* (CASCADE) |
| PATCH | `/admin/blog/{id}/publish` | 🛡️ | Xuất bản / ẩn bài viết | path: `id`, body: `status`* (`published`\|`draft`) | **blog_posts** (UPDATE status, published_at) |

---

## ADMIN — USERS
> 🌿 Branch: `feat/taynd/api-admin-users`
> 💬 `feat(admin/users): list, detail, toggle status/role, delete user accounts`

| Method | Endpoint | Quyền | Mô tả | Request | Bảng DB |
|--------|----------|-------|-------|---------|---------|
| GET | `/admin/users` | 🛡️ | Danh sách người dùng (filter, search) | `?q` (search name/email) `&role` (`user`\|`admin`) `&status` (`active`\|`banned`) `&page &per_page` | **users** (SELECT) |
| GET | `/admin/users/{id}` | 🛡️ | Chi tiết người dùng | path: `id` | **users** (SELECT), *ratings*, *point_transactions* (COUNT) |
| PATCH | `/admin/users/{id}/status` | 🛡️ | Kích hoạt / khóa tài khoản | path: `id`, body: `status`* (`active`\|`banned`) | **users** (UPDATE status) |
| PATCH | `/admin/users/{id}/role` | 🛡️ | Đổi role (user ↔ admin) | path: `id`, body: `role`* (`user`\|`admin`) | **users** (UPDATE role) |
| DELETE | `/admin/users/{id}` | 🛡️ | Xóa tài khoản | path: `id` | **users** (DELETE), *ratings*, *favorites*, *notifications*, *point_transactions* (CASCADE) |

---

## ADMIN — DASHBOARD & REPORTS
> 🌿 Branch: `feat/taynd/api-admin-dashboard`
> 💬 `feat(admin/dashboard): overview stats, reports by locations/ratings/users/points`

| Method | Endpoint | Quyền | Mô tả | Request | Bảng DB |
|--------|----------|-------|-------|---------|---------|
| GET | `/admin/dashboard` | 🛡️ | Tổng quan: số user, địa điểm, đánh giá, lượt xem | — | **users**, **locations**, **ratings**, **views** (SELECT COUNT) |
| GET | `/admin/reports/locations` | 🛡️ | Thống kê địa điểm theo danh mục, quận | `?from` (date) `&to` (date) | **locations** (SELECT GROUP BY category_id, district), *categories* (JOIN) |
| GET | `/admin/reports/ratings` | 🛡️ | Thống kê đánh giá theo thời gian | `?from &to &status` | **ratings** (SELECT GROUP BY DATE, status) |
| GET | `/admin/reports/users` | 🛡️ | Thống kê người dùng mới theo tháng | `?year` (default: năm hiện tại) | **users** (SELECT GROUP BY MONTH(created_at)) |
| GET | `/admin/reports/points` | 🛡️ | Thống kê giao dịch point | `?from &to &type` | **point_transactions** (SELECT GROUP BY type, DATE) |

---

## TAGS & AMENITIES
> 🌿 Branch: `feat/taynd/api-tags-amenities`
> 💬 `feat(tags/amenities): public list, admin create/delete tags and amenities`

| Method | Endpoint | Quyền | Mô tả | Request | Bảng DB |
|--------|----------|-------|-------|---------|---------|
| GET | `/tags` | 🌐 | Danh sách tất cả tags | `?type` (`cuisine`\|`service`\|`feature`\|`atmosphere`) | **tags** (SELECT) |
| GET | `/amenities` | 🌐 | Danh sách tất cả tiện ích | `?category` (`connectivity`\|`parking`\|`comfort`\|`payment`) | **amenities** (SELECT) |
| POST | `/admin/tags` | 🛡️ | Tạo tag mới | body: `name`* `slug`* `type` | **tags** (INSERT) |
| DELETE | `/admin/tags/{id}` | 🛡️ | Xóa tag | path: `id` | **tags** (DELETE), *location_tags* (CASCADE) |
| POST | `/admin/amenities` | 🛡️ | Tạo tiện ích mới | body: `name`* `icon` `category` | **amenities** (INSERT) |
| DELETE | `/admin/amenities/{id}` | 🛡️ | Xóa tiện ích | path: `id` | **amenities** (DELETE), *location_amenities* (CASCADE) |

---

## UPLOAD
> 🌿 Branch: `feat/taynd/api-upload`
> 💬 `feat(upload): upload image/multiple images to Cloudinary, delete image`
> 📝 Cloudinary trả về URL public trực tiếp — frontend dùng URL để hiển thị, không cần proxy qua backend

| Method | Endpoint | Quyền | Mô tả | Request | Bảng DB |
|--------|----------|-------|-------|---------|---------|
| POST | `/upload/image` | 🔐 | Upload 1 ảnh lên Cloudinary, trả về URL | body: `image`* (file, image/jpeg\|png\|webp, max 5MB) `folder` (cloudinary folder) | — |
| POST | `/upload/images` |  | Upload nhiều ảnh cùng lúc (max 10 files) | body: `images[]`* (files, image/jpeg\|png\|webp, mỗi file max 5MB) `folder` | — |
| DELETE | `/upload/image` | 🔐 | Xóa ảnh khỏi Cloudinary theo public_id | body: `public_id`* (Cloudinary public_id) | — |

---

## IMAGES (Hình ảnh theo đối tượng)
> 🌿 Branch: `feat/taynd/api-upload`
> 💬 Lấy danh sách URL ảnh đã lưu trong DB để hiển thị gallery

| Method | Endpoint | Quyền | Mô tả | Request | Bảng DB |
|--------|----------|-------|-------|---------|---------|
| GET | `/locations/{id}/images` | 🌐 | Danh sách ảnh của địa điểm (thumbnail + images[]) | path: `id` | **locations** (SELECT thumbnail, images) |
| GET | `/ratings/{id}/images` | 🌐 | Danh sách ảnh trong bài đánh giá | path: `id` | **rating_images** (SELECT WHERE rating_id, ORDER BY sort_order) |
| GET | `/admin/upload/images` |  | Danh sách ảnh đã upload theo folder trên Cloudinary | `?folder` `&page &per_page` |  *(Cloudinary Admin API)* |

---

## Tổng kết

| Nhóm | Public  | User  | Admin  | Branch |
|------|-----------|---------|----------|--------|
| Auth | 4 | 3 |  | `feat/taynd/api-auth` |
| Categories | 4 |  | 6 | `feat/taynd/api-categories` |
| Locations | 7 |  | 9 | `feat/taynd/api-locations` |
| Search | 3 |  |  | `feat/taynd/api-search` |
| Ratings |  | 4 | 5 | `feat/taynd/api-ratings` |
| Favorites |  | 3 |  | `feat/taynd/api-favorites` |
| Profile |  | 5 |  | `feat/taynd/api-user-profile` |
| Points |  | 3 |  | `feat/taynd/api-points` |
| Notifications |  | 4 |  | `feat/taynd/api-notifications` |
| Blog | 3 |  | 7 | `feat/taynd/api-blog` |
| Users |  |  | 5 | `feat/taynd/api-admin-users` |
| Dashboard |  |  | 5 | `feat/taynd/api-admin-dashboard` |
| Tags & Amenities | 2 |  | 4 | `feat/taynd/api-tags-amenities` |
| Upload |  | 3 |  | `feat/taynd/api-upload` |
| Images | 2 |  | 1 | `feat/taynd/api-upload` |
| **Tổng** | **25** | **25** | **42** | |
