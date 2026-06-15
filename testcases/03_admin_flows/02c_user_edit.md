# Admin — Chỉnh sửa người dùng (User Edit)

**Route:** `/admin/users/edit/:id`  
**API:** `GET/PUT /api/v1/admin/users/:id`, `PATCH .../role`, `PATCH .../status`, `DELETE .../:id`  
**Source:** `danangtrip-admin/src/pages/Users/UserEdit/`  
**Automation:** `tests/admin/users-edit.spec.ts` · `tests/admin/users-edit-extended.spec.ts` · `tests/api/admin-users-edit.api.spec.ts`  
**POM:** `UserEditPage.ts`

---

## 1. Phạm vi

| Hạng mục | Chi tiết |
|----------|----------|
| Vai trò | **Admin** only |
| PUT profile | Redirect `/admin/users/detail/:id` + toast |
| PATCH role/status | **Ở lại** trang edit — không redirect |
| Nâng ADMIN | Dialog confirm trước PATCH role |
| Hạ USER | PATCH trực tiếp — không dialog |
| Khóa (Edit) | PATCH trực tiếp — **không** BlockUserDialog (khác List) |
| Hủy | → `/admin/users` (list) |
| username | **Readonly** |
| password | Info box — không sửa tại đây |

## 2. Quy tắc kỹ thuật

| Vấn đề | Quy tắc |
|--------|---------|
| Toggle/radio không hoạt động | role/status gọi **PATCH ngay**; PUT chỉ profile |
| Header Lưu loading | Parent nhận `onSavePendingChange` từ form |
| Ngày sinh ISO | Chuẩn hóa `YYYY-MM-DD` trong `user.mapper.ts` |
| Quick action vs toggle | UI đọc server; `setValue(..., { shouldDirty: false })` |
| Unsaved guard | `common:notices.unsaved_changes_title` — assert heading, không filter dialog `hidden` |
| Breadcrumb Users | Scope `.sticky.top-0` — tránh click sidebar |

## 3. Tổng quan trạng thái

| Nhóm | Tổng TC | ✅ Auto | ⏳ Backlog |
|------|---------|---------|------------|
| Load & auth | 5 | 5 | 0 |
| Profile update | 6 | 6 | 0 |
| Role & status | 6 | 6 | 0 |
| Delete & navigation | 4 | 4 | 0 |
| UX & guards | 8 | 8 | 0 |
| Validation | 3 | 3 | 0 |
| **UI subtotal** | **32** | **32** | **0** |
| API smoke | 8 | 8 | 0 |
| **Tổng** | **40** | **40** | **0** |

**Chạy:** `npm run test:admin:user-edit` → **44 passed** (32 UI + 8 API + 4 auth/self describe overlap counted as separate tests)

---

## 4. Load & auth (P0–P1)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_UEDIT_001 | Preload dữ liệu user | ✅ |
| TC_AD_UEDIT_010 | User không tồn tại → 404 UI | ✅ |
| TC_AD_UEDIT_007 | Guest → `/login` | ✅ |
| TC_AD_UEDIT_008 | User `role=user` → `/login` | ✅ |
| TC_AD_UEDIT_025 | Loading skeleton khi fetch | ✅ |

---

## 5. Profile update (P1)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_UEDIT_002 | Cập nhật họ tên + SĐT → detail | ✅ |
| TC_AD_UEDIT_004 | Email sai format | ✅ |
| TC_AD_UEDIT_005 | Họ tên trống | ✅ |
| TC_AD_UEDIT_006 | Cảnh báo khi đổi email | ✅ |
| TC_AD_UEDIT_013 | Email trùng (422 API) | ✅ |
| TC_AD_UEDIT_030 | Cập nhật birthdate, gender, city | ✅ |
| TC_AD_UEDIT_031 | Phone invalid format | ✅ |
| TC_AD_UEDIT_032 | `full_name` / `city` max length | ✅ |

---

## 6. Role & status (P1–P2)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_UEDIT_003 | Nâng USER → ADMIN (confirm) | ✅ |
| TC_AD_UEDIT_017 | Hạ ADMIN → USER (không dialog) | ✅ |
| TC_AD_UEDIT_011 | Quick action khóa tài khoản | ✅ |
| TC_AD_UEDIT_014 | Toggle status khóa qua PATCH | ✅ |
| TC_AD_UEDIT_016 | Quick action **mở khóa** user banned | ✅ |
| TC_AD_UEDIT_034 | PATCH role/status **không redirect** | ✅ |
| TC_AD_UEDIT_033 | Admin confirm role: **Hủy** | ✅ |

---

## 7. Self-protection (P1–P2)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_UEDIT_009 | Self-edit: role radio disabled | ✅ |
| TC_AD_UEDIT_020 | Self-edit: status toggle disabled | ✅ |
| TC_AD_UEDIT_021 | Self-edit: quick delete ẩn; PATCH cập nhật auth store | ✅ |

---

## 8. Delete & navigation (P2)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_UEDIT_015 | Quick action xóa → dialog → list | ✅ |
| TC_AD_UEDIT_018 | Quick action **Xem hồ sơ** → detail | ✅ |
| TC_AD_UEDIT_019 | Quick action **Xem đơn hàng** → `bookings?user_id=` | ✅ |
| TC_AD_UEDIT_026 | Strip query params list khi vào edit | ✅ |

---

## 9. UX & guards (P2–P3)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_UEDIT_012 | Unsaved guard — chọn **Ở lại** | ✅ |
| TC_AD_UEDIT_029 | Unsaved guard — chọn **Rời trang** | ✅ |
| TC_AD_UEDIT_022 | Username readonly + badge | ✅ |
| TC_AD_UEDIT_023 | Password info box | ✅ |
| TC_AD_UEDIT_024 | Metadata sidebar (join, updated, email verified) | ✅ |
| TC_AD_UEDIT_027 | Spinner role radio / status toggle khi PATCH pending | ✅ |
| TC_AD_UEDIT_028 | Header Lưu disabled + `Đang lưu...` | ✅ |
| TC_AD_UEDIT_036 | Footer submit mobile (`md:hidden`) | ✅ |
| TC_AD_UEDIT_035 | `mapApiErrorMessage` trên PATCH/DELETE lỗi | ✅ |

---

## 10. API smoke (P1–P2)

| ID | Mô tả | Auto |
|----|--------|------|
| API_UEDIT_001 | PUT không token → 401 | ✅ |
| API_UEDIT_002 | PUT full_name hợp lệ → 200 | ✅ |
| API_UEDIT_003 | PUT email trùng → 422 | ✅ |
| API_UEDIT_004 | GET detail không token → 401 | ✅ |
| API_UEDIT_005 | PATCH role → 200 / 401 | ✅ |
| API_UEDIT_006 | PATCH status → 200 | ✅ |
| API_UEDIT_007 | DELETE → 200 / 401 | ✅ |
| API_UEDIT_008 | GET user không tồn tại → 404/422 | ✅ |

---

## 11. Ghi chú

- **Chạy:** `npm run test:admin:user-edit`
- Mock users: id `1` admin (self), `2` staff, `3` customer (default edit), `4` banned, `5` secondary admin (demote TC)
- Mock flags: `detailDelayMs`, `putDelayMs`, `patchDelayMs`, `roleFail`, `statusFail`, `deleteFail`, `putFail`
