# Màn hình: Danh sách Liên hệ

> Route: `/admin/contacts`
> Quyền: 🛡️ Admin / Staff
> Mô tả: Quản lý form liên hệ từ khách hàng — filter theo trạng thái, xem chi tiết, xóa, xuất Excel.

---

## Layout tổng thể

```
┌─────────────────────────────────────────────────────────────────┐
│  HEADER: Breadcrumb + Tiêu đề + [Xuất Excel]                    │
├─────────────────────────────────────────────────────────────────┤
│  STATS ROW: [Tổng LH] [Mới] [Đã đọc] [Đã trả lời]             │
├─────────────────────────────────────────────────────────────────┤
│  FILTER BAR: Search + Trạng thái + Lọc                          │
├─────────────────────────────────────────────────────────────────┤
│  TABLE TOOLBAR: Checkbox + Bulk delete + Per page               │
│  TABLE: Người gửi | Chủ đề | Trạng thái | Ngày gửi | Thao tác  │
│  PAGINATION                                                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1. Page Header

| Element | Style |
|---------|-------|
| Breadcrumb | `12px Inter 500 #94A3B8` — "Liên hệ / Danh sách Liên hệ" |
| Title | `24px Inter 700 #1E293B` — "Danh sách Liên hệ" |
| Subtitle | `14px Inter 400 #64748B` — "Quản lý yêu cầu liên hệ từ khách hàng" |
| Button "Xuất Excel" | `border #E2E8F0 bg white text #64748B radius-10 px-16 py-10` icon `download` hover `border #0066CC text #0066CC` | `GET /admin/contacts/export` |

---

## 2. Stats Row

`grid grid-cols-4 gap-4 mb-24`

| Thẻ | Icon | Icon bg | Value | Label | Value color |
|-----|------|---------|-------|-------|-------------|
| Tổng liên hệ | `mail` | `#EFF6FF` | `248` | "TỔNG LIÊN HỆ" | `#1E293B` |
| Mới | `mark_email_unread` | `#FEE2E2` | `12` | "MỚI" | `#EF4444` |
| Đã đọc | `drafts` | `#FEF3C7` | `186` | "ĐÃ ĐỌC" | `#F59E0B` |
| Đã trả lời | `mark_email_read` | `#D1FAE5` | `50` | "ĐÃ TRẢ LỜI" | `#10B981` |

> Thẻ "Mới" có pulse animation — urgent indicator

---

## 3. Filter Bar

**Card:** `bg white border #E2E8F0 radius-16 p-20 mb-24`

### Row 1 (`flex gap-3 flex-wrap`)

| Element | Width | Config |
|---------|-------|--------|
| Search | `flex-1 min-280px` | Placeholder "Tìm theo tên, email, chủ đề..." · debounce 300ms |
| Select Trạng thái | `180px` | Tất cả / Mới (new) / Đã đọc (read) / Đã trả lời (replied) |
| Button Lọc | `auto` | `bg #0066CC text white radius-10 px-20 py-10` |
| Button Đặt lại | `auto` | Chỉ hiện khi có filter |

### Row 2 — Active filter tags
- Tag: `bg #EFF6FF text #0066CC border #B3D9FF radius-full px-10 py-4 12px Inter 500`

---

## 4. Table

**Card:** `bg white border #E2E8F0 radius-16 overflow-hidden`

### 4.1 Toolbar

`flex justify-between items-center px-24 py-16 border-b #E2E8F0`

**Bên trái:**
- Checkbox "Chọn tất cả"
- Khi có row được chọn: `"Đã chọn 3" 13px 600 #0066CC` + bulk action:
  - "Xóa tất cả": `bg #FEE2E2 text #EF4444 radius-8 px-12 py-6 12px 600`

**Bên phải:**
- `"Hiển thị 1–10 / 248 liên hệ" 13px #94A3B8`
- Select per_page: 10 / 20 / 50

### 4.2 Table Header

`bg #F8FAFC border-b #E2E8F0`
`th: px-16 py-12, 11px Inter 600, uppercase, letter-spacing 0.06em, #94A3B8`

| Cột | Width | Ghi chú |
|-----|-------|---------|
| ☐ | 40px | Checkbox |
| Người gửi | 220px | Tên + email + phone |
| Chủ đề & Tin nhắn | auto | Subject + preview message |
| Trạng thái | 120px | Badge |
| Ngày gửi | 140px | Sortable ↕ |
| Thao tác | 100px | Xem + Xóa |

### 4.3 Table Body

`border-b #F1F5F9 min-h-64px`
- Hover: `bg #F8FAFC transition-150ms`
- Selected: `bg #EFF6FF border-l-3 #0066CC`
- Row status=new: `bg #FFF5F5 border-l-3 #EF4444` (urgent highlight)

**Col Người gửi** (`flex flex-col gap-2`):
- Name: `14px Inter 600 #1E293B`
- Email: `12px #94A3B8` (link `mailto:` hover `#0066CC`)
- Phone: `12px #94A3B8` (nếu có)

**Col Chủ đề & Tin nhắn** (`flex flex-col gap-2`):
- Subject: `13px Inter 600 #1E293B max-1-line ellipsis`
- Message preview: `12px #94A3B8 max-1-line ellipsis`

**Col Trạng thái** — badge pill `11px 700 rounded-full px-10 py-4`:

| Status | Background | Text |
|--------|-----------|------|
| new | `#FEE2E2` | `#EF4444` "MỚI" |
| read | `#FEF3C7` | `#F59E0B` "ĐÃ ĐỌC" |
| replied | `#D1FAE5` | `#10B981` "ĐÃ TRẢ LỜI" |

**Col Ngày gửi:**
- Date: `13px #1E293B` — e.g. "06/04/2026"
- Time: `11px #94A3B8` — e.g. "14:30"
- Relative: `"2 giờ trước" 11px #94A3B8`

**Col Thao tác** (`flex gap-4`):
- Xem & Trả lời: `28x28px bg #F8FAFC border #E2E8F0 radius-6 icon mail color #64748B`
  hover `border #0066CC color #0066CC`
  → Navigate `/admin/contacts/{id}`
- Xóa: icon `delete` hover `border #EF4444 color #EF4444`
  → confirm → `DELETE /admin/contacts/{id}`

### 4.4 Sample Data

| Người gửi | Chủ đề | Status | Ngày gửi |
|-----------|--------|--------|---------|
| Nguyễn Văn An · nguyenvanan@gmail.com | Hỏi về tour Bà Nà Hills | MỚI | 06/04 14:30 |
| Trần Thị Bích · tranbich@gmail.com | Phản hồi về dịch vụ | ĐÃ ĐỌC | 06/04 11:15 |
| Lê Minh Tuấn · leminhtuan@gmail.com | Yêu cầu hủy tour | ĐÃ TRẢ LỜI | 05/04 09:00 |
| Phạm Thu Hà · phamthuha@gmail.com | Góp ý cải thiện | MỚI | 05/04 08:00 |
| Hoàng Văn Đức · hoangduc@gmail.com | Hỏi về giá tour | ĐÃ ĐỌC | 04/04 10:00 |

---

## 5. Pagination

`flex justify-between items-center px-24 py-16 border-t #E2E8F0 bg #F8FAFC radius-b-16`

- Trái: `"Hiển thị 1–10 trong tổng số 248 liên hệ" 13px #64748B`
- Phải: Prev · 1 · 2 · ... · 25 · Next

---

## 6. Confirm Delete Dialog

**Modal:** `bg white radius-16 w-400px shadow-modal backdrop rgba(0,0,0,0.4)`

| Vùng | Nội dung |
|------|---------|
| Header | Icon `delete 40x40 bg #FEE2E2 radius-10 color #EF4444` + "Xóa liên hệ này?" `16px 700 #1E293B` |
| Body | "Liên hệ từ [Tên] sẽ bị xóa vĩnh viễn." `14px #64748B` |
| Footer | "Hủy" (ghost) + "Xóa" `bg #EF4444 hover #DC2626` |

---

## 7. Empty State

`center py-64`:
- SVG icon `mail_off 80x80px color #E2E8F0`
- Title: `"Không có liên hệ nào" 16px Inter 600 #1E293B`
- Subtitle: `"Thử thay đổi bộ lọc" 14px #94A3B8`

---

## 8. API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load danh sách | GET | `/admin/contacts?page=&per_page=` | Khi mount, đổi filter |
| Tìm kiếm | GET | `/admin/contacts?search=` | Nhập search (debounce 300ms) |
| Filter trạng thái | GET | `/admin/contacts?status=` | Chọn select |
| Xóa 1 liên hệ | DELETE | `/admin/contacts/{id}` | Confirm dialog |
| Bulk xóa | DELETE | `/admin/contacts/{id}` (loop) | Bulk action |
| Xuất Excel | GET | `/admin/contacts/export?status=` | Click "Xuất Excel" |
