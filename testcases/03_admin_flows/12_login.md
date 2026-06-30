# Admin — Đăng nhập (Login)

**Route:** `/login`  
**Source:** `danangtrip-admin/src/pages/Login/`  
**Automation:** `tests/admin/login.spec.ts` · `tests/admin/login-auth.spec.ts`  
**POM:** `LoginPage.ts` · Mock: `login.mock.ts` · Data: `login.data.ts`  
**Chạy test:** `npm run test:admin:login`

---

## 1. Phạm vi

| Hạng mục | Chi tiết |
|----------|----------|
| Vai trò | Guest · Admin · Staff (vào được) · Customer `role=user` (bị chặn) |
| API | `POST /auth/login` (prefix `/api/v1`) |
| UI | Form email/password · Remember me · Forgot password (disabled placeholder) |
| Redirect thành công | `/dashboard` |
| Route guard | `PrivateRoute` guest/non-panel → `/login` · `PublicRoute` panel user → `/dashboard` |

### Lệch doc gốc (đã mapping)

| Doc gốc | Product thực tế |
|---------|-----------------|
| `/admin/login` hoặc `/admin/auth` | **`/login`** |
| `POST /api/auth/admin/login` | **`POST /api/v1/auth/login`** |
| Redirect `/admin/dashboard` | **`/dashboard`** |

### Token storage

| Remember me | Lưu trữ |
|-------------|---------|
| Tắt (mặc định) | Session **cookie** (`access_token`) |
| Bật | **Cookie + localStorage** + `remember_me=true` |

---

## 2. UI Interactive Inventory

| # | Nhãn (i18n) | Loại | Hành vi kỳ vọng | TC | Auto |
|---|-------------|------|-----------------|-----|------|
| 1 | Email | input | Required + email format | 001, 008 | ✅ |
| 2 | Mật khẩu | input password | Required min 6 | 001, 009 | ✅ |
| 3 | Ghi nhớ đăng nhập | checkbox | Token vào localStorage | 007 | ✅ |
| 4 | Quên mật khẩu? | span disabled | Không navigate · title coming soon | 013 | ✅ |
| 5 | ĐĂNG NHẬP | button submit | POST login · loading state | 002–004, 011 | ✅ |
| 6 | Banner lỗi đỏ | inline error | Sai MK / không quyền / server | 002, 004, 012 | ✅ |
| 7 | Toast success/error | toast | Sonner | 003, 012 | ✅ |
| 8 | Route guard guest | redirect | `/dashboard` → `/login` | 005 | ✅ |
| 9 | PublicRoute | redirect | Admin session `/login` → `/dashboard` | 010 | ✅ |

---

## 3. Mapping testcase → automation

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_LOGIN_001 | Form trống → validation | ✅ |
| TC_AD_LOGIN_002 | Sai email/password | ✅ |
| TC_AD_LOGIN_003 | Admin → dashboard + token (cookie) | ✅ |
| TC_AD_LOGIN_004 | Customer bị chặn · token cleared (cookie + LS) | ✅ |
| TC_AD_LOGIN_005 | Guest vào `/dashboard` → login | ✅ |
| TC_AD_LOGIN_006 | Staff login thành công | ✅ |
| TC_AD_LOGIN_007 | Remember me → localStorage token | ✅ |
| TC_AD_LOGIN_008 | Email format invalid · không POST | ✅ |
| TC_AD_LOGIN_009 | Password &lt; 6 · không POST | ✅ |
| TC_AD_LOGIN_010 | Admin đã login mở `/login` → dashboard | ✅ |
| TC_AD_LOGIN_011 | Loading spinner khi POST delay | ✅ |
| TC_AD_LOGIN_012 | API 500 → banner + toast | ✅ |
| TC_AD_LOGIN_013 | Forgot password placeholder disabled | ✅ |

---

## 4. Test cases chi tiết

| ID | Nhóm | Test case | Dữ liệu | Kết quả mong đợi | Ưu tiên |
|----|------|-----------|---------|------------------|---------|
| TC_AD_LOGIN_001 | Validation | Form trống | — | Email + password required | High |
| TC_AD_LOGIN_002 | Auth | Sai thông tin | wrongadmin / 123456 | Banner credentials error | High |
| TC_AD_LOGIN_003 | Auth | Admin OK | admin@danangtrip.vn / Admin123! | Cookie token · `/dashboard` | Critical |
| TC_AD_LOGIN_004 | Auth | Customer chặn | customer@test.com / Customer123! | No permission · no cookie/LS token | High |
| TC_AD_LOGIN_005 | Guard | Guest dashboard | — | Redirect `/login` | Critical |
| TC_AD_LOGIN_006 | Auth | Staff OK | staff@danangtrip.vn / Staff123! | `/dashboard` | Medium |
| TC_AD_LOGIN_007 | UX | Remember me | admin + checkbox | LS token + remember_me=true | Medium |
| TC_AD_LOGIN_008 | Validation | Email invalid | not-an-email | Inline error · no POST | High |
| TC_AD_LOGIN_009 | Validation | Password short | 12345 | Inline min 6 · no POST | High |
| TC_AD_LOGIN_010 | PublicRoute | Already logged in | admin session | Redirect `/dashboard` | High |
| TC_AD_LOGIN_011 | UX | Loading | POST delay 1.5s | Disabled + logging_in text | Medium |
| TC_AD_LOGIN_012 | API | Login 500 | mock fail | Server error banner + toast | High |
| TC_AD_LOGIN_013 | UX | Forgot password | — | aria-disabled span · title hint | Low |

---

## 5. Test data mock

| Record | Mục đích |
|--------|----------|
| `loginCredentials.admin` | 003, 007, 011, 012 |
| `loginCredentials.wrong` | 002 |
| `loginCredentials.customer` | 004 |
| `loginCredentials.staff` | 006 |
| `loginValidationSamples` | 008, 009 |
| `setLoginDelay` / `setLoginApiFail` | 011, 012 |

---

## 6. Improvement backlog

| ID | Loại | Ưu tiên | Phát hiện | Trạng thái |
|----|------|---------|-----------|------------|
| IMP_LOGIN_001 | Doc | P2 | Route `/admin/login` | **fixed** |
| IMP_LOGIN_002 | Doc | P2 | API path admin/login | **fixed** |
| IMP_LOGIN_003 | Doc | P2 | Dashboard path | **fixed** |
| IMP_LOGIN_004 | Bug | P1 | Staff không login được | **fixed** |
| IMP_LOGIN_005 | UX | P3 | Forgot password dead link | **fixed** (disabled span + title) |
| IMP_LOGIN_006 | Test | P3 | Remember me persistence | **fixed** (TC 007) |
| IMP_LOGIN_007 | Test | P2 | Email invalid validation | **fixed** (TC 008) |
| IMP_LOGIN_008 | Test | P2 | Password min validation | **fixed** (TC 009) |
| IMP_LOGIN_009 | Test | P2 | PublicRoute redirect | **fixed** (TC 010) |
| IMP_LOGIN_010 | Test | P2 | Customer token cookie clear | **fixed** (TC 004) |
| IMP_LOGIN_011 | Test | P2 | Loading state | **fixed** (TC 011) |
| IMP_LOGIN_012 | Test | P2 | API 500 error UI | **fixed** (TC 012) |
| IMP_LOGIN_013 | Doc | P3 | Doc ghi chỉ localStorage token | **fixed** (section token storage) |

---

## 7. Ghi chú

- TC guard dashboard trùng `TC_AD_DASH_007` — giữ theo doc login.
- Customer: API 200 → SPA `logout()` → không còn cookie/localStorage token.
- Chạy: `npm run test:admin:login` (**13 tests**).
