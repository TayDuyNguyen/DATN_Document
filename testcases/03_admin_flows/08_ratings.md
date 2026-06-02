# Màn hình Quản lý Đánh giá & Bình luận (Ratings & Reviews Moderation)

## Phạm vi

- Route: `/admin/ratings` hoặc `/admin/reviews`
- API liên quan: Duyệt đánh giá, ẩn/xóa bình luận spam, phản hồi đánh giá khách hàng.
- Vai trò: Quản trị viên (Admin) / Nhân viên (Staff).

## Điều kiện trước

- Tài khoản: Đã đăng nhập vào trang quản trị bằng tài khoản Admin/Staff.
- Dữ liệu mẫu: Hệ thống đã có các đánh giá từ người dùng gửi về từ các tour đã hoàn thành.
- Môi trường: Local dev server (`http://localhost:5173`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_AD_RATE_001 | Danh sách Đánh giá | Renders danh sách đánh giá của các tour | Có đánh giá trong DB | Truy cập trang Quản lý Đánh giá. | | Hiển thị danh sách đánh giá đầy đủ thông tin: Người đánh giá, Tour được đánh giá, Số sao (1-5 sao hiển thị bằng icon ngôi sao), Nội dung nhận xét, Ngày đánh giá, Trạng thái (Đang chờ / Đã duyệt / Đã ẩn). | | | |
| 2 | TC_AD_RATE_002 | Lọc theo số sao | Lọc các đánh giá theo điểm số sao | | Chọn bộ lọc sao từ dropdown (ví dụ: Lọc chỉ xem đánh giá 1 sao hoặc 5 sao). | Bộ lọc: `1 sao` | Bảng cập nhật và chỉ hiển thị các bình luận/đánh giá có điểm xếp hạng là 1 sao để quản trị viên xử lý khiếu nại. | | | |
| 3 | TC_AD_RATE_003 | Duyệt đánh giá (Approve) | Kiểm tra phê duyệt đánh giá của khách hàng | Đánh giá đang ở trạng thái "Đang chờ" (Pending) | 1. Chọn đánh giá đang chờ duyệt.<br>2. Click nút "Duyệt" (Approve). | | - Đánh giá chuyển trạng thái thành "Đã duyệt" (Approved).<br>- Đánh giá này chính thức hiển thị công khai trên phần đánh giá tour tại Web client. | | | |
| 4 | TC_AD_RATE_004 | Ẩn đánh giá spam | Ẩn bình luận spam hoặc chứa từ ngữ không phù hợp | Đang có bình luận thô tục hoặc spam | 1. Tìm bình luận vi phạm.<br>2. Click nút "Ẩn" (Hide) hoặc "Khóa".<br>3. Xác nhận hành động. | | - Đánh giá chuyển trạng thái thành "Đã ẩn" (Hidden).<br>- Bình luận lập tức biến mất khỏi trang chi tiết tour bên Web client. | | | |
| 5 | TC_AD_RATE_005 | Phản hồi đánh giá | Admin/Staff viết phản hồi lại nhận xét của khách hàng | Đánh giá hợp lệ | 1. Click nút "Phản hồi" (Reply) tại dòng đánh giá.<br>2. Nhập nội dung phản hồi trong ô nhập liệu.<br>3. Nhấn "Gửi". | Phản hồi: "Cảm ơn quý khách đã tin tưởng dịch vụ của DaNangTrip!" | - Phản hồi được gửi lên hệ thống thành công.<br>- Hiển thị phản hồi của Admin bên dưới nhận xét của khách hàng ở cả giao diện quản trị và trang chi tiết tour phía Web client. | | | |

## Ghi chú

-
