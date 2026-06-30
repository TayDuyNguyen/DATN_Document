# Admin — Cấu hình Website (Website Settings)

**Route:** `/admin/settings`  
**Source:** `danangtrip-admin/src/pages/Settings/`  
**Automation:** `tests/admin/settings.spec.ts` · `tests/admin/settings-auth.spec.ts`  
**POM:** `SettingsPage.ts` · Mock: `settings.mock.ts` · Data: `settings.data.ts`  
**Chạy test:** `npm run test:admin:settings`

---

## 1. Phạm vi

| Hạng mục | Chi tiết |
|----------|----------|
| Vai trò | Admin đã đăng nhập (`PrivateRoute` — guest/non-admin → `/login`) |
| API | `GET /admin/settings` · `PUT /admin/settings` (body: `{ settings: WebsiteSettings }`) |
| UI | 6 tab sidebar: General · Brand · Social · Payment · Policy · SEO |
| Form | React Hook Form + Yup · SaveBar khi `isDirty` (Discard / Lưu thay đổi) |
| Không thuộc màn này | Đổi profile admin · Đổi mật khẩu (xem Dashboard control panel / Users) |

### Cổng thanh toán thực tế (khác doc gốc)

| Gateway | Trạng thái UI | Ghi chú |
|---------|---------------|---------|
| SePay VietQR | Active | Khuyên dùng — thay PayOS trong doc cũ |
| COD | Active | Chuyển khoản / tiền mặt |
| VNPay | Dự phòng (`reserved`) | Toggle có nhưng badge "Dự phòng" |
| MoMo | Dự phòng | |
| ZaloPay | Dự phòng | |

Validation: **ít nhất 1** trong 5 gateway phải bật.

---

## 2. UI Interactive Inventory

| # | Tab | Nhãn (i18n) | Loại | Hành vi kỳ vọng | TC | Auto |
|---|-----|-------------|------|-----------------|-----|------|
| 1 | — | Cấu hình Website | heading | Breadcrumb + title | SET_005 | ✅ TC_AD_SET_005 |
| 2 | Sidebar | Thông tin chung … SEO | button ×6 | Chuyển tab, dot đỏ khi lỗi section | SET_006 | ✅ TC_AD_SET_006 |
| 3 | General | Hotline / Email / Địa chỉ / Giờ hỗ trợ | text | Required + validate VN phone/email | SET_001, 008, 015 | ✅ |
| 4 | Brand | Tên Website / Logo / Favicon | text + upload | Required logo/favicon URL | SET_012, 019 | ✅ TC_AD_SET_012, 019 |
| 5 | Social | Facebook … Zalo OA | url optional | URL format | SET_016 | ✅ TC_AD_SET_016 |
| 6 | Payment | SePay / COD / VNPay / MoMo / ZaloPay | toggle | Min 1 gateway · reserved disabled | SET_002, 009, 018 | ✅ |
| 7 | Policy | Terms / Privacy / Data protection | url optional | | — | manual |
| 8 | SEO | Meta title / description / OG image | text + upload | Min/max length | SET_017 | ✅ TC_AD_SET_017 |
| 9 | SaveBar | Hủy bỏ / Lưu thay đổi | button | Chỉ khi dirty | SET_007 | ✅ TC_AD_SET_007 |
| 10 | System | Loading spinner | state | GET delay | SET_013 | ✅ TC_AD_SET_013 |
| 11 | System | Load error + Retry | state | GET 500 | SET_010 | ✅ TC_AD_SET_010 |
| 12 | System | Save error toast | toast | PUT 500 | SET_011 | ✅ TC_AD_SET_011 |
| 13 | — | Tab error dot khi validation | indicator | Lỗi section | SET_014 | ✅ TC_AD_SET_014 |
| 14 | General | Hotline invalid | validation | SET_015 | ✅ TC_AD_SET_015 |
| 15 | Social | URL invalid | validation | SET_016 | ✅ TC_AD_SET_016 |
| 16 | SEO | Meta title quá ngắn | validation | SET_017 | ✅ TC_AD_SET_017 |
| 17 | Payment | Reserved gateway disabled | toggle | SET_018 | ✅ TC_AD_SET_018 |
| 18 | Brand | Upload logo | upload | SET_019 | ✅ TC_AD_SET_019 |
| 19 | — | Chatbot hint → AI Assistant | link | IMP_SET_006 | ✅ UI |

---

## 3. Mapping testcase doc gốc → automation

| ID gốc | ID Auto | Mô tả | Auto | Ghi chú |
|--------|---------|--------|------|---------|
| TC_AD_SET_001 | TC_AD_SET_001 | Đổi hotline + email, Lưu | ✅ | Sync Web client → **manual/E2E cross-app** |
| TC_AD_SET_002 | TC_AD_SET_002 | Tắt cổng thanh toán | ✅ | Doc VNPay/PayOS → code **SePay/COD** |
| TC_AD_SET_003 | — | Đổi tên Admin profile | **manual-only** | Không có trên `/admin/settings` |
| TC_AD_SET_004 | — | Đổi mật khẩu admin | **manual-only** | Không có trên `/admin/settings` |
| — | TC_AD_SET_005 | Render tabs + data General | ✅ | Bổ sung |
| — | TC_AD_SET_006 | Điều hướng 6 tab | ✅ | Bổ sung |
| — | TC_AD_SET_007 | SaveBar dirty / discard | ✅ | Bổ sung |
| — | TC_AD_SET_008 | Validate email | ✅ | Bổ sung |
| — | TC_AD_SET_009 | Min 1 payment gateway | ✅ | Bổ sung |
| — | TC_AD_SET_010 | API load lỗi | ✅ | Bổ sung |
| — | TC_AD_SET_011 | API save lỗi | ✅ | Bổ sung |
| — | TC_AD_SET_012 | Lưu tên website Brand | ✅ | Bổ sung |
| — | TC_AD_SET_013 | Loading state | ✅ | Bổ sung |
| — | TC_AD_SET_014 | Tab error dot validation | ✅ | Bổ sung |
| — | TC_AD_SET_015 | Validate hotline | ✅ | Bổ sung |
| — | TC_AD_SET_016 | Validate social URL | ✅ | Bổ sung |
| — | TC_AD_SET_017 | Validate SEO meta title | ✅ | Bổ sung |
| — | TC_AD_SET_018 | Reserved gateway disabled | ✅ | Bổ sung |
| — | TC_AD_SET_019 | Upload brand logo | ✅ | Bổ sung |
| — | TC_AD_SET_040 | Guest → login | ✅ | Auth |
| — | TC_AD_SET_041 | Non-admin → login | ✅ | Auth |
| — | TC_AD_SET_042 | Admin truy cập | ✅ | Auth |
| SET_RSP_014 | — | Responsive mobile 375px | **manual-only** | |

---

## 4. Test cases chi tiết (spec gốc + bổ sung)

| ID | Nhóm | Test case | Tiền điều kiện | Bước | Dữ liệu | Kết quả mong đợi | Ưu tiên |
|----|------|-----------|----------------|------|---------|------------------|---------|
| TC_AD_SET_001 | General | Đổi hotline + email hỗ trợ | Admin login | 1. Sửa Hotline, Email<br>2. Lưu thay đổi | `1900 8888`, `support@danangtrip.vn` | Toast success · PUT body đúng · SaveBar ẩn | High |
| TC_AD_SET_002 | Payment | Tắt SePay (COD vẫn bật) | Tab Payment | 1. Tắt SePay<br>2. Lưu | sepay=false | Lưu OK · Web client ẩn SePay ở checkout (**manual**) | High |
| TC_AD_SET_003 | Profile | Đổi tên Admin | — | — | — | **Out of scope** — dùng Dashboard drawer | — |
| TC_AD_SET_004 | Security | Đổi mật khẩu | — | — | — | **Out of scope** — không có UI | — |
| TC_AD_SET_005 | UI | Load trang settings | Admin login | Mở `/admin/settings` | Mock GET | 6 tab + General prefilled | High |
| TC_AD_SET_006 | Navigation | Chuyển 6 tab | Trang loaded | Click từng tab | | Section title tương ứng hiển thị | Medium |
| TC_AD_SET_007 | SaveBar | Discard khôi phục | Dirty form | Sửa field → Hủy bỏ | | Giá trị cũ · SaveBar ẩn | High |
| TC_AD_SET_008 | Validation | Email không hợp lệ | General tab | Nhập email sai → Lưu | `not-an-email` | Lỗi inline · không PUT | High |
| TC_AD_SET_009 | Validation | Tắt hết cổng TT | Payment tab | Tắt SePay + COD → Lưu | | Banner `payment_required` | High |
| TC_AD_SET_010 | API | GET settings lỗi | API 500 | Vào trang | | Full-page error | High |
| TC_AD_SET_011 | API | PUT settings lỗi | API 500 | Sửa + Lưu | | Toast `save_failed` | High |
| TC_AD_SET_012 | Brand | Đổi tên website | Brand tab | Sửa Tên Website → Lưu | `DaNangTrip V2` | PUT brand.website_name | Medium |
| TC_AD_SET_013 | Loading | Spinner khi fetch | GET delay 1.5s | Vào trang | | Loading rồi render form | Medium |
| TC_AD_SET_014 | Validation | Tab error dot | Email invalid | Sửa + Lưu + chuyển tab | | Dot đỏ tab General | Medium |
| TC_AD_SET_015 | Validation | Hotline invalid | General tab | Nhập `12345` → Lưu | | Lỗi inline · không PUT | High |
| TC_AD_SET_016 | Validation | Social URL invalid | Social tab | URL sai → Lưu | | Lỗi inline + dot tab Social | Medium |
| TC_AD_SET_017 | Validation | SEO meta title ngắn | SEO tab | Title `short` → Lưu | | Lỗi min length + dot tab SEO | Medium |
| TC_AD_SET_018 | Payment | Reserved gateway disabled | Payment tab | Click VNPay/MoMo/ZaloPay | | Toggle disabled | Medium |
| TC_AD_SET_019 | Brand | Upload logo | Brand tab | Chọn file ảnh | | Preview + SaveBar dirty | Medium |
| TC_AD_SET_040 | Auth | Guest | Chưa login | Mở URL | | Redirect `/login` | Critical |
| TC_AD_SET_041 | Auth | Non-admin | User role | Mở URL | | Redirect `/login` | Critical |
| TC_AD_SET_042 | Auth | Admin | Admin session | Mở URL | | Heading visible | Critical |

---

## 5. Test data mock

| Record | Mục đích |
|--------|----------|
| `mockRawSettings` | GET mặc định — đủ 7 nhóm (kể cả `chatbot` ẩn UI) |
| `updatedGeneralContact` | TC_AD_SET_001 |
| `updatedBrandName` | TC_AD_SET_012 |

---

## 6. Improvement backlog

| ID | Loại | Ưu tiên | Phát hiện | Trạng thái |
|----|------|---------|-----------|------------|
| IMP_SET_001 | Doc | P2 | Doc gốc mô tả profile/password — lệch product | **fixed** (mapping) |
| IMP_SET_002 | Doc | P2 | Doc ghi PayOS — code dùng SePay | **fixed** (mapping) |
| IMP_SET_003 | Test | P3 | Cross-app sync Header/Footer Web client | open (manual) |
| IMP_SET_004 | UX | P3 | Load error message hardcode tiếng Anh | **fixed** |
| IMP_SET_005 | A11y | P3 | Payment toggle thiếu aria-label | **fixed** |
| IMP_SET_006 | Feature | P3 | `chatbot` trong schema nhưng không có tab UI | **fixed** (hint link) |

---

## 7. Ghi chú

- Upload ảnh (logo/favicon/og) gọi API riêng `POST/DELETE /admin/settings/images/{key}` — chưa auto (cần mock multipart).
- Staff có thể truy cập settings (không giới hạn như Reports) — không có TC riêng trừ khi product đổi policy.
