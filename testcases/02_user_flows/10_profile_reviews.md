# Màn hình Đánh giá của tôi (User Reviews & Ratings Given)

## Phạm vi

- Route: `/profile/ratings` hoặc `/[locale]/profile/ratings`
- API liên quan: Danh sách các đánh giá, nhận xét mà user hiện tại đã viết cho các tour du lịch.
- Vai trò: Người dùng đã đăng nhập (User).

## Điều kiện trước

- Tài khoản: Đã đăng nhập vào hệ thống, đã từng viết nhận xét đánh giá cho ít nhất một tour.
- Môi trường: Local dev server (`http://localhost:3000`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_US_REVIEW_001 | Danh sách đánh giá | Renders danh sách đánh giá cá nhân đã gửi | Có đánh giá đã gửi trong DB | Truy cập trang `/profile/ratings`. | | Danh sách hiển thị các nhận xét đã viết gồm: Tên tour du lịch, Số điểm sao đã đánh giá, Nội dung nhận xét, Ngày gửi nhận xét, Trạng thái kiểm duyệt của ban quản trị (Chờ duyệt / Đã duyệt / Đã ẩn). | | | |
| 2 | TC_US_REVIEW_002 | Xem tour được đánh giá | Click chuyển hướng sang trang tour từ nhận xét | | Click vào tên tour trên dòng nhận xét. | | Chuyển hướng thành công sang trang chi tiết của tour đó (`/tours/[slug]`). | | | |

## Ghi chú

-
