# DanangTrip Data Center

Day la diem mo dau tien cho AI khi tiep tuc cong viec du lieu DanangTrip.

Thu muc nay khong di chuyen file goc cua crawler/seeders. No gom trang thai bang index de tranh lam hong cac script dang dung duong dan hien tai.

## Nguon goc

- Crawler root: `D:\DATN\DATN_Tài liệu\danangtrip-crawler`
- Crawler data: `D:\DATN\DATN_Tài liệu\danangtrip-crawler\data`
- SQL seeders: `D:\DATN\DATN_Tài liệu\database-seeders`
- Memory: `D:\DATN\DATN_Tài liệu\danangtrip-crawler\memory.md`
- API migrations: `D:\DATN\danangtrip-api\database\migrations`

## Trang thai hien tai

- Tours: da crawl, normalize, review, approve batch dau.
- Tour schedules: da tao schedule review va approve theo tour approved.
- Locations/POI: da crawl Overpass, enriched image URL candidate, approve clean batch 1.
- Blog posts: seed cu dang la du lieu demo; dang bat dau thu thap travel guide text-only.
- User/action tables: nen seed demo, khong crawl du lieu that.

## File index chinh

- `indexes/data-inventory.md`
- `indexes/seed-run-order.md`
- `indexes/next-collection-plan.md`
- `reports/data-readiness-report-2026-06-03.md`

## Nguyen tac

- Khong ghi crawl data truc tiep vao production table.
- Luong dung: raw -> normalized -> pending_review -> approved -> published.
- Khong tao anh moi.
- Chi thu thap text/structured DB data va giu source_url.
- Noi dung dai phai rewrite/tom tat, khong copy nguyen van.
