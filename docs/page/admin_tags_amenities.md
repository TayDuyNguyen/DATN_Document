# Màn hình: Tags & Tiện ích

> Route: `/admin/tags` (Tab 1) · `/admin/amenities` (Tab 2)
> Quyền: 🛡️ Admin / Staff
> Mô tả: Quản lý tags và tiện ích dùng cho địa điểm — 2 tab trong cùng 1 trang. Mỗi tab có danh sách + inline form tạo/sửa.

---

## Layout tổng thể

```
┌─────────────────────────────────────────────────────────────────┐
│  HEADER: Breadcrumb + Tiêu đề + [Thêm]                         │
├─────────────────────────────────────────────────────────────────┤
│  TAB BAR: [Tags ← active] [Tiện ích]                           │
├─────────────────────────────────────────────────────────────────┤
│  STATS ROW: [Tổng tags] [Theo type]                            │
├──────────────────────────────────┬──────────────────────────────┤
│  CỘT TRÁI (flex-1)               │  CỘT PHẢI (380px)            │
│                                  │  sticky top-24               │
│  Toolbar: Search + Filter type   │  Form tạo / chỉnh sửa        │
│  Table: danh sách tags           │                              │
└──────────────────────────────────┴──────────────────────────────┘
```

---

## 1. Page Header

| Element | Style |
|---------|-------|
| Breadcrumb | `12px Inter 500 #94A3B8` — "Tags & Tiện ích" |
| Title | `24px Inter 700 #1E293B` — "Tags & Tiện ích" |
| Subtitle | `14px Inter 400 #64748B` — "Quản lý nhãn và tiện ích cho địa điểm du lịch" |
| Button "Thêm tag" (Tab 1) | `bg #0066CC text white radius-10 px-20 py-10 shadow` icon `add` → reset form tạo mới |
| Button "Thêm tiện ích" (Tab 2) | same style |

---

## 2. Tab Bar

`flex gap-0 bg white border #E2E8F0 radius-12 p-4 inline-flex mb-24`

| Tab | Style |
|-----|-------|
| Tags | Active: `bg #0066CC text white radius-8 px-16 py-8 13px 600` |
| Tiện ích | Inactive: `bg transparent text #64748B px-16 py-8 13px 500` hover `text #0066CC` |

---

## 3. TAB 1 — TAGS

### 3.1 Stats Row

`grid grid-cols-5 gap-3 mb-24`

| Thẻ | Value | Label | Color |
|-----|-------|-------|-------|
| Tổng tags | `48` | "TỔNG TAGS" | `#1E293B` |
| Ẩm thực | `12` | "ẨM THỰC" | `#FF6B35` |
| Dịch vụ | `10` | "DỊCH VỤ" | `#0066CC` |
| Đặc điểm | `16` | "ĐẶC ĐIỂM" | `#10B981` |
| Không khí | `10` | "KHÔNG KHÍ" | `#6366F1` |

Mỗi thẻ: `bg white border #E2E8F0 radius-12 p-14 text-center`
- Value: `18px Inter 700`
- Label: `10px uppercase #94A3B8 mt-2`

### 3.2 Cột trái — Danh sách Tags

**Card:** `bg white border #E2E8F0 radius-16 overflow-hidden`

**Toolbar** (`flex justify-between px-24 py-16 border-b #E2E8F0`):
- Search `width 220px`: placeholder "Tìm tag..."
- Select "Loại" `width 160px ml-8`:
  Tất cả / Ẩm thực (cuisine) / Dịch vụ (service) / Đặc điểm (feature) / Không khí (atmosphere)
- Text `"48 tags" 13px #94A3B8`

**Table Header** (`bg #F8FAFC border-b #E2E8F0`):

| Cột | Width |
|-----|-------|
| # | 48px |
| Tag | auto |
| Loại | 120px |
| Số địa điểm | 120px |
| Thao tác | 100px |

**Table Body** (`border-b #F1F5F9 min-h-52px`):
- Hover: `bg #F8FAFC`
- Row đang sửa: `bg #EFF6FF border-l-3 #0066CC`

**Col Tag** (`flex items-center gap-10`):
- Badge preview: `bg màu type (10% opacity) text màu type border màu type (20% opacity) radius-full px-12 py-6 13px 600`
  - e.g. cuisine: `bg #FFE0D4 text #FF6B35 border rgba(255,107,53,0.2)` "Hải sản"
- Slug: `11px #94A3B8 ml-8`

**Col Loại** — badge `11px 600 rounded-full px-8 py-3`:
| Type | Background | Text |
|------|-----------|------|
| cuisine | `#FFE0D4` | `#FF6B35` "ẨM THỰC" |
| service | `#EFF6FF` | `#0066CC` "DỊCH VỤ" |
| feature | `#D1FAE5` | `#10B981` "ĐẶC ĐIỂM" |
| atmosphere | `#EEF2FF` | `#6366F1` "KHÔNG KHÍ" |

**Col Số địa điểm:**
- `13px Inter 600 #1E293B` + mini bar `h-3px bg #E2E8F0 w-48px mt-4` fill `#0066CC`

**Col Thao tác:**
- Sửa: hover `border #F59E0B color #F59E0B` → load vào form phải
- Xóa: hover `border #EF4444 color #EF4444` → confirm → `DELETE /admin/tags/{id}`

**Sample data:**
| Tag | Loại | Địa điểm |
|-----|------|---------|
| Hải sản | ẨM THỰC | 18 |
| Wifi miễn phí | DỊCH VỤ | 24 |
| View biển | ĐẶC ĐIỂM | 12 |
| Yên tĩnh | KHÔNG KHÍ | 8 |
| Đặc sản địa phương | ẨM THỰC | 15 |

### 3.3 Cột phải — Form Tags

**Card:** `bg white border #E2E8F0 radius-16 p-24 sticky top-24`

**Card Header:**
- Tạo: "Thêm tag" + badge "MỚI" `bg #D1FAE5 text #10B981`
- Sửa: "Chỉnh sửa tag" + badge "ĐANG SỬA" `bg #EFF6FF text #0066CC`
- Button `×` đóng

**Form Fields** (`space-y-16`):

| Field | Type | Bắt buộc | Config |
|-------|------|----------|--------|
| Tên tag | text | ✅ | placeholder "Ví dụ: Hải sản" |
| Slug | text | — | placeholder "hai-san" · badge "Tự động" |
| Loại (Type) | select | — | Ẩm thực / Dịch vụ / Đặc điểm / Không khí |

**Preview Box** (`mt-16 bg #F8FAFC border #E2E8F0 radius-12 p-16`):
- Label: `"XEM TRƯỚC" 10px uppercase #94A3B8 mb-10`
- Badge preview: màu theo type đã chọn (live update)
  `radius-full px-12 py-6 13px 600`

**Form Footer** (`flex gap-8 mt-20 pt-16 border-t #F1F5F9`):
- "Hủy": ghost · "Lưu / Tạo tag": `bg #0066CC text white`

---

## 4. TAB 2 — TIỆN ÍCH (Amenities)

### 4.1 Stats Row

`grid grid-cols-5 gap-3 mb-24`

| Thẻ | Value | Label | Color |
|-----|-------|-------|-------|
| Tổng tiện ích | `32` | "TỔNG TIỆN ÍCH" | `#1E293B` |
| Kết nối | `8` | "KẾT NỐI" | `#0066CC` |
| Đỗ xe | `6` | "ĐỖ XE" | `#F59E0B` |
| Tiện nghi | `12` | "TIỆN NGHI" | `#10B981` |
| Thanh toán | `6` | "THANH TOÁN" | `#6366F1` |

### 4.2 Cột trái — Danh sách Tiện ích

**Toolbar:**
- Search: placeholder "Tìm tiện ích..."
- Select "Nhóm": Tất cả / Kết nối / Đỗ xe / Tiện nghi / Thanh toán

**Table Columns:**

| Cột | Width |
|-----|-------|
| # | 48px |
| Tiện ích | auto |
| Nhóm | 130px |
| Số địa điểm | 120px |
| Thao tác | 100px |

**Col Tiện ích** (`flex items-center gap-10`):
- Icon container: `32x32px radius-8 bg màu nhóm (10% opacity)`
  - icon Material `18px màu nhóm`
- Tên: `14px Inter 600 #1E293B`

**Col Nhóm** — badge `11px 600 rounded-full px-8 py-3`:
| Category | Background | Text |
|----------|-----------|------|
| connectivity | `#EFF6FF` | `#0066CC` "KẾT NỐI" |
| parking | `#FEF3C7` | `#F59E0B` "ĐỖ XE" |
| comfort | `#D1FAE5` | `#10B981` "TIỆN NGHI" |
| payment | `#EEF2FF` | `#6366F1` "THANH TOÁN" |

**Sample data:**
| Tiện ích | Nhóm | Địa điểm |
|---------|------|---------|
| 📶 Wifi miễn phí | KẾT NỐI | 24 |
| 🅿️ Bãi đỗ xe | ĐỖ XE | 18 |
| ❄️ Điều hòa | TIỆN NGHI | 32 |
| 💳 Thanh toán thẻ | THANH TOÁN | 15 |
| 🔌 Sạc điện thoại | KẾT NỐI | 12 |

### 4.3 Cột phải — Form Tiện ích

**Form Fields** (`space-y-16`):

| Field | Type | Bắt buộc | Config |
|-------|------|----------|--------|
| Tên tiện ích | text | ✅ | placeholder "Ví dụ: Wifi miễn phí" |
| Icon | text | — | placeholder "wifi" · helper "Tên icon Material Symbols" · preview icon live |
| Nhóm (Category) | select | — | Kết nối / Đỗ xe / Tiện nghi / Thanh toán |

**Preview Box:**
- Icon container `40x40px radius-10` bg màu nhóm (10% opacity) + icon live
- Tên tiện ích live update

---

## 5. Confirm Delete Dialog

**Modal:** `bg white radius-16 w-400px shadow-modal backdrop rgba(0,0,0,0.4)`

**Tags:**
| Vùng | Nội dung |
|------|---------|
| Header | Icon `label 40x40 bg #FEE2E2 radius-10 color #EF4444` + "Xóa tag này?" |
| Body | "Tag [Tên] sẽ bị xóa." + Warning: "⚠ Tag sẽ bị gỡ khỏi tất cả địa điểm đang sử dụng." |
| Footer | "Hủy" + "Xóa tag" `bg #EF4444` |

**Tiện ích:**
| Vùng | Nội dung |
|------|---------|
| Header | Icon `checklist 40x40 bg #FEE2E2 radius-10 color #EF4444` + "Xóa tiện ích này?" |
| Body | "Tiện ích [Tên] sẽ bị xóa." + Warning: "⚠ Tiện ích sẽ bị gỡ khỏi tất cả địa điểm đang sử dụng." |
| Footer | "Hủy" + "Xóa tiện ích" `bg #EF4444` |

---

## 6. API Mapping

### Tab 1 — Tags

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load tags | GET | `/tags` | Khi mount Tab 1 |
| Tạo tag | POST | `/admin/tags` | Submit form tạo mới |
| Cập nhật tag | PUT | `/admin/tags/{id}` | Submit form chỉnh sửa |
| Xóa tag | DELETE | `/admin/tags/{id}` | Confirm dialog |

### Tab 2 — Tiện ích

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load amenities | GET | `/amenities` | Khi mount Tab 2 |
| Tạo amenity | POST | `/admin/amenities` | Submit form tạo mới |
| Cập nhật amenity | PUT | `/admin/amenities/{id}` | Submit form chỉnh sửa |
| Xóa amenity | DELETE | `/admin/amenities/{id}` | Confirm dialog |
