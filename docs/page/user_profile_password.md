# Màn hình: Đổi mật khẩu

> Route: `/profile/password`
> Quyền: 🔐 Cần đăng nhập
> Mô tả: Đổi mật khẩu tài khoản.

---

## Tái sử dụng từ màn Hồ sơ cá nhân

> Xem chi tiết layout tại `user_profile.md`

Giữ nguyên: Header · Breadcrumb · Sidebar (item "Đổi mật khẩu" active) · Footer

---

## Main Content — Form đổi mật khẩu

**Card:** `bg white border #E2E8F0 radius-16 p-32 max-w-480px`

**Card header** (`mb-24 pb-16 border-b #F1F5F9`):
- Title: `"Đổi mật khẩu" 18px Inter 600 #1E293B`
- Subtitle: `"Mật khẩu mới phải có ít nhất 8 ký tự" 13px #94A3B8 mt-4`

**Form fields** (`space-y-20`):

| Field | Type | Bắt buộc | Config |
|-------|------|----------|--------|
| Mật khẩu hiện tại | password | ✅ | icon `lock` trái · toggle show/hide |
| Mật khẩu mới | password | ✅ | icon `lock` trái · toggle show/hide |
| Xác nhận mật khẩu mới | password | ✅ | icon `lock` trái · toggle show/hide |

**Password strength indicator** (hiện khi nhập mật khẩu mới):
`mt-8`
- Bar: `h-4px radius-full flex gap-2`
  - 4 segments, fill theo độ mạnh:
    - Yếu (1/4): `bg #EF4444`
    - Trung bình (2/4): `bg #F59E0B`
    - Mạnh (3/4): `bg #0066CC`
    - Rất mạnh (4/4): `bg #10B981`
- Label: `"Yếu" / "Trung bình" / "Mạnh" / "Rất mạnh" 11px` màu tương ứng

**Validation realtime:**
- Mật khẩu mới ≥ 8 ký tự: icon `check_circle 14px #10B981` hoặc `cancel 14px #EF4444`
- Có chữ hoa: same
- Có số: same
- Xác nhận khớp: same

**Form footer** (`flex justify-end gap-12 mt-24 pt-16 border-t #F1F5F9`):
- "Hủy": `border #E2E8F0 bg white text #64748B radius-10 px-20 py-10`
  → reset form
- "Đổi mật khẩu": `bg #0066CC text white radius-10 px-20 py-10 14px 600`
  disabled khi chưa hợp lệ
  → `PUT /user/password`

**Link "Quên mật khẩu?":**
`text-right mt-8`
`12px #0066CC` → `/forgot-password`

---

## Submit States

| Tình huống | Xử lý |
|-----------|-------|
| Đang lưu | Button disabled · spinner |
| Thành công | Toast `bg #D1FAE5 text #10B981` "Đổi mật khẩu thành công!" · reset form |
| Sai mật khẩu hiện tại | Error inline `"Mật khẩu hiện tại không đúng" 12px #EF4444` |
| Không khớp | Error inline `"Mật khẩu xác nhận không khớp" 12px #EF4444` |

---

## API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Đổi mật khẩu | PUT | `/user/password` | Submit form |

**Body:**
```json
{
  "current_password": "*",
  "password": "*",
  "password_confirmation": "*"
}
```
