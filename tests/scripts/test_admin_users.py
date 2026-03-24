"""
Test script - ADMIN USERS (Quan ly nguoi dung)
Run: python tests/scripts/test_admin_users.py
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
ADMIN_ID    = None
results     = []
created_user_ids = []


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
        if not ok:
            try:
                print(f"  [DEBUG] body = {res.json()}")
            except Exception:
                print(f"  [DEBUG] raw  = {res.text[:300]}")
        results.append((tc, desc, ok, res.status_code))
        return res
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
        return d if isinstance(d, dict) else {}
    except Exception:
        return {}


def get_admin_id(token):
    res = requests.get(f"{BASE_URL}/auth/me", headers=auth(token))
    if res.status_code == 200:
        data = extract_data(res)
        return data.get("id")
    return None


def get_target_user_id(admin_token, exclude_id=None):
    res = requests.get(f"{BASE_URL}/admin/users",
                       headers=auth(admin_token),
                       params={"role": "user", "per_page": 20})
    if res.status_code == 200:
        items = extract_items(res)
        for item in items:
            if isinstance(item, dict):
                uid = item.get("id")
                if uid and uid != exclude_id:
                    return uid
    return None


def register_test_user(suffix="del"):
    ts = int(time.time())
    body = {
        "username":              f"testdel_{suffix}_{ts}",
        "email":                 f"testdel_{suffix}_{ts}@example.com",
        "password":              "Password123!",
        "password_confirmation": "Password123!",
        "full_name":             f"Test Del {suffix}",
    }
    res = requests.post(f"{BASE_URL}/auth/register",
                        json=body, headers={"Accept": "application/json"})
    if res.status_code in (200, 201):
        data = res.json()
        uid  = (data.get("data", {}).get("user", {}).get("id")
                or data.get("data", {}).get("id")
                or data.get("user", {}).get("id")
                or data.get("id"))
        if uid:
            created_user_ids.append(uid)
            print(f"[SETUP] Registered test user id={uid} ({body['email']})")
        return uid
    print(f"[SETUP] Register failed: {res.status_code} - {res.text[:200]}")
    return None


def run_tests():
    global USER_TOKEN, ADMIN_TOKEN, ADMIN_ID

    USER_TOKEN  = login(USER_EMAIL, USER_PASSWORD)
    ADMIN_TOKEN = login(ADMIN_EMAIL, ADMIN_PASSWORD)

    if not USER_TOKEN:
        print("[ABORT] Khong lay duoc USER_TOKEN.")
        return
    if not ADMIN_TOKEN:
        print("[ABORT] Khong lay duoc ADMIN_TOKEN.")
        return

    ADMIN_ID = get_admin_id(ADMIN_TOKEN)
    print(f"[SETUP] ADMIN_ID = {ADMIN_ID}")

    url = BASE_URL

    #  GET /admin/users 

    res = run("TC01", "GET /admin/users - lay danh sach",
              "get", f"{url}/admin/users", 200,
              headers=auth(ADMIN_TOKEN))
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC01: {len(items)} users")
        if items and isinstance(items[0], dict):
            print(f"  [INFO] TC01: fields = {list(items[0].keys())}")
            for f in ["id", "email", "username", "role", "status"]:
                if f not in items[0]:
                    print(f"  [WARN] TC01: thieu field '{f}'")

    res = run("TC02", "GET /admin/users - phan trang per_page=5",
              "get", f"{url}/admin/users", 200,
              headers=auth(ADMIN_TOKEN), params={"page": 1, "per_page": 5})
    if res and res.status_code == 200:
        items = extract_items(res)
        if len(items) > 5:
            print(f"  [WARN] TC02: tra ve {len(items)} items, nen <= 5")
        else:
            print(f"  [INFO] TC02: {len(items)} items - OK")

    run("TC03", "GET /admin/users - trang 2",
        "get", f"{url}/admin/users", 200,
        headers=auth(ADMIN_TOKEN), params={"page": 2, "per_page": 5})

    res = run("TC04", "GET /admin/users - search ?q=user",
              "get", f"{url}/admin/users", 200,
              headers=auth(ADMIN_TOKEN), params={"q": "user"})
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC04: {len(items)} ket qua cho q=user")

    res = run("TC05", "GET /admin/users - search khong co ket qua",
              "get", f"{url}/admin/users", 200,
              headers=auth(ADMIN_TOKEN), params={"q": "xyzkhongtontai999abc"})
    if res and res.status_code == 200:
        items = extract_items(res)
        if len(items) == 0:
            print(f"  [INFO] TC05: data=[] - OK")
        else:
            print(f"  [WARN] TC05: tra ve {len(items)} items, ky vong 0")

    res = run("TC06", "GET /admin/users - filter role=user",
              "get", f"{url}/admin/users", 200,
              headers=auth(ADMIN_TOKEN), params={"role": "user"})
    if res and res.status_code == 200:
        items = extract_items(res)
        bad = [i for i in items if isinstance(i, dict) and i.get("role") != "user"]
        if bad:
            print(f"  [WARN] TC06: co {len(bad)} item khong phai role=user")
        else:
            print(f"  [INFO] TC06: {len(items)} items, tat ca role=user - OK")

    res = run("TC07", "GET /admin/users - filter role=admin",
              "get", f"{url}/admin/users", 200,
              headers=auth(ADMIN_TOKEN), params={"role": "admin"})
    if res and res.status_code == 200:
        items = extract_items(res)
        bad = [i for i in items if isinstance(i, dict) and i.get("role") != "admin"]
        if bad:
            print(f"  [WARN] TC07: co {len(bad)} item khong phai role=admin")
        else:
            print(f"  [INFO] TC07: {len(items)} items, tat ca role=admin - OK")

    res = run("TC08", "GET /admin/users - filter status=active",
              "get", f"{url}/admin/users", 200,
              headers=auth(ADMIN_TOKEN), params={"status": "active"})
    if res and res.status_code == 200:
        items = extract_items(res)
        bad = [i for i in items if isinstance(i, dict) and i.get("status") != "active"]
        if bad:
            print(f"  [WARN] TC08: co {len(bad)} item khong phai status=active")
        else:
            print(f"  [INFO] TC08: {len(items)} items, tat ca status=active - OK")

    res = run("TC09", "GET /admin/users - filter status=banned",
              "get", f"{url}/admin/users", 200,
              headers=auth(ADMIN_TOKEN), params={"status": "banned"})
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC09: {len(items)} banned users")

    res = run("TC10", "GET /admin/users - ket hop role=user&status=active",
              "get", f"{url}/admin/users", 200,
              headers=auth(ADMIN_TOKEN), params={"role": "user", "status": "active"})
    if res and res.status_code == 200:
        items = extract_items(res)
        bad = [i for i in items if isinstance(i, dict)
               and (i.get("role") != "user" or i.get("status") != "active")]
        if bad:
            print(f"  [WARN] TC10: co {len(bad)} item sai filter")
        else:
            print(f"  [INFO] TC10: {len(items)} items, tat ca role=user&status=active - OK")

    run("TC11", "GET /admin/users - role sai gia tri",
        "get", f"{url}/admin/users", 422,
        headers=auth(ADMIN_TOKEN), params={"role": "superadmin"})

    run("TC12", "GET /admin/users - status sai gia tri",
        "get", f"{url}/admin/users", 422,
        headers=auth(ADMIN_TOKEN), params={"status": "suspended"})

    res = run("TC13", "GET /admin/users - per_page=200 vuot max",
              "get", f"{url}/admin/users", [200, 422],
              headers=auth(ADMIN_TOKEN), params={"per_page": 200})
    if res and res.status_code == 422:
        print(f"  [INFO] TC13: backend validate per_page max - OK")
    elif res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC13: tra ve {len(items)} items {'(<= 100 OK)' if len(items) <= 100 else '(WARN > 100)'}")

    run("TC14", "GET /admin/users - user thuong bi 403",
        "get", f"{url}/admin/users", 403,
        headers=auth(USER_TOKEN))

    run("TC15", "GET /admin/users - khong co token",
        "get", f"{url}/admin/users", 401,
        headers=auth())

    #  GET /admin/users/{id} 

    target_id = get_target_user_id(ADMIN_TOKEN, exclude_id=ADMIN_ID)
    print(f"[SETUP] target_user_id = {target_id}")

    if target_id:
        res = run("TC16", f"GET /admin/users/{target_id} - chi tiet thanh cong",
                  "get", f"{url}/admin/users/{target_id}", 200,
                  headers=auth(ADMIN_TOKEN))
        if res and res.status_code == 200:
            data = extract_data(res)
            print(f"  [INFO] TC16: fields = {list(data.keys())}")
            for f in ["id", "email", "username", "full_name", "role", "status"]:
                if f not in data:
                    print(f"  [WARN] TC16: thieu field '{f}'")
    else:
        print("[SKIP] TC16 - khong tim duoc target_user_id")
        results.append(("TC16", "GET /admin/users/{id}", None, "skip"))

    if ADMIN_ID:
        res = run("TC17", f"GET /admin/users/{ADMIN_ID} - chi tiet admin user",
                  "get", f"{url}/admin/users/{ADMIN_ID}", 200,
                  headers=auth(ADMIN_TOKEN))
        if res and res.status_code == 200:
            data = extract_data(res)
            if data.get("role") == "admin":
                print(f"  [INFO] TC17: role=admin - OK")
            else:
                print(f"  [WARN] TC17: role={data.get('role')}, ky vong admin")
    else:
        print("[SKIP] TC17 - khong co ADMIN_ID")
        results.append(("TC17", "GET /admin/users/{id} admin", None, "skip"))

    run("TC18", "GET /admin/users/99999 - ID khong ton tai",
        "get", f"{url}/admin/users/99999", [404, 422],
        headers=auth(ADMIN_TOKEN))

    run("TC19", f"GET /admin/users/{target_id or 1} - user thuong bi 403",
        "get", f"{url}/admin/users/{target_id or 1}", 403,
        headers=auth(USER_TOKEN))

    run("TC20", f"GET /admin/users/{target_id or 1} - khong co token",
        "get", f"{url}/admin/users/{target_id or 1}", 401,
        headers=auth())

    #  PATCH /admin/users/{id}/status 

    status_target = target_id
    if not status_target:
        for tc in [f"TC{i}" for i in range(21, 30)]:
            print(f"[SKIP] {tc} - khong co target_user_id")
            results.append((tc, "PATCH .../status", None, "skip"))
    else:
        res = run("TC21", f"PATCH /admin/users/{status_target}/status - activebanned",
                  "patch", f"{url}/admin/users/{status_target}/status", 200,
                  headers=auth(ADMIN_TOKEN), json={"status": "banned"})
        if res and res.status_code == 200:
            data = extract_data(res)
            if data.get("status") == "banned":
                print(f"  [INFO] TC21: status=banned - OK")
            else:
                print(f"  [WARN] TC21: status={data.get('status')}, ky vong banned")

        res = run("TC22", f"PATCH /admin/users/{status_target}/status - bannedactive",
                  "patch", f"{url}/admin/users/{status_target}/status", 200,
                  headers=auth(ADMIN_TOKEN), json={"status": "active"})
        if res and res.status_code == 200:
            data = extract_data(res)
            if data.get("status") == "active":
                print(f"  [INFO] TC22: status=active - OK")

        run("TC23", f"PATCH /admin/users/{status_target}/status - idempotent",
            "patch", f"{url}/admin/users/{status_target}/status", 200,
            headers=auth(ADMIN_TOKEN), json={"status": "active"})

        run("TC24", f"PATCH /admin/users/{status_target}/status - status sai",
            "patch", f"{url}/admin/users/{status_target}/status", 422,
            headers=auth(ADMIN_TOKEN), json={"status": "suspended"})

        run("TC25", f"PATCH /admin/users/{status_target}/status - thieu status",
            "patch", f"{url}/admin/users/{status_target}/status", 422,
            headers=auth(ADMIN_TOKEN), json={})

        if ADMIN_ID:
            run("TC26", f"PATCH /admin/users/{ADMIN_ID}/status - admin tu ban minh",
                "patch", f"{url}/admin/users/{ADMIN_ID}/status", [200, 403, 422],
                headers=auth(ADMIN_TOKEN), json={"status": "banned"})
            # Restore lại active + re-login
            requests.patch(f"{url}/admin/users/{ADMIN_ID}/status",
                           headers=auth(ADMIN_TOKEN), json={"status": "active"})
            new_token = login(ADMIN_EMAIL, ADMIN_PASSWORD)
            if new_token:
                ADMIN_TOKEN = new_token
        else:
            print("[SKIP] TC26 - khong co ADMIN_ID")
            results.append(("TC26", "Admin tu ban minh", None, "skip"))

        run("TC27", "PATCH /admin/users/99999/status - ID khong ton tai",
            "patch", f"{url}/admin/users/99999/status", [404, 422],
            headers=auth(ADMIN_TOKEN), json={"status": "banned"})

        run("TC28", f"PATCH /admin/users/{status_target}/status - user thuong bi 403",
            "patch", f"{url}/admin/users/{status_target}/status", 403,
            headers=auth(USER_TOKEN), json={"status": "banned"})

        run("TC29", f"PATCH /admin/users/{status_target}/status - khong co token",
            "patch", f"{url}/admin/users/{status_target}/status", 401,
            headers=auth(), json={"status": "banned"})

    #  PATCH /admin/users/{id}/role 

    role_target = get_target_user_id(ADMIN_TOKEN, exclude_id=ADMIN_ID)
    if not role_target:
        for tc in [f"TC{i}" for i in range(30, 39)]:
            print(f"[SKIP] {tc} - khong co role_target")
            results.append((tc, "PATCH .../role", None, "skip"))
    else:
        print(f"[SETUP] role_target_id = {role_target}")

        res = run("TC30", f"PATCH /admin/users/{role_target}/role - useradmin",
                  "patch", f"{url}/admin/users/{role_target}/role", 200,
                  headers=auth(ADMIN_TOKEN), json={"role": "admin"})
        if res and res.status_code == 200:
            data = extract_data(res)
            if data.get("role") == "admin":
                print(f"  [INFO] TC30: role=admin - OK")

        res = run("TC31", f"PATCH /admin/users/{role_target}/role - adminuser",
                  "patch", f"{url}/admin/users/{role_target}/role", 200,
                  headers=auth(ADMIN_TOKEN), json={"role": "user"})
        if res and res.status_code == 200:
            data = extract_data(res)
            if data.get("role") == "user":
                print(f"  [INFO] TC31: role=user - OK")

        run("TC32", f"PATCH /admin/users/{role_target}/role - idempotent",
            "patch", f"{url}/admin/users/{role_target}/role", 200,
            headers=auth(ADMIN_TOKEN), json={"role": "user"})

        run("TC33", f"PATCH /admin/users/{role_target}/role - role sai gia tri",
            "patch", f"{url}/admin/users/{role_target}/role", 422,
            headers=auth(ADMIN_TOKEN), json={"role": "superadmin"})

        run("TC34", f"PATCH /admin/users/{role_target}/role - thieu role",
            "patch", f"{url}/admin/users/{role_target}/role", 422,
            headers=auth(ADMIN_TOKEN), json={})

        if ADMIN_ID:
            # TC35: dùng role_target thay vì ADMIN_ID để tránh mất quyền admin
            # Chỉ test self-action nếu không còn cách nào khác
            run("TC35", f"PATCH /admin/users/{ADMIN_ID}/role - admin tu doi role minh",
                "patch", f"{url}/admin/users/{ADMIN_ID}/role", [200, 403, 422],
                headers=auth(ADMIN_TOKEN), json={"role": "user"})
            # QUAN TRỌNG: restore lại role=admin ngay lập tức
            restore = requests.patch(f"{url}/admin/users/{ADMIN_ID}/role",
                                     headers=auth(ADMIN_TOKEN), json={"role": "admin"})
            if restore.status_code == 200:
                print(f"  [INFO] TC35: da restore role=admin cho ADMIN_ID={ADMIN_ID}")
                # Re-login để lấy token mới với role=admin
                new_token = login(ADMIN_EMAIL, ADMIN_PASSWORD)
                if new_token:
                    ADMIN_TOKEN = new_token
                    print(f"  [INFO] TC35: da re-login lay token moi voi role=admin")
            else:
                print(f"  [WARN] TC35: restore role that bai ({restore.status_code})"
                      f" — ADMIN bi mat quyen, cac TC sau se 403!")
        else:
            print("[SKIP] TC35 - khong co ADMIN_ID")
            results.append(("TC35", "Admin tu doi role minh", None, "skip"))

        run("TC36", "PATCH /admin/users/99999/role - ID khong ton tai",
            "patch", f"{url}/admin/users/99999/role", [404, 422, 403],
            headers=auth(ADMIN_TOKEN), json={"role": "admin"})

        run("TC37", f"PATCH /admin/users/{role_target}/role - user thuong bi 403",
            "patch", f"{url}/admin/users/{role_target}/role", 403,
            headers=auth(USER_TOKEN), json={"role": "admin"})

        run("TC38", f"PATCH /admin/users/{role_target}/role - khong co token",
            "patch", f"{url}/admin/users/{role_target}/role", 401,
            headers=auth(), json={"role": "admin"})

    #  DELETE /admin/users/{id} 

    delete_id = register_test_user("tc39")

    if not delete_id:
        for tc in ["TC39", "TC40", "TC41", "TC42", "TC43"]:
            print(f"[SKIP] {tc} - khong tao duoc test user")
            results.append((tc, "DELETE /admin/users/{id}", None, "skip"))
    else:
        run("TC40", "DELETE /admin/users/99999 - ID khong ton tai",
            "delete", f"{url}/admin/users/99999", [404, 422, 403],
            headers=auth(ADMIN_TOKEN))

        if ADMIN_ID:
            run("TC41", f"DELETE /admin/users/{ADMIN_ID} - admin tu xoa minh",
                "delete", f"{url}/admin/users/{ADMIN_ID}", [403, 422],
                headers=auth(ADMIN_TOKEN))
        else:
            print("[SKIP] TC41 - khong co ADMIN_ID")
            results.append(("TC41", "Admin tu xoa minh", None, "skip"))

        run("TC42", f"DELETE /admin/users/{delete_id} - user thuong bi 403",
            "delete", f"{url}/admin/users/{delete_id}", 403,
            headers=auth(USER_TOKEN))

        run("TC43", f"DELETE /admin/users/{delete_id} - khong co token",
            "delete", f"{url}/admin/users/{delete_id}", 401,
            headers=auth())

        res = run("TC39", f"DELETE /admin/users/{delete_id} - xoa thanh cong",
                  "delete", f"{url}/admin/users/{delete_id}", [200, 204],
                  headers=auth(ADMIN_TOKEN))
        if res and res.status_code in (200, 204):
            check = requests.get(f"{url}/admin/users/{delete_id}",
                                 headers=auth(ADMIN_TOKEN))
            if check.status_code == 404:
                print(f"  [INFO] TC39: GET lai  404 - OK")
            else:
                print(f"  [WARN] TC39: GET lai  {check.status_code}, ky vong 404")
            if delete_id in created_user_ids:
                created_user_ids.remove(delete_id)

    #  CLEANUP 

    if ADMIN_TOKEN and created_user_ids:
        print(f"\n[CLEANUP] Xoa {len(created_user_ids)} test users con lai...")
        for uid in list(created_user_ids):
            r = requests.delete(f"{url}/admin/users/{uid}", headers=auth(ADMIN_TOKEN))
            print(f"  [CLEANUP] DELETE /admin/users/{uid}  {r.status_code}")

    #  SUMMARY 

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
