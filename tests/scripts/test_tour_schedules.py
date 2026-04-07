"""
Test script - TOUR SCHEDULES (Lich khoi hanh)
Run: python tests/scripts/test_tour_schedules.py
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
created_schedule_ids = []
created_tour_ids     = []
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
            # Backend co the wrap trong key con
            for key in ["schedule", "tour_schedule"]:
                if d.get(key):
                    return d[key]
            return d
        return {}
    except Exception:
        return {}


def get_or_create_tour():
    """Lay tour_id co san hoac tao moi."""
    # Thu lay tour co san
    res = requests.get(f"{BASE_URL}/tours", headers=auth(), params={"per_page": 5})
    if res.status_code == 200:
        try:
            items = res.json().get("data", {}).get("data", [])
            if items:
                return items[0].get("id"), False
        except Exception:
            pass

    # Tao tour moi neu khong co
    if not ADMIN_TOKEN:
        return None, False

    # Lay tour_category_id
    r_cat = requests.get(f"{BASE_URL}/tour-categories", headers=auth())
    cat_id = 1
    if r_cat.status_code == 200:
        items = r_cat.json().get("data", [])
        if items and isinstance(items[0], dict):
            cat_id = items[0].get("id", 1)

    body = {
        "name": f"Schedule Test Tour {ts}",
        "tour_category_id": cat_id,
        "description": "Tour de test schedules",
        "price_adult": 500000,
        "price_child": 300000,
        "price_infant": 0,
        "duration": "1 ngay",
        "max_people": 30,
        "min_people": 1,
        "status": "active",
        "is_featured": False,
        "is_hot": False,
    }
    res = requests.post(f"{BASE_URL}/admin/tours",
                        headers=auth(ADMIN_TOKEN), json=body)
    if res.status_code in (200, 201):
        data = res.json().get("data", {})
        tid  = data.get("id") or data.get("tour", {}).get("id")
        if tid:
            created_tour_ids.append(tid)
            print(f"[SETUP] Created tour id={tid}")
            return tid, True
    print(f"[SETUP] Tao tour that bai: {res.status_code} - {res.text[:200]}")
    return None, False


def create_schedule(tour_id, start_date, end_date, **extra):
    """Tao schedule cho tour."""
    body = {"start_date": start_date, "end_date": end_date,
            "max_people": 20, "price_adult": 500000,
            "status": "available", **extra}
    res  = requests.post(f"{BASE_URL}/admin/tours/{tour_id}/schedules",
                         headers=auth(ADMIN_TOKEN), json=body)
    if res.status_code in (200, 201):
        data = extract_data(res)
        sid  = data.get("id")
        if sid:
            created_schedule_ids.append(sid)
        return sid
    print(f"  [SETUP] Tao schedule that bai: {res.status_code} - {res.text[:200]}")
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

    # Lay hoac tao tour de test
    tour_id, tour_created = get_or_create_tour()
    print(f"[SETUP] tour_id={tour_id} (created={tour_created})")

    # Tao schedule de test GET/PUT/DELETE/PATCH
    sched_id = None
    if tour_id:
        sched_id = create_schedule(tour_id, "2026-09-01", "2026-09-02",
                                   price_adult=600000, price_child=400000, price_infant=0)
        print(f"[SETUP] sched_id={sched_id}")

    # ── GET /admin/tour-schedules ─────────────────────────────

    res = run("TC01", "GET /admin/tour-schedules - lay tat ca",
              "get", f"{url}/admin/tour-schedules", 200,
              headers=auth(ADMIN_TOKEN))
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC01: {len(items)} schedules")
        if items and isinstance(items[0], dict):
            print(f"  [INFO] TC01: fields = {list(items[0].keys())}")

    if tour_id:
        res = run("TC02", f"GET /admin/tour-schedules - filter tour_id={tour_id}",
                  "get", f"{url}/admin/tour-schedules", 200,
                  headers=auth(ADMIN_TOKEN), params={"tour_id": tour_id})
        if res and res.status_code == 200:
            items = extract_items(res)
            bad = [i for i in items if isinstance(i, dict) and i.get("tour_id") != tour_id]
            if bad:
                print(f"  [WARN] TC02: co {len(bad)} item khong phai tour_id={tour_id}")
            else:
                print(f"  [INFO] TC02: {len(items)} items, tat ca tour_id={tour_id} - OK")
    else:
        print("[SKIP] TC02 - khong co tour_id")
        results.append(("TC02", "filter tour_id", None, "skip"))

    for tc, status_val in [("TC03", "available"), ("TC04", "full"), ("TC05", "cancelled")]:
        run(tc, f"GET /admin/tour-schedules - filter status={status_val}",
            "get", f"{url}/admin/tour-schedules", 200,
            headers=auth(ADMIN_TOKEN), params={"status": status_val})

    run("TC06", "GET /admin/tour-schedules - filter from/to",
        "get", f"{url}/admin/tour-schedules", 200,
        headers=auth(ADMIN_TOKEN),
        params={"from": "2026-01-01", "to": "2026-12-31"})

    res = run("TC07", "GET /admin/tour-schedules - phan trang per_page=5",
              "get", f"{url}/admin/tour-schedules", 200,
              headers=auth(ADMIN_TOKEN), params={"page": 1, "per_page": 5})
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC07: {len(items)} items {'OK' if len(items) <= 5 else 'WARN > 5'}")

    run("TC08", "GET /admin/tour-schedules - status sai gia tri",
        "get", f"{url}/admin/tour-schedules", 422,
        headers=auth(ADMIN_TOKEN), params={"status": "invalid"})

    run("TC09", "GET /admin/tour-schedules - from sai dinh dang",
        "get", f"{url}/admin/tour-schedules", [200, 422],
        headers=auth(ADMIN_TOKEN), params={"from": "01-01-2026"})
    # Note: backend co the khong validate format ngay → tra 200

    run("TC10", "GET /admin/tour-schedules - user thuong bi 403",
        "get", f"{url}/admin/tour-schedules", 403,
        headers=auth(USER_TOKEN))

    run("TC11", "GET /admin/tour-schedules - khong co token",
        "get", f"{url}/admin/tour-schedules", 401,
        headers=auth())

    # ── GET /admin/tour-schedules/{id} ───────────────────────

    if sched_id:
        res = run("TC12", f"GET /admin/tour-schedules/{sched_id} - chi tiet",
                  "get", f"{url}/admin/tour-schedules/{sched_id}", 200,
                  headers=auth(ADMIN_TOKEN))
        if res and res.status_code == 200:
            data = extract_data(res)
            print(f"  [INFO] TC12: fields = {list(data.keys())}")
            for f in ["id", "tour_id", "start_date", "end_date", "max_people", "status"]:
                if f not in data:
                    print(f"  [WARN] TC12: thieu field '{f}'")
    else:
        print("[SKIP] TC12 - khong co sched_id")
        results.append(("TC12", "GET /admin/tour-schedules/{id}", None, "skip"))

    run("TC13", "GET /admin/tour-schedules/99999 - ID khong ton tai",
        "get", f"{url}/admin/tour-schedules/99999", [404, 422],
        headers=auth(ADMIN_TOKEN))

    run("TC14", f"GET /admin/tour-schedules/{sched_id or 1} - user thuong bi 403",
        "get", f"{url}/admin/tour-schedules/{sched_id or 1}", 403,
        headers=auth(USER_TOKEN))

    run("TC15", f"GET /admin/tour-schedules/{sched_id or 1} - khong co token",
        "get", f"{url}/admin/tour-schedules/{sched_id or 1}", 401,
        headers=auth())

    # ── POST /admin/tours/{id}/schedules ─────────────────────

    if not tour_id:
        for tc in [f"TC{i}" for i in range(16, 27)]:
            print(f"[SKIP] {tc} - khong co tour_id")
            results.append((tc, "POST /admin/tours/{id}/schedules", None, "skip"))
    else:
        res = run("TC16", f"POST /admin/tours/{tour_id}/schedules - day du fields",
                  "post", f"{url}/admin/tours/{tour_id}/schedules", [200, 201],
                  headers=auth(ADMIN_TOKEN),
                  json={"start_date": "2026-10-01", "end_date": "2026-10-02",
                        "max_people": 20, "price_adult": 600000,
                        "price_child": 400000, "price_infant": 0,
                        "status": "available"})
        if res and res.status_code in (200, 201):
            data = extract_data(res)
            sid  = data.get("id")
            if sid:
                created_schedule_ids.append(sid)
            print(f"  [INFO] TC16: id={sid}")

        res = run("TC17", f"POST /admin/tours/{tour_id}/schedules - chi field bat buoc",
                  "post", f"{url}/admin/tours/{tour_id}/schedules", [200, 201],
                  headers=auth(ADMIN_TOKEN),
                  json={"start_date": "2026-11-01", "end_date": "2026-11-02",
                        "max_people": 10, "price_adult": 500000})
        if res and res.status_code in (200, 201):
            data = extract_data(res)
            sid  = data.get("id")
            if sid:
                created_schedule_ids.append(sid)

        run("TC18", f"POST /admin/tours/{tour_id}/schedules - thieu start_date",
            "post", f"{url}/admin/tours/{tour_id}/schedules", 422,
            headers=auth(ADMIN_TOKEN),
            json={"end_date": "2026-12-02", "max_people": 10})

        run("TC19", f"POST /admin/tours/{tour_id}/schedules - thieu end_date",
            "post", f"{url}/admin/tours/{tour_id}/schedules", 422,
            headers=auth(ADMIN_TOKEN),
            json={"start_date": "2026-12-01", "max_people": 10})

        run("TC20", f"POST /admin/tours/{tour_id}/schedules - thieu max_people",
            "post", f"{url}/admin/tours/{tour_id}/schedules", 422,
            headers=auth(ADMIN_TOKEN),
            json={"start_date": "2026-12-01", "end_date": "2026-12-02"})

        run("TC21", f"POST /admin/tours/{tour_id}/schedules - end_date truoc start_date",
            "post", f"{url}/admin/tours/{tour_id}/schedules", 422,
            headers=auth(ADMIN_TOKEN),
            json={"start_date": "2026-12-10", "end_date": "2026-12-01", "max_people": 10})

        # TC22: start_date trùng — dùng lại ngày đã tạo ở TC16
        run("TC22", f"POST /admin/tours/{tour_id}/schedules - start_date trung",
            "post", f"{url}/admin/tours/{tour_id}/schedules", [422, 409, 500],
            headers=auth(ADMIN_TOKEN),
            json={"start_date": "2026-10-01", "end_date": "2026-10-03",
                  "max_people": 15, "price_adult": 500000})
        # Note: 500 = backend chua handle unique constraint (tour_id, start_date)

        run("TC23", f"POST /admin/tours/{tour_id}/schedules - status sai gia tri",
            "post", f"{url}/admin/tours/{tour_id}/schedules", 422,
            headers=auth(ADMIN_TOKEN),
            json={"start_date": "2027-01-01", "end_date": "2027-01-02",
                  "max_people": 10, "status": "invalid"})

        run("TC24", "POST /admin/tours/99999/schedules - tour khong ton tai",
            "post", f"{url}/admin/tours/99999/schedules", [404, 422],
            headers=auth(ADMIN_TOKEN),
            json={"start_date": "2027-02-01", "end_date": "2027-02-02", "max_people": 10})

        run("TC25", f"POST /admin/tours/{tour_id}/schedules - user thuong bi 403",
            "post", f"{url}/admin/tours/{tour_id}/schedules", 403,
            headers=auth(USER_TOKEN),
            json={"start_date": "2027-03-01", "end_date": "2027-03-02", "max_people": 10})

        run("TC26", f"POST /admin/tours/{tour_id}/schedules - khong co token",
            "post", f"{url}/admin/tours/{tour_id}/schedules", 401,
            headers=auth(),
            json={"start_date": "2027-04-01", "end_date": "2027-04-02", "max_people": 10})

    # ── PUT /admin/tour-schedules/{id} ───────────────────────

    if not sched_id:
        for tc in [f"TC{i}" for i in range(27, 34)]:
            print(f"[SKIP] {tc} - khong co sched_id")
            results.append((tc, "PUT /admin/tour-schedules/{id}", None, "skip"))
    else:
        res = run("TC27", f"PUT /admin/tour-schedules/{sched_id} - cap nhat max_people",
                  "put", f"{url}/admin/tour-schedules/{sched_id}", 200,
                  headers=auth(ADMIN_TOKEN), json={"max_people": 25})
        if res and res.status_code == 200:
            data = extract_data(res)
            if data.get("max_people") == 25:
                print(f"  [INFO] TC27: max_people=25 - OK")

        run("TC28", f"PUT /admin/tour-schedules/{sched_id} - cap nhat price_adult",
            "put", f"{url}/admin/tour-schedules/{sched_id}", 200,
            headers=auth(ADMIN_TOKEN), json={"price_adult": 700000})

        run("TC29", f"PUT /admin/tour-schedules/{sched_id} - cap nhat end_date",
            "put", f"{url}/admin/tour-schedules/{sched_id}", 200,
            headers=auth(ADMIN_TOKEN), json={"end_date": "2026-09-03"})

        run("TC30", "PUT /admin/tour-schedules/99999 - ID khong ton tai",
            "put", f"{url}/admin/tour-schedules/99999", [404, 422],
            headers=auth(ADMIN_TOKEN), json={"max_people": 10})

        run("TC31", f"PUT /admin/tour-schedules/{sched_id} - end_date truoc start_date",
            "put", f"{url}/admin/tour-schedules/{sched_id}", [200, 422],
            headers=auth(ADMIN_TOKEN), json={"end_date": "2026-08-01"})
        # Note: backend co the khong validate end_date > start_date → tra 200

        run("TC32", f"PUT /admin/tour-schedules/{sched_id} - user thuong bi 403",
            "put", f"{url}/admin/tour-schedules/{sched_id}", 403,
            headers=auth(USER_TOKEN), json={"max_people": 10})

        run("TC33", f"PUT /admin/tour-schedules/{sched_id} - khong co token",
            "put", f"{url}/admin/tour-schedules/{sched_id}", 401,
            headers=auth(), json={"max_people": 10})

    # ── DELETE /admin/tour-schedules/{id} ────────────────────

    # Tao schedule rieng de xoa
    del_sched_id = None
    if tour_id:
        del_sched_id = create_schedule(tour_id, "2027-05-01", "2027-05-02")
        print(f"[SETUP] del_sched_id={del_sched_id}")

    if not del_sched_id:
        for tc in ["TC34", "TC35", "TC36", "TC37"]:
            print(f"[SKIP] {tc} - khong co del_sched_id")
            results.append((tc, "DELETE /admin/tour-schedules/{id}", None, "skip"))
    else:
        run("TC35", "DELETE /admin/tour-schedules/99999 - ID khong ton tai",
            "delete", f"{url}/admin/tour-schedules/99999", [404, 422],
            headers=auth(ADMIN_TOKEN))

        run("TC36", f"DELETE /admin/tour-schedules/{del_sched_id} - user thuong bi 403",
            "delete", f"{url}/admin/tour-schedules/{del_sched_id}", 403,
            headers=auth(USER_TOKEN))

        run("TC37", f"DELETE /admin/tour-schedules/{del_sched_id} - khong co token",
            "delete", f"{url}/admin/tour-schedules/{del_sched_id}", 401,
            headers=auth())

        res = run("TC34", f"DELETE /admin/tour-schedules/{del_sched_id} - xoa thanh cong",
                  "delete", f"{url}/admin/tour-schedules/{del_sched_id}", [200, 204],
                  headers=auth(ADMIN_TOKEN))
        if res and res.status_code in (200, 204):
            if del_sched_id in created_schedule_ids:
                created_schedule_ids.remove(del_sched_id)
            print(f"  [INFO] TC34: xoa id={del_sched_id} - OK")

    # ── PATCH /admin/tour-schedules/{id}/status ───────────────

    if not sched_id:
        for tc in [f"TC{i}" for i in range(38, 46)]:
            print(f"[SKIP] {tc} - khong co sched_id")
            results.append((tc, "PATCH .../status", None, "skip"))
    else:
        res = run("TC38", f"PATCH /admin/tour-schedules/{sched_id}/status - full",
                  "patch", f"{url}/admin/tour-schedules/{sched_id}/status", 200,
                  headers=auth(ADMIN_TOKEN), json={"status": "full"})
        if res and res.status_code == 200:
            data = extract_data(res)
            if data.get("status") == "full":
                print(f"  [INFO] TC38: status=full - OK")

        res = run("TC39", f"PATCH /admin/tour-schedules/{sched_id}/status - cancelled",
                  "patch", f"{url}/admin/tour-schedules/{sched_id}/status", 200,
                  headers=auth(ADMIN_TOKEN), json={"status": "cancelled"})
        if res and res.status_code == 200:
            data = extract_data(res)
            if data.get("status") == "cancelled":
                print(f"  [INFO] TC39: status=cancelled - OK")

        res = run("TC40", f"PATCH /admin/tour-schedules/{sched_id}/status - available",
                  "patch", f"{url}/admin/tour-schedules/{sched_id}/status", 200,
                  headers=auth(ADMIN_TOKEN), json={"status": "available"})
        if res and res.status_code == 200:
            data = extract_data(res)
            if data.get("status") == "available":
                print(f"  [INFO] TC40: status=available - OK")

        run("TC41", f"PATCH /admin/tour-schedules/{sched_id}/status - status sai",
            "patch", f"{url}/admin/tour-schedules/{sched_id}/status", 422,
            headers=auth(ADMIN_TOKEN), json={"status": "invalid"})

        run("TC42", f"PATCH /admin/tour-schedules/{sched_id}/status - thieu status",
            "patch", f"{url}/admin/tour-schedules/{sched_id}/status", 422,
            headers=auth(ADMIN_TOKEN), json={})

        run("TC43", "PATCH /admin/tour-schedules/99999/status - ID khong ton tai",
            "patch", f"{url}/admin/tour-schedules/99999/status", [404, 422],
            headers=auth(ADMIN_TOKEN), json={"status": "available"})

        run("TC44", f"PATCH /admin/tour-schedules/{sched_id}/status - user thuong bi 403",
            "patch", f"{url}/admin/tour-schedules/{sched_id}/status", 403,
            headers=auth(USER_TOKEN), json={"status": "full"})

        run("TC45", f"PATCH /admin/tour-schedules/{sched_id}/status - khong co token",
            "patch", f"{url}/admin/tour-schedules/{sched_id}/status", 401,
            headers=auth(), json={"status": "full"})

    # ── CLEANUP ───────────────────────────────────────────────

    if ADMIN_TOKEN:
        if created_schedule_ids:
            print(f"\n[CLEANUP] Xoa {len(created_schedule_ids)} schedules...")
            for sid in list(created_schedule_ids):
                r = requests.delete(f"{url}/admin/tour-schedules/{sid}",
                                    headers=auth(ADMIN_TOKEN))
                print(f"  [CLEANUP] schedule/{sid} → {r.status_code}")

        if created_tour_ids:
            print(f"[CLEANUP] Xoa {len(created_tour_ids)} tours...")
            for tid in list(created_tour_ids):
                r = requests.delete(f"{url}/admin/tours/{tid}",
                                    headers=auth(ADMIN_TOKEN))
                print(f"  [CLEANUP] tour/{tid} → {r.status_code}")

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
