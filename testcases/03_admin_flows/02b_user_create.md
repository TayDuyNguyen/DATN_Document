# Admin — Tạo người dùng (User Create)

**Route:** `/admin/users/create`  
**API:** `POST /api/v1/admin/users`  
**Source:** `danangtrip-admin/src/pages/Users/UserCreate/`  
**Automation:** `tests/admin/users-create.spec.ts` · `tests/admin/users-create-extended.spec.ts` · `tests/api/admin-users-create.api.spec.ts`  
**POM:** `UserCreatePage.ts`

---

## 1. Phạm vi

| Hạng mục | Chi tiết |
|----------|----------|
| Vai trò | **Admin** only |
| Nút submit | **Tạo người dùng** / Create User |
| Sau tạo thành công | `/admin/users/detail/:id` (fallback `/admin/users` nếu không có `id`) |
| Role | `admin` \| `user` (default: user) — không Staff |
| Status | `active` \| `banned` (default: active) |
| Nâng ADMIN | `CreateAdminConfirmDialog` xác nhận |

## 2. Trường form

| Field | Client (Yup) | Server |
|-------|--------------|--------|
| full_name | required, max 100 | required, max 100 |
| username | required, `[a-z0-9_]+`, max 50 | required, unique, max 50 |
| email | required, email, max 100 | required, unique, max 100 |
| password | required, min 8, complexity | required, min 8 |
| password_confirmation | required, match | — |
| phone | optional, format | optional |
| birthdate, gender, city | optional | optional |
| role, status | optional | optional |

## 3. Tổng quan trạng thái

| Nhóm | Tổng TC | ✅ Auto | ⏳ Backlog |
|------|---------|---------|------------|
| Validation | 12 | 12 | 0 |
| Success flows | 5 | 5 | 0 |
| Auth | 2 | 2 | 0 |
| Navigation & UX | 10 | 10 | 0 |
| Dialog | 1 | 1 | 0 |
| **UI subtotal** | **30** | **30** | **0** |
| API smoke | 8 | 8 | 0 |
| **Tổng** | **38** | **38** | **0** |

---

## 4. Validation (P1–P2)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_UCREATE_001 | Submit form trống → lỗi required | ✅ |
| TC_AD_UCREATE_002 | Email sai format | ✅ |
| TC_AD_UCREATE_005 | Username sai format (ký tự đặc biệt) | ✅ |
| TC_AD_UCREATE_006 | password_confirmation không khớp | ✅ |
| TC_AD_UCREATE_010 | Mật khẩu < 8 ký tự | ✅ |
| TC_AD_UCREATE_010b | Mật khẩu chỉ có số (8+ ký tự) | ✅ |
| TC_AD_UCREATE_011 | Số điện thoại sai format | ✅ |
| TC_AD_UCREATE_003 | Email trùng (422 API) | ✅ |
| TC_AD_UCREATE_009 | Username trùng (422 API) | ✅ |
| TC_AD_UCREATE_015 | `full_name` > 100 ký tự | ✅ |
| TC_AD_UCREATE_016 | `username` > 50 ký tự | ✅ |
| TC_AD_UCREATE_017 | `email` > 100 ký tự | ✅ |
| TC_AD_UCREATE_018 | `city` > 100 ký tự | ✅ |

---

## 5. Success flows (P1–P2)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_UCREATE_004 | Tạo thành công role USER → detail | ✅ |
| TC_AD_UCREATE_008 | Tạo role ADMIN sau dialog confirm | ✅ |
| TC_AD_UCREATE_013 | Tạo user status **banned** (toggle off) | ✅ |
| TC_AD_UCREATE_019 | POST kèm optional fields (phone, birthdate, gender, city) | ✅ |
| TC_AD_UCREATE_020 | Toast `create_success` sau tạo | ✅ |
| TC_AD_UCREATE_021 | API không trả `id` → fallback list | ✅ |

---

## 6. Auth (P0)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_UCREATE_007 | Guest → `/login` | ✅ |
| TC_AD_UCREATE_014 | User `role=user` → `/login` | ✅ |

---

## 7. Navigation & UX (P2–P3)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_UCREATE_012 | Cancel → `/admin/users` | ✅ |
| TC_AD_UCREATE_022 | Admin confirm dialog: **Hủy** / backdrop | ✅ |
| TC_AD_UCREATE_023 | Toggle hiện/ẩn password fields | ✅ |
| TC_AD_UCREATE_024 | Helper text username + password complexity | ✅ |
| TC_AD_UCREATE_025 | Helper card 4 bullet (cảnh báo admin) | ✅ |
| TC_AD_UCREATE_026 | Breadcrumb Danh sách → Tạo mới | ✅ |
| TC_AD_UCREATE_027 | Nút back (ArrowLeft) → list | ✅ |
| TC_AD_UCREATE_028 | Sticky header desktop + footer mobile submit | ✅ |
| TC_AD_UCREATE_029 | 422 → scroll tới field lỗi đầu tiên | ✅ |
| TC_AD_UCREATE_030 | Lỗi API không 422 → toast chung | ✅ |
| TC_AD_UCREATE_031 | Gender options: Nam / Nữ / Khác | ✅ |
| TC_AD_UCREATE_032 | Role card UI: DEFAULT / FULL POWER | ✅ |

---

## 8. API smoke (P1–P2)

| ID | Mô tả | Auto |
|----|--------|------|
| API_UCREATE_001 | POST không token → 401 | ✅ |
| API_UCREATE_002 | Payload thiếu field → 422 | ✅ |
| API_UCREATE_003 | Email trùng → 422 | ✅ |
| API_UCREATE_004 | Username trùng → 422 | ✅ |
| API_UCREATE_005 | POST thành công 201 | ✅ |
| API_UCREATE_006 | POST `status: banned`, `role: admin` | ✅ |
| API_UCREATE_007 | Token non-admin → 403/401 | ✅ |
| API_UCREATE_008 | Password complexity server 422 | ✅ |

---

## 9. Ghi chú

- **Chạy:** `npm run test:admin:user-create`
- **Extended UI:** `tests/admin/users-create-extended.spec.ts` (TC 015–032)
- **Mock flags:** `omitUserId`, `fail500`, `passwordComplexity422` trong `users-create.mock.ts`
- **API 007:** login `customer@test.com` / `Customer123!` — skip nếu API không có seed customer
