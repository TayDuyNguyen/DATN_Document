# Màn hình: Danh mục Địa điểm

> Route: `/admin/categories`
> Quyền: 🛡️ Admin / Staff
> Mô tả: Quản lý danh mục phân loại địa điểm — xem danh sách, tạo mới, chỉnh sửa, đổi trạng thái, xóa, quản lý danh mục con. Form tạo/sửa hiển thị inline bên phải.

---

## Tái sử dụng từ màn Danh mục Tour

> Xem chi tiết pattern tại `admin_tour_categories.md`

Giữ nguyên:
- Layout 2 cột: danh sách trái (flex-1) + form phải (400px sticky)
- Toolbar: search + filter trạng thái + count
- Table: drag handle, icon container, slug, thứ tự inline input, badge clickable, sửa/xóa
- Form fields: Tên · Slug · Icon/Emoji · Màu nền (8 swatches) · Mô tả · Thứ tự · Toggle trạng thái
- Preview box live update
- Form footer: Hủy + Lưu/Tạo
- Card footer: ghi chú drag & drop
- Empty state
- Design system, màu sắc, spacing

---

## Điểm khác biệt

---

### 1. Page Header

| Element | Danh mục Tour | Danh mục Địa điểm |
|---------|--------------|-------------------|
| Breadcrumb | "Quản lý Tour / Danh mục Tour" | "Quản lý Địa điểm / Danh mục Địa điểm" |
| Title | "Danh mục Tour" | "Danh mục Địa điểm" |
| Subtitle | "...tour du lịch" | "Quản lý các danh mục phân loại địa điểm du lịch" |

---

### 2. Stats Row

`grid grid-cols-3 gap-4 mb-24`

| Thẻ | Icon | Icon bg | Value | Label | Value color |
|-----|------|---------|-------|-------|-------------|
| Tổng danh mục | `category` | `#EFF6FF` | `12` | "TỔNG DANH MỤC" | `#1E293B` |
| Đang hoạt động | `check_circle` | `#D1FAE5` | `9` | "ĐANG HOẠT ĐỘNG" | `#10B981` |
| Tổng địa điểm | `location_on` | `#EEF2FF` | `124` | "TỔNG ĐỊA ĐIỂM" | `#6366F1` |

---

### 3. Table — Cột khác biệt

**Thêm cột "Danh mục con"** (sau cột Danh mục):
- Width: `100px`
- Value: `"3 con" 13px Inter 500 #64748B`
- Nếu = 0: `"—" color #94A3B8`

**Cột "Số địa điểm"** (thay "Số tour"):
- Value: `13px Inter 600 #1E293B` — e.g. `"28"`
- Mini bar: `h-3px bg #E2E8F0 radius-full w-48px mt-4` · fill `#0066CC` proportional

**Columns đầy đủ:**

| Cột | Width | Ghi chú |
|-----|-------|---------|
| # | 48px | Drag handle |
| Danh mục | auto | Tên + icon + slug + mô tả |
| Danh mục con | 100px | Số con |
| Số địa điểm | 110px | Count + mini bar |
| Thứ tự | 80px | Input inline |
| Trạng thái | 120px | Badge clickable |
| Thao tác | 100px | Sửa + Xóa |

---

### 4. Sample Data

| # | Danh mục | Con | Địa điểm | Thứ tự | Trạng thái |
|---|----------|-----|----------|--------|-----------|
| 1 | 🏖️ Bãi biển & Biển | 3 con | 28 | 1 | ĐANG HOẠT ĐỘNG |
| 2 | 🏛️ Di tích lịch sử | 2 con | 18 | 2 | ĐANG HOẠT ĐỘNG |
| 3 | 🍜 Ẩm thực | 4 con | 24 | 3 | ĐANG HOẠT ĐỘNG |
| 4 | 🎭 Văn hóa & Nghệ thuật | 2 con | 12 | 4 | ĐANG HOẠT ĐỘNG |
| 5 | 🌿 Thiên nhiên | 3 con | 16 | 5 | ĐANG HOẠT ĐỘNG |
| 6 | 🎉 Vui chơi giải trí | 2 con | 26 | 6 | TẠM DỪNG |

---

### 5. Confirm Delete — Warning text khác

```
⚠ Kiểm tra xem có địa điểm nào đang thuộc danh mục này không.
Nếu có, các địa điểm sẽ mất liên kết danh mục.
```

---

### 6. Form bên phải — Thêm section "Danh mục con"

Thêm sau Preview box, **chỉ hiện ở mode Chỉnh sửa**:

`mt-16`
- Label: `"DANH MỤC CON" 10px uppercase #94A3B8 mb-10`

**List danh mục con hiện có:**
- Mỗi item: `flex justify-between items-center py-8 border-b #F1F5F9`
  - Left: tên `13px Inter 500 #1E293B`
  - Right:
    - Badge trạng thái: `11px 600 rounded-full px-8 py-2`
      active: `bg #D1FAE5 text #10B981` | inactive: `bg #FEE2E2 text #EF4444`
    - Button xóa: icon `delete 16px #94A3B8` hover `#EF4444`
      → `DELETE /admin/subcategories/{id}`

**Button "Thêm danh mục con"** (`mt-8`):
- `border dashed #B3D9FF bg #EFF6FF/50 text #0066CC radius-8 py-8 full-width 12px 600`
- icon `add` bên trái
- Click → hiện mini form inline bên dưới:
  - Input "Tên danh mục con": `border #E2E8F0 radius-8 px-12 py-8 13px flex-1`
  - Button "Thêm": `bg #0066CC text white radius-8 px-14 py-8 12px 600`
  - → `POST /admin/subcategories` · body: `{ category_id, name, slug, status: "active" }`

**Khi ở mode Tạo mới** — thay bằng info box:
- `bg #EFF6FF border #B3D9FF radius-8 p-12 flex gap-8`
- icon `info 16px #0066CC` + text `12px #1E293B`:
  "Sau khi tạo danh mục, bạn có thể thêm danh mục con."

---

## Ghi chú màn 3.6 và 3.7

> Màn **3.6 Tạo Danh mục** và **3.7 Chỉnh sửa Danh mục** đều nằm trong file này
> dưới dạng 2 mode của form inline bên phải:
>
> - **3.6** → mode Tạo mới: badge "MỚI", button "Tạo danh mục" → `POST /admin/categories`
> - **3.7** → mode Chỉnh sửa: badge "ĐANG SỬA", button "Lưu" → `PUT /admin/categories/{id}`,
>   thêm section Danh mục con, load data từ `GET /categories/{id}`

**Upload ảnh icon** (3.6 có thêm `POST /upload/image`):
- Field "Icon / Emoji" trong form có thêm option upload ảnh:
  - Tab "Emoji / Icon name" (mặc định)
  - Tab "Upload ảnh": upload zone nhỏ `h-80px border dashed #E2E8F0 radius-8`
    → `POST /upload/image` → lưu URL vào field icon
    - Helper: "PNG, SVG · Tối đa 1MB · Khuyến nghị 64x64px"

---

## API Mapping

| Hành động | Method | Endpoint | Màn | Trigger |
|-----------|--------|----------|-----|---------|
| Load danh sách | GET | `/categories` | 3.5 | Khi mount |
| Load chi tiết danh mục | GET | `/categories/{id}` | 3.7 | Khi load form chỉnh sửa |
| Tạo danh mục | POST | `/admin/categories` | 3.6 | Submit form tạo mới |
| Upload ảnh icon | POST | `/upload/image` | 3.6 | Upload ảnh icon |
| Cập nhật danh mục | PUT | `/admin/categories/{id}` | 3.7 | Submit form chỉnh sửa |
| Đổi trạng thái | PATCH | `/admin/categories/{id}/status` | 3.5 | Click badge |
| Cập nhật thứ tự | PUT | `/admin/categories/{id}` | 3.5 | Blur input sort_order |
| Xóa danh mục | DELETE | `/admin/categories/{id}` | 3.5 | Confirm dialog |
| Thêm danh mục con | POST | `/admin/subcategories` | 3.7 | Submit mini form |
| Xóa danh mục con | DELETE | `/admin/subcategories/{id}` | 3.7 | Click xóa trong list |
