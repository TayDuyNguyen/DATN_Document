# Màn hình: Tạo Người dùng mới

> Route: `/admin/users/create`
> Quyền: 🛡️ Admin / Staff
> Mô tả: Form tạo tài khoản người dùng mới với thông tin cơ bản, phân quyền và trạng thái.

---

## Layout tổng thể

```
┌─────────────────────────────────────────────────────────────────┐
│  HEADER: Breadcrumb + Tiêu đề + [Hủy] [Tạo người dùng]        │
├──────────────────────────────────────┬──────────────────────────┤
│  LEFT COLUMN (65%)                   │  RIGHT COLUMN (320px)    │
│                                      │  sticky top-24           │
│  FORM CARD:                          │  Card 1: Cài đặt TK      │
│  - Họ tên · Username · Email         │  Card 2: Hướng dẫn       │
│  - Mật khẩu · Xác nhận MK           │                          │
│  - Divider "Thông tin bổ sung"       │                          │
│  - Phone · Ngày sinh · GT · TP       │                          │
│  - Form footer                       │                          │
└──────────────────────────────────────┴──────────────────────────┘
```

---

## 1. Page Header

| Element | Style |
|---------|-------|
| Breadcrumb | `12px Inter 500 #94A3B8` — "Người dùng / Danh sách Người dùng / Tạo mới" |
| Title | `24px Inter 700 #1E293B` — "Tạo Người dùng mới" |
| Subtitle | `14px Inter 400 #64748B` — "Thêm tài khoản người dùng vào hệ thống" |

**Buttons bên phải** (`flex gap-3`):

| Button | Style | Action |
|--------|-------|--------|
| Hủy | `border #E2E8F0 bg white text #64748B radius-10 px-20 py-10` hover `border #EF4444 text #EF4444` | Navigate `/admin/users` |
| Tạo người dùng | `bg #0066CC text white radius-10 px-20 py-10 shadow 14px 600` hover `bg #004999` | Submit `POST /admin/users` |

---

## 2. Left Column — Form Card

**Card:** `bg white border #E2E8F0 radius-16 p-24`

**Section header** (`flex items-center gap-10 mb-24 pb-16 border-b #F1F5F9`):
- Icon: `person_add` · container `32x32px bg #EFF6FF radius-8 color #0066CC`
- Title: `"Thông tin tài khoản" 15px Inter 600 #1E293B`

### Form Fields

`grid grid-cols-2 gap-20`

| Field | Type | Bắt buộc | Col | Config |
|-------|------|----------|-----|--------|
| Họ và tên | text | ✅ | 2 | placeholder "Nhập họ và tên đầy đủ" |
| Username | text | ✅ | 1 | placeholder "nguyenvanan" · prefix "@" `absolute left-14 14px #94A3B8` · helper "Chỉ dùng chữ thường, số và dấu gạch dưới" |
| Email | email | ✅ | 1 | placeholder "example@email.com" · icon `email` trái `#94A3B8` |
| Mật khẩu | password | ✅ | 1 | icon `lock` trái · button toggle show/hide `absolute right-14` · helper "Tối thiểu 8 ký tự, bao gồm chữ và số" |
| Xác nhận mật khẩu | password | ✅ | 1 | icon `lock` trái · validation: phải khớp với mật khẩu |

**Divider** (`col-span-2`):
- `1px solid #F1F5F9` · label `"THÔNG TIN BỔ SUNG" 11px uppercase #94A3B8 bg white px-12 absolute center`

| Field | Type | Bắt buộc | Col | Config |
|-------|------|----------|-----|--------|
| Số điện thoại | tel | — | 1 | placeholder "0905 xxx xxx" · icon `phone` trái |
| Ngày sinh | date | — | 1 | icon `cake` trái |
| Giới tính | select | — | 1 | Chưa chọn / Nam / Nữ / Khác |
| Thành phố | text | — | 1 | placeholder "Đà Nẵng" · icon `location_on` trái |

### Form Footer

`flex justify-end gap-12 mt-24 pt-16 border-t #F1F5F9`

| Button | Style | Action |
|--------|-------|--------|
| Hủy | `border #E2E8F0 bg white text #64748B radius-10 px-20 py-10` hover `border #EF4444 text #EF4444` | Navigate `/admin/users` |
| Tạo người dùng | `bg #0066CC text white radius-10 px-20 py-10 14px 600 shadow` hover `bg #004999` | Submit form |

---

## 3. Right Column — Sidebar

### Card 1 — Cài đặt tài khoản
`bg white border #E2E8F0 radius-16 p-20 mb-16`

**Role** (radio group `flex-col gap-10`):

| Option | Badge | Helper |
|--------|-------|--------|
| ● Người dùng (user) — default | `bg #F1F5F9 text #64748B` "USER" | "Khách hàng thông thường" |
| ○ Staff (staff) | `bg #EFF6FF text #0066CC` "STAFF" | "Nhân viên hỗ trợ" |
| ○ Admin (admin) | `bg #EEF2FF text #6366F1` "ADMIN" | "Quản trị viên toàn quyền" |

Helper: `12px #94A3B8`

**Toggle Trạng thái** (`flex justify-between items-center py-12 border-t #F1F5F9`):
- Label: `"Kích hoạt ngay" 14px #1E293B` + `"Tài khoản có thể đăng nhập ngay" 12px #94A3B8`
- Toggle: ON `#0066CC`, OFF `#E2E8F0`, `40x22px`, default ON

**Buttons:**
- "Tạo người dùng": `bg #0066CC text white radius-10 py-12 full-width 14px 600 shadow`
- "Hủy": `border #E2E8F0 bg white text #64748B radius-10 py-12 full-width mt-8` hover `border #EF4444 text #EF4444`

---

### Card 2 — Hướng dẫn
`bg #EFF6FF border #B3D9FF radius-16 p-20`

- Title: `"💡 Lưu ý" 13px Inter 600 #0066CC mb-12`
- Items: icon `arrow_right #0066CC` + `12px #1E293B`
  - "Username phải là duy nhất trong hệ thống"
  - "Mật khẩu nên có ít nhất 8 ký tự"
  - "Email dùng để đăng nhập và nhận thông báo"
  - "Role Admin có toàn quyền quản trị hệ thống"

---

## 4. Validation & States

| Tình huống | Xử lý |
|-----------|-------|
| Field bắt buộc trống | Border `#EF4444` · bg `rgba(239,68,68,0.04)` · error text `12px #EF4444` · scroll to first error |
| Email đã tồn tại | Error "Email này đã được sử dụng" |
| Username đã tồn tại | Error "Username này đã được sử dụng" |
| Mật khẩu không khớp | Error "Mật khẩu xác nhận không khớp" |
| Đang submit | Button disabled · spinner · "Đang tạo..." · `bg #3385D6 cursor-not-allowed` |
| Thành công | Toast `bg #D1FAE5 text #10B981` "Tạo người dùng thành công!" · redirect `/admin/users/{id}` |
| Thất bại | Toast `bg #FEE2E2 text #EF4444` "Có lỗi xảy ra. Vui lòng thử lại." |

---

## 5. API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Tạo người dùng | POST | `/admin/users` | Submit form |

**Body POST /admin/users:**
```json
{
  "username": "*",
  "email": "*",
  "password": "*",
  "full_name": "*",
  "role": "user",
  "status": "active"
}
```
