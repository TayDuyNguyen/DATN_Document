# Tour Schedule Operational Backfill - 2026-06-05

## Scope

Normalized all 300 tour schedules.

## Applied seed

- `D:\DATN\DATN_Tài liệu\database-seeders\44_tour_schedule_operational_backfill.sql`

## Backfill rules

- `departure_code`:
  - Format: `DNT-YYYYMMDD-T{tour_id}-S{schedule_id}`
  - Unique per schedule
- `departure_place`:
  - Uses `tours.meeting_point`
  - Falls back to `Trung tam Da Nang`
- `booking_deadline`:
  - Set to 12 hours before the scheduled tour start time
- Past schedules:
  - Keep operational status as `available` because the application only supports `available/cancelled`
  - Set `booking_availability` to `sold_out` so customers cannot book past departures
- Full schedules:
  - Set `booking_availability` to `sold_out`

## Final audit

- `total`: 300
- `missing_departure_code`: 0
- `missing_departure_place`: 0
- `missing_booking_deadline`: 0
- `duplicate_departure_code_groups`: 0
- `past_open_booking`: 0
- `past_sold_out_booking`: 142
- `future_open_booking`: 156
- `deadline_not_before_departure`: 0

Two future schedules remain sold out based on their current capacity state.
