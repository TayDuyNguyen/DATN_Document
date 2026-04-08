# Màn hình: Tìm kiếm (Đã đăng nhập)

> Route: `/search`
> Quyền: 🔐 Đã đăng nhập
> Mô tả: Trang tìm kiếm với thêm lịch sử tìm kiếm cá nhân.

---

## Tái sử dụng từ màn Tìm kiếm (Chưa đăng nhập)

> Xem chi tiết tại `user_search.md`

Giữ nguyên toàn bộ: search bar, autocomplete, filter bar, popular/trending keywords, result grid, pagination, empty state.

---

## Điểm khác biệt duy nhất

### Section 4.3 — Lịch sử tìm kiếm (thêm mới)

**API: `GET /user/search-history?limit=5`**

**Vị trí:** Hiển thị trong trạng thái Default (chưa nhập query), sau Section 4.2 (Xu hướng tìm kiếm)

`mt-32 max-w-800px mx-auto`

- Title: `"Tìm kiếm gần đây" 16px Inter 600 #1E293B mb-12`
  + Button "Xóa tất cả": `12px #EF4444 float-right` → `DELETE /user/search-history` → toast + ẩn section

**List** (`flex flex-col gap-4`):

Mỗi item: `flex justify-between items-center px-14 py-10 bg #F8FAFC border #E2E8F0 radius-10 cursor-pointer`
hover `bg #EFF6FF border #B3D9FF`

- Left: `flex items-center gap-10`
  - icon `history 16px #94A3B8`
  - Keyword: `13px Inter 500 #1E293B`
- Right: icon `close 14px #94A3B8` hover `#EF4444`
  → xóa item đó (không có API xóa từng item — xóa client-side hoặc gọi lại `DELETE /user/search-history` với param)

Click item → điền vào search input + submit tìm kiếm

**Empty state** (chưa có lịch sử):
- Không hiển thị section này

---

## API Mapping (bổ sung)

| Hành động | Method | Endpoint | Trigger |
|-----------|--------|----------|---------|
| Load lịch sử | GET | `/user/search-history?limit=5` | Khi mount + đã đăng nhập + query rỗng |
| Xóa toàn bộ lịch sử | DELETE | `/user/search-history` | Click "Xóa tất cả" |
