# KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

## 1. Kết quả đạt được

Sau quá trình phân tích, thiết kế và triển khai, đề tài **"Xây dựng website du lịch Đà Nẵng"** đã đạt được các kết quả chính:

- Xây dựng website người dùng bằng Next.js phục vụ tra cứu địa điểm, tour, blog, tìm kiếm, bản đồ, đặt tour, thanh toán và quản lý tài khoản.
- Xây dựng trang quản trị bằng React/Vite phục vụ quản lý toàn bộ dữ liệu vận hành như địa điểm, tour, lịch khởi hành, đơn đặt tour, thanh toán, người dùng, đánh giá, blog, khuyến mãi, thông báo và báo cáo.
- Xây dựng Server API bằng Laravel với cấu trúc rõ ràng, có xác thực JWT, phân quyền quản trị viên, kiểm tra dữ liệu và phân tách theo mẫu controller-service-repository.
- Thiết kế cơ sở dữ liệu đáp ứng các nghiệp vụ chính của hệ thống du lịch: địa điểm, tour, lịch khởi hành, đơn đặt tour, thanh toán, đánh giá, lượt đánh giá hữu ích, điểm thành viên, phiếu giảm giá cá nhân, yêu thích, nội dung và chatbot.
- Tích hợp các nghiệp vụ như thanh toán SePay/VietQR, tải ảnh lên Cloudinary, xuất báo cáo Excel, sinh hóa đơn PDF, gửi email và chatbot tư vấn thông minh (ứng dụng định tuyến NLU lai, tối ưu hóa tìm kiếm SQL LIKE và đồng bộ ngữ cảnh RAG Context Alignment để đảm bảo câu trả lời luôn chính xác và đồng nhất với thẻ gợi ý).
- Triển khai áp dụng khuyến mãi và phiếu giảm giá cá nhân trong luồng đặt tour; cộng điểm theo nguồn nghiệp vụ, đổi điểm lấy phần thưởng và quản lý lịch sử điểm.
- Triển khai thông báo trạng thái đơn/thanh toán, thông báo điểm và tác vụ nhắc lịch khởi hành; hỗ trợ quản trị viên xác nhận thanh toán chuyển khoản thủ công.
- Có nền tảng kiểm thử bằng PHPUnit, Playwright, Vitest và các script kiểm tra đóng gói, kiểu dữ liệu, quy tắc mã nguồn.

## 2. Những vấn đề còn tồn tại

Do giới hạn về thời gian và phạm vi đồ án, hệ thống vẫn còn một số điểm cần tiếp tục hoàn thiện:

- Chưa có dữ liệu vận hành thực tế đủ lớn để đánh giá sâu hiệu quả gợi ý cá nhân hóa.
- Chất lượng phản hồi của chatbot phụ thuộc vào độ đầy đủ của dữ liệu trong cơ sở tri thức, độ chính xác của bước phân tích truy vấn và khả năng sẵn sàng của các nhà cung cấp AI trong cơ chế chuyển đổi dự phòng.
- Chatbot mới ghi nhận `session_id` và lịch sử để theo dõi; chưa đưa 5-10 tin nhắn gần nhất vào prompt nên chưa hiểu đầy đủ các câu nối tiếp như "còn cái nào rẻ hơn?".
- Tìm kiếm embedding đang tính độ tương đồng trong PHP trên một tập ứng viên giới hạn, chưa sử dụng `pgvector` hoặc chỉ mục véc-tơ chuyên dụng.
- Mã nguồn hiện chỉ áp dụng rate limit theo phút tại endpoint chatbot; chưa có cơ chế giới hạn số lượt hỏi trong ngày hoặc phân chia hạn mức theo vai trò người dùng.
- Biến `CHATBOT_CACHE_DRIVER` đã được khai báo nhưng luồng hiện tại truy cập trực tiếp bảng `chat_cache`; thay đổi biến này chưa làm hệ thống chuyển sang Redis hoặc driver khác.
- Cache được xóa khi tour, địa điểm, bài viết hoặc cài đặt thay đổi, nhưng chưa có observer tương ứng cho lịch khởi hành. Thay đổi lịch có thể làm phản hồi cache cũ tồn tại đến khi hết TTL hoặc được xóa bởi sự kiện khác.
- Bộ kiểm thử chatbot hiện mới bao phủ một số trường hợp Intent Guard và Query Understanding, chưa bao phủ cache, AI failover, Hybrid Retrieval, chống prompt injection và hội thoại nhiều lượt.
- Chưa triển khai đầy đủ hệ thống gợi ý độc lập trong môi trường vận hành thực tế.
- Chưa tích hợp nhiều cổng thanh toán hoặc nhiều nhà cung cấp tour bên ngoài.
- Cần bổ sung thêm kiểm thử tự động cho toàn bộ luồng đầu cuối như đăng ký, đặt tour, thanh toán, quản trị đơn đặt tour và quản trị nội dung.
- Cần mở rộng kiểm thử tích hợp cho luồng đổi điểm - cấp phiếu - áp dụng phiếu và tác vụ nhắc lịch khởi hành.
- Cần tối ưu thêm SEO, hiệu năng, khả năng truy cập và trải nghiệm trên thiết bị di động.

## 3. Hướng phát triển

Trong tương lai, hệ thống có thể được mở rộng theo các hướng:

- Phát triển hệ thống gợi ý cá nhân hóa dựa trên lịch sử tìm kiếm, vị trí, ngân sách, số người, thời gian đi và hành vi tương tác.
- Xây dựng tính năng lập lịch trình du lịch tự động theo số ngày, ngân sách và sở thích.
- Tích hợp nhiều cổng thanh toán và ví điện tử.
- Phát triển ứng dụng di động cho khách du lịch.
- Tích hợp hệ thống đối tác để đồng bộ tour, khách sạn, phương tiện và vé tham quan.
- Bổ sung hệ thống đánh giá chống spam, kiểm duyệt tự động và phân tích cảm xúc.
- Bổ sung giao diện quản trị quy tắc điểm/phần thưởng, cơ chế thu hồi hoặc hoàn điểm khi đơn đặt tour bị hoàn tiền và báo cáo hiệu quả chương trình thành viên.
- Nâng cấp chatbot theo hướng RAG hoàn chỉnh hơn, có khả năng trích dẫn nguồn dữ liệu, ghi nhận độ tin cậy của câu trả lời và tư vấn theo ngữ cảnh cá nhân.
- Bổ sung bộ nhớ hội thoại ngắn hạn theo `session_id`, tool calling nội bộ, kiểm tra đầu ra chống bịa dữ liệu, streaming response và trang quản trị thống kê câu hỏi/cache/token/provider.
- Chuyển tìm kiếm ngữ nghĩa sang `pgvector` hoặc dịch vụ véc-tơ chuyên dụng khi cơ sở tri thức tăng lớn; đồng thời bổ sung kiểm thử tự động cho intent, typo, ranking, cache, failover và prompt injection.
- Triển khai giám sát, ghi nhật ký tập trung và cảnh báo lỗi trong môi trường vận hành thực tế.

## 4. Kết luận chung

Đề tài DanangTrip đã giúp sinh viên vận dụng tổng hợp kiến thức về phát triển phần mềm, thiết kế cơ sở dữ liệu, xây dựng giao diện người dùng, xây dựng Server API, tích hợp dịch vụ và kiểm thử. Sản phẩm tạo ra đáp ứng các nghiệp vụ cơ bản của hệ thống du lịch trực tuyến và có thể tiếp tục mở rộng theo hướng cá nhân hóa, tư vấn thông minh và tích hợp nhiều dịch vụ du lịch hơn.
