# Màn hình: Địa điểm lân cận (GPS)

> Route: `/nearby`
> Quyền: 🌐 Public — không cần đăng nhập
> Mô tả: Hiển thị địa điểm gần vị trí hiện tại của người dùng dựa trên GPS, kết hợp bản đồ và danh sách.

---

## Layout tổng thể

```
┌─────────────────────────────────────────────────────────────┐
│  HEADER (dùng chung)                                        │
├─────────────────────────────────────────────────────────────┤
│  PAGE HERO: Tiêu đề + Trạng thái GPS + Radius selector     │
├──────────────────────────────────┬──────────────────────────┤
│  BẢN ĐỒ (50% height)             │  DANH SÁCH (50% height)  │
│  - Google Maps / Leaflet         │  - Filter bar            │
│  - Markers địa điểm              │  - Card list             │
│  - Marker vị trí hiện tại        │  - Pagination            │
│  - Popup khi click marker        │                          │
└──────────────────────────────────┴──────────────────────────┘
│  FOOTER (dùng chung)                                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 1. Page Hero

`bg white border-b #E2E8F0 py-20`

`flex justify-between items-center max-w-1200px mx-auto px-24`

**Bên trái:**
- Title: `"Địa điểm gần bạn" 24px Inter 700 #1E293B`
- GPS status (dynamic):
  - Đang lấy vị trí: `flex items-center gap-8` · spinner `16px #0066CC` · `"Đang xác định vị trí..." 13px #64748B`
  - Có vị trí: icon `my_location 16px #10B981` · `"Đà Nẵng, Việt Nam · Cập nhật vừa xong" 13px #64748B`
  - Từ chối GPS: icon `location_off 16px #EF4444` · `"Không thể lấy vị trí" 13px #EF4444`

**Bên phải** (`flex items-center gap-12`):
- Label: `"Bán kính:" 13px #64748B`
- Radius selector (pill group):
  - "1 km" | "3 km" | "5 km" | "10 km"
  - Active: `bg #0066CC text white radius-full px-14 py-6 13px 600`
  - Inactive: `bg #F1F5F9 text #64748B radius-full px-14 py-6 13px 500` hover `bg #EFF6FF text #0066CC`
  - Click → gọi lại `GET /locations/nearby?radius={km}`

- Button "Cập nhật vị trí": icon `my_location 16px` `border #E2E8F0 bg white text #64748B radius-8 px-12 py-8 13px`
  hover `border #0066CC text #0066CC`
  → re-request GPS

---

## 2. Trạng thái GPS

### 2.1 Đang xin quyền / Lấy vị trí

`center h-400px flex-col gap-16`

- Spinner lớn `48px #0066CC`
- Text: `"Đang xác định vị trí của bạn..." 16px Inter 500 #64748B`
- Sub: `"Vui lòng cho phép truy cập vị trí khi được hỏi" 13px #94A3B8`

### 2.2 Từ chối GPS

`center h-400px flex-col gap-16 bg #F8FAFC`

- SVG icon `location_off 80px #E2E8F0`
- Title: `"Không thể lấy vị trí" 20px Inter 600 #1E293B`
- Subtitle: `"Vui lòng cho phép truy cập vị trí trong cài đặt trình duyệt" 14px #94A3B8 text-center max-w-300px`
- Button "Thử lại": `bg #0066CC text white radius-10 px-20 py-10 14px 600`
- Button "Nhập vị trí thủ công": `border #E2E8F0 bg white text #64748B radius-10 px-20 py-10 mt-8`
  → mở input nhập địa chỉ

---

## 3. Bản đồ

`height calc(100vh - header - hero) min-h-400px`

**Map container** (Google Maps hoặc Leaflet):

**Marker vị trí hiện tại:**
- Icon: `my_location` màu `#0066CC` với pulse animation
- Tooltip: "Vị trí của bạn"

**Marker địa điểm:**
- Icon: pin màu theo danh mục
- Click marker → hiện popup

**Popup khi click marker:**
`bg white radius-12 shadow-modal p-12 min-w-200px`
- Thumbnail: `full-width h-80px object-cover radius-8 mb-8`
- Tên: `13px Inter 600 #1E293B`
- Khoảng cách: `11px #94A3B8` icon `near_me 12px` — e.g. "1.2 km"
- Rating: `★ 4.8` `11px #F59E0B`
- Button "Xem chi tiết →": `13px #0066CC` → navigate `/locations/{slug}`

**Circle bán kính:**
- Vòng tròn bán kính đã chọn: `stroke #0066CC stroke-width 2 fill rgba(0,102,204,0.05)`

**Controls:**
- Zoom in/out: top-right
- "Về vị trí của tôi": bottom-right, icon `my_location`

---

## 4. Danh sách bên phải

`overflow-y-auto height calc(100vh - header - hero)`

### 4.1 Filter bar

`px-16 py-12 border-b #E2E8F0 flex gap-8 overflow-x-auto`

- Select "Danh mục": `border #E2E8F0 radius-8 px-10 py-8 13px`
- Select "Sắp xếp": Gần nhất · Đánh giá cao · Phổ biến nhất
- Button "Đặt lại" (khi có filter)

### 4.2 Result count

`px-16 py-10 border-b #F1F5F9`
`"Tìm thấy 18 địa điểm trong bán kính 5 km" 13px #64748B`

### 4.3 Card list

`px-16 py-8 space-y-12`

Mỗi location card (horizontal compact):
- `flex gap-12 bg white border #E2E8F0 radius-12 p-12 cursor-pointer`
  hover `border #0066CC shadow-card`
  - Thumbnail: `64x64px radius-8 object-cover flex-shrink-0`
  - Right:
    - Tên: `14px Inter 600 #1E293B`
    - `flex items-center gap-6 mt-4`:
      - icon `near_me 12px #0066CC` + khoảng cách `12px Inter 600 #0066CC` — e.g. "1.2 km"
      - `·` separator
      - Danh mục: `12px #94A3B8`
    - `flex items-center gap-8 mt-4`:
      - Rating: `★ 4.8` `11px #F59E0B`
      - Mức giá: `"Miễn phí"` hoặc `"$"` `11px #64748B`
  - Click → highlight marker trên bản đồ + navigate `/locations/{slug}`

**Khi hover card:** marker tương ứng trên bản đồ bounce/highlight

### 4.4 Pagination

`px-16 py-12 border-t #E2E8F0 flex justify-center`
- Compact: Prev · 1 · 2 · 3 · Next

---

## 5. Input vị trí thủ công (Modal)

**Trigger:** Click "Nhập vị trí thủ công" khi từ chối GPS

`Modal center w-400px`

- Title: `"Nhập vị trí" 18px Inter 600 #1E293B`
- Input: `border #E2E8F0 radius-10 px-14 py-12 14px` placeholder "Nhập địa chỉ hoặc tên khu vực..."
  - Autocomplete gợi ý địa chỉ
- Hoặc chọn quận nhanh:
  `flex flex-wrap gap-8 mt-12`
  - Pill mỗi quận: `bg #F1F5F9 text #64748B radius-full px-12 py-6 12px`
    hover `bg #EFF6FF text #0066CC`
- Button "Xác nhận": `bg #0066CC text white radius-10 px-20 py-10 full-width mt-16`
  → convert địa chỉ → lat/lng → gọi API

---

## 6. Empty State

`center py-48 text-center px-24`

- SVG icon `location_searching 80px #E2E8F0`
- Title: `"Không tìm thấy địa điểm nào" 18px Inter 600 #1E293B`
- Subtitle: `"Thử tăng bán kính tìm kiếm" 14px #94A3B8 mt-8`
- Radius buttons: "5 km" | "10 km" | "20 km" (quick select)

---

## 7. API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load địa điểm lân cận | GET | `/locations/nearby?lat=&lng=&radius=5` | Khi có GPS coords |
| Đổi bán kính | GET | `/locations/nearby?lat=&lng=&radius={km}` | Click radius pill |
| Filter danh mục | GET | `/locations/nearby?lat=&lng=&radius=&category_id=` | Chọn filter |
| Cập nhật vị trí | — | Browser Geolocation API | Click "Cập nhật vị trí" |
| Thêm yêu thích (🔐) | POST | `/user/favorites` | Click icon yêu thích khi chưa lưu |
| Xóa yêu thích (🔐) | DELETE | `/user/favorites` | Click icon yêu thích khi đã lưu |

**Query params của `/locations/nearby`:**

| Param | Mô tả | Bắt buộc |
|-------|-------|---------|
| `lat` | Vĩ độ | ✅ |
| `lng` | Kinh độ | ✅ |
| `radius` | Bán kính (km) | default: 5 |
