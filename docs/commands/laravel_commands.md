# Laravel Commands — Dự án Đà Nẵng Trip

> Stack: Laravel 10.x · ReactJS · TailwindCSS · MySQL 8.0 · Laravel Sanctum

---

## 1. Tạo dự án mới

```bash
composer create-project laravel/laravel danang-trip   # Tạo project Laravel mới
cd danang-trip                                         # Vào thư mục project
```

---

## 2. Cài đặt Packages

### Core / Production

```bash
composer require laravel/sanctum                       # Auth API bằng token (Sanctum)
composer require intervention/image                    # Xử lý ảnh (resize, crop)
composer require cloudinary-labs/cloudinary-laravel    # Upload ảnh lên Cloudinary
composer require spatie/laravel-sluggable              # Tự động tạo slug
composer require spatie/laravel-query-builder          # Filter/sort API linh hoạt
composer require league/fractal                        # Transform API response
composer require spatie/laravel-permission             # Phân quyền role/permission (admin, user...)
```

### Development only

```bash
composer require barryvdh/laravel-debugbar --dev       # Debug toolbar (chỉ dùng khi dev)
composer require laravel/telescope --dev               # Monitoring requests, queries, jobs
composer require fakerphp/faker --dev                  # Tạo dữ liệu giả cho Seeder/Factory
```

### Publish config & migrate

```bash
php artisan vendor:publish --provider="Laravel\Sanctum\SanctumServiceProvider"       # Publish Sanctum config
php artisan vendor:publish --provider="Spatie\Permission\PermissionServiceProvider"  # Publish spatie/permission config
php artisan migrate                                                                   # Tạo bảng roles, permissions của Spatie
php artisan telescope:install                                                         # Cài Telescope (tạo migration + assets)
php artisan migrate                                                                   # Chạy migration Telescope
```

---

## 3. Tạo Migration

> Theo đúng thứ tự phụ thuộc FK

```bash
php artisan make:migration create_users_table                # Bảng users (đã có sẵn, chỉnh sửa)
php artisan make:migration create_categories_table           # Bảng danh mục chính
php artisan make:migration create_subcategories_table        # Bảng danh mục con
php artisan make:migration create_tags_table                 # Bảng tags
php artisan make:migration create_amenities_table            # Bảng tiện ích
php artisan make:migration create_locations_table            # Bảng địa điểm (TRUNG TÂM)
php artisan make:migration create_location_tags_table        # Bảng trung gian location-tag
php artisan make:migration create_location_amenities_table   # Bảng trung gian location-amenity
php artisan make:migration create_ratings_table              # Bảng đánh giá
php artisan make:migration create_rating_images_table        # Bảng ảnh đánh giá
php artisan make:migration create_favorites_table            # Bảng yêu thích
php artisan make:migration create_views_table                # Bảng lượt xem
php artisan make:migration create_point_transactions_table   # Bảng giao dịch point
php artisan make:migration create_notifications_table        # Bảng thông báo
php artisan make:migration create_search_logs_table          # Bảng lịch sử tìm kiếm
php artisan make:migration create_blog_posts_table           # Bảng bài viết blog
php artisan make:migration create_blog_categories_table      # Bảng danh mục blog
php artisan make:migration create_blog_post_categories_table # Bảng trung gian blog-category
```

---

## 4. Chạy Migration

```bash
php artisan migrate                      # Chạy tất cả migration
php artisan migrate:fresh                # Xóa toàn bộ bảng và chạy lại từ đầu
php artisan migrate:fresh --seed         # Xóa + migrate + seed data
php artisan migrate:rollback             # Rollback migration gần nhất
php artisan migrate:rollback --step=3    # Rollback 3 migration gần nhất
php artisan migrate:status               # Xem trạng thái các migration
```

---

## 5. Tạo Models

```bash
php artisan make:model User              # Model User (đã có sẵn)
php artisan make:model Category          # Model danh mục chính
php artisan make:model Subcategory       # Model danh mục con
php artisan make:model Tag               # Model tag
php artisan make:model Amenity           # Model tiện ích
php artisan make:model Location          # Model địa điểm
php artisan make:model Rating            # Model đánh giá
php artisan make:model RatingImage       # Model ảnh đánh giá
php artisan make:model Favorite          # Model yêu thích
php artisan make:model View              # Model lượt xem
php artisan make:model PointTransaction  # Model giao dịch point
php artisan make:model Notification      # Model thông báo (đã có sẵn)
php artisan make:model SearchLog         # Model lịch sử tìm kiếm
php artisan make:model BlogPost          # Model bài viết blog
php artisan make:model BlogCategory      # Model danh mục blog
```

---

## 6. Tạo Controllers (API)

```bash
# Auth
php artisan make:controller Api/AuthController                # Đăng ký, đăng nhập, đăng xuất

# Public (Guest + User)
php artisan make:controller Api/LocationController            # CRUD + tìm kiếm địa điểm
php artisan make:controller Api/CategoryController            # Danh sách danh mục
php artisan make:controller Api/RatingController              # Tạo/sửa/xóa đánh giá
php artisan make:controller Api/SearchController              # Tìm kiếm + gợi ý
php artisan make:controller Api/BlogController                # Danh sách + chi tiết blog

# User (cần đăng nhập)
php artisan make:controller Api/User/ProfileController        # Quản lý hồ sơ cá nhân
php artisan make:controller Api/User/FavoriteController       # Quản lý yêu thích
php artisan make:controller Api/User/PointController          # Quản lý point
php artisan make:controller Api/User/NotificationController   # Quản lý thông báo

# Admin
php artisan make:controller Api/Admin/DashboardController     # Thống kê dashboard
php artisan make:controller Api/Admin/LocationController      # CRUD địa điểm (admin)
php artisan make:controller Api/Admin/CategoryController      # CRUD danh mục (admin)
php artisan make:controller Api/Admin/RatingController        # Duyệt/từ chối đánh giá
php artisan make:controller Api/Admin/UserController          # Quản lý người dùng
php artisan make:controller Api/Admin/BlogController          # CRUD bài viết blog
php artisan make:controller Api/Admin/ReportController        # Báo cáo thống kê
php artisan make:controller Api/Admin/SettingController       # Cấu hình hệ thống
```

---

## 7. Tạo Requests (Validation)

```bash
php artisan make:request Auth/RegisterRequest                 # Validate đăng ký
php artisan make:request Auth/LoginRequest                    # Validate đăng nhập
php artisan make:request Location/StoreLocationRequest        # Validate tạo địa điểm
php artisan make:request Location/UpdateLocationRequest       # Validate sửa địa điểm
php artisan make:request Rating/StoreRatingRequest            # Validate tạo đánh giá
php artisan make:request Rating/UpdateRatingRequest           # Validate sửa đánh giá
php artisan make:request Rating/RejectRatingRequest           # Validate từ chối đánh giá
php artisan make:request User/UpdateProfileRequest            # Validate cập nhật profile
php artisan make:request Point/PurchasePointRequest           # Validate nạp point
php artisan make:request Blog/StoreBlogPostRequest            # Validate tạo bài blog
```

---

## 8. Tạo Resources (API Response Transform)

```bash
php artisan make:resource UserResource               # Transform dữ liệu user
php artisan make:resource LocationResource           # Transform dữ liệu địa điểm
php artisan make:resource LocationCollection         # Transform danh sách địa điểm
php artisan make:resource RatingResource             # Transform dữ liệu đánh giá
php artisan make:resource CategoryResource           # Transform dữ liệu danh mục
php artisan make:resource PointTransactionResource   # Transform giao dịch point
php artisan make:resource NotificationResource       # Transform thông báo
php artisan make:resource BlogPostResource           # Transform bài viết blog
```

---

## 9. Tạo Seeders

```bash
php artisan make:seeder DatabaseSeeder    # Seeder gốc (đã có, chỉnh sửa)
php artisan make:seeder CategorySeeder    # Seed 3 danh mục chính
php artisan make:seeder SubcategorySeeder # Seed danh mục con
php artisan make:seeder TagSeeder         # Seed tags (wifi, view đẹp...)
php artisan make:seeder AmenitySeeder     # Seed tiện ích
php artisan make:seeder UserSeeder        # Seed users + 1 admin
php artisan make:seeder LocationSeeder    # Seed 100-150 địa điểm
php artisan make:seeder RatingSeeder      # Seed đánh giá giả lập
php artisan make:seeder BlogSeeder        # Seed bài viết blog
```

---

## 10. Tạo Factories (Fake data)

```bash
php artisan make:factory UserFactory       # Factory tạo user giả
php artisan make:factory LocationFactory   # Factory tạo địa điểm giả
php artisan make:factory RatingFactory     # Factory tạo đánh giá giả
php artisan make:factory BlogPostFactory   # Factory tạo bài blog giả
```

---

## 11. Tạo Jobs (Queue)

```bash
php artisan make:job SendRatingApprovedNotification   # Job gửi thông báo duyệt bài
php artisan make:job SendRatingRejectedNotification   # Job gửi thông báo từ chối bài
php artisan make:job UpdateLocationStats              # Job cập nhật thống kê địa điểm
```

---

## 12. Tạo Middleware

```bash
php artisan make:middleware CheckUserActive   # Kiểm tra user không bị banned
php artisan make:middleware AdminOnly         # Chỉ cho phép admin truy cập
```

---

## 13. Tạo Policies (Authorization)

```bash
php artisan make:policy RatingPolicy --model=Rating       # Quyền sửa/xóa đánh giá
php artisan make:policy LocationPolicy --model=Location   # Quyền quản lý địa điểm
php artisan make:policy BlogPostPolicy --model=BlogPost   # Quyền quản lý bài blog
```

---

## 14. Tạo Events & Listeners

```bash
php artisan make:event RatingApproved                   # Event khi duyệt đánh giá
php artisan make:event RatingRejected                   # Event khi từ chối đánh giá
php artisan make:listener SendApprovalNotification      # Listener gửi thông báo duyệt
php artisan make:listener SendRejectionNotification     # Listener gửi thông báo từ chối
php artisan make:listener DeductUserPoints              # Listener trừ point khi duyệt
```

---

## 15. Chạy Seeder

```bash
php artisan db:seed                              # Chạy tất cả seeders
php artisan db:seed --class=CategorySeeder       # Chạy 1 seeder cụ thể
php artisan db:seed --class=LocationSeeder       # Chạy seeder địa điểm
```

---

## 16. Cache & Optimize

```bash
php artisan config:cache      # Cache file config
php artisan route:cache       # Cache routes (tăng tốc)
php artisan view:cache        # Cache blade views
php artisan optimize          # Tối ưu toàn bộ
php artisan config:clear      # Xóa cache config
php artisan route:clear       # Xóa cache routes
php artisan cache:clear       # Xóa application cache
php artisan optimize:clear    # Xóa tất cả cache
```

---

## 17. Queue (Xử lý tác vụ nền)

```bash
php artisan queue:work                          # Chạy queue worker
php artisan queue:work --queue=notifications    # Chạy queue cụ thể
php artisan queue:listen                        # Lắng nghe queue (dev)
php artisan queue:failed                        # Xem các job thất bại
php artisan queue:retry all                     # Retry tất cả job thất bại
php artisan queue:flush                         # Xóa tất cả job thất bại
```

---

## 18. Storage

```bash
php artisan storage:link   # Tạo symlink public/storage → storage/app/public
```

---

## 19. Sanctum (API Auth)

```bash
php artisan sanctum:prune-expired --hours=24   # Xóa token hết hạn sau 24h
```

---

## 20. Tinker (Debug / Test nhanh)

```bash
php artisan tinker
```

```php
// Trong tinker:
App\Models\User::count();                                  // Đếm số user
App\Models\Location::with('category')->first();            // Xem địa điểm đầu tiên
App\Models\Rating::where('status', 'pending')->count();    // Đếm bài chờ duyệt
```

---

## 21. Route

```bash
php artisan route:list              # Xem tất cả routes
php artisan route:list --path=api   # Xem routes API
php artisan route:list --name=admin # Lọc routes theo tên
```
