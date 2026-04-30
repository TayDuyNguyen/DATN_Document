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

### 1.1 Gap thực tế hiện tại (từ bộ SQL đang có)

Đây là các bảng còn thiếu/chưa đủ mạnh so với mục tiêu ~100 rows/bảng:

- **Thiếu hoàn toàn (0 rows):**
  - `refresh_tokens`
  - `job_batches`

- **Rất thiếu (1-10 rows):**
  - `blog_categories` (8), `blog_posts` (5), `blog_post_categories` (7)
  - `tours` (4), `tour_locations` (5), `tour_schedules` (6)
  - `bookings` (4), `booking_items` (4), `payments` (3)
  - `ratings` (5), `rating_images` (3), `favorites` (4), `views` (3), `contacts` (2), `notifications` (2), `search_logs` (5)
  - `sessions` (2), `password_reset_tokens` (1), `jobs` (2), `failed_jobs` (1), `cache` (2), `cache_locks` (1)

- **Thiếu nhiều (11-30 rows):**
  - `categories` (5), `subcategories` (17)
  - `tags` (22), `amenities` (22)
  - `tour_categories` (10)
  - `users` (20)
  - `locations` (7), `location_tags` (7), `location_amenities` (3)

=> Bạn cần thu thập thêm dữ liệu cho **toàn bộ bảng**, ưu tiên theo thứ tự FK ở mục `## 7) Execution order`.

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
Không cần web search cho nhóm bảng kỹ thuật này. Hãy sinh dữ liệu synthetic nhưng hợp lệ tuyệt đối theo schema cho refresh_tokens, sessions, password_reset_tokens.

Yêu cầu:
- ~100 refresh_tokens (hiện đang thiếu).
- ~100 sessions.
- ~100 password_reset_tokens.
- FK/format phải hợp lệ theo schema:
  - sessions: id, user_id(nullable), ip_address(nullable), user_agent(nullable), payload, last_activity
  - password_reset_tokens: email(pk), token, created_at
  - refresh_tokens: id, user_id(FK users), token(unique length 64), expires_at, used_at(nullable), previous_token_id(nullable FK refresh_tokens), created_at, updated_at
 - Xuất SQL theo thứ tự: sessions -> password_reset_tokens -> refresh_tokens. (FILE: `10_system_tables.sql`)
```

### 6.2 jobs + job_batches + failed_jobs + cache + cache_locks

```text
Không cần web search cho nhóm bảng kỹ thuật này. Hãy sinh dữ liệu synthetic nhưng hợp lệ tuyệt đối theo schema cho jobs, job_batches, failed_jobs, cache, cache_locks.

Yêu cầu:
- ~100 jobs.
- ~100 job_batches (hiện đang thiếu).
- ~100 failed_jobs.
- ~100 cache.
- ~100 cache_locks.
- Đảm bảo đúng kiểu dữ liệu và unique key:
  - jobs: id, queue, payload, attempts(unsigned tinyint), reserved_at(nullable int), available_at(int), created_at(int)
  - job_batches: id(pk string), name, total_jobs, pending_jobs, failed_jobs, failed_job_ids, options(nullable), cancelled_at(nullable), created_at, finished_at(nullable)
  - failed_jobs: id, uuid(unique), connection, queue, payload, exception, failed_at
  - cache: key(pk), value, expiration
  - cache_locks: key(pk), owner, expiration
- Xuất SQL theo thứ tự: jobs -> job_batches -> failed_jobs -> cache -> cache_locks. (FILE: `10_system_tables.sql`)
```

## 7) Execution order

1. Master: `categories/subcategories -> tags/amenities -> tour_categories/blog_categories -> users`
2. Reference: `locations/pivots -> tours/pivots/schedules -> blog_posts/pivots`
3. Transaction: `bookings/items/payments -> interactions`
4. System tables.

## 8) Orchestrator prompt (để AI tự thu thập theo vòng lặp)

Copy prompt này cho AI có Web Search để nó tự chạy end-to-end:

```text
Bạn là Data Collection Orchestrator cho DanangTrip.

MỤC TIÊU:
- Tạo dữ liệu SQL seed cho toàn bộ 33 bảng theo schema migration PostgreSQL hiện tại.
- Mỗi bảng đạt khoảng 100 rows.
- Output tách đúng 10 file SQL theo thiết kế seed hiện tại.

NGUYÊN TẮC:
1) Bắt buộc dùng Web Search cho bảng nghiệp vụ/master/reference.
2) Bảng kỹ thuật hệ thống (sessions, refresh_tokens, jobs...) dùng synthetic data hợp lệ schema, không cần Web Search.
3) Không được dùng cột ngoài schema. Nếu không chắc: bỏ cột đó.
4) Luôn duy trì lookup IDs để giữ FK.

LUỒNG THỰC THI BẮT BUỘC:
Step A - Scan schema:
- Đọc migration/DBML, lập TABLE_SCHEMA_MAP (table -> columns, type, nullable, unique, FK, check).

Step B - Generate theo batch:
- Sinh SQL theo đúng thứ tự FK ở mục Execution order.
- Mỗi batch chỉ trả dữ liệu cho đúng file đích.

Step C - Self-validate trước khi trả:
- Kiểm tra nội bộ:
  - FK có tồn tại trong lookup không.
  - Unique key không trùng trong cùng file.
  - CHECK constraints (score 1..5, num_nonnulls..., status enum...) hợp lệ.
  - Date/Timestamp/JSON đúng format.

Step D - Gap-aware refill:
- Nếu bảng nào <100 rows, tự sinh thêm delta rows cho đúng bảng đó.
- Không được sửa/ghi đè dữ liệu đã hợp lệ, chỉ append.

Step E - Output chuẩn:
- Trả duy nhất 3 block:
  - [SOURCE_SUMMARY]
  - [LOOKUP_TABLES]
  - [SQL_OUTPUT]
- Trong [SQL_OUTPUT], mỗi file bắt đầu bằng:
  -- FILE: <filename>.sql

KẾT THÚC:
- Chỉ trả SQL và lookup, không giải thích dài.
```

## 9) Prompt bổ sung cho vòng “kiểm tra sau thu thập”

```text
Bạn là SQL QA Auditor cho seed DanangTrip.

Input:
- 10 file SQL đã thu thập.
- Schema migration/DBML hiện tại.

Nhiệm vụ:
1) Đếm số rows theo từng bảng.
2) Đối chiếu schema: cột thừa/thiếu/sai kiểu.
3) Đối chiếu ràng buộc: FK/UNIQUE/CHECK.
4) Xuất GAP_REPORT:
   - table_name
   - current_rows
   - target_rows(100)
   - missing_rows
   - errors_found
5) Sinh PATCH_SQL chỉ cho phần thiếu/sai (append-only, không drop dữ liệu hợp lệ).

Output:
- [GAP_REPORT]
- [PATCH_SQL]
```

## 10) Prompt bổ sung cho vòng “sửa lỗi migrate/seed fail”

```text
Bạn là Seeder Incident Responder.

Khi nhận log lỗi `php artisan migrate:fresh --seed`:
1) Trích xuất chính xác bảng/cột/constraint gây lỗi.
2) Chỉ ra file SQL nào gây lỗi.
3) Sinh SQL patch tối thiểu để sửa lỗi đó.
4) Không thay đổi phần đã đúng.
5) Trả về:
   - [ROOT_CAUSE]
   - [FIX_SQL]
   - [RETRY_ORDER]
```
