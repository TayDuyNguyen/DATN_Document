BEGIN;

INSERT INTO payments (
    booking_id,
    transaction_code,
    amount,
    payment_method,
    payment_status,
    payment_gateway,
    gateway_response,
    paid_at,
    created_at,
    updated_at
)
SELECT
    b.id,
    'BACKFILL-COMPLETED-' || b.id,
    b.final_amount,
    b.payment_method,
    'success',
    CASE
        WHEN upper(b.payment_method) = 'CASH' THEN 'CASH'
        ELSE 'DATA_BACKFILL'
    END,
    '{"source":"completed_booking_integrity_backfill"}'::json,
    COALESCE(b.completed_at, b.booked_at),
    COALESCE(b.completed_at, b.booked_at),
    CURRENT_TIMESTAMP
FROM bookings b
WHERE b.booking_status = 'completed'
  AND b.payment_status = 'pending'
  AND NOT EXISTS (
      SELECT 1
      FROM payments p
      WHERE p.booking_id = b.id
  )
  AND NOT EXISTS (
      SELECT 1
      FROM payments p
      WHERE p.transaction_code = 'BACKFILL-COMPLETED-' || b.id
  );

UPDATE bookings b
SET payment_status = 'success',
    updated_at = CURRENT_TIMESTAMP
WHERE b.booking_status = 'completed'
  AND b.payment_status = 'pending'
  AND EXISTS (
      SELECT 1
      FROM payments p
      WHERE p.booking_id = b.id
        AND p.payment_status = 'success'
  );

COMMIT;
