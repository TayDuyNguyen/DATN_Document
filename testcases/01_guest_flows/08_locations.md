# Man hinh Chi tiet Dia diem (Location Detail Page)

## Pham vi

- Route: `/locations/[slug]` hoac `/[locale]/locations/[slug]`
- API lien quan: Chi tiet dia diem, anh dia diem, nearby locations, ghi nhan luot xem, yeu thich dia diem, danh gia dia diem.
- Vai tro: Khach vang lai (Guest) / Nguoi dung da dang nhap (User).

## Dieu kien truoc

- Du lieu mau: Dia diem ton tai trong database, co mo ta, toa do, category, dia chi, anh, rating/review va danh sach dia diem gan do.
- Moi truong: Local dev server (`http://localhost:3000`).

## Test cases

| TT | Test Case ID | Chuc nang | Mo ta Test Case | Dieu kien tien quyet | Buoc thuc hien | Du lieu test | Ket qua mong doi | Ket qua thuc te | Status | Ghi chu |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_LOCATION_001 | Tai trang chi tiet | Kiem tra trang chi tiet dia diem render dung | Slug dia diem hop le | Truy cap `/vi/locations/[slug]`. | Dia diem active | Hien thi hero, ten dia diem, thong tin chinh, rating/review, sidebar va noi dung mo ta. Metadata page co title theo ten dia diem. | | | |
| 2 | TC_LOCATION_002 | Trang khong ton tai | Kiem tra xu ly slug sai | Khong co dia diem voi slug nay | Truy cap `/vi/locations/slug-khong-ton-tai`. | | Hien thi not found, khong render trang detail rong, khong loi console nghiem trong. | | | |
| 3 | TC_LOCATION_003 | Gallery anh | Kiem tra lay anh tu API images va fallback tu location.images | Dia diem co nhieu anh | Quan sat khu vuc gallery sau khi trang mount. | | Anh hien thi dung ti le; khi API images dang loading thi co loading/fallback; khi khong co anh thi khong lam vo layout. | | | |
| 4 | TC_LOCATION_004 | Ghi nhan luot xem | Kiem tra hook record view duoc goi khi vao trang | Dia diem hop le | Mo trang detail va theo doi network/log neu co. | | API record view duoc goi mot lan hop ly, khong spam khi re-render. | | | |
| 5 | TC_LOCATION_005 | Yeu thich dia diem | Kiem tra toggle favorite | User da dang nhap | Click nut yeu thich tren hero. | | Trang thai favorite cap nhat, nut disabled khi pending, thong bao/visual state ro rang. | | | |
| 6 | TC_LOCATION_006 | Yeu thich voi guest | Kiem tra hanh vi guest khi click favorite | Chua dang nhap | Click nut yeu thich. | | He thong yeu cau dang nhap hoac xu ly theo flow hien tai, khong reload sai trang va khong loi UI. | | | |
| 7 | TC_LOCATION_007 | Thong tin dia diem | Kiem tra LocationInfo | Dia diem co dia chi, toa do, gio mo cua/category | Doc phan thong tin chinh. | | Hien thi day du mo ta, dia chi, category, gio mo cua neu co; field null co fallback phu hop. | | | |
| 8 | TC_LOCATION_008 | Ban do/sidebar | Kiem tra LocationSidebar | Dia diem co toa do | Quan sat sidebar va click link/nut ban do neu co. | | Hien thi thong tin lien he/ban do/CTA dung; link ban do mo dung toa do/dia chi. | | | |
| 9 | TC_LOCATION_009 | Dia diem gan do | Kiem tra nearby locations | API nearby co du lieu | Cuon/quan sat sidebar muc nearby. | | Hien thi toi da 6 dia diem gan do, co loading state, click item chuyen sang chi tiet dia diem tuong ung. | | | |
| 10 | TC_LOCATION_010 | Danh gia dia diem | Kiem tra LocationReviews | Dia diem co review | Cuon den phan danh gia. | | Hien thi diem trung binh, so review, danh sach review; co empty/loading state neu chua co review. | | | |
| 11 | TC_LOCATION_011 | Responsive | Kiem tra layout mobile | | Mo viewport 375px va 768px. | | Hero, gallery, info, reviews va sidebar xep 1 cot; text khong tran, nut favorite khong che noi dung. | | | |

## Ghi chu

- Trang detail hien tai gom hero + gallery + info/reviews + sidebar/nearby, khong phai danh sach tour lien quan.
