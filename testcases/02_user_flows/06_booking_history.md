# Chi tiết booking của người dùng - Test Cases

## 1. Tổng quan màn hình

* Đường dẫn route: `/[locale]/profile/bookings/[id]`, `/[locale]/profile/bookings/code/[bookingCode]`
* File source chính: `D:\DATN\danangtrip-web\src\app\[locale]\(main)\(protected)\profile\bookings\[id]\page.tsx`, `D:\DATN\danangtrip-web\src\app\[locale]\(main)\(protected)\profile\bookings\code\[bookingCode]\page.tsx`
* Component liên quan: `BookingDetailClient`, `BookingStatusTimeline`, `BookingTourInfoCard`, `BookingCustomerInfoCard`, `BookingPriceSummaryCard`, `CancelBookingDialog`
* API/service sử dụng: `bookingService.detail(id)`, `bookingService.detailByCode(bookingCode)`, `bookingService.invoice(id)`, `bookingService.cancel(id)`, `paymentService.retry(bookingCode)`
* Quyền truy cập: User đã đăng nhập; guest bị protected layout chặn
* Mục đích màn hình: Cho người dùng xem chi tiết booking, tải/in hóa đơn, hủy booking nếu còn hợp lệ, tiếp tục thanh toán và đặt lại tour đã hủy.

## 2. Điều kiện tiền đề

* Dữ liệu cần có: booking của user hiện tại với trạng thái pending, confirmed, completed, cancelled; payment status success, pending, failed, unpaid, partially_paid.
* Tài khoản cần dùng: user sở hữu booking; user khác không sở hữu booking; guest.
* Trạng thái hệ thống: API booking, invoice và payment retry hoạt động.
* Quyền user/admin/staff: user chỉ xem booking của mình; admin/staff không dùng màn này.

## 3. Danh sách chức năng chính

* Load booking detail theo id hoặc bookingCode.
* Hiển thị loading skeleton, error/empty state.
* Hiển thị timeline trạng thái booking.
* Hiển thị thông tin tour, khách hàng, tổng tiền.
* Tải hóa đơn khi payment success.
* In hóa đơn bằng `window.print()`.
* Hủy booking khi pending/confirmed và chưa qua ngày đi.
* Tiếp tục thanh toán với gateway online.
* Hiển thị lý do hủy và CTA đặt lại khi booking cancelled.

## 4. Test cases chi tiết

| ID | Nhóm chức năng | Test case | Tiền điều kiện | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Mức độ ưu tiên | Loại test |
| -- | -------------- | --------- | -------------- | -------------- | ------------ | ---------------- | -------------- | --------- |
| USER_BOOKING_DETAIL_001 | Auth | Guest truy cập detail | Chưa đăng nhập | 1. Mở `/vi/profile/bookings/1`. | guest | Protected route chuyển sang login hoặc chặn truy cập; không gọi detail với token rỗng. | High | Permission |
| USER_BOOKING_DETAIL_002 | Load theo id | Mở detail bằng id hợp lệ | User sở hữu booking | 1. Mở `/vi/profile/bookings/101`.<br>2. Chờ load. | id=101 | Header, booking code, timeline, tour card, customer card, price summary hiển thị đúng. | High | Functional |
| USER_BOOKING_DETAIL_003 | Load theo code | Mở detail bằng bookingCode | User sở hữu booking | 1. Mở `/vi/profile/bookings/code/BK20260601001`. | bookingCode | Dữ liệu giống route id; breadcrumb hiển thị booking detail. | High | Functional |
| USER_BOOKING_DETAIL_004 | Invalid id | Booking id không tồn tại | User đăng nhập | 1. Mở `/vi/profile/bookings/999999`. | invalid id | Hiển thị error/empty card, nút quay lại danh sách và retry. | High | Negative |
| USER_BOOKING_DETAIL_005 | Không sở hữu | User xem booking người khác | Booking thuộc user khác | 1. Mở detail id của user khác. | id khác owner | API 403/404; UI không lộ dữ liệu booking; có error/back. | High | Permission |
| USER_BOOKING_DETAIL_006 | Loading | Skeleton khi API chậm | Delay API | 1. Mở detail. | delay 2s | Hiển thị skeleton header/timeline/tour/customer/summary; không nhấp nháy data cũ. | Medium | UI |
| USER_BOOKING_DETAIL_007 | Retry | Retry sau lỗi API | Mock lỗi rồi phục hồi | 1. Mở detail lỗi.<br>2. Click Retry. | 500 -> 200 | Gọi lại API và render data sau khi thành công. | Medium | API |
| USER_BOOKING_DETAIL_008 | Back | Quay lại danh sách booking | Detail đang mở | 1. Click nút back. | | Điều hướng về `/profile/bookings` đúng locale. | Medium | Functional |
| USER_BOOKING_DETAIL_009 | Timeline pending | Timeline booking pending | Booking pending | 1. Mở detail pending.<br>2. Quan sát timeline. | pending | Mốc pending/current hiển thị đúng; mốc sau chưa completed. | High | UI |
| USER_BOOKING_DETAIL_010 | Timeline confirmed | Timeline booking confirmed | Booking confirmed | 1. Mở detail confirmed. | confirmed | Timeline thể hiện đã xác nhận; action hủy còn hiển thị nếu chưa qua ngày. | High | UI |
| USER_BOOKING_DETAIL_011 | Timeline completed | Timeline booking completed | Booking completed | 1. Mở detail completed. | completed | Timeline completed; không hiển thị nút hủy; có thể tải invoice nếu paid. | High | UI |
| USER_BOOKING_DETAIL_012 | Timeline cancelled | Timeline booking cancelled | Booking cancelled | 1. Mở detail cancelled. | cancelled | Hiển thị trạng thái cancelled, lý do hủy nếu có, CTA đặt lại nếu có tour slug. | High | UI |
| USER_BOOKING_DETAIL_013 | Tour card | Hiển thị tour info | Booking có item tour | 1. Quan sát BookingTourInfoCard. | item có thumbnail | Hiển thị ảnh/tên tour/ngày đi/số lượng; ảnh fallback nếu thiếu thumbnail. | High | Functional |
| USER_BOOKING_DETAIL_014 | Thiếu item | Booking không có item | API trả booking_items rỗng | 1. Mở detail. | items=[] | UI hiển thị error/empty vì source yêu cầu `item`; không crash. | High | Edge Case |
| USER_BOOKING_DETAIL_015 | Customer info | Hiển thị khách hàng | Booking có customer fields | 1. Quan sát BookingCustomerInfoCard. | name/email/phone | Hiển thị đúng thông tin khách, address/note fallback nếu trống. | Medium | Functional |
| USER_BOOKING_DETAIL_016 | Price summary | Hiển thị tổng tiền | Booking có discount/deposit | 1. Quan sát summary. | total/discount/final | Tiền format VND đúng; không NaN khi discount=0. | High | Functional |
| USER_BOOKING_DETAIL_017 | Invoice unpaid | Tải hóa đơn khi chưa paid | payment_status != success | 1. Click download invoice. | pending/unpaid | Toast warning `invoice_unpaid_error`; không gọi download blob. | High | Validation |
| USER_BOOKING_DETAIL_018 | Invoice success | Tải hóa đơn thành công | payment_status success | 1. Click download invoice. | success | Gọi `bookingService.invoice`; tải file `invoice-{booking_code}.pdf`; toast success. | High | Functional |
| USER_BOOKING_DETAIL_019 | Invoice 401 | Tải invoice khi token hết hạn | Token expired | 1. Click download invoice. | 401 | Điều hướng login theo source; không treo loading. | High | Permission |
| USER_BOOKING_DETAIL_020 | Invoice blob lỗi | API invoice trả blob lỗi JSON | Mock lỗi blob | 1. Click download invoice. | error blob | Parse message từ blob nếu có; toast lỗi rõ ràng. | Medium | API |
| USER_BOOKING_DETAIL_021 | Invoice empty | API invoice trả rỗng | Mock empty blob | 1. Click download invoice. | empty | Toast lỗi server; không tạo file hỏng. | Medium | Negative |
| USER_BOOKING_DETAIL_022 | Print | In hóa đơn | Detail loaded | 1. Click print icon. | | Gọi `window.print()`; print-only header hiển thị khi in; action buttons ẩn trong print. | Medium | Functional |
| USER_BOOKING_DETAIL_023 | Can cancel pending | Hủy booking pending | pending, travelDate tương lai | 1. Click cancel.<br>2. Nhập lý do hợp lệ.<br>3. Submit. | lý do >= 10 ký tự | Gọi `bookingService.cancel`; dialog đóng; detail refetch; status cancelled. | High | Functional |
| USER_BOOKING_DETAIL_024 | Can cancel confirmed | Hủy booking confirmed | confirmed, chưa qua ngày đi | 1. Click cancel.<br>2. Submit reason. | confirmed | Hủy thành công nếu API cho phép; slot được backend xử lý; UI cập nhật. | High | Functional |
| USER_BOOKING_DETAIL_025 | Cannot cancel completed | Không hủy completed | completed | 1. Mở detail. | completed | Nút cancel không hiển thị. | High | Permission |
| USER_BOOKING_DETAIL_026 | Cannot cancel cancelled | Không hủy booking đã hủy | cancelled | 1. Mở detail. | cancelled | Nút cancel không hiển thị; chỉ hiển thị lý do/đặt lại. | High | Permission |
| USER_BOOKING_DETAIL_027 | Cannot cancel past date | Không hủy khi ngày đi đã qua | pending/confirmed nhưng travelDate quá khứ | 1. Mở detail. | travelDate yesterday | Nút cancel không hiển thị do `isPast=true`. | High | Edge Case |
| USER_BOOKING_DETAIL_028 | Cancel reason invalid | Lý do hủy quá ngắn | Có thể hủy | 1. Mở dialog.<br>2. Nhập dưới 10 ký tự.<br>3. Submit. | `Hủy` | Validation `cancel_reason_min_error`; không gọi API. | High | Validation |
| USER_BOOKING_DETAIL_029 | Cancel API lỗi | API cancel lỗi | Có thể hủy | 1. Submit lý do hợp lệ khi API 500. | 500 | Dialog không đóng hoặc hiển thị lỗi; status không đổi. | High | API |
| USER_BOOKING_DETAIL_030 | Retry payment visible | Booking còn nợ online | payment_method online, status pending/failed/unpaid/partially_paid, booking không cancelled | 1. Mở detail. | payos + failed | Panel continue payment hiển thị. | High | Functional |
| USER_BOOKING_DETAIL_031 | Retry payment hidden COD/bank | Payment method không online | bank_transfer hoặc booking cancelled | 1. Mở detail. | bank_transfer | Panel continue payment không hiển thị nếu không thuộc online methods hoặc đã cancelled. | Medium | Edge Case |
| USER_BOOKING_DETAIL_032 | Select retry gateway | Chọn cổng thanh toán lại | Panel hiển thị | 1. Click PayOS/VNPAY/MoMo/ZaloPay. | gateways enabled | Gateway active được highlight; không đổi booking data. | High | Functional |
| USER_BOOKING_DETAIL_033 | Retry payment success | Retry trả payment_url | Panel hiển thị | 1. Chọn gateway.<br>2. Click continue payment. | payment_url | Gọi `paymentService.retry` với bookingCode/payment_method; redirect đến URL. | High | Functional |
| USER_BOOKING_DETAIL_034 | Retry payment missing URL | API retry không trả URL | Panel hiển thị | 1. Click retry. | no URL | Toast lỗi payment link; không redirect undefined. | High | Negative |
| USER_BOOKING_DETAIL_035 | Retry payment API lỗi | API retry 500 | Panel hiển thị | 1. Click retry. | 500 | Toast retry_failed; nút hết loading. | High | API |
| USER_BOOKING_DETAIL_036 | App config gateway | Cổng bị tắt | appConfig payment momo=false | 1. Mở detail.<br>2. Quan sát options. | momo disabled | Cổng tắt không hiển thị; fallback PayOS nếu method hiện tại không enabled. | Medium | Edge Case |
| USER_BOOKING_DETAIL_037 | Rebook cancelled | Đặt lại booking đã hủy | Booking cancelled và item.tour.slug có giá trị | 1. Click nút đặt lại. | tour slug | Điều hướng `/tours/{slug}` đúng locale. | Medium | Functional |
| USER_BOOKING_DETAIL_038 | Rebook missing slug | Booking cancelled thiếu tour slug | tour null/slug null | 1. Mở detail. | no tour | Không hiển thị nút đặt lại hoặc không crash. | Medium | Edge Case |
| USER_BOOKING_DETAIL_039 | Locale route | Detail booking tiếng Anh | Locale en | 1. Mở `/en/profile/bookings/101`. | en | Text dịch theo locale; back/rebook/payment giữ locale. | Medium | Regression |
| USER_BOOKING_DETAIL_040 | Responsive | Detail trên mobile | Viewport 375px | 1. Mở detail.<br>2. Kiểm tra action icons, summary, timeline. | mobile | Layout 1 cột, action không tràn, timeline không bị cắt, print hidden đúng. | High | Responsive |

## 5. Test data đề xuất

* Booking pending online unpaid, confirmed paid, completed success, cancelled có lý do.
* Booking có item thiếu ảnh, item rỗng, booking của user khác.
* Payment methods: payos, vnpay, momo, zalopay, bank_transfer.
* Invoice API: success blob, 401, error blob JSON, empty response.

## 6. Checklist regression

* User không xem được booking của người khác.
* Invoice chỉ tải khi payment_status success.
* Hủy booking chỉ hiện khi pending/confirmed và chưa qua ngày đi.
* Retry payment không hiện cho cancelled/bank_transfer.
* Route id và route bookingCode cùng render đúng.
* Mobile không vỡ timeline/summary.

## 7. Ghi chú kỹ thuật

* Logic route lấy từ `profile/bookings/[id]/page.tsx` và `profile/bookings/code/[bookingCode]/page.tsx`.
* Client logic lấy từ `BookingDetailClient.tsx`.
* Validation hủy lấy từ `cancelBookingSchema` trong `booking.schema.ts`.
* Rủi ro cao: quyền sở hữu booking, invoice blob error, retry payment redirect, điều kiện `isPast` tính theo client date.
