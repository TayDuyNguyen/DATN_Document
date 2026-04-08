# Màn hình: Liên hệ (Master-Detail)

> Route: `/admin/contacts` · `/admin/contacts/{id}`
> Quyền: 🛡️ Admin / Staff
> Mô tả: Giao diện master-detail — danh sách liên hệ bên trái, chi tiết + form trả lời bên phải. Không chuyển trang khi xem chi tiết.

---

## Layout tổng thể

```
┌─────────────────────────────────────────────────────────────────┐
│  HEADER: Breadcrumb + Tiêu đề + [Xuất Excel]                    │
├─────────────────────────────────────────────────────────────────┤
│  STATS ROW: [Tổng LH] [Mới] [Đã đọc] [Đã trả lời]             │
├──────────────────────────────────┬──────────────────────────────┤
│  PANEL TRÁI (380px, fixed)       │  PANEL PHẢI (flex-1)         │
│                                  │                              │
│  Search + Filter status          │  [Chưa chọn] Empty state     │
│  ─────────────────────────────   │  hoặc                        │
│  List item (click → load phải)   │  Chi tiết liên hệ            │
│  - Tên + email                   │  + Form trả lời              │
│  - Subject preview               │  + Nội dung đã trả lời       │
│  - Badge status + time           │                              │
│  ─────────────────────────────   │                              │
│  Pagination mini                 │                              │
└──────────────────────────────────┴──────────────────────────────┘
```

---

## 1. Page Header

| Element | Style |
|---------|-------|
| Breadcrumb | `12px Inter 500 #94A3B8` — "Liên hệ" |
| Title | `24px Inter 700 #1E293B` — "Liên hệ" |
| Subtitle | `14px Inter 400 #64748B` — "Quản lý yêu cầu liên hệ từ khách hàng" |
| Button "Xuất Excel" | `border #E2E8F0 bg white text #64748B radius-10 px-16 py-10` icon `download` | `GET /admin/contacts/export` |

---

## 2. Stats Row

`grid grid-cols-4 gap-4 mb-24`

| Thẻ | Icon | Icon bg | Value | Label | Value color | Ghi chú |
|-----|------|---------|-------|-------|-------------|---------|
| Tổng liên hệ | `mail` | `#EFF6FF` | `248` | "TỔNG LIÊN HỆ" | `#1E293B` | |
| Mới | `mark_email_unread` | `#FEE2E2` | `12` | "MỚI" | `#EF4444` | Pulse animation |
| Đã đọc | `drafts` | `#FEF3C7` | `186` | "ĐÃ ĐỌC" | `#F59E0B` | |
| Đã trả lời | `mark_email_read` | `#D1FAE5` | `50` | "ĐÃ TRẢ LỜI" | `#10B981` | |

---

## 3. Panel trái — Danh sách

`width 380px, border-r #E2E8F0, height calc(100vh - header), overflow-y auto, flex-shrink-0`

### 3.1 Toolbar

`px-16 py-12 border-b #E2E8F0 space-y-8`

- Search: `border #E2E8F0 radius-8 px-10 py-8 pl-36 13px full-width` icon `search` trái · placeholder "Tìm liên hệ..."
- Filter tabs (`flex gap-4 mt-8`):
  - "Tất cả" | "Mới" | "Đã đọc" | "Đã trả lời"
  - Active: `bg #0066CC text white radius-6 px-10 py-5 11px 600`
  - Inactive: `bg #F1F5F9 text #64748B radius-6 px-10 py-5 11px 500` hover `text #0066CC`

### 3.2 Contact List Items

Mỗi item (`px-16 py-14 border-b #F1F5F9 cursor-pointer`):
- Hover: `bg #F8FAFC`
- Active (đang xem): `bg #EFF6FF border-l-3 #0066CC`
- Status=new: `bg #FFF5F5`

**Layout mỗi item:**

Row 1 (`flex justify-between items-start`):
- Left: Name `13px Inter 600 #1E293B`
- Right: Time `11px #94A3B8` — e.g. "2 giờ trước"

Row 2 (`mt-2`):
- Subject: `12px Inter 500 #64748B max-1-line ellipsis`

Row 3 (`flex justify-between items-center mt-6`):
- Message preview: `11px #94A3B8 max-1-line ellipsis flex-1`
- Badge status `11px 700 rounded-full px-8 py-2 ml-8`:
  - new: `bg #FEE2E2 text #EF4444` "MỚI"
  - read: `bg #FEF3C7 text #F59E0B` "ĐÃ ĐỌC"
  - replied: `bg #D1FAE5 text #10B981` "ĐÃ TRẢ LỜI"

**Unread dot** (status=new): `w-2 h-2 rounded-full bg #EF4444 absolute left-6 top-1/2`

### 3.3 Pagination mini

`px-16 py-10 border-t #E2E8F0 flex justify-between items-center`
- `"1–10 / 248" 11px #94A3B8`
- Prev / Next: `24x24px border #E2E8F0 radius-6 bg white color #64748B`
  hover `border #0066CC color #0066CC`

---

## 4. Panel phải — Chi tiết & Trả lời

`flex-1 overflow-y-auto`

### 4.1 Empty State (chưa chọn liên hệ)

`center h-full`:
- SVG icon `mail 80x80px color #E2E8F0`
- Title: `"Chọn một liên hệ để xem chi tiết" 16px Inter 600 #1E293B`
- Subtitle: `"Danh sách liên hệ ở bên trái" 14px #94A3B8`

### 4.2 Detail Header

`px-32 py-20 border-b #E2E8F0 flex justify-between items-start`

**Bên trái:**
- Subject: `20px Inter 700 #1E293B`
- `flex items-center gap-8 mt-6`:
  - Badge status
  - `"Gửi lúc 06/04/2026 14:30" 12px #94A3B8`

**Bên phải** (`flex gap-8`):
- Button xóa: `border #FEE2E2 bg white text #EF4444 radius-8 px-12 py-8 13px 600` icon `delete`
  hover `bg #FEE2E2` → confirm → `DELETE /admin/contacts/{id}`

### 4.3 Sender Info

`px-32 py-20 border-b #E2E8F0 flex items-start gap-16`

- Avatar: `48x48px rounded-full border-2 #E2E8F0`
- Right:
  - Name: `16px Inter 700 #1E293B`
  - `flex gap-16 mt-6`:
    - icon `email 16px #94A3B8` + email `13px #64748B` link `mailto:`
    - icon `phone 16px #94A3B8` + phone `13px #64748B` (nếu có)

### 4.4 Message Content

`px-32 py-20 border-b #E2E8F0`

- Label: `"NỘI DUNG" 10px uppercase #94A3B8 mb-10`
- `bg #F8FAFC border #E2E8F0 radius-12 p-20`
- Text: `15px Inter 400 #1E293B line-height 1.7 white-space pre-wrap`

### 4.5 Form Trả lời (chỉ hiện nếu status ≠ replied)

`px-32 py-20 border-b #E2E8F0`

- Section label: `flex items-center gap-8 mb-16`
  - icon `reply 18px #10B981`
  - `"Trả lời" 15px Inter 600 #1E293B`

- Reply to: `bg #F8FAFC border #E2E8F0 radius-8 px-14 py-10 flex items-center gap-8 mb-16`
  - icon `send 16px #94A3B8` + `"Gửi đến: email@example.com" 13px #64748B`

- Textarea: `rows-5 border #E2E8F0 radius-10 px-14 py-12 14px Inter resize-none full-width`
  placeholder "Nhập nội dung trả lời..."
  focus: `border #0066CC`
  counter: `"0/2000" 11px #94A3B8 text-right mt-4`

- `flex justify-between items-center mt-16`:
  - Left: `"Trả lời sẽ được gửi qua email" 12px #94A3B8` icon `info 14px`
  - Right: Button "Gửi trả lời" `bg #10B981 text white radius-10 px-20 py-10 14px 600` icon `send`
    hover `bg #059669` → `POST /admin/contacts/{id}/reply`

### 4.6 Nội dung đã trả lời (chỉ hiện nếu status = replied)

`px-32 py-20`

- `flex justify-between items-center mb-16`:
  - Left: `flex items-center gap-8`
    - icon `mark_email_read 18px #10B981`
    - `"Đã trả lời" 15px Inter 600 #1E293B`
  - Right: `"06/04/2026 16:45 · Admin Duy Tây" 12px #94A3B8`

- `bg #D1FAE5/20 border #10B981/20 radius-12 p-20`
  - Label: `"NỘI DUNG TRẢ LỜI" 10px uppercase #10B981 mb-10`
  - Text: `15px Inter 400 #1E293B line-height 1.7 white-space pre-wrap`

- `flex items-center gap-8 mt-12`
  - icon `check_circle 16px #10B981` + `"Email đã được gửi đến khách hàng" 12px #10B981`

---

## 5. Confirm Delete Dialog

**Modal:** `bg white radius-16 w-400px shadow-modal backdrop rgba(0,0,0,0.4)`

| Vùng | Nội dung |
|------|---------|
| Header | Icon `delete 40x40 bg #FEE2E2 radius-10 color #EF4444` + "Xóa liên hệ này?" `16px 700 #1E293B` |
| Body | "Liên hệ từ [Tên] sẽ bị xóa vĩnh viễn." `14px #64748B` |
| Footer | "Hủy" (ghost) + "Xóa" `bg #EF4444 hover #DC2626` |

Sau khi xóa: panel phải về empty state, item bị xóa khỏi list trái.

---

## 6. Submit States

| Tình huống | Xử lý |
|-----------|-------|
| Nội dung trả lời trống | Border `#EF4444` · error text `12px #EF4444` |
| Đang gửi | Button disabled · spinner · "Đang gửi..." |
| Gửi thành công | Toast `bg #D1FAE5 text #10B981` "Đã gửi trả lời!" · badge đổi "ĐÃ TRẢ LỜI" · form ẩn · nội dung trả lời hiện |
| Thất bại | Toast `bg #FEE2E2 text #EF4444` "Có lỗi xảy ra." |

---

## 7. API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load danh sách | GET | `/admin/contacts?page=&per_page=&status=` | Khi mount, đổi filter |
| Tìm kiếm | GET | `/admin/contacts?search=` | Nhập search (debounce 300ms) |
| Load chi tiết | GET | `/admin/contacts/{id}` | Click item trong list (tự động đổi new → read) |
| Gửi trả lời | POST | `/admin/contacts/{id}/reply` | Submit form trả lời |
| Xóa liên hệ | DELETE | `/admin/contacts/{id}` | Confirm dialog |
| Xuất Excel | GET | `/admin/contacts/export?status=` | Click "Xuất Excel" |
