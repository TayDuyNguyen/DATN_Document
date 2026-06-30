# Admin — Quản lý & Gửi Thông báo (Notifications)

**Route:** `/admin/notifications` · `/admin/notifications/send`  
**Source:** `danangtrip-admin/src/pages/Notifications/`  
**Automation:** `tests/admin/notifications-list.spec.ts` · `notifications-send.spec.ts` · `notifications-auth.spec.ts`  
**POM:** `NotificationListPage.ts` · `NotificationSendPage.ts` · Mock: `notifications.mock.ts` · Data: `notifications.data.ts`  
**Chạy test:** `npm run test:admin:notifications` — **28/28 passed** (2026-06-23)

---

## 1. Phạm vi

| Hạng mục | Chi tiết |
|----------|----------|
| Vai trò | Admin |
| API list | `GET /admin/notifications` · `DELETE /admin/notifications/:id` |
| API send | `POST /admin/notifications/send` · `POST /admin/notifications/send-all` |
| UI list | Stats (total/read/unread) · Filter (search/type/read/user) · Table · Pagination · Delete · Bulk delete |
| UI send | Mode individual/bulk · Recipient search · Preview · Optional link · Bulk confirm dialog |

**Lưu ý audit:** Doc gốc ghi cột "Người gửi" — UI thực tế **không có** cột sender; bảng gồm Recipient, Content, Type, Time, Read, Actions.

---

## 2. UI Interactive Inventory (PHASE 0.6)

| # | Vùng UI | Nhãn (i18n) | Loại | Hành vi kỳ vọng | TC Auto | Auto |
|---|---------|-------------|------|-----------------|---------|------|
| 1 | Header | Gửi thông báo / Send Notification | button | → `/admin/notifications/send` | TC_AD_NOTIF_007 | ✅ |
| 2 | Stats | Tổng / Đã đọc / Chưa đọc | cards | Số liệu từ `stats` API | TC_AD_NOTIF_001 | ✅ |
| 3 | Filter | Tìm theo tiêu đề, nội dung | input | Debounce 300ms → `?q=` | TC_AD_NOTIF_003, 003b | ✅ partial |
| 4 | Filter | Loại / Type | select | `?type=` | TC_AD_NOTIF_004 | ✅ |
| 5 | Filter | Trạng thái đọc | select | `?is_read=` | TC_AD_NOTIF_005 | ✅ |
| 6 | Filter | Người nhận | select | `?user_id=` | — | manual |
| 7 | Filter | Đặt lại / Reset | button | Xóa query params | TC_AD_NOTIF_006 | ✅ |
| 8 | Table | Checkbox row / header | checkbox | Chọn bulk delete | TC_AD_NOTIF_014 | ✅ |
| 9 | Table | Sort Time | columnheader | `sort_by=created_at` | — | manual |
| 10 | Table | Delete | button | Mở dialog → DELETE API | TC_AD_NOTIF_012, 013 | ✅ |
| 11 | Table | Bulk delete | button | `window.confirm` → DELETE nhiều | TC_AD_NOTIF_014 | ✅ |
| 12 | Pagination | Page / per_page | buttons | `?page=` | TC_AD_NOTIF_009 | ✅ |
| 13 | Send | Gửi cá nhân / Gửi hàng loạt | toggle | Đổi mode form | TC_AD_NOTIF_022 | ✅ |
| 14 | Send | Tiêu đề / Nội dung | input | Required | TC_AD_NOTIF_002 | ✅ |
| 15 | Send | Người nhận | search | Infinite user list | TC_AD_NOTIF_002b, 004 | ✅ |
| 16 | Send | Link đích (optional) | input | URL validation | TC_AD_NOTIF_020 | ✅ |
| 17 | Send | Preview | panel | Mirror title/content | TC_AD_NOTIF_023 | ✅ |
| 18 | Send | Hủy | button | → list | TC_AD_NOTIF_021 | ✅ |
| 19 | Send | Gửi thông báo | submit | POST send / send-all | TC_AD_NOTIF_003, 004 | ✅ |
| 20 | Send | Bulk confirm dialog | dialog | Confirm / Cancel | TC_AD_NOTIF_024 | ✅ |

---

## 3. Data Display Integrity (PHASE 0.7)

| # | Field API | Field UI | TC | Auto |
|---|-----------|----------|-----|------|
| 1 | `title`, `content` | Content column | TC_AD_NOTIF_001b | ✅ |
| 2 | `user.email`, `user.full_name` | Recipient | TC_AD_NOTIF_001b | ✅ |
| 3 | `type` | Type badge | TC_AD_NOTIF_001b | ✅ |
| 4 | `created_at` | Time column | TC_AD_NOTIF_001b | ✅ partial |
| 5 | `is_read` | Read badge/icon | TC_AD_NOTIF_001b | ✅ partial |
| 6 | `stats.total/read/unread` | Stats row | TC_AD_NOTIF_001 | ✅ |

---

## 4. Test cases — Doc gốc → Auto mapping

| Doc ID | ID Auto | Mô tả | Auto |
|--------|---------|--------|------|
| TC_AD_NOTIF_001 | TC_AD_NOTIF_001, 001b | Danh sách + hiển thị field API | ✅ |
| TC_AD_NOTIF_002 | TC_AD_NOTIF_002, 002b | Validate title/content/recipient | ✅ |
| TC_AD_NOTIF_003 *(bulk send doc)* | TC_AD_NOTIF_003 *(send spec)* | Gửi hàng loạt + confirm | ✅ |
| TC_AD_NOTIF_004 *(individual doc)* | TC_AD_NOTIF_004 *(send spec)* | Gửi cá nhân | ✅ |
| — | TC_AD_NOTIF_003 *(list)* | Lọc search qua `?q=` + API `search` | ✅ |
| — | TC_AD_NOTIF_003b | Debounce sync keyword → URL `q` | ✅ |

---

## 5. Test cases — Auth (P0)

| ID Auto | Mô tả | Auto |
|---------|--------|------|
| TC_AD_NOTIF_040 | Guest → `/login` | ✅ |
| TC_AD_NOTIF_041 | User `role=user` → `/login` | ✅ |
| TC_AD_NOTIF_042 | Admin vào list | ✅ |

---

## 6. Test cases — List (P1)

| ID Auto | Mô tả | Auto |
|---------|--------|------|
| TC_AD_NOTIF_001 | Heading, stats, filters, columns | ✅ |
| TC_AD_NOTIF_001b | Row fields từ API | ✅ |
| TC_AD_NOTIF_003 | Filter search (`?q=` → API `search`) | ✅ |
| TC_AD_NOTIF_003b | UI debounce → URL `q` | ✅ |
| TC_AD_NOTIF_004 | Filter type=system | ✅ |
| TC_AD_NOTIF_005 | Filter unread | ✅ |
| TC_AD_NOTIF_006 | Reset filters | ✅ |
| TC_AD_NOTIF_007 | Nút Gửi → send page | ✅ |
| TC_AD_NOTIF_009 | Pagination page 2 | ✅ |
| TC_AD_NOTIF_010 | Empty list API | ✅ |
| TC_AD_NOTIF_011 | Loading delay | ✅ |
| TC_AD_NOTIF_012 | Delete + confirm | ✅ |
| TC_AD_NOTIF_013 | Cancel delete dialog | ✅ |
| TC_AD_NOTIF_014 | Bulk delete + confirm | ✅ |

---

## 7. Test cases — Send (P1)

| ID Auto | Mô tả | Auto |
|---------|--------|------|
| TC_AD_NOTIF_002 | Empty title + content validation | ✅ |
| TC_AD_NOTIF_002b | Missing recipient (individual) | ✅ |
| TC_AD_NOTIF_003 | Bulk send success + toast | ✅ |
| TC_AD_NOTIF_004 | Individual send success + toast | ✅ |
| TC_AD_NOTIF_020 | Invalid optional link | ✅ |
| TC_AD_NOTIF_021 | Cancel → list | ✅ |
| TC_AD_NOTIF_022 | Switch individual/bulk | ✅ |
| TC_AD_NOTIF_023 | Preview reflects input | ✅ |
| TC_AD_NOTIF_024 | Bulk confirm cancel (no API) | ✅ |
| TC_AD_NOTIF_025 | Individual send API 500 | ✅ |
| TC_AD_NOTIF_026 | Bulk send API 500 | ✅ |

---

## 8. Improvement Backlog (PHASE 0.8)

| ID | Loại | Mô tả | Trạng thái |
|----|------|--------|------------|
| IMP_NOTIF_001 | Doc | Doc gốc ghi cột "Người gửi" — UI không có (API không có field sender) | **fixed** — cập nhật doc audit |
| IMP_NOTIF_002 | UX | Bulk delete dùng `window.confirm` thay vì dialog thống nhất | **fixed** |
| IMP_NOTIF_003 | Bug | Debounce search cập nhật `?q=` nhưng chưa refetch API | **fixed** — primitive queryKey + `urlSearchKey` + `staleTime: 0` |
| IMP_NOTIF_004 | UX | FilterBar debounce pattern RatingFilterBar | **fixed** |
| IMP_NOTIF_005 | UX | Stats nhãn khi có filter active (`*_filtered`) | **fixed** |
| IMP_NOTIF_006 | UX | Filter user searchable (infinite scroll) thay dropdown 50 user | **fixed** |
| IMP_NOTIF_007 | UX | Tag filter user hiển thị tên/email | **fixed** |
| IMP_NOTIF_008 | Code | Bulk delete `Promise.allSettled` + toast partial | **fixed** |
| IMP_NOTIF_009 | Code | `mapApiErrorMessage` cho delete errors | **fixed** |

---

## 9. Ghi chú kỹ thuật automation

- Mock list filter dùng query param `search` (axios map từ `q`).
- `TC_AD_NOTIF_003` list: search UI + assert API `search` (IMP_NOTIF_003 fixed).
- Toast bulk success regex: `Đã gửi đến tất cả.*thành công` (tránh match text cảnh báo bulk trên form).
- Bulk delete dùng dialog `data-testid=notification-bulk-delete-dialog` (không `window.confirm`).
