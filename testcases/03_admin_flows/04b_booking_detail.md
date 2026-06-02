# Man hinh Chi tiet Dat cho (Admin Booking Detail Page)

## Pham vi

- Route: `/admin/bookings/detail/:id`
- API lien quan: Chi tiet booking, cap nhat trang thai booking, huy booking, tai hoa don.
- Vai tro: Quan tri vien (Admin) / Nhan vien (Staff).

## Dieu kien truoc

- Tai khoan: Da dang nhap trang quan tri bang tai khoan Admin/Staff.
- Du lieu mau: Booking ton tai voi cac trang thai `pending`, `confirmed`, `completed`, `cancelled`; co thong tin khach, tour item, lich khoi hanh va thanh toan.
- Moi truong: Local dev server (`http://localhost:5173`).

## Test cases

| TT | Test Case ID | Chuc nang | Mo ta Test Case | Dieu kien tien quyet | Buoc thuc hien | Du lieu test | Ket qua mong doi | Ket qua thuc te | Status | Ghi chu |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_AD_BDETAIL_001 | Tai trang chi tiet | Hien thi day du thong tin booking | Booking id hop le | Truy cap `/admin/bookings/detail/:id`. | Booking bat ky | Header hien thi ma booking, booking status, payment status, ten/email khach; cac card customer, tour, hanh khach, payment summary va timeline hien thi dung. | | | |
| 2 | TC_AD_BDETAIL_002 | Loading state | Kiem tra skeleton khi dang tai | API phan hoi cham | Mo trang detail. | | Hien thi skeleton grid 2 cot, khong hien data rong. | | | |
| 3 | TC_AD_BDETAIL_003 | Error/retry | Kiem tra booking khong ton tai | ID khong hop le | Truy cap `/admin/bookings/detail/999999`, click Retry va Back. | | Hien thi error card; Retry goi lai API; Back ve `/admin/bookings`. | | | |
| 4 | TC_AD_BDETAIL_004 | Thong tin khach hang | Kiem tra card customer | Booking co customer note/address | Doc card customer. | | Hien thi ten, email, phone, address va note; neu thieu address/note thi hien fallback dung. | | | |
| 5 | TC_AD_BDETAIL_005 | Thong tin tour da dat | Kiem tra booked tour details | Booking co item tour | Doc card tour. | | Hien thi anh/fallback, ten tour, category, duration, travel date, departure place va schedule code. | | | |
| 6 | TC_AD_BDETAIL_006 | Hanh khach | Kiem tra so luong adults/children/infants | Booking co nhieu loai khach | Doc PassengerListPlaceholder. | 2 adults, 1 child, 1 infant | So luong tung loai tinh tong tu booking items chinh xac; notice API gap hien thi. | | | |
| 7 | TC_AD_BDETAIL_007 | Payment summary | Kiem tra tong tien | Booking co discount/deposit | Doc card payment. | | Hien thi subtotal, discount, deposit, final amount va payment method dung format tien. | | | |
| 8 | TC_AD_BDETAIL_008 | Confirm booking | Chuyen booking pending sang confirmed | Booking status `pending` | Click nut confirm. | | Goi update status `confirmed`, toast thanh cong, UI cap nhat/refetch theo query. | | | |
| 9 | TC_AD_BDETAIL_009 | Complete booking | Chuyen booking confirmed sang completed | Booking status `confirmed` | Click complete, xac nhan window confirm. | | Goi update status `completed`, toast thanh cong, button loading khi dang xu ly. | | | |
| 10 | TC_AD_BDETAIL_010 | Cancel booking | Huy booking pending/confirmed | Booking status `pending` hoac `confirmed` | Click cancel, nhap ly do, confirm dialog. | Ly do: Khach yeu cau huy | Goi update status `cancelled` kem reason, toast thanh cong, timeline them moc cancelled va hien ly do. | | | |
| 11 | TC_AD_BDETAIL_011 | Terminal state | Kiem tra booking completed/cancelled | Booking da completed hoac cancelled | Mo trang detail. | | Khong hien nut confirm/complete/cancel; hien notice trang thai cuoi phu hop. | | | |
| 12 | TC_AD_BDETAIL_012 | Tai hoa don | Kiem tra download invoice | Booking co invoice | Click nut invoice tren header. | | Goi API invoice, nut loading khi dang tai, toast thanh cong/loi dung. | | | |

## Ghi chu

- Code hien tai khong co action "Mark as Paid" truc tiep tren booking detail; viec thanh toan nam o payment flow/detail rieng.
