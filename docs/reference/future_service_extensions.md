# Màn hình mở rộng phase sau — Flight, Hotel, Combo, Visa

> Trạng thái: Planned phase sau  
> Mục tiêu: Gán chủ sở hữu tài liệu cho các API dịch vụ mở rộng ngoài core tour booking.

---

## API planned

| Method | Endpoint | Màn đề xuất | Mục đích |
|---|---|---|---|
| GET | `/flights/search` | Tìm chuyến bay | Tìm vé máy bay theo hành trình |
| GET | `/hotels/search` | Tìm khách sạn | Tìm khách sạn theo điểm đến/ngày |
| GET | `/flight-hotels/search` | Combo bay + khách sạn | Tìm combo du lịch |
| GET | `/visa/products` | Dịch vụ visa | Danh sách sản phẩm visa |

---

## Ghi chú triển khai

Các API này không thuộc core DanangTrip hiện tại. Khi triển khai cần bổ sung thiết kế DB hoặc xác định rõ tích hợp external provider. Trước mắt chỉ giữ ở trạng thái planned để không lẫn với tour booking, location, payment và admin vận hành.

---

## Validation & States

| Nhóm API | Quy tắc |
|---|---|
| Flight search | Bắt buộc có điểm đi, điểm đến, ngày đi; ngày về chỉ bắt buộc với khứ hồi |
| Hotel search | Bắt buộc có điểm đến, ngày nhận/trả phòng; `checkin < checkout` |
| Combo search | Phải validate đồng thời thông tin chuyến bay và khách sạn |
| Visa products | Nếu chưa có provider, ẩn entry khỏi navigation public |
| External error | Nếu provider lỗi, hiển thị trạng thái đang bảo trì dịch vụ thay vì lỗi hệ thống |

---

## Mức ưu tiên

| Nhóm | Ưu tiên | Lý do |
|---|---|---|
| Flight/Hotel/Combo | Bình | Ngoài core nghiệp vụ tour Đà Nẵng |
| Visa | Bình | Có thể là dịch vụ mở rộng sau khi core booking ổn định |
