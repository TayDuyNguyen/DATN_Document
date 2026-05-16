# Mapping prototype màn hình với tài liệu `docs/page`

> Cập nhật: 14/05/2026  
> Mục tiêu: đối chiếu nhanh giữa prototype trong `screen` và tài liệu nghiệp vụ trong `docs/page`.

---

## 1. Prototype đã có và tài liệu tương ứng

| Prototype | Tài liệu `docs/page` | Ghi chú |
|---|---|---|
| `1_Guest_Flows/01.*-Trang_Chu_Guest` | `user_home.md` | Có nhiều version |
| `1_Guest_Flows/02.*-Tim_Kiem` | `user_search.md`, `user_search_logged_in.md` | Logged-in history là planned |
| `1_Guest_Flows/03.1-Danh_Muc_Dia_Diem` | `user_locations_by_category.md` | |
| `1_Guest_Flows/03.2-Danh_Sach_Dia_Diem` | `user_locations_list.md` | |
| `1_Guest_Flows/04.*-Chi_Tiet_Dia_Diem*` | `user_location_detail.md` | |
| `1_Guest_Flows/04.3-Dia_Diem_Lan_Can` | `user_locations_nearby.md` | |
| `1_Guest_Flows/05.*-Gioi_Thieu_Da_Nang` | `user_destination_tour_landing.md` | Chỉ tương đương một phần |
| `1_Guest_Flows/06.1-Cam_Nang_Du_Lich` | `user_blog_list.md` | Chưa có detail/category |
| `1_Guest_Flows/07.1-Danh_Sach_Tour` | `user_tours_list.md` | |
| `1_Guest_Flows/07.2`, `07.3-Chi_Tiet_Tour` | `user_tour_detail.md` | |
| `1_Guest_Flows/08-Trang_Lien_He` | `user_contact.md` | |
| `1_Guest_Flows/09-Goi_Y_Cho_Ban` | `user_recommendations.md`, `user_home_logged_in.md` | Nên chuyển sang user flow |
| `2_User_Flows/02-Chi_Tiet_Dia_Diem_User` | `user_location_detail_logged_in.md` | |
| `2_User_Flows/03.1-Viet_Danh_Gia` | `user_rating_modal.md` | |
| `2_User_Flows/03.2`, `03.3-Danh_Gia_Cua_Toi` | `user_my_ratings.md` | |
| `2_User_Flows/04.*-Xac_Thuc_Email*` | `user_verify_email.md` | |
| `2_User_Flows/05.1-Trang_Ca_Nhan` | `user_profile.md` | |
| `2_User_Flows/05.2-Doi_Mat_Khau` | `user_profile_password.md` | |
| `2_User_Flows/05.3-Xoa_Tai_Khoan` | `user_profile_delete.md` | API planned |
| `2_User_Flows/07-Dia_Diem_Yeu_Thich` | `user_favorites.md` | |
| `2_User_Flows/08.1-Danh_Sach_Don_Dat_Tour` | `user_bookings_list.md` | |
| `2_User_Flows/08.2`, `08.3-Chi_Tiet_Don_Dat_Tour` | `user_booking_detail.md` | |
| `2_User_Flows/09.1-Dat_Tour` | `user_tour_booking.md` | |
| `2_User_Flows/09.2`, `09.3-Thanh_Toan` | `user_payment.md` | |
| `2_User_Flows/09.4-Thanh_Toan_Thanh_Cong` | `user_payment_result.md` | |
| `2_User_Flows/10-Thong_Bao` | `user_notifications.md` | |
| `3_Admin_Flows/01-Dashboard_Tong_Quan` | `admin_dashboard.md` | |
| `3_Admin_Flows/03.1` - `03.4` | `admin_locations_list.md`, `admin_locations_create.md`, `admin_locations_edit.md`, `admin_locations_detail.md` | |
| `3_Admin_Flows/04.1` - `04.4` | `admin_users_list.md`, `admin_users_edit.md`, `admin_users_create.md`, `admin_users_detail.md` | |
| `3_Admin_Flows/05.*-Danh_Muc_Con` | `admin_location_categories.md`, `admin_subcategories.md` | Cần tách rõ nếu triển khai UI |
| `3_Admin_Flows/06.1`, `06.2` | `admin_payments_list.md`, `admin_payments_detail.md` | |
| `3_Admin_Flows/07.1-Bao_Cao_Don_Hang` | `admin_reports_bookings.md` | |
| `3_Admin_Flows/07.2-Bao_Cao_Doanh_Thu` | `admin_reports_revenue.md` | |
| `3_Admin_Flows/07.3-Danh_Sach_Danh_Gia` | `admin_ratings_list.md` | |
| `3_Admin_Flows/08.1-Tags_Tien_Ich` | `admin_tags_amenities.md` | |
| `3_Admin_Flows/09.1` - `09.4` | `admin_tours_list.md`, `admin_tours_create.md`, `admin_tours_edit.md`, `admin_tours_detail.md` | |
| `3_Admin_Flows/09.5-Danh_Muc_Tour` | `admin_tour_categories.md` | |
| `3_Admin_Flows/09.6` - `09.8` | `admin_tour_schedules_list.md`, `admin_tour_schedules_create.md`, `admin_tour_schedules_edit.md` | |
| `3_Admin_Flows/10.1`, `10.2` | `admin_bookings_list.md`, `admin_bookings_detail.md` | |
| `3_Admin_Flows/02.1`, `02.2`, `11.1`, `11.2` | `admin_blog_posts_list.md`, `admin_blog_posts_create.md`, `admin_blog_posts_edit.md` | `02.2` là trạng thái duyệt bài |
| `3_Admin_Flows/11.3-Danh_Muc_Blog` | `admin_blog_categories.md` | |
| `3_Admin_Flows/12.1`, `12.2` | `admin_notifications_list.md`, `admin_notifications_send.md` | |
| `3_Admin_Flows/13.1`, `13.2` | `admin_contacts_list.md`, `admin_contacts_detail.md`, `admin_contacts.md` | |

---

## 2. Tài liệu đã có nhưng prototype còn thiếu

### User/Public

| Tài liệu | Prototype cần bổ sung | Ưu tiên |
|---|---|---|
| `user_login.md` | `1_Guest_Flows/10-Dang_Nhap.html` | Cao |
| `user_register.md` | `1_Guest_Flows/11-Dang_Ky.html` | Cao |
| `user_forgot_password.md` | `1_Guest_Flows/12-Quen_Mat_Khau.html` | Cao |
| `user_reset_password.md` | `1_Guest_Flows/13-Dat_Lai_Mat_Khau.html` | Cao |
| `user_blog_detail.md` | `1_Guest_Flows/06.2-Chi_Tiet_Blog.html` | Cao |
| `user_blog_by_category.md` | `1_Guest_Flows/06.3-Blog_Theo_Danh_Muc.html` | Trung bình |
| `user_tours_by_category.md` | `1_Guest_Flows/07.4-Tour_Theo_Danh_Muc.html` | Cao |
| `user_tour_departure_select.md` | `1_Guest_Flows/07.5-Chon_Lich_Khoi_Hanh.html` | Cao |
| `user_home_logged_in.md` | `2_User_Flows/01-Trang_Chu_User.html` | Cao |
| `user_booking_by_code.md` | `2_User_Flows/08.4-Tra_Cuu_Don_Theo_Ma.html` | Cao |
| `user_booking_invoice.md` | `2_User_Flows/08.5-Hoa_Don_Dat_Tour.html` | Cao |
| `user_rating_edit_modal.md` | Modal trong màn đánh giá | Trung bình |
| `user_rating_delete.md` | Confirm trong màn đánh giá | Trung bình |
| `user_rating_helpful.md` | Action trong detail địa điểm/tour | Trung bình |
| `user_cart.md` | `2_User_Flows/11-Gio_Hang.html` | Planned |

### Admin

| Tài liệu | Prototype cần bổ sung | Ưu tiên |
|---|---|---|
| `admin_reports_ratings.md` | `3_Admin_Flows/07.4-Bao_Cao_Danh_Gia.html` | Cao |
| `admin_reports_locations.md` | `3_Admin_Flows/07.5-Bao_Cao_Dia_Diem.html` | Cao |
| `admin_reports_users.md` | `3_Admin_Flows/07.6-Bao_Cao_Nguoi_Dung.html` | Cao |
| `admin_promotions.md` | `3_Admin_Flows/14.1-Danh_Sach_Khuyen_Mai.html` và form create/edit | Planned |
| `admin_site_settings.md` | `3_Admin_Flows/15.1-Cau_Hinh_Website.html` | Planned |
| `admin_landing_pages.md` | `3_Admin_Flows/15.2-Landing_Pages.html` | Planned |

---

## 3. Ghi chú chuẩn hóa khi triển khai code

1. Route chi tiết đơn hàng nên thống nhất theo `id`: `/admin/bookings/{id}`, `/bookings/{id}`. Nếu UI hiển thị mã đơn thì dùng `booking_code` làm dữ liệu hiển thị hoặc dùng riêng route `/bookings/code/{booking_code}` cho user.
2. Màn `Goi_Y_Cho_Ban` nên đặt trong user flow hoặc dùng chung nhưng phải thể hiện rõ cần đăng nhập để gọi `GET /recommendations`.
3. `Gioi_Thieu_Da_Nang` không thay thế hoàn toàn landing tour. Landing tour cần tập trung vào danh sách tour, bộ lọc, lịch khởi hành, giá, khuyến mãi.
4. Các màn planned vẫn giữ trong tài liệu để định hướng, nhưng khi code phải có fallback nếu API/database chưa có.
