# Admin — Danh sách Người dùng (User List Page)

**Route:** `/admin/users`  
**Source:** `danangtrip-admin/src/pages/Users/UserList/`  
**Automation:** `tests/admin/users.spec.ts` · `tests/admin/users-extended.spec.ts` · `tests/api/admin-users.api.spec.ts` · `tests/api/user-login-blocked.api.spec.ts`  
**POM:** `UserListPage.ts` · Mock: `tests/fixtures/api/users.mock.ts`

---

## 1. Phạm vi

| Hạng mục | Chi tiết |
|----------|----------|
| Vai trò | **Admin** only (`PrivateRoute`) |
| API list | `GET /api/v1/admin/users` — `page`, `per_page`, `q`, `role`, `status`, `sort_by`, `sort_order` |
| API stats | Embedded trong list response (`total`, `active`, `banned`, `admin`) |
| Mutations | `PATCH .../status`, `PATCH .../role`, `DELETE .../:id` |
| Export | `GET /admin/users/export` → `users-report.xlsx` |
| Role | `admin` \| `user` — **không** có Staff |
| Status UI | **HOẠT ĐỘNG** / **BỊ KHÓA** (`active` / `banned`) |
| Khóa tài khoản | **BlockUserDialog** xác nhận; mở khóa trực tiếp |
| Bulk delete | `window.confirm` (không modal custom) |

## 2. Điều kiện tiên quyết

- Admin đã đăng nhập · dev server `:5173`
- Mock: ≥4 user (1 admin, 2 active user, 1 banned)
- Chạy test: `npm run test:admin:users` → **67 passed**

## 3. Tổng quan trạng thái

| Nhóm | Tổng TC | ✅ Auto | ⏳ Backlog |
|------|---------|---------|------------|
| Render & navigation | 5 | 5 | 0 |
| Search & filter | 10 | 10 | 0 |
| Row actions | 6 | 6 | 0 |
| Bulk actions | 6 | 6 | 0 |
| Selection & sort | 6 | 6 | 0 |
| Pagination & refresh | 5 | 5 | 0 |
| Stats | 4 | 4 | 0 |
| Auth & security | 5 | 5 | 0 |
| Dialog UX | 4 | 4 | 0 |
| Export & errors | 5 | 5 | 0 |
| **UI subtotal** | **56** | **56** | **0** |
| API smoke | 10 | 10 | 0 |
| **Tổng** | **66** | **66** | **0** |

> Ghi chú: `TC_AD_ULIST_019` (XSS) thuộc security; stats refetch = `TC_AD_ULIST_054`. Export filter = `TC_AD_ULIST_055`. Mutation error = `TC_AD_ULIST_047b`.

---

## 4. Render & navigation (P1)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_ULIST_001 | Bảng đủ cột + stats + Export + Thêm user | ✅ |
| TC_AD_ULIST_022 | Nút **Xem** → `/admin/users/detail/:id` | ✅ |
| TC_AD_ULIST_023 | Nút **Sửa** → `/admin/users/edit/:id` | ✅ |
| TC_AD_ULIST_024 | Nút **Thêm user** → `/admin/users/create` | ✅ |
| TC_AD_ULIST_049 | Avatar ảnh hoặc chữ cái đầu; username dưới email | ✅ |

---

## 5. Search & filter (P1)

| ID | Mô tả | Dữ liệu | Auto |
|----|--------|---------|------|
| TC_AD_ULIST_002 | Tìm theo tên/email (debounce ~300ms) | `staff@danangtrip.vn` — **không phân biệt hoa thường** | ✅ |
| TC_AD_ULIST_060 | Search `STAFF@...` / `le thi...` cùng kết quả | — | ✅ |
| TC_AD_ULIST_003 | Lọc role **USER** | — | ✅ |
| TC_AD_ULIST_025 | Lọc role **ADMIN** | — | ✅ |
| TC_AD_ULIST_006 | Lọc status **BANNED** | — | ✅ |
| TC_AD_ULIST_026 | Lọc status **ACTIVE** | — | ✅ |
| TC_AD_ULIST_016 | Nút **Đặt lại** xóa filter + search | — | ✅ |
| TC_AD_ULIST_027 | Badge "Bộ lọc đang chọn" hiện `q`, role, status | — | ✅ |
| TC_AD_ULIST_017 | Search không khớp → empty state | `no-match-xyz` | ✅ |
| TC_AD_ULIST_051 | Empty state có subtitle | — | ✅ |
| TC_AD_ULIST_053 | Search debounce — không spam request | Gõ nhanh | ✅ |

---

## 6. Row actions (P1)

| ID | Mô tả | Dữ liệu | Auto |
|----|--------|---------|------|
| TC_AD_ULIST_004 | Khóa user active + BlockUserDialog + toast | `hatran@gmail.com` | ✅ |
| TC_AD_ULIST_005 | Mở khóa user banned + toast | `quangminh@yahoo.com` | ✅ |
| TC_AD_ULIST_011 | Nâng USER → ADMIN (dialog confirm) | User id=2 | ✅ |
| TC_AD_ULIST_038 | Hạ ADMIN → USER (không dialog) | — | ✅ |
| TC_AD_ULIST_012 | Xóa 1 user qua modal | User id=3 | ✅ |
| TC_AD_ULIST_040 | Click badge trạng thái cũng trigger khóa/mở | — | ✅ |

---

## 7. Bulk actions (P1)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_ULIST_009 | Bulk khóa ≥2 user | ✅ |
| TC_AD_ULIST_034 | Bulk **kích hoạt** (banned → active) | ✅ |
| TC_AD_ULIST_010 | Bulk xóa + `window.confirm` | ✅ |
| TC_AD_ULIST_045 | Select-all trên trang → toolbar bulk | ✅ |
| TC_AD_ULIST_035 | Select-all loại trừ admin hiện tại | ✅ |
| TC_AD_ULIST_037 | Hủy bulk delete khi reject confirm | ✅ |

---

## 8. Selection & sort (P1–P2)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_ULIST_013 | Self-row: checkbox/khóa/xóa disabled + badge BẠN/YOU | ✅ |
| TC_AD_ULIST_015 | Sort ngày tham gia asc ↔ desc | ✅ |
| TC_AD_ULIST_036 | Checkbox indeterminate khi chọn một phần | ✅ |
| TC_AD_ULIST_043 | Row selected highlight (`bg-[#dff7f4]`) | ✅ |
| TC_AD_ULIST_039 | Dropdown role đóng khi click outside | ✅ |
| TC_AD_ULIST_048 | Self-row: status/block disabled (không PATCH self) | ✅ |

---

## 9. Pagination & refresh (P1)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_ULIST_007 | Chuyển trang 2; URL `?page=2` | ✅ |
| TC_AD_ULIST_028 | Đổi `per_page` (URL sync + 14 rows @20) | ✅ |
| TC_AD_ULIST_029 | Summary "Hiển thị X–Y / Z" | ✅ |
| TC_AD_ULIST_030 | Prev/Next disabled; ellipsis `...` | ✅ |
| TC_AD_ULIST_031 | Nút Refresh → refetch list | ✅ |

---

## 10. Stats cards (P1)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_ULIST_032 | 4 thẻ: Tổng / Active / Banned / Admin | ✅ |
| TC_AD_ULIST_033 | Values khớp mock; format locale | ✅ |
| TC_AD_ULIST_052 | Loading state khi fetch chậm | ✅ |
| TC_AD_ULIST_054 | Sau delete → stats giảm (mock recalc) | ✅ |

---

## 11. Export (P1)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_ULIST_008 | Xuất Excel + download | ✅ |
| TC_AD_ULIST_055 | Export áp dụng filter hiện tại | ✅ |
| TC_AD_ULIST_046 | Export disabled khi pending | ✅ |
| TC_AD_ULIST_047 | Toast lỗi khi export fail | ✅ |
| TC_AD_ULIST_047b | PATCH block fail → user vẫn ACTIVE | ✅ |

---

## 12. Dialog UX (P2)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_ULIST_041 | BlockUserDialog: Hủy → không PATCH | ✅ |
| TC_AD_ULIST_042 | BlockUserDialog: cảnh báo amber | ✅ |
| TC_AD_ULIST_059 | DeleteUserDialog: Hủy → không DELETE | ✅ |
| TC_AD_ULIST_044 | UpdateRoleDialog: Hủy khi nâng ADMIN | ✅ |

---

## 13. Auth & security (P0)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_ULIST_014 | Guest → `/login` | ✅ |
| TC_AD_ULIST_021 | User `role=user` → `/login` | ✅ |
| TC_AD_ULIST_018 | SQLi payload an toàn | ✅ |
| TC_AD_ULIST_019 | XSS payload an toàn | ✅ |
| TC_AD_ULIST_020 | User banned không login (API 403) | ✅ |

---

## 14. API smoke (P1–P2)

| ID | Mô tả | Auto |
|----|--------|------|
| API_ULIST_001 | GET list không auth → 401 | ✅ |
| API_ULIST_002 | GET list admin → 200 + stats | ✅ |
| API_ULIST_003 | Filter `q` | ✅ |
| API_ULIST_011 | Filter `q` không phân biệt hoa thường | ✅ |
| API_ULIST_004 | Filter `role=user` | ✅ |
| API_ULIST_005 | Reject `role=staff` → 422 | ✅ |
| API_ULIST_006 | PATCH status active→banned→active | ✅ |
| API_ULIST_007 | PATCH status invalid → 422 | ✅ |
| API_ULIST_008 | PATCH user không tồn tại → 404 | ✅ |
| API_ULIST_009 | GET export không auth → 401 | ✅ |
| API_ULIST_010 | GET export với filter → 200 xlsx | ✅ |

---

## 15. Ghi chú

- Reset filter đã fix race debounce — không ghi lại `q` sau reset.
- Search `q`: `LOWER(full_name|email|username) LIKE` — **không phân biệt hoa thường** (PostgreSQL).
- Nâng ADMIN có dialog; hạ USER không dialog.
- Khác Detail/Edit: List khóa có **BlockUserDialog**; Detail/Edit PATCH trực tiếp.
- Mock `users.mock.ts`: stats recalc sau mutation; flags `exportFail`, `mutationFail`, `listDelayMs`.
- **Chạy:** `npm run test:admin:users` (67 tests)

