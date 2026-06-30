# Admin — Trang lỗi hệ thống (Error & 404)

**Routes:**
- `*` (không khớp route) → **PageNotFound** (`danangtrip-admin/src/pages/PageNotFound/`)
- Lỗi render route (error boundary) → **ErrorPage** (`danangtrip-admin/src/pages/ErrorPage/`)

**Source router:** `danangtrip-admin/src/routes/index.tsx` — `errorElement: ErrorPage` trên Public/Private routes; `path: '*'` → PageNotFound

---

## 1. Phạm vi

| Hạng mục | Chi tiết |
|----------|----------|
| PageNotFound | URL không tồn tại trong admin app; animation Lottie 404 |
| ErrorPage | Lỗi runtime khi load/render component con (React Router error boundary) |
| UI | Full-screen centered Lottie animation; **không** có nút quay lại/text trong code hiện tại |

## 2. Điều kiện tiên quyết

- Dev server `:5173`
- Admin đã đăng nhập (cho test 404 trong private layout)
- Có thể trigger ErrorPage bằng route/component throw error (test manual hoặc mock)

## 3. Test cases — PageNotFound 404 (P1)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_ERR_001 | Guest mở `/admin/unknown-path` → hiển thị PageNotFound | ⏳ |
| TC_AD_ERR_002 | Admin đã login mở `/dashboard/xyz` → PageNotFound (không crash app) | ⏳ |
| TC_AD_ERR_003 | Animation Lottie 404 render (loop, autoplay) | ⏳ |
| TC_AD_ERR_004 | Layout full viewport, centered | ⏳ |
| TC_AD_ERR_005 | Browser back sau 404 → quay trang trước | ⏳ |
| TC_AD_ERR_006 | Gõ URL hợp lệ sau 404 (vd `/dashboard`) → load bình thường | ⏳ |

## 4. Test cases — ErrorPage boundary (P1)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_ERR_010 | Route con throw error → ErrorPage thay vì white screen | ⏳ |
| TC_AD_ERR_011 | Animation Lottie error render full screen | ⏳ |
| TC_AD_ERR_012 | Error trong PrivateRoute/MainLayout → vẫn hiện ErrorPage | ⏳ |
| TC_AD_ERR_013 | Error trong PublicRoute (login) → ErrorPage | ⏳ |
| TC_AD_ERR_014 | Reload trang sau error → behavior theo route (có thể vẫn lỗi hoặc recover) | ⏳ |

## 5. Edge & UX (P2)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_ERR_020 | 404 với query string dài → vẫn render 404 | ⏳ |
| TC_AD_ERR_021 | 404 encoded path (`%20`, unicode) → không crash | ⏳ |
| TC_AD_ERR_022 | Mobile viewport 375px — animation scale hợp lý | ⏳ |
| TC_AD_ERR_023 | Không leak stack trace ra UI (chỉ animation) | ⏳ |

## 6. Ghi chú kỹ thuật

- Cả hai trang **chỉ** render Lottie JSON — không có CTA "Về trang chủ" trong source hiện tại.
- `PageNotFound` dùng asset `Bot Error 404.json`.
- `ErrorPage` dùng asset `Page Error Animation.json`.
- Nếu product bổ sung nút navigate, cần cập nhật testcase tương ứng.

## 7. Checklist regression

- Unknown URL → 404 animation, không unmount toàn app
- Runtime error → error boundary animation
- Auth session không bị xóa khi gặp 404 trong private area

**Trạng thái automation:** 0 TC ✅ · ~14 TC ⏳ backlog
