# Chọn lịch khởi hành và đặt tour - Test Cases

## 1. Tổng quan màn hình

* Đường dẫn route: `/[locale]/tours/[slug]/departures`, `/[locale]/tours/[slug]/book`
* File source chính: `D:\DATN\danangtrip-web\src\app\[locale]\(main)\(public)\tours\[slug]\departures\page.tsx`, `D:\DATN\danangtrip-web\src\app\[locale]\(main)\(protected)\tours\[slug]\book\page.tsx`
* Component liên quan: `DepartureSelectClient`, `ScheduleCalendar`, `BookingForm`, `OrderSummaryCard`, `PaymentMethodSelector`, `BookingProgressSteps`
* API/service sử dụng: `tourService.getDetail`, `tourService.getSchedules`, `bookingService.calculate`, `bookingService.create`, `paymentService.create`
* Quyền truy cập: departures public; booking form protected user
* Mục đích màn hình: Cho người dùng chọn lịch khởi hành, nhập thông tin khách, kiểm tra giá, tạo booking và chuyển sang thanh toán nếu chọn cổng online.

## 2. Điều kiện tiền đề

* Dữ liệu cần có: tour active, nhiều schedule với trạng thái available/full/cancelled, giá người lớn/trẻ em/em bé.
* Tài khoản cần dùng: guest để test redirect; user thường để đặt tour.
* Trạng thái hệ thống: API booking/payment hoạt động; cấu hình payment gateway có bật/tắt từng cổng.
* Quyền user/admin/staff: chỉ user đã đăng nhập được vào `/book`.

## 3. Danh sách chức năng chính

* Load tour và schedule theo slug/tour id.
* Chọn schedule trên calendar/list.
* Nhập số lượng khách và tính giá.
* Validate booking form bằng `bookingSchema`.
* Chọn phương thức thanh toán `momo`, `vnpay`, `zalopay`, `bank_transfer`, `payos`.
* Tạo booking và chuyển hướng thanh toán nếu có payment URL.
* Hiển thị loading/error/empty schedule.
* Bảo vệ route booking bằng protected layout.

## 4. Test cases chi tiết

| ID | Nhóm chức năng | Test case | Tiền điều kiện | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Mức độ ưu tiên | Loại test |
| -- | -------------- | --------- | -------------- | -------------- | ------------ | ---------------- | -------------- | --------- |
| TOUR_BOOK_001 | Route departures | Mở trang chọn lịch hợp lệ | Tour có slug hợp lệ | 1. Mở `/vi/tours/ba-na-hills/departures`.<br>2. Chờ load. | slug hợp lệ | Hiển thị thông tin tour, calendar/list schedule, giá và CTA tiếp tục. | High | Functional |
| TOUR_BOOK_002 | Route departures | Slug không tồn tại | Không có tour | 1. Mở route departures với slug sai. | invalid slug | Hiển thị lỗi/not found theo page; không gọi schedules với tour undefined. | High | Negative |
| TOUR_BOOK_003 | Loading schedules | API schedules đang tải | API delay | 1. Mở departures.<br>2. Quan sát loading. | delay 2s | Có loading state; không hiện danh sách rỗng trước khi data về. | Medium | UI |
| TOUR_BOOK_004 | Empty schedules | Tour không có lịch | `getSchedules=[]` | 1. Mở departures. | no schedules | Hiển thị empty/no departure; không cho tiếp tục booking. | High | Edge Case |
| TOUR_BOOK_005 | Schedule available | Chọn lịch còn chỗ | Có schedule available | 1. Click ngày/lịch available. | schedule_id=1 | Lịch được highlight; thông tin ngày đi/ngày về/giá cập nhật. | High | Functional |
| TOUR_BOOK_006 | Schedule full | Lịch hết chỗ | Schedule status full/slots 0 | 1. Click lịch full. | full | Không cho chọn hoặc hiển thị full; CTA bị disabled. | High | Edge Case |
| TOUR_BOOK_007 | Schedule cancelled | Lịch bị hủy | Schedule cancelled | 1. Quan sát calendar/list. | cancelled | Không cho đặt lịch cancelled; badge/status hiển thị đúng. | High | Edge Case |
| TOUR_BOOK_008 | Date display | Hiển thị ngày đúng locale | Có schedule | 1. Mở vi và en.<br>2. So ngày. | start/end date | Format ngày đúng locale; không lệch timezone qua ngày khác. | Medium | Regression |
| TOUR_BOOK_009 | Protected booking | Guest vào `/book` | Chưa đăng nhập | 1. Mở `/vi/tours/ba-na-hills/book`. | guest | Bị redirect login hoặc protected layout chặn; không thấy form booking. | High | Permission |
| TOUR_BOOK_010 | Booking form load | User vào form đặt tour | User đăng nhập | 1. Mở `/vi/tours/[slug]/book`. | user | Hiển thị progress steps, form khách hàng, chọn payment, order summary. | High | Functional |
| TOUR_BOOK_011 | Pre-fill user | Form tự điền thông tin user nếu có | User có name/email/phone | 1. Mở booking form.<br>2. Quan sát fields. | profile data | Tên/email/phone được điền nếu source hỗ trợ; vẫn sửa được. | Medium | Functional |
| TOUR_BOOK_012 | Validate schedule | Không chọn lịch | User ở form | 1. Bỏ chọn schedule nếu có.<br>2. Submit. | `tour_schedule_id=0` | Báo `validation.schedule_required`; không gọi create booking. | High | Validation |
| TOUR_BOOK_013 | Validate adult | Người lớn nhỏ hơn 1 | Form mở | 1. Set adult=0.<br>2. Submit. | adult=0 | Báo `validation.adult_required`; không submit. | High | Validation |
| TOUR_BOOK_014 | Validate child | Trẻ em âm | Form mở | 1. Set child=-1. | child=-1 | Không cho giá trị âm hoặc schema reject. | High | Validation |
| TOUR_BOOK_015 | Validate infant | Em bé âm | Form mở | 1. Set infant=-1. | infant=-1 | Không cho giá trị âm hoặc schema reject. | High | Validation |
| TOUR_BOOK_016 | Validate name | Tên khách quá ngắn | Form mở | 1. Nhập tên 1 ký tự.<br>2. Submit. | `A` | Báo `validation.name_min`. | High | Validation |
| TOUR_BOOK_017 | Validate email | Email sai định dạng | Form mở | 1. Nhập email sai.<br>2. Submit. | `abc` | Báo `validation.email_invalid`. | High | Validation |
| TOUR_BOOK_018 | Validate phone | SĐT sai định dạng | Form mở | 1. Nhập SĐT 9 số/chữ.<br>2. Submit. | `abc123` | Báo `validation.phone_invalid`; chỉ chấp nhận 10-11 số. | High | Validation |
| TOUR_BOOK_019 | Optional address | Địa chỉ trống | Form mở | 1. Để address trống.<br>2. Submit valid. | address empty | Không báo lỗi vì optional/nullable. | Medium | Edge Case |
| TOUR_BOOK_020 | Optional note | Ghi chú trống | Form mở | 1. Để note trống.<br>2. Submit valid. | note empty | Không báo lỗi vì optional/nullable. | Low | Edge Case |
| TOUR_BOOK_021 | Validate terms | Chưa đồng ý điều khoản | Form mở | 1. Bỏ check terms.<br>2. Submit. | agree_terms=false | Báo `validation.terms_required`; không gọi API. | High | Validation |
| TOUR_BOOK_022 | Payment method | Chọn PayOS | Gateway bật | 1. Chọn PayOS.<br>2. Submit valid. | payos | Payload có `payment_method=payos`; nếu API trả `payment_url` thì redirect. | High | Functional |
| TOUR_BOOK_023 | Payment method | Chọn bank transfer | Gateway/option có sẵn | 1. Chọn bank_transfer.<br>2. Submit. | bank_transfer | Booking được tạo; không bắt buộc redirect payment URL nếu backend không trả. | High | Functional |
| TOUR_BOOK_024 | Payment disabled | Gateway bị tắt trong config | app config tắt momo | 1. Mở form.<br>2. Quan sát option. | momo=false | Gateway bị tắt không nên được chọn hoặc hiển thị disabled. | Medium | Edge Case |
| TOUR_BOOK_025 | Calculate price | Tính giá theo số lượng | Schedule có giá riêng | 1. Chọn schedule.<br>2. Nhập 2 adult,1 child,1 infant. | 2/1/1 | `bookingService.calculate` được gọi; summary hiển thị từng dòng và tổng đúng. | High | API |
| TOUR_BOOK_026 | Calculate error | API calculate lỗi | Mock 500 | 1. Đổi số lượng.<br>2. Chờ tính giá. | 500 | Hiển thị lỗi/tổng fallback; không submit sai tổng. | High | API |
| TOUR_BOOK_027 | Create booking success | Tạo booking thành công | Form valid | 1. Submit form. | valid payload | Gọi `bookingService.create`; chuyển bước/redirect đúng theo payment method. | High | Functional |
| TOUR_BOOK_028 | Create booking 422 | Backend trả validation | Form gửi dữ liệu backend từ chối | 1. Submit với schedule hết chỗ do race condition. | 422 | Hiển thị lỗi API; không redirect thanh toán. | High | Negative |
| TOUR_BOOK_029 | Create booking 401 | Token hết hạn | User token invalid | 1. Submit form. | 401 | Bị đưa về login hoặc hiện lỗi auth theo axios interceptor. | High | Permission |
| TOUR_BOOK_030 | Payment URL thiếu | Create payment trả không có `payment_url` | Online method | 1. Submit.<br>2. Mock create payment thiếu URL. | no payment_url | Toast lỗi `errors.payment_link`; không set location.href undefined. | High | Negative |
| TOUR_BOOK_031 | Payment create error | API payment lỗi | Online method | 1. Submit.<br>2. Mock API lỗi. | 500 | Toast `errors.create_failed`; booking/payment state không kẹt loading. | High | API |
| TOUR_BOOK_032 | Double submit | Click submit liên tục | Form valid | 1. Double click nút đặt tour. | valid | Chỉ gửi một request hoặc button disabled khi pending. | High | Regression |
| TOUR_BOOK_033 | Deadline đã qua | Schedule quá hạn đặt | bookingDeadline < now | 1. Chọn schedule quá hạn. | expired deadline | Không cho đặt hoặc backend báo lỗi; UI không hiển thị như lịch còn đặt được. | High | Edge Case |
| TOUR_BOOK_034 | Tổng khách bằng 0 | Dữ liệu bất thường | adult=0 child=0 infant=0 | 1. Submit qua devtools/state. | 0 khách | Schema/API chặn do adult min 1. | High | Validation |
| TOUR_BOOK_035 | Giá schedule override | Schedule có giá khác tour | Schedule priceAdult khác base | 1. Chọn schedule.<br>2. Quan sát summary. | override price | Summary ưu tiên giá schedule nếu source dùng; không hiển thị base sai. | Medium | Edge Case |
| TOUR_BOOK_036 | Quay lại | Nút quay lại/step trước | Đang ở booking form | 1. Click back/previous nếu có.<br>2. Quan sát. | | Quay về tour/departures đúng locale, không mất route. | Medium | Functional |
| TOUR_BOOK_037 | Responsive departures | Calendar trên mobile | Viewport 375px | 1. Mở departures.<br>2. Chọn ngày. | mobile | Calendar/list không tràn ngang, ngày đủ click. | Medium | Responsive |
| TOUR_BOOK_038 | Responsive booking | Form trên mobile | Viewport 375px | 1. Mở booking form.<br>2. Nhập dữ liệu. | mobile | Form, summary, payment method xếp hợp lý; không che nút submit. | High | Responsive |
| TOUR_BOOK_039 | Locale | Booking với locale en | User logged in | 1. Mở `/en/tours/[slug]/book`. | en | Text dịch đúng; return_url payment chứa `/en/payment/result`. | Medium | Regression |
| TOUR_BOOK_040 | Regression toàn flow | End-to-end booking online | User, schedule available, gateway PayOS | 1. Chọn lịch.<br>2. Nhập form valid.<br>3. Chọn PayOS.<br>4. Submit. | valid | Tạo booking, tạo payment, redirect payment_url; không lỗi state/loading. | High | Regression |

## 5. Test data đề xuất

* Tour `ba-na-hills`: 3 schedule available/full/cancelled.
* User `user@danangtrip.vn`: có profile đầy đủ.
* Gateway config: PayOS bật, MoMo tắt để test disabled.
* Booking valid: adult 2, child 1, infant 0, phone `0901234567`, email hợp lệ.

## 6. Checklist regression

* Guest không vào được `/book`.
* Form validate đúng schema.
* Tính giá không NaN khi đổi số lượng.
* Không đặt được lịch full/cancelled/quá hạn.
* Online payment redirect đúng return URL.
* Mobile không tràn ngang.

## 7. Ghi chú kỹ thuật

* Validation lấy từ `booking.schema.ts`.
* Payment redirect lấy từ `usePayment.ts`.
* Rủi ro cao: race condition slot còn lại, payment_url thiếu, gateway config, return_url locale.
