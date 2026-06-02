# Admin lịch khởi hành tour - Test Cases

## 1. Tổng quan màn hình

* Đường dẫn route: `/admin/tours/schedules`, `/admin/tours/:id/schedules/create`, `/admin/tours/schedules/edit/:id`
* File source chính: `D:\DATN\danangtrip-admin\src\pages\Tours\TourSchedules\index.tsx`, `D:\DATN\danangtrip-admin\src\pages\Tours\TourScheduleCreate\index.tsx`, `D:\DATN\danangtrip-admin\src\pages\Tours\TourScheduleEdit\index.tsx`
* Component liên quan: `ScheduleForm`, `TourInfoBox`, `SchedulePreviewBox`, `ScheduleStatsBlock`, `ScheduleInfoBox`, `TourSchedulesTable`, `ScheduleCard`, `ScheduleDeleteDialog`
* API/service sử dụng: `scheduleApi.getSchedules`, `getSchedule`, `createSchedule`, `updateSchedule`, `updateScheduleStatus`, `deleteSchedule`
* Quyền truy cập: Admin route
* Mục đích màn hình: Quản lý danh sách, tạo và sửa lịch khởi hành tour; kiểm soát ngày, số chỗ, giá, trạng thái, deadline và điểm khởi hành.

## 2. Điều kiện tiền đề

* Dữ liệu cần có: tour tồn tại; schedule available/full/cancelled; schedule có bookedSlots > 0.
* Tài khoản cần dùng: admin.
* Trạng thái hệ thống: API schedule và tour info hoạt động.
* Quyền user/admin/staff: admin theo route guard.

## 3. Danh sách chức năng chính

* Danh sách schedule với filter, calendar/table/card, pagination.
* Tạo schedule cho tour.
* Sửa schedule theo id.
* Validate ngày bắt đầu/kết thúc/deadline/số chỗ/giá.
* Không cho giảm totalSlots nhỏ hơn bookedSlots khi edit.
* Cập nhật trạng thái/xóa schedule.

## 4. Test cases chi tiết

| ID | Nhóm chức năng | Test case | Tiền điều kiện | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Mức độ ưu tiên | Loại test |
| -- | -------------- | --------- | -------------- | -------------- | ------------ | ---------------- | -------------- | --------- |
| ADMIN_SCHEDULE_001 | Permission | Guest vào schedules | Chưa login | Mở `/admin/tours/schedules`. | guest | Redirect login. | High | Permission |
| ADMIN_SCHEDULE_002 | List load | Load danh sách lịch | Có schedules | Mở `/admin/tours/schedules`. | | Stats/filter/table hoặc calendar hiển thị. | High | Functional |
| ADMIN_SCHEDULE_003 | List empty | Không có schedule | API [] | Mở list. | empty | Empty state đúng. | Medium | Edge Case |
| ADMIN_SCHEDULE_004 | List error | API list lỗi | 500 | Mở list. | 500 | Hiển thị lỗi/retry nếu component hỗ trợ, không crash. | Medium | API |
| ADMIN_SCHEDULE_005 | Filter tour | Lọc theo tour | Có nhiều tour | Chọn tour filter. | tour_id | Danh sách chỉ lịch của tour đó. | Medium | Functional |
| ADMIN_SCHEDULE_006 | Filter date | Lọc theo ngày | Có date range | Chọn start/end filter. | date range | Query gửi đúng date, list cập nhật. | Medium | Functional |
| ADMIN_SCHEDULE_007 | Create load | Mở form tạo | Tour id hợp lệ | Mở `/admin/tours/1/schedules/create`. | tour id | Form, TourInfoBox, SchedulePreviewBox hiển thị. | High | Functional |
| ADMIN_SCHEDULE_008 | Create invalid tour | Tour id sai | Không có tour | Mở create với id sai. | invalid | Hiển thị lỗi hoặc không cho submit. | High | Negative |
| ADMIN_SCHEDULE_009 | Validate start required | Bỏ trống startDate | Form tạo | Submit. | empty | Báo required start_date. | High | Validation |
| ADMIN_SCHEDULE_010 | Validate start future | StartDate quá khứ khi create | Form tạo | Chọn ngày quá khứ, submit. | yesterday | Báo `start_date_future`. | High | Validation |
| ADMIN_SCHEDULE_011 | Edit allow past start | Edit lịch cũ | isEdit=true | Mở edit schedule có start quá khứ. | past start | Schema không fail `is-future` khi edit. | Medium | Edge Case |
| ADMIN_SCHEDULE_012 | Validate end required | Bỏ trống endDate | Form | Submit. | empty | Báo required end_date. | High | Validation |
| ADMIN_SCHEDULE_013 | Validate end before start | EndDate trước startDate | Form | Nhập end < start. | start tomorrow, end today | Báo `end_date_after`. | High | Validation |
| ADMIN_SCHEDULE_014 | Validate slots required | Bỏ trống totalSlots | Form | Submit. | empty | Báo required max_people. | High | Validation |
| ADMIN_SCHEDULE_015 | Validate slots min | totalSlots < 1 | Form | Nhập 0. | 0 | Báo min_number min 1. | High | Validation |
| ADMIN_SCHEDULE_016 | Validate slots booked | Edit totalSlots < bookedSlots | Schedule bookedSlots=10 | Nhập totalSlots=5. | 5 | Báo `total_slots_min_booked`, không submit. | High | Business Rule |
| ADMIN_SCHEDULE_017 | Price adult min | Giá adult âm | Form | Nhập -1. | -1 | Báo min 0. | High | Validation |
| ADMIN_SCHEDULE_018 | Price child min | Giá child âm | Form | Nhập -1. | -1 | Báo min 0. | High | Validation |
| ADMIN_SCHEDULE_019 | Price infant min | Giá infant âm | Form | Nhập -1. | -1 | Báo min 0. | High | Validation |
| ADMIN_SCHEDULE_020 | Status required | Bỏ trống status | Form | Submit. | empty | Báo required status. | High | Validation |
| ADMIN_SCHEDULE_021 | Departure code length | Code > 50 ký tự | Form | Nhập 51 ký tự. | long | Báo max_length 50. | Medium | Validation |
| ADMIN_SCHEDULE_022 | Departure place length | Place > 255 ký tự | Form | Nhập 256 ký tự. | long | Báo max_length 255. | Medium | Validation |
| ADMIN_SCHEDULE_023 | Deadline before start | Deadline sau start | Form | Nhập deadline > start. | invalid deadline | Báo `booking_deadline_before`. | High | Validation |
| ADMIN_SCHEDULE_024 | Create success | Tạo lịch hợp lệ | Form valid | Submit. | valid | API create gọi đúng tourId/payload; toast/điều hướng đúng. | High | Functional |
| ADMIN_SCHEDULE_025 | Create API lỗi | API create 500 | Form valid | Submit. | 500 | Hiển thị lỗi, không điều hướng sai. | High | API |
| ADMIN_SCHEDULE_026 | Edit load | Mở edit schedule | ID hợp lệ | Mở `/admin/tours/schedules/edit/1`. | id | Form điền dữ liệu hiện tại, ScheduleStatsBlock/InfoBox hiển thị. | High | Functional |
| ADMIN_SCHEDULE_027 | Edit invalid id | ID sai | Không có schedule | Mở edit invalid. | invalid | Error state hoặc redirect an toàn. | High | Negative |
| ADMIN_SCHEDULE_028 | Update success | Sửa lịch hợp lệ | Form edit | Submit thay đổi. | valid | API update gọi đúng id/payload, cache invalidated. | High | Functional |
| ADMIN_SCHEDULE_029 | Update API lỗi | API update 500 | Form valid | Submit. | 500 | Không mất dữ liệu form; báo lỗi. | High | API |
| ADMIN_SCHEDULE_030 | Delete schedule | Xóa lịch | Schedule không ràng buộc | Click delete, confirm. | id | API delete thành công, list refresh. | High | Functional |
| ADMIN_SCHEDULE_031 | Delete booked | Xóa lịch có booking | bookedSlots > 0 | Confirm delete. | booked | Backend có thể chặn; UI hiển thị lỗi, không xóa sai. | High | Business Rule |
| ADMIN_SCHEDULE_032 | Status update | Cập nhật status | Schedule active | Chọn status mới. | cancelled | API update status gọi đúng, list refresh. | High | Functional |
| ADMIN_SCHEDULE_033 | Calendar view | Xem calendar | Có schedules | Chuyển calendar view. | | Lịch hiển thị đúng ngày, status/slots. | Medium | UI |
| ADMIN_SCHEDULE_034 | Responsive | Mobile/tablet | Viewport 375px | Mở list/form. | mobile | Table/card/form không tràn ngang; date inputs dùng được. | Medium | Responsive |

## 5. Test data đề xuất

* Tour id=1 active.
* Schedule future available, full, cancelled, past, bookedSlots=10.
* Form valid: start tomorrow, end after start, slots 30, prices 1000000/700000/0.

## 6. Checklist regression

* Create không cho startDate quá khứ.
* Edit không fail startDate quá khứ.
* Không giảm totalSlots dưới bookedSlots.
* Deadline không được sau startDate.
* Delete booked schedule không xóa sai.

## 7. Ghi chú kỹ thuật

* Validation lấy từ `schedule.schema.ts`.
* API lấy từ `scheduleApi.ts`.
* Rủi ro cao: rule `isEdit`, bookedSlots, timezone date, xóa lịch đã có booking.
