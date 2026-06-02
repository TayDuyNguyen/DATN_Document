# Admin chi tiết địa điểm - Test Cases

## 1. Tổng quan màn hình

* Đường dẫn route: `/admin/locations/detail/:id`
* File source chính: `D:\DATN\danangtrip-admin\src\pages\Locations\LocationDetail\index.tsx`
* Component liên quan: `DetailHeader`, `DetailHero`, `DetailTabs`, `LocationInfoTab`, `LocationReviewsTab`, `LocationMapTab`, `DetailSidebar`, `DeleteLocationModal`
* API/service sử dụng: `locationApi.getDetail(id)`, update featured/status/delete location mutations
* Quyền truy cập: Admin qua `PrivateRoute`; management/danger zone chỉ hiển thị khi `user.role === 'admin'`
* Mục đích màn hình: Cho admin xem chi tiết địa điểm, tab thông tin/review/map, thống kê view/favorite và quản trị status/featured/delete.

## 2. Điều kiện tiền đề

* Dữ liệu cần có: location active/inactive, có ảnh/toạ độ/reviews/view/favorite; location thiếu ảnh/toạ độ.
* Tài khoản cần dùng: admin; staff/non-admin nếu có để test ẩn management.
* Trạng thái hệ thống: API location detail/reviews/status/featured/delete hoạt động.
* Quyền user/admin/staff: admin thao tác quản trị; non-admin chỉ xem nếu vào được layout.

## 3. Danh sách chức năng chính

* Load detail theo id, skeleton và error widget.
* Hiển thị hero media/header.
* Chuyển tab info/reviews/map.
* Hiển thị sidebar stats view/favorite.
* Admin đổi status active/inactive, toggle featured, xóa location.
* Điều hướng back/list/edit từ header nếu component hỗ trợ.

## 4. Test cases chi tiết

| ID | Nhóm chức năng | Test case | Tiền điều kiện | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Mức độ ưu tiên | Loại test |
| -- | -------------- | --------- | -------------- | -------------- | ------------ | ---------------- | -------------- | --------- |
| ADMIN_LOCATION_DETAIL_001 | Permission | Guest vào route | Chưa login | Mở `/admin/locations/detail/1`. | guest | Redirect login. | High | Permission |
| ADMIN_LOCATION_DETAIL_002 | Load dữ liệu | Admin mở location hợp lệ | Location tồn tại | Mở route detail. | id=1 | Header, hero, tabs, sidebar hiển thị. | High | Functional |
| ADMIN_LOCATION_DETAIL_003 | Loading | Skeleton khi API chậm | Delay API | Mở route. | delay | `LocationDetailSkeleton` hiển thị. | Medium | UI |
| ADMIN_LOCATION_DETAIL_004 | Error | ID không tồn tại | ID sai | Mở `/admin/locations/detail/999999`. | invalid | ErrorWidget hiển thị Retry và Back về list. | High | Negative |
| ADMIN_LOCATION_DETAIL_005 | Retry | Retry sau lỗi | API lỗi rồi hồi phục | Click Retry. | 500->200 | Refetch và render data. | Medium | API |
| ADMIN_LOCATION_DETAIL_006 | Header | Header tên/id | Location full | Quan sát DetailHeader. | full | Tên/id đúng, action header không lỗi. | Medium | UI |
| ADMIN_LOCATION_DETAIL_007 | Hero có ảnh | DetailHero media | Có ảnh | Quan sát hero. | image | Ảnh hiển thị đúng, không méo. | Medium | UI |
| ADMIN_LOCATION_DETAIL_008 | Hero thiếu ảnh | Không có ảnh | image null | Mở detail. | null | Fallback hợp lý, không vỡ layout. | Medium | Edge Case |
| ADMIN_LOCATION_DETAIL_009 | Tab info | Mở tab info | Detail loaded | Click tab Info. | | `LocationInfoTab` hiển thị mô tả/danh mục/thông tin. | High | Functional |
| ADMIN_LOCATION_DETAIL_010 | Info rich text | Mô tả HTML | Location có HTML | Quan sát info. | HTML | Render đúng, không raw HTML sai. | Medium | UI |
| ADMIN_LOCATION_DETAIL_011 | Info thiếu data | Thiếu mô tả/category | Partial data | Mở tab info. | null fields | Fallback đúng, không undefined/NaN. | Medium | Edge Case |
| ADMIN_LOCATION_DETAIL_012 | Tab reviews | Mở tab reviews | Có review | Click Reviews. | reviews | Review list/load state hiển thị. | Medium | Functional |
| ADMIN_LOCATION_DETAIL_013 | Reviews empty | Không có review | empty | Click Reviews. | [] | Empty state đúng. | Low | Edge Case |
| ADMIN_LOCATION_DETAIL_014 | Reviews API lỗi | Review API lỗi | Mock 500 | Click Reviews. | 500 | Lỗi review không crash toàn detail. | Medium | API |
| ADMIN_LOCATION_DETAIL_015 | Tab map | Mở tab map | Có tọa độ | Click Map. | lat/lng | Map/preview hiển thị đúng tọa độ. | Medium | Functional |
| ADMIN_LOCATION_DETAIL_016 | Map thiếu tọa độ | Không có tọa độ | lat/lng null | Click Map. | null | Fallback/empty map, không lỗi. | Medium | Edge Case |
| ADMIN_LOCATION_DETAIL_017 | Stats | View/favorite count | Có count | Quan sát sidebar. | counts | Count format đúng, không NaN. | Medium | UI |
| ADMIN_LOCATION_DETAIL_018 | Stats zero | Count bằng 0 | 0 | Mở detail. | 0 | Hiển thị 0 đúng. | Low | Edge Case |
| ADMIN_LOCATION_DETAIL_019 | Management visible | Admin thấy management | role admin | Quan sát sidebar. | admin | Card status/featured/tip/danger zone hiển thị. | High | Permission |
| ADMIN_LOCATION_DETAIL_020 | Management hidden | Non-admin không thấy management | role khác admin | Mở detail. | staff | Management/danger zone không hiển thị. | High | Permission |
| ADMIN_LOCATION_DETAIL_021 | Change status active | Đổi inactive -> active | Admin, location inactive | Chọn active trong CustomSelect. | active | Bulk action gọi đúng id/action, control disabled khi updating. | High | Functional |
| ADMIN_LOCATION_DETAIL_022 | Change status inactive | Đổi active -> inactive | Admin, location active | Chọn inactive. | inactive | API gọi đúng, UI cập nhật sau query/list. | High | Functional |
| ADMIN_LOCATION_DETAIL_023 | Status API lỗi | Đổi status lỗi | API 500 | Chọn status. | 500 | Control hết disabled, không đổi UI sai. | High | API |
| ADMIN_LOCATION_DETAIL_024 | Toggle featured on | Bật featured | Admin | Click toggle. | true | Gọi update featured `{id,isFeatured:true}`. | Medium | Functional |
| ADMIN_LOCATION_DETAIL_025 | Toggle featured off | Tắt featured | Admin | Click toggle. | false | Gọi update featured false; UI cập nhật. | Medium | Functional |
| ADMIN_LOCATION_DETAIL_026 | Featured API lỗi | Toggle lỗi | API 500 | Click toggle. | 500 | Không kẹt toggle/pending; có thể refetch. | Medium | API |
| ADMIN_LOCATION_DETAIL_027 | Delete open | Mở modal xóa | Admin | Click Delete. | | Modal hiển thị tên location. | High | Functional |
| ADMIN_LOCATION_DETAIL_028 | Delete confirm | Xóa thành công | Admin, location không ràng buộc | Confirm. | id | API delete; modal đóng; điều hướng `/admin/locations`. | High | Functional |
| ADMIN_LOCATION_DETAIL_029 | Delete API lỗi | Xóa thất bại | API 500/ràng buộc | Confirm. | 500 | Không điều hướng sai; modal/error xử lý đúng. | High | API |
| ADMIN_LOCATION_DETAIL_030 | Responsive | Mobile layout | 375px | Mở detail. | mobile | Grid 1 cột, tabs không tràn, sidebar dưới content. | Medium | Responsive |

## 5. Test data đề xuất

* Location active full, inactive full, không ảnh, không tọa độ, count 0.
* Admin role và non-admin role.
* Review list có dữ liệu và rỗng.

## 6. Checklist regression

* ErrorWidget Back/Retry hoạt động.
* Tabs info/reviews/map không mất state.
* Management chỉ hiển thị admin.
* Status/featured/delete không cập nhật sai khi API lỗi.
* Mobile tabs không tràn.

## 7. Ghi chú kỹ thuật

* Logic từ `LocationDetail/index.tsx`, `DetailTabs.tsx`, `DetailSidebar.tsx`.
* Rủi ro cao: quyền management, map thiếu tọa độ, bulk status dùng action string.
