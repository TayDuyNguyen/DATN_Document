# CHƯƠNG 1. CƠ SỞ LÝ THUYẾT

## 1.1. Tổng quan về kiến trúc Client-Server

Kiến trúc Client-Server là mô hình phổ biến trong phát triển ứng dụng web. Trong mô hình này, Client chịu trách nhiệm hiển thị giao diện và tương tác với người dùng, trong khi Server xử lý nghiệp vụ, truy xuất dữ liệu, xác thực, phân quyền và cung cấp API.

Trong hệ thống DanangTrip, kiến trúc Client-Server được thể hiện qua ba thành phần:

- `danangtrip-web`: website người dùng, gọi API để hiển thị dữ liệu địa điểm, tour, đơn đặt tour, thanh toán và hồ sơ.
- `danangtrip-admin`: giao diện quản trị, gọi API quản trị để quản lý dữ liệu và báo cáo.
- `danangtrip-api`: Server API được xây dựng bằng Laravel, cung cấp REST API cho website người dùng và trang quản trị.

Mô hình này giúp tách biệt trách nhiệm giữa giao diện và nghiệp vụ, thuận tiện cho bảo trì, mở rộng và triển khai độc lập.

## 1.2. Tổng quan về Next.js và React

React là thư viện JavaScript dùng để xây dựng giao diện người dùng theo hướng thành phần. Next.js là khung phát triển xây dựng trên React, hỗ trợ định tuyến theo cấu trúc tệp, kết xuất phía Server, sinh trang tĩnh, tối ưu SEO và triển khai linh hoạt.

Trong DanangTrip, Next.js được dùng cho website người dùng vì phù hợp với các trang cần SEO như trang chủ, danh sách địa điểm, chi tiết địa điểm, danh sách tour, chi tiết tour và blog. Dự án còn sử dụng:

- TypeScript để tăng độ an toàn kiểu dữ liệu.
- React Query để quản lý trạng thái dữ liệu lấy từ API.
- Zustand để quản lý trạng thái cục bộ như xác thực, giỏ hàng hoặc trạng thái ứng dụng.
- next-intl để hỗ trợ đa ngôn ngữ.
- Leaflet để hiển thị bản đồ và vị trí du lịch.

## 1.3. Tổng quan về React/Vite cho trang quản trị

Vite là công cụ đóng gói giao diện có tốc độ phát triển nhanh, phù hợp với ứng dụng quản trị dạng ứng dụng một trang. React Router được dùng để quản lý đường dẫn nội bộ, React Query để đồng bộ trạng thái dữ liệu từ Server, React Hook Form và Yup/Zod để xử lý biểu mẫu và kiểm tra dữ liệu.

Trang quản trị DanangTrip sử dụng React/Vite để xây dựng các phân hệ bảng điều khiển, tour, lịch khởi hành, đơn đặt tour, thanh toán, địa điểm, bài viết, người dùng, đánh giá, liên hệ, thông báo, khuyến mãi và cấu hình. Đây là nhóm màn hình có tính thao tác lặp lại cao, cần bảng dữ liệu, bộ lọc, biểu đồ, biểu mẫu thêm/sửa và kiểm soát trạng thái.

## 1.4. Tổng quan về Laravel REST API

Laravel là khung phát triển PHP hỗ trợ phát triển ứng dụng web và API với hệ sinh thái đầy đủ: định tuyến, lớp trung gian (middleware), ORM, migration, hàng đợi, kiểm tra dữ liệu, bộ nhớ đệm, sự kiện, tác vụ nền và kiểm thử. REST API là phong cách thiết kế API sử dụng các phương thức HTTP như GET, POST, PUT, PATCH và DELETE để thao tác tài nguyên.

Server API của DanangTrip sử dụng Laravel 12 và tổ chức mã nguồn theo hướng:

- Controller tiếp nhận yêu cầu và trả phản hồi.
- Service xử lý nghiệp vụ.
- Repository truy vấn và thao tác dữ liệu.
- Model đại diện bảng dữ liệu.
- Cơ chế kiểm tra yêu cầu đầu vào giúp xác thực dữ liệu trước khi xử lý nghiệp vụ.
- Middleware xử lý xác thực, phân quyền và throttle.

Cách tổ chức này giúp nghiệp vụ được tách khỏi controller, dễ kiểm thử và dễ mở rộng.

## 1.5. Xác thực JWT và phân quyền

JWT là chuẩn mã thông báo dùng để truyền thông tin xác thực giữa Client và Server. Sau khi đăng nhập thành công, Server cấp mã thông báo truy cập (access token) và mã thông báo làm mới (refresh token). Client gửi mã thông báo trong các yêu cầu cần bảo vệ. Server kiểm tra mã thông báo để xác định người dùng và quyền truy cập.

Trong DanangTrip, API được chia thành:

- Nhóm tuyến công khai: không cần mã thông báo, dùng cho trang chủ, địa điểm, tour, blog, tìm kiếm, chatbot và liên hệ.
- Nhóm tuyến yêu cầu xác thực: cần đăng nhập, dùng cho hồ sơ, đơn đặt tour, thanh toán, yêu thích, đánh giá, thông báo và giỏ hàng.
- Nhóm tuyến quản trị: cần mã thông báo và quyền quản trị viên, dùng cho quản trị hệ thống.

## 1.6. PostgreSQL/Supabase và migration

PostgreSQL là hệ quản trị cơ sở dữ liệu quan hệ mã nguồn mở, hỗ trợ khóa ngoại, giao dịch (transaction), chỉ mục (index), ràng buộc dữ liệu, JSON/JSONB và tìm kiếm toàn văn (full-text search). Supabase cung cấp nền tảng dịch vụ backend dựng sẵn (backend-as-a-service) sử dụng PostgreSQL làm lõi lưu trữ, phù hợp với các hệ thống cần triển khai nhanh cơ sở dữ liệu quan hệ và quản lý dữ liệu trên môi trường đám mây.

PostgreSQL/Supabase được sử dụng do hệ thống có nhiều quan hệ dữ liệu cần quản lý bằng khóa ngoại và giao dịch, chẳng hạn quan hệ giữa người dùng, tour, lịch khởi hành, đơn đặt tour, chi tiết đơn đặt tour và thanh toán.

Laravel migration giúp định nghĩa cấu trúc bảng bằng mã nguồn, hỗ trợ quản lý phiên bản lược đồ, tạo bảng, thêm cột, tạo chỉ mục và quay lui khi cần. Trong dự án, migration cũng được sử dụng để khai báo khóa ngoại, chỉ mục tìm kiếm, ràng buộc trạng thái, ràng buộc giá trị tiền và một số ràng buộc phục vụ toàn vẹn dữ liệu.

Các nhóm bảng chính của DanangTrip và chức năng tương ứng được mô tả chi tiết trong Bảng 1.2:

*Bảng 1.2: Các nhóm bảng cơ sở dữ liệu và phân hệ chức năng tương ứng*

| STT | Nhóm chức năng | Các bảng trong cơ sở dữ liệu | Mô tả chức năng chính |
| :---: | :--- | :--- | :--- |
| 1 | Nhóm người dùng và xác thực | `users`, `refresh_tokens`, `password_reset_tokens`, `sessions` | Quản lý thông tin tài khoản (khách du lịch, quản trị viên), lưu phiên làm việc, quản lý refresh token duy trì đăng nhập và xử lý yêu cầu đặt lại mật khẩu. |
| 2 | Nhóm địa điểm | `locations`, `categories`, `subcategories`, `tags`, `amenities`, `location_tags`, `location_amenities`, `views` | Lưu trữ thông tin chi tiết địa điểm (tọa độ GPS, mô tả, hình ảnh), danh mục phân loại, tiện ích dịch vụ đi kèm, thẻ tìm kiếm và thống kê lượt xem. |
| 3 | Nhóm tour và đặt tour | `tours`, `tour_categories`, `tour_schedules`, `tour_locations`, `bookings`, `booking_items`, `cart_items` | Lưu trữ thông tin tour, danh mục tour, lịch khởi hành, chỗ trống khả dụng, giỏ hàng tạm thời, đơn đặt tour, hành khách, khuyến mãi hệ thống và phiếu giảm giá cá nhân đã áp dụng. |
| 4 | Nhóm thanh toán | `payments` | Lưu trữ lịch sử giao dịch và trạng thái thanh toán của đơn đặt tour qua SePay/VietQR hoặc thao tác xác nhận chuyển khoản thủ công của quản trị viên. |
| 5 | Nhóm nội dung | `blog_posts`, `blog_categories`, `blog_post_categories`, `landing_pages` | Quản lý các bài viết cẩm nang du lịch Đà Nẵng, danh mục bài viết, liên kết danh mục và nội dung các trang đích (landing pages) phục vụ SEO. |
| 6 | Nhóm tương tác | `favorites`, `ratings`, `rating_images`, `rating_helpful_votes`, `search_logs`, `notifications`, `contacts` | Ghi nhận nội dung yêu thích, đánh giá kèm hình ảnh, người dùng xác nhận đánh giá hữu ích, nhật ký tìm kiếm, thông báo hệ thống và liên hệ. |
| 7 | Nhóm điểm thành viên | `user_point_balances`, `point_rules`, `point_rewards`, `point_transactions`, `user_vouchers` | Quản lý số dư điểm, quy tắc cộng điểm, phần thưởng đổi điểm, lịch sử biến động điểm và phiếu giảm giá cá nhân. |
| 8 | Nhóm cấu hình và chatbot | `settings`, `promotions`, `chat_messages`, `chat_cache`, `chat_knowledge_base` | Quản lý cấu hình chung, khuyến mãi, lịch sử hội thoại, bộ nhớ đệm câu trả lời và cơ sở tri thức có dữ liệu embedding. |

## 1.7. Thanh toán trực tuyến và IPN

Thanh toán trực tuyến trong hệ thống đặt tour cần đảm bảo các yếu tố: tạo giao dịch, gắn giao dịch với đơn đặt tour, xác nhận trạng thái, chống xử lý trùng, cập nhật trạng thái đơn đặt tour sau thanh toán và lưu lịch sử giao dịch.

DanangTrip tích hợp SePay/VietQR. Khi người dùng tạo thanh toán, hệ thống sinh thông tin giao dịch và nội dung chuyển khoản. Khi cổng thanh toán gửi IPN/callback, Server API kiểm tra dữ liệu, xác thực giao dịch, cập nhật bảng `payments` và trạng thái `bookings`.

## 1.8. Chatbot, truy xuất tri thức và gợi ý du lịch

Chatbot du lịch cần trả lời dựa trên dữ liệu thật của hệ thống như tour, địa điểm, bài viết và chính sách. Nếu chatbot chỉ dựa vào kiến thức tổng quát của mô hình AI, câu trả lời có thể sai với dữ liệu hiện có trong hệ thống. Vì vậy, DanangTrip tổ chức chatbot theo hướng truy xuất dữ liệu nội bộ trước khi sinh phản hồi.

Các thành phần chính trong quy trình xử lý của chatbot gồm:

- **Bộ kiểm soát ý định (Intent Guard)**: kiểm tra câu hỏi có thuộc phạm vi du lịch, tour, địa điểm, đặt tour, thanh toán, tài khoản hoặc chương trình điểm thành viên hay không.
- **Thành phần phân tích truy vấn (Query Understanding)**: trích xuất điểm đến, vùng, chủ đề địa điểm, khoảng giá, số người, ngày đi, thời lượng và tiêu chí sắp xếp.
- **Truy xuất dữ liệu có cấu trúc**: lọc dữ liệu từ `tours`, `tour_schedules`, `locations`, `blog_posts` và dữ liệu chính sách theo các tham số đã phân tích.
- **Tìm kiếm ngữ nghĩa bằng embedding**: khi được bật bằng cấu hình, hệ thống tạo embedding cho câu hỏi, lấy các bản ghi cơ sở tri thức có embedding và xếp hạng bằng độ tương đồng cosin. Phiên bản hiện tại không sử dụng một cơ sở dữ liệu véc-tơ chuyên dụng.
- **Lớp bộ nhớ đệm (Cache Layer)**: lưu phản hồi trong bảng `chat_cache` theo khóa tạo từ ngôn ngữ, ý định và câu hỏi đã chuẩn hóa.
- **Cơ chế chuyển đổi dự phòng AI (AI Failover)**: chuyển sang nhà cung cấp hoặc khóa khác khi nhà cung cấp hiện tại lỗi, hết hạn mức hoặc tạm thời không phản hồi.

DanangTrip có nhóm lớp dịch vụ xử lý chatbot gồm:

- `ChatService`: điều phối luồng gửi tin nhắn và tạo phản hồi.
- `ChatIntentGuardService`: phân loại ý định và giới hạn phạm vi câu hỏi.
- `ChatQueryUnderstandingService`: trích xuất điểm đến, giá, số người, ngày, thời lượng.
- `ChatKnowledgeSyncService`: đồng bộ dữ liệu tour, địa điểm, blog và chính sách vào cơ sở tri thức.
- `ChatKnowledgeSearchService`: tìm kiếm dữ liệu phù hợp từ tour, địa điểm, blog, chính sách và cơ sở tri thức.
- `ChatEmbeddingService`: tạo embedding thông qua nhà cung cấp như Gemini hoặc OpenAI khi cần tìm kiếm ngữ nghĩa.
- `ChatAiProviderService`: điều phối nhà cung cấp AI và xử lý chuyển đổi dự phòng khi gọi mô hình.

Mối quan hệ và luồng tương tác giữa các lớp dịch vụ xử lý chatbot này được biểu diễn trực quan thông qua sơ đồ cấu trúc các lớp dịch vụ chatbot (mã nguồn sơ đồ Draw.io được cung cấp tại Phụ lục - mục 7.3).

Trong hệ thống DanangTrip, câu hỏi được phân loại bằng bộ kiểm soát ý định, phân tích để trích xuất tham số, truy xuất dữ liệu từ các bảng nghiệp vụ và có thể bổ sung kết quả tìm kiếm ngữ nghĩa bằng embedding trước khi chuyển ngữ cảnh cho mô hình AI.

## 1.9. Đa ngôn ngữ trong website du lịch

Website du lịch thường phục vụ nhiều nhóm người dùng, gồm khách nội địa và khách quốc tế. Vì vậy, hỗ trợ đa ngôn ngữ là một yếu tố quan trọng. DanangTrip sử dụng `next-intl` ở website người dùng và `i18next` ở trang quản trị.

Lợi ích của đa ngôn ngữ:

- Tăng khả năng tiếp cận người dùng quốc tế.
- Tách nội dung hiển thị ra khỏi mã nguồn.
- Dễ bổ sung ngôn ngữ mới.
- Hỗ trợ SEO theo từng ngôn ngữ nếu cấu hình đường dẫn và siêu dữ liệu phù hợp.

## 1.10. Bản đồ số và dữ liệu vị trí

Đối với hệ thống du lịch, dữ liệu vị trí đóng vai trò quan trọng. Người dùng cần biết địa điểm nằm ở đâu, cách di chuyển như thế nào, có những điểm gần đó không và khoảng cách tương đối giữa các địa điểm.

DanangTrip lưu tọa độ `latitude`, `longitude` trong bảng địa điểm và sử dụng Leaflet để hiển thị bản đồ. Các chức năng liên quan gồm:

- Xem vị trí địa điểm trên bản đồ.
- Tìm địa điểm gần người dùng.
- Hiển thị nhiều điểm du lịch trên cùng bản đồ.
- Gợi ý địa điểm lân cận trong trang chi tiết.

## 1.11. Bảo mật trong hệ thống web

Hệ thống du lịch có nhiều dữ liệu nhạy cảm như thông tin tài khoản, số điện thoại, email, đơn đặt tour và thanh toán. Do đó, bảo mật cần được áp dụng ở nhiều lớp:

- Xác thực bằng mã thông báo và mã thông báo làm mới.
- Phân quyền theo vai trò người dùng/quản trị viên.
- Kiểm tra dữ liệu đầu vào bằng cơ chế xác thực yêu cầu của Laravel.
- Giới hạn tần suất gọi các API nhạy cảm như đăng nhập, đăng ký, quên mật khẩu, tải ảnh và thanh toán.
- Không cho người dùng truy cập dữ liệu đơn đặt tour của người khác.
- Kiểm tra chữ ký hoặc dữ liệu xác thực khi nhận callback/IPN thanh toán.
- Giới hạn loại tệp và dung lượng khi tải ảnh.
- Ghi nhật ký lỗi và xử lý phản hồi lỗi thống nhất.
