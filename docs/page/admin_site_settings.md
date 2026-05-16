# Màn hình Admin — Cấu hình website

> Route đề xuất: `/admin/settings`  
> Trạng thái: Planned  
> Nghiệp vụ tham khảo: travel.com.vn hiển thị hotline, email, địa chỉ, social, chính sách và phương thức thanh toán ở header/footer.

---

## Mục tiêu

Quản lý các cấu hình public của website thay vì hardcode trong frontend.

---

## Thành phần giao diện

| Nhóm | Field/chức năng |
|---|---|
| Thông tin liên hệ | Hotline, email, địa chỉ, giờ hỗ trợ |
| Thương hiệu | Logo, favicon, tên website |
| Social | Facebook, YouTube, TikTok, Zalo |
| Payment | Bật/tắt phương thức VNPay/MoMo/ZaloPay/chuyển khoản |
| Chính sách | Link điều khoản, riêng tư, bảo vệ dữ liệu cá nhân |
| SEO mặc định | Meta title, meta description, og image |

---

## API planned

| Method | Endpoint | Mục đích |
|---|---|---|
| GET | `/config` | Public config cho frontend |
| GET | `/admin/settings` | Admin xem config |
| PUT | `/admin/settings` | Admin cập nhật config |

---

## Ghi chú

`GET /config` đã được nhắc trong tài liệu home nhưng hiện chưa có route. Khi chưa implement, frontend cần fallback hardcode.

---

## Validation & States

| Nhóm setting | Quy tắc |
|---|---|
| `general.hotline` | Bắt buộc nếu `is_public=true`; định dạng số điện thoại Việt Nam |
| `general.email` | Phải đúng định dạng email |
| `brand.logo` | Chỉ nhận URL ảnh hoặc upload result hợp lệ |
| `payment.*` | Giá trị boolean; nếu tắt toàn bộ payment online phải còn ít nhất một phương thức thanh toán khả dụng |
| `seo.meta_title` | Khuyến nghị 30-70 ký tự |
| `seo.meta_description` | Khuyến nghị 120-160 ký tự |
| `value_type` | Chỉ nhận `string`, `number`, `boolean`, `json`, `url`, `image` |
| Save lỗi | Không ghi đè local form nếu API lỗi; hiển thị lỗi theo từng group |
| Public config fallback | Nếu `GET /config` lỗi, frontend dùng config hardcode tối thiểu: hotline, email, logo mặc định |
