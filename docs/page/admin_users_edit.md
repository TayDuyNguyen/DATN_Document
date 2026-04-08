# Màn hình: Chỉnh sửa Người dùng

> Route: `/admin/users/{id}/edit`
> Quyền: 🛡️ Admin / Staff
> Mô tả: Form chỉnh sửa thông tin người dùng. Tái sử dụng layout từ màn Tạo Người dùng, không cho phép đổi username và mật khẩu qua form này.

---

## Tái sử dụng từ màn Tạo Người dùng

> Xem chi tiết tại `admin_users_create.md`

Giữ nguyên:
- Layout 2 cột (left form + right sidebar 320px)
- Fields: Họ tên · Email · Phone · Ngày sinh · Giới tính · Thành phố
- Divider "Thông tin bổ sung"
- Design system, màu sắc, spacing

---

## Điểm khác biệt

---

### 1. Page Header

| Element | Tạo | Chỉnh sửa |
|---------|-----|-----------|
| Breadcrumb | ".../ Tạo mới" | ".../ Nguyễn Văn An / Chỉnh sửa" |
| Title | "Tạo Người dùng mới" | "Chỉnh sửa Người dùng" |
| Subtitle | "Thêm tài khoản..." | Tên người dùng `14px Inter 500 #64748B` |
| Button Hủy | → `/admin/users` | → `/admin/users/{id}` (chi tiết) |
| Button phụ | — | "Xem hồ sơ" icon `open_in_new` → `/admin/users/{id}` |
| Button chính | "Tạo người dùng" | "Lưu thay đổi" → `PUT /admin/users/{id}` |

---

### 2. Loading State

Khi fetch `GET /admin/users/{id}` chưa xong:
- Skeleton loading toàn bộ form: `h-10 bg #E2E8F0 radius-10 animation pulse`
- Spinner nhỏ + `"Đang tải dữ liệu..." 13px #94A3B8`

---

### 3. Form Fields Khác

**Bỏ hoàn toàn:** Username input · Mật khẩu · Xác nhận mật khẩu

**Thêm Username readonly** (thay input):
- `flex flex-col gap-4`
  - Label: `"USERNAME" 11px uppercase #94A3B8`
  - `flex items-center gap-8`:
    - Value: `"@nguyenvanan" 14px monospace #64748B`
    - Badge: `"Không thể thay đổi" bg #F1F5F9 text #94A3B8 11px radius-full px-8 py-2`

**Thêm info box mật khẩu** (`col-span-2`):
- `bg #EFF6FF border #B3D9FF radius-8 p-12`
- icon `info #0066CC` + text `13px #1E293B`:
  "Để đổi mật khẩu, vui lòng yêu cầu người dùng dùng chức năng 'Quên mật khẩu' hoặc liên hệ admin cấp cao."

**Email field:** Pre-filled · khi thay đổi → warning box bên dưới:
- `bg #FEF3C7 border rgba(245,158,11,0.3) radius-8 p-10 mt-6`
- icon `warning_amber #F59E0B` + text `12px #92400E`:
  "Thay đổi email sẽ yêu cầu xác thực lại."

**Tất cả fields còn lại:** Pre-filled từ response `GET /admin/users/{id}`

---

### 4. Section Header

- Icon: `edit` (thay `person_add`)
- Title: `"Chỉnh sửa thông tin"`

---

### 5. Sidebar — Card "Cài đặt tài khoản"

- Radio Role: pre-selected theo role hiện tại
- Toggle Trạng thái: pre-set theo status hiện tại

**Thêm block "Thông tin"** (trên buttons, `border-t #F1F5F9 pt-16`):
- Label: `"THÔNG TIN" 10px uppercase #94A3B8 mb-8`

| Label | Value |
|-------|-------|
| Ngày tham gia | "15/03/2026 09:30" `13px #64748B` |
| Cập nhật lần cuối | "01/04/2026 14:22" `13px #64748B` |
| Xác thực email | Badge "ĐÃ XÁC THỰC" `bg #D1FAE5 text #10B981` hoặc "CHƯA XÁC THỰC" `bg #FEF3C7 text #F59E0B` |

**Buttons:**
| Button | Tạo | Chỉnh sửa |
|--------|-----|-----------|
| Chính | "Tạo người dùng" | "Lưu thay đổi" |
| Phụ | "Hủy" | "Hủy thay đổi" → confirm nếu có thay đổi chưa lưu |

---

### 6. Sidebar — Card mới: "Thao tác nhanh"

Thêm sau Card Cài đặt:
`bg white border #E2E8F0 radius-16 p-20 mb-16`

Title: `"Thao tác nhanh" 14px Inter 600 #1E293B mb-12`

| Button | Icon | Hover | Action |
|--------|------|-------|--------|
| Xem hồ sơ | `person` | `border #0066CC text #0066CC` | `/admin/users/{id}` |
| Xem đơn hàng | `shopping_cart` | `border #0066CC text #0066CC` | `/admin/bookings?user_id={id}` |
| Khóa tài khoản (active) | `block` | `bg #FEE2E2` | `PATCH /admin/users/{id}/status { status: "banned" }` |
| Mở khóa (banned) | `lock_open` | — | `PATCH /admin/users/{id}/status { status: "active" }` · `bg #10B981 text white` |
| Xóa tài khoản | `delete` | `bg #FEE2E2` | Confirm → `DELETE /admin/users/{id}` → redirect `/admin/users` |

Ghost style: `border #E2E8F0 bg white text #64748B radius-10 py-10 full-width 13px 600`
Khóa/Xóa: `border #FEE2E2 text #EF4444`
Mở khóa: `bg #10B981 text white radius-10 py-10 full-width 13px 600`

---

### 7. Unsaved Changes Guard

Khi navigate away khi có thay đổi chưa lưu:

| Button | Style | Action |
|--------|-------|--------|
| Tiếp tục chỉnh sửa | `bg #0066CC text white radius-10` | Đóng dialog |
| Bỏ thay đổi | `border #E2E8F0 text #64748B` hover `text #EF4444` | Navigate away |

---

### 8. Submit States

| Tình huống | Xử lý |
|-----------|-------|
| Đang lưu | Button disabled · spinner · "Đang lưu..." · `bg #3385D6 cursor-not-allowed` |
| Thành công | Toast `bg #D1FAE5 text #10B981` "Cập nhật thành công!" · ở lại trang edit |
| Thất bại | Toast `bg #FEE2E2 text #EF4444` "Có lỗi xảy ra. Vui lòng thử lại." |
| Xóa thành công | Toast `bg #D1FAE5 text #10B981` "Đã xóa tài khoản." · redirect `/admin/users` |

---

## API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load dữ liệu | GET | `/admin/users/{id}` | Khi mount |
| Lưu thay đổi | PUT | `/admin/users/{id}` | Submit form |
| Đổi trạng thái | PATCH | `/admin/users/{id}/status` | Button khóa/mở khóa |
| Xóa tài khoản | DELETE | `/admin/users/{id}` | Confirm dialog |

**Body PUT /admin/users/{id}:** (all optional)
```json
{
  "full_name": "",
  "phone": "",
  "city": "",
  "role": "",
  "status": ""
}
```
