# Man hinh Lich su & Chi tiet Dat cho (Booking History & Booking Detail)

## Pham vi

- Route danh sach: `/profile/bookings` hoac `/[locale]/profile/bookings`
- Route chi tiet: `/profile/bookings/[id]`, `/profile/bookings/code/[bookingCode]` hoac locale tuong ung
- API lien quan: Danh sach booking ca nhan, chi tiet booking theo id/code, huy booking, tai hoa don, thanh toan lai, danh gia tour sau khi hoan thanh.
- Vai tro: Nguoi dung da dang nhap (User).

## Dieu kien truoc

- Tai khoan: Da dang nhap, co booking o nhieu trang thai: pending, confirmed, completed, cancelled; co booking online payment unpaid/failed/partially_paid.
- Moi truong: Local dev server (`http://localhost:3000`).

## Test cases

### Phan 1: Lich su dat cho (`/profile/bookings`)

| TT | Test Case ID | Chuc nang | Mo ta Test Case | Dieu kien tien quyet | Buoc thuc hien | Du lieu test | Ket qua mong doi | Ket qua thuc te | Status | Ghi chu |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_HISTORY_001 | Danh sach don hang | Xem danh sach booking ca nhan | User co booking | Truy cap `/vi/profile/bookings`. | | Hien thi card/bang booking gom ma don, ten tour, ngay khoi hanh, tong tien, booking status va payment status. | | | |
| 2 | TC_HISTORY_002 | Bo loc trang thai | Loc booking theo trang thai | Co nhieu status | Click lan luot cac tab/filter status. | Pending/Confirmed/Completed/Cancelled | Danh sach cap nhat dung status da chon, co empty state neu khong co du lieu. | | | |
| 3 | TC_HISTORY_003 | Mo chi tiet | Dieu huong sang booking detail | Co booking trong danh sach | Click "Xem chi tiet" tren mot booking. | | Chuyen den `/vi/profile/bookings/[id]` hoac route code tuong ung. | | | |
| 4 | TC_HISTORY_004 | Huy booking tu danh sach | Huy booking pending/confirmed chua qua ngay di | Booking co the huy | Click cancel tren card, nhap ly do, confirm. | Ly do: Thay doi ke hoach | Booking cap nhat sang cancelled, nut huy bien mat, danh sach refetch/cap nhat. | | | |
| 5 | TC_HISTORY_005 | Danh gia sau khi hoan thanh | Viet review cho tour completed | Booking completed va chua review | Click Review Now, chon sao, nhap noi dung, gui. | 5 sao, "Tour rat vui" | Toast thanh cong, nut review cap nhat/an, review xuat hien tren tour detail neu API dong bo. | | | |

### Phan 2: Chi tiet dat cho (`/profile/bookings/[id]` hoac `/profile/bookings/code/[bookingCode]`)

| TT | Test Case ID | Chuc nang | Mo ta Test Case | Dieu kien tien quyet | Buoc thuc hien | Du lieu test | Ket qua mong doi | Ket qua thuc te | Status | Ghi chu |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 6 | TC_BOOKINGDETAIL_001 | Tai chi tiet booking | Hien thi chi tiet booking theo id | Booking id/code hop le | Truy cap detail booking. | Booking bat ky | Hien thi header, ma booking, timeline status, tour card, customer info, price summary va action buttons. | | | |
| 7 | TC_BOOKINGDETAIL_002 | Loading skeleton | Kiem tra skeleton khi dang tai | API phan hoi cham | Mo route detail. | | Hien thi skeleton header, timeline, tour card, customer card va price summary. | | | |
| 8 | TC_BOOKINGDETAIL_003 | Error/retry/back | Kiem tra booking khong ton tai | ID/code khong hop le | Truy cap route sai, click Retry va Back. | | Hien thi error/empty card; Retry goi lai API; Back ve `/profile/bookings`. | | | |
| 9 | TC_BOOKINGDETAIL_004 | Download invoice unpaid | Chan tai hoa don khi chua thanh toan success | Booking payment_status khac `success` | Click nut download invoice. | Payment pending/unpaid | Hien toast warning invoice_unpaid_error, khong goi download blob. | | | |
| 10 | TC_BOOKINGDETAIL_005 | Download invoice success | Tai hoa don khi da thanh toan | Booking payment_status `success` | Click nut download invoice. | | Goi API invoice, tao file `invoice-[booking_code].pdf`, toast thanh cong, nut loading trong luc tai. | | | |
| 11 | TC_BOOKINGDETAIL_006 | Print invoice | Kiem tra in hoa don | Booking detail da tai | Click nut print. | | Goi `window.print()`, print-only invoice header hien khi in, action buttons an trong print. | | | |
| 12 | TC_BOOKINGDETAIL_007 | Huy booking detail | Huy booking pending/confirmed chua qua ngay di | Booking canCancel = true | Click icon huy, nhap ly do trong CancelBookingDialog, submit. | Ly do: Khong sap xep duoc thoi gian | Dialog dong, detail refetch, booking status thanh cancelled va hien cancellation reason. | | | |
| 13 | TC_BOOKINGDETAIL_008 | Khong the huy | Kiem tra booking khong huy duoc | Booking completed/cancelled hoac da qua ngay di | Mo detail booking. | | Nut huy khong hien; khong co cach submit cancel. | | | |
| 14 | TC_BOOKINGDETAIL_009 | Thanh toan lai | Kiem tra continue payment | Booking online payment pending/failed/unpaid/partially_paid va chua cancelled | Chon gateway PayOS/VNPay/MoMo/ZaloPay neu enabled, click continue payment. | Gateway: PayOS | Gateway active duoc highlight; retryPayment goi voi bookingCode va payment_method; nut loading khi dang xu ly. | | | |
| 15 | TC_BOOKINGDETAIL_010 | Booking cancelled | Kiem tra giao dien booking da huy | Booking status `cancelled`, co cancellation_reason | Mo detail. | | Hien panel ly do huy va nut dat lai neu co tour slug; click dat lai chuyen den `/tours/[slug]`. | | | |
| 16 | TC_BOOKINGDETAIL_011 | Responsive | Kiem tra mobile layout | | Mo viewport 375px va 768px. | | Header action icon khong tran, grid detail xep 1 cot, price summary/documents khong che noi dung. | | | |

## Ghi chu

- Route `/dashboard` cu khong phai route chinh cua booking history theo code hien tai; booking history nam trong profile.
