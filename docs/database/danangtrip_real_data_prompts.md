# DanangTrip - Real Data Collection Prompts (Target: ~100 rows/table)
Schema source: `D:\DATN\danangtrip-api\database`

## 1) Coverage check of current seed
Current dataset in `D:\DATN\DATN_Tài liệu\seeder` is **NOT enough** for full DB:
- Missing tables: `refresh_tokens`, `job_batches`
- Very low (<10 rows): `tours`, `tour_schedules`, `bookings`, `payments`, `ratings`, `views`, `contacts`, `notifications`, `blog_posts`, `location_amenities`, ...
- Partially filled: `locations` currently only sample rows, not full list

Use prompts below to collect and generate more SQL until each table reaches around 100 rows.

## 2) Global prompt rules (apply to every prompt)
Copy this block into every AI prompt:

```text
Hãy sử dụng công cụ tìm kiếm Google (Web Search) để thu thập dữ liệu thực tế và chính xác nhất cho các bảng được yêu cầu.

BẮT BUỘC:
1) Mục tiêu số lượng: tạo khoảng 100 bản ghi cho MỖI bảng được nêu trong prompt này.
2) Ưu tiên nguồn chính thống (.gov.vn, cổng dữ liệu mở, cổng du lịch chính thức, tài liệu kỹ thuật chính thức). Nếu thiếu thì dùng nguồn uy tín lớn và ghi rõ nguồn.
3) Ánh xạ đúng tên cột, kiểu dữ liệu, độ dài cột, CHECK/UNIQUE/FK theo PostgreSQL schema.
4) Giữ lookup ID để đảm bảo FK (ví dụ CATEGORY_LOOKUP, LOCATION_LOOKUP, TOUR_LOOKUP...).
5) Đầu ra bắt buộc là SQL PostgreSQL: INSERT INTO ... VALUES ...;
6) Không trả prose dài; trả theo cấu trúc:
   - [SOURCE_SUMMARY]
   - [LOOKUP_TABLES]
   - [SQL_OUTPUT]
7) Mỗi cụm dữ liệu phải có source_url và retrieved_date.
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
- Xuất SQL theo thứ tự: categories -> subcategories.
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
- Xuất SQL: tags -> amenities.
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
- Xuất SQL: tour_categories -> blog_categories.
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
- Xuất SQL users.
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
- Xuất SQL: locations -> location_tags -> location_amenities.
```

### 4.2 tours + tour_locations + tour_schedules (100 each table)
```text
Hãy sử dụng công cụ tìm kiếm Google (Web Search) để thu thập dữ liệu thực tế và chính xác nhất cho bảng tours, tour_locations, tour_schedules.

Schema:
- tours: đầy đủ cột theo migration (booking_availability chỉ open/sold_out)
- tour_locations: tour_id, location_id, created_at
- tour_schedules: tour_id, start_date, end_date, max_people, booked_people, price_adult, price_child, price_infant, status, created_at, updated_at

Yêu cầu:
- ~100 tours.
- ~100 tour_locations.
- ~100 tour_schedules.
- schedule.status chỉ dùng available/full/cancelled.
- booked_people <= max_people, end_date >= start_date.
- unique (tour_id, start_date).
- Tạo TOUR_LOOKUP.
- Xuất SQL: tours -> tour_locations -> tour_schedules.
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
- Xuất SQL: blog_posts -> blog_post_categories.
```

## 5) Transaction & interaction prompts

### 5.1 bookings + booking_items + payments (100 each table)
```text
Hãy sử dụng công cụ tìm kiếm Google (Web Search) để thu thập dữ liệu thực tế và chính xác nhất về hành vi đặt tour/thanh toán, sau đó sinh dữ liệu chuẩn cho bookings, booking_items, payments.

Schema:
- bookings: dùng customer_note, discount_amount, final_amount, booked_at; payment_status theo CHECK
- booking_items: bắt buộc item_type, item_name, travel_date, quantity, unit_price, subtotal
- payments: payment_method, payment_status, payment_gateway, gateway_response, paid_at/refunded_at

Yêu cầu:
- ~100 bookings.
- ~100 booking_items.
- ~100 payments.
- Dùng USER_LOOKUP, TOUR_LOOKUP, TOUR_SCHEDULE_LOOKUP.
- Tổng tiền và trạng thái phải logic.
- Xuất SQL: bookings -> booking_items -> payments.
```

### 5.2 ratings + rating_images + favorites + views + search_logs + contacts + notifications (100 each table)
```text
Hãy sử dụng công cụ tìm kiếm Google (Web Search) để thu thập dữ liệu thực tế và chính xác nhất về hành vi người dùng du lịch, sau đó sinh dữ liệu chuẩn cho ratings, rating_images, favorites, views, search_logs, contacts, notifications.

Ràng buộc bắt buộc:
- ratings: num_nonnulls(location_id, tour_id, booking_id)=1; score 1..5; image_count >=0
- rating_images: cột image_url (không phải image_path), chỉ có created_at
- favorites: num_nonnulls(location_id, tour_id)=1
- views: num_nonnulls(location_id, tour_id)=1; bắt buộc session_id
- search_logs: bắt buộc session_id
- contacts: cột reply (không phải notes)
- notifications: không có updated_at

Yêu cầu số lượng:
- ~100 bản ghi cho MỖI bảng trong nhóm này.

Dùng lookup: USER_LOOKUP, LOCATION_LOOKUP, TOUR_LOOKUP, BOOKING_LOOKUP, RATING_LOOKUP.
Xuất SQL theo thứ tự:
favorites/views/search_logs/contacts -> ratings -> rating_images -> notifications.
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
- Xuất SQL theo thứ tự: sessions -> password_reset_tokens -> refresh_tokens.
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
- Xuất SQL theo thứ tự: jobs -> job_batches -> failed_jobs -> cache -> cache_locks.
```

## 7) Execution order
1. Master: `categories/subcategories -> tags/amenities -> tour_categories/blog_categories -> users`
2. Reference: `locations/pivots -> tours/pivots/schedules -> blog_posts/pivots`
3. Transaction: `bookings/items/payments -> interactions`
4. System tables.

