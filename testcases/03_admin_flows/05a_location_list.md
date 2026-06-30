# Admin — Danh sách Địa điểm (Location List)

**Route:** `/admin/locations`  
**Source:** `danangtrip-admin/src/pages/Locations/LocationList/index.tsx`  
**Automation:** `location-list.spec.ts` + `location-list-auth.spec.ts` + `admin-location-list.api.spec.ts` · POM: `LocationListPage.ts`

**Chạy:** `npm run test:admin:location-list` — **39 passed** (`--workers=1`)

> **Lưu ý:** Chỉ Admin. Tìm kiếm **live onChange** (không cần Enter). Filter category/district/price/status **auto-apply**. Reset filter có `aria-label` Đặt lại/Reset. Cột: Địa điểm (kèm category + thumbnail), Quận, Mức giá, Đánh giá, Trạng thái, Nổi bật (toggle), Thao tác. Nút **Xuất Excel** gọi `GET /admin/locations/export`.

---

## 1. Phạm vi

| Hạng mục | Chi tiết |
|----------|----------|
| API list | `GET /admin/locations` — `q`, `category_id`, `district`, `price_level`, `status`, pagination |
| API stats | `GET /admin/locations/stats` |
| API filter meta | `GET /categories`, `GET /admin/locations/districts` |
| API mutation | `DELETE /admin/locations/:id`, `PATCH .../featured`, `PATCH .../status`, bulk qua client |
| Quyền | Admin route guard |

---

## 2. Tổng quan trạng thái

| Nhóm | Tổng TC | ✅ Auto | ⏳ Backlog |
|------|---------|---------|------------|
| Page load & stats | 3 | 3 | 0 |
| Data display | 1 | 1 | 0 |
| Search | 2 | 2 | 0 |
| Filters | 6 | 6 | 0 |
| Pagination & refresh | 3 | 3 | 0 |
| Navigation | 4 | 4 | 0 |
| Delete | 3 | 3 | 0 |
| Featured toggle | 2 | 2 | 0 |
| Bulk actions | 5 | 5 | 0 |
| Export & error recovery | 3 | 3 | 0 |
| Empty & select all | 2 | 2 | 0 |
| Auth | 2 | 2 | 0 |
| **UI subtotal** | **36** | **36** | **0** |
| API smoke | 4 | 4 | 0 |
| **Tổng automation** | **40** | **40** | **0** |

---

## 2b. UI Inventory (PHASE 0.6)

| # | Vùng UI | Nhãn (i18n) | Loại | Hành vi | TC | Trạng thái |
|---|---------|-------------|------|---------|-----|------------|
| 1 | Header | Danh sách Địa điểm | h1 | Title | LOCLIST_001 | ✅ |
| 2 | Header | Xuất Excel | button | `GET /admin/locations/export` | LOCLIST_032–033 | ✅ |
| 3 | Header | Thêm mới | button | → `/admin/locations/create` | LOCLIST_018 | ✅ |
| 4 | Stats | Tổng / Hoạt động / Nổi bật / Lượt xem | cards | API stats | LOCLIST_002 | ✅ |
| 5 | Filter | Tìm theo tên… | input | `q` live | LOCLIST_004–005 | ✅ |
| 6 | Filter | Danh mục | select | `category_id` | LOCLIST_006 | ✅ |
| 7 | Filter | Quận/Huyện | select | `district` | LOCLIST_007 | ✅ |
| 8 | Filter | Mức giá | select | `price_level` 1–4 | LOCLIST_008 | ✅ |
| 9 | Filter | Trạng thái | select | `status` | LOCLIST_009–010 | ✅ |
| 10 | Filter | Reset (icon) | button | Clear all filters + aria-label | LOCLIST_011 | ✅ |
| 11 | Table | Refresh | icon button | refetch | LOCLIST_014 | ✅ |
| 12 | Table | Per page | select | `per_page` | LOCLIST_013 | ✅ |
| 13 | Table | Pagination | buttons | page change | LOCLIST_012 | ✅ |
| 14 | Row | Checkbox | input | bulk select | LOCLIST_024, 029 | ✅ |
| 15 | Row | Tên địa điểm | heading click | → detail | LOCLIST_017 | ✅ |
| 16 | Row | Nổi bật | toggle button | PATCH featured | LOCLIST_022–023 | ✅ |
| 17 | Row | Xem / Sửa / Xóa | icon buttons | navigate / modal | LOCLIST_015–016, 019–021 | ✅ |
| 18 | Bulk bar | Kích hoạt / Tạm dừng / Xóa | buttons | PATCH/DELETE batch | LOCLIST_025–027 | ✅ |
| 19 | Dialog | Xóa địa điểm / bulk | modal | confirm DELETE | LOCLIST_019–021, 027–027b | ✅ |
| 20 | Empty | Không có dữ liệu | text | API `[]` | LOCLIST_028 | ✅ |
| 21 | Error panel | List load failed | panel + Retry | refetch list | LOCLIST_034 | ✅ |

---

## 2c. Data Display Integrity (PHASE 0.7)

| # | Vùng UI | Field API | Field UI | TC | Trạng thái |
|---|---------|-----------|----------|-----|------------|
| 1 | Row name | `name` | h4 + click detail | LOCLIST_003 | ✅ |
| 2 | Category | `category.name` | badge under name | LOCLIST_003 | ✅ |
| 3 | District | `district` | Badge column | LOCLIST_003, 007 | ✅ |
| 4 | Price | `price_min`, `price_max` (VND) | Khoảng giá / Miễn phí / Chưa cập nhật | LOCLIST_003 | ✅ |
| 5 | Rating | `avg_rating`, `review_count` | star + count | LOCLIST_003 | ✅ |
| 6 | Status | `status` | Badge active/inactive | LOCLIST_003, 009–010 | ✅ |
| 7 | Stats | stats API | 4 StatCards | LOCLIST_002 | ✅ |

---

## 3. Test cases (automation)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_LOCLIST_001 | Heading, stats, filter, table (10 rows/page) | ✅ |
| TC_AD_LOCLIST_002 | Stats cards đúng số từ mock | ✅ |
| TC_AD_LOCLIST_003 | Tên + category + quận + rating + status từ API | ✅ |
| TC_AD_LOCLIST_004 | Search theo tên địa điểm | ✅ |
| TC_AD_LOCLIST_005 | Search không phân biệt hoa thường | ✅ |
| TC_AD_LOCLIST_006 | Filter danh mục (Ẩm thực) | ✅ |
| TC_AD_LOCLIST_007 | Filter quận Sơn Trà | ✅ |
| TC_AD_LOCLIST_008 | Filter mức giá miễn phí | ✅ |
| TC_AD_LOCLIST_009 | Filter trạng thái active | ✅ |
| TC_AD_LOCLIST_010 | Filter trạng thái inactive | ✅ |
| TC_AD_LOCLIST_011 | Reset filter (icon) | ✅ |
| TC_AD_LOCLIST_012 | Pagination trang 2 | ✅ |
| TC_AD_LOCLIST_013 | Đổi per_page 20 | ✅ |
| TC_AD_LOCLIST_014 | Refresh refetch | ✅ |
| TC_AD_LOCLIST_015 | Eye → location detail | ✅ |
| TC_AD_LOCLIST_016 | Edit → location edit | ✅ |
| TC_AD_LOCLIST_017 | Click tên → detail | ✅ |
| TC_AD_LOCLIST_018 | Thêm mới → create | ✅ |
| TC_AD_LOCLIST_019 | Xóa địa điểm + confirm dialog | ✅ |
| TC_AD_LOCLIST_020 | Hủy dialog xóa — không gọi API | ✅ |
| TC_AD_LOCLIST_021 | Toast lỗi khi xóa fail (422 tour link) | ✅ |
| TC_AD_LOCLIST_022 | Toggle nổi bật PATCH featured | ✅ |
| TC_AD_LOCLIST_023 | Toast lỗi khi toggle featured fail | ✅ |
| TC_AD_LOCLIST_024 | Chọn dòng → bulk toolbar | ✅ |
| TC_AD_LOCLIST_025 | Bulk kích hoạt | ✅ |
| TC_AD_LOCLIST_026 | Bulk tạm dừng | ✅ |
| TC_AD_LOCLIST_027 | Bulk xóa sau confirm dialog | ✅ |
| TC_AD_LOCLIST_027b | Hủy bulk delete dialog — không gọi API | ✅ |
| TC_AD_LOCLIST_028 | Empty state khi list rỗng | ✅ |
| TC_AD_LOCLIST_029 | Chọn tất cả trên trang | ✅ |
| TC_AD_LOCLIST_032 | Xuất Excel tải file .xlsx | ✅ |
| TC_AD_LOCLIST_033 | Toast lỗi khi export fail | ✅ |
| TC_AD_LOCLIST_034 | Error panel + Retry khi list API lỗi | ✅ |
| TC_AD_LOCLIST_030 | Guest redirect login | ✅ |
| TC_AD_LOCLIST_031 | Non-admin redirect login | ✅ |
| API_LOCLIST_001 | GET list 401 unauthenticated | ✅ |
| API_LOCLIST_002 | GET list paginated admin | ✅ |
| API_LOCLIST_003 | GET list filter status | ✅ |
| API_LOCLIST_004 | GET stats | ✅ |

---

## 4. Test data đề xuất

* Primary: **Bán đảo Sơn Trà** (`id=101`) — search, display, navigation.
* Deletable: **Đèo Hải Vân** (`id=115`).
* Featured toggle: **Bãi biển Mỹ Khê** (`id=103`).
* Bulk inactive: **Công viên APEC** (`id=112`), **Hồ Hòa Trung** (`id=113`).
* Categories mock: Tham quan, Ẩm thực, Vui chơi giải trí.
* Districts: Sơn Trà, Ngũ Hành Sơn, Hải Châu, Thanh Khê, Liên Chiểu.

**Mock flags:** `setLocationListFail`, `setLocationListEmpty`, `setLocationExportFail`, `setLocationDeleteFailForId`, `setLocationFeaturedFailForId`, `setLocationMutationFail`

---

## 5. Checklist regression

* Chỉ admin vào được route.
* Search/filter cập nhật bảng đúng param API.
* Xóa có dialog xác nhận; lỗi 422 hiện toast.
* Toggle featured / bulk status invalidate list.
* Pagination + per_page đồng bộ URL query (client state).
* Empty state có copy — không skeleton vô hạn.

---

## 6. Ghi chú kỹ thuật

* Doc gốc mô tả cột cũ (Mô tả ngắn, Hình ảnh riêng) — UI hiện gộp vào cột **Địa điểm**.
* `price_level` API gửi số 1–4; UI map qua `normalizePriceLevelKey`.
* POM scope `tableCard` cho bulk/pagination — tránh trùng nút Xóa dialog.
* Screenshot UI (tùy chọn): `reports/ui-screenshots/location-list/<TC_ID>.png`.

---

## 7. Điều kiện trước (manual)

- Tài khoản Admin/Staff đã đăng nhập.
- Môi trường local: `http://localhost:5173`.

---

## 8. Đề xuất cải thiện (Improvement backlog — PHASE 0.8)

> Chi tiết + ID: `memory_test.md` mục 11 (Location List).

| ID | Loại | Ưu tiên | Tóm tắt | Trạng thái |
|----|------|---------|---------|------------|
| IMP_LOCLIST_001 | Function | P1 | Nút **Xuất Excel** — `GET /admin/locations/export` | **fixed** |
| IMP_LOCLIST_002 | UX | P2 | Reset filter có `aria-label` + `title` | **fixed** |
| IMP_LOCLIST_003 | UI | P2 | Layout full-bleed `w-full px-4 sm:px-6 lg:px-10` | **fixed** |
| IMP_LOCLIST_004 | UX | P2 | Bulk xóa có confirm dialog | **fixed** |
| IMP_LOCLIST_005 | UX | P2 | List API lỗi — error panel + retry | **fixed** |

**Đã đóng backlog IMP_LOCLIST_001–005** (2026-06-18). Automation: LOCLIST_027/027b, 032–034.
