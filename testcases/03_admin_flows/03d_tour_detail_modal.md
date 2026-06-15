# Admin — Modal chi tiết tour (Tour Detail Modal)

**Route:** `/admin/tours/list` → nút **Xem/View**  
**Source:** `danangtrip-admin/src/pages/Tours/TourList/components/TourDetailModal.tsx`  
**Automation:** `tests/admin/tours-detail-modal.spec.ts` · POM: `TourDetailModalPage.ts`

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
| Open / close | 5 | 3 | 2 |
| Tour info & badges | 8 | 6 | 2 |
| Media & pricing | 5 | 5 | 0 |
| Description & itinerary | 5 | 5 | 0 |
| Schedules | 6 | 6 | 0 |
| Navigation | 1 | 1 | 0 |
| Responsive | 1 | 1 | 0 |
| Scope / UX polish | 4 | 0 | 4 |
| **UI subtotal** | **35** | **26** | **9** |
| API smoke | 2 | 0 | 2 |
| **Tổng** | **37** | **26** | **11** |

---

## 3. Open / close (P1)

| ID | Mô tả | Auto | Ghi chú |
|----|--------|------|---------|
| TC_AD_TMOD_001 | Mở modal, title tour | ✅ | |
| TC_AD_TMOD_002 | Đóng nút X, giữ filter list | ✅ | |
| TC_AD_TMOD_003 | Đóng nút Close footer | ✅ | |
| TC_AD_TMOD_028 | Đóng backdrop / phím ESC | ⏳ | Headless UI `onClose` |
| TC_AD_TMOD_030 | Schedules **không fetch** khi modal đóng | ⏳ | `enabled: isOpen` |

---

## 4. Tour info & badges (P1–P2)

| ID | Mô tả | Auto | Ghi chú |
|----|--------|------|---------|
| TC_AD_TMOD_004 | Status + booking availability badge | ✅ | Tour Lăng Bác sold_out |
| TC_AD_TMOD_005 | Mã tour pad 3 số | ✅ | TOUR-007 |
| TC_AD_TMOD_014 | Badge featured/hot | ✅ | |
| TC_AD_TMOD_026 | Badge `booking_availability: open` | ⏳ | 004 chỉ sold_out |
| TC_AD_TMOD_027 | Status `inactive` badge | ⏳ | |
| TC_AD_TMOD_031 | Schedule `full` → hiển thị Active (mapper) | ⏳ | Regression |
| TC_AD_TMOD_032 | Scope: `min_people` không hiển thị | ⏳ | Doc note |

---

## 5. Media & pricing (P1)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_TMOD_006 | Thumbnail aspect video | ✅ |
| TC_AD_TMOD_007 | Fallback không thumbnail (Tour Tam Kỳ) | ✅ |
| TC_AD_TMOD_008 | Gallery tối đa 4 ảnh (6 ảnh mock) | ✅ |
| TC_AD_TMOD_029 | Không có `images[]` → chỉ thumbnail | ⏳ |
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
| API_TMOD_001 | GET schedules không token → 401 | ⏳ |
| API_TMOD_002 | GET schedules `?tour_id=` → 200 | ⏳ |

---

## 10. Ghi chú kỹ thuật

- POM: `[id^="headlessui-dialog-panel"]` — không assert outer `[role=dialog]`.
- Itinerary: UI đọc `title` + `content`; mapper `normalizeItineraryRaw()`.
- EN retry: **Try again** · EN itinerary empty: **No schedule**.
- Schedule `full` API → mapper `AVAILABLE` → UI **Active**.

**Chạy:** `npm run test:admin:tour-detail-modal` (26 TC)
