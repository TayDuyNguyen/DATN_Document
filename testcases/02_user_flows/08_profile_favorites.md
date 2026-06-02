# Màn hình Danh sách Yêu thích (Favorite Tours Page)

## Phạm vi

- Route: `/profile/favorites` hoặc `/[locale]/profile/favorites`
- API liên quan: Lấy danh sách tour yêu thích của user, xóa tour khỏi danh sách yêu thích.
- Vai trò: Người dùng đã đăng nhập (User).

## Điều kiện trước

- Tài khoản: Đã đăng nhập vào hệ thống.
- Môi trường: Local dev server (`http://localhost:3000`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_FAVORITE_001 | Danh sách trống | Hiển thị khi chưa yêu thích tour nào | Người dùng chưa bấm yêu thích tour nào | Truy cập trang `/profile/favorites`. | | Hiển thị thông điệp "Danh sách yêu thích trống" kèm hình ảnh minh họa và nút "Khám phá Tour". | | | |
| 2 | TC_FAVORITE_002 | Hiển thị danh sách | Hiển thị các tour đã lưu yêu thích | Đã lưu ít nhất 1 tour | Truy cập trang `/profile/favorites`. | | Hiển thị danh sách các card tour đã yêu thích với đầy đủ thông tin: Ảnh, Tên tour, Giá tiền, Đánh giá sao, và icon Trái tim màu đỏ. | | | |
| 3 | TC_FAVORITE_003 | Click Xem chi tiết | Click chọn xem chi tiết tour từ danh sách | | Click vào hình ảnh hoặc tiêu đề của tour trong danh sách yêu thích. | | Chuyển hướng thành công tới trang chi tiết tour tương ứng (`/tours/[slug]`). | | | |
| 4 | TC_FAVORITE_004 | Xóa khỏi danh sách | Bỏ yêu thích trực tiếp tại trang danh sách | | Click vào icon Trái tim (hoặc nút xóa) trên card tour yêu thích. | | - Tour biến mất khỏi danh sách yêu thích ngay lập tức với hiệu ứng mượt mà.<br>- Hiển thị toast thông báo "Đã xóa khỏi danh sách yêu thích". | | | |

## Ghi chú

-
