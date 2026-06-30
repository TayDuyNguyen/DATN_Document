# TESTCASE INDEX

## Phạm vi rà soát

* User Web: `D:\DATN\danangtrip-web`
* Admin Web: `D:\DATN\danangtrip-admin`
* Test case folder: `D:\DATN\DATN_Tài liệu\testcases`

## Màn hình detail/modal/panel đã tạo mới hoặc cập nhật theo source code

| Screen | Route | File Source | Test Case File | Status |
| ------ | ----- | ----------- | -------------- | ------ |
| Chi tiết tour | `/[locale]/tours/[slug]` | `danangtrip-web/src/app/[locale]/(main)/(public)/tours/[slug]/page.tsx` | `01_guest_flows/07_tour_detail.md` | Updated |
| Chọn lịch khởi hành và đặt tour | `/[locale]/tours/[slug]/departures`, `/[locale]/tours/[slug]/book` | `danangtrip-web/src/app/[locale]/(main)/(public)/tours/[slug]/departures/page.tsx`, `danangtrip-web/src/app/[locale]/(main)/(protected)/tours/[slug]/book/page.tsx` | `01_guest_flows/17_tour_departures.md` | Updated |
| Đặt lại mật khẩu | `/[locale]/reset-password` | `danangtrip-web/src/app/[locale]/(auth)/reset-password/page.tsx` | `01_guest_flows/21_reset_password.md` | Created |
| Chi tiết booking người dùng | `/[locale]/profile/bookings/[id]`, `/[locale]/profile/bookings/code/[bookingCode]` | `danangtrip-web/src/app/[locale]/(main)/(protected)/profile/bookings/[id]/page.tsx`, `danangtrip-web/src/app/[locale]/(main)/(protected)/profile/bookings/code/[bookingCode]/page.tsx` | `02_user_flows/06_booking_history.md` | Updated |
| Kết quả thanh toán | `/[locale]/payment/result` | `danangtrip-web/src/app/[locale]/(main)/(protected)/payment/result/page.tsx` | `02_user_flows/12_payment_result.md` | Created |
| Dashboard Thành viên | `/[locale]/dashboard`, `/dashboard/users`, `/dashboard/settings` | `danangtrip-web/src/app/[locale]/(main)/(protected)/dashboard/*` | `02_user_flows/13_user_dashboard.md` | Created |
| Chi tiết địa điểm | `/[locale]/locations/[slug]` | `danangtrip-web/src/app/[locale]/(main)/(public)/locations/[slug]/page.tsx` | `01_guest_flows/19_location_detail.md` | Created |
| Chi tiết bài viết blog | `/[locale]/blog/[slug]` | `danangtrip-web/src/app/[locale]/(main)/(public)/blog/[slug]/page.tsx` | `01_guest_flows/20_blog_detail.md` | Created |
| Admin chi tiết booking | `/admin/bookings/detail/:id` | `danangtrip-admin/src/pages/Bookings/BookingDetail/index.tsx` | `03_admin_flows/04b_booking_detail.md` | Updated |
| Admin chi tiết thanh toán | `/admin/payments/detail/:id` | `danangtrip-admin/src/pages/Payments/PaymentDetail/index.tsx` | `03_admin_flows/13b_payment_detail.md` | Created |
| Admin chi tiết người dùng | `/admin/users/detail/:id` | `danangtrip-admin/src/pages/Users/UserDetail/index.tsx` | `03_admin_flows/02d_user_detail.md` | Updated |
| Admin chi tiết địa điểm | `/admin/locations/detail/:id` | `danangtrip-admin/src/pages/Locations/LocationDetail/index.tsx` | `03_admin_flows/05d_location_detail.md` | Updated |
| Admin chi tiết bài viết | `/admin/blog-posts/:id` | `danangtrip-admin/src/pages/Blog/BlogPostDetail/index.tsx` | `03_admin_flows/06d_blog_detail.md` | Updated |
| Admin modal chi tiết tour | `/admin/tours/list` modal | `danangtrip-admin/src/pages/Tours/TourList/components/TourDetailModal.tsx` | `03_admin_flows/03d_tour_detail_modal.md` | Created |
| Admin lịch khởi hành tour | `/admin/tours/schedules`, `/admin/tours/:id/schedules/create`, `/admin/tours/schedules/edit/:id` | `danangtrip-admin/src/pages/Tours/TourSchedules/index.tsx`, `TourScheduleCreate/index.tsx`, `TourScheduleEdit/index.tsx` | `03_admin_flows/03e`–`03g` (list/create/edit) | Updated |
| Admin chi tiết lịch KH (API + read-only panels) | `/admin/tours/schedules/edit/:id` | `TourScheduleEdit/index.tsx` (`ScheduleInfoBox`, `ScheduleStatsBlock`) | `03_admin_flows/03h_tour_schedule_detail.md` | Updated |
| Admin chi tiết liên hệ panel | `/admin/contacts?id=:id` | `danangtrip-admin/src/pages/Contacts/index.tsx`, `ContactDetailPanel.tsx` | `03_admin_flows/09_contacts.md` | Updated |
| Admin quản lý đánh giá | `/admin/ratings` | `danangtrip-admin/src/pages/Ratings/index.tsx` | `03_admin_flows/08_ratings.md` | Updated |
| Admin Báo cáo thống kê | `/admin/reports/revenue`, `/admin/reports/bookings`, `/admin/reports/locations`, `/admin/reports/ratings`, `/admin/reports/users` | `danangtrip-admin/src/pages/Reports/*` | `03_admin_flows/10_reports.md` | Updated |
| Admin Quản lý trang đích | `/admin/landing-pages` | `danangtrip-admin/src/pages/LandingPages/index.tsx` | `03_admin_flows/18_landing_pages.md` | Created |

## Test case cũ đang tồn tại và được liên kết với các màn còn lại

| Screen | Route | File Source | Test Case File | Status |
| ------ | ----- | ----------- | -------------- | ------ |
| Trang chủ user | `/[locale]` | `danangtrip-web/src/app/[locale]/(main)/page.tsx` | `01_guest_flows/01_home.md` | Updated previously |
| Login user | `/[locale]/login` | `danangtrip-web/src/app/[locale]/(auth)/login/page.tsx` | `01_guest_flows/02_login.md` | Existing |
| Register user | `/[locale]/register` | `danangtrip-web/src/app/[locale]/(auth)/register/page.tsx` | `01_guest_flows/03_register.md` | Existing |
| Forgot password | `/[locale]/forgot-password` | `danangtrip-web/src/app/[locale]/(auth)/forgot-password/page.tsx` | `01_guest_flows/04_forgot_password.md` | Existing |
| Verify email | `/[locale]/verify-email` | `danangtrip-web/src/app/[locale]/(auth)/verify-email/page.tsx` | `01_guest_flows/05_verify_email.md` | Existing |
| Danh sách tour | `/[locale]/tours` | `danangtrip-web/src/app/[locale]/(main)/(public)/tours/page.tsx` | `01_guest_flows/06_tour_list.md` | Existing |
| Nearby | `/[locale]/nearby` | `danangtrip-web/src/app/[locale]/(main)/(public)/nearby/page.tsx` | `01_guest_flows/11_nearby.md` | Existing |
| Search | `/[locale]/search` | `danangtrip-web/src/app/[locale]/(main)/(public)/search/page.tsx` | `01_guest_flows/12_search.md` | Existing |
| About | `/[locale]/about` | `danangtrip-web/src/app/[locale]/(main)/(public)/about/page.tsx` | `01_guest_flows/13_about.md` | Existing |
| Category locations | `/[locale]/categories/[slug]/locations` | `danangtrip-web/src/app/[locale]/(main)/(public)/categories/[slug]/locations/page.tsx` | `01_guest_flows/14_categories_locations.md` | Existing |
| Đà Nẵng guide | `/[locale]/du-lich-da-nang` | `danangtrip-web/src/app/[locale]/(main)/(public)/du-lich-da-nang/page.tsx` | `01_guest_flows/15_danang_guide.md` | Existing |
| Category tours | `/[locale]/tour-categories/[slug]/tours` | `danangtrip-web/src/app/[locale]/(main)/(public)/tour-categories/[slug]/tours/page.tsx` | `01_guest_flows/16_tour_categories_tours.md` | Existing |
| Locations list | `/[locale]/locations` | `danangtrip-web/src/app/[locale]/(main)/(public)/locations/page.tsx` | `01_guest_flows/18_locations_list.md` | Existing |
| Profile edit | `/[locale]/profile` | `danangtrip-web/src/app/[locale]/(main)/(protected)/profile/page.tsx` | `02_user_flows/01_profile_edit.md` | Existing |
| Change password | `/[locale]/profile/password` | `danangtrip-web/src/app/[locale]/(main)/(protected)/profile/password/page.tsx` | `02_user_flows/02_password_change.md` | Existing |
| Cart | `/[locale]/cart` | `danangtrip-web/src/app/[locale]/(main)/(public)/cart/page.tsx` | `02_user_flows/04_cart.md` | Existing |
| Payment page | `/[locale]/payment` | `danangtrip-web/src/app/[locale]/(main)/(protected)/payment/page.tsx` | `02_user_flows/05_payment.md` | Existing |
| Delete profile | `/[locale]/profile/delete` | `danangtrip-web/src/app/[locale]/(main)/(protected)/profile/delete/page.tsx` | `02_user_flows/07_profile_delete.md` | Existing |
| Favorites | `/[locale]/profile/favorites` | `danangtrip-web/src/app/[locale]/(main)/(protected)/profile/favorites/page.tsx` | `02_user_flows/08_profile_favorites.md` | Existing |
| Profile notifications | `/[locale]/profile/notifications` | `danangtrip-web/src/app/[locale]/(main)/(protected)/profile/notifications/page.tsx` | `02_user_flows/09_profile_notifications.md` | Existing |
| Profile ratings | `/[locale]/profile/ratings` | `danangtrip-web/src/app/[locale]/(main)/(protected)/profile/ratings/page.tsx` | `02_user_flows/10_profile_reviews.md` | Existing |
| Recommendations | `/[locale]/profile/recommendations` | `danangtrip-web/src/app/[locale]/(main)/(protected)/profile/recommendations/page.tsx` | `02_user_flows/11_profile_recommendations.md` | Existing |
| Admin dashboard | `/dashboard` | `danangtrip-admin/src/pages/Dashboard/index.tsx` | `03_admin_flows/01_dashboard.md` | Updated previously |
| Admin users list/create/edit | `/admin/users`, `/admin/users/create`, `/admin/users/edit/:id` | `danangtrip-admin/src/pages/Users` | `03_admin_flows/02a_user_list.md`, `02b_user_create.md`, `02c_user_edit.md` | Updated previously |
| Admin tours list/create/edit | `/admin/tours/list`, `/admin/tours/create`, `/admin/tours/edit/:id` | `danangtrip-admin/src/pages/Tours` | `03_admin_flows/03a_tour_list.md`, `03b_tour_create.md`, `03c_tour_edit.md` | Updated previously |
| Admin tour schedules list/create/edit | `/admin/tours/schedules`, `/admin/tours/:id/schedules/create`, `/admin/tours/schedules/edit/:id` | `danangtrip-admin/src/pages/Tours` | `03_admin_flows/03e_tour_schedule_list.md`, `03f_tour_schedule_create.md`, `03g_tour_schedule_edit.md` | Existing |
| Admin bookings list | `/admin/bookings` | `danangtrip-admin/src/pages/Bookings/BookingList/index.tsx` | `03_admin_flows/04a_booking_list.md` | Existing |
| Admin locations list/create/edit | `/admin/locations`, `/admin/locations/create`, `/admin/locations/edit/:id` | `danangtrip-admin/src/pages/Locations` | `03_admin_flows/05a_location_list.md`, `05b_location_create.md`, `05c_location_edit.md` | Updated previously |
| Admin blog list/create/edit | `/admin/blog-posts`, `/admin/blog-posts/create`, `/admin/blog-posts/edit/:id` | `danangtrip-admin/src/pages/Blog` | `03_admin_flows/06a_blog_list.md`, `06b_blog_create.md`, `06c_blog_edit.md` | Updated previously |
| Promotions | `/admin/promotions` | `danangtrip-admin/src/pages/Promotions/index.tsx` | `03_admin_flows/07_promotions.md` | Existing |
| Contacts | `/admin/contacts` | `danangtrip-admin/src/pages/Contacts/index.tsx` | `03_admin_flows/09_contacts.md` | Updated |
| Reports | `/admin/reports/*` | `danangtrip-admin/src/pages/Reports` | `03_admin_flows/10_reports.md` | Existing |
| Settings | `/admin/settings` | `danangtrip-admin/src/pages/Settings/index.tsx` | `03_admin_flows/11_settings.md` | Existing |
| Admin login | `/login` | `danangtrip-admin/src/pages/Login/index.tsx` | `03_admin_flows/12_login.md` | Existing |
| Admin payments list | `/admin/payments` | `danangtrip-admin/src/pages/Payments/PaymentList/index.tsx` | `03_admin_flows/13a_payment_list.md` | Existing |
| Admin notifications | `/admin/notifications`, `/admin/notifications/send` | `danangtrip-admin/src/pages/Notifications` | `03_admin_flows/14_notifications.md` | Existing |
| Tour categories | `/admin/tour-categories` | `danangtrip-admin/src/pages/Tours/TourCategories/index.tsx` | `03_admin_flows/15_tour_categories.md` | Existing |
| Location categories | `/admin/location-categories` | `danangtrip-admin/src/pages/Locations/LocationCategories/index.tsx` | `03_admin_flows/16_location_categories.md` | Existing |
| Blog categories | `/admin/blog-categories` | `danangtrip-admin/src/pages/Blog/BlogCategories/index.tsx` | `03_admin_flows/17_blog_categories.md` | Existing |

## Ghi chú

* Tất cả các màn hình "Need Review" trước đây đều đã được hoàn thiện hóa bằng tài liệu chi tiết bám sát logic source code thực tế.
* Các liên kết và trạng thái mới đã được cập nhật đầy đủ và chính xác vào bảng chỉ mục.
