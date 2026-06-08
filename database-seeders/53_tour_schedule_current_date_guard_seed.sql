-- DanangTrip tour schedule current-date guard
-- Purpose:
--   Keep seeded tour schedules correct when the database is rebuilt on a later day.
--   Any schedule that has departed, passed its booking deadline, is full, or is cancelled
--   must not remain open for booking.

BEGIN;

UPDATE tour_schedules
SET
    booking_availability = 'sold_out',
    updated_at = NOW()
WHERE booking_availability = 'open'
  AND (
      start_date < CURRENT_DATE
      OR booking_deadline <= NOW()
      OR booked_people >= max_people
      OR status = 'cancelled'
  );

UPDATE tours t
SET
    booking_availability = CASE
        WHEN EXISTS (
            SELECT 1
            FROM tour_schedules ts
            WHERE ts.tour_id = t.id
              AND ts.status = 'available'
              AND ts.booking_availability = 'open'
              AND ts.start_date >= CURRENT_DATE
        )
        THEN 'open'
        ELSE 'sold_out'
    END,
    updated_at = NOW()
WHERE t.status = 'active'
  AND EXISTS (
      SELECT 1
      FROM tour_schedules ts
      WHERE ts.tour_id = t.id
  );

COMMIT;
