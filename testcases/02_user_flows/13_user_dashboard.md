# Dashboard Thành viên (User Dashboard) - Test Cases

## 1. Tổng quan màn hình

* Đường dẫn route: 
  - `/[locale]/dashboard` (Trang chủ dashboard)
  - `/[locale]/dashboard/users` (Trang danh sách user - placeholder)
  - `/[locale]/dashboard/settings` (Trang thiết lập - placeholder)
* File source chính: 
  - `D:\DATN\danangtrip-web\src\app\[locale]\(main)\(protected)\dashboard\layout.tsx`
  - `D:\DATN\danangtrip-web\src\app\[locale]\(main)\(protected)\dashboard\page.tsx`
  - `D:\DATN\danangtrip-web\src\app\[locale]\(main)\(protected)\dashboard\users\page.tsx`
  - `D:\DATN\danangtrip-web\src\app\[locale]\(main)\(protected)\dashboard\settings\page.tsx`
* Component liên quan: `Sidebar`, `Navbar`, Solar icons (`IoShieldCheckmarkOutline`, `IoFingerPrintOutline`, `IoRocketOutline`)
* API/service sử dụng: Phiên đăng nhập (`useAuth` hook, `useAuthStore` để lấy thông tin user đăng nhập).
* Quyền truy cập: Chỉ dành cho thành viên đã đăng nhập (role: user, tour_guide, manager, admin,...). Khách vãng lai bị chặn.
* Mục đích màn hình: Hiển thị thông tin tổng quan của tài khoản thành viên, cung cấp menu điều hướng quản trị cá nhân (Sidebar/Navbar).

## 2. Điều kiện tiền đề

* Tài khoản cần dùng: 
  - Một tài khoản thường đã đăng ký và kích hoạt (role `user`).
  - Một tài khoản chưa đăng nhập để test redirect.
* Trạng thái hệ thống: API Web hoạt động; cookie/localStorage lưu token hợp lệ.

## 3. Danh sách chức năng chính

* **Route Guard (Chặn truy cập trái phép)**:
  - Khi chưa đăng nhập (`isAuthenticated = false`), tự động lấy pathname và searchParams hiện tại, chuyển hướng sang `/login?callbackUrl=...`.
  - Trong lúc đang check auth (`isLoading = true`), hiển thị bộ khung xương (skeleton screen) hoạt ảnh pulse.
* **Layout chung (Dashboard Layout)**:
  - Hiển thị Navbar trên cùng và Sidebar bên trái (trên desktop).
  - Main section hiển thị content động của các trang con.
* **Trang chủ Dashboard (`/dashboard`)**:
  - Hiển thị lời chào: "Xin chào, {user.name}!".
  - Hiển thị mô tả cá nhân của dashboard thành viên.
  - Hộp thông báo "Tính năng đang cập nhật" đi kèm icon IoRocketOutline nhấp nháy (pulse).
  - Thẻ thông tin Trạng thái tài khoản: Hiển thị "Đang hoạt động" (Active).
  - Thẻ thông tin Loại tài khoản: Hiển thị tên role của user (in hoa chữ cái đầu hoặc Việt hóa theo i18n).
* **Trang con Users (`/dashboard/users`)**:
  - Hiển thị tiêu đề và nội dung mô tả lấy từ bản dịch `dashboardAdmin` namespace.
* **Trang con Settings (`/dashboard/settings`)**:
  - Hiển thị tiêu đề và nội dung thiết lập từ bản dịch `dashboardAdmin` namespace.

## 4. Test cases chi tiết

| ID | Nhóm chức năng | Test case | Tiền điều kiện | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Mức độ ưu tiên | Loại test |
| -- | -------------- | --------- | -------------- | -------------- | ------------ | ---------------- | -------------- | --------- |
| USR_DB_001 | Route Guard | Chưa đăng nhập cố tình vào dashboard | Chưa đăng nhập | 1. Mở thẳng link `/vi/dashboard`.<br>2. Quan sát URL và UI. | Guest | - Trong lúc check auth: Hiện skeleton loading.<br>- Sau đó: Chuyển hướng sang `/vi/login?callbackUrl=%2Fvi%2Fdashboard` kèm thông báo cần đăng nhập. | Critical | Security |
| USR_DB_002 | Route Guard | Chưa đăng nhập cố tình vào trang con dashboard | Chưa đăng nhập | 1. Mở thẳng link `/vi/dashboard/settings`.<br>2. Quan sát URL. | Guest | Chuyển hướng sang `/vi/login?callbackUrl=%2Fvi%2Fdashboard%2Fsettings`. | Critical | Security |
| USR_DB_003 | Auth Check UI | Giao diện đang check auth | Client đang tải thông tin session | 1. Mở trang dashboard với mạng giả lập cực chậm.<br>2. Quan sát màn hình. | Slow 3G | Hiển thị bộ xương skeleton pulse màu xám (1 sidebar bên trái có 3 dòng, 1 navbar trên cùng, 1 box content to ở giữa). Không hiển thị trang trắng hay bị nháy layout giật cục. | Medium | UI |
| USR_DB_004 | Layout | Đã đăng nhập vào dashboard thành công | Đã đăng nhập tài khoản user | 1. Đăng nhập.<br>2. Vào `/vi/dashboard`.<br>3. Kiểm tra sự hiện diện của Sidebar và Navbar. | User: `Nguyen Van A` | - Hiển thị thanh menu Sidebar bên trái.<br>- Hiển thị thanh Navbar trên đầu có thông tin user.<br>- Box nội dung chính hiển thị đúng các card thông tin. | Critical | Functional |
| USR_DB_005 | Dashboard Home | Hiển thị thông tin cá nhân trên trang chủ | Đã đăng nhập, vào trang `/dashboard` | 1. Vào `/vi/dashboard`.<br>2. So sánh thông tin với profile thật. | User `Nguyen Van A` / Role: `user` | - Hiển thị "Xin chào, Nguyen Van A!" (hoặc tương tự theo i18n).<br>- Trạng thái tài khoản hiển thị "Đang hoạt động" kèm icon khiên màu xanh lá cây.<br>- Loại tài khoản hiển thị "user". | High | Functional |
| USR_DB_006 | i18n | Đa ngôn ngữ trang chủ dashboard | Đang ở trang chủ dashboard | 1. Chuyển đổi ngôn ngữ sang Tiếng Anh `/en/dashboard`.<br>2. Quan sát văn bản. | Locale: `en` | Toàn bộ text chào mừng, mô tả, trạng thái hoạt động chuyển sang Tiếng Anh (ví dụ: "Active", "Member", "Welcome"). | High | Regression |
| USR_DB_007 | Users Page | Truy cập trang con `/dashboard/users` | Đã đăng nhập, ở dashboard | 1. Click vào mục Thành viên trên Sidebar hoặc gõ URL `/vi/dashboard/users`. | | Hiển thị trang quản lý thành viên với tiêu đề và mô tả placeholder (từ file dịch `dashboardAdmin` namespace). Không bị crash layout. | Medium | Functional |
| USR_DB_008 | Settings Page | Truy cập trang con `/dashboard/settings` | Đã đăng nhập, ở dashboard | 1. Click vào mục Cấu hình trên Sidebar hoặc gõ URL `/vi/dashboard/settings`. | | Hiển thị trang cấu hình hệ thống/cá nhân với tiêu đề và mô tả placeholder (từ file dịch `dashboardAdmin` namespace). Không bị crash layout. | Medium | Functional |
| USR_DB_009 | Responsive | Responsive layout trên màn hình nhỏ | Đã đăng nhập, mở dashboard | 1. Co nhỏ màn hình về tablet (768px) và mobile (375px).<br>2. Kiểm tra Sidebar và Navbar. | Mobile viewport | - Sidebar tự động ẩn đi trên mobile.<br>- Navbar hiển thị thêm nút Hamburger để mở menu hoặc hiển thị Sidebar dưới dạng drawer trượt ra từ cạnh.<br>- Content chính co giãn 100% chiều rộng, không bị tràn ngang. | High | Responsive |

## 5. Test data đề xuất

* Tài khoản test: `member@danangtrip.vn` / mật khẩu: `DaNangTrip@2026` (vai trò: `user`, trạng thái active).

## 6. Checklist regression

* Đăng nhập thành công và được redirect ngược lại chính xác trang dashboard con đã yêu cầu lúc trước (thông qua `callbackUrl`).
* Đăng xuất xóa cookie/token phải đá ngay người dùng ra khỏi `/dashboard` về lại trang chủ hoặc trang đăng nhập.

## 7. Ghi chú kỹ thuật

* Layout dashboard sử dụng hook `useAuth` từ `@/features/auth` để lấy dữ liệu đăng nhập.
* Link điều hướng và router chuyển hướng sử dụng router tùy chỉnh của `next-intl` (`@/i18n/navigation`) để giữ nguyên mã ngôn ngữ (`locale`) trên URL.
