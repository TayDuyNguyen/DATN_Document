# Đặt lại mật khẩu (Reset Password) - Test Cases

## 1. Tổng quan màn hình

* Đường dẫn route: `/[locale]/reset-password`
* File source chính: `D:\DATN\danangtrip-web\src\app\[locale]\(auth)\reset-password\page.tsx`
* Component liên quan: `ResetPasswordForm`, `Input`, `AmbientBackground`
* API/service sử dụng: `authService.resetPassword({ token, email, password, password_confirmation })`
* Quyền truy cập: Guest truy cập công khai qua link được gửi trong email.
* Mục đích màn hình: Cho phép người dùng điền mật khẩu mới và xác nhận mật khẩu sau khi click vào liên kết đặt lại mật khẩu từ email của họ.

## 2. Điều kiện tiền đề

* Dữ liệu cần có: Một email đã đăng ký tài khoản trong hệ thống và đã gửi yêu cầu reset mật khẩu để nhận token.
* Tài khoản cần dùng: Guest (chưa đăng nhập).
* Trạng thái hệ thống: API Web hoạt động bình thường.

## 3. Danh sách chức năng chính

* Kiểm tra sự tồn tại của tham số `token` trên URL.
  - **Trạng thái A (Invalid Token)**: Nếu thiếu token hoặc token trống, hiển thị màn hình thông báo liên kết không hợp lệ kèm link để yêu cầu lại liên kết mới hoặc quay lại Login.
  - **Trạng thái B (Form Entry)**: Nếu có token, hiển thị form để nhập email, mật khẩu mới và xác nhận mật khẩu.
* Tự động điền email từ tham số `email` trên URL (nếu có).
* Validation thời gian thực (real-time validation on blur/change) và validation trước khi submit:
  - **Email**: Phải có dữ liệu, đúng định dạng email tiêu chuẩn.
  - **Mật khẩu**: Tối thiểu 8 ký tự, chứa ít nhất 1 chữ thường, 1 chữ hoa, 1 chữ số, 1 ký tự đặc biệt thuộc nhóm `@$!%*?&`.
  - **Mật khẩu xác nhận**: Phải khớp chính xác với mật khẩu mới.
* Xử lý submit form:
  - Chuyển đổi payload trường `confirmPassword` thành `password_confirmation` để gửi lên API của Laravel.
  - Hiển thị trạng thái loading spinner và chữ "Đang gửi" (submitting) khi pending; disable nút submit và các input tránh double submit.
* **Trạng thái C (Success Card)**: Hiển thị giao diện thông báo thành công sau khi đổi mật khẩu thành công kèm nút chuyển hướng sang trang Đăng nhập.
* Xử lý lỗi API (tài khoản không tồn tại, token hết hạn, lỗi server 500) qua toast thông báo lỗi chi tiết.

## 4. Test cases chi tiết

| ID | Nhóm chức năng | Test case | Tiền điều kiện | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Mức độ ưu tiên | Loại test |
| -- | -------------- | --------- | -------------- | -------------- | ------------ | ---------------- | -------------- | --------- |
| RESET_PWD_001 | Token URL | Truy cập không có token trên URL (State A) | Chưa đăng nhập | 1. Mở `/vi/reset-password`.<br>2. Quan sát giao diện. | Không truyền token | Hiển thị màn hình thông báo liên kết không hợp lệ (màn hình đỏ cảnh báo), nút "Yêu cầu liên kết mới" và liên kết "Quay lại Đăng nhập". Không hiển thị form nhập mật khẩu. | Critical | Functional |
| RESET_PWD_002 | Token URL | Truy cập có token hợp lệ (State B) | Đã gửi yêu cầu reset mật khẩu | 1. Mở `/vi/reset-password?token=valid-token-123`.<br>2. Quan sát giao diện. | `token=valid-token-123` | Hiển thị form nhập Đặt lại mật khẩu (nhập Email, Mật khẩu mới, Xác nhận mật khẩu). Nút Đặt lại mật khẩu ở trạng thái disabled cho tới khi điền đầy đủ dữ liệu. | Critical | Functional |
| RESET_PWD_003 | Auto-fill Email | Tự động điền email từ URL parameter | Có email trên URL query | 1. Mở `/vi/reset-password?token=token123&email=user@test.com`.<br>2. Quan sát ô input Email. | `email=user@test.com` | Ô input Email hiển thị sẵn giá trị `user@test.com`. | High | Functional |
| RESET_PWD_004 | Validation | Để trống email khi blur | Form đang mở | 1. Focus ô Email.<br>2. Xóa sạch và blur ra ngoài. | Email trống | Hiển thị lỗi dưới ô input: `error.required` (hoặc bản dịch tương ứng). | High | Validation |
| RESET_PWD_005 | Validation | Nhập email sai định dạng | Form đang mở | 1. Nhập `user@test` hoặc `usertest.com` vào ô Email.<br>2. Blur ra ngoài hoặc nhấn submit. | Email sai định dạng | Hiển thị lỗi dưới ô input: `error.invalid_email`. | High | Validation |
| RESET_PWD_006 | Validation | Mật khẩu ngắn hơn 8 ký tự | Form đang mở | 1. Nhập `Abc@1` vào ô Mật khẩu.<br>2. Blur ra ngoài hoặc nhấn submit. | `Abc@1` (5 ký tự) | Hiển thị lỗi dưới ô mật khẩu: `error.invalid_password`. | High | Validation |
| RESET_PWD_007 | Validation | Mật khẩu thiếu chữ hoa | Form đang mở | 1. Nhập `abcde@123` vào ô Mật khẩu.<br>2. Blur ra ngoài. | `abcde@123` | Hiển thị lỗi dưới ô mật khẩu: `error.invalid_password`. | High | Validation |
| RESET_PWD_008 | Validation | Mật khẩu thiếu chữ số | Form đang mở | 1. Nhập `Abcde@fgh` vào ô Mật khẩu.<br>2. Blur ra ngoài. | `Abcde@fgh` | Hiển thị lỗi dưới ô mật khẩu: `error.invalid_password`. | High | Validation |
| RESET_PWD_009 | Validation | Mật khẩu thiếu ký tự đặc biệt | Form đang mở | 1. Nhập `Abcde1234` vào ô Mật khẩu.<br>2. Blur ra ngoài. | `Abcde1234` | Hiển thị lỗi dưới ô mật khẩu: `error.invalid_password`. | High | Validation |
| RESET_PWD_010 | Validation | Mật khẩu xác nhận không khớp | Form đang mở | 1. Nhập `Abcde@123` ở Mật khẩu.<br>2. Nhập `Abcde@124` ở Xác nhận mật khẩu.<br>3. Blur ra ngoài. | Mật khẩu không khớp | Hiển thị lỗi dưới ô Xác nhận mật khẩu: `error.password_mismatch`. Nút Submit ở trạng thái disabled. | Critical | Validation |
| RESET_PWD_011 | Submit Logic | Nút Submit thay đổi trạng thái theo validation | Form đang mở | 1. Nhập thiếu hoặc sai thông tin.<br>2. Quan sát nút Submit.<br>3. Điền đúng hết toàn bộ thông tin hợp lệ.<br>4. Quan sát lại nút Submit. | Dữ liệu đúng / sai | Nút Submit bị disabled khi có bất kỳ ô nào trống hoặc bị lỗi validation. Nút chỉ enabled khi tất cả các ô điền đúng và không còn lỗi. | High | UI |
| RESET_PWD_012 | API Call | Đặt lại mật khẩu thành công (State C) | Token và email hợp lệ | 1. Điền thông tin hợp lệ.<br>2. Nhấn nút Submit.<br>3. Quan sát API request và UI. | Email & mật khẩu hợp lệ | - API `authService.resetPassword` được gọi với payload: `{ token, email, password, password_confirmation }`. <br>- Hiện loading spinner trên nút và text chuyển thành "Đang gửi".<br>- Nhận response thành công, hiển thị toast success và giao diện chuyển hẳn sang State C (Success Card Screen) báo thành công kèm nút chuyển hướng sang Đăng nhập. | Critical | API |
| RESET_PWD_013 | API Lỗi | Token hết hạn hoặc không tồn tại | Token giả lập hết hạn | 1. Điền thông tin hợp lệ.<br>2. Nhấn Submit.<br>3. API trả về lỗi 400 (Invalid or expired token). | Token hết hạn | Hiển thị toast báo lỗi lấy từ response (ví dụ: Link đổi mật khẩu đã hết hạn hoặc không tồn tại). Form giữ nguyên để người dùng chỉnh sửa nếu cần. | High | API |
| RESET_PWD_014 | API Lỗi | Server lỗi 500 hoặc mất mạng | Mock lỗi server | 1. Nhấn Submit.<br>2. Mock API trả về lỗi 500. | Server error | Hiển thị toast báo lỗi mặc định `failure.general_error` hoặc lỗi kết nối; không làm sập ứng dụng (crash client). | High | API |
| RESET_PWD_015 | Direct URL Access | Đăng nhập rồi nhưng truy cập link reset | Đã đăng nhập tài khoản user | 1. Đăng nhập hệ thống.<br>2. Gõ thủ công URL `/vi/reset-password?token=123`. | User session active | Form vẫn hiển thị bình thường do đây là public auth route, tuy nhiên khuyên cáo kiểm tra logic logout hoặc giữ nguyên cho phép đổi mật khẩu mà không crash. | Medium | Security |
| RESET_PWD_016 | Responsive | Hiển thị responsive trên thiết bị | Màn hình reset password | 1. Mở trang trên Desktop (1440px), Tablet (768px), Mobile (375px).<br>2. Kiểm tra layout. | | - Desktop: Hiển thị panel trái (hình thương hiệu/background đồng màu) và panel phải chứa form.<br>- Mobile: Panel trái bị ẩn, panel phải mở rộng 100% viewport, form hiển thị rõ ràng, text không bị đè. | Medium | Responsive |

## 5. Test data đề xuất

* URL hợp lệ: `/vi/reset-password?token=test-token-active-1029&email=customer@danangtrip.vn`
* Email hợp lệ: `customer@danangtrip.vn`
* Mật khẩu mạnh hợp lệ: `DaNangTrip@2026`
* Mật khẩu yếu không hợp lệ: `123456`, `danang123`, `Danang123`, `Danang@`

## 6. Checklist regression

* Đặt lại mật khẩu thành công cập nhật được mật khẩu mới trong cơ sở dữ liệu (đăng nhập bằng mật khẩu mới thành công).
* Đặt lại mật khẩu thành công không làm mất token của phiên đăng nhập hiện tại nếu có.
* Form không cho phép nhấn Submit nhiều lần liên tiếp khi đang gửi yêu cầu (pending state).

## 7. Ghi chú kỹ thuật

* Schema Zod được quản lý tại `danangtrip-web/src/features/auth/validators/auth.schema.ts` (`resetPasswordSchema`).
* Form sử dụng hook `useMutation` của `@tanstack/react-query` để call API.
* Chú ý: Payload gửi lên API Laravel cần map `confirmPassword` -> `password_confirmation`.
