# Màn hình Kết quả Tìm kiếm tổng hợp (Search Page)

## Phạm vi

- Route: `/search` hoặc `/[locale]/search`
- API liên quan: Tìm kiếm từ khóa tổng hợp cho cả Tour, Địa điểm du lịch và Bài viết blog.
- Vai trò: Khách vãng lai (Guest) / Người dùng đã đăng nhập (User).

## Điều kiện trước

- Dữ liệu mẫu: Có tour, địa điểm du lịch và bài viết chứa từ khóa cần tìm trong DB.
- Môi trường: Local dev server (`http://localhost:3000`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Điều kiện tiên quyết | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Kết quả thực tế | Status | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_SEARCH_001 | Nhận diện từ khóa | Nhận diện từ khóa tìm kiếm truyền từ URL | | Truy cập trang tìm kiếm qua đường dẫn: `/search?q=Bà%20Nà`. | Từ khóa: `Bà Nà` | - Trang hiển thị ô tìm kiếm có sẵn từ khóa "Bà Nà" bên trong.<br>- Tiêu đề kết quả ghi rõ: `Kết quả tìm kiếm cho "Bà Nà"`. | | | |
| 2 | TC_SEARCH_002 | Phân nhóm kết quả | Hiển thị kết quả tìm kiếm theo từng phân mục | Có kết quả khớp ở cả Tour và Địa điểm | Thực hiện tìm kiếm tổng hợp và kiểm tra các tab kết quả: Tất cả, Tour du lịch, Địa điểm, Bài viết. | Từ khóa: `Đà Nẵng` | - Tab "Tour du lịch" hiển thị danh sách tour đi Đà Nẵng.<br>- Tab "Địa điểm" hiển thị các địa danh tại Đà Nẵng.<br>- Tab "Bài viết" hiển thị các bài viết chia sẻ kinh nghiệm về Đà Nẵng. | | | |
| 3 | TC_SEARCH_003 | Không tìm thấy kết quả | Hiển thị thông báo khi không có từ khóa nào khớp | | 1. Nhập từ khóa không có nghĩa hoặc không tồn tại trong hệ thống.<br>2. Bấm tìm kiếm. | Từ khóa: `xyzabc123` | - Hiển thị màn hình thông báo: "Không tìm thấy kết quả phù hợp với từ khóa xyzabc123".<br>- Có gợi ý tìm kiếm bằng các từ khóa phổ biến khác bên dưới. | | | |
| 4 | TC_SEARCH_004 | Gợi ý từ khóa nhanh | Kiểm tra gợi ý từ khóa khi đang nhập (Autosuggestion) | | 1. Đặt con trỏ vào ô tìm kiếm.<br>2. Nhập từ 2 ký tự đầu tiên (Ví dụ: `Hộ`). | Từ khóa: `Hộ` | Một dropdown gợi ý hiện ra bên dưới ô nhập chứa các từ khóa gợi ý như: "Hội An", "Tour Hội An 1 ngày". Click vào từ gợi ý sẽ tự điền và kích hoạt tìm kiếm. | | | |

## Ghi chú

-
