# Admin — Quản lý Giao dịch & Thanh toán (Payments)

**Route:** `/admin/payments` · `/admin/payments/detail/:id`  
**Source:** `danangtrip-admin/src/pages/Payments/`  
**Automation:** `tests/admin/payment-list.spec.ts` · `tests/admin/payment-list-auth.spec.ts` · `tests/admin/payment-detail.spec.ts`  
**POM:** `PaymentListPage.ts` · `PaymentDetailPage.ts` · Mock: `tests/fixtures/api/payments.mock.ts` · Data: `payments.data.ts`  
**Chạy test:** `npm run test:admin:payment-list` · `npm run test:admin:payment-detail`

---

## 1. Phạm vi

| Hạng mục | Chi tiết |
|----------|----------|
| Vai trò | **Admin** + **Staff** vào shell; **refund** chỉ Admin |
| API | `GET /admin/payments` · `GET /admin/payments/:id` · `POST .../:id/refund` · `GET /admin/payments/export` |
| Gateway thực tế | `sepay`, `vnpay`, `momo`, `zalopay`, `bank_transfer` (doc cũ ghi PayOS → map SePay) |
| UI List | Stats 4 card · Filter bar · Table + pagination · Refund dialog (list row) · Export Excel |
| UI Detail | Payment info · Booking & customer · Timeline · Refund dialog · Back to list |

## 2. UI Interactive Inventory — List

| # | Vùng UI | Nhãn (i18n) | Loại | Hành vi kỳ vọng | TC | Auto |
|---|---------|-------------|------|-----------------|-----|------|
| 1 | Header | Xuất báo cáo Excel | button | GET export blob + toast | TC_AD_PAY_021–022 | ✅ |
| 2 | Filter | Tìm kiếm mã giao dịch… | search | Debounce → `search` | TC_AD_PAY_002, 013 | ✅ |
| 3 | Filter | Tất cả Trạng thái | select | `payment_status` | TC_AD_PAY_004 | ✅ |
| 4 | Filter | Tất cả Cổng thanh toán | select | `payment_gateway` | TC_AD_PAY_003 | ✅ |
| 5 | Filter | Tất cả yêu cầu hoàn | select | `refund_status` | TC_AD_PAY_009 | ✅ |
| 6 | Filter | Làm mới / Reset | button | Clear filters (chỉ hiện khi có filter) | TC_AD_PAY_011 | ✅ |
| 7 | Table | Chi tiết | link | → `/admin/payments/detail/:id` | TC_AD_PAY_005 | ✅ |
| 8 | Table | Mã booking | link | → `/admin/bookings/detail/:bookingId` | TC_AD_PAY_025 | ✅ |
| 9 | Table | Hoàn tiền | button | Mở refund dialog (admin only) | TC_AD_PAY_023–024 | ✅ |
| 10 | Table | Làm mới (icon) | button | `refetch` | — | manual-only |
| 11 | Pagination | Số trang / next | button | API `page` | TC_AD_PAY_017 | ✅ |

## 3. UI Interactive Inventory — Detail

| # | Vùng UI | Nhãn (i18n) | Loại | Hành vi | TC | Auto |
|---|---------|-------------|------|---------|-----|------|
| 1 | Header | Hoàn tiền | button | Mở dialog (admin) | TC_AD_PAYDETAIL_007 | ✅ |
| 2 | Header | Hoàn tiền disabled | button | Staff + tooltip | TC_AD_PAYDETAIL_008 | ✅ |
| 3 | Booking block | Mã đơn | link | → booking detail | TC_AD_PAYDETAIL_004 | ✅ |
| 4 | Not found | Quay lại danh sách | button | → list | TC_AD_PAYDETAIL_011 | ✅ |
| 5 | Refund dialog | Xác nhận hoàn tiền | button | POST refund | TC_AD_PAYDETAIL_007 | ✅ |

## 4. Data Display Integrity

| # | Vùng UI | Field API | Field UI | TC | Auto |
|---|---------|-----------|----------|-----|------|
| 1 | Row | `transaction_code`, customer, `booking_code`, gateway, status | table cells | TC_AD_PAY_006 | ✅ |
| 2 | Row orphan | `booking=null` | cột booking `—` | TC_AD_PAY_007 | ✅ |
| 3 | Row partial | `reconciliation_status=partial` | badge partial + short amount | TC_AD_PAY_008 | ✅ |
| 4 | Stats | rows trang hiện tại | 4 stat cards (client-side) | TC_AD_PAY_026 | ✅ |
| 5 | Detail | transaction, customer, tour, timeline | sections + timeline labels | TC_AD_PAYDETAIL_001 | ✅ |
| 6 | Detail orphan | no booking | warning, không có block booking | TC_AD_PAYDETAIL_005 | ✅ |
| 7 | List empty | `data=[]` | `table.empty_title` | TC_AD_PAY_014 | ✅ |

## 5. Test cases — Auth (P0)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_PAY_040 | Guest → `/login` | ✅ |
| TC_AD_PAY_041 | User `role=user` → `/login` | ✅ |
| TC_AD_PAY_042 | Admin truy cập list | ✅ |

## 6. Test cases — List (P1)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_PAY_001 | Heading, stats, filter, cột bảng | ✅ |
| TC_AD_PAY_002 | Search theo mã giao dịch | ✅ |
| TC_AD_PAY_003 | Lọc gateway SePay (doc PayOS) | ✅ |
| TC_AD_PAY_004 | Lọc status success | ✅ |
| TC_AD_PAY_005 | Chi tiết → detail route | ✅ |
| TC_AD_PAY_006 | Data display row đầy đủ | ✅ |
| TC_AD_PAY_007 | Orphan booking dash | ✅ |
| TC_AD_PAY_008 | Partial paid + short amount | ✅ |
| TC_AD_PAY_009 | Lọc refund pending | ✅ |
| TC_AD_PAY_011 | Reset filter (UI row count) | ✅ |
| TC_AD_PAY_013 | Search theo mã booking | ✅ |
| TC_AD_PAY_014 | Empty state | ✅ |
| TC_AD_PAY_015 | Loading delay API | ✅ |
| TC_AD_PAY_017 | Pagination trang 2 | ✅ |
| TC_AD_PAY_021 | Export Excel thành công | ✅ |
| TC_AD_PAY_022 | Export lỗi → toast | ✅ |
| TC_AD_PAY_023 | Admin mở refund dialog từ list | ✅ |
| TC_AD_PAY_024 | Staff refund disabled | ✅ |
| TC_AD_PAY_025 | Link booking → booking detail | ✅ |
| TC_AD_PAY_026 | Stats đếm theo trang hiện tại | ✅ |

## 7. Test cases — Detail (P1)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_PAYDETAIL_001 | Payment + booking + timeline success | ✅ |
| TC_AD_PAYDETAIL_002 | Loading delay | ✅ |
| TC_AD_PAYDETAIL_003 | Not found + back button | ✅ |
| TC_AD_PAYDETAIL_004 | Link booking code | ✅ |
| TC_AD_PAYDETAIL_005 | Orphan warning | ✅ |
| TC_AD_PAYDETAIL_006 | Timeline failed | ✅ |
| TC_AD_PAYDETAIL_006b | Timeline refunded + reason | ✅ |
| TC_AD_PAYDETAIL_007 | Admin refund thành công | ✅ |
| TC_AD_PAYDETAIL_008 | Staff refund disabled | ✅ |
| TC_AD_PAYDETAIL_011 | Back to list | ✅ |

## 8. Đề xuất cải thiện product (Improvement Backlog)

| ID | Loại | Ưu tiên | Phát hiện | Đề xuất | File | Trạng thái |
|----|------|---------|-----------|---------|------|------------|
| IMP_PAY_001 | Doc | P2 | Doc testcase ghi PayOS | Cập nhật doc → SePay | `13a_payment_list.md` | **fixed** |
| IMP_PAY_002 | UX | P2 | Stats chỉ tính rows trang hiện tại, không phải tổng API | Nhãn `*_on_page` hoặc gọi API stats riêng | `PaymentList/index.tsx` | **fixed** |
| IMP_PAY_003 | i18n | P2 | Refund filter labels hardcode VI | `t('payment:filter.*')` | `PaymentFilterBar.tsx` | **fixed** |
| IMP_PAY_004 | UX | P2 | `FilterBar` nhận `onExport` nhưng không render nút export trong filter | Gỡ prop hoặc thêm nút | `PaymentFilterBar.tsx` | **fixed** |
| IMP_PAY_005 | Function | P2 | `partially_paid` không có trong dropdown status | Thêm option filter | `PaymentFilterBar.tsx` | **fixed** |
| IMP_PAY_006 | i18n | P2 | Validation refund dialog hardcode VI | Dùng i18n keys | `RefundPaymentDialog.tsx` | **fixed** |
| IMP_PAY_007 | Test | P1 | Mock pathname `isPaymentsListPath` so sánh `/admin/payments` thay vì `/api/v1/admin/payments` | Regex pathname + route `**/api/v1/admin/payments**` | `payments.mock.ts` | **fixed** |

**POM:** `PaymentListPage.ts` — scope `main main tbody`, reset trong `filterPanel`, toast sonner. `PaymentDetailPage.ts` — heading `PAY-*`, refund dialog `getByRole('heading')`.

**Automation (2026-06-23):** `npm run test:admin:payment-list` + `test:admin:payment-detail` — **33/33 passed** (`workers=1`).
