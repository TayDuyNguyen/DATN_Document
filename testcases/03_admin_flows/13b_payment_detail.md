# Admin — Chi tiết Giao dịch (Payment Detail)

**Route:** `/admin/payments/detail/:id`  
**Source:** `danangtrip-admin/src/pages/Payments/PaymentDetail/index.tsx`  
**Automation:** `tests/admin/payment-detail.spec.ts` · `tests/admin/payment-detail-auth.spec.ts`  
**POM:** `PaymentDetailPage.ts` · Mock: `payments.mock.ts` · Data: `payments.data.ts`  
**Chạy test:** `npm run test:admin:payment-detail` — **37/37 passed** (2026-06-23)

---

## 1. Phạm vi

| Hạng mục | Chi tiết |
|----------|----------|
| Vai trò | Admin + Staff vào shell; **refund** chỉ Admin (`user.role === 'admin'`) |
| API | `GET /admin/payments/:id` · `POST /admin/payments/:id/refund` |
| UI | Breadcrumb · Header (mã GD + badge) · Payment info card · Booking/customer card · Orphan warning · Timeline · Refund dialog |
| Gateway thực tế | `sepay`, `vnpay`, `momo`, `zalopay`, `bank_transfer` (doc cũ ghi PayOS → SePay) |
| Status UI | `pending`, `success`, `failed`, `refunded`, `partially_paid` |

---

## 2. UI Interactive Inventory (PHASE 0.6)

| # | Vùng UI | Nhãn (i18n) | Loại | Hành vi kỳ vọng | TC Auto | Auto |
|---|---------|-------------|------|-----------------|---------|------|
| 1 | Breadcrumb | Payments / Thanh toán | link | → `/admin/payments` | TC_AD_PAYDETAIL_012 | ⏳ gap |
| 2 | Breadcrumb | Detail / Chi tiết | text | Không click | — | manual-only |
| 3 | Header action | Hoàn tiền / Refund | button | Mở dialog (chỉ `status=success`) | TC_AD_PAYDETAIL_009, 007 | ✅ partial |
| 4 | Header | Mã giao dịch (h1) | text | Hiển thị `transactionCode` | TC_AD_PAYDETAIL_001 | ✅ |
| 5 | Header | Status badge | badge | Màu/nhãn theo status | TC_AD_PAYDETAIL_034 | ⏳ gap |
| 6 | Header | Staff hint | text | Tooltip chỉ admin (success + staff) | TC_AD_PAYDETAIL_008 | ✅ |
| 7 | Payment card | Thông tin Thanh toán | section | Labels + values | TC_AD_PAYDETAIL_001 | ✅ partial |
| 8 | Payment card | Số tiền | text | `formatCurrency(amount)` | TC_AD_PAYDETAIL_013 | ⏳ gap |
| 9 | Payment card | Cổng thanh toán | badge | `PaymentGatewayBadge` | TC_AD_PAYDETAIL_014 | ⏳ gap |
| 10 | Payment card | Thời gian khởi tạo | text | `formatAdminShortDate` | TC_AD_PAYDETAIL_015 | ⏳ gap |
| 11 | Payment card | Thời gian thanh toán | text | Chỉ khi `paidAt` có giá trị | TC_AD_PAYDETAIL_016 | ⏳ gap |
| 12 | Payment card | refundedAt / reason | text | Chỉ khi `status=refunded` | TC_AD_PAYDETAIL_006b | ✅ partial |
| 13 | Booking card | Đơn đặt & Khách hàng | section | Render khi `bookingId` | TC_AD_PAYDETAIL_001 | ✅ |
| 14 | Booking card | Mã đơn đặt | link | → `/admin/bookings/detail/:id` | TC_AD_PAYDETAIL_004 | ✅ |
| 15 | Booking card | Avatar khách | img / User icon | URL hoặc fallback | TC_AD_PAYDETAIL_017 | ⏳ gap |
| 16 | Booking card | Tour thumbnail | img | Optional | TC_AD_PAYDETAIL_018 | ⏳ gap |
| 17 | Orphan | Warning không đính kèm đơn | alert | Không render booking block | TC_AD_PAYDETAIL_005 | ✅ |
| 18 | Timeline | Lịch sử Trạng thái | section | VirtualTimeline milestones | TC_AD_PAYDETAIL_001, 006, 006b | ✅ |
| 19 | Not found | Quay lại danh sách | button | → `/admin/payments` | TC_AD_PAYDETAIL_011 | ✅ |
| 20 | Refund dialog | X đóng | button | Đóng dialog, không POST | TC_AD_PAYDETAIL_019 | ⏳ gap |
| 21 | Refund dialog | Hủy bỏ / Cancel | button | Đóng dialog | TC_AD_PAYDETAIL_019 | ⏳ gap |
| 22 | Refund dialog | Backdrop click | overlay | `onClose` | TC_AD_PAYDETAIL_020 | ⏳ gap |
| 23 | Refund dialog | Lý do hoàn tiền | textarea | Required min 10 chars | TC_AD_PAYDETAIL_010 | ⏳ gap |
| 24 | Refund dialog | Bank fields | input | Hiện khi thiếu `latestRefundRequest` bank info | TC_AD_PAYDETAIL_021 | ⏳ gap |
| 25 | Refund dialog | VietQR block | img | Khi có bank prefilled từ refund request | TC_AD_PAYDETAIL_022 | ⏳ gap |
| 26 | Refund dialog | Xác nhận hoàn tiền | button submit | POST refund | TC_AD_PAYDETAIL_007 | ✅ |
| 27 | Loading | Spinner + Đang tải | state | Khi `isLoading` | TC_AD_PAYDETAIL_002 | ✅ |
| 28 | Error | Không tìm thấy giao dịch | state | 404 / empty | TC_AD_PAYDETAIL_003 | ✅ |

---

## 3. Data Display Integrity (PHASE 0.7)

| # | Vùng UI | Field API | Field UI | TC | Auto |
|---|---------|-----------|----------|-----|------|
| 1 | Header | `transaction_code` | h1 text | ADMIN_007 / PAYDETAIL_013 | ⏳ |
| 2 | Payment card | `amount` | format VND | ADMIN_008–009 / PAYDETAIL_013 | ⏳ |
| 3 | Payment card | `payment_method` | gateway badge | ADMIN_010 / PAYDETAIL_014 | ⏳ |
| 4 | Payment card | `created_at` | label created_at | ADMIN_011 / PAYDETAIL_015 | ⏳ |
| 5 | Payment card | `paid_at` | label paid_at (conditional) | ADMIN_012–013 / PAYDETAIL_016 | ⏳ |
| 6 | Payment card | `refunded_at`, `refund_reason` | refunded fields | ADMIN_014–015 / PAYDETAIL_006b | ✅ partial |
| 7 | Booking | `customer_name`, `customer_email` | customer block | ADMIN_016 / PAYDETAIL_001 | ✅ |
| 8 | Booking | `booking_code`, `tour_name` | link + tour | ADMIN_016–017 / PAYDETAIL_001, 004 | ✅ |
| 9 | Orphan | `booking=null` | warning, no section | ADMIN_020 / PAYDETAIL_005 | ✅ |
| 10 | Timeline | status + gateway + dates | milestone labels | ADMIN_021–024 / PAYDETAIL_001, 006, 006b | ✅ |
| 11 | Partial | `reconciliation_status=partial` | badge `partially_paid` | PAYDETAIL_023 | ⏳ gap |
| 12 | Pending | `payment_status=pending` | badge + timeline created only | PAYDETAIL_024 | ⏳ gap |

---

## 4. Test cases — Auth (P0)

| ID gốc | ID Auto | Mô tả | Auto |
|--------|---------|--------|------|
| ADMIN_PAYMENT_DETAIL_001 | TC_AD_PAYDETAIL_040 | Guest → `/login` (detail URL) | ⏳ *(có thể tái dùng pattern list auth)* |
| ADMIN_PAYMENT_DETAIL_002 | TC_AD_PAYDETAIL_041 | User `role=user` → `/login` | ⏳ |
| — | TC_AD_PAYDETAIL_042 | Admin mở detail hợp lệ | ✅ *(qua PAYDETAIL_001)* |

---

## 5. Test cases — Load & Error (P0–P1)

| ID gốc | ID Auto | Mô tả | Auto |
|--------|---------|--------|------|
| ADMIN_PAYMENT_DETAIL_003 | TC_AD_PAYDETAIL_001 | Render đầy đủ sections + data | ✅ |
| ADMIN_PAYMENT_DETAIL_004 | TC_AD_PAYDETAIL_002 | Loading delay API | ✅ |
| ADMIN_PAYMENT_DETAIL_005 | TC_AD_PAYDETAIL_003 | Not found 404 | ✅ |
| ADMIN_PAYMENT_DETAIL_006 | TC_AD_PAYDETAIL_011 | Back to list | ✅ |
| ADMIN_PAYMENT_DETAIL_035 | TC_AD_PAYDETAIL_030 | Detail API 500 → not found UI | ⏳ |

---

## 6. Test cases — Payment fields (P1)

| ID gốc | ID Auto | Mô tả | Auto |
|--------|---------|--------|------|
| ADMIN_PAYMENT_DETAIL_007 | TC_AD_PAYDETAIL_013 | Mã GD header + card khớp | ⏳ |
| ADMIN_PAYMENT_DETAIL_008 | TC_AD_PAYDETAIL_013 | Format amount VND | ⏳ |
| ADMIN_PAYMENT_DETAIL_009 | TC_AD_PAYDETAIL_013b | Amount = 0 không NaN | ⏳ |
| ADMIN_PAYMENT_DETAIL_010 | TC_AD_PAYDETAIL_014 | Gateway badge SePay/VNPay/MoMo | ⏳ |
| ADMIN_PAYMENT_DETAIL_011 | TC_AD_PAYDETAIL_015 | Created date format locale | ⏳ |
| ADMIN_PAYMENT_DETAIL_012 | TC_AD_PAYDETAIL_016 | paidAt hiển thị khi success | ⏳ |
| ADMIN_PAYMENT_DETAIL_013 | TC_AD_PAYDETAIL_016b | Success nhưng paidAt null — không crash | ⏳ |
| ADMIN_PAYMENT_DETAIL_014 | TC_AD_PAYDETAIL_006b | refundedAt + reason | ✅ partial |
| ADMIN_PAYMENT_DETAIL_015 | TC_AD_PAYDETAIL_006c | Refunded thiếu reason — timeline fallback | ⏳ |
| ADMIN_PAYMENT_DETAIL_034 | TC_AD_PAYDETAIL_034 | Badge đủ 5 status | ⏳ |
| ADMIN_PAYMENT_DETAIL_036 | TC_AD_PAYDETAIL_035 | Mã GD dài không vỡ layout | ⏳ manual/CSS |
| ADMIN_PAYMENT_DETAIL_037 | TC_AD_PAYDETAIL_036 | Refund reason dài wrap | ⏳ manual |

---

## 7. Test cases — Booking & Orphan (P1)

| ID gốc | ID Auto | Mô tả | Auto |
|--------|---------|--------|------|
| ADMIN_PAYMENT_DETAIL_016 | TC_AD_PAYDETAIL_001 | Customer + tour block | ✅ |
| ADMIN_PAYMENT_DETAIL_017 | TC_AD_PAYDETAIL_004 | Click booking code → booking detail | ✅ |
| ADMIN_PAYMENT_DETAIL_018 | TC_AD_PAYDETAIL_017 | Avatar URL / User fallback | ⏳ |
| ADMIN_PAYMENT_DETAIL_019 | TC_AD_PAYDETAIL_018 | Tour thumbnail optional | ⏳ |
| ADMIN_PAYMENT_DETAIL_020 | TC_AD_PAYDETAIL_005 | Orphan warning, no booking section | ✅ |
| TC_AD_PAYDETAIL_012 | Breadcrumb Payments link → list | ⏳ |

---

## 8. Test cases — Timeline (P1)

| ID gốc | ID Auto | Mô tả | Auto |
|--------|---------|--------|------|
| ADMIN_PAYMENT_DETAIL_021 | TC_AD_PAYDETAIL_001 | Mốc created luôn có | ✅ |
| ADMIN_PAYMENT_DETAIL_022 | TC_AD_PAYDETAIL_001 | Success: created + gateway label | ✅ |
| ADMIN_PAYMENT_DETAIL_023 | TC_AD_PAYDETAIL_006 | Failed: created + failed | ✅ |
| ADMIN_PAYMENT_DETAIL_024 | TC_AD_PAYDETAIL_006b | Refunded: created + success + refunded | ✅ |
| TC_AD_PAYDETAIL_023 | Partial: badge + timeline (no success milestone) | ⏳ |
| TC_AD_PAYDETAIL_024 | Pending: chỉ created | ⏳ |

---

## 9. Test cases — Refund permission & dialog (P0–P1)

| ID gốc | ID Auto | Mô tả | Auto |
|--------|---------|--------|------|
| ADMIN_PAYMENT_DETAIL_025 | TC_AD_PAYDETAIL_009 | Admin success: refund enabled | ⏳ |
| ADMIN_PAYMENT_DETAIL_026 | TC_AD_PAYDETAIL_025 | Failed/pending/refunded: không có nút refund | ⏳ |
| ADMIN_PAYMENT_DETAIL_027 | TC_AD_PAYDETAIL_008 | Staff: refund disabled + hint | ✅ |
| ADMIN_PAYMENT_DETAIL_028 | TC_AD_PAYDETAIL_009 | Mở dialog, hiển thị form | ⏳ *(007 mở implicit)* |
| ADMIN_PAYMENT_DETAIL_029 | TC_AD_PAYDETAIL_010 | Reason trống / <10 ký tự → validation | ⏳ |
| ADMIN_PAYMENT_DETAIL_030 | TC_AD_PAYDETAIL_007 | Refund thành công + toast | ✅ |
| ADMIN_PAYMENT_DETAIL_031 | TC_AD_PAYDETAIL_031 | Refund API 500 → toast error | ⏳ |
| ADMIN_PAYMENT_DETAIL_032 | TC_AD_PAYDETAIL_032 | Double submit disabled | ⏳ |
| ADMIN_PAYMENT_DETAIL_033 | TC_AD_PAYDETAIL_033 | Refunded: không còn refund action | ⏳ |
| ADMIN_PAYMENT_DETAIL_040 | TC_AD_PAYDETAIL_040b | Lifecycle: refund → status refunded | ⏳ |
| TC_AD_PAYDETAIL_019 | Cancel / X đóng dialog không POST | ⏳ |
| TC_AD_PAYDETAIL_020 | Backdrop click đóng dialog | ⏳ |
| TC_AD_PAYDETAIL_021 | Bank fields khi không có refund request | ⏳ |
| TC_AD_PAYDETAIL_022 | VietQR khi có `latestRefundRequest` bank | ⏳ |

---

## 10. Test cases — Responsive (manual / low priority)

| ID gốc | ID Auto | Mô tả | Auto |
|--------|---------|--------|------|
| ADMIN_PAYMENT_DETAIL_038 | — | Desktop 2 cột (payment + timeline) | manual-only |
| ADMIN_PAYMENT_DETAIL_039 | TC_AD_PAYDETAIL_039 | Mobile 375px layout 1 cột | ⏳ optional |

---

## 11. Tổng hợp inventory ↔ automation

| Nhóm | Tổng TC có thể | Đã auto ✅ | Gap ⏳ | Manual |
|------|----------------|------------|--------|--------|
| Auth | 3 | 1 | 2 | 0 |
| Load/Error | 5 | 4 | 1 | 0 |
| Payment fields | 12 | 1 partial | 10 | 1 |
| Booking/Orphan | 6 | 4 | 2 | 0 |
| Timeline | 6 | 4 | 2 | 0 |
| Refund | 14 | 2 | 12 | 0 |
| Responsive | 2 | 0 | 1 | 1 |
| **Tổng** | **~48** | **37** | **~2** | **~9** |

**Hiện trạng:** `npm run test:admin:payment-detail` — **37/37 passed** (34 core + 3 auth).

---

## 12. Đề xuất cải thiện product (Improvement Backlog)

| ID | Loại | Ưu tiên | Phát hiện | Đề xuất | File | Trạng thái |
|----|------|---------|-----------|---------|------|------------|
| IMP_PAYDET_001 | Doc | P2 | Doc ghi PayOS / TXN001 | Cập nhật SePay + mã PAY-* | `13b_payment_detail.md` | **fixed** |
| IMP_PAYDET_002 | i18n | P2 | Refund validation hardcode VI | Dùng `payment:validation.*` | `RefundPaymentDialog.tsx` | **fixed** |
| IMP_PAYDET_003 | i18n | P2 | VietQR block hardcode VI | i18n keys | `RefundPaymentDialog.tsx` | **fixed** |
| IMP_PAYDET_004 | UX | P2 | Detail API 500 hiện not found (không phân biệt 404/500) | Tách copy load error vs not found | `PaymentDetail/index.tsx` | **fixed** |
| IMP_PAYDET_005 | Test | P1 | Thiếu `payment-detail-auth.spec.ts` | Tách auth TC 040–041 | `tests/admin/` | **fixed** |
| IMP_PAYDET_006 | Test | P1 | Refund regression chưa đủ | Bổ sung PAYDETAIL_010–040b | `payment-detail.spec.ts` | **fixed** |
| IMP_PAYDET_007 | A11y | P3 | Nút đóng dialog thiếu aria-label | Thêm label | `RefundPaymentDialog.tsx` | **fixed** |

---

## 13. Thứ tự implement automation (đề xuất)

```
P0 — Auth detail (040–041) + refund hidden non-success (025–026, 033)
P1 — Validation refund (010) + API error (031) + breadcrumb (012)
P1 — Field display (013–016) + status badges (034) + pending/partial timeline
P2 — Dialog cancel/backdrop (019–020) + VietQR path (022) + lifecycle (040b)
P3 — Responsive / long text (manual hoặc viewport test)
```

**Mock cần:** `setPaymentDetailFailForId`, `setPaymentRefundFailForId` — đã có trong `payments.mock.ts`.

**Data cần bổ sung:** `zeroAmountPayment`, `longTransactionCodePayment`, `refundedNoReasonPayment`, `pendingPayment` detail scenarios.

---

## 14. Ghi chú kỹ thuật

* Refund chỉ render action khi `payment.status === 'success'` (`isSuccess`).
* Timeline `partially_paid` / `pending` chỉ có mốc **created** (không có success milestone).
* `RefundPaymentDialog` refetch detail khi mở (`useAdminPaymentDetailQuery` enabled khi `isOpen`).
* Staff vẫn **thấy** nút refund nhưng `disabled` + hint dưới subtitle.
