# Admin — Chỉnh sửa Địa điểm (Location Edit)

**Route:** `/admin/locations/edit/:id`  
**Source:** `danangtrip-admin/src/pages/Locations/LocationEdit/index.tsx` + `LocationForm.tsx` (isEdit)  
**Automation:** `location-edit.spec.ts` + `location-edit-auth.spec.ts` + `admin-location-edit.api.spec.ts` · POM: `LocationEditPage.ts`

**Chạy:** `npm run test:admin:location-edit` (`--workers=1`)

> **Lưu ý:** Chỉ Admin (PrivateRoute). Form dùng chung `LocationForm` với create. Submit header `form="location-form"`. Sau cập nhật thành công: **toast + redirect `/admin/locations/detail/:id`**. Xóa địa điểm (admin): modal xác nhận → `DELETE` → list. PUT gửi **full payload** (không partial như Tour Edit).

---

## 1. Phạm vi

| Hạng mục | Chi tiết |
|----------|----------|
| API detail | `GET /admin/locations/:id` |
| API update | `PUT /admin/locations/:id` |
| API delete | `DELETE /admin/locations/:id` |
| API meta | categories, districts, tags, amenities (form) |
| Validation | `createLocationSchema` (dùng chung create/edit) |
| Quyền | Admin route guard; nút Xóa chỉ khi `role === admin` |

---

## 2. Tổng quan trạng thái

| Nhóm | Tổng TC | ✅ Auto | ⏳ Backlog |
|------|---------|---------|------------|
| Page load & preload | 4 | 4 | 0 |
| Update success | 3 | 3 | 0 |
| Validation | 3 | 3 | 0 |
| Navigation | 2 | 2 | 0 |
| Delete flow | 3 | 3 | 0 |
| Error states | 2 | 2 | 0 |
| Edit-specific UX | 2 | 2 | 0 |
| Auth | 2 | 2 | 0 |
| **UI subtotal** | **23** | **23** | **0** |
| API smoke | 3 | 3 | 0 |
| **Tổng automation** | **26** | **26** | **0** |

---

## 2b. UI Inventory (PHASE 0.6)

| # | Vùng UI | Nhãn (i18n) | Loại | Hành vi | TC | Trạng thái |
|---|---------|-------------|------|---------|-----|------------|
| 1 | Header | ArrowLeft back | button | → list | LOCEDIT_006 | ✅ |
| 2 | Header | Hủy | button | → list | LOCEDIT_007 | ✅ |
| 3 | Header | Xóa | button | mở modal (admin) | LOCEDIT_008–009 | ✅ |
| 4 | Header | Cập nhật địa điểm | submit | PUT + toast + detail | LOCEDIT_002–003 | ✅ |
| 5 | Header | Tên địa điểm (subtitle) | text | preload từ API | LOCEDIT_014 | ✅ |
| 6 | Form | Toàn bộ fields LocationForm | inputs | preload + validate | LOCEDIT_001 | ✅ |
| 7 | Basic | Slug + Tự động tạo | input + button | **không** auto slug khi edit | LOCEDIT_013 | ✅ |
| 8 | Sidebar | % hoàn thành | progress | cao khi đã load data | LOCEDIT_015 | ✅ |
| 9 | Sidebar | Trạng thái / Nổi bật | toggle | trong PUT body | LOCEDIT_012 | ✅ |
| 10 | Delete modal | Hủy / Xóa | buttons | cancel / DELETE | LOCEDIT_008–009 | ✅ |
| 11 | Not found | Return to List | button | GET 404 → UI lỗi | LOCEDIT_011 | ✅ |
| 12 | Mobile | Submit / Hủy | buttons | form id chung | — | covered via form |

---

## 2c. Data Display Integrity (PHASE 0.7)

| # | Vùng UI | Field API | Field form | TC | Trạng thái |
|---|---------|-----------|------------|-----|------------|
| 1 | Name / slug | `name`, `slug` | TextInput | LOCEDIT_001 | ✅ |
| 2 | Descriptions | `short_description`, `description` | textarea / markdown | LOCEDIT_001 | ✅ |
| 3 | Category | `category_id` + `category.name` | CustomSelect | LOCEDIT_001 | ✅ |
| 4 | Thumbnail | `thumbnail` | img preview | LOCEDIT_001 | ✅ |
| 5 | Opening hours legacy | `opening_hours[]` | multiline string | LOCEDIT_001b | ✅ |
| 6 | Coordinates | `latitude`, `longitude` | map display LAT/LNG | LOCEDIT_001 | ✅ |
| 7 | After update | `name` | detail header | LOCEDIT_002 | ✅ |

---

## 3. Test cases (automation)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_LOCEDIT_001 | Preload form đúng dữ liệu địa điểm từ GET detail | ✅ |
| TC_AD_LOCEDIT_001b | Legacy `opening_hours` array → hiển thị multiline trên form | ✅ |
| TC_AD_LOCEDIT_002 | Sửa mô tả chi tiết → PUT 200 + toast + redirect detail | ✅ |
| TC_AD_LOCEDIT_003 | Sửa tên → PUT body + mock dataset cập nhật | ✅ |
| TC_AD_LOCEDIT_004 | Submit với tên rỗng → lỗi validation | ✅ |
| TC_AD_LOCEDIT_005 | Email không hợp lệ → lỗi validation | ✅ |
| TC_AD_LOCEDIT_006 | Nút back → danh sách địa điểm | ✅ |
| TC_AD_LOCEDIT_007 | Hủy → danh sách địa điểm | ✅ |
| TC_AD_LOCEDIT_007b | Hủy mobile → danh sách địa điểm | ✅ |
| TC_AD_LOCEDIT_008 | Mở modal xóa → Hủy → không gọi DELETE | ✅ |
| TC_AD_LOCEDIT_009 | Xác nhận xóa → DELETE + redirect list | ✅ |
| TC_AD_LOCEDIT_009b | Mobile: nút Xóa mở modal xác nhận | ✅ |
| TC_AD_LOCEDIT_010 | PUT lỗi → toast error, ở lại trang edit | ✅ |
| TC_AD_LOCEDIT_011 | GET detail 404 → màn Not Found + Return to List | ✅ |
| TC_AD_LOCEDIT_012 | Toggle featured → gửi trong PUT body | ✅ |
| TC_AD_LOCEDIT_013 | Edit mode: đổi tên không tự đổi slug | ✅ |
| TC_AD_LOCEDIT_014 | Header hiển thị tên địa điểm subtitle | ✅ |
| TC_AD_LOCEDIT_015 | Sidebar completion ≥ 80% khi form đã load | ✅ |
| TC_AD_LOCEDIT_030 | Guest redirect login | ✅ |
| TC_AD_LOCEDIT_031 | Non-admin redirect login | ✅ |
| API_LOCEDIT_001 | GET detail 401 unauthenticated | ✅ |
| API_LOCEDIT_002 | PUT update 200 admin (khi API live) | ✅ |
| API_LOCEDIT_003 | GET detail 404 unknown id | ✅ |

---

## 4. Test data đề xuất

* ID mặc định: **101** — Bán đảo Sơn Trà  
* ID xóa: **104** — Ngũ Hành Sơn  
* ID not found: **9999**  
* Tên sau update: **Bán đảo Sơn Trà (đã cập nhật)**  
* Legacy opening hours: `['07:00 - 21:00', 'Cuối tuần: 08:00 - 22:00']`

**Mock flags:** `setLocationDetailFailForId`, `setLocationUpdateFail`, `patchMockLocation`, `setLocationDeleteFailForId`

---

## 5. Checklist regression

* GET detail trước khi render form (skeleton khi loading).
* PUT full payload + invalidate detail/list.
* Redirect detail sau update (không list).
* Delete chỉ admin; modal confirm trước DELETE.
* Auth guard edit route.
* Edit mode không auto-slug theo tên.

---

## 6. Ghi chú kỹ thuật

* POM kế thừa `LocationCreatePage` — scope `[data-location-field]`.
* Chờ form: `nameInput` visible hoặc Not Found heading.
* Assert redirect detail: `/admin/locations/detail/:id`.
* Mock cần handler `PUT /admin/locations/:id` (bổ sung trong `locations.mock.ts`).

---

## 7. Điều kiện trước (manual)

- Tài khoản Admin đã đăng nhập.
- Môi trường local: `http://localhost:5173`.

---

## 8. Đề xuất cải thiện (Improvement backlog — PHASE 0.8)

| ID | Loại | Ưu tiên | Tóm tắt | Trạng thái |
|----|------|---------|---------|------------|
| IMP_LOCEDIT_001 | UX | P2 | Màn 404 hardcode tiếng Anh | **fixed** — i18n `detail.not_found*` |
| IMP_LOCEDIT_002 | UI | P2 | Layout header `max-w-[1600px]` | **fixed** — full-bleed |
| IMP_LOCEDIT_003 | A11y | P3 | Nút back thiếu `aria-label` | **fixed** |
| IMP_LOCEDIT_004 | UX | P3 | PUT full payload | open — by design |
| IMP_LOCEDIT_005 | Code | P2 | Invalidate `detailRaw` sau PUT | **fixed** |
| IMP_LOCEDIT_006 | UX | P3 | Xóa không có trên mobile | **fixed** — sidebar mobile |
| IMP_LOCEDIT_007 | UX | P3 | Hủy mobile dùng `history.back` | **fixed** — `onCancel` → list |

**Automation:** 23/23 passed (2026-06-18, sau product fix).
