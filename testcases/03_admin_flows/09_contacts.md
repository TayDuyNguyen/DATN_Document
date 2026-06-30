# Admin — Quản lý Liên hệ (Contacts)

**Route:** `/admin/contacts?id=:id`  
**Source:** `danangtrip-admin/src/pages/Contacts/`  
**Automation:** `tests/admin/contacts.spec.ts` · `tests/admin/contacts-auth.spec.ts` · `tests/api/admin-contacts.api.spec.ts`  
**POM:** `ContactsPage.ts` · Mock: `tests/fixtures/api/contacts.mock.ts` · Data: `contacts-list.data.ts`  
**Chạy test:** `npm run test:admin:contacts`

---

## 1. Phạm vi

| Hạng mục | Chi tiết |
|----------|----------|
| Vai trò | **Admin** only (`PrivateRoute`) |
| API | `GET /admin/contacts` · `GET /admin/contacts/:id` · `POST .../reply` · `DELETE .../:id` · `GET .../export` |
| UI | Stats 4 card · Master list (search, tabs, pagination) · Detail panel (reply/delete) · Delete modal |
| Layout | Master-detail split; URL sync `q`, `status`, `page`, `per_page`, `id` |

## 2. UI Interactive Inventory

| # | Vùng UI | Nhãn (i18n) | Loại | Hành vi kỳ vọng | TC doc | Auto |
|---|---------|-------------|------|-----------------|--------|------|
| 1 | Breadcrumb | Xuất Excel | button | Export blob + toast | ADMIN_CONTACT_DETAIL_025 | ✅ TC_AD_CNT_023 |
| 2 | List | Tìm liên hệ... | search | Debounce 300ms → `q`, page=1, id cleared | ADMIN_CONTACT_DETAIL_009 | ✅ TC_AD_CNT_008 |
| 3 | List | Làm mới (refresh icon) | button | `refetchList` | — | manual-only |
| 4 | List tabs | Tất cả / Mới / Đã đọc / Đã trả lời | button | URL `status` + filter | ADMIN_CONTACT_DETAIL_010 | ✅ TC_AD_CNT_009 |
| 5 | List row | Contact item | click | URL `id` + detail API | ADMIN_CONTACT_DETAIL_004 | ✅ TC_AD_CNT_003 |
| 5b | List row | Xóa (icon) | button | Mở delete modal, không đổi selection | ADMIN_CONTACT_DETAIL_023 | ✅ TC_AD_CNT_031 |
| 6 | Pagination | Chevron prev/next | button | URL `page` | ADMIN_CONTACT_DETAIL_011–012 | ✅ TC_AD_CNT_010–011 |
| 7 | Detail empty | Chọn một liên hệ... | state | No `id` in URL | ADMIN_CONTACT_DETAIL_003 | ✅ TC_AD_CNT_002 |
| 8 | Detail | Xóa liên hệ | button | Mở delete modal | ADMIN_CONTACT_DETAIL_021 | ✅ TC_AD_CNT_020 |
| 9 | Reply form | Gửi trả lời | button | POST reply + toast | ADMIN_CONTACT_DETAIL_018 | ✅ TC_AD_CNT_017 |
| 10 | Delete modal | Xóa / Hủy | button | DELETE hoặc đóng | ADMIN_CONTACT_DETAIL_022 | ✅ TC_AD_CNT_021, 028 |

## 3. Data Display Integrity

| # | Vùng UI | Field API | Field UI | TC | Auto |
|---|---------|-----------|----------|-----|------|
| 1 | List row | `name`, `subject`, `message` | text preview | ADMIN_CONTACT_DETAIL_002 | ✅ TC_AD_CNT_029 |
| 2 | Detail header | `subject` | h2 truncate | ADMIN_CONTACT_DETAIL_028 | ✅ TC_AD_CNT_026 |
| 3 | Sender | `name`, `email`, `phone` | mailto/tel links | ADMIN_CONTACT_DETAIL_013–014 | ✅ TC_AD_CNT_012–013 |
| 4 | Message | `message` | whitespace-pre-wrap | ADMIN_CONTACT_DETAIL_015 | ✅ TC_AD_CNT_014 |
| 5 | Replied | `reply`, `replier.full_name` | replied panel | ADMIN_CONTACT_DETAIL_016 | ✅ TC_AD_CNT_015 |
| 6 | Stats | `stats.total/new/read/replied` | 4 stat cards | ADMIN_CONTACT_DETAIL_002 | ✅ TC_AD_CNT_029 |
| 7 | List empty | `data=[]` | list.empty | — | ✅ TC_AD_CNT_027 |
| 8 | Detail error | API 5xx | errors.detail_load_failed + retry | ADMIN_CONTACT_DETAIL_007 | ✅ TC_AD_CNT_006 |

## 4. Test cases — Auth (P0)

| ID gốc | ID Auto | Mô tả | Auto |
|--------|---------|--------|------|
| ADMIN_CONTACT_DETAIL_001 | TC_AD_CNT_040 | Guest → `/login` | ✅ |
| — | TC_AD_CNT_041 | User `role=user` → `/login` | ✅ |
| — | TC_AD_CNT_042 | Admin truy cập được | ✅ |

## 5. Test cases — Render & master-detail (P1)

| ID gốc | ID Auto | Mô tả | Auto |
|--------|---------|--------|------|
| ADMIN_CONTACT_DETAIL_002 | TC_AD_CNT_001 | Stats, search, tabs, list 10 dòng | ✅ |
| ADMIN_CONTACT_DETAIL_003 | TC_AD_CNT_002 | Detail empty state | ✅ |
| ADMIN_CONTACT_DETAIL_004 | TC_AD_CNT_003 | Chọn contact → URL `id` + detail | ✅ |
| ADMIN_CONTACT_DETAIL_005 | TC_AD_CNT_004 | Mở trực tiếp `?id=` | ✅ |
| ADMIN_CONTACT_DETAIL_006 | TC_AD_CNT_005 | Detail skeleton (delay API) | ✅ |
| ADMIN_CONTACT_DETAIL_007 | TC_AD_CNT_006 | Detail API lỗi | ✅ |
| ADMIN_CONTACT_DETAIL_008 | TC_AD_CNT_007 | List API lỗi, detail không crash | ✅ |
| ADMIN_CONTACT_DETAIL_009 | TC_AD_CNT_008 | Search debounce + clear id | ✅ |
| ADMIN_CONTACT_DETAIL_010 | TC_AD_CNT_009 | Tab status replied | ✅ |
| ADMIN_CONTACT_DETAIL_011 | TC_AD_CNT_010 | Pagination next | ✅ |
| ADMIN_CONTACT_DETAIL_012 | TC_AD_CNT_011 | Next disabled ở trang cuối | ✅ |
| ADMIN_CONTACT_DETAIL_027 | TC_AD_CNT_025 | URL `q` sync input | ✅ |
| ADMIN_CONTACT_DETAIL_028 | TC_AD_CNT_026 | Subject dài truncate | ✅ |
| — | TC_AD_CNT_027 | List empty state | ✅ |
| — | TC_AD_CNT_029 | Data display list + detail + stats | ✅ |

## 6. Test cases — Reply & Delete (P0–P1)

| ID gốc | ID Auto | Mô tả | Auto |
|--------|---------|--------|------|
| ADMIN_CONTACT_DETAIL_013 | TC_AD_CNT_012 | Email + phone links | ✅ |
| ADMIN_CONTACT_DETAIL_014 | TC_AD_CNT_013 | Không phone → không tel link | ✅ |
| ADMIN_CONTACT_DETAIL_015 | TC_AD_CNT_014 | Message multiline | ✅ |
| ADMIN_CONTACT_DETAIL_016 | TC_AD_CNT_015 | Lịch sử replied | ✅ |
| ADMIN_CONTACT_DETAIL_017 | TC_AD_CNT_016 | ReplyForm khi new/read | ✅ |
| ADMIN_CONTACT_DETAIL_018 | TC_AD_CNT_017 | Gửi reply hợp lệ | ✅ |
| ADMIN_CONTACT_DETAIL_019 | TC_AD_CNT_018 | Reply rỗng → validation | ✅ |
| ADMIN_CONTACT_DETAIL_020 | TC_AD_CNT_019 | Reply API lỗi | ✅ |
| ADMIN_CONTACT_DETAIL_021 | TC_AD_CNT_020 | Mở delete dialog | ✅ |
| ADMIN_CONTACT_DETAIL_022 | TC_AD_CNT_021 | Xóa contact đang chọn | ✅ |
| ADMIN_CONTACT_DETAIL_023 | TC_AD_CNT_031 | Xóa contact không active (từ list) | ✅ |
| ADMIN_CONTACT_DETAIL_024 | TC_AD_CNT_022 | Delete API lỗi | ✅ |
| — | TC_AD_CNT_028 | Hủy delete không gọi API | ✅ |

## 7. Test cases — Export & regression (P1)

| ID gốc | ID Auto | Mô tả | Auto |
|--------|---------|--------|------|
| ADMIN_CONTACT_DETAIL_025 | TC_AD_CNT_023 | Export Excel + toast | ✅ |
| ADMIN_CONTACT_DETAIL_026 | TC_AD_CNT_024 | Export API lỗi | ✅ |
| ADMIN_CONTACT_DETAIL_030 | TC_AD_CNT_030 | Flow search → select → reply | ✅ |
| ADMIN_CONTACT_DETAIL_029 | — | Responsive 768/375 | manual-only |

## 8. API tests

| ID | Mô tả | Auto |
|----|--------|------|
| API_CNT_001 | GET list không auth → 401 | ✅ |
| API_CNT_002 | GET list admin paginated | ✅ (skip nếu API off) |
| API_CNT_003 | GET list filter status=new | ✅ (skip nếu API off) |

## 9. Test data mock

| Record | Mục đích |
|--------|----------|
| `primaryNewContact` (id 1) | Search, select, reply |
| `readContactWithPhone` (id 2) | Phone + mailto |
| `repliedContact` (id 3) | Replied history |
| `noPhoneContact` (id 4) | Không SĐT |
| `multilineContact` (id 5) | Message nhiều dòng |
| `longSubjectContact` (id 6) | Subject dài |
| `deletableContact` (id 7) | Delete tests |
| ids 11–12 | Pagination page 2 |

**Stats kỳ vọng:** total 12 · new 5 · read 5 · replied 2 (theo dataset mock).

## 10. Checklist regression

- [x] URL query q/status/page/id đồng bộ (tab/page clear `id`)
- [x] List/stats/detail error panel + retry
- [x] Detail empty/loading/error
- [x] Reply ẩn với contact replied
- [x] Delete selected → clear id
- [x] Export giữ filter
- [ ] Responsive split panel (manual)

## 11. Đề xuất cải thiện (PHASE 0.8)

| ID | Loại | Severity | Phát hiện | Đề xuất | Trạng thái |
|----|------|----------|-----------|---------|------------|
| IMP_CNT_001 | UX | P2 | List lỗi không có nút retry | Thêm retry giống Promotions/Ratings | **fixed** |
| IMP_CNT_002 | UX | P2 | Detail error hiển thị duplicate network_error | Title + mô tả khác nhau | **fixed** |
| IMP_CNT_003 | UX | P2 | Stats lỗi chỉ hiện text đỏ, không retry | Error panel + refetch | **fixed** |
| IMP_CNT_004 | UX | P3 | Tab đổi status không reset `id` | Clear selection khi đổi tab | **fixed** |
| IMP_CNT_005 | Test | P3 | ADMIN_CONTACT_DETAIL_023 không khả thi trên UI hiện tại | Nút xóa trên list row | **fixed** |

**Trạng thái automation:** **37/37 passed** (`npm run test:admin:contacts`, 2026-06-23)

## 12. Ghi chú kỹ thuật

- Master-detail + URL state trong `Contacts/index.tsx`.
- Chọn contact `new` → optimistic mark read trong cache list.
- Reply validation: min 10 ký tự (`ReplyForm` + yup).
- Mock pathname list: regex `/admin/contacts/?$` (không match `/export` hay `/:id`).
