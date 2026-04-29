# DanangTrip - Prompt Kịch Bản Thu Thập Dữ Liệu Thực Tế (Google/Web Search)
Nguồn schema: `D:\DATN\danangtrip-api\database`  
Mục tiêu: tạo prompt để gửi cho AI có Internet, tự tra cứu dữ liệu thật và xuất `INSERT INTO` PostgreSQL.

## Quy ước dùng chung
- Chạy theo thứ tự từ trên xuống để không vỡ khóa ngoại.
- Mọi prompt đều yêu cầu:
  - Tìm dữ liệu thật qua Google/Web Search.
  - Ưu tiên nguồn chính thống (`.gov.vn`, cổng dữ liệu mở, cơ quan quản lý, wiki chính thống).
  - Map đúng cột/kiểu dữ liệu/độ dài/ràng buộc.
  - Xuất SQL `INSERT INTO`.
  - Kèm bảng tra cứu ID (`lookup`) để giữ toàn vẹn FK.

---

## NHÓM A - MASTER DATA (LẤY TRƯỚC)

### 1) Bảng `categories`, `subcategories`
**Dữ liệu cần tìm:** Danh mục điểm đến du lịch, nhóm chính/phụ phù hợp Đà Nẵng - miền Trung.

```text
Hãy sử dụng công cụ tìm kiếm Google (Web Search) để thu thập dữ liệu thực tế và chính xác nhất cho bảng categories và subcategories của hệ thống du lịch.

Yêu cầu bắt buộc:
1) Ưu tiên nguồn chính thống: cổng thông tin du lịch địa phương, trang .gov.vn, cục du lịch, wiki có kiểm chứng.
2) Sau khi thu thập dữ liệu thô, tự động ánh xạ về đúng cột:
   - categories: id, name(<=50), slug(<=60, unique), icon(<=50), description, image(<=255), sort_order, status(active/inactive), created_at, updated_at
   - subcategories: id, category_id(FK->categories.id), name(<=50), slug(<=60, unique), description, sort_order, status(active/inactive), created_at, updated_at
3) Bắt buộc tạo bảng tra cứu ID:
   - CATEGORY_LOOKUP(name -> id)
   - SUBCATEGORY_LOOKUP(name -> id, category_id)
4) Slug phải lowercase-kebab-case, không dấu, unique.
5) Đầu ra bắt buộc:
   - Khối SQL PostgreSQL INSERT INTO cho categories trước, subcategories sau.
   - Có chú thích nguồn cho từng nhóm dữ liệu: source_url + retrieved_date.
```

### 2) Bảng `tags`, `amenities`
**Dữ liệu cần tìm:** Từ khóa tiện ích/đặc trưng địa điểm du lịch và danh sách tiện nghi thực tế.

```text
Hãy sử dụng công cụ tìm kiếm Google (Web Search) để thu thập dữ liệu thực tế và chính xác nhất cho bảng tags và amenities trong hệ thống du lịch.

Yêu cầu bắt buộc:
1) Ưu tiên nguồn chính thống hoặc nguồn lớn có uy tín (cổng du lịch, booking platform lớn, wiki có kiểm chứng).
2) Map dữ liệu đúng schema:
   - tags: id, name(unique, <=50), slug(unique, <=60), type(<=30), created_at, updated_at
   - amenities: id, name(unique, <=50), icon(<=50), category(<=30), created_at, updated_at
3) Chuẩn hóa taxonomy:
   - tags.type ví dụ: cuisine, vibe, audience, activity, landscape...
   - amenities.category ví dụ: connectivity, parking, comfort, payment...
4) Tạo bảng tra cứu ID:
   - TAG_LOOKUP(name->id)
   - AMENITY_LOOKUP(name->id)
5) Đầu ra bắt buộc là SQL INSERT INTO PostgreSQL, có source_url + retrieved_date.
```

### 3) Bảng `tour_categories`, `blog_categories`
**Dữ liệu cần tìm:** Danh mục tour phổ biến và danh mục bài viết du lịch.

```text
Hãy sử dụng công cụ tìm kiếm Google (Web Search) để thu thập dữ liệu thực tế và chính xác nhất cho bảng tour_categories và blog_categories.

Yêu cầu bắt buộc:
1) Ưu tiên nguồn chính thống ngành du lịch, báo/chuyên trang du lịch uy tín, wiki có kiểm chứng.
2) Map đúng cột:
   - tour_categories: id, name(unique<=50), slug(unique<=60), description, icon(<=50), sort_order(unique), status(active/inactive), created_at, updated_at
   - blog_categories: id, name(unique<=50), slug(unique<=60), description, created_at, updated_at
3) Tạo TOUR_CATEGORY_LOOKUP và BLOG_CATEGORY_LOOKUP (name->id).
4) Đầu ra bắt buộc SQL INSERT INTO PostgreSQL, có nguồn.
```

### 4) Bảng `users` (seed thực tế an toàn)
**Dữ liệu cần tìm:** Danh sách tên người Việt phổ biến, nhà mạng email domain phổ biến, mã vùng điện thoại VN.

```text
Hãy sử dụng công cụ tìm kiếm Google (Web Search) để thu thập dữ liệu thực tế và chính xác nhất cho bảng users, nhưng không lấy dữ liệu cá nhân nhạy cảm của người thật.

Yêu cầu bắt buộc:
1) Tra cứu dữ liệu thống kê công khai (họ tên phổ biến, thành phố, định dạng số điện thoại VN) từ nguồn uy tín.
2) Tạo dữ liệu tổng hợp/anonymized và map đúng cột:
   id, username(unique<=50), email(unique<=100), password, full_name<=100, avatar<=255, phone<=20, birthdate, gender<=20, city<=100, role<=20, status<=20, email_verified_at, last_login_at, created_at, updated_at
3) role chỉ gồm user/admin; status theo domain hệ thống.
4) Đầu ra bắt buộc SQL INSERT INTO PostgreSQL.
5) Kèm source_url + retrieved_date cho các dữ liệu thống kê đã dùng.
```

---

## NHÓM B - REFERENCE DATA (PHỤ THUỘC MASTER)

### 5) Bảng `locations`, `location_tags`, `location_amenities`
**Dữ liệu cần tìm:** Địa điểm du lịch thực tế tại Đà Nẵng (tên, địa chỉ, tọa độ, giờ mở cửa, giá tham khảo).

```text
Hãy sử dụng công cụ tìm kiếm Google (Web Search) để thu thập dữ liệu thực tế và chính xác nhất cho bảng locations, location_tags, location_amenities.

Yêu cầu bắt buộc:
1) Ưu tiên nguồn chính thống (.gov.vn, cổng du lịch chính thức), sau đó đến nguồn uy tín lớn (Google Maps, wiki, OTA lớn) để đối chiếu chéo.
2) Thu thập ít nhất 200 địa điểm thật tại Đà Nẵng, có kiểm tra trùng.
3) Map đúng cột locations:
   id, name<=200, slug(unique<=220), category_id(FK), subcategory_id(FK nullable), description, short_description<=500, address<=255, district<=50, ward<=50,
   latitude(decimal 10,8), longitude(decimal 11,8), phone<=20, email<=100, website<=255, opening_hours(json),
   price_min(decimal12,2>=0), price_max(decimal12,2>=0 và >=price_min), price_level, avg_rating(0..5), review_count, view_count, favorite_count,
   thumbnail<=255, images(json), video_url<=255, status(active/inactive), is_featured, created_by(FK users), created_at, updated_at
4) Với bảng liên kết:
   - location_tags: map bằng TAG_LOOKUP, không trùng (location_id, tag_id)
   - location_amenities: map bằng AMENITY_LOOKUP, không trùng (location_id, amenity_id)
5) Bắt buộc có LOCATION_LOOKUP(name/slug -> id) để dùng cho các bảng sau.
6) Đầu ra: SQL INSERT INTO PostgreSQL theo thứ tự locations -> location_tags -> location_amenities.
7) Kèm source_url và retrieved_date cho từng location hoặc cụm location.
```

### 6) Bảng `tours`, `tour_locations`, `tour_schedules`
**Dữ liệu cần tìm:** Tour thực tế tại Đà Nẵng (giá, thời lượng, lịch trình, lịch khởi hành).

```text
Hãy sử dụng công cụ tìm kiếm Google (Web Search) để thu thập dữ liệu thực tế và chính xác nhất cho bảng tours, tour_locations, tour_schedules.

Yêu cầu bắt buộc:
1) Ưu tiên nguồn chính thống/công ty lữ hành uy tín/cổng du lịch có thông tin đầy đủ.
2) Thu thập tối thiểu 120 tour thật, map đúng cột tours:
   id, name<=200, slug(unique<=220), tour_category_id(FK), description, short_desc<=500, itinerary(json), inclusions(json), exclusions(json),
   price_adult/child/infant(decimal12,2 >=0), discount_percent(0..100), duration<=50, start_time<=50, meeting_point<=255,
   max_people>=0, min_people>=1 và min_people<=max_people, available_from, available_to,
   thumbnail<=255, images(json), video_url<=255, status, booking_availability(open/sold_out), is_featured, is_hot, view_count, booking_count, rating_count, rating_avg, created_by(FK), created_at, updated_at
3) tour_locations:
   - Dùng LOCATION_LOOKUP để map FK.
   - Không trùng (tour_id, location_id).
4) tour_schedules:
   - unique (tour_id, start_date)
   - end_date >= start_date
   - booked_people <= max_people
   - price override nullable nhưng nếu có phải >=0
5) Bắt buộc tạo TOUR_LOOKUP(name/slug -> id).
6) Đầu ra SQL INSERT INTO PostgreSQL theo thứ tự tours -> tour_locations -> tour_schedules.
7) Kèm source_url + retrieved_date.
```

### 7) Bảng `blog_posts`, `blog_post_categories`
**Dữ liệu cần tìm:** Bài viết du lịch thực tế và phân loại chủ đề.

```text
Hãy sử dụng công cụ tìm kiếm Google (Web Search) để thu thập dữ liệu thực tế và chính xác nhất cho bảng blog_posts và blog_post_categories.

Yêu cầu bắt buộc:
1) Ưu tiên nguồn chính thống, blog du lịch uy tín, báo điện tử uy tín.
2) Chỉ lấy dữ liệu công khai; tóm tắt/paraphrase, không sao chép nguyên văn dài.
3) Map đúng cột blog_posts:
   id, title<=255, slug(unique<=280), excerpt<=500, content(longtext), featured_image<=255, author_id(FK users), view_count, status(draft/published/archived), published_at, created_at, updated_at
4) blog_post_categories:
   - map qua BLOG_CATEGORY_LOOKUP
   - không trùng (post_id, blog_category_id)
5) Đầu ra SQL INSERT INTO PostgreSQL theo thứ tự blog_posts -> blog_post_categories, có source_url + retrieved_date.
```

---

## NHÓM C - TRANSACTION DATA (SINH TỪ DỮ LIỆU THẬT ĐÃ THU THẬP)

### 8) Bảng `bookings`, `booking_items`, `payments`
**Dữ liệu cần tìm:** Không có public raw transaction; cần tạo giao dịch mô phỏng dựa trên dữ liệu thật đã thu thập từ tours/schedules.

```text
Hãy sử dụng công cụ tìm kiếm Google (Web Search) để thu thập dữ liệu thực tế và chính xác nhất cho hành vi đặt tour/thanh toán (xu hướng đặt cọc, thanh toán theo đợt, tỷ lệ hủy), sau đó tạo dữ liệu giao dịch chuẩn cho bookings, booking_items, payments.

Yêu cầu bắt buộc:
1) Ưu tiên nguồn chính thống hoặc báo cáo uy tín (cơ quan du lịch, OTA, báo cáo thị trường).
2) Dựa trên TOUR_LOOKUP + tour_schedules + users để sinh dữ liệu transaction có phân phối thực tế.
3) Map đúng schema:
   - bookings: booking_code unique<=20, user_id nullable FK, customer_name/email/phone/address/note, amounts(decimal12,2, >=0), payment_method<=30, payment_status, booking_status, timestamps...
   - booking_items: FK booking_id/tour_id/tour_schedule_id, quantity_*, unit_price_*, subtotal, travel_date, status
   - payments: FK booking_id, transaction_code unique<=100, amount>=0, payment_status(pending/success/failed/refunded), gateway, paid_at/refunded_at, gateway_response(json)
4) Giữ toàn vẹn:
   - booking_items phải khớp tour và schedule có thật
   - subtotal và tổng tiền booking hợp logic
   - payment dòng tiền khớp trạng thái booking ở mức hợp lý nghiệp vụ
5) Bắt buộc xuất SQL INSERT INTO PostgreSQL theo thứ tự bookings -> booking_items -> payments.
6) Kèm source_url + retrieved_date cho dữ liệu xu hướng đã dùng.
```

### 9) Bảng `ratings`, `rating_images`, `notifications`, `favorites`, `views`, `search_logs`, `contacts`
**Dữ liệu cần tìm:** Hành vi người dùng thực tế (review pattern, thời lượng xem, truy vấn tìm kiếm, form liên hệ).

```text
Hãy sử dụng công cụ tìm kiếm Google (Web Search) để thu thập dữ liệu thực tế và chính xác nhất cho hành vi người dùng du lịch, sau đó tạo dữ liệu chuẩn cho ratings, rating_images, notifications, favorites, views, search_logs, contacts.

Yêu cầu bắt buộc:
1) Ưu tiên nguồn uy tín về hành vi người dùng (báo cáo OTA, UX report, phân tích thị trường) và nguồn chính thống khi có.
2) Map đúng schema và ràng buộc:
   - ratings: num_nonnulls(location_id,tour_id,booking_id)=1; score 1..5; image_count>=0; unique partial theo user-target; status + approved/rejected fields hợp lý
   - rating_images: FK rating_id, sort_order
   - notifications: FK user_id, type/title/content/data/is_read/read_at
   - favorites: num_nonnulls(location_id,tour_id)=1; unique partial
   - views: num_nonnulls(location_id,tour_id)=1; session_id; time_spent hợp lý
   - search_logs: query<=255, results_count, filters(json)
   - contacts: thông tin liên hệ hợp lệ, trạng thái xử lý
3) Bắt buộc dùng bảng tra cứu ID:
   USER_LOOKUP, LOCATION_LOOKUP, TOUR_LOOKUP, BOOKING_LOOKUP, RATING_LOOKUP.
4) Đầu ra bắt buộc SQL INSERT INTO PostgreSQL theo thứ tự:
   favorites/views/search_logs/contacts -> ratings -> rating_images -> notifications.
5) Kèm source_url + retrieved_date cho bộ dữ liệu hành vi tham chiếu.
```

---

## NHÓM D - SYSTEM TABLES (TÙY CHỌN)

### 10) `refresh_tokens`, `sessions`, `password_reset_tokens`, `jobs`, `job_batches`, `failed_jobs`, `cache`, `cache_locks`
**Dữ liệu cần tìm:** Chủ yếu kỹ thuật vận hành, không ưu tiên thu thập bên ngoài.

```text
Hãy sử dụng công cụ tìm kiếm Google (Web Search) để thu thập dữ liệu thực tế và chính xác nhất cho mẫu vận hành hệ thống Laravel/PostgreSQL (session lifecycle, token rotation, queue failure patterns), sau đó tạo dữ liệu seed kỹ thuật cho các bảng hệ thống.

Yêu cầu bắt buộc:
1) Dùng nguồn tài liệu chính thức Laravel/PostgreSQL và nguồn kỹ thuật uy tín.
2) Map đúng schema từng bảng hệ thống, đảm bảo không vi phạm unique/FK.
3) refresh_tokens phải có chuỗi previous_token_id hợp lệ.
4) Đầu ra SQL INSERT INTO PostgreSQL, có source_url + retrieved_date.
```

---

## Checklist chạy thực tế
1. Chạy prompt Nhóm A trước, lưu lại toàn bộ LOOKUP ID.
2. Chạy Nhóm B bằng LOOKUP từ Nhóm A.
3. Chạy Nhóm C bằng LOOKUP từ A+B.
4. Kiểm tra lại bằng:
   - unique constraint
   - foreign key integrity
   - check constraint
5. Mới thực thi `INSERT` vào PostgreSQL.
