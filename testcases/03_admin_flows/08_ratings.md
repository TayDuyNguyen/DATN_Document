# Admin — Quản lý đánh giá (Ratings)

**Route:** `/admin/ratings`  
**Source:** `danangtrip-admin/src/pages/Ratings/`  
**Automation:** `tests/admin/ratings.spec.ts` · `tests/admin/ratings-auth.spec.ts` · `tests/api/admin-ratings.api.spec.ts`  
**POM:** `RatingsPage.ts` · Mock: `tests/fixtures/api/ratings.mock.ts` · Data: `ratings-list.data.ts`  
**Chạy test:** `npm run test:admin:ratings` (cần `npm run dev` admin tại `http://localhost:5173`)

---

## 1. Phạm vi

| Hạng mục | Chi tiết |
|----------|----------|
| Vai trò | **Admin** only (`PrivateRoute`) |
| API | `GET /admin/reports/ratings` · `GET /admin/ratings` · `PATCH .../mark-viewed` · `PATCH .../reject` · `DELETE .../:id` · `GET .../export` |
| UI | Stats 4 card · Filter bar · Table + checkbox bulk · Reject/Hide dialog · Delete modal |
| Hành vi thực tế | **Đánh dấu đã xem** (`mark-viewed`), **Ẩn** (`reject`), không có nút approve trên màn |

## 2. UI Interactive Inventory

| # | Vùng UI | Nhãn (i18n) | Loại | Hành vi kỳ vọng | TC | Auto |
|---|---------|-------------|------|-----------------|-----|------|
| 1 | Header | Xuất báo cáo Excel | button | Export theo filter (không gửi page/per_page) | TC_AD_RAT_028–029 | ✅ |
| 2 | Filter | Tìm theo tên khách hàng… | search | Debounce 300ms → API `search` | TC_AD_RAT_004 | ✅ |
| 3 | Filter | Tất cả dịch vụ / Tour / Địa điểm | select | API `type` | TC_AD_RAT_005 | ✅ |
| 4 | Filter | Tất cả trạng thái / Mới / Đã xem / Đã ẩn | select | API `is_new` + `status=rejected` | TC_AD_RAT_006–007 | ✅ |
| 5 | Filter | Tất cả điểm sao | select | API `score` | — | ⬜ |
| 6 | Filter | Làm mới (reset) | button | Clear search + filters + selectedIds | TC_AD_RAT_008 | ✅ |
| 7 | Table | Checkbox từng dòng / select all | checkbox | `selectedIds` | TC_AD_RAT_011–013 | ✅ |
| 8 | Table | Đánh dấu đã xem | button | PATCH mark-viewed (chỉ rating `is_new`) | TC_AD_RAT_014–015 | ✅ |
| 9 | Table | Ẩn | button | Mở reject dialog | TC_AD_RAT_016–019, 030 | ✅ |
| 10 | Bulk | Ẩn đã chọn | button | Bulk reject + lý do | TC_AD_RAT_020 | ✅ |
| 11 | Table | Xóa vĩnh viễn (icon) | button | Mở delete dialog | TC_AD_RAT_021–024 | ✅ |
| 12 | Bulk | Xóa | button | Bulk delete modal | TC_AD_RAT_025–026 | ✅ |
| 13 | Table | Pagination / per_page | button/select | API `page`, `per_page` | TC_AD_RAT_009–010 | ✅ |

## 3. Data Display Integrity

| # | Vùng UI | Field API | Field UI | TC | Auto |
|---|---------|-----------|----------|-----|------|
| 1 | Row user | `user.full_name` | tên khách hàng | TC_AD_RAT_002 | ✅ |
| 2 | Row target | `tour.name` / `location.name` | link tour/location | TC_AD_RAT_002 | ✅ |
| 3 | Row score | `score` | `5.0 / 5.0` + sao | TC_AD_RAT_002 | ✅ |
| 4 | Row comment | `comment` | nội dung nhận xét | TC_AD_RAT_002 | ✅ |
| 5 | Row badge | `is_new` | Mới / Đã xem | TC_AD_RAT_002 | ✅ |
| 6 | Stats total | `summary.total_count` | Tổng đánh giá | TC_AD_RAT_003 | ✅ |
| 7 | Stats new/viewed/hidden | `new_count`, `viewed_count`, `rejected_count` | 4 cards KPI | TC_AD_RAT_003 | ✅ |
| 8 | Empty | `data=[]` | `charts.no_trend_data` | TC_AD_RAT_027 | ✅ |

## 4. Test cases — Auth (P0)

| ID | Mô tả | Auto | Map doc cũ |
|----|--------|------|------------|
| TC_AD_RAT_040 | Guest → `/login` | ✅ | ADMIN_RATING_001 |
| TC_AD_RAT_041 | User `role=user` → `/login` | ✅ | — |
| TC_AD_RAT_042 | Admin truy cập được | ✅ | — |

## 5. Test cases — Render & filter (P1)

| ID | Mô tả | Auto | Map doc cũ |
|----|--------|------|------------|
| TC_AD_RAT_001 | Heading, stats, filter, table 10 dòng | ✅ | ADMIN_RATING_002 |
| TC_AD_RAT_002 | Hiển thị user, tour, score, comment, badge Mới | ✅ | ADMIN_RATING_032 |
| TC_AD_RAT_003 | Stats cards khớp mock report | ✅ | ADMIN_RATING_002 |
| TC_AD_RAT_004 | Search keyword (debounce) | ✅ | ADMIN_RATING_008 |
| TC_AD_RAT_005 | Lọc type = tour | ✅ | ADMIN_RATING_007 |
| TC_AD_RAT_006 | Lọc trạng thái Mới | ✅ | ADMIN_RATING_006 |
| TC_AD_RAT_007 | Lọc trạng thái Đã ẩn | ✅ | ADMIN_RATING_006 |
| TC_AD_RAT_008 | Reset filter + clear selection | ✅ | ADMIN_RATING_009 |
| TC_AD_RAT_009 | Pagination trang 2 | ✅ | ADMIN_RATING_010 |
| TC_AD_RAT_010 | Đổi 20 dòng/trang | ✅ | ADMIN_RATING_010 |
| TC_AD_RAT_027 | Empty state | ✅ | ADMIN_RATING_005 |

## 6. Test cases — Selection & mark viewed (P1)

| ID | Mô tả | Auto | Map doc cũ |
|----|--------|------|------------|
| TC_AD_RAT_011 | Chọn 1 checkbox | ✅ | ADMIN_RATING_011 |
| TC_AD_RAT_012 | Chọn tất cả trang | ✅ | ADMIN_RATING_012 |
| TC_AD_RAT_013 | Bỏ chọn tất cả trang | ✅ | ADMIN_RATING_013 |
| TC_AD_RAT_014 | Đánh dấu đã xem | ✅ | ADMIN_RATING_014* |
| TC_AD_RAT_015 | Mark viewed API lỗi → toast | ✅ | ADMIN_RATING_015* |

\* Doc cũ ghi "approve" — UI thực tế là **mark-viewed**, không gọi `/approve`.

## 7. Test cases — Hide / reject (P1)

| ID | Mô tả | Auto | Map doc cũ |
|----|--------|------|------------|
| TC_AD_RAT_016 | Mở dialog ẩn | ✅ | ADMIN_RATING_016 |
| TC_AD_RAT_017 | Ẩn với lý do hợp lệ | ✅ | ADMIN_RATING_017 |
| TC_AD_RAT_018 | Lý do rỗng → validation | ✅ | ADMIN_RATING_018 |
| TC_AD_RAT_019 | Hủy dialog — không gọi API | ✅ | — |
| TC_AD_RAT_020 | Bulk ẩn đã chọn | ✅ | ADMIN_RATING_020–021 |
| TC_AD_RAT_030 | Reject API lỗi → toast | ✅ | ADMIN_RATING_019 |

## 8. Test cases — Delete & export (P1)

| ID | Mô tả | Auto | Map doc cũ |
|----|--------|------|------------|
| TC_AD_RAT_021 | Mở delete dialog | ✅ | ADMIN_RATING_023 |
| TC_AD_RAT_022 | Xóa sau xác nhận | ✅ | ADMIN_RATING_024 |
| TC_AD_RAT_023 | Hủy delete — không gọi API | ✅ | — |
| TC_AD_RAT_024 | Delete API lỗi — giữ row | ✅ | ADMIN_RATING_025 |
| TC_AD_RAT_025 | Bulk delete | ✅ | ADMIN_RATING_027 |
| TC_AD_RAT_026 | Đóng bulk delete backdrop — giữ selection | ✅ | ADMIN_RATING_028 |
| TC_AD_RAT_028 | Export Excel thành công | ✅ | ADMIN_RATING_029 |
| TC_AD_RAT_029 | Export API lỗi → toast | ✅ | ADMIN_RATING_030 |

## 9. API contract (P2)

| ID | Mô tả | Auto |
|----|--------|------|
| API_RAT_001 | GET list không auth → 401 | ✅ |
| API_RAT_002 | GET list admin → 200 paginated | ✅ |
| API_RAT_003 | GET list `type=tour` | ✅ |

## 10. Chưa automation (backlog manual / Phase 2)

| ID doc cũ | Mô tả | Ghi chú |
|-----------|--------|---------|
| ADMIN_RATING_003–004 | Loading report/list riêng | Chưa mock delay |
| ADMIN_RATING_022 | Bulk reject partial error | Cần mock partial 500 |
| ADMIN_RATING_031 | Disable khi `isMutating` | Regression manual |
| ADMIN_RATING_033 | Rating có ảnh | Badge `image_count` trên row |
| ADMIN_RATING_034 | Responsive 375/768 | Manual / visual |

## 11. Đề xuất cải thiện (PHASE 0.8)

| ID | Loại | Severity | Phát hiện | Đề xuất | Trạng thái |
|----|------|----------|-----------|---------|------------|
| IMP_RAT_001 | Doc | P3 | Doc cũ ghi approve — code dùng mark-viewed | Cập nhật testcase map | **fixed** |
| IMP_RAT_002 | UX | P2 | Reset filter bị debounce search ghi đè | Guard trong `RatingFilterBar` useEffect | **fixed** |
| IMP_RAT_003 | i18n | P2 | Toast mutation hardcode VI trong hook | Dùng `t()` trong `useRatingQueries` | **fixed** |
| IMP_RAT_004 | UX | P1 | List API lỗi không có error panel + retry | Giống Promotions (`rating-list-error`) | **fixed** |
| IMP_RAT_005 | Test | P3 | Mock pathname list ban đầu sai | Regex `/admin/ratings` | **fixed** |
| IMP_RAT_006 | Test | P3 | POM statCard / selectedCount / delete / toast | `RatingsPage.ts` | **fixed** |
| IMP_RAT_007 | UX | P1 | Bulk hide/delete `Promise.all` fail-fast | `Promise.allSettled` + toast partial | **fixed** |
| IMP_RAT_008 | UX | P1 | `selectedIds` không clear khi đổi filter/page | Clear trong `handleFilterChange` / `handleLimitChange` | **fixed** |
| IMP_RAT_009 | a11y | P2 | Nút delete icon thiếu accessible name | `aria-label` trên delete trong `RatingTable` | **fixed** |
| IMP_RAT_010 | UX | P2 | Nút reset filter trùng nhãn "Làm mới" (refresh bảng) | Key `actions.reset_filters` | **fixed** |
| IMP_RAT_011 | UX | P2 | Empty state dùng `charts.no_trend_data` | Key `table.empty_title` / `empty_subtitle` | **fixed** |
| IMP_RAT_012 | UX | P2 | Stats report lỗi im lặng hiện 0 | Error panel + retry (`rating-stats-error`) | **fixed** |
| IMP_RAT_013 | Code | P3 | `approveMutation` dead code trên màn quản lý | Gỡ khỏi `useAdminRatingMutations` | **fixed** |
| IMP_RAT_014 | UX | P3 | Row không hiển thị `image_count` | Badge ảnh trong cột comment | **fixed** |
| IMP_RAT_015 | UX | P3 | Bulk toast count sau `setSelectedIds([])` | Lưu `bulkCount` trước khi clear | **fixed** |
| IMP_RAT_016 | UX | P3 | `RejectRatingDialog` không reset form khi đóng | `reset()` trong `handleClose` | **fixed** |

## 12. Ghi chú kỹ thuật

- Mock dataset: 12 rows (`ratings-list.data.ts`), page 1 = 10 dòng.
- Stats kỳ vọng: total 12 · new 5 · viewed 7 · hidden 1.
- Filter management status: `new` → `is_new=true`, `viewed` → `is_new=false`, `hidden` → `status=rejected`.
- Export mutation toast dùng `toast.promise` trên page (hook không toast trùng).
- Delete row: `aria-label` + `title` = `table.tooltip_delete`.
- Reset filter: `actions.reset_filters` (khác refresh bảng).
- List lỗi: `data-testid="rating-list-error"`; stats lỗi: `rating-stats-error`.

## 13. Checklist regression

- [x] Auth guest/non-admin/admin
- [x] Render + stats + data row
- [x] Search + filter type/status + reset
- [x] Pagination + per_page
- [x] Checkbox select / bulk hide / bulk delete
- [x] Mark viewed + hide + delete + export
- [x] List error panel + stats error retry
- [ ] Responsive / ảnh rating (manual)

**Trạng thái automation:** **36/36 passed** (`npm run test:admin:ratings`, 2026-06-23 — IMP P1–P3 fixed)
