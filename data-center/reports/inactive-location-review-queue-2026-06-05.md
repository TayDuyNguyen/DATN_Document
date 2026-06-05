# Inactive Location Review Queue - 2026-06-05

## Scope

Reviewed the remaining `112` inactive locations after public location/media cleanup.

Input:

- `D:\DATN\DATN_Tài liệu\data-center\reports\inactive-locations-review-input-2026-06-05.json`
- `D:\DATN\DATN_Tài liệu\data-center\reports\all-location-names-for-duplicate-check-2026-06-05.json`

Output:

- `D:\DATN\DATN_Tài liệu\data-center\reports\inactive-locations-review-2026-06-05.csv`
- `D:\DATN\DATN_Tài liệu\data-center\reports\inactive-locations-review-2026-06-05.json`

## Result

- `manual_lodging_review`: 107
- `duplicate_keep_inactive`: 4
- `hold`: 1
- `activate_candidate`: 0

## Decision

No automatic activation seed was generated.

Reason:

- The only apparent non-lodging candidate, `Memory Lounge` (`id=221`), is a duplicate of active curated row `id=96`.
- Most remaining rows are lodging/hotel/homestay records. These should be manually reviewed before public activation because lodging data needs higher trust: exact name, address, room context, photo fit, and commercial usefulness.
- HanCook rows remain duplicate/manual-review candidates.

## Recommended next action

Use `inactive-locations-review-2026-06-05.csv` in admin/manual review.

Suggested manual buckets:

- Activate only hotels/homestays with strong address, clear brand/name, and acceptable image.
- Keep generic rooms/hostels/nha tro inactive unless needed for demo.
- Keep duplicate rows inactive.

## Current DB impact

No DB mutation was applied in this step.
