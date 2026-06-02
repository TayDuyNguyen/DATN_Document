# Admin chi tiết thanh toán - Test Cases

## 1. Tổng quan màn hình

* Đường dẫn route: `/admin/payments/detail/:id`
* File source chính: `D:\DATN\danangtrip-admin\src\pages\Payments\PaymentDetail\index.tsx`
* Component liên quan: `PaymentGatewayBadge`, `PaymentStatusBadge`, `RefundPaymentDialog`, `VirtualTimeline`, `Breadcrumbs`
* API/service sử dụng: `paymentApi.getDetail(id)`, `paymentApi.refund(id)`
* Quyền truy cập: Admin qua `PrivateRoute`; refund chỉ enabled khi `user.role === 'admin'`
* Mục đích màn hình: Cho admin xem chi tiết giao dịch, booking/customer liên quan, timeline trạng thái và hoàn tiền giao dịch thành công.

## 2. Điều kiện tiền đề

* Dữ liệu cần có: payment success, failed, pending, refunded; payment có bookingId và payment orphan không booking.
* Tài khoản cần dùng: admin; staff/non-admin để test refund disabled; guest/user để test guard.
* Trạng thái hệ thống: API payment detail/refund hoạt động.
* Quyền user/admin/staff: admin được refund; non-admin không được refund.

## 3. Danh sách chức năng chính

* Load payment detail theo id.
* Hiển thị transactionCode, status, amount, gateway, transactionDate, paidAt/refundedAt/refundReason.
* Hiển thị booking/customer/tour block nếu có bookingId.
* Hiển thị orphan warning nếu không có bookingId.
* Timeline created/success/failed/refunded theo status.
* Refund payment success bằng dialog nhập reason, chỉ admin.
* Error/not found state và back to list.

## 4. Test cases chi tiết

| ID | Nhóm chức năng | Test case | Tiền điều kiện | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Mức độ ưu tiên | Loại test |
| -- | -------------- | --------- | -------------- | -------------- | ------------ | ---------------- | -------------- | --------- |
| ADMIN_PAYMENT_DETAIL_001 | Permission | Guest vào route | Chưa đăng nhập | 1. Mở `/admin/payments/detail/1`. | guest | Redirect login; không lộ payment data. | High | Permission |
| ADMIN_PAYMENT_DETAIL_002 | Permission | User thường vào route | Role user | 1. Mở route. | user | Bị chặn bởi PrivateRoute. | High | Permission |
| ADMIN_PAYMENT_DETAIL_003 | Load dữ liệu | Admin mở payment hợp lệ | Payment tồn tại | 1. Login admin.<br>2. Mở `/admin/payments/detail/2001`. | success | Header transactionCode, badge, payment info, booking/customer, timeline hiển thị. | High | Functional |
| ADMIN_PAYMENT_DETAIL_004 | Loading | Spinner khi API chậm | Delay API | 1. Mở route. | delay | Hiển thị spinner/loading text. | Medium | UI |
| ADMIN_PAYMENT_DETAIL_005 | Invalid id | Payment không tồn tại | ID sai | 1. Mở `/admin/payments/detail/999999`. | invalid | Hiển thị not found, mô tả và nút quay lại danh sách. | High | Negative |
| ADMIN_PAYMENT_DETAIL_006 | Back | Quay về danh sách | Detail đang mở | 1. Click back_to_list. | | Điều hướng `/admin/payments`. | Medium | Functional |
| ADMIN_PAYMENT_DETAIL_007 | Transaction code | Hiển thị mã giao dịch | Payment có transactionCode | 1. Quan sát header/card. | `TXN001` | Mã hiển thị ở header và payment info, không bị truncate mất dữ liệu quan trọng. | High | UI |
| ADMIN_PAYMENT_DETAIL_008 | Amount | Format số tiền | Payment amount > 0 | 1. Quan sát amount. | 1500000 | Format tiền đúng; màu nhấn theo UI. | High | UI |
| ADMIN_PAYMENT_DETAIL_009 | Amount zero | Amount bằng 0 | Payment amount 0 | 1. Mở detail. | 0 | Hiển thị 0 hợp lệ; không NaN/blank. | Medium | Edge Case |
| ADMIN_PAYMENT_DETAIL_010 | Gateway badge | Hiển thị gateway | Payment gateway payos/vnpay/momo | 1. Mở từng payment. | gateway | Badge đúng gateway, text không sai chữ hoa/thường. | Medium | UI |
| ADMIN_PAYMENT_DETAIL_011 | Created date | Thời gian khởi tạo | transactionDate có giá trị | 1. Quan sát field. | date | Format theo locale admin hiện tại. | Medium | UI |
| ADMIN_PAYMENT_DETAIL_012 | PaidAt | Hiển thị thời gian thanh toán | status success, paidAt có giá trị | 1. Mở success detail. | paidAt | Field paidAt hiển thị. | High | Functional |
| ADMIN_PAYMENT_DETAIL_013 | Missing paidAt | Success nhưng paidAt null | Data thiếu | 1. Mở detail. | paidAt null | Không render undefined; timeline fallback dùng createdAt nếu source dùng. | Medium | Edge Case |
| ADMIN_PAYMENT_DETAIL_014 | Refunded fields | Hiển thị refundedAt/reason | status refunded | 1. Mở refunded detail. | refunded | RefundedAt và refundReason hiển thị nếu có. | High | Functional |
| ADMIN_PAYMENT_DETAIL_015 | Missing refund reason | Refunded thiếu reason | refundReason null | 1. Mở detail. | null | Không lộ undefined; timeline dùng fallback reason rỗng. | Medium | Edge Case |
| ADMIN_PAYMENT_DETAIL_016 | Booking linked | Payment có bookingId | bookingId hợp lệ | 1. Quan sát block booking/customer. | bookingId | Hiển thị customer avatar/name/email, booking code, tour thumbnail/name. | High | Functional |
| ADMIN_PAYMENT_DETAIL_017 | Booking link | Click booking code | Payment có bookingId | 1. Click booking code link. | bookingId=1001 | Điều hướng `/admin/bookings/detail/1001`. | High | Functional |
| ADMIN_PAYMENT_DETAIL_018 | Customer avatar | Có avatar | customerAvatar URL | 1. Quan sát customer. | avatar | Ảnh avatar hiển thị; nếu null có icon User fallback. | Low | UI |
| ADMIN_PAYMENT_DETAIL_019 | Tour thumbnail | Có tour thumbnail | tourThumbnail URL | 1. Quan sát tour block. | thumbnail | Thumbnail hiển thị đúng; nếu null block vẫn ổn. | Low | UI |
| ADMIN_PAYMENT_DETAIL_020 | Orphan payment | Payment không có bookingId | bookingId null | 1. Mở detail orphan. | no booking | Hiển thị warning orphan; không render booking block rỗng. | High | Edge Case |
| ADMIN_PAYMENT_DETAIL_021 | Timeline created | Mốc created | Bất kỳ payment | 1. Quan sát timeline. | createdAt | Timeline luôn có mốc created. | Medium | UI |
| ADMIN_PAYMENT_DETAIL_022 | Timeline success | Payment success | status success | 1. Mở success. | success | Timeline có created + success, label gateway uppercase. | High | UI |
| ADMIN_PAYMENT_DETAIL_023 | Timeline failed | Payment failed | status failed | 1. Mở failed. | failed | Timeline có created + failed, icon/ màu lỗi. | High | UI |
| ADMIN_PAYMENT_DETAIL_024 | Timeline refunded | Payment refunded | status refunded | 1. Mở refunded. | refunded | Timeline có created + success + refunded. | High | UI |
| ADMIN_PAYMENT_DETAIL_025 | Refund visible | Admin xem success | Admin, status success | 1. Mở detail success. | success | Action refund hiển thị/enabled nếu không pending mutation. | High | Permission |
| ADMIN_PAYMENT_DETAIL_026 | Refund hidden non-success | Payment failed/pending/refunded | Admin | 1. Mở các status khác. | failed/pending/refunded | Không hiển thị action refund vì `isSuccess` false. | High | Regression |
| ADMIN_PAYMENT_DETAIL_027 | Refund disabled staff | Non-admin xem success | user.role != admin | 1. Mở success. | staff | Action refund disabled hoặc tooltip cảnh báo chỉ admin. | High | Permission |
| ADMIN_PAYMENT_DETAIL_028 | Open refund dialog | Mở dialog hoàn tiền | Admin, success | 1. Click Refund. | | Dialog mở, hiển thị thông tin payment và input reason. | High | Functional |
| ADMIN_PAYMENT_DETAIL_029 | Refund reason empty | Submit reason trống | Dialog mở | 1. Để trống reason.<br>2. Submit. | empty | Validation dialog chặn hoặc API không được gọi. | High | Validation |
| ADMIN_PAYMENT_DETAIL_030 | Refund reason valid | Hoàn tiền thành công | Admin, success | 1. Nhập lý do.<br>2. Submit. | `Khách hủy tour` | Gọi `paymentApi.refund` với `refund_reason`; toast success; dialog đóng. | High | Functional |
| ADMIN_PAYMENT_DETAIL_031 | Refund API lỗi | Hoàn tiền thất bại | Mock 500 | 1. Submit reason. | 500 | Toast error với `mapApiErrorMessage`; dialog không đóng sai. | High | API |
| ADMIN_PAYMENT_DETAIL_032 | Double refund | Click submit nhiều lần | Dialog đang submitting | 1. Double click submit. | | Chỉ gửi một request hoặc button disabled khi `isSubmitting`. | High | Regression |
| ADMIN_PAYMENT_DETAIL_033 | Refund already refunded | Payment đã refunded | status refunded | 1. Mở detail. | refunded | Không có action refund, tránh hoàn tiền lặp. | High | Regression |
| ADMIN_PAYMENT_DETAIL_034 | Status badge | Badge theo status | success/failed/pending/refunded | 1. Mở từng status. | statuses | Badge đúng status/màu; không sai mapping refunded. | Medium | UI |
| ADMIN_PAYMENT_DETAIL_035 | Error API detail | Detail API 500 | Mock 500 | 1. Mở route. | 500 | Hiển thị error/not found state, không crash. | High | API |
| ADMIN_PAYMENT_DETAIL_036 | Long transaction code | Mã giao dịch dài | transactionCode dài | 1. Mở detail. | 80 chars | Header không tràn layout; mã vẫn đọc/copy được. | Medium | Edge Case |
| ADMIN_PAYMENT_DETAIL_037 | Long refund reason | Reason dài | refunded payment | 1. Mở detail refunded. | 500 chars | Reason wrap đúng trong card/timeline, không tràn. | Low | UI |
| ADMIN_PAYMENT_DETAIL_038 | Responsive desktop | Layout 2 cột | 1440px | 1. Mở detail. | | Payment/booking bên trái, timeline bên phải; spacing đúng. | Low | Responsive |
| ADMIN_PAYMENT_DETAIL_039 | Responsive mobile | Layout mobile | 375px | 1. Mở detail.<br>2. Kiểm tra header/actions. | mobile | Layout 1 cột, action không tràn, booking link vẫn click được. | Medium | Responsive |
| ADMIN_PAYMENT_DETAIL_040 | Regression refund lifecycle | Success -> refund | Payment success test | 1. Mở detail.<br>2. Refund.<br>3. Refetch/list. | success | Payment chuyển refunded trên backend/list; detail không còn refund action. | High | Regression |

## 5. Test data đề xuất

* Payment success có booking, failed có booking, pending có booking, refunded có reason, orphan payment không booking.
* Admin user role `admin`; staff/non-admin để test disabled refund.
* Refund reason hợp lệ và reason rỗng/dài.

## 6. Checklist regression

* Chỉ admin được refund.
* Refund chỉ hiện với status success.
* Orphan payment không render booking block rỗng.
* Timeline mapping success/failed/refunded đúng.
* Booking link điều hướng đúng route.
* Mobile không tràn header/action.

## 7. Ghi chú kỹ thuật

* Logic lấy từ `PaymentDetail/index.tsx`.
* API lấy từ `paymentApi.ts`.
* Rủi ro cao: refund lặp, non-admin refund, payment orphan, status refunded bị map UI khác nhau giữa admin và web.
