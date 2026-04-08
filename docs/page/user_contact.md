# Màn hình: Form Liên hệ

> Route: `/contact`
> Quyền: 🌐 Public — không cần đăng nhập
> Mô tả: Form gửi yêu cầu liên hệ đến đội ngũ Đà Nẵng Trip.

---

## Layout tổng thể

```
┌─────────────────────────────────────────────────────────────┐
│  HEADER (dùng chung)                                        │
├─────────────────────────────────────────────────────────────┤
│  PAGE HERO: Tiêu đề + Breadcrumb                           │
├──────────────────────────────────┬──────────────────────────┤
│  FORM (flex-1)                   │  INFO PANEL (380px)      │
│  - Họ tên                        │  - Địa chỉ               │
│  - Email                         │  - Điện thoại            │
│  - Số điện thoại                 │  - Email                 │
│  - Chủ đề                        │  - Giờ làm việc          │
│  - Nội dung                      │  - Bản đồ mini           │
│  - Button Gửi                    │  - Social links          │
└──────────────────────────────────┴──────────────────────────┘
│  FOOTER (dùng chung)                                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 1. Page Hero

`bg linear-gradient(135deg, #0066CC, #3385D6) py-48 text-center`

- Breadcrumb: `"Trang chủ / Liên hệ" 13px white/70`
- Title: `"Liên hệ với chúng tôi" 32px Inter 700 white`
- Subtitle: `"Chúng tôi luôn sẵn sàng hỗ trợ bạn" 16px white/80 mt-8`

---

## 2. Form

**Card:** `bg white border #E2E8F0 radius-16 p-32`

**Form fields** (`space-y-20`):

**Grid 2 cột** (`grid grid-cols-2 gap-20`):

| Field | Type | Bắt buộc | Config |
|-------|------|----------|--------|
| Họ và tên | text | ✅ | placeholder "Nhập họ và tên..." · icon `person` trái |
| Email | email | ✅ | placeholder "example@email.com" · icon `email` trái |
| Số điện thoại | tel | — | placeholder "0905 xxx xxx" · icon `phone` trái · col-span 1 |
| Chủ đề | select | — | "Hỏi về tour" / "Hỏi về địa điểm" / "Phản hồi dịch vụ" / "Hợp tác" / "Khác" · col-span 1 |

**Full width:**

| Field | Type | Bắt buộc | Config |
|-------|------|----------|--------|
| Nội dung | textarea rows-5 | ✅ | placeholder "Nhập nội dung tin nhắn..." · resize-none |

**Input style:**
- `border #E2E8F0 radius-10 px-14 py-12 14px Inter`
- icon trái: `absolute left-14 top-1/2 -translate-y-1/2 18px #94A3B8`
- padding-left: `pl-44` khi có icon
- focus: `border #0066CC ring rgba(0,102,204,0.15)`
- error: `border #EF4444 bg rgba(239,68,68,0.04)`
- error text: `12px #EF4444 mt-4`

**Checkbox đồng ý:**
`flex items-start gap-8 mt-4`
- Checkbox `16px accent-color #0066CC`
- Label: `13px #64748B line-height 1.5`
  "Tôi đồng ý với [Chính sách bảo mật](link) và cho phép Đà Nẵng Trip liên hệ lại."

**Button "Gửi tin nhắn":**
`bg #0066CC text white radius-12 py-14 full-width 16px Inter 600 mt-8`
icon `send` bên trái
hover `bg #004999`
shadow `0 4px 12px rgba(0,102,204,0.25)`

---

## 3. Submit States

**Đang gửi:**
- Button disabled · spinner · "Đang gửi..."
- `bg #3385D6 cursor-not-allowed`

**Gửi thành công:**
- Thay form bằng success state:
  `center py-48 text-center`
  - SVG icon `check_circle 80px #10B981`
  - Title: `"Gửi thành công!" 24px Inter 700 #1E293B mt-16`
  - Subtitle: `"Chúng tôi sẽ phản hồi trong vòng 24 giờ làm việc." 14px #64748B mt-8`
  - Button "Gửi tin nhắn khác": `border #E2E8F0 bg white text #64748B radius-10 px-20 py-10 mt-16`
    → reset form

**Gửi thất bại:**
- Toast: `bg #FEE2E2 text #EF4444` "Có lỗi xảy ra. Vui lòng thử lại."

---

## 4. Info Panel

`width 380px flex-shrink-0`

**Card:** `bg white border #E2E8F0 radius-16 p-24`

### 4.1 Thông tin liên hệ

`space-y-20`

Mỗi item: `flex items-start gap-16`
- Icon container: `44x44px radius-12 bg #EFF6FF flex-shrink-0`
  - Icon: `22px #0066CC`
- Right:
  - Label: `11px uppercase #94A3B8 mb-4`
  - Value: `14px Inter 500 #1E293B`

| Icon | Label | Value |
|------|-------|-------|
| `location_on` | ĐỊA CHỈ | "123 Nguyễn Văn Linh, Đà Nẵng" |
| `phone` | ĐIỆN THOẠI | "0905 xxx xxx" (link `tel:`) |
| `email` | EMAIL | "hello@danangtrip.vn" (link `mailto:`) |
| `schedule` | GIỜ LÀM VIỆC | "Thứ 2 - Thứ 6: 8:00 - 17:00\nThứ 7: 8:00 - 12:00" |

### 4.2 Bản đồ mini

`mt-20 h-200px bg #F1F5F9 radius-12 overflow-hidden`

- iframe Google Maps với marker văn phòng
- Button "Xem bản đồ lớn hơn": `flex items-center gap-4 mt-8 text-13 #0066CC`
  → mở Google Maps tab mới

### 4.3 Social Links

`mt-20 pt-20 border-t #F1F5F9`

- Label: `"Theo dõi chúng tôi" 13px Inter 600 #1E293B mb-12`
- `flex gap-8`:
  - Facebook: `40x40px bg #1877F2 text white rounded-full flex items-center justify-center`
  - Instagram: `40x40px bg gradient-instagram text white rounded-full`
  - YouTube: `40x40px bg #FF0000 text white rounded-full`
  - TikTok: `40x40px bg #000000 text white rounded-full`
  - hover: `opacity-80 transform scale-110 transition-200ms`

---

## 5. FAQ Section (Optional)

`py-48 bg #F8FAFC`

- Title: `"Câu hỏi thường gặp" 24px Inter 700 #1E293B mb-24 text-center`

**Accordion list** (`max-w-720px mx-auto space-y-8`):

Mỗi item: `bg white border #E2E8F0 radius-12 overflow-hidden`
- Header: `flex justify-between items-center px-20 py-16 cursor-pointer`
  - Question: `15px Inter 600 #1E293B`
  - icon `expand_more` / `expand_less` `#94A3B8`
  - hover: `bg #F8FAFC`
- Body (khi mở): `px-20 pb-16`
  - Answer: `14px #64748B line-height 1.7`

Sample FAQ:
1. "Làm thế nào để đặt tour?" → "Bạn có thể đặt tour trực tiếp trên website..."
2. "Chính sách hủy tour như thế nào?" → "Bạn có thể hủy tour miễn phí trước 24 giờ..."
3. "Có hỗ trợ thanh toán online không?" → "Chúng tôi hỗ trợ MoMo, VNPay, ZaloPay..."
4. "Tour có hướng dẫn viên không?" → "Tất cả tour đều có hướng dẫn viên chuyên nghiệp..."

---

## 6. API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Gửi form liên hệ | POST | `/contacts` | Submit form |

**Body POST /contacts:**
```json
{
  "name": "*",
  "email": "*",
  "phone": "",
  "subject": "",
  "message": "*"
}
```
