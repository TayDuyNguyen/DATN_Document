# Màn hình: Xác thực Email

> Route: `/verify-email`
> Quyền: 🔐 Cần đăng nhập (token từ email)
> Mô tả: Xác thực địa chỉ email sau khi đăng ký tài khoản. Người dùng nhận link/OTP qua email và xác nhận tại màn này.

---

## Layout tổng thể

```
┌─────────────────────────────────────────────────────────────┐
│  HEADER (minimal — chỉ logo)                                │
├─────────────────────────────────────────────────────────────┤
│  CENTER CARD: Nội dung xác thực                            │
│  (max-width 480px, mx-auto, mt-80px)                       │
├─────────────────────────────────────────────────────────────┤
│  FOOTER minimal                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 1. Header Minimal

`bg white border-b #E2E8F0 py-16 px-24`

- Logo "Đà Nẵng Trip" centered
- Không có navigation, không có auth buttons

---

## 2. Center Card

`bg white border #E2E8F0 radius-16 p-32 shadow-card max-w-480px mx-auto mt-80px`

---

## 3. Trạng thái: Đang xác thực (Auto-verify từ link email)

**Hiển thị khi:** URL có token param `?token=xxx&email=xxx`

`text-center py-16`

- Spinner: `48px #0066CC animate-spin mx-auto`
- Title: `"Đang xác thực email..." 20px Inter 600 #1E293B mt-16`
- Subtitle: `"Vui lòng chờ trong giây lát" 14px #94A3B8 mt-8`

→ Tự động gọi `POST /auth/verify-email` với token từ URL

---

## 4. Trạng thái: Nhập OTP thủ công

**Hiển thị khi:** Không có token trong URL (user vào trang trực tiếp)

`text-center`

- Icon: `mark_email_unread 64px #0066CC mx-auto`
- Title: `"Xác thực email của bạn" 22px Inter 700 #1E293B mt-16`
- Subtitle: `"Chúng tôi đã gửi mã xác thực đến" 14px #64748B mt-8`
- Email: `"nguyenvanan@gmail.com" 14px Inter 600 #0066CC`

**OTP Input** (`mt-24`):

`flex gap-12 justify-center`

- 6 ô input riêng biệt:
  - Mỗi ô: `w-48px h-56px border-2 #E2E8F0 radius-12 text-center 24px Inter 700 #1E293B`
  - focus: `border-2 #0066CC ring rgba(0,102,204,0.15)`
  - filled: `border-2 #0066CC bg #EFF6FF`
  - error: `border-2 #EF4444 bg rgba(239,68,68,0.04)`
  - Auto-focus next khi nhập · Auto-submit khi điền đủ 6 số
  - Backspace → focus previous

**Button "Xác thực"** (`mt-20 full-width`):
- Disabled khi chưa đủ 6 số: `bg #E2E8F0 text #94A3B8 cursor-not-allowed`
- Active: `bg #0066CC text white radius-12 py-14 16px 600`
  hover `bg #004999`

---

## 5. Trạng thái: Xác thực thành công

`text-center py-16`

- SVG icon `check_circle 80px #10B981 mx-auto`
- Title: `"Email đã được xác thực!" 22px Inter 700 #1E293B mt-16`
- Subtitle: `"Tài khoản của bạn đã được kích hoạt thành công." 14px #64748B mt-8`
- Countdown: `"Tự động chuyển hướng sau 3 giây..." 13px #94A3B8 mt-16`
  - Progress bar: `h-2px bg #E2E8F0 radius-full mt-8` · fill `bg #10B981` animate width 0→100% trong 3s
- Button "Về trang chủ": `bg #0066CC text white radius-12 py-12 px-24 14px 600 mt-16`
  → navigate `/` (hoặc redirect URL nếu có)

---

## 6. Trạng thái: Xác thực thất bại

`text-center py-16`

- SVG icon `error 80px #EF4444 mx-auto`
- Title: `"Xác thực thất bại" 22px Inter 700 #1E293B mt-16`
- Error message (dynamic):
  - Token hết hạn: `"Mã xác thực đã hết hạn. Vui lòng yêu cầu gửi lại." 14px #64748B mt-8`
  - Token sai: `"Mã xác thực không đúng. Vui lòng kiểm tra lại." 14px #64748B mt-8`
  - OTP sai: `"Mã OTP không chính xác. Còn 2 lần thử." 14px #EF4444 mt-8`

- Button "Thử lại": `bg #0066CC text white radius-12 py-12 px-24 14px 600 mt-16`
  → reset về trạng thái nhập OTP

---

## 7. Gửi lại email xác thực

**Hiển thị ở trạng thái nhập OTP và thất bại**

`mt-20 text-center`

- Text: `"Không nhận được email?" 13px #64748B`
- Button "Gửi lại" (countdown):
  - Còn thời gian: `"Gửi lại sau 45s" 13px #94A3B8 cursor-not-allowed`
    - Countdown timer giảm dần
  - Hết countdown: `"Gửi lại email" 13px #0066CC cursor-pointer` hover underline
    → `POST /auth/resend-verification`
    → Toast `"Đã gửi lại email xác thực!" bg #D1FAE5 text #10B981`
    → Reset countdown 60s

---

## 8. Thông báo đã xác thực rồi

**Hiển thị khi:** User đã xác thực email trước đó mà vào lại trang

`text-center py-16`

- icon `verified 64px #0066CC mx-auto`
- Title: `"Email đã được xác thực" 20px Inter 600 #1E293B mt-16`
- Subtitle: `"Tài khoản của bạn đã hoạt động bình thường." 14px #64748B mt-8`
- Button "Về trang chủ": `bg #0066CC text white radius-12 py-12 px-24 14px 600 mt-16`

---

## 9. API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Xác thực bằng token (link email) | POST | `/auth/verify-email` | Khi mount với `?token=` trong URL |
| Xác thực bằng OTP | POST | `/auth/verify-email` | Submit OTP form / Auto-submit khi đủ 6 số |
| Gửi lại email | POST | `/auth/resend-verification` | Click "Gửi lại email" |

**Body POST /auth/verify-email:**
```json
{
  "token": "*"
}
```
