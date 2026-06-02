# Kết quả thanh toán - Test Cases

## 1. Tổng quan màn hình

* Đường dẫn route: `/[locale]/payment/result`
* File source chính: `D:\DATN\danangtrip-web\src\app\[locale]\(main)\(protected)\payment\result\page.tsx`
* Component liên quan: `PaymentClient`, `PaymentStatusCard`, `PaymentSummaryCard`, `PaymentRetryPanel`, `PaymentActions`
* API/service sử dụng: `paymentService.status(transactionCode)`, `bookingService.detailByCode(bookingCode)`, `paymentService.retry(bookingCode)`
* Quyền truy cập: User đã đăng nhập
* Mục đích màn hình: Hiển thị kết quả thanh toán theo transaction_code/booking_code, cho phép retry khi pending/failed và điều hướng sau thanh toán.

## 2. Điều kiện tiền đề

* Dữ liệu cần có: transaction success/pending/failed/refunded; booking payment success/pending/failed.
* Tài khoản cần dùng: user sở hữu booking; guest để test protected.
* Trạng thái hệ thống: payment status API, booking detail by code API, retry payment API hoạt động.
* Quyền user/admin/staff: user protected; admin/staff không dùng màn này.

## 3. Danh sách chức năng chính

* Đọc query params `transaction_code` và `booking_code`.
* Fetch payment status khi có transaction_code.
* Fetch booking detail khi có booking_code.
* Xác định status UI: pending, success, failed, redirecting.
* Poll payment status mỗi 3 giây khi pending/partially_paid.
* Hiển thị summary booking nếu có booking data.
* Hiển thị retry panel khi failed/pending và có booking.
* Điều hướng hành động qua PaymentActions.

## 4. Test cases chi tiết

| ID | Nhóm chức năng | Test case | Tiền điều kiện | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Mức độ ưu tiên | Loại test |
| -- | -------------- | --------- | -------------- | -------------- | ------------ | ---------------- | -------------- | --------- |
| PAYMENT_RESULT_001 | Auth | Guest truy cập payment result | Chưa đăng nhập | 1. Mở `/vi/payment/result?booking_code=BK001`. | guest | Protected route chặn/redirect login; không lộ dữ liệu booking. | High | Permission |
| PAYMENT_RESULT_002 | Missing context | Không có query params | User đăng nhập | 1. Mở `/vi/payment/result`. | no params | Hiển thị failed status với message `errors.missing_context`; action cho missing context. | High | Negative |
| PAYMENT_RESULT_003 | Loading payment | Có transaction_code, API đang tải | Delay payment status | 1. Mở route có transaction_code. | transaction_code=TXN1 | Hiển thị PaymentLoadingState skeleton/status loading. | Medium | UI |
| PAYMENT_RESULT_004 | Loading booking | Có booking_code, API đang tải | Delay booking detail | 1. Mở route có booking_code. | booking_code=BK001 | Hiển thị loading state đến khi booking data về. | Medium | UI |
| PAYMENT_RESULT_005 | Payment success only | Payment success, không có booking | API payment success | 1. Mở `?transaction_code=TXN_SUCCESS`. | success | Status success; message `success_without_booking`; không hiển thị summary. | High | Functional |
| PAYMENT_RESULT_006 | Payment pending | Payment status pending | API trả pending | 1. Mở transaction pending.<br>2. Theo dõi refetch. | pending | Status card pending; query poll mỗi 3 giây cho đến khi status đổi. | High | API |
| PAYMENT_RESULT_007 | Payment partially paid | Payment partially_paid | API trả partially_paid | 1. Mở transaction.<br>2. Theo dõi polling. | partially_paid | Vẫn được coi là pending và refetch interval 3000ms. | High | Edge Case |
| PAYMENT_RESULT_008 | Payment failed | Payment failed | API trả failed | 1. Mở transaction failed. | failed | Status card failed; không polling tiếp. | High | Functional |
| PAYMENT_RESULT_009 | Payment refunded | Payment refunded | API trả refunded | 1. Mở transaction refunded. | refunded | UI map sang failed theo source; không hiển thị như success. | High | Edge Case |
| PAYMENT_RESULT_010 | Payment not found | Không có paymentData/bookingData | API null/404 | 1. Mở transaction không tồn tại. | invalid txn | Status failed, message `errors.payment_not_found`. | High | Negative |
| PAYMENT_RESULT_011 | Booking success | Booking payment success | Có booking_code | 1. Mở `?booking_code=BK_SUCCESS`. | success | Status success; PaymentSummaryCard hiển thị booking. | High | Functional |
| PAYMENT_RESULT_012 | Booking failed | Booking payment failed | Có booking_code | 1. Mở `?booking_code=BK_FAILED`. | failed | Status failed; summary và retry panel hiển thị. | High | Functional |
| PAYMENT_RESULT_013 | Booking pending | Booking payment pending | Có booking_code | 1. Mở `?booking_code=BK_PENDING`. | pending | Status pending; summary và retry panel hiển thị. | High | Functional |
| PAYMENT_RESULT_014 | Both params success | Có cả transaction và booking | Cả hai API trả success | 1. Mở route có cả params. | TXN + BK | Status ưu tiên paymentData success; summary lấy bookingData. | High | Functional |
| PAYMENT_RESULT_015 | Both params payment failed booking success | Payment failed, booking success | Data lệch | 1. Mở route. | failed + success | Theo source status lấy paymentData trước: failed; summary vẫn hiện booking. Cần đánh dấu rủi ro nghiệp vụ. | High | Edge Case |
| PAYMENT_RESULT_016 | Retry visible failed | Retry panel khi failed có booking | bookingData failed | 1. Mở result failed.<br>2. Quan sát retry panel. | failed | PaymentRetryPanel hiển thị, có bookedAt và nút retry. | High | Functional |
| PAYMENT_RESULT_017 | Retry visible pending | Retry panel khi pending có booking | bookingData pending | 1. Mở result pending. | pending | Retry panel hiển thị. | Medium | Functional |
| PAYMENT_RESULT_018 | Retry hidden success | Không retry khi success | bookingData success | 1. Mở result success. | success | Không hiển thị PaymentRetryPanel. | High | Regression |
| PAYMENT_RESULT_019 | Retry hidden redirecting | Trạng thái redirecting | retry mutation pending | 1. Click retry.<br>2. Quan sát. | isRetrying=true | Status chuyển redirecting, summary/retry/actions ẩn theo source. | High | Functional |
| PAYMENT_RESULT_020 | Retry success | Retry trả payment_url | Failed booking | 1. Click retry. | payment_url | Gọi `paymentService.retry` với return_url; browser chuyển tới payment_url. | High | Functional |
| PAYMENT_RESULT_021 | Retry missing URL | Retry không trả payment_url | Failed booking | 1. Click retry. | no payment_url | Toast lỗi payment link; không redirect undefined. | High | Negative |
| PAYMENT_RESULT_022 | Retry API error | Retry API 500 | Failed booking | 1. Click retry. | 500 | Toast `errors.retry_failed`; trạng thái hết loading. | High | API |
| PAYMENT_RESULT_023 | Return URL locale vi | Retry ở locale vi | locale vi | 1. Click retry.<br>2. Inspect payload. | vi | return_url là `{origin}/payment/result` không có `/vi` theo source. | Medium | Regression |
| PAYMENT_RESULT_024 | Return URL locale en | Retry ở locale en | locale en | 1. Click retry.<br>2. Inspect payload. | en | return_url là `{origin}/en/payment/result`. | Medium | Regression |
| PAYMENT_RESULT_025 | Summary fields | Summary booking hiển thị đủ | BookingData đầy đủ | 1. Mở result với booking. | booking full | Hiển thị mã booking, tour, số tiền/trạng thái theo PaymentSummaryCard. | High | UI |
| PAYMENT_RESULT_026 | Summary missing data | Booking thiếu một số field | Mock thiếu thumbnail/tour | 1. Mở result. | partial booking | Summary có fallback, không NaN/undefined lộ ra UI. | Medium | Edge Case |
| PAYMENT_RESULT_027 | Actions success | Action sau success | Status success | 1. Quan sát PaymentActions.<br>2. Click từng action. | success | Action điều hướng xem booking hoặc về trang phù hợp theo component. | Medium | Functional |
| PAYMENT_RESULT_028 | Actions failed | Action sau failed | Status failed | 1. Quan sát PaymentActions. | failed | Action quay lại/tạo lại/thử lại đúng; không hiển thị action success sai. | Medium | Functional |
| PAYMENT_RESULT_029 | Actions missing context | Action khi thiếu context | No params | 1. Mở no params.<br>2. Click action. | no params | Điều hướng về trang an toàn, không cần booking id. | Medium | Negative |
| PAYMENT_RESULT_030 | API payment 500 | Payment status API lỗi | Mock 500 | 1. Mở transaction. | 500 | Không crash; status fallback failed/payment_not_found hoặc error boundary tùy hook. | High | API |
| PAYMENT_RESULT_031 | API booking 500 | Booking detail by code lỗi | Mock 500 | 1. Mở booking_code. | 500 | Không crash; status failed/payment_not_found hoặc fallback phù hợp. | High | API |
| PAYMENT_RESULT_032 | Poll stop success | Pending chuyển success | API pending rồi success | 1. Mở transaction pending.<br>2. Chờ poll. | pending -> success | UI chuyển success và dừng polling. | High | API |
| PAYMENT_RESULT_033 | Poll stop failed | Pending chuyển failed | API pending rồi failed | 1. Chờ poll. | pending -> failed | UI chuyển failed và dừng polling. | High | API |
| PAYMENT_RESULT_034 | Duplicate retry click | Click retry nhiều lần | Failed booking | 1. Double click retry. | | Mutation pending disabled/không gửi nhiều redirect request. | High | Regression |
| PAYMENT_RESULT_035 | Query param encoding | booking_code có ký tự đặc biệt | Booking code encoded | 1. Mở URL encoded. | `BK%2F001` | Hook nhận đúng bookingCode; API gọi đúng encoded/decoded theo browser. | Medium | Edge Case |
| PAYMENT_RESULT_036 | Back navigation | Điều hướng sau payment | Result loaded | 1. Click action quay về/home/booking. | | Route giữ locale và không mất session. | Medium | Functional |
| PAYMENT_RESULT_037 | Responsive desktop | Layout desktop | 1440px | 1. Mở result success/failed. | | Card căn giữa, max width 4xl, summary không lệch. | Low | Responsive |
| PAYMENT_RESULT_038 | Responsive mobile | Layout mobile | 375px | 1. Mở result.<br>2. Quan sát buttons. | mobile | Card, summary, retry/actions xếp dọc; không tràn ngang. | High | Responsive |
| PAYMENT_RESULT_039 | Accessibility | Loading và buttons | Result loaded | 1. Tab qua actions.<br>2. Kiểm tra focus. | | Action button focus được, không kẹt keyboard. | Low | UI |
| PAYMENT_RESULT_040 | Regression toàn flow | Từ booking online về result | Booking online | 1. Tạo booking PayOS.<br>2. Giả lập return về result với params.<br>3. Kiểm tra status. | valid | Result phản ánh đúng trạng thái backend và cho retry nếu failed/pending. | High | Regression |

## 5. Test data đề xuất

* Transaction: `TXN_SUCCESS`, `TXN_PENDING`, `TXN_FAILED`, `TXN_REFUNDED`, `TXN_INVALID`.
* Booking: `BK_SUCCESS`, `BK_PENDING`, `BK_FAILED`, `BK_PARTIAL`.
* Locale: vi và en để kiểm tra return_url.

## 6. Checklist regression

* Missing query không crash.
* Pending/partially_paid có polling 3 giây.
* Success không hiển thị retry.
* Retry redirect đúng payment_url.
* Summary booking không lộ undefined/NaN.
* Mobile không vỡ layout.

## 7. Ghi chú kỹ thuật

* Logic status mapping lấy từ `PaymentClient.tsx`.
* Retry/return_url lấy từ `usePayment.ts`.
* Rủi ro cao: paymentData và bookingData lệch trạng thái, polling không dừng, return_url locale, retry missing payment_url.
