# PHỤ LỤC: GỢI Ý HÌNH ẢNH, BẢNG BIỂU VÀ BIỂU ĐỒ

## 1. Danh mục hình ảnh đề xuất

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

## 2. Danh mục bảng biểu đề xuất

| STT | Tên bảng | Vị trí gợi ý |
| --- | --- | --- |
| 1 | Bảng công nghệ sử dụng | Mở đầu |
| 2 | Bảng tác nhân hệ thống | Chương 2 |
| 3 | Bảng yêu cầu phi chức năng | Chương 2 |
| 4 | Bảng đặc tả ca sử dụng đăng nhập | Chương 2 |
| 5 | Bảng đặc tả ca sử dụng đặt tour | Chương 2 |
| 6 | Bảng đặc tả ca sử dụng thanh toán | Chương 2 |
| 7 | Bảng thực thể cơ sở dữ liệu | Chương 2 |
| 8 | Bảng đường dẫn website người dùng | Chương 3 |
| 9 | Bảng đường dẫn trang quản trị | Chương 3 |
| 10 | Bảng kết quả kiểm thử | Chương 3 |

## 3. Biểu đồ nên vẽ lại cho báo cáo Word

### 3.1. Biểu đồ kiến trúc tổng thể

Nên vẽ gồm các khối: Website người dùng, Trang quản trị, Laravel API, Cơ sở dữ liệu, Redis, Cloudinary, SePay, Dịch vụ email, Nhà cung cấp AI.

### 3.2. Biểu đồ use case tổng quan

Nên tách ba actor: Khách truy cập, Người dùng, Quản trị viên.

### 3.3. Biểu đồ tuần tự đặt tour và thanh toán

Nên thể hiện các đối tượng: Người dùng, Website, Laravel API, Database, SePay.

### 3.4. ERD cơ sở dữ liệu

Nên tập trung vào nhóm bảng chính để tránh quá rối:

- `users`
- `locations`, `categories`, `tags`, `amenities`
- `tours`, `tour_categories`, `tour_schedules`
- `bookings`, `booking_items`, `payments`
- `ratings`, `favorites`, `notifications`
- `blog_posts`, `promotions`, `settings`
- `chat_messages`, `chat_knowledge_base`

## 4. Mẫu bảng kết quả kiểm thử

| STT | Chức năng | Trường hợp kiểm thử | Kết quả mong đợi | Kết quả thực tế | Trạng thái |
| --- | --- | --- | --- | --- | --- |
| 1 | Đăng nhập | Nhập đúng email/mật khẩu | Đăng nhập thành công | Chưa kiểm thử thủ công | Cần kiểm thử giao diện |
| 2 | Tìm kiếm | Nhập từ khóa "Bà Nà" | Hiển thị địa điểm/tour liên quan | Chưa kiểm thử thủ công | Cần kiểm thử giao diện |
| 3 | Đặt tour | Chọn lịch còn chỗ và xác nhận | Tạo đơn đặt tour thành công | Chưa kiểm thử thủ công | Cần kiểm thử giao diện/API |
| 4 | Thanh toán | Thanh toán đúng nội dung chuyển khoản | Thanh toán và đơn đặt tour cập nhật thành công | Cần kiểm thử với payload SePay thật | Cần kiểm thử thanh toán |
| 5 | Quản trị tour | Quản trị viên thêm tour mới | Tour xuất hiện trong danh sách | Chưa kiểm thử thủ công | Cần kiểm thử giao diện/API |
| 6 | Duyệt đánh giá | Quản trị viên duyệt đánh giá | Đánh giá hiển thị công khai | Chưa kiểm thử thủ công | Cần kiểm thử giao diện/API |
| 7 | Chatbot | Hỏi tour phù hợp ngân sách | Chatbot trả lời theo dữ liệu hệ thống | Cần kiểm thử với nhà cung cấp AI thật | Cần kiểm thử AI |
| 8 | Chatbot | Hỏi câu ngoài phạm vi du lịch | Intent Guard từ chối hoặc hướng dẫn hỏi lại | Đã có xử lý trong `ChatIntentGuardService`, cần kiểm thử API | Một phần |
| 9 | Chatbot | Giả lập nhà cung cấp AI lỗi | AI Failover hoặc phản hồi dự phòng hoạt động | Đã có xử lý trong `ChatAiProviderService`, cần kiểm thử giả lập | Một phần |

## 5. Checklist phần còn thiếu cần bổ sung thủ công

Để báo cáo đủ tốt khi nộp, cần bổ sung thêm các nội dung sau:

- Ảnh chụp giao diện thật của website người dùng và trang quản trị.
- Sơ đồ ERD vẽ bằng draw.io/Figma/PlantUML dựa trên bảng dữ liệu.
- Biểu đồ use case tổng quan và phân rã theo từng tác nhân.
- Biểu đồ tuần tự cho các chức năng: đăng nhập, đặt tour, thanh toán, chatbot.
- Biểu đồ hoạt động cho các chức năng: tìm kiếm, đặt tour, quản trị tour, duyệt đánh giá.
- Bảng mô tả chi tiết các bảng dữ liệu chính.
- Bảng trường hợp kiểm thử có kết quả thật sau khi chạy kiểm thử.
- Liên kết hoặc ảnh minh họa kiểm thử API bằng Postman/Swagger nếu có.
- Ảnh minh họa cơ sở dữ liệu hoặc migration nếu giáo viên yêu cầu.
- Ảnh minh họa kết quả đóng gói/kiểm thử đạt.
- Bảng mô tả đầu vào/đầu ra của quy trình AI Chatbot.
- Ví dụ truy vấn chatbot với dữ liệu thật lấy từ cơ sở dữ liệu.
- Bảng môi trường triển khai thực tế.

## 6. Gợi ý phụ lục API

Khi báo cáo chính quá dài, có thể đưa danh sách API vào phụ lục:

| Nhóm API | Endpoint tiêu biểu |
| --- | --- |
| Auth | `POST /auth/register`, `POST /auth/login`, `POST /auth/refresh`, `POST /auth/logout` |
| Home | `GET /home`, `GET /home/locations`, `GET /home/tours`, `GET /home/blogs` |
| Locations | `GET /locations`, `GET /locations/{slug}`, `GET /locations/{id}/ratings` |
| Tours | `GET /tours`, `GET /tours/{slug}`, `GET /tours/{id}/schedules` |
| Đặt tour | `POST /bookings/calculate`, `POST /bookings`, `GET /user/bookings` |
| Thanh toán | `POST /payments/create`, `GET /payments/status/{transaction_code}`, `POST /sepay/ipn` |
| Cart | `GET /cart`, `POST /cart/items`, `PUT /cart/items/{id}`, `DELETE /cart` |
| Rating | `POST /ratings`, `PUT /ratings/{id}`, `DELETE /ratings/{id}` |
| Bảng điều khiển quản trị | `GET /admin/dashboard`, `GET /admin/dashboard/revenue`, `GET /admin/reports/bookings` |
| Quản trị tour | `GET /admin/tours`, `POST /admin/tours`, `PUT /admin/tours/{id}` |
| Quản trị địa điểm | `GET /admin/locations`, `POST /admin/locations`, `PUT /admin/locations/{id}` |
| Quản trị đơn đặt tour | `GET /admin/bookings`, `PATCH /admin/bookings/{id}/status` |

### 6.1. Gợi ý phụ lục quy trình AI Chatbot

| Thành phần | Nội dung cần chứng minh trong báo cáo |
| --- | --- |
| Intent Guard | Ví dụ câu hỏi hợp lệ và câu hỏi ngoài phạm vi; kết quả phân loại |
| Query Understanding | Ví dụ trích xuất `destination`, `price`, `people`, `date`, `duration` |
| SQL RAG | Bảng dữ liệu hoặc truy vấn SQL/nhật ký truy xuất tour, địa điểm, chính sách |
| Cache Layer | Cách xác định khóa bộ nhớ đệm; ví dụ có dữ liệu/không có dữ liệu trong bộ nhớ đệm |
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
        <mxCell id="redis" value="Redis&#xa;Cache / Queue" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;" vertex="1" parent="1">
          <mxGeometry x="790" y="150" width="170" height="70" as="geometry"/>
        </mxCell>
        <mxCell id="ai" value="Nhà cung cấp AI&#xa;Gemini / OpenAI" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;" vertex="1" parent="1">
          <mxGeometry x="790" y="250" width="170" height="70" as="geometry"/>
        </mxCell>
        <mxCell id="external" value="Cloudinary / SePay / Mail" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;" vertex="1" parent="1">
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
        <mxCell id="b" value="Intent Guard" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1"><mxGeometry x="220" y="160" width="140" height="60" as="geometry"/></mxCell>
        <mxCell id="c" value="Query Understanding" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1"><mxGeometry x="410" y="160" width="160" height="60" as="geometry"/></mxCell>
        <mxCell id="d" value="Bộ nhớ đệm&#xa;(Cache Layer)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1"><mxGeometry x="620" y="160" width="140" height="60" as="geometry"/></mxCell>
        <mxCell id="e" value="SQL RAG&#xa;tours, schedules, locations, blogs, policies" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;" vertex="1" parent="1"><mxGeometry x="810" y="140" width="210" height="100" as="geometry"/></mxCell>
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
