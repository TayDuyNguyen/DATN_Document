# CHƯƠNG 3. TRIỂN KHAI THỰC TẾ

## 3.1. Cấu trúc hệ thống

Dự án được tổ chức thành nhiều thư mục độc lập:

| Thư mục | Vai trò |
| --- | --- |
| `danangtrip-web` | Website người dùng xây dựng bằng Next.js |
| `danangtrip-admin` | Trang quản trị xây dựng bằng React/Vite |
| `danangtrip-api` | API phía máy chủ xây dựng bằng Laravel |
| `DATN_AI` | Định hướng mô-đun gợi ý/AI độc lập |
| `DATN_Tài liệu` | Tài liệu, dữ liệu hình ảnh/video và báo cáo |
| `Báo cáo DATN` | Bộ mẫu Word và file báo cáo mẫu |

## 3.2. Môi trường phát triển

| Thành phần | Công nghệ chính |
| --- | --- |
| API phía máy chủ | PHP 8.2, Laravel 12, Composer |
| Website người dùng | Node.js, Next.js 16, React 19, TypeScript |
| Trang quản trị | Node.js, Vite, React 19, TypeScript |
| Cơ sở dữ liệu | PostgreSQL/Supabase, quản lý lược đồ bằng Laravel migration |
| Bộ nhớ đệm/Hàng đợi | Redis/Predis, Laravel Queue/Jobs |
| Công cụ kiểm thử | PHPUnit, Playwright, Vitest |
| Công cụ triển khai giao diện | OpenNext Cloudflare, Wrangler, Vite build |

### 3.2.1. Môi trường triển khai dự kiến/thực tế

Khi hoàn thiện báo cáo, cần thay các giá trị mô tả ở bảng dưới bằng thông tin triển khai thật của đồ án nếu hệ thống đã được triển khai công khai.

| Thành phần | Môi trường/công cụ | Ghi chú |
| --- | --- | --- |
| Website người dùng | OpenNext Cloudflare/Cloudflare Workers hoặc môi trường tương đương | Dự án có cấu hình OpenNext Cloudflare và Wrangler |
| Trang quản trị | Cloudflare Pages/Vercel/máy chủ tĩnh hoặc môi trường tương đương | Đóng gói bằng Vite |
| API phía máy chủ | Máy chủ PHP/Laravel hoặc dịch vụ lưu trữ hỗ trợ Laravel | Laravel API cung cấp endpoint `/api/v1` |
| Cơ sở dữ liệu | Supabase PostgreSQL | Lưu dữ liệu nghiệp vụ chính |
| Bộ nhớ đệm/Hàng đợi | Redis/Predis và bảng `chat_cache` | Dùng cho bộ nhớ đệm, hàng đợi hoặc bộ nhớ đệm chatbot tùy cấu hình |
| Lưu trữ hình ảnh/video | Cloudinary | Lưu ảnh địa điểm, tour, ảnh đại diện, bài viết |
| Cổng thanh toán | SePay/VietQR | Nhận callback/IPN cập nhật thanh toán |
| Nhà cung cấp AI | Gemini/OpenAI hoặc nhà cung cấp cấu hình trong hệ thống | Dùng cho chatbot và embedding nếu bật |

Các thông tin nhạy cảm như khóa API, mật khẩu cơ sở dữ liệu, mã thông báo thanh toán hoặc khóa bí mật webhook không được đưa vào báo cáo.

## 3.3. Triển khai API phía máy chủ

Laravel cung cấp REST API phiên bản `/api/v1`. Các tuyến API được tổ chức theo nhóm công khai, nhóm yêu cầu xác thực và nhóm quản trị. Nghiệp vụ được triển khai trong các lớp dịch vụ như:

- `AuthService`: đăng ký, đăng nhập, làm mới mã thông báo, quên mật khẩu, xác thực email.
- `LocationService`: danh sách địa điểm, chi tiết, địa điểm nổi bật, địa điểm gần người dùng, đánh giá, ảnh, lượt xem, quản trị địa điểm.
- `TourService` và `TourScheduleService`: danh sách tour, chi tiết tour, lịch khởi hành, trạng thái, số chỗ.
- `BookingService`: tính giá, tạo đơn đặt tour, hủy đơn đặt tour, xác nhận, hoàn tất, cập nhật trạng thái.
- `PaymentService` và `SepayPaymentService`: tạo thanh toán, xử lý callback/IPN, thử lại giao dịch, hoàn tiền.
- `RatingService`: tạo, sửa, xóa, duyệt, thống kê đánh giá.
- `FavoriteService`: thêm/xóa/kiểm tra yêu thích.
- `SearchService`: tìm kiếm, gợi ý, xu hướng và đề xuất.
- `DashboardService`: thống kê bảng điều khiển, báo cáo doanh thu, đơn đặt tour, người dùng, địa điểm.
- `ChatService` và nhóm `Chat/*Service`: chatbot, cơ sở tri thức, embedding và tìm kiếm ngữ cảnh.

API phía máy chủ sử dụng giao dịch ở các nghiệp vụ quan trọng như tạo đơn đặt tour, cập nhật thanh toán và xác nhận đơn đặt tour nhằm đảm bảo toàn vẹn dữ liệu.

### 3.3.1. Tổ chức tuyến API

Tệp định tuyến chính của API phía máy chủ là `routes/api.php`. Tất cả API được đặt dưới tiền tố `/api/v1`. Việc chia tuyến thành ba nhóm giúp kiểm soát quyền truy cập rõ ràng:

- Tuyến công khai: phục vụ dữ liệu công khai, không yêu cầu mã thông báo.
- Tuyến yêu cầu xác thực: yêu cầu mã thông báo JWT, phục vụ nghiệp vụ cá nhân của người dùng.
- Tuyến quản trị: yêu cầu mã thông báo JWT và vai trò quản trị viên.

Cách tổ chức này làm giảm rủi ro truy cập sai quyền và giúp tầng giao diện biết rõ API nào cần đăng nhập.

### 3.3.2. Tổ chức tầng dịch vụ

API phía máy chủ không xử lý toàn bộ nghiệp vụ trực tiếp trong controller. Controller chủ yếu nhận yêu cầu, gọi service và trả phản hồi. Service chịu trách nhiệm xử lý logic nghiệp vụ, còn repository/model chịu trách nhiệm truy vấn dữ liệu. Ví dụ:

- Khi tạo đơn đặt tour, `BookingController` gọi `BookingService::createBooking`.
- `BookingService` kiểm tra lịch khởi hành, tính số lượng khách, tính giá, tạo đơn đặt tour và chi tiết đơn đặt tour trong giao dịch.
- Khi thanh toán thành công, `PaymentService` hoặc `SepayPaymentService` cập nhật thanh toán và đơn đặt tour.

Ưu điểm của cách tổ chức này:

- Controller gọn hơn.
- Nghiệp vụ tập trung ở service.
- Dễ kiểm thử từng service.
- Dễ mở rộng khi thêm phương thức thanh toán hoặc loại đơn đặt tour mới.

### 3.3.3. Kết nối cơ sở dữ liệu PostgreSQL/Supabase

API phía máy chủ Laravel sử dụng PostgreSQL/Supabase làm hệ quản trị cơ sở dữ liệu. Cấu trúc bảng được quản lý thông qua Laravel migration, giúp quá trình triển khai và cập nhật lược đồ có thể kiểm soát bằng mã nguồn.

Các nghiệp vụ quan trọng như tạo đơn đặt tour, xác nhận thanh toán, cập nhật số chỗ lịch khởi hành và hoàn tiền cần sử dụng giao dịch để đảm bảo dữ liệu không bị sai lệch khi có lỗi giữa chừng. Ngoài ra, các bảng như `locations`, `tours`, `bookings`, `payments` và `ratings` cần được đánh chỉ mục phù hợp để tối ưu truy vấn danh sách, tìm kiếm và báo cáo.

### 3.3.4. Xử lý lỗi và phản hồi API

Hệ thống có trait/support class phục vụ chuẩn hóa phản hồi lỗi. API cần trả về cấu trúc thống nhất để tầng giao diện dễ xử lý. Các nhóm lỗi phổ biến:

- Lỗi validate dữ liệu đầu vào.
- Lỗi xác thực hoặc hết hạn mã thông báo.
- Lỗi không đủ quyền.
- Lỗi không tìm thấy tài nguyên.
- Lỗi nghiệp vụ như hết chỗ, đơn đặt tour không thể hủy, thanh toán sai trạng thái.
- Lỗi hệ thống hoặc dịch vụ bên ngoài.

### 3.3.5. Xử lý tải ảnh

Tải ảnh được tách thành `UploadService`. Hệ thống hỗ trợ tải một ảnh, nhiều ảnh và xóa ảnh. Các chức năng cần tải ảnh gồm:

- Ảnh đại diện người dùng.
- Ảnh đại diện và bộ sưu tập ảnh của địa điểm.
- Ảnh đại diện và bộ sưu tập ảnh của tour.
- Ảnh trong đánh giá.
- Ảnh bài viết hoặc trang đích.

Khi viết báo cáo, nên chụp minh họa luồng tải ảnh ở trang quản trị địa điểm hoặc tour.

## 3.4. Triển khai website người dùng

Website người dùng nằm trong `danangtrip-web`, sử dụng Next.js App Router với đường dẫn theo ngôn ngữ. Các trang chính gồm:

- Trang chủ: `/[locale]`
- Giới thiệu: `/about`
- Danh sách và chi tiết địa điểm: `/locations`, `/locations/[slug]`
- Địa điểm theo danh mục: `/categories/[slug]/locations`
- Bản đồ và gần tôi: `/map`, `/nearby`
- Tìm kiếm: `/search`
- Danh sách và chi tiết tour: `/tours`, `/tours/[slug]`
- Lịch khởi hành và đặt tour: `/tours/[slug]/departures`, `/tours/[slug]/book`
- Danh sách tour theo danh mục: `/tour-categories/[slug]/tours`
- Blog: `/blog`, `/blog/[slug]`
- Giỏ hàng: `/cart`
- Thanh toán: `/payment`, `/payment/result`
- Hồ sơ cá nhân: `/profile`, `/profile/bookings`, `/profile/favorites`, `/profile/ratings`, `/profile/notifications`, `/profile/recommendations`
- Điều khoản, quyền riêng tư và liên hệ: `/terms`, `/privacy`, `/contact`

Các lớp dịch vụ phía giao diện như `location.service.ts`, `tour.service.ts`, `booking.service.ts`, `payment.service.ts`, `auth.service.ts`, `search.service.ts` chịu trách nhiệm gọi API. React Query được dùng để lưu bộ nhớ đệm và đồng bộ dữ liệu từ máy chủ.

### 3.4.1. Luồng trang chủ

Trang chủ là điểm vào chính của website. Nội dung trang chủ nên gồm:

- Hero/khối giới thiệu du lịch Đà Nẵng.
- Địa điểm nổi bật.
- Tour nổi bật hoặc tour được quan tâm nhiều.
- Danh mục khám phá.
- Bài viết mới.
- Thống kê hoặc thông tin giới thiệu.
- Chatbot hoặc thành phần hỗ trợ nhanh.

API phía máy chủ cung cấp các endpoint `/home`, `/home/locations`, `/home/tours`, `/home/blogs` để giao diện tải dữ liệu.

### 3.4.2. Luồng địa điểm

Phân hệ địa điểm gồm danh sách, bộ lọc, chi tiết, ảnh, đánh giá và bản đồ. Người dùng có thể lọc theo danh mục, quận/huyện, mức giá, đánh giá, từ khóa hoặc trạng thái nổi bật. Trang chi tiết địa điểm hiển thị mô tả, địa chỉ, giờ mở cửa, tọa độ, ảnh, đánh giá và địa điểm lân cận.

### 3.4.3. Luồng tour

Phân hệ tour gồm danh sách tour, chi tiết tour, lịch trình, giá, số khách, lịch khởi hành, đánh giá và đặt tour. Một tour có thể có nhiều lịch khởi hành, mỗi lịch có số chỗ và giá riêng. Trước khi đặt tour, hệ thống cần kiểm tra lịch còn chỗ và tính lại giá theo số lượng người lớn, trẻ em, em bé.

### 3.4.4. Luồng hồ sơ người dùng

Khu vực hồ sơ cho phép người dùng:

- Xem và cập nhật thông tin cá nhân.
- Đổi mật khẩu.
- Quản lý ảnh đại diện.
- Xem danh sách đơn đặt tour và chi tiết đơn đặt tour.
- Tra cứu đơn đặt tour theo mã.
- Xem danh sách yêu thích.
- Xem lịch sử đánh giá.
- Xem thông báo.
- Xem đề xuất cá nhân hóa.
- Xóa tài khoản.

Đây là nhóm màn hình cần chụp nhiều hình trong chương triển khai thực tế.

## 3.5. Triển khai trang quản trị

Trang quản trị nằm trong `danangtrip-admin`, sử dụng React Router. Các đường dẫn chính gồm:

- `/dashboard`: bảng điều khiển tổng quan.
- `/admin/tours/list`, `/admin/tours/create`, `/admin/tours/edit/:id`: quản lý tour.
- `/admin/tour-categories`: quản lý danh mục tour.
- `/admin/tours/schedules`: quản lý lịch khởi hành.
- `/admin/locations`, `/admin/locations/create`, `/admin/locations/edit/:id`, `/admin/locations/detail/:id`: quản lý địa điểm.
- `/admin/location-categories`: quản lý danh mục địa điểm.
- `/admin/bookings`, `/admin/bookings/detail/:id`: quản lý đơn đặt tour.
- `/admin/payments`, `/admin/payments/detail/:id`: quản lý thanh toán.
- `/admin/reports/ratings`, `/admin/reports/bookings`, `/admin/reports/revenue`, `/admin/reports/locations`, `/admin/reports/users`: báo cáo.
- `/admin/users`, `/admin/users/create`, `/admin/users/detail/:id`, `/admin/users/edit/:id`: quản lý người dùng.
- `/admin/blog-posts`, `/admin/blog-categories`: quản lý blog.
- `/admin/ratings`, `/admin/contacts`, `/admin/notifications`, `/admin/promotions`, `/admin/settings`, `/admin/landing-pages`.

Trang quản trị tập trung vào thao tác dữ liệu dạng bảng, bộ lọc, biểu mẫu thêm/sửa, xác nhận hành động, biểu đồ và báo cáo.

### 3.5.1. Dashboard và báo cáo

Bảng điều khiển quản trị giúp quản trị viên theo dõi tình trạng hệ thống. Các dữ liệu nên trình bày trong báo cáo:

- Tổng số người dùng.
- Tổng số đơn đặt tour.
- Doanh thu.
- Số thanh toán thành công/thất bại.
- Top tour được đặt nhiều.
- Top địa điểm được xem nhiều.
- Biểu đồ tăng trưởng người dùng.
- Biểu đồ đơn đặt tour theo thời gian.
- Xu hướng tìm kiếm.

### 3.5.2. Quản lý địa điểm

Quản trị viên có thể thêm, sửa, xóa, bật/tắt trạng thái và đánh dấu nổi bật địa điểm. Dữ liệu địa điểm gồm tên, đường dẫn định danh, danh mục, mô tả, địa chỉ, quận/huyện, tọa độ, giờ mở cửa, khoảng giá, ảnh, video, thẻ phân loại và tiện ích.

### 3.5.3. Quản lý tour và lịch khởi hành

Quản trị viên quản lý thông tin tour gồm tên, danh mục, mô tả, lịch trình, giá người lớn/trẻ em/em bé, thời lượng, điểm hẹn, ảnh, trạng thái, tour nổi bật và tour được quan tâm nhiều. Lịch khởi hành được quản lý riêng để kiểm soát ngày đi, ngày về, số chỗ, số chỗ đã đặt, giá ghi đè và trạng thái.

### 3.5.4. Quản lý đơn đặt tour và thanh toán

Quản trị viên có thể xem danh sách đơn đặt tour, lọc theo trạng thái, xem chi tiết khách hàng, xác nhận thanh toán, cập nhật trạng thái đơn đặt tour, xuất hóa đơn và xuất báo cáo. Với thanh toán, quản trị viên có thể xem mã giao dịch, cổng thanh toán, số tiền, trạng thái, thời gian thanh toán và xử lý hoàn tiền nếu có.

### 3.5.5. Quản lý nội dung và tương tác

Các phân hệ blog, trang đích, đánh giá, liên hệ, thông báo và khuyến mãi giúp hệ thống vận hành đầy đủ hơn. Quản trị viên có thể duyệt đánh giá, phản hồi liên hệ, gửi thông báo hàng loạt, tạo mã giảm giá và cập nhật cấu hình website.

## 3.6. Triển khai nghiệp vụ đặt tour

Luồng đặt tour được triển khai qua các bước:

1. Người dùng xem chi tiết tour và chọn lịch khởi hành.
2. Website người dùng gọi API để kiểm tra lịch khởi hành và tính giá.
3. Người dùng nhập thông tin khách, số lượng và mã khuyến mãi nếu có.
4. API phía máy chủ tạo đơn đặt tour và chi tiết đơn đặt tour trong giao dịch.
5. Người dùng chọn phương thức thanh toán.
6. API phía máy chủ tạo bản ghi thanh toán, sinh mã giao dịch/QR thanh toán.
7. Hệ thống nhận callback/IPN từ SePay và cập nhật trạng thái.
8. Người dùng xem kết quả thanh toán, chi tiết đơn đặt tour và hóa đơn.

Các trạng thái cần quản lý gồm trạng thái đơn đặt tour, trạng thái thanh toán, trạng thái lịch khởi hành và số chỗ còn lại.

## 3.7. Triển khai chatbot và gợi ý

Chatbot được triển khai ở API phía máy chủ thông qua endpoint `/chat`. Luồng xử lý chatbot không chỉ gửi trực tiếp câu hỏi của người dùng đến mô hình AI mà được tổ chức qua nhiều bước để đảm bảo câu trả lời bám sát dữ liệu hệ thống.

Hệ thống xây dựng cơ sở tri thức từ:

- Tour và lịch khởi hành.
- Địa điểm du lịch.
- Bài viết blog.
- Chính sách hỗ trợ, đặt tour và thanh toán.

Khi người dùng gửi câu hỏi, API phía máy chủ thực hiện các bước:

1. `ChatIntentGuardService` xác định câu hỏi có nằm trong phạm vi hỗ trợ của DanangTrip hay không.
2. `ChatQueryUnderstandingService` trích xuất các ràng buộc như điểm đến, ngân sách, số người, ngày đi và thời lượng.
3. Cache Layer kiểm tra khóa bộ nhớ đệm được tạo từ ngôn ngữ, ý định và câu hỏi đã chuẩn hóa nhằm xác định phản hồi tương ứng còn hiệu lực hay không.
4. `ChatKnowledgeSearchService` thực hiện SQL RAG, truy xuất dữ liệu liên quan từ tour, lịch khởi hành, địa điểm, bài viết và chính sách.
5. `ChatAiProviderService` gửi lời nhắc có ngữ cảnh đến nhà cung cấp AI và thực hiện chuyển đổi dự phòng khi nhà cung cấp lỗi, quá thời gian chờ hoặc vượt giới hạn.
6. Hệ thống lưu tin nhắn, lưu kết quả vào bộ nhớ đệm nếu phù hợp và trả phản hồi về giao diện.

API `/recommendations` cung cấp danh sách tour hoặc địa điểm đề xuất dựa trên các tín hiệu tương tác như tìm kiếm, lượt xem, yêu thích và đánh giá. Trong báo cáo cần nêu rõ thuật toán gợi ý hiện tại là dựa trên luật, thống kê hành vi hay mô hình học máy nếu có triển khai.

## 3.8. Triển khai tải ảnh, email, báo cáo và hóa đơn

Hệ thống có các tích hợp hỗ trợ vận hành:

- Tải ảnh qua Cloudinary cho địa điểm, tour, ảnh đại diện và nội dung.
- Gửi email qua dịch vụ thư điện tử/Brevo cho các luồng liên hệ, xác thực hoặc thông báo.
- Xuất báo cáo bằng Maatwebsite Excel cho bảng điều khiển, người dùng, đơn đặt tour, thanh toán, liên hệ, địa điểm.
- Sinh hóa đơn PDF bằng DomPDF thông qua `InvoicePdfService`.

## 3.9. Kiểm thử

Dự án có các kiểm thử phía máy chủ như:

- `ApiErrorResponseTest`
- `SecurityFixesTest`
- `RatingReadTrackingTest`
- `SyncTourScheduleAvailabilityTest`
- `AdminCategoryApiTest`
- `HomeControllerTest`
- `PromotionControllerTest`
- `SettingControllerTest`
- `UserProfileDeleteTest`

Dự án giao diện có các kiểm thử Playwright như:

- `user-booking-detail.spec.ts`
- `user-booking-by-code.spec.ts`
- `departure-select.spec.ts`
- `visual-change-password.spec.ts`
- `visual-test.ts`

Các lệnh kiểm thử/thẩm định cần ghi vào báo cáo sau khi chạy thực tế:

```bash
cd D:\DATN\danangtrip-api
php artisan test

cd D:\DATN\danangtrip-web
npm run typecheck
npm run lint
npm run build

cd D:\DATN\danangtrip-admin
npm run typecheck
npm run build
```

### 3.9.1. Kết quả kiểm thử chức năng

Trước khi kiểm thử thủ công từng chức năng, dự án được kiểm tra bằng các lệnh tự động ở API phía máy chủ, website người dùng và trang quản trị. Kết quả tại thời điểm biên soạn:

| STT | Thành phần | Lệnh kiểm tra | Kết quả thực tế | Trạng thái |
| --- | --- | --- | --- | --- |
| 1 | Laravel API | `php artisan test` | 38 kiểm thử đạt, 141 khẳng định, thời gian 2.16s | Đạt |
| 2 | Website người dùng Next.js | `npm run typecheck` | Kiểm tra kiểu dữ liệu TypeScript hoàn tất, không phát hiện lỗi kiểu | Đạt |
| 3 | Trang quản trị React/Vite | `npm run typecheck` | `tsc -b` hoàn tất, không phát hiện lỗi kiểu | Đạt |
| 4 | Website người dùng Next.js | `npm run build` | Đóng gói bản triển khai thành công, biên dịch thành công, sinh 66 trang tĩnh | Đạt |
| 5 | Trang quản trị React/Vite | `npm run build` | Đóng gói bản triển khai thành công, 3723 mô-đun được xử lý, hoàn tất trong 13.21s | Đạt |

Ghi chú về cảnh báo khi kiểm tra:

- API phía máy chủ có cảnh báo PHP thiếu phần mở rộng `imagick`, tuy nhiên toàn bộ kiểm thử vẫn đạt. Cảnh báo này cần được xử lý nếu chức năng xử lý ảnh yêu cầu Imagick trong môi trường vận hành thực tế.
- Bản đóng gói Next.js có cảnh báo quy ước tệp `middleware` không còn được khuyến nghị và cảnh báo môi trường thực thi biên đang ở trạng thái thử nghiệm. Đây không phải lỗi đóng gói nhưng cần theo dõi khi nâng cấp Next.js.
- Bản đóng gói trang quản trị có cảnh báo `lottie-web` sử dụng `eval`. Cần cân nhắc nếu hệ thống có yêu cầu bảo mật nghiêm ngặt về Content Security Policy.

Bảng dưới đây là khung kiểm thử chức năng thủ công cần điền kết quả thực tế sau khi chạy hệ thống với dữ liệu mẫu:

| STT | Phân hệ | Dữ liệu kiểm thử | Kết quả mong đợi | Kết quả thực tế | Trạng thái |
| --- | --- | --- | --- | --- | --- |
| 1 | Xác thực | Đăng ký bằng email chưa tồn tại | Tài khoản được tạo, không trùng email/tên đăng nhập | Chưa kiểm thử thủ công trong đợt chạy tự động | Cần kiểm thử giao diện |
| 2 | Xác thực | Đăng nhập đúng email/mật khẩu | Nhận mã thông báo và chuyển vào hệ thống | Chưa kiểm thử thủ công trong đợt chạy tự động | Cần kiểm thử giao diện |
| 3 | Xác thực | Đăng nhập sai mật khẩu | Hiển thị thông báo lỗi | Chưa kiểm thử thủ công trong đợt chạy tự động | Cần kiểm thử giao diện |
| 4 | Địa điểm | Lọc theo danh mục/quận | Danh sách hiển thị đúng dữ liệu | Chưa kiểm thử thủ công trong đợt chạy tự động | Cần kiểm thử giao diện |
| 5 | Địa điểm | Mở chi tiết một địa điểm | Hiển thị mô tả, ảnh, tọa độ, đánh giá | Chưa kiểm thử thủ công trong đợt chạy tự động | Cần kiểm thử giao diện |
| 6 | Tour | Mở chi tiết một tour đang hoạt động | Hiển thị giá, lịch trình, lịch khởi hành | Chưa kiểm thử thủ công trong đợt chạy tự động | Cần kiểm thử giao diện |
| 7 | Đặt tour | Tạo đơn đặt tour với lịch còn chỗ | Đơn đặt tour được tạo, số chỗ cập nhật | Chưa kiểm thử thủ công trong đợt chạy tự động | Cần kiểm thử giao diện/API |
| 8 | Đặt tour | Tạo đơn đặt tour vượt số chỗ | Hệ thống từ chối và báo lỗi | Chưa kiểm thử thủ công trong đợt chạy tự động | Cần kiểm thử giao diện/API |
| 9 | Thanh toán | Tạo thanh toán cho đơn đặt tour đang chờ xử lý | Sinh giao dịch/mã QR | Chưa kiểm thử thủ công trong đợt chạy tự động | Cần kiểm thử giao diện/API |
| 10 | Thanh toán | Nhận IPN hợp lệ từ SePay | Thanh toán thành công, đơn đặt tour được cập nhật | Đã có kiểm thử đơn vị kiểm tra callback gateway unsigned bị từ chối; IPN hợp lệ cần kiểm thử với payload SePay thật | Một phần |
| 11 | Đánh giá | Gửi đánh giá hợp lệ | Đánh giá được lưu/chờ duyệt | Đã có kiểm thử đơn vị liên quan trạng thái đã xem đánh giá; gửi đánh giá cần kiểm thử giao diện/API | Một phần |
| 12 | Quản trị tour | Quản trị viên thêm tour mới | Tour hiển thị ở danh sách quản trị và công khai khi đang hoạt động | Chưa kiểm thử thủ công trong đợt chạy tự động | Cần kiểm thử giao diện/API |
| 13 | Quản trị đánh giá | Quản trị viên duyệt đánh giá | Đánh giá hiển thị công khai | Chưa kiểm thử thủ công trong đợt chạy tự động | Cần kiểm thử giao diện/API |
| 14 | Chatbot | Hỏi tour theo ngân sách | Trả lời dựa trên dữ liệu tour phù hợp | Đã đối chiếu mã nguồn quy trình xử lý; cần kiểm thử với dữ liệu thật và nhà cung cấp AI được cấu hình | Cần kiểm thử AI |
| 15 | Chatbot | Hỏi câu ngoài phạm vi du lịch | Intent Guard từ chối hoặc hướng dẫn hỏi lại | Đã đối chiếu logic `ChatIntentGuardService`; cần kiểm thử API `/chat` | Một phần |
| 16 | Chatbot | Nhà cung cấp AI lỗi hoặc quá thời gian chờ | Hệ thống chuyển nhà cung cấp/khóa hoặc trả phản hồi dự phòng | Đã đối chiếu logic chuyển đổi dự phòng trong `ChatAiProviderService`; cần kiểm thử giả lập lỗi nhà cung cấp | Một phần |

### 3.9.2. Kế hoạch kiểm thử phi chức năng

| Nhóm | Cách kiểm thử đề xuất |
| --- | --- |
| Bảo mật | Kiểm tra API yêu cầu xác thực khi không có mã thông báo; kiểm tra người dùng thường truy cập API quản trị |
| Hiệu năng | Kiểm tra thời gian tải danh sách địa điểm/tour; kiểm tra phân trang |
| Tính đáp ứng giao diện | Chụp giao diện máy tính, máy tính bảng, thiết bị di động |
| Toàn vẹn dữ liệu | Kiểm tra đặt tour/thanh toán trong các trường hợp thành công/thất bại |
| Khả dụng | Kiểm tra trạng thái đang tải, trạng thái rỗng và trạng thái lỗi |
| Đa ngôn ngữ | Kiểm tra đường dẫn và nội dung ở tiếng Việt/tiếng Anh |

## 3.10. Kết quả giao diện cần chụp đưa vào báo cáo

Danh sách hình ảnh đề xuất:

- Hình 3.1: Giao diện trang chủ DanangTrip.
- Hình 3.2: Giao diện danh sách địa điểm.
- Hình 3.3: Giao diện chi tiết địa điểm.
- Hình 3.4: Giao diện bản đồ/gần tôi.
- Hình 3.5: Giao diện danh sách tour.
- Hình 3.6: Giao diện chi tiết tour.
- Hình 3.7: Giao diện chọn lịch khởi hành.
- Hình 3.8: Giao diện đặt tour.
- Hình 3.9: Giao diện thanh toán/QR.
- Hình 3.10: Giao diện kết quả thanh toán.
- Hình 3.11: Giao diện hồ sơ và lịch sử đặt tour.
- Hình 3.12: Giao diện chatbot tư vấn du lịch.
- Hình 3.13: Giao diện bảng điều khiển quản trị.
- Hình 3.14: Giao diện quản lý địa điểm.
- Hình 3.15: Giao diện quản lý tour.
- Hình 3.16: Giao diện quản lý đơn đặt tour.
- Hình 3.17: Giao diện quản lý thanh toán.
- Hình 3.18: Giao diện báo cáo doanh thu.

## 3.11. Đánh giá kết quả triển khai

Sau khi triển khai, hệ thống đáp ứng được hầu hết các nghiệp vụ chính của một website du lịch:

- Người dùng có thể tìm kiếm và khám phá nội dung du lịch.
- Người dùng có thể đặt tour, thanh toán và theo dõi đơn đặt tour.
- Người dùng có thể lưu yêu thích, đánh giá và nhận thông báo.
- Quản trị viên có thể quản lý dữ liệu và theo dõi báo cáo.
- API phía máy chủ có cấu trúc rõ ràng, phân quyền và xử lý nghiệp vụ tập trung.
- Hệ thống có hướng mở rộng cho AI/chatbot và hệ thống gợi ý.

Tuy nhiên, để đưa vào vận hành thực tế, hệ thống cần tiếp tục bổ sung dữ liệu thật, kiểm thử tải, giám sát, sao lưu dữ liệu, kiểm thử bảo mật chuyên sâu và quy trình vận hành.
