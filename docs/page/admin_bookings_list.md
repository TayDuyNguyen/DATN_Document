# Màn hình: Danh sách Đơn hàng

> Route: `/admin/bookings`
> Quyền: 🛡️ Admin / Staff
> Mô tả: Quản lý toàn bộ đơn đặt tour — filter theo trạng thái/thanh toán/ngày, xác nhận, hủy đơn, xuất Excel.

---

## Layout tổng thể

```
┌─────────────────────────────────────────────────────────────────┐
│  HEADER: Breadcrumb + Tiêu đề + [Xuất Excel]                    │
├─────────────────────────────────────────────────────────────────┤
│  STATS ROW: [Tổng đơn] [Chờ XN] [Đã XN] [Đã hủy]              │
├─────────────────────────────────────────────────────────────────┤
│  FILTER BAR: Search + TT đơn + TT thanh toán + Date range       │
│              Active filter tags                                 │
├─────────────────────────────────────────────────────────────────┤
│  TABLE TOOLBAR: Checkbox + Bulk actions + Per page              │
│  TABLE HEADER: ☐ | Mã đơn | Khách hàng | Tour | Ngày đặt |     │
│                Lịch KH | Tổng tiền | TT đơn | TT TT | ⚙        │
│  TABLE BODY: rows                                               │
│  PAGINATION                                                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1. Page Header

`flex justify-between items-start, mb 24px`

| Element | Style |
|---------|-------|
| Breadcrumb | `12px Inter 500 #94A3B8` — "Đơn hàng & Thanh toán / Danh sách Đơn hàng" |
| Title | `24px Inter 700 #1E293B` — "Danh sách Đơn hàng" |
| Subtitle | `14px Inter 400 #64748B` — "Quản lý toàn bộ đơn đặt tour của khách hàng" |
| Button "Xuất Excel" | `border #E2E8F0 bg white text #64748B radius-10 px-16 py-10` icon `download` hover `border #0066CC text #0066CC` | `GET /admin/bookings/export` |

---

## 2. Stats Row

`grid grid-cols-4 gap-4 mb-24`
Mỗi thẻ: `bg white border #E2E8F0 radius-12 p-16 flex items-center gap-12`

| Thẻ | Icon | Icon bg | Value | Label | Value color |
|-----|------|---------|-------|-------|-------------|
| Tổng đơn hàng | `shopping_cart` | `#EFF6FF` | `1.248` | "TỔNG ĐƠN HÀNG" | `#1E293B` |
| Chờ xác nhận | `pending` | `#FEF3C7` | `48` | "CHỜ XÁC NHẬN" | `#F59E0B` |
| Đã xác nhận | `check_circle` | `#D1FAE5` | `856` | "ĐÃ XÁC NHẬN" | `#10B981` |
| Đã hủy | `cancel` | `#FEE2E2` | `124` | "ĐÃ HỦY" | `#EF4444` |

---

## 3. Filter Bar

**Card:** `bg white border #E2E8F0 radius-16 p-20 mb-24`

### Row 1 (`flex gap-3 flex-wrap`)

| Element | Width | Config |
|---------|-------|--------|
| Search | `flex-1 min-280px` | Placeholder "Tìm theo mã đơn, tên khách hàng, email..." · debounce 300ms |
| Select TT đơn | `170px` | Tất cả / Chờ xác nhận (pending) / Đã xác nhận (confirmed) / Hoàn tất (completed) / Đã hủy (cancelled) |
| Select TT thanh toán | `170px` | Tất cả / Chờ thanh toán / Đã thanh toán / Hoàn tiền |
| Date "Từ ngày" | `150px` | Input date · icon `calendar_today` |
| Date "Đến ngày" | `150px` | Input date |
| Button Lọc | `auto` | `bg #0066CC text white radius-10 px-20 py-10` |
| Button Đặt lại | `auto` | Chỉ hiện khi có filter · hover `text #EF4444 border #EF4444` |

### Row 2 — Active filter tags
- Tag: `bg #EFF6FF text #0066CC border #B3D9FF radius-full px-10 py-4 12px Inter 500`
- Nút `×` xóa từng filter

---

## 4. Table

**Card:** `bg white border #E2E8F0 radius-16 overflow-hidden`

### 4.1 Toolbar

`flex justify-between items-center px-24 py-16 border-b #E2E8F0`

**Bên trái:**
- Checkbox "Chọn tất cả"
- Khi có row được chọn: `"Đã chọn 3" 13px 600 #0066CC` + bulk actions:
  - "Xác nhận": `bg #D1FAE5 text #10B981 radius-8 px-12 py-6 12px 600`
  - "Hủy đơn": `bg #FEE2E2 text #EF4444`

**Bên phải:**
- `"Hiển thị 1–10 / 1.248 đơn" 13px #94A3B8`
- Select per_page: 10 / 20 / 50

### 4.2 Table Header

`bg #F8FAFC border-b #E2E8F0`
`th: px-16 py-12, 11px Inter 600, uppercase, letter-spacing 0.06em, #94A3B8`

| Cột | Width | Ghi chú |
|-----|-------|---------|
| ☐ | 40px | Checkbox |
| Mã đơn | 120px | Sortable ↕ |
| Khách hàng | 200px | Avatar + tên + email |
| Tour | auto | Thumbnail + tên + danh mục |
| Ngày đặt | 140px | Sortable ↕ |
| Lịch KH | 120px | Ngày khởi hành |
| Tổng tiền | 130px | Sortable ↕ |
| TT đơn | 130px | Badge trạng thái đơn |
| TT thanh toán | 130px | Badge trạng thái TT |
| Thao tác | 100px | |

### 4.3 Table Body

`border-b #F1F5F9 min-h-64px`
- Hover: `bg #F8FAFC transition-150ms`
- Selected: `bg #EFF6FF border-l-3 #0066CC`

#### Chi tiết từng cột

**Col Mã đơn:**
- `"#BK-1008" 13px Inter 700 #0066CC` · hover underline · cursor pointer
- → Navigate `/admin/bookings/{id}`

**Col Khách hàng** (`flex items-center gap-10`):
- Avatar: `32x32px rounded-full border-2 #E2E8F0 object-cover`
- Name: `13px Inter 600 #1E293B`
- Email: `11px #94A3B8 max-1-line ellipsis`

**Col Tour** (`flex items-center gap-10`):
- Thumbnail: `40x40px radius-8 object-cover border #E2E8F0`
- Tên: `13px Inter 500 #1E293B max-1-line ellipsis`
- Danh mục: `11px #94A3B8`

**Col Ngày đặt:**
- Date: `13px Inter 600 #1E293B` — e.g. "06/04/2026"
- Time: `11px #94A3B8` — e.g. "14:30"

**Col Lịch KH:**
- Date: `13px Inter 500 #1E293B` — e.g. "15/04/2026"
- Ngày đã qua: text `#94A3B8` (muted)
- Trong 7 ngày tới: badge "SẮP TỚI" `bg #EFF6FF text #0066CC 10px 600 radius-full px-6 py-1`

**Col Tổng tiền:**
- `13px Inter 700 #1E293B` — e.g. "2.450.000 đ"

**Col TT đơn** — badge pill `11px 700 rounded-full px-10 py-4`:

| Status | Background | Text |
|--------|-----------|------|
| pending | `#FEF3C7` | `#F59E0B` "CHỜ XÁC NHẬN" |
| confirmed | `#DBEAFE` | `#3B82F6` "ĐÃ XÁC NHẬN" |
| completed | `#D1FAE5` | `#10B981` "HOÀN TẤT" |
| cancelled | `#FEE2E2` | `#EF4444` "ĐÃ HỦY" |

**Col TT thanh toán** — badge pill:

| Status | Background | Text |
|--------|-----------|------|
| pending | `#FEF3C7` | `#F59E0B` "CHỜ THANH TOÁN" |
| paid | `#D1FAE5` | `#10B981` "ĐÃ THANH TOÁN" |
| refunded | `#EEF2FF` | `#6366F1` "HOÀN TIỀN" |

**Col Thao tác** (`flex gap-4`):

| Button | Icon | Điều kiện hiện | Hover | Action |
|--------|------|----------------|-------|--------|
| Xem | `visibility` | Luôn hiện | `#0066CC` | `/admin/bookings/{id}` |
| Xác nhận | `check_circle` | status=pending | `#10B981` | `POST /admin/bookings/{id}/confirm` |
| Hủy | `cancel` | status=pending/confirmed | `#EF4444` | Confirm dialog → `POST /admin/bookings/{id}/cancel` |

Style chung: `28x28px bg #F8FAFC border #E2E8F0 radius-6 color #64748B`

### 4.4 Sample Data

| Mã đơn | Khách hàng | Tour | Ngày đặt | Lịch KH | Tổng tiền | TT đơn | TT TT |
|--------|-----------|------|----------|---------|-----------|--------|-------|
| #BK-1008 | Nguyễn Văn An | Bà Nà Hills | 06/04 14:30 | 15/04 | 2.450.000đ | HOÀN TẤT | ĐÃ THANH TOÁN |
| #BK-1007 | Trần Thị Bích | Ngũ Hành Sơn | 06/04 11:15 | 18/04 | 1.200.000đ | CHỜ XÁC NHẬN | CHỜ THANH TOÁN |
| #BK-1006 | Lê Minh Tuấn | Cù Lao Chàm | 05/04 09:00 | 20/04 | 3.600.000đ | ĐÃ XÁC NHẬN | ĐÃ THANH TOÁN |
| #BK-1005 | Phạm Thu Hà | Hội An Show | 05/04 16:45 | 12/04 SẮP TỚI | 980.000đ | ĐÃ XÁC NHẬN | ĐÃ THANH TOÁN |
| #BK-1004 | Hoàng Văn Đức | Sơn Trà | 04/04 10:20 | 08/04 | 750.000đ | ĐÃ HỦY | HOÀN TIỀN |

---

## 5. Pagination

`flex justify-between items-center px-24 py-16 border-t #E2E8F0 bg #F8FAFC radius-b-16`

- Trái: `"Hiển thị 1–10 trong tổng số 1.248 đơn hàng" 13px #64748B`
- Phải: Prev · 1 · 2 · ... · 125 · Next
  - Button: `32x32px border #E2E8F0 radius-8 bg white color #64748B`
  - Active: `bg #0066CC text white border #0066CC`

---

## 6. Confirm Hủy Đơn Dialog

**Modal:** `bg white radius-16 w-440px shadow-modal backdrop rgba(0,0,0,0.4)`

| Vùng | Nội dung |
|------|---------|
| Header | Icon `warning_amber 40x40 bg #FEE2E2 radius-10 color #EF4444` + "Hủy đơn hàng này?" `16px 700 #1E293B` |
| Body | "Đơn #BK-1008 của [Tên khách] sẽ bị hủy." `14px #64748B` + Textarea "Lý do hủy" (optional) `rows-3 border #E2E8F0 radius-10` + Warning `bg #FEF3C7 13px #92400E`: "⚠ Khách hàng sẽ nhận được thông báo hủy đơn qua email." |
| Footer | "Đóng" (ghost) + "Xác nhận hủy" `bg #EF4444 hover #DC2626` |

---

## 7. Empty State

`center py-64`:
- SVG icon `shopping_cart 80x80px color #E2E8F0`
- Title: `"Không tìm thấy đơn hàng nào" 16px Inter 600 #1E293B`
- Subtitle: `"Thử thay đổi bộ lọc hoặc khoảng thời gian" 14px #94A3B8`

---

## 8. API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load danh sách | GET | `/admin/bookings?page=&per_page=&sort=&order=` | Khi mount, đổi filter, đổi trang |
| Tìm kiếm | GET | `/admin/bookings?search=` | Nhập search (debounce 300ms) |
| Filter TT đơn | GET | `/admin/bookings?status=` | Chọn select |
| Filter TT thanh toán | GET | `/admin/bookings?payment_status=` | Chọn select |
| Filter ngày | GET | `/admin/bookings?date_from=&date_to=` | Chọn date range |
| Xác nhận đơn | POST | `/admin/bookings/{id}/confirm` | Click button xác nhận |
| Hủy đơn | POST | `/admin/bookings/{id}/cancel` | Confirm dialog |
| Bulk xác nhận | POST | `/admin/bookings/{id}/confirm` (loop) | Bulk action |
| Bulk hủy | POST | `/admin/bookings/{id}/cancel` (loop) | Bulk action |
| Xuất Excel | GET | `/admin/bookings/export?status=&payment_status=&date_from=&date_to=` | Click "Xuất Excel" |
