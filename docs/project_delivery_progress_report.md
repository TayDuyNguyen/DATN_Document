# Báo cáo Theo dõi Tiến độ Triển khai Dự án

> Ngày cập nhật: 21/05/2026  
> Phạm vi theo dõi:
> - `D:\DATN\danangtrip-web`
> - `D:\DATN\danangtrip-admin`
>  
> Cách tính tiến độ:
> - Tách làm 2 lớp:
>   - `Tổng màn của dự án` theo tài liệu thật trong `docs/page`
>   - `Phạm vi delivery đang theo dõi` theo các màn đã có `deploy-report` hoặc đã được chốt là màn kế tiếp trong rollout hiện tại
> - Với `danangtrip-web`, không tính 5 file component-spec của nhóm rating vào tổng số màn chính.
> - Trạng thái dùng 3 mức: `Chưa làm`, `Đang làm`, `Hoàn thành`.

---

## 1. Dự án `danangtrip-web`

### 1.0 Kiểm kê màn thực tế từ tài liệu

| Hạng mục | Số lượng | Ghi chú |
|---|---:|---|
| Tổng file `user_*` trong `docs/page` | 40 | Bao gồm cả screen spec và component spec |
| Component spec | 5 | `user_rating_modal`, `user_rating_edit_modal`, `user_rating_delete`, `user_rating_helpful`, `user_rating_images_lightbox` |
| Tổng màn chính của web | 35 | Đây là mẫu số đúng để theo dõi tiến độ màn hình |
| Prototype HTML trong `screen/2_User_Flows` | 20 | Chưa bao gồm Guest flows dùng chung như home/search/tour/blog/contact |

### 1.1 Tóm tắt tiến độ

| Chỉ số | Giá trị |
|---|---:|
| Tổng màn chính của dự án | 35 |
| Hoàn thành theo tổng màn | 6 |
| Đang làm theo tổng màn | 1 |
| Chưa làm theo tổng màn | 28 |
| % hoàn thành theo tổng màn | 17.1% |
| Tổng màn đang theo dõi | 11 |
| Hoàn thành | 6 |
| Đang làm | 1 |
| Chưa làm | 4 |
| % hoàn thành trong phạm vi theo dõi | 54.5% |

### 1.2 Schedule / Timeline

| Mốc thời gian | Màn hình | Kết quả |
|---|---|---|
| 10/05/2026 | `contact` | Hoàn thành |
| 16/05/2026 | `tour-detail` | Hoàn thành |
| 17/05/2026 | `tour-booking` | Hoàn thành |
| 17/05/2026 | `tour-payment` | Hoàn thành |
| 19/05/2026 | `tour-departure-select` | Hoàn thành |
| 21/05/2026 | `user-bookings-list` | Hoàn thành |
| Hiện tại | `user-booking-detail` | Đang làm theo prompt rollout hiện tại |
| Kế tiếp | `user-booking-by-code` | Chưa làm |
| Kế tiếp | `user-booking-invoice` | Chưa làm |
| Backlog gần | `favorites` | Chưa làm |
| Backlog gần | `notifications` | Chưa làm |

### 1.3 Chi tiết trạng thái công việc

| STT | Feature slug / Doc | Tên màn | Route | Trạng thái | Lý do |
|---:|---|---|---|---|---|
| 1 | `contact` | Liên hệ | `/contact` | Hoàn thành | Đã có `deploy-report` ngày `2026-05-10` |
| 2 | `tour-detail` | Chi tiết tour | `/tours/{slug}` | Hoàn thành | Đã có `deploy-report` ngày `2026-05-16` |
| 3 | `tour-booking` | Đặt tour | `/tours/{slug}/book` | Hoàn thành | Đã có `deploy-report` ngày `2026-05-17` |
| 4 | `tour-payment` | Thanh toán tour | Flow thanh toán hiện tại | Hoàn thành | Đã có `deploy-report` ngày `2026-05-17` |
| 5 | `tour-departure-select` | Chọn lịch khởi hành | `/tours/{slug}/departures` hoặc modal tương ứng | Hoàn thành | Đã có `deploy-report` ngày `2026-05-19` |
| 6 | `user-bookings-list` | Lịch sử đặt tour | `/bookings` | Hoàn thành | Đã có `deploy-report` ngày `2026-05-21`; vòng `09-testing` đã được chốt |
| 7 | `user-booking-detail` | Chi tiết đơn đặt tour | `/bookings/{id}` | Đang làm | Đã được chọn là màn hiện tại trong `STACK_SKILLS_INDEX.md`, nhưng chưa có artifact end-to-end |
| 8 | `user_booking_by_code.md` | Đơn đặt theo mã đơn | `/bookings/code/{code}` | Chưa làm | Có tài liệu màn nhưng chưa có `deploy-report`; đang đứng sau booking detail |
| 9 | `user_booking_invoice.md` | Hóa đơn booking | `/bookings/{id}/invoice` | Chưa làm | Hiện vẫn là action trong flow booking detail, chưa tách thành delivery độc lập |
| 10 | `favorites` | Yêu thích | Theo route repo reality | Chưa làm | API và doc có, nhưng chưa được ưu tiên bằng trục hậu booking |
| 11 | `notifications` | Thông báo người dùng | Theo route repo reality | Chưa làm | Có tài liệu nhưng chưa vào rollout hiện tại |

### 1.4 Danh sách đầy đủ các màn web cần làm trong tương lai

| STT | Doc / Feature | Màn hình | Route | Trạng thái | Route/code hiện có | API readiness | Lý do / Ghi chú | Khuyến nghị |
|---:|---|---|---|---|---|---|---|---|
| 1 | `user_booking_detail.md` | Chi tiết đơn đặt tour | `/bookings/{id}` | Đang làm | Chưa có route detail thật | Ready + Partial | `GET /user/bookings/{id}`, `invoice`, `cancel` có thật; `passengers` và `timeline` còn cần fallback/xác minh | Làm ngay |
| 2 | `user_booking_by_code.md` | Đơn đặt theo mã đơn | `/bookings/code/{booking_code}` | Chưa làm | Chưa có | Ready | API có thật; rất hợp sau booking detail | Làm ngay sau màn hiện tại |
| 3 | `user_favorites.md` | Yêu thích | `/favorites` | Chưa làm | Chưa có | Ready | Bộ API favorites đã có đầy đủ | Ưu tiên cao |
| 4 | `user_notifications.md` | Thông báo | `/notifications` | Chưa làm | Chưa có | Ready | Bộ API notifications user đã có đầy đủ | Ưu tiên cao |
| 5 | `user_profile_password.md` | Đổi mật khẩu | `/profile/password` | Chưa làm | Chưa có route riêng | Ready | `PUT /user/password` có thật | Ưu tiên cao |
| 6 | `user_verify_email.md` | Xác thực email | `/verify-email` | Chưa làm | Chưa có | Ready | `POST /auth/verify-email` có thật | Ưu tiên cao |
| 7 | `user_login.md` | Đăng nhập | `/login` | Chưa làm | Chưa có | Ready | `POST /auth/login` có thật; core auth chưa có delivery riêng | Ưu tiên cao |
| 8 | `user_register.md` | Đăng ký | `/register` | Chưa làm | Chưa có | Ready | `POST /auth/register` có thật | Ưu tiên cao |
| 9 | `user_forgot_password.md` | Quên mật khẩu | `/forgot-password` | Chưa làm | Chưa có | Ready | `POST /auth/forgot-password` có thật | Ưu tiên cao |
| 10 | `user_reset_password.md` | Đặt lại mật khẩu | `/reset-password` | Chưa làm | Chưa có | Ready | `POST /auth/reset-password` có thật | Ưu tiên cao |
| 11 | `user_profile.md` | Hồ sơ cá nhân | `/profile` | Cần hardening | Đã có route/page | Ready | Route có thật nhưng chưa có artifact delivery riêng trong pipeline hiện tại | Hardening |
| 12 | `user_recommendations.md` | Gợi ý cho bạn | `/recommendations` | Chưa làm | Chưa có route riêng | Ready | `GET /recommendations` có thật | Làm sau auth/account |
| 13 | `user_my_ratings.md` | Đánh giá của tôi | `/profile/ratings` | Chưa làm | Chưa có | Ready | `GET /user/ratings` có thật | Làm sau profile |
| 14 | `user_booking_invoice.md` | Hóa đơn booking | `/bookings/{id}/invoice` | Chưa làm | Chưa có màn riêng | Ready | API download invoice có thật; hiện mới là action trong flow booking detail | Làm sau booking-by-code |
| 15 | `user_home.md` | Trang chủ | `/` | Cần hardening | Đã có | Partial | Route có thật; docs còn nhắc `GET /weather`, `GET /config` là planned nên cần fallback rõ | Hardening |
| 16 | `user_search.md` | Tìm kiếm | `/search` | Cần hardening | Đã có | Ready + Planned | Search core API có thật; search-history vẫn planned | Hardening |
| 17 | `user_locations_list.md` | Danh sách địa điểm | `/locations` | Cần hardening | Đã có | Ready | Route và API có thật | Hardening |
| 18 | `user_location_detail.md` | Chi tiết địa điểm | `/locations/{slug}` | Cần hardening | Đã có | Ready | Route và API có thật; có thể mở rộng favorite/rating khi login | Hardening |
| 19 | `user_tours_list.md` | Danh sách tour | `/tours` | Cần hardening | Đã có | Ready | Route và API có thật | Hardening |
| 20 | `user_blog_list.md` | Danh sách bài viết | `/blog` | Cần hardening | Đã có | Ready | Route và API có thật | Hardening |
| 21 | `user_blog_detail.md` | Chi tiết bài viết | `/blog/{slug}` | Cần hardening | Đã có | Ready | Route và API có thật; docs vẫn xếp đây là màn cần bổ sung prototype | Hardening |
| 22 | `user_destination_tour_landing.md` | Landing tour Đà Nẵng | `/du-lich-da-nang` | Cần hardening | Đã có | Partial | Route đã có; docs còn phụ thuộc `landing-pages/{slug}` và `tours/filters` planned | Hardening với fallback |
| 23 | `user_locations_by_category.md` | Địa điểm theo danh mục | `/categories/{slug}/locations` | Chưa làm | Chưa có | Ready | `GET /categories/{slug}/locations` có thật | Làm sau locations core |
| 24 | `user_locations_nearby.md` | Địa điểm lân cận | `/nearby` | Chưa làm | Chưa có | Ready | `GET /locations/nearby` có thật | Làm sau locations core |
| 25 | `user_tours_by_category.md` | Tour theo danh mục | `/tour-categories/{slug}/tours` | Chưa làm | Chưa có | Ready | `GET /tour-categories/{slug}/tours` có thật | Làm sau tours core |
| 26 | `user_blog_by_category.md` | Blog theo danh mục | `/blog?category_id={id}` | Chưa làm | Chưa có route riêng | Ready | Có thể làm bằng query state trên list route | Làm sau blog core |
| 27 | `user_profile_delete.md` | Xóa tài khoản | `/profile/delete` | Chưa làm | Chưa có | Planned | `DELETE /user/account` vẫn là planned trong docs | Chờ API |
| 28 | `user_cart.md` | Giỏ hàng | `/cart` | Chưa làm | Chưa có | Planned | Bộ `/cart/*` vẫn planned | Backlog sau |

### 1.5 Thứ tự triển khai web khuyến nghị

| Giai đoạn | Danh sách màn |
|---|---|
| Làm ngay | `user-booking-detail`, `user-booking-by-code`, `user-favorites`, `user-notifications`, `user-profile-password`, `user-verify-email` |
| Hardening tiếp theo | `user-profile`, `user-home`, `user-search`, `user-locations-list`, `user-location-detail`, `user-tours-list`, `user-blog-list`, `user-blog-detail`, `user-destination-tour-landing` |
| Backlog mở rộng | `user-recommendations`, `user-my-ratings`, `user-locations-by-category`, `user-locations-nearby`, `user-tours-by-category`, `user-blog-by-category`, `user-booking-invoice`, `user-profile-delete`, `user-cart` |

### 1.6 Nhận định ngắn

| Nhận định | Giải thích |
|---|---|
| Trục đặt tour gần khép kín | Đã có detail tour, booking, payment, departure select, bookings list |
| Điểm hở lớn nhất hiện tại | `user-booking-detail` vì list booking đã có nhưng chưa có route detail thật |
| Ưu tiên sau màn hiện tại | `user-booking-by-code`, rồi mới đến `invoice`, `favorites`, `notifications` |

---

## 2. Dự án `danangtrip-admin`

### 2.0 Kiểm kê màn thực tế từ tài liệu

| Hạng mục | Số lượng | Ghi chú |
|---|---:|---|
| Tổng file `admin_*` trong `docs/page` | 40 | Tất cả đều là screen spec cấp dự án admin |
| Tổng màn chính của admin | 40 | Đây là mẫu số đúng để theo dõi tiến độ màn hình |
| Prototype HTML trong `screen/3_Admin_Flows` | 36 | Chưa tính utility pages trong `4_Others` |

### 2.1 Tóm tắt tiến độ

| Chỉ số | Giá trị |
|---|---:|
| Tổng màn chính của dự án | 40 |
| Hoàn thành theo tổng màn | 8 |
| Đang làm theo tổng màn | 1 |
| Chưa làm theo tổng màn | 31 |
| % hoàn thành theo tổng màn | 20.0% |
| Tổng màn đang theo dõi | 15 |
| Hoàn thành | 8 |
| Đang làm | 1 |
| Chưa làm | 6 |
| % hoàn thành trong phạm vi theo dõi | 53.3% |

### 2.2 Schedule / Timeline

| Mốc thời gian | Màn hình | Kết quả |
|---|---|---|
| 11/05/2026 | `create-new-location-danang-trip` | Hoàn thành |
| 12/05/2026 | `location-detail` | Hoàn thành |
| 13/05/2026 | `location-categories` | Hoàn thành |
| 17/05/2026 | `admin-bookings-list` | Hoàn thành |
| 17/05/2026 | `admin-payment-list` | Hoàn thành |
| 18/05/2026 | `admin-tour-schedule-form` | Hoàn thành |
| 20/05/2026 | `admin-tour-schedule-edit` | Hoàn thành |
| 21/05/2026 | `admin-bookings-detail` | Hoàn thành |
| Hiện tại | `admin-payments-detail` | Đang làm theo prompt rollout hiện tại |
| Backlog gần | `admin_reports_ratings` | Chưa làm |
| Backlog gần | `admin_reports_locations` | Chưa làm |
| Backlog gần | `admin_reports_users` | Chưa làm |
| Planned backlog | `admin_promotions` | Chưa làm |
| Planned backlog | `admin_site_settings` | Chưa làm |
| Planned backlog | `admin_landing_pages` | Chưa làm |

### 2.3 Chi tiết trạng thái công việc

| STT | Feature slug / Doc | Tên màn | Route | Trạng thái | Lý do |
|---:|---|---|---|---|---|
| 1 | `create-new-location-danang-trip` | Tạo địa điểm mới | Route create location admin | Hoàn thành | Đã có `deploy-report` ngày `2026-05-11` |
| 2 | `location-detail` | Chi tiết địa điểm | Route detail location admin | Hoàn thành | Đã có `deploy-report` ngày `2026-05-12` |
| 3 | `location-categories` | Danh mục địa điểm | `/admin/categories` hoặc route tương ứng | Hoàn thành | Đã có `deploy-report` ngày `2026-05-13` |
| 4 | `admin-bookings-list` | Danh sách đơn hàng | `/admin/bookings` | Hoàn thành | Đã có `deploy-report` ngày `2026-05-17` |
| 5 | `admin-payment-list` | Danh sách giao dịch | `/admin/payments` | Hoàn thành | Đã có `deploy-report` ngày `2026-05-17` |
| 6 | `admin-tour-schedule-form` | Tạo lịch khởi hành | Route create schedule admin | Hoàn thành | Đã có `deploy-report` ngày `2026-05-18` |
| 7 | `admin-tour-schedule-edit` | Chỉnh sửa lịch khởi hành | Route edit schedule admin | Hoàn thành | Đã có `deploy-report` ngày `2026-05-20` |
| 8 | `admin-bookings-detail` | Chi tiết đơn hàng | `/admin/bookings/{id}` | Hoàn thành | Đã có `deploy-report` cập nhật mới nhất ngày `2026-05-21` |
| 9 | `admin-payments-detail` | Chi tiết giao dịch | `/admin/payments/{id}` | Đang làm | Đã được chốt là màn kế tiếp trong `STACK_SKILLS_INDEX.md`, có API/hook nền nhưng chưa có delivery route hoàn chỉnh |
| 10 | `admin_reports_ratings.md` | Báo cáo đánh giá | `/admin/reports/ratings` | Chưa làm | Mới dừng ở mức tài liệu; chưa có artifact triển khai |
| 11 | `admin_reports_locations.md` | Báo cáo địa điểm | `/admin/reports/locations` | Chưa làm | Mới dừng ở mức tài liệu; chưa có dấu hiệu vào sprint hiện tại |
| 12 | `admin_reports_users.md` | Báo cáo người dùng | `/admin/reports/users` | Chưa làm | Mới dừng ở mức tài liệu; chưa có `deploy-report` |
| 13 | `admin_promotions.md` | Quản lý khuyến mãi | `/admin/promotions` | Chưa làm | Flow planned; chưa phải ưu tiên delivery gần |
| 14 | `admin_site_settings.md` | Cấu hình website | `/admin/settings` | Chưa làm | Flow planned; chưa vào rollout hiện tại |
| 15 | `admin_landing_pages.md` | Quản lý landing pages | Route landing pages admin | Chưa làm | Flow planned; ưu tiên thấp hơn booking/payment operations |

### 2.4 Danh sách đầy đủ các màn admin cần làm trong tương lai

| STT | Doc / Feature | Màn hình | Route | Trạng thái | Route/code hiện có | API readiness | Lý do / Ghi chú | Khuyến nghị |
|---:|---|---|---|---|---|---|---|---|
| 1 | `admin_payments_detail.md` | Chi tiết giao dịch | `/admin/payments/{id}` | Đang làm | Chưa có route detail thật | Ready | `GET /admin/payments/{id}` và `POST /admin/payments/{id}/refund` có thật | Làm ngay |
| 2 | `admin_dashboard.md` | Dashboard | `/admin/dashboard` | Chưa làm | Chưa thấy delivery artifact riêng | Ready | APIs dashboard có thật theo inventory admin | Ưu tiên cao |
| 3 | `admin_users_list.md` | Danh sách người dùng | `/admin/users` | Chưa làm | Chưa có | Ready | Core admin management screen | Ưu tiên cao |
| 4 | `admin_users_detail.md` | Chi tiết người dùng | `/admin/users/{id}` | Chưa làm | Chưa có | Ready | Hợp lý sau user list | Ưu tiên cao |
| 5 | `admin_users_create.md` | Tạo người dùng | `/admin/users/create` | Chưa làm | Chưa có | Ready | API create có thật theo inventory | Ưu tiên cao |
| 6 | `admin_users_edit.md` | Chỉnh sửa người dùng | `/admin/users/{id}/edit` | Chưa làm | Chưa có | Ready | API update có thật theo inventory | Ưu tiên cao |
| 7 | `admin_reports_bookings.md` | Báo cáo đơn hàng | `/admin/reports/bookings` | Chưa làm | Chưa có | Ready | API report bookings có thật theo docs | Ưu tiên cao |
| 8 | `admin_reports_revenue.md` | Báo cáo doanh thu | `/admin/reports/revenue` | Chưa làm | Chưa có | Ready | API revenue/report/export đã có trong inventory | Ưu tiên cao |
| 9 | `admin_reports_ratings.md` | Báo cáo đánh giá | `/admin/reports/ratings` | Chưa làm | Chưa có | Ready | Nằm trong nhóm report còn thiếu delivery | Ưu tiên cao |
| 10 | `admin_reports_locations.md` | Báo cáo địa điểm | `/admin/reports/locations` | Chưa làm | Chưa có | Ready | Nằm trong nhóm report còn thiếu delivery | Ưu tiên cao |
| 11 | `admin_reports_users.md` | Báo cáo người dùng | `/admin/reports/users` | Chưa làm | Chưa có | Ready | Nằm trong nhóm report còn thiếu delivery | Ưu tiên cao |
| 12 | `admin_contacts.md` | Liên hệ hỗ trợ | `/admin/contacts` | Chưa làm | Chưa có | Ready | List/detail/reply là khối quản trị độc lập | Làm sau reports hoặc cùng support tools |
| 13 | `admin_notifications_list.md` | Danh sách thông báo | `/admin/notifications` | Chưa làm | Chưa có | Ready | Hợp lý sau contacts/support | Làm sau |
| 14 | `admin_notifications_send.md` | Gửi thông báo | `/admin/notifications/send` | Chưa làm | Chưa có | Ready | Có thật trong admin inventory | Làm sau |
| 15 | `admin_blog_posts_list.md` | Danh sách bài viết | `/admin/blog-posts` | Chưa làm | Chưa có | Ready | Core CMS module | Làm sau |
| 16 | `admin_blog_posts_create.md` | Tạo bài viết | `/admin/blog-posts/create` | Chưa làm | Chưa có | Ready | Có API create/post upload | Làm sau |
| 17 | `admin_blog_posts_edit.md` | Chỉnh sửa bài viết | `/admin/blog-posts/{id}/edit` | Chưa làm | Chưa có | Ready | Có API update | Làm sau |
| 18 | `admin_blog_categories.md` | Danh mục blog | `/admin/blog-categories` | Chưa làm | Chưa có | Ready | Phụ thuộc module blog | Làm sau |
| 19 | `admin_ratings_list.md` | Danh sách đánh giá | `/admin/ratings` | Chưa làm | Chưa có | Ready | Moderation screen độc lập | Làm sau |
| 20 | `admin_tags_amenities.md` | Tags & tiện ích | `/admin/tags-amenities` hoặc tách route | Chưa làm | Chưa có | Ready | Có CRUD inventory level | Làm sau |
| 21 | `admin_locations_list.md` | Danh sách địa điểm | `/admin/locations` | Chưa làm | Chưa có artifact delivery riêng | Ready | Có thể đã có code nền nhưng chưa đi đủ pipeline | Hardening / delivery riêng |
| 22 | `admin_locations_create.md` | Tạo địa điểm | `/admin/locations/create` | Cần hardening | Đã có delivery gần tương ứng | Ready | Đã có feature `create-new-location-danang-trip`; nên đồng bộ theo doc chuẩn hiện tại | Hardening |
| 23 | `admin_locations_edit.md` | Chỉnh sửa địa điểm | `/admin/locations/{id}/edit` | Chưa làm | Chưa có artifact delivery riêng | Ready | API có thật; chưa thấy deploy artifact riêng | Làm sau |
| 24 | `admin_locations_detail.md` | Chi tiết địa điểm | `/admin/locations/{id}` | Cần hardening | Đã có delivery | Ready | Nên đồng bộ lại với doc chuẩn hiện tại nếu cần | Hardening |
| 25 | `admin_location_categories.md` | Danh mục địa điểm | `/admin/categories` | Cần hardening | Đã có delivery | Ready | Đã có artifact nhưng có thể cần đồng bộ tab/category-subcategory theo doc | Hardening |
| 26 | `admin_subcategories.md` | Danh mục con | `/admin/subcategories` hoặc tab | Chưa làm | Chưa có delivery riêng | Ready | Có tài liệu riêng, chưa có deploy artifact riêng | Làm sau |
| 27 | `admin_tours_list.md` | Danh sách tour | `/admin/tours` | Chưa làm | Chưa có | Ready | Core backoffice module | Làm sau |
| 28 | `admin_tours_create.md` | Tạo tour | `/admin/tours/create` | Chưa làm | Chưa có | Ready | API/create flow có thật | Làm sau |
| 29 | `admin_tours_edit.md` | Chỉnh sửa tour | `/admin/tours/{id}/edit` | Chưa làm | Chưa có | Ready | API/update flow có thật | Làm sau |
| 30 | `admin_tours_detail.md` | Chi tiết tour | `/admin/tours/{id}` | Chưa làm | Chưa có | Ready | Detail/admin analytics around tour | Làm sau |
| 31 | `admin_tour_categories.md` | Danh mục tour | `/admin/tour-categories` | Chưa làm | Chưa có | Ready | Taxonomy admin module | Làm sau |
| 32 | `admin_tour_schedules_list.md` | Lịch khởi hành | `/admin/tour-schedules` | Chưa làm | Chưa có delivery riêng | Ready | API schedule list/status has thật | Làm sau |
| 33 | `admin_tour_schedules_create.md` | Thêm lịch khởi hành | `/admin/tours/{id}/schedules/create` | Cần hardening | Đã có delivery tương ứng | Ready | Đã có `admin-tour-schedule-form`; nên đồng bộ doc chuẩn hiện tại | Hardening |
| 34 | `admin_tour_schedules_edit.md` | Chỉnh sửa lịch khởi hành | `/admin/tour-schedules/{id}/edit` | Cần hardening | Đã có delivery | Ready | Nên đồng bộ doc chuẩn hiện tại | Hardening |
| 35 | `admin_promotions.md` | Danh sách khuyến mãi | `/admin/promotions` | Chưa làm | Chưa có | Planned | Docs ghi planned; API chưa chốt | Backlog sau |
| 36 | `admin_site_settings.md` | Cấu hình website | `/admin/settings` | Chưa làm | Chưa có | Planned | Docs ghi planned | Backlog sau |
| 37 | `admin_landing_pages.md` | Landing pages | `/admin/landing-pages` | Chưa làm | Chưa có | Planned | Docs ghi planned | Backlog sau |

### 2.5 Thứ tự triển khai admin khuyến nghị

| Giai đoạn | Danh sách màn |
|---|---|
| Làm ngay | `admin-payments-detail` |
| Ưu tiên cao kế tiếp | `admin-dashboard`, `admin-users-list/detail/create/edit`, `admin-reports-bookings`, `admin-reports-revenue`, `admin-reports-ratings`, `admin-reports-locations`, `admin-reports-users` |
| Giai đoạn support/CMS | `admin-contacts`, `admin-notifications-list/send`, `admin-blog-posts-list/create/edit`, `admin-blog-categories`, `admin-ratings-list`, `admin-tags-amenities` |
| Giai đoạn catalog operations | `admin-locations-list/edit/subcategories`, `admin-tours-list/create/edit/detail`, `admin-tour-categories`, `admin-tour-schedules-list` |
| Hardening đã có nền | `admin-locations-create`, `admin-locations-detail`, `admin-location-categories`, `admin-tour-schedules-create`, `admin-tour-schedules-edit` |
| Planned backlog | `admin-promotions`, `admin-site-settings`, `admin-landing-pages` |

### 2.6 Nhận định ngắn

| Nhận định | Giải thích |
|---|---|
| Trục vận hành booking admin đã khá đầy | Đã có booking list và booking detail |
| Điểm hở lớn nhất hiện tại | `admin-payments-detail` vì payment list đã có nhưng thiếu route detail để audit và refund |
| Backlog sau màn hiện tại | Bộ `admin_reports_*`, rồi mới đến các flow planned như promotions/settings/landing pages |

---

## 3. Kết luận chung

| Dự án | Tổng màn chính | Hoàn thành | Đang làm | Chưa làm | % hoàn thành theo tổng màn | Màn đang làm |
|---|---:|---:|---:|---:|---:|---|
| `danangtrip-web` | 35 | 6 | 1 | 28 | 17.1% | `user-booking-detail` |
| `danangtrip-admin` | 40 | 8 | 1 | 31 | 20.0% | `admin-payments-detail` |

| Kết luận | Diễn giải |
|---|---|
| Hai dự án đang đi đúng trục hậu booking | Web đang khép `booking detail`, admin đang khép `payment detail` |
| Cần ưu tiên hoàn tất màn đang làm trước khi mở rộng | Nếu chen sang reports/favorites/notifications/planned features quá sớm sẽ làm phân mảnh delivery |
| Báo cáo này nên cập nhật sau mỗi lần có `deploy-report` mới | Khi một màn đi hết pipeline, chỉ cần đổi trạng thái và tính lại % |
| Nguồn backlog tương lai đã được gộp vào báo cáo này | Không cần tách riêng roadmap cho `web` hay `admin` nữa |
