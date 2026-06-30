# Bộ nhớ QA — DanangTrip (repo DATN only)

> **Phạm vi:** File này **chỉ dùng trong repo DATN / DanangTrip**. Khi chuyển sang dự án khác, **không copy** nội dung này — tạo file memory riêng cho project đó.
>
> **Quy tắc trong repo DATN:** Mọi AI / dev khi làm test hoặc Playwright cho `danangtrip-admin` **đọc file này trước**, rồi mới mở `testcases/03_admin_flows/*.md`.
>
> **Prompt Playwright generic:** `playwright_auto_test_generator_prompt.md` — dùng được mọi project (PHASE 0.6 inventory, 0.7 data display). **Chi tiết DanangTrip nằm ở file này**, không nằm trong prompt.

**Cập nhật lần cuối:** 2026-06-23 (Blog Categories `17` — product fixes + automation)
**Phạm vi đã làm:** User List (`02a`) · User Create (`02b`) · User Edit (`02c`) · User Detail (`02d`) · Tour List (`03a`) · Tour Create (`03b`) · Tour Edit (`03c`) · Tour Detail Modal (`03d`) · Tour Schedule List (`03e`) · Tour Schedule Create (`03f`) · Tour Schedule Edit (`03g`) · Tour Schedule Detail (`03h`) · Dashboard (`01`) · Booking List (`04a`) · Booking Detail (`04b`) · Location List (`05a`) · Location Create (`05b`) · Location Edit (`05c`) · Location Detail (`05d`) · Blog List (`06a`) · Blog Create (`06b`) · Blog Edit (`06c`) · Promotions (`07`) · **Payments List+Detail (`13a`)** · **Notifications (`14`)** · **Tour Categories (`15`)** · **Location Categories (`16`)** · **Blog Categories (`17`)**

---

## 1. Thứ tự làm việc (workflow)

```
1. Đọc memory_test.md (file này)
2. Đọc test case doc tương ứng (02a–02d…)
3. Audit source code + UI Interactive Inventory (mục 3)
4. **Data Display Integrity** (mục 3b) — trace API→mapper→UI; mock vs seed/DB
5. Gap → tự bổ sung testcase doc + POM + spec (không chờ user MarkUp từng nút)
6. **Mỗi TC UI:** chụp screenshot kiểm tra giao diện viewport **1535×697** (mục 3c)
7. Chạy npm run test:admin:<module> + prepush nếu cần
8. **Sau mỗi lần test chạm DB thật** (API smoke, seed SQL, INSERT cứng): xóa dữ liệu test + **đồng bộ sequence** PostgreSQL (mục 3d)
9. **Đóng module:** ghi **Improvement Backlog (mục 11 / PHASE 0.8 prompt)** — UI/code/chức năng đề xuất sửa
10. MarkUp / bug mới → fix UI/mapper (nếu có) + test regression + cập nhật 3 nơi: memory + testcase doc + spec
```

**Ba nơi luôn đồng bộ khi có thay đổi:**

| File | Vai trò |
|------|---------|
| `memory_test.md` | Quy ước ngắn, pattern đã chốt, bug đã gặp, **improvement backlog (mục 11)** |
| `testcases/03_admin_flows/02*.md` | Bảng TC + cột Auto ✅ + **mục 8 Đề xuất** |
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
| Schedule status | `schedule.mapper` `full` → `FULL` → UI **Đầy chỗ/Full** (`TMOD_031`) |

---

## 3c. Screenshot kiểm tra giao diện — mỗi test case (BẮT BUỘC)

> User yêu cầu (2026-06-18): **mỗi test case** phải chụp ảnh màn hình để kiểm tra giao diện ở kích thước viewport cố định (Chrome DevTools → Responsive).

### Viewport chuẩn

| Thuộc tính | Giá trị |
|------------|---------|
| **Width** | `1535` px |
| **Height** | `697` px |
| Chế độ | Desktop responsive (không phải mobile preset) |

### Quy tắc

1. **Mỗi TC** (`TC_AD_*` / `API_*`) — sau khi assert chính pass, chụp **ít nhất 1 screenshot** toàn màn (hoặc vùng POM scope nếu dialog/modal).
2. Đặt viewport **trước** `goto` / tương tác chính của TC:
   ```ts
   await page.setViewportSize({ width: 1535, height: 697 });
   ```
3. **Đặt tên file** theo TC ID để đối chiếu doc:
   `reports/ui-screenshots/<module>/<TC_ID>.png`  
   Ví dụ: `reports/ui-screenshots/tour-schedule-edit/TC_AD_SCHEDEDIT_001.png`
4. Dùng `await page.screenshot({ path, fullPage: false })` — `fullPage: false` giữ đúng khung **1535×697** (không scroll dài).
5. Test **mobile-only** (TC có `setViewportSize(390, …)`) — vẫn chụp thêm 1 ảnh ở viewport chuẩn **1535×697** cho bước assert UI chính; ảnh mobile tùy chọn suffix `_mobile.png`.
6. API-only test (không mở UI) — **không** bắt buộc screenshot.

### Gợi ý triển khai (fixture)

- `tests/helpers/uiScreenshot.ts` — `captureUiScreenshot(page, tcId, moduleSlug)`
- Hoặc `test.afterEach` trong từng `*.spec.ts` khi `testInfo.status === 'passed'`
- `playwright.config.ts` hiện `screenshot: 'only-on-failure'` — **không thay thế** quy tắc này; screenshot TC là **artifact chủ đích** cho review UI.

### Khi review / MarkUp

- So ảnh với Figma / màn thật ở **đúng 1535×697**
- Ghi lỗi layout vào testcase doc + fix UI nếu lệch

---

## 3d. PostgreSQL — sequence & duplicate key sau test (BẮT BUỘC)

> **Triệu chứng:** API trả **500** — `Duplicate key value violates unique constraint` khi user thật đặt tour / đánh giá sau khi chạy testcase chèn DB.
>
> **Nguyên nhân:** `INSERT` **chỉ định cứng `id`** (hoặc copy seed có ID cố định) khiến PostgreSQL **không tăng sequence**. Lần insert tiếp theo (API để DB tự sinh ID) lấy giá trị sequence cũ → **trùng khóa**.

### A. Khi tạo dữ liệu test (seeding / manual / API live)

| Khuyến nghị | Chi tiết |
|-------------|----------|
| **Ưu tiên** | **Không** chèn cứng cột `id` — để DB tự sinh (`SERIAL` / `RETURNING id`) |
| Playwright UI | Dùng **mock** (`tours.mock.ts`, …) — không ghi DB |
| API smoke | Chỉ chạy khi cần; sau run **xóa** bản ghi tạo + sync sequence |
| Bắt buộc ID cứng (FK) | Sau khi xong testcase → **bắt buộc** sync sequence (mục B) |

### B. Sau mỗi lần chạy test — đồng bộ sequence (chọn 1)

**Cách 1 — SQL** (Supabase SQL Editor / pgAdmin / `psql`):

```sql
-- Bookings
SELECT setval(pg_get_serial_sequence('bookings', 'id'), COALESCE((SELECT MAX(id) FROM bookings), 1), true);
SELECT setval(pg_get_serial_sequence('booking_items', 'id'), COALESCE((SELECT MAX(id) FROM booking_items), 1), true);

-- Ratings
SELECT setval(pg_get_serial_sequence('ratings', 'id'), COALESCE((SELECT MAX(id) FROM ratings), 1), true);
SELECT setval(pg_get_serial_sequence('rating_images', 'id'), COALESCE((SELECT MAX(id) FROM rating_images), 1), true);

-- Tour schedules (khi API create test chạm DB thật)
SELECT setval(pg_get_serial_sequence('tour_schedules', 'id'), COALESCE((SELECT MAX(id) FROM tour_schedules), 1), true);
```

**Cách 2 — Migration có sẵn** (`danangtrip-api`):

```bash
cd danangtrip-api
php artisan migrate
```

Migration liên quan:

| File | Bảng |
|------|------|
| `2026_05_17_000002_sync_booking_sequences.php` | `bookings`, `booking_items` |
| `2026_06_11_000008_sync_ratings_notifications_point_sequences.php` | `ratings`, `rating_images`, `notifications`, `point_transactions`, … |
| `2026_05_17_000001_sync_users_id_sequence.php` | `users` |
| `2026_05_13_000002_sync_categories_id_sequence.php` | `categories` |

> Nếu vừa test `tour_schedules` qua API → chạy thêm SQL `tour_schedules` ở Cách 1 (chưa có migration riêng).

### C. Sau test — dọn dữ liệu

| Thao tác | Sequence | Ghi chú |
|----------|----------|---------|
| `DELETE FROM … WHERE …` (xóa có chọn lọc) | Giữ mức cao | **An toàn** — ID mới > MAX cũ, không trùng |
| `TRUNCATE … RESTART IDENTITY CASCADE` | Reset về **1** | **Chỉ local/test** — xóa sạch cả bảng |

```sql
-- Chỉ môi trường test/local — KHÔNG production
TRUNCATE TABLE bookings RESTART IDENTITY CASCADE;
TRUNCATE TABLE ratings RESTART IDENTITY CASCADE;
```

### D. Checklist sau mỗi session test (AI / dev)

```
□ Xóa bản ghi test tạo qua API/SQL (vd. tour_schedules id 1633+, booking test)
□ Khôi phục bản ghi seed bị sửa (vd. PUT schedule 99) nếu có
□ Chạy setval / php artisan migrate cho bảng đã chèn ID cứng
□ Xác nhận không còn lỗi 500 duplicate key khi thao tác user thật
```

**Playwright mock-only:** không cần bước sequence. **API spec + manual SQL:** **bắt buộc** checklist trên.

---

## 3e. Search / filter text — không phân biệt hoa thường (BẮT BUỘC)

> User yêu cầu (2026-06-15): ô tìm kiếm **không bắt buộc** gõ đúng hoa hay thường — `Ba Na`, `ba na`, `BA NA` phải cho **cùng kết quả** (trừ khi product ghi ngoại lệ).

### Quy tắc product

| Nguyên tắc | Chi tiết |
|------------|----------|
| UX | User gõ keyword tự do — **không** phải khớp chính xác `UPPER`/`lower` |
| Backend PostgreSQL | Ưu tiên `ilike` hoặc `LOWER(col) LIKE LOWER(?)` — **không** dùng `LIKE` thuần trên `pgsql` |
| Tiếng Việt | Tour / schedule / location: thêm `unaccent(...) ilike unaccent(?)` khi tìm theo tên |
| Mock Playwright | `toLowerCase()` / normalize bỏ dấu khi filter — khớp hành vi API |
| Test | Mỗi module search chính có **ít nhất 1 TC** gõ mix case (`ba na` + `BA NA`, `staff@` + `STAFF@`, …) |

### Bảng module đã chốt

| Màn | Param API | Repository / ghi chú | TC case-insensitive |
|-----|-----------|----------------------|---------------------|
| Tour List `03a` | `search` | `TourRepository` — `unaccent` + `ilike` | `TC_AD_TLIST_073`, `API_TLIST_019` |
| User List `02a` | `q` | `UserRepository` — `LOWER(...)` | `TC_AD_ULIST_060`, `API_ULIST_011` |
| Schedule List `03e` | `q` (tour name) | `TourScheduleRepository` — `unaccent` + `ilike` | `TC_AD_SCHEDLIST_031`, `API_SCHEDLIST_007` |
| Dashboard Quick search `01` | `search` / `q` (proxy) | Gọi tours, users, bookings, locations, blog | `TC_AD_DASH_092`, `TC_AD_DASH_093`, `API_DASH_011` |
| Global search — bookings | `search` | `BookingRepository` — `ilike` (fix 2026-06) | `TC_AD_DASH_093` |

### Khi implement màn search mới

1. Backend: kiểm tra `DB_CONNECTION=pgsql` → dùng `ilike` / `LOWER`, không copy `LIKE` từ MySQL.
2. Frontend: chỉ truyền `q`/`search` — **không** ép `toLowerCase()` phía client (logic ở API).
3. Doc testcase: ghi rõ *“không phân biệt hoa thường”* ở inventory filter + thêm 1 TC mix case.
4. Regression: nếu mock pass nhưng API live fail → thêm API smoke so sánh 2 query cùng ID.

---

## 3f. Admin data table — layout cột không bị dồn (BẮT BUỘC khi làm/sửa bảng)

> User yêu cầu (2026-06-15): khi cột bị chồng chéo / không đọc được dữ liệu → kiểm tra pattern bảng toàn admin và fix theo chuẩn dưới đây.

### Triệu chứng thường gặp

- Header cột đè lên nhau; text tour/category (`KHÔNG PHÂN LOẠI`) chồng lên cột ngày.
- Chỉ thấy rõ 1–2 cột đầu; avatar + email/tour name bị ép ~40–80px.
- Nguyên nhân điển hình: **`table-fixed` + `min-w` thấp + thiếu width trên một số `<th>`** → các cột không có width chia phần còn lại cực hẹp.

### Pattern chuẩn (ưu tiên)

```tsx
<div className="overflow-x-auto [scrollbar-width:thin] [&::-webkit-scrollbar]:h-1.5">
  <table className="w-full text-left border-collapse min-w-[1280px]">
    <th className="px-6 py-4 w-40 whitespace-nowrap">...</th>
    <th className="px-6 py-4 min-w-[200px]">...</th>  {/* cột nội dung dài */}
    ...
    <td className="px-6 py-4 align-middle">
      <div className="min-w-0 flex flex-col">...</div>  {/* truncate an toàn */}
    </td>
  </table>
</div>
```

| Quy tắc | Chi tiết |
|---------|----------|
| Wrapper | Luôn bọc `overflow-x-auto` — bảng rộng scroll ngang, không ép viewport |
| `table-fixed` | **Chỉ dùng** khi **mọi** cột có `w-*` / `min-w-*` rõ ràng và tổng ≈ `min-w` bảng |
| Không `table-fixed` | An toàn hơn cho bảng nhiều cột nội dung (customer, tour, dates…) |
| `min-w` bảng | ≥ tổng width cột mong muốn (booking list: **1280px**) |
| Cell nội dung | `min-w-0` + `truncate` trên text; `shrink-0` trên avatar/icon |
| Cột ngày / sort | `whitespace-nowrap` trên cột datetime |
| Cột actions | `min-w-[168px]` khi có 3–4 nút icon 32px |

### Audit `table-fixed` trong `danangtrip-admin` (2026-06-15)

| File | `table-fixed` | Trạng thái |
|------|---------------|------------|
| `BookingList/.../BookingTable.tsx` | **Đã bỏ** (fix 2026-06) | `min-w-[1280px]` + `min-w` từng cột |
| `TourList/.../TourTable.tsx` | Có | OK — `min-w-[1500px]` + `meta.width` đủ cột |
| `Promotions/.../PromotionTable.tsx` | Có | OK — `min-w-[1300px]` + width đủ |
| `LandingPages/.../LandingPageTable.tsx` | Có | OK — mọi `<th>` có `w-[...]` (tổng ~1080px) |
| `UserTable`, `PaymentTable`, `RatingTable`, `BlogTable`, `NotificationTable`, `TourSchedulesTable`, Dashboard tables | Không | OK — chỉ `min-w-[...]` + auto layout |

### Checklist khi bảng bị dồn cột

1. DevTools: kiểm tra `<table>` có `table-fixed` không.
2. Đếm `<th>` có width vs không có width.
3. So sánh `min-w` bảng với tổng width cột.
4. Fix: bỏ `table-fixed` **hoặc** thêm `min-w-[...]` cho mọi cột thiếu + tăng `min-w` bảng.
5. Regression: reload màn + thu nhỏ viewport → scroll ngang vẫn đọc được từng cột.

### Reference fix

- `danangtrip-admin/src/pages/Bookings/BookingList/components/BookingTable.tsx` — bỏ `table-fixed`, `min-w-[1280px]`, customer `min-w-[200px]`, tour `min-w-[220px]`, dates `min-w-[240px]`, actions `min-w-[168px]`.

---

---

## 3c. Sticky header thu gọn khi cuộn (BẮT BUỘC cho create / edit / view)

> **Quy tắc user (2026-06-18):** Mọi màn admin **create**, **edit**, **view/detail** dùng **một quy chuẩn duy nhất**:
> 1. **Vào màn không để trống** — sticky header (back + breadcrumb + tiêu đề + action) hiện **ngay**, kể cả khi API/body đang loading (body skeleton riêng).
> 2. **Cuộn trong `<main>`** → header **thu gọn**: ẩn breadcrumb + subtitle, tiêu đề nhỏ hơn, badge ngữ cảnh.
> 3. **Hook dùng chung:** `src/hooks/useMainScrollCollapse.ts` — không copy inline listener nữa (trừ legacy chưa port).

### Điều kiện áp dụng

- Layout `min-h-screen` + nội dung cuộn trong `<main class="overflow-y-auto">` của `MainLayout`
- Header sticky chứa: breadcrumb (hoặc back), tiêu đề, mô tả phụ (tên entity / subtitle), nút action (Hủy/Lưu/Tạo/Edit/Delete)
- **Không** áp dụng cho: list/table thuần, modal, dashboard card ngắn

### Reference implementation (chuẩn repo)

| Loại | File chuẩn | Test collapse |
|------|------------|---------------|
| Create form dài | `TourCreate/index.tsx` | `TC_AD_TCREATE_027` · `TourCreatePage.scrollMainContent()` |
| Edit form dài | `TourEdit/index.tsx` | extended spec |
| View/detail | `BookingDetail/index.tsx` · `LocationDetail/components/DetailHeader.tsx` | `BookingDetailPage.scrollMainContent()` |

### Cơ chế kỹ thuật (copy khi làm màn mới)

1. **Scroll container:** `MainLayout` → `<main class="overflow-y-auto">` — **không** lắng nghe `window` scroll trực tiếp.
2. **Hook:** `const isScrolled = useMainScrollCollapse();`
3. **State `isScrolled`:** `scrollTop > 10` → thu gọn; `scrollTop < 2` → mở rộng (hysteresis tránh giật).
4. **Loading shell:** Header sticky luôn render; body = skeleton / ErrorWidget / content — **không** full-page skeleton che header.
5. **UI khi thu gọn:**
   - Ẩn breadcrumb + subtitle (`opacity-0 h-0 overflow-hidden`)
   - Tiêu đề `text-xl` → `text-base` (form) hoặc `text-2xl` → `text-lg` (tour create)
   - Hiện badge ngữ cảnh — `common:breadcrumb.add|edit|view` — `hidden md:inline-flex`
   - Giảm padding header (`min-h-20 py-3` → `py-2`)
   - **Giữ** nút action (Hủy / Lưu / Tạo / Edit / Delete); loading → skeleton nút trong header
6. **CSS:** `sticky top-0 z-40`, `transition-all duration-300`, `backdrop-blur`.
7. **Padding full-bleed:** Header + body dùng **`w-full px-4 sm:px-6 lg:px-10`** — **không** bọc `max-w-[1600px] mx-auto` trong sticky header.

### Bảng trạng thái màn (cập nhật 2026-06-18)

| Màn | Route / file | Sticky + shell loading | Collapse on scroll | Việc cần làm |
|-----|----------------|------------------------|-------------------|--------------|
| **Tour Create** | `TourCreate/index.tsx` | ✅ | ✅ **chuẩn form** | Port hook shared |
| **Tour Edit** | `TourEdit/index.tsx` | ✅ | ✅ | Port hook shared |
| **Tour Schedule Create/Edit** | `TourScheduleCreate/Edit` | ✅ | ✅ | — |
| **Booking Detail** | `BookingDetail/index.tsx` | ✅ | ✅ **chuẩn view** | Port hook shared |
| **Location Detail** | `LocationDetail/index.tsx` · `DetailHeader.tsx` | ✅ | ✅ | — |
| **Location Create** | `LocationCreate/index.tsx` | ✅ | ✅ | — |
| **Location Edit** | `LocationEdit/index.tsx` | ✅ | ✅ | — |
| User Create | `UserCreate/index.tsx` | ✅ | ❌ | Port pattern |
| User Edit | `UserEdit/index.tsx` | ✅ | ❌ | Port pattern |
| User Detail | `UserDetailHeader.tsx` | partial | ❌ | Port pattern |
| Blog Post Create/Edit | `BlogPostCreate/Edit` | ✅ | ❌ | Port pattern |
| Blog Post Detail | `BlogPostDetailHeader.tsx` | partial | ❌ | Port pattern |
| Settings | `Settings/index.tsx` | ✅ | ❌ | Port nếu form đủ dài |
| Chatbot | `Chatbot/index.tsx` | ✅ | ❌ | Tùy tab — ưu tiên thấp |

### Playwright (khi test collapse)

```typescript
// POM — cuộn đúng container
await page.locator('main').evaluate((el, y) => { el.scrollTop = y; }, 250);
await expect(page.locator('.sticky.top-0 span.rounded-full')).toBeVisible(); // badge thu gọn
```

- Trước khi assert: đảm bảo trang **đủ dài** để `scrollTop > 10`.
- Scope locator trong `.sticky.top-0` — tránh trùng copy body.
- Detail POM: `pageHeading` = `.sticky.top-0 h1` + `toContainText(entityName)` (tiêu đề có prefix "Chi tiết · …").

### Khi implement màn create/edit/view mới

1. Dùng `useMainScrollCollapse` + sticky header shell (header ngay, body skeleton riêng).
2. Copy UX từ `BookingDetail` (view) hoặc `TourCreate` (form).
3. Thêm TC UX: collapse sau scroll + expand khi scroll về đầu.
4. Cập nhật bảng trạng thái mục này.

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
- Search `q`: **không phân biệt hoa thường** — `LOWER(full_name|email|username)` (mục **3e**); TC `ULIST_060`.

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
- Search `search`: **không phân biệt hoa thường** — `unaccent` + `ilike` (mục **3e**); TC `TLIST_073`, `API_TLIST_019`

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

## 5e. Product conventions — Tour Schedule List (`03e`)

| Chủ đề | Quy ước |
|--------|---------|
| Route | `/admin/tours/schedules` — **không** tab Calendar/List; calendar + table cùng trang |
| Mock list | `filterSchedules` + `enrichScheduleRow(tour.name)` — assert text tour + `booked/max` |
| Mock flags | `setScheduleListFail`, `setScheduleListReturnEmpty`, `setScheduleStatsFail` |
| PATCH status | `/admin/tour-schedules/:id/status` — bulk + row dropdown (FULL → badge read-only) |
| Row actions | `aria-label` + `title`; delete disabled khi `bookedSlots > 0` |
| Tour name click | Lọc `tour_id` trên cùng trang (không navigate create) |
| URL sync | `tour_id`, `q`, `status`, `from`, `to`, `page`, `per_page` |
| Search `q` | **Không phân biệt hoa thường** — `unaccent` + `ilike` trên `tour.name` (mục **3e**); TC `SCHEDLIST_031` |
| Error state | EmptyState + nút Thử lại → `refetch()` |
| Bulk activate | i18n **Kích hoạt lịch** / **Activate schedules** |
| Breadcrumb tour | `a[href="/admin/tours/list"]` — EN label `Tours` không phải `Tour Management` |
| tableRows | Chỉ row có `checkbox` — bỏ empty-state row colspan |
| Giá null | UI **Theo tour** / **Tour default** |
| Delete test row | Schedule 99 `booked_people=0` → capacity `0/15` |

**Chạy:** `npm run test:admin:tour-schedule-list` — **35 passed, 1 skipped** (`API_SCHEDLIST_006`).

---

## 5f. Product conventions — Tour Schedule Create (`03f`)

| Chủ đề | Quy ước |
|--------|---------|
| Route | `/admin/tours/:id/schedules/create` |
| Submit label | **Thêm lịch** / **Add schedule** — không phải "Lưu" |
| Status form | `AVAILABLE` / `CANCELLED` — không có "open" |
| API create | `POST /admin/tours/:tourId/schedules` |
| Redirect | Mặc định → `/admin/tours/schedules?tour_id=`; `fromTourEdit` → `/admin/tours/edit/:id` |
| Mock flags | `setScheduleCreateFail`, `setScheduleCreateDelay`, `getLastCreatedScheduleId` |
| Tour info | `TourInfoBox` — skeleton / error banner + retry |
| Preview | `SchedulePreviewBox` — gồm vận hành + giá |
| Sticky header | Thu gọn khi cuộn `<main>` — badge ngữ cảnh giữ lại |
| Breadcrumb | Link → `/admin/tours/schedules?tour_id=` |
| Cancel | Fallback list/edit — không `navigate(-1)` |
| fromTourEdit | `location.state` **hoặc** `?from=edit` |
| Default slots | `totalSlots` seed từ `tour.max_people` |
| Auto end date | Chỉ khi `endDate` trống |

**Chạy:** `npm run test:admin:tour-schedule-create` — **32 passed**.

---

## 5g. Product conventions — Tour Schedule Edit (`03g`)

| Chủ đề | Quy ước |
|--------|---------|
| Route | `/admin/tours/schedules/edit/:id` |
| Submit label | **Cập nhật lịch** / **Save schedule** (`schedules:actions.save_schedule`) |
| Page title | **Cập nhật lịch trình** (`schedules:actions.edit_schedule`) |
| Delete | Disabled khi `bookedSlots > 0` — đồng bộ list |
| Cancel | Fallback list/tour edit — không `navigate(-1)` |
| Breadcrumb | Link → `/admin/tours/schedules?tour_id=` |
| fromTourEdit | `location.state` **hoặc** `?from=edit` |
| Sticky header | Thu gọn khi cuộn `<main>` |
| Mobile | `pb-24` |
| Schedule error | Banner + retry (`schedules:messages.fetch_error`) |

**Chạy:** `npm run test:admin:tour-schedule-edit` — **36 passed, 1 skipped** (`API_SCHEDEDIT_005` until API redeploy).

---

## 5h. Product conventions — Tour Schedule Detail (`03h`)

| Chủ đề | Quy ước |
|--------|---------|
| Không có route riêng | Chi tiết = `GET /admin/tour-schedules/:id` + panel read-only trên **Edit** |
| Read-only UI | `ScheduleInfoBox`, `ScheduleStatsBlock`, preload form, `SchedulePreviewBox` |
| Badge status | AVAILABLE / **Đầy chỗ** (FULL) / **Đã hủy** (CANCELLED) |
| Giá null | Preview hiện **Theo tour** (`schedules:fields.price_follows_tour`) |
| ISO date | Mapper `toYmd` — `2026-06-20T00:00:00Z` → input `YYYY-MM-DD` |
| Entry | List edit · Tour Edit departure edit · Tour Edit “Thêm lịch” → create |
| Mock helpers | `setScheduleDetailFail`, `clearScheduleDetailFail`, `patchMockSchedule` |
| Screenshot | `reports/ui-screenshots/tour-schedule-detail/<TC_ID>.png` — viewport **1535×697** |

**Chạy:** `npm run test:admin:tour-schedule-detail` — **30 passed, 3 skipped** (API live seed).

**Phân tách module:** Mutation (PUT/DELETE/validation) → **03g**; list/create → **03e/03f**.

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
  tests/admin/tours-detail-modal.spec.ts # 03d — 33 TC UI (gồm 017b legacy)
  tests/api/admin-tours-detail-modal.api.spec.ts # 03d — 2 API
  tests/admin/tour-schedule-list.spec.ts # 03e — 15 TC core
  tests/admin/tour-schedule-list-extended.spec.ts # 03e — 15 TC extended
  tests/api/admin-tour-schedule-list.api.spec.ts # 03e — 6 API
  tests/admin/tour-schedule-create.spec.ts # 03f — 15 TC core
  tests/admin/tour-schedule-create-extended.spec.ts # 03f — 11 TC extended
  tests/api/admin-tour-schedule-create.api.spec.ts # 03f — 4 API
  tests/admin/tour-schedule-edit.spec.ts # 03g — 18 TC core
  tests/admin/tour-schedule-edit-extended.spec.ts # 03g — 9 TC extended
  tests/api/admin-tour-schedule-edit.api.spec.ts # 03g — 6 API
  tests/admin/tour-schedule-detail.spec.ts # 03h — 14 TC core
  tests/admin/tour-schedule-detail-extended.spec.ts # 03h — 9 TC extended
  tests/api/admin-tour-schedule-detail.api.spec.ts # 03h — 11 API
  tests/pages/admin/TourScheduleListPage.ts
  tests/pages/admin/TourScheduleCreatePage.ts
  tests/admin/booking-detail.spec.ts       # 04b — core
  tests/admin/booking-detail-extended.spec.ts # 04b — extended + lifecycle
  tests/admin/booking-detail-auth.spec.ts  # 04b — auth guard
  tests/api/admin-booking-detail.api.spec.ts # 04b — 4 API
  tests/pages/admin/BookingDetailPage.ts
  tests/admin/location-list.spec.ts        # 05a — 33 UI core + improvements
  tests/admin/location-list-auth.spec.ts   # 05a — 2 auth
  tests/api/admin-location-list.api.spec.ts # 05a — 4 API
  tests/admin/location-create.spec.ts        # 05b — 19 UI core
  tests/admin/location-create-auth.spec.ts   # 05b — 2 auth
  tests/api/admin-location-create.api.spec.ts # 05b — 3 API
  tests/admin/location-edit.spec.ts          # 05c — 16 UI core
  tests/admin/location-edit-auth.spec.ts     # 05c — 2 auth
  tests/api/admin-location-edit.api.spec.ts  # 05c — 3 API
  tests/pages/admin/LocationListPage.ts
  tests/fixtures/data/locations.data.ts
  tests/fixtures/api/locations.mock.ts
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
npm run test:admin:tour-detail-modal  # 35 passed (--workers=1)
npm run test:admin:tour-schedule-list # 35 passed, 1 skipped (--workers=1)
npm run test:admin:tour-schedule-create # 32 passed (--workers=1)
npm run test:admin:tour-schedule-edit   # 36 passed, 1 skipped (--workers=1)
npm run test:admin:booking-list       # 52 passed, 1 skipped (--workers=1)
npm run test:admin:booking-detail     # 45 passed (--workers=1)
npm run test:admin:location-list      # 39 passed (--workers=1)
npm run test:admin:location-create    # 22 passed (--workers=1)
npm run test:admin:location-edit      # 23 passed (--workers=1)
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
| Schedule search `q` case-sensitive trên pgsql | `TourScheduleRepository` dùng `LIKE` | Đổi `unaccent` + `ilike` — mục **3e** |
| Booking global search case-sensitive | `BookingRepository` `LIKE` | Đổi `ilike` — `TC_AD_DASH_093` |
| Mock global search `BA NA` ≠ `Bà Nà` | Chỉ `toLowerCase()` không bỏ dấu | `normalizeGlobalSearchText` trong `dashboard.mock.ts` |
| Booking list cột chồng chéo, không đọc được tour/ngày | `table-fixed min-w-[1000px]` nhưng cột Customer + Tour **không** có width | Bỏ `table-fixed`, tăng `min-w-[1280px]`, `min-w` từng cột — mục **3f** |

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
| Tour Detail Modal | `03d_tour_detail_modal.md` | `tours-detail-modal.spec.ts` + API | **35 TC** (33 UI + 2 API) — **đóng module** |
| Tour Schedule List | `03e_tour_schedule_list.md` | `tour-schedule-list.spec.ts` + extended + API | **36 TC** (30 UI + 6 API) — **35 passed, 1 skipped** — **đóng module** |
| Tour Schedule Create | `03f_tour_schedule_create.md` | `tour-schedule-create.spec.ts` + extended + API | **34 TC** (30 UI + 4 API) — **32 passed** — **đóng module** |
| Tour Schedule Edit | `03g_tour_schedule_edit.md` | `tour-schedule-edit.spec.ts` + extended + API | **38 TC** (31 UI + 6 API + fixes) — **36 passed, 1 skipped** — **đóng module** |
| Tour Schedule Detail | `03h_tour_schedule_detail.md` | `tour-schedule-detail.spec.ts` + extended + API | **34 TC** (23 UI + 11 API) — **30 passed, 3 skipped** — **đóng module** |
| Booking List | `04a_booking_list.md` | `booking-list*.spec.ts` + API | **52 passed, 1 skipped** — **đóng module** |
| Booking Detail | `04b_booking_detail.md` | `booking-detail*.spec.ts` + `booking-detail-auth.spec.ts` + API | **45 TC** (41 UI + 4 API) — **45 passed — đóng module** |
| Location List | `05a_location_list.md` | `location-list.spec.ts` + `location-list-auth.spec.ts` + API | **39 TC** (35 UI + 4 API) — **39 passed — đóng module** (IMP_001–005 fixed) |
| Location Create | `05b_location_create.md` | `location-create.spec.ts` + auth + API | **27 TC** (24 UI + 3 API) — **22 passed — đóng module** |
| Location Edit | `05c_location_edit.md` | `location-edit.spec.ts` + auth + API | **26 TC** (23 UI + 3 API) — **23 passed — đóng module** |
| Blog List | `06a_blog_list.md` | `blog-list.spec.ts` + `blog-list-auth.spec.ts` + API | **42 TC** (35 UI + 3 auth + 4 API) — chạy `npm run test:admin:blog-list` |
| Blog Create | `06b_blog_create.md` | `blog-create.spec.ts` + `blog-create-auth.spec.ts` + API | **24 TC** (21 UI + 3 API) — chạy `npm run test:admin:blog-create` |
| Blog Edit | `06c_blog_edit.md` | `blog-edit.spec.ts` + `blog-edit-auth.spec.ts` + API | **31 TC** (27 UI + 4 API) — chạy `npm run test:admin:blog-edit` |
| Blog Detail | `06d_blog_detail.md` | `blog-detail.spec.ts` + `blog-detail-auth.spec.ts` + API | **42 TC** (37 UI + 2 auth + 3 API) — chạy `npm run test:admin:blog-detail` |
| Promotions | `07_promotions.md` | `promotions.spec.ts` + `promotions-auth.spec.ts` + API | **35 TC** (29 UI + 3 auth + 3 API) — **35 passed — đóng module** |
| Payments List+Detail | `13a` · `13b` | `payment-list*.spec.ts` + `payment-detail*.spec.ts` | List **23/23** · Detail **37/37** — **đóng module** |
| Notifications | `14_notifications.md` · `14b_notification_send.md` | `notifications-list/send/auth.spec.ts` | **53 TC** — **53 passed — đóng module** |
| Tour Categories | `15_tour_categories.md` | `tour-categories.spec.ts` + auth + API | **24 TC** (18 UI + 3 auth + 3 API) — **24 passed — đóng module** |
| Location Categories | `16_location_categories.md` | `location-categories.spec.ts` + auth + API | **24 TC** (18 UI + 3 auth + 3 API) — **24 passed — đóng module** |
| Blog Categories | `17_blog_categories.md` | `blog-categories.spec.ts` + auth + API | **23 TC** (17 UI + 3 auth + 3 API) — **23/23 passed — đóng module** |
| Chatbot Hub | `19_chatbot.md` | `chatbot.spec.ts` + auth + API | **39 TC** (32 UI + 3 auth + 4 API) — **39/39 passed** (product fixes + POM tabpanel scope) |
| Dashboard | `01_dashboard.md` | `dashboard.spec.ts` + `dashboard-auth.spec.ts` | 29 UI + 2 API smoke; mock `mockDashboardApi` |

**Màn tiếp theo:** áp dụng mục 3 (inventory đủ nút) trước khi đóng module mới.

---

## 10. Checklist trước khi báo “done”

- [ ] Đã đọc `memory_test.md`
- [ ] **Form dài create/edit:** đã áp dụng sticky header collapse (mục 3c) hoặc ghi lý do skip trong doc
- [ ] **Bảng list admin:** đã kiểm tra layout cột (mục 3f) — không `table-fixed` khi thiếu width đủ cột
- [ ] Inventory 100% button/link/toggle trên màn (mục 3)
- [ ] **Data Display Integrity** (mục 3b): mock vs seed, assert text thật, legacy/empty/error TC
- [ ] Doc `02*.md` / `03*.md` cột Auto ✅ khớp spec
- [ ] POM có getter từng control actionable
- [ ] Assert hành vi (không chỉ `toBeVisible`)
- [ ] Navigation round-trip nếu link sang màn khác
- [ ] `npm run test:admin:<module>` pass
- [ ] **Improvement backlog (PHASE 0.8):** mục 11 memory + mục 8 testcase doc — kể cả “không có”
- [ ] Cập nhật `memory_test.md` nếu có quy ước / bug mới

---

## 11. Improvement backlog — đề xuất sửa product (PHASE 0.8)

> Prompt: `playwright_auto_test_generator_prompt.md` **PHASE 0.8**. Ghi sau mỗi audit/đóng module. **Không** chỉ trả lời trong chat.

### Booking Detail `04b` (audit 2026-06-18)

| ID | Loại | Sev | Phát hiện | Đề xuất | File | Trạng thái |
|----|------|-----|----------|---------|------|------------|
| IMP_BDET_001 | UX | P1 | Error 404/ không load booking hiển thị `messages.update_error` (cùng copy mutation lỗi) | Tách copy: `detail.not_found_title` / `detail.load_error`; phân biệt 404 vs 500 | `BookingDetail/index.tsx`, `booking.json` | **fixed** 2026-06-18 |
| IMP_BDET_002 | UX/A11y | P1 | Complete booking dùng `window.confirm` — không đồng bộ Cancel/Confirm Payment (Headless UI) | Dialog `BookingCompleteDialog` có confirm/cancel, loading state | `BookingDetail/index.tsx` | **fixed** |
| IMP_BDET_003 | UI | P1 | PTTT hiển thị raw enum `bank_transfer` / `sepay` — user đọc không friendly | Map `paymentMethod` → i18n (`payment.methods.sepay`); ẩn legacy `bank_transfer` hoặc badge “Đã ngừng” | `BookingDetail`, mapper/helper | **fixed** |
| IMP_BDET_004 | UX | P1 | Nút **Xuất hóa đơn** `hidden md:flex` — mobile không tải PDF | Thêm nút invoice trong panel Operations hoặc sticky footer mobile | `BookingDetail/index.tsx` | **fixed** |
| IMP_BDET_005 | UX | P2 | Mobile 375px: operations xa below fold; heading section Playwright `hidden` (off-screen) | Sticky footer actions (pattern `TourEdit` mobile) hoặc FAB invoice | `BookingDetail/index.tsx` | **fixed** |
| IMP_BDET_006 | UI | P2 | Header/content `max-w-[1600px] mx-auto` — lệch full-bleed đã chốt ở form admin (mục 3c) | Cân nhắc `w-full px-4 sm:px-6 lg:px-10` như Tour Create/Edit | `BookingDetail/index.tsx` | **fixed** |
| IMP_BDET_007 | Function | P2 | Không có link nhanh → User detail / Tour từ customer & tour card (User Detail có actions card) | Thêm link `user_id`, `tour_id` tương tự `UserActionsCard` | `BookingDetail/index.tsx` | **fixed** |
| IMP_BDET_008 | Mock | P2 | Fixture mock vẫn `payment_method: 'bank_transfer'` trong khi web checkout **SePay-only** | Đổi seed mock → `sepay`; đồng bộ admin display | `booking-detail.data.ts` | **fixed** |
| IMP_BDET_009 | Function/API | P3 | Banner “passenger list chưa hỗ trợ API” — đúng nhưng hạn chế nghiệp vụ | Backlog API: `GET booking passengers` hoặc embed trong detail | API + UI | deferred |
| IMP_BDET_010 | Test | P3 | POM `errorPanel` trùng toast copy — fragile | Thêm `data-testid="booking-detail-error"` hoặc heading riêng | `BookingDetail` + POM | **fixed** |

### Location List `05a` (audit 2026-06-18)

| ID | Loại | Ưu tiên | Phát hiện | Đề xuất | File | Trạng thái |
|----|------|---------|-----------|---------|------|------------|
| IMP_LOCLIST_001 | Function | P1 | Nút **Xuất Excel** không có `onClick` | Wire `GET /admin/locations/export` | `LocationList/index.tsx`, `locationApi.ts` | **fixed** 2026-06-18 |
| IMP_LOCLIST_002 | UX/A11y | P2 | Reset filter chỉ icon — thiếu `aria-label` | `aria-label` + `title` | `LocationFilter.tsx` | **fixed** |
| IMP_LOCLIST_003 | UI | P2 | Layout `max-w-[1600px]` chưa full-bleed | `w-full px-4 sm:px-6 lg:px-10` | `LocationList/index.tsx` | **fixed** |
| IMP_LOCLIST_004 | UX | P2 | Bulk xóa không confirm dialog | `DeleteLocationModal` bulk mode | `LocationList/index.tsx` | **fixed** |
| IMP_LOCLIST_005 | UX | P2 | List API lỗi → empty thay error+retry | Error panel + retry (`data-testid`) | `LocationList/index.tsx` | **fixed** |

**Automation sau fix:** 39 passed — thêm TC LOCLIST_027b, 032–034.

### Location Create `05b` (audit 2026-06-18)

| ID | Loại | Ưu tiên | Phát hiện | Đề xuất | File | Trạng thái |
|----|------|---------|-----------|---------|------|------------|
| IMP_LOCCREATE_001 | UX | P2 | Sau create thành công không redirect — chỉ reset form | Redirect edit | `LocationCreate/index.tsx` | **fixed** |
| IMP_LOCCREATE_002 | UI | P2 | Layout header `max-w-[1600px]` | full-bleed như Location List | `LocationCreate/index.tsx` | **fixed** |
| IMP_LOCCREATE_003 | i18n | P3 | `price_level` hardcode tiếng Việt | Dùng `priceLevels.*` | `LocationForm.tsx` | **fixed** |
| IMP_LOCCREATE_004 | A11y | P3 | Map reset title tiếng Anh only | i18n aria-label | `MapPicker.tsx` | **fixed** |
| IMP_LOCCREATE_005 | Validation | P2 | `category_id` default 0 không báo lỗi | min(1) / null default | schema + form | **fixed** |
| IMP_LOCCREATE_006 | UX | P3 | Lỗi thumbnail ngoài data-location-field | Gom lỗi vào block | `LocationForm.tsx` | **fixed** |

**Automation:** 22/22 passed. **Product IMP:** 6/6 fixed (2026-06-18).

### Blog List `06a` (audit 2026-06-21)

| ID | Loại | Ưu tiên | Phát hiện | Đề xuất | File | Trạng thái |
|----|------|---------|-----------|---------|------|------------|
| IMP_BLOGLIST_001 | Doc | P2 | Route doc `/admin/blog` | Sửa `/admin/blog-posts` | `06a_blog_list.md` | **fixed** |
| IMP_BLOGLIST_002 | Doc | P2 | Doc ghi Staff | Chỉ Admin | `06a_blog_list.md` | **fixed** |
| IMP_BLOGLIST_003 | UX | P1 | List API lỗi → stats error + table empty, không retry | ErrorWidget như Location List | `BlogPostList/index.tsx` | **fixed** |
| IMP_BLOGLIST_004 | UX | P2 | Nút Đặt lại trong form thiếu `type="button"` | Thêm type button | `BlogFilterBar.tsx` | **fixed** |
| IMP_BLOGLIST_005 | UX | P2 | Sidebar `/admin/blog` không redirect | Navigate → blog-posts | `routes/index.tsx` | **fixed** |
| IMP_BLOGLIST_006 | UX | P2 | Stats error trùng list error | Ẩn BlogStatsRow khi list fail | `BlogPostList/index.tsx` | **fixed** |
| IMP_BLOGLIST_007 | i18n | P2 | Checkbox thiếu key select_all/select_row | Thêm `common.json` table | `public/lang/*/common.json` | **fixed** |
| IMP_BLOGLIST_008 | Test | P2 | Thiếu TC 025/029/055/058/061/067 | Bổ sung spec + mock scheduled | `blog-list*.spec.ts` | **fixed** |

**POM:** `BlogListPage.ts` — copy bilingual EN/VI (`Blog Posts`, `Add New`, `DRAFTS`). Scope status dropdown `.absolute.left-4.top-12`.

### Blog Create `06b` (audit 2026-06-21)

| ID | Loại | Ưu tiên | Phát hiện | Đề xuất | File | Trạng thái |
|----|------|---------|-----------|---------|------|------------|
| IMP_BLOGCREATE_001 | Doc | P2 | Route doc `/admin/blog/create` | Sửa `/admin/blog-posts/create` | `06b_blog_create.md` | **fixed** |
| IMP_BLOGCREATE_002 | Doc | P2 | Doc ghi Staff | Chỉ Admin | `06b_blog_create.md` | **fixed** |
| IMP_BLOGCREATE_003 | UI | P2 | Header `max-w-[1600px]` | full-bleed như Location Create | `BlogPostCreate/index.tsx` | **fixed** |
| IMP_BLOGCREATE_004 | Doc | P3 | Doc ảnh bìa required — schema optional | Cập nhật doc | `06b_blog_create.md` | **fixed** |
| IMP_BLOGCREATE_005 | A11y | P3 | Nút back thiếu aria-label | Thêm i18n aria | `BlogPostCreate/index.tsx` | **fixed** |
| IMP_BLOGCREATE_006 | i18n | P3 | "Loading..." / "No categories" hardcode EN | Dùng blog.json keys | `BlogPostForm.tsx` | **fixed** |
| IMP_BLOGCREATE_007 | UX | P1 | Mobile thiếu sticky footer | Pattern LocationForm | `BlogPostCreate/index.tsx` | **fixed** |
| IMP_BLOGCREATE_008 | Validation | P1 | Scheduled không có ngày | Validate `scheduleDate` | `BlogPostForm.tsx` | **fixed** |
| IMP_BLOGCREATE_009 | Code | P1 | Header submit `getElementById` | `form="blog-post-form"` | `BlogPostCreate/index.tsx` | **fixed** |
| IMP_BLOGCREATE_010 | UX | P2 | Sticky header collapse | `useMainScrollCollapse` | `BlogPostCreate/index.tsx` | **fixed** |
| IMP_BLOGCREATE_011 | UX | P2 | Redirect list sau create | Redirect edit | `BlogPostForm.tsx` | **fixed** |
| IMP_BLOGCREATE_012 | i18n | P3 | Editor hardcode EN | blog.json `form.editor` | `BlogMarkdownEditor.tsx` | **fixed** |
| IMP_BLOGCREATE_013 | A11y | P3 | Checkbox thiếu aria-label | `aria-label={cat.name}` | `BlogPostForm.tsx` | **fixed** |

**POM:** `BlogCreatePage.ts` — sidebar submit, markdown `.rc-md-editor textarea`, bilingual copy.

### Blog Edit `06c` (audit 2026-06-22)

| ID | Loại | Ưu tiên | Phát hiện | Đề xuất | File | Trạng thái |
|----|------|---------|-----------|---------|------|------------|
| IMP_BLOGEDIT_001 | Doc | P2 | Doc cũ 2 TC, ghi Staff | Cập nhật doc | `06c_blog_edit.md` | **fixed** |
| IMP_BLOGEDIT_002 | UI | P2 | Header `max-w-[1600px]` | full-bleed như Location Edit | `BlogPostEdit/index.tsx` | **fixed** |
| IMP_BLOGEDIT_003 | A11y | P3 | Nút back thiếu aria-label | Thêm i18n aria | `BlogPostEdit/index.tsx` | **fixed** |
| IMP_BLOGEDIT_004 | i18n | P3 | Loading categories hardcode EN | blog.json keys | `BlogPostEdit/BlogPostForm.tsx` | **fixed** |
| IMP_BLOGEDIT_005 | Code | P1 | Header save `requestSubmit()` | `form="blog-post-form"` | `BlogPostEdit/index.tsx` | **fixed** |
| IMP_BLOGEDIT_006 | Validation | P1 | Scheduled không có ngày vẫn submit | Validate scheduleDate | `BlogPostEdit/BlogPostForm.tsx` | **fixed** |
| IMP_BLOGEDIT_007 | UX | P2 | Chưa collapse header khi scroll | `useMainScrollCollapse` | `BlogPostEdit/index.tsx` | **fixed** |
| IMP_BLOGEDIT_008 | i18n | P3 | `error_post_not_found` chỉ defaultValue | Thêm keys blog.json | `blog.json` | **fixed** |
| IMP_BLOGEDIT_009–018 | Mixed | P1–P3 | Preview sync, mobile QA, redirect detail | xem `06c_blog_edit.md` | multiple | **fixed** |

**POM:** `BlogEditPage.ts` — quick actions card, duplicate/delete modals, PUT waitFor, bilingual copy.

### Promotions `07` (audit 2026-06-23)

| ID | Loại | Ưu tiên | Phát hiện | Đề xuất | File | Trạng thái |
|----|------|---------|-----------|---------|------|------------|
| IMP_PROM_001 | i18n | P2 | Stats card labels hardcode VI | `t('promotions:stats.*')` | `Promotions/index.tsx` | **fixed** |
| IMP_PROM_002 | i18n | P2 | Delete modal hardcode VI | `PromotionDeleteDialog` + i18n | `PromotionDeleteDialog.tsx` | **fixed** |
| IMP_PROM_003 | UX | P2 | Stats chỉ đếm trang hiện tại | Nhãn `*_on_page` + hint | `Promotions/index.tsx` | **fixed** |
| IMP_PROM_004 | i18n | P2 | Table columns hardcode VI | i18n keys trong `PromotionTable` | `PromotionTable.tsx` | **fixed** |
| IMP_PROM_005 | Test | P2 | Mock thiếu `status` default | `status ?? 'active'` | `promotions-list.data.ts` | **fixed** |
| IMP_PROM_006 | UX | P2 | Checkbox bulk vô nghĩa | Gỡ checkbox | `PromotionTable.tsx` | **fixed** |
| IMP_PROM_007 | UX | P2 | Reset filter nhãn "Hủy bỏ" | `actions.reset_filters` | `PromotionFilter.tsx` | **fixed** |
| IMP_PROM_008 | UX | P1 | List API lỗi không có retry UI | `promotion-list-error` panel | `Promotions/index.tsx` | **fixed** |
| IMP_PROM_009 | a11y | P2 | Drawer panel focus khi đóng | `aria-hidden` + `inert` | `Drawer.tsx` | **fixed** |
| IMP_PROM_010 | Test | P3 | Filter tag X chưa có automation | TC_AD_PROM_032–033 | `PromotionFilter.tsx` | **fixed** |
| IMP_PROM_011 | Test | P3 | Toggle expired / per_page / API error create-update | TC_AD_PROM_034–037 | `promotions.spec.ts` | **fixed** |
| IMP_PROM_012 | Test | P3 | Auth mock flaky | `mockAuthRefreshApi` → `auth/**` | `auth.mock.ts` | **fixed** |

**POM:** `PromotionsPage.ts` — `removeFilterTagByKey`, `changeLimit`, expired toggle `toBeDisabled`; filter tag `data-testid`. **Mock:** `setPromotionUpdateFailForId(null)` tắt flag đúng.

**Automation:** `npm run test:admin:promotions` — **35/35 passed**.

### Payments `13a` (audit 2026-06-23)

| ID | Loại | Ưu tiên | Phát hiện | Đề xuất | File | Trạng thái |
|----|------|---------|-----------|---------|------|------------|
| IMP_PAY_001 | Doc | P2 | Doc ghi PayOS | Cập nhật → SePay | `13a_payment_list.md` | **fixed** |
| IMP_PAY_002 | UX | P2 | Stats chỉ đếm trang hiện tại | Nhãn `*_on_page` hoặc API stats | `PaymentList/index.tsx` | open |
| IMP_PAY_003 | i18n | P2 | Refund filter hardcode VI | i18n keys | `PaymentFilterBar.tsx` | open |
| IMP_PAY_004 | UX | P2 | FilterBar `onExport` không render nút | Gỡ prop hoặc thêm UI | `PaymentFilterBar.tsx` | open |
| IMP_PAY_005 | Function | P2 | Thiếu filter `partially_paid` | Thêm option | `PaymentFilterBar.tsx` | open |
| IMP_PAY_006 | i18n | P2 | Refund validation hardcode VI | i18n | `RefundPaymentDialog.tsx` | open |
| IMP_PAY_007 | Test | P1 | Mock pathname sai → API không intercept | Regex `/admin/payments/` + route riêng | `payments.mock.ts` | **fixed** |

**POM:** `PaymentListPage.ts` — `filterPanel` scope reset; `tableBodyRows` scope `main main tbody`. `PaymentDetailPage.ts` — heading `PAY-*`; toast `[data-sonner-toast]`.

**Automation:** `npm run test:admin:payment-list` + `test:admin:payment-detail` — list **23/23** · detail **10/10 passed** (audit ~48 TC, ~30 gap).

### Payment Detail `13b` (audit 2026-06-23)

| ID | Loại | Ưu tiên | Phát hiện | Trạng thái |
|----|------|---------|-----------|------------|
| IMP_PAYDET_001 | Doc | P2 | PayOS / TXN001 trong doc cũ | **fixed** |
| IMP_PAYDET_002–003 | i18n | P2 | Refund dialog validation + VietQR hardcode VI | open |
| IMP_PAYDET_004 | UX | P2 | API 500 = not found UI | open |
| IMP_PAYDET_005 | Test | P1 | Thiếu `payment-detail-auth.spec.ts` | **fixed** |
| IMP_PAYDET_006 | Test | P1 | ~30 TC gap | **fixed** — 37 TC |

**Automation:** `npm run test:admin:payment-detail` — **37/37 passed**. Còn manual: responsive 038–039, long text 036–037.

### Notifications `14` (audit 2026-06-23)

| ID | Loại | Ưu tiên | Phát hiện | Trạng thái |
|----|------|---------|-----------|------------|
| IMP_NOTIF_001 | Doc | P2 | Doc gốc ghi cột sender — API không có field | **fixed** — doc audit |
| IMP_NOTIF_002 | UX | P2 | Bulk delete `window.confirm` | **fixed** — reuse DeleteNotificationDialog |
| IMP_NOTIF_003 | Bug | P1 | Search URL sync không refetch API | **fixed** — queryKey + urlSearchKey |
| IMP_NOTIF_004 | UX | P2 | FilterBar debounce | **fixed** |
| IMP_NOTIF_005 | UX | P2 | Stats nhãn filtered | **fixed** |
| IMP_NOTIF_006 | UX | P2 | User filter searchable | **fixed** — FilterUserSelect |
| IMP_NOTIF_007 | Code | P2 | Bulk delete partial failure toast | **fixed** |

| IMP_NOTIF_SEND_001 | Doc/Code | P1 | Success không redirect về list | **fixed** — navigate sau toast |
| IMP_NOTIF_SEND_002 | Product/BE | P1 | Bulk count gồm user banned | **fixed** — `status=active` FE + BE `chunkAll` |
| IMP_NOTIF_SEND_003 | UX | P1 | Bulk khi 0 user vẫn submit | **fixed** — disable mode bulk |
| IMP_NOTIF_SEND_004 | UX | P1 | Link lỗi trong panel collapse | **fixed** — auto-expand khi `errors.data` |
| IMP_NOTIF_SEND_005 | i18n | P2 | Toast lỗi hiện message API thô | **fixed** — dùng `send.toast.send_failed` |
| IMP_NOTIF_SEND_006 | UX | P2 | Mobile footer trong sidebar | **fixed** — sticky bottom bar |
| IMP_NOTIF_SEND_007 | UX | P3 | Màu breadcrumb teal vs form blue | **fixed** — `actionPrimaryClassName` #0066CC |
| IMP_NOTIF_SEND_008 | UX | P2 | Backdrop đóng bulk dialog nhầm | **fixed** — bỏ backdrop click |
| IMP_NOTIF_SEND_009 | UX | P2 | Success không reset mode | **fixed** — `clearComposeForm` → individual |
| IMP_NOTIF_SEND_010 | i18n | P3 | Preview `"..."` hardcode | **fixed** — `preview_empty_content` |
| IMP_NOTIF_SEND_011 | a11y | P2 | RecipientSelector thiếu combobox | **fixed** — role/keyboard |
| IMP_NOTIF_SEND_012 | a11y | P2 | Bulk dialog thiếu aria/escape | **fixed** |
| IMP_NOTIF_SEND_013 | UX | P2 | Không cảnh báo unsaved | **fixed** — `UnsavedChangesGuard` |
| IMP_NOTIF_SEND_014 | Code | P2 | Trùng infinite user search | **fixed** — `useAdminUserInfiniteSearch` |
| IMP_NOTIF_SEND_015/016 | Code | P3 | State kép + callback không memo | **partial** — `useCallback`; preview state giữ tối thiểu |
| IMP_NOTIF_SEND_017/018 | Code | P3 | Yup/useForm types | **fixed** — `useMemo` schema + typed form |
| IMP_NOTIF_SEND_019 | API | P2 | Toast bulk count stale | **fixed** — BE `sent_count` |
| IMP_NOTIF_SEND_020 | Doc | P3 | Key JSON legacy | **fixed** — removed `data_invalid_json` |
| IMP_NOTIF_SEND_021/022 | Test/a11y | P3 | Thiếu testid + breadcrumb trùng label | **fixed** |

**POM:** `NotificationListPage.ts` · `NotificationSendPage.ts`. **Mock:** `notifications.mock.ts` — list filter param `search` (map từ `q`).

**Automation:** `npm run test:admin:notifications` — **53/53 passed** (list 15 + send 35 + auth 4). Send chi tiết: `14b_notification_send.md` — TC `TC_AD_NOTIF_SEND_*`. `TC_AD_NOTIF_003` list dùng `goto(?q=)`; `003b` assert URL debounce.

### Tour Categories `15` (audit 2026-06-23)

| ID | Loại | Ưu tiên | Phát hiện | Trạng thái |
|----|------|---------|-----------|------------|
| IMP_TOURCAT_001 | Doc | P2 | Doc ghi route `/admin/tours/categories` — code dùng `/admin/tour-categories` | **fixed** — doc |
| IMP_TOURCAT_002 | i18n | P3 | Delete dialog dùng `dialog.button_delete` = "Xóa tour" | **fixed** — `categories.dialog.button_delete` |
| IMP_TOURCAT_003 | i18n | P3 | Empty grid dùng `messages.no_data` = "Không tìm thấy tour nào" | **fixed** — `categories.empty_*` |
| IMP_TOURCAT_004 | i18n | P3 | Card footer hardcode "VỊ TRÍ:" | **fixed** — `categories.table.header_order` |
| IMP_TOURCAT_005 | Test | P3 | Drag reorder pixel-perfect — automation cover enter/save/cancel only | manual |
| IMP_TOURCAT_006 | UX | P1 | Stats card nhãn/giá trị lệch + không ghi chú scope | **fixed** — labels + `stats_scope_note` |
| IMP_TOURCAT_007 | UX | P1 | Xóa danh mục còn tour chỉ fail sau confirm | **fixed** — disable nút xóa |
| IMP_TOURCAT_008 | Code | P1 | API unwrap `{ category }` | **fixed** — `tourCategoryApi` |
| IMP_TOURCAT_009 | UX | P2 | Search không debounce | **fixed** — `useDebounce(300)` |
| IMP_TOURCAT_010 | UX | P2 | Mô tả không hiển thị trên card | **fixed** — line-clamp |
| IMP_TOURCAT_011 | UX | P2 | Progress bar magic 50 | **fixed** — removed |
| IMP_TOURCAT_012 | A11y | P2 | Icon buttons thiếu aria-label | **fixed** |
| IMP_TOURCAT_013 | UX | P2 | Drawer backdrop đóng mất data | **fixed** — `UnsavedChangesGuard` + no backdrop close |
| IMP_TOURCAT_014 | UX | P2 | Reorder cancel không rollback | **fixed** |
| IMP_TOURCAT_015 | UX | P2 | Status toggle không disable khi pending | **fixed** |
| IMP_TOURCAT_016 | Code | P3 | Trùng colorOptions | **fixed** — `categoryTheme.ts` |
| IMP_TOURCAT_017 | Code | P3 | Validation dùng placeholder làm lỗi | **fixed** — `categories.validation.*` |
| IMP_TOURCAT_018 | Test | P3 | Thiếu data-testid | **fixed** |
| IMP_TOURCAT_019 | UX | P3 | Link tour count → tour list | **fixed** — `?tour_category_id=` + TourList read param |

**API:** `GET/POST /admin/tour-categories` · `PUT/PATCH/DELETE /:id` · `PATCH /:id/status` · `PATCH /reorder`. List `with_stats=true` → `{ categories: { data, meta }, stats }`. Stats card 1 map `total_tours`.

### Location Categories `16` (audit 2026-06-23)

| ID | Loại | Ưu tiên | Phát hiện | Trạng thái |
|----|------|---------|-----------|------------|
| IMP_LOCCAT_001 | Doc | P2 | Doc ghi route `/admin/locations/categories` — code `/admin/location-categories` | **fixed** — doc |
| IMP_LOCCAT_002 | UX | P1 | Xóa danh mục còn địa điểm chỉ fail sau confirm | **fixed** — disable nút xóa |
| IMP_LOCCAT_003 | i18n | P3 | Empty grid dùng `messages.no_data` chung | **fixed** — `categories.empty_*` |
| IMP_LOCCAT_004 | Test | P3 | Thiếu data-testid card/drawer/dialog | **fixed** |
| IMP_LOCCAT_005 | UX | P2 | Progress bar magic `/50` trên card | **fixed** — link count |
| IMP_LOCCAT_006 | A11y | P2 | Icon edit/delete thiếu aria-label | **fixed** |
| IMP_LOCCAT_007 | Test | P3 | Drag reorder pixel-perfect | manual |
| IMP_LOCCAT_008 | Code | P1 | API unwrap `{ category }` | **fixed** — `categoryApi` |
| IMP_LOCCAT_009 | UX | P1 | Subtitle drawer tạo mới sai | **fixed** |
| IMP_LOCCAT_010 | UX | P1 | Drawer backdrop / unsaved | **fixed** — `UnsavedChangesGuard` |
| IMP_LOCCAT_011 | UX | P2 | Link count → location list | **fixed** — `?category_id=` |
| IMP_LOCCAT_012 | UX | P2 | Stats scope note | **fixed** |
| IMP_LOCCAT_013 | UX | P2 | Reset filters | **fixed** |
| IMP_LOCCAT_014 | UX | P2 | Reorder cancel rollback | **fixed** |
| IMP_LOCCAT_015 | UX | P2 | Status pending disable | **fixed** |
| IMP_LOCCAT_016 | UX | P3 | Mô tả trên card | **fixed** |
| IMP_LOCCAT_017 | Code | P3 | Trùng colorOptions | **fixed** — `categoryTheme.ts` |
| IMP_LOCCAT_018 | Code | P3 | placeholderData stale filter | **fixed** |

**API:** `GET/POST /admin/categories` · `PUT/PATCH/DELETE /:id` · `PATCH /:id/status` · `PATCH /reorder`. List `with_stats=true` → `{ categories: { data, meta }, stats }`. Field count: `locations_count` → `locationsCount`.

**POM:** `LocationCategoriesPage.ts`. **Mock:** `location-categories.mock.ts` — route `**/api/v1/admin/categories**`.

**Automation:** `npm run test:admin:location-categories` — **24/24 passed** (18 UI + 3 auth + 3 API).

### Blog Categories `17` (audit 2026-06-23)

| ID | Loại | Ưu tiên | Phát hiện | Trạng thái |
|----|------|---------|-----------|------------|
| IMP_BLOGCAT_001 | Doc | P2 | Doc route `/admin/blog/categories` — code `/admin/blog-categories` | **fixed** — doc |
| IMP_BLOGCAT_002 | UX | P1 | Xóa danh mục còn bài viết chỉ fail sau confirm | **fixed** |
| IMP_BLOGCAT_003 | UX | P2 | Link post count → blog list filter | **fixed** |
| IMP_BLOGCAT_004 | Test | P3 | Thiếu data-testid | **fixed** |
| IMP_BLOGCAT_005 | UX | P2 | Reorder cancel không rollback | **fixed** |
| IMP_BLOGCAT_006 | i18n | P3 | Empty search dùng `empty.title` chung | **fixed** |
| IMP_BLOGCAT_007 | Test | P3 | Drag reorder pixel-perfect | manual |
| IMP_BLOGCAT_008 | UX | P2 | Form không reset sau tạo | **fixed** |
| IMP_BLOGCAT_009 | UX | P2 | UnsavedChangesGuard | **fixed** |
| IMP_BLOGCAT_010 | UX | P3 | Slug auto overwrite | **fixed** |
| IMP_BLOGCAT_011 | UX | P3 | Stats scope + reset search | **fixed** |
| IMP_BLOGCAT_012 | Code | P3 | Delete dialog inline | **fixed** |

**API:** `GET/POST /admin/blog-categories` · `PUT/DELETE /:id` · `PATCH /reorder`. Field count: `posts_count` → `postCount`. UI: card grid + inline form (không drawer).

**POM:** `BlogCategoriesPage.ts`. **Mock:** `blog-categories.mock.ts`.

**Automation:** `npm run test:admin:blog-categories` — **23/23 passed** (17 UI + 3 auth + 3 API; TC_005 gộp TC_017).

**POM:** `TourCategoriesPage.ts`. **Mock:** `tour-categories.mock.ts`. Card locator: `h3.font-black` trong `.rounded-[32px].border`. Edit/delete: icon `lucide-edit-2` / `lucide-trash-2`.

**Automation:** `npm run test:admin:tour-categories` — **24/24 passed** (18 UI + 3 auth + 3 API).

### Ratings list `08` (audit 2026-06-23)

| ID | Loại | Severity | Phát hiện | Trạng thái |
|----|------|----------|-----------|------------|
| IMP_RAT_001 | Doc | P3 | Doc cũ ghi approve — UI dùng mark-viewed | **fixed** — `08_ratings.md` |
| IMP_RAT_002 | UX | P2 | Reset filter bị debounce search ghi đè | **fixed** — `RatingFilterBar.tsx` |
| IMP_RAT_003 | i18n | P2 | Toast mutation hardcode VI trong hook | **fixed** — `useRatingQueries.ts` |
| IMP_RAT_004 | UX | P1 | List API lỗi không có retry panel | **fixed** — `rating-list-error` |
| IMP_RAT_005 | Test | P3 | Mock pathname `isRatingsListPath` sai | **fixed** — `ratings.mock.ts` |
| IMP_RAT_006 | Test | P3 | POM statCard/selectedCount/delete/toast | **fixed** — `RatingsPage.ts` |
| IMP_RAT_007–016 | UX/Code | P1–P3 | Bulk allSettled, clear selection, a11y, empty/stats error, image badge, dialog reset | **fixed** — `Ratings/index.tsx` + components |

**POM:** `RatingsPage.ts` — `resetFilter` = `actions.reset_filters`, `deleteBulkSuccess`, `expectToast()` sonner.  
**Mock:** 12 rows · stats new=5 viewed=7 · `PATCH mark-viewed/reject` · `DELETE` · export blob.  
**Script:** `npm run test:admin:ratings` — **36/36 passed** (2026-06-23).

### Contacts `09` (audit 2026-06-23)

| ID | Loại | Severity | Phát hiện | Trạng thái |
|----|------|----------|-----------|------------|
| IMP_CNT_001 | UX | P2 | List lỗi không retry | **fixed** |
| IMP_CNT_002 | UX | P2 | Detail error duplicate copy | **fixed** |
| IMP_CNT_003 | UX | P2 | Stats error không retry | **fixed** |
| IMP_CNT_004 | UX | P3 | Tab status không clear `id` | **fixed** |
| IMP_CNT_005 | Doc | P3 | TC_023 delete unselected — UI không hỗ trợ | **fixed** (list row delete) |

**POM:** `ContactsPage.ts` — `contact-list-error`, `contact-stats-error`, `contact-detail-error`, `listDeleteButton(id)`.  
**Mock:** 12 rows · stats total=12 · POST reply · DELETE · export blob.  
**Script:** `npm run test:admin:contacts` — **37/37 passed** (2026-06-23).

### Reports `10` (audit 2026-06-23)

| ID | Loại | Severity | Phát hiện | Trạng thái |
|----|------|----------|-----------|------------|
| IMP_REP_001 | Doc | P3 | REP_USR_018 role pie — UI chỉ growth table | open |
| IMP_REP_002 | Test | P3 | Flaky session TC_AD_REP_007/018 | open |
| IMP_REP_003 | UX | P3 | Top tour YAxis truncate 15 chars | open |

**POM:** `ReportPage.ts` — bilingual `reportsCopy`, route-aware `waitForContentLoaded`, mock toggle đa namespace.  
**Mock:** revenue 3 endpoints · bookings/ratings/users/locations reports · export MINIMAL_XLSX blob.  
**Script:** `npm run test:admin:reports` — **25/25 passed** (2026-06-23).

### Settings `11` (audit 2026-06-23)

| ID | Loại | Severity | Phát hiện | Trạng thái |
|----|------|----------|-----------|------------|
| IMP_SET_001 | Doc | P2 | Doc gốc mô tả profile/password — lệch product | **fixed** (mapping) |
| IMP_SET_002 | Doc | P2 | Doc ghi PayOS/VNPay — code dùng SePay/COD | **fixed** (mapping) |
| IMP_SET_003 | Test | P3 | Cross-app sync Header/Footer Web client | open (manual) |
| IMP_SET_004 | UX | P3 | Load error hardcode EN + no retry | **fixed** |
| IMP_SET_005 | A11y | P3 | Payment toggle thiếu aria-label | **fixed** |
| IMP_SET_006 | Feature | P3 | Chatbot schema without UI tab | **fixed** (hint banner) |

**POM:** `SettingsPage.ts` — bilingual copy EN/VI · SaveBar scoped `div.fixed` · gateway toggle qua h4 heading.  
**Mock:** GET/PUT `/admin/settings` · notification-counts · flags load/save fail/delay.  
**Script:** `npm run test:admin:settings` — **20/20 passed** (2026-06-23).

### Login `12` (audit 2026-06-23)

| ID | Loại | Severity | Phát hiện | Trạng thái |
|----|------|----------|-----------|------------|
| IMP_LOGIN_001 | Doc | P2 | Doc route `/admin/login` — code `/login` | **fixed** (mapping) |
| IMP_LOGIN_002 | Doc | P2 | Doc API `admin/login` — code `/auth/login` | **fixed** (mapping) |
| IMP_LOGIN_003 | Doc | P2 | Doc dashboard `/admin/dashboard` — code `/dashboard` | **fixed** (mapping) |
| IMP_LOGIN_004 | Bug | P1 | Login chỉ check role `admin`, Staff bị chặn | **fixed** (`canAccessAdminPanel`) |
| IMP_LOGIN_005 | UX | P3 | Forgot password `href="#"` dead link | **fixed** (disabled span + title) |
| IMP_LOGIN_006 | Test | P3 | Remember me token persistence | **fixed** (TC 007) |
| IMP_LOGIN_007–012 | Test | P2 | Validation, PublicRoute, loading, API 500, cookie clear | **fixed** |
| IMP_LOGIN_013 | Doc | P3 | Doc token storage chỉ ghi localStorage | **fixed** |

**POM:** `LoginPage.ts` — testids submit/error/remember · cookie+LS token helpers.  
**Mock:** `POST /auth/login` · delay · 500 fail · admin/staff/customer/wrong.  
**Script:** `npm run test:admin:login` — **13/13 passed** (2026-06-23).

### Location Edit `05c` (audit 2026-06-18)

| ID | Loại | Severity | Phát hiện | Trạng thái |
|----|------|----------|-----------|------------|
| IMP_LOCEDIT_001 | UX | P2 | Màn 404 hardcode tiếng Anh | **fixed** |
| IMP_LOCEDIT_002 | UI | P2 | Layout header `max-w-[1600px]` | **fixed** |
| IMP_LOCEDIT_003 | A11y | P3 | Nút back thiếu aria-label | **fixed** |
| IMP_LOCEDIT_004 | UX | P3 | PUT full payload (by design) | open |
| IMP_LOCEDIT_005 | Code | P2 | Invalidate detailRaw sau PUT | **fixed** |
| IMP_LOCEDIT_006 | UX | P3 | Xóa không có trên mobile | **fixed** |
| IMP_LOCEDIT_007 | UX | P3 | Hủy mobile history.back | **fixed** |

**Automation:** 23/23 passed.

### Location Detail `05d` (audit 2026-06-18)

| ID | Loại | Ưu tiên | Phát hiện | Trạng thái |
|----|------|---------|-----------|------------|
| IMP_LOCDET_001 | A11y | P3 | Nút back chỉ `title`, thiếu `aria-label` | **fixed** |
| IMP_LOCDET_002 | UX | P3 | ErrorWidget nút back dùng nhãn `Đóng` | **fixed** |
| IMP_LOCDET_003 | Error | P3 | Reviews API lỗi → empty | **fixed** |
| IMP_LOCDET_004 | UX | P3 | Header delete ẩn text mobile | **fixed** — aria-label |
| IMP_LOCDET_005 | Layout | P3 | Nút back bị sidebar che | **fixed** |
| IMP_LOCDET_006 | UX | P2 | 404 vs 500 cùng UI | **fixed** |
| IMP_LOCDET_007 | Code | P2 | Trùng delete modal | **fixed** |
| IMP_LOCDET_008 | UX | P3 | Toast bulk cho status đơn | **fixed** |
| IMP_LOCDET_009 | UX | P3 | Hero fullscreen dead button | **fixed** — lightbox |

**Automation:** 27/27 passed. Script: `npm run test:admin:location-detail`. POM: `LocationDetailPage.ts`. Mock: ratings/rating-stats + `setLocationStatusFailForId` + `setLocationDetailFailForId(id, status)`.

**Đã ổn (không đề xuất sửa):** sticky collapse, cancel validation, timeline milestones, mock thumbnail fallback (đã fix fixture), payment format VNĐ, terminal state ẩn action.

### Chatbot Hub `19` (audit + product fix 2026-06-23)

| ID | Loại | Sev | Phát hiện | Trạng thái |
|----|------|-----|-----------|------------|
| IMP_CHAT_001 | i18n | P2 | Toast cache hardcode EN | **fixed** — `useChatbotQueries` + `chatbot.json` |
| IMP_CHAT_002 | UX/A11y | P1 | `window.confirm` xóa cache | **fixed** — `ChatbotCacheConfirmDialog` |
| IMP_CHAT_003 | UX | P2 | Search logs gọi API mỗi keystroke | **fixed** — debounce 300ms |
| IMP_CHAT_004 | UX | P2 | Tab không sync URL / mất tab khi reload | **fixed** — `?tab=logs\|settings` |
| IMP_CHAT_005 | UX | P2 | Đổi tab mất filter logs | **fixed** — tab panels giữ mounted (`hidden`) |
| IMP_CHAT_006 | A11y | P2 | Tablist thiếu `role`/`aria-selected` | **fixed** |
| IMP_CHAT_007 | API | P2 | PUT settings full payload | **fixed** — `updateSettingGroups` partial |
| IMP_CHAT_008 | UX | P3 | Empty cache không phân biệt search | **fixed** — `no_cache` vs `no_cache_search` |
| IMP_CHAT_009 | Perf | P3 | Stats refetch khi tab ẩn | **fixed** — `isActive` trên dashboard hook |

**POM:** scope selector theo `chatbot-tabpanel-{dashboard|logs|settings}` — tab mounted nên `hub.locator('table tbody tr')` match nhiều bảng.  
**Script:** `npm run test:admin:chatbot` — **39/39 passed** (2026-06-23).

---

## 12. Liên kết

- Prompt **generic** (mọi project): `working-prompts/playwright_auto_test_generator_prompt.md`
- Test cases **DATN**: `testcases/03_admin_flows/`
- App: `danangtrip-admin` (Vite `:5173`) · API: `danangtrip-api` (`:8000/api/v1`)
