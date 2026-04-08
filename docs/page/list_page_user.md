# Danh sách màn hình — User (Frontend)

> Base URL: `/`
> File tham chiếu: `docs/api/api_list.md`
> Phân loại dựa trên quyền API: 🌐 Public (chưa đăng nhập) · 🔐 User (đã đăng nhập)

---

## ══════════════════════════════════════
## PHẦN 1 — CHƯA ĐĂNG NHẬP (🌐 Public)
## ══════════════════════════════════════

> Tất cả màn này dùng API � Public — không cần token.
> Người dùng chưa đăng nhập vẫn xem được đầy đủ.

---

### 1. AUTH (Chưa đăng nhập)

| # | Màn hình | Route | API sử dụng |
|---|----------|-------|-------------|
| 1.1 | Đăng nhập | `/login` | `POST /auth/login` |
| 1.2 | Đăng ký | `/register` | `POST /auth/register` |
| 1.3 | Quên mật khẩu | `/forgot-password` | `POST /auth/forgot-password` |
| 1.4 | Đặt lại mật khẩu | `/reset-password` | `POST /auth/reset-password` |

---

### 2. TRANG CHỦ

| # | Màn hình | Route | API sử dụng |
|---|----------|-------|-------------|
| 2.1 | Trang chủ | `/` | `GET /locations/featured` `GET /tours/featured` `GET /tours/hot` `GET /statistics` `GET /blog` `GET /categories` `GET /tour-categories` `GET /weather` `GET /config` |

---

### 3. TÌM KIẾM

| # | Màn hình | Route | API sử dụng |
|---|----------|-------|-------------|
| 3.1 | Trang tìm kiếm | `/search` | `GET /search` `GET /search/suggestions` `GET /search/popular` `GET /search/trending` |

---

### 4. ĐỊA ĐIỂM

| # | Màn hình | Route | API sử dụng |
|---|----------|-------|-------------|
| 4.1 | Danh sách Địa điểm | `/locations` | `GET /locations` `GET /categories` `GET /locations/districts` |
| 4.2 | Chi tiết Địa điểm | `/locations/{slug}` | `GET /locations/{slug}` `GET /locations/{id}/images` `GET /locations/{id}/ratings` `GET /locations/{id}/rating-stats` `GET /locations/{id}/nearby` `POST /locations/{id}/view` |
| 4.3 | Địa điểm theo Danh mục | `/categories/{slug}/locations` | `GET /categories/{slug}/locations` `GET /categories/{id}` |
| 4.4 | Địa điểm lân cận (GPS) | `/nearby` | `GET /locations/nearby?lat=&lng=&radius=` |

---

### 5. TOUR

| # | Màn hình | Route | API sử dụng |
|---|----------|-------|-------------|
| 5.1 | Danh sách Tour | `/tours` | `GET /tours` `GET /tour-categories` |
| 5.2 | Chi tiết Tour | `/tours/{slug}` | `GET /tours/{slug}` `GET /tours/{id}/schedules` `GET /tours/{id}/ratings` `GET /tours/{id}/rating-stats` `POST /tours/{id}/check-availability` |
| 5.3 | Tour theo Danh mục | `/tour-categories/{slug}/tours` | `GET /tour-categories/{slug}/tours` |

---

### 6. BLOG

| # | Màn hình | Route | API sử dụng |
|---|----------|-------|-------------|
| 6.1 | Danh sách Bài viết | `/blog` | `GET /blog` `GET /blog/categories` |
| 6.2 | Chi tiết Bài viết | `/blog/{slug}` | `GET /blog/{slug}` |
| 6.3 | Blog theo Danh mục | `/blog?category_id={id}` | `GET /blog?category_id=` |

---

### 7. LIÊN HỆ

| # | Màn hình | Route | API sử dụng |
|---|----------|-------|-------------|
| 7.1 | Form liên hệ | `/contact` | `POST /contacts` |

---

### Tổng Phần 1

| Nhóm | Số màn |
|------|--------|
| Auth | 4 |
| Trang chủ | 1 |
| Tìm kiếm | 1 |
| Địa điểm | 4 |
| Tour | 3 |
| Blog | 3 |
| Liên hệ | 1 |
| **Tổng** | **17** |

---

## ══════════════════════════════════════
## PHẦN 2 — ĐÃ ĐĂNG NHẬP (🔐 User)
## ══════════════════════════════════════

> Tất cả màn này dùng API 🔐 User — cần JWT token.
> Bao gồm cả các màn ở Phần 1 nhưng có thêm tính năng khi đăng nhập.
> Màn trùng API với Phần 1 vẫn được liệt kê nếu có thêm chức năng.

---

### 1. AUTH (Đã đăng nhập)

| # | Màn hình | Route | API sử dụng |
|---|----------|-------|-------------|
| 1.1 | Xác thực email | `/verify-email` | `POST /auth/verify-email` `POST /auth/resend-verification` |
| 1.2 | Đăng xuất | (action từ header) | `POST /auth/logout` |

---

### 2. TRANG CHỦ (có thêm khi đăng nhập)

| # | Màn hình | Route | API sử dụng |
|---|----------|-------|-------------|
| 2.1 | Trang chủ + Gợi ý cá nhân | `/` | *(Phần 1)* + `GET /recommendations` |

---

### 3. TÌM KIẾM (có thêm khi đăng nhập)

| # | Màn hình | Route | API sử dụng |
|---|----------|-------|-------------|
| 3.1 | Tìm kiếm + Lịch sử | `/search` | *(Phần 1)* + `GET /user/search-history` `DELETE /user/search-history` |

---

### 4. ĐỊA ĐIỂM (có thêm khi đăng nhập)

| # | Màn hình | Route | API sử dụng |
|---|----------|-------|-------------|
| 4.1 | Chi tiết Địa điểm + Yêu thích | `/locations/{slug}` | *(Phần 1)* + `GET /user/favorites/check/{id}` `POST /user/favorites` `DELETE /user/favorites/{id}` |

---

### 5. TOUR (có thêm khi đăng nhập)

| # | Màn hình | Route | API sử dụng |
|---|----------|-------|-------------|
| 5.1 | Đặt Tour | `/tours/{slug}/book` | `POST /bookings/calculate` `POST /bookings` |
| 5.2 | Thanh toán | `/payment` | `POST /payments/create` `GET /payments/status/{transaction_code}` `POST /payments/retry/{booking_code}` |
| 5.3 | Kết quả thanh toán | `/payment/result` | `GET /payments/status/{transaction_code}` |

---

### 6. HỒ SƠ & TÀI KHOẢN

| # | Màn hình | Route | API sử dụng |
|---|----------|-------|-------------|
| 6.1 | Hồ sơ cá nhân | `/profile` | `GET /user/profile` `PUT /user/profile` `POST /user/profile/avatar` |
| 6.2 | Đổi mật khẩu | `/profile/password` | `PUT /user/password` |
| 6.3 | Xóa tài khoản | `/profile/delete` | `DELETE /user/account` |

---

### 7. ĐẶT TOUR & ĐƠN HÀNG

| # | Màn hình | Route | API sử dụng |
|---|----------|-------|-------------|
| 7.1 | Lịch sử đặt tour | `/bookings` | `GET /user/bookings` |
| 7.2 | Chi tiết đơn đặt | `/bookings/{id}` | `GET /user/bookings/{id}` `POST /user/bookings/{id}/cancel` |
| 7.3 | Chi tiết theo mã đơn | `/bookings/code/{booking_code}` | `GET /user/bookings/code/{booking_code}` |
| 7.4 | Hóa đơn PDF | `/bookings/{id}/invoice` | `GET /user/bookings/{id}/invoice` |

---

### 8. YÊU THÍCH

| # | Màn hình | Route | API sử dụng |
|---|----------|-------|-------------|
| 8.1 | Địa điểm yêu thích | `/favorites` | `GET /user/favorites` `DELETE /user/favorites/{location_id}` `POST /user/favorites` |

---

### 9. ĐÁNH GIÁ

| # | Màn hình | Route | API sử dụng |
|---|----------|-------|-------------|
| 9.1 | Đánh giá của tôi | `/profile/ratings` | `GET /user/ratings` |
| 9.2 | Viết đánh giá | (modal trong chi tiết địa điểm/tour) | `GET /ratings/check` `POST /ratings` `POST /upload/images` |
| 9.3 | Sửa đánh giá | (modal inline) | `PUT /ratings/{id}` |
| 9.4 | Xóa đánh giá | (confirm inline) | `DELETE /ratings/{id}` |
| 9.5 | Đánh dấu hữu ích | (button inline) | `POST /ratings/{id}/helpful` |

---

### 10. THÔNG BÁO

| # | Màn hình | Route | API sử dụng |
|---|----------|-------|-------------|
| 10.1 | Danh sách Thông báo | `/notifications` | `GET /user/notifications` `GET /user/notifications/unread-count` `PATCH /user/notifications/{id}/read` `PATCH /user/notifications/read-all` `DELETE /user/notifications/{id}` |

---

### 11. GỢI Ý

| # | Màn hình | Route | API sử dụng |
|---|----------|-------|-------------|
| 11.1 | Gợi ý cho bạn | `/recommendations` | `GET /recommendations` |

---

### Tổng Phần 2

| Nhóm | Số màn |
|------|--------|
| Auth | 2 |
| Trang chủ (mở rộng) | 1 |
| Tìm kiếm (mở rộng) | 1 |
| Địa điểm (mở rộng) | 1 |
| Tour + Thanh toán | 3 |
| Hồ sơ & Tài khoản | 3 |
| Đặt tour & Đơn hàng | 4 |
| Yêu thích | 1 |
| Đánh giá | 5 |
| Thông báo | 1 |
| Gợi ý | 1 |
| **Tổng** | **23** |

---

## Tổng hợp

| Phần | Mô tả | Số màn |
|------|-------|--------|
| Phần 1 | Chưa đăng nhập (🌐 Public) | 17 |
| Phần 2 | Đã đăng nhập (🔐 User) | 23 |
| **Tổng** | | **40** |

> Lưu ý: Một số màn ở Phần 2 là mở rộng của Phần 1 (cùng route, thêm tính năng khi đăng nhập).
> Ví dụ: `/locations/{slug}` — chưa đăng nhập chỉ xem, đã đăng nhập có thêm toggle yêu thích + viết đánh giá.

---

## Ghi chú: Actions inline (không phải trang riêng)

| Action | Vị trí | API | Yêu cầu |
|--------|--------|-----|---------|
| Toggle yêu thích | Card địa điểm | `POST /user/favorites` · `DELETE /user/favorites/{id}` | 🔐 |
| Ghi nhận lượt xem | Chi tiết địa điểm | `POST /locations/{id}/view` | 🌐 |
| Đánh dấu thông báo đã đọc | Dropdown thông báo | `PATCH /user/notifications/{id}/read` | 🔐 |
| Autocomplete search | Search bar | `GET /search/suggestions` | 🌐 |
| Hủy đơn đặt | Chi tiết đơn | `POST /user/bookings/{id}/cancel` | 🔐 |
| Đánh dấu đánh giá hữu ích | Chi tiết địa điểm/tour | `POST /ratings/{id}/helpful` | 🔐 |
| Lịch sử tìm kiếm | Dropdown search | `GET /user/search-history` `DELETE /user/search-history` | 🔐 |
