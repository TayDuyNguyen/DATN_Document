# Bộ nhớ QA — DanangTrip (repo DATN only)

> **Phạm vi:** File này **chỉ dùng trong repo DATN / DanangTrip**. Khi chuyển sang dự án khác, **không copy** nội dung này — tạo file memory riêng cho project đó.
>
> **Quy tắc trong repo DATN:** Mọi AI / dev khi làm test hoặc Playwright cho `danangtrip-admin` **đọc file này trước**, rồi mới mở `testcases/03_admin_flows/*.md`.
>
> **Prompt Playwright generic:** `playwright_auto_test_generator_prompt.md` — dùng được mọi project (PHASE 0.6 inventory, 0.7 data display). **Chi tiết DanangTrip nằm ở file này**, không nằm trong prompt.

**Cập nhật lần cuối:** 2026-06-15 (User Edit automation hoàn tất)  
**Phạm vi đã làm:** User List (`02a`) · User Create (`02b`) · User Edit (`02c`) · User Detail (`02d`) · Tour List (`03a`) · Tour Create (`03b`) · Tour Detail Modal (`03d`) · **Dashboard (`01`)**

---

## 1. Thứ tự làm việc (workflow)

```
1. Đọc memory_test.md (file này)
2. Đọc test case doc tương ứng (02a–02d…)
3. Audit source code + UI Interactive Inventory (mục 3)
4. **Data Display Integrity** (mục 3b) — trace API→mapper→UI; mock vs seed/DB
5. Gap → tự bổ sung testcase doc + POM + spec (không chờ user MarkUp từng nút)
6. Chạy npm run test:admin:<module> + prepush nếu cần
7. MarkUp / bug mới → fix UI/mapper (nếu có) + test regression + cập nhật 3 nơi: memory + testcase doc + spec
```

**Ba nơi luôn đồng bộ khi có thay đổi:**

| File | Vai trò |
|------|---------|
| `memory_test.md` | Quy ước ngắn, pattern đã chốt, bug đã gặp |
| `testcases/03_admin_flows/02*.md` | Bảng TC + cột Auto ✅ |
| `danangtrip-admin/tests/**` | Playwright thực tế |

---

## 2. Quy ước giao tiếp & git (user)

- Trả lời user **bằng tiếng Việt**.
- Commit message **tiếng Anh**, tối đa **80 ký tự**.
- **Không commit** trừ khi user yêu cầu rõ.
- PowerShell: dùng `;` thay `&&`.

---

## 3. UI Interactive Inventory — test TẤT CẢ nút / link (BẮT BUỘC)

> User yêu cầu: *“test tất cả các nút có trên giao diện; chưa có thì tự bổ sung testcase”* — giống workflow MarkUp User Detail.

**Không được** chỉ implement testcase có sẵn trong doc. Phải quét `src/pages/...` và đảm bảo mỗi control actionable có TC + assert hành vi.

### Quy trình 5 bước

1. **INVENTORY** — Liệt kê button, Link, toggle, dialog actions, link trong bảng
2. **MAP** — Nhãn vi/en, `getByRole`, hành vi (navigate / PATCH / dialog / disabled)
3. **GAP** — So với `02*.md` và `*.spec.ts`
4. **SUPPLEMENT** — Thiếu → thêm row doc + `TC_*` + POM getter + test
5. **VERIFY** — Chạy script test module

### Assert tối thiểu

| Hành vi | Playwright |
|---------|------------|
| Link điều hướng | `toHaveAttribute('href')` + `click` + `toHaveURL` |
| Round-trip (MarkUp hay hỏi) | `goBack()` + về đúng URL detail/list |
| API mutation | `waitForResponse` + status + payload |
| Dialog | visible + confirm/cancel |
| Self / permission | `toBeDisabled()` |
| Hover (MarkUp) | `.hover()` trước click khi cần |

### POM

- Scope theo section: `actionsPanel`, sticky header — không locator global trùng nhãn.
- Object `copy` bilingual ở đầu `*Page.ts` — khớp `public/lang/vi` + `en`.
- **Không** dùng `nth-child` / selector MarkUp raw → map sang `getByRole('link', { name: /…/i })`.
- Tiếng Anh ratings link = **"View Reviews"** (không phải "View ratings").

---

## 3b. Data Display Integrity — dữ liệu phải hiện, không chỉ khung UI (BẮT BUỘC)

> User báo: modal **LỊCH TRÌNH TOUR** có timeline 1–9 nhưng **ô trống**. Test `TC_AD_TMOD_017` vẫn pass vì mock sai shape. Quy tắc generic: `playwright_auto_test_generator_prompt.md` **PHASE 0.7**.

### Quy trình 6 bước

1. **TRACE** — `API response` → `*.mapper.ts` → field component render (`item.title`, `item.content`, …)
2. **SHAPE** — So `tests/fixtures/data/*.data.ts` với `database-seeders/**` (SQL/JSON thật)
3. **GAP** — Ghi alias: `description`→`content`, `task`→`title`, ISO→`YYYY-MM-DD`, JSON string→array
4. **SUPPLEMENT** — Doc thiếu → tự thêm TC (`*_legacy`, `*_empty`, `*_error`) + spec
5. **ASSERT** — List/timeline: **title + body text**; không chỉ `toBeVisible()` container
6. **NEGATIVE** — `null`/`[]`/API lỗi → empty copy hoặc retry — **không** khung rỗng im lặng

### Ba trạng thái UI (mỗi cái một TC)

| Trạng thái | Assert |
|------------|--------|
| Có data | Text từ payload/seed hiện trên màn |
| Không data | `no_data` / `no_schedule` / tương đương |
| API lỗi | Alert + nút retry (nếu có) |

### Pass giả — không được chấp nhận

- Timeline/grid đủ **số ô** nhưng **không có chữ** khi API trả mảng có phần tử
- Mock chỉ dùng shape form admin trong khi DB dùng shape legacy
- Modal mở từ list: patch mock **sau** khi list đã load → phải `goto()` reload

### TC tự sinh khi doc chưa có

| Pattern | Ví dụ |
|---------|--------|
| Canonical | `TC_AD_TMOD_017` — `{day, title, content}` |
| Legacy/seed | `TC_AD_TMOD_017b` — `{time, title, description}` + reload list |
| Empty | `TC_AD_TMOD_018` — itinerary `[]` |
| API error | `TC_AD_TMOD_022` — schedules fail + retry |

---

## 4. MarkUp / Change Request — cách xử lý

1. Map element MarkUp → component React (vd. `UserActionsCard.tsx`, `div.space-y-3`).
2. MarkUp `nth-child` trên `a` **không** khớp DOM (có `<button>` xen giữa) → đếm theo **thứ tự link thực tế** trong source.
3. Phân loại: navigation | API | dialog | hover | round-trip.
4. Sửa product nếu bug thật; luôn thêm/sửa test regression.
5. Cập nhật **memory_test.md** nếu phát hiện pattern mới.

### MarkUp User Detail đã xử lý (session này)

| MarkUp | Element | Fix / TC |
|--------|---------|----------|
| ①② Link actions card | Xem đơn đặt tour, Xem đánh giá | `TC_AD_UDET_017`, `018` — href, hover, click, `user_id` |
| Round-trip “sang trang khác có về được không” | Cùng 2 link | `TC_AD_UDET_019`, `020` — `goBack()` về detail |
| Ratings Back bị kẹt | `RatingsReport` `setSearchParams` | Thêm `{ replace: true }` — tránh 2 entry history |
| Style ghost buttons | `UserActionsCard` | `justify-center` + `text-center` cho hover/căn giữa |

---

## 5. Product conventions — Admin User module

### API (prefix `/api/v1/admin/users`)

| Hành động | Method |
|-----------|--------|
| Profile (form Lưu) | `PUT /:id` |
| Role | `PATCH /:id/role` |
| Status | `PATCH /:id/status` |
| Xóa | `DELETE /:id` |
| Detail + bookings/ratings | `GET /:id`, `GET /:id/bookings`, `GET /:id/ratings` |

### Navigation đã chốt

| Màn | Hành vi |
|-----|---------|
| Edit — Lưu profile (PUT) | Redirect **`/admin/users/detail/:id`** + toast |
| Edit — Hủy | **`/admin/users`** (list), không phải detail |
| Create | Redirect detail sau tạo |
| PATCH role/status (edit) | **Ở lại** edit; gọi API **ngay** (toggle/radio/quick action) |
| Detail — Xóa | DELETE → list (~1s delay) |
| Detail — actions link bookings | `/admin/bookings?user_id={id}` |
| Detail — actions link ratings | `/admin/reports/ratings?user_id={id}` |

### UX / anti-pattern đã fix (đừng tái phạm)

- Toggle/radio **không** chỉ cập nhật form — phải `PATCH` ngay.
- `birthdate` ISO → `YYYY-MM-DD` trong `user.mapper.ts` (`normalizeDateForInput`).
- **Một** `useUserMutations()` — pending form: `onSavePendingChange` lên header.
- PUT profile **không** gửi `role`/`status`.
- Form `noValidate` (Yup thay HTML5).
- Nhãn submit: **Lưu thay đổi** / Save Changes — không phải “Cập nhật”.
- Self: disable khóa / đổi role / xóa; badge YOU/BẠN.
- POM detail heading: `.sticky.top-0 h1.text-xl` (tránh trùng layout).
- `goto()` detail: chỉ chờ `personalInfoCard`, không chờ `ratingsCard` (tránh flake).

---

## 5b. Product conventions — Admin Tour List (`03a`)

### API (prefix `/api/v1/admin/tours`)

| Hành động | Method |
|-----------|--------|
| List + filter/pagination | `GET /admin/tours` |
| Stats (embedded list response) | cùng GET list |
| Status bulk/row | `PATCH /:id/status` |
| Featured / Hot | `PATCH /:id/featured`, `PATCH /:id/hot` |
| Xóa | `DELETE /:id` |
| Export | `GET /export` |
| Categories filter | `GET /tour-categories` |
| Schedules modal | `GET /admin/tour-schedules?tour_id=` |

### UI đã chốt

| Màn | Hành vi |
|-----|---------|
| Status từng dòng | **Không có toggle** — chỉ badge; đổi status qua bulk toolbar |
| Featured/Hot | Switch trên dòng → PATCH ngay |
| Detail | Modal `TourDetailModal` trên list (không route riêng) |
| Modal panel locator | `[id^="headlessui-dialog-panel"]` — outer `[role=dialog]` bị hidden |
| Create / Edit row | Navigate `/admin/tours/create`, `/admin/tours/edit/:id` |

### POM

- `TourListPage` — list + mở modal
- `TourDetailModalPage` — assert trong panel, close X/footer, retry
- `TourCreatePage` — form create, upload, itinerary builder; category click `[class*="-control"]`; itinerary placeholder EN `Discover Ba Na`
- `copy.bulkActivate` / `bulkDeactivate` — regex **anchored** (`^Activate$`) tránh khớp Deactivate
- Mock 12 tour: `tests/fixtures/data/tours.data.ts` + `tours.mock.ts`

### Mapper — itinerary (đừng tái phạm)

- UI modal: `item.title` + `item.content`
- DB/seed: `{ time, title, description }` hoặc `{ time, task }`
- Fix: `normalizeItineraryRaw()` trong `tour.mapper.ts` — map `description`→`content`, `task`→`title`, parse JSON string
- Test regression: `TC_AD_TMOD_017b` — `patchMockTour` legacy shape → `listPage.goto()` → assert text

---

## 6. Cấu trúc automation hiện tại

```
danangtrip-admin/
  tests/admin/users.spec.ts              # 02a list core
  tests/admin/users-extended.spec.ts     # 02a list extended
  tests/admin/users-create.spec.ts       # 02b
  tests/admin/users-edit.spec.ts         # 02c core
  tests/admin/users-edit-extended.spec.ts # 02c extended
  tests/admin/users-detail.spec.ts       # 02d — 20 TC
  tests/admin/tours-list.spec.ts         # 03a — 12 TC
  tests/admin/tours-create.spec.ts       # 03b — 17 TC
  tests/admin/tours-detail-modal.spec.ts # 03d — 26 TC (gồm 017b legacy itinerary)
  tests/api/admin-users-*.api.spec.ts
  tests/api/admin-tours-list.api.spec.ts
  tests/pages/admin/User*Page.ts
  tests/pages/admin/TourListPage.ts
  tests/pages/admin/TourCreatePage.ts
  tests/fixtures/api/*.mock.ts
  tests/fixtures/data/users.data.ts
  tests/fixtures/data/tours.data.ts
  scripts/prepush-check.mjs
```

```bash
npm run test:admin:users
npm run test:admin:user-create
npm run test:admin:user-edit      # 44 passed (--workers=1)
npm run test:admin:user-detail    # 20 passed (--workers=1)
npm run test:admin:tour-list      # 12 passed (--workers=1)
npm run test:admin:tour-create      # 17 passed (--workers=1)
npm run test:admin:tour-detail-modal  # 26 passed (--workers=1)
npm run prepush:check             # cần dev server :5173
```

**Mock:** phải handle đủ endpoint UI gọi; thiếu `PATCH .../role` → test pass giả.  
**Mock shape:** ít nhất 1 record mirror **seed/DB** — không chỉ shape form lý tưởng (xem mục 3b).  
**Auth API test:** username admin từ login response — không hard-code `'admin'`.  
**Radio role:** `.click()` không `.check()` khi có confirm dialog.

---

## 7. User Detail — inventory card Thao tác (`UserActionsCard`)

Thứ tự children trong `div.space-y-3`:

| # | Control | Loại | TC auto |
|---|---------|------|---------|
| 1 | Chỉnh sửa thông tin | Link → edit | (header cũng có; có thể bổ sung round-trip) |
| 2 | Đổi vai trò | button → dialog | `TC_AD_UDET_013`, `014` |
| 3 | Xem đơn đặt tour | Link | `TC_AD_UDET_017`, `019` |
| 4 | Xem đánh giá | Link | `TC_AD_UDET_018`, `020` |
| 5 | Khóa / Mở khóa | button | `TC_AD_UDET_011`, `012` |
| 6 | Xóa tài khoản | button → dialog | `TC_AD_UDET_015`, `016` |

POM getters: `actionsViewBookingsLink`, `actionsViewRatingsLink`, `actionsChangeRoleButton`, …

---

## 8. Lỗi đã gặp & cách xử lý (troubleshooting)

| Triệu chứng | Nguyên nhân | Cách xử lý |
|-------------|-------------|------------|
| Header `isLoading` false khi submit | 2× `useUserMutations()` | `onSavePendingChange` |
| Toggle/radio “không hoạt động” | Chỉ đổi form | PATCH ngay |
| birthdate trống trên edit | ISO chưa normalize | `user.mapper.ts` |
| Lưu edit không sang detail | Navigate sai | `navigate(USERS_DETAIL)` sau PUT |
| Detail `goto` timeout | Chờ ratingsCard | Chỉ chờ `personalInfoCard` |
| Ratings: Back không về detail 1 lần | `setSearchParams` push thêm history | `{ replace: true }` |
| Locator ratings link not found (en) | Regex sai | `View Reviews` không phải `View.*ratings` |
| Delete button vi | Nhãn `Xóa` | POM `/^(Xóa|Delete)$/i` |
| Bulk Activate strict mode | Regex `/Activate/i` khớp cả **Deactivate** | POM `bulkActivate: /^Kích hoạt$|^Activate$/i` |
| Tour list mock flake | `mockAdminLayoutApis` + tours mock xung đột | Gộp notification-counts vào `mockToursApi`; một handler `**/api/v1/**` |
| Search/pagination timeout | Chờ URL thay vì UI | Assert `rowByTourName` + `waitForResponse` khi cần |
| Headless UI modal | `[role=dialog]` strict / invisible | `headlessui-dialog-panel` id |
| Schedule retry EN | Nhãn `Try again` không phải `Retry` | `/Thử lại|Try again/i` |
| Itinerary timeline trống (có số 1–N) | Mock `{day,title,content}`; DB `{time,title,description}`; mapper không map `description` | `normalizeItineraryRaw()` + `TC_AD_TMOD_017b` |
| Test itinerary pass nhưng UI thật trống | Chỉ assert heading mock; không dùng seed shape | Patch mock legacy + reload list + assert title **và** mô tả |
| Modal dùng tour từ list cache | `patchMockTour` sau khi list đã fetch | `patchMockTour` → `listPage.goto()` → mở modal |
| Create xong về list thay vì edit | `extractCreatedTourId` chỉ đọc `res.data.tour`; `unwrapApiData` trả `{ tour: { id } }` | Sửa `extractTourId.ts` — parse `res.tour` trước `res.data` |
| Itinerary POM timeout (EN) | Placeholder EN `e.g., Discover Ba Na Hills` không khớp regex cũ | `getByPlaceholder(/Khám phá Bà Nà\|Discover Ba Na/i)` |
| TC001 thumbnail không có lỗi đỏ | Yup required nhưng `ImageGallery` không render `errors.thumbnail` | Assert các field có DOM error; itinerary assert `p.text-red-500` |
| Create status Hidden vẫn `active` | `onPublish` hardcode `submitWithStatus(data, 'active')` | Dùng `data.status` khi submit |
| Featured/Hot toggle click fail | Checkbox `sr-only`, div peer chặn pointer | Click `label` bọc checkbox |
| Breadcrumb strict mode | Sidebar + main cùng nhãn Tour List | `getByRole('main').getByRole('link')` |
| Dashboard Refresh strict | Regex `/Refresh/i` khớp cả chart refresh | `exportButton.locator('xpath=following-sibling::button[1]')` |
| Unsaved guard dialog hidden | Headless UI `role=dialog` invisible dù `data-open` | Assert `getByRole('heading', { name: /Unsaved Changes|Thay đổi chưa được lưu/i })` |
| Breadcrumb Users click không guard | Click sidebar link cùng nhãn | Scope `.sticky.top-0` cho breadcrumb |
| Skeleton assert fail | Sidebar notification `animate-pulse` | Dùng `.animate-pulse.rounded-lg` (form skeleton) |
| Gender select timeout | react-select combobox ngoài viewport | Scroll section Giới tính + click `[class*="control"]` |
| Role spinner không thấy | Spinner nằm ngoài `user-edit-role-group` | `getByTestId('user-edit-role-group').locator('..').locator('.animate-spin')` |
| API GET user 999999999 | Backend trả 422 thay 404 | Assert `[404, 422].toContain(status)` |
| Top tours / search strict | Tên tour trùng keyword / recent orders | Scope `rounded-[32px]` card; keyword `exact: true` |
| Notification New Contacts strict | Trùng stat card `new-contacts` | Assert `notification-item-contacts` trong popover |
| Top tours heading EN | Doc regex `Top tours` ≠ `Top 5 Best Selling Tours` | POM `copy.topTours` bilingual đủ cụm |

---

## 9. Module đã hoàn thành (trạng thái session)

| Module | Doc | Spec | Ghi chú |
|--------|-----|------|---------|
| User List | `02a_user_list.md` | `users.spec.ts` + `users-extended.spec.ts` | **67 passed** (56 UI + 11 API) |
| User Create | `02b_user_create.md` | `users-create.spec.ts` + `users-create-extended.spec.ts` | **38 TC** (30 UI + 8 API) |
| User Edit | `02c_user_edit.md` | `users-edit.spec.ts` + `users-edit-extended.spec.ts` | **40 TC** (32 UI + 8 API) — **44 passed** |
| User Detail | `02d_user_detail.md` | `users-detail.spec.ts` | 20 UI + 3 API; MarkUp actions + round-trip |
| Tour List | `03a_tour_list.md` | `tours-list.spec.ts` | 12 UI + 2 API; bulk actions |
| Tour Create | `03b_tour_create.md` | `tours-create.spec.ts` | 17 UI; inventory + validation + status/toggles |
| Tour Detail Modal | `03d_tour_detail_modal.md` | `tours-detail-modal.spec.ts` | 26 UI (017b legacy itinerary); edge + mobile |
| Dashboard | `01_dashboard.md` | `dashboard.spec.ts` + `dashboard-auth.spec.ts` | 29 UI + 2 API smoke; mock `mockDashboardApi` |

**Màn tiếp theo:** áp dụng mục 3 (inventory đủ nút) trước khi đóng module mới.

---

## 10. Checklist trước khi báo “done”

- [ ] Đã đọc `memory_test.md`
- [ ] Inventory 100% button/link/toggle trên màn (mục 3)
- [ ] **Data Display Integrity** (mục 3b): mock vs seed, assert text thật, legacy/empty/error TC
- [ ] Doc `02*.md` / `03*.md` cột Auto ✅ khớp spec
- [ ] POM có getter từng control actionable
- [ ] Assert hành vi (không chỉ `toBeVisible`)
- [ ] Navigation round-trip nếu link sang màn khác
- [ ] `npm run test:admin:<module>` pass
- [ ] Cập nhật `memory_test.md` nếu có quy ước / bug mới

---

## 11. Liên kết

- Prompt **generic** (mọi project): `working-prompts/playwright_auto_test_generator_prompt.md`
- Test cases **DATN**: `testcases/03_admin_flows/`
- App: `danangtrip-admin` (Vite `:5173`) · API: `danangtrip-api` (`:8000/api/v1`)
