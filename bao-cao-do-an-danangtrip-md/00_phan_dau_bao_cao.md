# PHẦN ĐẦU BÁO CÁO

## Thông tin đề tài

- Tên đề tài: **Xây dựng website du lịch Đà Nẵng**
- Tên hệ thống: **DanangTrip**
- Sinh viên thực hiện: Nguyễn Duy Tây
- Số thẻ sinh viên: 102220083
- Lớp: 22T-DT1
- Khoa: Công nghệ thông tin
- Trường: Trường Đại học Bách khoa - Đại học Đà Nẵng
- Giảng viên hướng dẫn: TS. Bùi Thị Thanh Thanh
- Thời gian thực hiện: Năm học 2025-2026

## Tóm tắt

Trong bối cảnh các dịch vụ du lịch ngày càng được số hóa, nhu cầu tra cứu thông tin địa điểm, xem lịch trình tour, đặt dịch vụ và nhận hỗ trợ trực tuyến của người dùng có xu hướng tăng. Đà Nẵng là một địa phương có nhiều điểm tham quan, tour trải nghiệm và nội dung du lịch cần được tổ chức dưới dạng hệ thống thông tin có khả năng cập nhật, tìm kiếm và quản lý tập trung.

Đề tài **"Xây dựng website du lịch Đà Nẵng (DanangTrip)"** được thực hiện nhằm xây dựng một hệ thống web phục vụ tra cứu thông tin du lịch, quản lý tour, đặt tour, thanh toán, đánh giá và hỗ trợ tư vấn bằng chatbot. Bên cạnh website dành cho người dùng, hệ thống cung cấp trang quản trị để quản lý địa điểm, tour, lịch khởi hành, đơn đặt tour, thanh toán, người dùng, bài viết, đánh giá, khuyến mãi, thông báo và báo cáo thống kê.

Hệ thống được xây dựng theo kiến trúc Client-Server, gồm các thành phần chính:

- Website người dùng sử dụng Next.js, React, TypeScript, React Query, Zustand, next-intl và các thư viện bản đồ/giao diện.
- Hệ thống quản trị sử dụng React, Vite, TypeScript, React Router, React Query, React Hook Form, Recharts và i18next.
- API phía server sử dụng Laravel 12, PHP 8.2, JWT/Sanctum, mẫu Repository-Service, PostgreSQL/Supabase, bộ nhớ đệm Redis, tải ảnh Cloudinary, DomPDF và tích hợp thanh toán SePay.
- Thành phần AI/chatbot được tổ chức theo các bước Intent Guard, Query Understanding, SQL RAG, Cache Layer và AI Failover. Chatbot truy xuất dữ liệu từ các bảng nghiệp vụ như tour, địa điểm, bài viết và chính sách để tạo ngữ cảnh trước khi gọi nhà cung cấp AI.

Kết quả của đề tài là hệ thống DanangTrip gồm website người dùng, trang quản trị và API phía server, đáp ứng các nghiệp vụ chính như tra cứu địa điểm, quản lý tour, đặt tour, thanh toán, đánh giá, chatbot tư vấn và quản trị dữ liệu vận hành.

## Lời nói đầu

Đồ án tốt nghiệp là kết quả của quá trình học tập, nghiên cứu và vận dụng kiến thức chuyên ngành công nghệ thông tin vào việc giải quyết một bài toán thực tế. Với đề tài **"Xây dựng website du lịch Đà Nẵng"**, em tập trung xây dựng một hệ thống web hỗ trợ quản lý thông tin địa điểm, tour, đơn đặt tour và thanh toán trực tuyến.

Trong quá trình thực hiện, em đã tìm hiểu và áp dụng các công nghệ phát triển web như Next.js, React, TypeScript, Laravel, RESTful API, xác thực JWT, PostgreSQL/Supabase, thanh toán trực tuyến, quản trị nội dung và chatbot có truy xuất dữ liệu nội bộ. Đề tài giúp em rèn luyện tư duy phân tích yêu cầu, thiết kế hệ thống, tổ chức mã nguồn, xây dựng giao diện, xử lý nghiệp vụ phía server và kiểm thử chức năng.

Em xin chân thành cảm ơn quý thầy cô Khoa Công nghệ thông tin - Trường Đại học Bách khoa - Đại học Đà Nẵng đã truyền đạt kiến thức nền tảng và tạo điều kiện cho em thực hiện đồ án. Em xin gửi lời cảm ơn sâu sắc đến giảng viên hướng dẫn TS. Bùi Thị Thanh Thanh đã định hướng, góp ý và hỗ trợ em trong suốt quá trình thực hiện.

Do giới hạn về thời gian thực hiện và kinh nghiệm triển khai thực tế, đồ án vẫn còn một số hạn chế. Sinh viên mong nhận được góp ý từ giảng viên và hội đồng để tiếp tục hoàn thiện hệ thống và báo cáo.

## Lời cam đoan

Em xin cam đoan đồ án **"Xây dựng website du lịch Đà Nẵng"** là kết quả do em thực hiện dưới sự hướng dẫn của giảng viên hướng dẫn. Các nội dung, số liệu, hình ảnh minh họa và tài liệu tham khảo sử dụng trong báo cáo sẽ được trích dẫn rõ ràng theo quy định.

Em xin chịu trách nhiệm về tính trung thực của nội dung báo cáo và sản phẩm đồ án.

Đà Nẵng, tháng 06 năm 2026

Sinh viên thực hiện

Nguyễn Duy Tây

## Danh sách chữ viết tắt

| Từ viết tắt | Viết đầy đủ | Diễn giải |
| --- | --- | --- |
| API | Application Programming Interface | Giao diện lập trình ứng dụng |
| AI | Artificial Intelligence | Trí tuệ nhân tạo |
| DB | Database | Cơ sở dữ liệu |
| ERD | Entity Relationship Diagram | Biểu đồ quan hệ thực thể |
| JWT | JSON Web Token | Chuẩn token dùng cho xác thực |
| REST | Representational State Transfer | Kiến trúc API phổ biến trên HTTP |
| SEO | Search Engine Optimization | Tối ưu hóa công cụ tìm kiếm |
| UI | User Interface | Giao diện người dùng |
| UX | User Experience | Trải nghiệm người dùng |
| CRUD | Create, Read, Update, Delete | Nhóm thao tác thêm, đọc, sửa, xóa |
| IPN | Instant Payment Notification | Thông báo thanh toán tức thời |
| RAG | Retrieval-Augmented Generation | Kỹ thuật kết hợp truy xuất tri thức và sinh câu trả lời |
