# Admin chi tiết booking - Test Cases

## 1. Tổng quan màn hình

* Đường dẫn route: `/admin/bookings/detail/:id`
* File source chính: `D:\DATN\danangtrip-admin\src\pages\Bookings\BookingDetail\index.tsx`
* Component liên quan: `BookingStatusBadge`, `PaymentStatusBadge`, `BookingCancelDialog`, `VirtualTimeline`, `PassengerListPlaceholder`, `Breadcrumbs`
* API/service sử dụng: `bookingApi.getDetail(id)`, `bookingApi.updateStatus(id)`, `bookingApi.getInvoice(id)`
* Quyền truy cập: Admin qua `PrivateRoute`; source chỉ cho role admin theo `PrivateRoute`.
* Mục đích màn hình: Cho admin xem thông tin đặt tour, khách hàng, tour, hành khách, thanh toán, timeline; xác nhận, hoàn thành, hủy booking và tải hóa đơn.

## 2. Điều kiện tiền đề

* Dữ liệu cần có: booking pending, confirmed, completed, cancelled; booking có/không có note/address/thumbnail/schedule/departurePlace.
* Tài khoản cần dùng: admin hợp lệ; user/staff nếu muốn kiểm tra guard.
* Trạng thái hệ thống: API booking detail/update/invoice hoạt động.
* Quyền user/admin/staff: admin được vào; user không được vào admin; staff theo source hiện tại không qua `hasRole(user,'admin')` nếu role không phải admin.

## 3. Danh sách chức năng chính

* Load booking detail theo id.
* Hiển thị sticky header, breadcrumb, mã booking, booking/payment status.
* Hiển thị customer card, booked tour details, passenger breakdown, payment summary.
* Hiển thị virtual timeline theo booked/confirmed/completed/cancelled.
* Confirm pending booking.
* Complete confirmed booking với `window.confirm`.
* Cancel booking qua dialog nhập lý do.
* Download invoice.
* Error state có Back và Retry.

## 4. Test cases chi tiết

| ID | Nhóm chức năng | Test case | Tiền điều kiện | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Mức độ ưu tiên | Loại test |
| -- | -------------- | --------- | -------------- | -------------- | ------------ | ---------------- | -------------- | --------- |
| ADMIN_BOOKING_DETAIL_001 | Permission | Guest vào route admin | Chưa đăng nhập | 1. Mở `/admin/bookings/detail/1`. | guest | Bị redirect `/login`; không thấy data booking. | High | Permission |
| ADMIN_BOOKING_DETAIL_002 | Permission | User thường vào route admin | Đăng nhập role user | 1. Mở route detail. | user | Bị chặn bởi PrivateRoute; không render BookingDetail. | High | Permission |
| ADMIN_BOOKING_DETAIL_003 | Load dữ liệu | Admin mở booking hợp lệ | Booking tồn tại | 1. Login admin.<br>2. Mở `/admin/bookings/detail/1001`. | id=1001 | Header, badges, customer, tour, passenger, payment, timeline hiển thị đúng. | High | Functional |
| ADMIN_BOOKING_DETAIL_004 | Loading | Skeleton khi API chậm | Delay detail | 1. Mở route. | delay | Hiển thị skeleton grid; không hiển thị nội dung rỗng. | Medium | UI |
| ADMIN_BOOKING_DETAIL_005 | Invalid id | Booking không tồn tại | ID sai | 1. Mở `/admin/bookings/detail/999999`. | invalid | Hiển thị error card, Back và Retry. | High | Negative |
| ADMIN_BOOKING_DETAIL_006 | Retry | Retry sau lỗi | API lỗi rồi phục hồi | 1. Mở lỗi.<br>2. Click Retry. | 500->200 | Gọi refetch và hiển thị data sau khi thành công. | Medium | API |
| ADMIN_BOOKING_DETAIL_007 | Back | Quay về danh sách | Detail đang mở | 1. Click Back. | | Điều hướng `/admin/bookings`. | Medium | Functional |
| ADMIN_BOOKING_DETAIL_008 | Header badges | Hiển thị status badges | Booking có status/payment | 1. Quan sát header. | pending/unpaid | BookingStatusBadge và PaymentStatusBadge đúng status/màu. | High | UI |
| ADMIN_BOOKING_DETAIL_009 | Customer full | Thông tin khách đầy đủ | Booking có name/email/phone/address/note | 1. Quan sát customer card. | full | Tên, email, phone, address, note hiển thị đúng. | High | Functional |
| ADMIN_BOOKING_DETAIL_010 | Customer missing address | Thiếu địa chỉ | address null | 1. Mở detail. | null | Hiển thị fallback `address_missing`, không undefined. | Medium | Edge Case |
| ADMIN_BOOKING_DETAIL_011 | Customer missing note | Thiếu ghi chú | note null | 1. Mở detail. | null | Hiển thị `no_note`, không trống xấu. | Low | Edge Case |
| ADMIN_BOOKING_DETAIL_012 | Tour thumbnail | Tour có ảnh | item.tour.thumbnail có URL | 1. Quan sát tour card. | thumbnail | Ảnh hiển thị đúng kích thước, alt là tên tour. | Medium | UI |
| ADMIN_BOOKING_DETAIL_013 | Tour no thumbnail | Tour thiếu ảnh | thumbnail null | 1. Mở detail. | null | Hiển thị fallback icon ShoppingBag. | Medium | Edge Case |
| ADMIN_BOOKING_DETAIL_014 | Tour schedule | Hiển thị lịch khởi hành | Có travelDate/departurePlace/scheduleId | 1. Quan sát grid schedule. | full | Travel date format đúng locale, departure place, schedule code hiển thị. | High | Functional |
| ADMIN_BOOKING_DETAIL_015 | Missing departure place | Thiếu điểm khởi hành | departurePlace null | 1. Mở detail. | null | Hiển thị `departure_place_missing`. | Medium | Edge Case |
| ADMIN_BOOKING_DETAIL_016 | Passenger totals | Tính tổng hành khách | Booking nhiều items | 1. Quan sát PassengerListPlaceholder. | 2 items | Adults/children/infants bằng tổng các booking items. | High | Functional |
| ADMIN_BOOKING_DETAIL_017 | Passenger zero | Không có trẻ em/em bé | child=0, infant=0 | 1. Mở detail. | 0 | Hiển thị 0, không ẩn sai hoặc NaN. | Medium | Edge Case |
| ADMIN_BOOKING_DETAIL_018 | Payment summary | Tổng tiền | Booking có total/discount/deposit/final | 1. Quan sát payment card. | full | Format tiền đúng; discount âm; final amount nổi bật. | High | Functional |
| ADMIN_BOOKING_DETAIL_019 | Payment zero discount | Discount 0 | discount=0 | 1. Mở detail. | 0 | Hiển thị `- 0 ₫` hoặc format nhất quán, không NaN. | Low | Edge Case |
| ADMIN_BOOKING_DETAIL_020 | Timeline booked | Mốc booked | Booking mới | 1. Quan sát timeline. | bookedAt | Mốc booked luôn completed và có ngày. | Medium | UI |
| ADMIN_BOOKING_DETAIL_021 | Timeline confirmed | Mốc confirmed | confirmedAt có giá trị | 1. Mở confirmed. | confirmed | Mốc confirmed active, ngày đúng. | Medium | UI |
| ADMIN_BOOKING_DETAIL_022 | Timeline completed | Mốc completed | completedAt/status completed | 1. Mở completed. | completed | Mốc completed active; operations hiển thị terminal notice. | High | UI |
| ADMIN_BOOKING_DETAIL_023 | Timeline cancelled | Mốc cancelled | status cancelled | 1. Mở cancelled. | reason | Timeline thêm mốc cancelled và hiển thị reason nếu có. | High | UI |
| ADMIN_BOOKING_DETAIL_024 | Confirm visible | Nút confirm chỉ hiện pending | Booking pending | 1. Mở detail. | pending | Nút confirm hiển thị; complete không hiển thị. | High | Functional |
| ADMIN_BOOKING_DETAIL_025 | Confirm action | Xác nhận booking | Booking pending | 1. Click Confirm. | pending | Gọi `updateStatus` với `confirmed`; toast success; query cập nhật. | High | Functional |
| ADMIN_BOOKING_DETAIL_026 | Confirm API lỗi | Confirm thất bại | API 500 | 1. Click Confirm. | 500 | Toast update_error; status UI không đổi sai. | High | API |
| ADMIN_BOOKING_DETAIL_027 | Complete visible | Nút complete chỉ hiện confirmed | Booking confirmed | 1. Mở detail. | confirmed | Nút complete hiển thị; confirm không hiển thị. | High | Functional |
| ADMIN_BOOKING_DETAIL_028 | Complete cancel window confirm | Admin hủy confirm browser | Booking confirmed | 1. Click complete.<br>2. Chọn Cancel ở browser confirm. | | Không gọi API updateStatus. | Medium | Negative |
| ADMIN_BOOKING_DETAIL_029 | Complete action | Hoàn thành booking | Booking confirmed | 1. Click complete.<br>2. Xác nhận browser confirm. | confirmed | Gọi status `completed`; nút loading; toast success. | High | Functional |
| ADMIN_BOOKING_DETAIL_030 | Complete API lỗi | Complete thất bại | API 500 | 1. Confirm complete. | 500 | Toast update_error; `isCompleting` trở về false. | High | API |
| ADMIN_BOOKING_DETAIL_031 | Cancel visible | Nút cancel hiện với non-terminal | Booking pending/confirmed | 1. Mở detail. | pending | Nút cancel hiển thị trong operations. | High | Functional |
| ADMIN_BOOKING_DETAIL_032 | Cancel reason valid | Hủy booking | Booking pending | 1. Click Cancel.<br>2. Nhập lý do.<br>3. Submit. | `Khách yêu cầu hủy` | Gọi updateStatus `cancelled` kèm reason; toast success; dialog đóng. | High | Functional |
| ADMIN_BOOKING_DETAIL_033 | Cancel reason empty | Lý do trống | Dialog mở | 1. Submit không nhập lý do. | empty | Dialog validation chặn hoặc không gửi API. | High | Validation |
| ADMIN_BOOKING_DETAIL_034 | Cancel API lỗi | Hủy thất bại | API 500 | 1. Submit reason. | 500 | Toast update_error; dialog/booking không cập nhật sai. | High | API |
| ADMIN_BOOKING_DETAIL_035 | Terminal completed | Booking completed | status completed | 1. Mở detail. | completed | Không hiển thị confirm/complete/cancel; có notice completed. | High | Regression |
| ADMIN_BOOKING_DETAIL_036 | Terminal cancelled | Booking cancelled | status cancelled | 1. Mở detail. | cancelled | Không hiển thị action; có notice cancelled. | High | Regression |
| ADMIN_BOOKING_DETAIL_037 | Invoice download | Tải hóa đơn | Booking có invoice | 1. Click invoice. | id | Gọi `getInvoice`; tải file fallback `hoa_don_{code}.pdf`; toast export_success. | High | Functional |
| ADMIN_BOOKING_DETAIL_038 | Invoice API lỗi | Invoice lỗi | API 500 | 1. Click invoice. | 500 | Toast export_error; button hết loading. | Medium | API |
| ADMIN_BOOKING_DETAIL_039 | Responsive | Layout mobile/tablet | Viewport 375/768 | 1. Mở detail.<br>2. Quan sát sticky header, grid. | mobile | Header không tràn; layout chuyển 1 cột; actions vẫn dùng được. | Medium | Responsive |
| ADMIN_BOOKING_DETAIL_040 | Regression full lifecycle | Pending -> confirmed -> completed | Booking test pending | 1. Mở detail.<br>2. Confirm.<br>3. Refetch.<br>4. Complete. | pending | Trạng thái chuyển đúng, action thay đổi đúng, timeline cập nhật. | High | Regression |

## 5. Test data đề xuất

* Booking pending unpaid, confirmed paid, completed success, cancelled có lý do.
* Booking nhiều items để test passenger totals.
* Booking thiếu thumbnail/address/note/departurePlace.
* Admin account hợp lệ; user thường để test guard.

## 6. Checklist regression

* Chỉ admin vào được route.
* Confirm/complete/cancel chỉ hiện đúng trạng thái.
* Timeline không sai mốc ngày.
* Invoice không treo loading khi lỗi.
* Customer/tour/payment card không lộ undefined/NaN.
* Mobile không tràn header.

## 7. Ghi chú kỹ thuật

* Logic lấy từ `BookingDetail/index.tsx`.
* API lấy từ `bookingApi.ts`.
* Rủi ro cao: trạng thái terminal, browser confirm complete, hủy không validate đủ lý do, invoice blob.
