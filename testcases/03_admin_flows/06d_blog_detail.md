# Man hinh Chi tiet Bai viet (Admin Blog Post Detail Page)

## Pham vi

- Route: `/admin/blog-posts/:id`
- API lien quan: Chi tiet bai viet, cap nhat status, xoa bai viet, nhan ban bai viet.
- Vai tro: Quan tri vien (Admin) / Nhan vien (Staff).

## Dieu kien truoc

- Tai khoan: Da dang nhap trang quan tri bang tai khoan Admin/Staff.
- Du lieu mau: Bai viet ton tai voi cac status `draft`, `published`, `archived`, co featured image, author, categories, view count.
- Moi truong: Local dev server (`http://localhost:5173`).

## Test cases

| TT | Test Case ID | Chuc nang | Mo ta Test Case | Dieu kien tien quyet | Buoc thuc hien | Du lieu test | Ket qua mong doi | Ket qua thuc te | Status | Ghi chu |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_AD_BLOGDETAIL_001 | Tai trang chi tiet | Xem preview bai viet trong admin | Blog id hop le | Truy cap `/admin/blog-posts/:id`. | Bai viet bat ky | Hien thi sticky header, title, status badge, anh bia, noi dung rich text, sidebar action, author va metadata. | | | |
| 2 | TC_AD_BLOGDETAIL_002 | Loading skeleton | Kiem tra skeleton khi dang tai | API phan hoi cham | Mo trang detail. | | Hien thi skeleton content va sidebar, khong hien data null. | | | |
| 3 | TC_AD_BLOGDETAIL_003 | Error/not found | Kiem tra bai viet khong ton tai | ID khong hop le | Truy cap `/admin/blog-posts/999999`. | | Hien thi error card "Khong tim thay bai viet" va nut quay ve danh sach. | | | |
| 4 | TC_AD_BLOGDETAIL_004 | Doi status | Cap nhat draft/published/archived | Bai viet ton tai | Mo dropdown status tren header, chon status khac. | draft -> published | Goi mutation update status, dropdown dong, toast thanh cong, trang refetch va badge cap nhat. | | | |
| 5 | TC_AD_BLOGDETAIL_005 | Xem bai viet public | Mo preview public post | Bai viet status `published`, co slug | Click "Xem bai viet". | | Mo tab moi `http://localhost:3000/blog/[slug]`; nut preview bi disabled neu status khong phai published. | | | |
| 6 | TC_AD_BLOGDETAIL_006 | Chinh sua | Dieu huong sang form edit | Bai viet ton tai | Click nut edit tren header/sidebar. | | Dieu huong den `/admin/blog-posts/edit/:id`. | | | |
| 7 | TC_AD_BLOGDETAIL_007 | Nhan ban bai viet | Tao ban sao tu detail | Bai viet ton tai | Click "Nhan ban bai viet", xac nhan dialog. | | Dieu huong den `/admin/blog-posts/create` kem state duplicateData; toast thanh cong. | | | |
| 8 | TC_AD_BLOGDETAIL_008 | Xoa bai viet admin | Xoa bai viet qua confirm dialog | Dang nhap admin | Click Delete, xac nhan. | | Goi API xoa, toast thanh cong, dieu huong ve `/admin/blog-posts`. | | | |
| 9 | TC_AD_BLOGDETAIL_009 | Phan quyen xoa staff | Staff khong duoc xoa | Dang nhap staff | Mo detail va quan sat action xoa. | | Nut xoa bi an hoac disabled voi tooltip/visual disabled; khong goi API xoa. | | | |
| 10 | TC_AD_BLOGDETAIL_010 | Metadata sidebar | Kiem tra author, ngay tao/cap nhat, luot xem, category | Bai viet co metadata | Quan sat sidebar. | | Hien thi author, status/publishedAt, createdAt, updatedAt, view count, categories dung format. | | | |

## Ghi chu

- Route cu `/admin/blog/[id]` khong dung voi code hien tai.
