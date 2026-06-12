# ĐÁNH GIÁ PHẢN BIỆN VÀ ĐỐI CHIẾU VỚI MÃ NGUỒN

## Tổng quan đánh giá

**Điểm DATN dự kiến: 87/100**

**Mức độ: Có thể sử dụng sau khi bổ sung minh chứng thực nghiệm**

Bộ báo cáo đã mô tả đúng các thành phần chính của DanangTrip: website người dùng Next.js, trang quản trị React/Vite, API Laravel, PostgreSQL/Supabase, thanh toán SePay/VietQR, quản lý nội dung và chatbot. Nội dung đã được cập nhật theo mã nguồn ngày 12/06/2026 để bổ sung điểm thành viên, phiếu giảm giá cá nhân, lượt đánh giá hữu ích, xác nhận thanh toán thủ công, thông báo nghiệp vụ và nhắc lịch khởi hành.

## Các lỗi đã phát hiện và chỉnh sửa

1. Báo cáo cũ nhắc PayOS trong khi mã nguồn hiện tại đã chuyển sang SePay/VietQR. Nội dung đã được sửa.
2. Báo cáo cũ mô tả bộ nhớ đệm chatbot bằng Redis. Mã nguồn thực tế dùng bảng `chat_cache`; Redis chỉ là lựa chọn cấu hình triển khai.
3. Báo cáo cũ mô tả RAG như chỉ có truy vấn SQL hoặc dùng cơ sở dữ liệu véc-tơ chuyên dụng. Mã nguồn thực tế kết hợp truy xuất dữ liệu nghiệp vụ với embedding lưu trong PostgreSQL và tính độ tương đồng cosin ở tầng dịch vụ.
4. Báo cáo cũ cho rằng Laravel Policy kiểm soát quyền xem đơn. Mã nguồn hiện kiểm tra trực tiếp `user_id` trong `BookingService`.
5. Báo cáo cũ cho rằng đơn đặt tour dùng UUID. Hệ thống dùng khóa chính số tự tăng và `booking_code` ngẫu nhiên; việc chống truy cập trái phép vẫn dựa trên xác thực và kiểm tra quyền sở hữu.
6. Báo cáo cũ chưa mô tả các bảng `rating_helpful_votes`, `user_point_balances`, `point_rules`, `point_rewards`, `point_transactions` và `user_vouchers`.
7. Báo cáo cũ chưa mô tả thứ tự áp dụng giảm giá, phiếu cá nhân, đơn có giá trị bằng không, xác nhận thanh toán thủ công và tác vụ nhắc lịch.

## Sai lệch còn tồn tại trong mã nguồn

### 1. Điều kiện đánh giá tour chưa thống nhất

`RatingService` cho phép đánh giá khi đơn có trạng thái `confirmed` hoặc `completed`, nhưng thông báo lỗi lại yêu cầu người dùng phải “hoàn thành chuyến đi”. Hai cách hiểu này khác nhau.

Khuyến nghị: nếu nghiệp vụ yêu cầu trải nghiệm thực tế, chỉ chấp nhận `completed`. Nếu muốn cho phép đánh giá ngay sau khi xác nhận, cần sửa thông báo và nội dung báo cáo cho phù hợp. Báo cáo hiện không khẳng định điều kiện chặt hơn mã nguồn.

### 2. Xác thực IPN SePay phụ thuộc cấu hình

`SepayPaymentService` chỉ kiểm tra token/chữ ký khi `SEPAY_VERIFY_IPN_SIGNATURE=true`. Môi trường vận hành thật phải bật cấu hình này và đặt khóa bí mật; nếu không, IPN được chấp nhận mà không xác thực nguồn gửi.

### 3. Tìm kiếm embedding chưa tối ưu cho dữ liệu lớn

`ChatVectorSearchService` lấy một tập ứng viên từ PostgreSQL rồi tính độ tương đồng cosin trong PHP. Cách này phù hợp quy mô đồ án nhưng chưa thay thế chỉ mục véc-tơ chuyên dụng khi cơ sở tri thức tăng lớn.

### 4. Thiếu giao diện quản trị chương trình điểm

API và cơ sở dữ liệu đã có quy tắc điểm, phần thưởng và phiếu giảm giá, nhưng báo cáo chưa có minh chứng về giao diện quản trị riêng cho việc thay đổi các quy tắc này. Không nên khẳng định quản trị viên đã quản lý đầy đủ chương trình điểm nếu chưa có màn hình tương ứng.

## Các nội dung cần bổ sung thủ công

1. Ảnh giao diện `/profile/points`, lịch sử điểm, phần thưởng và phiếu giảm giá.
2. Ảnh bước đặt tour có lựa chọn khuyến mãi/phiếu giảm giá cá nhân.
3. Ảnh ghi nhận đánh giá hữu ích và thông báo điểm.
4. Ảnh trang quản trị xác nhận thanh toán thủ công.
5. Kết quả chạy lệnh nhắc lịch khởi hành với dữ liệu mẫu.
6. ERD cập nhật nhóm bảng điểm và `rating_helpful_votes`.
7. Bảng kiểm thử thực tế cho đổi điểm, áp dụng phiếu, chống ghi nhận hữu ích trùng và chống gửi nhắc lịch trùng.
8. Minh chứng cấu hình xác thực IPN trong môi trường trình diễn, không công bố khóa bí mật.
9. Cài đặt `pdo_sqlite` hoặc cấu hình cơ sở dữ liệu kiểm thử tương đương để chạy bốn trường hợp tích hợp đang bị bỏ qua trong `PointServiceTest`.

## Kiểm tra ngôn ngữ và văn phong

Các tên công nghệ, lớp, hàm, API và thuật ngữ không có bản dịch phổ biến được giữ nguyên. Báo cáo thống nhất sử dụng các thuật ngữ Client, Server, Client-Server và Server API; các thành phần chatbot vẫn được diễn giải bằng tiếng Việt trước tên tiếng Anh.

Một số tên tiếng Anh trong ngoặc được giữ lại để đối chiếu với mã nguồn và phục vụ phản biện, không được dùng thay cho phần diễn giải tiếng Việt.

## Kết luận

Nội dung hiện tại bám sát dự án hơn phiên bản trước và có thể dùng làm bản thảo báo cáo. Báo cáo chưa nên nộp như bản cuối cho đến khi bổ sung hình ảnh, sơ đồ, kết quả kiểm thử thật và xử lý hoặc giải trình điều kiện đánh giá tour cùng cấu hình xác thực IPN.
