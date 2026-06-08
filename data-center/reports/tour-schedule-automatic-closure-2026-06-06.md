# Tour Schedule Automatic Closure - 2026-06-06

## Implemented

- Command:
  - `php artisan tour-schedules:sync-availability`
- Service:
  - `app/Services/TourScheduleAvailabilityService.php`
- Scheduler:
  - runs every 15 minutes
  - prevents overlapping executions
- Test:
  - `tests/Unit/SyncTourScheduleAvailabilityTest.php`

## Closure rules

An open schedule is changed to `sold_out` when at least one condition is true:

- `start_date` is before the current date.
- `booking_deadline` has passed.
- `booked_people >= max_people`.
- operational status is `cancelled`.

Affected parent tours are synchronized after schedule updates.

## Database result

- First command run closed 41 schedules:
  - 14 schedules had already passed their departure date.
  - the remainder had passed their exact booking deadline or met another closure rule.
- Second command run closed 0 schedules, confirming idempotency.
- Final audit:
  - past open booking: 0
  - open past deadline: 0
  - open full schedules: 0
  - open cancelled schedules: 0
  - future open schedules: 115
  - missing departure metadata/deadline: 0

## Verification

- API tests: 36 passed, 136 assertions.
- PHPStan: no errors.
- Pint: passed.
- Scheduler registration confirmed with `php artisan schedule:list`.

## Production requirement

The server must invoke Laravel's scheduler every minute:

```cron
* * * * * cd /path/to/danangtrip-api && php artisan schedule:run >> /dev/null 2>&1
```

For a long-running worker environment, `php artisan schedule:work` can be managed by Supervisor or the platform process manager instead.
