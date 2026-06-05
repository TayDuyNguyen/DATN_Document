# Màn hình Báo cáo thống kê & Doanh thu (Admin Reports) - Test Cases

## 1. Tổng quan màn hình

* Đường dẫn route: 
  - `/admin/reports/revenue` (Báo cáo Doanh thu)
  - `/admin/reports/bookings` (Báo cáo Đơn đặt chỗ)
  - `/admin/reports/locations` (Báo cáo Địa điểm)
  - `/admin/reports/ratings` (Báo cáo Đánh giá)
  - `/admin/reports/users` (Báo cáo Khách hàng/Thành viên)
* File source chính: 
  - `D:\DATN\danangtrip-admin\src\pages\Reports\RevenueReport\index.tsx`
  - `D:\DATN\danangtrip-admin\src\pages\Reports\BookingsReport\index.tsx`
  - `D:\DATN\danangtrip-admin\src\pages\Reports\LocationReport\index.tsx`
  - `D:\DATN\danangtrip-admin\src\pages\Reports\RatingsReport\index.tsx`
  - `D:\DATN\danangtrip-admin\src\pages\Reports\UsersReport\index.tsx`
* Component liên quan: `ReportFilterBar`, `RevenueStatsCards`, `RevenueReportCharts`, `RevenueReportTable`, `Breadcrumbs`, `SectionHeader`
* API/service sử dụng:
  - `useRevenueReportQuery(activeFilters)` / `exportRevenueMutation`
  - `useBookingsReportQuery(activeFilters)` / `exportBookingsMutation`
  - `useLocationsReportQuery(activeFilters)` / `exportLocationsMutation`
  - `useRatingsReportQuery(activeFilters)` / `exportRatingsMutation`
  - `useUsersReportQuery(activeFilters)` / `exportUsersMutation`
* Quyền truy cập: Quản trị viên (Admin), Quản lý (Manager) có quyền xem; Staff hạn chế theo phân quyền.
* Mục đích màn hình: Cung cấp số liệu thống kê chi tiết, trực quan hóa dữ liệu qua biểu đồ, hỗ trợ phân tích xu hướng kinh doanh và xuất báo cáo ra Excel phục vụ nghiệp vụ kế toán/quản lý.

## 2. Điều kiện tiền đề

* Tài khoản cần dùng: Đăng nhập quyền `admin` hoặc `manager`.
* Dữ liệu mẫu: Hệ thống đã seed nhiều dữ liệu tour, địa điểm, thành viên, đánh giá, booking thanh toán qua nhiều cổng khác nhau và các mốc thời gian khác nhau.
* Trạng thái hệ thống: Cổng API hoạt động; mock mode bật/tắt được qua nút toggle.

## 3. Danh sách chức năng chính

* **Đồng bộ bộ lọc URL**: Mọi thay đổi về bộ lọc (Từ ngày, Đến ngày, Cổng thanh toán, Quận huyện, Trạng thái,...) tự động cập nhật lên URL search parameters để khi F5 trang không mất trạng thái lọc.
* **Xử lý Mock Mode (Dữ liệu giả lập)**:
  - Khi API lỗi hoặc chưa hoàn thiện, tự động kích hoạt Mock Mode (hoặc người dùng tự bấm nút toggle Mock Mode).
  - Hiển thị thông tin thống kê, biểu đồ và danh sách dữ liệu giả lập chất lượng cao, đúng định dạng.
* **Xử lý Lỗi API (Error State UI)**:
  - Hiển thị card cảnh báo kết nối thất bại, nút "Thử lại" (Retry) để gọi lại API, và nút "Sử dụng dữ liệu mẫu" (Mock Mode) để chuyển sang chế độ giả lập.
* **Báo cáo Doanh thu (Revenue)**:
  - Thống kê: Tổng doanh thu, Doanh thu trung bình ngày, Tổng số giao dịch, Số tiền đã hoàn.
  - Biểu đồ: Xu hướng doanh thu và giao dịch theo ngày, Biển đồ tròn cổng thanh toán (momo, vnpay, zalopay), Top 5 tour mang lại doanh thu cao nhất.
* **Báo cáo Booking**:
  - Thống kê: Tổng lượt đặt, tỷ lệ lấp đầy, số booking hoàn thành, đang chờ hoặc bị hủy.
  - Biểu đồ: Xu hướng booking theo thời gian, tỷ lệ trạng thái booking.
* **Báo cáo Địa điểm (Locations)**:
  - Thống kê: Tổng số địa điểm, số địa điểm active/draft, phân bố địa điểm theo quận huyện (Hải Châu, Sơn Trà, Ngũ Hành Sơn,...).
* **Báo cáo Đánh giá (Ratings)**:
  - Thống kê: Điểm đánh giá trung bình toàn hệ thống, tổng số lượt review, phân phối số sao (1-5 sao).
* **Báo cáo Khách hàng (Users)**:
  - Thống kê: Tổng số user đăng ký mới, số user active/blocked, phân bố vai trò (admin, user, tour_guide, manager).
* **Xuất báo cáo (Export Excel)**:
  - Ở chế độ Mock Mode: Tải file `.csv` giả lập trực tiếp từ Client.
  - Ở chế độ Real API: Gọi API Mutation xuất Excel tải file `.xlsx` thật từ Server.

## 4. Test cases chi tiết

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

## 5. Test data đề xuất

* Khoảng ngày thử nghiệm: `Từ ngày: 2026-05-01` tới `Đến ngày: 2026-05-31`
* Tài khoản test: 
  - Admin: `admin@danangtrip.vn` / `DaNangTrip@2026`
  - Staff hạn chế: `staff_junior@danangtrip.vn` / `DaNangTrip@2026`

## 6. Checklist regression

* Bộ lọc ngày tháng áp dụng đúng cho tất cả biểu đồ và bảng giao dịch (không xảy ra tình trạng bảng lọc đúng nhưng biểu đồ vẫn hiển thị toàn bộ thời gian).
* Bấm xuất Excel giữ nguyên các filter đang chọn để xuất đúng tập con dữ liệu mong muốn.
* Bật/Tắt Mock Mode cập nhật ngay lập tức giao diện mà không yêu cầu người dùng phải refresh trang thủ công.

## 7. Ghi chú kỹ thuật

* Các component biểu đồ sử dụng thư viện Recharts hoặc Chart.js (cần đảm bảo dọn dẹp canvas khi unmount tránh rò rỉ bộ nhớ).
* Logic Mock Mode được xử lý trong hàm `getMockRevenueReportData` (hoặc các hàm tương ứng từng report) sinh dữ liệu ngẫu nhiên nhưng nhất quán theo khoảng ngày chọn.
* Export file sử dụng `Blob` và URL tạm để trigger download trên trình duyệt client.
