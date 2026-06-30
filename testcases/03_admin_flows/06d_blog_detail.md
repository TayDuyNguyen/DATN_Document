# Admin — Chi tiết Bài viết (Blog Post Detail)

**Route:** `/admin/blog-posts/:id`  
**Source:** `danangtrip-admin/src/pages/Blog/BlogPostDetail/index.tsx` + `BlogPostDetailHeader` · `BlogPostDetailContent` · `BlogPostDetailSidebar`  
**Automation:** `tests/admin/blog-detail.spec.ts` · `blog-detail-auth.spec.ts` · `tests/api/admin-blog-detail.api.spec.ts` · POM: `BlogDetailPage.ts`

**Chạy:** `npm run test:admin:blog-detail` · `--workers=1`

> **Lưu ý thực tế:** Chỉ **Admin** (`PrivateRoute`) — không có Staff trên route này. Preview public: `{VITE_PUBLIC_WEB_URL}/blog/{slug}` (mặc định `http://localhost:3000`). Content render qua `dangerouslySetInnerHTML` (HTML từ API). Đổi status qua `PATCH /admin/blog-posts/:id/status` (header dropdown). Sidebar có prop `onStatusChange` nhưng **không dùng** — status chỉ đổi từ header.

---

## 1. Phạm vi

| Hạng mục | Chi tiết |
|----------|----------|
| API detail | `GET /admin/blog-posts/:id` |
| API status | `PATCH /admin/blog-posts/:id/status` |
| API delete | `DELETE /admin/blog-posts/:id` |
| Preview | Mở tab mới web user `/blog/{slug}` |
| Navigation | → list, → edit, → create (duplicate state) |
| Quyền | Admin route guard; nút xóa header/sidebar chỉ khi `isAdmin` |

---

## 2. Tổng quan trạng thái automation

| Nhóm | Tổng TC | ✅ Auto | ⏳ Backlog |
|------|---------|---------|------------|
| Auth | 2 | 2 | 0 |
| Load theo status | 4 | 4 | 0 |
| Loading / Error | 3 | 3 | 0 |
| Header & navigation | 5 | 3 | 2 (009, 051) |
| Status dropdown | 7 | 6 | 1 (016) |
| Preview public | 3 | 3 | 0 |
| Edit / Duplicate / Delete | 9 | 4 | 5 (025, 027–028, 031, 052) |
| Content preview | 10 | 6 | 4 (034, 037, 040, 046b) |
| Sidebar metadata | 6 | 5 | 1 (048 empty categories) |
| UX / Responsive | 3 | 2 | 1 (051 flow) |
| **UI subtotal** | **52** | **39** | **13** |
| API smoke | 3 | 3 | 0 |
| **Tổng automation** | **55** | **42** | **13** |

**Chạy:** `npm run test:admin:blog-detail` · `--workers=1`

---

## 2b. UI Inventory (PHASE 0.6)

| # | Vùng UI | Nhãn (i18n) | Loại | Hành vi | TC |
|---|---------|-------------|------|---------|-----|
| 1 | Header | Quay lại | button | → `/admin/blog-posts` | BLOGDET_010 |
| 2 | Header | Breadcrumb posts → view | breadcrumb | nav | BLOGDET_003 |
| 3 | Header | Chi tiết Bài viết | h1 | title trang | BLOGDET_003 |
| 4 | Header | Subtitle = `post.title` | text | truncate | BLOGDET_009 |
| 5 | Header | Status dropdown (DRAFT/PUBLISHED/ARCHIVED) | button + menu | PATCH status | BLOGDET_011–017 |
| 6 | Header | Xem bài viết | button | popup public (`md+`) | BLOGDET_018–020 |
| 7 | Header | Sửa | button | → edit | BLOGDET_021 |
| 8 | Header | Xóa | button | mở delete modal (`md+`, admin) | BLOGDET_027 |
| 9 | Content | Ảnh bìa hero / fallback | image / placeholder | onError fallback | BLOGDET_032–033, 046 |
| 10 | Content | Category tags trên ảnh | badges | overlay | BLOGDET_040 |
| 11 | Content | Tiêu đề bài viết | h1 | `post.title` | BLOGDET_003 |
| 12 | Content | Meta: tác giả, ngày tạo, lượt xem | text row | format date/views | BLOGDET_034 |
| 13 | Content | Slug + nút copy | code + button | clipboard + toast | BLOGDET_035 |
| 14 | Content | Excerpt box | blockquote style | ẩn nếu rỗng | BLOGDET_036–037 |
| 15 | Content | Nội dung HTML (prose) | `dangerouslySetInnerHTML` | render HTML | BLOGDET_038–039 |
| 16 | Sidebar | Thao tác nhanh | card | actions | BLOGDET_003 |
| 17 | Sidebar | Xem / Sửa / Nhân bản / Xóa | buttons | nav / modal | BLOGDET_020–028 |
| 18 | Sidebar | Trạng thái xuất bản | badge + ngày publish | read-only | BLOGDET_041–042 |
| 19 | Sidebar | Tác giả (avatar / initial) | card | ẩn nếu không author | BLOGDET_043 |
| 20 | Sidebar | THÔNG TIN: created, updated, views, categories | metadata | format | BLOGDET_044–045 |
| 21 | Modal | Xóa bài viết | DeleteConfirmDialog | DELETE → list | BLOGDET_029–031 |
| 22 | Modal | Nhân bản bài viết | DuplicateConfirmDialog | → create + state | BLOGDET_024–026 |
| 23 | Error | Không tìm thấy bài viết | panel | GET 404 | BLOGDET_007–008 |
| 24 | Loading | BlogPostDetailSkeleton | skeleton | delay API | BLOGDET_006 |

---

## 2c. Data Display Integrity (PHASE 0.7)

| # | Field API | Vùng UI | TC |
|---|-----------|---------|-----|
| 1 | `title` | Header subtitle + content h1 | BLOGDET_003 |
| 2 | `slug` | Slug block + preview URL | BLOGDET_035, 018 |
| 3 | `excerpt` | Excerpt box | BLOGDET_036 |
| 4 | `content` | Prose HTML body | BLOGDET_038 |
| 5 | `featured_image` | Hero banner | BLOGDET_032 |
| 6 | `status` | Header badge + sidebar publish card | BLOGDET_011, 041 |
| 7 | `published_at` | Sidebar khi published | BLOGDET_042 |
| 8 | `author.full_name`, `author.avatar` | Content meta + author card | BLOGDET_034, 043 |
| 9 | `view_count` | Content meta + sidebar | BLOGDET_034, 044 |
| 10 | `created_at`, `updated_at` | Sidebar metadata | BLOGDET_044 |
| 11 | `categories[].name` | Hero overlay + sidebar badges | BLOGDET_040, 044 |
| 12 | PATCH `status` | Refetch → badge đổi | BLOGDET_013–015, 047 |

---

## 3. Kịch bản & test cases chi tiết

### A. Auth & quyền (P0)

| ID | Mô tả | Bước | Kết quả mong đợi |
|----|--------|------|------------------|
| TC_AD_BLOGDET_001 | Guest redirect login | Mở `/admin/blog-posts/201` chưa đăng nhập | Redirect `/login`, không lộ nội dung |
| TC_AD_BLOGDET_002 | Non-admin redirect login | User role `user` + session seed | Redirect `/login` |

### B. Load trang theo trạng thái (P1)

| ID | Mô tả | Dữ liệu | Kết quả mong đợi |
|----|--------|---------|------------------|
| TC_AD_BLOGDET_003 | Load bài **published** đầy đủ UI | id=201 | Header, content hero, sidebar 4 cards, modals không mở |
| TC_AD_BLOGDET_004 | Load bài **draft** | id=203 | Badge DRAFT; preview disabled |
| TC_AD_BLOGDET_005 | Load bài **archived** | id=204 | Badge ARCHIVED; preview disabled |
| TC_AD_BLOGDET_045 | Load bài **scheduled** (published + `published_at` tương lai) | id=216 | Status published; ngày publish hiển thị sidebar |

### C. Loading & Error (P1)

| ID | Mô tả | Kết quả mong đợi |
|----|--------|------------------|
| TC_AD_BLOGDET_006 | API detail delay | `BlogPostDetailSkeleton` (content + sidebar skeleton) |
| TC_AD_BLOGDET_007 | ID không tồn tại (404) | Panel "Không tìm thấy bài viết" |
| TC_AD_BLOGDET_008 | Nút quay về từ error panel | Navigate `/admin/blog-posts` |

### D. Header & điều hướng (P1)

| ID | Mô tả | Kết quả mong đợi |
|----|--------|------------------|
| TC_AD_BLOGDET_009 | Title dài truncate header subtitle | Không vỡ layout sticky header |
| TC_AD_BLOGDET_010 | Nút back (ArrowLeft) | → blog list |
| TC_AD_BLOGDET_021 | Nút **Sửa** header | → `/admin/blog-posts/edit/:id` |
| TC_AD_BLOGDET_022 | Nút **Sửa** sidebar | → edit (cùng route) |
| TC_AD_BLOGDET_050 | Mobile (`sm`): nút Sửa chỉ icon | Text "Sửa" ẩn, button vẫn click được |

### E. Status dropdown (P1)

| ID | Mô tả | Kết quả mong đợi |
|----|--------|------------------|
| TC_AD_BLOGDET_011 | Mở dropdown | Hiện draft / published / archived; mục hiện tại có ✓ |
| TC_AD_BLOGDET_012 | Đóng dropdown click outside | Menu đóng, không đổi status |
| TC_AD_BLOGDET_013 | Đổi **published → draft** | PATCH `{status:'draft'}`; toast success; UI refetch badge |
| TC_AD_BLOGDET_014 | Đổi **draft → published** | PATCH published; preview enabled sau refetch |
| TC_AD_BLOGDET_015 | Đổi **published → archived** | PATCH archived; preview disabled |
| TC_AD_BLOGDET_016 | Đổi sang status **đang active** (re-select) | PATCH vẫn gọi hoặc không crash; UI ổn định |
| TC_AD_BLOGDET_017 | PATCH status API lỗi | Toast `network_error`; badge không đổi sai |
| TC_AD_BLOGDET_047 | Sau đổi status thành công | Header badge + sidebar publish card đồng bộ |

### F. Preview bài public (P1)

| ID | Mô tả | Kết quả mong đợi |
|----|--------|------------------|
| TC_AD_BLOGDET_018 | Published: click **Xem bài viết** header | Tab mới `/blog/{slug}` |
| TC_AD_BLOGDET_019 | Draft: nút preview disabled + title helper | `preview_disabled_helper` |
| TC_AD_BLOGDET_020 | Published: preview từ **sidebar** | Cùng URL public |

### G. Nhân bản (P1)

| ID | Mô tả | Kết quả mong đợi |
|----|--------|------------------|
| TC_AD_BLOGDET_024 | Click Nhân bản | Mở `DuplicateConfirmDialog` |
| TC_AD_BLOGDET_025 | Confirm nhân bản | → `/admin/blog-posts/create` + `state.duplicateData`; toast duplicate |
| TC_AD_BLOGDET_026 | Hủy modal nhân bản | Đóng modal; ở lại detail |

### H. Xóa bài viết (P1)

| ID | Mô tả | Kết quả mong đợi |
|----|--------|------------------|
| TC_AD_BLOGDET_027 | Admin: Delete header mở modal | `confirm_delete_title` + tên bài |
| TC_AD_BLOGDET_028 | Admin: Delete sidebar mở modal | Cùng modal |
| TC_AD_BLOGDET_029 | Confirm xóa | DELETE API; toast delete; → list |
| TC_AD_BLOGDET_030 | DELETE API lỗi | Toast error; không redirect list |
| TC_AD_BLOGDET_031 | Hủy modal xóa | Đóng modal; vẫn ở detail |

> **Ghi chú:** Doc cũ TC "staff xem detail" — route chỉ Admin nên kiểm tra qua **TC_002** (redirect login), không phải nút disabled trên trang.

### I. Content preview — cột trái (P1–P2)

| ID | Mô tả | Kết quả mong đợi |
|----|--------|------------------|
| TC_AD_BLOGDET_032 | Có `featured_image` | Hero hiển thị ảnh |
| TC_AD_BLOGDET_033 | Không ảnh bìa | Placeholder gradient + "Không có ảnh đại diện" |
| TC_AD_BLOGDET_034 | Meta row: author, created, views | Khớp API; format `dd/mm/yyyy hh:mm` |
| TC_AD_BLOGDET_035 | Copy slug | Clipboard slug; toast copy success; icon ✓ tạm thời |
| TC_AD_BLOGDET_036 | Có excerpt | Box excerpt hiển thị italic |
| TC_AD_BLOGDET_037 | Excerpt rỗng | Không render excerpt block |
| TC_AD_BLOGDET_038 | Content HTML (`<h2>`, `<p>`, …) | Render prose, không raw escape |
| TC_AD_BLOGDET_039 | Content rỗng | Message "Bài viết này không có nội dung" |
| TC_AD_BLOGDET_040 | Nhiều categories | Tags trên hero + sidebar metadata |
| TC_AD_BLOGDET_046 | Ảnh broken URL | Fallback unsplash placeholder (onError) |

### J. Sidebar metadata (P2)

| ID | Mô tả | Kết quả mong đợi |
|----|--------|------------------|
| TC_AD_BLOGDET_041 | Publish card hiển thị status badge | Khớp `post.status` |
| TC_AD_BLOGDET_042 | Published + `published_at` | Block ngày xuất bản |
| TC_AD_BLOGDET_043 | Author có/không avatar | Avatar img hoặc initial chữ cái |
| TC_AD_BLOGDET_044 | Metadata: created, updated, views | Format đúng; views dùng `info_views_val` |
| TC_AD_BLOGDET_048 | Không categories | Không block category sidebar; hero không tags |

### K. Responsive & regression (P2)

| ID | Mô tả | Kết quả mong đợi |
|----|--------|------------------|
| TC_AD_BLOGDET_049 | Viewport 390px | Content + sidebar xếp dọc; header không tràn |
| TC_AD_BLOGDET_051 | Flow: đổi published → preview → edit → back | Routes đúng; không mất session |
| TC_AD_BLOGDET_052 | `isMutating` disable actions | Khi PATCH/DELETE pending: dropdown/edit disabled |

### L. API smoke (P1)

| ID | Mô tả | Kết quả mong đợi |
|----|--------|------------------|
| API_BLOGDET_001 | `GET /admin/blog-posts/:id` không auth | 401 |
| API_BLOGDET_002 | `GET /admin/blog-posts/:id` có auth | 200 |
| API_BLOGDET_003 | `PATCH .../status` không auth | 401 |

---

## 3a. Test cases (automation)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_BLOGDET_001 | Guest redirect login | ✅ |
| TC_AD_BLOGDET_002 | Non-admin redirect login | ✅ |
| TC_AD_BLOGDET_003 | Load published đầy đủ UI | ✅ |
| TC_AD_BLOGDET_004 | Load draft + preview disabled | ✅ |
| TC_AD_BLOGDET_045 | Scheduled badge + preview disabled | ✅ |
| TC_AD_BLOGDET_006 | Skeleton khi API delay | ✅ |
| TC_AD_BLOGDET_007 | 404 not found panel | ✅ |
| TC_AD_BLOGDET_008 | Error panel → list | ✅ |
| TC_AD_BLOGDET_010 | Back → list | ✅ |
| TC_AD_BLOGDET_011 | Mở status dropdown | ✅ |
| TC_AD_BLOGDET_012 | Đóng dropdown click outside | ✅ |
| TC_AD_BLOGDET_013 | published → draft + toast | ✅ |
| TC_AD_BLOGDET_014 | draft → published + preview enabled | ✅ |
| TC_AD_BLOGDET_015 | published → archived | ✅ |
| TC_AD_BLOGDET_017 | PATCH status lỗi → toast | ✅ |
| TC_AD_BLOGDET_018 | Header preview tab mới (desktop) | ✅ |
| TC_AD_BLOGDET_019 | Draft preview disabled | ✅ |
| TC_AD_BLOGDET_020 | Sidebar preview tab mới | ✅ |
| TC_AD_BLOGDET_021 | Header Sửa → edit | ✅ |
| TC_AD_BLOGDET_022 | Sidebar Sửa → edit | ✅ |
| TC_AD_BLOGDET_024 | Nhân bản → confirm → create | ✅ |
| TC_AD_BLOGDET_026 | Hủy modal nhân bản | ✅ |
| TC_AD_BLOGDET_029 | Xóa confirm → list | ✅ |
| TC_AD_BLOGDET_030 | DELETE lỗi → toast | ✅ |
| TC_AD_BLOGDET_032 | Hero ảnh bìa | ✅ |
| TC_AD_BLOGDET_033 | Fallback không ảnh | ✅ |
| TC_AD_BLOGDET_035 | Copy slug + toast | ✅ |
| TC_AD_BLOGDET_036 | Excerpt block | ✅ |
| TC_AD_BLOGDET_038 | HTML content prose | ✅ |
| TC_AD_BLOGDET_039 | Content rỗng | ✅ |
| TC_AD_BLOGDET_041 | Author card | ✅ |
| TC_AD_BLOGDET_042 | Info created/updated/views | ✅ |
| TC_AD_BLOGDET_043 | Ngày publish sidebar | ✅ |
| TC_AD_BLOGDET_044 | Meta author/date/views | ✅ |
| TC_AD_BLOGDET_046 | Category tags hero | ✅ |
| TC_AD_BLOGDET_048 | Category tags sidebar | ✅ |
| TC_AD_BLOGDET_049 | Mobile sidebar quick actions | ✅ |
| TC_AD_BLOGDET_050 | Mobile header edit icon | ✅ |
| API_BLOGDET_001 | GET detail 401 | ✅ |
| API_BLOGDET_002 | GET detail 200 (skip nếu API down) | ✅ |
| API_BLOGDET_003 | PATCH status 401 | ✅ |

---

## 4. Test data đề xuất

| Key | id | Mục đích |
|-----|-----|----------|
| `primaryBlogRow` | 201 | Published, ảnh, categories, HTML content |
| `draftEditBlogId` | 203 | Draft, preview disabled |
| `archivedEditBlogId` | 204 | Archived |
| `scheduledEditBlogId` | 216 | Published + `published_at` future |
| `deleteEditBlogId` | 215 | Xóa automation (không dùng cho load chính) |
| `notFoundBlogId` | 99999 | 404 panel |

**Mock flags (`blogs.mock.ts`):** `setBlogDetailFailForId`, `setBlogDetailDelay`, `setBlogStatusFailForId`, `setBlogDeleteFailForId`.

---

## 5. Ghi chú doc cũ → thực tế

| Doc cũ | Thực tế |
|--------|---------|
| ID `ADMIN_BLOG_DETAIL_*` | Đề xuất `TC_AD_BLOGDET_*` (thống nhất module) |
| Staff xem detail + delete disabled | **Chỉ Admin** vào route; staff → login |
| Đổi status ở sidebar | **Chỉ header dropdown** (sidebar chỉ hiển thị badge) |
| 25 TC | **55 TC** sau inventory đầy đủ |
| WYSIWYG preview | HTML render (`dangerouslySetInnerHTML`) |

---

## 6. Đề xuất cải thiện (PHASE 0.8) — đã implement (2026-06-23)

| ID | Loại | Trạng thái | Tóm tắt |
|----|------|------------|---------|
| IMP_BLOGDET_001 | UX | ✅ | Full-bleed `w-full px-4 sm:px-6 lg:px-10` |
| IMP_BLOGDET_002 | A11y | ✅ | `aria-label` nút back |
| IMP_BLOGDET_003 | i18n | ✅ | Error panel dùng `form.back_to_list` |
| IMP_BLOGDET_004 | i18n | ✅ | Keys: `copy_success`, `empty.no_content`, `role.author`, `actions.copy`, `status.scheduled` |
| IMP_BLOGDET_005 | Code | ✅ | Duplicate dùng `ROUTES.BLOG_POSTS_CREATE` |
| IMP_BLOGDET_006 | UX | ✅ | `useMainScrollCollapse` + header collapse |
| IMP_BLOGDET_007 | UX | ✅ | Mobile sticky footer Preview/Sửa/Xóa; sidebar quick actions `lg+` |
| IMP_BLOGDET_008 | Code | ✅ | Xóa dead prop `onStatusChange` khỏi Sidebar |
| IMP_BLOGDET_009 | UX | ✅ | Skip PATCH khi chọn lại cùng status |
| IMP_BLOGDET_010 | Chức năng | ✅ | Badge **LÊN LỊCH** + preview disabled khi `published_at` tương lai (`blogPostStatus.ts`) |

---

## 7. Checklist regression

- [ ] Status dropdown PATCH + refetch đồng bộ header/sidebar
- [ ] Preview chỉ khi `status === 'published'`
- [ ] Delete chỉ admin (trên trang đã login admin)
- [ ] Duplicate truyền `duplicateData` sang create
- [ ] Copy slug + toast
- [ ] Hero fallback khi không ảnh / ảnh lỗi
- [ ] 404 panel + quay list
