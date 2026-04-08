# Component: Đánh dấu đánh giá Hữu ích

> Loại: Inline button (không phải trang riêng)
> Quyền: 🔐 Cần đăng nhập
> Mô tả: Button "Hữu ích" trên mỗi review — cho phép user đánh dấu đánh giá của người khác là hữu ích.

---

## Xuất hiện tại

| Màn hình | Vị trí | Tham chiếu |
|---------|--------|-----------|
| Chi tiết Địa điểm | Dưới mỗi review | `user_location_detail_logged_in.md` Section 4 |
| Chi tiết Tour | Dưới mỗi review | `user_tour_detail.md` Section 3.6 |

---

## Button States

`flex items-center gap-6 cursor-pointer`

| State | Icon | Style | Trigger |
|-------|------|-------|---------|
| Chưa đánh dấu | `thumb_up_outlined 16px #94A3B8` | `"Hữu ích (12)" 12px #94A3B8` | Click → `POST /ratings/{id}/helpful` |
| Đã đánh dấu | `thumb_up 16px #0066CC` (filled) | `"Hữu ích (13)" 12px #0066CC font-600` | Disabled (không thể bỏ) |
| Hover (chưa đánh dấu) | `thumb_up_outlined #0066CC` | `text #0066CC` | — |
| Chưa đăng nhập | `thumb_up_outlined #94A3B8` | `text #94A3B8` | Click → redirect `/login` |

**Transition:** count tăng +1 ngay lập tức (optimistic update) · icon đổi sang filled

---

## Ghi chú

- Mỗi user chỉ đánh dấu được **1 lần** — không thể bỏ đánh dấu
- Không đánh dấu được đánh giá của **chính mình**
- Count hiển thị realtime sau khi click

---

## API Mapping

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Đánh dấu hữu ích | POST | `/ratings/{id}/helpful` | Click button |
