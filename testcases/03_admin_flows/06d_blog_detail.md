# Admin chi tiết bài viết - Test Cases

## 1. Tổng quan màn hình

* Đường dẫn route: `/admin/blog-posts/:id`
* File source chính: `D:\DATN\danangtrip-admin\src\pages\Blog\BlogPostDetail\index.tsx`
* Component liên quan: `BlogPostDetailHeader`, `BlogPostDetailContent`, `BlogPostDetailSidebar`, `DeleteConfirmDialog`, `DuplicateConfirmDialog`
* API/service sử dụng: `useAdminBlogPostQuery(id)`, `useBlogMutations().updateStatusMutation`, `deleteMutation`
* Quyền truy cập: Admin route; action xóa chỉ hiển thị/enabled với `isAdmin`
* Mục đích màn hình: Xem preview bài viết trong admin, đổi trạng thái xuất bản, mở bài public, chỉnh sửa, nhân bản và xóa bài viết.

## 2. Điều kiện tiền đề

* Dữ liệu cần có: bài viết draft, published, archived; bài có/không có featured image, author, categories, content.
* Tài khoản cần dùng: admin; staff/non-admin để test quyền xóa.
* Trạng thái hệ thống: API blog detail/update/delete hoạt động; web user chạy ở `http://localhost:3000` nếu test preview.
* Quyền user/admin/staff: admin được xóa; non-admin không được xóa.

## 3. Danh sách chức năng chính

* Load detail bài viết theo id.
* Hiển thị sticky header, status dropdown, preview public, edit, delete.
* Hiển thị nội dung preview, ảnh bìa, metadata, author, category.
* Đổi status `draft`, `published`, `archived`.
* Nhân bản bài viết bằng navigation state `duplicateData`.
* Xóa bài viết bằng confirm dialog.
* Loading skeleton và error state.

## 4. Test cases chi tiết

| ID | Nhóm chức năng | Test case | Tiền điều kiện | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Mức độ ưu tiên | Loại test |
| -- | -------------- | --------- | -------------- | -------------- | ------------ | ---------------- | -------------- | --------- |
| ADMIN_BLOG_DETAIL_001 | Permission | Guest truy cập route | Chưa đăng nhập | Mở `/admin/blog-posts/1`. | guest | Redirect login, không lộ dữ liệu bài viết. | High | Permission |
| ADMIN_BLOG_DETAIL_002 | Load dữ liệu | Mở detail bài viết hợp lệ | Bài viết tồn tại | Mở `/admin/blog-posts/10`. | id=10 | Header, content preview, sidebar metadata/actions hiển thị đúng. | High | Functional |
| ADMIN_BLOG_DETAIL_003 | Loading | Skeleton khi API chậm | API delay | Mở route. | delay | `BlogPostDetailSkeleton` hiển thị content + sidebar skeleton. | Medium | UI |
| ADMIN_BLOG_DETAIL_004 | Error | Bài viết không tồn tại | ID sai | Mở `/admin/blog-posts/999999`. | invalid | Error card “Không tìm thấy bài viết”, nút quay về danh sách. | High | Negative |
| ADMIN_BLOG_DETAIL_005 | Header title | Hiển thị title trong header | Post có title | Quan sát header. | title dài | Header truncate hợp lý, không tràn layout. | Medium | UI |
| ADMIN_BLOG_DETAIL_006 | Status badge | Hiển thị trạng thái hiện tại | Post draft/published/archived | Mở từng post. | statuses | Badge/dot/text đúng status. | Medium | UI |
| ADMIN_BLOG_DETAIL_007 | Status dropdown | Mở dropdown status | Post loaded | Click status dropdown. | | Dropdown hiện đủ draft/published/archived, current có dấu check. | Medium | Functional |
| ADMIN_BLOG_DETAIL_008 | Change draft | Đổi sang draft | Post published | Chọn draft. | draft | Mutation gọi status draft, toast success, refetch. | High | Functional |
| ADMIN_BLOG_DETAIL_009 | Change published | Đổi sang published | Post draft | Chọn published. | published | Status cập nhật, preview public enabled sau refetch. | High | Functional |
| ADMIN_BLOG_DETAIL_010 | Change archived | Đổi sang archived | Post published | Chọn archived. | archived | Status cập nhật, preview public disabled nếu không published. | High | Functional |
| ADMIN_BLOG_DETAIL_011 | Status API lỗi | Đổi status lỗi | API 500 | Chọn status khác. | 500 | Toast network_error, status không đổi sai. | High | API |
| ADMIN_BLOG_DETAIL_012 | Preview published | Mở bài public | Post status published, có slug | Click “Xem bài viết”. | slug | Mở tab mới `http://localhost:3000/blog/{slug}`. | Medium | Functional |
| ADMIN_BLOG_DETAIL_013 | Preview disabled | Bài chưa published | status draft/archived | Quan sát nút preview. | draft | Nút preview disabled, có helper title. | Medium | Regression |
| ADMIN_BLOG_DETAIL_014 | Edit | Điều hướng edit | Post loaded | Click Edit. | id | Điều hướng `/admin/blog-posts/edit/:id`. | High | Functional |
| ADMIN_BLOG_DETAIL_015 | Duplicate | Nhân bản bài viết | Post loaded | Click duplicate, confirm dialog. | post data | Điều hướng `/admin/blog-posts/create` với state `duplicateData`, toast success. | High | Functional |
| ADMIN_BLOG_DETAIL_016 | Delete admin | Xóa bài viết | Admin, post tồn tại | Click Delete, confirm. | id | Delete API gọi, toast success, điều hướng `/admin/blog-posts`. | High | Functional |
| ADMIN_BLOG_DETAIL_017 | Delete non-admin | Staff/non-admin xem detail | user.role != admin | Quan sát action xóa. | staff | Nút xóa bị ẩn/disabled, không gọi API. | High | Permission |
| ADMIN_BLOG_DETAIL_018 | Delete API lỗi | Xóa thất bại | API 500 | Confirm delete. | 500 | Toast network_error, dialog xử lý đúng, không điều hướng sai. | High | API |
| ADMIN_BLOG_DETAIL_019 | Content HTML | Render nội dung rich text | Content có HTML | Quan sát preview. | `<h2>...` | Nội dung hiển thị đúng, không raw HTML sai. | Medium | UI |
| ADMIN_BLOG_DETAIL_020 | Missing image | Không có ảnh bìa | featuredImage null | Mở detail. | null | Không vỡ layout, fallback/không render ảnh đúng. | Medium | Edge Case |
| ADMIN_BLOG_DETAIL_021 | Author metadata | Hiển thị tác giả | post.author có data | Quan sát sidebar. | author | Avatar/tên/role author hiển thị, fallback nếu thiếu avatar. | Medium | UI |
| ADMIN_BLOG_DETAIL_022 | Dates/views/categories | Metadata bổ sung | Post có created/updated/views/categories | Quan sát sidebar. | full | Ngày format đúng, view count đúng, category badge hiển thị. | Medium | Functional |
| ADMIN_BLOG_DETAIL_023 | No categories | Bài không category | categories=[] | Mở detail. | empty | Không render category block rỗng xấu. | Low | Edge Case |
| ADMIN_BLOG_DETAIL_024 | Responsive | Mobile layout | Viewport 375px | Mở detail. | mobile | Header actions không tràn; content/sidebar xếp dọc. | Medium | Responsive |
| ADMIN_BLOG_DETAIL_025 | Regression | Status -> preview -> edit | Post test | Đổi published, preview, quay lại, edit. | | Các hành động đúng route/state, không mất dữ liệu. | High | Regression |

## 5. Test data đề xuất

* Blog draft, published, archived.
* Blog có content HTML dài, ảnh bìa, author, nhiều categories.
* Blog thiếu ảnh/category/avatar.
* Admin và non-admin.

## 6. Checklist regression

* Status dropdown cập nhật và refetch đúng.
* Preview chỉ enabled với published.
* Delete chỉ admin.
* Duplicate truyền đủ data sang create.
* Header không tràn với title dài.

## 7. Ghi chú kỹ thuật

* Logic chính từ `BlogPostDetail/index.tsx`, header/sidebar từ component con.
* Rủi ro cao: preview hardcode `http://localhost:3000/blog/${slug}` không có locale, delete permission chỉ dựa `isAdmin` UI.
