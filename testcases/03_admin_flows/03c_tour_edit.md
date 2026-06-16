# Admin — Chỉnh sửa Tour (Edit Tour Page)

**Route:** `/admin/tours/edit/:id`  
**API:** `GET/PUT /api/v1/admin/tours/:id`, `PATCH .../status|featured|hot`, `DELETE .../:id`, `GET /admin/tour-schedules?tour_id=`, `DELETE /admin/tour-schedules/:id`  
**Source:** `danangtrip-admin/src/pages/Tours/TourEdit/index.tsx`  
**Automation:** ✅ `tours-edit.spec.ts` + `tours-edit-extended.spec.ts` + `admin-tours-edit.api.spec.ts` · POM `TourEditPage.ts` (extends `TourCreatePage`)

**Chạy:** `npm run test:admin:tour-edit` — **48 passed, 2 skipped** (`API_TEDIT_006`, `API_TEDIT_008` khi API thật chặn DELETE)

**Chia sẻ form với Create:** `TourCreate/components/*`, schema `createTourSchema`, `ImageGallery`, `ItineraryBuilder`, `SidebarCards`

---

## 1. Phạm vi

| Hạng mục | Chi tiết |
|----------|----------|
| Vai trò | **Admin** only (`PrivateRoute`) |
| Sau PUT thành công | Toast + redirect **`/admin/tours/list`** |
| Partial PUT | Chỉ gửi field `dirtyFields` |
| Không đổi gì + Save | Navigate list, **không** gọi API |
| Slug | Toggle auto/manual (khác Create — Create luôn auto) |
| Departures | Section riêng Edit: list schedules + manage/edit/delete |
| Danger zone | Xóa tour → `TourDeleteDialog` |
| Nút submit | **Lưu thay đổi** / Save changes (header + sidebar) |

## 2. Điều kiện tiên quyết

- Admin đã đăng nhập · dev server `:5173`
- Tour tồn tại trong mock/DB (`mockToursApi`, `initialMockTours`)
- Categories: `useTourCategoriesQuery('admin')` (khác Create dùng public scope)

## 3. Tổng quan trạng thái

| Nhóm | Tổng TC | ✅ Auto | ⏳ Backlog |
|------|---------|---------|------------|
| Load & navigation | 6 | 6 | 0 |
| Update core | 8 | 8 | 0 |
| Slug (Edit-only) | 3 | 3 | 0 |
| Validation parity Create | 6 | 6 | 0 |
| Sidebar / status / flags | 2 | 2 | 0 |
| Departures section | 6 | 6 | 0 |
| Danger zone delete | 2 | 2 | 0 |
| UX / responsive | 3 | 3 | 0 |
| Auth | 2 | 2 | 0 |
| **UI subtotal (doc)** | **38** | **38** | **0** |
| UI bổ sung (audit code) | 4 | 4 | 0 |
| API smoke | 8 | 8 | 0 |
| **Tổng automation** | **50** | **50** | **0** |

> **File cũ chỉ có 3 TC thủ công, sai route, nhắc FAQ không tồn tại, nút "Cập nhật" sai label.**

---

## 4. Test cases — Load & navigation (P0–P1)

| ID | Mô tả | Dữ liệu | Auto |
|----|--------|---------|------|
| TC_AD_TEDIT_001 | Preload form đúng tour (tên, giá, itinerary, ảnh) | Tour id=1 | ✅ |
| TC_AD_TEDIT_004 | Tour fetch lỗi → `ErrorWidget` + Retry | Mock 500 | ✅ |
| TC_AD_TEDIT_005 | Loading spinner khi `tourLoading` | Slow mock | ✅ |
| TC_AD_TEDIT_006 | Back (ArrowLeft) + Cancel → `/admin/tours/list` | — | ✅ |
| TC_AD_TEDIT_013 | Breadcrumb → tour list | — | ✅ |
| TC_AD_TEDIT_030 | Tour không tồn tại → 404 UI | id=9999 | ✅ |

---

## 5. Update core (P0–P1)

| ID | Mô tả | Dữ liệu | Auto |
|----|--------|---------|------|
| TC_AD_TEDIT_002 | Sửa tên + `price_adult` → PUT + toast + redirect list | Giá 600.000 | ✅ |
| TC_AD_TEDIT_007 | **Partial PUT** — chỉ gửi field đã dirty | Chỉ đổi tên | ✅ |
| TC_AD_TEDIT_008 | Save không đổi → list, không API | — | ✅ |
| TC_AD_TEDIT_009 | Toast `update_success` sau PUT | — | ✅ |
| TC_AD_TEDIT_010 | PUT API lỗi → toast error | Mock 422/500 | ✅ |
| TC_AD_TEDIT_012 | Submit qua sidebar **Lưu thay đổi** | — | ✅ |
| TC_AD_TEDIT_003 | Xóa ảnh gallery + upload ảnh mới → PUT | — | ✅ |
| TC_AD_TEDIT_031 | Busy state: nút Save disabled + spinner | — | ✅ |

---

## 6. Slug — chỉ Edit (P1)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_TEDIT_014 | Toggle slug auto / manual | ✅ |
| TC_AD_TEDIT_015 | Manual slug → cảnh báo `slug_warning` | ✅ |
| TC_AD_TEDIT_016 | Auto slug ON → đổi tên cập nhật slug | ✅ |

---

## 7. Validation (parity Create) (P1–P2)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_TEDIT_011 | `available_to` < `available_from` | ✅ |
| TC_AD_TEDIT_032 | `max_people` < `min_people` | ✅ |
| TC_AD_TEDIT_033 | `short_desc` > 300 ký tự | ✅ |
| TC_AD_TEDIT_034 | `video_url` không hợp lệ | ✅ |
| TC_AD_TEDIT_035 | Tên tour < 3 ký tự | ✅ |
| TC_AD_TEDIT_036 | Itinerary add/remove ngày | ✅ |

---

## 8. Sidebar / status / flags (P2)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_TEDIT_017 | Đổi status active ↔ inactive trong PUT | ✅ |
| TC_AD_TEDIT_018 | Toggle featured/hot + partial PUT | ✅ |

---

## 9. Departures — lịch khởi hành (P1)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_TEDIT_019 | Hiển thị danh sách lịch (date, slots, status) | Tour id=1 | ✅ |
| TC_AD_TEDIT_020 | Empty state `form.departures.empty` | Tour không schedule | ✅ |
| TC_AD_TEDIT_021 | Load schedules lỗi + Retry | Mock fail | ✅ |
| TC_AD_TEDIT_022 | Nút **Thêm lịch** / Add schedule → schedule create (`fromTourEdit`) | — | ✅ |
| TC_AD_TEDIT_023 | Edit schedule row → schedule edit | — | ✅ |
| TC_AD_TEDIT_024 | Delete schedule → `ScheduleDeleteDialog` + refetch | — | ✅ |

---

## 10. Danger zone (P1)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_TEDIT_025 | Mở `TourDeleteDialog` từ danger zone | — | ✅ |
| TC_AD_TEDIT_026 | Confirm delete → toast + redirect list | Tour id=12 | ✅ |

---

## 11. UX & responsive (P2)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_TEDIT_027 | Mobile: header Save ẩn — footer cố định **Lưu thay đổi** | viewport 375px | ✅ |
| TC_AD_TEDIT_028 | Category API lỗi → banner + Retry | — | ✅ |
| TC_AD_TEDIT_029 | `video_url` invalid → hiện lỗi trong ImageGallery | — | ✅ |

---

## 12. Auth (P0)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_TEDIT_037 | Guest → `/login` | ✅ |
| TC_AD_TEDIT_038 | User `role=user` → `/login` | ✅ |

---

## 13. API smoke (P1–P2)

| ID | Mô tả | Auto |
|----|--------|------|
| API_TEDIT_001 | GET detail không token → 401 | ✅ |
| API_TEDIT_002 | GET detail admin → 200 | ✅ |
| API_TEDIT_003 | PUT không token → 401 | ✅ |
| API_TEDIT_004 | PUT hợp lệ → 200 | ✅ |
| API_TEDIT_005 | PUT tour không tồn tại → 404/422 | ✅ |
| API_TEDIT_006 | DELETE tour → 200 / skip nếu API chặn | ✅ (skip) |
| API_TEDIT_007 | GET schedules `?tour_id=` → 200 | ✅ |
| API_TEDIT_008 | DELETE schedule → 200 / skip nếu 400 bookings | ✅ (skip) |

---

## 13b. UI bổ sung từ audit code (không có trong doc gốc)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_TEDIT_001b | Legacy itinerary `description` → map `content` | ✅ |
| TC_AD_TEDIT_039 | Link `form.schedule.info_link` → tour list | ✅ |
| TC_AD_TEDIT_040 | Hủy `TourDeleteDialog` không gọi DELETE | ✅ |
| TC_AD_TEDIT_041 | Hủy `ScheduleDeleteDialog` không gọi DELETE | ✅ |

---

## 14. Ghi chú doc vs code

| Sai trong doc cũ | Thực tế |
|------------------|---------|
| Route `/admin/tours/[id]/edit` | `/admin/tours/edit/:id` |
| Field FAQ | **Không có** |
| Nút "Cập nhật" | **Lưu thay đổi** |
| Staff access | Chỉ **admin** |
| Sau update → ở lại edit | Redirect **list** |
| Nút departures | **Thêm lịch** / Add schedule (không phải "Quản lý") |
| ImageGallery Edit | Đã truyền `errors` — TC_AD_TEDIT_029 |
| Mobile save | Footer cố định `md:hidden` + `UnsavedChangesGuard` + sticky collapse |
| Layout header | `w-full px-4 sm:px-6 lg:px-10` — không `max-w-[1600px]` (parity Create, MarkUp 2026-06-16) |
| Layout | Header `w-full px-4 sm:px-6 lg:px-10` — không `max-w-[1600px]` (parity Create) |
| Dialog xóa lịch EN | Title `Delete this schedule?` (không phải "departure") |

## 15. Coverage gián tiếp hiện có

- Create TC004/009/016 → vào edit sau tạo tour
- List TC012 → navigate edit
- Modal TC024 → edit từ modal
- Dashboard TC045 → edit từ top tours

**Khuyến nghị:** ~~Tạo `tours-edit.spec.ts` + `TourEditPage.ts`~~ **Đã xong** — reuse `TourCreatePage` fields; mock PUT partial + schedule DELETE trong `tours.mock.ts`.
