# Màn hình: Xóa tài khoản

> Route: `/profile/delete`
> Quyền: 🔐 Cần đăng nhập
> Mô tả: Xóa vĩnh viễn tài khoản người dùng với xác nhận mật khẩu và cảnh báo rõ ràng.

---

## Tái sử dụng từ màn Hồ sơ cá nhân

> Xem chi tiết layout tại `user_profile.md`

Giữ nguyên: Header · Breadcrumb · Sidebar (item "Xóa tài khoản" active, màu `#EF4444`) · Footer

---

## Main Content

**Card:** `bg white border #EF4444/20 radius-16 p-32 max-w-480px`

**Card header** (`mb-24 pb-16 border-b #FEE2E2`):
- icon `warning 24px #EF4444`
- Title: `"Xóa tài khoản" 18px Inter 600 #EF4444 mt-8`
- Subtitle: `"Hành động này không thể hoàn tác" 13px #94A3B8 mt-4`

---

### Warning Box

`bg #FEE2E2 border rgba(239,68,68,0.2) radius-12 p-16 mb-24`

- Title: `"⚠️ Trước khi xóa, hãy lưu ý:" 14px Inter 600 #EF4444 mb-12`
- List (`space-y-8`):
  - icon `cancel 14px #EF4444` + `"Tất cả dữ liệu cá nhân sẽ bị xóa vĩnh viễn" 13px #1E293B`
  - icon `cancel 14px #EF4444` + `"Lịch sử đặt tour và đánh giá sẽ bị xóa" 13px #1E293B`
  - icon `cancel 14px #EF4444` + `"Địa điểm yêu thích sẽ bị xóa" 13px #1E293B`
  - icon `cancel 14px #EF4444` + `"Bạn sẽ không thể khôi phục tài khoản này" 13px #1E293B`

---

### Kiểm tra đơn hàng đang hoạt động

**Nếu có đơn hàng pending/confirmed:**

`bg #FEF3C7 border rgba(245,158,11,0.2) radius-12 p-14 mb-20`
- icon `warning_amber 18px #F59E0B`
- Text `13px #92400E`:
  "Bạn có 2 đơn hàng đang hoạt động. Vui lòng hủy hoặc hoàn thành trước khi xóa tài khoản."
- Link "Xem đơn hàng →": `13px #0066CC` → `/bookings`

---

### Form xác nhận

**Checkbox xác nhận:**
`flex items-start gap-8 mb-20`
- Checkbox `16px accent-color #EF4444`
- Label: `13px #1E293B line-height 1.5`
  "Tôi hiểu rằng việc xóa tài khoản là vĩnh viễn và không thể hoàn tác."

**Input mật khẩu:**
- Label: `"Nhập mật khẩu để xác nhận *" 13px Inter 600 #1E293B mb-6`
- Input password: `border #E2E8F0 radius-10 px-14 py-12 14px Inter full-width`
  icon `lock` trái · toggle show/hide
  focus: `border #EF4444 ring rgba(239,68,68,0.15)`
  placeholder "Nhập mật khẩu của bạn..."

**Form footer** (`flex justify-between items-center mt-24 pt-16 border-t #FEE2E2`):
- "Hủy": `border #E2E8F0 bg white text #64748B radius-10 px-20 py-10`
  → navigate `/profile`
- "Xóa tài khoản": `bg #EF4444 text white radius-10 px-20 py-10 14px 600`
  disabled khi chưa check + chưa nhập MK
  hover `bg #DC2626`
  → mở confirm dialog

---

### Confirm Dialog (2 bước)

**Modal:** `bg white radius-16 w-400px shadow-modal backdrop rgba(0,0,0,0.5)`

- Header: icon `delete_forever 40x40 bg #FEE2E2 radius-10 color #EF4444`
  + `"Xác nhận xóa tài khoản?" 16px 700 #1E293B`
- Body:
  - `"Tài khoản của bạn sẽ bị xóa vĩnh viễn." 14px #64748B`
  - `"Hành động này KHÔNG THỂ hoàn tác." 14px Inter 700 #EF4444 mt-8`
- Footer:
  - "Hủy": `border #E2E8F0 bg white text #64748B radius-10 px-20 py-10`
  - "Xóa vĩnh viễn": `bg #EF4444 text white radius-10 px-20 py-10 14px 600`
    hover `bg #DC2626`
    → `DELETE /user/account`

---

## Submit States

| Tình huống | Xử lý |
|-----------|-------|
| Đang xóa | Button disabled · spinner · "Đang xóa..." |
| Sai mật khẩu | Error `"Mật khẩu không đúng" 12px #EF4444` |
| Xóa thành công | Clear token · redirect `/` · Toast `"Tài khoản đã được xóa"` |
| Thất bại | Toast `bg #FEE2E2 text #EF4444` "Có lỗi xảy ra." |

---

## API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Xóa tài khoản | DELETE | `/user/account` | Confirm dialog → xác nhận |

**Body:**
```json
{
  "password": "*"
}
```
