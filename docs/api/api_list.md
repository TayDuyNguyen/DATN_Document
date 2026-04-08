# API List — Dự án Đà Nẵng Trip

> Base URL: `/api/v1`
> Auth: JWT Bearer Token (tymon/jwt-auth)
>
> **Ký hiệu:**
> - 🌐 Public — không cần đăng nhập
> - 🔐 User — cần đăng nhập (role: user hoặc admin)
> - 🛡️ Admin — chỉ admin/staff mới truy cập được
> - `*` = bắt buộc
> - **Bảng chính** = bảng bị đọc/ghi trực tiếp | *bảng phụ* = bảng join/liên quan

---

## AUTH
> 🌿 Branch: `feat/taynd/api-auth`
> 💬 `feat(auth): register, login, logout, refresh token, forgot/reset password via email`
> 🧪 Test: `python tests/scripts/test_auth.py`

| Method | Endpoint | Quyền | Mô tả | Request | Bảng DB |
|--------|----------|-------|-------|---------|---------|
| POST | `/auth/register` | 🌐 | Đăng ký tài khoản mới | body: `username`* `email`* `password`* `password_confirmation`* `full_name`* | **users** (INSERT) |
| POST | `/auth/login` | 🌐 | Đăng nhập, trả về JWT token | body: `email`* `password`* | **users** (SELECT) |
| POST | `/auth/logout` | 🔐 | Đăng xuất, thu hồi token | header: `Authorization: Bearer {token}` | — (JWT blacklist) |
| GET | `/auth/me` | 🔐 | Lấy thông tin user đang đăng nhập | header: `Authorization: Bearer {token}` | **users** (SELECT) |
| POST | `/auth/refresh` | 🔐 | Làm mới JWT token | header: `Authorization: Bearer {token}` | — (JWT refresh) |
| POST | `/auth/forgot-password` | 🌐 | Gửi email reset mật khẩu | body: `email`* | **users** (SELECT), **password_reset_tokens** (INSERT) |
| POST | `/auth/reset-password` | 🌐 | Đặt lại mật khẩu bằng token email | body: `token`* `email`* `password`* `password_confirmation`* | **users** (UPDATE), **password_reset_tokens** (DELETE) |
| POST | `/auth/verify-email` | 🔐 | Xác thực email bằng OTP/token | body: `token`* | **users** (UPDATE email_verified_at) |
| POST | `/auth/resend-verification` | 🔐 | Gửi lại email xác thực | — | **users** (SELECT), *(send mail)* |
---

## CATEGORIES & SUBCATEGORIES
> 🌿 Branch: `feat/taynd/api-categories`
> 💬 `feat(categories): CRUD categories & subcategories, admin only write, public read`
> 🧪 Test: `python tests/scripts/test_categories.py`

| Method | Endpoint | Quyền | Mô tả | Request | Bảng DB |
|--------|----------|-------|-------|---------|---------|
| GET | `/categories` | 🌐 | Danh sách tất cả danh mục (kèm subcategories) | — | **categories** (SELECT), *subcategories* (JOIN) |
| GET | `/categories/{id}` | 🌐 | Chi tiết 1 danh mục | path: `id` | **categories** (SELECT), *subcategories* (JOIN) |
| GET | `/categories/{slug}/locations` | 🌐 | Địa điểm theo danh mục | path: `slug`, `?page &per_page &sort &order` | **locations** (SELECT WHERE category slug), *categories* (JOIN) |
| GET | `/districts` | 🌐 | Danh sách quận (dùng để lọc) | — | *(static: Hải Châu, Sơn Trà, Ngũ Hành Sơn, Cẩm Lệ, Thanh Khê, Liên Chiểu)* |
| POST | `/admin/categories` | 🛡️ | Tạo danh mục mới | body: `name`* `slug` `icon` `description` `image` `sort_order` `status` | **categories** (INSERT) |
| PUT | `/admin/categories/{id}` | 🛡️ | Cập nhật danh mục | path: `id`, body: *(same as POST, all optional)* | **categories** (UPDATE) |
| DELETE | `/admin/categories/{id}` | 🛡️ | Xóa danh mục | path: `id` | **categories** (DELETE), *subcategories*, *locations* (CHECK FK) |
| PATCH | `/admin/categories/{id}/status` | 🛡️ | Đổi trạng thái | path: `id`, body: `status`* (`active`\|`inactive`) | **categories** (UPDATE status) |
| POST | `/admin/subcategories` | 🛡️ | Tạo danh mục con | body: `category_id`* `name`* `slug` `description` `sort_order` `status` | **subcategories** (INSERT) |
| PUT | `/admin/subcategories/{id}` | 🛡️ | Cập nhật danh mục con | path: `id`, body: *(same as POST, all optional)* | **subcategories** (UPDATE) |
| DELETE | `/admin/subcategories/{id}` | 🛡️ | Xóa danh mục con | path: `id` | **subcategories** (DELETE), *locations* (CHECK FK) |
| PATCH | `/admin/subcategories/{id}/status` | 🛡️ | Đổi trạng thái | path: `id`, body: `status`* (`active`\|`inactive`) | **subcategories** (UPDATE status) |

---

## LOCATIONS (Địa điểm)
> 🌿 Branch: `feat/taynd/api-locations`
> 💬 `feat(locations): list/detail/featured/nearby, track views, admin CRUD & toggle status/featured`
> 🧪 Test: `python tests/scripts/test_locations.py`

| Method | Endpoint | Quyền | Mô tả | Request | Bảng DB |
|--------|----------|-------|-------|---------|---------|
GET	/locations/{id}/nearby	🌐	Địa điểm lân cận (gợi ý sau khi xem chi tiết)	Trải nghiệm user tốt hơn
| GET | `/locations` | 🌐 | Danh sách địa điểm (filter, sort, paginate) | `?category_id &subcategory_id &district &price_level &sort &order &page &per_page` | **locations** (SELECT), *categories*, *subcategories* (JOIN) |
| GET | `/locations/featured` | 🌐 | Danh sách địa điểm nổi bật | `?limit` (default: 8) | **locations** (SELECT WHERE is_featured=1) |
| GET | `/locations/nearby` | 🌐 | Địa điểm gần vị trí hiện tại | `?lat`* `&lng`* `&radius` (km, default: 5) | **locations** (SELECT Haversine) |
| GET |/locations/districts	|🌐	| Danh sách quận có địa điểm (dynamic)|	locations (SELECT DISTINCT district) |
| GET | `/locations/{slug}` | 🌐 | Chi tiết địa điểm theo slug | path: `slug` | **locations** (SELECT), *categories*, *subcategories*, *tags*, *amenities* (JOIN) |
| GET | `/locations/{id}/images` | 🌐 | Danh sách ảnh của địa điểm | path: `id` | **locations** (SELECT thumbnail, images) |
| GET | `/locations/{id}/ratings` | 🌐 | Danh sách đánh giá của địa điểm | path: `id`, `?page &per_page` | **ratings** (SELECT), *users*, *rating_images* (JOIN) |
| GET |	/locations/{id}/rating-stats |	🌐 | Phân bố số sao (5 sao:12, 4 sao:8...)	| ratings (GROUP BY score) |
| GET |	/locations/{id}/nearby |	🌐	| Địa điểm lân cận (gợi ý sau khi xem chi tiết)	| locations (Haversine, limit 6) | 
| POST | `/locations/{id}/view` | 🌐 | Ghi nhận lượt xem | path: `id`, body: `session_id` | **views** (INSERT), **locations** (UPDATE view_count) |
| POST | `/admin/locations` | 🛡️ | Tạo địa điểm mới | body: `name`* `category_id`* `description`* `short_description`* `address`* `district`* `latitude`* `longitude`* `subcategory_id slug phone email website opening_hours price_min price_max price_level thumbnail images video_url status is_featured` | **locations** (INSERT) |
| PUT | `/admin/locations/{id}` | 🛡️ | Cập nhật địa điểm | path: `id`, body: *(same as POST, all optional)* | **locations** (UPDATE) |
| DELETE | `/admin/locations/{id}` | 🛡️ | Xóa địa điểm | path: `id` | **locations** (DELETE), *ratings*, *favorites*, *views*, *location_tags*, *location_amenities* (CASCADE) |
| PATCH | `/admin/locations/{id}/status` | 🛡️ | Đổi trạng thái | path: `id`, body: `status`* (`active`\|`inactive`) | **locations** (UPDATE status) |
| PATCH | `/admin/locations/{id}/featured` | 🛡️ | Bật/tắt nổi bật | path: `id`, body: `is_featured`* (bool) | **locations** (UPDATE is_featured) |
| GET | `/admin/locations/export` | 🛡️ | Export danh sách địa điểm ra Excel | `?category_id &district &status` | **locations** (SELECT) |
| POST | `/admin/locations/{id}/tags` | 🛡️ | Gán tags cho địa điểm | path: `id`, body: `tag_ids[]`* | **location_tags** (INSERT) |
| DELETE | `/admin/locations/{id}/tags/{tagId}` | 🛡️ | Xóa tag khỏi địa điểm | path: `id`, `tagId` | **location_tags** (DELETE) |
| POST | `/admin/locations/{id}/amenities` | 🛡️ | Gán tiện ích cho địa điểm | path: `id`, body: `amenity_ids[]`* | **location_amenities** (INSERT) |
| DELETE | `/admin/locations/{id}/amenities/{amenityId}` | 🛡️ | Xóa tiện ích khỏi địa điểm | path: `id`, `amenityId` | **location_amenities** (DELETE) |

---

## TOURS (Sản phẩm tour)
> 🌿 Branch: `feat/taynd/api-tours`
> 💬 `feat(tours): list/detail/featured/hot, admin CRUD & toggle status/featured/hot`
> 🧪 Test: `python tests/scripts/test_tours.py`

| Method | Endpoint | Quyền | Mô tả | Request | Bảng DB |
|--------|----------|-------|-------|---------|---------|
| GET | `/tours` | 🌐 | Danh sách tour (filter, sort, paginate) | `?tour_category_id &price_min &price_max &duration &available_from &available_to &sort &order &page &per_page` | **tours** (SELECT), *tour_categories* (JOIN) |
| GET | `/tours/featured` | 🌐 | Danh sách tour nổi bật | `?limit` (default: 8) | **tours** (SELECT WHERE is_featured=1) |
| GET | `/tours/hot` | 🌐 | Danh sách tour hot | `?limit` (default: 8) | **tours** (SELECT WHERE is_hot=1) |
| GET | `/tours/{slug}` | 🌐 | Chi tiết tour theo slug | path: `slug` | **tours** (SELECT), *tour_categories*, *tour_schedules* (JOIN) |
| GET | `/tours/{id}/schedules` | 🌐 | Lịch khởi hành của tour | path: `id`, `?from &to` | **tour_schedules** (SELECT WHERE tour_id, status=available) |
| GET | `/tours/{id}/ratings` | 🌐 | Đánh giá của tour | path: `id`, `?page &per_page` | **ratings** (SELECT WHERE tour_id), *users*, *rating_images* (JOIN) |
| GET | `/tours/{id}/rating-stats` | 🌐 | Phân bố số sao của tour | path: `id` | **ratings** (GROUP BY score WHERE tour_id) |
| POST | `/tours/{id}/check-availability` | 🌐 | Kiểm tra còn chỗ cho ngày cụ thể | path: `id`, body: `schedule_id`* `quantity_adult`* `quantity_child` `quantity_infant` | **tour_schedules** (SELECT booked_people, max_people) |
| POST | `/admin/tours` | 🛡️ | Tạo tour mới | body: `name`* `tour_category_id`* `price_adult`* `slug description short_desc itinerary inclusions exclusions price_child price_infant discount_percent duration start_time meeting_point max_people min_people available_from available_to thumbnail images video_url location_ids status is_featured is_hot` | **tours** (INSERT) |
| PUT | `/admin/tours/{id}` | 🛡️ | Cập nhật tour | path: `id`, body: *(same as POST, all optional)* | **tours** (UPDATE) |
| DELETE | `/admin/tours/{id}` | 🛡️ | Xóa tour | path: `id` | **tours** (DELETE), *tour_schedules*, *booking_items*, *ratings* (CHECK FK) |
| PATCH | `/admin/tours/{id}/status` | 🛡️ | Đổi trạng thái | path: `id`, body: `status`* (`active`\|`inactive`\|`sold_out`) | **tours** (UPDATE status) |
| PATCH | `/admin/tours/{id}/featured` | 🛡️ | Bật/tắt nổi bật | path: `id`, body: `is_featured`* (bool) | **tours** (UPDATE is_featured) |
| PATCH | `/admin/tours/{id}/hot` | 🛡️ | Bật/tắt tour hot | path: `id`, body: `is_hot`* (bool) | **tours** (UPDATE is_hot) |
| GET | `/admin/tours/export` | 🛡️ | Export danh sách tour ra Excel | `?tour_category_id &status` | **tours** (SELECT) |

---

## TOUR CATEGORIES (Danh mục tour)
> 🌿 Branch: `feat/taynd/api-tours`
> 💬 `feat(tour-categories): public list, admin CRUD`
> 🧪 Test: `python tests/scripts/test_tour_categories.py`

| Method | Endpoint | Quyền | Mô tả | Request | Bảng DB |
|--------|----------|-------|-------|---------|---------|
| GET | `/tour-categories` | 🌐 | Danh sách danh mục tour | — | **tour_categories** (SELECT WHERE status=active) |
| GET | `/tour-categories/{slug}/tours` | 🌐 | Tour theo danh mục | path: `slug`, `?page &per_page &sort &order` | **tours** (SELECT WHERE tour_category slug) |
| GET | `/admin/tour-categories` | 🛡️ | Danh sách (kể cả inactive) | `?status &page &per_page` | **tour_categories** (SELECT) |
| POST | `/admin/tour-categories` | 🛡️ | Tạo danh mục tour | body: `name`* `slug` `description` `icon` `sort_order` `status` | **tour_categories** (INSERT) |
| PUT | `/admin/tour-categories/{id}` | 🛡️ | Cập nhật | path: `id`, body: *(same as POST, all optional)* | **tour_categories** (UPDATE) |
| DELETE | `/admin/tour-categories/{id}` | 🛡️ | Xóa | path: `id` | **tour_categories** (DELETE), *tours* (CHECK FK) |
| PATCH | `/admin/tour-categories/{id}/status` | 🛡️ | Đổi trạng thái | path: `id`, body: `status`* (`active`\|`inactive`) | **tour_categories** (UPDATE status) |

---

## TOUR SCHEDULES (Lịch khởi hành)
> 🌿 Branch: `feat/taynd/api-tours`
> 💬 `feat(tour-schedules): admin manage departure schedules per tour`
> 🧪 Test: `python tests/scripts/test_tour_schedules.py`

| Method | Endpoint | Quyền | Mô tả | Request | Bảng DB |
|--------|----------|-------|-------|---------|---------|
| GET | `/admin/tour-schedules` | 🛡️ | Danh sách lịch khởi hành | `?tour_id &status &from &to &page &per_page` | **tour_schedules** (SELECT), *tours* (JOIN) |
| GET | `/admin/tour-schedules/{id}` | 🛡️ | Chi tiết lịch | path: `id` | **tour_schedules** (SELECT) |
| POST | `/admin/tours/{id}/schedules` | 🛡️ | Thêm lịch khởi hành cho tour | path: `id`, body: `start_date`* `end_date`* `max_people`* `price_adult price_child price_infant status` | **tour_schedules** (INSERT) |
| PUT | `/admin/tour-schedules/{id}` | 🛡️ | Cập nhật lịch | path: `id`, body: *(same as POST, all optional)* | **tour_schedules** (UPDATE) |
| DELETE | `/admin/tour-schedules/{id}` | 🛡️ | Xóa lịch | path: `id` | **tour_schedules** (DELETE), *booking_items* (CHECK FK) |
| PATCH | `/admin/tour-schedules/{id}/status` | 🛡️ | Đổi trạng thái | path: `id`, body: `status`* (`available`\|`full`\|`cancelled`) | **tour_schedules** (UPDATE status) |

---

## BOOKINGS (Đặt tour)
> 🌿 Branch: `feat/taynd/api-bookings`
> 💬 `feat(bookings): user book tour, view history, cancel; admin manage orders`
> 🧪 Test: `python tests/scripts/test_bookings.py`

| Method | Endpoint | Quyền | Mô tả | Request | Bảng DB |
|--------|----------|-------|-------|---------|---------|
| POST | `/bookings/calculate` | 🔐 | Tính tổng tiền trước khi đặt | body: `tour_id`* `tour_schedule_id`* `quantity_adult`* `quantity_child` `quantity_infant` | **tours**, **tour_schedules** (SELECT) |
| POST | `/bookings` | 🔐 | Đặt tour mới | body: `tour_id`* `tour_schedule_id`* `quantity_adult`* `quantity_child` `quantity_infant` `customer_name`* `customer_email`* `customer_phone`* `customer_address` `customer_note` `payment_method`* | **bookings** (INSERT), **booking_items** (INSERT), **tour_schedules** (UPDATE booked_people) |
| GET | `/user/bookings` | 🔐 | Lịch sử đặt tour của mình | `?status &page &per_page` | **bookings** (SELECT), *booking_items*, *tours* (JOIN) |
| GET | `/user/bookings/{id}` | 🔐 | Chi tiết đơn đặt theo ID | path: `id` | **bookings** (SELECT), *booking_items*, *tours*, *tour_schedules*, *payments* (JOIN) |
| GET | `/user/bookings/code/{booking_code}` | 🔐 | Chi tiết đơn đặt theo mã đơn | path: `booking_code` | **bookings** (SELECT WHERE booking_code), *booking_items*, *payments* (JOIN) |
| GET | `/user/bookings/{id}/invoice` | 🔐 | Xuất hóa đơn PDF | path: `id` | **bookings** (SELECT), *booking_items*, *tours* (JOIN) → PDF |
| POST | `/user/bookings/{id}/cancel` | 🔐 | Hủy đơn đặt | path: `id`, body: `cancellation_reason` | **bookings** (UPDATE booking_status=cancelled), **tour_schedules** (UPDATE booked_people) |
| GET | `/admin/bookings` | 🛡️ | Danh sách tất cả đơn hàng | `?status &payment_status &date_from &date_to &search &page &per_page` | **bookings** (SELECT), *users*, *booking_items* (JOIN) |
| GET | `/admin/bookings/{id}` | 🛡️ | Chi tiết đơn hàng | path: `id` | **bookings** (SELECT), *booking_items*, *tours*, *tour_schedules*, *payments*, *users* (JOIN) |
| PATCH | `/admin/bookings/{id}/status` | 🛡️ | Cập nhật trạng thái đơn | path: `id`, body: `booking_status`* (`pending`\|`confirmed`\|`cancelled`\|`completed`) | **bookings** (UPDATE booking_status) |
| POST | `/admin/bookings/{id}/confirm` | 🛡️ | Xác nhận đơn hàng | path: `id` | **bookings** (UPDATE booking_status=confirmed, confirmed_at), **notifications** (INSERT) |
| POST | `/admin/bookings/{id}/cancel` | 🛡️ | Hủy đơn hàng | path: `id`, body: `cancellation_reason` | **bookings** (UPDATE booking_status=cancelled, cancelled_at), **tour_schedules** (UPDATE booked_people), **notifications** (INSERT) |
| POST | `/admin/bookings/{id}/complete` | 🛡️ | Hoàn thành đơn | path: `id` | **bookings** (UPDATE booking_status=completed, completed_at) |
| GET | `/admin/bookings/export` | 🛡️ | Export danh sách đơn hàng Excel | `?status &payment_status &date_from &date_to` | **bookings** (SELECT) |

---

## PAYMENTS (Thanh toán)
> 🌿 Branch: `feat/taynd/api-bookings`
> 💬 `feat(payments): process payment, refund, admin manage transactions`
> 🧪 Test: `python tests/scripts/test_payments.py`

| Method | Endpoint | Quyền | Mô tả | Request | Bảng DB |
|--------|----------|-------|-------|---------|---------|
| POST | `/payments/callback` | 🌐 | Webhook nhận kết quả từ cổng thanh toán | body: *(gateway-specific)* | **payments** (UPDATE), **bookings** (UPDATE payment_status) |
| POST | `/payments/create` | 🔐 | Tạo link thanh toán (MoMo/VNPay) | body: `booking_id`* `payment_method`* (`momo`\|`vnpay`\|`zalopay`) | **payments** (INSERT), *(call payment gateway)* |
| GET | `/payments/status/{transaction_code}` | 🔐 | Kiểm tra trạng thái giao dịch | path: `transaction_code` | **payments** (SELECT WHERE transaction_code) |
| POST | `/payments/retry/{booking_code}` | 🔐 | Thử thanh toán lại | path: `booking_code` | **bookings** (SELECT), **payments** (INSERT), *(call payment gateway)* |
| GET | `/admin/payments` | 🛡️ | Danh sách giao dịch | `?payment_status &payment_gateway &date_from &date_to &page &per_page` | **payments** (SELECT), *bookings* (JOIN) |
| GET | `/admin/payments/{id}` | 🛡️ | Chi tiết giao dịch | path: `id` | **payments** (SELECT), *bookings* (JOIN) |
| POST | `/admin/payments/{id}/refund` | 🛡️ | Hoàn tiền | path: `id`, body: `refund_reason`* | **payments** (UPDATE payment_status=refunded, refunded_at), **bookings** (UPDATE payment_status=refunded) |
| GET | `/admin/payments/export` | 🛡️ | Export danh sách giao dịch Excel | `?payment_status &payment_gateway &date_from &date_to` | **payments** (SELECT) |

---

## RATINGS (Đánh giá)
> 🌿 Branch: `feat/taynd/api-ratings`
> 💬 `feat(ratings): user review location/tour after booking, admin approve/reject`
> 🧪 Test: `python tests/scripts/test_ratings.py`

| Method | Endpoint | Quyền | Mô tả | Request | Bảng DB |
|--------|----------|-------|-------|---------|---------|
| GET | `/ratings/check` | 🔐 | Kiểm tra user đã đánh giá địa điểm/tour chưa | `?location_id` hoặc `?tour_id` | **ratings** (SELECT WHERE user_id) |
| POST | `/ratings` | 🔐 | Tạo đánh giá (location hoặc tour) | body: `score`* (1-5) `comment` `images[]` (max 5) và một trong: `location_id` hoặc `tour_id`, `booking_id` | **ratings** (INSERT), *rating_images* (INSERT) |
| PUT | `/ratings/{id}` | 🔐 | Sửa đánh giá của mình | path: `id`, body: `score` `comment` `images[]` | **ratings** (UPDATE), *rating_images* (SYNC) |
| DELETE | `/ratings/{id}` | 🔐 | Xóa đánh giá của mình | path: `id` | **ratings** (DELETE), *rating_images* (CASCADE) |
| POST | `/ratings/{id}/helpful` | 🔐 | Đánh dấu hữu ích | path: `id` | **ratings** (UPDATE helpful_count) |
| GET | `/ratings/{id}/images` | 🌐 | Ảnh trong bài đánh giá | path: `id` | **rating_images** (SELECT) |
| GET | `/admin/ratings` | 🛡️ | Danh sách đánh giá | `?status &location_id &tour_id &page &per_page` | **ratings** (SELECT), *users*, *locations*, *tours*, *rating_images* (JOIN) |
| PATCH | `/admin/ratings/{id}/approve` | 🛡️ | Duyệt đánh giá | path: `id` | **ratings** (UPDATE status=approved), **locations** or **tours** (UPDATE avg_rating, review_count), **notifications** (INSERT) |
| PATCH | `/admin/ratings/{id}/reject` | 🛡️ | Từ chối đánh giá | path: `id`, body: `rejected_reason`* | **ratings** (UPDATE status=rejected), **notifications** (INSERT) |
| DELETE | `/admin/ratings/{id}` | 🛡️ | Xóa đánh giá | path: `id` | **ratings** (DELETE), *rating_images* (CASCADE) |
| GET | `/admin/ratings/export` | 🛡️ | Export danh sách đánh giá Excel | `?status &location_id &tour_id &date_from &date_to` | **ratings** (SELECT) |

---

## FAVORITES (Yêu thích)
> 🌿 Branch: `feat/taynd/api-favorites`
> 💬 `feat(favorites): user save/unsave locations, list saved locations`
> 🧪 Test: `python tests/scripts/test_favorites.py`

| Method | Endpoint | Quyền | Mô tả | Request | Bảng DB |
|--------|----------|-------|-------|---------|---------|
| GET | `/user/favorites` | 🔐 | Danh sách địa điểm đã lưu | `?page &per_page` | **favorites** (SELECT), *locations*, *categories* (JOIN) |
| GET | `/user/favorites/check/{location_id}` | 🔐 | Kiểm tra đã yêu thích chưa | path: `location_id` | **favorites** (SELECT WHERE user_id AND location_id) |
| POST | `/user/favorites` | 🔐 | Thêm vào yêu thích | body: `location_id`* | **favorites** (INSERT), **locations** (UPDATE favorite_count) |
| DELETE | `/user/favorites/{location_id}` | 🔐 | Xóa khỏi yêu thích | path: `location_id` | **favorites** (DELETE), **locations** (UPDATE favorite_count) |

---

## USER PROFILE
> 🌿 Branch: `feat/taynd/api-user-profile`
> 💬 `feat(profile): view/update profile, upload avatar, change password, booking/rating history`
> 🧪 Test: `python tests/scripts/test_user_profile.py`

| Method | Endpoint | Quyền | Mô tả | Request | Bảng DB |
|--------|----------|-------|-------|---------|---------|
| GET | `/user/profile` | 🔐 | Xem thông tin cá nhân | — | **users** (SELECT) |
| PUT | `/user/profile` | 🔐 | Cập nhật thông tin | body: `full_name` `phone` `birthdate` `gender` `city` | **users** (UPDATE) |
| POST | `/user/profile/avatar` | 🔐 | Upload ảnh đại diện | body: `avatar`* (file, max 2MB) | **users** (UPDATE avatar) |
| PUT | `/user/password` | 🔐 | Đổi mật khẩu | body: `current_password`* `password`* `password_confirmation`* | **users** (UPDATE password) |
| GET | `/user/ratings` | 🔐 | Lịch sử đánh giá của mình | `?status &page &per_page` | **ratings** (SELECT), *locations*, *tours*, *rating_images* (JOIN) |
| GET | `/user/search-history` | 🔐 | Lấy lịch sử tìm kiếm | `?limit` | **search_logs** (SELECT WHERE user_id) |
| DELETE | `/user/search-history` | 🔐 | Xóa lịch sử tìm kiếm | — | **search_logs** (DELETE WHERE user_id) |
| DELETE | `/user/account` | 🔐 | Xóa tài khoản (có confirm) | body: `password`* | **users** (DELETE or soft delete) |

---

## NOTIFICATIONS (Thông báo)
> 🌿 Branch: `feat/taynd/api-notifications`
> 💬 `feat(notifications): list, mark read, mark all read, delete; admin send notification`
> 🧪 Test: `python tests/scripts/test_notifications.py`

| Method | Endpoint | Quyền | Mô tả | Request | Bảng DB |
|--------|----------|-------|-------|---------|---------|
| GET | `/user/notifications` | 🔐 | Danh sách thông báo | `?is_read &page &per_page` | **notifications** (SELECT) |
| GET | `/user/notifications/unread-count` | 🔐 | Số thông báo chưa đọc | — | **notifications** (COUNT WHERE is_read=0) |
| PATCH | `/user/notifications/{id}/read` | 🔐 | Đánh dấu đã đọc | path: `id` | **notifications** (UPDATE is_read, read_at) |
| PATCH | `/user/notifications/read-all` | 🔐 | Đánh dấu tất cả đã đọc | — | **notifications** (UPDATE WHERE user_id AND is_read=0) |
| DELETE | `/user/notifications/{id}` | 🔐 | Xóa thông báo | path: `id` | **notifications** (DELETE) |
| GET | `/admin/notifications` | 🛡️ | Danh sách thông báo hệ thống | `?user_id &type &page &per_page` | **notifications** (SELECT) |
| POST | `/admin/notifications/send` | 🛡️ | Gửi thông báo đến user | body: `user_id`* `type`* `title`* `content` `data` | **notifications** (INSERT) |
| POST | `/admin/notifications/send-all` | 🛡️ | Gửi thông báo đến tất cả user | body: `type`* `title`* `content` `data` | **notifications** (INSERT batch) |
| DELETE | `/admin/notifications/{id}` | 🛡️ | Xóa thông báo | path: `id` | **notifications** (DELETE) |

---

## SEARCH (Tìm kiếm)
> 🌿 Branch: `feat/taynd/api-search`
> 💬 `feat(search): full-text search locations & tours, autocomplete, popular keywords`
> 🧪 Test: `python tests/scripts/test_search.py`

| Method | Endpoint | Quyền | Mô tả | Request | Bảng DB |
|--------|----------|-------|-------|---------|---------|
| GET | `/search` | 🌐 | Tìm kiếm địa điểm & tour | `?q`* `&type` (`location`\|`tour`) `&category_id &district &price_min &price_max &sort &order &page &per_page &session_id` | **locations**, **tours** (SELECT FULLTEXT), **search_logs** (INSERT) |
| GET | `/search/suggestions` | 🌐 | Gợi ý autocomplete | `?q`* `&limit` (default: 5) | **locations**, **tours** (SELECT LIKE name) |
| GET | `/search/popular` | 🌐 | Từ khóa phổ biến | `?limit` (default: 10) `&days` (default: 30) | **search_logs** (SELECT GROUP BY query) |
| GET | `/search/trending` | 🌐 | Xu hướng tìm kiếm hiện tại | `?limit` (default: 10) | **search_logs** (SELECT GROUP BY query WHERE 24h) |
| GET | `/statistics` | 🌐 | Thống kê tổng quan website | — | **locations**, **tours**, **blog_posts** (SELECT COUNT) |
| GET | `/recommendations` | 🔐 | Gợi ý địa điểm/tour dựa trên lịch sử | `?limit` (default: 10) | **views**, **bookings**, **favorites** (SELECT), *locations*, *tours* (JOIN) |

---

## BLOG
> 🌿 Branch: `feat/taynd/api-blog`
> 💬 `feat(blog): public list/detail/categories, admin CRUD & publish/archive posts`
> 🧪 Test: `python tests/scripts/test_blog.py`

| Method | Endpoint | Quyền | Mô tả | Request | Bảng DB |
|--------|----------|-------|-------|---------|---------|
| GET | `/blog` | 🌐 | Danh sách bài viết | `?category_id &page &per_page` | **blog_posts** (SELECT WHERE status=published), *users*, *blog_categories* (JOIN) |
| GET | `/blog/categories` | 🌐 | Danh sách danh mục blog | — | **blog_categories** (SELECT) |
| GET | `/blog/{slug}` | 🌐 | Chi tiết bài viết | path: `slug` | **blog_posts** (SELECT, UPDATE view_count), *users*, *blog_categories* (JOIN) |
| GET | `/admin/blog-posts` | 🛡️ | Danh sách bài viết (kể cả draft) | `?status &category_id &page &per_page` | **blog_posts** (SELECT), *users*, *blog_categories* (JOIN) |
| GET | `/admin/blog-posts/{id}` | 🛡️ | Chi tiết bài viết | path: `id` | **blog_posts** (SELECT), *blog_categories* (JOIN) |
| POST | `/admin/blog-posts` | 🛡️ | Tạo bài viết | body: `title`* `content`* `excerpt` `featured_image` `category_ids[]` `status` `published_at` | **blog_posts** (INSERT), **blog_post_categories** (INSERT) |
| PUT | `/admin/blog-posts/{id}` | 🛡️ | Cập nhật bài viết | path: `id`, body: *(same as POST, all optional)* | **blog_posts** (UPDATE), *blog_post_categories* (SYNC) |
| DELETE | `/admin/blog-posts/{id}` | 🛡️ | Xóa bài viết | path: `id` | **blog_posts** (DELETE), *blog_post_categories* (CASCADE) |
| PATCH | `/admin/blog-posts/{id}/status` | 🛡️ | Đổi trạng thái | path: `id`, body: `status`* (`draft`\|`published`\|`archived`) | **blog_posts** (UPDATE status, published_at) |
| GET | `/admin/blog-categories` | 🛡️ | Danh sách danh mục blog | — | **blog_categories** (SELECT) |
| POST | `/admin/blog-categories` | 🛡️ | Tạo danh mục blog | body: `name`* `slug` `description` | **blog_categories** (INSERT) |
| PUT | `/admin/blog-categories/{id}` | 🛡️ | Cập nhật | path: `id`, body: *(same as POST, all optional)* | **blog_categories** (UPDATE) |
| DELETE | `/admin/blog-categories/{id}` | 🛡️ | Xóa | path: `id` | **blog_categories** (DELETE), *blog_post_categories* (CASCADE) |

---

## ADMIN — USERS
> 🌿 Branch: `feat/taynd/api-admin-users`
> 💬 `feat(admin/users): list, detail, create, update, toggle status/role, delete`
> 🧪 Test: `python tests/scripts/test_admin_users.py`

| Method | Endpoint | Quyền | Mô tả | Request | Bảng DB |
|--------|----------|-------|-------|---------|---------|
| GET | `/admin/users` | 🛡️ | Danh sách người dùng | `?q &role` (`user`\|`admin`\|`staff`) `&status &page &per_page &sort &order` | **users** (SELECT) |
| GET | `/admin/users/{id}` | 🛡️ | Chi tiết người dùng | path: `id` | **users** (SELECT), *bookings*, *ratings* (COUNT) |
| POST | `/admin/users` | 🛡️ | Tạo user mới | body: `username`* `email`* `password`* `full_name`* `role` `status` | **users** (INSERT) |
| PUT | `/admin/users/{id}` | 🛡️ | Cập nhật thông tin user | path: `id`, body: `full_name` `phone` `city` `role` `status` | **users** (UPDATE) |
| DELETE | `/admin/users/{id}` | 🛡️ | Xóa tài khoản | path: `id` | **users** (DELETE), *bookings*, *ratings*, *favorites*, *notifications* (CASCADE) |
| PATCH | `/admin/users/{id}/status` | 🛡️ | Khóa / mở khóa tài khoản | path: `id`, body: `status`* (`active`\|`banned`) | **users** (UPDATE status) |
| PATCH | `/admin/users/{id}/role` | 🛡️ | Đổi role | path: `id`, body: `role`* (`user`\|`staff`\|`admin`) | **users** (UPDATE role) |
| GET | `/admin/users/{id}/bookings` | 🛡️ | Lịch sử đặt tour của user | path: `id`, `?page &per_page` | **bookings** (SELECT WHERE user_id), *booking_items* (JOIN) |
| GET | `/admin/users/{id}/ratings` | 🛡️ | Bài đánh giá của user | path: `id`, `?page &per_page` | **ratings** (SELECT WHERE user_id) |
| GET | `/admin/users/export` | 🛡️ | Export danh sách user Excel | `?role &status` | **users** (SELECT) |

---

## ADMIN — DASHBOARD & REPORTS
> 🌿 Branch: `feat/taynd/api-admin-dashboard`
> 💬 `feat(admin/dashboard): overview stats, revenue, top tours/locations, user growth, booking trend`
> 🧪 Test: `python tests/scripts/test_dashboard.py`

| Method | Endpoint | Quyền | Mô tả | Request | Bảng DB |
|--------|----------|-------|-------|---------|---------|
| GET | `/admin/dashboard/stats` | 🛡️ | Tổng quan: user, tour, booking, doanh thu | — | **users**, **tours**, **bookings**, **payments** (SELECT COUNT/SUM) |
| GET | `/admin/dashboard/revenue` | 🛡️ | Thống kê doanh thu | `?period` (`day`\|`week`\|`month`\|`year`) `&from &to` | **payments** (SELECT GROUP BY DATE, SUM amount) |
| GET | `/admin/dashboard/top-tours` | 🛡️ | Top tour bán chạy | `?limit` (default: 10) `&from &to` | **tours** (SELECT ORDER BY booking_count), *booking_items* (COUNT) |
| GET | `/admin/dashboard/top-locations` | 🛡️ | Top địa điểm được yêu thích | `?limit` (default: 10) | **locations** (SELECT ORDER BY favorite_count, view_count) |
| GET | `/admin/dashboard/user-growth` | 🛡️ | Tăng trưởng người dùng theo tháng | `?year` (default: năm hiện tại) | **users** (SELECT GROUP BY MONTH(created_at)) |
| GET | `/admin/dashboard/booking-trend` | 🛡️ | Xu hướng đặt tour | `?days` (default: 30) | **bookings** (SELECT GROUP BY DATE(booked_at)) |
| GET | `/admin/reports/bookings` | 🛡️ | Báo cáo đơn hàng | `?from &to &status &payment_status` | **bookings** (SELECT GROUP BY status, DATE) |
| GET | `/admin/reports/ratings` | 🛡️ | Thống kê đánh giá theo thời gian | `?from &to &status` | **ratings** (SELECT GROUP BY DATE, status) |
| GET | `/admin/reports/users` | 🛡️ | Thống kê người dùng mới | `?year` | **users** (SELECT GROUP BY MONTH(created_at)) |
| GET | `/admin/reports/revenue-detail` | 🛡️ | Báo cáo doanh thu chi tiết (theo tour) | `?from &to` | **payments**, **bookings**, **booking_items** (SELECT JOIN) |

---

## TAGS & AMENITIES
> 🌿 Branch: `feat/taynd/api-tags-amenities`
> 💬 `feat(tags/amenities): public list, admin CRUD`
> 🧪 Test: `python tests/scripts/test_tags_amenities.py`

| Method | Endpoint | Quyền | Mô tả | Request | Bảng DB |
|--------|----------|-------|-------|---------|---------|
| GET | `/tags` | 🌐 | Danh sách tags | `?type` (`cuisine`\|`service`\|`feature`\|`atmosphere`) | **tags** (SELECT) |
| GET | `/amenities` | 🌐 | Danh sách tiện ích | `?category` (`connectivity`\|`parking`\|`comfort`\|`payment`) | **amenities** (SELECT) |
| POST | `/admin/tags` | 🛡️ | Tạo tag | body: `name`* `slug` `type` | **tags** (INSERT) |
| PUT | `/admin/tags/{id}` | 🛡️ | Cập nhật tag | path: `id`, body: *(same as POST, all optional)* | **tags** (UPDATE) |
| DELETE | `/admin/tags/{id}` | 🛡️ | Xóa tag | path: `id` | **tags** (DELETE), *location_tags* (CASCADE) |
| POST | `/admin/amenities` | 🛡️ | Tạo tiện ích | body: `name`* `icon` `category` | **amenities** (INSERT) |
| PUT | `/admin/amenities/{id}` | 🛡️ | Cập nhật tiện ích | path: `id`, body: *(same as POST, all optional)* | **amenities** (UPDATE) |
| DELETE | `/admin/amenities/{id}` | 🛡️ | Xóa tiện ích | path: `id` | **amenities** (DELETE), *location_amenities* (CASCADE) |

---

## CONTACTS (Liên hệ)
> 🌿 Branch: `feat/taynd/api-contacts`
> 💬 `feat(contacts): public submit contact form, admin manage & reply`
> 🧪 Test: *(chưa có script)*

| Method | Endpoint | Quyền | Mô tả | Request | Bảng DB |
|--------|----------|-------|-------|---------|---------|
| POST | `/contacts` | 🌐 | Gửi form liên hệ | body: `name`* `email`* `phone` `subject` `message`* | **contacts** (INSERT) |
| GET | `/admin/contacts` | 🛡️ | Danh sách liên hệ | `?status` (`new`\|`read`\|`replied`) `&page &per_page` | **contacts** (SELECT) |
| GET | `/admin/contacts/{id}` | 🛡️ | Chi tiết liên hệ | path: `id` | **contacts** (SELECT, UPDATE status=read) |
| POST | `/admin/contacts/{id}/reply` | 🛡️ | Trả lời liên hệ | path: `id`, body: `reply`* | **contacts** (UPDATE status=replied, reply, replied_by, replied_at) |
| DELETE | `/admin/contacts/{id}` | 🛡️ | Xóa liên hệ | path: `id` | **contacts** (DELETE) |
| GET | `/admin/contacts/export` | 🛡️ | Export danh sách liên hệ Excel | `?status` | **contacts** (SELECT) |

---

## UPLOAD
> 🌿 Branch: `feat/taynd/api-upload`
> 💬 `feat(upload): upload image/multiple images to Cloudinary, delete image`
> 🧪 Test: `python tests/scripts/test_upload.py`

| Method | Endpoint | Quyền | Mô tả | Request | Bảng DB |
|--------|----------|-------|-------|---------|---------|
| POST | `/upload/image` | 🔐 | Upload 1 ảnh lên Cloudinary | body: `image`* (file, max 5MB) `folder` | — |
| POST | `/upload/images` | 🔐 | Upload nhiều ảnh (max 10) | body: `images[]`* (files, max 5MB each) `folder` | — |
| DELETE | `/upload/image` | 🔐 | Xóa ảnh khỏi Cloudinary | body: `public_id`* | — |

---

## CONFIG & UTILITIES
> 🌿 Branch: `feat/taynd/api-config`
> 💬 `feat(config): website config, weather, health check`
> 🧪 Test: *(chưa có script)*

| Method | Endpoint | Quyền | Mô tả | Request | Bảng DB |
|--------|----------|-------|-------|---------|---------|
| GET | `/config` | 🌐 | Lấy cấu hình website (hotline, email, logo, meta) | — | **settings** (SELECT) |
| GET | `/weather` | 🌐 | Lấy thời tiết Đà Nẵng hiện tại (có cache) | — | — *(external API)* |
| GET | `/health` | 🌐 | Kiểm tra server health | — | — |

---

## Tổng kết

| Nhóm | Public 🌐 | User 🔐 | Admin 🛡️ | Branch |
|------|-----------|---------|----------|--------|
| Auth | 4 | 5 | — | `feat/taynd/api-auth` |
| Categories | 4 | — | 8 | `feat/taynd/api-categories` |
| Locations | 11 | — | 10 | `feat/taynd/api-locations` |
| Tours | 8 | — | 6 | `feat/taynd/api-tours` |
| Tour Categories | 2 | — | 5 | `feat/taynd/api-tours` |
| Tour Schedules | — | — | 6 | `feat/taynd/api-tours` |
| Bookings | — | 7 | 7 | `feat/taynd/api-bookings` |
| Payments | 1 | 3 | 4 | `feat/taynd/api-bookings` |
| Ratings | 2 | 5 | 5 | `feat/taynd/api-ratings` |
| Favorites | — | 4 | — | `feat/taynd/api-favorites` |
| Profile | — | 8 | — | `feat/taynd/api-user-profile` |
| Notifications | — | 5 | 4 | `feat/taynd/api-notifications` |
| Search | 5 | 1 | — | `feat/taynd/api-search` |
| Blog | 3 | — | 10 | `feat/taynd/api-blog` |
| Admin Users | — | — | 10 | `feat/taynd/api-admin-users` |
| Dashboard | — | — | 10 | `feat/taynd/api-admin-dashboard` |
| Tags & Amenities | 2 | — | 6 | `feat/taynd/api-tags-amenities` |
| Contacts | 1 | — | 6 | `feat/taynd/api-contacts` |
| Upload | — | 3 | — | `feat/taynd/api-upload` |
| Config & Utilities | 3 | — | — | `feat/taynd/api-config` |
| **Tổng** | **46** | **41** | **97** | |
