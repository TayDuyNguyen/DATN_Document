# Màn hình: Hồ sơ cá nhân

> Route: `/profile`
> Quyền: 🔐 Cần đăng nhập
> Mô tả: Xem và chỉnh sửa thông tin cá nhân, upload avatar.

---

## Layout tổng thể

```
┌─────────────────────────────────────────────────────────────┐
│  HEADER (dùng chung)                                        │
├─────────────────────────────────────────────────────────────┤
│  BREADCRUMB: Trang chủ / Hồ sơ cá nhân                     │
├──────────────────────────────────┬──────────────────────────┤
│  SIDEBAR (240px)                 │  MAIN CONTENT (flex-1)   │
│  - Avatar + Tên                  │  - Form thông tin        │
│  - Navigation menu               │  - Submit button         │
│    · Hồ sơ (active)              │                          │
│    · Đổi mật khẩu                │                          │
│    · Đơn đặt tour                │                          │
│    · Địa điểm yêu thích          │                          │
│    · Đánh giá của tôi            │                          │
│    · Thông báo                   │                          │
│    · Xóa tài khoản               │                          │
└──────────────────────────────────┴──────────────────────────┘
│  FOOTER (dùng chung)                                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 1. Breadcrumb

`py-12 border-b #E2E8F0`
`"Trang chủ / Hồ sơ cá nhân" 13px #94A3B8`

---

## 2. Sidebar

`width 240px flex-shrink-0`

### 2.1 Avatar + Tên

**Card:** `bg white border #E2E8F0 radius-16 p-20 mb-16 text-center`

**Avatar upload:**
`relative w-96px h-96px mx-auto mb-12`
- Avatar: `96x96px rounded-full border-3 #E2E8F0 object-cover`
  - Nếu không có: bg gradient initials `text white 28px 700`
- Overlay khi hover: `absolute inset-0 bg rgba(0,0,0,0.4) rounded-full flex items-center justify-center opacity-0 hover:opacity-100 transition-200ms cursor-pointer`
  - icon `camera_alt 24px white`
  - Text `"Đổi ảnh" 11px white mt-4`
- Click → mở file picker → `POST /user/profile/avatar`
- Loading: spinner overlay

**Tên:** `16px Inter 700 #1E293B`
**Email:** `13px #94A3B8 mt-4`
**Badge role:** `"Thành viên" bg #EFF6FF text #0066CC 11px 600 radius-full px-8 py-2 mt-8`

### 2.2 Navigation Menu

**Card:** `bg white border #E2E8F0 radius-16 overflow-hidden`

Mỗi item: `flex items-center gap-12 px-16 py-14 border-b #F1F5F9 cursor-pointer`
hover `bg #F8FAFC`
Active: `bg #EFF6FF border-l-3 #0066CC`

| Icon | Label | Route |
|------|-------|-------|
| `person` | Hồ sơ cá nhân | `/profile` |
| `lock` | Đổi mật khẩu | `/profile/password` |
| `shopping_cart` | Đơn đặt tour | `/bookings` |
| `favorite` | Địa điểm yêu thích | `/favorites` |
| `star` | Đánh giá của tôi | `/profile/ratings` |
| `notifications` | Thông báo | `/notifications` |

Divider `1px #F1F5F9`

- `delete_forever #EF4444` + "Xóa tài khoản" `text #EF4444` → `/profile/delete`

Icon: `20px #64748B` · Label: `14px Inter 500 #1E293B`
Active: icon + label `color #0066CC`

---

## 3. Main Content — Form thông tin

**Card:** `bg white border #E2E8F0 radius-16 p-32`

**Card header** (`flex justify-between items-center mb-24 pb-16 border-b #F1F5F9`):
- Title: `"Thông tin cá nhân" 18px Inter 600 #1E293B`
- Badge xác thực email:
  - Đã xác thực: `bg #D1FAE5 text #10B981 12px 600 radius-full px-10 py-4` icon `verified 14px` "Email đã xác thực"
  - Chưa xác thực: `bg #FEF3C7 text #F59E0B 12px 600 radius-full px-10 py-4` "Chưa xác thực"
    + Link "Xác thực ngay" `12px #0066CC` → `/verify-email`

**Form fields** (`grid grid-cols-2 gap-20`):

| Field | Type | Bắt buộc | Col | Config |
|-------|------|----------|-----|--------|
| Họ và tên | text | ✅ | 2 | placeholder "Nhập họ và tên..." |
| Số điện thoại | tel | — | 1 | placeholder "0905 xxx xxx" icon `phone` |
| Ngày sinh | date | — | 1 | icon `cake` |
| Giới tính | select | — | 1 | Nam / Nữ / Khác / Không muốn tiết lộ |
| Thành phố | text | — | 1 | placeholder "Đà Nẵng" icon `location_on` |

**Email field** (readonly, full width):
`flex items-center gap-12 p-14 bg #F8FAFC border #E2E8F0 radius-10`
- icon `email 18px #94A3B8`
- Email: `14px Inter 500 #1E293B flex-1`
- Badge: `"Không thể thay đổi" bg #F1F5F9 text #94A3B8 11px radius-full px-8 py-2`

**Username field** (readonly, full width):
`flex items-center gap-12 p-14 bg #F8FAFC border #E2E8F0 radius-10`
- icon `alternate_email 18px #94A3B8`
- Username: `"@nguyenvanan" 14px monospace #64748B flex-1`
- Badge: `"Không thể thay đổi" bg #F1F5F9 text #94A3B8 11px radius-full px-8 py-2`

**Input style:**
- `border #E2E8F0 radius-10 px-14 py-12 14px Inter`
- focus: `border #0066CC ring rgba(0,102,204,0.15)`
- Label: `13px Inter 600 #1E293B mb-6`

**Form footer** (`flex justify-between items-center mt-24 pt-16 border-t #F1F5F9`):
- Left: `"Cập nhật lần cuối: 01/04/2026" 12px #94A3B8`
- Right (`flex gap-12`):
  - "Hủy thay đổi": `border #E2E8F0 bg white text #64748B radius-10 px-20 py-10`
    hover `border #EF4444 text #EF4444`
    → reset form về giá trị ban đầu
  - "Lưu thay đổi": `bg #0066CC text white radius-10 px-20 py-10 14px 600`
    hover `bg #004999`
    → `PUT /user/profile`

---

## 4. Submit States

| Tình huống | Xử lý |
|-----------|-------|
| Đang lưu | Button disabled · spinner · "Đang lưu..." · `bg #3385D6` |
| Lưu thành công | Toast `bg #D1FAE5 text #10B981` "Cập nhật thông tin thành công!" |
| Thất bại | Toast `bg #FEE2E2 text #EF4444` "Có lỗi xảy ra." |
| Upload avatar | Spinner overlay trên avatar · Toast khi xong |

---

## 5. API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load thông tin | GET | `/user/profile` | Khi mount |
| Cập nhật thông tin | PUT | `/user/profile` | Submit form |
| Upload avatar | POST | `/user/profile/avatar` | Chọn ảnh |

**Body PUT /user/profile:**
```json
{
  "full_name": "",
  "phone": "",
  "birthdate": "",
  "gender": "",
  "city": ""
}
```

**Body POST /user/profile/avatar:**
```
multipart/form-data: avatar (file, max 2MB)
```
