# Màn hình: Gợi ý cho bạn

> Route: `/recommendations`
> Quyền: 🔐 Cần đăng nhập
> Mô tả: Trang gợi ý địa điểm và tour cá nhân hóa dựa trên lịch sử xem, đặt tour và yêu thích.

---

## Layout tổng thể

```
┌─────────────────────────────────────────────────────────────┐
│  HEADER (dùng chung)                                        │
├─────────────────────────────────────────────────────────────┤
│  PAGE HERO: Tiêu đề + Mô tả cá nhân hóa                   │
├─────────────────────────────────────────────────────────────┤
│  FILTER TABS: Tất cả · Địa điểm · Tour                     │
├─────────────────────────────────────────────────────────────┤
│  GRID: Kết quả gợi ý                                       │
├─────────────────────────────────────────────────────────────┤
│  FOOTER (dùng chung)                                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 1. Page Hero

`bg linear-gradient(135deg, #0066CC, #6366F1) py-48 text-center`

- Breadcrumb: `"Trang chủ / Gợi ý cho bạn" 13px white/70`
- Title: `"Gợi ý dành riêng cho bạn" 32px Inter 700 white`
- Subtitle: `"Dựa trên lịch sử khám phá và sở thích của bạn" 16px white/80 mt-8`

---

## 2. Filter Tabs

`bg white border-b #E2E8F0`

`flex gap-0 max-w-1200px mx-auto`

| Tab | Label |
|-----|-------|
| Tất cả | "Tất cả" |
| Địa điểm | "Địa điểm" |
| Tour | "Tour" |

- Active: `border-b-2 border-#0066CC text #0066CC 14px 600`
- Inactive: `text #64748B 14px 500` hover `text #0066CC`

---

## 3. Result Grid

**API: `GET /recommendations?limit=12`**

`grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-20 py-32`

### 3.1 Location Card

- Thumbnail: `full-width h-200px object-cover radius-t-16`
  - Badge "📍 ĐỊA ĐIỂM": `absolute top-12 left-12 bg white/90 text #6366F1 11px 600 radius-full px-8 py-3`
  - Button yêu thích: `absolute top-12 right-12 w-32 h-32 bg white/80 rounded-full`
- Body (`p-16`):
  - Danh mục badge + Quận
  - Tên: `15px Inter 600 #1E293B`
  - Địa chỉ: `12px #94A3B8 mt-4`
  - `flex justify-between mt-12 pt-12 border-t #F1F5F9`:
    - Rating: `★ 4.8` `12px #F59E0B`
    - Mức giá: `12px #0066CC`
- → `/locations/{slug}`

### 3.2 Tour Card

- Thumbnail: `full-width h-200px object-cover radius-t-16`
  - Badge "🎫 TOUR": `absolute top-12 left-12 bg white/90 text #FF6B35 11px 600 radius-full px-8 py-3`
- Body (`p-16`):
  - Danh mục badge
  - Tên: `15px Inter 600 #1E293B`
  - `flex items-center gap-8 mt-6`:
    - Thời lượng `12px #64748B` · Số người `12px #64748B`
  - `flex justify-between mt-12 pt-12 border-t #F1F5F9`:
    - Rating: `★ 4.8 (128)` `12px #F59E0B`
    - Giá: `"850.000 đ" 14px Inter 700 #FF6B35`
- → `/tours/{slug}`

### 3.3 Reason Tag

**Thêm vào mỗi card** — lý do được gợi ý:

`flex items-center gap-6 px-12 py-6 bg #F8FAFC border #E2E8F0 radius-full mt-8 inline-flex`

| Lý do | Icon | Text |
|-------|------|------|
| Đã xem trước | `visibility 12px #94A3B8` | "Bạn đã xem" |
| Tương tự yêu thích | `favorite 12px #EF4444` | "Tương tự yêu thích" |
| Phổ biến gần bạn | `location_on 12px #0066CC` | "Phổ biến gần bạn" |
| Đặt nhiều | `trending_up 12px #10B981` | "Được đặt nhiều" |

`11px #94A3B8`

---

## 4. Loading State

`grid grid-cols-4 gap-20 py-32`

- 8 skeleton cards: `bg #E2E8F0 radius-16 h-280px animation pulse`

---

## 5. Empty State

**Hiển thị khi:** Chưa có đủ lịch sử để gợi ý

`center py-64 text-center max-w-480px mx-auto`

- SVG icon `explore 80px #E2E8F0`
- Title: `"Chưa có gợi ý nào" 20px Inter 600 #1E293B mt-16`
- Subtitle: `"Hãy khám phá thêm địa điểm và tour để nhận gợi ý phù hợp!" 14px #94A3B8 mt-8 text-center`
- `flex gap-12 justify-center mt-20`:
  - Button "Khám phá Địa điểm": `bg #0066CC text white radius-10 px-20 py-12 14px 600`
    → `/locations`
  - Button "Khám phá Tour": `bg #FF6B35 text white radius-10 px-20 py-12 14px 600`
    → `/tours`

---

## 6. API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load gợi ý | GET | `/recommendations?limit=12` | Khi mount |
| Filter loại | GET | `/recommendations?limit=12&type=location` hoặc `?type=tour` | Click tab |
| Toggle yêu thích | POST/DELETE | `/user/favorites` | Click icon yêu thích |
