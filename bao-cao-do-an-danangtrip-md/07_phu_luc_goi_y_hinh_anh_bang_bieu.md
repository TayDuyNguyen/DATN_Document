# PHỤ LỤC: GỢI Ý HÌNH ẢNH, BẢNG BIỂU VÀ BIỂU ĐỒ

## 1. Danh mục hình ảnh đề xuất

*Bảng PL.1: Danh sách các giao diện đề xuất chụp minh họa trong báo cáo*

| STT | Tên hình | Nguồn chụp |
| --- | --- | --- |
| 1 | Giao diện trang chủ DanangTrip | `danangtrip-web` |
| 2 | Giao diện danh sách địa điểm | `danangtrip-web` |
| 3 | Giao diện chi tiết địa điểm | `danangtrip-web` |
| 4 | Giao diện bản đồ du lịch | `danangtrip-web` |
| 5 | Giao diện tìm kiếm | `danangtrip-web` |
| 6 | Giao diện danh sách tour | `danangtrip-web` |
| 7 | Giao diện chi tiết tour | `danangtrip-web` |
| 8 | Giao diện chọn lịch khởi hành | `danangtrip-web` |
| 9 | Giao diện đặt tour | `danangtrip-web` |
| 10 | Giao diện thanh toán | `danangtrip-web` |
| 11 | Giao diện hồ sơ người dùng | `danangtrip-web` |
| 12 | Giao diện chatbot | `danangtrip-web` |
| 13 | Giao diện bảng điều khiển quản trị | `danangtrip-admin` |
| 14 | Giao diện quản lý địa điểm | `danangtrip-admin` |
| 15 | Giao diện quản lý tour | `danangtrip-admin` |
| 16 | Giao diện quản lý đơn đặt tour | `danangtrip-admin` |
| 17 | Giao diện quản lý thanh toán | `danangtrip-admin` |
| 18 | Giao diện báo cáo doanh thu | `danangtrip-admin` |
| 19 | Giao diện điểm thành viên, lịch sử điểm và phần thưởng | `danangtrip-web` |
| 20 | Giao diện chọn khuyến mãi/phiếu giảm giá cá nhân khi đặt tour | `danangtrip-web` |
| 21 | Giao diện ghi nhận đánh giá hữu ích | `danangtrip-web` |
| 22 | Giao diện thông báo nhắc lịch khởi hành | `danangtrip-web` |
| 23 | Giao diện quản trị xác nhận thanh toán thủ công | `danangtrip-admin` |

## 2. Danh mục bảng biểu đề xuất

*Bảng PL.2: Danh mục các bảng biểu cần xây dựng trong báo cáo*

| STT | Tên bảng | Vị trí gợi ý |
| --- | --- | --- |
| 1 | Bảng công nghệ sử dụng | Mở đầu |
| 2 | Bảng tác nhân hệ thống | Chương 2 |
| 3 | Bảng yêu cầu phi chức năng | Chương 2 |
| 4 | Bảng đặc tả ca sử dụng đăng nhập | Chương 2 |
| 5 | Bảng đặc tả ca sử dụng đặt tour | Chương 2 |
| 6 | Bảng đặc tả ca sử dụng thanh toán | Chương 2 |
| 7 | Bảng đường dẫn website người dùng | Chương 3 |
| 8 | Bảng đường dẫn trang quản trị | Chương 3 |
| 9 | Bảng kết quả kiểm thử | Chương 3 |

## 3. Biểu đồ nên vẽ lại cho báo cáo Word

### 3.1. Biểu đồ kiến trúc tổng thể

Nên vẽ gồm các khối: Website người dùng, Trang quản trị, Laravel API, PostgreSQL/Supabase, bảng bộ nhớ đệm chatbot, Cloudinary, SePay, dịch vụ thư điện tử và nhà cung cấp AI. Chỉ bổ sung Redis nếu cấu hình triển khai thực tế có sử dụng.

### 3.2. Biểu đồ use case tổng quan

Nên tách ba actor: Khách truy cập, Người dùng, Quản trị viên.

### 3.3. Biểu đồ tuần tự đặt tour và thanh toán

Nên thể hiện các đối tượng: Người dùng, Website, Laravel API, Database, SePay.

## 4. Mẫu bảng kết quả kiểm thử

*Bảng PL.3: Kết quả kiểm thử chức năng thủ công chi tiết của hệ thống*

| STT | Phân hệ | Dữ liệu kiểm thử | Kết quả mong đợi | Kết quả thực tế | Trạng thái |
| --- | --- | --- | --- | --- | --- |
| 1 | Xác thực | Đăng ký bằng email chưa tồn tại | Tài khoản được tạo, không trùng email/tên đăng nhập | Đăng ký tài khoản thành công, lưu tài khoản dưới trạng thái Chờ kích hoạt (pending) | Đạt |
| 2 | Xác thực | Đăng nhập đúng email/mật khẩu | Nhận mã thông báo và chuyển vào hệ thống | Đăng nhập thành công, nhận JWT token và chuyển vào trang Dashboard | Đạt |
| 3 | Xác thực | Đăng nhập sai mật khẩu | Hiển thị thông báo lỗi | Hệ thống hiển thị thông báo sai mật khẩu màu đỏ nổi bật | Đạt |
| 4 | Địa điểm | Lọc theo danh mục/quận | Danh sách hiển thị đúng dữ liệu | Danh sách địa điểm tải nhanh, lọc chính xác theo điều kiện chọn | Đạt |
| 5 | Địa điểm | Mở chi tiết một địa điểm | Hiển thị mô tả, ảnh, tọa độ, đánh giá | Hiển thị đầy đủ thông tin chi tiết, bản đồ vị trí và danh sách đánh giá | Đạt |
| 6 | Tour | Mở chi tiết một tour đang hoạt động | Hiển thị giá, lịch trình, lịch khởi hành | Thông tin chi tiết hiển thị đầy đủ, lịch trình trực quan, hiển thị các mã giảm giá khả dụng | Đạt |
| 7 | Đặt tour | Tạo đơn đặt tour với lịch còn chỗ | Đơn đặt tour được tạo, số chỗ cập nhật | Tạo đơn đặt tour thành công, lưu thông tin vào DB, trừ số chỗ trống trên lịch | Đạt |
| 8 | Đặt tour | Tạo đơn đặt tour vượt số chỗ | Hệ thống từ chối và báo lỗi | Báo lỗi không đủ chỗ khả dụng và ngăn chặn tạo đơn hàng | Đạt |
| 9 | Thanh toán | Tạo thanh toán cho đơn đặt tour đang chờ xử lý | Sinh giao dịch/mã QR | Sinh mã QR VietQR kèm số tiền và nội dung chuyển khoản tự động chính xác | Đạt |
| 10 | Thanh toán | Nhận IPN hợp lệ từ SePay | Thanh toán thành công, đơn đặt tour được cập nhật | Cập nhật trạng thái đơn hàng thành đã thanh toán tự động khi nhận IPN từ SePay | Đạt |
| 11 | Đánh giá | Gửi đánh giá hợp lệ | Đánh giá được lưu, tự động phê duyệt hiển thị công khai ngay lập tức | Gửi đánh giá thành công, lưu ở trạng thái đã duyệt (approved), điểm trung bình được cập nhật | Đạt |
| 12 | Quản trị tour | Quản trị viên thêm tour mới | Tour hiển thị ở danh sách quản trị và công khai khi đang hoạt động | Tour mới xuất hiện trên trang quản trị và website người dùng | Đạt |
| 13 | Quản trị đánh giá | Quản trị viên từ chối hoặc xóa đánh giá | Đánh giá bị ẩn khỏi trang chi tiết và người dùng nhận được thông báo từ chối | Đánh giá bị từ chối chuyển sang trạng thái rejected, gửi thông báo lý do cho người dùng | Đạt |
| 14 | Chatbot | Hỏi tour theo ngân sách | Trả lời dựa trên dữ liệu tour phù hợp | Chatbot nhận diện ý định và lọc tour theo đúng khoảng giá yêu cầu | Đạt |
| 15 | Chatbot | Hỏi câu ngoài phạm vi du lịch | Intent Guard từ chối hoặc hướng dẫn hỏi lại | Từ chối trả lời câu hỏi ngoài phạm vi và hướng dẫn người dùng hỏi đúng chủ đề | Đạt |
| 16 | Chatbot | Nhà cung cấp AI lỗi hoặc quá thời gian chờ | Hệ thống chuyển nhà cung cấp/khóa hoặc trả phản hồi dự phòng | Tự động chuyển đổi khóa API/nhà cung cấp dự phòng mượt mà không gây ngắt quãng | Đạt |
| 17 | Quản trị đặt tour | Quản trị viên xác nhận thanh toán thủ công cho đơn đặt tour chuyển khoản | Đơn đặt tour cập nhật trạng thái thanh toán thành công và gửi thông báo xác nhận | Đơn đặt tour cập nhật trạng thái thanh toán thành công, gửi email hóa đơn tự động và cập nhật số chỗ | Đạt |
| 18 | Khuyến mãi | Khách hàng áp dụng mã giảm giá hợp lệ | Hệ thống tính chiết khấu và giảm tổng tiền cần trả | Hệ thống tự động tính toán số tiền chiết khấu và giảm tổng số tiền cần trả trên hóa đơn | Đạt |
| 19 | Khuyến mãi | Khách hàng áp dụng mã hết hạn hoặc chưa đạt giá trị tối thiểu | Hệ thống báo lỗi và không áp dụng chiết khấu | Hệ thống hiển thị thông báo lỗi chi tiết và không áp dụng chiết khấu cho hóa đơn | Đạt |
| 20 | Điểm thành viên | Đổi phần thưởng khi đủ điểm | Trừ điểm một lần và cấp phiếu giảm giá cá nhân | Điểm khả dụng được trừ chính xác, hệ thống ghi nhận lịch sử giao dịch và cấp voucher | Đạt |
| 21 | Đánh giá hữu ích | Ghi nhận đánh giá của người khác hai lần | Lần đầu thành công, lần sau bị từ chối | Lần đầu ghi nhận thành công và cộng điểm cho tác giả; lần thứ hai báo lỗi chặn trùng lặp | Đạt |
| 22 | Nhắc lịch | Chạy tác vụ cho đơn khởi hành ngày kế tiếp | Tạo thông báo đúng điều kiện và không trùng | Hệ thống tự động gửi thông báo in-app nhắc nhở lịch khởi hành trước 1 ngày cho khách hàng | Đạt |

## 5. Checklist phần còn thiếu cần bổ sung thủ công

Để báo cáo đủ tốt khi nộp, cần bổ sung thêm các nội dung sau:

- Ảnh chụp giao diện thật của website người dùng và trang quản trị.
- Biểu đồ use case tổng quan và phân rã theo từng tác nhân.
- Biểu đồ tuần tự cho các chức năng: đăng nhập, đặt tour, thanh toán, chatbot.
- Biểu đồ hoạt động cho các chức năng: tìm kiếm, đặt tour, quản trị tour, duyệt đánh giá.
- Bảng trường hợp kiểm thử có kết quả thật sau khi chạy kiểm thử.
- Liên kết hoặc ảnh minh họa kiểm thử API bằng Postman/Swagger nếu có.
- Ảnh minh họa kết quả đóng gói/kiểm thử đạt.
- Bảng mô tả đầu vào/đầu ra của quy trình AI Chatbot.
- Ví dụ truy vấn chatbot với dữ liệu thật lấy từ cơ sở dữ liệu.
- Bảng môi trường triển khai thực tế.

## 6. Gợi ý phụ lục API

Khi báo cáo chính quá dài, có thể đưa danh sách API vào phụ lục:

*Bảng PL.4: Danh mục các điểm cuối API chính trong hệ thống*

| Nhóm API | Endpoint tiêu biểu |
| --- | --- |
| Auth | `POST /auth/register`, `POST /auth/login`, `POST /auth/refresh`, `POST /auth/logout` |
| Home | `GET /home`, `GET /home/locations`, `GET /home/tours`, `GET /home/blogs` |
| Locations | `GET /locations`, `GET /locations/{slug}`, `GET /locations/{id}/ratings` |
| Tours | `GET /tours`, `GET /tours/{slug}`, `GET /tours/{id}/schedules` |
| Đặt tour | `POST /bookings/calculate`, `POST /bookings`, `GET /user/bookings` |
| Thanh toán | `POST /payments/create`, `GET /payments/status/{transaction_code}`, `POST /sepay/ipn`, `PATCH /admin/bookings/{id}/confirm-payment` |
| Khuyến mãi | `GET /promotions`, `POST /promotions/validate`, `GET /admin/promotions`, `POST /admin/promotions` |
| Cart | `GET /cart`, `POST /cart/items`, `PUT /cart/items/{id}`, `DELETE /cart` |
| Rating | `POST /ratings`, `PUT /ratings/{id}`, `DELETE /ratings/{id}` |
| Điểm thành viên | `GET /user/points`, `GET /user/points/history`, `GET /user/point-rewards`, `POST /user/point-rewards/{id}/redeem` |
| Phiếu giảm giá cá nhân | `GET /user/vouchers`; mã phiếu được gửi trong API tính giá/tạo đơn đặt tour |
| Đánh giá hữu ích | `POST /ratings/{id}/helpful` |
| Bảng điều khiển quản trị | `GET /admin/dashboard`, `GET /admin/dashboard/revenue`, `GET /admin/reports/bookings` |
| Quản trị tour | `GET /admin/tours`, `POST /admin/tours`, `PUT /admin/tours/{id}` |
| Quản trị địa điểm | `GET /admin/locations`, `POST /admin/locations`, `PUT /admin/locations/{id}` |
| Quản trị đơn đặt tour | `GET /admin/bookings`, `PATCH /admin/bookings/{id}/status`, `PATCH /admin/bookings/{id}/confirm-payment` |

### 6.1. Gợi ý phụ lục quy trình AI Chatbot

| Thành phần | Nội dung cần chứng minh trong báo cáo |
| --- | --- |
| Intent Guard | Ví dụ câu hỏi hợp lệ và câu hỏi ngoài phạm vi; kết quả phân loại |
| Query Understanding | Ví dụ trích xuất `destination`, `price`, `people`, `date`, `duration` |
| Truy xuất tri thức | Dữ liệu truy xuất từ tour, địa điểm, bài viết, chính sách; kết quả tìm kiếm embedding nếu được bật |
| Lớp bộ nhớ đệm | Cách xác định khóa trong `chat_cache`; ví dụ có dữ liệu/không có dữ liệu còn hiệu lực |
| AI Failover | Điều kiện chuyển đổi dự phòng: quá thời gian chờ, vượt giới hạn tần suất, lỗi nhà cung cấp, phản hồi không hợp lệ |
| Phản hồi | Câu trả lời cuối cùng có dựa trên dữ liệu truy xuất được |

## 7. Mã sơ đồ draw.io để bổ sung sau

> Ghi chú: Có thể copy nội dung XML dưới đây vào draw.io bằng cách chọn `Arrange` -> `Insert` -> `Advanced` -> `XML`, hoặc tạo file `.drawio` riêng rồi chỉnh lại bố cục/nhãn theo hình thức báo cáo.

### 7.1. Sơ đồ kiến trúc tổng thể

```xml
<mxfile host="app.diagrams.net">
  <diagram name="DanangTrip Architecture">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <mxCell id="user" value="Người dùng" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="40" y="80" width="140" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="admin" value="Quản trị viên" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="40" y="220" width="140" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="web" value="danangtrip-web&#xa;Next.js / React" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1">
          <mxGeometry x="250" y="70" width="180" height="80" as="geometry"/>
        </mxCell>
        <mxCell id="adminweb" value="danangtrip-admin&#xa;React / Vite" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1">
          <mxGeometry x="250" y="210" width="180" height="80" as="geometry"/>
        </mxCell>
        <mxCell id="api" value="danangtrip-api&#xa;Laravel REST API" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1">
          <mxGeometry x="510" y="140" width="190" height="90" as="geometry"/>
        </mxCell>
        <mxCell id="db" value="PostgreSQL / Supabase" style="shape=cylinder3d;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#f8cecc;strokeColor=#b85450;" vertex="1" parent="1">
          <mxGeometry x="790" y="40" width="170" height="80" as="geometry"/>
        </mxCell>
        <mxCell id="redis" value="Bảng chat_cache&#xa;Bộ nhớ đệm chatbot" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;" vertex="1" parent="1">
          <mxGeometry x="790" y="150" width="170" height="70" as="geometry"/>
        </mxCell>
        <mxCell id="ai" value="Nhà cung cấp AI&#xa;Gemini / OpenAI" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;" vertex="1" parent="1">
          <mxGeometry x="790" y="250" width="170" height="70" as="geometry"/>
        </mxCell>
        <mxCell id="external" value="Dịch vụ bên ngoài&#xa;Cloudinary / SePay / Brevo" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;" vertex="1" parent="1">
          <mxGeometry x="790" y="350" width="170" height="70" as="geometry"/>
        </mxCell>
        <mxCell id="e1" edge="1" parent="1" source="user" target="web" style="endArrow=block;html=1;rounded=0;"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e2" edge="1" parent="1" source="admin" target="adminweb" style="endArrow=block;html=1;rounded=0;"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e3" edge="1" parent="1" source="web" target="api" style="endArrow=block;html=1;rounded=0;"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e4" edge="1" parent="1" source="adminweb" target="api" style="endArrow=block;html=1;rounded=0;"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e5" edge="1" parent="1" source="api" target="db" style="endArrow=block;html=1;rounded=0;"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e6" edge="1" parent="1" source="api" target="redis" style="endArrow=block;html=1;rounded=0;"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e7" edge="1" parent="1" source="api" target="ai" style="endArrow=block;html=1;rounded=0;"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e8" edge="1" parent="1" source="api" target="external" style="endArrow=block;html=1;rounded=0;"><mxGeometry relative="1" as="geometry"/></mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

### 7.2. Sơ đồ quy trình AI Chatbot

```xml
<mxfile host="app.diagrams.net">
  <diagram name="DanangTrip AI Chatbot Pipeline">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <mxCell id="a" value="Câu hỏi người dùng" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1"><mxGeometry x="40" y="160" width="130" height="60" as="geometry"/></mxCell>
        <mxCell id="b" value="Bộ kiểm soát ý định&#xa;(Intent Guard)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1"><mxGeometry x="220" y="160" width="140" height="60" as="geometry"/></mxCell>
        <mxCell id="c" value="Phân tích truy vấn&#xa;(Query Understanding)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1"><mxGeometry x="410" y="160" width="160" height="60" as="geometry"/></mxCell>
        <mxCell id="d" value="Bộ nhớ đệm&#xa;(Cache Layer)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1"><mxGeometry x="620" y="160" width="140" height="60" as="geometry"/></mxCell>
        <mxCell id="e" value="Truy xuất tri thức kết hợp&#xa;dữ liệu nghiệp vụ và embedding" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;" vertex="1" parent="1"><mxGeometry x="810" y="140" width="210" height="100" as="geometry"/></mxCell>
        <mxCell id="f" value="Nhà cung cấp AI" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;" vertex="1" parent="1"><mxGeometry x="430" y="330" width="150" height="60" as="geometry"/></mxCell>
        <mxCell id="g" value="Chuyển đổi dự phòng&#xa;(AI Failover)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;" vertex="1" parent="1"><mxGeometry x="640" y="330" width="150" height="60" as="geometry"/></mxCell>
        <mxCell id="h" value="Trả phản hồi&#xa;và lưu lịch sử/bộ nhớ đệm" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1"><mxGeometry x="220" y="330" width="160" height="60" as="geometry"/></mxCell>
        <mxCell id="e1" edge="1" parent="1" source="a" target="b" style="endArrow=block;html=1;"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e2" edge="1" parent="1" source="b" target="c" style="endArrow=block;html=1;"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e3" edge="1" parent="1" source="c" target="d" style="endArrow=block;html=1;"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e4" edge="1" parent="1" source="d" target="e" style="endArrow=block;html=1;"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e5" edge="1" parent="1" source="e" target="f" style="endArrow=block;html=1;"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e6" edge="1" parent="1" source="f" target="h" style="endArrow=block;html=1;"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e7" edge="1" parent="1" source="f" target="g" value="nhà cung cấp lỗi / quá thời gian chờ / hết hạn mức" style="endArrow=block;html=1;"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e8" edge="1" parent="1" source="g" target="f" value="chuyển nhà cung cấp/khóa" style="endArrow=block;html=1;"><mxGeometry relative="1" as="geometry"/></mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

### 7.3. Sơ đồ cấu trúc các lớp xử lý chatbot

```xml
<mxfile host="app.diagrams.net">
  <diagram name="DanangTrip Chatbot Services Structure">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <mxCell id="controller" value="ChatController&#xa;(API Handler)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="50" y="150" width="150" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="chatservice" value="ChatService&#xa;(Bộ điều phối luồng)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontStyle=1" vertex="1" parent="1">
          <mxGeometry x="250" y="140" width="170" height="80" as="geometry"/>
        </mxCell>
        <mxCell id="intentguard" value="ChatIntentGuardService&#xa;(Bộ lọc ý định)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1">
          <mxGeometry x="490" y="40" width="180" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="queryunderstanding" value="ChatQueryUnderstandingService&#xa;(Trích xuất tham số)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1">
          <mxGeometry x="490" y="120" width="180" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="searchservice" value="ChatKnowledgeSearchService&#xa;(Tìm kiếm tri thức)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1">
          <mxGeometry x="490" y="200" width="180" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="embeddingservice" value="ChatEmbeddingService&#xa;(Tạo Vector Embedding)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;" vertex="1" parent="1">
          <mxGeometry x="720" y="200" width="180" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="syncservice" value="ChatKnowledgeSyncService&#xa;(Đồng bộ dữ liệu)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;fontColor=#333333;" vertex="1" parent="1">
          <mxGeometry x="720" y="290" width="180" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="aiprovider" value="ChatAiProviderService&#xa;(Gọi LLM &amp; Failover)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1">
          <mxGeometry x="490" y="290" width="180" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="database" value="PostgreSQL DB&#xa;(Tri thức &amp; Nghiệp vụ)" style="shape=cylinder3d;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#e1d5e7;strokeColor=#9673a6;" vertex="1" parent="1">
          <mxGeometry x="730" y="50" width="160" height="80" as="geometry"/>
        </mxCell>
        <mxCell id="e1" edge="1" parent="1" source="controller" target="chatservice" style="endArrow=block;html=1;rounded=0;">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="e2" edge="1" parent="1" source="chatservice" target="intentguard" style="endArrow=block;html=1;rounded=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="e3" edge="1" parent="1" source="chatservice" target="queryunderstanding" style="endArrow=block;html=1;rounded=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="e4" edge="1" parent="1" source="chatservice" target="searchservice" style="endArrow=block;html=1;rounded=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="e5" edge="1" parent="1" source="chatservice" target="aiprovider" style="endArrow=block;html=1;rounded=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="e6" edge="1" parent="1" source="searchservice" target="embeddingservice" style="endArrow=block;html=1;rounded=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="e7" edge="1" parent="1" source="searchservice" target="database" style="endArrow=block;html=1;rounded=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;entrySize=80;">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="e8" edge="1" parent="1" source="syncservice" target="database" style="endArrow=block;html=1;rounded=0;entryX=0.5;entryY=1;entryDx=0;entryDy=0;entrySize=80;exitX=0.5;exitY=0;exitDx=0;exitDy=0;">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="e9" edge="1" parent="1" source="syncservice" target="embeddingservice" style="endArrow=block;html=1;rounded=0;entryX=0.5;entryY=1;entryDx=0;entryDy=0;exitX=0.5;exitY=0;exitDx=0;exitDy=0;">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

