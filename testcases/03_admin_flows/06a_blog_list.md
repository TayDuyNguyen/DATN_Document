# Admin — Danh sách Bài viết (Blog Posts List)

**Route:** `/admin/blog-posts`  
**Source:** `danangtrip-admin/src/pages/Blog/BlogPostList/index.tsx`  
**Automation:** `blog-list.spec.ts` + `blog-list-auth.spec.ts` + `admin-blog-list.api.spec.ts` · POM: `BlogListPage.ts`

**Chạy:** `npm run test:admin:blog-list` · `--workers=1`

> **Lưu ý:** Chỉ **Admin** (`PrivateRoute`). Tìm kiếm **debounce 300ms** + Enter. Filter category/status **auto-apply**. Stats nhúng trong response list (`stats`). Cột: Bài viết (ảnh + excerpt + tác giả), Danh mục, Lượt xem, Ngày tạo, Ngày xuất bản, Trạng thái (dropdown), Thao tác.

---

## 1. Phạm vi

| Hạng mục | Chi tiết |
|----------|----------|
| API list | `GET /admin/blog-posts` — `search`, `category_id`, `status`, `sort`, `order`, `page`, `per_page` |
| API categories | `GET /admin/blog-categories` |
| API mutation | `PATCH /admin/blog-posts/:id/status`, `DELETE /admin/blog-posts/:id`, bulk qua client |
| Quyền | Admin route guard |

---

## 2. Tổng quan trạng thái

| Nhóm | Tổng TC | ✅ Auto | ⏳ Backlog |
|------|---------|---------|------------|
| Page load & stats | 3 | 3 | 0 |
| Data display | 1 | 1 | 0 |
| Search | 2 | 2 | 0 |
| Filters | 5 | 5 | 0 |
| Pagination & refresh | 3 | 3 | 0 |
| Navigation | 4 | 4 | 0 |
| Sort | 2 | 2 | 0 |
| Delete | 3 | 3 | 0 |
| Status inline | 2 | 2 | 0 |
| Bulk actions | 6 | 6 | 0 |
| Empty & error | 3 | 3 | 0 |
| Auth | 3 | 3 | 0 |
| **UI subtotal** | **35** | **35** | **0** |
| API smoke | 4 | 4 | 0 |
| **Tổng automation** | **42** | **42** | **0** |

---

## 2b. UI Inventory (PHASE 0.6)

| # | Vùng UI | Nhãn (i18n) | Loại | Hành vi | TC | Trạng thái |
|---|---------|-------------|------|---------|-----|------------|
| 1 | Header | Danh sách Bài viết / Blog Posts | h1 | Title | BLOGLIST_001 | ✅ |
| 2 | Header | Thêm mới / Add New | button | → create | BLOGLIST_004 | ✅ |
| 3 | Stats | Tổng / Published / Draft / Archived | cards | API stats | BLOGLIST_002 | ✅ |
| 4 | Filter | Tìm tiêu đề | input | debounce + Enter | BLOGLIST_014–015 | ✅ |
| 5 | Filter | Danh mục | select | category_id | BLOGLIST_018 | ✅ |
| 6 | Filter | Trạng thái | select | status | BLOGLIST_019–021 | ✅ |
| 7 | Filter | Đặt lại + chip bộ lọc | button/chip | clear + active label | BLOGLIST_024–025 | ✅ |
| 8 | Table | Refresh | icon | refetch | BLOGLIST_035 | ✅ |
| 9 | Table | Per page | select | per_page | BLOGLIST_033 | ✅ |
| 10 | Table | Pagination | buttons | page | BLOGLIST_032 | ✅ |
| 11 | Row | Checkbox | input | bulk | BLOGLIST_051–052 | ✅ |
| 12 | Row | Tiêu đề click | h4 | → detail | BLOGLIST_038 | ✅ |
| 13 | Row | Status dropdown | button | PATCH status | BLOGLIST_041 | ✅ |
| 14 | Row | Xem / Sửa / Xóa | icon | nav / modal | BLOGLIST_036–037, 046 | ✅ |
| 15 | Bulk bar | Xuất bản / Lưu trữ / Xóa | buttons | batch + partial | BLOGLIST_054–058 | ✅ |
| 16 | Dialog | Xóa đơn / bulk | modal | DELETE | BLOGLIST_046–048, 056–057 | ✅ |
| 17 | Empty | Không tìm thấy bài viết | text | API `[]` | BLOGLIST_060 | ✅ |
| 18 | List error | Không tải được danh sách + Retry | panel | list fail, stats ẩn | BLOGLIST_062 | ✅ |
| 19 | Scheduled | Badge LÊN LỊCH | chip | published_at tương lai | BLOGLIST_061 | ✅ |

---

## 2c. Data Display Integrity (PHASE 0.7)

| # | Vùng UI | Field API | Field UI | TC | Trạng thái |
|---|---------|-----------|----------|-----|------------|
| 1 | Title | `title` | h4 + click | BLOGLIST_003 | ✅ |
| 2 | Excerpt | `excerpt` | paragraph | BLOGLIST_003 | ✅ |
| 3 | Author | `author.full_name` | text under title | BLOGLIST_003 | ✅ |
| 4 | Category | `categories[].name` | badge | BLOGLIST_003, 018 | ✅ |
| 5 | Views | `view_count` | formatted number | BLOGLIST_003 | ✅ |
| 6 | Stats | `stats` in list | 4 StatCards | BLOGLIST_002 | ✅ |

---

## 3. Test cases (automation)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_BLOGLIST_001 | Heading, stats, filter, table (10 rows/page) | ✅ |
| TC_AD_BLOGLIST_002 | Stats cards đúng số từ mock | ✅ |
| TC_AD_BLOGLIST_003 | Title + excerpt + author + category + views | ✅ |
| TC_AD_BLOGLIST_004 | Thêm mới → create | ✅ |
| TC_AD_BLOGLIST_014 | Search debounce theo tiêu đề | ✅ |
| TC_AD_BLOGLIST_015 | Search Enter | ✅ |
| TC_AD_BLOGLIST_018 | Filter danh mục Kinh nghiệm | ✅ |
| TC_AD_BLOGLIST_019 | Filter trạng thái draft | ✅ |
| TC_AD_BLOGLIST_020 | Filter trạng thái published | ✅ |
| TC_AD_BLOGLIST_021 | Filter trạng thái archived | ✅ |
| TC_AD_BLOGLIST_024 | Reset filter | ✅ |
| TC_AD_BLOGLIST_025 | Chip bộ lọc đang kích hoạt | ✅ |
| TC_AD_BLOGLIST_028 | Sort lượt xem desc/asc | ✅ |
| TC_AD_BLOGLIST_029 | Sort ngày tạo desc/asc | ✅ |
| TC_AD_BLOGLIST_032 | Pagination trang 2 | ✅ |
| TC_AD_BLOGLIST_033 | Đổi per_page 20 | ✅ |
| TC_AD_BLOGLIST_035 | Refresh refetch | ✅ |
| TC_AD_BLOGLIST_036 | Eye → detail | ✅ |
| TC_AD_BLOGLIST_037 | Edit → edit page | ✅ |
| TC_AD_BLOGLIST_038 | Click title → detail | ✅ |
| TC_AD_BLOGLIST_041 | Đổi status → published | ✅ |
| TC_AD_BLOGLIST_045 | Toast lỗi khi status fail | ✅ |
| TC_AD_BLOGLIST_046 | Xóa + confirm dialog | ✅ |
| TC_AD_BLOGLIST_048 | Hủy dialog — không DELETE | ✅ |
| TC_AD_BLOGLIST_050 | Toast lỗi khi delete fail | ✅ |
| TC_AD_BLOGLIST_051 | Chọn dòng → bulk toolbar | ✅ |
| TC_AD_BLOGLIST_052 | Chọn tất cả trên trang | ✅ |
| TC_AD_BLOGLIST_054 | Bulk xuất bản | ✅ |
| TC_AD_BLOGLIST_055 | Bulk lưu trữ | ✅ |
| TC_AD_BLOGLIST_056 | Bulk xóa sau confirm | ✅ |
| TC_AD_BLOGLIST_057 | Hủy bulk delete | ✅ |
| TC_AD_BLOGLIST_058 | Bulk partial fail toast | ✅ |
| TC_AD_BLOGLIST_060 | Empty state | ✅ |
| TC_AD_BLOGLIST_061 | Badge lên lịch (scheduled) | ✅ |
| TC_AD_BLOGLIST_062 | List error + Retry, stats ẩn | ✅ |
| TC_AD_BLOGLIST_065 | Guest redirect login | ✅ |
| TC_AD_BLOGLIST_066 | Non-admin redirect login | ✅ |
| TC_AD_BLOGLIST_067 | Legacy `/admin/blog` redirect | ✅ |
| API_BLOGLIST_001 | GET list 401 unauthenticated | ✅ |
| API_BLOGLIST_002 | GET list paginated admin | ✅ |
| API_BLOGLIST_003 | GET list filter status | ✅ |
| API_BLOGLIST_004 | GET categories | ✅ |

---

## 4. Test data

* Primary search: **Ẩm thực Đà Nẵng** (`id=201`)
* Deletable: **Bài viết test xóa automation** (`id=215`)
* Status change: **Lịch trình 3 ngày 2 đêm** (`id=203`, draft)
* Bulk draft: **Draft bulk publish A/B** (`id=212`, `213`)
* Scheduled: **Bài viết lên lịch automation** (`id=216`, `published_at` tương lai)
* Categories: Kinh nghiệm, Ẩm thực, Du lịch

**Mock flags:** `setBlogListFail`, `setBlogListEmpty`, `setBlogDeleteFailForId`, `setBlogStatusFailForId`, `setBlogMutationFail`

---

## 8. Đề xuất cải thiện (PHASE 0.8)

| ID | Loại | Ưu tiên | Tóm tắt | Trạng thái |
|----|------|---------|---------|------------|
| IMP_BLOGLIST_001 | Doc | P2 | Doc gốc route `/admin/blog` — thực tế `/admin/blog-posts` | **fixed** (doc) |
| IMP_BLOGLIST_002 | Doc | P2 | Doc ghi Staff — thực tế chỉ Admin | **fixed** (doc) |
| IMP_BLOGLIST_003 | UX | P1 | List API lỗi → bảng empty, không ErrorWidget + Retry (khác Location List) | **fixed** |
| IMP_BLOGLIST_004 | UX | P2 | Nút Đặt lại trong `<form>` thiếu `type="button"` | **fixed** |
| IMP_BLOGLIST_005 | UX | P2 | Sidebar parent `/admin/blog` không có route redirect | **fixed** |
| IMP_BLOGLIST_006 | UX | P2 | Stats error trùng list error panel | **fixed** — ẩn stats khi list fail |
| IMP_BLOGLIST_007 | i18n | P2 | Checkbox thiếu key `common:table.select_*` | **fixed** |
| IMP_BLOGLIST_008 | Test | P2 | Thiếu TC bulk archive / partial / redirect / sort created_at / scheduled / chips | **fixed** |
