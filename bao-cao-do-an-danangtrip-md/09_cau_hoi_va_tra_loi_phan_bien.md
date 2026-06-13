# CÂU HỎI VÀ TRẢ LỜI PHẢN BIỆN ĐỒ ÁN TỐT NGHIỆP

Tài liệu này tổng hợp câu hỏi và câu trả lời gợi ý phục vụ cho quá trình phản biện đồ án tốt nghiệp đề tài **"Hệ thống thông tin du lịch thông minh Đà Nẵng - DanangTrip"**. Các câu trả lời được biên soạn theo chuẩn học thuật, bám sát cấu trúc kỹ thuật thực tế của dự án.

---

## 1. Nhóm câu hỏi cơ bản (Dễ)

### Câu 1.1: Vì sao đề tài lựa chọn Next.js cho website người dùng thay vì sử dụng React thuần?
* **Trả lời**:
  * **Tối ưu hóa SEO**: React thuần (Single Page Application - SPA) hoạt động theo cơ chế Client-Side Rendering (CSR), mã nguồn ban đầu gửi về trình duyệt chỉ là một tệp HTML rỗng chứa liên kết JavaScript. Các công cụ tìm kiếm (Googlebot, Bingbot) khó thu thập dữ liệu và lập chỉ mục. Next.js hỗ trợ Server-Side Rendering (SSR) và Static Site Generation (SSG), trả về tệp HTML đầy đủ nội dung ngay khi có yêu cầu, giúp tối ưu hóa SEO cho các trang địa điểm du lịch và tour.
  * **Tốc độ tải trang đầu tiên (FCP)**: Prerendering trên server giúp trình duyệt hiển thị giao diện nhanh hơn mà không cần đợi tải toàn bộ bundle JavaScript lớn, cải thiện trải nghiệm người dùng trên thiết bị di động hoặc mạng yếu.
  * **Tích hợp sẵn các công cụ tối ưu**: Next.js cung cấp các thẻ tối ưu ảnh (`next/image`), tối ưu phông chữ, định tuyến động (App Router) và tải trước tài nguyên (Prefetching).

### Câu 1.2: Laravel trong hệ thống DanangTrip đảm nhiệm những vai trò nào?
* **Trả lời**:
  Laravel đóng vai trò là Server API trung tâm, thực hiện các nhiệm vụ:
  * **Xử lý nghiệp vụ**: Tính toán giá tour, áp dụng khuyến mãi/phiếu giảm giá cá nhân, kiểm tra số lượng chỗ trống, quản lý giỏ hàng, điểm thành viên và thanh toán.
  * **Xác thực và phân quyền**: Cung cấp cơ chế đăng ký, đăng nhập, xác thực bằng mã OTP qua email, phân quyền người dùng thông qua Middleware và mã thông báo JWT.
  * **Quản trị cơ sở dữ liệu**: Định nghĩa lược đồ dữ liệu thông qua migrations, truy vấn dữ liệu qua Eloquent ORM và xử lý giao dịch (Database Transactions).
  * **Tích hợp dịch vụ bên thứ ba**: Tiếp nhận webhook/IPN từ cổng thanh toán SePay, lưu trữ ảnh trên Cloudinary, gửi email qua Brevo, xuất báo cáo Excel và sinh hóa đơn PDF.
  * **Xử lý hội thoại AI**: Phân loại ý định, phân tích truy vấn, kết hợp dữ liệu nghiệp vụ với tìm kiếm ngữ nghĩa bằng embedding và gọi mô hình ngôn ngữ lớn.

### Câu 1.3: Các nhóm người dùng chính của hệ thống là ai?
* **Trả lời**:
  Hệ thống DanangTrip phân chia thành 3 nhóm tác nhân chính:
  * **Khách truy cập (Guest)**: Người dùng chưa đăng nhập. Có quyền xem danh sách và chi tiết địa điểm, tour, bài viết blog, tìm kiếm thông tin và chat cơ bản với chatbot.
  * **Khách hàng (User)**: Người dùng đã đăng nhập. Có đầy đủ quyền của khách truy cập, đồng thời có thể quản lý hồ sơ cá nhân, lưu địa điểm yêu thích, đặt tour, thực hiện thanh toán trực tuyến qua mã QR, xem hóa đơn PDF, gửi đánh giá và nhận thông báo cá nhân hóa.
  * **Quản trị viên (Admin)**: Nhân sự vận hành. Có quyền truy cập hệ thống quản trị (`danangtrip-admin`) để quản lý toàn bộ dữ liệu (đơn đặt tour, tour, địa điểm, người dùng, đánh giá, mã giảm giá, cấu hình) và theo dõi báo cáo thống kê doanh thu.

### Câu 1.4: Hệ thống quản lý những dữ liệu chính nào trong cơ sở dữ liệu?
* **Trả lời**:
  Cơ sở dữ liệu PostgreSQL của hệ thống quản lý các nhóm dữ liệu chính:
  * **Người dùng và xác thực**: Bảng `users`, `sessions`, `refresh_tokens`, `password_reset_tokens`.
  * **Địa điểm du lịch**: Bảng `locations`, `categories`, `subcategories`, `tags`, `amenities`, `location_tags`, `location_amenities`.
  * **Tour và đặt tour**: Bảng `tours`, `tour_categories`, `tour_schedules`, `tour_locations`, `bookings`, `booking_items`, `cart_items`.
  * **Thanh toán & Khuyến mãi**: Bảng `payments` và `promotions`.
  * **Tương tác và chatbot**: Bảng `favorites`, `ratings`, `rating_images`, `rating_helpful_votes`, `chat_messages`, `chat_cache`, `chat_knowledge_base`.
  * **Điểm thành viên**: Bảng `user_point_balances`, `point_rules`, `point_rewards`, `point_transactions`, `user_vouchers`.

### Câu 1.5: Chatbot của DanangTrip hỗ trợ những nhóm câu hỏi nào?
* **Trả lời**:
  Thông qua bộ lọc phân loại ý định (Intent Guard), chatbot hỗ trợ trả lời các nhóm chủ đề:
  * **Thông tin tour**: Tìm kiếm và tư vấn tour phù hợp theo ngân sách, lịch khởi hành, số lượng người.
  * **Thông tin địa điểm**: Tra cứu địa chỉ, giờ hoạt động, đặc trưng nổi bật của danh lam thắng cảnh.
  * **Đơn hàng & Thanh toán**: Hướng dẫn thanh toán, kiểm tra trạng thái đơn đặt tour và chính sách hoàn tiền.
  * **Chính sách chung**: Quy định hủy tour, điều kiện áp dụng khuyến mãi, thông tin liên hệ hỗ trợ.
  * *Các câu hỏi ngoài phạm vi hoặc mang tính công kích sẽ bị chatbot từ chối trả lời một cách lịch sự.*

---

## 2. Nhóm câu hỏi trung bình

### Câu 2.1: Vì sao cần tách website người dùng, trang quản trị và Server API thành các dự án độc lập?
* **Trả lời**:
  Đề tài áp dụng kiến trúc hệ thống phân tách (Decoupled Architecture) nhằm đạt được:
  * **Độc lập công nghệ và mục tiêu**: Next.js hướng tới hiệu năng kết xuất và tối ưu SEO. React/Vite phục vụ ứng dụng quản trị dạng SPA. Laravel Server API tập trung vào xử lý dữ liệu, nghiệp vụ và bảo mật.
  * **Khả năng mở rộng**: Cho phép nhân bản và nâng cấp tài nguyên độc lập cho từng thành phần. Khi lượng truy cập tăng cao, hệ thống có thể mở rộng Next.js Server và API Server mà không cần thay đổi trang quản trị.
  * **Quy trình phát triển độc lập**: Các nhóm phát triển giao diện và API có thể làm việc song song dựa trên tài liệu đặc tả API được thống nhất trước.

### Câu 2.2: JWT được sử dụng như thế nào trong luồng đăng nhập và phân quyền?
* **Trả lời**:
  * **Luồng đăng nhập**: Khi người dùng gửi thông tin xác thực chính xác, Laravel API ký và trả về một cặp mã thông báo: `AccessToken` (thời hạn ngắn, chứa ID người dùng và vai trò) và `RefreshToken` (thời hạn dài, lưu trong cookie bảo mật HttpOnly).
  * **Xác thực yêu cầu**: Trình duyệt đính kèm `AccessToken` vào tiêu đề HTTP `Authorization: Bearer <token>` trên mỗi yêu cầu gửi lên API. Middleware của Laravel giải mã, kiểm tra chữ ký số để xác định danh tính mà không cần truy vấn lại bảng người dùng (Stateless Authentication).
  * **Phân quyền**: Vai trò người dùng (`admin` hoặc `user`) được mã hóa trong payload của JWT. Middleware của Laravel sẽ kiểm tra vai trò này trước khi cho phép yêu cầu tiếp cận các endpoint quản trị `/api/v1/admin/*`.

### Câu 2.3: Khi người dùng đặt tour, hệ thống kiểm soát số chỗ còn lại như thế nào?
* **Trả lời**:
  * **Kiểm tra số chỗ khả dụng**: Hệ thống đối chiếu số lượng khách đăng ký đặt với số lượng chỗ còn trống (`max_participants - booked_count`) trong bảng `tour_schedules`. Nếu số chỗ đăng ký lớn hơn số chỗ trống, hệ thống trả về lỗi `422 Unprocessable Entity`.
  * **Khóa bản ghi (Pessimistic Locking)**: Để ngăn chặn tình trạng đặt vượt số chỗ khả dụng (Overbooking) khi nhiều người dùng cùng đặt một tour tại cùng một thời điểm, hệ thống thực hiện truy vấn khóa dòng: `SELECT ... FOR UPDATE` trên lịch trình khởi hành tương ứng trong Database Transaction. Dòng dữ liệu này bị khóa tạm thời cho đến khi transaction hiện tại cập nhật số lượng chỗ đã đặt (`booked_count`) và commit thành công.

### Câu 2.4: Vì sao cần dùng giao dịch cơ sở dữ liệu (Database Transaction) trong nghiệp vụ đặt tour và thanh toán?
* **Trả lời**:
  Database Transaction bảo đảm tính nhất quán và toàn vẹn dữ liệu (đặc tính Atomicity trong ACID):
  * **Khi đặt tour**: Luồng đặt tour yêu cầu ghi dữ liệu đồng thời vào nhiều bảng: tạo hóa đơn chính (`bookings`), tạo chi tiết hành khách (`booking_items`), trừ số chỗ trống (`tour_schedules`) và cập nhật số lần sử dụng mã giảm giá (`promotions`). Nếu bất kỳ bước nào thất bại, toàn bộ quá trình sẽ được Rollback về trạng thái cũ để tránh dữ liệu mồ côi hoặc sai lệch số chỗ.
  * **Khi thanh toán trực tuyến**: Khi nhận callback IPN từ SePay, hệ thống cập nhật đồng thời trạng thái đơn hàng sang `paid` và tạo bản ghi lịch sử giao dịch trong bảng `payments`. Transaction đảm bảo trạng thái tài chính và trạng thái đơn hàng luôn đồng nhất.

### Câu 2.5: Lớp bộ nhớ đệm trong chatbot giúp cải thiện hệ thống ở điểm nào?
* **Trả lời**:
  * **Giảm độ trễ phản hồi**: Bảng `chat_cache` lưu phản hồi theo khóa được tạo từ ngôn ngữ, nhóm ý định và câu hỏi đã chuẩn hóa. Khi bản ghi còn hiệu lực, hệ thống không phải thực hiện lại toàn bộ quy trình.
  * **Tiết kiệm chi phí**: Giảm số lượng Token đầu vào và đầu ra cần gửi đến nhà cung cấp mô hình AI (do LLM tính phí theo số lượng Token tiêu thụ).
  * **Giảm tải Server**: Hạn chế việc hệ thống liên tục truy xuất dữ liệu và gọi mô hình AI cho cùng một câu hỏi trong thời gian ngắn.

---

## 3. Nhóm câu hỏi chuyên sâu (Khó)

### Câu 3.1: DanangTrip kết hợp truy xuất dữ liệu có cấu trúc và tìm kiếm embedding như thế nào?
* **Trả lời**:
  * **Dữ liệu có cấu trúc**: Thành phần phân tích truy vấn trích xuất điểm đến, vùng, chủ đề, khoảng giá, số người, ngày đi và tiêu chí sắp xếp. `ChatKnowledgeSearchService` dùng các tham số này để lọc tour, lịch khởi hành, địa điểm, bài viết và chính sách.
  * **Tìm kiếm ngữ nghĩa**: Khi được bật bằng cấu hình, `ChatVectorSearchService` tạo embedding cho câu hỏi, lấy các bản ghi có embedding từ `chat_knowledge_base`, tính độ tương đồng cosin ở tầng dịch vụ và chọn các kết quả vượt ngưỡng.
  * **Giới hạn kỹ thuật**: Embedding được lưu trong PostgreSQL nhưng phiên bản hiện tại chưa dùng cơ sở dữ liệu véc-tơ hoặc chỉ mục véc-tơ chuyên dụng. Dữ liệu truy xuất giúp giảm nguy cơ trả lời sai nhưng không thể bảo đảm loại bỏ hoàn toàn hiện tượng mô hình sinh thông tin không chính xác.

### Câu 3.2: Nếu nhà cung cấp AI trả lời sai hoặc không phản hồi, hệ thống xử lý thế nào để không ảnh hưởng đến người dùng?
* **Trả lời**:
  Hệ thống thiết kế cơ chế chịu lỗi nhiều lớp (Graceful Degradation & Failover):
  * **Chuyển đổi dự phòng AI**: `ChatAiProviderService` duyệt nhà cung cấp và khóa truy cập theo thứ tự cấu hình. Khi gặp lỗi kết nối, quá thời gian chờ, vượt giới hạn tần suất hoặc khóa không hợp lệ, hệ thống thử lựa chọn tiếp theo.
  * **Phản hồi dự phòng**: Nếu không thể nhận phản hồi hợp lệ, `ChatService` sử dụng câu trả lời dự phòng hoặc thông báo ngoài phạm vi thay vì để yêu cầu thất bại không kiểm soát.

### Câu 3.2a: Chatbot hiện tại có nhớ ngữ cảnh nhiều lượt hay không?
* **Trả lời**:
  Chưa hoàn chỉnh. Server API có lưu `session_id`, câu hỏi và câu trả lời trong `chat_messages`, nhưng chưa truy vấn các tin nhắn trước để đưa vào prompt của lượt tiếp theo. Website hiện giữ tin nhắn bằng Zustand trong bộ nhớ của trang và chưa gửi `session_id` đến API. Vì vậy chatbot xử lý tốt từng câu hỏi độc lập nhưng có thể không hiểu câu nối tiếp như "còn tour nào rẻ hơn?" nếu câu đó không chứa đủ thực thể.

### Câu 3.2b: Vì sao gọi kiến trúc hiện tại là Hybrid RAG quy mô đồ án?
* **Trả lời**:
  Hệ thống kết hợp lọc dữ liệu nghiệp vụ trực tiếp bằng SQL với tìm kiếm embedding tùy chọn, sau đó chỉ gửi một số kết quả liên quan vào mô hình AI. Cách này mạnh hơn chatbot chỉ gọi LLM vì giá, lịch và trạng thái được lấy từ dữ liệu hệ thống. Tuy nhiên độ tương đồng véc-tơ vẫn được tính trong PHP trên tối đa một tập ứng viên cấu hình, chưa có chỉ mục `pgvector`, chưa có trích dẫn nguồn bắt buộc và chưa có bộ nhớ hội thoại nhiều lượt; do đó chưa nên mô tả là nền tảng RAG quy mô lớn.

### Câu 3.3: Làm thế nào để bảo đảm người dùng không xem được đơn đặt tour của người khác?
* **Trả lời**:
  Hệ thống thực hiện kiểm soát truy cập và bảo mật đa lớp:
  * **Xác thực và kiểm tra quyền sở hữu tại API**: Điểm cuối `/api/v1/user/bookings/{id}` yêu cầu JWT. `BookingService` so sánh người dùng hiện tại với `user_id` của đơn; nếu không trùng, API trả về `403 Forbidden`.
  * **Tách biệt phân hệ quản trị**: Endpoint lấy thông tin quản trị `/api/v1/admin/bookings/{id}` được bảo vệ riêng biệt bởi Middleware kiểm tra vai trò người dùng, chỉ tài khoản có vai trò `admin` mới được cấp quyền truy cập.
  * **Mã đơn không thay thế kiểm tra quyền**: Hệ thống có `booking_code` ngẫu nhiên để tra cứu thuận tiện, nhưng khóa chính vẫn là số tự tăng. Bảo vệ chính vẫn là xác thực và kiểm tra `user_id`; không được xem mã đơn là biện pháp ngăn IDOR độc lập.

### Câu 3.4: Nếu IPN thanh toán từ SePay bị giả mạo hoặc gửi lặp lại, hệ thống kiểm tra và chống xử lý trùng như thế nào?
* **Trả lời**:
  * **Xác thực IPN theo cấu hình**: Khi `SEPAY_VERIFY_IPN_SIGNATURE` được bật, hệ thống chấp nhận mã bí mật trong tiêu đề Bearer/token hoặc kiểm tra HMAC-SHA256 trên nội dung thô. Nếu cấu hình này tắt, bước xác thực chữ ký được bỏ qua; vì vậy môi trường thật bắt buộc phải bật và cấu hình khóa bí mật.
  * **Kiểm tra dữ liệu nghiệp vụ**: Hệ thống trích xuất mã đơn từ nội dung chuyển khoản, đối chiếu số tiền nhận được với số tiền của đơn và từ chối dữ liệu không hợp lệ.
  * **Chống xử lý lặp theo trạng thái**: Nếu đơn đã có trạng thái thanh toán thành công, hệ thống trả kết quả đã xử lý mà không cộng điểm hoặc cập nhật lại. Việc cập nhật thanh toán được thực hiện trong giao dịch và khóa bản ghi thanh toán chờ xử lý.

### Câu 3.5: Nếu dữ liệu tour và địa điểm tăng lớn, cần tối ưu cơ sở dữ liệu, API và giao diện như thế nào?
* **Trả lời**:
  Hệ thống thực hiện tối ưu hóa 3 tầng:
  * **Tầng Cơ sở dữ liệu (PostgreSQL)**:
    * Đánh chỉ mục B-Tree cho các trường tìm kiếm và sắp xếp thường xuyên (`price`, `starts_at`, `status`).
    * Có thể bổ sung chỉ mục `GIN` kết hợp `tsvector` cho tìm kiếm toàn văn khi khối lượng dữ liệu tăng; đây là hướng tối ưu, không phải chức năng đã được chứng minh trong phiên bản hiện tại.
    * Phân vùng dữ liệu (Partitioning) đối với các bảng ghi nhật ký có dung lượng lớn như `payments` hoặc `bookings`.
  * **Tầng API (Laravel)**:
    * Áp dụng phân trang (`paginate()` hoặc `cursorPaginate()`) cho các danh sách trả về, tránh truy xuất toàn bộ dữ liệu.
    * Sử dụng cơ chế nạp trước (Eager Loading) thông qua `with([...])` của Eloquent để giải quyết triệt để vấn đề truy vấn thừa $N+1$.
    * Lưu trữ bộ nhớ đệm Redis đối với các dữ liệu tĩnh ít biến động như danh sách danh mục, cấu hình hệ thống.
  * **Tầng Giao diện (Next.js/React)**:
    * Áp dụng danh sách ảo (Virtual List) đối với danh sách hiển thị dài.
    * Tải ảnh lười (Lazy Loading) thông qua bộ tối ưu hóa ảnh của Next.js giúp giảm dung lượng mạng tải trang.
