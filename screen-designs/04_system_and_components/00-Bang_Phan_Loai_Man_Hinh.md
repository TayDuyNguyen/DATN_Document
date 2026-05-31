# Phân loại màn hình DanangTrip

> Cập nhật: 14/05/2026  
> Phạm vi: `D:\DATN\DATN_Tài liệu\screen`  
> Chuẩn đối chiếu: `D:\DATN\DATN_Tài liệu\docs\page`

Tài liệu này thay thế bảng phân loại cũ. Các mục như "Bài đăng của tôi", "Lịch sử hoạt động", "Nạp Point", "Quản lý Point" không còn là nghiệp vụ chính của hệ thống DanangTrip hiện tại và không dùng làm chuẩn triển khai.

---

## 1. Quy ước trạng thái

| Trạng thái | Ý nghĩa |
|---|---|
| Đã có prototype | Đã có file `.html` và `.png` trong thư mục `screen` |
| Có một phần | Đã có màn gần tương đương nhưng thiếu đúng flow hoặc thiếu trạng thái |
| Cần bổ sung | `docs/page` đã mô tả nhưng `screen` chưa có prototype |
| Planned | Có trong tài liệu để mở rộng, API/database có thể chưa hoàn chỉnh |

---

## 2. Public / Guest flows

| Nhóm | Màn theo `docs/page` | Prototype hiện có | Trạng thái |
|---|---|---|---|
| Auth | Đăng nhập | Chưa có file riêng | Cần bổ sung |
| Auth | Đăng ký | Chưa có file riêng | Cần bổ sung |
| Auth | Quên mật khẩu | Chưa có file riêng | Cần bổ sung |
| Auth | Đặt lại mật khẩu | Chưa có file riêng | Cần bổ sung |
| Trang chủ | Trang chủ | `1_Guest_Flows/01.*-Trang_Chu_Guest` | Đã có prototype |
| Trang chủ | Landing tour Đà Nẵng | `1_Guest_Flows/05.*-Gioi_Thieu_Da_Nang` | Có một phần |
| Tìm kiếm | Trang tìm kiếm | `1_Guest_Flows/02.*-Tim_Kiem` | Đã có prototype |
| Địa điểm | Danh sách địa điểm | `1_Guest_Flows/03.2-Danh_Sach_Dia_Diem` | Đã có prototype |
| Địa điểm | Địa điểm theo danh mục | `1_Guest_Flows/03.1-Danh_Muc_Dia_Diem` | Đã có prototype |
| Địa điểm | Chi tiết địa điểm guest | `1_Guest_Flows/04.*-Chi_Tiet_Dia_Diem*` | Đã có prototype |
| Địa điểm | Địa điểm lân cận | `1_Guest_Flows/04.3-Dia_Diem_Lan_Can` | Đã có prototype |
| Tour | Danh sách tour | `1_Guest_Flows/07.1-Danh_Sach_Tour` | Đã có prototype |
| Tour | Chi tiết tour | `1_Guest_Flows/07.2`, `07.3-Chi_Tiet_Tour` | Đã có prototype |
| Tour | Tour theo danh mục | Chưa có file riêng | Cần bổ sung |
| Tour | Chọn lịch khởi hành | Chưa có file riêng/modal riêng | Cần bổ sung |
| Blog | Danh sách blog | `1_Guest_Flows/06.1-Cam_Nang_Du_Lich` | Đã có prototype |
| Blog | Chi tiết blog | Chưa có file riêng | Cần bổ sung |
| Blog | Blog theo danh mục | Chưa có file riêng | Cần bổ sung |
| Liên hệ | Form liên hệ | `1_Guest_Flows/08-Trang_Lien_He` | Đã có prototype |

---

## 3. User flows

| Nhóm | Màn theo `docs/page` | Prototype hiện có | Trạng thái |
|---|---|---|---|
| Auth | Xác thực email | `2_User_Flows/04.*-Xac_Thuc_Email*` | Đã có prototype |
| Trang chủ | Trang chủ có gợi ý cá nhân | `1_Guest_Flows/09-Goi_Y_Cho_Ban` | Có một phần |
| Tìm kiếm | Tìm kiếm có lịch sử | `1_Guest_Flows/02.*-Tim_Kiem` | Có một phần / Planned |
| Địa điểm | Chi tiết địa điểm user | `2_User_Flows/02-Chi_Tiet_Dia_Diem_User` | Đã có prototype |
| Tour | Đặt tour | `2_User_Flows/09.1-Dat_Tour` | Đã có prototype |
| Tour | Thanh toán | `2_User_Flows/09.2`, `09.3-Thanh_Toan` | Đã có prototype |
| Tour | Kết quả thanh toán | `2_User_Flows/09.4-Thanh_Toan_Thanh_Cong` | Đã có prototype |
| Tour | Giỏ hàng | Chưa có file riêng | Planned |
| Hồ sơ | Hồ sơ cá nhân | `2_User_Flows/05.1-Trang_Ca_Nhan` | Đã có prototype |
| Hồ sơ | Đổi mật khẩu | `2_User_Flows/05.2-Doi_Mat_Khau` | Đã có prototype |
| Hồ sơ | Xóa tài khoản | `2_User_Flows/05.3-Xoa_Tai_Khoan` | Đã có prototype / Planned API |
| Đơn hàng | Lịch sử đặt tour | `2_User_Flows/08.1-Danh_Sach_Don_Dat_Tour` | Đã có prototype |
| Đơn hàng | Chi tiết đơn đặt | `2_User_Flows/08.2`, `08.3-Chi_Tiet_Don_Dat_Tour` | Đã có prototype |
| Đơn hàng | Chi tiết theo mã đơn | Chưa có file riêng | Cần bổ sung |
| Đơn hàng | Hóa đơn PDF | Chưa có file riêng | Cần bổ sung |
| Yêu thích | Danh sách yêu thích | `2_User_Flows/07-Dia_Diem_Yeu_Thich` | Đã có prototype |
| Đánh giá | Đánh giá của tôi | `2_User_Flows/03.2`, `03.3-Danh_Gia_Cua_Toi` | Đã có prototype |
| Đánh giá | Viết đánh giá | `2_User_Flows/03.1-Viet_Danh_Gia` | Đã có prototype |
| Đánh giá | Sửa/xóa/hữu ích | Chưa có modal/action riêng | Cần bổ sung |
| Thông báo | Danh sách thông báo | `2_User_Flows/10-Thong_Bao` | Đã có prototype |
| Gợi ý | Gợi ý cho bạn | `1_Guest_Flows/09-Goi_Y_Cho_Ban` | Có một phần |

---

## 4. Admin flows

| Nhóm | Màn theo `docs/page` | Prototype hiện có | Trạng thái |
|---|---|---|---|
| Dashboard | Tổng quan dashboard | `3_Admin_Flows/01-Dashboard_Tong_Quan` | Đã có prototype |
| Tour | Danh sách/tạo/sửa/chi tiết tour | `3_Admin_Flows/09.1` - `09.4` | Đã có prototype |
| Tour | Danh mục tour | `3_Admin_Flows/09.5-Danh_Muc_Tour` | Đã có prototype |
| Tour | Lịch khởi hành | `3_Admin_Flows/09.6` - `09.8` | Đã có prototype |
| Địa điểm | Danh sách/tạo/sửa/chi tiết địa điểm | `3_Admin_Flows/03.1` - `03.4` | Đã có prototype |
| Địa điểm | Danh mục địa điểm | `3_Admin_Flows/05.*-Danh_Muc_Con` | Có một phần |
| Địa điểm | Danh mục con | `3_Admin_Flows/05.*-Danh_Muc_Con` | Đã có prototype |
| Đơn hàng | Danh sách/chi tiết đơn hàng | `3_Admin_Flows/10.1`, `10.2` | Đã có prototype |
| Thanh toán | Danh sách/chi tiết giao dịch | `3_Admin_Flows/06.1`, `06.2` | Đã có prototype |
| Đánh giá | Danh sách đánh giá | `3_Admin_Flows/07.3-Danh_Sach_Danh_Gia` | Đã có prototype |
| Người dùng | Danh sách/tạo/sửa/chi tiết người dùng | `3_Admin_Flows/04.1` - `04.4` | Đã có prototype |
| Blog | Danh sách/tạo/sửa bài viết | `3_Admin_Flows/02.1`, `11.1`, `11.2` | Đã có prototype |
| Blog | Danh mục blog | `3_Admin_Flows/11.3-Danh_Muc_Blog` | Đã có prototype |
| Tags & tiện ích | Tags/amenities | `3_Admin_Flows/08.1-Tags_Tien_Ich` | Đã có prototype |
| Khuyến mãi | Danh sách/tạo/sửa khuyến mãi | Chưa có file riêng | Planned |
| Thông báo | Danh sách/gửi thông báo | `3_Admin_Flows/12.1`, `12.2` | Đã có prototype |
| Liên hệ | Danh sách/chi tiết trả lời | `3_Admin_Flows/13.1`, `13.2` | Đã có prototype |
| Cấu hình | Cấu hình website | Chưa có file riêng | Planned |
| Cấu hình | Landing pages | Chưa có file riêng | Planned |
| Báo cáo | Báo cáo đơn hàng | `3_Admin_Flows/07.1-Bao_Cao_Don_Hang` | Đã có prototype |
| Báo cáo | Báo cáo doanh thu | `3_Admin_Flows/07.2-Bao_Cao_Doanh_Thu` | Đã có prototype |
| Báo cáo | Báo cáo đánh giá | Chưa có file riêng | Cần bổ sung |
| Báo cáo | Báo cáo địa điểm | Chưa có file riêng | Cần bổ sung |
| Báo cáo | Báo cáo người dùng | Chưa có file riêng | Cần bổ sung |

---

## 5. Màn hệ thống dùng chung

| Màn | Prototype hiện có | Trạng thái |
|---|---|---|
| 403 | `4_Others/01-Trang_403` | Đã có prototype |
| 404 | `4_Others/02-Trang_404` | Đã có prototype |
| Bảo trì | `4_Others/03-Trang_Bao_Tri` | Đã có prototype |
| Pagination component | `4_Others/04-Pagination_Components` | Đã có prototype |
| Style guide | `4_Others/05-Style_Guide` | Đã có prototype |

---

## 6. Việc cần làm để đồng bộ hoàn toàn

### Ưu tiên cao

1. Bổ sung prototype auth: đăng nhập, đăng ký, quên mật khẩu, đặt lại mật khẩu.
2. Bổ sung user booking theo mã đơn và hóa đơn PDF.
3. Bổ sung blog detail và blog theo danh mục.
4. Bổ sung chọn lịch khởi hành tour và tour theo danh mục.
5. Bổ sung 3 báo cáo admin: đánh giá, địa điểm, người dùng.

### Ưu tiên trung bình

1. Tách rõ landing tour Đà Nẵng khỏi màn giới thiệu Đà Nẵng.
2. Tách rõ trang chủ user có gợi ý cá nhân khỏi trang chủ guest.
3. Tách rõ danh mục địa điểm và danh mục con trong admin.
4. Tạo prototype cho các màn planned khi API/database đã sẵn sàng: cart, promotions, settings, landing pages.

---

## 7. File mapping chi tiết

Xem thêm: `4_Others/01-Screen_To_Docs_Mapping.md`.
