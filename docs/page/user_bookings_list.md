# Màn hình: Lịch sử đặt tour

> Route: `/bookings`
> Quyền: 🔐 Cần đăng nhập
> Mô tả: Xem toàn bộ lịch sử đặt tour của người dùng với filter theo trạng thái.

---

## Tái sử dụng từ màn Hồ sơ cá nhân

> Xem chi tiết layout tại `user_profile.md`

Giữ nguyên: Header · Breadcrumb · Sidebar (item "Đơn đặt tour" active) · Footer

---

## Main Content

### 1. Page Header

`flex justify-between items-center mb-24`

- Title: `"Đơn đặt tour của tôi" 20px Inter 700 #1E293B`
- Count: `"12 đơn" 14px #94A3B8`

### 2. Filter Tabs

`flex gap-0 border-b #E2E8F0 mb-24`

| Tab | Label | Count |
|-----|-------|-------|
| Tất cả | "Tất cả" | (12) |
| Chờ xác nhận | "Chờ xác nhận" | (2) |
| Đã xác nhận | "Đã xác nhận" | (3) |
| Hoàn tất | "Hoàn tất" | (6) |
| Đã hủy | "Đã hủy" | (1) |

- Active: `border-b-2 border-#0066CC text #0066CC 14px 600`
- Inactive: `text #64748B 14px 500` hover `text #0066CC`
- Click → filter `status=`

### 3. Booking Card List

**API: `GET /user/bookings?status=&page=1&per_page=10`**

`flex flex-col gap-16`

Mỗi booking card:
`bg white border #E2E8F0 radius-16 overflow-hidden hover shadow-card`

**Card header** (`flex justify-between items-center px-20 py-14 bg #F8FAFC border-b #F1F5F9`):
- Left:
  - Mã đơn: `"#BK-1008" 13px Inter 700 #0066CC`
  - `·` separator
  - Ngày đặt: `"06/04/2026" 13px #94A3B8`
- Right: Badge trạng thái `11px 700 rounded-full px-10 py-4`

| Status | Background | Text |
|--------|-----------|------|
| pending | `#FEF3C7` | `#F59E0B` "CHỜ XÁC NHẬN" |
| confirmed | `#DBEAFE` | `#3B82F6` "ĐÃ XÁC NHẬN" |
| completed | `#D1FAE5` | `#10B981` "HOÀN TẤT" |
| cancelled | `#FEE2E2` | `#EF4444` "ĐÃ HỦY" |

**Card body** (`flex gap-16 p-20`):
- Thumbnail: `80x80px radius-12 object-cover flex-shrink-0`
- Right (`flex-1`):
  - Tên tour: `16px Inter 600 #1E293B`
  - `flex items-center gap-12 mt-6`:
    - icon `calendar_today 14px #94A3B8` + "Ngày KH: 15/04/2026" `13px #64748B`
    - icon `group 14px #94A3B8` + "2 NL · 1 TE" `13px #64748B`
  - `flex justify-between items-center mt-12`:
    - Tổng tiền: `"2.200.000 đ" 16px Inter 700 #FF6B35`
    - Badge TT thanh toán `11px 700 rounded-full px-8 py-3`:
      - paid: `bg #D1FAE5 text #10B981` "ĐÃ THANH TOÁN"
      - pending: `bg #FEF3C7 text #F59E0B` "CHỜ THANH TOÁN"
      - refunded: `bg #EEF2FF text #6366F1` "HOÀN TIỀN"

**Card footer** (`flex justify-between items-center px-20 py-12 border-t #F1F5F9`):
- Left: `"Đặt lúc 06/04/2026 14:30" 12px #94A3B8`
- Right (`flex gap-8`):
  - Button "Xem chi tiết": `border #E2E8F0 bg white text #0066CC radius-8 px-14 py-8 13px 600`
    → `/bookings/{id}`
  - Button "Hủy đơn" (chỉ hiện nếu status=pending/confirmed):
    `border #FEE2E2 bg white text #EF4444 radius-8 px-14 py-8 13px 600`
    hover `bg #FEE2E2`
    → confirm dialog → `POST /user/bookings/{id}/cancel`
  - Button "Đặt lại" (chỉ hiện nếu status=completed/cancelled):
    `bg #FF6B35 text white radius-8 px-14 py-8 13px 600`
    hover `bg #E55A2B`
    → `/tours/{slug}`
  - Button "Đánh giá" (chỉ hiện nếu status=completed + chưa đánh giá):
    `bg #0066CC text white radius-8 px-14 py-8 13px 600`
    → mở modal viết đánh giá

### 4. Pagination

`flex justify-center mt-24`
- Prev · 1 · 2 · Next

### 5. Empty State

`center py-64 text-center`

- SVG icon `shopping_cart 80px #E2E8F0`
- Title: `"Chưa có đơn đặt tour nào" 18px Inter 600 #1E293B mt-16`
- Subtitle: `"Hãy khám phá và đặt tour ngay!" 14px #94A3B8 mt-8`
- Button "Khám phá Tour": `bg #FF6B35 text white radius-10 px-24 py-12 14px 600 mt-16`
  → `/tours`

### 6. Confirm Hủy đơn Dialog

`Modal w-400px backdrop rgba(0,0,0,0.4)`

- Header: icon `warning_amber 40x40 bg #FEE2E2 radius-10 color #EF4444`
  + `"Hủy đơn hàng này?" 16px 700 #1E293B`
- Body:
  - `"Đơn #BK-1008 sẽ bị hủy." 14px #64748B`
  - Textarea "Lý do hủy" (optional): `rows-2 border #E2E8F0 radius-10 px-14 py-10 13px`
  - Warning: `bg #FEF3C7 radius-8 p-12 mt-8 13px #92400E`
    "⚠ Chính sách hủy: Miễn phí trước 24 giờ. Sau đó mất 50% phí."
- Footer: "Đóng" (ghost) + "Xác nhận hủy" `bg #EF4444`

---

## API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load danh sách | GET | `/user/bookings?status=&page=1&per_page=10` | Khi mount, đổi tab |
| Hủy đơn | POST | `/user/bookings/{id}/cancel` | Confirm dialog |
