# MỞ ĐẦU

## 1. Giới thiệu

Trong lĩnh vực du lịch, công nghệ thông tin được ứng dụng để hỗ trợ tra cứu thông tin, quản lý dịch vụ, tiếp nhận đặt chỗ và tương tác với khách hàng trên môi trường trực tuyến. Người dùng thường tìm kiếm thông tin địa điểm, xem đánh giá, tham khảo lịch trình, so sánh giá tour và đặt dịch vụ trực tuyến trước khi quyết định chuyến đi. Đối với Đà Nẵng, hệ thống thông tin du lịch có thể hỗ trợ tổ chức dữ liệu địa điểm, tour, lịch khởi hành và đơn đặt tour theo mô hình tập trung, qua đó giảm thao tác quản lý thủ công và cải thiện khả năng tra cứu của người dùng.

Hệ thống DanangTrip được xây dựng nhằm cung cấp nền tảng web phục vụ tra cứu thông tin du lịch Đà Nẵng, đặt tour trực tuyến và quản lý dữ liệu du lịch thông qua giao diện người dùng và giao diện quản trị. Hệ thống bao gồm các nhóm chức năng: tìm kiếm địa điểm/tour, bản đồ, giỏ hàng, đặt tour, thanh toán, đánh giá, quản lý tài khoản, trợ lý tư vấn du lịch và quản trị dữ liệu vận hành.

## 2. Mục đích và ý nghĩa đề tài

### 2.1. Mục đích

Mục đích của đề tài là xây dựng một website du lịch Đà Nẵng có khả năng phục vụ đồng thời hai nhóm người dùng: khách du lịch và quản trị viên. Hệ thống cần đáp ứng các mục tiêu chính:

- Cung cấp thông tin địa điểm du lịch, danh mục, tiện ích, hình ảnh, vị trí và đánh giá.
- Cung cấp danh sách tour, chi tiết tour, lịch khởi hành, kiểm tra chỗ trống và đặt tour.
- Hỗ trợ giỏ hàng, tính giá, khuyến mãi, thanh toán và tra cứu trạng thái thanh toán.
- Hỗ trợ tài khoản người dùng, hồ sơ cá nhân, yêu thích, lịch sử đặt tour, thông báo và đánh giá.
- Cung cấp trợ lý tư vấn du lịch (chatbot), tìm kiếm và gợi ý dựa trên dữ liệu trong hệ thống.
- Cung cấp trang quản trị để vận hành dữ liệu, theo dõi doanh thu, đơn đặt tour, thanh toán, đánh giá và báo cáo.

### 2.2. Ý nghĩa

Về mặt thực tiễn, đề tài góp phần xây dựng một nền tảng số hóa thông tin du lịch Đà Nẵng, giúp người dùng tìm kiếm và đặt dịch vụ thuận tiện hơn. Hệ thống cũng hỗ trợ đơn vị quản lý giảm thao tác thủ công trong việc cập nhật dữ liệu, xử lý đặt chỗ, xác nhận thanh toán và theo dõi tình hình kinh doanh.

Về mặt học thuật, đề tài giúp sinh viên vận dụng kiến thức về phân tích thiết kế hệ thống, cơ sở dữ liệu, phát triển giao diện web, xây dựng API phía máy chủ, xác thực, phân quyền, xử lý giao dịch, tích hợp dịch vụ bên ngoài, kiểm thử và triển khai.

Về khả năng mở rộng, hệ thống có thể được bổ sung các chức năng cá nhân hóa lịch trình, đề xuất tour dựa trên hành vi người dùng và tích hợp dữ liệu từ các nhà cung cấp dịch vụ du lịch.

## 3. Phạm vi đề tài

Đề tài tập trung vào các chức năng chính:

- Website người dùng: trang chủ, địa điểm, tour, tìm kiếm, bản đồ, gần tôi, blog, liên hệ, giỏ hàng, đặt tour, thanh toán, hồ sơ, đánh giá, yêu thích và thông báo.
- Website quản trị: bảng điều khiển, quản lý địa điểm, danh mục địa điểm, tour, danh mục tour, lịch khởi hành, đơn đặt tour, thanh toán, người dùng, bài viết, đánh giá, liên hệ, thông báo, khuyến mãi, cấu hình và báo cáo.
- API phía máy chủ: cung cấp REST API theo nhóm công khai, nhóm yêu cầu xác thực và nhóm quản trị; xử lý xác thực, phân quyền, nghiệp vụ đặt tour, thanh toán, đánh giá, tải ảnh, thống kê và chatbot.
- Cơ sở dữ liệu: sử dụng PostgreSQL/Supabase để lưu trữ người dùng, địa điểm, tour, lịch khởi hành, đơn đặt tour, thanh toán, đánh giá, blog, thông báo, khuyến mãi, cấu hình, dữ liệu chatbot và nhật ký tương tác.

Các nội dung ngoài phạm vi phiên bản hiện tại:

- Kết nối trực tiếp với hệ thống quản lý tour của bên thứ ba.
- Tối ưu đầy đủ hệ thống gợi ý độc lập trong môi trường vận hành thực tế.
- Ứng dụng di động nguyên bản.
- Hệ thống kế toán hoặc quản trị tài chính chuyên sâu.

## 4. Đối tượng nghiên cứu

Đối tượng nghiên cứu của đề tài gồm các thành phần sau:

- Nghiệp vụ du lịch trực tuyến: tra cứu địa điểm, xem tour, đặt tour, thanh toán, đánh giá và chăm sóc khách hàng.
- Nghiệp vụ quản trị du lịch: quản lý địa điểm, tour, lịch khởi hành, đơn đặt tour, thanh toán, người dùng, nội dung, khuyến mãi và báo cáo.
- Kiến trúc phát triển web hiện đại với tầng giao diện tách riêng API phía máy chủ.
- Kỹ thuật xây dựng RESTful API, xác thực bằng mã thông báo (token), phân quyền và xử lý giao dịch.
- Kỹ thuật tổ chức dữ liệu du lịch và khai thác dữ liệu cho tìm kiếm, gợi ý và chatbot.

## 5. Phương pháp nghiên cứu

Đề tài sử dụng các phương pháp sau:

### 5.1. Phương pháp khảo sát và phân tích yêu cầu

Sinh viên khảo sát các chức năng phổ biến của website du lịch như tìm kiếm địa điểm, xem thông tin tour, đặt tour, thanh toán trực tuyến, quản lý hồ sơ người dùng, đánh giá dịch vụ và quản trị nội dung. Từ đó xác định các tác nhân, yêu cầu chức năng, yêu cầu phi chức năng và phạm vi triển khai.

### 5.2. Phương pháp phân tích thiết kế hướng chức năng

Các nghiệp vụ chính được phân rã thành ca sử dụng (use case), biểu đồ tuần tự, biểu đồ hoạt động và mô hình dữ liệu. Phương pháp này giúp làm rõ luồng xử lý giữa người dùng, giao diện, API, cơ sở dữ liệu và dịch vụ bên ngoài.

### 5.3. Phương pháp thiết kế cơ sở dữ liệu quan hệ

Dữ liệu được mô hình hóa thành các thực thể như người dùng, địa điểm, tour, lịch khởi hành, đơn đặt tour, thanh toán, đánh giá, bài viết và thông báo. Các quan hệ một-nhiều, nhiều-nhiều và ràng buộc dữ liệu được thể hiện qua migration Laravel.

### 5.4. Phương pháp phát triển lặp

Hệ thống được triển khai theo từng phân hệ: API phía máy chủ, website người dùng, trang quản trị, thanh toán, báo cáo, chatbot và kiểm thử. Sau mỗi phân hệ, sinh viên kiểm tra chức năng, sửa lỗi và tích hợp với các phân hệ liên quan.

### 5.5. Phương pháp kiểm thử thực nghiệm

Các chức năng được kiểm thử thông qua kiểm thử đơn vị, kiểm thử chức năng, kiểm thử giao diện và kiểm thử thủ công. Đối với các luồng quan trọng như đặt tour và thanh toán, cần kiểm tra cả trường hợp thành công và thất bại.

## 6. Các bước triển khai

Quá trình thực hiện đề tài được chia thành các giai đoạn:

1. Khảo sát và phân tích yêu cầu: xác định tác nhân, nghiệp vụ người dùng, nghiệp vụ quản trị và các dữ liệu cần quản lý.
2. Thiết kế hệ thống: thiết kế kiến trúc tổng thể, phân tách website người dùng, trang quản trị, API phía máy chủ và cơ sở dữ liệu.
3. Xây dựng API phía máy chủ: triển khai Laravel API, migration, model, repository, service, controller, middleware xác thực và phân quyền.
4. Xây dựng website người dùng: triển khai Next.js, giao diện đa ngôn ngữ, tích hợp API, các luồng tìm kiếm, đặt tour, thanh toán và hồ sơ cá nhân.
5. Xây dựng trang quản trị: triển khai React/Vite, định tuyến, biểu mẫu quản trị, bảng dữ liệu, báo cáo và phân quyền quản trị viên.
6. Tích hợp dịch vụ: tải hình ảnh lên Cloudinary, thanh toán SePay, gửi email, xuất báo cáo và sinh hóa đơn PDF.
7. Tích hợp AI/chatbot: đồng bộ cơ sở tri thức từ tour, địa điểm, bài viết và chính sách; xây dựng luồng tư vấn du lịch.
8. Kiểm thử và hoàn thiện: kiểm tra chức năng, xử lý lỗi, tối ưu giao diện, hoàn thiện tài liệu và báo cáo.

## 7. Công nghệ và kỹ thuật sử dụng

| Thành phần | Công nghệ |
| --- | --- |
| Website người dùng | Next.js 16, React 19, TypeScript, React Query, Zustand, next-intl |
| Trang quản trị | React 19, Vite, TypeScript, React Router, React Query, React Hook Form |
| API phía máy chủ | Laravel 12, PHP 8.2, JWT Auth, Laravel Sanctum, mẫu Repository-Service |
| Cơ sở dữ liệu | PostgreSQL/Supabase, quản lý lược đồ bằng Laravel migrations |
| Bộ nhớ đệm/Hàng đợi | Redis/Predis, Laravel Jobs |
| Bản đồ | Leaflet, React Leaflet, Leaflet Routing Machine |
| Tải ảnh | Cloudinary |
| Thanh toán | SePay/VietQR, callback/IPN thanh toán |
| Báo cáo/tài liệu | Maatwebsite Excel, DomPDF |
| AI/chatbot | Intent Guard, Query Understanding, SQL RAG, AI Failover, Cache Layer |
| Kiểm thử | PHPUnit, Vitest, Playwright |

## 8. Cấu trúc báo cáo

Báo cáo được tổ chức theo các phần chính:

- **Mở đầu**: Trình bày lý do chọn đề tài, mục tiêu, ý nghĩa, phạm vi, đối tượng, phương pháp nghiên cứu và công nghệ sử dụng.
- **Chương 1 - Cơ sở lý thuyết**: Trình bày kiến thức nền về kiến trúc máy khách - máy chủ, Next.js/React, Laravel API, xác thực JWT, cơ sở dữ liệu quan hệ, thanh toán trực tuyến, chatbot và kiểm thử.
- **Chương 2 - Phân tích thiết kế hệ thống**: Trình bày tác nhân, yêu cầu chức năng, yêu cầu phi chức năng, ca sử dụng, biểu đồ tuần tự, biểu đồ hoạt động, kiến trúc hệ thống, thiết kế cơ sở dữ liệu và API.
- **Chương 3 - Triển khai thực tế**: Trình bày cấu trúc dự án, môi trường phát triển, triển khai API phía máy chủ, website người dùng, trang quản trị, đặt tour, thanh toán, chatbot, kiểm thử và kết quả giao diện.
- **Kết luận và hướng phát triển**: Tổng kết kết quả đạt được, hạn chế và hướng mở rộng.

## 9. Kết quả dự kiến đạt được

### 9.1. Về mặt lý thuyết

- Nắm được quy trình phân tích, thiết kế và triển khai một hệ thống web theo kiến trúc máy khách - máy chủ.
- Hiểu cách tổ chức API phía máy chủ theo controller, service, repository, model và migration.
- Hiểu cách xây dựng giao diện web hiện đại với Next.js, React Query, quản lý trạng thái và đa ngôn ngữ.
- Nắm được quy trình thiết kế cơ sở dữ liệu cho nghiệp vụ du lịch, đặt tour, thanh toán và quản trị nội dung.
- Biết cách tích hợp các dịch vụ như thanh toán, tải ảnh, email, PDF, báo cáo và chatbot.

### 9.2. Về mặt ứng dụng

- Hoàn thiện website người dùng phục vụ tra cứu, khám phá, đặt tour và quản lý tài khoản.
- Hoàn thiện trang quản trị phục vụ vận hành dữ liệu và theo dõi hoạt động kinh doanh.
- Hoàn thiện API phía máy chủ có phân quyền, xử lý nghiệp vụ và cung cấp dữ liệu cho website người dùng cùng trang quản trị.
- Xây dựng nền tảng mở rộng cho gợi ý thông minh và trợ lý tư vấn du lịch.
