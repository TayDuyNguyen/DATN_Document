# KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

## 1. Kết quả đạt được

Sau quá trình phân tích, thiết kế và triển khai, đề tài **"Xây dựng website du lịch Đà Nẵng"** đã đạt được các kết quả chính:

- Xây dựng website người dùng bằng Next.js phục vụ tra cứu địa điểm, tour, blog, tìm kiếm, bản đồ, đặt tour, thanh toán và quản lý tài khoản.
- Xây dựng trang quản trị bằng React/Vite phục vụ quản lý toàn bộ dữ liệu vận hành như địa điểm, tour, lịch khởi hành, đơn đặt tour, thanh toán, người dùng, đánh giá, blog, khuyến mãi, thông báo và báo cáo.
- Xây dựng API phía máy chủ bằng Laravel với cấu trúc rõ ràng, có xác thực JWT, phân quyền quản trị viên, kiểm tra dữ liệu và phân tách theo mẫu controller-service-repository.
- Thiết kế cơ sở dữ liệu đáp ứng các nghiệp vụ chính của hệ thống du lịch: địa điểm, tour, lịch khởi hành, đơn đặt tour, thanh toán, đánh giá, yêu thích, nội dung và chatbot.
- Tích hợp các nghiệp vụ như thanh toán SePay/VietQR, tải ảnh lên Cloudinary, xuất báo cáo Excel, sinh hóa đơn PDF, gửi email và chatbot tư vấn dựa trên dữ liệu nội bộ.
- Có nền tảng kiểm thử bằng PHPUnit, Playwright, Vitest và các script kiểm tra đóng gói, kiểu dữ liệu, quy tắc mã nguồn.

## 2. Những vấn đề còn tồn tại

Do giới hạn về thời gian và phạm vi đồ án, hệ thống vẫn còn một số điểm cần tiếp tục hoàn thiện:

- Chưa có dữ liệu vận hành thực tế đủ lớn để đánh giá sâu hiệu quả gợi ý cá nhân hóa.
- Chất lượng phản hồi của chatbot phụ thuộc vào độ đầy đủ của dữ liệu trong cơ sở tri thức, độ chính xác của bước phân tích truy vấn và khả năng sẵn sàng của các nhà cung cấp AI trong cơ chế chuyển đổi dự phòng.
- Chưa triển khai đầy đủ hệ thống gợi ý độc lập trong môi trường vận hành thực tế.
- Chưa tích hợp nhiều cổng thanh toán hoặc nhiều nhà cung cấp tour bên ngoài.
- Cần bổ sung thêm kiểm thử tự động cho toàn bộ luồng đầu cuối như đăng ký, đặt tour, thanh toán, quản trị đơn đặt tour và quản trị nội dung.
- Cần tối ưu thêm SEO, hiệu năng, khả năng truy cập và trải nghiệm trên thiết bị di động.

## 3. Hướng phát triển

Trong tương lai, hệ thống có thể được mở rộng theo các hướng:

- Phát triển hệ thống gợi ý cá nhân hóa dựa trên lịch sử tìm kiếm, vị trí, ngân sách, số người, thời gian đi và hành vi tương tác.
- Xây dựng tính năng lập lịch trình du lịch tự động theo số ngày, ngân sách và sở thích.
- Tích hợp nhiều cổng thanh toán và ví điện tử.
- Phát triển ứng dụng di động cho khách du lịch.
- Tích hợp hệ thống đối tác để đồng bộ tour, khách sạn, phương tiện và vé tham quan.
- Bổ sung hệ thống đánh giá chống spam, kiểm duyệt tự động và phân tích cảm xúc.
- Nâng cấp chatbot theo hướng RAG hoàn chỉnh hơn, có khả năng trích dẫn nguồn dữ liệu, ghi nhận độ tin cậy của câu trả lời và tư vấn theo ngữ cảnh cá nhân.
- Triển khai giám sát, ghi nhật ký tập trung và cảnh báo lỗi trong môi trường vận hành thực tế.

## 4. Kết luận chung

Đề tài DanangTrip đã giúp sinh viên vận dụng tổng hợp kiến thức về phát triển phần mềm, thiết kế cơ sở dữ liệu, xây dựng giao diện người dùng, xây dựng API phía máy chủ, tích hợp dịch vụ và kiểm thử. Sản phẩm tạo ra đáp ứng các nghiệp vụ cơ bản của hệ thống du lịch trực tuyến và có thể tiếp tục mở rộng theo hướng cá nhân hóa, tư vấn thông minh và tích hợp nhiều dịch vụ du lịch hơn.
