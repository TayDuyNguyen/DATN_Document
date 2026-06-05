# Booking Payment Integrity Backfill - 2026-06-05

## Initial audit

- Bookings without payment records: 34
- Valid cancelled/unpaid bookings: 11
- Pending bookings without payment attempts: 14
- Invalid completed/pending bookings without payment history: 9

## Applied

- Backup:
  - `D:\DATN\DATN_Tài liệu\data-center\backups\booking-payment-backfill-20260605-145913.json`
- Seed:
  - `D:\DATN\DATN_Tài liệu\database-seeders\46_completed_booking_payment_backfill.sql`
- Audit:
  - `D:\DATN\DATN_Tài liệu\database-seeders\audit_booking_payment_integrity.php`

The backfill created one successful payment per affected completed booking and synchronized the booking payment status to `success`.

## Final audit

- Bookings: 105
- Payments: 83
- Booking payment status:
  - success: 69
  - refunded: 9
  - pending: 16
  - unpaid: 11
- Bookings without payment records: 25
  - cancelled/unpaid: 11
  - pending without payment attempt: 14
- Success booking without success payment: 0
- Refunded booking without refunded payment: 0
- Payment amount mismatch: 0
- Successful payment without `paid_at`: 0
- Refunded payment without `refunded_at`: 0

## API fix

Completed on 2026-06-05:

- `BookingService::completeBooking()` now locks the booking row.
- Reuses an existing successful payment when present.
- Creates an admin successful payment history when none exists.
- Updates the booking and payment history in one transaction.
- Rolls back if the booking status cannot be persisted.
- Added `tests/Unit/BookingServiceTest.php`.

Verification:

- API tests: 37 passed, 140 assertions.
- PHPStan: no errors.
- Pint: passed.
