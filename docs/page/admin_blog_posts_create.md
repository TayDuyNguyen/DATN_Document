# Màn hình: Tạo Bài viết Blog

> Route: `/admin/blog-posts/create`
> Quyền: 🛡️ Admin / Staff
> Mô tả: Form tạo bài viết blog mới với rich text editor, ảnh đại diện, danh mục và cài đặt xuất bản.

---

## Layout tổng thể

```
┌─────────────────────────────────────────────────────────────────┐
│  HEADER: Breadcrumb + Tiêu đề + [Hủy] [Lưu nháp] [Xuất bản]   │
├──────────────────────────────────────┬──────────────────────────┤
│  LEFT COLUMN (65%)                   │  RIGHT COLUMN (320px)    │
│                                      │  sticky top-24           │
│  Section 1: Nội dung bài viết        │  Card 1: Xuất bản        │
│  - Tiêu đề                           │  Card 2: Danh mục        │
│  - Excerpt (mô tả ngắn)              │  Card 3: Ảnh đại diện    │
│  - Rich text editor (nội dung)       │  Card 4: Hướng dẫn       │
└──────────────────────────────────────┴──────────────────────────┘
```

---

## 1. Page Header

| Element | Style |
|---------|-------|
| Breadcrumb | `12px Inter 500 #94A3B8` — "Blog / Danh sách Bài viết / Tạo mới" |
| Title | `24px Inter 700 #1E293B` — "Tạo Bài viết mới" |
| Subtitle | `14px Inter 400 #64748B` — "Viết và xuất bản bài viết blog du lịch" |

**Buttons bên phải** (`flex gap-3`):

| Button | Style | Action |
|--------|-------|--------|
| Hủy | `border #E2E8F0 bg white text #64748B radius-10 px-20 py-10` hover `border #EF4444 text #EF4444` | Navigate `/admin/blog-posts` |
| Lưu nháp | `border #E2E8F0 bg white text #64748B radius-10 px-20 py-10` hover `border #0066CC text #0066CC` | Submit `status=draft` |
| Xuất bản | `bg #0066CC text white radius-10 px-20 py-10 shadow 14px 600` hover `bg #004999` | Submit `status=published` |

---

## 2. Left Column

### Section 1 — Nội dung bài viết

**Card:** `bg white border #E2E8F0 radius-16 p-24`

**Field "Tiêu đề bài viết"** ✅:
- Input text, `font-size 20px Inter 600 #1E293B`
- placeholder "Nhập tiêu đề bài viết..."
- `border-none border-b border-#E2E8F0 radius-0 px-0 py-12`
- focus: `border-b-2 border-#0066CC`
- Character counter: `"0/200" 11px #94A3B8 text-right mt-4`

**Field "Slug"** (mt-12):
- `flex items-center gap-8`
- Label: `"URL:" 12px #94A3B8`
- Input text: `flex-1 border #E2E8F0 radius-8 px-12 py-6 13px #64748B`
- placeholder "tieu-de-bai-viet"
- Badge "Tự động": `bg #EFF6FF text #0066CC 11px radius-6 px-8 py-2`
- Helper: `"danangtrip.vn/blog/[slug]" 11px #94A3B8 mt-4`

**Field "Mô tả ngắn (Excerpt)"** (mt-20):
- Label: `"Mô tả ngắn" 13px Inter 600 #1E293B mb-6`
- Textarea `rows-3`
- placeholder "Mô tả ngắn gọn về bài viết, hiển thị trong danh sách..."
- `border #E2E8F0 radius-10 px-14 py-10 14px Inter resize-none`
- Character counter: `"0/300" 11px #94A3B8 text-right mt-4`

**Rich Text Editor** (mt-20):
- Label: `"Nội dung" 13px Inter 600 #1E293B mb-6` + badge "Bắt buộc" `bg #FEE2E2 text #EF4444 11px radius-full px-8 py-2`

- Toolbar (bg #F8FAFC, border #E2E8F0, radius-t-10, px-12 py-8, flex gap-4 flex-wrap):
  - Group 1 — Text format:
    icon `format_bold` | `format_italic` | `format_underline` | `strikethrough_s`
  - Divider: `1px solid #E2E8F0 h-20px`
  - Group 2 — Heading:
    Dropdown "Đoạn văn ▾" → H1 / H2 / H3 / Đoạn văn
  - Divider
  - Group 3 — List:
    icon `format_list_bulleted` | `format_list_numbered`
  - Divider
  - Group 4 — Insert:
    icon `link` | `image` (upload ảnh inline → POST /upload/image) | `format_quote`
  - Divider
  - Group 5 — Align:
    icon `format_align_left` | `format_align_center` | `format_align_right`

  - Mỗi toolbar button: `28x28px radius-6 color #64748B`
    hover: `bg #EFF6FF color #0066CC`
    active: `bg #EFF6FF color #0066CC border #B3D9FF`

- Editor area:
  `min-h-400px border #E2E8F0 radius-b-10 px-20 py-16 14px Inter #1E293B line-height 1.8`
  focus: `border #0066CC`
  placeholder: `"Bắt đầu viết nội dung bài viết..." color #94A3B8`

---

## 3. Right Column — Sidebar

### Card 1 — Xuất bản
`bg white border #E2E8F0 radius-16 p-20 mb-16`

Title: `"Xuất bản" 14px Inter 600 #1E293B mb-16`

**Trạng thái** (radio group `flex-col gap-10`):
| Option | Badge | Helper |
|--------|-------|--------|
| ● Bản nháp (draft) — default | `bg #FEF3C7 text #F59E0B` "BẢN NHÁP" | "Chưa hiển thị công khai" |
| ○ Xuất bản ngay (published) | `bg #D1FAE5 text #10B981` "XUẤT BẢN" | "Hiển thị ngay sau khi lưu" |
| ○ Lên lịch (scheduled) | `bg #EFF6FF text #0066CC` "LÊN LỊCH" | "Xuất bản vào thời điểm đã chọn" |

**Khi chọn "Lên lịch"** → hiện thêm:
- `flex gap-8 mt-8`:
  - Input date: `flex-1 border #E2E8F0 radius-8 px-10 py-8 13px`
  - Input time: `w-100px border #E2E8F0 radius-8 px-10 py-8 13px`

**Divider** `1px #F1F5F9 my-16`

**Buttons:**
- "Xuất bản": `bg #0066CC text white radius-10 py-12 full-width 14px 600 shadow`
- "Lưu nháp": `border #E2E8F0 bg white text #64748B radius-10 py-12 full-width mt-8`

---

### Card 2 — Danh mục
`bg white border #E2E8F0 radius-16 p-20 mb-16`

Title: `"Danh mục" 14px Inter 600 #1E293B mb-12`

Load từ `GET /admin/blog-categories`:
- Checkbox list (`space-y-8`):
  - Mỗi item: `flex items-center gap-8`
    - Checkbox `16px accent-color #0066CC`
    - Label: `13px Inter 500 #1E293B`
  - Checked: label `color #0066CC font-600`

- Button "Thêm danh mục mới" (`mt-12`):
  `border dashed #B3D9FF bg #EFF6FF/50 text #0066CC radius-8 py-8 full-width 12px 600`
  icon `add` bên trái
  → mở mini form inline:
    Input tên + Button "Thêm" → `POST /admin/blog-categories`

---

### Card 3 — Ảnh đại diện
`bg white border #E2E8F0 radius-16 p-20 mb-16`

Title: `"Ảnh đại diện" 14px Inter 600 #1E293B mb-12`

Upload zone: `h-160px border-2 dashed #E2E8F0 radius-12 bg #F8FAFC flex-col center gap-8`
- icon `upload_file 40px #94A3B8`
- Text `"Kéo thả ảnh vào đây hoặc" 14px #64748B`
- Button "Chọn ảnh": `bg #EFF6FF text #0066CC radius-8 px-16 py-8 13px 600`
- Helper: `"PNG, JPG, WEBP · Tối đa 5MB · Khuyến nghị 1200x630px" 12px #94A3B8`

Khi có ảnh: preview `full-width h-160px object-cover radius-12`
Overlay hover: button "Thay đổi" + "Xóa"

API: `POST /upload/image`

---

### Card 4 — Hướng dẫn
`bg #EFF6FF border #B3D9FF radius-16 p-20`

- Title: `"💡 Lưu ý" 13px Inter 600 #0066CC mb-12`
- Items: icon `arrow_right #0066CC` + `12px #1E293B`
  - "Tiêu đề nên ngắn gọn, có từ khóa SEO"
  - "Ảnh đại diện tỷ lệ 16:9 (1200x630px)"
  - "Mô tả ngắn hiển thị trong kết quả tìm kiếm"
  - "Lưu nháp trước khi xuất bản để kiểm tra"

---

## 4. Validation & States

| Tình huống | Xử lý |
|-----------|-------|
| Tiêu đề trống | Border `#EF4444` · error text `12px #EF4444` |
| Nội dung trống | Border editor `#EF4444` · error text |
| Đang submit | Button disabled · spinner · "Đang lưu..." · `bg #3385D6` |
| Lưu nháp thành công | Toast `bg #FEF3C7 text #F59E0B` "Đã lưu bản nháp!" · redirect `/admin/blog-posts/{id}/edit` |
| Xuất bản thành công | Toast `bg #D1FAE5 text #10B981` "Bài viết đã được xuất bản!" · redirect `/admin/blog-posts/{id}` |
| Thất bại | Toast `bg #FEE2E2 text #EF4444` "Có lỗi xảy ra." |

---

## 5. API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load danh mục | GET | `/admin/blog-categories` | Khi mount |
| Upload ảnh đại diện | POST | `/upload/image` | Chọn ảnh featured |
| Upload ảnh inline | POST | `/upload/image` | Click icon ảnh trong toolbar editor |
| Tạo bài viết | POST | `/admin/blog-posts` | Submit form |
| Tạo danh mục mới | POST | `/admin/blog-categories` | Submit mini form |

**Body POST /admin/blog-posts:**
```json
{
  "title": "*",
  "content": "*",
  "excerpt": "",
  "featured_image": "",
  "category_ids": [],
  "status": "draft",
  "published_at": ""
}
```
