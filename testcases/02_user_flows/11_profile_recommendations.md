# Màn hình Gợi ý riêng cho bạn (Personalized Recommendations Page)

## Phạm vi

- Route: `/profile/recommendations` hoặc `/[locale]/profile/recommendations`
- API liên quan: Lấy danh sách tour gợi ý dựa trên sở thích, lịch sử tìm kiếm và các tour đã đặt trước đó của user (Recommendation System).
- Vai trò: Người dùng đã đăng nhập (User).

## Điều kiện trước

- Tài khoản: Đã đăng nhập vào hệ thống.
- Môi trường: Local dev server (`http://localhost:3000`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_US_RECOM_001 | Hiển thị gợi ý | Hiển thị danh sách tour du lịch gợi ý cá nhân hóa | Hệ thống đã phân tích hành vi của user | Truy cập trang `/profile/recommendations`. | | - Hiển thị tiêu đề giới thiệu gợi ý riêng biệt.<br>- Renders danh sách các card tour được gợi ý có nhãn hoặc giải thích lý do gợi ý (Ví dụ: "Vì bạn đã quan tâm đến Bà Nà Hills"). | | | |
| 2 | TC_US_RECOM_002 | Khám phá nhanh | Kiểm tra click chuyển hướng từ tour gợi ý | | Click chọn 1 card tour trong danh sách gợi ý. | | Chuyển hướng thành công tới trang chi tiết tour (`/tours/[slug]`). | | | |

## Ghi chú

-
