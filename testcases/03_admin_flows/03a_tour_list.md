# Man hinh Danh sach Tour & Modal Chi tiet Tour (Admin Tour List Page)

## Pham vi

- Route: `/admin/tours/list`
- API lien quan: Danh sach tour co phan trang/loc/tim kiem, thong ke tour, cap nhat status/featured/hot, xoa tour, export, lich khoi hanh trong modal chi tiet.
- Vai tro: Quan tri vien (Admin) / Nhan vien (Staff).

## Dieu kien truoc

- Tai khoan: Da dang nhap trang quan tri bang tai khoan Admin/Staff.
- Du lieu mau: Co nhieu tour voi category, status, booking availability, thumbnail/gallery, itinerary, schedules.
- Moi truong: Local dev server (`http://localhost:5173`).

## Test cases

### Phan 1: Danh sach tour

| TT | Test Case ID | Chuc nang | Mo ta Test Case | Dieu kien tien quyet | Buoc thuc hien | Du lieu test | Ket qua mong doi | Ket qua thuc te | Status | Ghi chu |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_AD_TLIST_001 | Render danh sach | Hien thi bang tour va stats | Co du lieu tour | Truy cap `/admin/tours/list`. | | Hien thi header, stats, filter va bang tour voi anh, ten, gia nguoi lon, category, status, booking availability, ngay tao, action. | | | |
| 2 | TC_AD_TLIST_002 | Tim kiem nhanh | Tim tour theo keyword | Co tour khop | Nhap keyword trong filter. | Tu khoa: `Ba Na` | Bang cap nhat tour phu hop, page reset ve 1. | | | |
| 3 | TC_AD_TLIST_003 | Loc tour | Loc theo category/status/booking availability/type/sort | Co nhieu loai tour | Chon tung filter. | Status: active | Danh sach cap nhat dung filter; selection cu duoc clear khi doi filter/limit. | | | |
| 4 | TC_AD_TLIST_004 | Phan trang | Kiem tra pagination va limit | Tong tour > limit | Doi page va limit. | Limit: 20 | Bang hien dung so dong, page cap nhat, khong mat filter dang chon. | | | |
| 5 | TC_AD_TLIST_005 | Toggle status | Bat/tat trang thai tour | Tour dang active/inactive | Doi status tren dong tour. | active -> inactive | Goi mutation status dung id/status, toast/refresh phu hop, UI cap nhat. | | | |
| 6 | TC_AD_TLIST_006 | Toggle featured/hot | Bat/tat featured va hot | Tour ton tai | Click switch featured/hot tren dong tour. | | Goi API dung id/value; switch disabled/loading neu co; khong double submit. | | | |
| 7 | TC_AD_TLIST_007 | Bulk status | Doi status nhieu tour | Chon nhieu dong | Tick checkbox nhieu tour, chon bulk active/inactive. | 2 tours | Goi mutation cho tung id, toast thanh cong voi count, rowSelection clear. | | | |
| 8 | TC_AD_TLIST_008 | Xoa tour | Xoa mot tour | Tour co the xoa | Click delete tai dong tour, confirm dialog. | | Goi API xoa, dialog dong, bang refresh/loai tour khoi danh sach; neu co rang buoc booking thi hien loi. | | | |
| 9 | TC_AD_TLIST_009 | Bulk delete | Xoa nhieu tour | Chon nhieu tour co the xoa | Tick nhieu dong, click bulk delete, confirm. | 2 tours | Goi delete tung id, toast thanh cong voi count, selection clear. | | | |
| 10 | TC_AD_TLIST_010 | Export | Xuat danh sach tour theo filter | Co quyen export | Click export tren header. | | Goi export voi filters hien tai, nut loading khi export, file tai ve/thong bao thanh cong. | | | |

### Phan 2: Modal chi tiet tour

| TT | Test Case ID | Chuc nang | Mo ta Test Case | Dieu kien tien quyet | Buoc thuc hien | Du lieu test | Ket qua mong doi | Ket qua thuc te | Status | Ghi chu |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 11 | TC_AD_TDETAIL_001 | Mo modal chi tiet | Xem nhanh thong tin tour tu list | Co tour trong bang | Click action view/xem chi tiet tren dong tour. | | Modal hien overlay, title tour, ma tour, status badge, booking availability badge, nut edit va close. | | | |
| 12 | TC_AD_TDETAIL_002 | Media preview | Kiem tra thumbnail/gallery trong modal | Tour co thumbnail/images | Quan sat khu vuc anh trong modal. | | Thumbnail hien dung aspect video; toi da 4 anh gallery; neu thieu anh hien fallback no data, khong vo layout. | | | |
| 13 | TC_AD_TDETAIL_003 | Quick stats | Kiem tra gia/thoi luong/so nguoi/meeting point | Tour co field day du | Doc card thong tin ben phai. | | Gia format theo locale, thoi luong, max people va meeting point hien dung; field thieu hien no data. | | | |
| 14 | TC_AD_TDETAIL_004 | Mo ta va itinerary | Kiem tra rich description va lich trinh | Tour co description HTML va itinerary | Cuon trong modal den description/itinerary. | | Description HTML render dung; itinerary hien theo ngay/tieu de/noi dung; neu rong hien empty state. | | | |
| 15 | TC_AD_TDETAIL_005 | Lich khoi hanh trong modal | Kiem tra API schedules cua tour | Tour co schedules | Mo modal va doi schedules load xong. | | Hien loading khi dang tai; sau do hien danh sach startDate-endDate, bookedSlots/totalSlots va status available/full/cancelled. | | | |
| 16 | TC_AD_TDETAIL_006 | Schedules error retry | Kiem tra loi load schedules | Gia lap API schedules loi | Mo modal, click retry trong alert. | | Alert loi hien ro; click retry goi lai API va co the hien du lieu sau khi thanh cong. | | | |
| 17 | TC_AD_TDETAIL_007 | Edit tu modal | Dieu huong sang form edit | Modal dang mo | Click nut edit trong modal. | | Modal dong va dieu huong den `/admin/tours/edit/:id`. | | | |
| 18 | TC_AD_TDETAIL_008 | Dong modal | Dong bang nut X/backdrop/close | Modal dang mo | Click X hoac nut close cuoi modal. | | Modal dong, scroll/background list tro lai binh thuong, khong mat filter/list state. | | | |

## Ghi chu

- Code hien tai khong co route admin tour detail rieng; chi tiet tour nam trong `TourDetailModal` cua trang list.
