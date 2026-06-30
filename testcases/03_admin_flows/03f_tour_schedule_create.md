# Admin — Thêm lịch khởi hành (Tour Schedule Create)

**Route:** `/admin/tours/:id/schedules/create`  
**Source:** `danangtrip-admin/src/pages/Tours/TourScheduleCreate/index.tsx`  
**Automation:** `tests/admin/tour-schedule-create.spec.ts` + `tour-schedule-create-extended.spec.ts` + `tests/api/admin-tour-schedule-create.api.spec.ts` · POM: `TourScheduleCreatePage.ts`

**Chạy:** `npm run test:admin:tour-schedule-create` — **32 passed** (`--workers=1`)

> **Lưu ý doc gốc (3 TC):** Nút submit là **Thêm lịch** (`schedules:actions.add_new`), **không** phải "Lưu". Trạng thái form là **Đang hoạt động** (`AVAILABLE`) / **Đã hủy** (`CANCELLED`) — **không** có "Mở bán - open". API: `POST /admin/tours/:id/schedules` (prefix `/api/v1`).

---

## 1. Phạm vi

| Hạng mục | Chi tiết |
|----------|----------|
| API create | `POST /admin/tours/:tourId/schedules` |
| API tour info | `GET /admin/tours/:id` (TourInfoBox) |
| Redirect success | Mặc định → `/admin/tours/schedules?tour_id=:id`; từ Tour Edit (`fromTourEdit`) → `/admin/tours/edit/:id` |
| Quyền | Admin route guard |

---

## 2. Tổng quan trạng thái

| Nhóm | Tổng TC | ✅ Auto | ⏳ Backlog |
|------|---------|---------|------------|
| Page load & tour info | 5 | 5 | 0 |
| Form fields & preview | 6 | 6 | 0 |
| Validation | 6 | 6 | 0 |
| Submit & navigation | 6 | 6 | 0 |
| Navigation & UX | 5 | 5 | 0 |
| Error / cancel | 2 | 2 | 0 |
| **UI subtotal** | **30** | **30** | **0** |
| API smoke | 4 | 4 | 0 |
| **Tổng automation** | **34** | **34** | **0** |

---

## 2b. UI Inventory (PHASE 0.6 — audit 2026-06-15)

| # | Vùng UI | Nhãn (i18n) | Loại | Hành vi | TC | Trạng thái |
|---|---------|-------------|------|---------|-----|------------|
| 1 | Header | Thêm lịch | h1 | Title trang | SCHEDCREATE_001 | ✅ added |
| 2 | Breadcrumb | Lịch khởi hành › Thêm lịch | text | Ngữ cảnh điều hướng | SCHEDCREATE_002 | ✅ added |
| 3 | TourInfoBox | Tên tour, danh mục, thời lượng | card | `GET /admin/tours/:id` | SCHEDCREATE_003 | ✅ added |
| 4 | TourInfoBox | Skeleton | placeholder | `isLoadingTour` | SCHEDCREATE_004 | ✅ added |
| 5 | TourInfoBox | Ẩn khi tour lỗi | — | `!tour` → null | SCHEDCREATE_005 | ✅ added |
| 6 | Form | Ngày khởi hành * | date | Yup required + future | SCHEDCREATE_006, 019, 020 | ✅ added |
| 7 | Form | Ngày kết thúc * | date | Yup required + ≥ start | SCHEDCREATE_007, 019, 021 | ✅ added |
| 8 | Form | Số người tối đa * | number | Default 20; min 1 | SCHEDCREATE_008, 019, 023 | ✅ added |
| 9 | Form | Trạng thái | CustomSelect | AVAILABLE / CANCELLED | SCHEDCREATE_009 | ✅ added |
| 10 | Form | Mã chuyến | text | Optional max 50 | SCHEDCREATE_010 | ✅ added |
| 11 | Form | Điểm khởi hành | text | Optional max 255 | SCHEDCREATE_011 | ✅ added |
| 12 | Form | Hạn chót đặt chỗ | date | Optional ≤ start | SCHEDCREATE_012, 022 | ✅ added |
| 13 | Form | Giá NL/TE/EB | CurrencyInput | Optional null = theo tour | SCHEDCREATE_013 | ✅ added |
| 14 | Preview | Xem trước | panel | `useWatch` realtime | SCHEDCREATE_014, 028 | ✅ added |
| 15 | Notice | price_override_help | static | Hướng dẫn giá theo tour | SCHEDCREATE_015 | ✅ added |
| 16 | Header actions | Hủy | button | `navigate(-1)` | SCHEDCREATE_016, 027 | ✅ added |
| 17 | Header actions | Thêm lịch | button | POST create (desktop `md:flex`) | SCHEDCREATE_017, 024 | ✅ added |
| 18 | Mobile bar | Hủy / Thêm lịch | fixed bottom | `md:hidden` | SCHEDCREATE_018 | ✅ added |
| 19 | Toast | Tạo thành công / lỗi | sonner | mutation onSuccess/onError | SCHEDCREATE_024, 026 | ✅ added |
| 20 | Redirect | `fromTourEdit` state | router | Tour Edit → quay lại edit | SCHEDCREATE_025 | ✅ added |

**Doc gốc thiếu (đã bổ sung):** 17/20 control — 3 TC ban đầu **lỗi thời** (nút "Lưu", status "open", thiếu end_date & preview).

---

## 2c. TC tự sinh từ audit (PHASE 0.7)

| ID | Mô tả | Nguồn audit |
|----|-------|-------------|
| TC_AD_SCHEDCREATE_004 | Skeleton TourInfoBox khi đang tải tour | #4 |
| TC_AD_SCHEDCREATE_005 | TourInfoBox ẩn khi GET tour 500 | #5 |
| TC_AD_SCHEDCREATE_021 | endDate < startDate → lỗi | #7 |
| TC_AD_SCHEDCREATE_022 | bookingDeadline > startDate → lỗi | #12 |
| TC_AD_SCHEDCREATE_023 | totalSlots = 0 → lỗi min | #8 |
| TC_AD_SCHEDCREATE_025 | Tạo từ Tour Edit → redirect edit | #20 |
| TC_AD_SCHEDCREATE_026 | API create fail → toast lỗi | #19 |
| TC_AD_SCHEDCREATE_027 | Hủy không gọi POST | #16 |
| TC_AD_SCHEDCREATE_028 | Preview cập nhật khi nhập ngày/slots | #14 |

---

## 3. Test cases

| TT | Test Case ID | Chức năng | Mô tả | Kết quả mong đợi | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | TC_AD_SCHEDCREATE_001 | Page load | Heading + form + preview | Hiển thị đầy đủ layout | ✅ |
| 2 | TC_AD_SCHEDCREATE_002 | Breadcrumb | Ngữ cảnh trang | Lịch khởi hành › Thêm lịch | ✅ |
| 3 | TC_AD_SCHEDCREATE_003 | Tour info | TourInfoBox | Tên tour từ API | ✅ |
| 4 | TC_AD_SCHEDCREATE_004 | Loading | Skeleton tour | Skeleton hiện khi delay tour detail | ✅ |
| 5 | TC_AD_SCHEDCREATE_005 | Tour error | GET tour fail | TourInfoBox không hiện tên | ✅ |
| 6 | TC_AD_SCHEDCREATE_006 | Form fields | Các input chính | start/end date, slots, status visible | ✅ |
| 7 | TC_AD_SCHEDCREATE_007 | Operational | Trường vận hành | departure code/place, deadline | ✅ |
| 8 | TC_AD_SCHEDCREATE_008 | Price section | Giá tùy chọn | 3 CurrencyInput + nhãn Theo tour | ✅ |
| 9 | TC_AD_SCHEDCREATE_009 | Status default | CustomSelect | Mặc định Đang hoạt động | ✅ |
| 10 | TC_AD_SCHEDCREATE_010 | Notice | Help box | price_override_help visible | ✅ |
| 11 | TC_AD_SCHEDCREATE_011 | Mobile actions | Viewport nhỏ | Nút Hủy + Thêm lịch ở bottom bar | ✅ |
| 12 | TC_AD_SCHEDCREATE_012 | Preview empty | Ban đầu | Ngày `-`, giá Theo tour | ✅ |
| 13 | TC_AD_SCHEDCREATE_019 | Validate trống | Submit không điền ngày | Lỗi startDate + endDate; URL giữ nguyên | ✅ |
| 14 | TC_AD_SCHEDCREATE_020 | Ngày quá khứ | startDate < today | Lỗi start_date_future | ✅ |
| 15 | TC_AD_SCHEDCREATE_021 | end < start | endDate trước start | Lỗi end_date_after | ✅ |
| 16 | TC_AD_SCHEDCREATE_022 | Deadline | bookingDeadline > start | Lỗi booking_deadline_before | ✅ |
| 17 | TC_AD_SCHEDCREATE_023 | Slots min | totalSlots = 0 | Lỗi min_number | ✅ |
| 18 | TC_AD_SCHEDCREATE_024 | Tạo thành công | POST + redirect | Toast + `/admin/tours/schedules?tour_id=` | ✅ |
| 19 | TC_AD_SCHEDCREATE_025 | fromTourEdit | Từ Tour Edit | Redirect `/admin/tours/edit/:id` | ✅ |
| 20 | TC_AD_SCHEDCREATE_026 | API error | Mock 500 | Toast lỗi, ở lại trang | ✅ |
| 21 | TC_AD_SCHEDCREATE_027 | Hủy | Cancel | Không POST create | ✅ |
| 22 | TC_AD_SCHEDCREATE_028 | Preview live | Nhập form | Preview hiển thị ngày/slots | ✅ |
| 23 | TC_AD_SCHEDCREATE_029 | POST operational | Mã chuyến / điểm KH / deadline | Body API có `departure_*`, `booking_deadline` | ✅ |
| 24 | API_SCHEDCREATE_001 | API auth | POST không token | 401 | ✅ |
| 24 | API_SCHEDCREATE_002 | API create | POST hợp lệ admin | 201 + body schedule | ✅ |
| 25 | API_SCHEDCREATE_003 | API validation | start_date quá khứ | 422 | ✅ |
| 26 | API_SCHEDCREATE_004 | API not found | tour_id không tồn tại | 404 | ✅ |

---

## Ghi chú

- **Fix 2026-06-15 (P1):** Create gửi đủ `departureCode/Place/bookingDeadline`; banner lỗi tour + disable submit; `pb-24` mobile.
- **Fix 2026-06-15 (P2):** Sticky header collapse; breadcrumb link; cancel/`?from=edit`; slots mặc định từ `tour.max_people`; auto `endDate`; preview vận hành; a11y `htmlFor` + `min` date.
- Sticky header collapse (Tour Create style) **chưa** có trên màn này — không yêu cầu TC scroll.
- Doc gốc TC_001–003 đã được **map** lần lượt → SCHEDCREATE_019, 020, 024 (cập nhật nhãn & kỳ vọng).