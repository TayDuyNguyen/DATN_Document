-- DanangTrip tour schedule operational backfill
-- FILE: 44_tour_schedule_operational_backfill.sql
-- Purpose:
--   Add stable departure metadata and booking deadlines to all schedules.
--   Close booking for past schedules without incorrectly marking them cancelled.

UPDATE tour_schedules ts
SET departure_code = COALESCE(
        NULLIF(ts.departure_code, ''),
        'DNT-' || TO_CHAR(ts.start_date, 'YYYYMMDD') || '-T' || ts.tour_id || '-S' || ts.id
    ),
    departure_place = COALESCE(
        NULLIF(ts.departure_place, ''),
        NULLIF(t.meeting_point, ''),
        'Trung tam Da Nang'
    ),
    booking_deadline = COALESCE(
        ts.booking_deadline,
        (
            ts.start_date::text || ' ' || COALESCE(NULLIF(t.start_time, ''), '07:30')
        )::timestamp - INTERVAL '12 hours'
    ),
    booking_availability = CASE
        WHEN ts.start_date < CURRENT_DATE THEN 'sold_out'
        WHEN ts.booked_people >= ts.max_people THEN 'sold_out'
        ELSE ts.booking_availability
    END,
    updated_at = NOW()
FROM tours t
WHERE t.id = ts.tour_id;
