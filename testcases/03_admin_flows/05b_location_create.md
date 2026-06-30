# Admin — Thêm mới Địa điểm (Location Create)

**Route:** `/admin/locations/create`  
**Source:** `danangtrip-admin/src/pages/Locations/LocationCreate/index.tsx` + `LocationForm.tsx`  
**Automation:** `location-create.spec.ts` + `location-create-auth.spec.ts` + `admin-location-create.api.spec.ts` · POM: `LocationCreatePage.ts`

**Chạy:** `npm run test:admin:location-create` — **22 passed** (`--workers=1`)

> **Lưu ý:** Chỉ Admin. Form dùng `react-hook-form` + `createLocationSchema`. Submit header `form="location-form"`. Sau tạo thành công: **toast + reset form**, **giữ URL create** (không redirect list/edit). Upload thumbnail/gallery qua `POST /upload/image(s)` khi submit. Map: click map hoặc nút reset tâm Đà Nẵng để set tọa độ.

---

## 1. Phạm vi

| Hạng mục | Chi tiết |
|----------|----------|
| API create | `POST /admin/locations` |
| API meta | `GET /categories`, `GET /admin/locations/districts`, `GET /tags`, `GET /amenities` |
| Upload | `POST /upload/image`, `POST /upload/images` |
| Validation | `location.schema.ts` — name, slug, category, descriptions, address, district, lat/lng, thumbnail |
| Quyền | Admin route guard |

---

## 2. Tổng quan trạng thái

| Nhóm | Tổng TC | ✅ Auto | ⏳ Backlog |
|------|---------|---------|------------|
| Page load | 2 | 2 | 0 |
| Validation | 8 | 8 | 0 |
| Slug & map | 3 | 3 | 0 |
| Media | 2 | 2 | 0 |
| Success & navigation | 4 | 4 | 0 |
| Status sidebar | 2 | 2 | 0 |
| API error | 1 | 1 | 0 |
| Auth | 2 | 2 | 0 |
| **UI subtotal** | **24** | **24** | **0** |
| API smoke | 3 | 3 | 0 |
| **Tổng automation** | **27** | **27** | **0** |

---

## 2b. UI Inventory (PHASE 0.6)

| # | Vùng UI | Nhãn (i18n) | Loại | Hành vi | TC | Trạng thái |
|---|---------|-------------|------|---------|-----|------------|
| 1 | Header | Quay lại (ArrowLeft) | button | → list | LOCCREATE_022 | ✅ |
| 2 | Header | Hủy | button | → list | LOCCREATE_021 | ✅ |
| 3 | Header | Lưu địa điểm | button submit | POST create | LOCCREATE_020 | ✅ |
| 4 | Basic | Tên địa điểm | input | required min 3 | LOCCREATE_001–002 | ✅ |
| 5 | Basic | Slug + Tự động tạo | input + button | slugify | LOCCREATE_010 | ✅ |
| 6 | Basic | Danh mục | select | required | LOCCREATE_001 | ✅ |
| 7 | Basic | Mô tả ngắn / chi tiết | textarea + markdown | required | LOCCREATE_001, 003 | ✅ |
| 8 | Contact | Địa chỉ / Quận | input + select | required | LOCCREATE_001 | ✅ |
| 9 | Contact | Phone / Email / Website | input | email/url validate | LOCCREATE_004–005 | ✅ |
| 10 | Map | Leaflet map + reset pin | map + button | lat/lng required | LOCCREATE_012 | ✅ |
| 11 | Pricing | Giá min/max, mức giá, giờ mở cửa | inputs | max≥min | LOCCREATE_007 | ✅ |
| 12 | Tags | Tags / Amenities | TagSelector | optional | LOCCREATE_020 | ✅ |
| 13 | Media | Thumbnail / Gallery / Video | upload + input | thumbnail required | LOCCREATE_011, 006 | ✅ |
| 14 | Sidebar | % hoàn thành | progress | updates on fill | LOCCREATE_013 | ✅ |
| 15 | Sidebar | Trạng thái / Nổi bật | toggle | POST payload | LOCCREATE_023 | ✅ |
| 16 | Mobile | Submit / Hủy | buttons | same as header | — | covered via form id |

---

## 2c. Data Display Integrity (PHASE 0.7)

| # | Vùng UI | Field API | Field form | TC | Trạng thái |
|---|---------|-----------|------------|-----|------------|
| 1 | Category select | `category_id` + `category.name` | CustomSelect label | LOCCREATE_014 | ✅ |
| 2 | District select | `district` | CustomSelect | LOCCREATE_014 | ✅ |
| 3 | POST payload | snake_case body | form values | LOCCREATE_020 | ✅ |
| 4 | List after create | `name` | row text | LOCCREATE_020 | ✅ |

---

## 3. Test cases (automation)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_LOCCREATE_001 | Submit form trống → lỗi các trường bắt buộc | ✅ |
| TC_AD_LOCCREATE_002 | Tên < 3 ký tự → lỗi min length | ✅ |
| TC_AD_LOCCREATE_003 | Mô tả ngắn > 300 ký tự → lỗi max | ✅ |
| TC_AD_LOCCREATE_004 | Email không hợp lệ | ✅ |
| TC_AD_LOCCREATE_005 | Website URL không hợp lệ | ✅ |
| TC_AD_LOCCREATE_006 | Video URL không hợp lệ | ✅ |
| TC_AD_LOCCREATE_007 | price_max < price_min → lỗi max_gte_min | ✅ |
| TC_AD_LOCCREATE_010 | Nút Tự động tạo slug từ tên | ✅ |
| TC_AD_LOCCREATE_011 | Upload thumbnail hiện preview | ✅ |
| TC_AD_LOCCREATE_012 | Reset map pin → set lat/lng (pass validate map) | ✅ |
| TC_AD_LOCCREATE_013 | Sidebar completion % tăng khi điền field | ✅ |
| TC_AD_LOCCREATE_014 | Category + district options load từ API | ✅ |
| TC_AD_LOCCREATE_020 | Tạo thành công → toast + form reset + có trên list | ✅ |
| TC_AD_LOCCREATE_021 | Hủy → danh sách địa điểm | ✅ |
| TC_AD_LOCCREATE_022 | Nút back → danh sách địa điểm | ✅ |
| TC_AD_LOCCREATE_023 | Tạo inactive + featured trong POST body | ✅ |
| TC_AD_LOCCREATE_024 | API create lỗi → toast error, ở lại trang | ✅ |
| TC_AD_LOCCREATE_030 | Guest redirect login | ✅ |
| TC_AD_LOCCREATE_031 | Non-admin redirect login | ✅ |
| API_LOCCREATE_001 | POST create 401 unauthenticated | ✅ |
| API_LOCCREATE_002 | POST create 201 admin | ✅ |
| API_LOCCREATE_003 | POST create 422 duplicate slug | ✅ |

---

## 4. Test data đề xuất

* Tên mẫu: **Suối Hoa Đà Nắm** — slug `suoi-hoa-da-nam`
* Category mock: **Tham quan** (id=1)
* District: **Sơn Trà**
* Tọa độ: 16.0544, 108.2022 (tâm Đà Nẵng)
* Thumbnail: `tinyPngBuffer` (Playwright fixture)

**Mock flags:** `setLocationCreateFail`, `setLocationMutationFail` (create POST)

---

## 5. Checklist regression

* Validate client trước POST.
* Upload blob → URL thật trước khi gửi payload.
* Invalidate list/stats sau create.
* Cancel/back không gọi POST.
* Auth guard create route.

---

## 6. Ghi chú kỹ thuật

* POM scope `[data-location-field="…"]` cho lỗi validation.
* CustomSelect: click `-control` ancestor rồi chọn `option`.
* Map click flaky — ưu tiên nút reset tâm map (MapPin overlay).
* Doc cũ kỳ vọng redirect list sau save — **product redirect `/admin/locations/edit/:id` sau create thành công**.

---

## 7. Điều kiện trước (manual)

- Tài khoản Admin đã đăng nhập.
- Môi trường local: `http://localhost:5173`.

---

## 8. Đề xuất cải thiện (Improvement backlog — PHASE 0.8)

| ID | Loại | Ưu tiên | Tóm tắt | Trạng thái |
|----|------|---------|---------|------------|
| IMP_LOCCREATE_001 | UX | P2 | Sau create thành công redirect edit | **fixed** — `LocationCreate` + `extractCreatedLocationId` |
| IMP_LOCCREATE_002 | UI | P2 | Layout full-bleed | **fixed** — `w-full px-4 sm:px-6 lg:px-10` |
| IMP_LOCCREATE_003 | i18n | P3 | `price_level` hardcode | **fixed** — `priceLevels.*` + section Tags/Amenities |
| IMP_LOCCREATE_004 | A11y | P3 | Map reset title tiếng Anh only | **fixed** — `form.map.reset_center` aria-label |
| IMP_LOCCREATE_005 | Validation | P2 | `category_id` default 0 | **fixed** — null default + schema `.min(1)` |
| IMP_LOCCREATE_006 | UX | P3 | Lỗi thumbnail ngoài data-location-field | **fixed** — gom trong block + hiện lỗi `video_url` |

**Automation:** 22/22 passed (2026-06-18, sau product fix).
