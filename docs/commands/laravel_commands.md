san route:list
php artisan route:list --path=api
php artisan route:list --name=admin
```
T (API Auth)

```bash
php artisan jwt:secret
php artisan jwt:secret --force
```

---

## 20. Tinker (Debug / Test nhanh)

```bash
php artisan tinker
```

```php
App\Models\User::count();
App\Models\Tour::with('tourCategory')->where('status', 'active')->get();
App\Models\Booking::where('booking_status', 'pending')->count();
App\Models\Rating::where('status', 'pending')->count();
App\Models\TourSchedule::where('start_date', '>=', now())->where('status', 'available')->get();
```

---

## 21. Route

```bash
php arti config:cache
php artisan route:cache
php artisan view:cache
php artisan optimize
php artisan config:clear
php artisan route:clear
php artisan cache:clear
php artisan optimize:clear
```

---

## 17. Queue (Xử lý tác vụ nền)

```bash
php artisan queue:work
php artisan queue:work --queue=emails
php artisan queue:work --queue=notifications
php artisan queue:listen
php artisan queue:failed
php artisan queue:retry all
php artisan queue:flush
```

---

## 18. Storage

```bash
php artisan storage:link
```

---

## 19. JWingCancelledEmail
php artisan make:listener SendPaymentSuccessEmail
php artisan make:listener UpdateLocationRatingStats
php artisan make:listener UpdateTourBookingCount
php artisan make:listener SendRatingApprovedNotification
php artisan make:listener SendRatingRejectedNotification
```

---

## 15. Chạy Seeder

```bash
php artisan db:seed
php artisan db:seed --class=UserSeeder
php artisan db:seed --class=TourSeeder
php artisan db:seed --class=LocationSeeder
```

---

## 16. Cache & Optimize

```bash
php artisanp artisan make:policy LocationPolicy --model=Location
php artisan make:policy TourPolicy     --model=Tour
php artisan make:policy BlogPostPolicy --model=BlogPost
```

---

## 14. Tạo Events & Listeners

```bash
# Events
php artisan make:event BookingConfirmed
php artisan make:event BookingCancelled
php artisan make:event PaymentSuccess
php artisan make:event RatingApproved
php artisan make:event RatingRejected

# Listeners
php artisan make:listener SendBookingConfirmedEmail
php artisan make:listener SendBook artisan make:job SendRatingApprovedNotification
php artisan make:job SendRatingRejectedNotification
php artisan make:job UpdateLocationStats
php artisan make:job UpdateTourBookingCount
```

---

## 12. Tạo Middleware

```bash
php artisan make:middleware CheckUserActive
php artisan make:middleware AdminOnly
php artisan make:middleware StaffOrAdmin
```

---

## 13. Tạo Policies (Authorization)

```bash
php artisan make:policy RatingPolicy   --model=Rating
php artisan make:policy BookingPolicy  --model=Booking
ph

## 10. Tạo Factories (Fake data)

```bash
php artisan make:factory UserFactory
php artisan make:factory LocationFactory
php artisan make:factory TourFactory
php artisan make:factory TourScheduleFactory
php artisan make:factory BookingFactory
php artisan make:factory RatingFactory
php artisan make:factory BlogPostFactory
```

---

## 11. Tạo Jobs (Queue)

```bash
php artisan make:job SendBookingConfirmationEmail
php artisan make:job SendBookingCancelledEmail
php artisan make:job SendPaymentSuccessEmail
phpBookingSeeder
php artisan make:seeder RatingSeeder
php artisan make:seeder BlogSeeder
```

---eder TourScheduleSeeder
php artisan make:seeder Seeder
php artisan make:seeder TourSeeder
php artisan make:se make:seeder LocationSeeder
php artisan make:seeder TourCategoryurce BookingItemResource
php artisan make:resource PaymentResource
php artisan make:resource RatingResource
php artisan make:resource NotificationResource
php artisan make:resource BlogPostResource
php artisan make:resource ContactResource
```

---

## 9. Tạo Seeders

```bash
php artisan make:seeder DatabaseSeeder
php artisan make:seeder UserSeeder
php artisan make:seeder CategorySeeder
php artisan make:seeder SubcategorySeeder
php artisan make:seeder TagSeeder
php artisan make:seeder AmenitySeeder
php artisan
```

---

## 8. Tạo Resources (API Response Transform)

```bash
php artisan make:resource UserResource
php artisan make:resource CategoryResource
php artisan make:resource SubcategoryResource
php artisan make:resource LocationResource
php artisan make:resource LocationCollection
php artisan make:resource TourCategoryResource
php artisan make:resource TourResource
php artisan make:resource TourCollection
php artisan make:resource TourScheduleResource
php artisan make:resource BookingResource
php artisan make:resortisan make:request Blog/UpdateBlogPostRequest

# Contact
php artisan make:request Contact/StoreContactRequestuest User/UpdateProfileRequest

# Blog
php artisan make:request Blog/StoreBlogPostRequest
php auest Rating/UpdateRatingRequest
php artisan make:request Rating/RejectRatingRequest

# User
php artisan make:reqst

# Rating
php artisan make:request Rating/StoreRatingRequest
php artisan make:reqtoreTourScheduleRequest
php artisan make:request Tour/UpdateTourScheduleRequest

# Booking
php artisan make:request Booking/StoreBookingRequest
php artisan make:request Booking/UpdateBookingStatusRequest Tour/SteTourRequest
php artisan make:requerRequest
php artisan make:request Tour/Updauest

# Tour
php artisan make:request Tour/StoreToun/UpdateLocationReqn make:request Locatioion/StoreLocationRequest
php artisa# Location
php artisan make:request Locatst

ontroller Api/Admin/PaymentController
php artisan make:controller Api/Admin/RatingController
php artisan make:controller Api/Admin/UserController
php artisan make:controller Api/Admin/BlogController
php artisan make:controller Api/Admin/ReportController
php artisan make:controller Api/Admin/ContactController
```

---

## 7. Tạo Requests (Validation)

```bash
# Auth
php artisan make:request Auth/RegisterRequest
php artisan make:request Auth/LoginRequeller Api/User/BookingController
php artisan make:controller Api/User/NotificationController

# Admin
php artisan make:controller Api/Admin/DashboardController
php artisan make:controller Api/Admin/LocationController
php artisan make:controller Api/Admin/CategoryController
php artisan make:controller Api/Admin/TourController
php artisan make:controller Api/Admin/TourCategoryController
php artisan make:controller Api/Admin/TourScheduleController
php artisan make:controller Api/Admin/BookingController
php artisan make:cblic
php artisan make:controller Api/LocationController
php artisan make:controller Api/CategoryController
php artisan make:controller Api/TourController
php artisan make:controller Api/TourCategoryController
php artisan make:controller Api/RatingController
php artisan make:controller Api/SearchController
php artisan make:controller Api/BlogController

# User (cần đăng nhập)
php artisan make:controller Api/User/ProfileController
php artisan make:controller Api/User/FavoriteController
php artisan make:controake:model Booking
php artisan make:model BookingItem
php artisan make:model Payment

# Tương tác
php artisan make:model Rating
php artisan make:model RatingImage
php artisan make:model Favorite
php artisan make:model View

# Blog
php artisan make:model BlogCategory
php artisan make:model BlogPost

# Tiện ích
php artisan make:model Notification
php artisan make:model SearchLog
php artisan make:model Contact
```

---

## 6. Tạo Controllers (API)

```bash
# Auth
php artisan make:controller Api/AuthController

# Pugrate:rollback --step=3
php artisan migrate:status
```

---

## 5. Tạo Models

```bash
# Người dùng
php artisan make:model User

# Địa điểm
php artisan make:model Category
php artisan make:model Subcategory
php artisan make:model Tag
php artisan make:model Amenity
php artisan make:model Location
php artisan make:model LocationTag
php artisan make:model LocationAmenity

# Tour
php artisan make:model TourCategory
php artisan make:model Tour
php artisan make:model TourSchedule

# Đặt chỗ & Thanh toán
php artisan mNhóm 6: Blog
php artisan make:migration create_blog_categories_table
php artisan make:migration create_blog_posts_table
php artisan make:migration create_blog_post_categories_table

# Nhóm 7: Tiện ích
php artisan make:migration create_notifications_table
php artisan make:migration create_search_logs_table
php artisan make:migration create_contacts_table
```

---

## 4. Chạy Migration

```bash
php artisan migrate
php artisan migrate:fresh
php artisan migrate:fresh --seed
php artisan migrate:rollback
php artisan mitable
php artisan make:migration create_tours_table
php artisan make:migration create_tour_schedules_table

# Nhóm 4: Đặt chỗ & Thanh toán
php artisan make:migration create_bookings_table
php artisan make:migration create_booking_items_table
php artisan make:migration create_payments_table

# Nhóm 5: Tương tác
php artisan make:migration create_ratings_table
php artisan make:migration create_rating_images_table
php artisan make:migration create_favorites_table
php artisan make:migration create_views_table

# Nhóm 1: Người dùng
php artisan make:migration create_users_table

# Nhóm 2: Địa điểm
php artisan make:migration create_categories_table
php artisan make:migration create_subcategories_table
php artisan make:migration create_tags_table
php artisan make:migration create_amenities_table
php artisan make:migration create_locations_table
php artisan make:migration create_location_tags_table
php artisan make:migration create_location_amenities_table

# Nhóm 3: Tour
php artisan make:migration create_tour_categories_omposer require spatie/laravel-query-builder
composer require league/fractal
```

### Development only

```bash
composer require barryvdh/laravel-debugbar --dev
composer require laravel/telescope --dev
composer require fakerphp/faker --dev
```

### Publish config & setup JWT

```bash
php artisan vendor:publish --provider="Tymon\JWTAuth\Providers\LaravelServiceProvider"
php artisan jwt:secret
php artisan telescope:install
php artisan migrate
```

---

## 3. Tạo Migration

> Theo đúng thứ tự phụ thuộc FK

```bash
# omposer require cloudinary-labs/cloudinary-laravel
composer require spatie/laravel-sluggable
ccd danang-trip
```

---

## 2. Cài đặt Packages

### Core / Production

```bash
composer require tymon/jwt-auth
composer require intervention/image
cán mới

```bash
composer create-project laravel/laravel danang-trip
0 · JWT (tymon/jwt-auth)

---

## 1. Tạo dự x · ReactJS · TailwindCSS · MySQL 8.: Laravel 11. Trip

