# Man hinh Quan ly Giao dich & Thanh toan (Payment Transactions Management)

## Pham vi

- Route: `/admin/payments`, `/admin/payments/detail/:id`
- API lien quan: Danh sach giao dich thanh toan, chi tiet giao dich, hoan tien giao dich thanh cong.
- Vai tro: Quan tri vien (Admin) / Nhan vien (Staff).

## Dieu kien truoc

- Tai khoan: Da dang nhap trang quan tri bang tai khoan Admin/Staff.
- Du lieu mau: Co giao dich o cac status `success`, `failed`, `pending`, `refunded`; co giao dich lien ket booking va giao dich orphan khong co booking.
- Moi truong: Local dev server (`http://localhost:5173`).

## Test cases

### Phan 1: Danh sach giao dich (`/admin/payments`)

| TT | Test Case ID | Chuc nang | Mo ta Test Case | Dieu kien tien quyet | Buoc thuc hien | Du lieu test | Ket qua mong doi | Ket qua thuc te | Status | Ghi chu |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_AD_PAY_001 | Danh sach giao dich | Xem danh sach toan bo giao dich thanh toan | Co du lieu payment | Truy cap `/admin/payments`. | | Bang hien thi ma giao dich, ma booking, cong thanh toan, so tien, trang thai, ngay giao dich va action. | | | |
| 2 | TC_AD_PAY_002 | Tim kiem giao dich | Tim theo ma giao dich hoac ma don | Co ma can tim | Nhap tu khoa vao search va submit. | Ma: `PAY123456` | Bang cap nhat dung giao dich phu hop, pagination reset ve trang dau neu co. | | | |
| 3 | TC_AD_PAY_003 | Loc cong thanh toan | Loc theo gateway | Co nhieu gateway | Chon PayOS/VNPay/MoMo/ZaloPay trong filter. | Gateway: PayOS | Chi hien thi giao dich cua gateway da chon. | | | |
| 4 | TC_AD_PAY_004 | Loc trang thai | Loc theo payment status | Co nhieu status | Chon status success/failed/pending/refunded. | Status: success | Bang chi hien thi giao dich dung status, badge mau dung. | | | |
| 5 | TC_AD_PAY_005 | Mo chi tiet | Dieu huong tu list sang detail | Co giao dich trong bang | Click nut xem chi tiet tai mot dong. | | Dieu huong den `/admin/payments/detail/:id`. | | | |

### Phan 2: Chi tiet giao dich (`/admin/payments/detail/:id`)

| TT | Test Case ID | Chuc nang | Mo ta Test Case | Dieu kien tien quyet | Buoc thuc hien | Du lieu test | Ket qua mong doi | Ket qua thuc te | Status | Ghi chu |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 6 | TC_AD_PAYDETAIL_001 | Tai trang chi tiet | Hien thi thong tin giao dich | Payment id hop le | Truy cap `/admin/payments/detail/:id`. | Payment success | Hien thi transactionCode, status badge, amount, gateway badge, transactionDate, paidAt/refundedAt neu co, booking/customer block va timeline. | | | |
| 7 | TC_AD_PAYDETAIL_002 | Loading state | Kiem tra spinner khi dang tai | API phan hoi cham | Mo trang detail. | | Hien thi spinner/loading text, khong hien data rong. | | | |
| 8 | TC_AD_PAYDETAIL_003 | Not found/error | Kiem tra giao dich khong ton tai | ID khong hop le | Truy cap `/admin/payments/detail/999999`. | | Hien thi "Khong tim thay giao dich" va nut quay ve danh sach. | | | |
| 9 | TC_AD_PAYDETAIL_004 | Booking linked | Kiem tra block don dat va khach hang | Payment co bookingId | Quan sat block "Don dat & Khach hang", click booking code. | | Hien thi customer name/email/avatar, booking code, tour name/thumbnail; click booking code chuyen den `/admin/bookings/detail/:bookingId`. | | | |
| 10 | TC_AD_PAYDETAIL_005 | Orphan payment | Kiem tra giao dich khong gan booking | Payment khong co bookingId | Mo detail payment orphan. | | Hien thi warning giao dich khong dinh kem don hang, khong render block booking rong. | | | |
| 11 | TC_AD_PAYDETAIL_006 | Timeline success/failed/refunded | Kiem tra timeline theo status | Co payment success, failed, refunded | Mo tung detail. | | Success co moc created + success; failed co created + failed; refunded co created + success + refunded va ly do. | | | |
| 12 | TC_AD_PAYDETAIL_007 | Hoan tien admin | Admin refund payment success | Dang nhap admin, payment status `success` | Click Refund, nhap ly do, confirm. | Ly do: Khach huy tour | Goi API refund, toast thanh cong, dialog dong, status/timeline cap nhat sau refetch. | | | |
| 13 | TC_AD_PAYDETAIL_008 | Phan quyen refund staff | Staff khong duoc refund | Dang nhap staff, payment success | Mo detail payment success. | | Nut refund bi disabled/an, hien helper "Chi nguoi quan tri moi co quyen..." va khong goi API. | | | |

## Ghi chu

- Code hien tai khong hien raw payload/webhook log tren detail; testcase da cap nhat theo UI thuc te gom payment info, booking/customer, timeline va refund.
