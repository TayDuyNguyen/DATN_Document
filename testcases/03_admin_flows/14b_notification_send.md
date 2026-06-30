# Admin — Gửi Thông báo (Notification Send)



**Route:** `/admin/notifications/send`  

**Source:** `danangtrip-admin/src/pages/Notifications/NotificationSend/`  

**Components:** `NotificationSendForm`, `NotificationPreview`, `RecipientSelector`, `BulkConfirmDialog`  

**API:**

- `POST /admin/notifications` (gửi cá nhân — `user_id`, `type`, `title`, `content`, `data?`)

- `POST /admin/notifications/send-all` (gửi hàng loạt)

- `GET /admin/users` (đếm `totalUserCount` cho bulk preview)



---



## 1. Phạm vi



| Hạng mục | Chi tiết |

|----------|----------|

| Vai trò | **Admin** |

| Chế độ gửi | **Individual** (1 user) · **Bulk** (tất cả user active) |

| Validation | `title` required max 100 · `content` required max 500 · `data` link tùy chọn (`https://` hoặc `/`) |

| Preview | Sidebar live preview theo form values |

| Bulk safety | Dialog xác nhận trước khi `send-all` |



## 2. Điều kiện tiên quyết



- Admin đã đăng nhập

- Có ≥1 user trong hệ thống để chọn recipient (individual) hoặc đếm bulk

- List notifications (`/admin/notifications`) hoạt động để quay lại



## 3. Test cases — Navigation (P0)



| ID | Mô tả | Auto |

|----|--------|------|

| TC_AD_NOTIF_SEND_001 | Guest `/admin/notifications/send` → `/login` | ✅ |

| TC_AD_NOTIF_SEND_002 | Breadcrumb: Notifications → Gửi thông báo | ✅ |

| TC_AD_NOTIF_SEND_003 | Nút Cancel → navigate `/admin/notifications` | ✅ |

| TC_AD_NOTIF_SEND_004 | Từ list notifications click "Gửi mới" → mở send page | ✅ |



## 4. Form — Validation (P0)



| ID | Mô tả | Auto |

|----|--------|------|

| TC_AD_NOTIF_SEND_010 | Submit trống title → lỗi `title_required` | ✅ |

| TC_AD_NOTIF_SEND_011 | Submit trống content → lỗi `content_required` | ✅ |

| TC_AD_NOTIF_SEND_012 | Title > 100 ký tự → lỗi `title_max` | ✅ |

| TC_AD_NOTIF_SEND_013 | Content > 500 ký tự → lỗi `content_max` | ✅ |

| TC_AD_NOTIF_SEND_014 | Link `data` không hợp lệ (vd: `abc`) → `data_invalid_link` | ✅ |

| TC_AD_NOTIF_SEND_015 | Link hợp lệ `https://...` hoặc `/tours` → pass validation | ✅ |

| TC_AD_NOTIF_SEND_016 | Individual mode chưa chọn user → `recipientError`, không gọi API | ✅ |



## 5. Chế độ Individual (P1)



| ID | Mô tả | Auto |

|----|--------|------|

| TC_AD_NOTIF_SEND_020 | Chọn type: system / booking / promotion / rating | ✅ |

| TC_AD_NOTIF_SEND_021 | RecipientSelector tìm user theo email/tên | ✅ |

| TC_AD_NOTIF_SEND_022 | Chọn user → preview hiển thị tên/email recipient | ✅ |

| TC_AD_NOTIF_SEND_023 | Gửi thành công → toast `send_individual_success`, form reset | ✅ |

| TC_AD_NOTIF_SEND_024 | Payload API gồm `user_id`, `type`, `title`, `content`; `data.url` nếu có link | ✅ |

| TC_AD_NOTIF_SEND_025 | API lỗi → toast `send_failed`, form giữ dữ liệu | ✅ |

| TC_AD_NOTIF_SEND_026 | Đang submit → nút disabled, label `btn_sending` | ✅ |



## 6. Chế độ Bulk (P1)



| ID | Mô tả | Auto |

|----|--------|------|

| TC_AD_NOTIF_SEND_030 | Chuyển mode Bulk → ẩn RecipientSelector, preview hiện tổng user | ✅ |

| TC_AD_NOTIF_SEND_031 | `totalUserCount` lấy từ `GET /admin/users?page=1&per_page=1` meta.total | ✅ |

| TC_AD_NOTIF_SEND_032 | Submit bulk → mở BulkConfirmDialog, chưa gọi API | ✅ |

| TC_AD_NOTIF_SEND_033 | Dialog hiển thị số người nhận = `totalUserCount` | ✅ |

| TC_AD_NOTIF_SEND_034 | Confirm bulk → `POST send-all` + toast success kèm count | ✅ |

| TC_AD_NOTIF_SEND_035 | Hủy dialog → đóng, không gọi API | ✅ |

| TC_AD_NOTIF_SEND_036 | Bulk API lỗi → toast error, dialog đóng | ✅ |

| TC_AD_NOTIF_SEND_037 | Success bulk → form reset (`resetSignal` clear fields) | ✅ |



## 7. Live Preview (P1)



| ID | Mô tả | Auto |

|----|--------|------|

| TC_AD_NOTIF_SEND_040 | Gõ title/content → preview cập nhật realtime | ✅ |

| TC_AD_NOTIF_SEND_041 | Đổi type → preview đổi icon/màu theo loại | ✅ |

| TC_AD_NOTIF_SEND_042 | Individual: preview hiện tên user đã chọn | ✅ |

| TC_AD_NOTIF_SEND_043 | Bulk: preview hiện "Gửi tới X người dùng" | ✅ |

| TC_AD_NOTIF_SEND_044 | Title/content trống → preview placeholder | ✅ |



## 8. UI phụ (P2)



| ID | Mô tả | Auto |

|----|--------|------|

| TC_AD_NOTIF_SEND_050 | Collapse/expand trường Data (link) tùy chọn | ✅ |

| TC_AD_NOTIF_SEND_051 | Guide card 4 mục hướng dẫn hiển thị | ✅ |

| TC_AD_NOTIF_SEND_052 | Mobile: footer submit/cancel riêng (md:hidden) | ✅ |

| TC_AD_NOTIF_SEND_053 | Header actions Submit gắn `form="notification-send-form"` | ✅ |

| TC_AD_NOTIF_SEND_054 | Responsive: form 65% + sidebar 35% trên desktop | ✅ |



## 9. API contract (P2)



| ID | Mô tả | Auto |

|----|--------|------|

| API_NOTIF_SEND_001 | POST individual không auth → 401 | ⏳ manual-only (backend contract) |

| API_NOTIF_SEND_002 | POST individual thiếu `user_id` → 422 | ⏳ manual-only (backend contract) |

| API_NOTIF_SEND_003 | POST send-all admin → 200 | ✅ (via TC_AD_NOTIF_SEND_034 mock) |

| API_NOTIF_SEND_004 | POST send-all không auth → 401 | ⏳ manual-only (backend contract) |



---



## 10. Ghi chú



- File `14_notifications.md` cover danh sách + TC cơ bản gửi; file này chi tiết hóa màn **Send** riêng.

- `data` field: chỉ gửi lên API khi có link hợp lệ, dạng `{ url: string }`.

- Bulk confirm bắt buộc — không có shortcut gửi all không qua dialog.
- Gửi thành công → toast + **redirect** `/admin/notifications`.
- Bulk chỉ gửi tới **user active**; count lấy từ `GET /admin/users?status=active`.



## 11. Checklist regression



- Validation title/content/link

- Individual cần chọn user

- Bulk qua confirm dialog

- Preview sync form

- Success reset form + toast



## 12. Automation



| File | Mục đích |

|------|----------|

| `tests/pages/admin/NotificationSendPage.ts` | POM send |

| `tests/admin/notifications-send.spec.ts` | 35 TC send (14b) |

| `tests/admin/notifications-auth.spec.ts` | TC_AD_NOTIF_SEND_001 auth |

| `tests/fixtures/api/notifications.mock.ts` | Mock send / send-all |



**Script:** `npm run test:admin:notifications` — **53/53 passed** (list 15 + send 35 + auth 4)



**Trạng thái automation:** 39 TC ✅ · 3 TC ⏳ manual-only (API contract backend)

