# Màn hình: Chi tiết Bài viết Blog

> Route: `/blog/{slug}`
> Quyền: 🌐 Public — không cần đăng nhập
> Mô tả: Đọc bài viết blog đầy đủ với nội dung rich text, thông tin tác giả, chia sẻ và bài viết liên quan.

---

## Layout tổng thể

```
┌─────────────────────────────────────────────────────────────┐
│  HEADER (dùng chung)                                        │
├─────────────────────────────────────────────────────────────┤
│  BREADCRUMB: Trang chủ / Blog / Tiêu đề bài viết           │
├─────────────────────────────────────────────────────────────┤
│  FEATURED IMAGE: Ảnh đại diện full-width                   │
├──────────────────────────────────┬──────────────────────────┤
│  ARTICLE CONTENT (flex-1)        │  SIDEBAR (300px)         │
│  - Meta: Tác giả + Ngày + Views  │  - Mục lục (TOC)         │
│  - Tiêu đề                       │  - Danh mục blog         │
│  - Danh mục tags                 │  - Bài viết liên quan    │
│  - Nội dung rich text            │  - Share buttons         │
│  - Share buttons                 │                          │
│  - Author card                   │                          │
├─────────────────────────────────────────────────────────────┤
│  SECTION: Bài viết liên quan (grid)                        │
├─────────────────────────────────────────────────────────────┤
│  FOOTER (dùng chung)                                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 1. Breadcrumb

`py-12 border-b #E2E8F0`
`"Trang chủ / Blog / Khám phá Bà Nà Hills" 13px #94A3B8`

---

## 2. Featured Image

`mb-0`

- Ảnh: `full-width max-h-480px object-cover`
- Không có radius (edge-to-edge)

---

## 3. Article Content

`max-w-720px`

### 3.1 Meta

`flex items-center gap-16 py-20 border-b #F1F5F9 mb-24`

- `flex items-center gap-8`:
  - Avatar tác giả: `36x36px rounded-full border #E2E8F0`
  - Name: `13px Inter 600 #1E293B`
- `·` separator `text #E2E8F0`
- Ngày: `13px #94A3B8` — e.g. "15/03/2026"
- `·`
- icon `visibility 14px #94A3B8` + `"1.248 lượt xem" 13px #94A3B8`
- `·`
- icon `schedule 14px #94A3B8` + `"5 phút đọc" 13px #94A3B8`

### 3.2 Tiêu đề

`28px Inter 700 #1E293B letter-spacing -0.3px line-height 1.3 mb-16`

### 3.3 Danh mục Tags

`flex flex-wrap gap-8 mb-24`

- Mỗi tag: `px-12 py-6 bg #EFF6FF border #B3D9FF text #0066CC radius-full 12px Inter 600 cursor-pointer`
  hover `bg #0066CC text white`
  → navigate `/blog?category_id={id}`

### 3.4 Nội dung Rich Text

`prose max-w-none`

**Typography cho nội dung:**
- `h2`: `22px Inter 700 #1E293B mt-32 mb-12`
- `h3`: `18px Inter 600 #1E293B mt-24 mb-8`
- `p`: `16px Inter 400 #1E293B line-height 1.8 mb-16`
- `ul/ol`: `16px #1E293B line-height 1.8 pl-24 mb-16`
- `li`: `mb-8`
- `blockquote`: `border-l-4 border-#0066CC pl-16 py-4 bg #EFF6FF radius-r-8 italic 16px #64748B my-20`
- `img`: `full-width radius-12 my-20 shadow-card`
- `a`: `text #0066CC underline` hover `text #004999`
- `strong`: `font-700 #1E293B`
- `code`: `bg #F1F5F9 px-6 py-2 radius-4 13px monospace #EF4444`
- `pre`: `bg #1E293B text #F8FAFC p-20 radius-12 overflow-x-auto my-20 13px monospace`

### 3.5 Share Buttons

`flex items-center gap-12 py-20 border-y #F1F5F9 mt-32 mb-24`

- Label: `"Chia sẻ:" 13px Inter 600 #64748B`
- Facebook: `flex items-center gap-6 px-14 py-8 bg #1877F2 text white radius-8 13px 600`
- Twitter/X: `flex items-center gap-6 px-14 py-8 bg #000000 text white radius-8 13px 600`
- Copy link: `flex items-center gap-6 px-14 py-8 border #E2E8F0 bg white text #64748B radius-8 13px 600`
  hover `border #0066CC text #0066CC`
  → copy URL to clipboard + toast "Đã sao chép!"

### 3.6 Author Card

`bg #F8FAFC border #E2E8F0 radius-16 p-20 mb-32`

`flex items-start gap-16`

- Avatar: `64x64px rounded-full border-2 #E2E8F0`
- Right:
  - Label: `"TÁC GIẢ" 10px uppercase #94A3B8 mb-4`
  - Name: `18px Inter 700 #1E293B`
  - Bio: `13px #64748B mt-4 line-height 1.6`
  - `flex gap-8 mt-12`:
    - Social links (nếu có): icon `24x24px border #E2E8F0 radius-full bg white color #64748B`
      hover `border #0066CC color #0066CC`

---

## 4. Sidebar

`width 300px flex-shrink-0`

### 4.1 Mục lục (Table of Contents)

**Card:** `bg white border #E2E8F0 radius-16 p-20 mb-16 sticky top-24`

- Title: `"Mục lục" 14px Inter 600 #1E293B mb-12`
- List (`space-y-4`):
  - Mỗi heading: `flex items-center gap-8 px-8 py-6 radius-6 cursor-pointer 13px #64748B`
    hover `bg #EFF6FF text #0066CC`
    - H2: `pl-8`
    - H3: `pl-20 text-12`
  - Active (đang đọc): `bg #EFF6FF text #0066CC font-600`
  - Click → scroll to heading (smooth)

### 4.2 Danh mục Blog

**Card:** `bg white border #E2E8F0 radius-16 p-20 mb-16`

- Title: `"Danh mục" 14px Inter 600 #1E293B mb-12`
- List (`space-y-4`):
  - Mỗi item: `flex justify-between items-center px-8 py-8 radius-6 cursor-pointer`
    hover `bg #EFF6FF`
    - Tên: `13px #64748B`
    - Count: `12px #94A3B8`
  - → navigate `/blog?category_id={id}`

### 4.3 Bài viết liên quan

**Card:** `bg white border #E2E8F0 radius-16 p-20 mb-16`

- Title: `"Bài viết liên quan" 14px Inter 600 #1E293B mb-12`
- List 4 bài (`space-y-12`):
  - Mỗi item: `flex gap-10 cursor-pointer`
    hover `opacity-80`
    - Thumbnail: `56x56px radius-8 object-cover flex-shrink-0`
    - Right:
      - Tiêu đề: `12px Inter 600 #1E293B` max 2 lines
      - Ngày: `11px #94A3B8 mt-4`
    - → navigate `/blog/{slug}`

### 4.4 Share Buttons (Sidebar)

**Card:** `bg white border #E2E8F0 radius-16 p-20`

- Title: `"Chia sẻ bài viết" 14px Inter 600 #1E293B mb-12`
- `flex flex-col gap-8`:
  - Facebook: full-width button
  - Twitter/X: full-width button
  - Copy link: full-width button

---

## 5. Bài viết liên quan (Bottom)

`py-48 bg #F8FAFC`

- Title: `"Bài viết liên quan" 22px Inter 700 #1E293B mb-24`

`grid grid-cols-1 md:grid-cols-3 gap-20`

Mỗi card (same style as blog list card):
- Thumbnail + Body (tiêu đề + excerpt + meta)
- → navigate `/blog/{slug}`

---

## 6. Reading Progress Bar

`fixed top-0 left-0 h-3px bg #0066CC z-50`
- Width: dynamic theo scroll position (0% → 100%)
- Transition: `width 100ms linear`

---

## 7. API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load bài viết | GET | `/blog/{slug}` | Khi mount (tự động tăng view_count) |
| Load danh mục (sidebar) | GET | `/blog/categories` | Khi mount |

> Bài viết liên quan và bài phổ biến trong sidebar có thể lấy từ cùng `GET /blog` với filter `category_id` của bài hiện tại.

---

## Validation & States

| Hạng mục | Quy tắc |
|---|---|
| Slug | Bắt buộc có slug; nếu slug rỗng chuyển 404 |
| Không tìm thấy | Nếu `GET /blog/{slug}` trả 404, hiển thị trang bài viết không tồn tại và CTA về `/blog` |
| Bài chưa publish | Public không hiển thị bài `draft`/`archived`; admin preview cần route riêng nếu có |
| Nội dung rỗng | Nếu content rỗng, hiển thị excerpt hoặc thông báo đang cập nhật |
| Ảnh lỗi | Dùng ảnh placeholder, không làm vỡ hero/sidebar |
| Related posts | Nếu không có bài liên quan, ẩn section thay vì hiển thị danh sách rỗng |
