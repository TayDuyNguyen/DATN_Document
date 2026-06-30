# Admin — Modal chi tiết tour (Tour Detail Modal)

**Route:** `/admin/tours/list` → nút **Xem/View**  
**Source:** `danangtrip-admin/src/pages/Tours/TourList/components/TourDetailModal.tsx`  
**Automation:** `tests/admin/tours-detail-modal.spec.ts` + `tests/api/admin-tours-detail-modal.api.spec.ts` · POM: `TourDetailModalPage.ts`

**Chạy:** `npm run test:admin:tour-detail-modal` — **35 passed** (33 UI + 2 API, `--workers=1`)

---

## 1. Phạm vi

| Hạng mục | Chi tiết |
|----------|----------|
| Modal | Không có route riêng — mở từ Tour List |
| API schedules | `GET /admin/tour-schedules?tour_id=` — chỉ khi modal mở (`enabled: isOpen`) |
| Quyền | Admin route guard |
| Phạm vi hiển thị | **Không** có: short_desc, category, inclusions/exclusions, child/infant price, min_people, video_url, slug |

## 2. Tổng quan trạng thái

| Nhóm | Tổng TC | ✅ Auto | ⏳ Backlog |
|------|---------|---------|------------|
| Open / close | 5 | 5 | 0 |
| Tour info & badges | 8 | 8 | 0 |
| Media & pricing | 5 | 5 | 0 |
| Description & itinerary | 6 | 6 | 0 |
| Schedules | 6 | 6 | 0 |
| Navigation | 1 | 1 | 0 |
| Responsive | 1 | 1 | 0 |
| **UI subtotal** | **32** | **32** | **0** |
| UI bổ sung audit | 1 | 1 | 0 |
| API smoke | 2 | 2 | 0 |
| **Tổng automation** | **35** | **35** | **0** |

> Đếm doc gốc 37 TC gồm `017b` trong nhóm itinerary (6 dòng) — automation **35 test** cover đủ 37 ID (017 + 017b).

---

## 2b. UI Inventory (PHASE 0.6 — audit 2026-06-16)

| # | Vùng UI | Nhãn / control | Loại | TC | Trạng thái |
|---|---------|----------------|------|-----|------------|
| 1 | Header | Edit | button → navigate edit | TMOD_024 | ✅ |
| 2 | Header | Close (X) | button aria-label | TMOD_002 | ✅ |
| 3 | Footer | Close | button | TMOD_003 | ✅ |
| 4 | Overlay | ESC / backdrop | Headless UI onClose | TMOD_028 | ✅ |
| 5 | List trigger | View tour | mở modal | TMOD_001 | ✅ |
| 6 | Header meta | Status badge | span | TMOD_004, 027 | ✅ |
| 7 | Header meta | Booking availability | span | TMOD_004, 026 | ✅ |
| 8 | Header meta | Tour code TOUR-XXX | text | TMOD_005 | ✅ |
| 9 | Media | Thumbnail / fallback | img / ImageOff | TMOD_006, 007, 029 | ✅ |
| 10 | Media | Gallery grid (max 4) | img | TMOD_008, 029 | ✅ |
| 11 | Stats | Price + currency | text | TMOD_009, 010 | ✅ |
| 12 | Stats | Duration | text | TMOD_011 | ✅ |
| 13 | Stats | Max people | text | TMOD_012 | ✅ |
| 14 | Stats | Meeting point | truncate | TMOD_013 | ✅ |
| 15 | Stats | min_people | **không render** | TMOD_032 | ✅ |
| 16 | Tags | Featured / Hot | span | TMOD_014 | ✅ |
| 17 | Description | prose HTML / no_data | div | TMOD_015, 016 | ✅ |
| 18 | Itinerary | timeline / empty | headings + body | TMOD_017, 017b, 018 | ✅ |
| 19 | Schedules | loading / list / empty / error | ul + alert | TMOD_019–023 | ✅ |
| 20 | Schedules | Retry | button | TMOD_022, 023 | ✅ |
| 21 | Schedules | legacy `status=full` row | Full / Đầy chỗ label | TMOD_031 | ✅ |
| 22 | Fetch guard | schedules API | chỉ khi `isOpen` | TMOD_030 | ✅ |
| 23 | Responsive | mobile scroll body | scroll | TMOD_025 | ✅ |

---

## 3. Open / close (P1)

| ID | Mô tả | Auto | Ghi chú |
|----|--------|------|---------|
| TC_AD_TMOD_001 | Mở modal, title tour | ✅ | |
| TC_AD_TMOD_002 | Đóng nút X, giữ filter list | ✅ | |
| TC_AD_TMOD_003 | Đóng nút Close footer | ✅ | |
| TC_AD_TMOD_028 | Đóng backdrop / phím ESC | ✅ | `closeByEscape`, `closeByBackdrop` |
| TC_AD_TMOD_030 | Schedules **không fetch** khi modal đóng | ✅ | `enabled: isOpen` |

---

## 4. Tour info & badges (P1–P2)

| ID | Mô tả | Auto | Ghi chú |
|----|--------|------|---------|
| TC_AD_TMOD_004 | Status + booking availability badge | ✅ | Tour Lăng Bác sold_out |
| TC_AD_TMOD_005 | Mã tour pad 3 số | ✅ | TOUR-007 |
| TC_AD_TMOD_014 | Badge featured/hot | ✅ | |
| TC_AD_TMOD_026 | Badge `booking_availability: open` | ✅ | Còn chỗ / Open |
| TC_AD_TMOD_027 | Status `inactive` badge | ✅ | Tạm ẩn / Hidden |
| TC_AD_TMOD_031 | Schedule `full` → hiển thị **Đầy chỗ / Full** (mapper `FULL`) | ✅ | Regression |
| TC_AD_TMOD_032 | Scope: `min_people` không hiển thị | ✅ | |

---

## 5. Media & pricing (P1)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_TMOD_006 | Thumbnail aspect video | ✅ |
| TC_AD_TMOD_007 | Fallback không thumbnail (Tour Tam Kỳ) | ✅ |
| TC_AD_TMOD_008 | Gallery tối đa 4 ảnh (6 ảnh mock) | ✅ |
| TC_AD_TMOD_029 | Không có `images[]` → chỉ thumbnail | ✅ |
| TC_AD_TMOD_009 | Format giá + currency (Tour Huế 1.500.000) | ✅ |
| TC_AD_TMOD_010 | Giá = 0, không NaN (Tour dù lượn) | ✅ |

---

## 6. Description & itinerary (P1–P2)

| ID | Mô tả | Auto | Ghi chú |
|----|--------|------|---------|
| TC_AD_TMOD_011 | Duration / no_data | ✅ | |
| TC_AD_TMOD_012 | Max people + unit | ✅ | |
| TC_AD_TMOD_013 | Meeting point truncate | ✅ | class `truncate` |
| TC_AD_TMOD_015 | Description HTML (`.prose strong`) | ✅ | |
| TC_AD_TMOD_016 | Thiếu description → no_data | ✅ | |
| TC_AD_TMOD_017 | Itinerary timeline (form shape) | ✅ | `{day,title,content}` |
| TC_AD_TMOD_017b | Itinerary legacy DB shape | ✅ | `{time,title,description}` |
| TC_AD_TMOD_018 | Itinerary rỗng | ✅ | `no_schedule` |

---

## 7. Schedules preview (P1–P2)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_TMOD_019 | Loading schedules (`setScheduleDelay`) | ✅ |
| TC_AD_TMOD_020 | Schedules slots + status | ✅ |
| TC_AD_TMOD_021 | Schedules empty | ✅ |
| TC_AD_TMOD_022 | Schedules error + retry btn | ✅ |
| TC_AD_TMOD_023 | Retry sau lỗi | ✅ |

---

## 8. Navigation & responsive (P1–P2)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_TMOD_024 | Edit → `/admin/tours/edit/:id` | ✅ |
| TC_AD_TMOD_025 | Mobile 375px — scroll trong modal | ✅ |

---

## 9. API smoke (P2)

| ID | Mô tả | Auto |
|----|--------|------|
| API_TMOD_001 | GET schedules không token → 401 | ✅ |
| API_TMOD_002 | GET schedules `?tour_id=` → 200 | ✅ |

---

## 10. Ghi chú kỹ thuật

- POM: `TourListPage.detailModalPanel` (`[id^="headlessui-dialog-panel"]`) — không assert outer `[role=dialog]` khi transition.
- Itinerary list: UI đọc `title` + `content`; legacy patch qua `patchMockTour` + reload list.
- Schedule mapper: `status=full` → `normalizeStatus` → **FULL** → UI **Đầy chỗ / Full** (TMOD_031).
- EN retry: **Try again** · EN itinerary empty: **No schedule**.
- Mock: `setScheduleDelay`, `setScheduleEmptyForTour`, `setScheduleErrorForTour`, `releaseScheduleErrorForTour`, `patchMockTour`.

**Module đóng** — 2026-06-16.
