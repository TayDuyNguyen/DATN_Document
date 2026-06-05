# Inactive Location Activation Batch 1 - 2026-06-04

## Scope

Activated curated non-lodging inactive locations after media completion.

Included categories:

- `am-thuc-dia-phuong`
- `ca-phe-tra-sua`
- `check-in-noi-tieng`
- `bao-tang-di-tich`
- `cong-vien-vuon-hoa`
- `cong-vien-nuoc`
- `hang-dong-nui-non`

Excluded:

- `khach-san-homestay`
- normalized-name duplicate HanCook rows
- rows marked as manual review

## Files

- Quality review CSV:
  - `D:\DATN\DATN_Tài liệu\data-center\reports\inactive-locations-quality-review-2026-06-04.csv`
- Activation batch CSV:
  - `D:\DATN\DATN_Tài liệu\data-center\reports\inactive-locations-activate-batch1-2026-06-04.csv`
- Applied seed:
  - `D:\DATN\DATN_Tài liệu\database-seeders\37_activate_curated_inactive_locations_batch1.sql`
- Duplicate correction seed:
  - `D:\DATN\DATN_Tài liệu\database-seeders\38_deactivate_memory_lounge_crawl_duplicate.sql`

## Result

- Before activation:
  - `locations.active`: 111
  - `locations.inactive`: 222
- Batch 1 activated: 111
- Duplicate correction:
  - moved `id=221`, `slug=memory-lounge`, back to inactive.
  - kept curated `id=96`, `slug=memory-lounge-danang`, active.
- Final:
  - `locations.total`: 333
  - `locations.active`: 221
  - `locations.inactive`: 112
  - `active_missing_thumbnail`: 0
  - `inactive_missing_thumbnail`: 0
  - `active_duplicate_lower_name_groups`: 0
  - `inactive_duplicate_lower_name_groups`: 1

## Remaining review queue

112 inactive locations remain.

Most remaining rows are lodging/homestay/hotel style records or duplicate/manual-review candidates. They should be reviewed visually and commercially before public activation.
