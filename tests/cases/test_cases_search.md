# Test Cases — SEARCH (Tìm kiếm)

> Base URL: `http://localhost:8000/api/v1`
> Branch: `feat/taynd/api-search`
> 🌐 Public (không cần token) | 🔐 User token cho `/recommendations`

---

## 1. GET /search — Tìm kiếm địa điểm & tour

### ✅ TC01 — Từ khóa hợp lệ, có kết quả
```http
GET /api/v1/search?q=đà nẵng
```
- Expected: `200 OK`, `data` là array, mỗi item có `id`, `name`, `slug`

### ✅ TC02 — Từ khóa không có kết quả
```http
GET /api/v1/search?q=xyzkhongcokq999abc
```
- Expected: `200 OK`, `data` là array rỗng

### ✅ TC03 — Filter `type=location`
```http
GET /api/v1/search?q=đà nẵng&type=location
```
- Expected: `200 OK`, tất cả kết quả là location

### ✅ TC04 — Filter `type=tour`
```http
GET /api/v1/search?q=tour&type=tour
```
- Expected: `200 OK`, tất cả kết quả là tour

### ✅ TC05 — Filter `category_id`
```http
GET /api/v1/search?q=đà nẵng&category_id=1
```
- Expected: `200 OK`

### ✅ TC06 — Filter `district`
```http
GET /api/v1/search?q=quán&district=Hải Châu
```
- Expected: `200 OK`

### ✅ TC07 — Filter `price_min` và `price_max`
```http
GET /api/v1/search?q=tour&price_min=100000&price_max=1000000
```
- Expected: `200 OK`

### ✅ TC08 — Sort `avg_rating` desc
```http
GET /api/v1/search?q=đà nẵng&sort=avg_rating&order=desc
```
- Expected: `200 OK`, `avg_rating` item đầu >= item cuối

### ✅ TC09 — Sort `price` asc
```http
GET /api/v1/search?q=tour&sort=price&order=asc
```
- Expected: `200 OK`

### ✅ TC10 — Phân trang `per_page=5`
```http
GET /api/v1/search?q=đà nẵng&page=1&per_page=5
```
- Expected: `200 OK`, `data` có tối đa 5 phần tử

### ✅ TC11 — Truyền `session_id` (ghi log cho guest)
```http
GET /api/v1/search?q=biển&session_id=sess_test_123
```
- Expected: `200 OK`, ghi vào `search_logs` với `session_id`

### ✅ TC12 — Kết hợp nhiều filter
```http
GET /api/v1/search?q=đà nẵng&type=location&sort=avg_rating&order=desc&page=1&per_page=10
```
- Expected: `200 OK`

### ✅ TC13 — User đã đăng nhập (ghi log với user_id)
```http
GET /api/v1/search?q=tour biển
Authorization: Bearer {user_token}
```
- Expected: `200 OK`, ghi `search_logs` với `user_id`

### ❌ TC14 — Thiếu `q`
```http
GET /api/v1/search
```
- Expected: `422 Unprocessable`

### ❌ TC15 — `q` quá ngắn (1 ký tự)
```http
GET /api/v1/search?q=a
```
- Expected: `200 OK` hoặc `422 Unprocessable`
- Note: tùy backend có validate min length không

### ❌ TC16 — `type` sai giá trị
```http
GET /api/v1/search?q=test&type=invalid_type
```
- Expected: `422 Unprocessable`

### ❌ TC17 — `sort` sai giá trị
```http
GET /api/v1/search?q=test&sort=invalid_field
```
- Expected: `200 OK` hoặc `422 Unprocessable`

### ❌ TC18 — `order` sai giá trị
```http
GET /api/v1/search?q=test&order=random
```
- Expected: `422 Unprocessable`

### ❌ TC19 — `per_page` vượt max
```http
GET /api/v1/search?q=test&per_page=200
```
- Expected: `200 OK` hoặc `422 Unprocessable`

---

## 2. GET /search/suggestions — Gợi ý autocomplete

### ✅ TC20 — Có gợi ý
```http
GET /api/v1/search/suggestions?q=bà nà
```
- Expected: `200 OK`, `data` là array, mỗi item có `id`, `name`, `slug`

### ✅ TC21 — Không khớp → array rỗng
```http
GET /api/v1/search/suggestions?q=xyzkhongco999
```
- Expected: `200 OK`, `data = []`

### ✅ TC22 — Giới hạn `limit=3`
```http
GET /api/v1/search/suggestions?q=đà&limit=3
```
- Expected: `200 OK`, `data` có tối đa 3 phần tử

### ✅ TC23 — Default limit (không truyền)
```http
GET /api/v1/search/suggestions?q=đà
```
- Expected: `200 OK`, `data` có tối đa 5 phần tử (default)

### ❌ TC24 — Thiếu `q`
```http
GET /api/v1/search/suggestions
```
- Expected: `422 Unprocessable`

### ❌ TC25 — `limit` vượt max
```http
GET /api/v1/search/suggestions?q=đà&limit=100
```
- Expected: `200 OK` hoặc `422 Unprocessable`

### ❌ TC26 — `limit` không phải số
```http
GET /api/v1/search/suggestions?q=đà&limit=abc
```
- Expected: `422 Unprocessable`

---

## 3. GET /search/popular — Từ khóa phổ biến

### ✅ TC27 — Lấy danh sách mặc định
```http
GET /api/v1/search/popular
```
- Expected: `200 OK`, `data` là array, mỗi item có `query` và `count`

### ✅ TC28 — Giới hạn `limit=5`
```http
GET /api/v1/search/popular?limit=5
```
- Expected: `200 OK`, `data` có tối đa 5 phần tử

### ✅ TC29 — Filter `days=7`
```http
GET /api/v1/search/popular?days=7
```
- Expected: `200 OK`, chỉ tính trong 7 ngày gần nhất

### ✅ TC30 — Sắp xếp `count` desc
```http
GET /api/v1/search/popular?limit=10
```
- Expected: `200 OK`, `count` item đầu >= item sau

### ❌ TC31 — `limit` vượt max
```http
GET /api/v1/search/popular?limit=200
```
- Expected: `200 OK` hoặc `422 Unprocessable`

### ❌ TC32 — `days` âm
```http
GET /api/v1/search/popular?days=-1
```
- Expected: `422 Unprocessable`

### ❌ TC33 — `days=0` (edge case)
```http
GET /api/v1/search/popular?days=0
```
- Expected: `200 OK` hoặc `422 Unprocessable`

---

## 4. GET /search/trending — Xu hướng tìm kiếm

### ✅ TC34 — Lấy xu hướng hiện tại (24h)
```http
GET /api/v1/search/trending
```
- Expected: `200 OK`, `data` là array, mỗi item có `query` và `count`

### ✅ TC35 — Giới hạn `limit=5`
```http
GET /api/v1/search/trending?limit=5
```
- Expected: `200 OK`, `data` có tối đa 5 phần tử

### ❌ TC36 — `limit` vượt max
```http
GET /api/v1/search/trending?limit=200
```
- Expected: `200 OK` hoặc `422 Unprocessable`

### ❌ TC37 — `limit` không phải số
```http
GET /api/v1/search/trending?limit=abc
```
- Expected: `422 Unprocessable`

---

## 5. GET /statistics — Thống kê tổng quan

### ✅ TC38 — Lấy thống kê thành công
```http
GET /api/v1/statistics
```
- Expected: `200 OK`
- Verify: response có các field `locations`, `tours`, `blog_posts` (hoặc tương đương)

### ✅ TC39 — Không cần token (public)
```http
GET /api/v1/statistics
```
- Expected: `200 OK` (không cần Authorization header)

---

## 6. GET /recommendations — Gợi ý cá nhân hóa

### ✅ TC40 — User đã đăng nhập
```http
GET /api/v1/recommendations
Authorization: Bearer {user_token}
```
- Expected: `200 OK`, `data` là array địa điểm/tour gợi ý

### ✅ TC41 — Có `limit=5`
```http
GET /api/v1/recommendations?limit=5
Authorization: Bearer {user_token}
```
- Expected: `200 OK`, `data` có tối đa 5 phần tử

### ❌ TC42 — `limit` vượt max
```http
GET /api/v1/recommendations?limit=200
```
- Expected: `200 OK` hoặc `422 Unprocessable`

### ❌ TC43 — Không có token → 401
```http
GET /api/v1/recommendations
```
- Expected: `401 Unauthorized`

### ❌ TC44 — Token sai → 401
```http
GET /api/v1/recommendations
Authorization: Bearer invalid_token_xyz
```
- Expected: `401 Unauthorized`

---

## Tổng kết

| TC | API | Trường hợp | Expected |
|----|-----|-----------|----------|
| TC01 | GET /search | Từ khóa có kết quả | 200 |
| TC02 | GET /search | Từ khóa không có kết quả | 200 |
| TC03 | GET /search | Filter type=location | 200 |
| TC04 | GET /search | Filter type=tour | 200 |
| TC05 | GET /search | Filter category_id | 200 |
| TC06 | GET /search | Filter district | 200 |
| TC07 | GET /search | Filter price_min & price_max | 200 |
| TC08 | GET /search | Sort avg_rating desc | 200 |
| TC09 | GET /search | Sort price asc | 200 |
| TC10 | GET /search | Phân trang per_page=5 | 200 |
| TC11 | GET /search | Truyền session_id | 200 |
| TC12 | GET /search | Kết hợp nhiều filter | 200 |
| TC13 | GET /search | User đăng nhập | 200 |
| TC14 | GET /search | Thiếu q | 422 |
| TC15 | GET /search | q quá ngắn | 200/422 |
| TC16 | GET /search | type sai giá trị | 422 |
| TC17 | GET /search | sort sai giá trị | 200/422 |
| TC18 | GET /search | order sai giá trị | 422 |
| TC19 | GET /search | per_page vượt max | 200/422 |
| TC20 | GET /search/suggestions | Có gợi ý | 200 |
| TC21 | GET /search/suggestions | Không khớp | 200 |
| TC22 | GET /search/suggestions | limit=3 | 200 |
| TC23 | GET /search/suggestions | Default limit | 200 |
| TC24 | GET /search/suggestions | Thiếu q | 422 |
| TC25 | GET /search/suggestions | limit vượt max | 200/422 |
| TC26 | GET /search/suggestions | limit không phải số | 422 |
| TC27 | GET /search/popular | Lấy mặc định | 200 |
| TC28 | GET /search/popular | limit=5 | 200 |
| TC29 | GET /search/popular | days=7 | 200 |
| TC30 | GET /search/popular | Sắp xếp count desc | 200 |
| TC31 | GET /search/popular | limit vượt max | 200/422 |
| TC32 | GET /search/popular | days âm | 422 |
| TC33 | GET /search/popular | days=0 edge case | 200/422 |
| TC34 | GET /search/trending | Lấy xu hướng 24h | 200 |
| TC35 | GET /search/trending | limit=5 | 200 |
| TC36 | GET /search/trending | limit vượt max | 200/422 |
| TC37 | GET /search/trending | limit không phải số | 422 |
| TC38 | GET /statistics | Thống kê tổng quan | 200 |
| TC39 | GET /statistics | Không cần token | 200 |
| TC40 | GET /recommendations | User đăng nhập | 200 |
| TC41 | GET /recommendations | limit=5 | 200 |
| TC42 | GET /recommendations | limit vượt max | 200/422 |
| TC43 | GET /recommendations | Không có token | 401 |
| TC44 | GET /recommendations | Token sai | 401 |

**Tổng: 44 test cases** — 26 happy path ✅ · 18 error case ❌
