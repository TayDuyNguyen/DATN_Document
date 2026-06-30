# Admin — Chi tiết Booking (Booking Detail)

**Route:** `/admin/bookings/detail/:id`  
**Source:** `danangtrip-admin/src/pages/Bookings/BookingDetail/index.tsx`  
**Automation:** `booking-detail.spec.ts` + `booking-detail-extended.spec.ts` + `booking-detail-auth.spec.ts` + `admin-booking-detail.api.spec.ts` · POM: `BookingDetailPage.ts`

**Chạy:** `npm run test:admin:booking-detail` — **45 passed** (`--workers=1`)

> **Lưu ý:** Chỉ Admin. Sticky header thu gọn khi cuộn `<main>`. Complete dùng `window.confirm`. Cancel qua dialog lý do. Invoice tải PDF mock. Mock detail: `booking-detail.data.ts` + `bookings.mock.ts`.

---

## 1. Phạm vi

| Hạng mục | Chi tiết |
|----------|----------|
| API detail | `GET /admin/bookings/:id` |
| API mutation | `PATCH /admin/bookings/:id/status`, `PATCH /admin/bookings/:id/confirm-payment` |
| API invoice | `GET /admin/bookings/:id/invoice` |
| Quyền | Admin route guard |

---

## 2. Tổng quan trạng thái

| Nhóm | Tổng TC | ✅ Auto | Ghi chú |
|------|---------|---------|---------|
| Permission | 2 | 2 | `BDET_001`, `002` |
| Load / error / retry | 4 | 4 | skeleton delay, 404, retry |
| Data display | 12 | 12 | customer, tour, payment, passengers |
| Timeline | 4 | 4 | booked → cancelled |
| Actions | 14 | 14 | confirm, complete, cancel, payment, invoice |
| Terminal / regression | 3 | 3 | completed, cancelled, lifecycle |
| UX | 3 | 3 | sticky collapse, mobile, viewport screenshot |
| **UI subtotal** | **42** | **42** | |
| API smoke | 4 | 4 | khi API live |
| **Tổng automation** | **45** | **45** | **đóng module** |

---

## 2b. UI Inventory (PHASE 0.6)

| # | Vùng UI | Nhãn (i18n) | Loại | Hành vi | TC | Trạng thái |
|---|---------|-------------|------|---------|-----|------------|
| 1 | Header | Quay lại danh sách | button | → `/admin/bookings` | BDET_007 | ✅ |
| 2 | Header | Xuất hóa đơn | button | GET invoice PDF | BDET_037, 038 | ✅ |
| 3 | Header | Booking / Payment badges | badge | status hiển thị | BDET_008 | ✅ |
| 4 | Sticky | Badge Chi tiết khi scroll | span | collapse | BDET_041 | ✅ |
| 5 | Customer | name, email, phone, address, note | text | data display | BDET_009–011 | ✅ |
| 6 | Tour | thumbnail / fallback | img / icon | có/không ảnh | BDET_012, 013 | ✅ |
| 7 | Tour | travel date, departure, schedule | grid | format locale | BDET_014, 015 | ✅ |
| 8 | Passengers | adults / children / infants | counts | tổng items | BDET_016, 017 | ✅ |
| 9 | Payment | subtotal, discount, deposit, final | currency | không NaN | BDET_018, 019 | ✅ |
| 10 | Operations | Xác nhận đơn | button | PATCH confirmed | BDET_024, 025, 026 | ✅ |
| 11 | Operations | Xác nhận thanh toán | button + dialog | PATCH confirm-payment | BDET_053 | ✅ |
| 12 | Operations | Hoàn tất đơn | button + confirm | PATCH completed | BDET_027–030 | ✅ |
| 13 | Operations | Hủy đơn | button + dialog | PATCH cancelled + reason | BDET_031–034 | ✅ |
| 14 | Timeline | booked / confirmed / completed / cancelled | milestones | ngày + lý do | BDET_020–023 | ✅ |
| 15 | Error | Back + Retry | buttons | refetch detail | BDET_005, 006 | ✅ |
| 16 | Mobile | actions usable 375px | layout | scroll + click | BDET_039 | ✅ |

---

## 2c. Data Display Integrity (PHASE 0.7)

| # | Vùng UI | Field API | Field UI | TC | Trạng thái |
|---|---------|-----------|----------|-----|------------|
| 1 | Customer | `customer_name`, `customer_email`, … | card text | BDET_009 | ✅ |
| 2 | Tour thumb | `items[].tour.thumbnail` | `<img alt={name}>` | BDET_012 | ✅ fallback URL mock |
| 3 | Passengers | `quantity_adult/child/infant` | grid 3 cột | BDET_016 | ✅ |
| 4 | Payment | `total_amount`, `discount_amount`, … | format VNĐ | BDET_018 | ✅ |
| 5 | Timeline | `booked_at`, `confirmed_at`, … | milestone date | BDET_021 | ✅ |

---

## 3. Map doc ID → Playwright ID

| Doc (ADMIN_BOOKING_DETAIL_*) | Playwright | Auto |
|------------------------------|------------|------|
| 001 Guest | TC_AD_BDET_001 | ✅ |
| 002 User | TC_AD_BDET_002 | ✅ |
| 003 Load detail | TC_AD_BDET_003 | ✅ |
| 004 Loading skeleton | TC_AD_BDET_004 | ✅ |
| 005 Invalid id | TC_AD_BDET_005 | ✅ |
| 006 Retry | TC_AD_BDET_006 | ✅ |
| 007 Back | TC_AD_BDET_007 | ✅ |
| 008 Badges | TC_AD_BDET_008 | ✅ |
| 009 Customer full | TC_AD_BDET_009 | ✅ |
| 010 Address missing | TC_AD_BDET_010 | ✅ |
| 011 Note missing | TC_AD_BDET_010 (cùng edge fixture) | ✅ |
| 012 Thumbnail | TC_AD_BDET_012 | ✅ |
| 013 No thumbnail | TC_AD_BDET_013 | ✅ |
| 014 Schedule | TC_AD_BDET_014 | ✅ |
| 015 Departure missing | TC_AD_BDET_015 | ✅ |
| 016 Passenger totals | TC_AD_BDET_016, 016b | ✅ |
| 017 Passenger zero | TC_AD_BDET_010 (edge 0 child/infant) | ✅ |
| 018 Payment summary | TC_AD_BDET_018 | ✅ |
| 019 Discount zero | TC_AD_BDET_019 | ✅ |
| 020–023 Timeline | TC_AD_BDET_020–023 | ✅ |
| 024 Confirm visible | TC_AD_BDET_024 | ✅ |
| 025 Confirm action | TC_AD_BDET_025 | ✅ |
| 026 Confirm API error | TC_AD_BDET_026 | ✅ |
| 027 Complete visible | TC_AD_BDET_027 | ✅ |
| 028 Complete dismiss confirm | TC_AD_BDET_028 | ✅ |
| 029 Complete action | TC_AD_BDET_029 | ✅ |
| 030 Complete API error | TC_AD_BDET_030 | ✅ |
| 031 Cancel visible | TC_AD_BDET_024 | ✅ |
| 032 Cancel reason | TC_AD_BDET_032 | ✅ |
| 033 Cancel empty reason | TC_AD_BDET_033 | ✅ |
| 034 Cancel API error | TC_AD_BDET_034 | ✅ |
| 035 Terminal completed | TC_AD_BDET_035 | ✅ |
| 036 Terminal cancelled | TC_AD_BDET_036 | ✅ |
| 037 Invoice | TC_AD_BDET_037 | ✅ |
| 038 Invoice error | TC_AD_BDET_038 | ✅ |
| 039 Responsive mobile | TC_AD_BDET_039 | ✅ |
| 040 Lifecycle | TC_AD_BDET_040 | ✅ |
| — Confirm payment (inventory) | TC_AD_BDET_053 | ✅ |
| — Sticky collapse | TC_AD_BDET_041 | ✅ |
| — Viewport 1535×697 | TC_AD_BDET_060 | ✅ |

**API:** `API_BDET_001`–`004`

---

## 4. Test cases chi tiết (mô tả gốc)

| ID | Nhóm chức năng | Test case | Tiền điều kiện | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Mức độ ưu tiên | Loại test |
| -- | -------------- | --------- | -------------- | -------------- | ------------ | ---------------- | -------------- | --------- |
| ADMIN_BOOKING_DETAIL_001 | Permission | Guest vào route admin | Chưa đăng nhập | 1. Mở `/admin/bookings/detail/1`. | guest | Bị redirect `/login`; không thấy data booking. | High | Permission |
| ADMIN_BOOKING_DETAIL_002 | Permission | User thường vào route admin | Đăng nhập role user | 1. Mở route detail. | user | Bị chặn bởi PrivateRoute; không render BookingDetail. | High | Permission |
| ADMIN_BOOKING_DETAIL_003 | Load dữ liệu | Admin mở booking hợp lệ | Booking tồn tại | 1. Login admin.<br>2. Mở `/admin/bookings/detail/1001`. | id=1001 | Header, badges, customer, tour, passenger, payment, timeline hiển thị đúng. | High | Functional |
| ADMIN_BOOKING_DETAIL_004 | Loading | Skeleton khi API chậm | Delay detail | 1. Mở route. | delay | Hiển thị skeleton grid; không hiển thị nội dung rỗng. | Medium | UI |
| ADMIN_BOOKING_DETAIL_005 | Invalid id | Booking không tồn tại | ID sai | 1. Mở `/admin/bookings/detail/999999`. | invalid | Hiển thị error card, Back và Retry. | High | Negative |
| ADMIN_BOOKING_DETAIL_006 | Retry | Retry sau lỗi | API lỗi rồi phục hồi | 1. Mở lỗi.<br>2. Click Retry. | 500->200 | Gọi refetch và hiển thị data sau khi thành công. | Medium | API |
| ADMIN_BOOKING_DETAIL_007 | Back | Quay về danh sách | Detail đang mở | 1. Click Back. | | Điều hướng `/admin/bookings`. | Medium | Functional |
| ADMIN_BOOKING_DETAIL_008 | Header badges | Hiển thị status badges | Booking có status/payment | 1. Quan sát header. | pending/unpaid | BookingStatusBadge và PaymentStatusBadge đúng status/màu. | High | UI |
| ADMIN_BOOKING_DETAIL_009 | Customer full | Thông tin khách đầy đủ | Booking có name/email/phone/address/note | 1. Quan sát customer card. | full | Tên, email, phone, address, note hiển thị đúng. | High | Functional |
| ADMIN_BOOKING_DETAIL_010 | Customer missing address | Thiếu địa chỉ | address null | 1. Mở detail. | null | Hiển thị fallback `address_missing`, không undefined. | Medium | Edge Case |
| ADMIN_BOOKING_DETAIL_011 | Customer missing note | Thiếu ghi chú | note null | 1. Mở detail. | null | Hiển thị `no_note`, không trống xấu. | Low | Edge Case |
| ADMIN_BOOKING_DETAIL_012 | Tour thumbnail | Tour có ảnh | item.tour.thumbnail có URL | 1. Quan sát tour card. | thumbnail | Ảnh hiển thị đúng kích thước, alt là tên tour. | Medium | UI |
| ADMIN_BOOKING_DETAIL_013 | Tour no thumbnail | Tour thiếu ảnh | thumbnail null | 1. Mở detail. | null | Hiển thị fallback icon ShoppingBag. | Medium | Edge Case |
| ADMIN_BOOKING_DETAIL_014 | Tour schedule | Hiển thị lịch khởi hành | Có travelDate/departurePlace/scheduleId | 1. Quan sát grid schedule. | full | Travel date format đúng locale, departure place, schedule code hiển thị. | High | Functional |
| ADMIN_BOOKING_DETAIL_015 | Missing departure place | Thiếu điểm khởi hành | departurePlace null | 1. Mở detail. | null | Hiển thị `departure_place_missing`. | Medium | Edge Case |
| ADMIN_BOOKING_DETAIL_016 | Passenger totals | Tính tổng hành khách | Booking nhiều items | 1. Quan sát PassengerListPlaceholder. | 2 items | Adults/children/infants bằng tổng các booking items. | High | Functional |
| ADMIN_BOOKING_DETAIL_017 | Passenger zero | Không có trẻ em/em bé | child=0, infant=0 | 1. Mở detail. | 0 | Hiển thị 0, không ẩn sai hoặc NaN. | Medium | Edge Case |
| ADMIN_BOOKING_DETAIL_018 | Payment summary | Tổng tiền | Booking có total/discount/deposit/final | 1. Quan sát payment card. | full | Format tiền đúng; discount âm; final amount nổi bật. | High | Functional |
| ADMIN_BOOKING_DETAIL_019 | Payment zero discount | Discount 0 | discount=0 | 1. Mở detail. | 0 | Hiển thị `- 0 ₫` hoặc format nhất quán, không NaN. | Low | Edge Case |
| ADMIN_BOOKING_DETAIL_020 | Timeline booked | Mốc booked | Booking mới | 1. Quan sát timeline. | bookedAt | Mốc booked luôn completed và có ngày. | Medium | UI |
| ADMIN_BOOKING_DETAIL_021 | Timeline confirmed | Mốc confirmed | confirmedAt có giá trị | 1. Mở confirmed. | confirmed | Mốc confirmed active, ngày đúng. | Medium | UI |
| ADMIN_BOOKING_DETAIL_022 | Timeline completed | Mốc completed | completedAt/status completed | 1. Mở completed. | completed | Mốc completed active; operations hiển thị terminal notice. | High | UI |
| ADMIN_BOOKING_DETAIL_023 | Timeline cancelled | Mốc cancelled | status cancelled | 1. Mở cancelled. | reason | Timeline thêm mốc cancelled và hiển thị reason nếu có. | High | UI |
| ADMIN_BOOKING_DETAIL_024 | Confirm visible | Nút confirm chỉ hiện pending | Booking pending | 1. Mở detail. | pending | Nút confirm hiển thị; complete không hiển thị. | High | Functional |
| ADMIN_BOOKING_DETAIL_025 | Confirm action | Xác nhận booking | Booking pending | 1. Click Confirm. | pending | Gọi `updateStatus` với `confirmed`; toast success; query cập nhật. | High | Functional |
| ADMIN_BOOKING_DETAIL_026 | Confirm API lỗi | Confirm thất bại | API 500 | 1. Click Confirm. | 500 | Toast update_error; status UI không đổi sai. | High | API |
| ADMIN_BOOKING_DETAIL_027 | Complete visible | Nút complete chỉ hiện confirmed | Booking confirmed | 1. Mở detail. | confirmed | Nút complete hiển thị; confirm không hiển thị. | High | Functional |
| ADMIN_BOOKING_DETAIL_028 | Complete cancel window confirm | Admin hủy confirm browser | Booking confirmed | 1. Click complete.<br>2. Chọn Cancel ở browser confirm. | | Không gọi API updateStatus. | Medium | Negative |
| ADMIN_BOOKING_DETAIL_029 | Complete action | Hoàn thành booking | Booking confirmed | 1. Click complete.<br>2. Xác nhận browser confirm. | confirmed | Gọi status `completed`; nút loading; toast success. | High | Functional |
| ADMIN_BOOKING_DETAIL_030 | Complete API lỗi | Complete thất bại | API 500 | 1. Confirm complete. | 500 | Toast update_error; `isCompleting` trở về false. | High | API |
| ADMIN_BOOKING_DETAIL_031 | Cancel visible | Nút cancel hiện với non-terminal | Booking pending/confirmed | 1. Mở detail. | pending | Nút cancel hiển thị trong operations. | High | Functional |
| ADMIN_BOOKING_DETAIL_032 | Cancel reason valid | Hủy booking | Booking pending | 1. Click Cancel.<br>2. Nhập lý do.<br>3. Submit. | `Khách yêu cầu hủy` | Gọi updateStatus `cancelled` kèm reason; toast success; dialog đóng. | High | Functional |
| ADMIN_BOOKING_DETAIL_033 | Cancel reason empty | Lý do trống | Dialog mở | 1. Submit không nhập lý do. | empty | Dialog validation chặn hoặc không gửi API. | High | Validation |
| ADMIN_BOOKING_DETAIL_034 | Cancel API lỗi | Hủy thất bại | API 500 | 1. Submit reason. | 500 | Toast update_error; dialog/booking không cập nhật sai. | High | API |
| ADMIN_BOOKING_DETAIL_035 | Terminal completed | Booking completed | status completed | 1. Mở detail. | completed | Không hiển thị confirm/complete/cancel; có notice completed. | High | Regression |
| ADMIN_BOOKING_DETAIL_036 | Terminal cancelled | Booking cancelled | status cancelled | 1. Mở detail. | cancelled | Không hiển thị action; có notice cancelled. | High | Regression |
| ADMIN_BOOKING_DETAIL_037 | Invoice download | Tải hóa đơn | Booking có invoice | 1. Click invoice. | id | Gọi `getInvoice`; tải file fallback `hoa_don_{code}.pdf`; toast export_success. | High | Functional |
| ADMIN_BOOKING_DETAIL_038 | Invoice API lỗi | Invoice lỗi | API 500 | 1. Click invoice. | 500 | Toast export_error; button hết loading. | Medium | API |
| ADMIN_BOOKING_DETAIL_039 | Responsive | Layout mobile/tablet | Viewport 375/768 | 1. Mở detail.<br>2. Quan sát sticky header, grid. | mobile | Header không tràn; layout chuyển 1 cột; actions vẫn dùng được. | Medium | Responsive |
| ADMIN_BOOKING_DETAIL_040 | Regression full lifecycle | Pending -> confirmed -> completed | Booking test pending | 1. Mở detail.<br>2. Confirm.<br>3. Refetch.<br>4. Complete. | pending | Trạng thái chuyển đúng, action thay đổi đúng, timeline cập nhật. | High | Regression |

---

## 5. Test data đề xuất

* Booking pending unpaid (`id=101`), confirmed paid (`103`), completed (`107`), cancelled có lý do (`104`).
* Booking edge minimal (`112`) — thiếu address/note/thumbnail/departure.
* Booking multi passenger (`108`) — 2 items.
* Admin account hợp lệ; user thường để test guard.

**Mock flags:** `setBookingDetailFail`, `setBookingDetailDelay`, `setBookingMutationFail`, `setBookingInvoiceFail`

---

## 6. Checklist regression

* Chỉ admin vào được route.
* Confirm/complete/cancel chỉ hiện đúng trạng thái.
* Timeline không sai mốc ngày.
* Invoice không treo loading khi lỗi.
* Customer/tour/payment card không lộ undefined/NaN.
* Mobile không tràn header; nút action scroll được.

---

## 7. Ghi chú kỹ thuật

* Logic lấy từ `BookingDetail/index.tsx`.
* API lấy từ `bookingApi.ts` / `useBookingQueries`.
* Screenshot UI: `reports/ui-screenshots/booking-detail/<TC_ID>.png` — viewport **1535×697**.
* POM scope `main` cho section headings — tránh trùng sidebar/layout.

---

## 8. Đề xuất cải thiện (Improvement backlog — PHASE 0.8)

> Chi tiết đầy đủ + ID: `memory_test.md` mục **11**. Cập nhật khi fix xong (`open` → `fixed`).

| ID | Loại | Ưu tiên | Tóm tắt | Trạng thái |
|----|------|---------|---------|------------|
| IMP_BDET_001 | UX | P1 | Error load/404 dùng nhầm copy `update_error` | **fixed** 2026-06-18 |
| IMP_BDET_002 | UX/A11y | P1 | Complete dùng `window.confirm` thay dialog | **fixed** — `BookingCompleteDialog` |
| IMP_BDET_003 | UI | P1 | PTTT hiện raw enum (`bank_transfer`) | **fixed** — `PaymentGatewayBadge` |
| IMP_BDET_004 | UX | P1 | Xuất hóa đơn ẩn trên mobile (`hidden md:flex`) | **fixed** — Operations + mobile footer |
| IMP_BDET_005 | UX | P2 | Mobile: actions xa, cần sticky footer | **fixed** — `data-booking-detail-mobile-footer` |
| IMP_BDET_006 | UI | P2 | Layout `max-w-[1600px]` chưa full-bleed | **fixed** |
| IMP_BDET_007 | Function | P2 | Thiếu link nhanh → user / tour detail | **fixed** |
| IMP_BDET_008 | Mock | P2 | Mock còn `bank_transfer` (web đã SePay-only) | **fixed** — mock `sepay` |
| IMP_BDET_009 | API | P3 | Danh sách hành khách chi tiết — backlog API | deferred |
| IMP_BDET_010 | Test | P3 | Error state thiếu test id ổn định | **fixed** — `data-testid="booking-detail-error"` |

**Ưu tiên sửa trước release:** IMP_BDET_001 → 004 (copy lỗi, dialog, PTTT label, mobile invoice).
