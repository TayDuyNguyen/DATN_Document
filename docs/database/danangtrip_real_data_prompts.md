# DanangTrip - Real Data Collection Prompts (Target: ~100 rows/table)

Schema source: `D:\DATN\danangtrip-api\database`

## 1) Coverage check of current seed

Database của dự án có **tổng 33 bảng** (theo migration/postgres).

Trong thư mục `D:\DATN\DATN_Tài liệu\seeder` hiện bạn có **10 file SQL**, nhưng mỗi file là _gom nhóm nhiều bảng_ (nên “10 file” != “10 bảng”).

Prompt dưới đây nhằm mục tiêu:

1. Sinh dữ liệu đủ cho **toàn bộ 33 bảng** (mỗi bảng ~100 rows).
2. Bắt buộc SQL phải khớp **schema migration hiện tại** (không dùng schema cũ).
3. File `10_system_tables.sql` phải sinh INSERT thật cho các bảng kỹ thuật
   (`sessions`, `password_reset_tokens`, `refresh_tokens`, `jobs`, `job_batches`,
   `failed_jobs`, `cache`, `cache_locks`) thay vì placeholder.

## 2) Global prompt rules (apply to every prompt)

Copy this block into every AI prompt:

```text
Hãy sử dụng công cụ tìm kiếm Google (Web Search) để thu thập dữ liệu thực tế và chính xác nhất cho các bảng được yêu cầu.

BẮT BUỘC:
1) Mục tiêu số lượng: tạo khoảng 100 bản ghi cho MỖI bảng được nêu trong prompt này.
2) Ưu tiên nguồn chính thống (.gov.vn, cổng dữ liệu mở, cổng du lịch chính thức, tài liệu kỹ thuật chính thức). Nếu thiếu thì dùng nguồn uy tín lớn và ghi rõ nguồn.
3) Ánh xạ đúng tên cột, kiểu dữ liệu, độ dài cột, CHECK/UNIQUE/FK theo PostgreSQL schema.
   - Nếu output có cột không tồn tại trong migration/DBML: loại cột đó (không tự ý tạo thêm).
   - DATE columns: dùng dạng `'YYYY-MM-DD'` (không kèm giờ).
   - TIMESTAMP columns: dùng `NOW()` hoặc `'YYYY-MM-DD HH:MM:SS'`.
   - JSON columns: dùng literal JSON nằm trong dấu nháy (ví dụ `'[]'` hoặc `'{"a":1}'`).
4) Giữ lookup ID để đảm bảo FK (ví dụ CATEGORY_LOOKUP, LOCATION_LOOKUP, TOUR_LOOKUP...).
5) Đầu ra bắt buộc là SQL PostgreSQL: INSERT INTO ... VALUES ...;
6) Không trả prose dài; trả theo cấu trúc:
   - [SOURCE_SUMMARY]
   - [LOOKUP_TABLES]
   - [SQL_OUTPUT]
7) Mỗi cụm dữ liệu phải có source_url và retrieved_date.
8) Trong [SQL_OUTPUT], tách theo file và ghi rõ tên file:
   - Dòng đầu mỗi file là comment: `-- FILE: <filename>.sql`
   - Mỗi file chỉ chứa INSERT cho các bảng trong đúng thứ tự xuất SQL của prompt.
```

## 2.1 Prompt dùng để giao việc “thu thập dữ liệu” (cho người/AI)

Copy & gửi nguyên khối dưới đây cho người/AI thu thập:

```text
Bạn là người/AI thu thập dữ liệu để tạo dữ liệu SQL seed cho dự án DanangTrip.

YÊU CẦU CHÍNH:
1) Dự án có tổng 33 bảng; trong thư mục seeder hiện có 10 file, nhưng mỗi file là nhóm nhiều bảng.
2) Output phải là SQL PostgreSQL INSERT, khớp 100% schema migration/DBML hiện tại.
3) Không dùng schema cũ (đặc biệt các cột sai như first_name/last_name, location_ids JSON cũ, departure_date/return_date cũ...).
4) Luôn giữ lookup ID để đảm bảo FK: CATEGORY_LOOKUP, SUBCATEGORY_LOOKUP, TAG_LOOKUP, AMENITY_LOOKUP, TOUR_LOOKUP, TOUR_SCHEDULE_LOOKUP, USER_LOOKUP...

PHÂN CÔNG THU THẬP THEO NHÓM (10 file):
- FILE 01_categories_subcategories.sql: categories (100) + subcategories (100)
- FILE 02_tags_amenities.sql: tags (100) + amenities (100)
- FILE 03_tour_blog_categories.sql: tour_categories (100) + blog_categories (100)
- FILE 04_users.sql: users (100) [anonymized/synthetic hợp lệ, không lấy dữ liệu nhạy cảm]
- FILE 05_locations.sql: locations (100) + location_tags (100) + location_amenities (100)
- FILE 06_tours.sql: tours (~100) + tour_locations (~100) + tour_schedules (~100)
- FILE 07_blog_posts.sql: blog_posts (~100) + blog_post_categories (~100)
- FILE 08_bookings_payments.sql: bookings (~100) + booking_items (~100) + payments (~100)
- FILE 09_ratings_interactions.sql: ratings (~100) + rating_images (~100) + favorites (~100) + views (~100) + search_logs (~100) + contacts (~100) + notifications (~100)
- FILE 10_system_tables.sql: data kỹ thuật cho sessions, password_reset_tokens, refresh_tokens, jobs, job_batches, failed_jobs, cache, cache_locks (có thể synthetic, KHÔNG cần web search)

QUY TẮC OUTPUT BẮT BUỘC:
- Mỗi file: dòng đầu `-- FILE: <filename>.sql`
- Không trả prose dài; trả [SOURCE_SUMMARY], [LOOKUP_TABLES], [SQL_OUTPUT]
- DATE dùng 'YYYY-MM-DD'; TIMESTAMP dùng NOW() hoặc 'YYYY-MM-DD HH:MM:SS'
- JSON dùng literal JSON nằm trong dấu nháy
- Nếu AI/collector không chắc cột nào: bỏ, không đoán.

KẾT THÚC: chỉ trả SQL, không kèm hướng dẫn chạy.
```

## 3) Master data prompts

### 3.1 categories + subcategories (100 each)

```text
Hãy sử dụng công cụ tìm kiếm Google (Web Search) để thu thập dữ liệu thực tế và chính xác nhất cho bảng categories và subcategories của hệ thống du lịch.

Schema cần map:
- categories: id, name, slug, icon, description, image, sort_order, status, created_at, updated_at
- subcategories: id, category_id, name, slug, description, sort_order, status, created_at, updated_at

Yêu cầu thêm:
- Tạo CATEGORY_LOOKUP và SUBCATEGORY_LOOKUP.
- Slug phải unique, lowercase-kebab-case.
- Mục tiêu: ~100 categories và ~100 subcategories.
- Xuất SQL theo thứ tự: categories -> subcategories. (FILE: `01_categories_subcategories.sql`)
```

### 3.2 tags + amenities (100 each)

```text
Hãy sử dụng công cụ tìm kiếm Google (Web Search) để thu thập dữ liệu thực tế và chính xác nhất cho bảng tags và amenities.

Schema:
- tags: id, name, slug, type, created_at, updated_at
- amenities: id, name, icon, category, created_at, updated_at

Yêu cầu:
- ~100 tags và ~100 amenities.
- Tạo TAG_LOOKUP, AMENITY_LOOKUP.
- Đảm bảo unique cho name/slug theo schema.
- Xuất SQL: tags -> amenities. (FILE: `02_tags_amenities.sql`)
```

### 3.3 tour_categories + blog_categories (100 each)

```text
Hãy sử dụng công cụ tìm kiếm Google (Web Search) để thu thập dữ liệu thực tế và chính xác nhất cho bảng tour_categories và blog_categories.

Schema:
- tour_categories: id, name, slug, description, icon, sort_order, status, created_at, updated_at
- blog_categories: id, name, slug, description, created_at, updated_at

Yêu cầu:
- ~100 tour_categories và ~100 blog_categories.
- Tạo TOUR_CATEGORY_LOOKUP và BLOG_CATEGORY_LOOKUP.
- sort_order không trùng.
- Xuất SQL: tour_categories -> blog_categories. (FILE: `03_tour_blog_categories.sql`)
```

### 3.4 users (100)

```text
Hãy sử dụng công cụ tìm kiếm Google (Web Search) để thu thập dữ liệu thực tế và chính xác nhất cho bảng users (dữ liệu tổng hợp/anonymized, không lấy thông tin nhạy cảm của cá nhân thật).

Schema:
- users: id, username, email, password, full_name, avatar, phone, birthdate, gender, city, role, status, email_verified_at, last_login_at, created_at, updated_at

Yêu cầu:
- ~100 users.
- role chỉ dùng user/admin; status theo domain.
- username/email unique.
- Xuất SQL users. (FILE: `04_users.sql`)
```

## 4) Reference data prompts

### 4.1 locations + location_tags + location_amenities (100 each table)

```text
Hãy sử dụng công cụ tìm kiếm Google (Web Search) để thu thập dữ liệu thực tế và chính xác nhất cho bảng locations, location_tags, location_amenities tại thị trường Đà Nẵng/miền Trung.

Schema:
- locations: đầy đủ tất cả cột theo migration (bao gồm lat/lng, opening_hours JSON, price_min/max, status, is_featured, created_by)
- location_tags: location_id, tag_id
- location_amenities: location_id, amenity_id

Yêu cầu:
- ~100 locations.
- ~100 dòng location_tags.
- ~100 dòng location_amenities.
- Dùng CATEGORY_LOOKUP, SUBCATEGORY_LOOKUP, TAG_LOOKUP, AMENITY_LOOKUP, USER_LOOKUP.
- Không trùng cặp FK ở bảng pivot.
- Xuất SQL: locations -> location_tags -> location_amenities. (FILE: `05_locations.sql`)
```

### 4.2 tours + tour_locations + tour_schedules (100 each table)

```text
Hãy sử dụng công cụ tìm kiếm Google (Web Search) để thu thập dữ liệu thực tế và chính xác nhất cho bảng tours, tour_locations, tour_schedules.

Schema:
- tours: đầy đủ cột theo migration
  - status chỉ dùng active|inactive
  - booking_availability chỉ dùng open|sold_out
  - giá: price_adult/child/infant là decimal(12,2), không âm
- tour_locations: tour_id, location_id, created_at
- tour_schedules: tour_id, start_date, end_date, max_people, booked_people,
  - price_adult/child/infant decimal(12,2) (có thể nullable theo migration)
  - status chỉ dùng available|full|cancelled
  - created_at, updated_at

Yêu cầu:
- ~100 tours.
- ~100 tour_locations.
- ~100 tour_schedules.
- booked_people <= max_people, end_date >= start_date.
- unique (tour_id, start_date).
- Tạo TOUR_LOOKUP (tour_id -> id) và TOUR_SCHEDULE_LOOKUP (tour_id+start_date -> tour_schedule_id).
- Xuất SQL: tours -> tour_locations -> tour_schedules. (FILE: `06_tours.sql`)
```

### 4.3 blog_posts + blog_post_categories (100 each table)

```text
Hãy sử dụng công cụ tìm kiếm Google (Web Search) để thu thập dữ liệu thực tế và chính xác nhất cho bảng blog_posts và blog_post_categories.

Schema:
- blog_posts: id, title, slug, excerpt, content, featured_image, author_id, view_count, status, published_at, created_at, updated_at
- blog_post_categories: post_id, blog_category_id

Yêu cầu:
- ~100 blog_posts.
- ~100 blog_post_categories.
- Không copy dài nguyên văn; chỉ tóm tắt/paraphrase nội dung công khai.
- Dùng USER_LOOKUP và BLOG_CATEGORY_LOOKUP.
- Không trùng cặp (post_id, blog_category_id).
- Xuất SQL: blog_posts -> blog_post_categories. (FILE: `07_blog_posts.sql`)
```

## 5) Transaction & interaction prompts

### 5.1 bookings + booking_items + payments (100 each table)

```text
Hãy sử dụng công cụ tìm kiếm Google (Web Search) để thu thập dữ liệu thực tế và chính xác nhất về hành vi đặt tour/thanh toán, sau đó sinh dữ liệu chuẩn cho bookings, booking_items, payments.

Schema:
- bookings:
  - booking_code (unique), user_id (nullable), customer_name/email/phone/address/note
  - total_amount, discount_amount, final_amount, deposit_amount (>=0)
  - payment_method
  - payment_status IN ('pending','success','failed','refunded','unpaid','partially_paid')
  - booking_status IN ('pending','confirmed','completed','cancelled')
  - cancellation_reason (nullable)
  - booked_at, confirmed_at/cancelled_at/completed_at (nullable)
- booking_items:
  - booking_id, tour_id, tour_schedule_id
  - item_type (default 'tour'), item_name
  - travel_date (date) = tour_schedules.start_date
  - quantity_adult/quantity_child/quantity_infant
  - unit_price_adult/child/infant, subtotal
  - status (default 'pending'), created_at/updated_at
- payments:
  - booking_id
  - transaction_code (unique), amount (>=0), payment_method
  - payment_status IN ('pending','success','failed','refunded')
  - payment_gateway (nullable)
  - gateway_response (json, nullable)
  - paid_at, refunded_at, refund_reason (nullable)

Yêu cầu:
- ~100 bookings.
- ~100 booking_items.
- ~100 payments.
- Dùng USER_LOOKUP, TOUR_LOOKUP, TOUR_SCHEDULE_LOOKUP.
- Tổng tiền và trạng thái phải logic.
- Xuất SQL: bookings -> booking_items -> payments. (FILE: `08_bookings_payments.sql`)
```

### 5.2 ratings + rating_images + favorites + views + search_logs + contacts + notifications (100 each table)

```text
Hãy sử dụng công cụ tìm kiếm Google (Web Search) để thu thập dữ liệu thực tế và chính xác nhất về hành vi người dùng du lịch, sau đó sinh dữ liệu chuẩn cho ratings, rating_images, favorites, views, search_logs, contacts, notifications.

Ràng buộc bắt buộc:
- ratings:
  - num_nonnulls(location_id, tour_id, booking_id) = 1 (đúng CHECK ratings_exactly_one_target_chk)
  - score BETWEEN 1 AND 5 (đúng CHECK ratings_score_chk)
  - image_count >= 0 (đúng CHECK ratings_image_count_chk)
  - status IN ('pending','approved','rejected')
- rating_images:
  - chỉ có created_at (không có updated_at)
  - cột image_url (không phải image_path)
- favorites:
  - num_nonnulls(location_id, tour_id) = 1 (đúng favorites_exactly_one_target_chk)
- views:
  - num_nonnulls(location_id, tour_id) = 1
  - bắt buộc session_id (varchar(100))
- search_logs:
  - bắt buộc session_id
- contacts:
  - message (text) bắt buộc
  - reply (text) nullable
- notifications:
  - không có updated_at

Yêu cầu số lượng:
- ~100 bản ghi cho MỖI bảng trong nhóm này.

Dùng lookup: USER_LOOKUP, LOCATION_LOOKUP, TOUR_LOOKUP, BOOKING_LOOKUP, RATING_LOOKUP.
Xuất SQL theo thứ tự:
favorites/views/search_logs/contacts -> ratings -> rating_images -> notifications. (FILE: `09_ratings_interactions.sql`)
```

## 6) System tables prompts (fill missing + reach ~100)

### 6.1 refresh_tokens + sessions + password_reset_tokens

```text
Hãy sử dụng công cụ tìm kiếm Google (Web Search) để thu thập dữ liệu thực tế và chính xác nhất về mẫu vận hành auth/session của Laravel, sau đó sinh dữ liệu cho refresh_tokens, sessions, password_reset_tokens.

Yêu cầu:
- ~100 refresh_tokens (hiện đang thiếu).
- ~100 sessions.
- ~100 password_reset_tokens.
- FK/format phải hợp lệ theo schema.
 - Xuất SQL theo thứ tự: sessions -> password_reset_tokens -> refresh_tokens. (FILE: `10_system_tables.sql`)
```

### 6.2 jobs + job_batches + failed_jobs + cache + cache_locks

```text
Hãy sử dụng công cụ tìm kiếm Google (Web Search) để thu thập dữ liệu thực tế và chính xác nhất về queue/cache patterns trong Laravel/PostgreSQL, sau đó sinh dữ liệu cho jobs, job_batches, failed_jobs, cache, cache_locks.

Yêu cầu:
- ~100 jobs.
- ~100 job_batches (hiện đang thiếu).
- ~100 failed_jobs.
- ~100 cache.
- ~100 cache_locks.
- Đảm bảo đúng kiểu dữ liệu và unique key.
- Xuất SQL theo thứ tự: jobs -> job_batches -> failed_jobs -> cache -> cache_locks. (FILE: `10_system_tables.sql`)
```

## 7) Execution order

1. Master: `categories/subcategories -> tags/amenities -> tour_categories/blog_categories -> users`
2. Reference: `locations/pivots -> tours/pivots/schedules -> blog_posts/pivots`
3. Transaction: `bookings/items/payments -> interactions`
4. System tables.
