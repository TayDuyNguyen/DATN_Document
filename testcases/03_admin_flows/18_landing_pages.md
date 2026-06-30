# Quản lý Trang đích (Landing Pages) - Test Cases

> **Trạng thái UI (2026-06-23):** Mục menu **đã ẩn** khỏi sidebar admin. Route `/admin/landing-pages` vẫn hoạt động khi truy cập trực tiếp. Lý do: module CMS landing chưa tích hợp đầy đủ với website user (nội dung public đang fallback i18n). Automation Playwright: **tạm hoãn** cho đến khi bật lại menu.

## 1. Tổng quan màn hình

* Đường dẫn route: `/admin/landing-pages`
* File source chính:
  - `D:\DATN\danangtrip-admin\src\pages\LandingPages\index.tsx`
  - `D:\DATN\danangtrip-admin\src\pages\LandingPages\components\LandingPageFormDrawer.tsx`
  - `D:\DATN\danangtrip-admin\src\pages\LandingPages\components\LandingPageTable.tsx`
  - `D:\DATN\danangtrip-admin\src\pages\LandingPages\components\LandingPageFilter.tsx`
* Component liên quan: `SectionHeader`, `Button`, `CustomSelect`, `TextInput`, `TextareaField`, `UnsavedChangesGuard`
* API/service sử dụng:
  - Queries: `useLandingPages` (Lọc theo search, type, status; hỗ trợ phân trang).
  - Mutations: `useCreateLandingPage`, `useUpdateLandingPage`, `useUpdateLandingPageStatus`, `useDeleteLandingPage`.
  - Image Upload: `axiosClient.post(API_ENDPOINTS.UPLOAD.IMAGE, formData)` (Upload hình ảnh).
* Quyền truy cập: Quản trị viên (Admin), Quản lý (Manager) có toàn quyền.
* Mục đích màn hình: Quản lý danh sách các trang đích phục vụ chiến dịch marketing (Destination, Tour line, Promotion). Hỗ trợ tùy chỉnh SEO nâng cao, lọc tour mặc định qua JSON và cấu hình content blocks (FAQ, Description) động.

## 2. Điều kiện tiền đề

* Tài khoản cần dùng: Đăng nhập quyền `admin` hoặc `manager`.
* Dữ liệu mẫu: Đã có sẵn một vài trang đích trong cơ sở dữ liệu.
* Trạng thái hệ thống: API hoạt động; thư mục lưu trữ ảnh hoạt động.

## 3. Danh sách chức năng chính

* **Tìm kiếm & Lọc**: Tìm kiếm theo tên tiêu đề; lọc theo Loại trang (Destination, Tour Line, Promotion) và Trạng thái (Draft, Published).
* **Danh sách bảng (Table)**:
  - Hiển thị danh sách trang đích, phân trang và thay đổi giới hạn dòng hiển thị.
  - Sửa trang đích (mở drawer điền sẵn data).
  - Xóa trang đích (yêu cầu xác nhận qua alert dialog).
  - Đổi trạng thái hiển thị nhanh (click toggle status: draft <-> published).
* **Drawer thêm mới / cập nhật trang đích**:
  - Gồm 3 Tab chính: `content` (Nội dung), `seo` (SEO nâng cao), `settings` (Bộ lọc & Blocks nội dung).
  - **Tab Content**:
    - Nhập Tiêu đề (max 150 ký tự), SEO Slug (max 100 ký tự, regex `/^[a-z0-9-]+$/`).
    - *Auto-generate Slug*: Tự động chuyển đổi Tiêu đề tiếng Việt có dấu thành slug không dấu phân cách bằng dấu gạch ngang (chỉ thực hiện khi tạo mới, không đè khi sửa).
    - Chọn loại trang, trạng thái, viết intro giới thiệu (max 1000 ký tự).
    - Chọn/Tải lên Banner Hero: Hỗ trợ upload ảnh lên server, xem trước ảnh vừa upload và có nút Xóa ảnh.
  - **Tab SEO**:
    - Tiêu đề SEO (max 150 ký tự, có đếm ký tự hiển thị đề xuất 70).
    - Mô tả SEO (max 1000 ký tự, có đếm ký tự hiển thị đề xuất 160).
    - Chọn/Tải lên OG Image (upload/preview/delete).
  - **Tab Settings**:
    - Nhập bộ lọc tour mặc định bằng văn bản JSON (Có validation kiểm tra cú pháp JSON hợp lệ khi submit).
    - Content Blocks Builder: Thêm mới động không giới hạn số lượng các block nội dung loại **FAQ** (nhập câu hỏi & câu trả lời) hoặc **Description** (nhập tiêu đề block & nội dung block). Cho phép xóa block bất kỳ.
* **Unsaved Changes Guard (Chặn đóng khi chưa lưu)**:
  - Nếu người dùng đã sửa đổi bất kỳ trường nào trong form (form bị dơ - `isDirty`):
    - Khi bấm đóng drawer hoặc click backdrop: Hiển thị hộp thoại cảnh báo thay đổi chưa lưu mặc định của trình duyệt (`window.confirm`).
    - Khi bấm chuyển hướng route khác trên sidebar: Hiển thị dialog modal `UnsavedChangesGuard` chặn route lại và hỏi ý kiến tiếp tục rời đi hay ở lại.

## 4. Test cases chi tiết

| ID | Nhóm chức năng | Test case | Tiền điều kiện | Bước thực hiện | Dữ liệu test | Kết quả mong đợi | Mức độ ưu tiên | Loại test |
| -- | -------------- | --------- | -------------- | -------------- | ------------ | ---------------- | -------------- | --------- |
| LD_PG_001 | Danh sách | Tìm kiếm trang đích bằng tiêu đề | Màn hình Landing Pages đang mở | 1. Nhập từ khóa tìm kiếm vào ô Search.<br>2. Chờ 400ms (debounce).<br>3. Quan sát bảng. | Search: `Đà Nẵng` | Bảng cập nhật danh sách trang đích có tiêu đề chứa từ "Đà Nẵng". Query gọi API với tham số `search` tương ứng. | High | Functional |
| LD_PG_002 | Danh sách | Lọc trang đích theo loại trang và trạng thái | Màn hình Landing Pages đang mở | 1. Chọn loại: `destination`.<br>2. Chọn trạng thái: `published`.<br>3. Quan sát bảng. | Type + Status | Bảng lọc chỉ hiển thị các trang đích là Destination có trạng thái Published. | High | Functional |
| LD_PG_003 | Danh sách | Đổi nhanh trạng thái hiển thị (Draft/Published) | Có item trong bảng | 1. Click vào badge trạng thái (hoặc nút switch) của một dòng.<br>2. Chờ API xử lý. | Item ID: `5` | - API `useUpdateLandingPageStatus` được gọi.<br>- Badge trạng thái đổi màu/text ngay lập tức (ví dụ: Draft -> Published).<br>- Toast hiển thị cập nhật trạng thái thành công. | Critical | Functional |
| LD_PG_004 | Danh sách | Xóa trang đích - Hủy bỏ | Có item trong bảng | 1. Click nút Xóa (Trash icon).<br>2. Khi alert confirm xuất hiện, bấm Cancel. | Item ID: `5` | Trình duyệt không gọi API xóa; dòng dữ liệu giữ nguyên trong danh sách. | Medium | Negative |
| LD_PG_005 | Danh sách | Xóa trang đích - Xác nhận | Có item trong bảng | 1. Click nút Xóa.<br>2. Khi confirm xuất hiện, bấm OK. | Item ID: `5` | - Gọi API `useDeleteLandingPage` với ID tương ứng.<br>- Item biến mất khỏi bảng danh sách.<br>- Toast hiển thị xóa thành công. | Critical | Functional |
| LD_PG_006 | Drawer Form | Tự động sinh Slug từ Tiêu đề (Auto-slug) | Mở drawer tạo mới | 1. Bấm "+ Thêm mới".<br>2. Nhập tiêu đề: `Khám phá Bán đảo Sơn Trà 2026`.<br>3. Quan sát ô Slug. | Title: `Khám phá Bán đảo Sơn Trà 2026` | Ô Slug tự động điền: `kham-pha-ban-dao-son-tra-2026`. Các ký tự đặc biệt, dấu tiếng Việt được loại bỏ sạch. | High | Functional |
| LD_PG_007 | Drawer Form | Sửa tiêu đề không đè lên Slug khi Edit | Mở drawer sửa trang đích | 1. Bấm nút Sửa một dòng trong bảng.<br>2. Thay đổi nội dung ô Tiêu đề.<br>3. Quan sát ô Slug. | Sửa title | Ô Slug giữ nguyên không thay đổi theo tiêu đề mới để tránh hỏng SEO cũ. | High | Functional |
| LD_PG_008 | Tab Content | Kiểm tra validation các trường bắt buộc | Mở drawer tạo mới | 1. Để trống Title, Slug.<br>2. Bấm Lưu. | Để trống | Hiện thông báo lỗi ngay dưới ô nhập: Tiêu đề bắt buộc, Slug bắt buộc. | High | Validation |
| LD_PG_009 | Tab Content | Kiểm tra độ dài giới hạn Tiêu đề | Mở drawer tạo mới | 1. Nhập tiêu đề dài hơn 150 ký tự.<br>2. Bấm Lưu. | > 150 ký tự | Hiện lỗi: Tiêu đề không được vượt quá 150 ký tự. | High | Validation |
| LD_PG_010 | Tab Content | Kiểm tra định dạng Slug chỉ chứa chữ thường, số, dấu gạch ngang | Mở drawer tạo mới | 1. Nhập slug có dấu cách hoặc chữ viết hoa hoặc ký tự lạ (vd: `Son-Tra-2026!`).<br>2. Bấm Lưu. | `Son-Tra-2026!` | Hiện lỗi: Slug không hợp lệ (chỉ chứa chữ thường không dấu, số và gạch ngang). | High | Validation |
| LD_PG_011 | Tab Content | Upload Banner Hero thành công | Mở drawer form | 1. Click nút Tải lên tại phần Hero Image.<br>2. Chọn 1 file ảnh hợp lệ (`.png` hoặc `.jpg`, <5MB).<br>3. Chờ upload. | File ảnh `.png` | - Nút hiển thị trạng thái đang tải lên.<br>- Gọi API upload ảnh thành công.<br>- Hiển thị ảnh preview bên dưới form kèm nút Xóa.<br>- URL ảnh được điền vào ô text. | High | API |
| LD_PG_012 | Tab Content | Upload Banner Hero dung lượng quá lớn hoặc sai định dạng | Mở drawer form | 1. Chọn file `.pdf` hoặc file ảnh nặng 15MB.<br>2. Upload. | File >15MB / PDF | Báo lỗi qua toast (File không đúng định dạng hoặc vượt quá kích thước cho phép); không thay đổi link ảnh cũ. | Medium | Negative |
| LD_PG_013 | Tab Content | Xóa ảnh Hero đã upload | Đang có ảnh preview | 1. Click nút X trên góc ảnh preview.<br>2. Quan sát. | Click button X | Ảnh preview biến mất; ô input văn bản link ảnh trống trơn; form chuyển sang trạng thái bị sửa đổi (dirty). | High | Functional |
| LD_PG_014 | Tab SEO | Đếm số ký tự trực quan | Mở Tab SEO | 1. Nhập tiêu đề SEO và Mô tả SEO.<br>2. Quan sát số đếm góc dưới. | Text nhập vào | Số lượng ký tự cập nhật liên tục khi gõ (ví dụ: `25/70 ký tự`, `80/160 ký tự`). | Low | UI |
| LD_PG_015 | Tab SEO | Kiểm tra giới hạn ký tự SEO | Mở Tab SEO | 1. Nhập mô tả SEO cực dài (>1000 ký tự).<br>2. Bấm Lưu. | > 1000 ký tự | Form báo lỗi validation: Mô tả SEO không được vượt quá 1000 ký tự. | High | Validation |
| LD_PG_016 | Tab Settings | Nhập bộ lọc JSON hợp lệ | Mở Tab Settings | 1. Nhập chuỗi JSON đúng chuẩn: `{"category": "tour", "price_max": 5000000}` vào ô Filters.<br>2. Bấm Lưu. | Valid JSON | Form submit thành công, JSON được parse chuẩn gửi lên backend. | High | Validation |
| LD_PG_017 | Tab Settings | Nhập bộ lọc JSON sai cú pháp | Mở Tab Settings | 1. Nhập chuỗi sai: `{category: tour, price_max: 5000000}` (thiếu dấu ngoặc kép key/value).<br>2. Bấm Lưu. | Invalid JSON | Toast báo lỗi định dạng JSON không hợp lệ; form ngăn không cho submit. | High | Validation |
| LD_PG_018 | Tab Settings | Thêm/Xóa FAQ block động | Mở Tab Settings | 1. Click nút "+ FAQ".<br>2. Điền câu hỏi, câu trả lời.<br>3. Click nút Trash kế bên để xóa. | Append & Remove | - Click "+ FAQ" thêm 1 block mới vào mảng với 2 input Câu hỏi & Trả lời.<br>- Điền thông tin lưu vào mảng.<br>- Click Xóa: Block tương ứng biến mất lập tức khỏi form. | High | Functional |
| LD_PG_019 | Tab Settings | Thêm/Xóa Mô tả block động | Mở Tab Settings | 1. Click nút "+ Block" mô tả.<br>2. Nhập tiêu đề và nội dung block.<br>3. Click nút Xóa. | Append & Remove | Block mô tả mới được append/remove bình thường như FAQ block. | High | Functional |
| LD_PG_020 | Form Guard | Drawer Form Dirty - Đóng Drawer hủy bỏ | Form đang bị sửa đổi (dirty) | 1. Nhập title.<br>2. Click nút X trên header hoặc click backdrop ngoài drawer. | Form dirty | Hiển thị thông báo xác nhận rời trang của trình duyệt. Bấm Hủy (Stay): Drawer giữ nguyên trạng thái không đóng. | High | Functional |
| LD_PG_021 | Form Guard | Drawer Form Dirty - Đóng Drawer đồng ý | Form đang bị sửa đổi (dirty) | 1. Thay đổi thông tin.<br>2. Click nút Cancel hoặc X.<br>3. Khi confirm hiện ra, bấm OK (Leave). | Form dirty | Drawer đóng lại lập tức; dữ liệu đã nhập/sửa bị hủy bỏ hoàn toàn. | High | Functional |
| LD_PG_022 | Blocker Route | Blocker Route khi đổi trang trên Sidebar | Form đang bị sửa đổi (dirty) | 1. Nhập dữ liệu vào form.<br>2. Click mục "Dashboard" trên sidebar để chuyển trang. | Thay đổi route | - Dialog Modal của `UnsavedChangesGuard` xuất hiện trên cùng màn hình (chứa icon Alert màu vàng, title Thay đổi chưa được lưu).<br>- Bấm "Ở lại" (Stay): Modal ẩn, giữ nguyên form.<br>- Bấm "Rời đi" (Leave): Modal đóng, route thay đổi sang Dashboard, form bị hủy bỏ. | Critical | Security |
| LD_PG_023 | Drawer Submit | Submit tạo mới Landing Page thành công | Điền đúng toàn bộ các trường | 1. Bấm Lưu.<br>2. Chờ phản hồi API. | Dữ liệu hợp lệ | - API `useCreateLandingPage` được gọi.<br>- Hiện trạng thái loading trên nút.<br>- Form drawer đóng lại; bảng danh sách xuất hiện bản ghi mới; toast thông báo thành công. | Critical | API |
| LD_PG_024 | Drawer Submit | Submit sửa Landing Page thành công | Mở edit, sửa thông tin | 1. Bấm Sửa.<br>2. Sửa SEO Title.<br>3. Bấm Lưu. | Dữ liệu hợp lệ | - API `useUpdateLandingPage` được gọi.<br>- Drawer đóng; thông tin mới cập nhật trên bảng; toast hiển thị thành công. | Critical | API |
| LD_PG_025 | Drawer Submit | API submit trả lỗi 422 trùng slug | Nhập slug đã tồn tại trong DB | 1. Nhập slug bị trùng.<br>2. Bấm Lưu. | Trùng slug | Toast hiển thị thông báo lỗi chi tiết từ server (ví dụ: Slug đã được sử dụng); form giữ nguyên để sửa lại slug. | High | API |
| LD_PG_026 | Responsive | Responsive hiển thị Drawer | Drawer đang mở | 1. Co kích thước màn hình về 375px.<br>2. Kiểm tra layout drawer. | Viewport mobile | Drawer mở rộng chiếm 100% chiều rộng màn hình mobile; các ô input và tab navigation hiển thị rõ ràng, dễ cuộn dọc. Nút lưu/hủy neo cố định ở chân trang. | Medium | Responsive |

## 5. Test data đề xuất

* Title hợp lệ: `Cẩm nang Du lịch Bà Nà Hills tự túc` -> Sinh slug: `cam-nang-du-lich-ba-na-hills-tu-tuc`
* Bộ lọc JSON hợp lệ:
  ```json
  {
    "category_slug": "ba-na-hills",
    "is_featured": true,
    "limit": 6
  }
  ```
* Bộ lọc JSON không hợp lệ:
  ```
  {
    category_slug: 'ba-na-hills',
    is_featured: true
  }
  ```

## 6. Checklist regression

* Tự động sinh slug hoạt động mượt mà khi gõ tiêu đề mà không gây giật lag trình duyệt (debounce/optimize keyup).
* Đổi trạng thái hiển thị nhanh ngoài bảng không làm mất bộ lọc tìm kiếm hiện tại.
* UnsavedChangesGuard hoạt động đúng cho cả hai trường hợp: click menu chuyển route React Router và click nút đóng drawer vật lý.

## 7. Ghi chú kỹ thuật

* Component `UnsavedChangesGuard` sử dụng hook `useBlocker` từ `react-router-dom` (yêu cầu cấu hình router thích hợp).
* JSON filter validation sử dụng Yup `.test()` để tránh ném ra ngoại lệ JavaScript làm crash app khi parse chuỗi rỗng hoặc chuỗi sai.
