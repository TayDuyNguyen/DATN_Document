# Màn hình: Thêm Lịch khởi hành

> Route: `/admin/tours/{id}/schedules/create`
> Quyền: 🛡️ Admin / Staff
> Mô tả: Form thêm lịch khởi hành mới cho một tour cụ thể. Hỗ trợ đặt giá riêng ghi đè giá tour.

---

## Layout tổng thể

```
┌─────────────────────────────────────────────────────────────┐
│  HEADER: Breadcrumb + Tiêu đề + Tour info box + [Hủy][Thêm]│
├─────────────────────────────────────────────────────────────┤
│  FORM CARD (max-width 680px, centered):                     │
│  - Section header + badge "MỚI"                             │
│  - Ngày KH · Ngày KT · Số người · Trạng thái               │
│  - Divider "GIÁ RIÊNG (tuỳ chọn)"                          │
│  - Giá NL · Giá TE · Giá EB                                 │
│  - Preview / Summary box (live update)                      │
│  - Footer: [Hủy] [Thêm lịch]                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 1. Page Header

`flex justify-between items-start, mb 24px`

### Bên trái

| Element | Style |
|---------|-------|
| Breadcrumb | `12px Inter 500 #94A3B8` — "Quản lý Tour / Bà Nà Hills - Cầu Vàng / Thêm lịch khởi hành" |
| Title | `24px Inter 700 #1E293B` — "Thêm lịch khởi hành" |

**Tour info box** (`mt-8 inline-flex`):
- `bg #EFF6FF border #B3D9FF radius-10 px-14 py-10 flex items-center gap-10`
- Thumbnail: `32x32px radius-6 object-cover border #E2E8F0`
- Text: `"Tour: Bà Nà Hills - Cầu Vàng" 13px Inter 600 #0066CC`
- Badge: `"Tham quan" 11px bg white border #B3D9FF text #0066CC radius-full px-8 py-2`

### Bên phải (`flex gap-3`)

| Button | Style | Action |
|--------|-------|--------|
| Hủy | `border #E2E8F0 bg white text #64748B radius-10 px-20 py-10` hover `border #EF4444 text #EF4444` | Navigate `/admin/tours/{id}` |
| Thêm lịch | `bg #0066CC text white radius-10 px-20 py-10 shadow 14px 600` hover `bg #004999` | Submit `POST /admin/tours/{id}/schedules` |

---

## 2. Form Card

`bg white border #E2E8F0 radius-16 p-32 max-w-680px mx-auto`

### 2.1 Section Header

`flex items-center gap-10 mb-24 pb-16 border-b #F1F5F9`

- Icon: `calendar_month` · container `32x32px bg #EFF6FF radius-8 color #0066CC`
- Title: `"Thông tin lịch khởi hành" 15px Inter 600 #1E293B`
- Badge "MỚI": `bg #D1FAE5 text #10B981 11px radius-full px-8 py-2`

### 2.2 Form Fields

`grid grid-cols-2 gap-20`

| Field | Type | Bắt buộc | Col | Config |
|-------|------|----------|-----|--------|
| Ngày khởi hành | date | ✅ | 1 | icon `calendar_today` trái `#94A3B8` · validation: không chọn ngày quá khứ |
| Ngày kết thúc | date | ✅ | 1 | icon `calendar_today` trái · validation: >= ngày KH · helper "Thường trùng ngày KH với tour 1 ngày" |
| Số người tối đa | number | ✅ | 1 | min 1 · placeholder "20" · icon `group` trái · helper "Tối đa người có thể đặt cho lịch này" |
| Trạng thái | select | — | 1 | default "Còn chỗ" · mỗi option có colored dot |

**Trạng thái options:**
| Option | Dot color |
|--------|-----------|
| Còn chỗ (available) | `#10B981` |
| Đầy chỗ (full) | `#EF4444` |
| Đã hủy (cancelled) | `#94A3B8` |

**Divider** (`col-span-2`):
- `1px solid #F1F5F9` · label `"GIÁ RIÊNG (tuỳ chọn)" 11px uppercase #94A3B8 bg white px-12 absolute center`

| Field | Type | Col | Config |
|-------|------|-----|--------|
| Giá người lớn | number | 1 | suffix "đ" · placeholder "Để trống = dùng giá tour" · helper "Ghi đè giá tour cho lịch này" · khi nhập: badge "GIÁ RIÊNG" `bg #FFE0D4 text #FF6B35` |
| Giá trẻ em | number | 1 | suffix "đ" · placeholder "Để trống = dùng giá tour" |
| Giá em bé | number | 1 | suffix "đ" · placeholder "Để trống = dùng giá tour" |

### 2.3 Preview / Summary Box

`mt-24 bg #F8FAFC border #E2E8F0 radius-12 p-20`

- Label: `"XEM TRƯỚC" 10px uppercase #94A3B8 mb-12`
- Grid 2 cột, gap 16px · mỗi item: `flex items-center gap-8`
  - Icon `18px color #0066CC` + Label `12px #94A3B8` + Value `13px Inter 600 #1E293B` (live update)

| Icon | Label | Value mặc định |
|------|-------|----------------|
| `event` | Ngày KH | "—" → "15/04/2026 (Thứ Tư)" |
| `event` | Ngày KT | "—" → "15/04/2026" |
| `group` | Tối đa | "—" → "20 người" |
| `payments` | Giá NL | "Theo tour" → "900.000 đ" |
| `child_care` | Giá TE | "Theo tour" → "500.000 đ" |
| `circle` | Trạng thái | Badge colored live |

---

## 3. Form Footer

`flex justify-end gap-12 mt-24 pt-16 border-t #F1F5F9`

| Button | Style | Action |
|--------|-------|--------|
| Hủy | `border #E2E8F0 bg white text #64748B radius-10 px-20 py-10` hover `border #EF4444 text #EF4444` | Navigate `/admin/tours/{id}` |
| Thêm lịch | `bg #0066CC text white radius-10 px-20 py-10 14px 600 shadow` hover `bg #004999` | Submit form |

---

## 4. Validation & States

| Tình huống | Xử lý |
|-----------|-------|
| Field bắt buộc trống | Border `#EF4444` · bg `rgba(239,68,68,0.04)` · error text `12px #EF4444` · scroll to first error |
| Ngày KH < hôm nay | Error "Ngày khởi hành phải từ hôm nay trở đi" |
| Ngày KT < Ngày KH | Error "Ngày kết thúc phải sau ngày khởi hành" |
| Đang submit | Button disabled · spinner · "Đang thêm..." · `bg #3385D6 cursor-not-allowed` |
| Thành công | Toast `bg #D1FAE5 text #10B981` "Thêm lịch thành công!" · redirect `/admin/tours/{id}` |
| Thất bại | Toast `bg #FEE2E2 text #EF4444` "Có lỗi xảy ra. Vui lòng thử lại." |

---

## 5. API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Tạo lịch mới | POST | `/admin/tours/{id}/schedules` | Submit form |

**Body:**
```json
{
  "start_date": "*",
  "end_date": "*",
  "max_people": "*",
  "status": "available",
  "price_adult": "",
  "price_child": "",
  "price_infant": ""
}
```
