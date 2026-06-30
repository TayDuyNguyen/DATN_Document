# Admin — Chi tiết lịch khởi hành (Tour Schedule Detail)

**Route thực tế:** `/admin/tours/schedules/detail/:id` (read-only) · Edit: `/admin/tours/schedules/edit/:id`  
**API:** `GET /admin/tour-schedules/:id` (+ `GET /admin/tours/:id` cho TourInfoBox, `GET /admin/bookings?tour_schedule_id=` cho link đơn)  
**Source:** `danangtrip-admin/src/pages/Tours/TourScheduleDetail/index.tsx`  
**Components read-only:** `ScheduleInfoBox`, `ScheduleStatsBlock`, `ScheduleDetailPanels`, `TourInfoBox`  
**Automation:** `tests/admin/tour-schedule-detail.spec.ts` + `tour-schedule-detail-extended.spec.ts` + `tests/api/admin-tour-schedule-detail.api.spec.ts` · POM: `TourScheduleDetailPage.ts`

**Chạy:** `npm run test:admin:tour-schedule-detail` — **30 passed, 3 skipped** (`API_SCHEDDETAIL_004` user login, `008`/`009` seed mismatch live API, `--workers=1`)

> **Lưu ý doc gốc (34 TC `ADMIN_SCHEDULE_*`):** Nội dung cũ gộp list/create/edit — **lỗi thời**, đã tách sang `03e` / `03f` / `03g`. File này chỉ cover **xem chi tiết lịch** (API GET + panel read-only + điểm vào).

---

## 1. Phạm vi

| Hạng mục | Chi tiết |
|----------|----------|
| API detail | `GET /admin/tour-schedules/:id` — nested `tour`, dates, slots, status, giá, vận hành |
| UI detail | `ScheduleDetailPanels` (tóm tắt) + `ScheduleInfoBox` + `ScheduleStatsBlock` |
| Route detail | `/admin/tours/schedules/detail/:id` — nút **Chỉnh sửa** → Edit |
| Điểm vào | List → **Xem chi tiết** (Eye) · List → Edit · Tour Edit departures → Edit · Tour Edit “Quản lý lịch” → List · “Thêm lịch” → Create |
| Quyền | Admin route guard |
| Mapper | `schedule.mapper.ts` — `toYmd`, status normalize, `price_*` null → “Theo tour” |

---

## 2. Tổng quan trạng thái

| Nhóm | Tổng TC | ✅ Auto | ⏳ Backlog |
|------|---------|---------|------------|
| Auth | 1 | 1 | 0 |
| Load & detail preload | 2 | 2 | 0 |
| ScheduleInfoBox display | 4 | 4 | 0 |
| Stats & progress | 2 | 2 | 0 |
| Status variants (FULL/CANCELLED) | 3 | 3 | 0 |
| Operational & price display | 3 | 3 | 0 |
| Error & retry | 2 | 2 | 0 |
| Navigation / entry | 4 | 4 | 0 |
| Responsive & screenshot | 2 | 2 | 0 |
| **UI subtotal** | **23** | **23** | **0** |
| API smoke | 11 | 11 | 0 |
| **Tổng automation** | **34** | **30** | **3** (API live seed) |

---

## 2b. UI Inventory (PHASE 0.6 — audit 2026-06-18)

| # | Vùng UI | Nhãn (i18n) | Loại | Hành vi | TC | Trạng thái |
|---|---------|-------------|------|---------|-----|------------|
| 1 | ScheduleInfoBox | Ngày KH – KT | text | `startDate`–`endDate` từ API | SCHEDDETAIL_020 | ✅ added |
| 2 | ScheduleInfoBox | Badge trạng thái | badge | AVAILABLE / FULL / CANCELLED | SCHEDDETAIL_021–023 | ✅ added |
| 3 | ScheduleInfoBox | Sức chứa | text | `bookedSlots / totalSlots` | SCHEDDETAIL_024 | ✅ added |
| 4 | ScheduleInfoBox | Tên tour | text | `schedule.tourName` | SCHEDDETAIL_025 | ✅ added |
| 5 | ScheduleStatsBlock | THỐNG KÊ LỊCH | block | booked / available / max | SCHEDDETAIL_026 | ✅ added |
| 6 | ScheduleStatsBlock | Progress % | bar | Màu theo %; 100% khi full | SCHEDDETAIL_027 | ✅ added |
| 7 | ScheduleDetailPanels | Tóm tắt (id, ngày, vận hành, giá) | panel | `ScheduleDetailPanels` | SCHEDDETAIL_010, 030–032 | ✅ added |
| 8 | ScheduleDetailPanels | Giá Theo tour / VND | panel | null vs override | SCHEDDETAIL_031–032 | ✅ added |
| 9 | Error | not_found / server_error + Thử lại | alert + button | 404 vs 5xx | SCHEDDETAIL_012–013 | ✅ added |
| 10 | Breadcrumb | Lịch khởi hành | link | → list `?tour_id=` | SCHEDDETAIL_043 | ✅ added |
| 11 | Entry List | Xem chi tiết (Eye) | icon | → detail + GET | SCHEDDETAIL_042 | ✅ added |
| 12 | Entry Tour Edit | Chỉnh sửa đợt KH | button | → edit + GET detail | SCHEDDETAIL_040 | ✅ added |
| 13 | Entry Tour Edit | Thêm lịch / Quản lý lịch | button | create · list `?tour_id=` | SCHEDDETAIL_041 | ✅ added |

**Doc gốc thiếu:** 34/34 TC cũ trùng module khác — **thay thế hoàn toàn**.

---

## 2c. Data Display Audit (PHASE 0.7)

| # | Vùng UI | Field API | Field UI | Shape mock | Mapper | TC | Trạng thái |
|---|---------|-----------|----------|------------|--------|-----|------------|
| 1 | InfoBox dates | `start_date`, `end_date` | `formatAdminShortDate` | `YYYY-MM-DD` | `toYmd` | SCHEDDETAIL_020 | ✅ |
| 2 | InfoBox dates legacy | `2026-06-20T00:00:00Z` | input `YYYY-MM-DD` | ISO string | `toYmd` | SCHEDDETAIL_033 | ✅ added |
| 3 | Capacity | `booked_people`, `max_people` | `2 / 20` | seed mock | `toNumberSafe` | SCHEDDETAIL_024 | ✅ |
| 4 | Status FULL | `status: full` | Đầy chỗ | id 102 mock | `normalizeStatus` | SCHEDDETAIL_022 | ✅ added |
| 5 | Status CANCELLED | `status: cancelled` | Đã hủy | id 103 mock | `normalizeStatus` | SCHEDDETAIL_023 | ✅ added |
| 6 | Tour name | `tour.name` | heading h4 | nested tour | `tourName` | SCHEDDETAIL_025 | ✅ |
| 7 | Giá null | `price_adult: null` | Theo tour | mock default | preview helper | SCHEDDETAIL_031 | ✅ added |
| 8 | Giá override | `price_adult: 1500000` | `1.500.000 ₫` | patch mock | `formatCurrency` | SCHEDDETAIL_032 | ✅ added |
| 9 | API error | 500 GET | alert + retry | mock fail | — | SCHEDDETAIL_012–013 | ✅ added |
| 10 | 404 id | missing row | fetch_error | id 999999 | — | SCHEDDETAIL_012 | ✅ added |

---

## 2d. TC tự sinh từ audit

| ID | Mô tả | Nguồn |
|----|-------|-------|
| TC_AD_SCHEDDETAIL_022 | Badge FULL + capacity full | PHASE 0.7 #4 |
| TC_AD_SCHEDDETAIL_023 | Badge CANCELLED | PHASE 0.7 #5 |
| TC_AD_SCHEDDETAIL_027 | Progress 100% full schedule | #6 |
| TC_AD_SCHEDDETAIL_031 | Giá “Theo tour” khi null | #7 |
| TC_AD_SCHEDDETAIL_032 | Giá override VND | #8 |
| TC_AD_SCHEDDETAIL_033 | ISO date legacy shape | #2 |
| TC_AD_SCHEDDETAIL_013 | Retry sau GET lỗi | #9 |
| TC_AD_SCHEDDETAIL_040–042 | Entry Tour Edit / List | Inventory #11–12 |
| TC_AD_SCHEDDETAIL_060 | Screenshot 1535×697 | memory §3c |

---

## 3. Test cases (automation)

| TT | Test Case ID | Chức năng | Mô tả | Status |
| --- | --- | --- | --- | --- |
| 1 | TC_AD_SCHEDDETAIL_001 | Auth | Guest → login | ✅ |
| 2 | TC_AD_SCHEDDETAIL_010 | Preload | Form + status từ GET detail | ✅ |
| 3 | TC_AD_SCHEDDETAIL_012 | Error | ID không tồn tại → alert | ✅ |
| 4 | TC_AD_SCHEDDETAIL_013 | Retry | Thử lại sau GET 500 | ✅ |
| 5 | TC_AD_SCHEDDETAIL_020 | InfoBox | Ngày khởi hành hiển thị | ✅ |
| 6 | TC_AD_SCHEDDETAIL_021 | InfoBox | Badge Đang hoạt động | ✅ |
| 7 | TC_AD_SCHEDDETAIL_022 | InfoBox | Badge Đầy chỗ | ✅ |
| 8 | TC_AD_SCHEDDETAIL_023 | InfoBox | Badge Đã hủy | ✅ |
| 9 | TC_AD_SCHEDDETAIL_024 | InfoBox | Capacity booked/max | ✅ |
| 10 | TC_AD_SCHEDDETAIL_025 | TourInfoBox | Tên tour nested API | ✅ |
| 11 | TC_AD_SCHEDDETAIL_026 | Stats | 3 ô + nhãn | ✅ |
| 12 | TC_AD_SCHEDDETAIL_027 | Stats | Progress 100% full | ✅ |
| 13 | TC_AD_SCHEDDETAIL_030 | Vận hành | Preload mã/điểm/deadline | ✅ |
| 14 | TC_AD_SCHEDDETAIL_031 | Preview | Giá Theo tour | ✅ |
| 15 | TC_AD_SCHEDDETAIL_032 | Preview | Giá override VND | ✅ |
| 16 | TC_AD_SCHEDDETAIL_033 | Mapper | ISO date → input | ✅ |
| 17 | TC_AD_SCHEDDETAIL_040 | Navigation | Tour Edit → edit lịch | ✅ |
| 18 | TC_AD_SCHEDDETAIL_041 | Navigation | Tour Edit → Thêm lịch | ✅ |
| 19 | TC_AD_SCHEDDETAIL_042 | Navigation | List → edit + detail | ✅ |
| 20 | TC_AD_SCHEDDETAIL_043 | Navigation | Breadcrumb → list filter | ✅ |
| 21 | TC_AD_SCHEDDETAIL_060 | Screenshot | Viewport 1535×697 | ✅ |
| 22 | TC_AD_SCHEDDETAIL_061 | Responsive | Mobile info box | ✅ |
| 23 | API_SCHEDDETAIL_001 | API | GET 401 | ✅ |
| 24 | API_SCHEDDETAIL_002 | API | GET 200 admin | ✅ |
| 25 | API_SCHEDDETAIL_003 | API | GET 404 | ✅ |
| 26 | API_SCHEDDETAIL_004 | API | GET 403 user | ✅ |
| 27 | API_SCHEDDETAIL_005 | API | booked ≤ max | ✅ |
| 28 | API_SCHEDDETAIL_006 | API | nested tour.name | ✅ |
| 29 | API_SCHEDDETAIL_007 | API | status available | ✅ |
| 30 | API_SCHEDDETAIL_008 | API | status full (id 102) | ✅ |
| 31 | API_SCHEDDETAIL_009 | API | status cancelled (id 103) | ✅ |
| 32 | API_SCHEDDETAIL_010 | API | operational fields | ✅ |
| 33 | API_SCHEDDETAIL_011 | API | nullable price fields | ✅ |

---

## 4. Test data

| Seed / mock | Mô tả |
|-------------|--------|
| `id=99` | AVAILABLE, tour 1, 0/15 booked — default detail |
| `id=101` | 10/30 booked — stats notice (cover ở 03g) |
| `id=102` | FULL 25/25 — badge + progress 100% |
| `id=103` | CANCELLED 5/20 |
| `invalidScheduleId=999999` | 404 UI |
| `detailOperationalFixture` | departure_code, place, deadline |
| `isoStartDateLegacy` | `2026-06-20T00:00:00.000Z` |

---

## 5. Checklist regression

* GET detail 404 → không crash; có retry.
* ISO `start_date` không làm form trống.
* Badge FULL/CANCELLED khớp `schedule.mapper` normalize.
* Giá null → “Theo tour”; có số → format VND.
* Sau test API live: xóa dữ liệu + sync sequence (`memory_test.md` §3d).

---

## 6. Ghi chú kỹ thuật

* Chi tiết lịch **không** có route riêng — Edit vừa xem vừa sửa; mutation TC nằm ở **03g**.
* List/create TC nằm ở **03e** / **03f**.
* Mock: `patchMockSchedule`, `setScheduleDetailFail`, `clearScheduleDetailFail`.
* Screenshot: `reports/ui-screenshots/tour-schedule-detail/<TC_ID>.png`.

---

## 7. Liên kết module

| Module | File | Quan hệ |
|--------|------|---------|
| List | `03e_tour_schedule_list.md` | Entry edit → detail |
| Create | `03f_tour_schedule_create.md` | Entry từ Tour Edit manage |
| Edit | `03g_tour_schedule_edit.md` | Mutation + shared route |
| Tour Modal | `03d_tour_detail_modal.md` | Preview lịch từ list API |
