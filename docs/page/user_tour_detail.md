# Màn hình: Chi tiết Tour

> Route: `/tours/{slug}`
> Quyền: 🌐 Public — không cần đăng nhập
> Mô tả: Xem đầy đủ thông tin tour — ảnh, mô tả, lịch trình, bao gồm/không bao gồm, lịch khởi hành, đánh giá và đặt tour.

---

## Layout tổng thể

```
┌─────────────────────────────────────────────────────────────┐
│  HEADER (dùng chung)                                        │
├─────────────────────────────────────────────────────────────┤
│  BREADCRUMB: Trang chủ / Tour / Tên tour                   │
├─────────────────────────────────────────────────────────────┤
│  IMAGE GALLERY: Ảnh chính + Grid ảnh phụ                   │
├──────────────────────────────────┬──────────────────────────┤
│  LEFT COLUMN (flex-1)            │  RIGHT COLUMN (380px)    │
│                                  │  sticky top-24           │
│  - Tên + Badges + Info bar       │  Card: Đặt tour          │
│  - Mô tả                         │  - Chọn lịch khởi hành  │
│  - Lịch trình (timeline)         │  - Số lượng người        │
│  - Bao gồm / Không bao gồm       │  - Tính giá             │
│  - Điểm tập trung + Bản đồ       │  - Button Đặt ngay      │
│  - Đánh giá                      │                          │
├─────────────────────────────────────────────────────────────┤
│  FOOTER (dùng chung)                                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 1. Breadcrumb

`py-12 border-b #E2E8F0`
`"Trang chủ / Tour / Bà Nà Hills - Cầu Vàng" 13px #94A3B8`

---

## 2. Image Gallery

Tương tự màn Chi tiết Địa điểm — ảnh chính + grid ảnh phụ + lightbox.

---

## 3. Left Column

### 3.1 Tên + Badges + Info bar

**Tên + Badges:**
- Tên: `28px Inter 700 #1E293B letter-spacing -0.3px`
- `flex items-center gap-8 mt-8`:
  - Badge danh mục: `bg #FFE0D4 text #FF6B35 12px 600 radius-full px-10 py-4`
  - Badge "⭐ NỔI BẬT" (nếu is_featured): `bg #EFF6FF text #0066CC`
  - Badge "🔥 HOT" (nếu is_hot): `bg #FF6B35 text white`

**Info bar** (`flex flex-wrap gap-20 py-20 border-y #F1F5F9 mb-24`):

| Icon | Label | Value |
|------|-------|-------|
| `schedule #FF6B35` | Thời lượng | "1 ngày" |
| `group #0066CC` | Số người | "Tối đa 20 · Tối thiểu 2" |
| `access_time #10B981` | Giờ khởi hành | "07:00" |
| `flag #F59E0B` | Điểm tập trung | "Trước cổng Bà Nà Hills" |
| `star #F59E0B` | Đánh giá | "4.8 · 128 đánh giá" |

### 3.2 Mô tả

- Title: `"Giới thiệu tour" 18px Inter 600 #1E293B mb-12`
- Text: `15px Inter 400 #1E293B line-height 1.7`
- Nếu dài: 4 dòng + "Xem thêm ▾" `13px #FF6B35`

### 3.3 Lịch trình (Itinerary)

`mb-24`

- Title: `"Lịch trình" 18px Inter 600 #1E293B mb-16`

**Timeline:**
- Mỗi ngày: `flex gap-16`
  - Left: `flex flex-col items-center`
    - Badge "Ngày 1": `28x28px bg #FFE0D4 text #FF6B35 12px 700 rounded-full flex-shrink-0`
    - Line: `flex-1 w-2px bg #E2E8F0 mx-auto` (không có ở ngày cuối)
  - Right: `pb-20`
    - Content: `14px Inter 400 #1E293B line-height 1.7 white-space pre-wrap`

### 3.4 Bao gồm & Không bao gồm

`mb-24 grid grid-cols-2 gap-20`

**Bao gồm:**
- Title: `"✓ Bao gồm" 15px Inter 600 #10B981 mb-12`
- List: mỗi item `flex gap-8`
  - icon `check_circle 16px #10B981`
  - Text `14px #1E293B`

**Không bao gồm:**
- Title: `"✗ Không bao gồm" 15px Inter 600 #EF4444 mb-12`
- List: mỗi item `flex gap-8`
  - icon `cancel 16px #EF4444`
  - Text `14px #1E293B`

### 3.5 Điểm tập trung + Bản đồ

`mb-24`

- Title: `"Điểm tập trung" 18px Inter 600 #1E293B mb-12`
- `flex items-start gap-12 mb-16`:
  - icon `location_on 20px #FF6B35`
  - Address: `14px Inter 500 #1E293B`
- Map: `h-200px bg #F1F5F9 radius-12 overflow-hidden`
  - iframe Google Maps với marker

### 3.6 Đánh giá

Tương tự màn Chi tiết Địa điểm — Rating overview + distribution + review list.

**API:** `GET /tours/{id}/ratings` · `GET /tours/{id}/rating-stats`

---

## 4. Right Column — Card Đặt tour (Sticky)

**Card:** `bg white border #E2E8F0 radius-16 p-24 sticky top-24`

### 4.1 Giá

`flex items-end gap-8 mb-20`

- Giá gốc (nếu có giảm): `"1.000.000 đ" 14px #94A3B8 line-through`
- Giá: `"850.000 đ" 28px Inter 700 #FF6B35`
- `"/ người lớn" 13px #94A3B8`

Nếu có giảm giá:
- Badge: `"-15%" bg #FEE2E2 text #EF4444 12px 700 radius-full px-8 py-3 ml-8`

### 4.2 Chọn lịch khởi hành

**API: `GET /tours/{id}/schedules?from=&to=`**

- Label: `"Chọn ngày khởi hành *" 13px Inter 600 #1E293B mb-8`

**Date picker mini:**
- `border #E2E8F0 radius-10 p-12`
- Hiển thị tháng hiện tại
- Ngày có lịch: highlight `bg #FFE0D4 text #FF6B35 rounded-full`
- Ngày đã chọn: `bg #FF6B35 text white rounded-full`
- Ngày hết chỗ: `text #94A3B8 line-through cursor-not-allowed`
- Ngày đã qua: `text #E2E8F0 cursor-not-allowed`

**Thông tin lịch đã chọn** (hiện sau khi chọn ngày):
`bg #FFF5F0 border rgba(255,107,53,0.2) radius-10 p-12 mt-8`
- `"15/04/2026 · Còn 8/20 chỗ" 13px Inter 500 #FF6B35`
- Progress bar: `h-4px bg #E2E8F0 radius-full` · fill `bg #FF6B35` width 40%

### 4.3 Số lượng người

- Label: `"Số lượng *" 13px Inter 600 #1E293B mb-8`

**Counter group** (`space-y-8`):

Mỗi loại (Người lớn / Trẻ em / Em bé):
- `flex justify-between items-center`
  - Left:
    - Label: `"Người lớn" 13px Inter 500 #1E293B`
    - Giá: `"850.000 đ/người" 12px #94A3B8`
  - Right: `flex items-center gap-12`
    - Button `-`: `24x24px border #E2E8F0 radius-full bg white color #64748B`
      disabled khi = 0 (hoặc min)
    - Count: `16px Inter 700 #1E293B w-24px text-center`
    - Button `+`: `24x24px bg #FF6B35 text white rounded-full`
      disabled khi = max

### 4.4 Tính giá

**API: `POST /tours/{id}/check-availability`** (khi chọn đủ thông tin)

`bg #F8FAFC border #E2E8F0 radius-10 p-14 mt-16`

- Rows (`space-y-8 flex justify-between 13px`):
  - "Người lớn × 2": "1.700.000 đ" `#1E293B`
  - "Trẻ em × 1": "500.000 đ" `#1E293B`
  - Divider `1px #E2E8F0`
  - "TỔNG CỘNG": `"2.200.000 đ" 18px Inter 700 #FF6B35`

**Trạng thái còn chỗ:**
- Còn chỗ: `"✓ Còn 8 chỗ trống" 12px #10B981`
- Sắp hết: `"⚠ Chỉ còn 2 chỗ!" 12px #F59E0B`
- Hết chỗ: `"✗ Hết chỗ cho ngày này" 12px #EF4444`

### 4.5 Buttons

**Button "Đặt ngay":**
- Có đủ thông tin + còn chỗ: `bg #FF6B35 text white radius-12 py-14 full-width 16px 600 shadow`
  hover `bg #E55A2B`
  → navigate `/tours/{slug}/book` (🔐 redirect login nếu chưa đăng nhập)

**Button "Thêm vào yêu thích":**
- `border #E2E8F0 bg white text #64748B radius-12 py-12 full-width mt-8 13px 600` icon `favorite_border`
- 🔐 Cần đăng nhập

**Button "Chia sẻ":**
- `border #E2E8F0 bg white text #64748B radius-12 py-12 full-width mt-8 13px 600` icon `share`

### 4.6 Chính sách

`mt-16 space-y-8`

- icon `verified 16px #10B981` + `"Đặt chỗ miễn phí, hủy linh hoạt" 12px #64748B`
- icon `support_agent 16px #0066CC` + `"Hỗ trợ 24/7" 12px #64748B`
- icon `security 16px #F59E0B` + `"Thanh toán an toàn" 12px #64748B`

---

## 5. Sticky Bottom Bar (Mobile)

**Chỉ hiển thị trên mobile khi scroll qua card đặt tour**

`fixed bottom-0 left-0 right-0 bg white border-t #E2E8F0 px-16 py-12 flex justify-between items-center z-50`

- Left: Giá `"850.000 đ / người" 16px Inter 700 #FF6B35`
- Right: Button "Đặt ngay" `bg #FF6B35 text white radius-10 px-24 py-12 15px 600`

---

## 6. API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load chi tiết tour | GET | `/tours/{slug}` | Khi mount |
| Load lịch khởi hành | GET | `/tours/{id}/schedules?from=&to=` | Khi mount + đổi tháng |
| Load đánh giá | GET | `/tours/{id}/ratings?page=1&per_page=5` | Khi mount |
| Load rating stats | GET | `/tours/{id}/rating-stats` | Khi mount |
| Kiểm tra còn chỗ | POST | `/tours/{id}/check-availability` | Khi chọn đủ ngày + số người |
| Kiểm tra đã đánh giá (🔐) | GET | `/ratings/check?tour_id={id}` | Khi mount + đã đăng nhập |
| Gửi đánh giá (🔐) | POST | `/ratings` | Submit modal |
| Thêm yêu thích (🔐) | POST | `/user/favorites` | Click button yêu thích khi chưa lưu |
| Xóa yêu thích (🔐) | DELETE | `/user/favorites` | Click button yêu thích khi đã lưu |

**Body POST /tours/{id}/check-availability:**
```json
{
  "schedule_id": "*",
  "quantity_adult": "*",
  "quantity_child": 0,
  "quantity_infant": 0
}
```
