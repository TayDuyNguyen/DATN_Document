# Màn hình: Gửi Thông báo

> Route: `/admin/notifications/send`
> Quyền: 🛡️ Admin / Staff
> Mô tả: Form gửi thông báo đến 1 người dùng cụ thể hoặc toàn bộ người dùng. Hỗ trợ 2 mode: gửi cá nhân và gửi hàng loạt.

---

## Layout tổng thể

```
┌─────────────────────────────────────────────────────────────────┐
│  HEADER: Breadcrumb + Tiêu đề + [Hủy] [Gửi thông báo]         │
├──────────────────────────────────────┬──────────────────────────┤
│  LEFT COLUMN (65%)                   │  RIGHT COLUMN (320px)    │
│                                      │  sticky top-24           │
│  MODE TOGGLE: Cá nhân / Hàng loạt   │  Card 1: Xem trước       │
│  FORM CARD:                          │  Card 2: Hướng dẫn       │
│  - Người nhận (mode cá nhân)         │                          │
│  - Loại thông báo                    │                          │
│  - Tiêu đề                           │                          │
│  - Nội dung                          │                          │
│  - Dữ liệu bổ sung (optional)        │                          │
└──────────────────────────────────────┴──────────────────────────┘
```

---

## 1. Page Header

| Element | Style |
|---------|-------|
| Breadcrumb | `12px Inter 500 #94A3B8` — "Thông báo / Gửi Thông báo" |
| Title | `24px Inter 700 #1E293B` — "Gửi Thông báo" |
| Subtitle | `14px Inter 400 #64748B` — "Gửi thông báo đến người dùng hệ thống" |

**Buttons bên phải** (`flex gap-3`):

| Button | Style | Action |
|--------|-------|--------|
| Hủy | `border #E2E8F0 bg white text #64748B radius-10 px-20 py-10` hover `border #EF4444 text #EF4444` | Navigate `/admin/notifications` |
| Gửi thông báo | `bg #0066CC text white radius-10 px-20 py-10 shadow 14px 600` icon `send` | Submit form |

---

## 2. Left Column

### 2.1 Mode Toggle

`flex gap-0 bg white border #E2E8F0 radius-12 p-4 inline-flex mb-24`

| Mode | Style |
|------|-------|
| Gửi cá nhân | Active: `bg #0066CC text white radius-8 px-16 py-8 13px 600` |
| Gửi hàng loạt | Inactive: `bg transparent text #64748B px-16 py-8 13px 500` hover `text #0066CC` |

**Khi chọn "Gửi hàng loạt":**
- Info box xuất hiện bên dưới toggle:
  `bg #FEF3C7 border rgba(245,158,11,0.3) radius-10 p-14 mb-16 flex gap-10`
  - icon `warning_amber 20px #F59E0B`
  - text `13px #92400E`:
    "Thông báo sẽ được gửi đến **tất cả người dùng** trong hệ thống (4.850 người dùng).
    Hành động này không thể hoàn tác."

---

### 2.2 Form Card

**Card:** `bg white border #E2E8F0 radius-16 p-24`

**Section header** (`flex items-center gap-10 mb-24 pb-16 border-b #F1F5F9`):
- Icon: `send` · container `32x32px bg #EFF6FF radius-8 color #0066CC`
- Title: `"Nội dung thông báo" 15px Inter 600 #1E293B`

**Form Fields** (`space-y-20`):

**Field "Người nhận"** ✅ (chỉ hiện ở mode Cá nhân):
- Label: `"Người nhận *" 13px Inter 600 #1E293B mb-6`
- Search input với autocomplete:
  - `border #E2E8F0 radius-10 px-14 py-10 pl-40 14px Inter`
  - icon `search` trái `#94A3B8`
  - placeholder "Tìm theo tên, email, username..."
  - focus: `border #0066CC`
  - Khi nhập → dropdown kết quả (API: `GET /admin/users?q=...`):
    - Dropdown: `bg white border #E2E8F0 radius-10 shadow-modal mt-4 max-h-200px overflow-y-auto`
    - Mỗi item: `flex items-center gap-10 px-14 py-10 hover bg #F8FAFC cursor-pointer`
      - Avatar `28x28px rounded-full border #E2E8F0`
      - Name `13px Inter 600 #1E293B` + Email `11px #94A3B8`
- Khi đã chọn user → hiện selected card:
  `flex items-center gap-10 bg #EFF6FF border #B3D9FF radius-10 px-14 py-10`
  - Avatar `32x32px rounded-full`
  - Name `13px Inter 600 #0066CC` + Email `11px #64748B`
  - Button `×`: `icon close 16px #94A3B8` hover `#EF4444` → xóa selection

**Field "Loại thông báo"** ✅:
- Label: `"Loại thông báo *"`
- Select dropdown:
  - Đặt tour (booking) — icon `shopping_cart`
  - Đánh giá (rating) — icon `star`
  - Hệ thống (system) — icon `settings`
  - Khuyến mãi (promotion) — icon `local_offer`
- Mỗi option: `flex items-center gap-8` · icon `16px màu type` + text `13px #1E293B`
- `border #E2E8F0 radius-10 px-14 py-10 14px Inter`

**Field "Tiêu đề"** ✅:
- Input text
- placeholder "Nhập tiêu đề thông báo..."
- Character counter: `"0/100" 11px #94A3B8 text-right mt-4`

**Field "Nội dung"**:
- Textarea `rows-4`
- placeholder "Nhập nội dung thông báo..."
- `border #E2E8F0 radius-10 px-14 py-10 14px Inter resize-none`
- Character counter: `"0/500" 11px #94A3B8 text-right mt-4`

**Field "Dữ liệu bổ sung (data)"** (optional, collapsible):
- Toggle row: `flex justify-between items-center cursor-pointer`
  - Label: `"Dữ liệu bổ sung" 13px Inter 600 #64748B`
  - icon `expand_more` / `expand_less` `#94A3B8`
- Khi mở:
  - Textarea `rows-3`
  - placeholder `'{"booking_id": "BK-1008", "url": "/bookings/1008"}'`
  - Helper: `"JSON format. Dùng để điều hướng khi người dùng click thông báo." 12px #94A3B8`
  - `border #E2E8F0 radius-10 px-14 py-10 13px monospace`

**Form Footer** (`flex justify-end gap-12 mt-24 pt-16 border-t #F1F5F9`):
- "Hủy": `border #E2E8F0 bg white text #64748B radius-10 px-20 py-10`
- "Gửi thông báo": `bg #0066CC text white radius-10 px-20 py-10 14px 600 shadow` icon `send`

---

## 3. Right Column — Sidebar

### Card 1 — Xem trước
`bg white border #E2E8F0 radius-16 p-20 mb-16`

Title: `"Xem trước" 14px Inter 600 #1E293B mb-16`

**Preview notification card** (live update khi nhập):
`bg #F8FAFC border #E2E8F0 radius-12 p-16`

- `flex items-start gap-12`:
  - Icon container: `40x40px radius-10` bg màu theo loại (10% opacity)
    - icon loại `20px` màu theo loại
  - Right:
    - Tiêu đề: `14px Inter 600 #1E293B` (live) hoặc `"Tiêu đề thông báo" #94A3B8 italic`
    - Nội dung: `13px #64748B line-height 1.5 mt-4` (live, max 2 lines)
    - `flex items-center gap-8 mt-8`:
      - Badge loại: `11px 600 rounded-full px-8 py-3` màu theo loại
      - Time: `"Vừa xong" 11px #94A3B8`

**Người nhận** (mt-12, pt-12, border-t #F1F5F9):
- Mode cá nhân: `flex items-center gap-8`
  - Avatar `24x24px rounded-full` + Name `13px Inter 500 #1E293B`
  - hoặc `"Chưa chọn người nhận" 13px #94A3B8 italic`
- Mode hàng loạt: `flex items-center gap-8`
  - icon `group 16px #0066CC` + `"Tất cả 4.850 người dùng" 13px Inter 600 #0066CC`

---

### Card 2 — Hướng dẫn
`bg #EFF6FF border #B3D9FF radius-16 p-20`

Title: `"💡 Lưu ý" 13px Inter 600 #0066CC mb-12`

Items: icon `arrow_right #0066CC` + `12px #1E293B`
- "Tiêu đề nên ngắn gọn, rõ ràng (tối đa 100 ký tự)"
- "Thông báo hàng loạt không thể hoàn tác"
- "Dữ liệu bổ sung dùng để điều hướng khi click"
- "Người dùng nhận thông báo trong app và email"

---

## 4. Validation & States

| Tình huống | Xử lý |
|-----------|-------|
| Chưa chọn người nhận (mode cá nhân) | Error "Vui lòng chọn người nhận" |
| Tiêu đề trống | Border `#EF4444` · error text `12px #EF4444` |
| JSON không hợp lệ (data field) | Error "Dữ liệu JSON không hợp lệ" |
| Đang gửi | Button disabled · spinner · "Đang gửi..." · `bg #3385D6` |
| Gửi cá nhân thành công | Toast `bg #D1FAE5 text #10B981` "Đã gửi thông báo thành công!" · redirect `/admin/notifications` |
| Gửi hàng loạt thành công | Toast `bg #D1FAE5 text #10B981` "Đã gửi đến 4.850 người dùng!" · redirect `/admin/notifications` |
| Thất bại | Toast `bg #FEE2E2 text #EF4444` "Có lỗi xảy ra." |

**Confirm trước khi gửi hàng loạt:**
- Dialog `w-440px`:
  - Header: icon `warning_amber 40x40 bg #FEF3C7 radius-10 color #F59E0B` + "Xác nhận gửi hàng loạt?" `16px 700 #1E293B`
  - Body: "Thông báo sẽ được gửi đến **4.850 người dùng**. Hành động này không thể hoàn tác." `14px #64748B`
  - Footer: "Hủy" (ghost) + "Xác nhận gửi" `bg #0066CC text white`

---

## 5. API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Tìm kiếm user | GET | `/admin/users?q=` | Nhập search người nhận (debounce 300ms) |
| Gửi cá nhân | POST | `/admin/notifications/send` | Submit form mode cá nhân |
| Gửi hàng loạt | POST | `/admin/notifications/send-all` | Confirm dialog → submit |

**Body POST /admin/notifications/send:**
```json
{
  "user_id": "*",
  "type": "*",
  "title": "*",
  "content": "",
  "data": {}
}
```

**Body POST /admin/notifications/send-all:**
```json
{
  "type": "*",
  "title": "*",
  "content": "",
  "data": {}
}
```
