# Admin — Dashboard (Trang chủ quản trị)

**Route:** `/dashboard`  
**Source:** `danangtrip-admin/src/pages/Dashboard/`  
**Automation:** `tests/admin/dashboard.spec.ts` · `tests/admin/dashboard-auth.spec.ts` · `tests/api/admin-dashboard.api.spec.ts`  
**POM:** `DashboardPage.ts`

---

## 1. Phạm vi

- Vai trò: **Admin** (`PrivateRoute` — không có Staff)
- API:
  - `GET /admin/dashboard/stats`
  - `GET /admin/bookings/status-counts`
  - `GET /admin/dashboard/revenue`
  - `GET /admin/dashboard/booking-trend`
  - `GET /admin/dashboard/user-growth`
  - `GET /admin/dashboard/top-tours`
  - `GET /admin/dashboard/search-trends`
  - `GET /admin/bookings` (bảng đơn gần đây)
  - `GET /admin/dashboard/export`
  - `GET /admin/dashboard/notification-counts`
- URL query: `revenue_period`, `trend_days`, `page`, `status`

## 2. Điều kiện tiên quyết

- Admin đã đăng nhập · dev server `:5173`
- Mock: `mockDashboardApi` · data: `tests/fixtures/data/dashboard.data.ts`

## 3. Test cases — Auth & routing (P0)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_DASH_007 | Guest `/dashboard` → `/login` | ✅ |
| TC_AD_DASH_008 | User `role=user` → `/login` | ✅ |
| TC_AD_DASH_009 | Welcome heading có `full_name` admin | ✅ |
| TC_AD_DASH_010 | Reload giữ session | ⏳ |

## 4. Header actions (P1)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_DASH_011 | Export báo cáo → blob + toast success | ✅ |
| TC_AD_DASH_012 | Export API lỗi → toast error | ⏳ |
| TC_AD_DASH_013 | Refresh toàn trang → refetch stats | ✅ |
| TC_AD_DASH_014 | Subtitle / aria dashboard | ⏳ |

## 5. Stats cards — 6 thẻ (P1)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_DASH_015 | 6 card `dashboard-stat-*` visible | ✅ |
| TC_AD_DASH_016 | Revenue đúng mock + trend % | ✅ |
| TC_AD_DASH_017 | Orders = tổng 4 status counts | ✅ |
| TC_AD_DASH_018 | Users + Tours sold + trend | ✅ |
| TC_AD_DASH_019 | Pending orders + New contacts | ✅ |
| TC_AD_DASH_020 | Stats API 500 → error card | ⏳ |
| TC_AD_DASH_021 | Status-counts API 500 → orders/pending error | ⏳ |

## 6. Charts — 4 widget (P1)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_DASH_022 | Revenue mặc định `revenue_period=day` | ⏳ |
| TC_AD_DASH_023 | Đổi period Week → URL + refetch | ✅ |
| TC_AD_DASH_024 | Badge tổng revenue khớp mock | ⏳ |
| TC_AD_DASH_025 | Refresh riêng revenue chart | ⏳ |
| TC_AD_DASH_026 | Revenue empty → empty state | ⏳ |
| TC_AD_DASH_027 | Revenue error + retry | ⏳ |
| TC_AD_DASH_028 | Booking trend 7/30/90 ngày → URL | ✅ |
| TC_AD_DASH_029 | Subtitle tổng đơn trend | ⏳ |
| TC_AD_DASH_030 | Trend empty / error | ⏳ |
| TC_AD_DASH_031 | User growth 12 tháng render | ⏳ |
| TC_AD_DASH_032 | Badge tổng user mới | ⏳ |
| TC_AD_DASH_033 | User growth empty / error | ⏳ |
| TC_AD_DASH_034 | Order status 4 cột đúng count | ⏳ |
| TC_AD_DASH_035 | Tổng badge = sum status (khớp stats orders) | ⏳ |
| TC_AD_DASH_036 | All zero → empty | ⏳ |

## 7. Search trends panel (P1)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_DASH_037 | Keywords: text + count | ✅ |
| TC_AD_DASH_038 | Clicked queries text + count | ✅ |
| TC_AD_DASH_039 | Zero-result keywords | ⏳ |
| TC_AD_DASH_040 | Trending tour/location badge | ⏳ |
| TC_AD_DASH_041 | Panel empty | ⏳ |
| TC_AD_DASH_042 | View all → `/admin/locations` | ⏳ |
| TC_AD_DASH_042b | Error + retry | ⏳ |

## 8. Top tours table (P1)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_DASH_043 | Hiển thị title mock | ✅ |
| TC_AD_DASH_045 | Click row → `/admin/tours/edit/:id` | ✅ |
| TC_AD_DASH_046 | Revenue / rating formatted | ⏳ |
| TC_AD_DASH_047 | View all → tour list | ⏳ |
| TC_AD_DASH_047b | Empty / error | ⏳ |

## 9. Recent orders (P1) — mở rộng doc cũ 004/005

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_DASH_048 | Bảng 8 dòng/trang, cột đủ | ✅ |
| TC_AD_DASH_049 | Data display: code, KH, tour, tiền, status | ✅ |
| TC_AD_DASH_050 | Customer/tour trống → N/A | ⏳ |
| TC_AD_DASH_051 | Filter status → URL `status` + API | ✅ |
| TC_AD_DASH_052 | Filter reset page=1 | ⏳ |
| TC_AD_DASH_053 | Pagination → URL `page` | ✅ |
| TC_AD_DASH_054 | Click row → booking detail | ✅ |
| TC_AD_DASH_055 | View all / Manage orders → bookings | ✅ |
| TC_AD_DASH_056 | Empty state | ⏳ |
| TC_AD_DASH_057 | API error + retry | ⏳ |

## 10. Sidebar navigation (P1) — mở rộng doc cũ 001

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_DASH_058 | Dashboard active | ⏳ |
| TC_AD_DASH_059 | Tours submenu → list | ✅ |
| TC_AD_DASH_060 | Locations submenu | ⏳ |
| TC_AD_DASH_061 | Bookings top-level | ✅ |
| TC_AD_DASH_062 | Payments, Ratings | ⏳ |
| TC_AD_DASH_063 | Reports submenu (5 routes) | ⏳ |
| TC_AD_DASH_064 | Blog, Users, Notifications, Contacts, Chatbot, Settings, Promotions, Landing | ⏳ |
| TC_AD_DASH_065 | Collapse sidebar | ✅ |
| TC_AD_DASH_066 | Logout → login | ⏳ |

## 11. Notification bell (P1) — mở rộng doc cũ 006

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_DASH_067 | Mở popover | ✅ |
| TC_AD_DASH_068 | Badge `total_unread` | ✅ |
| TC_AD_DASH_069 | Contacts → `/admin/contacts?status=new` | ✅ |
| TC_AD_DASH_070 | Bookings → `/admin/bookings?status=pending` | ✅ |
| TC_AD_DASH_071 | Ratings → `/admin/ratings?is_new=1` | ⏳ |
| TC_AD_DASH_072 | Open management → notifications | ⏳ |
| TC_AD_DASH_073 | Đóng X / outside / Escape | ⏳ |
| TC_AD_DASH_074 | notification-counts API lỗi | ⏳ |

## 12. Global search (P2)

Quick search header — gọi song song tours / users / bookings / locations / blog. **Search không phân biệt hoa thường** trên PostgreSQL (tours/users/locations/blog đã có; bookings fix `ilike` 2026-06).

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_DASH_076 | Gõ keyword → dropdown nhóm | ✅ |
| TC_AD_DASH_077 | Chọn kết quả → navigate | ✅ |
| TC_AD_DASH_078 | Phím `/` focus search | ✅ |
| TC_AD_DASH_079 | Không có kết quả | ✅ |
| TC_AD_DASH_080 | Arrow + Enter | ✅ |
| TC_AD_DASH_092 | Tour keyword `BA NA` → cùng kết quả `ba na` | ✅ |
| TC_AD_DASH_093 | Booking code `bk-...` → khớp `BK-...` | ✅ |
| API_DASH_011 | `GET /admin/bookings?search=` case-insensitive | ✅ |

## 13. Language & layout phụ (P2)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_DASH_081 | Đổi EN ↔ VI labels | ⏳ |
| TC_AD_DASH_082 | Control Panel drawer mở | ⏳ |
| TC_AD_DASH_083 | Profile / Quick settings tabs | ⏳ |
| TC_AD_DASH_084 | Font size preference save | ⏳ |
| TC_AD_DASH_085 | Footer copyright | ⏳ |

## 14. URL state (P2)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_DASH_086 | Deep link query giữ sau reload | ⏳ |
| TC_AD_DASH_087 | `revenue_period` invalid → fallback day | ⏳ |
| TC_AD_DASH_088 | `trend_days` invalid → fallback 30 | ⏳ |

## 15. Negative / edge (P3)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_DASH_089 | Tất cả widget API 500 — không crash | ⏳ |
| TC_AD_DASH_090 | Legacy revenue shape mapper | ⏳ |
| TC_AD_DASH_091 | Pagination 1 trang — prev disabled | ⏳ |
| TC_AD_DASH_092 | Mobile viewport scroll bảng | ⏳ |

## 16. API contract (P2)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_DASH_API_001 | GET stats không auth → 401 | ✅ |
| TC_AD_DASH_API_002 | GET stats admin → 200 | ✅ |
| TC_AD_DASH_API_003–010 | revenue, trend, growth, top-tours, search, bookings, export, notifications | ⏳ |

---

## 17. Ghi chú kỹ thuật

- **Doc cũ lệch product:** route `/dashboard` (không `/admin/dashboard`); 6 stats (không 4); 4 charts; thêm Search trends + Top tours.
- **Recent orders:** click **cả row** (không nút View riêng); `per_page=8`.
- **Orders stat:** khi có `status-counts`, tổng = pending+confirmed+completed+cancelled.
- **Mock:** `mockDashboardApi` — không trùng `mockToursApi` khi test dashboard-only.
- **Chạy test:** `npm run test:admin:dashboard` (UI) · `npm run test:api -- admin-dashboard` (API smoke)

## 18. Checklist regression

- Auth guest/non-admin ✅
- Stats data display ✅
- Chart filter URL ✅
- Search trends + top tours + recent orders ✅
- Notification bell ✅
- Sidebar collapse + nav mẫu ✅

**Trạng thái automation:** 29 TC UI ✅ · 2 API ✅ · ~61 TC ⏳ backlog
