# Màn hình: Chi tiết & Trả lời Liên hệ

> Route: `/admin/contacts/{id}`
> Quyền: 🛡️ Admin / Staff
> Mô tả: Xem nội dung liên hệ đầy đủ và trả lời qua email. Khi mở trang, trạng thái tự động chuyển từ "new" → "read".

---

## Layout tổng thể

```
┌─────────────────────────────────────────────────────────────────┐
│  HEADER: Breadcrumb + Chủ đề + Badge status + [Xóa] [← Quay]  │
├──────────────────────────────────────┬──────────────────────────┤
│  LEFT COLUMN (65%)                   │  RIGHT COLUMN (320px)    │
│                                      │  sticky top-24           │
│  Section 1: Nội dung liên hệ         │  Card 1: Thông tin       │
│  Section 2: Form trả lời             │  Card 2: Thao tác        │
│  Section 3: Nội dung đã trả lời      │                          │
│             (nếu đã replied)         │                          │
└──────────────────────────────────────┴──────────────────────────┘
```

---

## 1. Page Header

`flex justify-between items-start, mb 24px`

### Bên trái

| Element | Style |
|---------|-------|
| Breadcrumb | `12px Inter 500 #94A3B8` — "Liên hệ / Danh sách Liên hệ / Hỏi về tour Bà Nà Hills" |
| Title + Badge | `flex items-center gap-12 mt-4` |
| Title | `24px Inter 700 #1E293B` — subject của liên hệ |
| Badge status | `11px 700 rounded-full px-10 py-4` |
| Subtitle | `13px Inter 400 #94A3B8` — "Gửi lúc 06/04/2026 14:30" |

**Badge status:**
| Status | Background | Text |
|--------|-----------|------|
| new | `#FEE2E2` | `#EF4444` "MỚI" |
| read | `#FEF3C7` | `#F59E0B` "ĐÃ ĐỌC" |
| replied | `#D1FAE5` | `#10B981` "ĐÃ TRẢ LỜI" |

### Bên phải (`flex gap-3`)

| Button | Style | Action |
|--------|-------|--------|
| ← Quay lại | `border #E2E8F0 bg white text #64748B radius-10 px-16 py-10` icon `arrow_back` | Navigate `/admin/contacts` |
| Xóa liên hệ | `border #FEE2E2 bg white text #EF4444 radius-10 px-16 py-10` icon `delete` hover `bg #FEE2E2` | Confirm → `DELETE /admin/contacts/{id}` |

---

## 2. Left Column

### Section 1 — Nội dung liên hệ

**Card:** `bg white border #E2E8F0 radius-16 p-24 mb-24`

**Section header** (`flex items-center gap-10 mb-20 pb-16 border-b #F1F5F9`):
- Icon: `mail #0066CC bg #EFF6FF` · Title: `"Nội dung liên hệ" 15px Inter 600 #1E293B`

**Sender info** (`flex items-start gap-16 mb-20`):
- Avatar: `48x48px rounded-full border-2 #E2E8F0`
  - Nếu không có: bg gradient initials · text white `16px 700`
- Right:
  - Name: `16px Inter 700 #1E293B`
  - `flex gap-16 mt-6`:
    - icon `email 16px #94A3B8` + email `13px #64748B` (link `mailto:` hover `#0066CC`)
    - icon `phone 16px #94A3B8` + phone `13px #64748B` (nếu có, link `tel:`)
  - `flex gap-8 mt-6`:
    - Badge subject: `bg #EFF6FF text #0066CC border #B3D9FF radius-full px-10 py-4 11px 600`
      — e.g. "Hỏi về tour Bà Nà Hills"

**Message content** (`bg #F8FAFC border #E2E8F0 radius-12 p-20 mt-4`):
- Label: `"NỘI DUNG" 10px uppercase #94A3B8 mb-10`
- Text: `15px Inter 400 #1E293B line-height 1.7 white-space pre-wrap`

---

### Section 2 — Form trả lời

**Card:** `bg white border #E2E8F0 radius-16 p-24 mb-24`

**Chỉ hiện nếu status ≠ replied.**

**Section header** (`flex items-center gap-10 mb-20 pb-16 border-b #F1F5F9`):
- Icon: `reply #10B981 bg #D1FAE5` · Title: `"Trả lời" 15px Inter 600 #1E293B`

**Reply to info** (`flex items-center gap-8 mb-16`):
- `bg #F8FAFC border #E2E8F0 radius-8 px-14 py-10 flex items-center gap-8`
- icon `send 16px #94A3B8`
- Text: `"Gửi đến: nguyenvanan@gmail.com" 13px Inter 500 #64748B`

**Textarea "Nội dung trả lời"** ✅:
- `rows-6 border #E2E8F0 radius-10 px-14 py-12 14px Inter #1E293B line-height 1.7 resize-none`
- placeholder "Nhập nội dung trả lời..."
- focus: `border #0066CC ring rgba(0,102,204,0.15)`
- Character counter: `"0/2000" 11px #94A3B8 text-right mt-4`

**Form footer** (`flex justify-between items-center mt-16`):
- Left: `"Trả lời sẽ được gửi qua email đến khách hàng" 12px #94A3B8` icon `info 14px #94A3B8`
- Right (`flex gap-12`):
  - "Hủy": `border #E2E8F0 bg white text #64748B radius-10 px-20 py-10`
  - "Gửi trả lời": `bg #10B981 text white radius-10 px-20 py-10 14px 600` icon `send`
    hover `bg #059669`
    → `POST /admin/contacts/{id}/reply`

---

### Section 3 — Nội dung đã trả lời

**Chỉ hiện nếu status = replied.**

**Card:** `bg white border #E2E8F0 radius-16 p-24 mb-24`

**Section header** (`flex items-center gap-10 mb-20 pb-16 border-b #F1F5F9`):
- Icon: `mark_email_read #10B981 bg #D1FAE5` · Title: `"Đã trả lời" 15px Inter 600 #1E293B`

**Reply info** (`flex items-center gap-8 mb-16`):
- `flex justify-between items-center`
- Left: `flex items-center gap-8`
  - icon `person 16px #94A3B8` + `"Trả lời bởi: Admin Duy Tây" 13px #64748B`
- Right: `"06/04/2026 16:45" 12px #94A3B8`

**Reply content** (`bg #D1FAE5/20 border #10B981/20 radius-12 p-20`):
- Label: `"NỘI DUNG TRẢ LỜI" 10px uppercase #10B981 mb-10`
- Text: `15px Inter 400 #1E293B line-height 1.7 white-space pre-wrap`

**Note** (`mt-12 flex items-center gap-8`):
- icon `check_circle 16px #10B981`
- `"Email đã được gửi đến nguyenvanan@gmail.com" 12px #10B981`

---

## 3. Right Column — Sidebar

### Card 1 — Thông tin
`bg white border #E2E8F0 radius-16 p-20 mb-16`

Title: `"Thông tin liên hệ" 14px Inter 600 #1E293B mb-16`

Rows (`space-y-12 flex justify-between items-start 13px`):

| Label | Value |
|-------|-------|
| Trạng thái | Badge status |
| Họ tên | "Nguyễn Văn An" `#1E293B` |
| Email | "nguyenvanan@gmail.com" link `#0066CC` |
| Điện thoại | "0905 xxx xxx" hoặc "—" |
| Chủ đề | "Hỏi về tour Bà Nà Hills" `#1E293B` |
| Ngày gửi | "06/04/2026 14:30" `#64748B` |
| Trả lời lúc | "06/04/2026 16:45" hoặc "—" `#64748B` |
| Trả lời bởi | "Admin Duy Tây" hoặc "—" `#64748B` |

---

### Card 2 — Thao tác
`bg white border #E2E8F0 radius-16 p-20 mb-16`

Title: `"Thao tác" 14px Inter 600 #1E293B mb-12`

| Button | Style | Action |
|--------|-------|--------|
| Gửi trả lời (nếu chưa replied) | `bg #10B981 text white radius-10 py-10 full-width` icon `reply` | Scroll to form trả lời |
| Gửi email trực tiếp | ghost icon `email` | Mở `mailto:email?subject=Re: [subject]` |
| Xóa liên hệ | `border #FEE2E2 text #EF4444` hover `bg #FEE2E2` icon `delete` | Confirm → `DELETE /admin/contacts/{id}` → redirect `/admin/contacts` |

Ghost style: `border #E2E8F0 bg white text #64748B radius-10 py-10 full-width 13px 600` hover `border #0066CC text #0066CC`

---

## 4. Confirm Delete Dialog

**Modal:** `bg white radius-16 w-400px shadow-modal backdrop rgba(0,0,0,0.4)`

| Vùng | Nội dung |
|------|---------|
| Header | Icon `delete 40x40 bg #FEE2E2 radius-10 color #EF4444` + "Xóa liên hệ này?" `16px 700 #1E293B` |
| Body | "Liên hệ từ [Tên] sẽ bị xóa vĩnh viễn." `14px #64748B` |
| Footer | "Hủy" (ghost) + "Xóa" `bg #EF4444 hover #DC2626` |

---

## 5. Submit States

| Tình huống | Xử lý |
|-----------|-------|
| Nội dung trả lời trống | Border `#EF4444` · error text `12px #EF4444` |
| Đang gửi | Button disabled · spinner · "Đang gửi..." · `bg #059669` |
| Gửi thành công | Toast `bg #D1FAE5 text #10B981` "Đã gửi trả lời thành công!" · status badge đổi thành "ĐÃ TRẢ LỜI" · Section 2 ẩn · Section 3 hiện |
| Thất bại | Toast `bg #FEE2E2 text #EF4444` "Có lỗi xảy ra." |

---

## 6. API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load chi tiết | GET | `/admin/contacts/{id}` | Khi mount (tự động đổi status new → read) |
| Gửi trả lời | POST | `/admin/contacts/{id}/reply` | Submit form trả lời |
| Xóa liên hệ | DELETE | `/admin/contacts/{id}` | Confirm dialog |

**Body POST /admin/contacts/{id}/reply:**
```json
{
  "reply": "*"
}
```
