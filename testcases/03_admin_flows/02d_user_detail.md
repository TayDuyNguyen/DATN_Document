# Admin — Chi tiết người dùng (User Detail)

**Route:** `/admin/users/detail/:id`  
**API:** `GET /api/v1/admin/users/:id`, `GET .../bookings`, `GET .../ratings`, `PATCH .../role`, `PATCH .../status`, `DELETE .../:id`  
**Source:** `danangtrip-admin/src/pages/Users/UserDetail/`  
**Automation:** `tests/admin/users-detail.spec.ts` · `tests/admin/users-detail-extended.spec.ts` · `tests/api/admin-users-detail.api.spec.ts`  
**POM:** `UserDetailPage.ts`

---

## 1. Phạm vi

| Hạng mục | Chi tiết |
|----------|----------|
| Vai trò | **Admin** only |
| Bookings | GET limit 5 + total count |
| Ratings | GET limit 3 + total count |
| Khóa/mở | PATCH status — **không** BlockUserDialog (khác List) |
| Đổi role | Dialog → PATCH role |
| Xóa | Confirm dialog → DELETE → redirect list (~100ms delay) |
| Self | `isSelf` → disable khóa / đổi role / xóa |

## 2. Tổng quan trạng thái

| Nhóm | Tổng TC | ✅ Auto | ⏳ Backlog |
|------|---------|---------|------------|
| Auth | 2 | 2 | 0 |
| Load & 404 | 3 | 3 | 0 |
| Profile & stats | 6 | 6 | 0 |
| Bookings | 6 | 6 | 0 |
| Ratings | 7 | 7 | 0 |
| Status & role | 11 | 11 | 0 |
| Delete | 4 | 4 | 0 |
| Navigation | 5 | 5 | 0 |
| Self-protection | 1 | 1 | 0 |
| UX / i18n / error | 11 | 11 | 0 |
| **UI subtotal** | **52** | **52** | **0** |
| API smoke | 8 | 8 | 0 |
| **Tổng** | **60** | **60** | **0** |

> **Chạy:** `npm run test:admin:user-detail` → **60 passed** (`--workers=1`)

---

## 3. Auth (P0)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_UDET_007 | Guest → `/login` | ✅ |
| TC_AD_UDET_008 | User `role=user` → `/login` | ✅ |

---

## 4. Load & 404 (P1–P2)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_UDET_001 | Load profile + sections | ✅ |
| TC_AD_UDET_010 | User không tồn tại → 404 UI | ✅ |
| TC_AD_UDET_051 | Loading skeleton khi fetch user detail | ✅ |

---

## 5. Profile & stats (P1–P2)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_UDET_002 | Personal info + stats bookings/spend | ✅ |
| TC_AD_UDET_006 | User mới — zero stats (admin) | ✅ |
| TC_AD_UDET_027 | Stat card **Yêu thích** (`favoritesCount`) | ✅ |
| TC_AD_UDET_028 | Email `mailto:`; avatar ảnh vs initial | ✅ |
| TC_AD_UDET_029 | Field: gender, city, birthdate, created/updated, email verified | ✅ |
| TC_AD_UDET_030 | Account sidebar: role, status, last login | ✅ |

---

## 6. Bookings (P1–P2)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_UDET_003 | 5 booking gần đây, total 10 | ✅ |
| TC_AD_UDET_005 | Link booking row → booking detail | ✅ |
| TC_AD_UDET_017 | Actions: Xem đơn → `bookings?user_id=` | ✅ |
| TC_AD_UDET_019 | Bookings link → browser Back → detail | ✅ |
| TC_AD_UDET_031 | Link **Xem tất cả** khi total > 0 | ✅ |
| TC_AD_UDET_032 | Badge status: pending/confirmed/completed/cancelled | ✅ |

---

## 7. Ratings (P2)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_UDET_004 | Ratings gần đây, total 5 | ✅ |
| TC_AD_UDET_018 | Actions: Xem đánh giá → `ratings?user_id=` | ✅ |
| TC_AD_UDET_020 | Ratings link → browser Back → detail | ✅ |
| TC_AD_UDET_033 | Empty state `no_ratings` | ✅ |
| TC_AD_UDET_034 | Stars, score, comment, status badge | ✅ |
| TC_AD_UDET_035 | Rating gắn **location** (không chỉ tour) | ✅ |
| TC_AD_UDET_036 | Link **Xem tất cả đánh giá** | ✅ |

---

## 8. Status & role (P1–P2)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_UDET_011 | Khóa user active (header/actions) | ✅ |
| TC_AD_UDET_012 | Mở khóa user banned | ✅ |
| TC_AD_UDET_013 | Mở dialog đổi role | ✅ |
| TC_AD_UDET_014 | Nâng role → ADMIN | ✅ |
| TC_AD_UDET_024 | Header badge **status** click toggle (không dialog) | ✅ |
| TC_AD_UDET_023 | Header badge **role** click mở dialog | ✅ |
| TC_AD_UDET_037 | Hạ ADMIN → USER qua dialog | ✅ |
| TC_AD_UDET_038 | Dialog role: Save disabled khi không đổi; cảnh báo nâng admin | ✅ |
| TC_AD_UDET_039 | Dialog role: **Hủy** | ✅ |
| TC_AD_UDET_043 | Sau PATCH → `refetchUser()` cập nhật UI | ✅ |
| TC_AD_UDET_045 | Badge status `pending` (amber) | ✅ |

---

## 9. Delete (P1–P2)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_UDET_015 | Mở dialog xóa + tên user | ✅ |
| TC_AD_UDET_016 | Xóa user → redirect list + toast | ✅ |
| TC_AD_UDET_040 | Dialog cascade warning (bookings, ratings, favorites) | ✅ |
| TC_AD_UDET_041 | Dialog xóa: **Hủy** | ✅ |

---

## 10. Navigation & actions (P1–P2)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_UDET_009 | Self — dangerous actions disabled | ✅ |
| TC_AD_UDET_021 | Header **Chỉnh sửa** → edit | ✅ |
| TC_AD_UDET_022 | Back / breadcrumb → list | ✅ |
| TC_AD_UDET_025 | Actions card: Chỉnh sửa thông tin | ✅ |
| TC_AD_UDET_026 | Actions card: Khóa/mở khóa | ✅ |

---

## 11. UX / i18n / error (P2–P3)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_UDET_042 | `showMutationErrorToast` trên status/role/delete fail | ✅ |
| TC_AD_UDET_044 | `formatAdminShortDate` theo locale | ✅ |
| TC_AD_UDET_007b | Avatar URL lỗi → fallback initial | ✅ (onError) |
| TC_AD_UDET_008b | Long text — break-words header + profile | ✅ (CSS) |
| TC_AD_UDET_012b | Empty bookings riêng user id (staff) | ✅ |
| TC_AD_UDET_046 | API 500 bookings path — hiện ErrorWidget + Thử lại | ✅ |
| TC_AD_UDET_047 | API 500 ratings path — hiện ErrorWidget + Thử lại | ✅ |
| TC_AD_UDET_048 | Refetch cache — assert network | ✅ |
| TC_AD_UDET_049 | Responsive / sticky CSS | ✅ |
| TC_AD_UDET_050 | Full regression flow | ✅ |

---

## 12. API smoke (P1–P2)

| ID | Mô tả | Auto |
|----|--------|------|
| API_UDET_001 | GET detail không token → 401 | ✅ |
| API_UDET_002 | GET detail hợp lệ → 200 | ✅ |
| API_UDET_003 | PATCH status không token → 401 | ✅ |
| API_UDET_004 | GET bookings → 200 / 401 | ✅ |
| API_UDET_005 | GET ratings → 200 / 401 | ✅ |
| API_UDET_006 | DELETE → 200 / 401 | ✅ |
| API_UDET_007 | PATCH role success | ✅ |
| API_UDET_008 | GET detail 404 | ✅ |

---

## 13. Ghi chú

- Khác List: Detail khóa **PATCH trực tiếp**, không BlockUserDialog.
- Mock: `users-detail.mock.ts` — users 1–6, flags `detailDelayMs`, `bookingsFail`, `ratingsFail`, `roleFail`, `statusFail`, `deleteFail`; `shouldRegisterMockRoutes(page, 'users-detail')` từ `tests/helpers/mockRouteOnce.ts`.
- Extended spec: `serial` chỉ trên describe PATCH/DELETE/error — không serial toàn file.
- Bookings/ratings API lỗi: `ErrorWidget` + nút Thử lại (`refetch`), không hiện empty state gây hiểu nhầm.
- A11y: `aria-label` nút back + badge role/status trên header.
- Avatar URL hỏng: `onError` fallback về chữ cái đầu; text dài dùng `break-words`/`break-all`.
- **Chạy:** `npm run test:admin:user-detail`
