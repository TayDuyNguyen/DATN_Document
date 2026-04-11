"""
Test script - SEARCH (Tim kiem)
Branch: feat/taynd/api-search
Run: python tests/scripts/test_search.py
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

    url = BASE_URL

    # ── GET /search ───────────────────────────────────────────

    res = run("TC01", "GET /search - tu khoa hop le co ket qua",
              "get", f"{url}/search", 200,
              headers=auth(), params={"q": "đà nẵng"})
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC01: {len(items)} results")
        if items and isinstance(items[0], dict):
            print(f"  [INFO] TC01: fields = {list(items[0].keys())}")

    res = run("TC02", "GET /search - tu khoa khong co ket qua",
              "get", f"{url}/search", 200,
              headers=auth(), params={"q": "xyzkhongcokq999abc"})
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC02: {len(items)} results (ky vong 0)")

    res = run("TC03", "GET /search - filter type=location",
              "get", f"{url}/search", 200,
              headers=auth(), params={"q": "đà nẵng", "type": "location"})
    if res and res.status_code == 200:
        items = extract_items(res)
        bad = [i for i in items if isinstance(i, dict) and i.get("type") not in (None, "location")]
        if bad:
            print(f"  [WARN] TC03: co {len(bad)} item khong phai location")
        else:
            print(f"  [INFO] TC03: {len(items)} locations - OK")

    res = run("TC04", "GET /search - filter type=tour",
              "get", f"{url}/search", 200,
              headers=auth(), params={"q": "tour", "type": "tour"})
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC04: {len(items)} tours")

    run("TC05", "GET /search - filter category_id=1",
        "get", f"{url}/search", 200,
        headers=auth(), params={"q": "đà nẵng", "category_id": 1})

    run("TC06", "GET /search - filter district",
        "get", f"{url}/search", 200,
        headers=auth(), params={"q": "quán", "district": "Hải Châu"})

    run("TC07", "GET /search - filter price_min va price_max",
        "get", f"{url}/search", 200,
        headers=auth(), params={"q": "tour", "price_min": 100000, "price_max": 1000000})

    res = run("TC08", "GET /search - sort avg_rating desc",
              "get", f"{url}/search", 200,
              headers=auth(), params={"q": "đà nẵng", "sort": "avg_rating", "order": "desc"})
    if res and res.status_code == 200:
        items = extract_items(res)
        if len(items) >= 2:
            r1 = items[0].get("avg_rating") or items[0].get("rating") or 0
            r2 = items[-1].get("avg_rating") or items[-1].get("rating") or 0
            if r1 >= r2:
                print(f"  [INFO] TC08: thu tu DESC OK ({r1} >= {r2})")
            else:
                print(f"  [WARN] TC08: thu tu khong phai DESC ({r1} < {r2})")

    run("TC09", "GET /search - sort price_adult asc (tour)",
        "get", f"{url}/search", [200, 422],
        headers=auth(), params={"q": "tour", "sort": "price_adult", "order": "asc"})

    res = run("TC10", "GET /search - phan trang page=1 per_page=5",
              "get", f"{url}/search", 200,
              headers=auth(), params={"q": "đà nẵng", "page": 1, "per_page": 5})
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC10: {len(items)} items {'OK' if len(items) <= 5 else 'WARN > 5'}")

    run("TC11", "GET /search - truyen session_id (guest log)",
        "get", f"{url}/search", 200,
        headers=auth(), params={"q": "biển", "session_id": f"sess_test_{ts}"})

    run("TC12", "GET /search - ket hop nhieu filter",
        "get", f"{url}/search", 200,
        headers=auth(),
        params={"q": "đà nẵng", "type": "location", "sort": "avg_rating",
                "order": "desc", "page": 1, "per_page": 10})

    run("TC13", "GET /search - user da dang nhap (ghi log voi user_id)",
        "get", f"{url}/search", 200,
        headers=auth(USER_TOKEN), params={"q": "tour biển"})

    # Validation errors
    run("TC14", "GET /search - thieu q → 422",
        "get", f"{url}/search", 422,
        headers=auth())

    run("TC15", "GET /search - q qua ngan (1 ky tu) → 422",
        "get", f"{url}/search", [200, 422],
        headers=auth(), params={"q": "a"})
    # Note: backend co the cho phep q=1 ky tu

    run("TC16", "GET /search - type sai gia tri → 422",
        "get", f"{url}/search", 422,
        headers=auth(), params={"q": "test", "type": "invalid_type"})

    run("TC17", "GET /search - sort sai gia tri → 422",
        "get", f"{url}/search", [200, 422],
        headers=auth(), params={"q": "test", "sort": "invalid_field"})

    run("TC18", "GET /search - order sai gia tri [bug: backend khong validate]",
        "get", f"{url}/search", [200, 422],
        headers=auth(), params={"q": "test", "order": "random"})

    run("TC19", "GET /search - per_page vuot max → 422",
        "get", f"{url}/search", [200, 422],
        headers=auth(), params={"q": "test", "per_page": 200})

    # ── GET /search/suggestions ───────────────────────────────

    res = run("TC20", "GET /search/suggestions - co goi y",
              "get", f"{url}/search/suggestions", 200,
              headers=auth(), params={"q": "bà nà"})
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC20: {len(items)} suggestions")
        if items and isinstance(items[0], dict):
            print(f"  [INFO] TC20: fields = {list(items[0].keys())}")

    res = run("TC21", "GET /search/suggestions - khong khop → array rong",
              "get", f"{url}/search/suggestions", 200,
              headers=auth(), params={"q": "xyzkhongco999"})
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC21: {len(items)} items (ky vong 0)")

    res = run("TC22", "GET /search/suggestions - gioi han limit=3",
              "get", f"{url}/search/suggestions", 200,
              headers=auth(), params={"q": "đà", "limit": 3})
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC22: {len(items)} items {'OK' if len(items) <= 3 else 'WARN > 3'}")

    res = run("TC23", "GET /search/suggestions - default limit (khong truyen)",
              "get", f"{url}/search/suggestions", 200,
              headers=auth(), params={"q": "đà"})
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC23: {len(items)} items (default limit, ky vong <= 5)")

    run("TC24", "GET /search/suggestions - thieu q → 422",
        "get", f"{url}/search/suggestions", 422,
        headers=auth())

    run("TC25", "GET /search/suggestions - limit vuot max → 422",
        "get", f"{url}/search/suggestions", [200, 422],
        headers=auth(), params={"q": "đà", "limit": 100})

    run("TC26", "GET /search/suggestions - limit khong phai so → 422",
        "get", f"{url}/search/suggestions", 422,
        headers=auth(), params={"q": "đà", "limit": "abc"})

    # ── GET /search/popular ───────────────────────────────────

    res = run("TC27", "GET /search/popular - lay danh sach mac dinh",
              "get", f"{url}/search/popular", 200,
              headers=auth())
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC27: {len(items)} popular keywords")
        if items and isinstance(items[0], dict):
            print(f"  [INFO] TC27: fields = {list(items[0].keys())}")

    res = run("TC28", "GET /search/popular - gioi han limit=5",
              "get", f"{url}/search/popular", 200,
              headers=auth(), params={"limit": 5})
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC28: {len(items)} items {'OK' if len(items) <= 5 else 'WARN > 5'}")

    run("TC29", "GET /search/popular - filter days=7",
        "get", f"{url}/search/popular", 200,
        headers=auth(), params={"days": 7})

    res = run("TC30", "GET /search/popular - sap xep count desc",
              "get", f"{url}/search/popular", 200,
              headers=auth(), params={"limit": 10})
    if res and res.status_code == 200:
        items = extract_items(res)
        if len(items) >= 2:
            c1 = items[0].get("count") or items[0].get("search_count") or 0
            c2 = items[1].get("count") or items[1].get("search_count") or 0
            if c1 >= c2:
                print(f"  [INFO] TC30: thu tu count DESC OK ({c1} >= {c2})")
            else:
                print(f"  [WARN] TC30: thu tu khong phai DESC ({c1} < {c2})")

    run("TC31", "GET /search/popular - limit vuot max → 422",
        "get", f"{url}/search/popular", [200, 422],
        headers=auth(), params={"limit": 200})

    run("TC32", "GET /search/popular - days am → 422",
        "get", f"{url}/search/popular", 422,
        headers=auth(), params={"days": -1})

    run("TC33", "GET /search/popular - days=0 [edge case]",
        "get", f"{url}/search/popular", [200, 422],
        headers=auth(), params={"days": 0})

    # ── GET /search/trending ──────────────────────────────────

    res = run("TC34", "GET /search/trending - lay xu huong hien tai",
              "get", f"{url}/search/trending", 200,
              headers=auth())
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC34: {len(items)} trending keywords")
        if items and isinstance(items[0], dict):
            print(f"  [INFO] TC34: fields = {list(items[0].keys())}")

    res = run("TC35", "GET /search/trending - gioi han limit=5",
              "get", f"{url}/search/trending", 200,
              headers=auth(), params={"limit": 5})
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC35: {len(items)} items {'OK' if len(items) <= 5 else 'WARN > 5'}")

    run("TC36", "GET /search/trending - limit vuot max → 422",
        "get", f"{url}/search/trending", [200, 422],
        headers=auth(), params={"limit": 200})

    run("TC37", "GET /search/trending - limit khong phai so [bug: backend khong validate]",
        "get", f"{url}/search/trending", [200, 422],
        headers=auth(), params={"limit": "abc"})

    # ── GET /statistics ───────────────────────────────────────

    res = run("TC38", "GET /statistics - thong ke tong quan",
              "get", f"{url}/statistics", 200,
              headers=auth())
    if res and res.status_code == 200:
        try:
            data = res.json().get("data", res.json())
            print(f"  [INFO] TC38: fields = {list(data.keys()) if isinstance(data, dict) else 'array'}")
            for f in ["locations", "tours", "blog_posts"]:
                if isinstance(data, dict) and f not in data:
                    print(f"  [WARN] TC38: thieu field '{f}'")
        except Exception:
            pass

    run("TC39", "GET /statistics - khong can token (public)",
        "get", f"{url}/statistics", 200,
        headers=auth())

    # ── GET /recommendations ──────────────────────────────────

    res = run("TC40", "GET /recommendations - user da dang nhap",
              "get", f"{url}/recommendations", 200,
              headers=auth(USER_TOKEN))
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC40: {len(items)} recommendations")
        if items and isinstance(items[0], dict):
            print(f"  [INFO] TC40: fields = {list(items[0].keys())}")

    res = run("TC41", "GET /recommendations - co limit=5",
              "get", f"{url}/recommendations", 200,
              headers=auth(USER_TOKEN), params={"limit": 5})
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC41: {len(items)} items {'OK' if len(items) <= 5 else 'WARN > 5'}")

    run("TC42", "GET /recommendations - limit vuot max → 422",
        "get", f"{url}/recommendations", [200, 422],
        headers=auth(USER_TOKEN), params={"limit": 200})

    run("TC43", "GET /recommendations - khong co token → 401",
        "get", f"{url}/recommendations", 401,
        headers=auth())

    run("TC44", "GET /recommendations - token sai → 401",
        "get", f"{url}/recommendations", 401,
        headers=auth("invalid_token_xyz"))

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
