# Man hinh Cam nang du lich / Blog (Blog Listing & Blog Detail)

## Pham vi

- Route: `/blog`, `/blog/[slug]` hoac `/[locale]/blog`, `/[locale]/blog/[slug]`
- API lien quan: Danh sach bai viet blog, chi tiet bai viet blog, sidebar popular posts, bai viet lien quan.
- Vai tro: Khach vang lai (Guest) / Nguoi dung da dang nhap (User).

## Dieu kien truoc

- Du lieu mau: Co danh sach bai viet voi category, featured image, excerpt; bai viet chi tiet co content HTML gom H2/H3 de tao table of contents.
- Moi truong: Local dev server (`http://localhost:3000`).

## Test cases

### Phan 1: Trang danh sach Blog (`/blog`)

| TT | Test Case ID | Chuc nang | Mo ta Test Case | Dieu kien tien quyet | Buoc thuc hien | Du lieu test | Ket qua mong doi | Ket qua thuc te | Status | Ghi chu |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_BLOG_001 | Tai danh sach | Kiem tra trang danh sach blog | Co bai viet published | Truy cap `/vi/blog`. | | Hien thi featured post/card blog, category/sidebar neu co, anh dai dien, tieu de, excerpt, author/date. | | | |
| 2 | TC_BLOG_002 | Tim kiem bai viet | Tim kiem bai viet theo tu khoa | Co bai viet phu hop | Nhap tu khoa tim kiem va submit. | Tu khoa: "Da Nang" | Danh sach cap nhat va chi hien bai viet phu hop; co empty state neu khong co ket qua. | | | |
| 3 | TC_BLOG_003 | Loc theo chuyen muc | Loc danh sach bai viet theo category | Co bai viet thuoc category | Click mot category tren thanh/category row/sidebar. | Category: Am thuc | URL/filter cap nhat, danh sach chi hien bai viet thuoc category da chon. | | | |
| 4 | TC_BLOG_004 | Click xem chi tiet | Dieu huong sang blog detail | Co bai viet hien thi | Click anh/tieu de bai viet. | | Chuyen den `/vi/blog/[slug]`, detail render dung bai viet vua chon. | | | |

### Phan 2: Trang chi tiet bai viet (`/blog/[slug]`)

| TT | Test Case ID | Chuc nang | Mo ta Test Case | Dieu kien tien quyet | Buoc thuc hien | Du lieu test | Ket qua mong doi | Ket qua thuc te | Status | Ghi chu |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 5 | TC_BLOGDETAIL_001 | Tai trang chi tiet | Hien thi bai viet chi tiet | Slug bai viet published hop le | Truy cap `/vi/blog/[slug]`. | Bai viet published | Hien thi ReadingProgressBar, header bai viet, featured image neu co, rich text content, author card, related posts va sidebar tren desktop. Metadata/OpenGraph theo bai viet. | | | |
| 6 | TC_BLOGDETAIL_002 | Trang khong ton tai | Xu ly slug sai | Khong co bai viet voi slug nay | Truy cap `/vi/blog/slug-khong-ton-tai`. | | Hien thi not found hoac trang loi theo Next.js, khong render content rong. | | | |
| 7 | TC_BLOGDETAIL_003 | Rich text content | Kiem tra noi dung HTML | Bai viet co H2/H3, paragraph, image/list/blockquote | Doc phan noi dung. | | Heading, paragraph, list, quote, link va image render dung style; text khong tran layout, khong hien HTML raw khong mong muon. | | | |
| 8 | TC_BLOGDETAIL_004 | Table of contents | Kiem tra TOC tu H2/H3 | Content co it nhat 2 heading H2/H3 | Quan sat sidebar desktop, click mot heading. | | TOC hien danh sach heading da duoc inject id; click cuon den dung section. Mobile khong bat buoc hien sidebar. | | | |
| 9 | TC_BLOGDETAIL_005 | Reading progress | Kiem tra thanh tien do doc | Bai viet dai hon 1 man hinh | Cuon tu dau toi cuoi bai viet. | | ReadingProgressBar tang theo vi tri scroll va khong che noi dung. | | | |
| 10 | TC_BLOGDETAIL_006 | Bai viet lien quan | Dieu huong qua related posts | Co related posts cung category | Cuon den muc related posts, click mot bai. | | Chuyen den detail bai viet lien quan; khong hien bai viet hien tai trong related list. | | | |
| 11 | TC_BLOGDETAIL_007 | Popular posts sidebar | Kiem tra sidebar bai viet pho bien | Co popular posts | Quan sat sidebar desktop, click mot bai pho bien. | | Hien toi da 5 popular posts; click dieu huong dung slug. | | | |
| 12 | TC_BLOGDETAIL_008 | Responsive | Kiem tra mobile layout | | Mo viewport 375px va 768px. | | Noi dung xep 1 cot; featured image dung aspect ratio; sidebar an/hien theo thiet ke; text khong tran. | | | |

## Ghi chu

- Code detail hien tai xu ly content HTML server-side de inject id cho H2/H3 va tao TOC.
