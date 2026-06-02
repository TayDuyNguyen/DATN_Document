# Admin quản lý đánh giá - Test Cases

## 1. Tổng quan màn hình

* Đường dẫn route: `/admin/ratings`
* File source chính: `D:\DATN\danangtrip-admin\src\pages\Ratings\index.tsx`
* Component liên quan: `RatingStatsCards`, `RatingFilterBar`, `RatingTable`, `RejectRatingDialog`, `RatingDeleteDialog`
* API/service sử dụng: `useRatingsReportQuery`, `useAdminRatingsListQuery`, `approveMutation`, `rejectMutation`, `deleteMutation`, `exportMutation`
* Quyền truy cập: Admin route
* Mục đích màn hình: Quản lý danh sách đánh giá, lọc/tìm kiếm, duyệt, ẩn/từ chối, xóa đơn lẻ/hàng loạt và xuất Excel.

## 2. Điều kiện tiền đề

* Dữ liệu cần có: rating pending/approved/rejected; rating location/tour; nhiều rating để bulk.
* Tài khoản cần dùng: admin.
* Trạng thái hệ thống: API report/list/mutations/export hoạt động.
* Quyền user/admin/staff: admin theo route guard.

## 3. Danh sách chức năng chính

* Load KPI report và list ratings song song.
* Filter status/type/search/page/per_page/date/location/tour.
* Select all/current page, bulk reject, bulk delete.
* Approve individual rating.
* Reject individual hoặc bulk với lý do.
* Delete individual hoặc bulk.
* Export Excel theo filter.

## 4. Test cases chi tiết

| ID | Nhóm chức năng | Test case | Tiền điều kiện | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Mức độ ưu tiên | Loại test |
| -- | -------------- | --------- | -------------- | -------------- | ------------ | ---------------- | -------------- | --------- |
| ADMIN_RATING_001 | Permission | Guest vào route | Chưa login | Mở `/admin/ratings`. | guest | Redirect login. | High | Permission |
| ADMIN_RATING_002 | Load data | Load ratings | Có data | Mở route. | | Stats, filter, table hiển thị. | High | Functional |
| ADMIN_RATING_003 | Stats loading | Report loading | API delay | Mở route. | delay | StatsCards loading, table có thể load riêng. | Medium | UI |
| ADMIN_RATING_004 | List loading | List loading | API delay | Mở route. | delay | Table loading state hiển thị. | Medium | UI |
| ADMIN_RATING_005 | Empty list | Không có rating | API items=[] | Mở route/filter không match. | empty | Empty state table đúng. | Medium | Edge Case |
| ADMIN_RATING_006 | Filter status | Lọc pending/approved/rejected | Có nhiều status | Chọn status pending. | pending | Query list/report theo status, page reset nếu filter bar xử lý. | Medium | Functional |
| ADMIN_RATING_007 | Filter type | Lọc tour/location | Có rating hai loại | Chọn type tour. | tour | Chỉ hiển thị rating tour. | Medium | Functional |
| ADMIN_RATING_008 | Search | Tìm kiếm rating/user | Có data khớp | Nhập search. | keyword | List cập nhật đúng search. | Medium | Functional |
| ADMIN_RATING_009 | Reset filter | Reset filter | Đã lọc | Click reset. | | Filters về all/search empty/page 1, selectedIds clear, toast success. | Medium | Functional |
| ADMIN_RATING_010 | Pagination | Đổi page/limit | total > limit | Click page 2, đổi per_page. | limit 20 | Query cập nhật page/limit, list đúng. | Low | Functional |
| ADMIN_RATING_011 | Select one | Chọn một rating | List có data | Tick một dòng. | id | selectedIds chứa id. | Medium | Functional |
| ADMIN_RATING_012 | Select all | Chọn tất cả trang hiện tại | List có data | Tick select all. | page items | selectedIds gồm id của các item trang hiện tại. | Medium | Functional |
| ADMIN_RATING_013 | Unselect all | Bỏ chọn tất cả trang | selected all | Bỏ tick select all. | | selectedIds loại bỏ ids trang hiện tại. | Low | Functional |
| ADMIN_RATING_014 | Approve | Duyệt rating pending | Rating pending | Click approve. | id | approveMutation gọi, refetch report/list. | High | Functional |
| ADMIN_RATING_015 | Approve API lỗi | Approve lỗi | Mock 500 | Click approve. | 500 | Mutation lỗi, không cập nhật sai. | High | API |
| ADMIN_RATING_016 | Reject open | Mở dialog reject | Rating pending/approved | Click reject. | item | Dialog mở với rating item. | High | Functional |
| ADMIN_RATING_017 | Reject reason | Reject hợp lệ | Dialog mở | Nhập reason, submit. | reason | rejectMutation gọi id/rejected_reason, selectedIds bỏ id, refetch. | High | Functional |
| ADMIN_RATING_018 | Reject empty | Reason rỗng | Dialog mở | Submit rỗng. | empty | Dialog validation chặn hoặc không gọi API. | High | Validation |
| ADMIN_RATING_019 | Reject API lỗi | Reject lỗi | Mock 500 | Submit reason. | 500 | Hiển thị lỗi/toast promise, dialog không cập nhật sai. | High | API |
| ADMIN_RATING_020 | Bulk reject open | Mở bulk reject | selectedIds > 0 | Click bulk reject. | 3 ids | Dialog bulk hiển thị selectedCount. | High | Functional |
| ADMIN_RATING_021 | Bulk reject success | Reject hàng loạt | selectedIds > 0 | Nhập reason, submit. | 3 ids | Promise.all gọi từng id, toast success count, selectedIds clear, refetch. | High | Functional |
| ADMIN_RATING_022 | Bulk reject partial error | Một request lỗi | selectedIds > 1 | Submit bulk. | one 500 | Toast error, isBulkLoading false, cần kiểm tra trạng thái các item đã xử lý. | High | Edge Case |
| ADMIN_RATING_023 | Delete open | Mở delete individual | Rating item | Click delete. | id | RatingDeleteDialog mở với userName. | High | Functional |
| ADMIN_RATING_024 | Delete confirm | Xóa individual | Dialog mở | Confirm. | id | deleteMutation gọi, selectedIds bỏ id, refetch. | High | Functional |
| ADMIN_RATING_025 | Delete API lỗi | Xóa lỗi | Mock 500 | Confirm. | 500 | Không xóa sai; dialog/error xử lý. | High | API |
| ADMIN_RATING_026 | Bulk delete open | Mở bulk delete | selectedIds > 0 | Click bulk delete. | 3 ids | Modal bulk delete hiển thị count. | High | Functional |
| ADMIN_RATING_027 | Bulk delete confirm | Xóa hàng loạt | Modal mở | Confirm. | 3 ids | Promise.all delete, toast success count, selectedIds clear, modal đóng, refetch. | High | Functional |
| ADMIN_RATING_028 | Bulk delete backdrop | Đóng bulk delete bằng backdrop | Modal mở | Click backdrop. | | Modal đóng, selectedIds giữ nguyên. | Low | UI |
| ADMIN_RATING_029 | Export | Xuất Excel | Có data/filter | Click export. | filters | exportMutation gọi không kèm page/per_page, filename đúng ngày, toast success. | Medium | Functional |
| ADMIN_RATING_030 | Export API lỗi | Export lỗi | Mock 500 | Click export. | 500 | Toast export_failed. | Medium | API |
| ADMIN_RATING_031 | Mutating disabled | Khi mutation pending | Approve/reject/delete pending | Click action khác. | pending | isMutating disable action trong table/dialog nếu component hỗ trợ. | Medium | Regression |
| ADMIN_RATING_032 | Long content | Review dài | Rating content dài | Mở list. | long | Table không vỡ layout; text truncate/wrap hợp lý. | Low | UI |
| ADMIN_RATING_033 | Rating photos | Rating có ảnh | item có photos | Quan sát row/detail nếu có. | photos | Ảnh/indicator hiển thị đúng nếu table hỗ trợ. | Low | UI |
| ADMIN_RATING_034 | Responsive | Mobile/tablet | 375/768 | Mở route. | mobile | Filter/table/actions dùng được hoặc có scroll ngang có kiểm soát. | Medium | Responsive |

## 5. Test data đề xuất

* Rating pending, approved, rejected.
* Rating type tour và location.
* Nhiều rating cùng trang để bulk.
* Review dài, userName dài, có/không ảnh.

## 6. Checklist regression

* Approve/reject/delete refetch cả stats và list.
* Bulk action clear selection sau success.
* Export không gửi page/per_page.
* Reset filter clear selectedIds.
* Partial failure bulk được tester ghi nhận.

## 7. Ghi chú kỹ thuật

* Logic từ `Ratings/index.tsx`.
* Rủi ro cao: bulk Promise.all partial success, selectedIds giữ qua pagination/filter, export filter mapping.
