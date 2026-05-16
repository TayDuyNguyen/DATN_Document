# BA & System Architecture Consistency Review

> Ngày cập nhật: 14/05/2026  
> Phạm vi rà soát:  
> - Tài liệu màn hình: `docs/page` (80 file screen spec + 5 component spec)  
> - Screen prototypes: `screen/` (79 file HTML + PNG từ Stitch)  
> - Danh sách API: `docs/api`  
> - Database schema: `docs/database/database.dbml`  
> Vai trò: Senior Business Analyst & System Architect  
> Trạng thái: Bản sau chuẩn hóa tài liệu + rà soát screen coverage

---

## 1. Kết luận tổng quan

Ba lớp tài liệu hiện đã được chuẩn hóa đồng bộ ở mức kiến trúc:

| Hạng mục | Kết quả |
|---|---:|
| Tổng file screen spec trong `docs/page` | 80 |
| Tổng file component spec trong `docs/page` | 5 |
| File tham khảo (đã chuyển sang `docs/reference`) | 6 |
| File trùng lặp đã xóa | 5 |
| Tổng screen prototype (HTML) trong `screen/` | 79 |
| Page docs CÓ prototype tương ứng | 58 |
| Page docs THIẾU prototype | 22 |
| Screen prototype KHÔNG có page doc | 21 |
| Tổng API endpoint trong `docs/api` | 214 |
| API không có chủ trong tài liệu màn | 0 |
| Tổng bảng DBML | 43 |
| Ref DBML trỏ tới bảng không tồn tại | 0 |

Kết quả kiểm tra cuối:

```text
PAGE_TOTAL=80 (screen spec) + 5 (component spec)
PAGE_PASS=80
NEED_FIX=0
SCREEN_PROTOTYPES=79
SCREEN_MATCHED=58
SCREEN_MISSING=22 (5 High + 8 Medium + 9 Low)
SCREEN_EXTRA=21 (14 variants + 2 unique + 5 utility)
API_COUNT=214
USED_API_COUNT=214
ORPHAN_COUNT=0
DB_TABLES=43
MISSING_REF_TABLES=0
```

**Kết luận:** tài liệu màn hình, API và DBML nhất quán về kiến trúc. 58/80 page docs đã có prototype từ Stitch. Còn **13 màn ưu tiên cao/trung** cần bổ sung prototype (auth flow, blog detail, reports, booking utils).

---

## 2. Rà soát Screen Prototype Coverage

> Ngày rà soát: 14/05/2026
> Nguồn prototype: Google Stitch export → `screen/` (4 thư mục: Guest, User, Admin, Others)

### 2.0.1 Dọn dẹp tài liệu đã thực hiện

| Hành động | File | Lý do |
|---|---|---|
| Chuyển → `docs/reference/` | `list_page.md`, `list_page_user.md`, `screen_gap_analysis.md`, `travel_com_benchmark_flow.md`, `future_service_extensions.md`, `system_runtime_endpoints.md` | File meta/planning, không phải screen spec |
| Xóa (trùng lặp) | `admin_contacts_list.md`, `admin_contacts_detail.md` | Giữ `admin_contacts.md` (master-detail), xóa 2 approach xung đột |
| Xóa + merge vào file gốc | `user_search_logged_in.md`, `user_home_logged_in.md`, `user_location_detail_logged_in.md` | Nội dung đã merge vào file gốc dưới section "Điểm khác biệt khi đã đăng nhập" |

### 2.0.2 Page docs THIẾU screen prototype

#### HIGH — Core flow, cần prototype trước khi dev (5 màn)

| Page Doc | Tên màn | Route | Lý do |
|---|---|---|---|
| `user_login.md` | Đăng nhập | `/login` | Core auth, mọi user phải đi qua |
| `user_register.md` | Đăng ký | `/register` | Core auth, onboarding flow |
| `user_forgot_password.md` | Quên mật khẩu | `/forgot-password` | Core auth recovery |
| `user_reset_password.md` | Đặt lại mật khẩu | `/reset-password` | Core auth recovery |
| `user_blog_detail.md` | Chi tiết Bài viết Blog | `/blog/{slug}` | Content page chính, SEO quan trọng |

#### MEDIUM — Tính năng phụ trợ quan trọng (8 màn)

| Page Doc | Tên màn | Route | Ghi chú |
|---|---|---|---|
| `user_tour_departure_select.md` | Chọn lịch khởi hành | modal trong `/tours/{slug}` | Bước trước đặt tour |
| `user_booking_by_code.md` | Đơn đặt theo Mã đơn | `/bookings/code/{code}` | Access từ email xác nhận |
| `user_booking_invoice.md` | Hóa đơn PDF | `/bookings/{id}/invoice` | Tính năng nghiệp vụ |
| `user_tours_by_category.md` | Tour theo Danh mục | `/tour-categories/{slug}/tours` | Landing page SEO |
| `admin_location_categories.md` | Danh mục Địa điểm (Tab 1) | `/admin/categories` | Chỉ Tab 2 subcategories có prototype |
| `admin_reports_ratings.md` | Báo cáo Đánh giá | `/admin/reports/ratings` | Nhóm 3 reports thiếu |
| `admin_reports_locations.md` | Báo cáo Địa điểm | `/admin/reports/locations` | (cùng nhóm) |
| `admin_reports_users.md` | Báo cáo Người dùng | `/admin/reports/users` | (cùng nhóm) |

#### LOW — Component nhỏ / Planned features (9 màn)

| Page Doc | Tên màn | Ghi chú |
|---|---|---|
| `user_rating_edit_modal.md` | Modal Sửa đánh giá | Component, tương tự viết đánh giá |
| `user_rating_delete.md` | Dialog Xóa đánh giá | Chỉ là confirm dialog |
| `user_rating_helpful.md` | Button Hữu ích | Inline button |
| `user_rating_images_lightbox.md` | Lightbox ảnh đánh giá | Component gallery |
| `user_cart.md` | Giỏ hàng tour | **Planned** |
| `user_destination_tour_landing.md` | Landing tour điểm đến | **Planned** |
| `admin_promotions.md` | Quản lý khuyến mãi | **Planned** |
| `admin_site_settings.md` | Cấu hình website | **Planned** |
| `admin_landing_pages.md` | Quản lý Landing Pages | **Planned** |

### 2.0.3 Screen prototypes KHÔNG có page doc

#### Màn hình riêng biệt cần bổ sung page doc (2)

| Screen File | Tên màn | Đề xuất |
|---|---|---|
| `1_Guest/05.1-Gioi_Thieu_Da_Nang.html` | Giới thiệu Đà Nẵng | Cần tạo `user_about_danang.md` |
| `3_Admin/02.2-Duyet_Bai_Viet.html` | Duyệt Bài viết (Moderator) | Merge vào `admin_blog_posts_list.md` hoặc tạo riêng |

#### Design variants — đã có page doc ở bản gốc (14)

Các file v2, v3, sub-state thuộc page doc gốc: Trang chủ (3 variants), Tìm kiếm (2v), Chi tiết Địa điểm Mỹ Khê, Giới thiệu ĐN v2, Chi tiết Tour v2, Đánh giá v3, Xác thực Email (3 sub-states), Chi tiết đơn v2, Thanh toán v2, Danh mục con v2, Hộp thư hỗ trợ.

#### System / Utility — không cần page doc (5)

Trang 403, 404, Bảo trì, Pagination Components, Style Guide.

---

## 3. Những việc đã chuẩn hóa

### 3.1. Chuẩn hóa tài liệu màn hình `docs/page`

Đã rà soát và bổ sung tiêu chuẩn cho toàn bộ nhóm màn chính:

| Nhóm | Việc đã làm | Kết quả |
|---|---|---|
| Admin dashboard | Bổ sung validation date range, period, chart empty/error state, permission state | Đạt |
| Admin tour/location detail | Bổ sung rule trạng thái, xóa, toggle featured/hot, empty ratings/schedules/images | Đạt |
| Admin reports | Bổ sung validation filter, date range, export consistency, empty chart/table | Đạt |
| Admin settings | Bổ sung validation `value_type`, hotline, email, payment methods, SEO, fallback config | Đạt |
| User booking | Bổ sung validation list, booking code, cancel rule, invoice rule, passengers, timeline | Đạt |
| User cart | Bổ sung rule session, số khách, sức chứa, promotion, expired item, checkout lỗi | Đạt |
| User rating | Bổ sung flow edit/delete/helpful: quyền thao tác, confirm, optimistic update, rollback | Đạt |
| User blog | Bổ sung not found, empty category, unpublished post, related posts fallback | Đạt |
| User landing tour | Bổ sung validation filter giá/ngày/danh mục, SEO fallback, landing fallback | Đạt |
| User favorites | Chuẩn hóa endpoint thành `POST /user/favorites` và `DELETE /user/favorites` | Đạt |
| System/runtime endpoints | Tạo tài liệu chủ sở hữu cho auth runtime, payment callback, health check | Đạt |
| Future service extensions | Tạo tài liệu planned cho flight/hotel/combo/visa | Đạt |

### 3.2. Chuẩn hóa API mồ côi

Trước đó có một số API không có màn/chức năng sở hữu rõ ràng. Đã gán chủ sở hữu tài liệu như sau:

| API | Chủ sở hữu hiện tại | Ghi chú |
|---|---|---|
| `GET /auth/me` | `system_runtime_endpoints.md` | App bootstrap/auth guard |
| `POST /auth/refresh` | `system_runtime_endpoints.md` | Auth interceptor |
| `POST /payments/callback` | `system_runtime_endpoints.md` | Webhook backend, không phải UI |
| `GET /ping` | `system_runtime_endpoints.md` | Monitoring |
| `GET /health` | `system_runtime_endpoints.md` | Monitoring planned |
| `GET /ratings/{id}/images` | `user_rating_images_lightbox.md` | Modal xem ảnh đánh giá |
| `GET /flights/search` | `future_service_extensions.md` | Phase sau |
| `GET /hotels/search` | `future_service_extensions.md` | Phase sau |
| `GET /flight-hotels/search` | `future_service_extensions.md` | Phase sau |
| `GET /visa/products` | `future_service_extensions.md` | Phase sau |

Kết quả hiện tại: **không còn API mồ côi**.

### 3.3. Chuẩn hóa API quận/huyện

Đã thống nhất endpoint lọc quận/huyện cho địa điểm:

| Trước | Sau |
|---|---|
| Có cả `GET /districts` và `GET /locations/districts` | Dùng chuẩn `GET /locations/districts` |

Lý do: dữ liệu quận nên lấy động theo địa điểm hiện có, phục vụ trực tiếp màn danh sách địa điểm và filter.

### 3.4. Chuẩn hóa DBML cho các planned flow

Đã bổ sung các bảng phục vụ nghiệp vụ planned nhưng đã xuất hiện trong API/page docs:

| Bảng | Phục vụ nghiệp vụ |
|---|---|
| `landing_pages` | Landing tour/điểm đến, SEO page |
| `site_settings` | Cấu hình website/public config |
| `promotions` | Khuyến mãi/coupon/quà tặng |
| `promotion_targets` | Điều kiện áp dụng promotion |
| `booking_promotions` | Promotion đã áp dụng vào booking |
| `carts` | Giỏ hàng theo user/session |
| `cart_items` | Item trong giỏ hàng |
| `booking_passengers` | Danh sách hành khách trong booking |
| `booking_status_histories` | Timeline trạng thái đơn |
| `payment_status_histories` | Timeline trạng thái thanh toán/callback |

Đã kiểm tra DBML:

```text
DB_TABLES=43
MISSING_REF_TABLES=0
```

---

## 4. Kiểm tra từng nhóm màn

| Nhóm màn | API có trong danh sách? | DB hỗ trợ? | Validation đầy đủ? | Flow rõ ràng? | Kết luận |
|---|---|---|---|---|---|
| Admin dashboard | ✅ | ✅ | ✅ | ✅ | Đạt |
| Admin tours | ✅ | ✅ | ✅ | ✅ | Đạt |
| Admin tour categories/schedules | ✅ | ✅ | ✅ | ✅ | Đạt |
| Admin locations/categories/subcategories | ✅ | ✅ | ✅ | ✅ | Đạt |
| Admin bookings/payments | ✅ | ✅ | ✅ | ✅ | Đạt |
| Admin ratings | ✅ | ✅ | ✅ | ✅ | Đạt |
| Admin users | ✅ | ✅ | ✅ | ✅ | Đạt |
| Admin blog | ✅ | ✅ | ✅ | ✅ | Đạt |
| Admin tags/amenities | ✅ | ✅ | ✅ | ✅ | Đạt |
| Admin notifications | ✅ | ✅ | ✅ | ✅ | Đạt |
| Admin contacts | ✅ | ✅ | ✅ | ✅ | Đạt |
| Admin reports | ✅ | ✅ | ✅ | ✅ | Đạt |
| Admin promotions planned | ✅ | ✅ | ✅ | ✅ | Đạt có điều kiện planned |
| Admin landing/settings planned | ✅ | ✅ | ✅ | ✅ | Đạt có điều kiện planned |
| User auth | ✅ | ✅ | ✅ | ✅ | Đạt |
| User home/search | ✅ | ✅ | ✅ | ✅ | Đạt |
| User locations | ✅ | ✅ | ✅ | ✅ | Đạt |
| User tours/booking/payment | ✅ | ✅ | ✅ | ✅ | Đạt |
| User bookings/invoice/passengers/timeline | ✅ | ✅ | ✅ | ✅ | Đạt |
| User profile/favorites | ✅ | ✅ | ✅ | ✅ | Đạt |
| User ratings | ✅ | ✅ | ✅ | ✅ | Đạt |
| User notifications/recommendations | ✅ | ✅ | ✅ | ✅ | Đạt |
| User blog/contact | ✅ | ✅ | ✅ | ✅ | Đạt |
| User cart planned | ✅ | ✅ | ✅ | ✅ | Đạt có điều kiện planned |
| Runtime/system endpoints | ✅ | ✅ | ✅ | ✅ | Đạt |
| Future service extensions | ✅ | ⚠️ External/phase sau | ✅ | ✅ | Đạt có điều kiện planned |

---

## 5. API mồ côi

Kết quả hiện tại:

| API Endpoint | Method | Mục đích API | Đề xuất màn hình sử dụng | Lý do cần thêm màn |
|---|---|---|---|---|
| Không có | Không có | Tất cả API đã có chủ sở hữu trong tài liệu | Không cần thêm màn bắt buộc | `ORPHAN_COUNT=0` |

---

## 6. DB schema review

| Nhóm bảng | Bảng chính | Phục vụ API | Phục vụ màn | Ghi chú |
|---|---|---|---|---|
| Auth/User | `users`, `password_reset_tokens`, `refresh_tokens` | Auth, profile, admin users | Login, register, profile, user admin | Đủ |
| Location | `categories`, `subcategories`, `locations`, `tags`, `amenities`, join tables | Location APIs | Location list/detail/admin | Đủ |
| Tour | `tour_categories`, `tours`, `tour_schedules`, `tour_locations` | Tour APIs | Tour list/detail/admin schedule | Đủ |
| Booking | `bookings`, `booking_items`, `booking_passengers` | Booking APIs | Booking, passengers, invoice | Đủ |
| Payment | `payments`, `payment_status_histories` | Payment/callback/refund | Payment, admin transaction, timeline | Đủ |
| Timeline | `booking_status_histories`, `payment_status_histories` | Timeline planned | User/admin booking detail | Đủ |
| Rating | `ratings`, `rating_images` | Rating APIs | Rating modal/list/lightbox | Đủ |
| Favorite/View/Search | `favorites`, `views`, `search_logs` | Favorite, recommendation, search | Favorites, search, recommendations | Đủ |
| Notification | `notifications` | User/admin notifications | Notification screens | Đủ |
| Blog | `blog_posts`, `blog_categories`, `blog_post_categories` | Blog APIs | Blog public/admin | Đủ |
| Contact | `contacts` | Contact APIs | Contact/admin support | Đủ |
| Promotion planned | `promotions`, `promotion_targets`, `booking_promotions` | Promotions planned | Admin promotions, cart, tour landing | Đủ cho planned |
| Cart planned | `carts`, `cart_items` | Cart planned | User cart | Đủ cho planned |
| CMS/config planned | `landing_pages`, `site_settings` | Landing/settings/config planned | Landing pages, admin settings | Đủ cho planned |
| Runtime | `sessions`, `cache`, `jobs`, `failed_jobs` | Laravel runtime | Không phải màn nghiệp vụ | Đủ |

---

## 7. Đề xuất còn lại

Các đề xuất dưới đây không còn là lỗi tài liệu, mà là khuyến nghị khi triển khai code/migration thật.

| Đề xuất | Lý do | Ưu tiên |
|---|---|---|
| Thêm check constraint cho `favorites`: chỉ một trong `location_id` hoặc `tour_id` có giá trị | Tránh dữ liệu favorite sai đối tượng | Cao |
| Thêm unique index cho favorite theo user + target | Tránh lưu trùng yêu thích | Cao |
| Thêm check constraint cho `ratings`: score 1-5 và chỉ một target location/tour | Đảm bảo dữ liệu đánh giá hợp lệ | Cao |
| Thêm index cho `promotions(code, status, starts_at, ends_at)` | Tối ưu validate mã giảm giá | Trung |
| Chốt scope cart/promotion/landing CMS trước khi code | Đây là planned flow, có thể tăng phạm vi triển khai | Trung |
| Chốt phase sau cho flight/hotel/visa | Không thuộc core tour booking hiện tại | Bình |

---

## 8. Checklist triển khai tiếp theo

| Việc cần làm | Mục tiêu | Ưu tiên |
|---|---|---|
| **Tạo prototype Stitch cho 5 màn HIGH** (login, register, forgot/reset password, blog detail) | Hoàn thiện core auth flow + content page | **Cao** |
| **Tạo prototype Stitch cho 8 màn MEDIUM** (departure select, booking by code/invoice, tours by category, admin reports x3, location categories) | Bổ sung tính năng phụ trợ | **Cao** |
| Tạo page doc cho `Giới thiệu Đà Nẵng` (đã có prototype) | Đồng bộ docs ↔ screen | Trung |
| Chuyển validation trong docs/page thành validation frontend/backend | Đảm bảo code bám tài liệu | Cao |
| Sinh migration từ DBML mới | Đồng bộ database thật với tài liệu | Cao |
| Rà API thực tế trong `danangtrip-api` với `docs/api/api_list.md` | Tránh docs có nhưng route chưa có | Cao |
| Rà frontend/admin gọi đúng endpoint đã chuẩn hóa | Tránh gọi endpoint cũ như `/districts` hoặc `DELETE /user/favorites/{id}` | Cao |
| Tạo prototype/cập nhật screen cho các màn planned nếu triển khai | Đồng bộ tài liệu với UI prototype | Trung |

---

## 9. Kết luận cuối

Bộ tài liệu hiện đã đạt chuẩn ở mức BA/System Architecture:

```text
PAGE_TOTAL=80 (screen spec) + 5 (component spec)
PAGE_PASS=80
NEED_FIX=0
SCREEN_PROTOTYPES=79
SCREEN_MATCHED=58
SCREEN_MISSING_HIGH=5
SCREEN_MISSING_MEDIUM=8
SCREEN_MISSING_LOW=9
API_COUNT=214
USED_API_COUNT=214
ORPHAN_COUNT=0
DB_TABLES=43
MISSING_REF_TABLES=0
```

Không còn mâu thuẫn lớn giữa tài liệu màn hình, API docs và DBML. 58/80 page docs đã có prototype tương ứng. Còn **13 màn ưu tiên cao/trung** cần bổ sung prototype trên Stitch trước khi triển khai (auth flow, blog detail, admin reports, booking utils). Các điểm còn lại là khuyến nghị triển khai thực tế.
