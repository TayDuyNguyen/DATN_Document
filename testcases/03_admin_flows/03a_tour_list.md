# Admin — Danh sách Tour (Tour List Page)

**Route:** `/admin/tours/list`  
**Source:** `danangtrip-admin/src/pages/Tours/TourList/`  
**Automation:** `tests/admin/tours-list.spec.ts` · `tests/admin/tours-list-extended.spec.ts` · `tests/api/admin-tours-list.api.spec.ts`  
**POM:** `TourListPage.ts` · Mock: `tests/fixtures/api/tours.mock.ts`

**Modal chi tiết tour:** `03d_tour_detail_modal.md` · `tests/admin/tours-detail-modal.spec.ts` (25 TC — **không** nằm trong file này)

---

## 1. Phạm vi

| Hạng mục | Chi tiết |
|----------|----------|
| Vai trò | **Admin** (`PrivateRoute` — không có Staff) |
| URL query | **Không** — filter/page/limit là React state local |
| API list | `GET /api/v1/admin/tours` — `page`, `per_page`, `search`, `tour_category_id`, `status`, `booking_availability`, `is_featured`, `is_hot`, `sort_by`, `sort_order` |
| API stats | 4× `GET /admin/tours?per_page=1` (total, active, featured, sold_out) |
| API categories | `GET /api/v1/tour-categories` |
| Mutations | `PATCH .../status`, `PATCH .../featured`, `PATCH .../hot`, `DELETE .../:id` |
| Export | `GET /admin/tours/export` → blob `danh-sach-tour_YYYY-MM-DD.xlsx` |
| Sort UI | **Không có** — API luôn `sort_by=created_at`, `sort_order=desc` |
| Status từng dòng | **Không có toggle** — chỉ badge read-only + bulk toolbar |

## 2. Điều kiện tiên quyết

- Admin đã đăng nhập · dev server `:5173`
- Mock: `mockToursApi` (12 tour, 2 trang @ limit 10) · `initialMockTours` trong `tours.data.ts`
- Chạy test: `npm run test:admin:tour-list`

## 3. Tổng quan trạng thái automation

| Nhóm | Tổng TC | ✅ Auto | ⏳ Backlog |
|------|---------|---------|------------|
| Auth & routing | 3 | 3 | 0 |
| Header & navigation | 3 | 3 | 0 |
| Stats cards | 4 | 4 | 0 |
| Filter & search | 15 | 15 | 0 |
| Bảng — hiển thị | 10 | 10 | 0 |
| Selection & bulk | 10 | 10 | 0 |
| Toggle featured/hot | 4 | 4 | 0 |
| Pagination & refresh | 6 | 6 | 0 |
| Export | 4 | 4 | 0 |
| Delete dialog UX | 4 | 4 | 0 |
| View → modal (smoke) | 1 | 1 | 0 |
| i18n | 1 | 1 | 0 |
| **UI subtotal** | **65** | **65** | **0** |
| API smoke | 18 | 17 | 1 |
| **Tổng** | **83** | **82** | **1** |

> **Kết luận:** **82/83 auto** (UI 65/65 + API 17/18; `API_TLIST_017` skip khi không login được user test). Modal chi tiết đầy đủ → `03d`.

---

## 4. Test cases — Auth & routing (P0)

| ID | Mô tả | Dữ liệu | Auto |
|----|--------|---------|------|
| TC_AD_TLIST_013 | Guest `/admin/tours/list` → redirect `/login` | Không token | ✅ |
| TC_AD_TLIST_014 | User `role=user` → redirect `/login` | `seedNonAdminSession` | ✅ |
| TC_AD_TLIST_015 | Sidebar submenu Tours → Tour List | Navigation | ✅ |

---

## 5. Header & navigation (P1)

| ID | Mô tả | Dữ liệu | Auto |
|----|--------|---------|------|
| TC_AD_TLIST_001 | Render heading, breadcrumb, stats section, filter, bảng 10 dòng | 12 tour mock | ✅ |
| TC_AD_TLIST_011 | Nút **Thêm tour** → `/admin/tours/create` | — | ✅ |
| TC_AD_TLIST_016 | Breadcrumb: Quản lý Tour → Danh sách Tour | — | ✅ |

---

## 6. Stats cards — 4 thẻ (P1)

| ID | Mô tả | Dữ liệu | Auto |
|----|--------|---------|------|
| TC_AD_TLIST_017 | 4 label: Tổng tour / Đang hoạt động / Nổi bật / Hết chỗ | — | ✅ |
| TC_AD_TLIST_018 | Values khớp mock (total, active, featured, `booking_availability=sold_out`) | Fixture counts | ✅ |
| TC_AD_TLIST_019 | Loading skeleton → hiện số | Slow API mock | ✅ |
| TC_AD_TLIST_020 | Sau delete/toggle → stats refetch (`tourKeys.all`) | Delete 1 tour | ✅ |

---

## 7. Filter & search (P1)

| ID | Mô tả | Dữ liệu | Auto |
|----|--------|---------|------|
| TC_AD_TLIST_002 | Tìm kiếm keyword | `Ba Na` | ✅ |
| TC_AD_TLIST_003 | Lọc status **active** | Tour inactive ẩn | ✅ |
| TC_AD_TLIST_021 | Lọc status **inactive** | Tour Bán đảo Sơn Trà, Mỹ Sơn | ✅ |
| TC_AD_TLIST_022 | Lọc **danh mục** (Mountain / category_id=2) | Tour Sơn Trà, Huế | ✅ |
| TC_AD_TLIST_023 | Lọc **Còn chỗ** (`booking_availability=open`) | — | ✅ |
| TC_AD_TLIST_024 | Lọc **Hết chỗ** (`booking_availability=sold_out`) | id 4, 9 | ✅ |
| TC_AD_TLIST_025 | Lọc **type = featured** | `is_featured=1` | ✅ |
| TC_AD_TLIST_026 | Lọc **type = hot** | `is_hot=1` | ✅ |
| TC_AD_TLIST_027 | Lọc **type = normal** | không featured & không hot | ✅ |
| TC_AD_TLIST_028 | **Kết hợp** nhiều filter (category + status + type) | — | ✅ |
| TC_AD_TLIST_029 | Search **không có kết quả** → empty state | keyword `xyz` | ✅ |
| TC_AD_TLIST_030 | Nút **Đặt lại** hiện khi có filter + reset về 12 rows | — | ✅ |
| TC_AD_TLIST_031 | **Active filter tags** (category/status/type) + click × xóa tag | — | ✅ |
| TC_AD_TLIST_032 | Search debounce **300ms** — không spam request | Gõ nhanh | ✅ |
| TC_AD_TLIST_033 | Đổi filter → **page reset về 1** | Đang ở page 2 | ✅ |
| TC_AD_TLIST_034 | Category select **searchable** trong dropdown | Gõ "City" | ✅ |

---

## 8. Bảng — hiển thị cột & edge cases (P1–P2)

| ID | Mô tả | Dữ liệu | Auto |
|----|--------|---------|------|
| TC_AD_TLIST_035 | Cột giá format VNĐ + "/ người" | Tour Ba Na 850.000 | ✅ |
| TC_AD_TLIST_036 | Tour **không thumbnail** — icon placeholder | Tour Tam Kỳ | ✅ |
| TC_AD_TLIST_037 | `schedules_count=0` → đỏ **Hết lịch** | Tour Tam Kỳ | ✅ |
| TC_AD_TLIST_038 | **StatusBadge** active vs inactive | — | ✅ |
| TC_AD_TLIST_039 | **BookingAvailabilityBadge** open vs sold_out | — | ✅ |
| TC_AD_TLIST_040 | Row tags Featured / Hot / Thường | — | ✅ |
| TC_AD_TLIST_041 | Slug hiển thị; fallback `TOUR-XXX` khi thiếu slug | — | ✅ |
| TC_AD_TLIST_042 | **STT trang 2** bắt đầu từ 11 (limit 10) | Page 2 | ✅ |
| TC_AD_TLIST_043 | Row **selected** — highlight bg teal + border trái | Checkbox | ✅ |
| TC_AD_TLIST_044 | Giá **0** hiển thị đúng | Tour dù lượn | ✅ |

---

## 9. Selection & bulk actions (P1)

| ID | Mô tả | Dữ liệu | Auto |
|----|--------|---------|------|
| TC_AD_TLIST_005 | Bulk **deactivate** 1 tour (thay toggle từng dòng) | Tour Hội An id=2 | ✅ |
| TC_AD_TLIST_007 | Bulk **activate** nhiều tour + toast | id 4, 8 inactive | ✅ |
| TC_AD_TLIST_008 | **Xóa 1 tour** — confirm dialog + DELETE | Tour dù lượn id=12 | ✅ |
| TC_AD_TLIST_009 | **Bulk delete** 2 tour — dialog xác nhận | id 2, 3 | ✅ |
| TC_AD_TLIST_045 | **Select all** trên trang → toolbar "Đã chọn N" | — | ✅ |
| TC_AD_TLIST_046 | Select all → **đổi trang** — selection vẫn giữ | Document behavior | ✅ |
| TC_AD_TLIST_047 | Đổi filter/limit → **selection cleared** | — | ✅ |
| TC_AD_TLIST_048 | Bulk deactivate **nhiều** tour + toast | — | ✅ |
| TC_AD_TLIST_049 | Bulk toolbar **ẩn** khi bỏ chọn hết | — | ✅ |
| TC_AD_TLIST_050 | Bulk delete **hủy** dialog → tours còn nguyên | — | ✅ |
| TC_AD_TLIST_051 | Single delete **hủy** / đóng × → không DELETE | — | ✅ |

---

## 10. Toggle featured / hot (P1)

| ID | Mô tả | Dữ liệu | Auto |
|----|--------|---------|------|
| TC_AD_TLIST_006 | Toggle featured ON + hot ON trên dòng | Tour Hội An id=2 | ✅ |
| TC_AD_TLIST_053 | Toggle featured **OFF** (tour đã featured) | Tour Ba Na id=1 | ✅ |
| TC_AD_TLIST_054 | Toggle hot **OFF** | — | ✅ |
| TC_AD_TLIST_055 | PATCH featured/hot **API lỗi** → rollback UI + toast | Mock 500 | ✅ |

---

## 11. Pagination & refresh (P1)

| ID | Mô tả | Dữ liệu | Auto |
|----|--------|---------|------|
| TC_AD_TLIST_004 | Page 2 + đổi limit **20** | `waitForResponse` page=2, per_page=20 | ✅ |
| TC_AD_TLIST_057 | **Prev** disabled trang 1; **Next** disabled trang cuối | — | ✅ |
| TC_AD_TLIST_058 | Click **Prev/Next** (không chỉ số trang) | — | ✅ |
| TC_AD_TLIST_059 | Ellipsis khi nhiều trang | Mock >20 tours | ✅ |
| TC_AD_TLIST_060 | Limit **50** | — | ✅ |
| TC_AD_TLIST_061 | Nút **Refresh** → refetch list + icon spin | — | ✅ |

---

## 12. Export (P1)

| ID | Mô tả | Dữ liệu | Auto |
|----|--------|---------|------|
| TC_AD_TLIST_010 | Export → GET 200 | — | ✅ |
| TC_AD_TLIST_063 | Export với **filter active** — URL chứa params | status=active | ✅ |
| TC_AD_TLIST_064 | Export **disabled/spinner** khi pending | — | ✅ |
| TC_AD_TLIST_065 | Export **API lỗi** → toast error | Mock 500 | ✅ |

---

## 13. Delete dialog UX (P2)

| ID | Mô tả | Dữ liệu | Auto |
|----|--------|---------|------|
| TC_AD_TLIST_067 | Single dialog hiện **đúng tên tour** | — | ✅ |
| TC_AD_TLIST_068 | Bulk dialog hiện **count** tours | — | ✅ |
| TC_AD_TLIST_069 | Nút confirm **disabled** khi `isDeleting` | Slow DELETE | ✅ |
| TC_AD_TLIST_070 | Single delete API lỗi → toast, tour còn trong list | Mock 500 | ✅ |

---

## 14. Row actions (P1)

| ID | Mô tả | Dữ liệu | Auto |
|----|--------|---------|------|
| TC_AD_TLIST_012 | Nút **Sửa** → `/admin/tours/edit/:id` | Tour id=1 | ✅ |
| TC_AD_TLIST_071 | Nút **View** mở modal (smoke — panel visible) | Chi tiết → `03d` | ✅ |

---

## 15. i18n (P2)

| ID | Mô tả | Dữ liệu | Auto |
|----|--------|---------|------|
| TC_AD_TLIST_072 | Locale **EN** — heading "Tour List", filter labels EN | Switch language | ✅ |

---

## 16. API smoke (P1–P2)

| ID | Mô tả | Auto |
|----|--------|------|
| API_TLIST_001 | GET list không auth → 401 | ✅ |
| API_TLIST_002 | GET list admin → 200, `data` là array | ✅ |
| API_TLIST_003 | `?search=` lọc đúng | ✅ |
| API_TLIST_004 | `?tour_category_id=` | ✅ |
| API_TLIST_005 | `?status=active\|inactive` | ✅ |
| API_TLIST_006 | `?booking_availability=open\|sold_out` | ✅ |
| API_TLIST_007 | `?is_featured=1` / `?is_hot=1` / normal combo | ✅ |
| API_TLIST_008 | `?page=&per_page=` — metadata pagination | ✅ |
| API_TLIST_009 | `?sort_by=&sort_order=` | ✅ |
| API_TLIST_010 | PATCH `/status` không auth → 401 | ✅ |
| API_TLIST_011 | PATCH `/featured`, `/hot` không auth → 401 | ✅ |
| API_TLIST_012 | DELETE không auth → 401 | ✅ |
| API_TLIST_013 | GET `/export` không auth → 401 | ✅ |
| API_TLIST_014 | GET `/tour-categories` — dependency filter | ✅ |
| API_TLIST_015 | PATCH status tour không tồn tại → 404 | ✅ |
| API_TLIST_016 | DELETE tour không tồn tại → 404 | ✅ |
| API_TLIST_017 | Token non-admin → 403 (nếu API enforce) | ⏭️ skip |
| API_TLIST_018 | Export với filter → 200 + content-type xlsx | ✅ |

---

## 17. Ghi chú doc vs code

| Mô tả cũ / giả định | Code thực tế |
|---------------------|--------------|
| Staff truy cập được | Chỉ **admin** |
| Sort cột bảng | **Không có** UI sort |
| Cột Đánh giá | **Không có** |
| Click badge đổi status | Badge **read-only**; bulk toolbar |
| Status "Hết chỗ" trong filter status | Tách: `status` vs `booking_availability` |
| View → route `/admin/tours/:id` | View → **TourDetailModal** |
| Empty state có nút Thêm tour | **Không có** nút trong empty |
| Stats "Hết chỗ" | `booking_availability=sold_out`, không phải `status` |
| Nút **Lọc** | **Decorative** — filter apply ngay khi đổi select |
| Active tags | **Không** tag search / booking_availability |
| **TLIST_005** | Bulk deactivate thay per-row toggle |

---

## 18. Liên kết

| Tài liệu | Nội dung |
|----------|----------|
| `03d_tour_detail_modal.md` | 25 TC modal View (schedules, gallery, itinerary…) |
| `03b_tour_create.md` | Tạo tour |
| `03c_tour_edit.md` | Sửa tour (nếu có) |

**Chạy automation:**
```bash
npm run test:admin:tour-list          # 65 UI + 17 API (1 skip)
npm run test:admin:tour-detail-modal  # 25 modal (03d)
```
