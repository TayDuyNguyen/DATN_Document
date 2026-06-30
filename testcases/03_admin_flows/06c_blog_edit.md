# Admin — Chỉnh sửa Bài viết (Blog Post Edit)

**Route:** `/admin/blog-posts/edit/:id`  
**Source:** `danangtrip-admin/src/pages/Blog/BlogPostEdit/index.tsx` + `BlogPostForm.tsx`  
**Automation:** `blog-edit.spec.ts` + `blog-edit-auth.spec.ts` + `admin-blog-edit.api.spec.ts` · POM: `BlogEditPage.ts`

**Chạy:** `npm run test:admin:blog-edit` · `--workers=1`

> **Lưu ý:** Chỉ **Admin** (`PrivateRoute`). Form `react-hook-form` + `createBlogPostSchema`. Editor Markdown. Sidebar: Draft / Publish / Scheduled / **Archived** + datetime + **THÔNG TIN** (created, updated, author, views). Quick actions: Xem bài viết, Nhân bản, Xóa. Sau cập nhật thành công → **redirect** `/admin/blog-posts`. `UnsavedChangesGuard` khi form dirty.

---

## 1. Phạm vi

| Hạng mục | Chi tiết |
|----------|----------|
| API detail | `GET /admin/blog-posts/:id` |
| API update | `PUT /admin/blog-posts/:id` |
| API delete | `DELETE /admin/blog-posts/:id` (quick action) |
| API meta | `GET /admin/blog-categories`, `POST /admin/blog-categories` (inline) |
| Upload | `POST /upload/image` |
| Validation | `blog.schema.ts` — title, content, category_ids (min 1), excerpt max 500 |
| Quyền | Admin route guard |

---

## 2. Tổng quan trạng thái

| Nhóm | Tổng TC | ✅ Auto | ⏳ Backlog |
|------|---------|---------|------------|
| Page load & preload | 3 | 3 | 0 |
| Status preload | 3 | 3 | 0 |
| Validation | 3 | 3 | 0 |
| Slug warning | 1 | 1 | 0 |
| Update flows | 4 | 4 | 0 |
| Category inline | 1 | 1 | 0 |
| Preview | 2 | 2 | 0 |
| Quick actions | 2 | 2 | 0 |
| Navigation | 2 | 2 | 0 |
| Error / not found | 2 | 2 | 0 |
| Categories load | 1 | 1 | 0 |
| Auth | 2 | 2 | 0 |
| **UI subtotal** | **27** | **27** | **0** |
| API smoke | 4 | 4 | **0** |
| **Tổng automation** | **31** | **31** | **0** |

---

## 2b. UI Inventory (PHASE 0.6)

| # | Vùng UI | Nhãn (i18n) | Loại | Hành vi | TC | Trạng thái |
|---|---------|-------------|------|---------|-----|------------|
| 1 | Header | Chỉnh sửa Bài viết | h1 | Title | BLOGEDIT_002 | ✅ |
| 2 | Header | Subtitle = title bài viết | text | preload | BLOGEDIT_001 | ✅ |
| 3 | Header | Quay lại | button | → list | BLOGEDIT_021 | ✅ |
| 4 | Header | Hủy / Xem bài viết / Lưu thay đổi | buttons | nav / preview / submit | BLOGEDIT_016–017, 020 | ✅ |
| 5 | Content | Tiêu đề | input | preload + validate | BLOGEDIT_001, 007–008 | ✅ |
| 6 | Content | Slug preview + warning | text | slugify + cảnh báo đổi slug | BLOGEDIT_010 | ✅ |
| 7 | Content | Mô tả ngắn | textarea | max 500 | BLOGEDIT_009 | ✅ |
| 8 | Content | Nội dung Markdown | editor | preload + update | BLOGEDIT_001, 011 | ✅ |
| 9 | Sidebar | Draft / Published / Scheduled / Archived | radio | status PUT | BLOGEDIT_004–006, 013–014 | ✅ |
| 10 | Sidebar | Ngày + giờ lên lịch | date/time | scheduled | BLOGEDIT_006, 014 | ✅ |
| 11 | Sidebar | THÔNG TIN (created, updated, author, views) | static | read-only | BLOGEDIT_003 | ✅ |
| 12 | Sidebar | Lưu thay đổi / Hủy | buttons | PUT / nav | BLOGEDIT_011, 020 | ✅ |
| 13 | Sidebar | Danh mục checkbox | input | preload + min 1 | BLOGEDIT_001, 024 | ✅ |
| 14 | Sidebar | Thêm danh mục mới | inline form | POST category | BLOGEDIT_015 | ✅ |
| 15 | Sidebar | Ảnh đại diện | upload | preload + replace | BLOGEDIT_001, 012 | ✅ |
| 16 | Quick actions | Xem bài viết | button | popup public URL (published only) | BLOGEDIT_016–017 | ✅ |
| 17 | Quick actions | Nhân bản bài viết | button + modal | → create + state | BLOGEDIT_018 | ✅ |
| 18 | Quick actions | Xóa bài viết | button + modal | DELETE → list | BLOGEDIT_019 | ✅ |
| 19 | Mobile footer | Hủy / Lưu thay đổi | buttons | md:hidden | (covered by submit POM) | ✅ |
| 20 | Error | Không tìm thấy bài viết | panel | GET 404 | BLOGEDIT_023 | ✅ |

---

## 2c. Data Display Integrity (PHASE 0.7)

| # | Vùng UI | Field API | Field form | TC | Trạng thái |
|---|---------|-----------|------------|-----|------------|
| 1 | Title | `title` | title input | BLOGEDIT_001 | ✅ |
| 2 | Excerpt | `excerpt` | textarea | BLOGEDIT_001 | ✅ |
| 3 | Content | `content` | markdown editor | BLOGEDIT_001 | ✅ |
| 4 | Categories | `categories[].name` | checkbox checked | BLOGEDIT_001 | ✅ |
| 5 | Featured image | `featured_image` | img preview | BLOGEDIT_001 | ✅ |
| 6 | Draft status | `status: draft` | radio draft | BLOGEDIT_004 | ✅ |
| 7 | Archived status | `status: archived` | radio archived | BLOGEDIT_005 | ✅ |
| 8 | Scheduled | `published_at` future | radio scheduled + date | BLOGEDIT_006 | ✅ |
| 9 | Author | `author.full_name` | info section | BLOGEDIT_003 | ✅ |
| 10 | Views | `view_count` | info section | BLOGEDIT_003 | ✅ |
| 11 | PUT update | changed fields | mock dataset | BLOGEDIT_011–014 | ✅ |

---

## 3. Test cases (automation)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_BLOGEDIT_001 | Preload title, excerpt, content, category, ảnh bìa | ✅ |
| TC_AD_BLOGEDIT_002 | Heading, publish options (4), info, quick actions | ✅ |
| TC_AD_BLOGEDIT_003 | Info section: author + view count | ✅ |
| TC_AD_BLOGEDIT_004 | Draft post → radio draft checked | ✅ |
| TC_AD_BLOGEDIT_005 | Archived post → radio archived checked | ✅ |
| TC_AD_BLOGEDIT_006 | Scheduled post → date prefilled 2099-12-31 | ✅ |
| TC_AD_BLOGEDIT_007 | Submit title trống → lỗi | ✅ |
| TC_AD_BLOGEDIT_008 | Title > 255 ký tự | ✅ |
| TC_AD_BLOGEDIT_009 | Excerpt > 500 ký tự | ✅ |
| TC_AD_BLOGEDIT_010 | Đổi title → hiện slug warning | ✅ |
| TC_AD_BLOGEDIT_011 | Update title + content → toast + redirect detail | ✅ |
| TC_AD_BLOGEDIT_012 | Upload ảnh mới trong PUT payload | ✅ |
| TC_AD_BLOGEDIT_013 | Đổi status archived trong PUT | ✅ |
| TC_AD_BLOGEDIT_014 | Lên lịch với ngày tương lai trong PUT | ✅ |
| TC_AD_BLOGEDIT_014b | Lên lịch không chọn ngày → lỗi validation | ✅ |
| TC_AD_BLOGEDIT_015 | Thêm danh mục inline + auto chọn | ✅ |
| TC_AD_BLOGEDIT_016 | Draft → preview disabled | ✅ |
| TC_AD_BLOGEDIT_017 | Published → preview mở tab public | ✅ |
| TC_AD_BLOGEDIT_018 | Nhân bản → modal → redirect create | ✅ |
| TC_AD_BLOGEDIT_019 | Xóa → modal → redirect list | ✅ |
| TC_AD_BLOGEDIT_020 | Hủy header → list | ✅ |
| TC_AD_BLOGEDIT_021 | Nút back → list | ✅ |
| TC_AD_BLOGEDIT_022 | API update lỗi → toast, ở lại trang | ✅ |
| TC_AD_BLOGEDIT_023 | Bài viết không tồn tại → error panel | ✅ |
| TC_AD_BLOGEDIT_024 | Categories load từ API | ✅ |
| TC_AD_BLOGEDIT_025 | Guest redirect login | ✅ |
| TC_AD_BLOGEDIT_026 | Non-admin redirect login | ✅ |
| API_BLOGEDIT_001 | PUT update 401 unauthenticated | ✅ |
| API_BLOGEDIT_002 | PUT update valid admin | ✅ |
| API_BLOGEDIT_003 | PUT invalid payload 422+ | ✅ |
| API_BLOGEDIT_004 | GET detail 401 unauthenticated | ✅ |

---

## 4. Test data

* Default edit: **id=201** — `Ẩm thực Đà Nẵng: 10 quán must-try` (published, category Ẩm thực)
* Draft edit: **id=203**
* Archived edit: **id=204**
* Scheduled edit: **id=216** — `2099-12-31T08:00:00Z`
* Delete edit: **id=215** — `Bài viết test xóa automation`
* Not found: **id=99999**
* Updated title: **Ẩm thực Đà Nẵng — bản cập nhật automation**

**Mock flags:** `setBlogDetailFailForId`, `setBlogUpdateFail`

---

## 5. Ghi chú doc cũ → thực tế

| Doc cũ | Thực tế |
|--------|---------|
| Quyền Admin/Staff | **Chỉ Admin** |
| WYSIWYG | **Markdown editor** |
| Chỉ 2 TC (load + update) | **30 TC** automation đầy đủ |
| Nút "Cập nhật" | **"Lưu thay đổi"** (`actions.save_changes`) |
| Sau update ở lại trang | **Redirect detail** `/admin/blog-posts/:id` |

---

## 6. Đề xuất cải thiện (PHASE 0.8)

| ID | Loại | Ưu tiên | Tóm tắt | Trạng thái |
|----|------|---------|---------|------------|
| IMP_BLOGEDIT_001 | Doc | P2 | Doc cũ 2 TC, ghi Staff | **fixed** (doc) |
| IMP_BLOGEDIT_002 | UX | P2 | Header `max-w-[1600px]` chưa full-bleed | **fixed** |
| IMP_BLOGEDIT_003 | A11y | P3 | Nút back thiếu `aria-label` | **fixed** |
| IMP_BLOGEDIT_004 | i18n | P3 | Loading categories hardcode EN | **fixed** |
| IMP_BLOGEDIT_005 | Code | P1 | Header save dùng `requestSubmit()` | **fixed** (`form=`) |
| IMP_BLOGEDIT_006 | Validation | P1 | Scheduled không có ngày vẫn submit | **fixed** |
| IMP_BLOGEDIT_007 | UX | P2 | Chưa có `useMainScrollCollapse` | **fixed** |
| IMP_BLOGEDIT_008 | i18n | P3 | `error_post_not_found` thiếu key | **fixed** |
| IMP_BLOGEDIT_009 | UX | P1 | Preview không sync form state | **fixed** |
| IMP_BLOGEDIT_010 | Code | P1 | Sidebar submit onClick sai status | **fixed** |
| IMP_BLOGEDIT_011 | UX | P2 | Sidebar submit trùng desktop | **fixed** (`md:hidden`) |
| IMP_BLOGEDIT_012 | UX | P2 | Redirect list sau update | **fixed** → detail |
| IMP_BLOGEDIT_013 | UX | P2 | Panel 404 nút "Hủy" | **fixed** |
| IMP_BLOGEDIT_014 | UX | P2 | Mobile thiếu quick actions | **fixed** |
| IMP_BLOGEDIT_015 | A11y | P3 | Checkbox thiếu aria-label | **fixed** |
| IMP_BLOGEDIT_016 | Code | P3 | Hidden submit buttons dead code | **fixed** |
| IMP_BLOGEDIT_017 | Code | P3 | Duplicate navigate hardcode path | **fixed** |
| IMP_BLOGEDIT_018 | Code | P3 | Cast status thiếu archived | **fixed** |
