# CHƯƠNG 1. CƠ SỞ LÝ THUYẾT

## 1.1. Tổng quan về kiến trúc client-server

Kiến trúc client-server là mô hình phổ biến trong phát triển ứng dụng web. Trong mô hình này, phía client chịu trách nhiệm hiển thị giao diện và tương tác với người dùng, trong khi phía server xử lý nghiệp vụ, truy xuất dữ liệu, xác thực, phân quyền và cung cấp API.

Trong hệ thống DanangTrip, kiến trúc client-server được thể hiện qua ba thành phần:

- `danangtrip-web`: website người dùng, gọi API để hiển thị dữ liệu địa điểm, tour, đơn đặt tour, thanh toán và hồ sơ.
- `danangtrip-admin`: giao diện quản trị, gọi API quản trị để quản lý dữ liệu và báo cáo.
- `danangtrip-api`: API phía server được xây dựng bằng Laravel, cung cấp REST API cho website người dùng và trang quản trị.

Mô hình này giúp tách biệt trách nhiệm giữa giao diện và nghiệp vụ, thuận tiện cho bảo trì, mở rộng và triển khai độc lập.

## 1.2. Tổng quan về Next.js và React

React là thư viện JavaScript dùng để xây dựng giao diện người dùng theo hướng thành phần (component). Next.js là khung phát triển (framework) xây dựng trên React, hỗ trợ định tuyến theo cấu trúc tệp, kết xuất phía server, sinh trang tĩnh, tối ưu SEO và triển khai linh hoạt.

Trong DanangTrip, Next.js được dùng cho website người dùng vì phù hợp với các trang cần SEO như trang chủ, danh sách địa điểm, chi tiết địa điểm, danh sách tour, chi tiết tour và blog. Dự án còn sử dụng:

- TypeScript để tăng độ an toàn kiểu dữ liệu.
- React Query để quản lý trạng thái dữ liệu lấy từ API.
- Zustand để quản lý trạng thái cục bộ như xác thực, giỏ hàng hoặc trạng thái ứng dụng.
- next-intl để hỗ trợ đa ngôn ngữ.
- Leaflet để hiển thị bản đồ và vị trí du lịch.

## 1.3. Tổng quan về React/Vite cho trang quản trị

Vite là công cụ đóng gói giao diện có tốc độ phát triển nhanh, phù hợp với ứng dụng quản trị dạng ứng dụng một trang. React Router được dùng để quản lý đường dẫn nội bộ, React Query để đồng bộ trạng thái dữ liệu từ server, React Hook Form và Yup/Zod để xử lý biểu mẫu và kiểm tra dữ liệu.

Trang quản trị DanangTrip sử dụng React/Vite để xây dựng các phân hệ bảng điều khiển, tour, lịch khởi hành, đơn đặt tour, thanh toán, địa điểm, bài viết, người dùng, đánh giá, liên hệ, thông báo, khuyến mãi và cấu hình. Đây là nhóm màn hình có tính thao tác lặp lại cao, cần bảng dữ liệu, bộ lọc, biểu đồ, biểu mẫu thêm/sửa và kiểm soát trạng thái.

## 1.4. Tổng quan về Laravel REST API

Laravel là khung phát triển PHP hỗ trợ phát triển ứng dụng web và API với hệ sinh thái đầy đủ: định tuyến, lớp trung gian (middleware), ORM, migration, hàng đợi, kiểm tra dữ liệu, bộ nhớ đệm, sự kiện, tác vụ nền và kiểm thử. REST API là phong cách thiết kế API sử dụng các phương thức HTTP như GET, POST, PUT, PATCH và DELETE để thao tác tài nguyên.

API phía server của DanangTrip sử dụng Laravel 12 và tổ chức mã nguồn theo hướng:

- Controller tiếp nhận yêu cầu và trả phản hồi.
- Service xử lý nghiệp vụ.
- Repository truy vấn và thao tác dữ liệu.
- Model đại diện bảng dữ liệu.
- Cơ chế kiểm tra yêu cầu đầu vào giúp xác thực dữ liệu trước khi xử lý nghiệp vụ.
- Middleware xử lý xác thực, phân quyền và throttle.

Cách tổ chức này giúp nghiệp vụ được tách khỏi controller, dễ kiểm thử và dễ mở rộng.

## 1.5. Xác thực JWT và phân quyền

JWT là chuẩn mã thông báo dùng để truyền thông tin xác thực giữa client và server. Sau khi đăng nhập thành công, server cấp mã thông báo truy cập (access token) và mã thông báo làm mới (refresh token). Client gửi mã thông báo trong các yêu cầu cần bảo vệ. Server kiểm tra mã thông báo để xác định người dùng và quyền truy cập.

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
| 3 | Nhóm tour và đặt tour | `tours`, `tour_categories`, `tour_schedules`, `tour_locations`, `bookings`, `booking_items`, `cart_items` | Lưu trữ thông tin tour, danh mục tour, lịch khởi hành, chỗ trống khả dụng, giỏ hàng tạm thời, quản lý chi tiết đơn đặt tour (booking) và danh sách hành khách đi kèm. |
| 4 | Nhóm thanh toán | `payments` | Lưu trữ lịch sử giao dịch và trạng thái thanh toán của đơn đặt tour (qua cổng tự động Sepay/PayOS hoặc đối soát chuyển khoản ngân hàng thủ công). |
| 5 | Nhóm nội dung | `blog_posts`, `blog_categories`, `blog_post_categories`, `landing_pages` | Quản lý các bài viết cẩm nang du lịch Đà Nẵng, danh mục bài viết, liên kết danh mục và nội dung các trang đích (landing pages) phục vụ SEO. |
| 6 | Nhóm tương tác | `favorites`, `ratings`, `rating_images`, `search_logs`, `notifications`, `contacts` | Ghi nhận danh sách địa điểm/tour yêu thích của khách hàng, lưu trữ đánh giá/phản hồi kèm hình ảnh của người dùng, nhật ký tìm kiếm, thông báo hệ thống và liên hệ. |
| 7 | Nhóm cấu hình & AI Chatbot | `settings`, `promotions`, `chat_messages`, `chat_cache`, `chat_knowledge_base` | Quản lý cấu hình chung hệ thống, thông tin mã giảm giá, lưu lịch sử hội thoại của người dùng với AI, bộ nhớ đệm câu trả lời và dữ liệu cơ sở tri thức SQL RAG. |

## 1.7. Thanh toán trực tuyến và IPN

Thanh toán trực tuyến trong hệ thống đặt tour cần đảm bảo các yếu tố: tạo giao dịch, gắn giao dịch với đơn đặt tour, xác nhận trạng thái, chống xử lý trùng, cập nhật trạng thái đơn đặt tour sau thanh toán và lưu lịch sử giao dịch.

DanangTrip tích hợp SePay/VietQR. Khi người dùng tạo thanh toán, hệ thống sinh thông tin giao dịch và nội dung chuyển khoản. Khi cổng thanh toán gửi IPN/callback, API phía server kiểm tra dữ liệu, xác thực giao dịch, cập nhật bảng `payments` và trạng thái `bookings`.

## 1.8. Chatbot, SQL RAG và gợi ý du lịch

Chatbot du lịch cần trả lời dựa trên dữ liệu thật của hệ thống như tour, địa điểm, bài viết và chính sách. Nếu chatbot chỉ dựa vào kiến thức tổng quát của mô hình AI, câu trả lời có thể sai với dữ liệu hiện có trong hệ thống. Vì vậy, DanangTrip tổ chức chatbot theo hướng truy xuất dữ liệu nội bộ trước khi sinh phản hồi.

Các thành phần chính trong quy trình xử lý của chatbot gồm:

- **Intent Guard**: kiểm tra câu hỏi có thuộc phạm vi du lịch, tour, địa điểm, đặt tour, chính sách hoặc hỗ trợ hệ thống hay không. Thành phần này giúp hạn chế câu hỏi ngoài phạm vi.
- **Query Understanding**: phân tích câu hỏi để trích xuất thông tin như điểm đến, khoảng giá, số người, ngày đi, thời lượng hoặc loại nhu cầu.
- **SQL RAG**: truy xuất dữ liệu từ các bảng nghiệp vụ như `tours`, `tour_schedules`, `locations`, `blog_posts`, `settings` hoặc dữ liệu chính sách để tạo ngữ cảnh trả lời.
- **Cache Layer**: lưu phản hồi hoặc dữ liệu trung gian nhằm giảm độ trễ và giảm số lần gọi nhà cung cấp AI đối với các câu hỏi lặp lại.
- **AI Failover**: chuyển sang nhà cung cấp hoặc khóa khác khi nhà cung cấp hiện tại lỗi, hết hạn mức hoặc tạm thời không phản hồi.

DanangTrip có nhóm lớp dịch vụ xử lý chatbot gồm:

- `ChatService`: điều phối luồng gửi tin nhắn và tạo phản hồi.
- `ChatIntentGuardService`: phân loại ý định và giới hạn phạm vi câu hỏi.
- `ChatQueryUnderstandingService`: trích xuất điểm đến, giá, số người, ngày, thời lượng.
- `ChatKnowledgeSyncService`: đồng bộ dữ liệu tour, địa điểm, blog và chính sách vào cơ sở tri thức.
- `ChatKnowledgeSearchService`: tìm kiếm dữ liệu phù hợp từ tour, địa điểm, blog, chính sách và cơ sở tri thức.
- `ChatEmbeddingService`: tạo embedding thông qua nhà cung cấp như Gemini hoặc OpenAI khi cần tìm kiếm ngữ nghĩa.
- `ChatAiProviderService`: điều phối nhà cung cấp AI và xử lý chuyển đổi dự phòng khi gọi mô hình.

Mối quan hệ và luồng tương tác giữa các lớp dịch vụ xử lý chatbot này được biểu diễn trực quan thông qua sơ đồ cấu trúc các lớp dịch vụ chatbot (mã nguồn sơ đồ Draw.io được cung cấp tại Phụ lục - mục 7.3).

Trong hệ thống DanangTrip, chatbot áp dụng hướng tiếp cận RAG ở mức truy xuất dữ liệu nội bộ: câu hỏi được phân loại bằng Intent Guard, phân tích bằng Query Understanding, truy xuất dữ liệu từ các bảng nghiệp vụ, sau đó chuyển ngữ cảnh cho mô hình AI để sinh phản hồi.

## 1.9. Kiểm thử phần mềm

Kiểm thử giúp đảm bảo hệ thống hoạt động đúng và giảm lỗi khi thay đổi. Dự án DanangTrip có các nhóm kiểm thử:

- Kiểm thử đơn vị và kiểm thử chức năng phía server bằng PHPUnit cho API, bảo mật, cấu hình, khuyến mãi, trang chủ, đánh giá và đặt tour.
- Kiểm thử giao diện bằng Vitest và Playwright cho luồng đặt tour, tra cứu đơn đặt tour theo mã, đổi mật khẩu và kiểm thử giao diện.
- Kiểm tra đóng gói, quy tắc mã nguồn và kiểu dữ liệu bằng các script trong `package.json` và `composer.json`.

## 1.10. Tổng quan về React Query và quản lý trạng thái dữ liệu server

Trong ứng dụng web hiện đại, dữ liệu từ server thường có các đặc điểm: bất đồng bộ, cần bộ nhớ đệm, có trạng thái đang tải hoặc lỗi, cần tải lại khi dữ liệu thay đổi và cần đồng bộ giữa nhiều thành phần giao diện. React Query là thư viện giúp quản lý trạng thái dữ liệu server hiệu quả hơn so với việc tự quản lý bằng trạng thái cục bộ.

Trong DanangTrip, React Query phù hợp cho các luồng:

- Lấy danh sách địa điểm, tour, blog, khuyến mãi, thông báo.
- Lấy chi tiết địa điểm, tour, đơn đặt tour và thanh toán.
- Lưu dữ liệu vào bộ nhớ đệm để giảm số lần gọi API lặp lại.
- Tự động cập nhật lại dữ liệu sau khi người dùng tạo đơn đặt tour, đánh giá hoặc cập nhật hồ sơ.
- Quản lý thống nhất các trạng thái đang tải, lỗi và thành công trên giao diện.

Việc dùng React Query giúp giao diện phản hồi tốt hơn và giảm độ phức tạp khi xử lý dữ liệu bất đồng bộ.

## 1.11. Tổng quan về quản lý trạng thái phía client

Bên cạnh dữ liệu lấy từ server, giao diện còn cần quản lý các trạng thái cục bộ như thông tin đăng nhập, giỏ hàng, ngôn ngữ, cấu hình giao diện, hộp thoại và dữ liệu tạm. DanangTrip sử dụng Zustand cho một số trạng thái cục bộ vì thư viện này gọn nhẹ, dễ dùng và không cần nhiều mã lặp.

Ví dụ các trạng thái phù hợp lưu ở phía client:

- Mã thông báo truy cập hoặc trạng thái đăng nhập.
- Thông tin người dùng hiện tại.
- Giỏ hàng cục bộ trước khi đồng bộ lên server.
- Cấu hình giao diện hoặc trạng thái ứng dụng.

## 1.12. Đa ngôn ngữ trong website du lịch

Website du lịch thường phục vụ nhiều nhóm người dùng, gồm khách nội địa và khách quốc tế. Vì vậy, hỗ trợ đa ngôn ngữ là một yếu tố quan trọng. DanangTrip sử dụng `next-intl` ở website người dùng và `i18next` ở trang quản trị.

Lợi ích của đa ngôn ngữ:

- Tăng khả năng tiếp cận người dùng quốc tế.
- Tách nội dung hiển thị ra khỏi mã nguồn.
- Dễ bổ sung ngôn ngữ mới.
- Hỗ trợ SEO theo từng ngôn ngữ nếu cấu hình đường dẫn và siêu dữ liệu phù hợp.

## 1.13. Bản đồ số và dữ liệu vị trí

Đối với hệ thống du lịch, dữ liệu vị trí đóng vai trò quan trọng. Người dùng cần biết địa điểm nằm ở đâu, cách di chuyển như thế nào, có những điểm gần đó không và khoảng cách tương đối giữa các địa điểm.

DanangTrip lưu tọa độ `latitude`, `longitude` trong bảng địa điểm và sử dụng Leaflet để hiển thị bản đồ. Các chức năng liên quan gồm:

- Xem vị trí địa điểm trên bản đồ.
- Tìm địa điểm gần người dùng.
- Hiển thị nhiều điểm du lịch trên cùng bản đồ.
- Gợi ý địa điểm lân cận trong trang chi tiết.

## 1.14. Tối ưu tìm kiếm trong hệ thống du lịch

Tìm kiếm là chức năng quan trọng vì dữ liệu du lịch có nhiều loại: tên địa điểm, địa chỉ, mô tả, danh mục, tour, bài viết, từ khóa phổ biến và xu hướng. API phía server của DanangTrip sử dụng chỉ mục tìm kiếm toàn văn ở các bảng như `locations` và `tours` để hỗ trợ tìm kiếm theo nội dung.

Các yếu tố cần quan tâm khi thiết kế tìm kiếm:

- Chuẩn hóa từ khóa đầu vào.
- Hỗ trợ tìm theo tên, mô tả, địa chỉ, danh mục.
- Phân trang và sắp xếp kết quả.
- Ghi nhận nhật ký tìm kiếm để phân tích xu hướng.
- Gợi ý từ khóa khi người dùng nhập.
- Kết hợp hành vi người dùng để đề xuất nội dung phù hợp.

## 1.15. Bảo mật trong hệ thống web

Hệ thống du lịch có nhiều dữ liệu nhạy cảm như thông tin tài khoản, số điện thoại, email, đơn đặt tour và thanh toán. Do đó, bảo mật cần được áp dụng ở nhiều lớp:

- Xác thực bằng mã thông báo và mã thông báo làm mới.
- Phân quyền theo vai trò người dùng/quản trị viên.
- Kiểm tra dữ liệu đầu vào bằng cơ chế xác thực yêu cầu của Laravel.
- Giới hạn tần suất gọi các API nhạy cảm như đăng nhập, đăng ký, quên mật khẩu, tải ảnh và thanh toán.
- Không cho người dùng truy cập dữ liệu đơn đặt tour của người khác.
- Kiểm tra chữ ký hoặc dữ liệu xác thực khi nhận callback/IPN thanh toán.
- Giới hạn loại tệp và dung lượng khi tải ảnh.
- Ghi nhật ký lỗi và xử lý phản hồi lỗi thống nhất.

## 1.16. Cơ sở lý thuyết về báo cáo và thống kê

Trang quản trị cần cung cấp dữ liệu tổng quan để hỗ trợ ra quyết định. Các chỉ số thống kê quan trọng trong hệ thống DanangTrip gồm:

- Số lượng người dùng.
- Số lượng đơn đặt tour theo trạng thái.
- Doanh thu theo thời gian.
- Tour được đặt nhiều.
- Địa điểm được xem/yêu thích nhiều.
- Đánh giá mới và đánh giá cần duyệt.
- Xu hướng tìm kiếm.

Dữ liệu thống kê được trực quan hóa bằng biểu đồ trong trang quản trị, đồng thời có thể xuất ra tệp Excel để phục vụ báo cáo.

## 1.17. Cơ chế bộ nhớ đệm và chuyển đổi dự phòng trong hệ thống AI

Trong DanangTrip, thành phần AI phụ thuộc vào nhà cung cấp mô hình bên ngoài. Vì vậy, hệ thống cần xử lý các trường hợp lỗi mạng, vượt giới hạn tần suất, hết hạn mức hoặc phản hồi quá thời gian chờ thông qua cơ chế chuyển đổi dự phòng.

Cache Layer trong chatbot được sử dụng để lưu dữ liệu truy xuất hoặc phản hồi đối với các truy vấn lặp lại, nhằm giảm thời gian xử lý và hạn chế số lần gọi đến nhà cung cấp AI. Cache Layer có thể được sử dụng ở hai mức:

- Lưu kết quả truy vấn hoặc tri thức liên quan đến câu hỏi vào bộ nhớ đệm.
- Lưu phản hồi chatbot đối với câu hỏi phổ biến hoặc câu hỏi có nội dung tương tự vào bộ nhớ đệm.

Trong hệ thống DanangTrip, AI Failover được hiểu là cơ chế chuyển sang nhà cung cấp hoặc khóa API dự phòng khi nhà cung cấp hiện tại trả lỗi, vượt giới hạn tần suất, quá thời gian chờ hoặc phản hồi không hợp lệ.

Đối với DanangTrip, hai cơ chế này giúp chatbot giảm phụ thuộc vào một nhà cung cấp duy nhất và cải thiện trải nghiệm người dùng trong các tình huống lỗi tạm thời.
