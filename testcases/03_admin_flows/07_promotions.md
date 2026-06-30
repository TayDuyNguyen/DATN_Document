# Admin — Quản lý Khuyến mãi & Mã giảm giá (Promotions)

**Route:** `/admin/promotions`  
**Source:** `danangtrip-admin/src/pages/Promotions/`  
**Automation:** `tests/admin/promotions.spec.ts` · `tests/admin/promotions-auth.spec.ts` · `tests/api/admin-promotions.api.spec.ts`  
**POM:** `PromotionsPage.ts` · Mock: `tests/fixtures/api/promotions.mock.ts` · Data: `promotions-list.data.ts`  
**Chạy test:** `npm run test:admin:promotions`

---

## 1. Phạm vi

| Hạng mục | Chi tiết |
|----------|----------|
| Vai trò | **Admin** only (`PrivateRoute`) |
| API | `GET/POST /admin/promotions` · `PUT /admin/promotions/:id` · `PATCH .../status` · `DELETE .../:id` |
| UI | Stats 3 card · Filter bar · Table + pagination · Drawer form (create/edit) · Delete modal |
| Seed mirror | `17_promotions_seed.sql` (DANANG10, FLASH20, EXPIRED50K, …) |

## 2. UI Interactive Inventory

| # | Vùng UI | Nhãn (i18n) | Loại | Hành vi kỳ vọng | TC doc | Auto |
|---|---------|-------------|------|-----------------|--------|------|
| 1 | Header | Thêm mã giảm giá mới | button | Mở drawer create | TC_AD_PROM_001 | ✅ |
| 2 | Filter | Tìm kiếm theo mã hoặc tên | search | Debounce 300ms → API `search` | TC_AD_PROM_020 | ✅ |
| 3 | Filter | Tất cả trạng thái / Đang chạy / … | select | API `status` | TC_AD_PROM_021 | ✅ |
| 4 | Filter | Đang có hiệu lực lúc này | button toggle | API `valid_now=true` | TC_AD_PROM_022 | ✅ |
| 5 | Filter | Đặt lại bộ lọc (reset) | button | Clear search + filters | TC_AD_PROM_023 | ✅ |
| 6 | Filter tag | X trên tag lọc | button | Xóa từng filter | TC_AD_PROM_032–033 | ✅ |
| 7 | Table | Toggle kích hoạt | toggle | PATCH status active↔inactive | TC_AD_PROM_014–015 | ✅ |
| 8 | Table | Chỉnh sửa mã | icon button | Mở drawer edit | TC_AD_PROM_024 | ✅ |
| 9 | Table | Xóa | icon button | Mở delete modal | TC_AD_PROM_016 | ✅ |
| 10 | Table | Pagination prev/next/số trang | button | API `page` | TC_AD_PROM_026 | ✅ |
| 11 | Table | 10/20/50 dòng/trang | select | API `per_page` | TC_AD_PROM_026 | ✅ |
| 12 | List error | Thử lại | button | `refetch` sau lỗi API list | TC_AD_PROM_028 | ✅ |
| 13 | Drawer | Lưu thông tin | button | POST/PUT + toast | TC_AD_PROM_011–012, 025 | ✅ |
| 14 | Drawer | Hủy bỏ | button | Đóng drawer | TC_AD_PROM_029 | ✅ |
| 15 | Drawer | Loại giảm giá | select | percent / fixed | TC_AD_PROM_012 | ✅ |
| 16 | Delete modal | Đồng ý xóa | button | DELETE + toast | TC_AD_PROM_016 | ✅ |
| 17 | Delete modal | Hủy bỏ | button | Đóng modal | TC_AD_PROM_017 | ✅ |

## 3. Data Display Integrity

| # | Vùng UI | Field API | Field UI | TC | Auto |
|---|---------|-----------|----------|-----|------|
| 1 | Row code | `code` | badge uppercase | TC_AD_PROM_002 | ✅ |
| 2 | Row name | `name` | text bold | TC_AD_PROM_002 | ✅ |
| 3 | Row description | `description` | line-clamp | TC_AD_PROM_002 | ✅ |
| 4 | Discount | `discount_type`, `discount_value` | `-10%` / `-200,000 đ` | TC_AD_PROM_002, 012 | ✅ |
| 5 | Usage | `used_count`, `usage_limit` | `42 / 500 lượt` | TC_AD_PROM_002 | ✅ |
| 6 | Stats total | `total` | card Tổng số mã | TC_AD_PROM_003 | ✅ |
| 7 | Empty | `data=[]` | `labels.no_data` | TC_AD_PROM_027 | ✅ |

## 4. Test cases — Auth (P0)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_PROM_040 | Guest → `/login` | ✅ |
| TC_AD_PROM_041 | User `role=user` → `/login` | ✅ |
| TC_AD_PROM_042 | Admin truy cập được | ✅ |

## 5. Test cases — Render & data (P1)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_PROM_001 | Heading, stats, filter, table 10 dòng | ✅ |
| TC_AD_PROM_002 | Hiển thị code, name, description, discount, usage | ✅ |
| TC_AD_PROM_003 | Stats cards khớp mock page 1 | ✅ |
| TC_AD_PROM_027 | Empty state | ✅ |
| TC_AD_PROM_028 | List API lỗi → error panel + retry | ✅ |

## 6. Test cases — Drawer create/edit (P0–P1)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_PROM_010 | Validate trường bắt buộc (code, name) | ✅ |
| TC_AD_PROM_011 | Tạo mã % thành công (HELLOSUMMER) | ✅ |
| TC_AD_PROM_012 | Tạo mã fixed 200.000đ | ✅ |
| TC_AD_PROM_013 | Ngày kết thúc < ngày bắt đầu → lỗi | ✅ |
| TC_AD_PROM_024 | Mở edit — prefill code/name | ✅ |
| TC_AD_PROM_025 | Cập nhật tên chương trình | ✅ |
| TC_AD_PROM_029 | Hủy drawer | ✅ |

## 7. Test cases — Status & delete (P1)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_PROM_014 | Toggle active → inactive | ✅ |
| TC_AD_PROM_015 | Toggle inactive → active | ✅ |
| TC_AD_PROM_016 | Xóa + xác nhận | ✅ |
| TC_AD_PROM_017 | Hủy xóa — không gọi API | ✅ |
| TC_AD_PROM_030 | PATCH status lỗi → toast error | ✅ |
| TC_AD_PROM_031 | DELETE lỗi → giữ row | ✅ |
| TC_AD_PROM_034 | Toggle mã expired bị disabled | ✅ |
| TC_AD_PROM_036 | POST create lỗi → toast | ✅ |
| TC_AD_PROM_037 | PUT update lỗi → toast | ✅ |

## 8. Test cases — Filter & pagination (P1)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_PROM_020 | Search theo mã (debounce) | ✅ |
| TC_AD_PROM_021 | Lọc trạng thái Tạm ngưng | ✅ |
| TC_AD_PROM_022 | Lọc Đang có hiệu lực lúc này | ✅ |
| TC_AD_PROM_023 | Reset filter | ✅ |
| TC_AD_PROM_032 | Xóa tag lọc trạng thái | ✅ |
| TC_AD_PROM_033 | Xóa tag lọc valid now | ✅ |
| TC_AD_PROM_026 | Đổi limit + trang 2 | ✅ |
| TC_AD_PROM_035 | Đổi 20 dòng/trang | ✅ |

## 9. API contract (P2)

| ID | Mô tả | Auto |
|----|--------|------|
| API_PROM_001 | GET list không auth → 401 | ✅ |
| API_PROM_002 | GET list admin → 200 paginated | ✅ |
| API_PROM_003 | GET list `status=active` | ✅ |

## 10. Đề xuất cải thiện (PHASE 0.8)

| ID | Loại | Severity | Phát hiện | Đề xuất | Trạng thái |
|----|------|----------|-----------|---------|------------|
| IMP_PROM_001 | i18n | P2 | Stats card labels hardcode tiếng Việt | Dùng `t('promotions:stats.*')` | **fixed** |
| IMP_PROM_002 | i18n | P2 | Delete modal title/nút hardcode VI | `PromotionDeleteDialog` + i18n | **fixed** |
| IMP_PROM_003 | UX | P2 | Stats active/uses chỉ đếm trang hiện tại | Nhãn `*_on_page` + hint phạm vi trang | **fixed** |
| IMP_PROM_004 | Doc | P3 | Doc cũ ghi Staff — thực tế chỉ Admin route | Đã sửa trong file này | **fixed** |
| IMP_PROM_005 | UX | P2 | Checkbox bulk không có hành động | Gỡ checkbox khỏi table | **fixed** |
| IMP_PROM_006 | UX | P2 | Filter reset nhãn "Hủy bỏ" gây nhầm | Đổi `actions.reset_filters` | **fixed** |
| IMP_PROM_007 | UX | P1 | List API lỗi không có UI retry | `promotion-list-error` + nút Thử lại | **fixed** |
| IMP_PROM_008 | a11y | P2 | Drawer backdrop vẫn focusable khi đóng | `aria-hidden` + `inert` trên panel | **fixed** |
| IMP_PROM_010 | Test | P3 | Filter tag X chưa có automation | TC_AD_PROM_032–033 | **fixed** |
| IMP_PROM_011 | Test | P3 | Toggle expired / per_page / create-update error | TC_AD_PROM_034–037 | **fixed** |
| IMP_PROM_012 | Test | P3 | Auth mock flaky redirect login | `mockAuthRefreshApi` auth/** + session recovery | **fixed** |

## 11. Ghi chú kỹ thuật

- Drawer dùng `react-hook-form` + `promotionSchema` (yup).
- Toggle status **disabled** khi `status === 'expired'`.
- Filter reset dùng nhãn `actions.reset_filters` (= "Đặt lại bộ lọc").
- Delete dialog: `data-testid="promotion-delete-dialog"` · confirm `promotion-delete-confirm`.
- List lỗi: `data-testid="promotion-list-error"`.
- Mock `valid_now` dùng reference date `2026-06-15` — VIP25 (starts 2026-09) bị loại.

## 12. Checklist regression

- [x] Auth guest/non-admin
- [x] Data display code + discount + usage
- [x] Create percent/fixed + date validation
- [x] Toggle status + delete confirm/cancel
- [x] Search + filter + pagination
- [x] Edit update + empty state

**Trạng thái automation:** **35/35 passed** (`npm run test:admin:promotions`)
