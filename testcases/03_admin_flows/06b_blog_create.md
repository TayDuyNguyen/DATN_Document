# Admin — Thêm mới Bài viết (Blog Post Create)

**Route:** `/admin/blog-posts/create`  
**Source:** `danangtrip-admin/src/pages/Blog/BlogPostCreate/index.tsx` + `BlogPostForm.tsx`  
**Automation:** `blog-create.spec.ts` + `blog-create-auth.spec.ts` + `admin-blog-create.api.spec.ts` · POM: `BlogCreatePage.ts`

**Chạy:** `npm run test:admin:blog-create` · `--workers=1`

> **Lưu ý:** Chỉ **Admin** (`PrivateRoute`). Form `react-hook-form` + `createBlogPostSchema`. Editor Markdown (`BlogMarkdownEditor`). Sidebar: Draft / Publish / Scheduled + datetime. Sau tạo thành công → **redirect** `/admin/blog-posts/edit/:id`. Upload ảnh đại diện qua `POST /upload/image`.

---

## 1. Phạm vi

| Hạng mục | Chi tiết |
|----------|----------|
| API create | `POST /admin/blog-posts` |
| API meta | `GET /admin/blog-categories`, `POST /admin/blog-categories` (inline) |
| API slug | `GET /admin/blog-posts/check-slug` (duplicate flow) |
| Upload | `POST /upload/image` |
| Validation | `blog.schema.ts` — title, content, category_ids (min 1), excerpt max 500 |
| Quyền | Admin route guard |

---

## 2. Tổng quan trạng thái

| Nhóm | Tổng TC | ✅ Auto | ⏳ Backlog |
|------|---------|---------|------------|
| Page load | 2 | 2 | 0 |
| Validation | 3 | 3 | 0 |
| Slug & content | 2 | 2 | 0 |
| Media | 1 | 1 | 0 |
| Publish flows | 3 | 3 | 0 |
| Category inline | 1 | 1 | 0 |
| Navigation | 3 | 3 | 0 |
| API error | 1 | 1 | 0 |
| UX | 2 | 2 | 0 |
| Auth | 2 | 2 | 0 |
| **UI subtotal** | **20** | **20** | **0** |
| API smoke | 3 | 3 | 0 |
| **Tổng automation** | **23** | **23** | **0** |

---

## 2b. UI Inventory (PHASE 0.6)

| # | Vùng UI | Nhãn (i18n) | Loại | Hành vi | TC | Trạng thái |
|---|---------|-------------|------|---------|-----|------------|
| 1 | Header | Tạo Bài viết mới | h1 | Title | BLOGCREATE_001 | ✅ |
| 2 | Header | Quay lại | button | → list | BLOGCREATE_017 | ✅ |
| 3 | Header | Hủy / Lưu nháp / Xuất bản | buttons | nav / submit | BLOGCREATE_016, 019 | ✅ |
| 4 | Content | Tiêu đề | input | required max 255 | BLOGCREATE_003–004 | ✅ |
| 5 | Content | Slug preview | text | auto slugify | BLOGCREATE_006 | ✅ |
| 6 | Content | Mô tả ngắn | textarea | max 500 | BLOGCREATE_005 | ✅ |
| 7 | Content | Nội dung Markdown | editor | required | BLOGCREATE_003, 007 | ✅ |
| 8 | Sidebar | Draft / Published / Scheduled | radio | status payload | BLOGCREATE_010–012 | ✅ |
| 9 | Sidebar | Ngày + giờ lên lịch | date/time | scheduled only | BLOGCREATE_012 | ✅ |
| 10 | Sidebar | Lưu bản nháp / Xuất bản | button submit | POST | BLOGCREATE_010–011 | ✅ |
| 11 | Sidebar | Hủy | button | → list | BLOGCREATE_015 | ✅ |
| 12 | Sidebar | Danh mục checkbox | input | min 1 category | BLOGCREATE_002–003 | ✅ |
| 13 | Sidebar | Thêm danh mục mới | inline form | POST category | BLOGCREATE_014 | ✅ |
| 14 | Sidebar | Ảnh đại diện | upload | optional | BLOGCREATE_008 | ✅ |
| 15 | Sidebar | 💡 Lưu ý | guidelines | static | BLOGCREATE_001 | ✅ |

---

## 2c. Data Display Integrity (PHASE 0.7)

| # | Vùng UI | Field API | Field form | TC | Trạng thái |
|---|---------|-----------|------------|-----|------------|
| 1 | Categories | `categories[].name` | checkbox label | BLOGCREATE_002 | ✅ |
| 2 | Slug preview | slugify(title) | preview text | BLOGCREATE_006 | ✅ |
| 3 | POST draft | `status: draft` | radio draft | BLOGCREATE_010 | ✅ |
| 4 | POST publish | `status: published` | radio published | BLOGCREATE_011 | ✅ |
| 5 | POST scheduled | `published_at` + published | date/time | BLOGCREATE_012 | ✅ |
| 6 | List after create | `title` | row text | BLOGCREATE_020 | ✅ |

---

## 3. Test cases (automation)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_BLOGCREATE_001 | Heading, form, publish options, guidelines | ✅ |
| TC_AD_BLOGCREATE_002 | Categories load từ API | ✅ |
| TC_AD_BLOGCREATE_003 | Submit trống → lỗi title, content, category | ✅ |
| TC_AD_BLOGCREATE_004 | Title > 255 ký tự | ✅ |
| TC_AD_BLOGCREATE_005 | Excerpt > 500 ký tự | ✅ |
| TC_AD_BLOGCREATE_006 | Slug preview tự động từ title | ✅ |
| TC_AD_BLOGCREATE_007 | Nhập markdown vào editor | ✅ |
| TC_AD_BLOGCREATE_008 | Upload ảnh đại diện + preview | ✅ |
| TC_AD_BLOGCREATE_010 | Lưu bản nháp → toast + redirect edit | ✅ |
| TC_AD_BLOGCREATE_011 | Xuất bản → toast + redirect edit | ✅ |
| TC_AD_BLOGCREATE_012 | Lên lịch với ngày tương lai trong payload | ✅ |
| TC_AD_BLOGCREATE_013 | Lên lịch không chọn ngày → lỗi validation | ✅ |
| TC_AD_BLOGCREATE_014 | Thêm danh mục inline + auto chọn | ✅ |
| TC_AD_BLOGCREATE_015 | Hủy sidebar (mobile) → list | ✅ |
| TC_AD_BLOGCREATE_016 | Hủy header → list | ✅ |
| TC_AD_BLOGCREATE_017 | Nút back → list | ✅ |
| TC_AD_BLOGCREATE_018 | API create lỗi → toast, ở lại trang | ✅ |
| TC_AD_BLOGCREATE_019 | Chọn published đổi label nút header | ✅ |
| TC_AD_BLOGCREATE_020 | Draft mới xuất hiện trên list | ✅ |
| TC_AD_BLOGCREATE_025 | Guest redirect login | ✅ |
| TC_AD_BLOGCREATE_026 | Non-admin redirect login | ✅ |
| API_BLOGCREATE_001 | POST create 401 unauthenticated | ✅ |
| API_BLOGCREATE_002 | POST create valid admin | ✅ |
| API_BLOGCREATE_003 | POST create invalid payload 422+ | ✅ |

---

## 4. Test data

* Title draft/publish: **Ăn gì ở Đà Nẵng: Top 10 món ngon automation**
* Slug source: **Bánh tráng cuốn thịt heo** → `banh-trang-cuon-thit-heo`
* Category: **Ẩm thực** (`id=2`)
* Inline category: **Danh mục test automation**
* Scheduled: `2099-12-31` `09:00`

**Mock flags:** `setBlogCreateFail`, `setBlogCategoryCreateFail`

---

## 8. Đề xuất cải thiện (PHASE 0.8)

| ID | Loại | Ưu tiên | Tóm tắt | Trạng thái |
|----|------|---------|---------|------------|
| IMP_BLOGCREATE_001 | Doc | P2 | Doc cũ route `/admin/blog/create` | **fixed** (doc) |
| IMP_BLOGCREATE_002 | Doc | P2 | Doc ghi Staff — thực tế chỉ Admin | **fixed** (doc) |
| IMP_BLOGCREATE_003 | UX | P2 | Layout header `max-w-[1600px]` chưa full-bleed | **fixed** |
| IMP_BLOGCREATE_004 | Validation | P3 | Doc ghi ảnh bìa bắt buộc — schema optional | **fixed** (doc) |
| IMP_BLOGCREATE_005 | A11y | P3 | Nút back thiếu `aria-label` | **fixed** |
| IMP_BLOGCREATE_006 | i18n | P3 | Loading categories hardcode EN | **fixed** |
| IMP_BLOGCREATE_007 | UX | P1 | Mobile thiếu sticky footer actions | **fixed** |
| IMP_BLOGCREATE_008 | Validation | P1 | Scheduled không có ngày vẫn submit được | **fixed** |
| IMP_BLOGCREATE_009 | Code | P1 | Header submit dùng `getElementById` | **fixed** (`form="blog-post-form"`) |
| IMP_BLOGCREATE_010 | UX | P2 | Sticky header chưa collapse khi scroll | **fixed** |
| IMP_BLOGCREATE_011 | UX | P2 | Sau create redirect list thay vì edit | **fixed** |
| IMP_BLOGCREATE_012 | i18n | P3 | Markdown editor hardcode EN | **fixed** |
| IMP_BLOGCREATE_013 | A11y | P3 | Checkbox category thiếu `aria-label` | **fixed** |

---

## Ghi chú doc cũ → thực tế

| Doc cũ | Thực tế |
|--------|---------|
| Route `/admin/blog/create` | `/admin/blog-posts/create` |
| WYSIWYG | **Markdown editor** (react-markdown-editor-lite) |
| Quyền Admin/Staff | **Chỉ Admin** |
| Ảnh bìa bắt buộc | **Optional** trong Yup schema |
