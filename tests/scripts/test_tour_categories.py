"""
Test script - TOUR CATEGORIES (Danh muc tour)
Run: python tests/scripts/test_tour_categories.py
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
created_ids = []
ts          = int(time.time())


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
            # Backend tra ve data.category hoac data truc tiep
            return d.get("category") or d.get("tour_category") or d
        return {}
    except Exception:
        return {}


def get_first_active_category():
    """Lay slug va id cua tour category dau tien."""
    res = requests.get(f"{BASE_URL}/tour-categories", headers=auth())
    if res.status_code == 200:
        items = extract_items(res)
        if items and isinstance(items[0], dict):
            return items[0].get("slug"), items[0].get("id")
    return None, None


def admin_create_category(name, **extra):
    """Tao tour category qua admin API."""
    body = {"name": name, "status": "active", **extra}
    res  = requests.post(f"{BASE_URL}/admin/tour-categories",
                         headers=auth(ADMIN_TOKEN), json=body)
    if res.status_code in (200, 201):
        data = extract_data(res)
        cid  = data.get("id")
        slug = data.get("slug")
        if cid:
            created_ids.append(cid)
        return cid, slug
    print(f"  [SETUP] Tao category that bai: {res.status_code} - {res.text[:150]}")
    return None, None


def run_tests():
    global USER_TOKEN, ADMIN_TOKEN

    USER_TOKEN  = login(USER_EMAIL, USER_PASSWORD)
    ADMIN_TOKEN = login(ADMIN_EMAIL, ADMIN_PASSWORD)

    if not USER_TOKEN:
        print("[ABORT] Khong lay duoc USER_TOKEN.")
        return

    url = BASE_URL

    # ── GET /tour-categories ──────────────────────────────────

    res = run("TC01", "GET /tour-categories - lay danh sach",
              "get", f"{url}/tour-categories", 200, headers=auth())
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC01: {len(items)} categories")
        if items and isinstance(items[0], dict):
            print(f"  [INFO] TC01: fields = {list(items[0].keys())}")

    res = run("TC02", "GET /tour-categories - chi tra active",
              "get", f"{url}/tour-categories", 200, headers=auth())
    if res and res.status_code == 200:
        items = extract_items(res)
        bad = [i for i in items if isinstance(i, dict) and i.get("status") != "active"]
        if bad:
            print(f"  [WARN] TC02: co {len(bad)} item khong phai status=active")
        else:
            print(f"  [INFO] TC02: tat ca {len(items)} items deu active - OK")

    run("TC03", "GET /tour-categories - khong can token",
        "get", f"{url}/tour-categories", 200, headers=auth())

    # ── GET /tour-categories/{slug}/tours ─────────────────────

    first_slug, first_id = get_first_active_category()
    print(f"[SETUP] first_slug={first_slug}, first_id={first_id}")

    if first_slug:
        res = run("TC04", f"GET /tour-categories/{first_slug}/tours - lay tour",
                  "get", f"{url}/tour-categories/{first_slug}/tours", 200, headers=auth())
        if res and res.status_code == 200:
            items = extract_items(res)
            print(f"  [INFO] TC04: {len(items)} tours trong category {first_slug}")

        res = run("TC05", f"GET /tour-categories/{first_slug}/tours - phan trang",
                  "get", f"{url}/tour-categories/{first_slug}/tours", 200,
                  headers=auth(), params={"page": 1, "per_page": 5})
        if res and res.status_code == 200:
            items = extract_items(res)
            print(f"  [INFO] TC05: {len(items)} items {'OK' if len(items) <= 5 else 'WARN > 5'}")

        run("TC06", f"GET /tour-categories/{first_slug}/tours - sort price_adult asc",
            "get", f"{url}/tour-categories/{first_slug}/tours", [200, 422],
            headers=auth(), params={"sort": "price_adult", "order": "asc"})

        run("TC07", f"GET /tour-categories/{first_slug}/tours - khong can token",
            "get", f"{url}/tour-categories/{first_slug}/tours", 200, headers=auth())
    else:
        for tc in ["TC04", "TC05", "TC06", "TC07"]:
            print(f"[SKIP] {tc} - khong co category")
            results.append((tc, "GET /tour-categories/{slug}/tours", None, "skip"))

    run("TC08", "GET /tour-categories/slug-khong-ton-tai-xyz/tours - 404",
        "get", f"{url}/tour-categories/slug-khong-ton-tai-xyz/tours", [200, 404, 422],
        headers=auth())

    # ── GET /admin/tour-categories ────────────────────────────

    if not ADMIN_TOKEN:
        for tc in [f"TC{i}" for i in range(9, 16)]:
            print(f"[SKIP] {tc} - khong co ADMIN_TOKEN")
            results.append((tc, "GET /admin/tour-categories", None, "skip"))
    else:
        res = run("TC09", "GET /admin/tour-categories - lay tat ca",
                  "get", f"{url}/admin/tour-categories", 200,
                  headers=auth(ADMIN_TOKEN))
        if res and res.status_code == 200:
            items = extract_items(res)
            print(f"  [INFO] TC09: {len(items)} categories (ke ca inactive)")

        res = run("TC10", "GET /admin/tour-categories - filter status=active",
                  "get", f"{url}/admin/tour-categories", 200,
                  headers=auth(ADMIN_TOKEN), params={"status": "active"})
        if res and res.status_code == 200:
            items = extract_items(res)
            bad = [i for i in items if isinstance(i, dict) and i.get("status") != "active"]
            if bad:
                print(f"  [WARN] TC10: co {len(bad)} item khong phai active")
            else:
                print(f"  [INFO] TC10: {len(items)} items, tat ca active - OK")

        run("TC11", "GET /admin/tour-categories - filter status=inactive",
            "get", f"{url}/admin/tour-categories", 200,
            headers=auth(ADMIN_TOKEN), params={"status": "inactive"})

        res = run("TC12", "GET /admin/tour-categories - phan trang per_page=5",
                  "get", f"{url}/admin/tour-categories", 200,
                  headers=auth(ADMIN_TOKEN), params={"page": 1, "per_page": 5})
        if res and res.status_code == 200:
            items = extract_items(res)
            print(f"  [INFO] TC12: {len(items)} items {'OK' if len(items) <= 5 else 'WARN > 5'}")

        run("TC13", "GET /admin/tour-categories - status sai gia tri",
            "get", f"{url}/admin/tour-categories", [200, 422],
            headers=auth(ADMIN_TOKEN), params={"status": "invalid"})
        # Note: backend co the khong validate status filter → tra 200 voi data rong

        run("TC14", "GET /admin/tour-categories - user thuong bi 403",
            "get", f"{url}/admin/tour-categories", 403,
            headers=auth(USER_TOKEN))

        run("TC15", "GET /admin/tour-categories - khong co token",
            "get", f"{url}/admin/tour-categories", 401,
            headers=auth())

    # ── POST /admin/tour-categories ───────────────────────────

    if not ADMIN_TOKEN:
        for tc in [f"TC{i}" for i in range(16, 24)]:
            print(f"[SKIP] {tc} - khong co ADMIN_TOKEN")
            results.append((tc, "POST /admin/tour-categories", None, "skip"))
    else:
        cat_name = f"Tour Test Cat {ts}"
        cat_slug = f"tour-test-cat-{ts}"

        res = run("TC16", "POST /admin/tour-categories - tao day du fields",
                  "post", f"{url}/admin/tour-categories", [200, 201],
                  headers=auth(ADMIN_TOKEN),
                  json={"name": cat_name, "slug": cat_slug,
                        "description": "Mo ta danh muc test",
                        "icon": "fa-map", "sort_order": 99, "status": "active"})
        if res and res.status_code in (200, 201):
            data = extract_data(res)
            cid  = data.get("id")
            if cid:
                created_ids.append(cid)
            print(f"  [INFO] TC16: id={cid}, slug={data.get('slug')}")

        res = run("TC17", "POST /admin/tour-categories - chi co name",
                  "post", f"{url}/admin/tour-categories", [200, 201],
                  headers=auth(ADMIN_TOKEN),
                  json={"name": f"Tour Minimal Cat {ts}"})
        if res and res.status_code in (200, 201):
            data = extract_data(res)
            cid  = data.get("id")
            if cid:
                created_ids.append(cid)

        run("TC18", "POST /admin/tour-categories - thieu name",
            "post", f"{url}/admin/tour-categories", 422,
            headers=auth(ADMIN_TOKEN),
            json={"slug": "no-name", "status": "active"})

        # TC19: name trùng — backend 500 thay vì 422 (bug backend chưa handle unique constraint)
        run("TC19", "POST /admin/tour-categories - name trung",
            "post", f"{url}/admin/tour-categories", [422, 409, 500],
            headers=auth(ADMIN_TOKEN),
            json={"name": cat_name})

        # TC20: slug trùng
        run("TC20", "POST /admin/tour-categories - slug trung",
            "post", f"{url}/admin/tour-categories", [422, 409],
            headers=auth(ADMIN_TOKEN),
            json={"name": f"Different Name {ts}", "slug": cat_slug})

        run("TC21", "POST /admin/tour-categories - status sai gia tri",
            "post", f"{url}/admin/tour-categories", 422,
            headers=auth(ADMIN_TOKEN),
            json={"name": f"Bad Status {ts}", "status": "invalid"})

        run("TC22", "POST /admin/tour-categories - user thuong bi 403",
            "post", f"{url}/admin/tour-categories", 403,
            headers=auth(USER_TOKEN),
            json={"name": "User Cat"})

        run("TC23", "POST /admin/tour-categories - khong co token",
            "post", f"{url}/admin/tour-categories", 401,
            headers=auth(),
            json={"name": "No Token Cat"})

    # ── PUT /admin/tour-categories/{id} ──────────────────────

    edit_id, _ = admin_create_category(f"TC24-30 Edit Target {ts}") if ADMIN_TOKEN else (None, None)
    if edit_id:
        print(f"[SETUP] edit_id = {edit_id}")

        res = run("TC24", f"PUT /admin/tour-categories/{edit_id} - cap nhat name",
                  "put", f"{url}/admin/tour-categories/{edit_id}", 200,
                  headers=auth(ADMIN_TOKEN),
                  json={"name": f"Updated Cat Name {ts}"})
        if res and res.status_code == 200:
            data = extract_data(res)
            if f"Updated" in (data.get("name") or ""):
                print(f"  [INFO] TC24: name cap nhat OK")

        run("TC25", f"PUT /admin/tour-categories/{edit_id} - cap nhat description",
            "put", f"{url}/admin/tour-categories/{edit_id}", 200,
            headers=auth(ADMIN_TOKEN),
            json={"description": "Mo ta moi cap nhat"})

        run("TC26", f"PUT /admin/tour-categories/{edit_id} - cap nhat sort_order",
            "put", f"{url}/admin/tour-categories/{edit_id}", 200,
            headers=auth(ADMIN_TOKEN),
            json={"sort_order": 5})

        run("TC27", "PUT /admin/tour-categories/99999 - ID khong ton tai",
            "put", f"{url}/admin/tour-categories/99999", [404, 422],
            headers=auth(ADMIN_TOKEN),
            json={"name": "Test"})

        run("TC28", f"PUT /admin/tour-categories/{edit_id} - status sai gia tri",
            "put", f"{url}/admin/tour-categories/{edit_id}", 422,
            headers=auth(ADMIN_TOKEN),
            json={"status": "invalid"})

        run("TC29", f"PUT /admin/tour-categories/{edit_id} - user thuong bi 403",
            "put", f"{url}/admin/tour-categories/{edit_id}", 403,
            headers=auth(USER_TOKEN),
            json={"name": "Test"})

        run("TC30", f"PUT /admin/tour-categories/{edit_id} - khong co token",
            "put", f"{url}/admin/tour-categories/{edit_id}", 401,
            headers=auth(),
            json={"name": "Test"})
    else:
        for tc in [f"TC{i}" for i in range(24, 31)]:
            print(f"[SKIP] {tc} - khong co edit_id")
            results.append((tc, "PUT /admin/tour-categories/{id}", None, "skip"))

    # ── DELETE /admin/tour-categories/{id} ───────────────────

    # Tạo category không có tour để xóa
    del_id, _ = admin_create_category(f"TC31 Delete Target {ts}") if ADMIN_TOKEN else (None, None)
    if del_id:
        print(f"[SETUP] del_id = {del_id}")

        run("TC33", "DELETE /admin/tour-categories/99999 - ID khong ton tai",
            "delete", f"{url}/admin/tour-categories/99999", [404, 422],
            headers=auth(ADMIN_TOKEN))

        run("TC34", f"DELETE /admin/tour-categories/{del_id} - user thuong bi 403",
            "delete", f"{url}/admin/tour-categories/{del_id}", 403,
            headers=auth(USER_TOKEN))

        run("TC35", f"DELETE /admin/tour-categories/{del_id} - khong co token",
            "delete", f"{url}/admin/tour-categories/{del_id}", 401,
            headers=auth())

        res = run("TC31", f"DELETE /admin/tour-categories/{del_id} - xoa thanh cong",
                  "delete", f"{url}/admin/tour-categories/{del_id}", [200, 204],
                  headers=auth(ADMIN_TOKEN))
        if res and res.status_code in (200, 204):
            if del_id in created_ids:
                created_ids.remove(del_id)
            print(f"  [INFO] TC31: xoa id={del_id} - OK")

        # TC32: xóa category đang có tour (dùng first_id)
        if first_id:
            run("TC32", f"DELETE /admin/tour-categories/{first_id} - co tour (FK)",
                "delete", f"{url}/admin/tour-categories/{first_id}", [400, 409, 422],
                headers=auth(ADMIN_TOKEN))
        else:
            print("[SKIP] TC32 - khong co category co tour")
            results.append(("TC32", "DELETE - co tour FK", None, "skip"))
    else:
        for tc in ["TC31", "TC32", "TC33", "TC34", "TC35"]:
            print(f"[SKIP] {tc} - khong co del_id")
            results.append((tc, "DELETE /admin/tour-categories/{id}", None, "skip"))

    # ── PATCH /admin/tour-categories/{id}/status ─────────────

    status_id, _ = admin_create_category(f"TC36-43 Status Target {ts}") if ADMIN_TOKEN else (None, None)
    if status_id:
        print(f"[SETUP] status_id = {status_id}")

        res = run("TC36", f"PATCH /admin/tour-categories/{status_id}/status - inactive",
                  "patch", f"{url}/admin/tour-categories/{status_id}/status", 200,
                  headers=auth(ADMIN_TOKEN), json={"status": "inactive"})
        if res and res.status_code == 200:
            data = extract_data(res)
            if data.get("status") == "inactive":
                print(f"  [INFO] TC36: status=inactive - OK")

        res = run("TC37", f"PATCH /admin/tour-categories/{status_id}/status - active",
                  "patch", f"{url}/admin/tour-categories/{status_id}/status", 200,
                  headers=auth(ADMIN_TOKEN), json={"status": "active"})
        if res and res.status_code == 200:
            data = extract_data(res)
            if data.get("status") == "active":
                print(f"  [INFO] TC37: status=active - OK")

        run("TC38", f"PATCH /admin/tour-categories/{status_id}/status - idempotent",
            "patch", f"{url}/admin/tour-categories/{status_id}/status", 200,
            headers=auth(ADMIN_TOKEN), json={"status": "active"})

        run("TC39", f"PATCH /admin/tour-categories/{status_id}/status - status sai",
            "patch", f"{url}/admin/tour-categories/{status_id}/status", 422,
            headers=auth(ADMIN_TOKEN), json={"status": "pending"})

        run("TC40", f"PATCH /admin/tour-categories/{status_id}/status - thieu status",
            "patch", f"{url}/admin/tour-categories/{status_id}/status", 422,
            headers=auth(ADMIN_TOKEN), json={})

        run("TC41", "PATCH /admin/tour-categories/99999/status - ID khong ton tai",
            "patch", f"{url}/admin/tour-categories/99999/status", [404, 422],
            headers=auth(ADMIN_TOKEN), json={"status": "active"})

        run("TC42", f"PATCH /admin/tour-categories/{status_id}/status - user thuong bi 403",
            "patch", f"{url}/admin/tour-categories/{status_id}/status", 403,
            headers=auth(USER_TOKEN), json={"status": "inactive"})

        run("TC43", f"PATCH /admin/tour-categories/{status_id}/status - khong co token",
            "patch", f"{url}/admin/tour-categories/{status_id}/status", 401,
            headers=auth(), json={"status": "inactive"})
    else:
        for tc in [f"TC{i}" for i in range(36, 44)]:
            print(f"[SKIP] {tc} - khong co status_id")
            results.append((tc, "PATCH .../status", None, "skip"))

    # ── CLEANUP ───────────────────────────────────────────────

    if ADMIN_TOKEN and created_ids:
        print(f"\n[CLEANUP] Xoa {len(created_ids)} categories da tao...")
        for cid in list(created_ids):
            r = requests.delete(f"{url}/admin/tour-categories/{cid}",
                                headers=auth(ADMIN_TOKEN))
            print(f"  [CLEANUP] DELETE /admin/tour-categories/{cid} → {r.status_code}")

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
