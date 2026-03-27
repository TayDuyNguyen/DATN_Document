# Test Cases — UPLOAD (Upload ảnh Cloudinary)

> Base URL: `http://localhost:8000/api/v1`
> 🔐 User token bắt buộc cho tất cả endpoints
> Upload dạng `multipart/form-data`

---

## 1. POST /upload/image — Upload 1 ảnh

### ✅ TC01 — Upload JPEG thành công
- body: `image` = file .jpg hợp lệ (< 5MB)
- Expected: `200 OK` hoặc `201 Created`
- Verify: response có `url` là HTTPS link Cloudinary

### ✅ TC02 — Upload PNG thành công
- body: `image` = file .png hợp lệ
- Expected: `200 OK` hoặc `201 Created`

### ✅ TC03 — Upload WEBP thành công
- body: `image` = file .webp hợp lệ
- Expected: `200 OK` hoặc `201 Created`

### ✅ TC04 — Upload với `folder` chỉ định
- body: `image` = file .jpg, `folder` = `locations`
- Expected: `200 OK` hoặc `201 Created`
- Verify: URL trả về chứa folder `locations`

### ✅ TC05 — Upload không có `folder` (optional)
- body: `image` = file .jpg, không có `folder`
- Expected: `200 OK` hoặc `201 Created`

### ❌ TC06 — Thiếu `image`
- body: không có file
- Expected: `422 Unprocessable`

### ❌ TC07 — File không phải ảnh (PDF)
- body: `image` = file .pdf
- Expected: `422 Unprocessable`

### ❌ TC08 — File không phải ảnh (TXT)
- body: `image` = file .txt
- Expected: `422 Unprocessable`

### ❌ TC09 — File quá lớn (> 5MB)
- body: `image` = file 6MB
- Expected: `422 Unprocessable` hoặc `413 Request Entity Too Large`

### ❌ TC10 — Không có token
- body: `image` = file .jpg hợp lệ
- Expected: `401 Unauthorized`

---

## 2. POST /upload/images — Upload nhiều ảnh

### ✅ TC11 — Upload 2 ảnh thành công
- body: `images[]` = 2 file .jpg hợp lệ
- Expected: `200 OK` hoặc `201 Created`
- Verify: response có array `urls` với 2 phần tử

### ✅ TC12 — Upload 1 ảnh qua endpoint multiple
- body: `images[]` = 1 file .jpg
- Expected: `200 OK` hoặc `201 Created`

### ✅ TC13 — Upload 10 ảnh (max)
- body: `images[]` = 10 file .jpg
- Expected: `200 OK` hoặc `201 Created`
- Verify: response có 10 URLs

### ✅ TC14 — Upload với `folder` chỉ định
- body: `images[]` = 2 file .jpg, `folder` = `ratings`
- Expected: `200 OK` hoặc `201 Created`

### ❌ TC15 — Upload 11 ảnh (vượt max 10)
- body: `images[]` = 11 file .jpg
- Expected: `422 Unprocessable`

### ❌ TC16 — Thiếu `images[]`
- body: không có file
- Expected: `422 Unprocessable`

### ❌ TC17 — Có 1 file không phải ảnh trong batch
- body: `images[]` = 1 file .jpg + 1 file .pdf
- Expected: `422 Unprocessable`

### ❌ TC18 — Có 1 file quá lớn trong batch
- body: `images[]` = 1 file .jpg + 1 file 6MB
- Expected: `422 Unprocessable` hoặc `413`

### ❌ TC19 — Không có token
- body: `images[]` = 1 file .jpg
- Expected: `401 Unauthorized`

---

## 3. DELETE /upload/image — Xóa ảnh

### ✅ TC20 — Xóa ảnh thành công
- Upload 1 ảnh trước → lấy `public_id` → DELETE
- body: `public_id` = public_id hợp lệ vừa upload
- Expected: `200 OK`
- Verify: response có message thành công

### ❌ TC21 — `public_id` không tồn tại trên Cloudinary
- body: `public_id` = `danang_trip/khong_ton_tai_xyz_999`
- Expected: `200 OK` hoặc `404 Not Found` hoặc `422 Unprocessable`
- Note: Cloudinary API trả về success khi xóa ID không tồn tại — đây là behavior bình thường

### ❌ TC22 — Thiếu `public_id`
- body: `{}`
- Expected: `422 Unprocessable`

### ❌ TC23 — `public_id` rỗng
- body: `public_id` = `""`
- Expected: `422 Unprocessable`

### ❌ TC24 — Không có token
- body: `public_id` = public_id hợp lệ
- Expected: `401 Unauthorized`

---

## Tổng kết

| TC | API | Trường hợp | Expected |
|----|-----|-----------|----------|
| TC01 | POST /upload/image | Upload JPEG | 200/201 |
| TC02 | POST /upload/image | Upload PNG | 200/201 |
| TC03 | POST /upload/image | Upload WEBP | 200/201 |
| TC04 | POST /upload/image | Upload với folder | 200/201 |
| TC05 | POST /upload/image | Không có folder | 200/201 |
| TC06 | POST /upload/image | Thiếu image | 422 |
| TC07 | POST /upload/image | File PDF | 422 |
| TC08 | POST /upload/image | File TXT | 422 |
| TC09 | POST /upload/image | File > 5MB | 422/413 |
| TC10 | POST /upload/image | Không có token | 401 |
| TC11 | POST /upload/images | Upload 2 ảnh | 200/201 |
| TC12 | POST /upload/images | Upload 1 ảnh | 200/201 |
| TC13 | POST /upload/images | Upload 10 ảnh (max) | 200/201 |
| TC14 | POST /upload/images | Upload với folder | 200/201 |
| TC15 | POST /upload/images | 11 ảnh vượt max | 422 |
| TC16 | POST /upload/images | Thiếu images[] | 422 |
| TC17 | POST /upload/images | Có file PDF trong batch | 422 |
| TC18 | POST /upload/images | Có file > 5MB trong batch | 422/413 |
| TC19 | POST /upload/images | Không có token | 401 |
| TC20 | DELETE /upload/image | Xóa thành công | 200 |
| TC21 | DELETE /upload/image | public_id không tồn tại | 200/404/422 |
| TC22 | DELETE /upload/image | Thiếu public_id | 422 |
| TC23 | DELETE /upload/image | public_id rỗng | 422 |
| TC24 | DELETE /upload/image | Không có token | 401 |
