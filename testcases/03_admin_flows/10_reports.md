# Admin — Báo cáo thống kê & Doanh thu (Reports)

**Routes:**
- `/admin/reports/revenue` — Báo cáo Doanh thu
- `/admin/reports/bookings` — Báo cáo Đơn đặt chỗ
- `/admin/reports/locations` — Báo cáo Địa điểm
- `/admin/reports/ratings` — Báo cáo Đánh giá
- `/admin/reports/users` — Báo cáo Người dùng

**Source:** `danangtrip-admin/src/pages/Reports/`  
**Automation:** `tests/admin/reports-revenue.spec.ts` · `tests/admin/reports-smoke.spec.ts` · `tests/admin/reports-auth.spec.ts`  
**POM:** `ReportPage.ts` · Mock: `reports.mock.ts` · Data: `reports-shared.data.ts`  
**Chạy test:** `npm run test:admin:reports`

---

## 1. Phạm vi

| Hạng mục | Chi tiết |
|----------|----------|
| Vai trò | **Admin** only (`PrivateRoute` — staff/user → `/login`) |
| API Revenue | `GET /admin/dashboard/revenue` · `GET /admin/reports/revenue-detail` · `GET /admin/payments` · `GET /admin/payments/export` |
| API Bookings | `GET /admin/reports/bookings` · `GET /admin/bookings/export` |
| API Locations | `GET /admin/reports/locations` · `GET /admin/locations/stats` · `GET /admin/locations` · `GET /admin/locations/export` |
| API Ratings | `GET /admin/reports/ratings` · `GET /admin/ratings/export` |
| API Users | `GET /admin/reports/users` · `GET /admin/users/export` |
| UI chung | Filter bar · Mock toggle · Export Excel · Error panel (retry + use mock) · Stats cards · Recharts · Table + pagination |
| URL sync | `from`, `to`, `payment_gateway`, `page` (revenue/bookings/ratings/locations); `year` (users). `per_page` **không** sync URL (hardcode 10). |

## 2. UI Interactive Inventory (Revenue — đại diện)

| # | Vùng UI | Nhãn (i18n) | Loại | Hành vi kỳ vọng | TC doc | Auto |
|---|---------|-------------|------|-----------------|--------|------|
| 1 | Header | Dữ liệu Thật/Giả lập | button | Toggle mock + toast | REP_GEN_005 | ✅ TC_AD_REP_005 |
| 2 | Header | Xuất Excel | button | Mock CSV hoặc API xlsx | REP_EXP_019–021 | ✅ TC_AD_REP_019–021 |
| 3 | Filter | Từ ngày / Đến ngày | date | URL sync on Apply | REP_GEN_001–002 | ✅ TC_AD_REP_001–002 |
| 4 | Filter | Áp dụng | button | Validate range + fetch | REP_GEN_003 | ✅ TC_AD_REP_003 |
| 5 | Filter | Mặc định | button | Reset defaults + URL | REP_GEN_004 | ✅ TC_AD_REP_004 |
| 6 | Error panel | Thử lại | button | Refetch API | REP_GEN_008 | ✅ TC_AD_REP_008 |
| 7 | Error panel | Sử dụng Mock Data | button | Bật mock mode | REP_GEN_007 | ✅ TC_AD_REP_007 |
| 8 | Charts | Xu hướng doanh thu | chart | Recharts area | REP_REV_010 | ✅ TC_AD_REP_010 |
| 9 | Charts | Cơ cấu cổng thanh toán | chart | Donut + gateway legend | REP_REV_011 | ✅ TC_AD_REP_011 |
| 10 | Charts | Top 5 Tour doanh thu cao | chart | 5 bar horizontal | REP_REV_012 | ✅ TC_AD_REP_012 |
| 11 | Table | Chi tiết giao dịch | table | Fields + pagination | REP_REV_013, REP_EXP_022 | ✅ TC_AD_REP_013, 022 |
| 12 | Auto mock | API 500 | system | Toast + mock On | REP_GEN_006 | ✅ TC_AD_REP_006 |
| 13 | Loading | Skeleton/spinner | state | Delay API | REP_GEN_009 | ✅ TC_AD_REP_009 |

**Bookings / Locations / Ratings / Users:** cùng pattern mock toggle + export + filter; smoke assert stats/charts/table tương ứng.

## 3. Mapping testcase doc → automation

| ID gốc | ID Auto | Mô tả | Auto |
|--------|---------|--------|------|
| REP_GEN_001 | TC_AD_REP_001 | URL sync filter Apply | ✅ |
| REP_GEN_002 | TC_AD_REP_002 | Khôi phục filter từ URL | ✅ |
| REP_GEN_003 | TC_AD_REP_003 | Validate ngày from > to | ✅ |
| REP_GEN_004 | TC_AD_REP_004 | Reset filter mặc định | ✅ |
| REP_GEN_005 | TC_AD_REP_005 | Toggle mock thủ công | ✅ |
| REP_GEN_006 | TC_AD_REP_006 | API lỗi → error panel (không auto mock) | ✅ |
| REP_GEN_007 | TC_AD_REP_007 | Error panel → Use Mock | ✅ |
| REP_GEN_008 | TC_AD_REP_008 | Retry từ error panel | ✅ |
| REP_GEN_009 | TC_AD_REP_009 | Loading state | ✅ |
| REP_REV_010 | TC_AD_REP_010 | Biểu đồ xu hướng doanh thu | ✅ |
| REP_REV_011 | TC_AD_REP_011 | Biểu đồ cổng thanh toán | ✅ |
| REP_REV_012 | TC_AD_REP_012 | Widget Top 5 tours | ✅ |
| REP_REV_013 | TC_AD_REP_013 | Bảng giao dịch (mapper fields) | ✅ |
| REP_BKG_014 | TC_AD_REP_014 | Bookings stats + charts | ✅ |
| REP_LOC_015 | TC_AD_REP_015 | Locations theo quận | ✅ |
| REP_RAT_016 | TC_AD_REP_016 | Ratings star distribution | ✅ |
| REP_USR_017 | TC_AD_REP_017 | Users growth chart | ✅ |
| REP_USR_018 | TC_AD_REP_018 | Users year filter + table | ✅ |
| REP_EXP_019 | TC_AD_REP_019 | Export mock CSV | ✅ |
| REP_EXP_020 | TC_AD_REP_020 | Export real xlsx API | ✅ |
| REP_EXP_021 | TC_AD_REP_021 | Export API lỗi → toast | ✅ |
| REP_EXP_022 | TC_AD_REP_022 | Pagination bảng revenue | ✅ |
| REP_SEC_023 | TC_AD_REP_041 | Non-admin → `/login` | ✅ |
| REP_SEC_024 | TC_AD_REP_040 | Guest → `/login` | ✅ |
| — | TC_AD_REP_042 | Admin truy cập revenue | ✅ |
| REP_RSP_025 | — | Responsive 375px | **manual-only** |

## 4. Test cases chi tiết (spec gốc)

| ID | Nhóm chức năng | Test case | Tiền điều kiện | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Mức độ ưu tiên | Loại test |
| -- | -------------- | --------- | -------------- | -------------- | ------------ | ---------------- | -------------- | --------- |
| REP_GEN_001 | URL Sync | Đồng bộ hóa bộ lọc lên URL query string | Admin đã đăng nhập | 1. Thay đổi ngày "Từ ngày", "Đến ngày", và chọn cổng thanh toán/trạng thái.<br>2. Bấm "Áp dụng" (Apply).<br>3. Kiểm tra thanh địa chỉ trình duyệt. | `from=2026-05-01`<br>`to=2026-05-31`<br>`gateway=momo` | URL cập nhật thành dạng `?from=2026-05-01&to=2026-05-31&payment_gateway=momo&page=1` khớp đúng các giá trị đã chọn. | High | Functional |
| REP_GEN_002 | URL Recovery | Giữ bộ lọc khi F5 tải lại trang | Có query string trên URL | 1. Mở link `/admin/reports/revenue?from=2026-04-01&to=2026-04-30`.<br>2. Quan sát ô lọc ngày trên giao diện. | URL có sẵn params | Bộ lọc hiển thị đúng ngày bắt đầu là `01/04/2026` và ngày kết thúc là `30/04/2026`. | High | Functional |
| REP_GEN_003 | Validation | Ngày bắt đầu lớn hơn ngày kết thúc | Bộ lọc đang mở | 1. Nhập ngày "Từ ngày": `2026-06-15`.<br>2. Nhập ngày "Đến ngày": `2026-06-01`.<br>3. Bấm nút áp dụng. | `from > to` | Hiển thị toast thông báo lỗi ngày bắt đầu không được lớn hơn ngày kết thúc. Không gửi request lên API. | High | Validation |
| REP_GEN_004 | Validation | Reset bộ lọc về mặc định | Bộ lọc đang được áp dụng khác mặc định | 1. Click nút "Đặt lại" (Reset).<br>2. Quan sát bộ lọc và URL. | | - Ngày "Từ ngày" reset về ngày đầu tiên của tháng hiện tại.<br>- Ngày "Đến ngày" reset về ngày hôm nay.<br>- Các select filter reset về mặc định "Tất cả" (All).<br>- URL params cập nhật lại. | Medium | Functional |
| REP_GEN_005 | Mock Mode | Chuyển chế độ Mock Mode thủ công | Đang ở màn hình báo cáo | 1. Click nút "Dữ liệu mẫu" (Mock Mode) trên header.<br>2. Quan sát nút bấm và thông báo. | Bấm Toggle | - Nút đổi màu vàng/xám cảnh báo đang bật dữ liệu mẫu.<br>- Toast hiển thị: Đã chuyển sang chế độ dữ liệu mẫu.<br>- Biểu đồ và bảng dữ liệu được thay thế bằng dữ liệu mock phong phú. | High | Functional |
| REP_GEN_006 | API Error | API thật bị lỗi tải trang (Error State) | Tắt Mock Mode, API server lỗi | 1. Vào trang báo cáo.<br>2. API trả về lỗi 500.<br>3. Quan sát giao diện. | API 500 error | - Hiển thị bảng thông báo lỗi kết nối kèm biểu tượng cảnh báo đỏ.<br>- Có 2 nút hành động: "Thử lại" và "Sử dụng dữ liệu mẫu". | Critical | API |
| REP_GEN_007 | API Error | Chuyển dữ liệu mẫu tự động khi API thật lỗi | API server lỗi | 1. API trả về lỗi 500.<br>2. Click nút "Sử dụng dữ liệu mẫu" trên UI lỗi.<br>3. Quan sát. | Click button | - Giao diện chuyển ngay sang hiển thị dữ liệu Mock.<br>- Hiển thị toast thông báo đã tự động chuyển sang chế độ dữ liệu mẫu. | High | Negative |
| REP_GEN_008 | API Error | Thử tải lại API thật từ màn hình lỗi | API server lỗi sau đó khôi phục | 1. API lỗi hiển thị màn hình đỏ.<br>2. Admin bấm nút "Thử lại". | Click Retry | Request API được gọi lại. Nếu API phản hồi ok, màn hình lỗi biến mất và hiển thị dữ liệu thật. | High | API |
| REP_GEN_009 | Loading | Loading state khi gọi API | API chậm | 1. Nhấn Lọc hoặc chuyển trang.<br>2. Quan sát các block stats/charts/table. | Delay 3s | Hiển thị skeleton loading hoặc hiệu ứng mờ kèm spinner quay; các nút bấm bị disable tạm thời để tránh double submit. | Medium | UI |
| REP_REV_010 | Revenue | Hiển thị biểu đồ doanh thu & giao dịch | Vào báo cáo doanh thu | 1. Xem biểu đồ Trend ở giữa trang. | Mock/Real data | Biểu đồ cột/đường hiển thị đúng xu hướng doanh thu và số lượng giao dịch tương ứng theo ngày đã lọc. Hover chuột vào từng cột hiện tooltip chi tiết. | High | UI |
| REP_REV_011 | Revenue | Thống kê doanh thu theo cổng thanh toán | Vào báo cáo doanh thu | 1. Xem biểu đồ hình tròn/donut cổng thanh toán. | Momo, VNPay, ZaloPay | Hiển thị tỷ lệ phần trăm phân bố doanh thu của từng cổng thanh toán; màu sắc các cổng nhất quán (Momo màu hồng, VNPay màu xanh navy,...). | Medium | UI |
| REP_REV_012 | Revenue | Danh sách Top 5 tour doanh thu cao nhất | Vào báo cáo doanh thu | 1. Xem widget xếp hạng Top Tours. | Top 5 tours | Hiển thị đủ 5 tour kèm số lượt booking và tổng số doanh thu thu được, sắp xếp giảm dần theo doanh thu. | Medium | Functional |
| REP_REV_013 | Revenue | Bảng chi tiết giao dịch doanh thu | Vào báo cáo doanh thu | 1. Cuộn xuống bảng chi tiết.<br>2. Kiểm tra các cột dữ liệu. | Table data | Hiển thị: Mã GD, Mã Booking, Tên KH, Tên Tour, Số tiền (format VNĐ đúng dấu phân cách), Cổng thanh toán, Ngày giờ giao dịch, Trạng thái (Paid, Pending, Failed, Refunded). | High | UI |
| REP_BKG_014 | Bookings | Thống kê trạng thái booking | Vào báo cáo bookings | 1. Quan sát card số liệu tổng quan.<br>2. Quan sát biểu đồ trạng thái. | Bookings list | Hiển thị chính xác tổng số booking, số lượng booking thành công (completed), đang chờ (pending), bị hủy (cancelled) cùng tỷ lệ % tương ứng. | High | Functional |
| REP_LOC_015 | Locations | Báo cáo địa điểm theo quận huyện | Vào báo cáo địa điểm | 1. Lọc theo quận huyện "Sơn Trà".<br>2. Quan sát bảng và biểu đồ quận huyện. | Quận Sơn Trà | Biểu đồ hiển thị chính xác số lượng địa điểm thuộc quận Sơn Trà; bảng chỉ list các địa điểm nằm tại Sơn Trà. | High | Functional |
| REP_RAT_016 | Ratings | Báo cáo phân phối số sao đánh giá | Vào báo cáo đánh giá | 1. Quan sát widget cột phân bố sao (từ 5 sao xuống 1 sao). | Ratings list | Hiển thị tổng số review, điểm trung bình toàn hệ thống (ví dụ: 4.5) và thanh progress bar thể hiện tỷ lệ số lượng review của từng mức sao. | High | Functional |
| REP_USR_017 | Users | Báo cáo tăng trưởng thành viên | Vào báo cáo khách hàng | 1. Quan sát biểu đồ đăng ký mới theo tháng/ngày. | Khách hàng mới | Biểu đồ line thể hiện đúng lượng tài khoản được tạo mới theo thời gian đã lọc. | Medium | Functional |
| REP_USR_018 | Users | Báo cáo vai trò thành viên | Vào báo cáo khách hàng | 1. Quan sát phân phối vai trò. | Roles: user, admin,... | Biểu đồ tròn hiển thị đúng tỷ lệ tài khoản theo vai trò (User chiếm đa số, Staff/Manager/Admin số lượng ít). | Medium | Functional |
| REP_EXP_019 | Export | Xuất Excel trong chế độ Mock Mode | Đang bật Mock Mode | 1. Bấm nút "Xuất Excel" (Export).<br>2. Quan sát. | Mock data active | - Hiển thị toast báo tải file thành công.<br>- Client tự sinh và tải xuống file `.csv` giả lập có chứa toàn bộ dòng dữ liệu đang xem trên bảng. | High | Functional |
| REP_EXP_020 | Export | Xuất Excel chế độ API thật | Chế độ API thật hoạt động | 1. Bấm nút "Xuất Excel".<br>2. Chờ API xử lý.<br>3. Kiểm tra file tải về. | Real data active | - API `exportRevenueMutation` (hoặc tương ứng) được gọi.<br>- Hiện toast loading, sau đó tải xuống file định dạng `.xlsx` hoặc `.xls`.<br>- Tên file tự sinh theo định dạng: `bao-cao-[loai]_[from]_to_[to]_[date].xlsx`. | Critical | API |
| REP_EXP_021 | Export | Xuất Excel API trả lỗi | API export trả 500/400 | 1. Bấm nút "Xuất Excel".<br>2. API trả lỗi. | Mock export error | Hiển thị toast thông báo lỗi xuất file từ server; không crash client, không tải xuống file rỗng/lỗi. | High | API |
| REP_EXP_022 | Paging | Phân trang bảng thống kê chi tiết | Bảng chi tiết có nhiều trang | 1. Click chọn trang 2.<br>2. Click đổi số dòng trên trang (10 -> 20 -> 50). | Pagination | - Bảng dữ liệu load đúng trang 2.<br>- URL params cập nhật `page=2`.<br>- Khi đổi số dòng, reset trang về 1, URL params cập nhật. | High | Functional |
| REP_SEC_023 | Permission | Quyền truy cập báo cáo của Nhân viên (Staff) | Tài khoản nhân viên thông thường | 1. Đăng nhập tài khoản Staff có quyền hạn chế.<br>2. Cố gắng vào `/admin/reports/revenue`. | Staff role | Chuyển hướng sang trang Dashboard chính hoặc trang 403 Forbidden theo chính sách bảo mật; không render menu báo cáo trên sidebar. | Critical | Permission |
| REP_SEC_024 | Security | Truy cập trực tiếp link báo cáo không token | Chưa đăng nhập admin | 1. Đăng xuất.<br>2. Mở trực tiếp `/admin/reports/revenue`. | Không token | Chuyển hướng ngay lập tức về trang Đăng nhập `/login` của admin. | Critical | Security |
| REP_RSP_025 | Responsive | Hiển thị biểu đồ và bảng trên Mobile | Viewport di động | 1. Chuyển sang màn hình 375px.<br>2. Kiểm tra layout. | Responsive testing | - Các khối stats chuyển từ hàng ngang thành cột đứng.<br>- Biểu đồ charts tự động resize theo khung chứa, không bị méo/tràn ngang.<br>- Bảng dữ liệu hiển thị scroll ngang mượt mà, text không chồng chéo. | Medium | Responsive |

## 5. Test data mock

| Record | Mục đích |
|--------|----------|
| `primaryRevenuePayment` (TX20834 / DNT10452) | Bảng revenue, pagination |
| `mockRevenueTourDetails` (5 tours) | Top 5 chart |
| `mockBookingsReport` | Bookings smoke |
| `mockLocationsDistribution` + list Mỹ Khê | Locations smoke |
| `mockRatingsReport` | Ratings smoke |
| `mockUsersReport` year 2026 | Users chart + table |

**Filter kỳ vọng:** `from=2026-05-01` · `to=2026-05-31` · URL recovery `2026-04-01`–`2026-04-30`

## 6. Checklist regression

- [x] URL query from/to/payment_gateway/page/per_page/mock đồng bộ (revenue)
- [x] API lỗi → error panel + toast cảnh báo; retry / use mock thủ công
- [x] Export mock CSV vs real xlsx
- [x] Pagination URL `page=2` + selector `per_page`
- [x] Auth guest → `/login`; staff → `/dashboard`; admin/manager vào reports
- [x] Users role pie chart + stats cards thật
- [ ] Responsive charts mobile (manual REP_RSP_025)

## 7. Đề xuất cải thiện (PHASE 0.8)

| ID | Loại | Severity | Phát hiện | Đề xuất | Trạng thái |
|----|------|----------|-----------|---------|------------|
| IMP_REP_001 | Feature | P1 | REP_USR_018 thiếu role pie | Thêm `UsersRoleChart` + mapper `role_distribution` | **fixed** |
| IMP_REP_002 | Test | P3 | TC flaky session khi chạy dài | mockAuthRefresh cho staff test | open |
| IMP_REP_003 | UX | P2 | Top tour chart truncate 15 ký tự | YAxis width 140 + tooltip full name | **fixed** |

**Trạng thái automation:** **26/26 passed** (`npm run test:admin:reports`, 2026-06-23; 3 flaky pass on retry)

## 8. Ghi chú kỹ thuật

- Revenue gọi **3 API song song**; lỗi → hiển thị error panel + toast `reports_common.mock.toast_to_mock` (không auto bật mock).
- Cột tour trong bảng revenue: ưu tiên `booking.tour_name` từ API payments.
- Mock mode persist URL `?mock=1`; i18n mock thống nhất namespace `reports_common`.
- `ReportPageShell` + `data-testid` trên Revenue/Users; breadcrumb hub → `/admin/reports/revenue`.
- Bookings/Locations/Ratings: đã bọc `ReportPageShell`, mock banner, `data-testid`, quick filter auto-apply, `per_page` URL.
- Users report: role pie + total users / active rate stats; filter năm (`#users-filter-year`).
- Recharts component unmount cần cleanup canvas (regression manual).
