# Màn hình: Danh sách Giao dịch

> Route: `/admin/payments`
> Quyền: 🛡️ Admin / Staff
> Mô tả: Quản lý toàn bộ giao dịch thanh toán — filter theo trạng thái/cổng TT/ngày, xem chi tiết, hoàn tiền, xuất Excel.

---

## Tái sử dụng từ màn Danh sách Đơn hàng

> Xem pattern tại `admin_bookings_list.md`

Giữ nguyên: layout header + stats + filter + table + pagination, design system, màu sắc, spacing.

---

## Điểm khác biệt

---

### 1. Page Header

| Element | Đơn hàng | Giao dịch |
|---------|----------|-----------|
| Breadcrumb | ".../ Danh sách Đơn hàng" | ".../ Danh sách Giao dịch" |
| Title | "Danh sách Đơn hàng" | "Danh sách Giao dịch" |
| Subtitle | "...đơn đặt tour..." | "Quản lý toàn bộ giao dịch thanh toán của hệ thống" |
| Button thêm | Không có | Không có (giao dịch do hệ thống tạo) |

---

### 2. Stats Row

`grid grid-cols-4 gap-4 mb-24`

| Thẻ | Icon | Icon bg | Value | Label | Value color |
|-----|------|---------|-------|-------|-------------|
| Tổng giao dịch | `payments` | `#EFF6FF` | `1.248` | "TỔNG GIAO DỊCH" | `#1E293B` |
| Đã thanh toán | `check_circle` | `#D1FAE5` | `1.024` | "ĐÃ THANH TOÁN" | `#10B981` |
| Chờ thanh toán | `pending` | `#FEF3C7` | `186` | "CHỜ THANH TOÁN" | `#F59E0B` |
| Đã hoàn tiền | `currency_exchange` | `#EEF2FF` | `38` | "ĐÃ HOÀN TIỀN" | `#6366F1` |

---

### 3. Filter Bar

| Element | Width | Config |
|---------|-------|--------|
| Search | `flex-1 min-280px` | Placeholder "Tìm theo mã giao dịch, mã đơn hàng..." |
| Select Trạng thái | `170px` | Tất cả / Đã thanh toán (paid) / Chờ TT (pending) / Hoàn tiền (refunded) / Thất bại (failed) |
| Select Cổng TT | `150px` | Tất cả / MoMo / VNPay / ZaloPay |
| Date Từ ngày | `150px` | Input date |
| Date Đến ngày | `150px` | Input date |
| Button Lọc | `auto` | `bg #0066CC` |
| Button Đặt lại | `auto` | Chỉ hiện khi có filter |

---

### 4. Table

#### 4.1 Toolbar

- Checkbox "Chọn tất cả" — **không có bulk action buttons**
- Khi có row được chọn: chỉ hiện `"Đã chọn X" 13px 600 #0066CC` (không có action)
- Bên phải: count + per_page select

#### 4.2 Table Columns

| Cột | Width | Ghi chú |
|-----|-------|---------|
| ☐ | 40px | Checkbox |
| Mã GD | 160px | Sortable ↕ |
| Mã đơn hàng | 120px | Link sang đơn hàng |
| Khách hàng | 180px | Avatar + tên + email |
| Cổng TT | 110px | Badge màu |
| Số tiền | 130px | Sortable ↕ |
| Ngày GD | 140px | Sortable ↕ |
| Trạng thái | 130px | Badge |
| Thao tác | 80px | Xem + Hoàn tiền |

#### 4.3 Chi tiết từng cột

**Col Mã GD:**
- `"TXN-20260406-001" 13px Inter 700 #1E293B`
- `"GD-001" 12px #94A3B8` bên dưới (transaction_code ngắn)

**Col Mã đơn hàng:**
- `"#BK-1008" 13px Inter 600 #0066CC` · hover underline · cursor pointer
- → Navigate `/admin/bookings/{booking_id}`

**Col Khách hàng** (`flex items-center gap-8`):
- Avatar: `28x28px rounded-full border #E2E8F0`
- Name: `13px Inter 500 #1E293B`
- Email: `11px #94A3B8`

**Col Cổng TT** — badge `11px Inter 700 rounded-full px-10 py-4`:

| Gateway | Background | Text | Border |
|---------|-----------|------|--------|
| MoMo | `#FFE0D4` | `#FF6B35` | `rgba(255,107,53,0.2)` |
| VNPay | `#EFF6FF` | `#0066CC` | `#B3D9FF` |
| ZaloPay | `#D1FAE5` | `#10B981` | `rgba(16,185,129,0.2)` |

**Col Số tiền:**
- `13px Inter 700 #1E293B` — e.g. "2.450.000 đ"

**Col Ngày GD:**
- Date: `13px Inter 600 #1E293B` — e.g. "06/04/2026"
- Time: `11px #94A3B8` — e.g. "14:35"

**Col Trạng thái** — badge pill `11px 700 rounded-full px-10 py-4`:

| Status | Background | Text |
|--------|-----------|------|
| paid | `#D1FAE5` | `#10B981` "ĐÃ THANH TOÁN" |
| pending | `#FEF3C7` | `#F59E0B` "CHỜ THANH TOÁN" |
| refunded | `#EEF2FF` | `#6366F1` "ĐÃ HOÀN TIỀN" |
| failed | `#FEE2E2` | `#EF4444` "THẤT BẠI" |

**Col Thao tác** (`flex gap-4`):

| Button | Icon | Điều kiện | Hover | Action |
|--------|------|-----------|-------|--------|
| Xem | `visibility` | Luôn hiện | `#0066CC` | `/admin/payments/{id}` |
| Hoàn tiền | `currency_exchange` | status=paid | `#6366F1` | Confirm dialog → `POST /admin/payments/{id}/refund` |

Style chung: `28x28px bg #F8FAFC border #E2E8F0 radius-6 color #64748B`

#### 4.4 Sample Data

| Mã GD | Mã đơn | Khách hàng | Cổng | Số tiền | Ngày GD | Status |
|-------|--------|-----------|------|---------|---------|--------|
| TXN-001 | #BK-1008 | Nguyễn Văn An | MoMo | 2.450.000đ | 06/04 14:35 | ĐÃ THANH TOÁN |
| TXN-002 | #BK-1007 | Trần Thị Bích | VNPay | 1.200.000đ | 06/04 11:20 | CHỜ THANH TOÁN |
| TXN-003 | #BK-1006 | Lê Minh Tuấn | ZaloPay | 3.600.000đ | 05/04 09:05 | ĐÃ THANH TOÁN |
| TXN-004 | #BK-1005 | Phạm Thu Hà | MoMo | 980.000đ | 05/04 16:50 | ĐÃ HOÀN TIỀN |
| TXN-005 | #BK-1004 | Hoàng Văn Đức | VNPay | 750.000đ | 04/04 10:25 | THẤT BẠI |

---

### 5. Confirm Hoàn tiền Dialog

**Modal:** `bg white radius-16 w-440px shadow-modal backdrop rgba(0,0,0,0.4)`

| Vùng | Nội dung |
|------|---------|
| Header | Icon `currency_exchange 40x40 bg #EEF2FF radius-10 color #6366F1` + "Hoàn tiền giao dịch này?" `16px 700 #1E293B` |
| Body | "Giao dịch [Mã GD] số tiền [Số tiền] sẽ được hoàn lại cho khách hàng." `14px #64748B` + Textarea "Lý do hoàn tiền" * `rows-3 border #E2E8F0 radius-10` + Warning `bg #FEF3C7 13px #92400E`: "⚠ Thao tác này không thể hoàn tác. Tiền sẽ được hoàn qua cổng thanh toán gốc." |
| Footer | "Đóng" (ghost) + "Xác nhận hoàn tiền" `bg #6366F1 hover #4F46E5` |

---

### 6. Empty State

`center py-64`:
- SVG icon `payments 80x80px color #E2E8F0`
- Title: `"Không tìm thấy giao dịch nào" 16px Inter 600 #1E293B`
- Subtitle: `"Thử thay đổi bộ lọc hoặc khoảng thời gian" 14px #94A3B8`

---

## API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load danh sách | GET | `/admin/payments?page=&per_page=&sort=&order=` | Khi mount, đổi filter, đổi trang |
| Tìm kiếm | GET | `/admin/payments?search=` | Nhập search (debounce 300ms) |
| Filter trạng thái | GET | `/admin/payments?payment_status=` | Chọn select |
| Filter cổng TT | GET | `/admin/payments?payment_gateway=` | Chọn select |
| Filter ngày | GET | `/admin/payments?date_from=&date_to=` | Chọn date range |
| Hoàn tiền | POST | `/admin/payments/{id}/refund` | Confirm dialog |
| Xuất Excel | GET | `/admin/payments/export?payment_status=&payment_gateway=&date_from=&date_to=` | Click "Xuất Excel" |
