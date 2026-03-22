# Test Cases — SEARCH (Tìm kiếm)

> Base URL: `http://localhost:8000/api/v1`
> Tất cả API Search đều là 🌐 Public — không cần token

---

## 1. GET /search — Tìm kiếm địa điểm

### ✅ TC01 — Từ khóa hợp lệ, có kết quả
```http
GET /api/v1/search?q=hải sản
```
- Expected: `200 OK`, `data` là array, `meta.total > 0`

### ✅ TC02 — Từ khóa hợp lệ, không có kết quả
```http
GET /api/v1/search?q=xyzkhongcokq123
```
- Expected: `200 OK`, `data` là array rỗng, `meta.total = 0`

### ✅ TC03 — Kết hợp filter `category_id`
```http
GET /api/v1/search?q=quán&category_id=1
```
- Expected: `200 OK`, tất cả kết quả thuộc `category_id = 1`

### ✅ TC04 — Kết hợp filter `district`
```http
GET /api/v1/search?q=cà phê&district=Hải Châu
```
- Expected: `200 OK`, tất cả kết quả có `district = Hải Châu`

### ✅ TC05 — Kết hợp filter `price_level`
```http
GET /api/v1/search?q=nhà hàng&price_level=2
```
- Expected: `200 OK`, tất cả kết quả có `price_level = 2`

### ✅ TC06 — Kết hợp filter `price_min` và `price_max`
```http
GET /api/v1/search?q=buffet&price_min=100000&price_max=500000
```
- Expected: `200 OK`, kết quả nằm trong khoảng giá

### ✅ TC07 — Kết hợp filter `rating_min`
```http
GET /api/v1/search?q=resort&rating_min=4.0
```
- Expected: `200 OK`, tất cả kết quả có `avg_rating >= 4.0`

### ✅ TC08 — Sort theo `avg_rating` giảm dần
```http
GET /api/v1/search?q=khách sạn&sort=avg_rating&order=desc
```
- Expected: `200 OK`, kết quả sắp xếp `avg_rating` từ cao xuống thấp

### ✅ TC09 — Sort theo `view_count` tăng dần
```http
GET /api/v1/search?q=biển&sort=view_count&order=asc
```
- Expected: `200 OK`, kết quả sắp xếp `view_count` từ thấp lên cao

### ✅ TC10 — Phân trang `page=2`
```http
GET /api/v1/search?q=ăn&page=2&per_page=5
```
- Expected: `200 OK`, `meta.current_page = 2`, `data` có tối đa 5 phần tử

### ✅ TC11 — Truyền `session_id` (ghi log cho guest)
```http
GET /api/v1/search?q=hải sản&session_id=sess_abc123
```
- Expected: `200 OK`, ghi vào `search_logs` với `session_id = sess_abc123`

### ✅ TC12 — Kết hợp nhiều filter cùng lúc
```http
GET /api/v1/search?q=nhà hàng&category_id=1&district=Sơn Trà&price_level=2&sort=avg_rating&order=desc&page=1&per_page=10
```
- Expected: `200 OK`, kết quả thỏa tất cả điều kiện

### ❌ TC13 — Thiếu `q`
```http
GET /api/v1/search
```
- Expected: `422 Unprocessable`, lỗi validation `q required`

### ❌ TC14 — `q` quá ngắn (1 ký tự)
```http
GET /api/v1/search?q=a
```
- Expected: `422 Unprocessable`, lỗi `q phải có ít nhất 2 ký tự`

### ❌ TC15 — `price_level` sai giá trị
```http
GET /api/v1/search?q=nhà hàng&price_level=9
```
- Expected: `422 Unprocessable`, lỗi `price_level phải là 1, 2, 3 hoặc 4`

### ❌ TC16 — `sort` sai giá trị
```http
GET /api/v1/search?q=nhà hàng&sort=invalid_field
```
- Expected: `422 Unprocessable`, lỗi `sort không hợp lệ`

### ❌ TC17 — `order` sai giá trị
```http
GET /api/v1/search?q=nhà hàng&order=random
```
- Expected: `422 Unprocessable`, lỗi `order phải là asc hoặc desc`

### ❌ TC18 — `per_page` vượt quá max (100)
```http
GET /api/v1/search?q=nhà hàng&per_page=200
```
- Expected: `422 Unprocessable`, lỗi `per_page tối đa 100`

### ❌ TC19 — `rating_min` ngoài khoảng 0-5
```http
GET /api/v1/search?q=nhà hàng&rating_min=6
```
- Expected: `422 Unprocessable`, lỗi `rating_min phải từ 0 đến 5`

---

## 2. GET /search/suggestions — Gợi ý tìm kiếm

### ✅ TC20 — Từ khóa hợp lệ, có gợi ý
```http
GET /api/v1/search/suggestions?q=bé m
```
- Expected: `200 OK`, `data` là array, mỗi phần tử có `id`, `name`, `slug`, `district`

### ✅ TC21 — Từ khóa không khớp địa điểm nào
```http
GET /api/v1/search/suggestions?q=xyzkhongco
```
- Expected: `200 OK`, `data` là array rỗng

### ✅ TC22 — Giới hạn `limit`
```http
GET /api/v1/search/suggestions?q=nhà&limit=3
```
- Expected: `200 OK`, `data` có tối đa 3 phần tử

### ✅ TC23 — Không truyền `limit` (dùng default)
```http
GET /api/v1/search/suggestions?q=nhà
```
- Expected: `200 OK`, `data` có tối đa 5 phần tử (default)

### ✅ TC24 — Không ghi vào `search_logs`
```http
GET /api/v1/search/suggestions?q=nhà hàng
```
- Expected: `200 OK`, bảng `search_logs` không tăng thêm record

### ❌ TC25 — Thiếu `q`
```http
GET /api/v1/search/suggestions
```
- Expected: `422 Unprocessable`, lỗi `q required`

### ❌ TC26 — `limit` vượt max (20)
```http
GET /api/v1/search/suggestions?q=nhà&limit=50
```
- Expected: `422 Unprocessable`, lỗi `limit tối đa 20`

### ❌ TC27 — `limit` không phải số
```http
GET /api/v1/search/suggestions?q=nhà&limit=abc
```
- Expected: `422 Unprocessable`, lỗi `limit phải là số nguyên`

---

## 3. GET /search/popular — Từ khóa phổ biến

### ✅ TC28 — Lấy danh sách mặc định
```http
GET /api/v1/search/popular
```
- Expected: `200 OK`, `data` là array, mỗi phần tử có `query` và `count`

### ✅ TC29 — Giới hạn `limit`
```http
GET /api/v1/search/popular?limit=5
```
- Expected: `200 OK`, `data` có tối đa 5 phần tử

### ✅ TC30 — Lọc theo `days`
```http
GET /api/v1/search/popular?days=7
```
- Expected: `200 OK`, `meta.period_days = 7`, chỉ tính trong 7 ngày gần nhất

### ✅ TC31 — Kết quả sắp xếp theo `count` giảm dần
```http
GET /api/v1/search/popular?limit=10
```
- Expected: `200 OK`, `data[0].count >= data[1].count >= ...`

### ✅ TC32 — Không có dữ liệu search_logs (DB trống)
```http
GET /api/v1/search/popular
```
- Expected: `200 OK`, `data` là array rỗng

### ❌ TC33 — `limit` vượt max (50)
```http
GET /api/v1/search/popular?limit=100
```
- Expected: `422 Unprocessable`, lỗi `limit tối đa 50`

### ❌ TC34 — `days` không phải số nguyên dương
```http
GET /api/v1/search/popular?days=-1
```
- Expected: `422 Unprocessable`, lỗi `days phải là số nguyên dương`

---

## Tổng kết

| TC | API | Trường hợp | Expected |
|----|-----|-----------|----------|
| TC01 | GET /search | Từ khóa hợp lệ, có kết quả | 200 |
| TC02 | GET /search | Từ khóa không có kết quả | 200 |
| TC03 | GET /search | Filter category_id | 200 |
| TC04 | GET /search | Filter district | 200 |
| TC05 | GET /search | Filter price_level | 200 |
| TC06 | GET /search | Filter price_min & price_max | 200 |
| TC07 | GET /search | Filter rating_min | 200 |
| TC08 | GET /search | Sort avg_rating desc | 200 |
| TC09 | GET /search | Sort view_count asc | 200 |
| TC10 | GET /search | Phân trang page=2 | 200 |
| TC11 | GET /search | Truyền session_id | 200 |
| TC12 | GET /search | Kết hợp nhiều filter | 200 |
| TC13 | GET /search | Thiếu q | 422 |
| TC14 | GET /search | q quá ngắn (1 ký tự) | 422 |
| TC15 | GET /search | price_level sai giá trị | 422 |
| TC16 | GET /search | sort sai giá trị | 422 |
| TC17 | GET /search | order sai giá trị | 422 |
| TC18 | GET /search | per_page vượt max (100) | 422 |
| TC19 | GET /search | rating_min ngoài khoảng | 422 |
| TC20 | GET /search/suggestions | Có gợi ý | 200 |
| TC21 | GET /search/suggestions | Không khớp | 200 |
| TC22 | GET /search/suggestions | Giới hạn limit | 200 |
| TC23 | GET /search/suggestions | Default limit | 200 |
| TC24 | GET /search/suggestions | Không ghi search_logs | 200 |
| TC25 | GET /search/suggestions | Thiếu q | 422 |
| TC26 | GET /search/suggestions | limit vượt max (20) | 422 |
| TC27 | GET /search/suggestions | limit không phải số | 422 |
| TC28 | GET /search/popular | Lấy mặc định | 200 |
| TC29 | GET /search/popular | Giới hạn limit | 200 |
| TC30 | GET /search/popular | Lọc theo days | 200 |
| TC31 | GET /search/popular | Sắp xếp count desc | 200 |
| TC32 | GET /search/popular | DB trống | 200 |
| TC33 | GET /search/popular | limit vượt max (50) | 422 |
| TC34 | GET /search/popular | days âm | 422 |
