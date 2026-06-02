# Man hinh Chi tiet Dia diem (Admin Location Detail Page)

## Pham vi

- Route: `/admin/locations/detail/:id`
- API lien quan: Chi tiet dia diem, danh gia dia diem, cap nhat status, toggle featured, xoa dia diem.
- Vai tro: Quan tri vien (Admin) / Nhan vien (Staff).

## Dieu kien truoc

- Tai khoan: Da dang nhap trang quan tri bang tai khoan Admin/Staff.
- Du lieu mau: Dia diem ton tai trong DB, co anh, toa do, review, view/favorite count.
- Moi truong: Local dev server (`http://localhost:5173`).

## Test cases

| TT | Test Case ID | Chuc nang | Mo ta Test Case | Dieu kien tien quyet | Buoc thuc hien | Du lieu test | Ket qua mong doi | Ket qua thuc te | Status | Ghi chu |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_AD_LOCDETAIL_001 | Tai trang chi tiet | Hien thi layout chi tiet dia diem | Location id hop le | Truy cap `/admin/locations/detail/:id`. | Dia diem active | Hien thi header, hero media, tabs Info/Reviews/Map, sidebar stats va card quan tri neu la admin. | | | |
| 2 | TC_AD_LOCDETAIL_002 | Loading state | Kiem tra skeleton detail | API phan hoi cham | Mo trang detail. | | Hien thi LocationDetailSkeleton, khong hien data rong. | | | |
| 3 | TC_AD_LOCDETAIL_003 | Error/retry/back | Kiem tra dia diem khong ton tai | ID khong hop le | Truy cap `/admin/locations/detail/999999`, click retry/back. | | Hien thi ErrorWidget; Retry goi lai API; Back ve `/admin/locations`. | | | |
| 4 | TC_AD_LOCDETAIL_004 | Tab Info | Kiem tra thong tin chinh | Trang detail da tai | Click tab Info. | | Hien thi mo ta, category, dia chi, toa do, gio mo cua/thong tin lien quan; rich text render dung. | | | |
| 5 | TC_AD_LOCDETAIL_005 | Tab Reviews | Kiem tra danh gia dia diem | Location co review | Click tab Reviews. | | Hien thi danh sach review/rating, loading/empty state dung neu chua co review. | | | |
| 6 | TC_AD_LOCDETAIL_006 | Tab Map | Kiem tra ban do/toa do | Location co latitude/longitude | Click tab Map. | | Hien thi ban do/preview dung toa do; neu thieu toa do thi co fallback thong bao. | | | |
| 7 | TC_AD_LOCDETAIL_007 | Stats sidebar | Kiem tra view/favorite count | Location co thong ke | Quan sat sidebar. | | View count va favorite count dung format, khong hien NaN/null. | | | |
| 8 | TC_AD_LOCDETAIL_008 | Doi status | Admin cap nhat active/inactive | Dang nhap admin | Doi select status trong Management Card. | active -> inactive | Goi bulk action dung id/action; control disabled khi updating; UI cap nhat sau thanh cong. | | | |
| 9 | TC_AD_LOCDETAIL_009 | Toggle featured | Admin bat/tat featured | Dang nhap admin | Click ToggleSwitch featured. | | Goi API update featured dung id/value; trang thai toggle cap nhat, khong double submit. | | | |
| 10 | TC_AD_LOCDETAIL_010 | Xoa dia diem | Admin xoa location | Dang nhap admin | Click Delete, xac nhan dialog. | | Goi API delete, dialog dong, dieu huong ve `/admin/locations`. | | | |
| 11 | TC_AD_LOCDETAIL_011 | Phan quyen staff | Staff xem detail | Dang nhap staff | Mo trang detail. | | Staff xem duoc thong tin/tabs/stats; card management/danger zone khong hien neu khong co role admin. | | | |

## Ghi chu

- Route cu `/admin/locations/[id]` khong dung voi code hien tai.
