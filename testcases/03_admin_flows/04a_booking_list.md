# Admin — Danh sách Đơn hàng (Booking List)

**Route:** `/admin/bookings` (query `?user_id=`, `?tour_schedule_id=`, `?status=`, `?payment_status=` tùy chọn)  
**Source:** `danangtrip-admin/src/pages/Bookings/BookingList/index.tsx`  
**Automation:** `booking-list.spec.ts` + `booking-list-extended.spec.ts` + `booking-list-backlog.spec.ts` + `admin-booking-list.api.spec.ts` · POM: `BookingListPage.ts`

**Chạy:** `npm run test:admin:booking-list` — **52 passed, 1 skipped** (`--workers=1`)

> **Lưu ý:** Chỉ Admin. Cột PTTT gộp 2 badge trong cột Trạng thái. Eye **navigate** sang detail. Filter “Đã thanh toán” gửi `payment_status=success` (API enum). Sort tiền dùng `sort_by=total_amount`.

---

## 1. Phạm vi

| Hạng mục | Chi tiết |
|----------|----------|
| API list | `GET /admin/bookings` — search, filter, sort, pagination |
| API stats | `GET /admin/bookings/status-counts` |
| API mutation | `PATCH /admin/bookings/:id/status`, `PATCH /admin/bookings/:id/confirm-payment` |
| API export | `GET /admin/bookings/export` |
| Quyền | Admin route guard |

---

## 2. Tổng quan trạng thái

| Nhóm | Tổng TC | ✅ Auto | ⏳ Backlog |
|------|---------|---------|------------|
| Page load & stats | 4 | 4 | 0 |
| Data display | 2 | 2 | 0 |
| Search | 4 | 4 | 0 |
| Filters | 8 | 8 | 0 |
| Sort & pagination | 4 | 4 | 0 |
| Row actions | 9 | 9 | 0 |
| Export | 2 | 2 | 0 |
| Deep link / URL | 5 | 5 | 0 |
| Empty & errors | 3 | 3 | 0 |
| **UI subtotal** | **41** | **41** | **0** |
| API smoke | 7 | 7 | 0 |
| **Tổng automation** | **48** | **48** | **0** |

---

## 2b. UI Inventory (PHASE 0.6)

| # | Vùng UI | Nhãn (i18n) | Loại | Hành vi | TC | Trạng thái |
|---|---------|-------------|------|---------|-----|------------|
| 1 | Header | Danh sách Đơn hàng | h1 | Title | BLIST_001 | ✅ |
| 2 | Header | Xuất Excel | button | Download xlsx | BLIST_004, 076 | ✅ |
| 3 | Stats | Tổng / Chờ XN / Đã XN / Hoàn tất / Đã hủy | cards | API status-counts | BLIST_002, 002b | ✅ |
| 4 | Filter | Tìm theo mã đơn… | input + Lọc | `search` param | BLIST_011–015 | ✅ |
| 5 | Filter | Trạng thái đơn | select auto-apply | `status` | BLIST_018–021, 023 | ✅ |
| 6 | Filter | Thanh toán | select auto-apply | `payment_status` (`success`=đã TT) | BLIST_024–026, 053b | ✅ |
| 7 | Filter | Từ/Đến ngày + Lọc | date + button | `from_date`/`to_date` | BLIST_028 | ✅ |
| 8 | Filter | Chip xóa từng filter | button X | Clear 1 filter | BLIST_036 | ✅ |
| 9 | Filter | Đặt lại | button | Clear all + deep links | BLIST_035 | ✅ |
| 10 | Table | Refresh | icon button | refetch | BLIST_050 | ✅ |
| 11 | Table | Per page | select | `per_page` | BLIST_046 | ✅ |
| 12 | Table | Sort Ngày đặt / Tổng tiền | th click | `sort_by` booked_at / total_amount | BLIST_040, 041 | ✅ |
| 13 | Table | Pagination | buttons | page change | BLIST_064 | ✅ |
| 14 | Row | Xem | button | → detail | BLIST_047 | ✅ |
| 15 | Row | Xác nhận đơn | button (pending) | PATCH status | BLIST_049, 057 | ✅ |
| 16 | Row | Xác nhận thanh toán | button | dialog + PATCH | BLIST_053–054, 062, 065 | ✅ |
| 17 | Row | Hủy đơn | button | dialog + reason | BLIST_058–059, 063, 069, 071–072 | ✅ |
| 18 | Empty | Không tìm thấy đơn | text | API `[]` | BLIST_068 | ✅ |
| 19 | Error | Không tải được list + Thử lại | panel | API 500 | BLIST_077 | ✅ |
| 20 | URL | `?user_id=` | query | Filter user | BLIST_051 | ✅ |
| 21 | URL | `?tour_schedule_id=` | query | Filter schedule (giữ khi đổi filter) | BLIST_052, 052b | ✅ |

---

## 2c. Data Display Integrity (PHASE 0.7)

| # | Vùng UI | Field API | Field UI | TC | Trạng thái |
|---|---------|-----------|----------|-----|------------|
| 1 | Row code | `booking_code` | monospace badge | BLIST_003 | ✅ |
| 2 | Customer | `customer_name`, `customer_email` | avatar + text | BLIST_003 | ✅ |
| 3 | Tour | `tour_name`, `tour_category` | thumbnail + name | BLIST_003, 014 | ✅ |
| 4 | Dates | `booked_at`, `departure_date` | 2 dòng icon | BLIST_003b | ✅ |
| 5 | Amount | `total_amount` | formatted currency | BLIST_003 | ✅ |
| 6 | Badges | `booking_status`, `payment_status` | 2 badges | BLIST_003 | ✅ |
| 7 | Stats | status-counts | 5 cards | BLIST_002, 002b | ✅ |

---

## 3. Test cases (automation)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_BLIST_001 | Heading, stats, filter, table (10 rows/page) | ✅ |
| TC_AD_BLIST_002 | Stats cards đúng số từ mock | ✅ |
| TC_AD_BLIST_002b | Card Hoàn tất đúng số | ✅ |
| TC_AD_BLIST_003 | Mã đơn + KH + tour + tiền từ API | ✅ |
| TC_AD_BLIST_003b | Ngày đặt + ngày khởi hành trong row | ✅ |
| TC_AD_BLIST_004 | Export Excel download | ✅ |
| TC_AD_BLIST_011 | Search theo mã đơn | ✅ |
| TC_AD_BLIST_012 | Search theo tên KH | ✅ |
| TC_AD_BLIST_014 | Search theo tên tour | ✅ |
| TC_AD_BLIST_015 | Search không phân biệt hoa thường | ✅ |
| TC_AD_BLIST_018 | Filter pending | ✅ |
| TC_AD_BLIST_019 | Filter confirmed | ✅ |
| TC_AD_BLIST_020 | Filter completed | ✅ |
| TC_AD_BLIST_021 | Filter cancelled | ✅ |
| TC_AD_BLIST_023 | Mở với `?status=pending` | ✅ |
| TC_AD_BLIST_024 | Filter payment pending | ✅ |
| TC_AD_BLIST_025 | Filter payment paid (API `success`) | ✅ |
| TC_AD_BLIST_026 | Filter payment refunded | ✅ |
| TC_AD_BLIST_028 | Filter khoảng ngày + Lọc | ✅ |
| TC_AD_BLIST_035 | Reset filter | ✅ |
| TC_AD_BLIST_036 | Xóa chip filter trạng thái | ✅ |
| TC_AD_BLIST_040 | Sort cột ngày đặt | ✅ |
| TC_AD_BLIST_041 | Sort cột tổng tiền (`total_amount`) | ✅ |
| TC_AD_BLIST_046 | Đổi per_page 20 | ✅ |
| TC_AD_BLIST_047 | Eye → booking detail | ✅ |
| TC_AD_BLIST_049 | Xác nhận đơn pending | ✅ |
| TC_AD_BLIST_050 | Refresh refetch | ✅ |
| TC_AD_BLIST_051 | Deep link `?user_id=` | ✅ |
| TC_AD_BLIST_052 | Deep link `?tour_schedule_id=` | ✅ |
| TC_AD_BLIST_052b | Giữ `tour_schedule_id` khi đổi status | ✅ |
| TC_AD_BLIST_053 | Mở dialog xác nhận TT | ✅ |
| TC_AD_BLIST_053b | Deep link `?payment_status=success` | ✅ |
| TC_AD_BLIST_054 | Xác nhận thanh toán | ✅ |
| TC_AD_BLIST_057 | Ẩn nút xác nhận khi đã confirmed | ✅ |
| TC_AD_BLIST_058 | Mở dialog hủy đơn | ✅ |
| TC_AD_BLIST_062 | Ẩn nút TT khi cancelled | ✅ |
| TC_AD_BLIST_063 | Ẩn nút hủy khi cancelled | ✅ |
| TC_AD_BLIST_064 | Pagination trang 2 | ✅ |
| TC_AD_BLIST_065 | Đóng dialog TT — không PATCH | ✅ |
| TC_AD_BLIST_068 | Empty state | ✅ |
| TC_AD_BLIST_069 | Validation lý do hủy | ✅ |
| TC_AD_BLIST_071 | Hủy đơn với lý do hợp lệ | ✅ |
| TC_AD_BLIST_072 | Đóng dialog hủy — không PATCH | ✅ |
| TC_AD_BLIST_076 | Export lỗi → toast | ✅ |
| TC_AD_BLIST_077 | List API lỗi → error panel + retry | ✅ |
| TC_AD_BLIST_078 | Mutation lỗi → toast | ✅ |
| API_BLIST_001 | 401 unauthenticated list | ✅ |
| API_BLIST_002 | 200 list admin | ✅ |
| API_BLIST_003 | Filter booking_status | ✅ |
| API_BLIST_005 | Filter user_id | ✅ |
| API_BLIST_007 | Search case-insensitive | ✅ |
| API_BLIST_009 | 200 status-counts | ✅ |
| API_BLIST_014 | 403 customer token | ✅ |

---

## 4. Quy tắc kỹ thuật

- Mock list: `tests/fixtures/data/bookings.data.ts` — 12 rows; `payment_status` dùng `success` (khớp API).
- Search: case-insensitive trong mock — khớp PostgreSQL `ilike`.
- Status/payment select: apply ngay; search/date cần **Lọc** hoặc Enter.
- Sort tiền: UI `total_amount` → API `sort_by=total_amount` (alias `amount` ở API + `bookingApi.ts`).
- Filter đã TT: UI label “Đã thanh toán”, value `success` (alias `paid` ở API).
- `tour_schedule_id` / `user_id` giữ trên URL khi đổi filter khác; Reset xóa deep links.
- Stats API **không** filter theo `status`/`payment_status` (chỉ user_id, search, date).
- Dead code đã xóa: `BookingDetailDialog`, `BookingCard`, `BookingTimeline`.
- Bảng list: `min-w-[1280px]`, không `table-fixed` — xem `memory_test.md` mục **3f**.

---

## 5. Fixes đã áp dụng (2026-06-15)

| Gap | Fix |
|-----|-----|
| Sort amount sai API | `total_amount` + alias API/mock |
| Filter `paid` invalid | Value `success`, label “Đã thanh toán” |
| `tour_schedule_id` mất URL | `buildSearchParams` giữ deep link |
| Dead dialog/card/timeline | Xóa file + cleanup `index.tsx` |
| Stats thiếu Hoàn tất | Card thứ 5 + i18n `completed_label` |
| List API error | Error panel + retry |
| Table layout dồn cột | Mục 3f memory |
