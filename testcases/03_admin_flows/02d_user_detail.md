# Man hinh Chi tiet Nguoi dung (Admin User Detail Page)

## Pham vi

- Route: `/admin/users/detail/:id`
- API lien quan: Chi tiet user, booking gan day, rating gan day, cap nhat role/status, xoa user.
- Vai tro: Quan tri vien (Admin).

## Dieu kien truoc

- Tai khoan: Da dang nhap trang quan tri bang tai khoan Admin.
- Du lieu mau: User ton tai, co booking/rating/favorite; co them user khac de test khoa/xoa, va tai khoan admin hien tai de test self-protection.
- Moi truong: Local dev server (`http://localhost:5173`).

## Test cases

| TT | Test Case ID | Chuc nang | Mo ta Test Case | Dieu kien tien quyet | Buoc thuc hien | Du lieu test | Ket qua mong doi | Ket qua thuc te | Status | Ghi chu |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_AD_UDETAIL_001 | Tai trang chi tiet | Xem thong tin tong quan user | User id hop le | Truy cap `/admin/users/detail/:id`. | User active | Hien thi header, avatar/ten/email/role/status, PersonalInfoCard, booking gan day, rating gan day, stats va sidebar tai khoan. | | | |
| 2 | TC_AD_UDETAIL_002 | Loading state | Kiem tra trang thai dang tai | API detail phan hoi cham | Mo trang detail. | | Hien thi spinner/loading text; khong hien thong tin rong truoc khi co du lieu. | | | |
| 3 | TC_AD_UDETAIL_003 | Not found/error | Kiem tra user khong ton tai | ID khong hop le | Truy cap `/admin/users/detail/999999`. | | Hien thi card loi "Khong tim thay tai khoan" va nut quay lai danh sach user. | | | |
| 4 | TC_AD_UDETAIL_004 | Booking gan day | Kiem tra bang booking cua user | User co booking | Quan sat UserBookingsTable. | | Hien thi toi da 5 booking gan day, tong so booking dung, co ma booking/tour/tong tien/trang thai; loading table ro rang. | | | |
| 5 | TC_AD_UDETAIL_005 | Rating gan day | Kiem tra danh sach rating cua user | User co rating | Quan sat UserRatingsList. | | Hien thi toi da 3 rating gan day, tong so rating dung, diem sao/noi dung/ngay tao dung. | | | |
| 6 | TC_AD_UDETAIL_006 | Stats card | Kiem tra thong ke user | User co du lieu thong ke | Quan sat UserStatsCards. | | Hien thi bookingsCount, ratingsCount, favoritesCount, totalSpend dung format tien/so. | | | |
| 7 | TC_AD_UDETAIL_007 | Khoa/mo khoa user | Cap nhat status active/banned | User khac admin hien tai | Click action khoa tai khoan, sau do click mo khoa. | | Goi mutation status dung; toast thanh cong; trang refetch va status cap nhat. | | | |
| 8 | TC_AD_UDETAIL_008 | Doi vai tro | Cap nhat role user/admin | User khac admin hien tai | Mo ChangeRoleDialog, chon role moi, xac nhan. | Role: admin/user | Dialog dong sau thanh cong, toast thanh cong, role tren header/sidebar cap nhat. | | | |
| 9 | TC_AD_UDETAIL_009 | Self protection | Khong cho admin tu khoa/doi role/xoa chinh minh | Dang xem user id trung currentAdmin.id | Quan sat action card/header. | | Cac action nguy hiem bi an/disabled theo UI, khong the tu khoa hoac xoa tai khoan dang dang nhap. | | | |
| 10 | TC_AD_UDETAIL_010 | Xoa user | Xoa user qua confirm dialog | User khac admin hien tai | Click xoa, xac nhan trong dialog. | | Goi API xoa, toast thanh cong, dieu huong ve `/admin/users`. | | | |

## Ghi chu

- Route cu `/admin/users/[id]` khong dung voi code hien tai.
