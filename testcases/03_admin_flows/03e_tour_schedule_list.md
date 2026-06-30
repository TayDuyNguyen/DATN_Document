# Admin — Danh sách Lịch khởi hành (Tour Schedule List)

**Route:** `/admin/tours/schedules` (query `?tour_id=` tùy chọn)  
**Source:** `danangtrip-admin/src/pages/Tours/TourSchedules/index.tsx`  
**Automation:** `tests/admin/tour-schedule-list.spec.ts` + `tour-schedule-list-extended.spec.ts` + `tests/api/admin-tour-schedule-list.api.spec.ts` · POM: `TourScheduleListPage.ts`

**Chạy:** `npm run test:admin:tour-schedule-list` — **35 passed, 1 skipped** (`--workers=1`)

> **Lưu ý doc gốc (3 TC):** Route thực tế là `/admin/tours/schedules` (không phải `/admin/tours/[id]/schedules`). UI **không có tab** Calendar/List — **calendar + bảng + filter** hiển thị **cùng lúc** trên một trang.

---

## 1. Phạm vi

| Hạng mục | Chi tiết |
|----------|----------|
| API list | `GET /admin/tour-schedules` — filter `tour_id`, `q`, `status`, `from`, `to`, sort, pagination |
| API stats | `GET /admin/tour-schedules/status-counts` |
| API mutation | `PATCH /admin/tour-schedules/:id/status`, `DELETE /admin/tour-schedules/:id` |
| Quyền | Admin route guard |

---

## 2. Tổng quan trạng thái

| Nhóm | Tổng TC | ✅ Auto | ⏳ Backlog |
|------|---------|---------|------------|
| Page load & stats | 3 | 3 | 0 |
| Data display | 4 | 4 | 0 |
| Calendar | 3 | 3 | 0 |
| Filters | 6 | 6 | 0 |
| Table actions | 7 | 7 | 0 |
| Bulk & status | 4 | 4 | 0 |
| Empty / error | 2 | 2 | 0 |
| Navigation | 2 | 2 | 0 |
| **UI subtotal** | **31** | **31** | **0** |
| API smoke | 7 | 7 | 0 |
| **Tổng automation** | **38** | **38** | **0** |

---

## 2b. UI Inventory (PHASE 0.6 — audit 2026-06-16)

| # | Vùng UI | Nhãn (i18n) | Loại | Hành vi | TC | Trạng thái |
|---|---------|-------------|------|---------|-----|------------|
| 1 | Header | Lịch khởi hành | h1 | Hiển thị title | SCHEDLIST_001 | ✅ covered |
| 2 | Breadcrumb | Quản lý Tour | link | → `/admin/tours/list` | SCHEDLIST_016 | ✅ added |
| 3 | Stats | Tổng lịch / Còn chỗ / Đầy chỗ / Đã hủy | cards | Số từ API stats | SCHEDLIST_002 | ✅ added |
| 4 | Calendar | Tháng N, YYYY | heading | Hiển thị tháng hiện tại | SCHEDLIST_004 | ✅ added |
| 5 | Calendar | Prev / Next month | button | Đổi tháng | SCHEDLIST_004 | ✅ added |
| 6 | Calendar | Ô ngày | cell click | Filter `start_date` + `end_date` | SCHEDLIST_005 | ✅ added |
| 7 | Calendar | Đặt lại (khi chọn ngày) | button | Clear date filter | SCHEDLIST_022 | ✅ added |
| 8 | Filter | Tìm theo tên tour | input debounce | `q` param — **không phân biệt hoa thường** (PostgreSQL `ilike`) | SCHEDLIST_006, 031 | ✅ added |
| 9 | Filter | Tất cả tour | select | `tour_id` | SCHEDLIST_007 | ✅ added |
| 10 | Filter | Trạng thái | select | `status` | SCHEDLIST_008 | ✅ added |
| 11 | Filter | Từ ngày / Đến ngày | date input | `from` / `to` | SCHEDLIST_020 | ✅ added |
| 12 | Filter | Lọc | button | Apply date range | SCHEDLIST_020 | ✅ added |
| 13 | Filter | Đặt lại | button | Reset all filters | SCHEDLIST_021 | ✅ added |
| 14 | Table | Chọn tất cả | checkbox | Bulk toolbar | SCHEDLIST_024 | ✅ added |
| 15 | Table | Sort Ngày KH | button | Toggle asc/desc | SCHEDLIST_019 | ✅ added |
| 16 | Table | Per page | select | `per_page` | SCHEDLIST_028 | ✅ added |
| 17 | Table row | Tour name | button | Lọc theo `tour_id` (cùng trang) | SCHEDLIST_013 | ✅ covered |
| 18 | Table row | Status dropdown | select / badge | AVAILABLE/CANCELLED dropdown; FULL → badge read-only **Đầy chỗ** | SCHEDLIST_017, 027 | ✅ covered |
| 19 | Table row | + Thêm lịch | icon button | → create | SCHEDLIST_012 | ✅ added |
| 20 | Table row | Chỉnh sửa | icon button | → edit | SCHEDLIST_011 | ✅ added |
| 21 | Table row | Xóa | icon button | Open delete dialog; **disabled** khi `bookedSlots > 0` | SCHEDLIST_009, 030 | ✅ covered |
| 22 | Bulk toolbar | Kích hoạt lịch | button | bulk PATCH available | SCHEDLIST_026 | ✅ covered |
| 23 | Bulk toolbar | Hủy lịch | button | bulk PATCH cancelled | SCHEDLIST_025 | ✅ added |
| 24 | Delete dialog | Hủy / Xóa lịch | buttons | Cancel / DELETE | SCHEDLIST_010, 009 | ✅ added |
| 25 | Empty | Không có lịch khởi hành | text | API `[]` | SCHEDLIST_014 | ✅ added |
| 26 | Error | Không tải được dữ liệu | EmptyState + **Thử lại** | API 5xx → `refetch()` | SCHEDLIST_015 | ✅ covered |
| 27 | Data | Đặt/Tối đa, Hết chỗ/Còn chỗ | text/badge | mapper + seed | SCHEDLIST_003, 017, 018 | ✅ added |
| 28 | Data | Theo tour (giá) | text | `price_adult` null | SCHEDLIST_029 | ✅ added |
| 29 | URL | `?tour_id=` `?q=` `?status=` `?from=` `?to=` | query | Sync filter ↔ URL | SCHEDLIST_023 | ✅ covered |
| 30 | Calendar | `booked/max` hoặc `N lịch` | label | Dưới dot màu mỗi ngày | — | product-only |

**Doc gốc thiếu (đã bổ sung):** 26/29 control — chỉ 3 TC ban đầu (tab calendar/list/delete) **lỗi thời** so với implementation.

---

## 2c. Data Display Integrity (PHASE 0.7)

| # | Vùng UI | Field API | Field UI | TC | Trạng thái |
|---|---------|-----------|----------|-----|------------|
| 1 | Row tour | `tour.name` (nested) | tour name button | SCHEDLIST_003 | ✅ |
| 2 | Row capacity | `booked_people` / `max_people` | `10 / 30` text | SCHEDLIST_003 | ✅ |
| 3 | Booking badge | `booking_availability` | Còn chỗ / Hết chỗ | SCHEDLIST_017, 018 | ✅ |
| 4 | Status `full` | `status=full` | badge **Đầy chỗ** (cột status) + Hết chỗ (availability) | SCHEDLIST_017 | ✅ |
| 5 | Stats cards | `status-counts` API | 4 số thống kê | SCHEDLIST_002 | ✅ |
| 6 | Calendar labels | schedules in month | dot + `booked/max` hoặc `N lịch` | — | product-only |

---

## 3. Test cases (automation)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_SCHEDLIST_001 | Heading, stats, calendar, filter, table | ✅ |
| TC_AD_SCHEDLIST_002 | Stats cards đúng số từ mock | ✅ |
| TC_AD_SCHEDLIST_003 | Tour name + capacity text từ API | ✅ |
| TC_AD_SCHEDLIST_004 | Calendar prev/next month | ✅ |
| TC_AD_SCHEDLIST_005 | Click ngày calendar → filter bảng | ✅ |
| TC_AD_SCHEDLIST_006 | Search theo tên tour | ✅ |
| TC_AD_SCHEDLIST_031 | Search không phân biệt hoa thường (`ba na` / `BA NA`) | ✅ |
| TC_AD_SCHEDLIST_007 | Filter dropdown tour | ✅ |
| TC_AD_SCHEDLIST_008 | Filter status cancelled | ✅ |
| TC_AD_SCHEDLIST_009 | Xóa lịch — confirm dialog | ✅ |
| TC_AD_SCHEDLIST_010 | Hủy dialog — không DELETE | ✅ |
| TC_AD_SCHEDLIST_011 | Edit → `/admin/tours/schedules/edit/:id` | ✅ |
| TC_AD_SCHEDLIST_012 | Add → `/admin/tours/:id/schedules/create` | ✅ |
| TC_AD_SCHEDLIST_013 | Click tên tour → lọc bảng theo `tour_id` + URL | ✅ |
| TC_AD_SCHEDLIST_014 | Empty state khi không có lịch | ✅ |
| TC_AD_SCHEDLIST_015 | Error state khi API list fail | ✅ |
| TC_AD_SCHEDLIST_016 | Breadcrumb → tour list | ✅ |
| TC_AD_SCHEDLIST_017 | Hàng full: badge Hết chỗ | ✅ |
| TC_AD_SCHEDLIST_018 | Hàng open: badge Còn chỗ | ✅ |
| TC_AD_SCHEDLIST_019 | Sort cột ngày khởi hành | ✅ |
| TC_AD_SCHEDLIST_020 | Filter khoảng ngày + Lọc | ✅ |
| TC_AD_SCHEDLIST_021 | Reset filter | ✅ |
| TC_AD_SCHEDLIST_022 | Calendar reset ngày đã chọn | ✅ |
| TC_AD_SCHEDLIST_023 | Mở với `?tour_id=1` | ✅ |
| TC_AD_SCHEDLIST_024 | Chọn tất cả + bulk toolbar | ✅ |
| TC_AD_SCHEDLIST_025 | Bulk hủy lịch (PATCH) | ✅ |
| TC_AD_SCHEDLIST_026 | Bulk còn chỗ (PATCH) | ✅ |
| TC_AD_SCHEDLIST_027 | Đổi status từng dòng | ✅ |
| TC_AD_SCHEDLIST_028 | Đổi per_page | ✅ |
| TC_AD_SCHEDLIST_029 | Giá “Theo tour” khi không override | ✅ |
| TC_AD_SCHEDLIST_030 | Nút Xóa disabled khi đã có booking | ✅ |
| API_SCHEDLIST_001 | 401 unauthenticated list | ✅ |
| API_SCHEDLIST_002 | 200 list admin | ✅ |
| API_SCHEDLIST_003 | Filter tour_id | ✅ |
| API_SCHEDLIST_004 | 401 unauthenticated stats | ✅ |
| API_SCHEDLIST_005 | 200 stats admin | ✅ |
| API_SCHEDLIST_006 | 403 customer token | ✅ |

---

## 4. Quy tắc kỹ thuật

- Mock schedule list: enrich `tour.name` từ `toursById` — không assert chỉ có row count.
- Row actions: `aria-label` + `title` — POM hỗ trợ cả hai; delete row `0/15` (schedule 99, `booked_people=0`) cho TC xóa.
- Bulk toolbar chỉ hiện khi `selectedIds.length > 0` — scope `.animate-in`; nhãn bulk activate **Kích hoạt lịch** / **Activate schedules**.
- `status=FULL` → cột status: badge read-only **Đầy chỗ** (không dropdown); cột availability: **Hết chỗ**.
- Filter sync URL: `tour_id`, `q`, `status`, `from`, `to`, `page`, `per_page`.
- Search `q`: lọc theo `tour.name` — **case-insensitive** trên PostgreSQL (`unaccent` + `ilike`), khớp mock Playwright (`toLowerCase()`).
- Error list: EmptyState + nút **Thử lại** gọi `refetch()`.
- Empty table: subtitle `schedules:no_data.description`.

---

## 5. Ghi chú doc gốc (deprecated)

| TC cũ | Thực tế |
|-------|---------|
| SCHEDLIST_001 tab Calendar | Calendar luôn hiển thị — không có tab |
| SCHEDLIST_002 tab List | Bảng luôn hiển thị bên dưới calendar |
| SCHEDLIST_003 xóa khi không có booking | UI chặn: `bookedSlots > 0` → nút Xóa disabled; TC_009 dùng row `0/15` |
