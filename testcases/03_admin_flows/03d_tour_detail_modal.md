# Admin modal chi tiết tour - Test Cases

## 1. Tổng quan màn hình

* Đường dẫn route: `/admin/tours/list` mở modal qua action xem chi tiết
* File source chính: `D:\DATN\danangtrip-admin\src\pages\Tours\TourList\components\TourDetailModal.tsx`
* Component liên quan: `TourList`, `TourTable`, `StatusBadge`, `BookingAvailabilityBadge`, schedules preview
* API/service sử dụng: `useTourDetailModalSchedules(tour?.id, isOpen)`, tour list mutations/actions
* Quyền truy cập: Admin route
* Mục đích màn hình: Xem nhanh chi tiết tour trong modal, gồm ảnh, giá, duration, meeting point, mô tả, itinerary và lịch khởi hành gần đây.

## 2. Điều kiện tiền đề

* Dữ liệu cần có: tour có/không có thumbnail, gallery, itinerary, schedules available/full/cancelled.
* Tài khoản cần dùng: admin.
* Trạng thái hệ thống: API danh sách tour và schedules preview hoạt động.
* Quyền user/admin/staff: chỉ admin theo admin route guard.

## 3. Danh sách chức năng chính

* Mở/đóng modal từ TourList.
* Hiển thị header tour, mã tour, status, booking availability.
* Hiển thị thumbnail/gallery, giá, duration, max people, meeting point, hot/featured.
* Hiển thị description HTML, itinerary.
* Load schedules preview, error retry, empty state.
* Điều hướng edit từ modal.

## 4. Test cases chi tiết

| ID | Nhóm chức năng | Test case | Tiền điều kiện | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Mức độ ưu tiên | Loại test |
| -- | -------------- | --------- | -------------- | -------------- | ------------ | ---------------- | -------------- | --------- |
| ADMIN_TOUR_MODAL_001 | Mở modal | Click xem chi tiết tour | Tour list có data | 1. Mở `/admin/tours/list`.<br>2. Click action view. | tour id | Modal overlay mở, title là tên tour. | High | Functional |
| ADMIN_TOUR_MODAL_002 | Đóng modal X | Đóng bằng nút X | Modal mở | Click X. | | Modal đóng, list/filter state còn nguyên. | Medium | Functional |
| ADMIN_TOUR_MODAL_003 | Đóng modal footer | Đóng bằng nút close cuối modal | Modal mở | Click Close. | | Modal đóng đúng. | Low | Functional |
| ADMIN_TOUR_MODAL_004 | Header badges | Hiển thị status/availability | Tour có status | Quan sát header. | active/full | StatusBadge và BookingAvailabilityBadge đúng. | Medium | UI |
| ADMIN_TOUR_MODAL_005 | Tour code | Mã tour pad 3 chữ số | Tour id=7 | Mở modal. | id=7 | Hiển thị prefix + `007`. | Low | UI |
| ADMIN_TOUR_MODAL_006 | Thumbnail | Tour có thumbnail | thumbnail URL | Quan sát media. | URL | Ảnh aspect video hiển thị đúng. | Medium | UI |
| ADMIN_TOUR_MODAL_007 | No thumbnail | Tour thiếu thumbnail | null | Mở modal. | null | Fallback ImageOff/no data hiển thị. | Medium | Edge Case |
| ADMIN_TOUR_MODAL_008 | Gallery | Tour có nhiều images | images > 4 | Quan sát gallery. | 6 images | Chỉ hiển thị 4 ảnh đầu, không tràn. | Low | UI |
| ADMIN_TOUR_MODAL_009 | Price format | Format giá người lớn | price_adult | Mở modal. | 1500000 | Giá format theo locale và kèm currency. | Medium | UI |
| ADMIN_TOUR_MODAL_010 | Price zero | Giá bằng 0 | price_adult=0 | Mở modal. | 0 | Hiển thị 0 đúng, không NaN. | Medium | Edge Case |
| ADMIN_TOUR_MODAL_011 | Duration | Hiển thị duration | duration có data | Mở modal. | `2N1Đ` | Duration đúng; thiếu thì `no_data`. | Low | UI |
| ADMIN_TOUR_MODAL_012 | Max people | Hiển thị max people | max_people có data | Mở modal. | 30 | Hiển thị số người và unit. | Low | UI |
| ADMIN_TOUR_MODAL_013 | Meeting point | Hiển thị điểm hẹn | meeting_point dài | Mở modal. | long text | Text truncate/wrap hợp lý. | Low | UI |
| ADMIN_TOUR_MODAL_014 | Featured/hot | Badge hot/featured | is_hot/is_featured true | Mở modal. | true | Badge hiển thị đúng; false không hiển thị. | Low | UI |
| ADMIN_TOUR_MODAL_015 | Description HTML | Mô tả HTML | description có HTML | Cuộn description. | HTML | HTML render đúng bằng dangerouslySetInnerHTML. | Medium | UI |
| ADMIN_TOUR_MODAL_016 | No description | Thiếu mô tả | description null | Mở modal. | null | Hiển thị `no_data`. | Low | Edge Case |
| ADMIN_TOUR_MODAL_017 | Itinerary | Lịch trình có dữ liệu | itinerary array | Cuộn itinerary. | 3 ngày | Hiển thị day/title/content theo timeline. | Medium | Functional |
| ADMIN_TOUR_MODAL_018 | No itinerary | Itinerary rỗng | [] | Mở modal. | empty | Empty state với icon Map và no schedule. | Low | Edge Case |
| ADMIN_TOUR_MODAL_019 | Schedules loading | Load schedules preview | API delay | Mở modal. | delay | Loading schedules hiển thị. | Medium | API |
| ADMIN_TOUR_MODAL_020 | Schedules data | Có schedules | API trả list | Mở modal. | schedules | Hiển thị start-end date, booked/total slots, status. | Medium | Functional |
| ADMIN_TOUR_MODAL_021 | Schedules empty | Không có schedules | [] | Mở modal. | empty | Empty state schedules no_data. | Low | Edge Case |
| ADMIN_TOUR_MODAL_022 | Schedules error | API schedules lỗi | 500 | Mở modal. | 500 | Alert lỗi và nút retry hiển thị. | Medium | API |
| ADMIN_TOUR_MODAL_023 | Retry schedules | Retry sau lỗi | Alert lỗi | Click retry. | 500->200 | Refetch schedules và hiển thị list. | Medium | API |
| ADMIN_TOUR_MODAL_024 | Edit action | Click edit | Modal mở | Click Edit. | id | Modal đóng và điều hướng `/admin/tours/edit/:id`. | High | Functional |
| ADMIN_TOUR_MODAL_025 | Responsive | Modal mobile | Viewport 375px | Mở modal. | mobile | Modal vừa màn, scroll trong modal hoạt động, header actions không tràn. | Medium | Responsive |

## 5. Test data đề xuất

* Tour full với thumbnail, 6 images, description HTML, 3 itinerary, schedules.
* Tour thiếu thumbnail/description/itinerary/schedules.
* Schedules available/full/cancelled.

## 6. Checklist regression

* Modal mở/đóng không mất state list.
* Edit điều hướng đúng.
* Schedules preview không crash khi lỗi.
* Giá và slots không NaN.
* Mobile modal scroll được.

## 7. Ghi chú kỹ thuật

* Modal không có route riêng; mở từ `TourList`.
* Rủi ro cao: `dangerouslySetInnerHTML`, schedules query chỉ enabled khi modal mở, layout modal mobile.
