# DaNangTrip Documentation

Bo tai lieu nay gom cac tai lieu phan tich, thiet ke man hinh, API, database va tien do ban giao cua du an DaNangTrip.

## Cau truc chinh

| Thu muc | Vai tro | Ghi chu |
| --- | --- | --- |
| `docs/` | Tai lieu nghiep vu va ky thuat chinh | Nguon uu tien khi cap nhat bao cao, prompt va codegraph. |
| `danangtrip-crawler/` | He thong thu thap du lieu du lich | Scaffold crawler doc/code rieng cho Google Places, image API, blog/FAQ. |
| `screen-designs/` | Anh va HTML thiet ke man hinh | Chia theo guest, user, admin va man hinh he thong. |
| `testcases/` | Test case chuan bi kiem thu | Chia theo guest, user, admin va API. |
| `database-seeders/` | SQL seed data | Du lieu mau theo thu tu khoi tao bang. |
| `working-prompts/` | Prompt lam viec noi bo | Chi dung cho lap ke hoach va dieu phoi agent, khong xem la tai lieu ban giao. |
| `archive/` | Tai nguyen tham khao/ban generate cu | Khong dung lam nguon chinh khi cap nhat tai lieu. |

## Tai lieu nen doc truoc

1. `docs/project_delivery_progress_report.md`
2. `docs/ba_system_architecture_consistency_review.md`
3. `docs/reference/screen_gap_analysis.md`
4. `docs/database/database.dbml`
5. `docs/api/api_list.md`

## Quy uoc su dung

- Tai lieu chinh dat trong `docs/`.
- Man hinh thiet ke dat trong `screen-designs/`, khong tron voi tai lieu phan tich.
- File prompt tam thoi dat trong `working-prompts/`.
- Tai nguyen generate hoac tham khao ngoai du an dat trong `archive/`.
- Khi cap nhat tien do, uu tien doi chieu `docs/project_delivery_progress_report.md` voi codegraph cua `danangtrip-web`, `danangtrip-admin` va `danangtrip-api`.
