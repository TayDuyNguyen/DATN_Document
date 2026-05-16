# Màn hình Admin — Quản lý Landing Pages

> Route UI: `/admin/landing-pages`  
> Trạng thái: Planned  
> API planned: `GET /admin/landing-pages`, `POST /admin/landing-pages`, `PUT /admin/landing-pages/{id}`, `PATCH /admin/landing-pages/{id}/status`, `DELETE /admin/landing-pages/{id}`

---

## Mục tiêu

Quản lý các trang landing SEO như `/du-lich-da-nang`, landing theo dòng tour hoặc landing theo chương trình khuyến mãi.

---

## Thành phần giao diện

| Khu vực | Thành phần | Chức năng |
|---|---|---|
| Toolbar | Search, filter page type, filter status | Tìm landing nhanh |
| Danh sách | Slug, tiêu đề, loại trang, trạng thái, ngày cập nhật | Theo dõi landing |
| Action inline | Xem, sửa, publish/unpublish, xóa | Quản trị nhanh |
| Form nội dung | Slug, page_type, title, intro, hero_image | Nội dung chính |
| SEO | seo_title, seo_description, og image | Tối ưu tìm kiếm |
| Filters mặc định | JSON/filter builder | Gắn landing với bộ lọc tour |
| Content blocks | FAQ, mô tả điểm đến, section CTA | Nội dung dài |

---

## API planned

| Method | Endpoint | Mô tả |
|---|---|---|
| GET | `/admin/landing-pages` | Danh sách landing |
| POST | `/admin/landing-pages` | Tạo landing |
| PUT | `/admin/landing-pages/{id}` | Cập nhật landing |
| PATCH | `/admin/landing-pages/{id}/status` | Publish/unpublish |
| DELETE | `/admin/landing-pages/{id}` | Xóa landing |

---

## Rule nghiệp vụ

| Rule | Mô tả |
|---|---|
| Slug unique | Không trùng route landing |
| Page type | `destination`, `tour_line`, `promotion` |
| Published | Chỉ trang published mới public |
| Filters | Dùng để query danh sách tour mặc định trên landing |
