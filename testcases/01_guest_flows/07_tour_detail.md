# Man hinh Chi tiet Tour (Tour Detail Page)

## Pham vi

- Route: `/tours/[slug]` hoac `/[locale]/tours/[slug]`
- API lien quan: Chi tiet tour, lich khoi hanh/booking sidebar, yeu thich tour, danh sach danh gia.
- Vai tro: Khach vang lai (Guest) / Nguoi dung da dang nhap (User).

## Dieu kien truoc

- Du lieu mau: Tour ton tai trong DB, co thumbnail/gallery, mo ta, itinerary, gia, lich khoi hanh con cho, thong tin bao gom/khong bao gom, diem hen va danh gia.
- Moi truong: Local dev server (`http://localhost:3000`).

## Test cases

| TT | Test Case ID | Chuc nang | Mo ta Test Case | Dieu kien tien quyet | Buoc thuc hien | Du lieu test | Ket qua mong doi | Ket qua thuc te | Status | Ghi chu |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_TOURDETAIL_001 | Tai trang chi tiet | Kiem tra trang chi tiet tour render dung du lieu server | Tour slug hop le | Truy cap `/vi/tours/[slug]`. | Slug tour dang active | Hien thi breadcrumb, gallery, ten tour, badge hot/featured neu co, thoi luong, rating, mo ta, itinerary va booking sidebar. Metadata page co title theo ten tour. | | | |
| 2 | TC_TOURDETAIL_002 | Trang khong ton tai | Kiem tra xu ly slug sai | Khong co tour voi slug nay | Truy cap `/vi/tours/slug-khong-ton-tai`. | | Hien thi trang not found, khong render layout detail rong, khong loi console nghiem trong. | | | |
| 3 | TC_TOURDETAIL_003 | Gallery anh | Kiem tra gallery gom thumbnail va images khong trung lap | Tour co thumbnail va nhieu images | Quan sat khu vuc gallery, click/doi anh neu component ho tro. | | Anh hien thi dung ti le, khong meo, khong lap anh trung, alt/title theo ten tour, fallback khong vo layout neu thieu anh. | | | |
| 4 | TC_TOURDETAIL_004 | Thong tin tong quan | Kiem tra noi dung overview va rich text | Tour co short_desc va description HTML/text | Doc phan Tong quan. | | Short description hien thi noi bat; description HTML render dung, text xuong dong dung, khong tran layout tren desktop/mobile. | | | |
| 5 | TC_TOURDETAIL_005 | Itinerary | Kiem tra lich trinh tour | Tour co itinerary nhieu ngay | Cuon toi phan itinerary. | Itinerary 2-3 ngay | Hien thi day du ngay, tieu de, noi dung tung moc lich trinh; neu itinerary rong thi hien thi trang thai trong phu hop. | | | |
| 6 | TC_TOURDETAIL_006 | Inclusions/Exclusions/Meeting point | Kiem tra cac khoi thong tin bo sung | Tour co inclusions, exclusions, meeting_point | Cuon qua cac khoi bao gom, khong bao gom, diem hen. | | Noi dung hien thi dung, giu xuong dong, khong hien khoi rong khi field null/empty. | | | |
| 7 | TC_TOURDETAIL_007 | Yeu thich tour | Kiem tra nut favorite tren tour detail | User da dang nhap | Click nut trai tim tren header tour. | | Trang thai favorite doi mau/fill, API toggle thanh cong, nut disabled khi dang xu ly va khong bi click lap nhieu lan. | | | |
| 8 | TC_TOURDETAIL_008 | Yeu thich khi chua dang nhap | Kiem tra hanh vi favorite voi guest | Chua dang nhap | Click nut trai tim. | | He thong yeu cau dang nhap hoac xu ly theo co che favorite hien tai; khong mat trang detail va khong loi UI. | | | |
| 9 | TC_TOURDETAIL_009 | Booking sidebar | Kiem tra chon lich khoi hanh va so khach | Tour co lich khoi hanh con cho | Chon ngay khoi hanh, tang/giam nguoi lon/tre em/em be. | 2 nguoi lon, 1 tre em | Tong tien/tam tinh cap nhat dung theo gia; nut tru khong cho so luong am; so cho con lai duoc ton trong. | | | |
| 10 | TC_TOURDETAIL_010 | Dat tour guest | Kiem tra dat tour khi chua dang nhap | Guest, da chon lich hop le | Click nut dat tour trong booking sidebar. | | Chuyen sang trang login hoac yeu cau xac thuc, giu duong dan quay lai/du lieu dat tour neu he thong ho tro. | | | |
| 11 | TC_TOURDETAIL_011 | Dat tour user | Kiem tra dat tour khi da dang nhap | User da dang nhap, lich con cho | Click nut dat tour sau khi chon thong tin. | | Chuyen den `/tours/[slug]/book` hoac flow dat tour tuong ung, thong tin lich va so khach duoc giu dung. | | | |
| 12 | TC_TOURDETAIL_012 | Danh gia tour | Kiem tra khu vuc review | Tour co danh gia | Cuon den phan danh gia. | | Hien thi diem trung binh, so luong review, danh sach review; loading/empty state ro rang neu chua co du lieu. | | | |
| 13 | TC_TOURDETAIL_013 | Responsive | Kiem tra layout tren mobile | | Mo viewport 375px va 768px. | | Gallery, noi dung va booking sidebar sap xep 1 cot, nut favorite/booking khong che noi dung, text khong tran khung. | | | |

## Ghi chu

- UI hien tai khong dung tab Overview/Itinerary/Reviews rieng; cac muc hien thi lien tuc trong trang va booking sidebar nam ben phai tren desktop.
