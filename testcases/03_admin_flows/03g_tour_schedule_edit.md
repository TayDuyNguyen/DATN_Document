# Admin — Chỉnh sửa lịch khởi hành (Tour Schedule Edit)

**Route:** `/admin/tours/schedules/edit/:id`  
**Source:** `danangtrip-admin/src/pages/Tours/TourScheduleEdit/index.tsx`  
**Automation:** `tests/admin/tour-schedule-edit.spec.ts` + `tour-schedule-edit-extended.spec.ts` + `tests/api/admin-tour-schedule-edit.api.spec.ts` · POM: `TourScheduleEditPage.ts`

**Chạy:** `npm run test:admin:tour-schedule-edit` — **32 passed, 1 skipped** (`API_SCHEDEDIT_005`, `--workers=1`)

> **Lưu ý doc gốc (3 TC):** Route thực tế là `/admin/tours/schedules/edit/:id` (không phải `/admin/tours/:id/schedules/:schedule_id/edit`). Nút submit là **Chỉnh sửa** (`common:actions.edit`), **không** phải "Cập nhật". Trạng thái form: **Đang hoạt động** (`AVAILABLE`) / **Đã hủy** (`CANCELLED`) — **không** có "Tạm đóng/Closed". API: `GET/PUT/DELETE /admin/tour-schedules/:id`.

---

## 1. Phạm vi

| Hạng mục | Chi tiết |
|----------|----------|
| API detail | `GET /admin/tour-schedules/:id` |
| API update | `PUT /admin/tour-schedules/:id` |
| API delete | `DELETE /admin/tour-schedules/:id` |
| API tour info | `GET /admin/tours/:id` (TourInfoBox) |
| Redirect success | Mặc định → `/admin/tours/schedules?tour_id=`; từ Tour Edit (`fromTourEdit` state) → `/admin/tours/edit/:id` |
| Delete success | → `/admin/tours/schedules` |
| Quyền | Admin route guard |

---

## 2. Tổng quan trạng thái

| Nhóm | Tổng TC | ✅ Auto | ⏳ Backlog |
|------|---------|---------|------------|
| Page load & schedule info | 7 | 7 | 0 |
| Form, preview & stats | 6 | 6 | 0 |
| Validation | 3 | 3 | 0 |
| Submit, delete & navigation | 8 | 8 | 0 |
| Error / guard | 4 | 4 | 0 |
| **UI subtotal** | **28** | **28** | **0** |
| API smoke | 6 | 6 | 0 |
| **Tổng automation** | **34** | **34** | **0** |

---

## 2b. UI Inventory (PHASE 0.6 — audit 2026-06-15)

| # | Vùng UI | Nhãn (i18n) | Loại | Hành vi | TC | Trạng thái |
|---|---------|-------------|------|---------|-----|------------|
| 1 | Header | Chỉnh sửa | h1 | Title trang | SCHEDEDIT_004 | ✅ added |
| 2 | Breadcrumb | Lịch khởi hành › Chỉnh sửa | text | Ngữ cảnh (không link) | SCHEDEDIT_004 | ✅ added |
| 3 | TourInfoBox | Tên tour | card | `GET /admin/tours/:id` | SCHEDEDIT_006 | ✅ added |
| 4 | ScheduleInfoBox | Ngày, badge trạng thái, capacity | card | Hiển thị từ schedule | SCHEDEDIT_005 | ✅ added |
| 5 | Past warning | past_event_title | banner | `isPastSchedule` | SCHEDEDIT_024 | ✅ added |
| 6 | Form | Ngày KH / KT / slots / status | fields | Yup edit schema | SCHEDEDIT_001–003, 016–018 | ✅ added |
| 7 | Form | Vận hành (mã, điểm, deadline) | fields | Optional | SCHEDEDIT_012, 025 | ✅ added |
| 8 | Form | Giá NL/TE/EB | CurrencyInput | Optional override | — | manual-only (reuse Create) |
| 9 | Preview | Xem trước + price_override_help | panel | `useWatch` | SCHEDEDIT_009, 026 | ✅ added |
| 10 | Stats | THỐNG KÊ LỊCH | block | booked/available/max + bar | SCHEDEDIT_007, 008 | ✅ added |
| 11 | Header | Hủy | button | `navigate(-1)` | SCHEDEDIT_022 | ✅ added |
| 12 | Header | Chỉnh sửa | button | PUT update (desktop) | SCHEDEDIT_002, 003, 019 | ✅ added |
| 13 | Mobile bar | Hủy / Chỉnh sửa | fixed bottom | `md:hidden` | SCHEDEDIT_023 | ✅ added |
| 14 | Danger | Xóa lịch này | button | Mở dialog | SCHEDEDIT_013, 027 | ✅ added |
| 15 | Delete dialog | Hủy / Xóa lịch | modal | DELETE hoặc đóng | SCHEDEDIT_014, 015, 028 | ✅ added |
| 16 | Guard | UnsavedChangesGuard | modal | `isDirty` | SCHEDEDIT_022 | ✅ added |
| 17 | Loading | Spinner | placeholder | `isLoadingSchedule` | SCHEDEDIT_011 | ✅ added |
| 18 | Toast | Cập nhật / Xóa | sonner | mutation feedback | SCHEDEDIT_019, 020, 028 | ✅ added |
| 19 | Redirect | fromTourEdit | router | Tour Edit → quay lại edit | SCHEDEDIT_021 | ✅ added |

**Doc gốc thiếu:** 16/19 control — 3 TC ban đầu **lỗi thời** (route, nút "Cập nhật", status "Closed").

---

## 2c. TC tự sinh từ audit (PHASE 0.7)

| ID | Mô tả | Nguồn audit |
|----|-------|-------------|
| TC_AD_SCHEDEDIT_004 | Heading + breadcrumb | #1–2 |
| TC_AD_SCHEDEDIT_005 | ScheduleInfoBox capacity | #4 |
| TC_AD_SCHEDEDIT_006 | TourInfoBox tên tour | #3 |
| TC_AD_SCHEDEDIT_007 | ScheduleStatsBlock | #10 |
| TC_AD_SCHEDEDIT_008 | Notice khi có booking | #10 |
| TC_AD_SCHEDEDIT_009 | Preview + help notice | #9 |
| TC_AD_SCHEDEDIT_011 | Loading khi fetch schedule | #17 |
| TC_AD_SCHEDEDIT_012 | Trường vận hành | #7 |
| TC_AD_SCHEDEDIT_013–015 | Delete flow | #14–15 |
| TC_AD_SCHEDEDIT_016 | totalSlots < bookedSlots | #6 |
| TC_AD_SCHEDEDIT_017–018 | endDate / bookingDeadline | #6 |
| TC_AD_SCHEDEDIT_019–020 | Toast success / fail update | #18 |
| TC_AD_SCHEDEDIT_021 | Redirect fromTourEdit | #19 |
| TC_AD_SCHEDEDIT_022 | UnsavedChangesGuard | #16 |
| TC_AD_SCHEDEDIT_023 | Mobile action bar | #13 |
| TC_AD_SCHEDEDIT_024 | Past schedule warning | #5 |
| TC_AD_SCHEDEDIT_025 | PUT gửi operational fields | #7 |
| TC_AD_SCHEDEDIT_026 | Preview realtime | #9 |
| TC_AD_SCHEDEDIT_027 | Delete warning hint | #14 |
| TC_AD_SCHEDEDIT_028 | Delete fail toast | #18 |

---

## 3. Test cases (automation)

| TT | Test Case ID | Chức năng | Mô tả | Status |
| --- | --- | --- | --- | --- |
| 1 | TC_AD_SCHEDEDIT_001 | Tải form | Preload dữ liệu lịch lên form | ✅ |
| 2 | TC_AD_SCHEDEDIT_002 | Cập nhật slots | Tăng max_people → redirect list | ✅ |
| 3 | TC_AD_SCHEDEDIT_003 | Đóng bán | Chọn CANCELLED → PUT | ✅ |
| 4 | TC_AD_SCHEDEDIT_004 | Header | Heading + breadcrumb | ✅ |
| 5 | TC_AD_SCHEDEDIT_005 | ScheduleInfoBox | Capacity hiển thị | ✅ |
| 6 | TC_AD_SCHEDEDIT_006 | TourInfoBox | Tên tour | ✅ |
| 7 | TC_AD_SCHEDEDIT_007 | Stats | Thống kê lịch | ✅ |
| 8 | TC_AD_SCHEDEDIT_008 | Stats notice | Cảnh báo có booking | ✅ |
| 9 | TC_AD_SCHEDEDIT_009 | Preview | Panel + help | ✅ |
| 10 | TC_AD_SCHEDEDIT_011 | Loading | Spinner fetch schedule | ✅ |
| 11 | TC_AD_SCHEDEDIT_012 | Vận hành | Mã/điểm/deadline | ✅ |
| 12 | TC_AD_SCHEDEDIT_013 | Delete | Mở dialog | ✅ |
| 13 | TC_AD_SCHEDEDIT_014 | Delete cancel | Đóng không DELETE | ✅ |
| 14 | TC_AD_SCHEDEDIT_015 | Delete confirm | Xóa + redirect list | ✅ |
| 15 | TC_AD_SCHEDEDIT_016 | Validation | Slots < booked | ✅ |
| 16 | TC_AD_SCHEDEDIT_017 | Validation | end < start | ✅ |
| 17 | TC_AD_SCHEDEDIT_018 | Validation | deadline > start | ✅ |
| 18 | TC_AD_SCHEDEDIT_019 | Toast | Update success | ✅ |
| 19 | TC_AD_SCHEDEDIT_020 | Toast | Update fail | ✅ |
| 20 | TC_AD_SCHEDEDIT_021 | Navigation | fromTourEdit redirect | ✅ |
| 21 | TC_AD_SCHEDEDIT_022 | Guard | Unsaved changes | ✅ |
| 22 | TC_AD_SCHEDEDIT_023 | Mobile | Action bar | ✅ |
| 23 | TC_AD_SCHEDEDIT_024 | Past warning | Banner quá khứ | ✅ |
| 24 | TC_AD_SCHEDEDIT_025 | API body | Operational PUT | ✅ |
| 25 | TC_AD_SCHEDEDIT_026 | Preview | Cập nhật realtime | ✅ |
| 26 | TC_AD_SCHEDEDIT_027 | UX | Delete hint | ✅ |
| 27 | TC_AD_SCHEDEDIT_028 | Toast | Delete fail | ✅ |
| 28 | API_SCHEDEDIT_001 | API | GET 401 | ✅ |
| 29 | API_SCHEDEDIT_002 | API | GET detail admin | ✅ |
| 30 | API_SCHEDEDIT_003 | API | PUT 401 | ✅ |
| 31 | API_SCHEDEDIT_004 | API | PUT valid | ✅ |
| 32 | API_SCHEDEDIT_005 | API | PUT slots < booked | ✅ |
| 33 | API_SCHEDEDIT_006 | API | DELETE 401 | ✅ |

---

## Ghi chú

- Seed mock: schedule `id=99` (tour 1, 0 booked), `id=101` (10 booked / 30 max).
- Cancel dùng `navigate(-1)` — khác Create (fallback list).
