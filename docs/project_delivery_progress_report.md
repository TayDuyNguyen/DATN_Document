# Báo cáo Theo dõi Tiến độ Triển khai Dự án

> Ngày cập nhật: 24/05/2026  
> Phạm vi theo dõi:
> - `D:\DATN\danangtrip-web`
> - `D:\DATN\danangtrip-admin`
> - `D:\DATN\danangtrip-api`
>  
> Cách tính tiến độ:
> - Tách làm 2 lớp:
>   - `Tổng màn của dự án` theo tài liệu thật trong `docs/page`
>   - `Phạm vi delivery đang theo dõi` theo các màn đã có `deploy-report` hoặc đã được chốt là màn kế tiếp trong rollout hiện tại
> - Với `danangtrip-web`, không tính 5 file component-spec của nhóm rating vào tổng số màn chính.
> - Trạng thái dùng 3 mức: `Chưa làm`, `Đang làm`, `Hoàn thành`.

---

## 0.0.11 Current delivery override - 2026-05-24

Phan nay la nguon chuan moi nhat sau khi doc lai `.codegraph/codegraph.db` cua `danangtrip-web`, `danangtrip-admin`, `danangtrip-api` luc `2026-05-24 20:53` va doi chieu lai cac nhanh da push:

- Admin PR: `https://github.com/TayDuyNguyen/danangtrip-admin/pull/new/feat/DATN-91/admin-notifications-send`
- API PR: `https://github.com/TayDuyNguyen/danangtrip-api/pull/new/feat/DATN-92/notification-email-delivery`
- Web PR: `https://github.com/TayDuyNguyen/danangtrip-web/pull/new/feat/DATN-92/user-blog-by-category`

Neu cac phan cu ben duoi con khoa `user-blog-by-category` hoac `admin_notifications_send` la man tiep theo, xem chung la da loi thoi vi hai man nay da di het Step 10 va da push branch review.

### Completed since previous override

| Project | Completed screen / work item | Route / API | Evidence |
|---|---|---|---|
| Web | `user-blog-by-category` | `/blog?category_id={id}` | Co artifacts Step 01-10 `2026-05-24__user-blog-by-category__*.md`, codegraph thay blog/category related artifacts va repo co thay doi trong `BlogContent.tsx`, `BlogSidebar.tsx`, `BlogSkeleton.tsx`, `src/messages/*/blog.json`. Branch da push: `feat/DATN-92/user-blog-by-category`. |
| Web hardening | Absolute notification target URL support | User notifications card | `NotificationItemCard.tsx` ho tro `data.url` dang `https://...` bang `window.location.assign`, van giu router noi bo cho `/...`. |
| Admin | `admin_notifications_send` | `/admin/notifications/send` | Codegraph/repo xac nhan `src/pages/Notifications/NotificationSend/index.tsx`, `NotificationSendForm`, `RecipientSelector`, `NotificationPreview`, `BulkConfirmDialog`, route `ROUTES.NOTIFICATIONS_SEND`, lazy route, notification API send/sendAll hooks va i18n. Branch da push: `feat/DATN-91/admin-notifications-send`. |
| API | Notification email delivery | `POST /admin/notifications/send`, `POST /admin/notifications/send-all` | Co `AdminNotificationMail`, `SendAdminNotificationEmail` job, `NotificationService` mail dispatch support, `UserRepository::chunkAll()` lay email/full_name, README Gmail SMTP huong dan. Branch da push: `feat/DATN-92/notification-email-delivery`. |

### Current locked screens for next implementation

| Project | Last completed screen | Next locked screen | Route | Current code status | Reason |
|---|---|---|---|---|---|
| Web | `user-blog-by-category` | `TBD - API/planning review needed` | Candidate: `/profile/delete` or `/cart` | Codegraph khong thay route `/profile/delete`, `/cart`, hay API `DELETE /user/account`/cart routes san sang. | Public discovery backlog da khep cac man category/nearby/tours/blog. Hai item con lai trong backlog web (`user-profile-delete`, `user-cart`) dang phu thuoc API/planned flow nen chua nen khoa prompt tiep theo khi chua chot API. |
| Admin | `admin_notifications_send` | `admin_blog_posts_list` | `/admin/blog-posts` | Codegraph/API xac nhan backend admin blog routes `GET/POST/PUT/DELETE/PATCH /admin/blog-posts`; admin repo chua thay page/module blog posts. | Sau notifications list/send, module CMS blog la khoi admin API-ready tiep theo trong support/CMS backlog. |

### Updated counts

| Project | Total main screens | Deploy-completed | In progress | Not started | Completion % | Next selected screen |
|---|---:|---:|---:|---:|---:|---|
| Web | 35 | 20 | 0 | 15 | 57.1% | `TBD - API/planning review needed` |
| Admin | 40 | 21 | 0 | 19 | 52.5% | `admin_blog_posts_list` |

### Updated code-level counts

| Project | Total documented main screens | Screens with route/page code | Screens without route/page code | Code coverage |
|---|---:|---:|---:|---:|
| Web | 35 | 32 | 3 | 91.4% |
| Admin | 40 | 29 | 11 | 72.5% |

### Codegraph / repo verification notes

| Project | Codegraph snapshot | Verification |
|---|---|---|
| Web | `files=335`, `nodes=2771`, `edges=5166`, mtime `2026-05-24 20:53:14` | Codegraph/repo scan thay Step 01-10 artifacts `user-blog-by-category`, blog component updates, i18n updates va notification absolute link hardening. |
| Admin | `files=320`, `nodes=2955`, `edges=6172`, mtime `2026-05-24 20:53:11` | Codegraph/repo scan thay route lazy import `NotificationSend`, page/components trong `src/pages/Notifications/NotificationSend`, i18n va send/sendAll wiring. |
| API | `files=450`, `nodes=4303`, `edges=6265`, mtime `2026-05-24 20:53:13` | Codegraph/repo scan thay `AdminNotificationMail`, `SendAdminNotificationEmail`, notification service email support, va admin blog-post routes san sang cho man admin tiep theo. |

### Validation snapshot

| Project | Validation |
|---|---|
| Web | `npm.cmd run prepush:check` PASS sau khi chay ngoai sandbox vi Wrangler can ghi log AppData. Lint/typecheck/route check/build deu PASS. |
| Admin | `npm.cmd run prepush:check` PASS. ESLint co 0 error va 3 warning React Compiler/react-hook-form watch da ghi nhan; typecheck/build/console smoke PASS. |
| API | `php -l` PASS cho file mail/service/repository, `composer analyze` PASS, `composer test` PASS voi 12 tests / 48 assertions. |

### Selection notes

| Project | Notes |
|---|---|
| Web | `user-blog-by-category` da xong. Khong nen khoa `user-profile-delete` hoac `user-cart` truoc khi API contract duoc chot; neu can tiep tuc web ngay, nen mo mot vong API/planning review de chon giua account delete, cart, hoac hardening cac route da co. |
| Admin | `admin_notifications_send` da xong. `admin_blog_posts_list` la ung vien tiep theo vi API CRUD blog posts da ton tai va admin repo chua co UI module tuong ung. |

### Next execution order

1. Admin: cap nhat prompt `danangtrip-admin/.agent/skills/STACK_SKILLS_INDEX.md` sang `admin_blog_posts_list`, route `/admin/blog-posts`, sau do chay Step 01 -> Step 10.
2. Web: chay vong planning/API readiness truoc khi khoa prompt tiep theo; candidate hien tai la `user-profile-delete` hoac `user-cart` nhung codegraph chua xac nhan API/route san sang.
3. API: neu chon web `user-profile-delete`/`user-cart`, can chot/bo sung API truoc; neu chon admin blog posts, API da co route CRUD co ban.
4. Completed screens chi hardening-only: `user-locations-by-category`, `user-locations-nearby`, `user-tours-by-category`, `user-blog-by-category`, `admin_contacts`, `admin_notifications_list`, `admin_notifications_send`, users cluster, reports cluster, booking invoice.

---

## 0.0.10 Current delivery override - 2026-05-24

Phan nay la nguon chuan moi nhat sau khi checkout/pull `dev` cho `danangtrip-web`, `danangtrip-admin`, `danangtrip-api` va doi chieu lai `.codegraph/codegraph.db` luc `2026-05-24 16:05`.
Neu cac phan cu ben duoi con khoa `user-tours-by-category` hoac `admin_notifications_list` la man tiep theo, xem chung la da loi thoi vi hai man nay da duoc merge vao `dev`.

### Completed since previous override

| Project | Completed screen / work item | Route / API | Evidence |
|---|---|---|---|
| Web | `user-tours-by-category` | `/tour-categories/{slug}/tours` | Co `src/app/[locale]/(main)/(public)/tour-categories/[slug]/tours/page.tsx`, `src/features/tour/category/components/CategoryToursClient.tsx`, `src/features/tour/category/hooks/useCategoryTours.ts`, route helper `CATEGORY_TOURS`, API helper `TOURS.BY_CATEGORY_SLUG`, i18n updates va deploy/review/test artifacts `2026-05-24__user-tours-by-category__*.md`. |
| Admin | `admin_notifications_list` | `/admin/notifications` | Co `src/pages/Notifications/NotificationList/index.tsx`, components filter/stats/table/delete dialog, route `ROUTES.NOTIFICATIONS`, sidebar link, endpoint constants, `notificationApi`, mapper, hook `useNotificationQueries`, i18n `notification.json`, deploy/review artifacts `2026-05-24__admin_notifications_list__*.md`. |
| API | Tour category list and admin notifications support | `GET /tour-categories/{slug}/tours`, `GET /admin/notifications`, `DELETE /admin/notifications/{id}` | `routes/api.php` co public tour category route va admin notification routes; backend co `ToursBySlugTourCategoryRequest`, `AdminListNotificationRequest`, notification service/repository admin list/delete support. |

### Current locked screens for next implementation

| Project | Last completed screen | Next locked screen | Route | Current code status | Reason |
|---|---|---|---|---|---|
| Web | `user-tours-by-category` | `user-blog-by-category` | `/blog?category_id={id}` | Blog list da co `category_id` query handling trong `BlogContent`, nhung chua co delivery artifact rieng cho doc `user_blog_by_category.md`; khong co route rieng can tao neu tiep tuc theo query-state design. | Day la API-ready/backfill-hardening item con lai cua public discovery cluster. `user-profile-delete` va `user-cart` van phu thuoc API/planned flow nen khong nen uu tien truoc. |
| Admin | `admin_notifications_list` | `admin_notifications_send` | `/admin/notifications/send` | List page da co CTA navigate den `/admin/notifications/send`, endpoint constants co `SEND`/`SEND_ALL`, backend co `POST /admin/notifications/send` va `POST /admin/notifications/send-all`, nhung chua co route/page send. | Tiep tuc cung module notifications de khep communication workflow sau list/delete. |

### Updated counts

| Project | Total main screens | Deploy-completed | In progress | Not started | Completion % | Next selected screen |
|---|---:|---:|---:|---:|---:|---|
| Web | 35 | 19 | 0 | 16 | 54.3% | `user-blog-by-category` |
| Admin | 40 | 20 | 0 | 20 | 50.0% | `admin_notifications_send` |

### Updated code-level counts

| Project | Total documented main screens | Screens with route/page code | Screens without route/page code | Code coverage |
|---|---:|---:|---:|---:|
| Web | 35 | 31 | 4 | 88.6% |
| Admin | 40 | 28 | 12 | 70.0% |

### Codegraph / repo verification notes

| Project | Verification |
|---|---|
| Web | `.codegraph/codegraph.db` cap nhat luc `2026-05-24 16:05`; repo scan xac nhan route `/tour-categories/[slug]/tours`, feature folder `src/features/tour/category`, service/config route helpers va artifacts Step 10 da ton tai. |
| Admin | `.codegraph/codegraph.db` cap nhat luc `2026-05-24 16:05`; repo scan xac nhan `src/pages/Notifications/NotificationList`, route `/admin/notifications`, sidebar, API/hook/mapper/i18n da ton tai. Chua thay route/page `/admin/notifications/send`. |
| API | `.codegraph/codegraph.db` cap nhat luc `2026-05-24 16:05`; repo scan xac nhan public tour category route va admin notification list/send/delete routes trong `routes/api.php`. |

### Validation snapshot

| Project | Validation |
|---|---|
| Web | `dev` da pull fast-forward den `2d18fc2`; worktree sach ngay sau pull. Latest artifacts cho `user-tours-by-category` co deploy/review/test report ngay `2026-05-24`. |
| Admin | `dev` da pull fast-forward den `4feb075`; worktree sach ngay sau pull. Latest artifacts cho `admin_notifications_list` co deploy/review report ngay `2026-05-24`. |
| API | `dev` da pull fast-forward den `2b71bc1`; worktree sach ngay sau pull. Route inventory xac nhan endpoints can thiet cho hai man vua merge va man admin send tiep theo. |

### Selection notes

| Project | Notes |
|---|---|
| Web | `user-tours-by-category` da xong, chi quay lai neu bugfix/hardening. `user-blog-by-category` nen duoc xu ly nhu query-state hardening/backfill tren `/blog?category_id={id}` thay vi tao route moi khi docs khong bat buoc route rieng. |
| Admin | `admin_notifications_list` da xong. `admin_notifications_send` la man tiep theo hop ly vi list da co CTA, backend co send/send-all endpoints, va module Notifications can khep ca list + send. |

### Next execution order

1. Web: cap nhat prompt `danangtrip-web/.agent/skills/STACK_SKILLS_INDEX.md` sang `user-blog-by-category`, sau do chay Step 01 -> Step 10 voi pham vi query-state `/blog?category_id={id}`.
2. Admin: cap nhat prompt `danangtrip-admin/.agent/skills/STACK_SKILLS_INDEX.md` sang `admin_notifications_send`, sau do chay Step 01 -> Step 10.
3. API: chi mo rong neu frontend contract thieu; hien tai admin notifications send/send-all da co endpoint, web blog category da co public category/query data path.
4. Completed screens chi hardening-only: `user-locations-by-category`, `user-locations-nearby`, `user-tours-by-category`, `admin_contacts`, `admin_notifications_list`, users cluster, reports cluster, booking invoice.

---

## 0.0.9 Current delivery override - 2026-05-24

Phan nay la nguon chuan moi nhat sau khi checkout/pull `dev` cho `danangtrip-web`, `danangtrip-admin`, `danangtrip-api` va doc lai `.codegraph`/repo reality luc `2026-05-24 13:21`.
Neu cac phan cu ben duoi con khoa `user-locations-nearby` hoac `admin_contacts` la man tiep theo, xem chung la da loi thoi vi hai man nay da duoc merge vao `dev`.

### Completed since previous override

| Project | Completed screen / work item | Route / API | Evidence |
|---|---|---|---|
| Web | `user-locations-nearby` | `/nearby` | Co `src/app/[locale]/(main)/(public)/nearby/page.tsx`, `src/features/locations/nearby`, `locationService.getNearby`, API constant `LOCATIONS.NEARBY`, i18n `locations.json`, deploy/review artifacts `2026-05-24__user-locations-nearby__*.md`. |
| Admin | `admin_contacts` | `/admin/contacts`, `/admin/contacts?id={id}` | Co `src/pages/Contacts/index.tsx`, `src/pages/Contacts/components/*`, route/sidebar/i18n/API hook/data mapper, deploy/review artifacts `2026-05-24__admin-contacts__*.md`. |
| API | Contact stats/search and nearby support | `GET /admin/contacts`, `GET /locations/nearby` | Contact list response co `stats`, search ho tro `q` va `phone`; nearby query eager-load `category`/`subcategory`. |

### Current locked screens for next implementation

| Project | Last completed screen | Next locked screen | Route | Current code status | Reason |
|---|---|---|---|---|---|
| Web | `user-locations-nearby` | `user-tours-by-category` | `/tour-categories/{slug}/tours` | Chua thay App Router page rieng hoac feature folder rieng cho route category tours. API public `GET /tour-categories/{slug}/tours` da co trong `routes/api.php`. | Sau khi public locations cluster da co category + nearby, tiep tuc sang tours taxonomy page la ung vien API-ready con thieu route/page. |
| Admin | `admin_contacts` | `admin_notifications_list` | `/admin/notifications` | Chua thay `src/pages/Notifications` hoac route admin notifications. API admin notifications da co list/send/send-all/delete trong `routes/api.php`. | Sau support contacts, notifications la support/admin communication tool ke tiep, co API san sang va chua co UI module. |

### Updated counts

| Project | Total main screens | Deploy-completed | In progress | Not started | Completion % | Next selected screen |
|---|---:|---:|---:|---:|---:|---|
| Web | 35 | 18 | 0 | 17 | 51.4% | `user-tours-by-category` |
| Admin | 40 | 19 | 0 | 21 | 47.5% | `admin_notifications_list` |

### Updated code-level counts

| Project | Total documented main screens | Screens with route/page code | Screens without route/page code | Code coverage |
|---|---:|---:|---:|---:|
| Web | 35 | 30 | 5 | 85.7% |
| Admin | 40 | 27 | 13 | 67.5% |

### Codegraph / repo verification notes

| Project | Verification |
|---|---|
| Web | `.codegraph/codegraph.db` cap nhat luc `2026-05-24 13:21`; repo scan xac nhan `/nearby` va `src/features/locations/nearby` da ton tai. Khong thay route/page rieng `tour-categories/{slug}/tours`. |
| Admin | `.codegraph/codegraph.db` cap nhat luc `2026-05-24 13:21`; repo scan xac nhan `src/pages/Contacts` va route contacts da ton tai. Khong thay `src/pages/Notifications` hoac route `/admin/notifications`. |
| API | `.codegraph/codegraph.db` cap nhat luc `2026-05-24 13:21`; repo scan xac nhan `GET /tour-categories/{slug}/tours` va admin notifications routes co that. |

### Validation snapshot

| Project | Validation |
|---|---|
| Web | `dev` da pull fast-forward den `e82cbac`; worktree sach. Truoc khi merge, Step 10 artifact ghi prepush/build/typecheck route checks da pass cho `user-locations-nearby`. |
| Admin | `dev` da pull fast-forward den `56d7956`; worktree sach. Step 10 artifact cho `admin-contacts` da co deploy/review. Cac kiem tra gan nhat sau fix stats/search: typecheck PASS, lint khong co error, con warning cu `react-hook-form watch`. |
| API | `dev` da pull fast-forward den `7c817eb`; worktree sach. PHP syntax cac file contact/service/repository da pass trong lan fix gan nhat. |

### Selection notes

| Project | Notes |
|---|---|
| Web | `user-locations-by-category` va `user-locations-nearby` deu da xong. Khong chon lai hai man nay tru khi bugfix/hardening. `user-tours-by-category` duoc chon vi API da co va route/page rieng chua co. |
| Admin | `admin_contacts` da xong. `admin_notifications_list` duoc chon tiep vi la module support doc lap, backend da co endpoints va repo chua co UI module. `admin_notifications_send` nen lam sau list hoac tach man ke tiep tuy prompt. |

### Next execution order

1. Web: cap nhat prompt `danangtrip-web/.agent/skills/STACK_SKILLS_INDEX.md` sang `user-tours-by-category`, sau do chay Step 01 -> Step 10.
2. Admin: cap nhat prompt `danangtrip-admin/.agent/skills/STACK_SKILLS_INDEX.md` sang `admin_notifications_list`, sau do chay Step 01 -> Step 10.
3. API: chi mo rong khi frontend contract thieu; hien tai route tour category va admin notifications da co endpoint nen uu tien doc/request validation truoc khi sua backend.
4. Completed screens chi hardening-only: `user-locations-by-category`, `user-locations-nearby`, `admin_contacts`, users cluster, reports cluster, booking invoice.

---

## 0.0.8 Current delivery override - 2026-05-24

Phan nay la nguon chuan moi nhat sau khi checkout/pull `dev` va doc lai repo thuc te cung `.codegraph` cua `danangtrip-web`, `danangtrip-admin`, `danangtrip-api`.
Neu cac phan cu ben duoi con khoa `user-locations-by-category` hoac `admin_users_edit` la man tiep theo, xem chung la da loi thoi vi hai man nay da co code va deploy/review artifacts.

### Completed since previous override

| Project | Completed screen / work item | Route / API | Evidence |
|---|---|---|---|
| Web | `user-locations-by-category` | `/categories/{slug}/locations` | Co `src/app/[locale]/(main)/(public)/categories/[slug]/locations/page.tsx`, `src/features/locations/category/components/CategoryLocationListClient.tsx`, route constant `CATEGORY_LOCATIONS`, `locationService.getByCategory`, i18n `locations.json`, deploy/review artifacts ngay `2026-05-23`. |
| Admin | `admin_users_edit` | `/admin/users/:id/edit` | Co `src/pages/Users/UserEdit/index.tsx`, `UserEditForm.tsx`, route `USERS_EDIT`, lazy route, API/hook/schema updates, deploy/review/test artifacts ngay `2026-05-23`. |
| Admin/API hardening | Booking list filter/loading, report filters, invoice PDF | `/admin/bookings`, `/admin/reports/*`, `/admin/bookings/{id}/invoice`, `/user/bookings/{id}/invoice` | Admin co loading list/refetch cho bookings, filter `user_id`, report param sanitization/mappers, CustomSelect report bars. API co `InvoicePdfService` va admin/user invoice routes. |
| API | Category locations and booking user filter support | `GET /categories/{slug}/locations`, `GET /admin/bookings?user_id=` | Backend co `LocationsBySlugCategoryRequest`, category repository/service alignment, `IndexBookingRequest.user_id`, booking repository filter/status counts. |

### Current locked screens for next implementation

| Project | Last completed screen | Next locked screen | Route | Current code status | Reason |
|---|---|---|---|---|---|
| Web | `user-locations-by-category` | `user-locations-nearby` | `/nearby` | Chua thay App Router page rieng; backend co `GET /locations/nearby` va `GET /locations/{id}/nearby`. | Tiep tuc cum public locations sau category, API da san sang, co the tai su dung location grid/filter/card. |
| Admin | `admin_users_edit` | `admin_contacts` | `/admin/contacts` | Chua thay page/module admin contacts; backend co list/detail/reply/delete/export contacts. | Sau khi reports va users cluster da khep, contacts la support tool doc lap co API san sang. |

### Updated counts

| Project | Total main screens | Deploy-completed | In progress | Not started | Completion % | Next selected screen |
|---|---:|---:|---:|---:|---:|---|
| Web | 35 | 17 | 0 | 18 | 48.6% | `user-locations-nearby` |
| Admin | 40 | 18 | 0 | 22 | 45.0% | `admin_contacts` |

### Updated code-level counts

| Project | Total documented main screens | Screens with route/page code | Screens without route/page code | Code coverage |
|---|---:|---:|---:|---:|
| Web | 35 | 29 | 6 | 82.9% |
| Admin | 40 | 26 | 14 | 65.0% |

### Codegraph / repo verification notes

| Project | Verification |
|---|---|
| Web | `.codegraph/codegraph.db` cap nhat luc `2026-05-24 01:41`; repo scan xac nhan route category locations da ton tai. `npm run build` nhan dynamic route `/[locale]/categories/[slug]/locations`. Dev server can chay `next dev --webpack` de tranh Turbopack dev manifest 404 cho route dong long sau. |
| Admin | `.codegraph/codegraph.db` cap nhat luc `2026-05-24 01:42`; repo scan xac nhan `Users/UserEdit` da ton tai va route users cluster da co list/detail/create/edit. |
| API | `.codegraph/codegraph.db` cap nhat luc `2026-05-24 01:42`; repo scan xac nhan public category locations, admin booking invoice, user booking invoice va booking `user_id` filter da co trong `routes/api.php`/controller/request/repository. |

### Validation snapshot

| Project | Validation |
|---|---|
| Web | `npm.cmd run typecheck` PASS, `npm.cmd run check:routes` PASS, `npm.cmd run build` PASS sau khi cho phep ghi Wrangler log ngoai sandbox. Runtime test: `http://localhost:3000/categories/ca-phe-tra-sua/locations` tra `200` khi dev server chay webpack. |
| Admin | Sau cac fix gan nhat: `npm.cmd run typecheck` PASS, `npm.cmd run lint` PASS voi 1 warning cu o `Users/UserEdit/components/UserEditForm.tsx`. |
| API | `php -l` PASS cho cac file invoice/controller da them; route list xac nhan co `api/v1/admin/bookings/{id}/invoice`. |

### Selection notes

| Project | Notes |
|---|---|
| Web | `user-locations-by-category` da xong, chi quay lai neu bugfix/hardening. `user-locations-nearby` la ung vien tiep theo vi nam cung cum locations va backend endpoint da san sang. |
| Admin | `admin_users_edit` da xong, users management cluster da du list/detail/create/edit. `bookings-detail-typography`, report filters, invoice PDF la hardening/fix, khong tinh them man moi. `admin_contacts` la man doc lap tiep theo co API san sang. |

### Next execution order

1. Web: cap nhat prompt `danangtrip-web/.agent/skills/STACK_SKILLS_INDEX.md` sang `user-locations-nearby`, sau do chay Step 01 -> Step 10.
2. Admin: cap nhat prompt `danangtrip-admin/.agent/skills/STACK_SKILLS_INDEX.md` sang `admin_contacts`, sau do chay Step 01 -> Step 10.
3. API: chi can mo rong khi hai man tiep theo thieu contract; hien tai ca hai nhom deu co endpoint nen uu tien frontend delivery.
4. Completed screens chi hardening-only: `user-locations-by-category`, `user-my-ratings`, `admin_users_list/detail/create/edit`, reports cluster, booking invoice.

---

## 0.0.7 Current next-screen override - 2026-05-23

Phan nay la nguon chuan moi nhat sau khi doc lai repo thuc te, artifacts Step 10 va `.codegraph` cua `danangtrip-web` / `danangtrip-admin`.
Neu cac phan cu ben duoi con khoa `user-my-ratings` hoac `admin_users_create`, hay xem chung la da loi thoi.

### Completed since previous override

| Project | Completed screen | Route | Evidence |
|---|---|---|---|
| Web | `user-my-ratings` | `/profile/ratings` | Co `src/app/[locale]/(main)/(protected)/profile/ratings/page.tsx`, `src/features/profile/ratings`, i18n `ratings.json`, deploy/review artifacts Step 10 ngay `2026-05-23`. |
| Admin | `admin_users_create` | `/admin/users/create` | Co `src/pages/Users/UserCreate/index.tsx`, `UserCreateForm.tsx`, route `ROUTES.USERS_CREATE`, lazy route, validation schema, deploy/review/test artifacts Step 10 ngay `2026-05-23`. |

### Current locked screens for next implementation

| Project | Last completed screen | Next locked screen | Route | Prompt updated | Current code status |
|---|---|---|---|---|---|
| Web | `user-my-ratings` | `user-locations-by-category` | `/categories/{slug}/locations` | `D:\DATN\danangtrip-web\.agent\skills\STACK_SKILLS_INDEX.md` | Chua co route/page/component; backend co `GET /categories/{slug}/locations`; repo co location list components de tai su dung. |
| Admin | `admin_users_create` | `admin_users_edit` | `/admin/users/{id}/edit` | `D:\DATN\danangtrip-admin\.agent\skills\STACK_SKILLS_INDEX.md` | Chua co route/page/component; backend co `GET /admin/users/{id}` va `PUT /admin/users/{id}`; create/detail/list da co code. |

### Updated counts

| Project | Total main screens | Deploy-completed | In progress | Not started | Completion % | Next selected screen |
|---|---:|---:|---:|---:|---:|---|
| Web | 35 | 16 | 0 | 19 | 45.7% | `user-locations-by-category` |
| Admin | 40 | 17 | 0 | 23 | 42.5% | `admin_users_edit` |

### Updated code-level counts

| Project | Total documented main screens | Screens with route/page code | Screens without route/page code | Code coverage |
|---|---:|---:|---:|---:|
| Web | 35 | 28 | 7 | 80.0% |
| Admin | 40 | 25 | 15 | 62.5% |

### Selection notes

| Project | Notes |
|---|---|
| Web | `user-my-ratings` is complete and must not be selected again except for bugfix/hardening. `user-locations-by-category` is selected because it has a ready public API, no route/page code, and can reuse the locations list module. `user_booking_invoice` remains an action flow from booking detail unless a standalone page is explicitly requested. |
| Admin | `admin_users_create` is complete and must not be selected again except for bugfix/hardening. `admin_users_edit` is the next missing screen in the users management cluster after list/detail/create. |

### Next execution order

1. Web: start `user-locations-by-category` from Step 01, then continue through Step 10.
2. Admin: start `admin_users_edit` from Step 01, then continue through Step 10.
3. Keep prompts independent: Web prompt must not depend on admin state, and admin prompt must not depend on web state.
4. Only implement screens that still lack route/page/component code; completed screens are hardening-only.

---

## 0.0.6 Current next-screen override - 2026-05-23

Phan nay la nguon chuan moi nhat sau khi doc lai repo thuc te, artifacts, va `.codegraph` cua `danangtrip-web` / `danangtrip-admin`.
Neu cac phan cu ben duoi con khoa `user-recommendations` hoac `admin_users_detail`, hay xem chung la da loi thoi.

### Completed / code-completed since previous override

| Project | Completed screen | Route | Evidence |
|---|---|---|---|
| Web | `user-recommendations` | `/recommendations` | Co `src/app/[locale]/(main)/(protected)/recommendations/page.tsx`, `src/features/recommendations`, i18n `recommendations.json`, deploy/review artifacts Step 10 ngay `2026-05-23`. |
| Admin | `admin_users_detail` | `/admin/users/:id` | Co `src/pages/Users/UserDetail/index.tsx`, route `ROUTES.USERS_DETAIL`, lazy route, user detail API/hook/components, test report va walkthrough ngay `2026-05-23`. Luu y: chua thay deploy artifact rieng `admin_users_detail`; neu can co the backfill Step 10 rieng, nhung khong chon lai lam man tiep theo. |

### Current locked screens for next implementation

| Project | Last completed screen | Next locked screen | Route | Prompt updated | Current code status |
|---|---|---|---|---|---|
| Web | `user-recommendations` | `user-my-ratings` | `/profile/ratings` | `D:\DATN\danangtrip-web\.agent\skills\STACK_SKILLS_INDEX.md` | Chua co route/page/component; API constants/service co `GET /user/ratings`, `PUT /ratings/{id}`, `DELETE /ratings/{id}`. |
| Admin | `admin_users_detail` | `admin_users_create` | `/admin/users/create` | `D:\DATN\danangtrip-admin\.agent\skills\STACK_SKILLS_INDEX.md` | Chua co route/page/component; list da tro toi `/admin/users/create`; backend co `POST /admin/users`. |

### Updated counts

| Project | Total main screens | Deploy-completed | In progress | Not started | Completion % | Next selected screen |
|---|---:|---:|---:|---:|---:|---|
| Web | 35 | 15 | 0 | 20 | 42.9% | `user-my-ratings` |
| Admin | 40 | 16 | 0 | 24 | 40.0% | `admin_users_create` |

### Updated code-level counts

| Project | Total documented main screens | Screens with route/page code | Screens without route/page code | Code coverage |
|---|---:|---:|---:|---:|
| Web | 35 | 27 | 8 | 77.1% |
| Admin | 40 | 24 | 16 | 60.0% |

### Selection notes

| Project | Notes |
|---|---|
| Web | `user-recommendations` is complete and must not be selected again except for bugfix/hardening. `user-my-ratings` is the next protected account screen with real API and no route/page code. |
| Admin | `admin_users_detail` has code and verification evidence, but no dedicated deploy report artifact was found. Do not reselect it as the next implementation screen unless the explicit task is Step 10 backfill. `admin_users_create` is next because the users list already links to `/admin/users/create` and the backend create API exists. |

### Next execution order

1. Web: start `user-my-ratings` from Step 01, then continue through Step 10.
2. Admin: start `admin_users_create` from Step 01, then continue through Step 10.
3. Keep prompts independent: Web prompt must not depend on admin state, and admin prompt must not depend on web state.
4. Only implement screens that still lack route/page/component code; completed screens are hardening-only.

---

## 0.0.5 Current next-screen override - 2026-05-23

Phần này là nguồn chuẩn mới nhất sau khi đọc lại repo thật, artifacts Step 10 và `.codegraph` của `danangtrip-web` / `danangtrip-admin`.
Nếu các phần cũ bên dưới còn khóa `user-reset-password` hoặc `admin_users_list`, hãy xem chúng là đã lỗi thời.

### Completed since previous override

| Project | Completed screen | Route | Evidence |
|---|---|---|---|
| Web | `user-reset-password` | `/reset-password` | Có `src/app/[locale]/(auth)/reset-password/page.tsx`, `src/features/auth/components/reset-password-form.tsx`, i18n `reset-password.json`, deploy/review artifacts Step 10 ngày `2026-05-23`. |
| Admin | `admin_users_list` | `/admin/users` | Có `src/pages/Users/UserList/index.tsx`, route `ROUTES.USERS_LIST`, lazy route, user API/hook/mapper/components, deploy/review artifacts Step 10 ngày `2026-05-23`. |

### Current locked screens for next implementation

| Project | Last completed screen | Next locked screen | Route | Prompt updated | Current code status |
|---|---|---|---|---|---|
| Web | `user-reset-password` | `user-recommendations` | `/recommendations` | `D:\DATN\danangtrip-web\.agent\skills\STACK_SKILLS_INDEX.md` | Chưa có route/page/component; backend có `GET /recommendations`, docs có `user_recommendations.md`. |
| Admin | `admin_users_list` | `admin_users_detail` | `/admin/users/:id` | `D:\DATN\danangtrip-admin\.agent\skills\STACK_SKILLS_INDEX.md` | Chưa có route/page/component; backend có `GET /admin/users/{id}`, `/bookings`, `/ratings`, status/role/delete APIs. |

### Updated counts

| Project | Total main screens | Deploy-completed | In progress | Not started | Completion % | Next selected screen |
|---|---:|---:|---:|---:|---:|---|
| Web | 35 | 14 | 0 | 21 | 40.0% | `user-recommendations` |
| Admin | 40 | 16 | 0 | 24 | 40.0% | `admin_users_detail` |

### Updated code-level counts

| Project | Total documented main screens | Screens with route/page code | Screens without route/page code | Code coverage |
|---|---:|---:|---:|---:|
| Web | 35 | 26 | 9 | 74.3% |
| Admin | 40 | 23 | 17 | 57.5% |

### Selection notes

| Project | Notes |
|---|---|
| Web | `user-reset-password` is complete and must not be selected again except for bugfix/hardening. `user-booking-invoice` already has feature artifacts and invoice action integration in booking detail, so the next standalone missing route with ready API is `user-recommendations`. |
| Admin | `admin_users_list` is complete and must not be selected again except for bugfix/hardening. The next user-management screen after list is `admin_users_detail`, because the list already links conceptually into detail/edit workflows and backend detail/bookings/ratings endpoints exist. |

### Next execution order

1. Web: start `user-recommendations` from Step 01, then continue through Step 10.
2. Admin: start `admin_users_detail` from Step 01, then continue through Step 10.
3. Keep prompts independent: Web prompt must not depend on admin state, and admin prompt must not depend on web state.
4. Only implement screens that still lack route/page/component code; completed screens are hardening-only.

---

## 0.0.4 Next-screen lock override - 2026-05-23

Phan nay cap nhat sau khi nguoi dung da hoan tat dot code truoc, doc lai repo thuc te va doc `.codegraph` cua Web/Admin. Neu cac phan cu ben duoi con ghi prompt dang khoa `user-forgot-password` hoac `admin_reports_users`, uu tien dung phan nay lam nguon chuan moi nhat.

### Current locked screens for next implementation

| Project | Last completed screen | Next locked screen | Route | Prompt updated | Current code status |
|---|---|---|---|---|---|
| Web | `user-forgot-password` | `user-reset-password` | `/reset-password` | `D:\DATN\danangtrip-web\.agent\skills\STACK_SKILLS_INDEX.md` | No route/page/component found; API/type/service/schema partially exist |
| Admin | `admin_reports_users` | `admin_users_list` | `/admin/users` | `D:\DATN\danangtrip-admin\.agent\skills\STACK_SKILLS_INDEX.md` | No route/page found; sidebar path and backend APIs exist |

### Codegraph/repo verification

| Project | Evidence | Decision |
|---|---|---|
| Web | `.codegraph` has no file path matching `reset-password`; repo grep has no `src/app/[locale]/(auth)/reset-password/page.tsx` and no `reset-password-form.tsx`. It does have `ResetPasswordRequest`, `ResetPasswordData`, `resetPasswordSchema`, `API_ENDPOINTS.AUTH.RESET_PASSWORD`, and `authService.resetPassword`. | Select `user-reset-password` as the next Web screen. Step 03 must align frontend schema/type with backend because backend requires `email`, `token`, `password`, and `password_confirmation`. |
| Admin | `.codegraph` has no `src/pages/Users`, no `UserList`, no `UsersList`, and no `/admin/users` UI node. Repo has only sidebar link `/admin/users`; router has no `USERS_LIST` route. Backend has `GET /admin/users`, export, status, role, delete, create, update, detail, bookings, ratings routes. | Select `admin_users_list` as the next Admin screen. Step 03 must use backend-supported filters only: `q`, `role`, `status`, `page`, `per_page`, `sort_by`, `sort_order`. |

### Delivery counts remain unchanged

| Project | Total main screens | Deploy-completed | In progress | Not started | Completion % | Next selected screen |
|---|---:|---:|---:|---:|---:|---|
| Web | 35 | 13 | 0 | 22 | 37.1% | `user-reset-password` |
| Admin | 40 | 15 | 0 | 25 | 37.5% | `admin_users_list` |

### Next execution order

1. Web: start `user-reset-password` from `01-screen-analysis`, then continue through Step 10.
2. Admin: start `admin_users_list` from `01-screen-analysis`, then continue through Step 10.
3. Keep prompts independent: Web prompt must not depend on admin state, and admin prompt must not depend on web state.
4. Do not reselect completed screens `user-forgot-password` or `admin_reports_users` except for hardening/bugfix work.

---

## 0.0.3 Step 10 completion override - 2026-05-23

Phan nay cap nhat sau khi kiem tra lai code moi cua hai repo va chay Step 10 revalidation cho ca Web/Admin.

### Completed in this update

| Project | Completed feature | Route | Step 10 status | Validation |
|---|---|---|---|---|
| Web | `user-forgot-password` | `/forgot-password` | Completed and revalidated | `npm.cmd run prepush:check` PASS after rerun outside sandbox |
| Admin | `admin_reports_users` | `/admin/reports/users` | Completed and revalidated | `npm.cmd run prepush:check` PASS |

### Updated delivery counts

| Project | Total main screens | Deploy-completed | In progress | Not started | Completion % | Next missing-code screen |
|---|---:|---:|---:|---:|---:|---|
| Web | 35 | 13 | 0 | 22 | 37.1% | `user-reset-password` |
| Admin | 40 | 15 | 0 | 25 | 37.5% | `admin_users_list` |

### Updated code-level counts

| Project | Total documented main screens | Screens with route/page code | Screens without route/page code | Code coverage |
|---|---:|---:|---:|---:|
| Web | 35 | 25 | 10 | 71.4% |
| Admin | 40 | 22 | 18 | 55.0% |

### Verification notes

- Web Step 10 fix: resend success toast now waits for `POST /auth/forgot-password` success before showing success.
- Web first sandbox validation failed because Wrangler could not write to `AppData\Roaming\xdg.config`; rerun outside sandbox passed.
- Admin Step 10 fix: mock mode now disables the real `GET /admin/reports/users` query instead of continuing to fetch in the background.
- Admin validation included Playwright console check: 5/5 routes passed, including `/admin/reports/users`.
- Remaining warnings are non-blocking: Web Next middleware/proxy deprecation and experimental edge runtime; Admin `lottie-web` eval warning and large vendor chunks.

---

## 0.0.2 Implemented-code audit override - 2026-05-23

Phan nay la audit moi nhat theo tieu chi `man da lam roi` = da co route/page/component code trong repo hien tai. Phan nay khac voi `deploy-report`: mot man co the da co code that nhung chua co deploy artifact rieng. Neu cac bang cu ben duoi mau thuan, uu tien dung phan override nay de biet man nao da co code va man nao con chua co code.

### Audit source

- Web route scan: `D:\DATN\danangtrip-web\src\app\[locale]\**\page.tsx`
- Web route config: `D:\DATN\danangtrip-web\src\config\routes.ts`
- Web feature folders: `D:\DATN\danangtrip-web\src\features`
- Web codegraph: `D:\DATN\danangtrip-web\.codegraph\codegraph.db`
- Admin page scan: `D:\DATN\danangtrip-admin\src\pages\**\index.tsx`
- Admin route config: `D:\DATN\danangtrip-admin\src\routes\routes.ts`
- Admin router: `D:\DATN\danangtrip-admin\src\routes\index.tsx`
- Admin codegraph: `D:\DATN\danangtrip-admin\.codegraph\codegraph.db`

### Code-level progress summary

| Project | Total documented main screens | Screens with route/page code | Screens without route/page code | Code coverage | Next screen under no-code rule |
|---|---:|---:|---:|---:|---|
| Web | 35 | 25 | 10 | 71.4% | `user-reset-password` |
| Admin | 40 | 22 | 18 | 55.0% | `admin_users_list` |

Deployment pipeline counts remain separate:

- Web deploy-completed count is now `13 / 35` from feature deploy artifacts.
- Admin deploy-completed count is now `15 / 40` from feature deploy artifacts.
- This audit is for implementation/code existence, not final delivery readiness.

### Web screens with route/page code

| Feature slug / Doc | Route | Evidence |
|---|---|---|
| `user_home.md` | `/` | `src\app\[locale]\(main)\page.tsx` |
| `user_search.md` | `/search` | `src\app\[locale]\(main)\(public)\search\page.tsx` |
| `user_contact.md` | `/contact` | `src\app\[locale]\(main)\(public)\contact\page.tsx` |
| `user_blog_list.md` | `/blog` | `src\app\[locale]\(main)\(public)\blog\page.tsx` |
| `user_blog_detail.md` | `/blog/{slug}` | `src\app\[locale]\(main)\(public)\blog\[slug]\page.tsx` |
| `user_destination_tour_landing.md` | `/du-lich-da-nang` | `src\app\[locale]\(main)\(public)\du-lich-da-nang\page.tsx`; codegraph confirms path |
| `user_locations_list.md` | `/locations` | `src\app\[locale]\(main)\(public)\locations\page.tsx` |
| `user_location_detail.md` | `/locations/{slug}` | `src\app\[locale]\(main)\(public)\locations\[slug]\page.tsx` |
| `user_tours_list.md` | `/tours` | `src\app\[locale]\(main)\(public)\tours\page.tsx` |
| `user_tour_detail.md` | `/tours/{slug}` | `src\app\[locale]\(main)\(public)\tours\[slug]\page.tsx` |
| `user_tour_departure_select.md` | `/tours/{slug}/departures` | `src\app\[locale]\(main)\(public)\tours\[slug]\departures\page.tsx` |
| `user_tour_booking.md` | `/tours/{slug}/book` | `src\app\[locale]\(main)\(protected)\tours\[slug]\book\page.tsx` |
| `user_payment.md` | `/payment` | `src\app\[locale]\(main)\(protected)\payment\page.tsx` |
| `user_payment_result.md` | `/payment/result` | `src\app\[locale]\(main)\(protected)\payment\result\page.tsx` |
| `user_bookings_list.md` | `/bookings` | `src\app\[locale]\(main)\(protected)\bookings\page.tsx` |
| `user_booking_detail.md` | `/bookings/{id}` | `src\app\[locale]\(main)\(protected)\bookings\[id]\page.tsx` |
| `user_booking_by_code.md` | `/bookings/code/{bookingCode}` | `src\app\[locale]\(main)\(protected)\bookings\code\[bookingCode]\page.tsx`; codegraph confirms path |
| `user_favorites.md` | `/favorites` | `src\app\[locale]\(main)\(protected)\favorites\page.tsx` |
| `user_notifications.md` | `/notifications` | `src\app\[locale]\(main)\(protected)\notifications\page.tsx` |
| `user_profile.md` | `/profile` | `src\app\[locale]\(main)\(protected)\profile\page.tsx` |
| `user_profile_password.md` | `/profile/password` | `src\app\[locale]\(main)\(protected)\profile\password\page.tsx`; codegraph confirms path |
| `user_login.md` | `/login` | `src\app\[locale]\(auth)\login\page.tsx`; `src\features\auth\components\login-form.tsx`; codegraph confirms both |
| `user_register.md` | `/register` | `src\app\[locale]\(auth)\register\page.tsx`; `src\features\auth\components\register-form.tsx`; codegraph confirms both |
| `user_verify_email.md` | `/verify-email` | `src\app\[locale]\(auth)\verify-email\page.tsx`; `src\features\auth\components\verify-email-form.tsx`; codegraph confirms both |
| `user_forgot_password.md` | `/forgot-password` | `src\app\[locale]\(auth)\forgot-password\page.tsx`; `src\features\auth\components\forgot-password-form.tsx`; Step 10 completed 2026-05-23 |

### Web screens without route/page code

| Feature slug / Doc | Expected route | Current code status | Recommendation |
|---|---|---|---|
| `user_reset_password.md` | `/reset-password` | No route/page/component found; API/type/service exist | Next Web screen |
| `user_booking_invoice.md` | `/bookings/{id}/invoice` | Invoice API/service exists, but no standalone screen route found | Implement screen or intentionally keep as booking-detail action |
| `user_recommendations.md` | `/recommendations` | No route/page found | Backlog |
| `user_my_ratings.md` | `/profile/ratings` | No route/page found; API constants mention `/user/ratings` | Backlog |
| `user_locations_by_category.md` | `/categories/{slug}/locations` | Service exists, no route/page found | Backlog |
| `user_locations_nearby.md` | `/nearby` | Nearby service exists, no route/page found | Backlog |
| `user_tours_by_category.md` | `/tour-categories/{slug}/tours` | API constants exist, no route/page found | Backlog |
| `user_blog_by_category.md` | `/blog?category_id={id}` or category route | No dedicated route/page found | Backlog |
| `user_profile_delete.md` | `/profile/delete` | No route/page found | Backlog / API readiness check |
| `user_cart.md` | `/cart` | No route/page found | Backlog / planned API |

### Admin screens with route/page code

| Feature slug / Doc | Route | Evidence |
|---|---|---|
| `admin_dashboard.md` | `/dashboard` | `src\pages\Dashboard\index.tsx`; registered in `src\routes\index.tsx` |
| `admin_tours_list.md` | `/admin/tours/list` | `src\pages\Tours\TourList\index.tsx`; route constant `TOURS_LIST` |
| `admin_tours_create.md` | `/admin/tours/create` | `src\pages\Tours\TourCreate\index.tsx`; route constant `TOURS_CREATE` |
| `admin_tours_edit.md` | `/admin/tours/edit/:id` | `src\pages\Tours\TourEdit\index.tsx`; route constant `TOURS_EDIT` |
| `admin_tour_categories.md` | `/admin/tours/categories` | `src\pages\Tours\TourCategories\index.tsx`; route constant `TOURS_CATEGORIES` |
| `admin_tour_schedules_list.md` | `/admin/tours/schedules` | `src\pages\Tours\TourSchedules\index.tsx`; route constant `TOURS_SCHEDULES` |
| `admin_tour_schedules_create.md` | `/admin/tours/:id/schedules/create` | `src\pages\Tours\TourScheduleCreate\index.tsx`; route constant `TOURS_SCHEDULE_CREATE` |
| `admin_tour_schedules_edit.md` | `/admin/tours/schedules/edit/:id` | `src\pages\Tours\TourScheduleEdit\index.tsx`; route constant `TOURS_SCHEDULE_EDIT` |
| `admin_locations_list.md` | `/admin/locations` | `src\pages\Locations\LocationList\index.tsx`; route constant `LOCATIONS_LIST` |
| `admin_locations_create.md` | `/admin/locations/create` | `src\pages\Locations\LocationCreate\index.tsx`; route constant `LOCATIONS_CREATE` |
| `admin_locations_edit.md` | `/admin/locations/edit/:id` | `src\pages\Locations\LocationEdit\index.tsx`; route constant `LOCATIONS_EDIT` |
| `admin_locations_detail.md` | `/admin/locations/detail/:id` | `src\pages\Locations\LocationDetail\index.tsx`; route constant `LOCATIONS_DETAIL` |
| `admin_location_categories.md` | `/admin/locations/categories` | `src\pages\Locations\LocationCategories\index.tsx`; route constant `LOCATIONS_CATEGORIES` |
| `admin_bookings_list.md` | `/admin/bookings` | `src\pages\Bookings\BookingList\index.tsx`; route constant `BOOKINGS_LIST` |
| `admin_bookings_detail.md` | `/admin/bookings/:id` | `src\pages\Bookings\BookingDetail\index.tsx`; route constant `BOOKINGS_DETAIL` |
| `admin_payments_list.md` | `/admin/payments` | `src\pages\Payments\PaymentList\index.tsx`; route constant `PAYMENTS_LIST` |
| `admin_payments_detail.md` | `/admin/payments/:id` | `src\pages\Payments\PaymentDetail\index.tsx`; route constant `PAYMENTS_DETAIL` |
| `admin_reports_ratings.md` | `/admin/reports/ratings` | `src\pages\Reports\RatingsReport\index.tsx`; route constant `REPORTS_RATINGS` |
| `admin_reports_bookings.md` | `/admin/reports/bookings` | `src\pages\Reports\BookingsReport\index.tsx`; route constant `REPORTS_BOOKINGS` |
| `admin_reports_revenue.md` | `/admin/reports/revenue` | `src\pages\Reports\RevenueReport\index.tsx`; route constant `REPORTS_REVENUE`; codegraph confirms report files |
| `admin_reports_locations.md` | `/admin/reports/locations` | `src\pages\Reports\LocationReport\index.tsx`; route constant `REPORTS_LOCATIONS`; codegraph confirms report files |
| `admin_reports_users.md` | `/admin/reports/users` | `src\pages\Reports\UsersReport\index.tsx`; route constant `REPORTS_USERS`; Step 10 completed 2026-05-23 |

### Admin screens without route/page code

| Feature slug / Doc | Expected route | Current code status | Recommendation |
|---|---|---|---|
| `admin_users_list.md` | `/admin/users` | No page/route found | Next Admin screen |
| `admin_users_detail.md` | `/admin/users/{id}` | No page/route found | Backlog |
| `admin_users_create.md` | `/admin/users/create` | No page/route found | Backlog |
| `admin_users_edit.md` | `/admin/users/{id}/edit` | No page/route found | Backlog |
| `admin_contacts.md` | `/admin/contacts` | API constants/fallback counts exist, no page/route found | Backlog |
| `admin_notifications_list.md` | `/admin/notifications` | No page/route found | Backlog |
| `admin_notifications_send.md` | `/admin/notifications/send` | No page/route found | Backlog |
| `admin_blog_posts_list.md` | `/admin/blog-posts` | No page/route found | Backlog |
| `admin_blog_posts_create.md` | `/admin/blog-posts/create` | No page/route found | Backlog |
| `admin_blog_posts_edit.md` | `/admin/blog-posts/{id}/edit` | No page/route found | Backlog |
| `admin_blog_categories.md` | `/admin/blog-categories` | No page/route found | Backlog |
| `admin_ratings_list.md` | `/admin/ratings` | No page/route found | Backlog |
| `admin_tags_amenities.md` | `/admin/tags-amenities` or split route | API/helper references exist through location module, no standalone page/route found | Backlog |
| `admin_subcategories.md` | `/admin/subcategories` or category tab | No standalone page/route found | Backlog |
| `admin_tours_detail.md` | `/admin/tours/{id}` | No detail page/route found | Backlog |
| `admin_promotions.md` | `/admin/promotions` | No page/route found | Planned backlog |
| `admin_site_settings.md` | `/admin/settings` | No page/route found | Planned backlog |
| `admin_landing_pages.md` | `/admin/landing-pages` | No page/route found | Planned backlog |

### Updated no-code implementation order

1. Web: implement `user-reset-password` next because forgot-password is now completed.
2. Admin: implement `admin_users_list` next because reports users is now completed and the admin users module has no page/route yet.
3. Keep older completed screens in hardening backlog only if product quality review requires it.

---

## 0.0.1 No-code-only next screen selection override - 2026-05-23

Phan nay cap nhat sau khi doc lai bao cao tien do, codegraph va repo thuc te cua `danangtrip-web`, `danangtrip-admin`, `danangtrip-api`. Tieu chi moi: chi chon man tiep theo neu man do chua co route/page/component code trong repo hien tai. Neu mot man da co code that nhung chua co deploy artifact rieng, khong chon lam man tiep theo trong dot nay; chi dua vao backlog hardening sau.

Neu cac bang cu ben duoi con ghi `user-verify-email`, `admin_reports_locations`, `user-login`, hoac `user-register` la man dang lam/ke tiep, hay dung phan override nay lam nguon chuan moi nhat.

### Source checked

- Progress report: `D:\DATN\DATN_Document\docs\project_delivery_progress_report.md`
- Web repo: `D:\DATN\danangtrip-web`
- Admin repo: `D:\DATN\danangtrip-admin`
- Backend repo: `D:\DATN\danangtrip-api`
- Web prompt: `D:\DATN\danangtrip-web\.agent\skills\STACK_SKILLS_INDEX.md`
- Admin prompt: `D:\DATN\danangtrip-admin\.agent\skills\STACK_SKILLS_INDEX.md`
- Web codegraph: `D:\DATN\danangtrip-web\.codegraph`
- Admin codegraph: `D:\DATN\danangtrip-admin\.codegraph`

### Current completion status

| Project | Completed | In progress | Not started | Completion % | Last completed feature |
|---|---:|---:|---:|---:|---|
| Web | 12 / 35 | 0 | 23 | 34.3% | `user-verify-email` Step 10 completed |
| Admin | 14 / 40 | 0 | 26 | 35.0% | `admin_reports_locations` Step 10 completed |

### Next selected screens

| Project | Next selected screen | Feature slug | Route | Prompt status | Reason |
|---|---|---|---|---|---|
| Web | User Forgot Password | `user-forgot-password` | `/forgot-password` | Step 01 pending in web prompt | Re-check found `/login` and `/register` already have route/form code; `/forgot-password` has API/service support but no frontend route/page yet. |
| Admin | Admin Reports Users | `admin_reports_users` | `/admin/reports/users` | Step 01 pending in admin prompt | Report cluster has completed ratings/bookings/revenue/locations; backend users report endpoint exists but admin frontend screen is missing. |

### No-code-only audit summary

| Project | Screen checked | Code status | Decision |
|---|---|---|---|
| Web | `user-login` (`/login`) | Code exists: `src\app\[locale]\(auth)\login\page.tsx`, `src\features\auth\components\login-form.tsx` | Exclude from next implementation; hardening-only later if needed |
| Web | `user-register` (`/register`) | Code exists: `src\app\[locale]\(auth)\register\page.tsx`, `src\features\auth\components\register-form.tsx` | Exclude from next implementation; hardening-only later if needed |
| Web | `user-forgot-password` (`/forgot-password`) | No route/page/component/i18n found; API/type/service exist | Select as next Web screen |
| Web | `user-reset-password` (`/reset-password`) | No route/page/component found | Keep as next missing-code backlog after forgot-password |
| Admin | `admin_reports_locations` (`/admin/reports/locations`) | Code exists: `src\pages\Reports\LocationReport\index.tsx` and route registration | Exclude from next implementation; already completed Step 10 |
| Admin | `admin_reports_users` (`/admin/reports/users`) | No `src\pages\Reports\UsersReport`, no route constant, no lazy route, no report API/hook/mapper found | Select as next Admin screen |

### Repo reality found

- Web `user-login`: route exists at `src\app\[locale]\(auth)\login\page.tsx`; form exists at `src\features\auth\components\login-form.tsx`; API path is `POST /auth/login`; therefore it is not selected as the next new route/page screen.
- Web `user-register`: route exists at `src\app\[locale]\(auth)\register\page.tsx`; form exists at `src\features\auth\components\register-form.tsx`; therefore it is also not selected as the next new route/page screen.
- Web `user-forgot-password`: API endpoint/type/service exist (`POST /auth/forgot-password`), but no route/page/component/i18n exists yet. Also fix the login form forgot-password link currently pointing to `ROUTES.CONTACT`.
- Admin `admin_reports_users`: backend route exists as `GET /admin/reports/users`; backend request currently supports `year` only; admin frontend has no `UsersReport` page, no route constant, no lazy route, no report API method, no hook, and no mapper yet.
- Admin issue to verify in Step 01-03: docs mention filters/KPIs beyond current backend payload; implementation must not fabricate unsupported role/status/active-user data.

### Next implementation order

1. Web: start `user-forgot-password` from `01-screen-analysis`, then continue through Step 10.
2. Admin: start `admin_reports_users` from `01-screen-analysis`, then continue through Step 10.
3. Keep the two prompts independent. Web progress must not reference admin state as its active screen, and admin progress must not reference web state as its active screen.

---

## 0.0 Step 10 completion override - 2026-05-22

Phan nay cap nhat sau khi hoan tat Step 10 cho ca hai du an. Neu cac bang cu ben duoi con ghi `user-verify-email` hoac `admin_reports_locations` la `In progress`, hay dung phan nay lam nguon chuan moi nhat.

| Project | Completed | In progress | Not started | Completion % | Current status |
|---|---:|---:|---:|---:|---|
| Web | 12 / 35 | 0 | 23 | 34.3% | `user-verify-email` Step 10 completed |
| Admin | 14 / 40 | 0 | 26 | 35.0% | `admin_reports_locations` Step 10 completed |

Completed in this update:

- Web: `user-verify-email` completed with deploy/review artifacts, corrected authenticated OTP contract, and passing `lint`, `typecheck`, `build`, `prepush:check`.
- Admin: `admin_reports_locations` completed with feature-specific deploy/review artifacts and passing `lint`, `typecheck`, `build`, `prepush:check`.

Next selection:

- Web: choose the next web screen independently after `user-verify-email`.
- Admin: choose the next admin screen independently after `admin_reports_locations`.

---

## 0. Progress update override - 2026-05-22

Phan nay la trang thai tien trinh moi nhat sau khi doc lai 2 du an `danangtrip-web` va `danangtrip-admin`. Neu cac bang/ghi chu cu ben duoi con mau thuan, uu tien dung phan override nay lam nguon chuan.

### 0.1 Source checked

- Web project: `D:\DATN\danangtrip-web`
- Admin project: `D:\DATN\danangtrip-admin`
- Web working state: `danangtrip-web\.agent\memory\WORKING_STATE.md`
- Admin working state: `danangtrip-admin\.agent\memory\WORKING_STATE.md`
- Web prompt index: `danangtrip-web\.agent\skills\STACK_SKILLS_INDEX.md`
- Admin prompt index: `danangtrip-admin\.agent\skills\STACK_SKILLS_INDEX.md`
- Web route verified: `src\app\[locale]\(auth)\verify-email\page.tsx`
- Admin route verified: `src\pages\Reports\LocationReport\index.tsx`

### 0.2 Current active screens

| Project | Active screen | Feature slug | Route | Current step | Status | Next action |
|---|---|---|---|---|---|---|
| Web | User Verify Email | `user-verify-email` | `/verify-email` | Step 05 - UI components | In progress | Continue Step 06 - data integration, then finish Steps 07-10 |
| Admin | Admin Reports Locations | `admin_reports_locations` | `/admin/reports/locations` | Step 06/07 area - data + UX completion | In progress | Finish integration, validation, review, tests, deploy notes |

### 0.3 Updated delivery counts

| Project | Total main screens | Completed | In progress | Not started | Completion % | Current note |
|---|---:|---:|---:|---:|---:|---|
| Web | 35 | 11 | 1 | 23 | 31.4% | `user-profile-password` is counted completed; `user-verify-email` is active |
| Admin | 40 | 13 | 1 | 26 | 32.5% | `admin_reports_revenue` remains completed; `admin_reports_locations` is active |

### 0.4 Web progress update

- Completed screen added to progress: `user-profile-password`.
- Current active screen: `user-verify-email`.
- Verified artifacts for `user-verify-email`: screen analysis, setup report, API contract, route plan, UI spec.
- Verified route exists: `src\app\[locale]\(auth)\verify-email\page.tsx`.
- Current prompt state: `danangtrip-web\.agent\skills\STACK_SKILLS_INDEX.md` is scoped only to the web project and targets `user-verify-email` from Step 01 to Step 10.
- Next implementation order for web: Step 06 data integration, Step 07 states and validation, Step 08 accessibility/responsive, Step 09 tests, Step 10 review/deploy handoff.

### 0.5 Admin progress update

- Completed admin count remains 13.
- Current active screen: `admin_reports_locations`.
- Verified route exists: `src\pages\Reports\LocationReport\index.tsx`.
- Verified artifacts for `admin_reports_locations`: screen analysis, project audit/setup, API contract, test report.
- Existing implementation notes indicate route registration, sidebar update, i18n key `location_report`, skeleton, and report components are already present.
- Current prompt state: `danangtrip-admin\.agent\skills\STACK_SKILLS_INDEX.md` is scoped only to the admin project and targets `admin_reports_locations` from Step 01 to Step 10.
- Next implementation order for admin: finish data integration, loading/error/empty states, RightSidebar polish, tests, review, deploy handoff.

### 0.6 Cross-project next order

1. Finish `admin_reports_locations` to Step 10 because the admin route/components already exist and the remaining work is closeout/integration quality.
2. Continue `user-verify-email` from Step 06 to Step 10 after the admin report screen is stabilized.
3. After both active screens are completed, select the next backlog screen separately for each project; the two prompt indexes are independent and must not share delivery state.

---

## 1. Dự án `danangtrip-web`

### 1.0 Kiểm kê màn thực tế từ tài liệu

| Hạng mục | Số lượng | Ghi chú |
# Báo cáo Theo dõi Tiến độ Triển khai Dự án

> Ngày cập nhật: 22/05/2026  
> Phạm vi theo dõi:
> - `D:\DATN\danangtrip-web`
> - `D:\DATN\danangtrip-admin`
>  
> Cách tính tiến độ:
> - Tách làm 2 lớp:
>   - `Tổng màn của dự án` theo tài liệu thật trong `docs/page`
>   - `Phạm vi delivery đang theo dõi` theo các màn đã có `deploy-report` hoặc đã được chốt là màn kế tiếp trong rollout hiện tại
> - Với `danangtrip-web`, không tính 5 file component-spec của nhóm rating vào tổng số màn chính.
> - Trạng thái dùng 3 mức: `Chưa làm`, `Đang làm`, `Hoàn thành`.

---

## 1. Dự án `danangtrip-web`

### 1.0 Kiểm kê màn thực tế từ tài liệu

| Hạng mục | Số lượng | Ghi chú |
|---|---:|---|
| Tổng file `user_*` trong `docs/page` | 40 | Bao gồm cả screen spec và component spec |
| Component spec | 5 | `user_rating_modal`, `user_rating_edit_modal`, `user_rating_delete`, `user_rating_helpful`, `user_rating_images_lightbox` |
| Tổng màn chính của web | 35 | Đây là mẫu số đúng để theo dõi tiến độ màn hình |
| Prototype HTML trong `screen/2_User_Flows` | 20 | Chưa bao gồm Guest flows dùng chung như home/search/tour/blog/contact |

### 1.1 Tóm tắt tiến độ

| Chỉ số | Giá trị |
|---|---:|
| Tổng màn chính của dự án | 35 |
| Hoàn thành theo tổng màn | 10 |
| Đang làm theo tổng màn | 0 |
| Chưa làm theo tổng màn | 25 |
| % hoàn thành theo tổng màn | 28.6% |
| Tổng màn đang theo dõi | 11 |
| Hoàn thành | 10 |
| Đang làm | 0 |
| Chưa làm | 1 |
| % hoàn thành trong phạm vi theo dõi | 90.9% |

### 1.2 Schedule / Timeline

| Mốc thời gian | Màn hình | Kết quả |
|---|---|---|
| 10/05/2026 | `contact` | Hoàn thành |
| 16/05/2026 | `tour-detail` | Hoàn thành |
| 17/05/2026 | `tour-booking` | Hoàn thành |
| 17/05/2026 | `tour-payment` | Hoàn thành |
| 19/05/2026 | `tour-departure-select` | Hoàn thành |
| 21/05/2026 | `user-bookings-list` | Hoàn thành |
| 21/05/2026 | `user-booking-detail` | Hoàn thành |
| 22/05/2026 | `favorites` | Hoàn thành |
| 22/05/2026 | `notifications` | Hoàn thành |
| Kế tiếp | `user-profile-password` | Chưa làm |
| Backlog gần | `user-verify-email` | Chưa làm |

### 1.3 Chi tiết trạng thái công việc

| STT | Feature slug / Doc | Tên màn | Route | Trạng thái | Lý do |
|---:|---|---|---|---|---|
| 1 | `contact` | Liên hệ | `/contact` | Hoàn thành | Đã có `deploy-report` ngày `2026-05-10` |
| 2 | `tour-detail` | Chi tiết tour | `/tours/{slug}` | Hoàn thành | Đã có `deploy-report` ngày `2026-05-16` |
| 3 | `tour-booking` | Đặt tour | `/tours/{slug}/book` | Hoàn thành | Đã có `deploy-report` ngày `2026-05-17` |
| 4 | `tour-payment` | Thanh toán tour | Flow thanh toán hiện tại | Hoàn thành | Đã có `deploy-report` ngày `2026-05-17` |
| 5 | `tour-departure-select` | Chọn lịch khởi hành | `/tours/{slug}/departures` hoặc modal tương ứng | Hoàn thành | Đã có `deploy-report` ngày `2026-05-19` |
| 6 | `user-bookings-list` | Lịch sử đặt tour | `/bookings` | Hoàn thành | Đã có `deploy-report` ngày `2026-05-21`; vòng `09-testing` đã được chốt |
| 7 | `user-booking-detail` | Chi tiết đơn đặt tour | `/bookings/{id}` | Hoàn thành | Đã có `deploy-report` ngày `2026-05-21`; route thật đã tồn tại ở `src/app/[locale]/(main)/(protected)/bookings/[id]/page.tsx` |
| 8 | `user-booking-by-code` | Đơn đặt theo mã đơn | `/bookings/code/{code}` | Hoàn thành | Đã có `deploy-report` ngày `2026-05-21`; PR `feat/DATN-80-user-booking-by-code` đã merge vào `dev` |
| 9 | `user_booking_invoice.md` | Hóa đơn booking | `/bookings/{id}/invoice` | Cần hardening | Đã có trong code và có artifact kỹ thuật/nghiệp vụ, nhưng chưa có `deploy-report` nên chưa tính là hoàn thành full pipeline |
| 10 | `favorites` | Yêu thích | `/favorites` | Hoàn thành | Đã có route/page thật và đã đi hết pipeline với `deploy-report` ngày `2026-05-22` |
| 11 | `notifications` | Thông báo người dùng | `/notifications` | Hoàn thành | Đã có route/page thật và đã đi hết pipeline với `deploy-report` ngày `2026-05-22` |

### 1.4 Danh sách đầy đủ các màn web cần làm trong tương lai

| STT | Doc / Feature | Màn hình | Route | Trạng thái | Route/code hiện có | API readiness | Lý do / Ghi chú | Khuyến nghị |
|---:|---|---|---|---|---|---|---|---|
| 1 | `user_booking_detail.md` | Chi tiết đơn đặt tour | `/bookings/{id}` | Hoàn thành | Đã có route detail thật | Ready + Partial | `GET /user/bookings/{id}`, `invoice`, `cancel` có thật; residual risk backend encoding đã được ghi trong deploy report | Đã xong |
| 2 | `user_booking_by_code.md` | Đơn đặt theo mã đơn | `/bookings/code/{booking_code}` | Hoàn thành | Đã có route thật `src/app/[locale]/(main)/(protected)/bookings/code/[bookingCode]/page.tsx` | Ready | API có thật; đã reuse booking detail display | Đã xong |
| 3 | `user_favorites.md` | Yêu thích | `/favorites` | Hoàn thành | Đã có route/page thật | Ready | Đã hoàn thành full pipeline và merge vào `dev` | Đã xong |
| 4 | `user_notifications.md` | Thông báo | `/notifications` | Hoàn thành | Đã có route/page thật | Ready | Bộ API notifications user đã có đầy đủ | Đã xong |
| 5 | `user_profile_password.md` | Đổi mật khẩu | `/profile/password` | Chưa làm | Chưa có route riêng | Ready | `PUT /user/password` có thật | Ưu tiên cao |
| 6 | `user_verify_email.md` | Xác thực email | `/verify-email` | Chưa làm | Chưa có | Ready | `POST /auth/verify-email` có thật | Ưu tiên cao |
| 7 | `user_login.md` | Đăng nhập | `/login` | Chưa làm | Chưa có | Ready | `POST /auth/login` có thật; core auth chưa có delivery riêng | Ưu tiên cao |
| 8 | `user_register.md` | Đăng ký | `/register` | Chưa làm | Chưa có | Ready | `POST /auth/register` có thật | Ưu tiên cao |
| 9 | `user_forgot_password.md` | Quên mật khẩu | `/forgot-password` | Chưa làm | Chưa có | Ready | `POST /auth/forgot-password` có thật | Ưu tiên cao |
| 10 | `user_reset_password.md` | Đặt lại mật khẩu | `/reset-password` | Chưa làm | Chưa có | Ready | `POST /auth/reset-password` có thật | Ưu tiên cao |
| 11 | `user_profile.md` | Hồ sơ cá nhân | `/profile` | Cần hardening | Đã có route/page | Ready | Route có thật nhưng chưa có artifact delivery riêng trong pipeline hiện tại | Hardening |
| 12 | `user_recommendations.md` | Gợi ý cho bạn | `/recommendations` | Chưa làm | Chưa có route riêng | Ready | `GET /recommendations` có thật | Làm sau auth/account |
| 13 | `user_my_ratings.md` | Đánh giá của tôi | `/profile/ratings` | Chưa làm | Chưa có | Ready | `GET /user/ratings` có thật | Làm sau profile |
| 14 | `user_booking_invoice.md` | Hóa đơn booking | `/bookings/{id}/invoice` | Cần hardening | Đã có action PDF trong `BookingDetailClient`, nhưng chưa có `deploy-report` riêng | Ready | API `GET /user/bookings/{id}/invoice` đã được wired; vẫn nên chốt full pipeline riêng nếu muốn tính hoàn thành chính thức | Hardening |
| 15 | `user_home.md` | Trang chủ | `/` | Cần hardening | Đã có | Partial | Route có thật; docs còn nhắc `GET /weather`, `GET /config` là planned nên cần fallback rõ | Hardening |
| 16 | `user_search.md` | Tìm kiếm | `/search` | Cần hardening | Đã có | Ready + Planned | Search core API có thật; search-history vẫn planned | Hardening |
| 17 | `user_locations_list.md` | Danh sách địa điểm | `/locations` | Cần hardening | Đã có | Ready | Route và API có thật | Hardening |
| 18 | `user_location_detail.md` | Chi tiết địa điểm | `/locations/{slug}` | Cần hardening | Đã có | Ready | Route và API có thật; có thể mở rộng favorite/rating khi login | Hardening |
| 19 | `user_tours_list.md` | Danh sách tour | `/tours` | Cần hardening | Đã có | Ready | Route và API có thật | Hardening |
| 20 | `user_blog_list.md` | Danh sách bài viết | `/blog` | Cần hardening | Đã có | Ready | Route và API có thật | Hardening |
| 21 | `user_blog_detail.md` | Chi tiết bài viết | `/blog/{slug}` | Cần hardening | Đã có | Ready | Route và API có thật; docs vẫn xếp đây là màn cần bổ sung prototype | Hardening |
| 22 | `user_destination_tour_landing.md` | Landing tour Đà Nẵng | `/du-lich-da-nang` | Cần hardening | Đã có | Partial | Route đã có; docs còn phụ thuộc `landing-pages/{slug}` và `tours/filters` planned | Hardening với fallback |
| 23 | `user_locations_by_category.md` | Địa điểm theo danh mục | `/categories/{slug}/locations` | Chưa làm | Chưa có | Ready | `GET /categories/{slug}/locations` có thật | Làm sau locations core |
| 24 | `user_locations_nearby.md` | Địa điểm lân cận | `/nearby` | Chưa làm | Chưa có | Ready | `GET /locations/nearby` có thật | Làm sau locations core |
| 25 | `user_tours_by_category.md` | Tour theo danh mục | `/tour-categories/{slug}/tours` | Chưa làm | Chưa có | Ready | `GET /tour-categories/{slug}/tours` có thật | Làm sau tours core |
| 26 | `user_blog_by_category.md` | Blog theo danh mục | `/blog?category_id={id}` | Chưa làm | Chưa có route riêng | Ready | Có thể làm bằng query state trên list route | Làm sau blog core |
| 27 | `user_profile_delete.md` | Xóa tài khoản | `/profile/delete` | Chưa làm | Chưa có | Planned | `DELETE /user/account` vẫn là planned trong docs | Chờ API |
| 28 | `user_cart.md` | Giỏ hàng | `/cart` | Chưa làm | Chưa có | Planned | Bộ `/cart/*` vẫn planned | Backlog sau |

### 1.5 Thứ tự triển khai web khuyến nghị

| Giai đoạn | Danh sách màn |
|---|---|
| Làm ngay | `user-profile-password`, `user-verify-email` |
| Hardening tiếp theo | `user-profile`, `user-home`, `user-search`, `user-locations-list`, `user-location-detail`, `user-tours-list`, `user-blog-list`, `user-blog-detail`, `user-destination-tour-landing` |
| Backlog mở rộng | `user-recommendations`, `user-my-ratings`, `user-locations-by-category`, `user-locations-nearby`, `user-tours-by-category`, `user-blog-by-category`, `user-profile-delete`, `user-cart` |

### 1.6 Nhận định ngắn

| Nhận định | Giải thích |
|---|---|
| Trục đặt tour gần khép kín | Đã có detail tour, booking, payment, departure select, bookings list, booking detail và booking lookup theo mã |
| Điểm hở delivery lớn nhất hiện tại | `user-profile-password` vì đây là account-security screen kế tiếp đã có API sẵn nhưng chưa có route/page thật trong repo |
| Ưu tiên sau màn vừa hoàn thành | `user-profile-password`, rồi mới đến `verify-email`, `login/register` hardening |

---

## 2. Dự án `danangtrip-admin`

### 2.0 Kiểm kê màn thực tế từ tài liệu

| Hạng mục | Số lượng | Ghi chú |
|---|---:|---|
| Tổng file `admin_*` trong `docs/page` | 40 | Tất cả đều là screen spec cấp dự án admin |
| Tổng màn chính của admin | 40 | Đây là mẫu số đúng để theo dõi tiến độ màn hình |
| Prototype HTML trong `screen/3_Admin_Flows` | 36 | Chưa tính utility pages trong `4_Others` |

### 2.1 Tóm tắt tiến độ

| Chỉ số | Giá trị |
|---|---:|
| Tổng màn chính của dự án | 40 |
| Hoàn thành theo tổng màn | 13 |
| Đang làm theo tổng màn | 0 |
| Chưa làm theo tổng màn | 27 |
| % hoàn thành theo tổng màn | 32.5% |
| Tổng màn đang theo dõi | 15 |
| Hoàn thành | 13 |
| Đang làm | 0 |
| Chưa làm | 2 |
| % hoàn thành trong phạm vi theo dõi | 86.7% |

### 2.2 Schedule / Timeline

| Mốc thời gian | Màn hình | Kết quả |
|---|---|---|
| 11/05/2026 | `create-new-location-danang-trip` | Hoàn thành |
| 12/05/2026 | `location-detail` | Hoàn thành |
| 13/05/2026 | `location-categories` | Hoàn thành |
| 17/05/2026 | `admin-bookings-list` | Hoàn thành |
| 17/05/2026 | `admin-payment-list` | Hoàn thành |
| 18/05/2026 | `admin-tour-schedule-form` | Hoàn thành |
| 20/05/2026 | `admin-tour-schedule-edit` | Hoàn thành |
| 21/05/2026 | `admin-bookings-detail` | Hoàn thành |
| 21/05/2026 | `admin-payments-detail` | Hoàn thành |
| 21/05/2026 | `admin-dashboard` | Hoàn thành |
| 22/05/2026 | `admin_reports_ratings` | Hoàn thành |
| 22/05/2026 | `admin_reports_bookings` | Hoàn thành |
| 22/05/2026 | `admin_reports_revenue` | Hoàn thành |
| Kế tiếp | `admin_reports_locations` | Chưa làm |
| Backlog gần | `admin_reports_users` | Chưa làm |
| Backlog gần | `admin_reports_users` | Chưa làm |

### 2.3 Chi tiết trạng thái công việc

| STT | Feature slug / Doc | Tên màn | Route | Trạng thái | Lý do |
|---:|---|---|---|---|---|
| 1 | `create-new-location-danang-trip` | Tạo địa điểm mới | Route create location admin | Hoàn thành | Đã có `deploy-report` ngày `2026-05-11` |
| 2 | `location-detail` | Chi tiết địa điểm | Route detail location admin | Hoàn thành | Đã có `deploy-report` ngày `2026-05-12` |
| 3 | `location-categories` | Danh mục địa điểm | `/admin/categories` hoặc route tương ứng | Hoàn thành | Đã có `deploy-report` ngày `2026-05-13` |
| 4 | `admin-bookings-list` | Danh sách đơn hàng | `/admin/bookings` | Hoàn thành | Đã có `deploy-report` ngày `2026-05-17` |
| 5 | `admin-payment-list` | Danh sách giao dịch | `/admin/payments` | Hoàn thành | Đã có `deploy-report` ngày `2026-05-17` |
| 6 | `admin-tour-schedule-form` | Tạo lịch khởi hành | Route create schedule admin | Hoàn thành | Đã có `deploy-report` ngày `2026-05-18` |
| 7 | `admin-tour-schedule-edit` | Chỉnh sửa lịch khởi hành | Route edit schedule admin | Hoàn thành | Đã có `deploy-report` ngày `2026-05-20` |
| 8 | `admin-bookings-detail` | Chi tiết đơn hàng | `/admin/bookings/{id}` | Hoàn thành | Đã có `deploy-report` cập nhật mới nhất ngày `2026-05-21` |
| 9 | `admin-payments-detail` | Chi tiết giao dịch | `/admin/payments/{id}` | Hoàn thành | Đã có `deploy-report` ngày `2026-05-21`; route/page thật đã tồn tại ở `src/pages/Payments/PaymentDetail/index.tsx` |
| 10 | `admin-dashboard` | Dashboard | `/dashboard` | Hoàn thành | Đã có `deploy-report` ngày `2026-05-21`; PR `feat/DATN-79-admin-dashboard` đã merge vào `dev` |
| 11 | `admin_reports_ratings.md` | Báo cáo đánh giá | `/admin/reports/ratings` | Hoàn thành | Đã hoàn tất triển khai màn hình Báo cáo Đánh giá và Moderation kèm kiểm tra Quality Gate 100% |
| 12 | `admin_reports_revenue.md` | Báo cáo doanh thu | `/admin/reports/revenue` | Hoàn thành | Đã có `deploy-report` ngày `2026-05-22` |
| 13 | `admin_reports_locations.md` | Báo cáo địa điểm | `/admin/reports/locations` | Chưa làm | Đây là candidate kế tiếp thật sự sau khi revenue đã hoàn thành |
| 14 | `admin_reports_users.md` | Báo cáo người dùng | `/admin/reports/users` | Chưa làm | Mới dừng ở mức tài liệu; chưa có `deploy-report` |
| 15 | `admin_promotions.md` | Quản lý khuyến mãi | `/admin/promotions` | Chưa làm | Flow planned; chưa phải ưu tiên delivery gần |

### 2.4 Danh sách đầy đủ các màn admin cần làm trong tương lai

| STT | Doc / Feature | Màn hình | Route | Trạng thái | Route/code hiện có | API readiness | Lý do / Ghi chú | Khuyến nghị |
|---:|---|---|---|---|---|---|---|---|
| 1 | `admin_payments_detail.md` | Chi tiết giao dịch | `/admin/payments/{id}` | Hoàn thành | Đã có route detail thật | Ready | `GET /admin/payments/{id}` và `POST /admin/payments/{id}/refund` có thật; Step 10 đã chốt `READY` | Đã xong |
| 2 | `admin_dashboard.md` | Dashboard | `/dashboard` | Hoàn thành | Đã có delivery artifact riêng | Ready | APIs dashboard có thật theo inventory admin; route repo reality là `/dashboard` | Đã xong |
| 3 | `admin_users_list.md` | Danh sách người dùng | `/admin/users` | Chưa làm | Chưa có | Ready | Core admin management screen | Ưu tiên cao |
| 4 | `admin_users_detail.md` | Chi tiết người dùng | `/admin/users/{id}` | Chưa làm | Chưa có | Ready | Hợp lý sau user list | Ưu tiên cao |
| 5 | `admin_users_create.md` | Tạo người dùng | `/admin/users/create` | Chưa làm | Chưa có | Ready | API create có thật theo inventory | Ưu tiên cao |
| 6 | `admin_users_edit.md` | Chỉnh sửa người dùng | `/admin/users/{id}/edit` | Chưa làm | Chưa có | Ready | API update có thật theo inventory | Ưu tiên cao |
| 7 | `admin_reports_bookings.md` | Báo cáo đơn hàng | `/admin/reports/bookings` | Hoàn thành | Đã có | Ready | API report bookings có thật theo docs; 100% i18n & E2E checked | Đã xong |
| 8 | `admin_reports_revenue.md` | Báo cáo doanh thu | `/admin/reports/revenue` | Hoàn thành | Đã có | Ready | API revenue/report/export đã có trong inventory | Đã xong |
| 9 | `admin_reports_ratings.md` | Báo cáo đánh giá | `/admin/reports/ratings` | Hoàn thành | Đã có delivery artifact | Ready | Hoàn thành màn hình dashboard glassmorphism | Đã xong |
| 10 | `admin_reports_locations.md` | Báo cáo địa điểm | `/admin/reports/locations` | Chưa làm | Chưa có | Ready | Nằm trong nhóm report còn thiếu delivery | Ưu tiên cao |
| 11 | `admin_reports_users.md` | Báo cáo người dùng | `/admin/reports/users` | Chưa làm | Chưa có | Ready | Nằm trong nhóm report còn thiếu delivery | Ưu tiên cao |
| 12 | `admin_contacts.md` | Liên hệ hỗ trợ | `/admin/contacts` | Chưa làm | Chưa có | Ready | List/detail/reply là khối quản trị độc lập | Làm sau reports hoặc cùng support tools |
| 13 | `admin_notifications_list.md` | Danh sách thông báo | `/admin/notifications` | Chưa làm | Chưa có | Ready | Hợp lý sau contacts/support | Làm sau |
| 14 | `admin_notifications_send.md` | Gửi thông báo | `/admin/notifications/send` | Chưa làm | Chưa có | Ready | Có thật trong admin inventory | Làm sau |
| 15 | `admin_blog_posts_list.md` | Danh sách bài viết | `/admin/blog-posts` | Chưa làm | Chưa có | Ready | Core CMS module | Làm sau |
| 16 | `admin_blog_posts_create.md` | Tạo bài viết | `/admin/blog-posts/create` | Chưa làm | Chưa có | Ready | Có API create/post upload | Làm sau |
| 17 | `admin_blog_posts_edit.md` | Chỉnh sửa bài viết | `/admin/blog-posts/{id}/edit` | Chưa làm | Chưa có | Ready | Có API update | Làm sau |
| 18 | `admin_blog_categories.md` | Danh mục blog | `/admin/blog-categories` | Chưa làm | Chưa có | Ready | Phụ thuộc module blog | Làm sau |
| 19 | `admin_ratings_list.md` | Danh sách đánh giá | `/admin/ratings` | Chưa làm | Chưa có | Ready | Moderation screen độc lập | Làm sau |
| 20 | `admin_tags_amenities.md` | Tags & tiện ích | `/admin/tags-amenities` hoặc tách route | Chưa làm | Chưa có | Ready | Có CRUD inventory level | Làm sau |
| 21 | `admin_locations_list.md` | Danh sách địa điểm | `/admin/locations` | Chưa làm | Chưa có artifact delivery riêng | Ready | Có thể đã có code nền nhưng chưa đi đủ pipeline | Hardening / delivery riêng |
| 22 | `admin_locations_create.md` | Tạo địa điểm | `/admin/locations/create` | Cần hardening | Đã có delivery gần tương ứng | Ready | Đã có feature `create-new-location-danang-trip`; nên đồng bộ theo doc chuẩn hiện tại | Hardening |
| 23 | `admin_locations_edit.md` | Chỉnh sửa địa điểm | `/admin/locations/{id}/edit` | Chưa làm | Chưa có artifact delivery riêng | Ready | API có thật; chưa thấy deploy artifact riêng | Làm sau |
| 24 | `admin_locations_detail.md` | Chi tiết địa điểm | `/admin/locations/{id}` | Cần hardening | Đã có delivery | Ready | Nên đồng bộ lại với doc chuẩn hiện tại nếu cần | Hardening |
| 25 | `admin_location_categories.md` | Danh mục địa điểm | `/admin/categories` | Cần hardening | Đã có delivery | Ready | Đã có artifact nhưng có thể cần đồng bộ tab/category-subcategory theo doc | Hardening |
| 26 | `admin_subcategories.md` | Danh mục con | `/admin/subcategories` hoặc tab | Chưa làm | Chưa có delivery riêng | Ready | Có tài liệu riêng, chưa có deploy artifact riêng | Làm sau |
| 27 | `admin_tours_list.md` | Danh sách tour | `/admin/tours` | Chưa làm | Chưa có | Ready | Core backoffice module | Làm sau |
| 28 | `admin_tours_create.md` | Tạo tour | `/admin/tours/create` | Chưa làm | Chưa có | Ready | API/create flow có thật | Làm sau |
| 29 | `admin_tours_edit.md` | Chỉnh sửa tour | `/admin/tours/{id}/edit` | Chưa làm | Chưa có | Ready | API/update flow có thật | Làm sau |
| 30 | `admin_tours_detail.md` | Chi tiết tour | `/admin/tours/{id}` | Chưa làm | Chưa có | Ready | Detail/admin analytics around tour | Làm sau |
| 31 | `admin_tour_categories.md` | Danh mục tour | `/admin/tour-categories` | Chưa làm | Chưa có | Ready | Taxonomy admin module | Làm sau |
| 32 | `admin_tour_schedules_list.md` | Lịch khởi hành | `/admin/tour-schedules` | Chưa làm | Chưa có delivery riêng | Ready | API schedule list/status has thật | Làm sau |
| 33 | `admin_tour_schedules_create.md` | Thêm lịch khởi hành | `/admin/tours/{id}/schedules/create` | Cần hardening | Đã có delivery tương ứng | Ready | Đã có `admin-tour-schedule-form`; nên đồng bộ doc chuẩn hiện tại | Hardening |
| 34 | `admin_tour_schedules_edit.md` | Chỉnh sửa lịch khởi hành | `/admin/tour-schedules/{id}/edit` | Cần hardening | Đã có delivery | Ready | Nên đồng bộ doc chuẩn hiện tại | Hardening |
| 35 | `admin_promotions.md` | Danh sách khuyến mãi | `/admin/promotions` | Chưa làm | Chưa có | Planned | Docs ghi planned; API chưa chốt | Backlog sau |
| 36 | `admin_site_settings.md` | Cấu hình website | `/admin/settings` | Chưa làm | Chưa có | Planned | Docs ghi planned | Backlog sau |
| 37 | `admin_landing_pages.md` | Landing pages | `/admin/landing-pages` | Chưa làm | Chưa có | Planned | Docs ghi planned | Backlog sau |

### 2.5 Thứ tự triển khai admin khuyến nghị

| Giai đoạn | Danh sách màn |
|---|---|
| Làm ngay | `admin_reports_locations` |
| Ưu tiên cao kế tiếp | `admin-reports-users`, `admin-users-list/detail/create/edit` |
| Giai đoạn support/CMS | `admin-contacts`, `admin-notifications-list/send`, `admin-blog-posts-list/create/edit`, `admin-blog-categories`, `admin-ratings-list`, `admin-tags-amenities` |
| Giai đoạn catalog operations | `admin-locations-list/edit/subcategories`, `admin-tours-list/create/edit/detail`, `admin-tour-categories`, `admin-tour-schedules-list` |
| Hardening đã có nền | `admin-locations-create`, `admin-locations-detail`, `admin-location-categories`, `admin-tour-schedules-create`, `admin-tour-schedules-edit` |
| Planned backlog | `admin-promotions`, `admin-site-settings`, `admin-landing-pages` |

### 2.6 Nhận định ngắn

| Nhận định | Giải thích |
|---|---|
| Trục vận hành booking admin đã khá đầy | Đã có booking list, booking detail, payment list, payment detail và dashboard |
| Điểm hở lớn nhất hiện tại | `admin_reports_locations` để khép tiếp cụm report analytics sau ratings, bookings, và revenue |
| Backlog sau màn kế tiếp | `admin_reports_users`, rồi mới đến users management và các flow planned |

---


---

## 3. Kết luận chung

| Dự án | Tổng màn chính | Hoàn thành | Đang làm | Chưa làm | % hoàn thành theo tổng màn | Màn kế tiếp đã chốt prompt |
|---|---:|---:|---:|---:|---:|---|
| `danangtrip-web` | 35 | 20 | 0 | 15 | 57.1% | `TBD - API/planning review needed` |
| `danangtrip-admin` | 40 | 21 | 0 | 19 | 52.5% | `admin_blog_posts_list` |

| Kết luận | Diễn giải |
|---|---|
| Hai dự án đang đi đúng trục hậu booking | Web đã khép lookup theo mã booking, favorites, notifications, ratings, recommendations, locations category/nearby, tours category và blog category; admin đã khép dashboard, reports, users cluster, contacts support, notifications list và notifications send |
| Có thể chọn màn tiếp theo | Web cần vòng API/planning review trước khi khóa prompt mới vì `user-profile-delete`/`user-cart` chưa thấy API/route sẵn sàng trong codegraph. Admin nên chuyển sang `admin_blog_posts_list` vì backend admin blog-posts CRUD đã có route và admin UI chưa có module tương ứng |
| Báo cáo này nên cập nhật sau mỗi lần có `deploy-report` mới | Khi một màn đi hết pipeline, chỉ cần đổi trạng thái và tính lại % |
| Nguồn backlog tương lai đã được gộp vào báo cáo này | Không cần tách riêng roadmap cho `web` hay `admin` nữa |
