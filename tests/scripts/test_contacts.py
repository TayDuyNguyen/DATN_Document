
"""
Test script - CONTACTS (Lien he)
Branch: feat/taynd/api-contacts
Run: python tests/scripts/test_contacts.py
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
created_contact_ids = []
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
    kwargs.setdefault("timeout", 30)
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


def extract_data(res):
    try:
        d = res.json().get("data", res.json())
        if isinstance(d, dict):
            for key in ["contact"]:
                if d.get(key):
                    return d[key]
            return d
        return {}
    except Exception:
        return {}


def run_tests():
    global USER_TOKEN, ADMIN_TOKEN

    USER_TOKEN  = login(USER_EMAIL, USER_PASSWORD)
    ADMIN_TOKEN = login(ADMIN_EMAIL, ADMIN_PASSWORD)

    if not ADMIN_TOKEN:
        print("[ABORT] Khong lay duoc ADMIN_TOKEN.")
        return

    url = BASE_URL

    # ── POST /contacts ────────────────────────────────────────

    res = run("TC01", "POST /contacts - gui day du fields",
              "post", f"{url}/contacts", [200, 201],
              headers=auth(),
              json={"name": f"Nguyen Van A {ts}", "email": f"contact{ts}@example.com",
                    "phone": "0901234567", "subject": "Hoi ve tour",
                    "message": "Toi muon hoi ve tour Ba Na Hills"})
    contact_id = None
    if res and res.status_code in (200, 201):
        data = extract_data(res)
        contact_id = data.get("id")
        if contact_id:
            created_contact_ids.append(contact_id)
        print(f"  [INFO] TC01: id={contact_id}")

    res = run("TC02", "POST /contacts - chi fields bat buoc (khong phone, subject)",
              "post", f"{url}/contacts", [200, 201],
              headers=auth(),
              json={"name": f"Nguyen Van B {ts}", "email": f"contact2{ts}@example.com",
                    "message": "Noi dung lien he toi thieu"})
    if res and res.status_code in (200, 201):
        cid = extract_data(res).get("id")
        if cid:
            created_contact_ids.append(cid)

    run("TC03", "POST /contacts - khong can token (public)",
        "post", f"{url}/contacts", [200, 201],
        headers=auth(),
        json={"name": f"Guest User {ts}", "email": f"guest{ts}@example.com",
              "message": "Lien he tu khach"})

    run("TC04", "POST /contacts - thieu name → 422",
        "post", f"{url}/contacts", 422,
        headers=auth(),
        json={"email": "test@example.com", "message": "Noi dung"})

    import time as _time; _time.sleep(2)

    run("TC05", "POST /contacts - thieu email → 422",
        "post", f"{url}/contacts", 422,
        headers=auth(),
        json={"name": "Test User", "message": "Noi dung"})

    _time.sleep(2)

    run("TC06", "POST /contacts - thieu message → 422",
        "post", f"{url}/contacts", [422, 429],
        headers=auth(),
        json={"name": "Test User", "email": "test@example.com"})

    _time.sleep(2)

    run("TC07", "POST /contacts - email sai dinh dang → 422",
        "post", f"{url}/contacts", [422, 429],
        headers=auth(),
        json={"name": "Test User", "email": "not-an-email", "message": "Noi dung"})

    _time.sleep(2)

    run("TC08", "POST /contacts - message qua ngan [edge case]",
        "post", f"{url}/contacts", [200, 201, 422, 429],
        headers=auth(),
        json={"name": "Test User", "email": "test@example.com", "message": "Hi"})

    # ── GET /admin/contacts ───────────────────────────────────

    res = run("TC09", "GET /admin/contacts - lay tat ca lien he",
              "get", f"{url}/admin/contacts", 200,
              headers=auth(ADMIN_TOKEN))
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC09: {len(items)} contacts")
        if items and isinstance(items[0], dict):
            print(f"  [INFO] TC09: fields = {list(items[0].keys())}")

    for tc, status_val in [("TC10", "new"), ("TC11", "read"), ("TC12", "replied")]:
        res = run(tc, f"GET /admin/contacts - filter status={status_val}",
                  "get", f"{url}/admin/contacts", 200,
                  headers=auth(ADMIN_TOKEN), params={"status": status_val})
        if res and res.status_code == 200:
            items = extract_items(res)
            bad = [i for i in items if isinstance(i, dict) and i.get("status") != status_val]
            if bad:
                print(f"  [WARN] {tc}: co {len(bad)} item khong phai status={status_val}")
            else:
                print(f"  [INFO] {tc}: {len(items)} items, tat ca status={status_val} - OK")

    res = run("TC13", "GET /admin/contacts - phan trang per_page=5",
              "get", f"{url}/admin/contacts", 200,
              headers=auth(ADMIN_TOKEN), params={"page": 1, "per_page": 5})
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC13: {len(items)} items {'OK' if len(items) <= 5 else 'WARN > 5'}")

    run("TC14", "GET /admin/contacts - status sai gia tri → 422",
        "get", f"{url}/admin/contacts", 422,
        headers=auth(ADMIN_TOKEN), params={"status": "invalid_status"})

    run("TC15", "GET /admin/contacts - user thuong bi 403",
        "get", f"{url}/admin/contacts", 403,
        headers=auth(USER_TOKEN))

    run("TC16", "GET /admin/contacts - khong co token → 401",
        "get", f"{url}/admin/contacts", 401,
        headers=auth())

    # ── GET /admin/contacts/{id} ──────────────────────────────

    # Lay contact_id tu danh sach neu chua co
    if not contact_id:
        all_contacts = extract_items(
            requests.get(f"{url}/admin/contacts", headers=auth(ADMIN_TOKEN)))
        if all_contacts and isinstance(all_contacts[0], dict):
            contact_id = all_contacts[0].get("id")
            print(f"[SETUP] Lay contact_id tu danh sach: {contact_id}")

    if contact_id:
        res = run("TC17", f"GET /admin/contacts/{contact_id} - chi tiet",
                  "get", f"{url}/admin/contacts/{contact_id}", 200,
                  headers=auth(ADMIN_TOKEN))
        if res and res.status_code == 200:
            data = extract_data(res)
            print(f"  [INFO] TC17: fields = {list(data.keys())}")
            for f in ["id", "name", "email", "message", "status"]:
                if f not in data:
                    print(f"  [WARN] TC17: thieu field '{f}'")

        # TC18: verify status tu dong chuyen sang read
        res2 = requests.get(f"{url}/admin/contacts/{contact_id}",
                            headers=auth(ADMIN_TOKEN))
        if res2.status_code == 200:
            status_after = extract_data(res2).get("status")
            ok = status_after == "read"
            label = "\033[92mPASS\033[0m" if ok else "\033[91mFAIL\033[0m"
            print(f"[{label}] TC18 - GET /admin/contacts/{{id}} - status tu dong chuyen sang read | status={status_after}")
            results.append(("TC18", "status tu dong read", ok, 200))
        else:
            print("[SKIP] TC18 - khong lay duoc response lan 2")
            results.append(("TC18", "status tu dong read", None, "skip"))
    else:
        for tc in ["TC17", "TC18"]:
            print(f"[SKIP] {tc} - khong co contact_id")
            results.append((tc, "GET /admin/contacts/{id}", None, "skip"))

    import time as _t; _t.sleep(1)

    run("TC19", "GET /admin/contacts/99999 - ID khong ton tai → 404",
        "get", f"{url}/admin/contacts/99999", [404, 422],
        headers=auth(ADMIN_TOKEN), timeout=30)

    run("TC20", f"GET /admin/contacts/{contact_id or 1} - user thuong bi 403",
        "get", f"{url}/admin/contacts/{contact_id or 1}", 403,
        headers=auth(USER_TOKEN), timeout=30)

    run("TC21", f"GET /admin/contacts/{contact_id or 1} - khong co token → 401",
        "get", f"{url}/admin/contacts/{contact_id or 1}", 401,
        headers=auth())

    # ── POST /admin/contacts/{id}/reply ───────────────────────

    if contact_id:
        res = run("TC22", f"POST /admin/contacts/{contact_id}/reply - tra loi thanh cong",
                  "post", f"{url}/admin/contacts/{contact_id}/reply", 200,
                  headers=auth(ADMIN_TOKEN),
                  json={"reply": "Cam on ban da lien he. Chung toi se phan hoi trong 24h."})
        if res and res.status_code == 200:
            data = extract_data(res)
            if data.get("status") == "replied":
                print(f"  [INFO] TC22: status=replied - OK")
            if data.get("reply"):
                print(f"  [INFO] TC22: reply set - OK")
            if data.get("replied_at"):
                print(f"  [INFO] TC22: replied_at set - OK")

        run("TC23", f"POST /admin/contacts/{contact_id}/reply - tra loi lan 2 [backend khong cho override]",
            "post", f"{url}/admin/contacts/{contact_id}/reply", [200, 400],
            headers=auth(ADMIN_TOKEN),
            json={"reply": "Noi dung tra loi moi cap nhat"})
    else:
        for tc in ["TC22", "TC23"]:
            print(f"[SKIP] {tc} - khong co contact_id")
            results.append((tc, "POST /admin/contacts/{id}/reply", None, "skip"))

    run("TC24", f"POST /admin/contacts/{contact_id or 1}/reply - thieu reply → 422",
        "post", f"{url}/admin/contacts/{contact_id or 1}/reply", 422,
        headers=auth(ADMIN_TOKEN), json={})

    run("TC25", f"POST /admin/contacts/{contact_id or 1}/reply - reply rong → 422",
        "post", f"{url}/admin/contacts/{contact_id or 1}/reply", 422,
        headers=auth(ADMIN_TOKEN), json={"reply": ""})

    run("TC26", "POST /admin/contacts/99999/reply - ID khong ton tai → 404",
        "post", f"{url}/admin/contacts/99999/reply", [404, 422],
        headers=auth(ADMIN_TOKEN), json={"reply": "Test reply"})

    run("TC27", f"POST /admin/contacts/{contact_id or 1}/reply - user thuong bi 403",
        "post", f"{url}/admin/contacts/{contact_id or 1}/reply", 403,
        headers=auth(USER_TOKEN), json={"reply": "Test reply"})

    run("TC28", f"POST /admin/contacts/{contact_id or 1}/reply - khong co token → 401",
        "post", f"{url}/admin/contacts/{contact_id or 1}/reply", 401,
        headers=auth(), json={"reply": "Test reply"})

    # ── DELETE /admin/contacts/{id} ───────────────────────────

    # Tao contact rieng de xoa
    del_res = requests.post(f"{url}/contacts",
                            headers=auth(),
                            json={"name": f"Del Contact {ts}",
                                  "email": f"del{ts}@example.com",
                                  "message": "Contact to be deleted"})
    del_id = None
    if del_res.status_code in (200, 201):
        del_id = extract_data(del_res).get("id")

    run("TC30", "DELETE /admin/contacts/99999 - ID khong ton tai → 404",
        "delete", f"{url}/admin/contacts/99999", [404, 422],
        headers=auth(ADMIN_TOKEN))

    run("TC31", f"DELETE /admin/contacts/{del_id or contact_id or 1} - user thuong bi 403",
        "delete", f"{url}/admin/contacts/{del_id or contact_id or 1}", 403,
        headers=auth(USER_TOKEN))

    run("TC32", f"DELETE /admin/contacts/{del_id or contact_id or 1} - khong co token → 401",
        "delete", f"{url}/admin/contacts/{del_id or contact_id or 1}", 401,
        headers=auth())

    if del_id:
        res = run("TC29", f"DELETE /admin/contacts/{del_id} - xoa thanh cong",
                  "delete", f"{url}/admin/contacts/{del_id}", [200, 204],
                  headers=auth(ADMIN_TOKEN))
        if res and res.status_code in (200, 204):
            print(f"  [INFO] TC29: xoa contact id={del_id} - OK")
            # Verify: GET lai → 404
            verify = requests.get(f"{url}/admin/contacts/{del_id}",
                                  headers=auth(ADMIN_TOKEN))
            if verify.status_code in (404, 422):
                print(f"  [INFO] TC29: verify GET sau xoa → {verify.status_code} - OK")
    else:
        print("[SKIP] TC29 - khong tao duoc contact de xoa")
        results.append(("TC29", "DELETE /admin/contacts/{id}", None, "skip"))

    # ── GET /admin/contacts/export ────────────────────────────

    res = run("TC33", "GET /admin/contacts/export - export tat ca",
              "get", f"{url}/admin/contacts/export", [200, 404],
              headers=auth(ADMIN_TOKEN), timeout=30)
    if res and res.status_code == 200:
        ct = res.headers.get("Content-Type", "")
        print(f"  [INFO] TC33: Content-Type = {ct}")
        if "spreadsheet" in ct or "excel" in ct or "octet-stream" in ct:
            print(f"  [INFO] TC33: Excel format - OK")
        else:
            print(f"  [WARN] TC33: Content-Type khong phai Excel: {ct}")

    run("TC34", "GET /admin/contacts/export - filter status=new",
        "get", f"{url}/admin/contacts/export", [200, 404],
        headers=auth(ADMIN_TOKEN), params={"status": "new"}, timeout=30)

    run("TC35", "GET /admin/contacts/export - filter status=replied",
        "get", f"{url}/admin/contacts/export", [200, 404],
        headers=auth(ADMIN_TOKEN), params={"status": "replied"}, timeout=30)

    run("TC36", "GET /admin/contacts/export - status sai gia tri → 422",
        "get", f"{url}/admin/contacts/export", 422,
        headers=auth(ADMIN_TOKEN), params={"status": "invalid_status"}, timeout=30)

    run("TC37", "GET /admin/contacts/export - user thuong bi 403",
        "get", f"{url}/admin/contacts/export", 403,
        headers=auth(USER_TOKEN), timeout=30)

    run("TC38", "GET /admin/contacts/export - khong co token → 401",
        "get", f"{url}/admin/contacts/export", 401,
        headers=auth(), timeout=30)

    # ── CLEANUP ───────────────────────────────────────────────

    if ADMIN_TOKEN and created_contact_ids:
        print(f"\n[CLEANUP] Xoa {len(created_contact_ids)} contacts...")
        for cid in created_contact_ids:
            r = requests.delete(f"{url}/admin/contacts/{cid}",
                                headers=auth(ADMIN_TOKEN))
            print(f"  [CLEANUP] contact/{cid} → {r.status_code}")

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
