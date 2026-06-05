# Crawl Pending Review Audit - 2026-06-05

## Input

- `D:\DATN\DATN_Tài liệu\data-center\reports\crawl-items-pending-review-input-2026-06-05.json`
- `D:\DATN\DATN_Tài liệu\data-center\reports\crawl-items-pending-review-2026-06-05.csv`
- `D:\DATN\DATN_Tài liệu\data-center\reports\crawl-items-pending-review-2026-06-05.json`

## Initial classification

- `manual_review`: 258
- `duplicate_reject_or_link`: 102

Reason counters:

- `missing_image_candidate`: 360
- `weak_address`: 309
- `duplicate_match`: 102
- `lodging_manual_review`: 73

Entity distribution:

- `location/manual_review`: 134
- `restaurant/manual_review`: 89
- `hotel/manual_review`: 35
- `restaurant/duplicate_reject_or_link`: 52
- `hotel/duplicate_reject_or_link`: 37
- `location/duplicate_reject_or_link`: 13

## Applied cleanup

Applied seed:

- `D:\DATN\DATN_Tài liệu\database-seeders\42_reject_duplicate_pending_crawl_items.sql`

Purpose:

- Move pending rows with `duplicate_source_id IS NOT NULL` to `rejected`.
- Preserve data; no rows are deleted.
- Do not publish anything automatically.

## Final state

- `crawl_items`: 942
- `crawl_pending_review`: 258
- `crawl_published`: 222
- `crawl_rejected`: 462

## Decision

No automatic publish seed was generated.

Reason:

- Remaining 258 pending items all lack image candidates.
- Most also have weak address signals.
- These should be manually reviewed or re-enriched before publishing.

## Recommended next action

If the project needs more public locations:

1. Re-enrich the remaining 258 pending rows with better image/source data.
2. Prioritize non-lodging categories:
   - `check-in-noi-tieng`
   - `ca-phe-tra-sua`
   - `am-thuc-dia-phuong`
   - `cong-vien-vuon-hoa`
   - `bao-tang-di-tich`
3. Keep lodging/hotel rows manual-review only.
