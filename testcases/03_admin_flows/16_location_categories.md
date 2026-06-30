# Màn hình Quản lý Danh mục Địa điểm (Location Categories Management)

## Phạm vi

- Route: `/admin/location-categories` (redirect cũ: `/admin/locations/categories`)
- API liên quan: `GET/POST /admin/categories`, `PUT/PATCH/DELETE /admin/categories/:id`, `PATCH /admin/categories/:id/status`, `PATCH /admin/categories/reorder`
- Vai trò: Quản trị viên (Admin) / Nhân viên (Staff).

## Điều kiện trước

- Tài khoản: Đã đăng nhập vào trang quản trị bằng tài khoản Admin/Staff.
- Môi trường: Local dev server (`http://localhost:5173`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Auto |
| --- | --- | --- | --- | --- |
| 1 | TC_AD_LOCCAT_001 | Danh sách danh mục | Hiển thị lưới card: tên, slug, số địa điểm, thứ tự | ✅ |
| 2 | TC_AD_LOCCAT_002 | Thêm — Validate | Bấm Lưu khi chưa nhập tên → báo lỗi | ✅ |
| 3 | TC_AD_LOCCAT_003 | Thêm thành công | Tạo mới + auto slug từ tên (vd. "Khu Vui Chơi" → `khu-vui-choi`) | ✅ |
| 4 | TC_AD_LOCCAT_004 | Chỉnh sửa | Sửa mô tả và lưu thành công | ✅ |
| 5 | TC_AD_LOCCAT_005 | Xóa (có địa điểm) | Chặn xóa khi danh mục còn địa điểm liên kết | ✅ (TC_017) |
| 6 | TC_AD_LOCCAT_006 | Thống kê | Stats: tổng / active / inactive danh mục | ✅ |
| 7 | TC_AD_LOCCAT_007 | Tìm kiếm | Lọc theo tên/slug | ✅ |
| 8 | TC_AD_LOCCAT_008 | Lọc trạng thái | Lọc inactive/active | ✅ |
| 9 | TC_AD_LOCCAT_009 | Toggle status | Đổi trạng thái ngay trên card (PATCH) | ✅ |
| 10 | TC_AD_LOCCAT_010 | Empty state | Không có kết quả sau lọc | ✅ |
| 11 | TC_AD_LOCCAT_011 | Lỗi tải + retry | Hiển thị lỗi và nút Thử lại | ✅ |
| 12 | TC_AD_LOCCAT_012 | Reorder — hủy | Vào chế độ sắp xếp và hủy | ✅ |
| 13 | TC_AD_LOCCAT_013 | Reorder — disabled | Không sắp xếp khi đang search/lọc | ✅ |
| 14 | TC_AD_LOCCAT_014 | Reorder — lưu | Lưu thứ tự (PATCH reorder) | ✅ |
| 15 | TC_AD_LOCCAT_015 | Xóa — hủy dialog | Hủy xác nhận xóa | ✅ |
| 16 | TC_AD_LOCCAT_016 | Xóa thành công | Xóa danh mục không có địa điểm | ✅ |
| 17 | TC_AD_LOCCAT_017 | Xóa bị chặn | Nút xóa disabled khi còn địa điểm liên kết | ✅ |
| 18 | TC_AD_LOCCAT_018 | Drawer — hủy | Đóng drawer tạo mới | ✅ |
| 19 | TC_AD_LOCCAT_019 | Icon browser | Mở thư viện icon trong drawer | ✅ |
| 40 | TC_AD_LOCCAT_040 | Auth guest | Guest redirect login | ✅ |
| 41 | TC_AD_LOCCAT_041 | Auth non-admin | User thường redirect login | ✅ |
| 42 | TC_AD_LOCCAT_042 | Auth admin | Admin truy cập được | ✅ |

## Ghi chú

- UI dùng **card grid** (không phải bảng); mô tả chỉ hiển thị trong drawer.
- Nút breadcrumb **Thêm mới** mở drawer tạo danh mục.
- Xóa danh mục còn địa điểm: nút xóa **disabled** + tooltip (giống Tour Categories).
- Drag reorder pixel-perfect: kiểm thử thủ công nếu cần (automation cover enter/save/cancel).

## Automation

- Script: `npm run test:admin:location-categories`
- Spec: `tests/admin/location-categories.spec.ts`, `location-categories-auth.spec.ts`, `api/admin-location-categories.api.spec.ts`
- POM: `tests/pages/admin/LocationCategoriesPage.ts`
- Mock: `tests/fixtures/api/location-categories.mock.ts`

## Improvement backlog (PHASE 0.8)

| ID | Loại | Ưu tiên | Phát hiện | Ghi chú |
|----|------|---------|-----------|---------|
| IMP_LOCCAT_001 | Doc | P2 | Doc cũ ghi route `/admin/locations/categories` | **fixed** — doc |
| IMP_LOCCAT_002 | UX | P1 | Xóa danh mục còn địa điểm chỉ fail sau confirm | **fixed** — disable nút xóa |
| IMP_LOCCAT_003 | i18n | P3 | Empty grid dùng `messages.no_data` chung | **fixed** — `categories.empty_*` |
| IMP_LOCCAT_004 | Test | P3 | Thiếu data-testid trên card/drawer/dialog | **fixed** |
| IMP_LOCCAT_005 | UX | P2 | Progress bar `/50` trên card | **fixed** — bỏ bar, link count |
| IMP_LOCCAT_006 | A11y | P2 | Nút edit/delete icon-only thiếu aria-label | **fixed** |
| IMP_LOCCAT_007 | Test | P3 | Drag reorder pixel-perfect | manual |
| IMP_LOCCAT_008 | Code | P1 | API unwrap `{ category }` | **fixed** — `categoryApi` |
| IMP_LOCCAT_009 | UX | P1 | Subtitle drawer tạo mới sai ngữ cảnh | **fixed** — `categories.form.create_subtitle` |
| IMP_LOCCAT_010 | UX | P1 | Drawer backdrop đóng mất data | **fixed** — `UnsavedChangesGuard` |
| IMP_LOCCAT_011 | UX | P2 | Link count → location list | **fixed** — `?category_id=` + LocationList |
| IMP_LOCCAT_012 | UX | P2 | Stats không ghi chú scope | **fixed** — `stats_scope_note` |
| IMP_LOCCAT_013 | UX | P2 | Thiếu reset filters | **fixed** |
| IMP_LOCCAT_014 | UX | P2 | Reorder cancel không rollback | **fixed** |
| IMP_LOCCAT_015 | UX | P2 | Status toggle không disable pending | **fixed** |
| IMP_LOCCAT_016 | UX | P3 | Mô tả không hiện trên card | **fixed** — line-clamp |
| IMP_LOCCAT_017 | Code | P3 | Trùng colorOptions | **fixed** — `categoryTheme.ts` |
| IMP_LOCCAT_018 | Code | P3 | placeholderData giữ data cũ | **fixed** — bỏ placeholderData |
