# Chức năng hệ thống — Runtime, Auth Session, Payment Callback

> Loại: Technical/system flow, không phải màn nghiệp vụ độc lập  
> Mục tiêu: Gán chủ sở hữu tài liệu cho các API nền không nên hiển thị như trang riêng.

---

## API sử dụng

| Method | Endpoint | Chủ sở hữu UI/Service | Mục đích |
|---|---|---|---|
| GET | `/auth/me` | App bootstrap/auth guard | Lấy user hiện tại khi reload app hoặc kiểm tra quyền truy cập route |
| POST | `/auth/refresh` | Auth interceptor/service | Làm mới JWT khi token sắp hết hạn |
| POST | `/payments/callback` | Payment gateway webhook | Nhận kết quả từ cổng thanh toán, không gọi từ frontend |
| GET | `/ping` | DevOps/API monitor | Kiểm tra API server còn phản hồi |
| GET | `/health` | DevOps/API monitor | Health check sâu hơn cho uptime/monitoring |

---

## Flow xử lý

| Flow | Mô tả |
|---|---|
| App bootstrap | Frontend gọi `GET /auth/me` nếu có token để phục hồi session, role và menu |
| Token refresh | HTTP client tự gọi `POST /auth/refresh` khi token gần hết hạn hoặc nhận lỗi hết hạn token |
| Payment callback | Gateway gọi `POST /payments/callback`; backend cập nhật `payments`, `bookings`, `payment_status_histories` |
| Monitoring | Tool vận hành gọi `/ping` hoặc `/health`; không nằm trong menu user/admin |

---

## Validation & rule

| API | Rule |
|---|---|
| `/auth/me` | Nếu token không hợp lệ, xóa session local và chuyển về `/login` khi route cần auth |
| `/auth/refresh` | Nếu refresh thất bại, logout cưỡng bức |
| `/payments/callback` | Phải verify chữ ký/hash từ gateway trước khi cập nhật thanh toán |
| `/ping`, `/health` | Không trả dữ liệu nhạy cảm; chỉ trả trạng thái cần cho monitoring |
