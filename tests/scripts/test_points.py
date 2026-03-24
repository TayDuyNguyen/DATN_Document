"""
Test script - POINTS (Diem thuong)
Run: python tests/scripts/test_points.py
Yeu cau: pip install requests
"""

import requests

BASE_URL      = "http://localhost:8000/api/v1"
USER_EMAIL    = "user1@example.com"
USER_PASSWORD = "password"

USER_TOKEN = None
results    = []


# ── Helpers ───────────────────────────────────────────────────────────────────

def login(email, password):
    res = requests.post(f"{BASE_URL}/auth/login",
                        json={"email": email, "password": password},
                        headers={"Accept": "application/json"})
    if res.status_code == 200:
        data  = res.json()
        token = (data.get("token")
                 or data.get("access_token")
                 or data.get("data", {}).get("token")
                 or data.get("data", {}).get("access_token"))
        if token:
            print(f"[AUTH] Logged in as {email}")
            return token
    print(f"[AUTH ERROR] {email}: {res.status_code} - {res.text[:200]}")
    return None


def auth(token=None):
    h = {"Accept": "application/json"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def run(tc, desc, method, url, expected, **kwargs):
    try:
        res   = getattr(requests, method)(url, **kwargs)
        ok    = res.status_code in expected if isinstance(expected, list) else res.status_code == expected
        label = "\033[92mPASS\033[0m" if ok else "\033[91mFAIL\033[0m"
        print(f"[{label}] {tc} - {desc} | got {res.status_code}, expected {expected}")
        results.append((tc, desc, ok, res.status_code))
        return res
    except Exception as e:
        print(f"[ERROR] {tc} - {desc} | {e}")
        results.append((tc, desc, False, "error"))
        return None


def get_point_balance(token):
    """Lấy point_balance hiện tại của user."""
    res = requests.get(f"{BASE_URL}/user/points", headers=auth(token))
    if res.status_code == 200:
        try:
            data = res.json().get("data", res.json())
            if isinstance(data, dict):
                return data.get("point_balance") or data.get("balance") or data.get("points")
        except Exception:
            pass
    return None


def extract_items(res):
    """Trích xuất list items từ paginated response."""
    try:
        data  = res.json().get("data", [])
        return data if isinstance(data, list) else data.get("data", [])
    except Exception:
        return []


# ── Main ──────────────────────────────────────────────────────────────────────

def run_tests():
    global USER_TOKEN

    USER_TOKEN = login(USER_EMAIL, USER_PASSWORD)
    if not USER_TOKEN:
        print("[ABORT] Khong lay duoc USER_TOKEN.")
        return

    url = BASE_URL

    # ── GET /user/points ──────────────────────────────────────

    res = run("TC01", "GET /user/points - lay so du",
              "get", f"{url}/user/points", 200,
              headers=auth(USER_TOKEN))
    balance_tc01 = None
    if res and res.status_code == 200:
        try:
            data = res.json().get("data", res.json())
            print(f"  [INFO] TC01: response = {data}")
            balance_tc01 = (data.get("point_balance")
                            or data.get("balance")
                            or data.get("points")) if isinstance(data, dict) else None
            if balance_tc01 is not None:
                print(f"  [INFO] TC01: point_balance = {balance_tc01}")
            else:
                print(f"  [WARN] TC01: khong tim thay field point_balance/balance/points")
        except Exception:
            pass

    # TC02: verify khớp với /user/profile
    res_profile = requests.get(f"{url}/user/profile", headers=auth(USER_TOKEN))
    if res_profile.status_code == 200 and balance_tc01 is not None:
        try:
            profile_data    = res_profile.json().get("data", res_profile.json())
            profile_balance = profile_data.get("point_balance") if isinstance(profile_data, dict) else None
            if profile_balance is not None:
                match = (balance_tc01 == profile_balance)
                ok    = match
                label = "\033[92mPASS\033[0m" if ok else "\033[91mFAIL\033[0m"
                print(f"[{label}] TC02 - GET /user/points - verify khop profile | "
                      f"points={balance_tc01}, profile={profile_balance}")
                results.append(("TC02", "GET /user/points - verify khop profile", ok,
                                 200 if match else "mismatch"))
            else:
                print(f"[SKIP] TC02 - profile khong co field point_balance")
                results.append(("TC02", "GET /user/points - verify khop profile", None, "skip"))
        except Exception as e:
            print(f"[ERROR] TC02 - {e}")
            results.append(("TC02", "GET /user/points - verify khop profile", False, "error"))
    else:
        print(f"[SKIP] TC02 - khong lay duoc du lieu de so sanh")
        results.append(("TC02", "GET /user/points - verify khop profile", None, "skip"))

    run("TC03", "GET /user/points - khong co token",
        "get", f"{url}/user/points", 401,
        headers=auth())

    # ── GET /user/points/transactions ─────────────────────────

    res = run("TC04", "GET /user/points/transactions - lay tat ca",
              "get", f"{url}/user/points/transactions", 200,
              headers=auth(USER_TOKEN))
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC04: {len(items)} transactions")
        if items and isinstance(items[0], dict):
            print(f"  [INFO] TC04: fields = {list(items[0].keys())}")
            for f in ["id", "type", "amount", "created_at"]:
                if f not in items[0]:
                    print(f"  [WARN] TC04: thieu field '{f}'")

    for tc, type_val in [("TC05", "purchase"), ("TC06", "spend"),
                          ("TC07", "bonus"),   ("TC08", "refund")]:
        res = run(tc, f"GET /user/points/transactions - filter type={type_val}",
                  "get", f"{url}/user/points/transactions", 200,
                  headers=auth(USER_TOKEN), params={"type": type_val})
        if res and res.status_code == 200:
            items = extract_items(res)
            bad   = [r for r in items if isinstance(r, dict) and r.get("type") != type_val]
            if bad:
                print(f"  [WARN] {tc}: co {len(bad)} record khong phai type={type_val}")
            else:
                print(f"  [INFO] {tc}: {len(items)} records, tat ca type={type_val} - OK")

    res = run("TC09", "GET /user/points/transactions - phan trang per_page=5",
              "get", f"{url}/user/points/transactions", 200,
              headers=auth(USER_TOKEN), params={"page": 1, "per_page": 5})
    if res and res.status_code == 200:
        items = extract_items(res)
        if len(items) > 5:
            print(f"  [WARN] TC09: data co {len(items)} phan tu, nen <= 5")
        else:
            print(f"  [INFO] TC09: {len(items)} items - OK")

    run("TC10", "GET /user/points/transactions - trang 2",
        "get", f"{url}/user/points/transactions", 200,
        headers=auth(USER_TOKEN), params={"page": 2, "per_page": 5})

    run("TC11", "GET /user/points/transactions - type sai gia tri",
        "get", f"{url}/user/points/transactions", 422,
        headers=auth(USER_TOKEN), params={"type": "invalid"})

    run("TC12", "GET /user/points/transactions - khong co token",
        "get", f"{url}/user/points/transactions", 401,
        headers=auth())

    # ── POST /user/points/purchase ────────────────────────────

    balance_before = get_point_balance(USER_TOKEN)
    print(f"[SETUP] point_balance truoc khi nap = {balance_before}")

    for tc, amount, method in [
        ("TC13", 100, "momo"),
        ("TC14", 200, "vnpay"),
        ("TC15", 500, "bank"),
        ("TC16", 1,   "momo"),
    ]:
        bal_before = get_point_balance(USER_TOKEN)
        res = run(tc, f"POST /user/points/purchase - nap {amount} via {method}",
                  "post", f"{url}/user/points/purchase", [200, 201],
                  headers=auth(USER_TOKEN),
                  json={"amount": amount, "payment_method": method})
        if res and res.status_code in (200, 201):
            try:
                data = res.json().get("data", res.json())
                print(f"  [INFO] {tc}: response keys = {list(data.keys()) if isinstance(data, dict) else type(data)}")
            except Exception:
                pass
            # Verify balance tăng
            bal_after = get_point_balance(USER_TOKEN)
            if bal_before is not None and bal_after is not None:
                diff = bal_after - bal_before
                if diff == amount:
                    print(f"  [INFO] {tc}: balance tang dung {amount} ({bal_before} -> {bal_after}) - OK")
                else:
                    print(f"  [WARN] {tc}: balance tang {diff}, ky vong {amount} ({bal_before} -> {bal_after})")
        elif res:
            print(f"\n>>> DEBUG {tc} <<<")
            print(f"  status : {res.status_code}")
            try:
                import json
                print(f"  body   : {json.dumps(res.json(), ensure_ascii=False, indent=2)}")
            except Exception:
                print(f"  raw    : {res.text[:800]}")
            print(f">>> END {tc} <<<\n")

    # Verify transaction mới nhất là purchase
    res_txn = requests.get(f"{url}/user/points/transactions",
                           headers=auth(USER_TOKEN),
                           params={"type": "purchase", "per_page": 1})
    if res_txn.status_code == 200:
        items = extract_items(res_txn)
        if items and isinstance(items[0], dict):
            print(f"  [INFO] TC13-16: transaction moi nhat = {items[0]}")

    # Validation cases
    run("TC17", "POST /user/points/purchase - amount = 0",
        "post", f"{url}/user/points/purchase", 422,
        headers=auth(USER_TOKEN),
        json={"amount": 0, "payment_method": "momo"})

    run("TC18", "POST /user/points/purchase - amount am",
        "post", f"{url}/user/points/purchase", 422,
        headers=auth(USER_TOKEN),
        json={"amount": -100, "payment_method": "momo"})

    run("TC19", "POST /user/points/purchase - amount khong phai so",
        "post", f"{url}/user/points/purchase", 422,
        headers=auth(USER_TOKEN),
        json={"amount": "abc", "payment_method": "momo"})

    run("TC20", "POST /user/points/purchase - payment_method sai",
        "post", f"{url}/user/points/purchase", 422,
        headers=auth(USER_TOKEN),
        json={"amount": 100, "payment_method": "paypal"})

    run("TC21", "POST /user/points/purchase - thieu amount",
        "post", f"{url}/user/points/purchase", 422,
        headers=auth(USER_TOKEN),
        json={"payment_method": "momo"})

    run("TC22", "POST /user/points/purchase - thieu payment_method",
        "post", f"{url}/user/points/purchase", 422,
        headers=auth(USER_TOKEN),
        json={"amount": 100})

    run("TC23", "POST /user/points/purchase - body rong",
        "post", f"{url}/user/points/purchase", 422,
        headers=auth(USER_TOKEN),
        json={})

    run("TC24", "POST /user/points/purchase - khong co token",
        "post", f"{url}/user/points/purchase", 401,
        headers=auth(),
        json={"amount": 100, "payment_method": "momo"})

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
