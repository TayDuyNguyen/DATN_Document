"""
Test script - PAYMENTS (Thanh toan)
Run: python tests/scripts/test_payments.py
Yeu cau: pip install requests
"""

import requests
import time

BASE_URL       = "http://localhost:8000/api/v1"
USER_EMAIL     = "user1@example.com"
USER_PASSWORD  = "password"
ADMIN_EMAIL    = "admin@example.com"
ADMIN_PASSWORD = "password"

USER_TOKEN  = None
ADMIN_TOKEN = None
results     = []
ts = int(time.time())


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
    kwargs.setdefault("timeout", 20)
    try:
        res = getattr(requests, method)(url, **kwargs)
        ok  = res.status_code in expected if isinstance(expected, list) else res.status_code == expected
        label = "\033[92mPASS\033[0m" if ok else "\033[91mFAIL\033[0m"
        print(f"[{label}] {tc} - {desc} | got {res.status_code}, expected {expected}")
        if not ok:
            try:
                body = res.json()
                print(f"  [DEBUG] {body.get('message') or str(body)[:150]}")
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
        if isinstance(data, list):
            return data
        return data.get("data", [])
    except Exception:
        return []


def extract_data(res):
    try:
        d = res.json().get("data", res.json())
        if isinstance(d, dict):
            for key in ["payment"]:
                if d.get(key):
                    return d[key]
            return d
        return {}
    except Exception:
        return {}


def get_booking_id():
    """Lay booking_id co san (pending)."""
    res = requests.get(f"{BASE_URL}/user/bookings",
                       headers=auth(USER_TOKEN),
                       params={"status": "pending", "per_page": 5})
    if res.status_code == 200:
        try:
            items = res.json().get("data", {})
            if isinstance(items, dict):
                items = items.get("data", [])
            if isinstance(items, list) and items:
                return items[0].get("id"), items[0].get("booking_code")
        except Exception:
            pass
    return None, None


def get_payment_id():
    """Lay payment id co san tu admin."""
    res = requests.get(f"{BASE_URL}/admin/payments",
                       headers=auth(ADMIN_TOKEN),
                       params={"per_page": 5})
    if res.status_code == 200:
        items = extract_items(res)
        if items and isinstance(items[0], dict):
            return items[0].get("id"), items[0].get("transaction_code")
    return None, None


def get_success_payment_id():
    """Lay payment id co status=success de test refund."""
    res = requests.get(f"{BASE_URL}/admin/payments",
                       headers=auth(ADMIN_TOKEN),
                       params={"payment_status": "success", "per_page": 5})
    if res.status_code == 200:
        items = extract_items(res)
        if items and isinstance(items[0], dict):
            return items[0].get("id")
    return None


def run_tests():
    global USER_TOKEN, ADMIN_TOKEN

    USER_TOKEN  = login(USER_EMAIL, USER_PASSWORD)
    ADMIN_TOKEN = login(ADMIN_EMAIL, ADMIN_PASSWORD)

    if not USER_TOKEN:
        print("[ABORT] Khong lay duoc USER_TOKEN.")
        return
    if not ADMIN_TOKEN:
        print("[ABORT] Khong lay duoc ADMIN_TOKEN.")
        return

    url = BASE_URL

    booking_id, booking_code = get_booking_id()
    print(f"[SETUP] booking_id={booking_id}, booking_code={booking_code}")

    # ── POST /payments/callback ───────────────────────────────

    res = run("TC01", "POST /payments/callback - webhook mock",
              "post", f"{url}/payments/callback", [200, 422],
              headers=auth(),
              json={"transaction_code": "TEST-001", "status": "success",
                    "amount": 500000})
    if res:
        print(f"  [INFO] TC01: status={res.status_code} (webhook endpoint)")

    run("TC02", "POST /payments/callback - khong can token",
        "post", f"{url}/payments/callback", [200, 422],
        headers=auth(),
        json={"transaction_code": "TEST-002"})

    # ── POST /payments/create ─────────────────────────────────

    if booking_id:
        for tc, method in [("TC03", "momo"), ("TC04", "vnpay"), ("TC05", "zalopay")]:
            res = run(tc, f"POST /payments/create - {method}",
                      "post", f"{url}/payments/create", [200, 201],
                      headers=auth(USER_TOKEN),
                      json={"booking_id": booking_id, "payment_method": method})
            if res and res.status_code in (200, 201):
                data = extract_data(res)
                print(f"  [INFO] {tc}: fields = {list(data.keys())}")
    else:
        for tc in ["TC03", "TC04", "TC05"]:
            print(f"[SKIP] {tc} - khong co booking_id")
            results.append((tc, f"POST /payments/create", None, "skip"))

    run("TC06", "POST /payments/create - thieu booking_id",
        "post", f"{url}/payments/create", 422,
        headers=auth(USER_TOKEN),
        json={"payment_method": "momo"})

    run("TC07", "POST /payments/create - thieu payment_method",
        "post", f"{url}/payments/create", 422,
        headers=auth(USER_TOKEN),
        json={"booking_id": booking_id or 1})

    run("TC08", "POST /payments/create - payment_method sai gia tri",
        "post", f"{url}/payments/create", 422,
        headers=auth(USER_TOKEN),
        json={"booking_id": booking_id or 1, "payment_method": "paypal"})

    run("TC09", "POST /payments/create - booking_id khong ton tai",
        "post", f"{url}/payments/create", [404, 422],
        headers=auth(USER_TOKEN),
        json={"booking_id": 99999, "payment_method": "momo"})

    run("TC10", "POST /payments/create - khong co token",
        "post", f"{url}/payments/create", 401,
        headers=auth(),
        json={"booking_id": booking_id or 1, "payment_method": "momo"})

    # ── GET /payments/status/{transaction_code} ───────────────

    payment_id, transaction_code = get_payment_id()
    print(f"[SETUP] payment_id={payment_id}, transaction_code={transaction_code}")

    if transaction_code:
        res = run("TC11", f"GET /payments/status/{transaction_code} - kiem tra trang thai",
                  "get", f"{url}/payments/status/{transaction_code}", 200,
                  headers=auth(USER_TOKEN))
        if res and res.status_code == 200:
            data = extract_data(res)
            print(f"  [INFO] TC11: fields = {list(data.keys())}")
    else:
        print("[SKIP] TC11 - khong co transaction_code")
        results.append(("TC11", "GET /payments/status/{code}", None, "skip"))

    run("TC12", "GET /payments/status/INVALID-TXN-XYZ - khong ton tai",
        "get", f"{url}/payments/status/INVALID-TXN-XYZ", [404, 422],
        headers=auth(USER_TOKEN))

    run("TC13", f"GET /payments/status/{transaction_code or 'TEST'} - khong co token",
        "get", f"{url}/payments/status/{transaction_code or 'TEST'}", 401,
        headers=auth())

    # ── POST /payments/retry/{booking_code} ──────────────────

    if booking_code:
        res = run("TC14", f"POST /payments/retry/{booking_code} - retry thanh cong",
                  "post", f"{url}/payments/retry/{booking_code}", [200, 201],
                  headers=auth(USER_TOKEN))
        if res and res.status_code in (200, 201):
            data = extract_data(res)
            print(f"  [INFO] TC14: fields = {list(data.keys())}")
    else:
        print("[SKIP] TC14 - khong co booking_code")
        results.append(("TC14", "POST /payments/retry/{code}", None, "skip"))

    run("TC15", "POST /payments/retry/INVALID-CODE-XYZ - khong ton tai",
        "post", f"{url}/payments/retry/INVALID-CODE-XYZ", [404, 422],
        headers=auth(USER_TOKEN))

    run("TC16", "POST /payments/retry/{code} - booking da thanh toan",
        "post", f"{url}/payments/retry/{booking_code or 'TEST'}", [400, 422],
        headers=auth(USER_TOKEN))

    run("TC17", f"POST /payments/retry/{booking_code or 'TEST'} - khong co token",
        "post", f"{url}/payments/retry/{booking_code or 'TEST'}", 401,
        headers=auth())

    # ── GET /admin/payments ───────────────────────────────────

    res = run("TC18", "GET /admin/payments - lay tat ca",
              "get", f"{url}/admin/payments", 200,
              headers=auth(ADMIN_TOKEN))
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC18: {len(items)} payments")
        if items and isinstance(items[0], dict):
            print(f"  [INFO] TC18: fields = {list(items[0].keys())}")

    for tc, sv in [("TC19", "pending"), ("TC20", "success"),
                   ("TC21", "failed"),  ("TC22", "refunded")]:
        run(tc, f"GET /admin/payments - filter payment_status={sv}",
            "get", f"{url}/admin/payments", 200,
            headers=auth(ADMIN_TOKEN), params={"payment_status": sv})

    for tc, gw in [("TC23", "momo")]:
        run(tc, f"GET /admin/payments - filter payment_gateway={gw}",
            "get", f"{url}/admin/payments", 200,
            headers=auth(ADMIN_TOKEN), params={"payment_gateway": gw})

    run("TC24", "GET /admin/payments - filter date_from/date_to",
        "get", f"{url}/admin/payments", 200,
        headers=auth(ADMIN_TOKEN),
        params={"date_from": "2026-01-01", "date_to": "2026-12-31"})

    res = run("TC25", "GET /admin/payments - phan trang per_page=5",
              "get", f"{url}/admin/payments", 200,
              headers=auth(ADMIN_TOKEN), params={"page": 1, "per_page": 5})
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC25: {len(items)} items {'OK' if len(items) <= 5 else 'WARN > 5'}")

    run("TC26", "GET /admin/payments - payment_status sai gia tri",
        "get", f"{url}/admin/payments", 422,
        headers=auth(ADMIN_TOKEN), params={"payment_status": "invalid"})

    run("TC27", "GET /admin/payments - date_from sai dinh dang",
        "get", f"{url}/admin/payments", [200, 422],
        headers=auth(ADMIN_TOKEN), params={"date_from": "01-01-2026"})

    run("TC28", "GET /admin/payments - user thuong bi 403",
        "get", f"{url}/admin/payments", 403,
        headers=auth(USER_TOKEN))

    run("TC29", "GET /admin/payments - khong co token",
        "get", f"{url}/admin/payments", 401,
        headers=auth())

    # ── GET /admin/payments/{id} ──────────────────────────────

    if payment_id:
        res = run("TC30", f"GET /admin/payments/{payment_id} - chi tiet",
                  "get", f"{url}/admin/payments/{payment_id}", 200,
                  headers=auth(ADMIN_TOKEN))
        if res and res.status_code == 200:
            data = extract_data(res)
            print(f"  [INFO] TC30: fields = {list(data.keys())}")
    else:
        print("[SKIP] TC30 - khong co payment_id")
        results.append(("TC30", "GET /admin/payments/{id}", None, "skip"))

    run("TC31", "GET /admin/payments/99999 - ID khong ton tai",
        "get", f"{url}/admin/payments/99999", [404, 422],
        headers=auth(ADMIN_TOKEN))

    run("TC32", f"GET /admin/payments/{payment_id or 1} - user thuong bi 403",
        "get", f"{url}/admin/payments/{payment_id or 1}", 403,
        headers=auth(USER_TOKEN))

    run("TC33", f"GET /admin/payments/{payment_id or 1} - khong co token",
        "get", f"{url}/admin/payments/{payment_id or 1}", 401,
        headers=auth())

    # ── POST /admin/payments/{id}/refund ─────────────────────

    success_pid = get_success_payment_id()
    print(f"[SETUP] success_payment_id={success_pid}")

    if success_pid:
        res = run("TC34", f"POST /admin/payments/{success_pid}/refund - hoan tien",
                  "post", f"{url}/admin/payments/{success_pid}/refund", 200,
                  headers=auth(ADMIN_TOKEN),
                  json={"refund_reason": "Khach hang yeu cau hoan tien"})
        if res and res.status_code == 200:
            data = extract_data(res)
            if data.get("payment_status") == "refunded":
                print(f"  [INFO] TC34: payment_status=refunded - OK")
    else:
        print("[SKIP] TC34 - khong co payment success de refund")
        results.append(("TC34", "POST /admin/payments/{id}/refund", None, "skip"))

    run("TC35", f"POST /admin/payments/{payment_id or 1}/refund - thieu refund_reason",
        "post", f"{url}/admin/payments/{payment_id or 1}/refund", 422,
        headers=auth(ADMIN_TOKEN),
        json={})

    # TC36: refund giao dich chua success (dung payment_id pending)
    if payment_id:
        run("TC36", f"POST /admin/payments/{payment_id}/refund - chua success",
            "post", f"{url}/admin/payments/{payment_id}/refund", [400, 422],
            headers=auth(ADMIN_TOKEN),
            json={"refund_reason": "Test"})
    else:
        print("[SKIP] TC36 - khong co payment_id")
        results.append(("TC36", "refund chua success", None, "skip"))

    run("TC37", "POST /admin/payments/99999/refund - ID khong ton tai",
        "post", f"{url}/admin/payments/99999/refund", [404, 422],
        headers=auth(ADMIN_TOKEN),
        json={"refund_reason": "Test"})

    run("TC38", f"POST /admin/payments/{payment_id or 1}/refund - user thuong bi 403",
        "post", f"{url}/admin/payments/{payment_id or 1}/refund", 403,
        headers=auth(USER_TOKEN),
        json={"refund_reason": "Test"})

    run("TC39", f"POST /admin/payments/{payment_id or 1}/refund - khong co token",
        "post", f"{url}/admin/payments/{payment_id or 1}/refund", 401,
        headers=auth(),
        json={"refund_reason": "Test"})

    # ── GET /admin/payments/export ────────────────────────────

    res = run("TC40", "GET /admin/payments/export - export thanh cong",
              "get", f"{url}/admin/payments/export", 200,
              headers=auth(ADMIN_TOKEN), timeout=30)
    if res and res.status_code == 200:
        ct = res.headers.get("Content-Type", "")
        print(f"  [INFO] TC40: Content-Type={ct}")

    run("TC41", "GET /admin/payments/export - voi filter",
        "get", f"{url}/admin/payments/export", 200,
        headers=auth(ADMIN_TOKEN),
        params={"payment_status": "pending"}, timeout=30)

    run("TC42", "GET /admin/payments/export - user thuong bi 403",
        "get", f"{url}/admin/payments/export", 403,
        headers=auth(USER_TOKEN))

    run("TC43", "GET /admin/payments/export - khong co token",
        "get", f"{url}/admin/payments/export", 401,
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
