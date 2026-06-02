# Chi tiết bài viết blog - Test Cases

## 1. Tổng quan màn hình

* Đường dẫn route: `/[locale]/blog/[slug]`
* File source chính: `D:\DATN\danangtrip-web\src\app\[locale]\(main)\(public)\blog\[slug]\page.tsx`
* Component liên quan: `ReadingProgressBar`, `BlogDetailHeader`, `BlogRichText`, `AuthorCard`, `RelatedPosts`, `BlogDetailSidebar`, `TableOfContents`
* API/service sử dụng: `blogService.getDetail(slug)`, `blogService.getSidebarData()`, `blogService.getLatest({ category_id })`
* Quyền truy cập: Guest/User đều xem được
* Mục đích màn hình: Hiển thị bài viết chi tiết, xử lý heading để tạo mục lục, hiển thị tác giả, bài liên quan và sidebar bài phổ biến.

## 2. Điều kiện tiền đề

* Dữ liệu cần có: bài viết published có slug, content HTML, author, categories, featured_image.
* Tài khoản cần dùng: không bắt buộc đăng nhập.
* Trạng thái hệ thống: API blog detail/sidebar/latest hoạt động.
* Quyền user/admin/staff: public.

## 3. Danh sách chức năng chính

* Server load post detail và metadata OpenGraph.
* Xử lý HTML content để inject id cho H2/H3 và tạo TOC.
* Load popular posts sidebar.
* Load related posts cùng category, loại trừ bài hiện tại.
* Hiển thị featured image, rich text, author card, reading progress.
* Xử lý not found khi post không tồn tại.

## 4. Test cases chi tiết

| ID | Nhóm chức năng | Test case | Tiền điều kiện | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Mức độ ưu tiên | Loại test |
| -- | -------------- | --------- | -------------- | -------------- | ------------ | ---------------- | -------------- | --------- |
| BLOG_DETAIL_001 | Load dữ liệu | Mở bài viết hợp lệ | Blog published tồn tại | 1. Mở `/vi/blog/cam-nang-da-nang`.<br>2. Chờ load. | slug hợp lệ | Header, ảnh, content, author, related/sidebar hiển thị. | High | Functional |
| BLOG_DETAIL_002 | Metadata | Metadata theo bài viết | Post có title/excerpt/image | 1. Kiểm tra title/OG. | post full | Title, description, OG image, author, publishedTime đúng post. | Medium | Regression |
| BLOG_DETAIL_003 | Not found | Slug không tồn tại | Không có post | 1. Mở `/vi/blog/invalid`. | invalid | Gọi `notFound()`, không render content rỗng. | High | Negative |
| BLOG_DETAIL_004 | API detail lỗi | API detail trả lỗi | Mock 500 | 1. Mở bài viết. | 500 | Error được throw/notFound theo source; không lộ partial data sai. | High | API |
| BLOG_DETAIL_005 | Featured image | Bài viết có ảnh bìa | `featured_image` có URL | 1. Quan sát ảnh. | image URL | Ảnh aspect video, alt bằng title, priority load. | Medium | UI |
| BLOG_DETAIL_006 | Không có ảnh bìa | `featured_image=null` | Post thiếu ảnh | 1. Mở detail. | null | Không render khung ảnh rỗng; content vẫn đúng. | Medium | Edge Case |
| BLOG_DETAIL_007 | Rich text heading | Content có H2/H3 | HTML content | 1. Mở detail.<br>2. Inspect heading id. | H2/H3 | Heading thiếu id được inject id; TOC có heading tương ứng. | High | Functional |
| BLOG_DETAIL_008 | Heading đã có id | H2/H3 có id sẵn | HTML có id | 1. Mở detail.<br>2. Inspect heading. | `<h2 id="x">` | Giữ id cũ, không tạo id mới sai. | Medium | Regression |
| BLOG_DETAIL_009 | Content không heading | Bài không có H2/H3 | Content plain paragraph | 1. Mở detail. | no headings | TOC rỗng/ẩn hợp lý; content vẫn render. | Medium | Edge Case |
| BLOG_DETAIL_010 | HTML phức tạp | Content có list/blockquote/link/image | Post full content | 1. Cuộn content. | HTML | `BlogRichText` render đúng style, không raw tag lỗi. | High | UI |
| BLOG_DETAIL_011 | XSS regression | Content chứa script | Dữ liệu kiểm thử an toàn | 1. Render content có `<script>`. | script tag | Script không được thực thi nếu backend/sanitizer xử lý; cần đánh dấu nếu vẫn render raw nguy hiểm. | High | Security |
| BLOG_DETAIL_012 | Reading progress | Thanh tiến độ đọc | Bài dài | 1. Cuộn từ đầu đến cuối. | long post | Progress tăng theo scroll, không che header/content. | Low | UI |
| BLOG_DETAIL_013 | Author card | Hiển thị tác giả | Post có author | 1. Quan sát AuthorCard. | author full | Tên/avatar/thông tin author hiển thị; fallback nếu thiếu avatar. | Medium | UI |
| BLOG_DETAIL_014 | Author thiếu data | Author thiếu avatar/name phụ | Partial author | 1. Mở detail. | no avatar | Không crash; fallback avatar/initial hợp lý. | Medium | Edge Case |
| BLOG_DETAIL_015 | Related posts | Bài liên quan cùng category | Post có category và latest posts | 1. Cuộn related.<br>2. Click một bài. | 3 related | Related tối đa 3, không chứa post hiện tại, click đúng slug. | Medium | Functional |
| BLOG_DETAIL_016 | Không có category | Post không có categories | categories=[] | 1. Mở detail. | no category | Không gọi latest category hoặc related rỗng; không crash. | Medium | Edge Case |
| BLOG_DETAIL_017 | Sidebar popular | Popular posts desktop | Sidebar data có popular | 1. Mở desktop.<br>2. Quan sát sidebar. | 5 popular | Hiển thị tối đa 5 popular posts; link đúng locale/slug. | Low | Functional |
| BLOG_DETAIL_018 | Sidebar API lỗi | sidebarData lỗi | Mock 500 | 1. Mở detail. | 500 | Nếu Promise.all lỗi, route xử lý lỗi; ghi nhận rủi ro vì detail có thể fail do sidebar. | High | API |
| BLOG_DETAIL_019 | Latest API lỗi | related latest lỗi | Mock 500 | 1. Mở detail. | 500 | Nếu Promise.all lỗi, route throw; cần xác nhận error boundary/notFound. | High | API |
| BLOG_DETAIL_020 | Locale vi/en | Đường dẫn locale | Có locale en | 1. Mở `/en/blog/[slug]`. | en | Header/sidebar link giữ locale; metadata không lỗi. | Medium | Regression |
| BLOG_DETAIL_021 | TOC click | Click mục lục | Desktop, có headings | 1. Click heading trong sidebar. | H2 | Scroll đến đúng section id. | Medium | Functional |
| BLOG_DETAIL_022 | Mobile sidebar | Sidebar ẩn trên mobile | Viewport 375px | 1. Mở detail. | mobile | Sidebar hidden theo `hidden lg:block`; content 1 cột không tràn. | Medium | Responsive |
| BLOG_DETAIL_023 | Desktop layout | Layout 8/4 cột | Viewport 1440px | 1. Mở detail. | desktop | Content 8 cột, sidebar 4 cột; gap đúng, không overlap. | Low | Responsive |
| BLOG_DETAIL_024 | Image lỗi | Featured image 404 | URL lỗi | 1. Mở detail. | 404 image | Next Image xử lý lỗi không làm mất content; cần fallback nếu có. | Low | Edge Case |
| BLOG_DETAIL_025 | Regression | Bài viết dài | Content rất dài | 1. Cuộn hết bài.<br>2. Kiểm tra footer. | long post | Progress, sidebar sticky/hidden và related không chồng footer. | Medium | Regression |

## 5. Test data đề xuất

* Post full: có featured image, author, 2 categories, content H2/H3/list/blockquote.
* Post thiếu ảnh, không category, không heading.
* Sidebar popular có 5 bài.
* Related có 4 bài cùng category, trong đó có post hiện tại để test filter.

## 6. Checklist regression

* Slug sai vào not found.
* Heading H2/H3 tạo TOC đúng.
* Related không chứa bài hiện tại.
* Sidebar lỗi không gây trải nghiệm xấu.
* Mobile ẩn sidebar, không tràn ngang.

## 7. Ghi chú kỹ thuật

* Hàm `processContent` nằm trực tiếp trong `blog/[slug]/page.tsx`.
* `Promise.all` cho sidebar/related là điểm rủi ro vì lỗi phụ có thể làm fail detail.
* Rủi ro cao: render HTML content, XSS, heading id sinh từ text tiếng Việt/ký tự đặc biệt.
