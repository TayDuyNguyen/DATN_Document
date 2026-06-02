# Chi tiết tour - Test Cases

## 1. Tổng quan màn hình

* Đường dẫn route: `/[locale]/tours/[slug]`
* File source chính: `D:\DATN\danangtrip-web\src\app\[locale]\(main)\(public)\tours\[slug]\page.tsx`
* Component liên quan: `TourDetailClient`, `TourImageGallery`, `BookingSidebar`, `ItineraryTimeline`, `ReviewSection`, `RatingStars`, `FavoriteButton`
* API/service sử dụng: `tourService.getDetail(slug)`, `tourService.getSchedules(id)`, `tourService.checkAvailability(id)`, `tourService.getRatings(id)`, `tourService.getRatingStats(id)`, favorite hooks
* Quyền truy cập: Guest xem được; User đăng nhập thao tác yêu thích và đặt tour
* Mục đích màn hình: Hiển thị chi tiết tour, ảnh, mô tả, lịch trình, thông tin giá/đặt tour, đánh giá và điều hướng sang flow đặt tour.

## 2. Điều kiện tiền đề

* Dữ liệu cần có: tour active có slug hợp lệ; tour có/không có ảnh, itinerary, inclusions, exclusions, meeting point, lịch khởi hành, rating.
* Tài khoản cần dùng: guest; user thường đã đăng nhập.
* Trạng thái hệ thống: API web hoạt động; dữ liệu tour và schedule đã seed.
* Quyền user/admin/staff: guest chỉ xem; user được favorite và tiếp tục đặt tour; admin/staff không dùng màn này trong admin.

## 3. Danh sách chức năng chính

* Server load chi tiết tour theo slug và metadata SEO.
* Xử lý not found khi slug không tồn tại hoặc API lỗi.
* Hiển thị breadcrumb, gallery ảnh, badge hot/featured, tên tour, duration, rating.
* Hiển thị mô tả ngắn, mô tả HTML/text, itinerary, inclusions, exclusions, meeting point.
* Toggle yêu thích tour.
* Booking sidebar chọn lịch/số lượng và tính khả dụng.
* Hiển thị danh sách đánh giá và thống kê rating.
* Responsive layout 1 cột/mobile, 2 cột desktop.

## 4. Test cases chi tiết

| ID | Nhóm chức năng | Test case | Tiền điều kiện | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Mức độ ưu tiên | Loại test |
| -- | -------------- | --------- | -------------- | -------------- | ------------ | ---------------- | -------------- | --------- |
| TOUR_DETAIL_001 | Load dữ liệu | Mở trang tour detail với slug hợp lệ | Tour active tồn tại | 1. Mở `/vi/tours/ba-na-hills`.<br>2. Chờ API detail hoàn tất.<br>3. Quan sát toàn bộ first viewport. | slug `ba-na-hills` | Trang hiển thị breadcrumb, gallery, tên tour, duration, rating, booking sidebar; không có lỗi console nghiêm trọng. | High | Functional |
| TOUR_DETAIL_002 | Metadata | Kiểm tra metadata theo tour | Tour có name, thumbnail, short_desc | 1. Mở trang detail.<br>2. Kiểm tra title/meta/OG qua devtools hoặc SSR response. | Tour có thumbnail | Title dạng `{tour.name} — brand`; description lấy từ `short_desc` hoặc description rút gọn; OG image lấy thumbnail. | Medium | Regression |
| TOUR_DETAIL_003 | Not found | Slug không tồn tại | Không có tour với slug | 1. Mở `/vi/tours/invalid-slug`.<br>2. Quan sát UI. | `invalid-slug` | Render trang not found; không hiển thị layout detail rỗng; không gọi booking sidebar với tour undefined. | High | Negative |
| TOUR_DETAIL_004 | API lỗi | API detail trả lỗi 500 | Mock API lỗi | 1. Mở slug hợp lệ khi API lỗi.<br>2. Quan sát route. | HTTP 500 | Trang xử lý bằng `notFound()` theo source; không crash client. | High | API |
| TOUR_DETAIL_005 | Gallery | Gallery có thumbnail và nhiều ảnh | Tour có `thumbnail` và `images` | 1. Mở trang.<br>2. Quan sát gallery.<br>3. Kiểm tra ảnh trùng. | thumbnail + 4 images | Gallery loại bỏ URL trùng, hiển thị ảnh đúng tỷ lệ, alt theo tên tour. | High | UI |
| TOUR_DETAIL_006 | Gallery thiếu ảnh | Tour không có thumbnail/images | Tour active không có ảnh | 1. Mở detail tour thiếu ảnh.<br>2. Quan sát gallery. | `thumbnail=null`, `images=[]` | Gallery không làm vỡ layout; vùng ảnh có fallback hoặc không render theo component. | Medium | Edge Case |
| TOUR_DETAIL_007 | Badge | Hiển thị badge hot/featured | Tour `is_hot=true`, `is_featured=true` | 1. Mở detail.<br>2. Quan sát header tour. | hot + featured | Badge hot và featured hiển thị đúng text/màu; không hiển thị nếu false. | Low | UI |
| TOUR_DETAIL_008 | Rating | Hiển thị rating hợp lệ | Tour có avg_rating/review_count | 1. Mở detail.<br>2. Quan sát RatingStars. | avg 4.5, count 10 | Số sao và count hiển thị đúng; nếu rating không hợp lệ thì fallback 0. | Medium | Edge Case |
| TOUR_DETAIL_009 | Mô tả HTML | Render description dạng HTML | Tour description chứa HTML | 1. Mở detail.<br>2. Quan sát phần overview. | `<p>...</p>` | HTML render đúng, không hiển thị raw tag; layout không tràn. | High | UI |
| TOUR_DETAIL_010 | Mô tả text | Render description text thường | Description không có `<` | 1. Mở detail.<br>2. Quan sát line break. | text nhiều dòng | Text giữ xuống dòng bằng `whitespace-pre-line`; không mất nội dung. | Medium | UI |
| TOUR_DETAIL_011 | Thiếu mô tả | Không có short_desc/description | Tour thiếu mô tả | 1. Mở detail.<br>2. Quan sát overview. | null/empty | Section overview không render rỗng hoặc có fallback hợp lý; không tạo khoảng trắng bất thường. | Medium | Edge Case |
| TOUR_DETAIL_012 | Itinerary có dữ liệu | Hiển thị timeline lịch trình | Tour có itinerary | 1. Cuộn đến itinerary.<br>2. Kiểm tra từng ngày. | 3 ngày | Hiển thị đủ ngày, tiêu đề, nội dung; thứ tự đúng theo data. | High | Functional |
| TOUR_DETAIL_013 | Itinerary rỗng | Xử lý tour không có itinerary | `itinerary=[]` | 1. Mở detail.<br>2. Cuộn đến itinerary. | empty array | Component không crash; hiển thị empty/fallback theo thiết kế. | Medium | Edge Case |
| TOUR_DETAIL_014 | Inclusions | Hiển thị thông tin bao gồm | Tour có inclusions | 1. Cuộn đến block inclusions. | Text nhiều dòng | Nội dung hiển thị đúng, giữ xuống dòng, không bị cắt. | Medium | UI |
| TOUR_DETAIL_015 | Exclusions | Hiển thị thông tin không bao gồm | Tour có exclusions | 1. Cuộn đến block exclusions. | Text nhiều dòng | Nội dung hiển thị đúng; nếu field rỗng thì block không render. | Medium | UI |
| TOUR_DETAIL_016 | Meeting point | Hiển thị điểm hẹn | Tour có meeting_point | 1. Cuộn đến meeting point. | `Số 1 Bạch Đằng` | Điểm hẹn hiển thị cùng icon MapPin, không tràn text dài. | Medium | UI |
| TOUR_DETAIL_017 | Favorite user | User thêm tour yêu thích | User đã đăng nhập | 1. Click nút trái tim.<br>2. Chờ mutation xong. | tour_id hợp lệ | Icon đổi trạng thái/fill; API toggle được gọi; không double submit khi pending. | High | Functional |
| TOUR_DETAIL_018 | Favorite remove | User bỏ yêu thích | Tour đang favorite | 1. Click lại nút trái tim.<br>2. Chờ xong. | tour_id hợp lệ | Icon trở về trạng thái chưa favorite; cache cập nhật. | High | Functional |
| TOUR_DETAIL_019 | Favorite guest | Guest click favorite | Chưa đăng nhập | 1. Mở detail guest.<br>2. Click favorite. | guest | Hệ thống xử lý theo hook auth hiện tại: yêu cầu đăng nhập/toast hoặc fallback; không crash. | Medium | Permission |
| TOUR_DETAIL_020 | Favorite loading | Favorite query đang tải | API favorite chậm | 1. Mở trang.<br>2. Click nhanh favorite khi loading. | delay 2s | Button disabled khi `isLoading`/`isPending`; không gửi request lặp. | Medium | Regression |
| TOUR_DETAIL_021 | Booking sidebar load | Sidebar hiển thị thông tin đặt tour | Tour có lịch | 1. Mở detail.<br>2. Quan sát sidebar. | schedule available | Sidebar hiển thị giá, lựa chọn lịch/số khách/action đặt tour. | High | Functional |
| TOUR_DETAIL_022 | Chọn lịch | Chọn schedule còn chỗ | Tour có schedule available | 1. Chọn một ngày/lịch.<br>2. Quan sát trạng thái. | schedule_id available | Schedule được chọn, các thông tin giá/khả dụng cập nhật. | High | Functional |
| TOUR_DETAIL_023 | Lịch hết chỗ | Schedule full/remaining 0 | Có schedule full | 1. Chọn lịch full nếu UI cho chọn.<br>2. Quan sát CTA. | remaining 0 | Không cho đặt hoặc hiển thị hết chỗ; không chuyển sang booking với slot 0. | High | Edge Case |
| TOUR_DETAIL_024 | Số lượng người lớn | Người lớn tối thiểu 1 | Sidebar đang mở | 1. Giảm người lớn về 0.<br>2. Quan sát. | adult=1 | Không cho adult nhỏ hơn 1; validation/tổng tiền vẫn đúng. | High | Validation |
| TOUR_DETAIL_025 | Số lượng trẻ em/em bé | Child/infant không âm | Sidebar đang mở | 1. Tăng/giảm child/infant.<br>2. Giảm dưới 0. | child=0, infant=0 | Không cho số lượng âm; tổng khách cập nhật đúng. | High | Validation |
| TOUR_DETAIL_026 | Vượt sức chứa | Tổng khách vượt slot | Schedule còn 2 chỗ | 1. Chọn 3 khách.<br>2. Click đặt tour/check availability. | remaining=2, qty=3 | API/UX báo không đủ chỗ; không tiếp tục đặt tour. | High | Edge Case |
| TOUR_DETAIL_027 | Giá bằng 0 | Tour/schedule có giá 0 | Dữ liệu giá 0 | 1. Mở detail.<br>2. Quan sát giá/tổng tiền. | price=0 | Hiển thị miễn phí/0đ nhất quán; không NaN; vẫn tôn trọng rule booking. | Medium | Edge Case |
| TOUR_DETAIL_028 | Đặt tour guest | Guest click đặt tour | Chưa đăng nhập, đã chọn lịch | 1. Chọn lịch và số khách.<br>2. Click đặt tour. | guest | Điều hướng login hoặc thông báo cần đăng nhập theo guard; giữ callback nếu source hỗ trợ. | High | Permission |
| TOUR_DETAIL_029 | Đặt tour user | User click đặt tour | User đăng nhập, schedule hợp lệ | 1. Chọn lịch/số khách.<br>2. Click đặt tour. | valid data | Điều hướng sang `/tours/[slug]/book` hoặc flow booking đúng; dữ liệu chọn không bị mất nếu source lưu. | High | Functional |
| TOUR_DETAIL_030 | Check availability lỗi | API checkAvailability lỗi | Mock HTTP 500 | 1. Chọn lịch.<br>2. Click đặt/check. | 500 | Hiển thị lỗi/toast; không điều hướng sai. | High | API |
| TOUR_DETAIL_031 | Reviews load | Load danh sách đánh giá tour | Tour có review | 1. Cuộn đến ReviewSection.<br>2. Chờ API. | 10 reviews | Hiển thị stats và list review; phân trang/load more nếu component hỗ trợ. | Medium | Functional |
| TOUR_DETAIL_032 | Reviews empty | Tour chưa có review | No reviews | 1. Mở tour chưa review.<br>2. Quan sát ReviewSection. | count=0 | Hiển thị trạng thái chưa có đánh giá, không render danh sách rỗng sai. | Low | Edge Case |
| TOUR_DETAIL_033 | Reviews API lỗi | API ratings lỗi | Mock ratings 500 | 1. Mở detail.<br>2. Cuộn reviews. | 500 | Section review hiển thị lỗi/fallback; phần còn lại của trang vẫn dùng được. | Medium | API |
| TOUR_DETAIL_034 | Breadcrumb | Điều hướng về danh sách tour | Trang detail đang mở | 1. Click breadcrumb Tours. | | Điều hướng về `/tours` đúng locale. | Low | Regression |
| TOUR_DETAIL_035 | Locale EN | Route tiếng Anh | Có locale en | 1. Mở `/en/tours/[slug]`. | locale en | Text dịch theo locale; route và link giữ locale. | Medium | Regression |
| TOUR_DETAIL_036 | Responsive desktop | Layout 2 cột desktop | Viewport 1440px | 1. Mở trang.<br>2. Cuộn. | | Content 8 cột, sidebar 4 cột; sidebar không che footer/header. | Medium | Responsive |
| TOUR_DETAIL_037 | Responsive tablet | Layout tablet | Viewport 768px | 1. Mở trang.<br>2. Kiểm tra gallery/sidebar. | | Không tràn ngang; booking sidebar chuyển vị trí hợp lý. | Medium | Responsive |
| TOUR_DETAIL_038 | Responsive mobile | Layout mobile | Viewport 375px | 1. Mở trang.<br>2. Cuộn toàn trang. | | Một cột, CTA/nút favorite đủ chạm, text không chồng nhau. | High | Responsive |
| TOUR_DETAIL_039 | Dữ liệu số sai | avg_rating/review_count không phải số | Mock data lỗi | 1. Render detail với rating string invalid. | `avg_rating='abc'` | Fallback rating 0, review count 0; không NaN. | Medium | Edge Case |
| TOUR_DETAIL_040 | Regression visual | Kiểm tra không vỡ bố cục sau thay đổi CSS | Tour đầy đủ dữ liệu | 1. Chụp màn desktop/mobile.<br>2. So với baseline. | full data | Gallery, card content, sidebar, reviews không overlap. | Medium | Regression |

## 5. Test data đề xuất

* Tour full: `ba-na-hills`, active, hot, featured, 5 ảnh, 3 ngày itinerary, 3 schedule, rating 4.5.
* Tour thiếu dữ liệu: không ảnh, description rỗng, itinerary rỗng, meeting_point null.
* Schedule: available còn 20 chỗ, full 0 chỗ, deadline đã qua, giá adult/child/infant khác nhau.
* User: guest, user thường đã đăng nhập, user đã favorite tour.

## 6. Checklist regression

* Detail tour load đúng slug và không bị not found sai.
* Gallery không trùng ảnh, không vỡ layout khi thiếu ảnh.
* Booking sidebar không cho đặt khi thiếu lịch/hết chỗ.
* Favorite không gửi request lặp.
* Review section không làm crash trang khi API lỗi.
* Mobile không tràn ngang.

## 7. Ghi chú kỹ thuật

* Logic server route lấy từ `tours/[slug]/page.tsx`.
* UI chính lấy từ `TourDetailClient.tsx`.
* Booking sidebar phụ thuộc `BookingSidebar`, `tourService.getSchedules`, `tourService.checkAvailability`.
* Rủi ro cao: dữ liệu thiếu ảnh/mô tả, schedule full, favorite guest, rating invalid và layout mobile.
