# Màn hình: Chỉnh sửa Lịch khởi hành

> Route: `/admin/tour-schedules/{id}/edit`
> Quyền: 🛡️ Admin / Staff
> Mô tả: Form chỉnh sửa lịch khởi hành đã tồn tại. Tái sử dụng layout từ màn Thêm lịch, bổ sung thống kê đặt chỗ, thông tin và nút xóa lịch.

---

## Tái sử dụng từ màn Thêm lịch

> Xem chi tiết tại `admin_tour_schedules_create.md`

Giữ nguyên:
- Layout single column centered `max-w-680px`
- Form card: `bg white border #E2E8F0 radius-16 p-32`
- Tất cả fields: Ngày KH · Ngày KT · Số người · Trạng thái
- Divider "GIÁ RIÊNG" + fields: Giá NL · Giá TE · Giá EB
- Preview / Summary box live update

---

## Điểm khác biệt

---

### 1. Page Header

| Element | Thêm lịch | Chỉnh sửa lịch |
|---------|-----------|----------------|
| Breadcrumb | ".../ Thêm lịch khởi hành" | ".../ Lịch khởi hành / 15/04/2026 - Bà Nà Hills / Chỉnh sửa" |
| Title | "Thêm lịch khởi hành" | "Chỉnh sửa lịch khởi hành" |
| Info box | Tour info (xanh) | Schedule info (vàng) |
| Button Hủy | → `/admin/tours/{id}` | → `/admin/tour-schedules` |
| Button chính | "Thêm lịch" | "Lưu thay đổi" → `PUT /admin/tour-schedules/{id}` |

**Schedule info box** (thay Tour info box, `mt-8 inline-flex`):
- `bg #FEF3C7 border rgba(245,158,11,0.3) radius-10 px-14 py-10 flex items-center gap-10`
- Icon `calendar_month 18px color #F59E0B`
- Text: `"Lịch: 15/04/2026 · Bà Nà Hills - Cầu Vàng" 13px Inter 600 #92400E`
- Badge trạng thái hiện tại: e.g. `"CÒN CHỖ" bg #D1FAE5 text #10B981 11px 700 radius-full px-8 py-2`

---

### 2. Loading State

Khi fetch `GET /admin/tour-schedules/{id}` chưa xong:
- Skeleton loading toàn bộ form fields: `h-10 bg #E2E8F0 radius-10 animation pulse`
- Spinner nhỏ + `"Đang tải dữ liệu..." 13px #94A3B8`

---

### 3. Form Pre-filled

- Tất cả fields điền sẵn từ response
- Nếu ngày KH đã qua → warning box bên dưới field Ngày KH:
  - `bg #FEF3C7 border rgba(245,158,11,0.3) radius-8 p-12`
  - icon `warning_amber #F59E0B` + text `13px #92400E`:
    "Lịch này đã khởi hành. Chỉnh sửa có thể ảnh hưởng đến đơn đặt hiện có."

---

### 4. Section Header Badge

Đổi `"MỚI"` → `"ĐANG SỬA"`: `bg #EFF6FF text #0066CC`

---

### 5. Thêm: Block Thống kê lịch (sau Preview box)

`mt-16 bg white border #E2E8F0 radius-12 p-20`

- Label: `"THỐNG KÊ" 10px uppercase #94A3B8 mb-12`
- Grid 3 cột, gap 12px:
  - Mỗi stat: `bg #F8FAFC border #E2E8F0 radius-10 p-12 text-center`
    - Value: `18px Inter 700 #1E293B`
    - Label: `11px uppercase #94A3B8`

| Value | Label |
|-------|-------|
| "12" | "ĐÃ ĐẶT" |
| "8" | "CÒN TRỐNG" |
| "20" | "TỐI ĐA" |

**Progress bar** (`mt-12 flex items-center gap-8`):
- Label: `"12/20 chỗ đã đặt" 13px #64748B`
- Bar: `flex-1 h-8px bg #E2E8F0 radius-full` · fill dynamic width

| Tỷ lệ | Fill color |
|-------|-----------|
| 0–60% | `#0066CC` |
| 61–89% | `#F59E0B` |
| 90–100% | `#EF4444` |

- Percent: `"60%" 13px Inter 600 #0066CC`

**Info box** (chỉ hiện nếu `booked > 0`, `mt-12`):
- `bg #DBEAFE border rgba(59,130,246,0.2) radius-8 p-12`
- icon `info #3B82F6` + text `13px #1E40AF`:
  "Có 12 đơn đặt cho lịch này. Thay đổi số người tối đa không được nhỏ hơn số đã đặt."

---

### 6. Thêm: Block Thông tin (sau Thống kê)

`mt-12 space-y-8`

| Label | Value | Style |
|-------|-------|-------|
| Ngày tạo | "15/03/2026 09:30" | `flex justify-between 13px #64748B` |
| Cập nhật lần cuối | "01/04/2026 14:22" | same |
| Thuộc tour | "Bà Nà Hills - Cầu Vàng" | link `#0066CC` hover underline → `/admin/tours/{id}` |

---

### 7. Form Footer — Khác

`flex justify-between items-center` (thay vì `justify-end`)

**Bên trái:**
- Button "Xóa lịch này": `border #FEE2E2 bg white text #EF4444 radius-10 px-16 py-10 13px 600` icon `delete` · hover `bg #FEE2E2`
  → confirm delete dialog

**Bên phải** (`flex gap-3`):
- "Hủy": `border #E2E8F0 bg white text #64748B radius-10 px-20 py-10`
- "Lưu thay đổi": `bg #0066CC text white radius-10 px-20 py-10 14px 600`

---

### 8. Confirm Delete Dialog

**Modal:** `bg white radius-16 w-400px shadow-modal backdrop rgba(0,0,0,0.4)`

| Vùng | Nội dung |
|------|---------|
| Header | Icon `warning_amber 40x40 bg #FEE2E2 radius-10 color #EF4444` + "Xóa lịch khởi hành này?" `16px 700 #1E293B` |
| Body | "Lịch ngày 15/04/2026 của tour Bà Nà Hills sẽ bị xóa vĩnh viễn." `14px #64748B` |
| Warning (nếu booked > 0) | `bg #FEF3C7 border warning radius-8 p-12 13px #92400E`: "⚠ Có 12 đơn đặt cho lịch này. Hãy hủy tất cả đơn đặt trước khi xóa lịch." |
| Footer | "Hủy" (ghost) + "Xóa lịch" `bg #EF4444 hover #DC2626` |

---

### 9. Unsaved Changes Guard

Khi navigate away khi có thay đổi chưa lưu:

| Button | Style | Action |
|--------|-------|--------|
| Tiếp tục chỉnh sửa | `bg #0066CC text white radius-10` | Đóng dialog |
| Bỏ thay đổi | `border #E2E8F0 text #64748B` hover `text #EF4444` | Navigate away |

---

### 10. Submit States

| Tình huống | Xử lý |
|-----------|-------|
| Đang lưu | Button disabled · spinner · "Đang lưu..." · `bg #3385D6 cursor-not-allowed` |
| Lưu thành công | Toast `bg #D1FAE5 text #10B981` "Cập nhật lịch thành công!" · ở lại trang edit |
| Lưu thất bại | Toast `bg #FEE2E2 text #EF4444` "Có lỗi xảy ra. Vui lòng thử lại." |
| Xóa thành công | Toast `bg #D1FAE5 text #10B981` "Đã xóa lịch." · redirect `/admin/tour-schedules` |

---

## API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load dữ liệu | GET | `/admin/tour-schedules/{id}` | Khi mount |
| Lưu thay đổi | PUT | `/admin/tour-schedules/{id}` | Submit form |
| Xóa lịch | DELETE | `/admin/tour-schedules/{id}` | Confirm dialog |

**Body PUT** (all optional):
```json
{
  "start_date": "",
  "end_date": "",
  "max_people": "",
  "status": "",
  "price_adult": "",
  "price_child": "",
  "price_infant": ""
}
```
