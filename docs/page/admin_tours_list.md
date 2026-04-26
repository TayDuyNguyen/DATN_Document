# Màn hình: Danh sách Tour

> Route: `/admin/tours`
> Quyền: 🛡️ Admin / Staff
> Mô tả: Quản lý toàn bộ sản phẩm tour du lịch — xem, lọc, đổi trạng thái, bật/tắt nổi bật/hot, xóa.

---

## Layout tổng thể

```
┌─────────────────────────────────────────────────────────────┐
│  HEADER: Breadcrumb + Tiêu đề + [Xuất Excel] [Thêm Tour]   │
├─────────────────────────────────────────────────────────────┤
│  FILTER BAR: Search + Danh mục + Trạng thái + Loại + Lọc   │
│              Active filter tags (khi có filter)             │
├─────────────────────────────────────────────────────────────┤
│  STATS ROW: [Tổng tour] [Đang HĐ] [Nổi bật] [Hết chỗ]     │
├─────────────────────────────────────────────────────────────┤
│  TABLE TOOLBAR: Checkbox chọn tất + Bulk actions + Per page │
│  TABLE HEADER: □ # | Tour | Giá | Lịch | ★ | Bán | TT | ⭐ | 🔥 | ⚙ │
│  TABLE BODY:   5–50 rows                                    │
│  PAGINATION:   Thông tin + Prev/Next/Pages                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 1. Page Header

**Vị trí:** Top of main content, `flex justify-between items-start`

### Bên trái
| Element | Style |
|---------|-------|
| Breadcrumb | `12px Inter 500 #94A3B8` — "Quản lý Tour / Danh sách Tour" |
| Title | `24px Inter 700 #1E293B letter-spacing -0.3px` — "Danh sách Tour" |
| Subtitle | `14px Inter 400 #64748B` — "Quản lý toàn bộ sản phẩm tour du lịch" |

### Bên phải (`flex gap-3`)
| Button | Style | Action |
|--------|-------|--------|
| Xuất Excel | `border #E2E8F0 bg white text #64748B radius-10 px-16 py-10` icon download | `GET /admin/tours/export` |
| Thêm Tour mới | `bg #0066CC text white radius-10 px-20 py-10 shadow` icon + | Navigate `/admin/tours/create` |

---

## 2. Filter Bar

**Container:** `bg white border #E2E8F0 radius-16 p-24 mb-24`

### Row 1 — Inputs (`flex gap-3 flex-wrap`)

| Element | Width | Config |
|---------|-------|--------|
| Search input | `flex-1 min-280px` | Placeholder: "Tìm theo tên tour, mã tour..." · icon search trái · debounce 300ms |
| Select Danh mục | `200px` | Options từ `GET /tour-categories` + "Tất cả danh mục" |
| Select Trạng thái | `160px` | Tất cả / Đang hoạt động (`active`) / Tạm dừng (`inactive`) / Hết chỗ (`sold_out`) |
| Select Loại | `160px` | Tất cả / Nổi bật (`featured`) / Tour Hot (`hot`) / Thường (`normal`) |
| Button Lọc | `auto` | `bg #0066CC text white` · submit filter |
| Button Đặt lại | `auto` | Chỉ hiện khi có filter active · hover `text #EF4444 border #EF4444` |

### Row 2 — Active filter tags (chỉ hiện khi có filter)
- Mỗi tag: `bg #EFF6FF text #0066CC border #B3D9FF radius-full px-10 py-4 text-12`
- Có nút `×` để xóa từng filter riêng lẻ
- Ví dụ: `Danh mục: Tham quan ×` · `Trạng thái: Đang hoạt động ×`

---

## 3. Stats Row (Thống kê nhanh)

**Layout:** `grid grid-cols-4 gap-4 mb-24`
**Mỗi thẻ:** `bg white border #E2E8F0 radius-12 p-16 flex items-center gap-12`

| Thẻ | Icon | Icon bg | Value | Label | Value color |
|-----|------|---------|-------|-------|-------------|
| Tổng tour | `inventory_2` | `#EFF6FF` | `48` | "TỔNG TOUR" | `#1E293B` |
| Đang hoạt động | `check_circle` | `#D1FAE5` | `35` | "ĐANG HOẠT ĐỘNG" | `#10B981` |
| Tour nổi bật | `star` | `#FEF3C7` | `12` | "NỔI BẬT" | `#F59E0B` |
| Hết chỗ | `block` | `#FEE2E2` | `3` | "HẾT CHỖ" | `#EF4444` |

- Icon container: `36x36px radius-8`
- Label: `12px uppercase #94A3B8`
- Value: `20px Inter 700`

> **API thực tế — 4 request song song khi mount:**
> ```
> GET /tours?per_page=1                          → data.total  (Tổng tour)
> GET /tours?status=active&per_page=1            → data.total  (Đang hoạt động)
> GET /tours?is_featured=1&per_page=1            → data.total  (Nổi bật)
> GET /tours?status=sold_out&per_page=1          → data.total  (Hết chỗ)
> ```
> Gọi `Promise.all([...])` để load song song, tránh waterfall.

---

## 4. Table

**Container:** `bg white border #E2E8F0 radius-16 overflow-hidden`

### 4.1 Table Toolbar

`flex justify-between items-center px-24 py-16 border-b #E2E8F0`

**Bên trái:**
- Checkbox "Chọn tất cả"
- Khi có row được chọn → hiện `"Đã chọn 3" 13px 600 #0066CC` + bulk actions:
  - `Kích hoạt` — `bg #D1FAE5 text #10B981 radius-8 px-12 py-6 text-12 600`
  - `Tạm dừng` — `bg #FEF3C7 text #F59E0B`
  - `Xóa` — `bg #FEE2E2 text #EF4444`

**Bên phải:**
- Text `"Hiển thị 1–10 / 48 tour" 13px #94A3B8`
- Select per_page: `10 / trang` | `20 / trang` | `50 / trang`

### 4.2 Table Header

`bg #F8FAFC border-b #E2E8F0`
`th: px-16 py-12 text-11 uppercase tracking-wide #94A3B8 text-left`

| Cột | Width | Ghi chú |
|-----|-------|---------|
| ☐ Checkbox | 40px | |
| # STT | 48px | |
| Tour | auto | Sortable ↕ |
| Giá | 130px | Sortable ↕ |
| Lịch | 100px | |
| Đánh giá | 100px | |
| Lượt bán | 100px | Sortable ↕ |
| Trạng thái | 120px | |
| Nổi bật | 80px | |
| Hot | 70px | |
| Thao tác | 100px | |

Cột sortable: icon `↕` khi hover, `↑`/`↓` khi active, color `#0066CC`

### 4.3 Table Body

`border-b #F1F5F9 min-h-64px`
- Hover: `bg #F8FAFC transition-150ms`
- Selected: `bg #EFF6FF border-l-3 #0066CC`

#### Chi tiết từng cột

**Col ☐ Checkbox**
- `input[type=checkbox] accent-color #0066CC w-16`

**Col # STT**
- `13px Inter 500 #94A3B8`

**Col Tour** (`flex items-center gap-12`)
- Thumbnail: `56x56px radius-10 object-cover border #E2E8F0`
- Tên tour: `14px Inter 600 #1E293B` · hover `#0066CC` · 1 line ellipsis
- Mã tour: `11px Inter 500 #94A3B8` — e.g. `TOUR-001`
- Danh mục tag: `11px 600 bg #EFF6FF text #0066CC border #B3D9FF radius-full px-8 py-2`

**Col Giá**
- Giá: `13px Inter 700 #1E293B` — e.g. `850.000 đ`
- `/ người`: `11px #94A3B8`

**Col Lịch**
- Có lịch: `13px Inter 600 #10B981` — e.g. `5 lịch`
- Hết lịch: `13px Inter 600 #EF4444` — `Hết lịch`

**Col Đánh giá**
- `★ 4.8` — `13px Inter 600 #1E293B` · star `#F59E0B`
- `(128)` — `11px #94A3B8`

**Col Lượt bán**
- `13px Inter 600 #1E293B`

**Col Trạng thái**
- Badge `11px Inter 700 rounded-full px-10 py-4`
- Click → dropdown inline đổi trạng thái

| Giá trị | Background | Text | Border |
|---------|-----------|------|--------|
| ĐANG HOẠT ĐỘNG | `#D1FAE5` | `#10B981` | `rgba(16,185,129,0.2)` |
| TẠM DỪNG | `#FEE2E2` | `#EF4444` | `rgba(239,68,68,0.2)` |
| HẾT CHỖ | `#FEF3C7` | `#F59E0B` | `rgba(245,158,11,0.2)` |

**Col Nổi bật**
- Toggle switch `36x20px` · ON: `bg #0066CC` · OFF: `bg #E2E8F0`
- Thumb: `16px white rounded-full`
- Tooltip: "Bật/tắt nổi bật"
- API: `PATCH /admin/tours/{id}/featured`

**Col Hot**
- Toggle switch · ON: `bg #FF6B35` · OFF: `bg #E2E8F0`
- API: `PATCH /admin/tours/{id}/hot`

**Col Thao tác** (`flex gap-4`)

| Button | Icon | Hover color | Action |
|--------|------|-------------|--------|
| Xem | `visibility` | `#0066CC` | Navigate `/admin/tours/{id}` |
| Sửa | `edit` | `#F59E0B` | Navigate `/admin/tours/{id}/edit` |
| Xóa | `delete` | `#EF4444` | Confirm dialog → `DELETE /admin/tours/{id}` |

Style chung: `28x28px bg #F8FAFC border #E2E8F0 radius-6 color #64748B`

### 4.4 Sample Data

| # | Tên tour | Giá | Lịch | ★ | Bán | Trạng thái | Nổi bật | Hot |
|---|----------|-----|------|---|-----|------------|---------|-----|
| 1 | Bà Nà Hills - Cầu Vàng | 850.000đ | 5 lịch | 4.9 | 428 | ĐANG HOẠT ĐỘNG | ON | ON |
| 2 | Phố cổ Hội An - Show Ký ức | 650.000đ | 3 lịch | 4.8 | 385 | ĐANG HOẠT ĐỘNG | ON | OFF |
| 3 | Ngũ Hành Sơn - Làng đá | 450.000đ | 2 lịch | 4.7 | 312 | ĐANG HOẠT ĐỘNG | OFF | OFF |
| 4 | Cù Lao Chàm - Lặn biển | 1.200.000đ | Hết lịch | 4.8 | 241 | HẾT CHỖ | ON | OFF |
| 5 | Sơn Trà - Chùa Linh Ứng | 350.000đ | 1 lịch | 4.6 | 198 | TẠM DỪNG | OFF | OFF |

---

## 5. Pagination

`flex justify-between items-center px-24 py-16 border-t #E2E8F0 bg #F8FAFC radius-b-16`

- Trái: `"Hiển thị 1–10 trong tổng số 48 tour" 13px #64748B`
- Phải: Prev · 1 · 2 · 3 · ... · 5 · Next
  - Button: `32x32px border #E2E8F0 radius-8 bg white color #64748B`
  - Active: `bg #0066CC text white border #0066CC`
  - Disabled: `opacity-40 cursor-not-allowed`
  - Hover: `border #0066CC color #0066CC`

---

## 6. Confirm Delete Dialog

**Trigger:** Click button Xóa trong cột Thao tác
**Backdrop:** `rgba(0,0,0,0.4)` · Modal: `bg white radius-16 w-400px shadow-modal`

| Vùng | Nội dung |
|------|---------|
| Header | Icon warning `40x40 bg #FEE2E2 radius-10 color #EF4444` + Title "Xóa tour này?" `16px 700 #1E293B` |
| Body | Text xác nhận `14px #64748B` + Warning box `bg #FEF3C7 border warning radius-8` |
| Footer | Button "Hủy" (ghost) + Button "Xóa tour" `bg #EF4444 hover #DC2626` |

---

## 7. Empty State

**Hiển thị khi:** Không có kết quả sau khi filter / search

- SVG icon `80x80px color #E2E8F0`
- Title: `"Không tìm thấy tour nào" 16px Inter 600 #1E293B`
- Subtitle: `"Thử thay đổi bộ lọc hoặc tạo tour mới" 14px #94A3B8`
- Button "Thêm Tour mới": `bg #0066CC text white radius-10 px-20 py-10`

---

## 9. Cấu trúc Response thực tế

---

### GET /tours

```json
{
  "code": 200,
  "message": "Success",
  "data": {
    "current_page": 1,
    "data": [
      {
        "id": 36,
        "name": "Slug Seed Tour 1775792959",
        "slug": "slug-tour-trung-1775792959",
        "tour_category_id": 5,
        "description": "Mo ta seed slug",
        "short_desc": null,
        "itinerary": [{"day":1,"title":"Ngay 1","content":"Noi dung"}],
        "inclusions": null,
        "exclusions": null,
        "price_adult": "300000",        // string
        "price_child": "0",             // string
        "price_infant": "0",            // string
        "discount_percent": 0,          // number
        "duration": "1 ngay",
        "start_time": null,
        "meeting_point": null,
        "max_people": 0,
        "min_people": 1,
        "available_from": null,
        "available_to": null,
        "thumbnail": null,
        "images": null,
        "video_url": null,
        "location_ids": null,
        "status": "available",          // "active"|"inactive"|"sold_out"
        "is_featured": false,
        "is_hot": false,
        "view_count": 0,
        "booking_count": 0,
        "created_by": null,
        "created_at": "2026-04-09T07:49:19.000000Z",
        "updated_at": "2026-04-09T07:49:19.000000Z"
      }
    ],
    "total": 33,
    "per_page": 1,
    "last_page": 33
  }
}
```

**TypeScript:**
```ts
interface Tour {
  id: number;
  name: string;
  slug: string;
  tour_category_id: number;
  description: string;
  short_desc: string | null;
  itinerary: Array<{day: number; title: string; content: string}> | null;
  inclusions: string | null;
  exclusions: string | null;
  price_adult: string;      // parse: parseFloat(price_adult)
  price_child: string;
  price_infant: string;
  discount_percent: number;
  duration: string;
  start_time: string | null;
  meeting_point: string | null;
  max_people: number;
  min_people: number;
  available_from: string | null;
  available_to: string | null;
  thumbnail: string | null;
  images: string[] | null;
  video_url: string | null;
  location_ids: number[] | null;
  status: 'active' | 'inactive' | 'sold_out';
  is_featured: boolean;
  is_hot: boolean;
  view_count: number;
  booking_count: number;
  created_by: number | null;
  created_at: string;
  updated_at: string;
}
// Truy cập: response.data.data (mảng), response.data.total, response.data.last_page
```

---

### GET /tour-categories

```json
{
  "code": 200,
  "data": [
    {
      "id": 1,
      "name": "Tour Bà Nà Hills",
      "slug": "tour-ba-na-hills",
      "description": "Các tour thuộc nhóm Tour Bà Nà Hills...",
      "icon": "mountain",
      "sort_order": 0,
      "status": "active",
      "created_at": "2026-04-08T00:45:45.000000Z",
      "updated_at": "2026-04-08T00:45:45.000000Z"
    }
  ]
}
```

**TypeScript:**
```ts
interface TourCategory {
  id: number;
  name: string;
  slug: string;
  description: string;
  icon: string;
  sort_order: number;
  status: 'active' | 'inactive';
  created_at: string;
  updated_at: string;
}
// Truy cập: response.data (mảng trực tiếp, không wrap)
```

---

### PATCH /admin/tours/{id}/status

```json
{
  "code": 200,
  "message": "Status updated successfully",
  "data": {
    "id": 1,
    "name": "Khám phá Sun World Ba Na Hills",
    "status": "active",
    "...": "..."
  }
}
```

Trả về tour object đầy đủ sau khi update.

---

### PATCH /admin/tours/{id}/featured

```json
{
  "code": 200,
  "message": "Featured status toggled successfully",
  "data": {
    "id": 1,
    "is_featured": true,
    "...": "..."
  }
}
```

---

### PATCH /admin/tours/{id}/hot

```json
{
  "code": 200,
  "message": "Hot status toggled successfully",
  "data": {
    "id": 1,
    "is_hot": true,
    "...": "..."
  }
}
```

---

### GET /admin/tours/export

- Status: `200 OK`
- Content-Type: `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
- Body: Binary Excel file (OOXML format)
- Size: ~9KB cho 33 tours

**Download đúng cách:**
```javascript
const response = await fetch('/api/v1/admin/tours/export?status=active', {
  headers: { 'Authorization': `Bearer ${token}` }
});
const blob = await response.blob();
const url = URL.createObjectURL(blob);
const a = document.createElement('a');
a.href = url;
a.download = 'tours.xlsx';
a.click();
URL.revokeObjectURL(url);
```

---

## 8. API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load danh sách | GET | `/tours?page=&per_page=&sort=&order=` | Vào trang, đổi filter, đổi trang |
| Tìm kiếm | GET | `/tours?q=` | Nhập search (debounce 300ms) |
| Filter danh mục | GET | `/tours?tour_category_id=` | Chọn select danh mục |
| Filter trạng thái | GET | `/tours?status=` | Chọn select trạng thái |
| Stats — Tổng tour | GET | `/tours?per_page=1` | Khi mount → `data.total` |
| Stats — Đang HĐ | GET | `/tours?status=active&per_page=1` | Khi mount → `data.total` |
| Stats — Nổi bật | GET | `/tours?is_featured=1&per_page=1` | Khi mount → `data.total` |
| Stats — Hết chỗ | GET | `/tours?status=sold_out&per_page=1` | Khi mount → `data.total` |
| Load danh mục (select) | GET | `/tour-categories` | Khi mount component |
| Đổi trạng thái | PATCH | `/admin/tours/{id}/status` | Click badge → chọn trạng thái mới |
| Bật/tắt nổi bật | PATCH | `/admin/tours/{id}/featured` | Toggle switch Nổi bật |
| Bật/tắt hot | PATCH | `/admin/tours/{id}/hot` | Toggle switch Hot |
| Xóa 1 tour | DELETE | `/admin/tours/{id}` | Confirm dialog → xác nhận |
| Bulk kích hoạt | PATCH | `/admin/tours/{id}/status` (loop) | Bulk action "Kích hoạt" |
| Bulk tạm dừng | PATCH | `/admin/tours/{id}/status` (loop) | Bulk action "Tạm dừng" |
| Bulk xóa | DELETE | `/admin/tours/{id}` (loop) | Bulk action "Xóa" |
| Xuất Excel | GET | `/admin/tours/export?tour_category_id=&status=` | Click "Xuất Excel" |
