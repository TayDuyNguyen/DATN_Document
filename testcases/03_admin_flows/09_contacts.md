# Admin chi tiết liên hệ - Test Cases

## 1. Tổng quan màn hình

* Đường dẫn route: `/admin/contacts?id=:id`
* File source chính: `D:\DATN\danangtrip-admin\src\pages\Contacts\index.tsx`
* Component liên quan: `ContactDetailPanel`, `ContactListItem`, `ReplyForm`, `DeleteContactDialog`, `ContactStatsRow`
* API/service sử dụng: `contactApi.getList`, `contactApi.getDetail`, `contactApi.reply`, `contactApi.delete`, `contactApi.export`
* Quyền truy cập: Admin route
* Mục đích màn hình: Quản lý liên hệ theo master-detail, xem nội dung yêu cầu, trả lời, xóa và export.

## 2. Điều kiện tiền đề

* Dữ liệu cần có: contact status new/read/replied; contact có/không có phone; contact đã reply.
* Tài khoản cần dùng: admin.
* Trạng thái hệ thống: API contact list/detail/reply/delete/export hoạt động.
* Quyền user/admin/staff: admin theo route guard.

## 3. Danh sách chức năng chính

* Đồng bộ search/status/page/per_page/id qua URL query.
* Master list search debounce 300ms, tab status, pagination.
* Detail panel loading/error/empty.
* Hiển thị subject, status, sender, email, phone, message.
* Reply contact nếu chưa replied; hiển thị lịch sử reply nếu đã replied.
* Delete contact, export contacts.

## 4. Test cases chi tiết

| ID | Nhóm chức năng | Test case | Tiền điều kiện | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Mức độ ưu tiên | Loại test |
| -- | -------------- | --------- | -------------- | -------------- | ------------ | ---------------- | -------------- | --------- |
| ADMIN_CONTACT_DETAIL_001 | Permission | Guest vào contacts | Chưa login | Mở `/admin/contacts`. | guest | Redirect login. | High | Permission |
| ADMIN_CONTACT_DETAIL_002 | List load | Load danh sách | Có contacts | Mở contacts. | | Stats, search, tabs, list hiển thị. | High | Functional |
| ADMIN_CONTACT_DETAIL_003 | Empty detail | Chưa chọn contact | selectedId rỗng | Mở `/admin/contacts`. | no id | Detail panel empty_state_title/subtitle hiển thị. | Medium | UI |
| ADMIN_CONTACT_DETAIL_004 | Select detail | Chọn contact | Có list data | Click một contact. | id | URL có `id`, detail API gọi và panel hiển thị. | High | Functional |
| ADMIN_CONTACT_DETAIL_005 | Direct id | Mở trực tiếp có id | Contact tồn tại | Mở `/admin/contacts?id=10`. | id=10 | Detail panel load đúng contact. | High | Functional |
| ADMIN_CONTACT_DETAIL_006 | Detail loading | API detail chậm | Delay | Chọn contact. | delay | Skeleton trong panel hiển thị. | Medium | UI |
| ADMIN_CONTACT_DETAIL_007 | Detail error | API detail lỗi | Mock 500 | Chọn contact. | 500 | Panel error hiển thị network_error. | High | API |
| ADMIN_CONTACT_DETAIL_008 | List error | API list lỗi | Mock 500 | Mở contacts. | 500 | Left panel hiển thị network_error; detail không crash. | Medium | API |
| ADMIN_CONTACT_DETAIL_009 | Search debounce | Tìm kiếm liên hệ | Có contacts | Nhập keyword. | `Nguyen` | Sau 300ms URL q cập nhật, page=1, id cleared. | Medium | Functional |
| ADMIN_CONTACT_DETAIL_010 | Status tab | Lọc status | Có new/read/replied | Click tab replied. | replied | URL status cập nhật, list lọc đúng. | Medium | Functional |
| ADMIN_CONTACT_DETAIL_011 | Pagination next | Trang tiếp | totalPages > 1 | Click next. | page 1 | URL page tăng, list cập nhật. | Low | Functional |
| ADMIN_CONTACT_DETAIL_012 | Pagination disabled | Trang cuối | page=last | Click next. | last | Button disabled, không tăng page. | Low | UI |
| ADMIN_CONTACT_DETAIL_013 | Sender info | Contact có phone | Detail loaded | Quan sát sender card. | phone | Name, email mailto, phone tel hiển thị. | Medium | UI |
| ADMIN_CONTACT_DETAIL_014 | No phone | Contact không phone | phone null | Mở detail. | null | Không render phone link, layout vẫn đẹp. | Low | Edge Case |
| ADMIN_CONTACT_DETAIL_015 | Message whitespace | Message nhiều dòng | Contact message multiline | Quan sát message. | multiline | `whitespace-pre-wrap` giữ xuống dòng. | Medium | UI |
| ADMIN_CONTACT_DETAIL_016 | Replied history | Contact status replied | replied data | Mở detail. | reply | Hiển thị replied title, replied_by_meta, reply content, success email note. | High | Functional |
| ADMIN_CONTACT_DETAIL_017 | Reply form visible | Contact chưa replied | status new/read | Mở detail. | new | ReplyForm hiển thị. | High | Functional |
| ADMIN_CONTACT_DETAIL_018 | Reply submit | Gửi reply hợp lệ | Contact chưa replied | Nhập reply và submit. | reply text | API reply gọi, toast success. | High | Functional |
| ADMIN_CONTACT_DETAIL_019 | Reply empty | Reply rỗng | Form mở | Submit rỗng. | empty | Validation form chặn hoặc không gọi API. | High | Validation |
| ADMIN_CONTACT_DETAIL_020 | Reply API lỗi | API reply lỗi | Mock 500 | Submit reply. | 500 | Toast network_error, form không kẹt loading. | High | API |
| ADMIN_CONTACT_DETAIL_021 | Delete open | Mở dialog xóa | Detail loaded | Click delete. | id | DeleteContactDialog hiển thị tên contact. | High | Functional |
| ADMIN_CONTACT_DETAIL_022 | Delete selected | Xóa contact đang chọn | Dialog mở | Confirm. | selected id | API delete, toast success, URL id cleared, page=1. | High | Functional |
| ADMIN_CONTACT_DETAIL_023 | Delete unselected | Xóa contact không active | deleteTarget khác selectedId | Confirm. | id khác | Selection giữ nguyên nếu active không bị xóa. | Medium | Edge Case |
| ADMIN_CONTACT_DETAIL_024 | Delete API lỗi | Xóa thất bại | Mock 500 | Confirm. | 500 | Toast network_error, dialog đóng theo source, không clear sai. | High | API |
| ADMIN_CONTACT_DETAIL_025 | Export | Xuất contacts | Có data | Click export. | filters | API export gọi với q/status hiện tại, filename fallback theo ngày, toast success. | Medium | Functional |
| ADMIN_CONTACT_DETAIL_026 | Export error | Export lỗi | Mock 500 | Click export. | 500 | Toast network_error. | Medium | API |
| ADMIN_CONTACT_DETAIL_027 | URL sync q | URL q đổi ngoài input | Query param q thay đổi | Set URL `?q=A`. | q=A | searchInput đồng bộ với q. | Low | Regression |
| ADMIN_CONTACT_DETAIL_028 | Long subject | Subject dài | Contact subject dài | Mở detail. | long | Header truncate, không tràn nút delete. | Low | UI |
| ADMIN_CONTACT_DETAIL_029 | Responsive | Split panel mobile/tablet | Viewport 768/375 | Mở contacts. | mobile | Master-detail không tràn nghiêm trọng; nếu thiết kế desktop-only cần ghi nhận rủi ro. | Medium | Responsive |
| ADMIN_CONTACT_DETAIL_030 | Regression | Search -> select -> reply -> delete | Contact test | Thực hiện full flow. | | URL/filter/detail/action cập nhật đúng, không mất state bất ngờ. | High | Regression |

## 5. Test data đề xuất

* Contact new/read/replied.
* Contact có phone và không phone.
* Contact message nhiều dòng, subject dài.
* Reply hợp lệ và reply rỗng.

## 6. Checklist regression

* URL query q/status/page/id đồng bộ đúng.
* Detail empty/loading/error rõ ràng.
* Reply không hiển thị cho contact đã replied.
* Delete selected contact clear id.
* Export giữ filter hiện tại.

## 7. Ghi chú kỹ thuật

* Logic master-detail nằm trong `Contacts/index.tsx`.
* Detail panel nằm trong `ContactDetailPanel.tsx`.
* Rủi ro cao: responsive split panel, URL state phức tạp, reply validation phụ thuộc `ReplyForm`.
