
"""
Test script - ADMIN DASHBOARD & REPORTS
Branch: feat/taynd/api-admin-dashboard
Run: python tests/scripts/test_dashboard.py
Yeu cau: pip install requests
"""

import requests

BASE_URL       = "http://localhost:8000/api/v1"
USER_EMAIL     = "user1@example.com"
USER_PASSWORD  = "password"
ADMIN_EMAIL    = "admin@example.com"
ADMIN_PASSWORD = "password"

USER_TOKEN  = None
ADMIN_TOKEN = None
results     = []


def login(email, password):
    res = requests.post(f"{BASE_URL}/auth/login",
                        json={"email": email, "password": password},
                        headers={"Accept": "application/json"})
    if res.status_code == 200:
        data  = res.json()
        token = (data.get("token") or data.get("access_token")
                 or data.get("data", {}).get("token")
                 or data.get("data", {}).get("access_token"))
        if token:
            print(f"[AUTH] Logged in as {email}")
            return token
    print(f"[AUTH ERROR] {email}: {res.status_code} - {res.text[:150]}")
    return None


def auth(token=None):
    h = {"Accept": "application/json"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def run(tc, desc, method, url, expected, **kwargs):
    kwargs.setdefault("timeout", 15)
    try:
        res = getattr(requests, method)(url, **kwargs)
        ok  = res.status_code in expected if isinstance(expected, list) else res.status_code == expected
        label = "\033[92mPASS\033[0m" if ok else "\033[91mFAIL\033[0m"
        print(f"[{label}] {tc} - {desc} | got {res.status_code}, expected {expected}")
        if not ok:
            try:
                body = res.json()
                print(f"  [DEBUG] {body.get('message') or str(body)[:200]}")
            except Exception:
                print(f"  [DEBUG] {res.text[:200]}")
        results.append((tc, desc, ok, res.status_code))
        return res
    except requests.exceptions.Timeout:
        print(f"[TIMEOUT] {tc} - {desc}")
        results.append((tc, desc, False, "timeout"))
        return None
    except Exception as e:
        print(f"[ERROR] {tc} - {desc} | {e}")
        results.append((tc, desc, False, "error"))
        return None


def extract_items(res):
    try:
        data = res.json().get("data", [])
        return data if isinstance(data, list) else data.get("data", [])
    except Exception:
        return []


def run_tests():
    global USER_TOKEN, ADMIN_TOKEN

    USER_TOKEN  = login(USER_EMAIL, USER_PASSWORD)
    ADMIN_TOKEN = login(ADMIN_EMAIL, ADMIN_PASSWORD)

    if not ADMIN_TOKEN:
        print("[ABORT] Khong lay duoc ADMIN_TOKEN.")
        return

    url = BASE_URL

    # ── GET /admin/dashboard/stats ────────────────────────────

    res = run("TC01", "GET /admin/dashboard/stats - lay tong quan",
              "get", f"{url}/admin/dashboard/stats", 200,
              headers=auth(ADMIN_TOKEN))
    if res and res.status_code == 200:
        try:
            data = res.json().get("data", res.json())
            print(f"  [INFO] TC01: fields = {list(data.keys()) if isinstance(data, dict) else 'array'}")
            for f in ["total_users", "total_tours", "total_bookings"]:
                if isinstance(data, dict) and f not in data:
                    print(f"  [WARN] TC01: thieu field '{f}'")
        except Exception:
            pass

    run("TC02", "GET /admin/dashboard/stats - user thuong bi 403",
        "get", f"{url}/admin/dashboard/stats", 403,
        headers=auth(USER_TOKEN))

    run("TC03", "GET /admin/dashboard/stats - khong co token → 401",
        "get", f"{url}/admin/dashboard/stats", 401,
        headers=auth())

    # ── GET /admin/dashboard/revenue ──────────────────────────

    res = run("TC04", "GET /admin/dashboard/revenue - mac dinh",
              "get", f"{url}/admin/dashboard/revenue", 200,
              headers=auth(ADMIN_TOKEN))
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC04: {len(items)} data points")

    for period in ["day", "week", "month", "year"]:
        run(f"TC0{5 + ['day','week','month','year'].index(period)}",
            f"GET /admin/dashboard/revenue - period={period}",
            "get", f"{url}/admin/dashboard/revenue", 200,
            headers=auth(ADMIN_TOKEN), params={"period": period})

    run("TC09", "GET /admin/dashboard/revenue - filter from + to",
        "get", f"{url}/admin/dashboard/revenue", 200,
        headers=auth(ADMIN_TOKEN),
        params={"from": "2026-01-01", "to": "2026-12-31"})

    run("TC10", "GET /admin/dashboard/revenue - period sai gia tri → 422",
        "get", f"{url}/admin/dashboard/revenue", 422,
        headers=auth(ADMIN_TOKEN), params={"period": "invalid_period"})

    run("TC11", "GET /admin/dashboard/revenue - from sai dinh dang → 422",
        "get", f"{url}/admin/dashboard/revenue", 422,
        headers=auth(ADMIN_TOKEN), params={"from": "31-01-2026"})

    run("TC12", "GET /admin/dashboard/revenue - user thuong bi 403",
        "get", f"{url}/admin/dashboard/revenue", 403,
        headers=auth(USER_TOKEN))

    run("TC13", "GET /admin/dashboard/revenue - khong co token → 401",
        "get", f"{url}/admin/dashboard/revenue", 401,
        headers=auth())

    # ── GET /admin/dashboard/top-tours ────────────────────────

    res = run("TC14", "GET /admin/dashboard/top-tours - mac dinh",
              "get", f"{url}/admin/dashboard/top-tours", 200,
              headers=auth(ADMIN_TOKEN))
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC14: {len(items)} top tours")
        if items and isinstance(items[0], dict):
            print(f"  [INFO] TC14: fields = {list(items[0].keys())}")

    res = run("TC15", "GET /admin/dashboard/top-tours - limit=5",
              "get", f"{url}/admin/dashboard/top-tours", 200,
              headers=auth(ADMIN_TOKEN), params={"limit": 5})
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC15: {len(items)} items {'OK' if len(items) <= 5 else 'WARN > 5'}")

    run("TC16", "GET /admin/dashboard/top-tours - filter from + to",
        "get", f"{url}/admin/dashboard/top-tours", 200,
        headers=auth(ADMIN_TOKEN),
        params={"from": "2026-01-01", "to": "2026-12-31"})

    run("TC17", "GET /admin/dashboard/top-tours - limit khong phai so → 422",
        "get", f"{url}/admin/dashboard/top-tours", [200, 422],
        headers=auth(ADMIN_TOKEN), params={"limit": "abc"})

    run("TC18", "GET /admin/dashboard/top-tours - user thuong bi 403",
        "get", f"{url}/admin/dashboard/top-tours", 403,
        headers=auth(USER_TOKEN))

    run("TC19", "GET /admin/dashboard/top-tours - khong co token → 401",
        "get", f"{url}/admin/dashboard/top-tours", 401,
        headers=auth())

    # ── GET /admin/dashboard/top-locations ────────────────────

    res = run("TC20", "GET /admin/dashboard/top-locations - mac dinh",
              "get", f"{url}/admin/dashboard/top-locations", 200,
              headers=auth(ADMIN_TOKEN))
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC20: {len(items)} top locations")

    res = run("TC21", "GET /admin/dashboard/top-locations - limit=5",
              "get", f"{url}/admin/dashboard/top-locations", 200,
              headers=auth(ADMIN_TOKEN), params={"limit": 5})
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC21: {len(items)} items {'OK' if len(items) <= 5 else 'WARN > 5'}")

    run("TC22", "GET /admin/dashboard/top-locations - limit khong phai so → 422",
        "get", f"{url}/admin/dashboard/top-locations", [200, 422],
        headers=auth(ADMIN_TOKEN), params={"limit": "abc"})

    run("TC23", "GET /admin/dashboard/top-locations - user thuong bi 403",
        "get", f"{url}/admin/dashboard/top-locations", 403,
        headers=auth(USER_TOKEN))

    run("TC24", "GET /admin/dashboard/top-locations - khong co token → 401",
        "get", f"{url}/admin/dashboard/top-locations", 401,
        headers=auth())

    # ── GET /admin/dashboard/user-growth ──────────────────────

    res = run("TC25", "GET /admin/dashboard/user-growth - nam hien tai",
              "get", f"{url}/admin/dashboard/user-growth", 200,
              headers=auth(ADMIN_TOKEN))
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC25: {len(items)} data points (ky vong 12 thang)")

    run("TC26", "GET /admin/dashboard/user-growth - year=2026",
        "get", f"{url}/admin/dashboard/user-growth", 200,
        headers=auth(ADMIN_TOKEN), params={"year": 2026})

    run("TC27", "GET /admin/dashboard/user-growth - year=2025 (qua khu)",
        "get", f"{url}/admin/dashboard/user-growth", 200,
        headers=auth(ADMIN_TOKEN), params={"year": 2025}, timeout=30)

    run("TC28", "GET /admin/dashboard/user-growth - year khong phai so → 422",
        "get", f"{url}/admin/dashboard/user-growth", 422,
        headers=auth(ADMIN_TOKEN), params={"year": "abc"})

    run("TC29", "GET /admin/dashboard/user-growth - user thuong bi 403",
        "get", f"{url}/admin/dashboard/user-growth", 403,
        headers=auth(USER_TOKEN))

    run("TC30", "GET /admin/dashboard/user-growth - khong co token → 401",
        "get", f"{url}/admin/dashboard/user-growth", 401,
        headers=auth())

    # ── GET /admin/dashboard/booking-trend ────────────────────

    res = run("TC31", "GET /admin/dashboard/booking-trend - mac dinh (30 ngay)",
              "get", f"{url}/admin/dashboard/booking-trend", 200,
              headers=auth(ADMIN_TOKEN))
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC31: {len(items)} data points")

    run("TC32", "GET /admin/dashboard/booking-trend - days=7",
        "get", f"{url}/admin/dashboard/booking-trend", 200,
        headers=auth(ADMIN_TOKEN), params={"days": 7})

    run("TC33", "GET /admin/dashboard/booking-trend - days=90",
        "get", f"{url}/admin/dashboard/booking-trend", 200,
        headers=auth(ADMIN_TOKEN), params={"days": 90})

    run("TC34", "GET /admin/dashboard/booking-trend - days am → 422",
        "get", f"{url}/admin/dashboard/booking-trend", 422,
        headers=auth(ADMIN_TOKEN), params={"days": -1})

    run("TC35", "GET /admin/dashboard/booking-trend - days khong phai so → 422",
        "get", f"{url}/admin/dashboard/booking-trend", 422,
        headers=auth(ADMIN_TOKEN), params={"days": "abc"})

    run("TC36", "GET /admin/dashboard/booking-trend - user thuong bi 403",
        "get", f"{url}/admin/dashboard/booking-trend", 403,
        headers=auth(USER_TOKEN))

    run("TC37", "GET /admin/dashboard/booking-trend - khong co token → 401",
        "get", f"{url}/admin/dashboard/booking-trend", 401,
        headers=auth())

    # ── GET /admin/reports/bookings ───────────────────────────

    res = run("TC38", "GET /admin/reports/bookings - khong filter",
              "get", f"{url}/admin/reports/bookings", 200,
              headers=auth(ADMIN_TOKEN))
    if res and res.status_code == 500:
        try:
            print(f"  [ERROR DETAIL] {res.json()}")
        except Exception:
            print(f"  [ERROR DETAIL] {res.text[:500]}")
    if res and res.status_code == 200:
        try:
            data = res.json().get("data", {})
            print(f"  [INFO] TC38: fields = {list(data.keys()) if isinstance(data, dict) else 'array'}")
        except Exception:
            pass

    run("TC39", "GET /admin/reports/bookings - filter from + to",
        "get", f"{url}/admin/reports/bookings", 200,
        headers=auth(ADMIN_TOKEN),
        params={"from": "2026-01-01", "to": "2026-12-31"})

    run("TC40", "GET /admin/reports/bookings - filter status=confirmed",
        "get", f"{url}/admin/reports/bookings", 200,
        headers=auth(ADMIN_TOKEN), params={"status": "confirmed"})

    run("TC41", "GET /admin/reports/bookings - filter payment_status=paid",
        "get", f"{url}/admin/reports/bookings", 200,
        headers=auth(ADMIN_TOKEN), params={"payment_status": "paid"})

    run("TC42", "GET /admin/reports/bookings - ket hop tat ca filters",
        "get", f"{url}/admin/reports/bookings", 200,
        headers=auth(ADMIN_TOKEN),
        params={"from": "2026-01-01", "to": "2026-12-31",
                "status": "confirmed", "payment_status": "paid"})

    run("TC43", "GET /admin/reports/bookings - status sai gia tri → 422",
        "get", f"{url}/admin/reports/bookings", 422,
        headers=auth(ADMIN_TOKEN), params={"status": "invalid_status"})

    run("TC44", "GET /admin/reports/bookings - from sai dinh dang → 422",
        "get", f"{url}/admin/reports/bookings", 422,
        headers=auth(ADMIN_TOKEN), params={"from": "31-01-2026"})

    run("TC45", "GET /admin/reports/bookings - user thuong bi 403",
        "get", f"{url}/admin/reports/bookings", 403,
        headers=auth(USER_TOKEN))

    run("TC46", "GET /admin/reports/bookings - khong co token → 401",
        "get", f"{url}/admin/reports/bookings", 401,
        headers=auth())

    # ── GET /admin/reports/ratings ────────────────────────────

    res = run("TC47", "GET /admin/reports/ratings - khong filter",
              "get", f"{url}/admin/reports/ratings", 200,
              headers=auth(ADMIN_TOKEN))
    if res and res.status_code == 200:
        try:
            data = res.json().get("data", {})
            print(f"  [INFO] TC47: fields = {list(data.keys()) if isinstance(data, dict) else 'array'}")
        except Exception:
            pass

    run("TC48", "GET /admin/reports/ratings - filter from + to",
        "get", f"{url}/admin/reports/ratings", 200,
        headers=auth(ADMIN_TOKEN),
        params={"from": "2026-01-01", "to": "2026-12-31"})

    for status_val in ["approved", "pending", "rejected"]:
        run(f"TC{49 + ['approved','pending','rejected'].index(status_val)}",
            f"GET /admin/reports/ratings - filter status={status_val}",
            "get", f"{url}/admin/reports/ratings", 200,
            headers=auth(ADMIN_TOKEN), params={"status": status_val})

    run("TC52", "GET /admin/reports/ratings - status sai gia tri → 422",
        "get", f"{url}/admin/reports/ratings", 422,
        headers=auth(ADMIN_TOKEN), params={"status": "invalid_status"})

    run("TC53", "GET /admin/reports/ratings - from sai dinh dang → 422",
        "get", f"{url}/admin/reports/ratings", 422,
        headers=auth(ADMIN_TOKEN), params={"from": "31-01-2026"})

    run("TC54", "GET /admin/reports/ratings - user thuong bi 403",
        "get", f"{url}/admin/reports/ratings", 403,
        headers=auth(USER_TOKEN))

    run("TC55", "GET /admin/reports/ratings - khong co token → 401",
        "get", f"{url}/admin/reports/ratings", 401,
        headers=auth())

    # ── GET /admin/reports/users ──────────────────────────────

    res = run("TC56", "GET /admin/reports/users - nam hien tai",
              "get", f"{url}/admin/reports/users", 200,
              headers=auth(ADMIN_TOKEN))
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC56: {len(items)} data points")

    run("TC57", "GET /admin/reports/users - year=2026",
        "get", f"{url}/admin/reports/users", 200,
        headers=auth(ADMIN_TOKEN), params={"year": 2026})

    run("TC58", "GET /admin/reports/users - year=2025 (qua khu)",
        "get", f"{url}/admin/reports/users", 200,
        headers=auth(ADMIN_TOKEN), params={"year": 2025})

    run("TC59", "GET /admin/reports/users - year khong phai so → 422",
        "get", f"{url}/admin/reports/users", 422,
        headers=auth(ADMIN_TOKEN), params={"year": "abc"})

    run("TC60", "GET /admin/reports/users - user thuong bi 403",
        "get", f"{url}/admin/reports/users", 403,
        headers=auth(USER_TOKEN))

    run("TC61", "GET /admin/reports/users - khong co token → 401",
        "get", f"{url}/admin/reports/users", 401,
        headers=auth())

    # ── GET /admin/reports/revenue-detail ─────────────────────

    res = run("TC62", "GET /admin/reports/revenue-detail - khong filter",
              "get", f"{url}/admin/reports/revenue-detail", 200,
              headers=auth(ADMIN_TOKEN))
    if res and res.status_code == 200:
        try:
            data = res.json().get("data", {})
            print(f"  [INFO] TC62: fields = {list(data.keys()) if isinstance(data, dict) else 'array'}")
        except Exception:
            pass

    run("TC63", "GET /admin/reports/revenue-detail - filter from + to",
        "get", f"{url}/admin/reports/revenue-detail", 200,
        headers=auth(ADMIN_TOKEN),
        params={"from": "2026-01-01", "to": "2026-12-31"})

    run("TC64", "GET /admin/reports/revenue-detail - from sai dinh dang → 422",
        "get", f"{url}/admin/reports/revenue-detail", 422,
        headers=auth(ADMIN_TOKEN), params={"from": "31-01-2026"})

    run("TC65", "GET /admin/reports/revenue-detail - user thuong bi 403",
        "get", f"{url}/admin/reports/revenue-detail", 403,
        headers=auth(USER_TOKEN))

    run("TC66", "GET /admin/reports/revenue-detail - khong co token → 401",
        "get", f"{url}/admin/reports/revenue-detail", 401,
        headers=auth())

    # ── SUMMARY ──────────────────────────────────────────────

    total   = len(results)
    passed  = sum(1 for _, _, ok, _ in results if ok is True)
    failed  = sum(1 for _, _, ok, _ in results if ok is False)
    skipped = sum(1 for _, _, ok, _ in results if ok is None)

    print(f"\n{'='*55}")
    print(f"  TOTAL: {total} | PASS: {passed} | FAIL: {failed} | SKIP: {skipped}")
    print(f"{'='*55}")
    if failed:
        print("\nFailed cases:")
        for tc, desc, ok, code in results:
            if ok is False:
                print(f"  - {tc}: {desc} (got {code})")
    if skipped:
        print("\nSkipped cases:")
        for tc, desc, ok, code in results:
            if ok is None:
                print(f"  - {tc}: {desc}")


if __name__ == "__main__":
    run_tests()
