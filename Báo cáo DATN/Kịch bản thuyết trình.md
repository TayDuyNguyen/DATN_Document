# KỊCH BẢN THUYẾT TRÌNH BẢO VỆ ĐỒ ÁN TỐT NGHIỆP
## Đề tài: Xây dựng website du lịch "Da Nang Trip" – Tích hợp hệ thống đánh giá, quản lý nội dung và gợi ý địa điểm dựa trên điểm thưởng

> **Tổng thời gian trình bày:** ~15–20 phút
> **Thời gian Q&A:** ~10–15 phút
> **Người trình bày:** [Tên sinh viên]
> **GVHD:** [Tên giáo viên hướng dẫn]

---

## 📌 LƯU Ý TRƯỚC KHI BẮT ĐẦU

- Đứng thẳng, nhìn hội đồng khi nói – không đọc nguyên văn slide
- Nói rõ ràng, tốc độ vừa phải, tự tin
- Chuẩn bị sẵn con trỏ để chỉ vào sơ đồ khi cần

---

## 🎬 SLIDE 1 – TRANG BÌA

**[Lời nói]:**

> *(Đứng trước hội đồng, gật đầu chào)*

"Kính chào Hội đồng phản biện, kính chào quý Thầy/Cô!

Em tên là **[Tên sinh viên]**, sinh viên **[Khoa/Ngành]**, dưới sự hướng dẫn của **[Thầy/Cô GVHD]**.

Hôm nay em xin trình bày đồ án tốt nghiệp với đề tài:

**'Xây dựng website du lịch Da Nang Trip – Tích hợp hệ thống đánh giá, quản lý nội dung và gợi ý địa điểm dựa trên điểm thưởng'**

Em rất mong nhận được sự đánh giá và góp ý từ Hội đồng."

---

## 🎬 SLIDE 2 – NỘI DUNG BÁO CÁO

**[Lời nói]:**

"Em xin trình bày theo 5 phần chính:

1. **Đặt vấn đề** – Lý do và bài toán cần giải quyết
2. **Mục tiêu đề tài** – Những gì đề tài hướng đến
3. **Kiến trúc và công nghệ** – Cách hệ thống được xây dựng
4. **Demo chức năng** – Các tính năng đã hoàn thành
5. **Kết quả và hướng phát triển** – Đánh giá và những bước tiếp theo

Bây giờ em xin bắt đầu từ phần Đặt vấn đề."

---

## 🎬 SLIDE 3 – ĐẶT VẤN ĐỀ

**[Lời nói]:**

"Đà Nẵng là một trong những điểm du lịch phát triển mạnh nhất Việt Nam. Tuy nhiên qua khảo sát thực tế, em nhận thấy **3 vấn đề người dùng thường gặp**:

**Thứ nhất**, thông tin về địa điểm, nhà hàng, tour du lịch rải rác nhiều nơi, không có một nền tảng tập trung.

**Thứ hai**, gợi ý hiện tại chủ yếu dựa trên lượt xem hoặc danh sách thủ công – chưa cá nhân hóa theo sở thích người dùng.

**Thứ ba**, chưa có cơ chế khuyến khích người dùng tham gia đánh giá và đóng góp nội dung chất lượng.

Từ đó, em đề xuất xây dựng **Da Nang Trip** – một website du lịch tích hợp hệ thống đánh giá, gợi ý thông minh và chương trình điểm thưởng để giải quyết các vấn đề này."

---

## 🎬 SLIDE 4 – MỤC TIÊU ĐỀ TÀI

**[Lời nói]:**

"Đề tài đặt ra **4 mục tiêu cụ thể**:

**Mục tiêu 1:** Xây dựng hệ thống quản lý địa điểm, tour du lịch và nội dung blog đầy đủ.

**Mục tiêu 2:** Tích hợp chức năng đặt tour, thanh toán online qua VietQR và quản lý trạng thái booking.

**Mục tiêu 3:** Xây dựng **hệ thống gợi ý địa điểm** dựa trên lịch sử đánh giá của người dùng, sử dụng mô hình **LightFM** – một thuật toán học máy kết hợp Collaborative Filtering và Matrix Factorization.

**Mục tiêu 4:** Thiết kế **chương trình điểm thưởng** – người dùng được tích điểm khi đặt tour, viết đánh giá, và có thể dùng điểm để đổi ưu đãi, khuyến khích tương tác lâu dài."

---

## 🎬 SLIDE 5 – CƠ SỞ LÝ THUYẾT

**[Lời nói]:**

"Về phần lý thuyết, em tập trung vào **mô hình LightFM** được dùng cho hệ thống gợi ý.

LightFM là thư viện Python chuyên cho bài toán **Collaborative Filtering kết hợp Content-Based** (Hybrid Recommender). Điểm mạnh của LightFM là:

- **Xử lý được Cold Start:** Với người dùng hoặc địa điểm mới chưa có tương tác, LightFM dùng **đặc trưng nội dung** (category, tag, khu vực…) để gợi ý thay vì từ chối
- **Matrix Factorization:** Biểu diễn người dùng và địa điểm thành các vector ẩn (latent factors), học từ dữ liệu đánh giá thực tế
- **Item Similarity:** Tính độ tương đồng giữa các địa điểm dựa trên vector embedding

Hệ thống có **3 loại gợi ý:**
1. Gợi ý cá nhân hóa cho từng user dựa trên lịch sử
2. Địa điểm tương tự (Similar locations)
3. Fallback: địa điểm phổ biến – dùng cho user mới chưa có dữ liệu"

---

## 🎬 SLIDE 6 – KIẾN TRÚC HỆ THỐNG

**[Lời nói]:**

"Về kiến trúc, hệ thống DanangTrip gồm **4 thành phần chính:**

*(Chỉ vào sơ đồ)*

**1. Backend chính – Laravel 12 (PHP):**
Xử lý toàn bộ nghiệp vụ: xác thực JWT, quản lý địa điểm/tour/booking, thanh toán SePay, điểm thưởng, thông báo, chatbot. Kết nối database **PostgreSQL** trên Supabase.

**2. AI Service – FastAPI (Python):**
Service riêng biệt chạy mô hình LightFM. Laravel gọi FastAPI qua HTTP khi cần trả kết quả gợi ý cho người dùng. Tách riêng để không ảnh hưởng đến API chính.

**3. Web người dùng – Next.js (TypeScript):**
Giao diện web cho du khách. Các tính năng chính: tìm kiếm, xem địa điểm/tour, đặt tour, thanh toán, xem gợi ý, tích điểm.

**4. Web quản trị (Admin) – React + Vite (TypeScript):**
Giao diện dành cho quản trị viên: quản lý nội dung, tour, người dùng, đơn đặt, xử lý refund, duyệt đánh giá.

**Cơ sở hạ tầng:** Docker để container hóa, deploy trên Render, database Supabase."

---

## 🎬 SLIDE 7 – CÔNG NGHỆ SỬ DỤNG

**[Lời nói]:**

"Dưới đây là tech stack cụ thể của từng thành phần:

| Thành phần | Công nghệ |
|---|---|
| Backend API | Laravel 12, PHP |
| Database | PostgreSQL (Supabase) |
| AI / Recommender | Python, FastAPI, LightFM |
| Web người dùng | Next.js, TypeScript |
| Web Admin | React 19, Vite, Zustand, TanStack Query |
| Thanh toán | SePay + VietQR |
| Auth | JWT + Refresh Token rotation |
| Deploy | Docker, Render |

Lý do chọn tách AI service riêng: để có thể train lại mô hình, cập nhật thuật toán mà không cần deploy lại toàn bộ backend."

---

## 🎬 SLIDE 8–10 – DEMO CHỨC NĂNG

**[Lời nói – Web người dùng (Next.js)]:**

"Em xin demo các chức năng chính trên **giao diện web người dùng**:

**Trang chủ & Khám phá:**
- Tìm kiếm địa điểm, lọc theo danh mục, quận, đánh giá
- Xem chi tiết địa điểm: hình ảnh, mô tả, amenity, giờ mở cửa, bản đồ

**Hệ thống gợi ý:**
- Section 'Gợi ý cho bạn': hiển thị top địa điểm được mô hình LightFM gợi ý dựa trên lịch sử của user
- Section 'Địa điểm tương tự': khi xem chi tiết một địa điểm, hệ thống gợi ý các địa điểm có vector embedding gần nhất
- Với user mới: fallback về danh sách địa điểm phổ biến

**Đặt tour & Thanh toán:**
- Chọn lịch, số lượng người lớn/trẻ em/em bé
- Tạo booking → nhận mã VietQR → chuyển khoản với nội dung `DNT {booking_code}`
- SePay IPN tự động xác nhận booking khi nhận đủ tiền

**Đánh giá & Điểm thưởng:**
- Người dùng viết đánh giá sau khi đi tour → nhận điểm thưởng
- Điểm tích lũy hiển thị trên profile, có thể dùng cho ưu đãi
- Điểm bị trừ lại nếu hủy booking đã thanh toán

**Chatbot AI (Copilot):**
- Hỗ trợ tư vấn địa điểm, tour theo yêu cầu tự nhiên
- Dùng RAG – tìm kiếm vector trên knowledge base chứa dữ liệu thật của hệ thống"

**[Lời nói – Web Admin (React)]:**

"**Giao diện Admin** cho phép quản trị viên:
- Quản lý địa điểm, tour, lịch khởi hành
- Xem và xử lý đơn đặt tour, xác nhận thanh toán
- Duyệt yêu cầu hoàn tiền (refund) – scan VietQR để chuyển khoản trả lại
- Duyệt đánh giá của người dùng
- Quản lý blog, danh mục, cài đặt hệ thống"

---

## 🎬 SLIDE 11 – ĐÁNH GIÁ KẾT QUẢ

**[Lời nói]:**

"Để đánh giá hệ thống gợi ý, em thực hiện trên **tập dữ liệu đánh giá** của người dùng với phương pháp **K-Fold Cross-Validation**.

Chỉ số đánh giá:
- **Precision@K** và **Recall@K**: đo tỷ lệ gợi ý đúng trong top K địa điểm
- **AUC (Area Under ROC Curve)**: đánh giá tổng thể khả năng xếp hạng của mô hình

*(Trình bày số liệu trên slide)*

So sánh với baseline là **gợi ý ngẫu nhiên** và **gợi ý theo lượt xem**, mô hình LightFM cho kết quả cải thiện rõ rệt – đặc biệt với người dùng đã có ít nhất **3–5 lượt đánh giá**.

Về hệ thống tổng thể: toàn bộ luồng từ đặt tour → thanh toán → xác nhận → hoàn tiền đã được kiểm thử đầy đủ theo các kịch bản thực tế."

---

## 🎬 SLIDE 12 – KẾT QUẢ ĐẠT ĐƯỢC & HẠN CHẾ

**[Lời nói – Kết quả]:**

"Tóm lại, đề tài đã **hoàn thành** các mục tiêu đề ra:

✅ Website du lịch đầy đủ: địa điểm, tour, blog, tìm kiếm, lọc nâng cao

✅ Đặt tour và thanh toán VietQR tự động qua SePay

✅ Hệ thống gợi ý cá nhân hóa với LightFM + fallback cho user mới

✅ Chương trình điểm thưởng tích hợp vào toàn bộ vòng đời booking

✅ Chatbot AI hỗ trợ tư vấn du lịch với RAG và vector search

✅ Web Admin đầy đủ: quản lý nội dung, đơn hàng, hoàn tiền, thống kê"

**[Lời nói – Hạn chế]:**

"Tuy nhiên em cũng thành thật nhận thấy **một số hạn chế**:

⚠️ **Cold Start với user hoàn toàn mới:** Mặc dù LightFM hỗ trợ item features, nhưng với user chưa có bất kỳ tương tác nào, hệ thống chỉ trả về danh sách phổ biến – chưa thực sự cá nhân hóa

⚠️ **Dữ liệu đánh giá còn hạn chế:** Hệ thống mới nên số lượng rating thực tế chưa nhiều, ảnh hưởng đến chất lượng mô hình

⚠️ **Chưa có ứng dụng di động:** Hiện tại chỉ có web, chưa có native mobile app"

---

## 🎬 SLIDE 13 – HƯỚNG PHÁT TRIỂN

**[Lời nói]:**

"Với những hạn chế trên, em đề xuất một số hướng phát triển:

**Ngắn hạn:**
- Bổ sung bước onboarding cho user mới: chọn sở thích → có dữ liệu khởi đầu cho gợi ý ngay từ đầu
- Thu thập thêm dữ liệu implicit (lịch sử xem, yêu thích) để cải thiện chất lượng gợi ý

**Trung hạn:**
- Phát triển **mobile app** (React Native hoặc Flutter) để tiếp cận người dùng di động
- Nâng cấp chatbot: hỗ trợ đặt tour trực tiếp qua chat, không cần vào trang tour

**Dài hạn:**
- Mở rộng phủ sóng ra ngoài Đà Nẵng – các tỉnh thành du lịch lớn khác
- Tích hợp thêm đối tác: khách sạn, phương tiện, dịch vụ địa phương"

---

## 🎬 SLIDE 14 – KẾT LUẬN & CẢM ƠN

**[Lời nói]:**

"Kính thưa Hội đồng,

Qua quá trình thực hiện đồ án, em đã xây dựng được một hệ thống du lịch có đầy đủ tính năng thực tế: từ quản lý nội dung, đặt tour, thanh toán, đến gợi ý thông minh và chương trình khách hàng thân thiết.

Điểm nổi bật của đề tài là sự **kết hợp giữa nghiệp vụ thực tế** (booking, payment, refund) và **ứng dụng học máy** (LightFM recommender, chatbot RAG) vào một sản phẩm có thể triển khai thực tế.

Em xin chân thành cảm ơn **Thầy/Cô [Tên GVHD]** đã hướng dẫn tận tình trong suốt quá trình. Em cũng cảm ơn Hội đồng đã dành thời gian lắng nghe và đánh giá đề tài.

**Em xin hết. Kính mời Hội đồng đặt câu hỏi ạ!**"

---

# ❓ PHẦN DỰ PHÒNG – CÂU HỎI HAY GẶP

---

### ❓ CÂU HỎI 1: LightFM là gì? Tại sao chọn nó thay vì tự cài CF thuần?

**Trả lời:**
"Thưa Thầy/Cô, LightFM là thư viện Python chuyên cho hệ thống gợi ý, cài đặt thuật toán **Hybrid Collaborative Filtering + Content-Based** bằng Matrix Factorization.

Em chọn LightFM vì:
- Nó giải quyết được **Cold Start** – điểm yếu của CF thuần, bằng cách sử dụng thêm đặc trưng nội dung (category, tag…)
- Tích hợp sẵn nhiều loss function (WARP, BPR, logistic) phù hợp cho implicit feedback
- Thư viện ổn định, có tài liệu và benchmark rõ ràng
- Thời gian implement nhanh hơn so với tự xây từ đầu, phù hợp quy mô đồ án"

---

### ❓ CÂU HỎI 2: Cold Start xử lý như thế nào?

**Trả lời:**
"Thưa Thầy/Cô, đây là hạn chế em đã thừa nhận trong slide.

Hiện tại em xử lý theo **3 tầng fallback:**

1. Nếu user có đủ rating → dùng LightFM gợi ý cá nhân hóa
2. Nếu user mới, chưa có rating → trả về **Popular Fallback**: danh sách địa điểm phổ biến nhất theo view count và avg_rating
3. Với gợi ý 'Similar': dùng item embedding của LightFM – không cần dữ liệu user

Hướng cải thiện: bổ sung màn onboarding, để user mới chọn sở thích ngay từ đầu."

---

### ❓ CÂU HỎI 3: Thanh toán VietQR hoạt động như thế nào? Có an toàn không?

**Trả lời:**
"Thưa Thầy/Cô, luồng thanh toán hoạt động như sau:

1. User tạo booking → API sinh mã QR chứa nội dung chuyển khoản `DNT {booking_code}`
2. User chuyển khoản qua ngân hàng với đúng nội dung
3. SePay nhận giao dịch → gửi IPN (webhook) về API
4. API xác minh chữ ký, khớp booking_code và số tiền → cập nhật trạng thái booking

Về bảo mật: giao tiếp qua HTTPS, xác minh IPN signature, idempotent – nhận nhiều lần cũng không confirm hai lần."

---

### ❓ CÂU HỎI 4: Chatbot dùng kỹ thuật gì? Có khác gì ChatGPT thông thường?

**Trả lời:**
"Thưa Thầy/Cô, chatbot trong hệ thống dùng kỹ thuật **RAG – Retrieval-Augmented Generation**:

- Dữ liệu địa điểm, tour, blog của hệ thống được lưu thành knowledge base và **vector hóa** bằng Gemini Embedding
- Khi user hỏi, hệ thống tìm các đoạn thông tin liên quan nhất theo độ tương đồng vector
- Thông tin đó được đưa vào prompt gửi cho LLM → LLM trả lời dựa trên **dữ liệu thật của hệ thống**

Điểm khác biệt so với ChatGPT thông thường: chatbot chỉ biết về dữ liệu DanangTrip, không hallucinate thông tin bên ngoài, câu trả lời chính xác và cập nhật theo dữ liệu thật."

---

### ❓ CÂU HỎI 5: Hệ thống điểm thưởng hoạt động thế nào? Có tránh được gian lận không?

**Trả lời:**
"Thưa Thầy/Cô, người dùng tích điểm qua các hành động: đặt tour thành công, viết đánh giá được duyệt. Điểm bị trừ lại nếu hủy booking đã thanh toán.

Để tránh gian lận:
- Điểm chỉ được cộng sau khi admin **duyệt đánh giá** – tránh đánh giá spam
- Mỗi user-location chỉ được đánh giá **một lần** (unique constraint)
- Hủy booking trước ngày khởi hành sẽ **hoàn tiền theo chính sách** và đồng thời **thu hồi điểm** đã cộng"

---

### ❓ CÂU HỎI 6: Tại sao chọn Next.js cho web người dùng, còn Admin lại dùng React + Vite?

**Trả lời:**
"Thưa Thầy/Cô, đây là lựa chọn phù hợp với mục đích từng phần:

**Next.js cho web người dùng:**
- Hỗ trợ **Server-Side Rendering (SSR)** và **Static Generation** – tốt cho SEO, địa điểm du lịch cần được index bởi Google
- Routing file-based, middleware auth tích hợp sẵn

**React + Vite cho Admin:**
- Admin dashboard không cần SEO
- Vite cho phép build cực nhanh, HMR tốt khi phát triển
- React với TanStack Query và Zustand đủ để quản lý state phức tạp của dashboard"

---

*Hết kịch bản thuyết trình*

---

> **Nhắc nhở cuối:** Sau mỗi câu trả lời Q&A, kết thúc bằng: *"Em xin hết ạ. Thầy/Cô có câu hỏi thêm không ạ?"*
