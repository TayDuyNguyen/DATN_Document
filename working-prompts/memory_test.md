# Bộ nhớ QA — DanangTrip (repo DATN only)

> **Phạm vi:** File này **chỉ dùng trong repo DATN / DanangTrip**. Khi chuyển sang dự án khác, **không copy** nội dung này — tạo file memory riêng cho project đó.
>
> **Quy tắc trong repo DATN:** Mọi AI / dev khi làm test hoặc Playwright cho `danangtrip-admin` **đọc file này trước**, rồi mới mở `testcases/03_admin_flows/*.md`.
>
> **Prompt Playwright generic:** `playwright_auto_test_generator_prompt.md` — dùng được mọi project (PHASE 0.6 inventory, 0.7 data display). **Chi tiết DanangTrip nằm ở file này**, không nằm trong prompt.

**Cập nhật lần cuối:** 2026-06-16 (Tour Edit 03c đóng; Tour Create 03b đóng; quy ước sticky header collapse mục 3c)  
**Phạm vi đã làm:** User List (`02a`) · User Create (`02b`) · User Edit (`02c`) · User Detail (`02d`) · Tour List (`03a`) · Tour Create (`03b`) · **Tour Edit (`03c`)** · Tour Detail Modal (`03d`) · **Dashboard (`01`)**

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

## 3c. Sticky header thu gọn khi cuộn (BẮT BUỘC cho form dài)

> **Quy tắc user:** Màn admin **form dài** (create/edit) có header `sticky top-0` + breadcrumb + nút action → **phải** áp dụng cơ chế thu gọn khi cuộn giống **Tour Create**, trừ khi màn là detail/read-only ngắn.

### Điều kiện áp dụng (màn “cùng kiểu”)

- Layout `min-h-screen` + nội dung form nhiều section (cuộn trong `<main>` của `MainLayout`)
- Header sticky chứa: breadcrumb (hoặc back), tiêu đề, mô tả phụ, nút Hủy/Lưu hoặc Tạo
- **Không** áp dụng cho: list/table, modal, dashboard card, detail chỉ đọc ngắn

### Reference implementation (chuẩn repo)

**File:** `danangtrip-admin/src/pages/Tours/TourCreate/index.tsx`  
**Test:** `TC_AD_TCREATE_027` — `TourCreatePage.scrollMainContent()` + badge `title.breadcrumb_create`

### Cơ chế kỹ thuật (copy khi làm màn mới)

1. **Scroll container:** `MainLayout` → `<main class="overflow-y-auto">` — **không** lắng nghe `window` scroll trực tiếp.
2. **Listener:** `window.addEventListener('scroll', handler, true)` (capture); trong handler chỉ xử lý khi `e.target.tagName === 'MAIN'` (hoặc có class `overflow-y-auto`).
3. **State `isScrolled`:** `scrollTop > 10` → thu gọn; `scrollTop < 2` → mở rộng (hysteresis tránh giật).
4. **UI khi thu gọn:**
   - Ẩn breadcrumb + subtitle (`opacity-0 h-0 overflow-hidden`)
   - Tiêu đề `text-2xl` → `text-lg`
   - Hiện badge ngữ cảnh (vd. `title.breadcrumb_create` / `breadcrumb_edit`) — `hidden md:inline-flex`
   - Giảm padding header (`py-5` → `py-3`)
   - **Giữ** nút action (Hủy / Lưu / Tạo)
5. **CSS:** `sticky top-0 z-30` (hoặc `z-40`), `transition-all duration-300`, `backdrop-blur`.
6. **Padding full-bleed (đừng quên):** Header + body form dùng **`w-full px-4 sm:px-6 lg:px-10`** — **không** bọc `max-w-[1600px] mx-auto` trong sticky header (Tour Edit từng lệch Create → MarkUp 2026-06-16). Nội dung form và header phải căn cùng một lề ngang.

### Bảng trạng thái màn (cập nhật 2026-06-16)

| Màn | Route / file | Sticky header | Collapse on scroll | Việc cần làm |
|-----|----------------|---------------|-------------------|--------------|
| **Tour Create** | `/admin/tours/create` · `TourCreate/index.tsx` | ✅ | ✅ **chuẩn** | — |
| Tour Edit | `/admin/tours/edit/:id` · `TourEdit/index.tsx` | ✅ | ✅ | — |
| User Create | `/admin/users/create` · `UserCreate/index.tsx` | ✅ | ❌ | Port pattern |
| User Edit | `/admin/users/edit/:id` · `UserEdit/index.tsx` | ✅ | ❌ | Port pattern |
| Blog Post Create | `BlogPostCreate/index.tsx` | ✅ | ❌ | Port pattern |
| Blog Post Edit | `BlogPostEdit/index.tsx` | ✅ | ❌ | Port pattern |
| Location Create | `LocationCreate/index.tsx` | ✅ | ❌ | Port pattern |
| Location Edit | `LocationEdit/index.tsx` | ✅ | ❌ | Port pattern |
| Settings | `Settings/index.tsx` | ✅ | ❌ | Port pattern (nếu form đủ dài) |
| Chatbot | `Chatbot/index.tsx` | ✅ | ❌ | Tùy tab — ưu tiên thấp |
| Booking Detail | `BookingDetail/index.tsx` | ✅ | ❌ | Detail — cân nhắc riêng |
| User Detail | `UserDetailHeader.tsx` | ✅ | ❌ | Detail read-only — **không bắt buộc** |
| Blog Post Detail | `BlogPostDetailHeader.tsx` | ✅ | ❌ | Detail — **không bắt buộc** |

### Playwright (khi test collapse)

```typescript
// POM — cuộn đúng container
await page.locator('main').evaluate((el, y) => { el.scrollTop = y; }, 250);
await expect(page.getByText(/Tạo mới|Create new/i)).toBeVisible(); // badge thu gọn
```

- Trước khi assert: đảm bảo trang **đủ dài** để `scrollTop > 10`.
- Scope badge/tiêu đề trong header sticky, tránh trùng copy body (vd. schedule guide “After creating…”).

### Khi implement màn create/edit mới

1. Copy hook/UX từ `TourCreate` (hoặc tách shared `useMainScrollCollapse` sau).
2. Thêm TC UX: collapse sau scroll + expand khi scroll về đầu.
3. Cập nhật bảng trạng thái mục này.

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
- `TourCreatePage` — form create, upload, itinerary builder; category click `[class*="-control"]`; itinerary placeholder EN `Discover Ba Na`; **`scrollMainContent()`** cho sticky collapse (mục 3c)
- `copy.bulkActivate` / `bulkDeactivate` — regex **anchored** (`^Activate$`) tránh khớp Deactivate
- Mock 12 tour: `tests/fixtures/data/tours.data.ts` + `tours.mock.ts` — flags: `setTourStatsDelay`, `setTourExportFail`, `setFeaturedFailForTour`, `setDeleteFailForTour`, `appendMockTours`
- Filter react-select: click `ancestor div[class*="-control"]` sau `scrollIntoViewIfNeeded` (tránh dummy input ngoài viewport)
- `tourListCopy` bilingual — EN filter labels khác VI (`Hot Tour`, `Hidden`, `Active filters:`)

### Mapper — itinerary (đừng tái phạm)

- UI modal: `item.title` + `item.content`
- DB/seed: `{ time, title, description }` hoặc `{ time, task }`
- Fix: `normalizeItineraryRaw()` trong `tour.mapper.ts` — map `description`→`content`, `task`→`title`, parse JSON string
- Test regression: `TC_AD_TMOD_017b` — `patchMockTour` legacy shape → `listPage.goto()` → assert text

---

## 5c. Product conventions — Admin Tour Create (`03b`)

### Sticky header thu gọn

- **Chuẩn repo** cho mục **3c** — màn form dài create/edit khác port từ đây.
- Khi scroll `<main>`: ẩn breadcrumb + `form.page_subtitle`, thu nhỏ `title.add`, badge `title.breadcrumb_create`.
- TC: `TC_AD_TCREATE_027`.

### API / form (tóm tắt)

| Hạng mục | Chi tiết |
|----------|----------|
| Create | `POST /admin/tours` → redirect edit |
| Upload | `POST /upload/image`, `/upload/images` |
| Submit | Header `form.actions.create_tour` · sidebar `form.actions.submit` |
| Mock flags | `setTourCategoriesBlocked`, `setTourCategoriesDelay`, `setTourCreateDelay` |

**Chạy:** `npm run test:admin:tour-create` — 36 passed, 1 skipped (`API_TCREATE_004b`).

---

## 5d. Product conventions — Admin Tour Edit (`03c`)

### Khác Create

| Hạng mục | Chi tiết |
|----------|----------|
| Update | `PUT /admin/tours/:id` partial (`dirtyFields`) → redirect **list** |
| Categories | `useTourCategoriesQuery('admin')` — cache 30 phút; test lỗi category cần **browser context mới** |
| Slug | Toggle auto/manual + `slug_warning` |
| Departures | List schedules + `ScheduleDeleteDialog`; nút **Thêm lịch** / Add schedule |
| Mobile | Footer cố định `data-tour-mobile-footer` (`md:hidden`) |
| Guard | `UnsavedChangesGuard` + sticky header collapse (port từ Create) |
| ImageGallery | Truyền `errors={errors}` |
| **Layout header** | **`w-full px-4 sm:px-6 lg:px-10`** — **không** `max-w-[1600px] mx-auto` (căn sát lề như Create) |
| Mock flags | `setTourDetailFail/Delay`, `setTourUpdateFail/Delay`, `setScheduleErrorForTour`, `patchMockTour` |

### POM / specs

- `TourEditPage.ts` extends `TourCreatePage` — scope `form .sticky` / `form aside` (tránh trùng sidebar nav)
- Locator busy: `headerSaveOrSavingButton` (label đổi sang Saving khi pending)
- Dialog xóa lịch EN: `Delete this schedule?`

**Chạy:** `npm run test:admin:tour-edit` — **48 passed, 2 skipped** (`API_TEDIT_006`, `API_TEDIT_008`).

---

## 6. Cấu trúc automation hiện tại

```
danangtrip-admin/
  tests/admin/users.spec.ts              # 02a list core
  tests/admin/users-extended.spec.ts     # 02a list extended
  tests/admin/users-create.spec.ts       # 02b
  tests/admin/users-edit.spec.ts         # 02c core
  tests/admin/users-edit-extended.spec.ts # 02c extended
  tests/admin/users-detail.spec.ts       # 02d — 20 TC core
  tests/admin/users-detail-extended.spec.ts # 02d — 32 TC extended
  tests/admin/tours-list.spec.ts         # 03a — 12 TC core
  tests/admin/tours-list-extended.spec.ts # 03a — 53 TC extended
  tests/admin/tours-create.spec.ts       # 03b — 17 TC core
  tests/admin/tours-create-extended.spec.ts # 03b — 19 TC extended
  tests/api/admin-tours-create.api.spec.ts  # 03b — 5 API
  tests/admin/tours-edit.spec.ts         # 03c — 20 TC core (+ 001b)
  tests/admin/tours-edit-extended.spec.ts # 03c — 22 TC extended
  tests/api/admin-tours-edit.api.spec.ts  # 03c — 8 API
  tests/admin/tours-detail-modal.spec.ts # 03d — 26 TC (gồm 017b legacy itinerary)
  tests/api/admin-tours-list.api.spec.ts  # 03a — 18 API
  tests/pages/admin/User*Page.ts
  tests/pages/admin/TourListPage.ts
  tests/pages/admin/TourCreatePage.ts
  tests/pages/admin/TourEditPage.ts
  tests/fixtures/data/tour-edit.data.ts
  tests/fixtures/api/*.mock.ts
  tests/fixtures/data/users.data.ts
  tests/fixtures/data/tours.data.ts
  tests/helpers/mockRouteOnce.ts       # shouldRegisterMockRoutes — mock route 1 lần/page
  scripts/prepush-check.mjs
```

**Mock route-once:** `shouldRegisterMockRoutes(page, mockId)` — cập nhật flags mỗi lần gọi; chỉ `page.route` lần đầu. Áp dụng: `users-detail`, `users-edit`, `users-create`, `tours`. Chưa: `users.mock` (dataset closure).

```bash
npm run test:admin:users
npm run test:admin:user-create
npm run test:admin:user-edit      # 44 passed (--workers=1)
npm run test:admin:user-detail    # 60 passed (--workers=1)
npm run test:admin:tour-list      # 12 passed (--workers=1)
npm run test:admin:tour-create      # 36 passed, 1 skipped (--workers=1)
npm run test:admin:tour-edit        # 48 passed, 2 skipped (--workers=1)
npm run test:admin:tour-detail-modal  # 26 passed (--workers=1)
npm run test:api                  # --workers=1
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
| 1 | Chỉnh sửa thông tin | Link → edit | `TC_AD_UDET_021`, `025` |
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
| Detail `goto` timeout | Ratings chưa load xong (skeleton không có heading) | Chờ `personalInfoCard` + `ratingsCard` sau goto |
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
| Role dialog USER strict | Regex `/USER/i` khớp mô tả admin EN ("user accounts") | `getByRole('button', { name: /^USER\b/i })` |
| Detail mock flake parallel | `usersById` shared + PATCH từ test khác | `test.describe.configure({ mode: 'serial' })` + `resetMockDetailUsers()` |
| Detail mock gọi 2 lần | `page.route` trùng pattern | `shouldRegisterMockRoutes` trong `tests/helpers/mockRouteOnce.ts` |
| View All link strict | 2 link "View All →" bookings + ratings | Scope trong `bookingsCard` / `ratingsCard` ancestor |
| Top tours heading EN | Doc regex `Top tours` ≠ `Top 5 Best Selling Tours` | POM `copy.topTours` bilingual đủ cụm |

---

## 9. Module đã hoàn thành (trạng thái session)

| Module | Doc | Spec | Ghi chú |
|--------|-----|------|---------|
| User List | `02a_user_list.md` | `users.spec.ts` + `users-extended.spec.ts` | **67 passed** (56 UI + 11 API) |
| User Create | `02b_user_create.md` | `users-create.spec.ts` + `users-create-extended.spec.ts` | **38 TC** (30 UI + 8 API) |
| User Edit | `02c_user_edit.md` | `users-edit.spec.ts` + `users-edit-extended.spec.ts` | **40 TC** (32 UI + 8 API) — **44 passed** |
| User Detail | `02d_user_detail.md` | `users-detail.spec.ts` + `users-detail-extended.spec.ts` + API | **52 UI + 8 API — 60 passed** (đóng module) |
| Tour List | `03a_tour_list.md` | `tours-list.spec.ts` + `tours-list-extended.spec.ts` + API | **82/83 auto** (65 UI + 17 API; `API_TLIST_017` skip) — **đóng module** |
| Tour Create | `03b_tour_create.md` | `tours-create.spec.ts` + extended + API | **33/34 auto** (30 UI + 3 API; `API_TCREATE_004b` skip) — **đóng module** |
| Tour Edit | `03c_tour_edit.md` | `tours-edit.spec.ts` + extended + API | **50 TC** (42 UI + 8 API) — **48 passed, 2 skipped** — **đóng module** |
| Tour Detail Modal | `03d_tour_detail_modal.md` | `tours-detail-modal.spec.ts` | 26 UI (017b legacy itinerary); edge + mobile |
| Dashboard | `01_dashboard.md` | `dashboard.spec.ts` + `dashboard-auth.spec.ts` | 29 UI + 2 API smoke; mock `mockDashboardApi` |

**Màn tiếp theo:** áp dụng mục 3 (inventory đủ nút) trước khi đóng module mới.

---

## 10. Checklist trước khi báo “done”

- [ ] Đã đọc `memory_test.md`
- [ ] **Form dài create/edit:** đã áp dụng sticky header collapse (mục 3c) hoặc ghi lý do skip trong doc
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
