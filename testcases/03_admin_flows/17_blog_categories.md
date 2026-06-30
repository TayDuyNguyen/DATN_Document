# Màn hình Quản lý Danh mục Bài viết (Blog Categories Management)

## Phạm vi

- Route: `/admin/blog-categories` (redirect cũ có thể ghi `/admin/blog/categories`)
- API liên quan: `GET/POST /admin/blog-categories`, `PUT/DELETE /admin/blog-categories/:id`, `PATCH /admin/blog-categories/reorder`
- Vai trò: Quản trị viên (Admin) / Nhân viên (Staff).
- UI: **Lưới card** bên trái + **form inline** bên phải (không dùng drawer).

## Điều kiện trước

- Tài khoản: Đã đăng nhập vào trang quản trị bằng tài khoản Admin/Staff.
- Môi trường: Local dev server (`http://localhost:5173`).

## Test cases

| TT | Test Case ID | Chức năng | Mô tả Test Case | Auto |
| --- | --- | --- | --- | --- |
| 1 | TC_AD_BLOGCAT_001 | Danh sách danh mục | Card grid: tên, slug, mô tả, số bài viết | ✅ |
| 2 | TC_AD_BLOGCAT_002 | Thêm — Validate | Bấm Tạo mới khi chưa nhập tên → báo lỗi | ✅ |
| 3 | TC_AD_BLOGCAT_003 | Thêm thành công | Tạo mới + auto slug (`Cẩm Nang Ăn Uống` → `cam-nang-an-uong`) | ✅ |
| 4 | TC_AD_BLOGCAT_004 | Chỉnh sửa | Sửa mô tả và lưu thành công | ✅ |
| 5 | TC_AD_BLOGCAT_005 | Xóa (có bài viết) | Chặn xóa khi danh mục còn bài viết | ✅ (TC_017) |
| 6 | TC_AD_BLOGCAT_006 | Thống kê | Stats: tổng danh mục / tổng bài viết | ✅ |
| 7 | TC_AD_BLOGCAT_007 | Tìm kiếm | Lọc client-side theo tên/slug/mô tả | ✅ |
| 8 | TC_AD_BLOGCAT_008 | Preview form | Khung xem trước cập nhật theo tên nhập | ✅ |
| 9 | TC_AD_BLOGCAT_009 | Highlight edit | Card đang sửa có ring highlight | ✅ |
| 10 | TC_AD_BLOGCAT_010 | Empty state | Không có kết quả sau search | ✅ |
| 11 | TC_AD_BLOGCAT_011 | Lỗi tải + retry | Hiển thị lỗi và nút Thử lại | ✅ |
| 12 | TC_AD_BLOGCAT_012 | Reorder — hủy | Vào chế độ sắp xếp và hủy | ✅ |
| 13 | TC_AD_BLOGCAT_013 | Reorder — disabled | Không sắp xếp khi đang search | ✅ |
| 14 | TC_AD_BLOGCAT_014 | Reorder — lưu | Lưu thứ tự (PATCH reorder) | ✅ |
| 15 | TC_AD_BLOGCAT_015 | Xóa — hủy dialog | Hủy xác nhận xóa | ✅ |
| 16 | TC_AD_BLOGCAT_016 | Xóa thành công | Xóa danh mục không có bài viết | ✅ |
| 17 | TC_AD_BLOGCAT_017 | Xóa bị chặn | API 400 — danh mục vẫn còn sau confirm | ✅ |
| 18 | TC_AD_BLOGCAT_018 | Form — hủy | Reset form về chế độ thêm mới | ✅ |
| 40 | TC_AD_BLOGCAT_040 | Auth guest | Guest redirect login | ✅ |
| 41 | TC_AD_BLOGCAT_041 | Auth non-admin | User thường redirect login | ✅ |
| 42 | TC_AD_BLOGCAT_042 | Auth admin | Admin truy cập được | ✅ |

## Ghi chú

- Nút **Thêm danh mục mới** (header) scroll tới form bên phải.
- Click **Sửa** trên card load dữ liệu vào form inline.
- Drag reorder: automation cover enter/save/cancel; pixel-perfect manual.

## Automation

- Script: `npm run test:admin:blog-categories`
- Spec: `tests/admin/blog-categories.spec.ts`, `blog-categories-auth.spec.ts`, `api/admin-blog-categories.api.spec.ts`
- POM: `tests/pages/admin/BlogCategoriesPage.ts`
- Mock: `tests/fixtures/api/blog-categories.mock.ts`

## Improvement backlog (PHASE 0.8)

| ID | Loại | Ưu tiên | Phát hiện | Ghi chú |
|----|------|---------|-----------|---------|
| IMP_BLOGCAT_001 | Doc | P2 | Doc ghi route `/admin/blog/categories` — code `/admin/blog-categories` | **fixed** — doc |
| IMP_BLOGCAT_002 | UX | P1 | Xóa danh mục còn bài viết chỉ fail sau confirm | **fixed** — disable nút xóa + tooltip |
| IMP_BLOGCAT_003 | UX | P2 | Link số bài viết → blog list `?category_id=` | **fixed** |
| IMP_BLOGCAT_004 | Test | P3 | Thiếu data-testid | **fixed** |
| IMP_BLOGCAT_005 | UX | P2 | Reorder cancel không rollback list local | **fixed** |
| IMP_BLOGCAT_006 | i18n | P3 | Empty search dùng `empty.title` chung blog | **fixed** — `empty_search_*` |
| IMP_BLOGCAT_007 | Test | P3 | Drag reorder pixel-perfect | manual |
| IMP_BLOGCAT_008 | UX | P2 | Form không reset sau tạo | **fixed** |
| IMP_BLOGCAT_009 | UX | P2 | UnsavedChangesGuard + confirm chuyển card | **fixed** |
| IMP_BLOGCAT_010 | UX | P3 | Slug auto ghi đè khi user sửa tay | **fixed** — `slugTouched` |
| IMP_BLOGCAT_011 | UX | P3 | Stats scope note + reset search | **fixed** |
| IMP_BLOGCAT_012 | Code | P3 | Delete dialog inline trong index | **fixed** — `BlogCategoryDeleteDialog` |
