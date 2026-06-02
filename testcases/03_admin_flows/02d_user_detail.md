# Admin chi tiết người dùng - Test Cases

## 1. Tổng quan màn hình

* Đường dẫn route: `/admin/users/detail/:id`
* File source chính: `D:\DATN\danangtrip-admin\src\pages\Users\UserDetail\index.tsx`
* Component liên quan: `UserDetailHeader`, `PersonalInfoCard`, `UserBookingsTable`, `UserRatingsList`, `UserStatsCards`, `UserAccountSidebar`, `UserActionsCard`, `ChangeRoleDialog`, `ConfirmDeleteUserDialog`
* API/service sử dụng: `userApi.getDetail`, user bookings/ratings queries, user role/status/delete mutations
* Quyền truy cập: Admin qua `PrivateRoute`
* Mục đích màn hình: Cho admin xem hồ sơ người dùng, thống kê, booking/rating gần đây và thực hiện khóa/mở khóa, đổi vai trò, xóa tài khoản.

## 2. Điều kiện tiền đề

* Dữ liệu cần có: user active, user banned, user có booking/rating/favorite/spend; current admin.
* Tài khoản cần dùng: admin đang đăng nhập; user thường để test guard.
* Trạng thái hệ thống: API user detail/bookings/ratings và mutations hoạt động.
* Quyền user/admin/staff: admin được thao tác; self-protection khi xem chính mình.

## 3. Danh sách chức năng chính

* Load user detail theo id.
* Load booking gần đây và rating gần đây.
* Hiển thị stats bookings/reviews/favorites/totalSpend.
* Toggle status active/banned.
* Đổi role admin/user bằng dialog.
* Xóa user bằng confirm dialog.
* Error/not found và loading state.
* Self check để hạn chế thao tác nguy hiểm.

## 4. Test cases chi tiết

| ID | Nhóm chức năng | Test case | Tiền điều kiện | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Mức độ ưu tiên | Loại test |
| -- | -------------- | --------- | -------------- | -------------- | ------------ | ---------------- | -------------- | --------- |
| ADMIN_USER_DETAIL_001 | Permission | Guest truy cập | Chưa login | Mở `/admin/users/detail/1`. | guest | Redirect login. | High | Permission |
| ADMIN_USER_DETAIL_002 | Permission | User thường truy cập | role user | Mở route detail. | user | Bị chặn bởi PrivateRoute. | High | Permission |
| ADMIN_USER_DETAIL_003 | Load dữ liệu | Mở user hợp lệ | User tồn tại | Mở `/admin/users/detail/10`. | id=10 | Header, info, bookings, ratings, stats, sidebar, actions hiển thị. | High | Functional |
| ADMIN_USER_DETAIL_004 | Loading | Spinner khi đang tải | API delay | Mở detail. | delay | Spinner và loading text hiển thị. | Medium | UI |
| ADMIN_USER_DETAIL_005 | Not found | User không tồn tại | ID sai | Mở `/admin/users/detail/999999`. | invalid | Card không tìm thấy và nút quay lại danh sách. | High | Negative |
| ADMIN_USER_DETAIL_006 | Personal info | Thông tin cá nhân đầy đủ | User full data | Quan sát PersonalInfoCard. | full | Họ tên, email, phone, role, status, created date đúng. | High | Functional |
| ADMIN_USER_DETAIL_007 | Missing avatar | User không avatar | avatar null | Mở detail. | null | Fallback avatar/initial không vỡ layout. | Low | Edge Case |
| ADMIN_USER_DETAIL_008 | Missing phone | User không phone | phone null | Mở detail. | null | Fallback phù hợp, không undefined. | Low | Edge Case |
| ADMIN_USER_DETAIL_009 | Stats | Thống kê user | User có bookings/reviews/favorites/spend | Quan sát UserStatsCards. | counts | Số liệu đúng format, totalSpend đúng tiền. | High | Functional |
| ADMIN_USER_DETAIL_010 | Stats zero | User mới chưa hoạt động | counts 0 | Mở detail. | zero | Hiển thị 0, không NaN/blank. | Medium | Edge Case |
| ADMIN_USER_DETAIL_011 | Bookings list | Booking gần đây | User có >5 bookings | Quan sát UserBookingsTable. | 10 bookings | Hiển thị 5 booking gần đây và totalCount đúng. | Medium | Functional |
| ADMIN_USER_DETAIL_012 | Bookings empty | User chưa booking | bookings=[] | Mở detail. | empty | Empty/loading state đúng. | Low | Edge Case |
| ADMIN_USER_DETAIL_013 | Ratings list | Rating gần đây | User có ratings | Quan sát UserRatingsList. | 5 ratings | Hiển thị tối đa 3 rating và total đúng. | Medium | Functional |
| ADMIN_USER_DETAIL_014 | Ratings empty | User chưa rating | ratings=[] | Mở detail. | empty | Empty state đúng. | Low | Edge Case |
| ADMIN_USER_DETAIL_015 | Toggle ban | Khóa user active | User khác current admin | Click khóa tài khoản. | active | Gọi mutation status `banned`, toast thành công, refetch. | High | Functional |
| ADMIN_USER_DETAIL_016 | Toggle unban | Mở khóa user banned | User banned | Click mở khóa. | banned | Gọi mutation status `active`, toast thành công, refetch. | High | Functional |
| ADMIN_USER_DETAIL_017 | Status API lỗi | Khóa/mở khóa lỗi | API 500 | Click action. | 500 | Toast lỗi mapApiErrorMessage, status không đổi sai. | High | API |
| ADMIN_USER_DETAIL_018 | Change role open | Mở dialog đổi role | User khác admin hiện tại | Click đổi vai trò. | role user | Dialog mở với role hiện tại. | Medium | Functional |
| ADMIN_USER_DETAIL_019 | Change role submit | Đổi role user -> admin | Dialog mở | Chọn admin và confirm. | admin | Mutation gọi đúng; toast success; dialog đóng; refetch. | High | Functional |
| ADMIN_USER_DETAIL_020 | Change role API lỗi | Đổi role thất bại | API 500 | Submit role. | 500 | Toast lỗi, dialog không cập nhật sai. | High | API |
| ADMIN_USER_DETAIL_021 | Self protection | Xem chính admin đang login | currentAdmin.id === id | Mở detail chính mình. | self | Action nguy hiểm bị disable/ẩn theo `isSelf`; không tự khóa/xóa/đổi role sai. | High | Permission |
| ADMIN_USER_DETAIL_022 | Delete open | Mở confirm delete | User khác current admin | Click delete. | | Confirm dialog hiển thị tên user. | High | Functional |
| ADMIN_USER_DETAIL_023 | Delete confirm | Xóa user | Dialog mở | Confirm delete. | id | Mutation delete gọi; toast success; điều hướng `/admin/users`. | High | Functional |
| ADMIN_USER_DETAIL_024 | Delete API lỗi | Xóa thất bại | API 500 | Confirm delete. | 500 | Toast lỗi; dialog xử lý đúng, không điều hướng sai. | High | API |
| ADMIN_USER_DETAIL_025 | Long name/email | Dữ liệu dài | User name/email dài | Mở detail. | long strings | Header/card truncate/wrap hợp lý, không tràn layout. | Medium | Edge Case |
| ADMIN_USER_DETAIL_026 | Refetch after mutation | Cache cập nhật sau status/role | Mutation success | Thực hiện status/role. | | Detail query refetch, thông tin mới xuất hiện. | Medium | Regression |
| ADMIN_USER_DETAIL_027 | Responsive | Layout mobile | Viewport 375px | Mở detail. | mobile | Grid chuyển 1 cột, actions dùng được. | Medium | Responsive |
| ADMIN_USER_DETAIL_028 | Sticky sidebar | Sidebar desktop | 1440px | Cuộn trang. | desktop | Sidebar sticky top-24, không che content. | Low | UI |
| ADMIN_USER_DETAIL_029 | Booking link | Click booking trong table | User có booking | Click xem booking nếu có. | booking id | Điều hướng admin booking detail đúng route nếu component hỗ trợ. | Medium | Functional |
| ADMIN_USER_DETAIL_030 | Regression | Full thao tác user | User test riêng | Ban -> unban -> đổi role -> delete. | test user | Mỗi mutation thành công, toast đúng, không ảnh hưởng current admin. | High | Regression |

## 5. Test data đề xuất

* User active có booking/rating/favorite/spend.
* User banned.
* User mới không booking/rating.
* Current admin để test self-protection.

## 6. Checklist regression

* Route chỉ admin truy cập.
* Self-protection không bị mất.
* Status/role/delete mutation refetch đúng.
* Booking/rating list không vỡ khi rỗng.
* Mobile layout không tràn.

## 7. Ghi chú kỹ thuật

* Logic từ `UserDetail/index.tsx`.
* Rủi ro cao: tự khóa/xóa admin hiện tại, cache sau mutation, long text trong header/sidebar.
