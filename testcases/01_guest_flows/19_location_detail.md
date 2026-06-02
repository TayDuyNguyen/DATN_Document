# Chi tiết địa điểm - Test Cases

## 1. Tổng quan màn hình

* Đường dẫn route: `/[locale]/locations/[slug]`
* File source chính: `D:\DATN\danangtrip-web\src\app\[locale]\(main)\(public)\locations\[slug]\page.tsx`
* Component liên quan: `LocationDetailClient`, `LocationHero`, `LocationGallery`, `LocationInfo`, `LocationSidebar`, `LocationReviews`, `WriteReviewModal`, `LocationNearby`, `WeatherWidget`, `LocationMapPreview`
* API/service sử dụng: `locationService.getDetail(slug)`, `locationService.getImages(id)`, `locationService.getNearbyByLocationId(id)`, rating APIs, favorite hooks, record view hook
* Quyền truy cập: Guest xem được; user đăng nhập được favorite, viết review, đánh dấu helpful nếu source cho phép.
* Mục đích màn hình: Hiển thị thông tin chi tiết địa điểm, ảnh, bản đồ/sidebar, thời tiết/nearby, đánh giá và tương tác yêu thích/review.

## 2. Điều kiện tiền đề

* Dữ liệu cần có: địa điểm active có slug, ảnh, mô tả, category, địa chỉ, tọa độ, rating/reviews, nearby.
* Tài khoản cần dùng: guest; user chưa review; user đã review.
* Trạng thái hệ thống: API location/images/nearby/rating hoạt động.
* Quyền user/admin/staff: guest chỉ xem; user có thể tương tác; admin/staff không dùng màn này.

## 3. Danh sách chức năng chính

* Server load location detail và metadata.
* Client record view sau khi mount.
* Fetch ảnh bổ sung và nearby bằng React Query.
* Toggle favorite địa điểm.
* Hiển thị gallery, info, sidebar, bản đồ, weather/nearby.
* Hiển thị review list, write review modal, helpful action.
* Loading/error/empty cho images, nearby, reviews.

## 4. Test cases chi tiết

| ID | Nhóm chức năng | Test case | Tiền điều kiện | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Mức độ ưu tiên | Loại test |
| -- | -------------- | --------- | -------------- | -------------- | ------------ | ---------------- | -------------- | --------- |
| LOCATION_DETAIL_001 | Load dữ liệu | Mở detail địa điểm hợp lệ | Location active | 1. Mở `/vi/locations/ngu-hanh-son`.<br>2. Chờ trang load. | slug hợp lệ | Hiển thị hero, tên địa điểm, info, reviews, sidebar; metadata title theo location. | High | Functional |
| LOCATION_DETAIL_002 | Not found | Slug không tồn tại | Không có location | 1. Mở `/vi/locations/invalid`. | invalid | Trang not found; không render client detail rỗng. | High | Negative |
| LOCATION_DETAIL_003 | API detail lỗi | API detail trả 500 | Mock 500 | 1. Mở slug hợp lệ. | 500 | Route xử lý notFound theo source; không crash toàn app. | High | API |
| LOCATION_DETAIL_004 | Record view | Ghi nhận lượt xem | Location hợp lệ | 1. Mở detail.<br>2. Theo dõi network. | id location | Hook record view gọi hợp lý sau mount, không spam request khi re-render. | Medium | API |
| LOCATION_DETAIL_005 | Gallery API | Ảnh lấy từ API images | API images có data | 1. Mở detail.<br>2. Chờ images query. | 5 images | Gallery dùng ảnh API nếu có, hiển thị đúng locationName. | High | UI |
| LOCATION_DETAIL_006 | Gallery fallback | API images rỗng, location.images có data | images API empty | 1. Mở detail. | location.images | Gallery fallback sang `location.images`. | Medium | Edge Case |
| LOCATION_DETAIL_007 | Gallery loading | Images loading và chưa có fallback | API delay, images rỗng | 1. Mở detail. | delay | Gallery loading state hiển thị, không vỡ layout. | Medium | UI |
| LOCATION_DETAIL_008 | Không có ảnh | Location không có ảnh | No images | 1. Mở detail. | empty | Section gallery không render hoặc fallback hợp lý; không tạo khoảng trắng lớn. | Medium | Edge Case |
| LOCATION_DETAIL_009 | Favorite user | User toggle favorite | User đăng nhập | 1. Click favorite trên hero. | user | Trạng thái favorite cập nhật; button pending khi mutation chạy. | High | Functional |
| LOCATION_DETAIL_010 | Favorite guest | Guest click favorite | Chưa đăng nhập | 1. Click favorite. | guest | Hiển thị yêu cầu đăng nhập/toast theo hook; không crash. | Medium | Permission |
| LOCATION_DETAIL_011 | Info đầy đủ | Hiển thị thông tin địa điểm | Có description/address/category | 1. Quan sát LocationInfo. | full data | Mô tả, category, địa chỉ, rating/count hiển thị đúng; rich text không raw HTML sai. | High | Functional |
| LOCATION_DETAIL_012 | Info thiếu mô tả | Description rỗng | Location thiếu description | 1. Mở detail. | empty desc | Có fallback hoặc không render block rỗng; layout ổn. | Medium | Edge Case |
| LOCATION_DETAIL_013 | Giá miễn phí | price_min = 0 | Sidebar có price | 1. Quan sát sidebar. | 0 | Hiển thị `free`/miễn phí theo translation, không `0 / undefined`. | Medium | Edge Case |
| LOCATION_DETAIL_014 | Sidebar booking CTA | Click book now | Sidebar hiển thị | 1. Click book now/contact consultancy nếu có. | | Điều hướng hoặc CTA hoạt động theo component; không dead button. | Medium | Functional |
| LOCATION_DETAIL_015 | Map link | View on map | Location có tọa độ/địa chỉ | 1. Click view_on_map. | lat/lng | Mở link bản đồ đúng tọa độ/dữ liệu map URL. | Medium | Functional |
| LOCATION_DETAIL_016 | Thiếu tọa độ | Location không có lat/lng | No coords | 1. Mở detail. | null coords | Map preview/link có fallback; không mở URL lỗi. | Medium | Edge Case |
| LOCATION_DETAIL_017 | Nearby load | Load nearby locations | API nearby có data | 1. Mở detail.<br>2. Quan sát sidebar nearby. | 6 nearby | Hiển thị tối đa 6 địa điểm gần đó; click item đi đến detail slug tương ứng. | Medium | Functional |
| LOCATION_DETAIL_018 | Nearby empty | Không có nearby | API [] | 1. Mở detail. | empty | Empty state/fallback, không render danh sách rỗng xấu. | Low | Edge Case |
| LOCATION_DETAIL_019 | Nearby error | API nearby lỗi | Mock 500 | 1. Mở detail. | 500 | Sidebar vẫn render phần chính; nearby lỗi không crash trang. | Medium | API |
| LOCATION_DETAIL_020 | Weather unavailable | Weather API không có dữ liệu | Weather error/no data | 1. Quan sát WeatherWidget. | no weather | Hiển thị `weather_unavailable`; không che sidebar. | Low | Edge Case |
| LOCATION_DETAIL_021 | Reviews load | Load đánh giá | Có reviews | 1. Cuộn đến reviews. | 10 reviews | Hiển thị điểm trung bình, count, danh sách review. | Medium | Functional |
| LOCATION_DETAIL_022 | Reviews empty | Không có reviews | count=0 | 1. Mở detail. | empty | Hiển thị `no_reviews` và subtitle. | Low | Edge Case |
| LOCATION_DETAIL_023 | Reviews error | API review lỗi | Mock 500 | 1. Cuộn reviews. | 500 | Hiển thị lỗi reviews_load_error; trang còn lại dùng được. | Medium | API |
| LOCATION_DETAIL_024 | Write review guest | Guest mở review modal | Chưa đăng nhập | 1. Click write review. | guest | Toast `login_to_review`; modal không mở hoặc bị chặn. | High | Permission |
| LOCATION_DETAIL_025 | Write review user | User viết review hợp lệ | User chưa review | 1. Click write review.<br>2. Chọn 5 sao.<br>3. Nhập comment.<br>4. Submit. | score=5 | Gọi API submit; toast success; list/refetch cập nhật. | High | Functional |
| LOCATION_DETAIL_026 | Review already rated | User đã review | hasRated true | 1. Quan sát reviews. | hasRated | Hiển thị `already_reviewed`; hạn chế submit thêm. | High | Permission |
| LOCATION_DETAIL_027 | Review images | Upload ảnh review | User mở modal | 1. Chọn ảnh.<br>2. Xóa một ảnh.<br>3. Submit. | jpg/png | Preview ảnh, remove hoạt động, payload ảnh hợp lệ. | Medium | Functional |
| LOCATION_DETAIL_028 | Helpful guest | Guest click helpful | Chưa đăng nhập | 1. Click helpful. | guest | Toast `helpful_login`; không gọi API thành công. | Medium | Permission |
| LOCATION_DETAIL_029 | Helpful user | User click helpful | User đăng nhập | 1. Click helpful trên review. | review id | API helpful gọi thành công, count cập nhật. | Medium | Functional |
| LOCATION_DETAIL_030 | Responsive | Layout mobile | 375px | 1. Mở detail.<br>2. Cuộn hết trang. | mobile | Hero, gallery, info, reviews, sidebar xếp 1 cột; không tràn ngang. | High | Responsive |

## 5. Test data đề xuất

* Location full: `ngu-hanh-son` có ảnh, tọa độ, review, nearby.
* Location thiếu dữ liệu: không ảnh, không mô tả, không tọa độ, price_min=0.
* User chưa review và user đã review.
* Review có/không có ảnh, helpful count.

## 6. Checklist regression

* Not found hoạt động đúng.
* Gallery fallback đúng khi API images rỗng/lỗi.
* Favorite/review/helpful chặn guest.
* Nearby và weather lỗi không crash trang.
* Mobile không tràn ngang.

## 7. Ghi chú kỹ thuật

* Server load từ `locations/[slug]/page.tsx`.
* Client state từ `LocationDetailClient.tsx`.
* Review logic nằm ở `LocationReviews.tsx` và `WriteReviewModal.tsx`.
* Rủi ro cao: record view spam, guest interactions, gallery fallback, map URL khi thiếu tọa độ.
