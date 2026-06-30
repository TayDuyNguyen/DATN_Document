# Admin — Chi tiết Địa điểm (Location Detail)

**Route:** `/admin/locations/detail/:id`  
**Source:** `danangtrip-admin/src/pages/Locations/LocationDetail/index.tsx` + components con  
**Automation:** `location-detail.spec.ts` + `location-detail-auth.spec.ts` + `admin-location-detail.api.spec.ts` · POM: `LocationDetailPage.ts`

**Chạy:** `npm run test:admin:location-detail` (`--workers=1`)

> **Lưu ý:** Chỉ Admin (`PrivateRoute`). Sidebar quản trị (status/featured/delete) chỉ render khi `user.role === 'admin'`. Reviews dùng API public: `GET /locations/:id/ratings` + `GET /locations/:id/rating-stats`.

---

## 1. Phạm vi

| Hạng mục | Chi tiết |
|----------|----------|
| API detail | `GET /admin/locations/:id` |
| API reviews | `GET /locations/:id/ratings`, `GET /locations/:id/rating-stats` |
| API status | `PATCH /admin/locations/:id/status` (bulk action sidebar) |
| API featured | `PATCH /admin/locations/:id/featured` |
| API delete | `DELETE /admin/locations/:id` |
| Quyền | Admin route guard; management chỉ admin |

---

## 2. Tổng quan trạng thái

| Nhóm | Tổng TC | ✅ Auto | ⏳ Backlog |
|------|---------|---------|------------|
| Load & display | 5 | 5 | 0 |
| Tabs (info/reviews/map) | 4 | 4 | 0 |
| Navigation | 2 | 2 | 0 |
| Admin management | 5 | 5 | 0 |
| Error states | 4 | 4 | 0 |
| Auth | 2 | 2 | 0 |
| **UI subtotal** | **22** | **22** | **0** |
| API smoke | 3 | 3 | 0 |
| **Tổng automation** | **25** | **25** | **0** |

---

## 2b. UI Inventory (PHASE 0.6)

| # | Vùng UI | Nhãn (i18n) | Loại | Hành vi | TC | Trạng thái |
|---|---------|-------------|------|---------|-----|------------|
| 1 | Header | ArrowLeft back | button | → list | LOCDET_020 | ✅ |
| 2 | Header | Chỉnh sửa | button | → edit | LOCDET_021 | ✅ |
| 3 | Header | Xóa địa điểm | button | mở modal | LOCDET_033 | ✅ |
| 4 | Hero | Thumbnail / fallback | media | ảnh hoặc no_images | LOCDET_004–004b | ✅ |
| 5 | Tabs | Thông tin chi tiết | button | tab info default | LOCDET_002 | ✅ |
| 6 | Tabs | Đánh giá của khách | button | load ratings API | LOCDET_011–012 | ✅ |
| 7 | Tabs | Vị trí & Bản đồ | button | map iframe / fallback | LOCDET_013–014 | ✅ |
| 8 | Sidebar | Lượt xem / Yêu thích | StatCard | formatMetric K/M | LOCDET_003 | ✅ |
| 9 | Management | Trạng thái hiển thị | CustomSelect | PATCH status | LOCDET_031, 042 | ✅ |
| 10 | Management | Nổi bật | ToggleSwitch | PATCH featured | LOCDET_032, 041 | ✅ |
| 11 | Danger zone | Xóa địa điểm | button | DELETE + list | LOCDET_034 | ✅ |
| 12 | Error | Thử lại / Đóng | buttons | refetch / list | LOCDET_040, 043 | ✅ |
| 13 | Loading | LocationDetailSkeleton | skeleton | delay GET detail | LOCDET_005 | ✅ |

---

## 2c. Data Display Integrity (PHASE 0.7)

| # | Vùng UI | Field API | Hiển thị | TC | Trạng thái |
|---|---------|-----------|----------|-----|------------|
| 1 | Header h1 | `name` | page title | LOCDET_001 | ✅ |
| 2 | Hero | `thumbnail`, `category`, `district` | badge + district | LOCDET_001, 004 | ✅ |
| 3 | Stats | `view_count`, `favorite_count` | 48.2K / 3.2K | LOCDET_003 | ✅ |
| 4 | Info tab | `description`, `address` | prose + contact | LOCDET_002 | ✅ |
| 5 | Reviews | ratings API `comment`, `user.full_name` | review cards | LOCDET_011 | ✅ |
| 6 | Map | `latitude`, `longitude` | coords + iframe | LOCDET_013 | ✅ |

---

## 3. Test cases (automation)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_LOCDET_001 | Load header, hero, tabs, sidebar stats | ✅ |
| TC_AD_LOCDET_002 | Tab info mặc định: mô tả + liên hệ | ✅ |
| TC_AD_LOCDET_003 | Format view/favorite (48.2K, 3.2K) | ✅ |
| TC_AD_LOCDET_004 | Hero hiển thị thumbnail | ✅ |
| TC_AD_LOCDET_004b | Hero fallback khi không có ảnh | ✅ |
| TC_AD_LOCDET_005 | Skeleton khi GET detail delay | ✅ |
| TC_AD_LOCDET_011 | Tab reviews có dữ liệu mock | ✅ |
| TC_AD_LOCDET_012 | Tab reviews empty (id 103) | ✅ |
| TC_AD_LOCDET_013 | Tab map: tọa độ + iframe + chỉ đường | ✅ |
| TC_AD_LOCDET_014 | Tab map fallback khi thiếu tọa độ | ✅ |
| TC_AD_LOCDET_020 | Nút back → danh sách | ✅ |
| TC_AD_LOCDET_021 | Nút Chỉnh sửa → edit | ✅ |
| TC_AD_LOCDET_030 | Admin thấy management + danger zone | ✅ |
| TC_AD_LOCDET_031 | Đổi status inactive → PATCH | ✅ |
| TC_AD_LOCDET_032 | Toggle featured off → PATCH + toast | ✅ |
| TC_AD_LOCDET_033 | Modal xóa header → Hủy, không DELETE | ✅ |
| TC_AD_LOCDET_034 | Xóa từ danger zone → DELETE + list | ✅ |
| TC_AD_LOCDET_040 | GET 404 → ErrorWidget + Đóng → list | ✅ |
| TC_AD_LOCDET_041 | Featured PATCH lỗi → toast error | ✅ |
| TC_AD_LOCDET_042 | Status PATCH lỗi → toast error | ✅ |
| TC_AD_LOCDET_043 | Retry sau lỗi server tạm thời → reload detail | ✅ |
| TC_AD_LOCDET_044 | Reviews API lỗi → error + retry | ✅ |
| TC_AD_LOCDET_050 | Guest redirect login | ✅ |
| TC_AD_LOCDET_051 | Non-admin redirect login | ✅ |
| API_LOCDET_001 | GET detail 401 unauthenticated | ✅ |
| API_LOCDET_002 | GET detail 200 admin (khi API live) | ✅ |
| API_LOCDET_003 | GET detail 404 unknown id | ✅ |

---

## 4. Test data đề xuất

* ID mặc định: **101** — Bán đảo Sơn Trà (featured, view 48.2K, favorite 3.2K)  
* ID reviews empty: **103** — Bãi biển Mỹ Khê  
* ID xóa: **105** — Chùa Linh Ứng Bãi Bụt  
* ID not found: **9999**

**Mock flags:** `setLocationDetailFailForId`, `setLocationDetailDelay`, `setLocationRatingsFailForId`, `setLocationFeaturedFailForId`, `setLocationStatusFailForId`, `patchMockLocation`

---

## 5. Checklist regression

* Skeleton → content khi GET detail chậm.
* Tabs info/reviews/map không crash khi thiếu data.
* ErrorWidget Retry/Đóng hoạt động.
* Status/featured không cập nhật sai khi API lỗi.
* Delete modal confirm trước DELETE; redirect list sau xóa.
* Auth guard detail route (guest + non-admin).

---

## 6. Ghi chú kỹ thuật

* POM: `LocationDetailPage.ts` — copy i18n từ `public/lang/vi/location.json`.
* Chờ load: `h1` visible hoặc ErrorWidget hoặc skeleton.
* Reviews mock: handler `**/locations/*/ratings**` + `rating-stats` trong `locations.mock.ts`.
* **Không test** non-admin thấy management — `PrivateRoute` chặn toàn route.

---

## 7. Điều kiện trước (manual)

- Tài khoản Admin đã đăng nhập.
- Môi trường local: `http://localhost:5173`.

---

## 8. Đề xuất cải thiện (Improvement backlog — PHASE 0.8)

| ID | Loại | Ưu tiên | Tóm tắt | Trạng thái |
|----|------|---------|---------|------------|
| IMP_LOCDET_001 | A11y | P3 | Nút back chỉ có `title`, thiếu `aria-label` | **fixed** |
| IMP_LOCDET_002 | UX | P3 | ErrorWidget nút back dùng nhãn `Đóng` thay vì Quay lại danh sách | **fixed** — `backLabel` |
| IMP_LOCDET_003 | Error | P3 | Reviews API lỗi fallback empty thay vì error state | **fixed** |
| IMP_LOCDET_004 | UX | P3 | Header delete ẩn text trên mobile (`hidden sm:inline`) | **fixed** — `aria-label` |
| IMP_LOCDET_005 | Layout | P3 | Nút back `lg:-ml-12` bị sidebar che | **fixed** |
| IMP_LOCDET_006 | UX | P2 | 404/500 cùng một error UI | **fixed** |
| IMP_LOCDET_007 | Code | P2 | Trùng DeleteLocationModal header/sidebar | **fixed** |
| IMP_LOCDET_008 | UX | P3 | Toast bulk khi đổi status 1 record | **fixed** |
| IMP_LOCDET_009 | UX | P3 | Nút fullscreen hero không hoạt động | **fixed** — lightbox |

**Automation:** 27/27 passed (2026-06-18).
