# Admin — Thêm mới Tour (Create Tour Page)

**Route:** `/admin/tours/create`  
**Source:** `danangtrip-admin/src/pages/Tours/TourCreate/index.tsx`  
**Automation:** `tests/admin/tours-create.spec.ts` · POM: `TourCreatePage.ts`  
**Mock:** `tests/fixtures/api/tours.mock.ts`

---

## 1. Phạm vi

| Hạng mục | Chi tiết |
|----------|----------|
| API | `POST /admin/tours`, `POST /upload/image`, `POST /upload/images` |
| Sau tạo | Redirect `/admin/tours/edit/:id` + toast `create_success` |
| Submit | Header **Tạo tour** · sidebar **Lưu tour** |
| Slug | Auto từ tên (`slugifyVietnamese`), readOnly |
| Categories | `useTourCategoriesQuery()` public scope |

## 2. Tổng quan trạng thái

| Nhóm | Tổng TC | ✅ Auto | ⏳ Backlog |
|------|---------|---------|------------|
| Validation | 10 | 7 | 3 |
| Media & itinerary | 5 | 4 | 1 |
| Success & navigation | 4 | 4 | 0 |
| API error | 1 | 1 | 0 |
| Status & flags | 2 | 2 | 0 |
| UX polish | 8 | 0 | 8 |
| Auth | 2 | 0 | 2 |
| **UI subtotal** | **32** | **17** | **15** |
| API smoke | 4 | 0 | 4 |
| **Tổng** | **36** | **17** | **19** |

---

## 3. Validation (P1)

| ID | Mô tả | Auto | Ghi chú |
|----|--------|------|---------|
| TC_AD_TCREATE_001 | Form trống → lỗi schema + itinerary | ✅ | Không assert thumbnail DOM |
| TC_AD_TCREATE_007 | `available_to` < `available_from` | ✅ | `date_after` |
| TC_AD_TCREATE_011 | `short_desc` > 300 ký tự | ✅ | |
| TC_AD_TCREATE_012 | `max_people` < `min_people` | ✅ | |
| TC_AD_TCREATE_013 | `video_url` không hợp lệ | ✅ | Lỗi đỏ gallery |
| TC_AD_TCREATE_018 | Tên tour < 3 ký tự | ⏳ | `name.min(3)` |
| TC_AD_TCREATE_020 | `discount_percent` > 100 hoặc < 0 | ⏳ | |
| TC_AD_TCREATE_024 | `price_child` / `price_infant` âm | ⏳ | |
| TC_AD_TCREATE_025 | `min_people` ≤ 0 | ⏳ | |
| TC_AD_TCREATE_029 | Thumbnail required — assert DOM (regression UI gap) | ⏳ | Product: chưa có DOM error |

---

## 4. Media & itinerary (P1)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_TCREATE_002 | Upload thumbnail + gallery; xóa ảnh gallery | ✅ |
| TC_AD_TCREATE_003 | Itinerary thêm ngày | ✅ |
| TC_AD_TCREATE_008 | Xóa ngày itinerary | ✅ |
| TC_AD_TCREATE_015 | Xóa / thay thumbnail cover | ✅ |
| TC_AD_TCREATE_026 | Inclusions/exclusions trong sidebar checklist | ⏳ |

---

## 5. Success & navigation (P1)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_TCREATE_004 | Tạo tour → toast + edit page + list | ✅ |
| TC_AD_TCREATE_005 | Cancel → tour list | ✅ |
| TC_AD_TCREATE_016 | Submit qua sidebar Save Tour | ✅ |
| TC_AD_TCREATE_017 | Breadcrumb + schedule guide → list | ✅ |

---

## 6. Status, flags & slug (P1–P2)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_TCREATE_009 | Tạo tour status Hidden (`inactive`) | ✅ |
| TC_AD_TCREATE_014 | Featured + Hot trong POST payload | ✅ |
| TC_AD_TCREATE_010 | Slug tự sinh từ tên | ✅ |

---

## 7. API error (P1)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_TCREATE_006 | API create lỗi + dismiss alert | ✅ |

---

## 8. UX polish (P2–P3)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_TCREATE_019 | Giá sau giảm cập nhật realtime | ⏳ |
| TC_AD_TCREATE_021 | Category API lỗi → banner + Retry | ⏳ |
| TC_AD_TCREATE_022 | Category loading state | ⏳ |
| TC_AD_TCREATE_023 | Sidebar checklist % hoàn thành | ⏳ |
| TC_AD_TCREATE_027 | Sticky header thu gọn khi scroll | ⏳ |
| TC_AD_TCREATE_028 | Submit disabled + spinner khi `busy` | ⏳ |

---

## 9. Auth (P0)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_TCREATE_030 | Guest → `/login` | ⏳ |
| TC_AD_TCREATE_031 | User `role=user` → `/login` | ⏳ |

---

## 10. API smoke (P1–P2)

| ID | Mô tả | Auto |
|----|--------|------|
| API_TCREATE_001 | POST không token → 401 | ⏳ |
| API_TCREATE_002 | POST payload hợp lệ → 201 | ⏳ |
| API_TCREATE_003 | POST validation 422 | ⏳ |
| API_TCREATE_004 | Upload image auth | ⏳ |

---

## 11. Ghi chú kỹ thuật

- `meeting_point` **không** required.
- `prepareValidSubmit()` = `fillForm(validCreateTour)` + upload PNG 1×1.
- Category: react-select `[class*="-control"]`.
- Breadcrumb: scope `main` — tránh strict sidebar.
- Bug đã fix: `extractCreatedTourId`, `onPublish` tôn trọng status Hidden, `ImageGallery` hiện lỗi `video_url`.

**Chạy:** `npm run test:admin:tour-create` (17 TC)
