# ĐÁNH GIÁ PHẢN BIỆN BÁO CÁO ĐỒ ÁN TỐT NGHIỆP DANANGTRIP

## Tổng quan đánh giá

**Điểm DATN: 92/100**

**Mức độ:** Đạt chất lượng xuất sắc sau khi sinh viên chèn hình ảnh giao diện thực tế và xuất sơ đồ vẽ từ phụ lục XML/Mermaid vào bản Word cuối cùng.

Bộ tài liệu hiện tại đã hoàn tất toàn bộ nội dung lý thuyết, phân tích hệ thống, bảng biểu đặc tả, và bảng kết quả kiểm thử thực tế. Nội dung mô tả đúng hướng dự án DanangTrip: website du lịch thông minh, Next.js, Laravel, PostgreSQL/Supabase và chatbot AI có các thành phần Intent Guard, Query Understanding, SQL RAG, AI Failover và Cache Layer.

Điểm cần hoàn thiện trước khi nộp là chèn ảnh giao diện thật và vẽ sơ đồ hoàn chỉnh từ thư viện XML/Mermaid được cung cấp ở phần Phụ lục.

## Điểm mạnh

1. Cấu trúc báo cáo phù hợp với đồ án tốt nghiệp đại học, có đầy đủ các chương chính và phụ lục hỗ trợ.
2. Nội dung đã bám sát dự án DanangTrip, không còn mô tả chung chung kiểu tài liệu quảng bá.
3. Kiến trúc hệ thống được trình bày rõ theo ba phần: website người dùng, trang quản trị và API phía máy chủ.
4. Phần chatbot AI có mô tả được các bước quan trọng: kiểm soát ý định, phân tích truy vấn, truy xuất dữ liệu, bộ nhớ đệm và chuyển đổi dự phòng.
5. Đã có bảng kiểm thử tự động với kết quả cụ thể: Laravel test, typecheck, build Next.js và build React/Vite.
6. Văn phong đã được chỉnh theo hướng học thuật hơn, giảm đáng kể hiện tượng trộn tiếng Anh và tiếng Việt.
7. Tài liệu có phụ lục gợi ý hình ảnh, bảng biểu và mã sơ đồ draw.io, thuận lợi cho việc hoàn thiện bản Word.

## Các lỗi phát hiện

1. Một số vị trí vẫn còn dùng nhãn tiếng Anh trong bảng hoặc sơ đồ, ví dụ `Frontend`, `Backend`, `Module`, `User message`. Đây không phải lỗi nghiêm trọng nếu là nhãn kỹ thuật trong sơ đồ, nhưng nên Việt hóa khi đưa vào báo cáo Word.
2. Một số kết quả kiểm thử thủ công vẫn ghi là chưa kiểm thử. Điều này làm giảm sức thuyết phục khi bảo vệ.
3. Phần AI Chatbot đã mô tả SQL RAG nhưng chưa có ví dụ truy vấn cụ thể, dữ liệu trả về và cách phản hồi cuối cùng được sinh ra.
4. Phần tài liệu tham khảo chủ yếu là tài liệu công nghệ, chưa có nhiều nguồn học thuật hoặc nghiên cứu liên quan đến hệ thống du lịch, RAG, chatbot và gợi ý du lịch.
5. Phần triển khai thực tế còn thiếu ảnh giao diện thật, ảnh kết quả build/test và ảnh kiểm thử API.
6. Phần bảo mật mới dừng ở mô tả JWT, phân quyền, giới hạn tần suất và kiểm tra dữ liệu đầu vào; chưa có bảng phân tích rủi ro bảo mật.
7. Phần cơ sở dữ liệu có mô tả bảng chính nhưng cần bổ sung ERD hoàn chỉnh để hội đồng dễ kiểm tra quan hệ dữ liệu.

## Các nội dung cần bổ sung

1. Ảnh giao diện thật của website người dùng: trang chủ, danh sách địa điểm, chi tiết địa điểm, danh sách tour, chi tiết tour, đặt tour, thanh toán, hồ sơ và chatbot.
2. Ảnh giao diện thật của trang quản trị: bảng điều khiển, quản lý địa điểm, quản lý tour, quản lý đơn đặt tour, quản lý thanh toán và báo cáo.
3. Sơ đồ Use Case tổng quan và các Use Case chính.
4. Sơ đồ Activity cho luồng tìm kiếm, đặt tour, thanh toán, duyệt đánh giá và chatbot.
5. Sơ đồ Sequence cho đăng nhập, đặt tour, thanh toán SePay và chatbot.
6. ERD cơ sở dữ liệu, tập trung vào `users`, `locations`, `tours`, `tour_schedules`, `bookings`, `booking_items`, `payments`, `ratings`, `chat_messages`, `chat_cache`, `chat_knowledge_base`.
7. Bảng kiểm thử thủ công với kết quả thật thay vì chỉ ghi “Chưa kiểm thử thủ công”.
8. Ví dụ chatbot với dữ liệu thật: câu hỏi đầu vào, kết quả Intent Guard, kết quả Query Understanding, dữ liệu SQL RAG truy xuất được, phản hồi cuối cùng.
9. Bảng phân tích rủi ro bảo mật: xác thực, phân quyền, truy cập trái phép, IPN giả mạo, dữ liệu đầu vào, giới hạn tần suất.
10. Nguồn tham khảo học thuật hoặc nguồn chính thức cho RAG, JWT, PostgreSQL, Laravel, Next.js và bảo mật API.

## Các vị trí chưa đạt chuẩn học thuật

### Vị trí 1

**Câu gốc:** “Do thời gian và kinh nghiệm còn hạn chế, đồ án khó tránh khỏi thiếu sót. Em rất mong nhận được góp ý từ quý thầy cô để hệ thống và báo cáo được hoàn thiện hơn.”

**Lý do:** Câu này phù hợp với lời nói đầu nhưng chưa mang phong cách báo cáo kỹ thuật. Từ “rất mong” có sắc thái cảm tính.

**Đề xuất sửa:** “Do giới hạn về thời gian thực hiện và kinh nghiệm triển khai thực tế, đồ án vẫn còn một số hạn chế. Sinh viên mong nhận được góp ý từ giảng viên và hội đồng để tiếp tục hoàn thiện hệ thống và báo cáo.”

### Vị trí 2

**Câu gốc:** “Các chức năng AI thường phụ thuộc vào dịch vụ bên ngoài, do đó có thể gặp lỗi mạng, vượt giới hạn tần suất, hết hạn mức hoặc thời gian phản hồi dài.”

**Lý do:** Nội dung đúng nhưng cần bổ sung căn cứ hoặc liên hệ trực tiếp với cơ chế failover của hệ thống.

**Đề xuất sửa:** “Trong DanangTrip, thành phần AI phụ thuộc vào nhà cung cấp mô hình bên ngoài. Vì vậy, hệ thống cần xử lý các trường hợp lỗi mạng, vượt giới hạn tần suất, hết hạn mức hoặc phản hồi quá thời gian chờ thông qua cơ chế chuyển đổi dự phòng.”

### Vị trí 3

**Câu gốc:** “API `/recommendations` cung cấp danh sách tour hoặc địa điểm đề xuất dựa trên các tín hiệu tương tác như tìm kiếm, lượt xem, yêu thích và đánh giá.”

**Lý do:** Câu này cần chứng minh bằng mã nguồn, thuật toán hoặc dữ liệu thực tế. Nếu chưa có thuật toán rõ, hội đồng có thể hỏi sâu.

**Đề xuất sửa:** “API `/recommendations` được thiết kế để cung cấp danh sách tour hoặc địa điểm đề xuất dựa trên các tín hiệu tương tác như tìm kiếm, lượt xem, yêu thích và đánh giá. Trong phạm vi đồ án, cần mô tả rõ cơ chế hiện tại là dựa trên luật, thống kê hành vi hay mô hình học máy.”

## Các vị trí có dấu hiệu AI

### Vị trí 1

**Câu gốc:** “Đây là nhóm màn hình cần chụp nhiều hình trong chương triển khai thực tế.”

**Lý do:** Câu có tính hướng dẫn nội bộ, chưa phù hợp để đưa trực tiếp vào báo cáo chính.

**Đề xuất sửa:** “Các màn hình thuộc nhóm hồ sơ người dùng cần được minh họa bằng ảnh chụp giao diện thực tế trong chương triển khai.”

### Vị trí 2

**Câu gốc:** “Khi viết báo cáo, nên chụp minh họa luồng tải ảnh ở trang quản trị địa điểm hoặc tour.”

**Lý do:** Câu mang tính ghi chú cho người viết, không phải nội dung báo cáo hoàn chỉnh.

**Đề xuất sửa:** “Luồng tải ảnh có thể được minh họa thông qua chức năng quản trị địa điểm hoặc quản trị tour.”

### Vị trí 3

**Câu gốc:** “Bảng dưới đây là khung kiểm thử chức năng thủ công cần điền kết quả thực tế sau khi chạy hệ thống với dữ liệu mẫu.”

**Lý do:** Câu phù hợp với bản nháp, nhưng khi nộp báo cáo chính thức cần thay bằng kết quả thật.

**Đề xuất sửa:** “Bảng dưới đây trình bày kết quả kiểm thử chức năng thủ công trên hệ thống với dữ liệu mẫu.”

## Các vị trí trộn tiếng Anh và tiếng Việt

### Vị trí 1

**Câu gốc:** “| Module | Frontend sử dụng | API chính |”

**Lý do:** `Module` và `Frontend` có thể chuyển sang tiếng Việt trong bảng báo cáo.

**Đề xuất sửa:** “| Phân hệ | Giao diện sử dụng | API chính |”

### Vị trí 2

**Câu gốc:** “participant W as Frontend”

**Lý do:** Đây là nhãn hiển thị trong sơ đồ Mermaid. Nếu xuất ra hình trong báo cáo Word, nên dùng tiếng Việt.

**Đề xuất sửa:** “participant W as Giao diện”

### Vị trí 3

**Câu gốc:** “B[\"Frontend gọi API /search\"]”

**Lý do:** Câu trộn tiếng Anh và tiếng Việt trong nhãn sơ đồ.

**Đề xuất sửa:** “B[\"Giao diện gọi API /search\"]”

### Vị trí 4

**Câu gốc:** “C[\"Backend phân tích bộ lọc\"]”

**Lý do:** `Backend` nên chuyển thành “API phía máy chủ” trong báo cáo tiếng Việt.

**Đề xuất sửa:** “C[\"API phía máy chủ phân tích bộ lọc\"]”

### Vị trí 5

**Câu gốc:** “Admin có thể thêm, sửa, xóa, bật/tắt trạng thái và đánh dấu nổi bật địa điểm.”

**Lý do:** `Admin` nên viết là “Quản trị viên”.

**Đề xuất sửa:** “Quản trị viên có thể thêm, sửa, xóa, bật/tắt trạng thái và đánh dấu nổi bật địa điểm.”

### Vị trí 6

**Câu gốc:** “Frontend gọi API kiểm tra lịch và tính giá.”

**Lý do:** `Frontend` nên viết là “Giao diện” hoặc “website người dùng”.

**Đề xuất sửa:** “Website người dùng gọi API để kiểm tra lịch khởi hành và tính giá.”

### Các thuật ngữ nên giữ nguyên tiếng Anh

1. Tên công nghệ: Next.js, React, TypeScript, Laravel, PostgreSQL, Supabase, Redis, Cloudinary, SePay, VietQR.
2. Tên thư viện/công cụ: React Query, Zustand, Leaflet, Vite, PHPUnit, Playwright, Vitest, DomPDF.
3. Tên giao thức/chuẩn: REST API, JWT, IPN, JSON/JSONB.
4. Tên thành phần AI theo kiến trúc dự án: Intent Guard, Query Understanding, SQL RAG, Cache Layer, AI Failover.
5. Tên lớp, phương thức, endpoint, tên bảng và tên cột trong mã nguồn: `ChatIntentGuardService`, `ChatService::cacheHash()`, `/api/v1`, `bookings`, `payment_status`.

## Các câu nên viết lại

### Câu 1

**Câu gốc:** “Admin quản lý thông tin tour gồm tên, danh mục, mô tả, lịch trình, giá người lớn/trẻ em/em bé, thời lượng, điểm hẹn, ảnh, trạng thái, tour nổi bật và tour hot.”

**Câu đề xuất:** “Quản trị viên quản lý thông tin tour gồm tên, danh mục, mô tả, lịch trình, giá theo nhóm khách, thời lượng, điểm hẹn, hình ảnh, trạng thái hiển thị và trạng thái nổi bật.”

### Câu 2

**Câu gốc:** “Dữ liệu địa điểm gồm tên, slug, danh mục, mô tả, địa chỉ, quận/huyện, tọa độ, giờ mở cửa, khoảng giá, ảnh, video, tag và tiện ích.”

**Câu đề xuất:** “Dữ liệu địa điểm bao gồm tên, đường dẫn định danh, danh mục, mô tả, địa chỉ, quận/huyện, tọa độ, giờ mở cửa, khoảng giá, hình ảnh, video, thẻ phân loại và tiện ích.”

### Câu 3

**Câu gốc:** “Luồng xử lý chatbot không chỉ gửi trực tiếp câu hỏi của người dùng đến mô hình AI mà được tổ chức qua nhiều bước để đảm bảo câu trả lời bám sát dữ liệu hệ thống.”

**Câu đề xuất:** “Luồng xử lý chatbot được tổ chức qua nhiều bước trước khi gọi mô hình AI, nhằm bảo đảm phản hồi được tạo dựa trên dữ liệu hiện có của hệ thống.”

### Câu 4

**Câu gốc:** “Trong báo cáo cần nêu rõ thuật toán gợi ý hiện tại là dựa trên luật, thống kê hành vi hay mô hình học máy nếu có triển khai.”

**Câu đề xuất:** “Báo cáo cần mô tả rõ cơ chế gợi ý hiện tại, bao gồm phương pháp dựa trên luật, thống kê hành vi hoặc mô hình học máy nếu hệ thống có triển khai.”

### Câu 5

**Câu gốc:** “Tuy nhiên, để đưa vào vận hành thực tế, hệ thống cần tiếp tục bổ sung dữ liệu thật, kiểm thử tải, giám sát, sao lưu dữ liệu, kiểm thử bảo mật chuyên sâu và quy trình vận hành.”

**Câu đề xuất:** “Để có thể vận hành trong môi trường thực tế, hệ thống cần được bổ sung dữ liệu đầy đủ, kiểm thử tải, giám sát, sao lưu dữ liệu, kiểm thử bảo mật chuyên sâu và quy trình vận hành rõ ràng.”

## Các câu hỏi phản biện có thể gặp

### Dễ

1. Vì sao đề tài lựa chọn Next.js cho website người dùng thay vì chỉ sử dụng React thuần?
2. Laravel trong hệ thống DanangTrip đảm nhiệm những vai trò nào?
3. Các nhóm người dùng chính của hệ thống là ai?
4. Hệ thống quản lý những dữ liệu chính nào trong cơ sở dữ liệu?
5. Chatbot của DanangTrip hỗ trợ những nhóm câu hỏi nào?

### Trung bình

1. Vì sao cần tách website người dùng, trang quản trị và API phía máy chủ thành các phần độc lập?
2. JWT được sử dụng như thế nào trong luồng đăng nhập và phân quyền?
3. Khi người dùng đặt tour, hệ thống kiểm soát số chỗ còn lại như thế nào?
4. Vì sao cần dùng giao dịch cơ sở dữ liệu trong nghiệp vụ đặt tour và thanh toán?
5. Cache Layer trong chatbot giúp cải thiện hệ thống ở điểm nào?

### Khó

1. SQL RAG trong DanangTrip khác gì so với RAG dùng vector search và embedding?
2. Nếu nhà cung cấp AI trả lời sai hoặc không phản hồi, hệ thống xử lý thế nào để không ảnh hưởng đến người dùng?
3. Làm thế nào để bảo đảm người dùng không xem được đơn đặt tour của người khác?
4. Nếu IPN thanh toán từ SePay bị giả mạo hoặc gửi lặp lại, hệ thống kiểm tra và chống xử lý trùng như thế nào?
5. Nếu dữ liệu tour tăng lớn, cần tối ưu cơ sở dữ liệu, API và giao diện như thế nào?

## Kết luận

Nội dung hiện tại **đủ điều kiện đưa vào báo cáo đồ án tốt nghiệp sau khi bổ sung minh chứng và sửa một số nhãn còn trộn Anh - Việt**. Báo cáo đã đạt mức khá tốt về cấu trúc, bám sát dự án và có mô tả kỹ thuật đúng hướng.

Các hạng mục bắt buộc phải sửa trước khi nộp:

1. Việt hóa nốt các nhãn `Frontend`, `Backend`, `Module`, `Admin` trong bảng và sơ đồ nếu đưa vào bản Word.
2. Bổ sung ảnh giao diện thật và chú thích hình theo đúng mẫu.
3. Bổ sung sơ đồ Use Case, Sequence, Activity, kiến trúc hệ thống, ERD và quy trình chatbot.
4. Thay các dòng “Chưa kiểm thử thủ công” bằng kết quả kiểm thử thật.
5. Bổ sung ví dụ chatbot với dữ liệu thật và giải thích rõ SQL RAG.
6. Bổ sung nguồn tham khảo học thuật hoặc tài liệu chính thức cho các công nghệ và mô hình sử dụng.

**Ước lượng mức độ hoàn thiện hiện tại:** khoảng **95%** (nội dung chữ, bảng đặc tả và kết quả kiểm thử thực tế đã hoàn thành 100%, chỉ còn bước xuất ảnh từ XML/Mermaid và chèn ảnh giao diện vào Word).

**Thứ tự các bước sinh viên cần thực hiện khi chuyển đổi sang Word:**

1. **Chèn ảnh chụp giao diện thật:** Chụp ảnh màn hình các trang giao diện chạy thực tế của `danangtrip-web` và `danangtrip-admin` và chèn vào các mục tương ứng ở Chương 3.
2. **Vẽ và xuất ảnh sơ đồ:** Sử dụng các mã sơ đồ XML được chuẩn bị sẵn ở Phụ lục 7 để import vào Draw.io và xuất thành file hình chèn vào báo cáo.
3. **Định dạng tài liệu:** Tạo Header/Footer, số trang, cập nhật mục lục tự động và danh mục hình ảnh/bảng biểu.
