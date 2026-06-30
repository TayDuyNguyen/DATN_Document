# Màn hình Quản lý Danh mục Tour (Tour Categories Management)

## Phạm vi

- Route: `/admin/tour-categories`
- API liên quan: `GET/POST /admin/tour-categories`, `PUT/PATCH/DELETE /admin/tour-categories/:id`, `PATCH /admin/tour-categories/:id/status`, `PATCH /admin/tour-categories/reorder`
- Vai trò: Quản trị viên (Admin) / Nhân viên (Staff).

## Điều kiện trước

- Tài khoản: Đã đăng nhập vào trang quản trị bằng tài khoản Admin/Staff.
- Môi trường: Local dev server (`http://localhost:5173`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Auto |
| --- | --- | --- | --- | --- |
| 1 | TC_AD_TOURCAT_001 | Danh sách danh mục | Hiển thị lưới card: tên, slug, icon, số tour, thứ tự | ✅ |
| 2 | TC_AD_TOURCAT_002 | Thêm — Validate | Bấm Lưu khi chưa nhập tên → báo lỗi | ✅ |
| 3 | TC_AD_TOURCAT_003 | Thêm thành công | Tạo mới + auto slug từ tên | ✅ |
| 4 | TC_AD_TOURCAT_004 | Chỉnh sửa | Sửa mô tả và lưu thành công | ✅ |
| 5 | TC_AD_TOURCAT_005 | Xóa (có tour) | Chặn xóa khi danh mục còn tour liên kết | ✅ (TC_017) |
| 6 | TC_AD_TOURCAT_006 | Thống kê | Stats: tổng tour, danh mục active/inactive | ✅ |
| 7 | TC_AD_TOURCAT_007 | Tìm kiếm | Lọc theo tên/slug | ✅ |
| 8 | TC_AD_TOURCAT_008 | Lọc trạng thái | Lọc inactive/active | ✅ |
| 9 | TC_AD_TOURCAT_009 | Toggle status | Đổi trạng thái ngay trên card (PATCH) | ✅ |
| 10 | TC_AD_TOURCAT_010 | Empty state | Không có kết quả sau lọc | ✅ |
| 11 | TC_AD_TOURCAT_011 | Lỗi tải + retry | Hiển thị lỗi và nút Thử lại | ✅ |
| 12 | TC_AD_TOURCAT_012 | Reorder — hủy | Vào chế độ sắp xếp và hủy | ✅ |
| 13 | TC_AD_TOURCAT_013 | Reorder — disabled | Không sắp xếp khi đang search/lọc | ✅ |
| 14 | TC_AD_TOURCAT_014 | Reorder — lưu | Lưu thứ tự (PATCH reorder) | ✅ |
| 15 | TC_AD_TOURCAT_015 | Xóa — hủy dialog | Hủy xác nhận xóa | ✅ |
| 16 | TC_AD_TOURCAT_016 | Xóa thành công | Xóa danh mục không có tour | ✅ |
| 17 | TC_AD_TOURCAT_017 | Xóa bị chặn | Toast lỗi khi còn tour | ✅ |
| 18 | TC_AD_TOURCAT_018 | Drawer — hủy | Đóng drawer tạo mới | ✅ |
| 19 | TC_AD_TOURCAT_019 | Icon browser | Mở thư viện biểu tượng trong drawer | ✅ |
| 40 | TC_AD_TOURCAT_040 | Auth guest | Guest redirect login | ✅ |
| 41 | TC_AD_TOURCAT_041 | Auth non-admin | User thường redirect login | ✅ |
| 42 | TC_AD_TOURCAT_042 | Auth admin | Admin truy cập được | ✅ |

## Ghi chú

- Nút breadcrumb **Thêm mới** mở drawer tạo danh mục.
- Mô tả danh mục chỉ hiển thị trong drawer, không trên card.
- Drag reorder trên UI: kiểm thử thủ công nếu cần pixel-perfect (automation cover enter/save/cancel).

## Automation

- Script: `npm run test:admin:tour-categories`
- Spec: `tests/admin/tour-categories.spec.ts`, `tour-categories-auth.spec.ts`, `api/admin-tour-categories.api.spec.ts`
- POM: `tests/pages/admin/TourCategoriesPage.ts`
- Mock: `tests/fixtures/api/tour-categories.mock.ts`
