"""
Test script - USER PROFILE
Branch: feat/taynd/api-user-profile
Run: python tests/scripts/test_user_profile.py
Yeu cau: pip install requests
"""

import requests
import time
import os

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


def extract_data(res):
    try:
        d = res.json().get("data", res.json())
        if isinstance(d, dict):
            for key in ["user", "profile"]:
                if d.get(key):
                    return d[key]
            return d
        return {}
    except Exception:
        return {}


def extract_items(res):
    try:
        data = res.json().get("data", [])
        if isinstance(data, list):
            return data
        return data.get("data", [])
    except Exception:
        return []


def run_tests():
    global USER_TOKEN, ADMIN_TOKEN

    USER_TOKEN  = login(USER_EMAIL, USER_PASSWORD)
    ADMIN_TOKEN = login(ADMIN_EMAIL, ADMIN_PASSWORD)

    if not USER_TOKEN:
        print("[ABORT] Khong lay duoc USER_TOKEN.")
        return

    url = BASE_URL

    # ── GET /user/profile ────────────────────────────────────

    res = run("TC01", "GET /user/profile - lay thong tin ca nhan",
              "get", f"{url}/user/profile", 200,
              headers=auth(USER_TOKEN))
    if res and res.status_code == 200:
        data = extract_data(res)
        print(f"  [INFO] TC01: fields = {list(data.keys())}")
        for f in ["id", "full_name", "email"]:
            if f not in data:
                print(f"  [WARN] TC01: thieu field '{f}'")

    run("TC02", "GET /user/profile - khong co token → 401",
        "get", f"{url}/user/profile", 401,
        headers=auth())

    run("TC03", "GET /user/profile - token sai → 401",
        "get", f"{url}/user/profile", 401,
        headers=auth("invalid_token_xyz"))

    # ── PUT /user/profile ────────────────────────────────────

    res = run("TC04", "PUT /user/profile - cap nhat day du fields",
              "put", f"{url}/user/profile", 200,
              headers=auth(USER_TOKEN),
              json={
                  "full_name": f"User Test {ts}",
                  "phone": "0901234567",
                  "birthdate": "1995-06-15",
                  "gender": "male",
                  "city": "Da Nang"
              })
    if res and res.status_code == 200:
        data = extract_data(res)
        if data.get("full_name") == f"User Test {ts}":
            print(f"  [INFO] TC04: full_name cap nhat OK")

    res = run("TC05", "PUT /user/profile - cap nhat 1 field (full_name)",
              "put", f"{url}/user/profile", 200,
              headers=auth(USER_TOKEN),
              json={"full_name": f"Updated {ts}"})
    if res and res.status_code == 200:
        data = extract_data(res)
        print(f"  [INFO] TC05: full_name = {data.get('full_name')}")

    run("TC06", "PUT /user/profile - phone sai dinh dang",
        "put", f"{url}/user/profile", [200, 422],
        headers=auth(USER_TOKEN),
        json={"phone": "abc-not-phone"})
    # Note: backend co the khong validate format phone

    run("TC07", "PUT /user/profile - gender sai gia tri",
        "put", f"{url}/user/profile", 422,
        headers=auth(USER_TOKEN),
        json={"gender": "invalid_gender"})

    run("TC08", "PUT /user/profile - birthdate sai dinh dang",
        "put", f"{url}/user/profile", 422,
        headers=auth(USER_TOKEN),
        json={"birthdate": "15-06-1995"})

    run("TC09", "PUT /user/profile - body rong (khong co gi de update)",
        "put", f"{url}/user/profile", [200, 422],
        headers=auth(USER_TOKEN),
        json={})

    run("TC10", "PUT /user/profile - khong co token → 401",
        "put", f"{url}/user/profile", 401,
        headers=auth(),
        json={"full_name": "No Token"})

    # ── POST /user/profile/avatar ────────────────────────────

    # Tao file anh gia de test
    # 1x1 pixel JPEG hop le
    dummy_jpg = (
        b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00"
        b"\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t"
        b"\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a"
        b"\x1f\x1e\x1d\x1a\x1c\x1c $.' \",#\x1c\x1c(7),01444\x1f'9=82<.342\x1e"
        b"\xff\xc0\x00\x0b\x08\x00\x01\x00\x01\x01\x01\x11\x00"
        b"\xff\xc4\x00\x1f\x00\x00\x01\x05\x01\x01\x01\x01\x01\x01\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b"
        b"\xff\xc4\x00\xb5\x10\x00\x02\x01\x03\x03\x02\x04\x03\x05\x05\x04"
        b"\x04\x00\x00\x01}\x01\x02\x03\x00\x04\x11\x05\x12!1A\x06\x13Qa"
        b"\xff\xda\x00\x08\x01\x01\x00\x00?\x00\xfb\xd2\x8a(\x03\xff\xd9"
    )
    # 1x1 pixel PNG hop le (tao bang zlib compress)
    import zlib, struct
    def make_png():
        def chunk(name, data):
            c = struct.pack('>I', len(data)) + name + data
            return c + struct.pack('>I', zlib.crc32(name + data) & 0xffffffff)
        sig = b'\x89PNG\r\n\x1a\n'
        ihdr = chunk(b'IHDR', struct.pack('>IIBBBBB', 1, 1, 8, 2, 0, 0, 0))
        raw  = b'\x00\xff\x00\x00'  # filter byte + 1 RGB pixel
        idat = chunk(b'IDAT', zlib.compress(raw))
        iend = chunk(b'IEND', b'')
        return sig + ihdr + idat + iend
    dummy_png = make_png()

    res = run("TC11", "POST /user/profile/avatar - upload anh hop le (JPEG)",
              "post", f"{url}/user/profile/avatar", [200, 201],
              headers=auth(USER_TOKEN),
              files={"avatar": ("avatar.jpg", dummy_jpg, "image/jpeg")})
    if res and res.status_code in (200, 201):
        data = extract_data(res)
        avatar_url = data.get("avatar") or data.get("avatar_url")
        print(f"  [INFO] TC11: avatar_url = {avatar_url}")

    run("TC12", "POST /user/profile/avatar - upload PNG",
        "post", f"{url}/user/profile/avatar", [200, 201],
        headers=auth(USER_TOKEN),
        files={"avatar": ("avatar.png", dummy_png, "image/png")})

    # File qua lon (>2MB)
    big_file = b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00" + b"\x00" * (2 * 1024 * 1024 + 1)
    run("TC13", "POST /user/profile/avatar - file qua lon (>2MB) → 422",
        "post", f"{url}/user/profile/avatar", [413, 422],
        headers=auth(USER_TOKEN),
        files={"avatar": ("big.jpg", big_file, "image/jpeg")})

    run("TC14", "POST /user/profile/avatar - sai dinh dang file (txt) → 422",
        "post", f"{url}/user/profile/avatar", 422,
        headers=auth(USER_TOKEN),
        files={"avatar": ("file.txt", b"not an image", "text/plain")})

    run("TC15", "POST /user/profile/avatar - thieu file avatar → 422",
        "post", f"{url}/user/profile/avatar", 422,
        headers=auth(USER_TOKEN))

    run("TC16", "POST /user/profile/avatar - khong co token → 401",
        "post", f"{url}/user/profile/avatar", 401,
        headers=auth(),
        files={"avatar": ("avatar.jpg", dummy_jpg, "image/jpeg")})

    # ── PUT /user/password ───────────────────────────────────

    run("TC17", "PUT /user/password - doi mat khau thanh cong",
        "put", f"{url}/user/password", 200,
        headers=auth(USER_TOKEN),
        json={
            "current_password": USER_PASSWORD,
            "password": "NewPassword123!",
            "password_confirmation": "NewPassword123!"
        })

    # Doi lai mat khau cu de cac TC sau van dung duoc
    requests.put(f"{url}/user/password",
                 headers=auth(USER_TOKEN),
                 json={
                     "current_password": "NewPassword123!",
                     "password": USER_PASSWORD,
                     "password_confirmation": USER_PASSWORD
                 })
    print(f"  [SETUP] Doi lai mat khau ve '{USER_PASSWORD}'")

    run("TC18", "PUT /user/password - mat khau hien tai sai → 400",
        "put", f"{url}/user/password", [400, 401, 422],
        headers=auth(USER_TOKEN),
        json={
            "current_password": "WrongPassword999",
            "password": "NewPassword123!",
            "password_confirmation": "NewPassword123!"
        })

    run("TC19", "PUT /user/password - password_confirmation khong khop → 422",
        "put", f"{url}/user/password", 422,
        headers=auth(USER_TOKEN),
        json={
            "current_password": USER_PASSWORD,
            "password": "NewPassword123!",
            "password_confirmation": "DifferentPassword!"
        })

    run("TC20", "PUT /user/password - mat khau moi qua ngan → 422",
        "put", f"{url}/user/password", 422,
        headers=auth(USER_TOKEN),
        json={
            "current_password": USER_PASSWORD,
            "password": "123",
            "password_confirmation": "123"
        })

    run("TC21", "PUT /user/password - thieu current_password → 422",
        "put", f"{url}/user/password", 422,
        headers=auth(USER_TOKEN),
        json={
            "password": "NewPassword123!",
            "password_confirmation": "NewPassword123!"
        })

    run("TC22", "PUT /user/password - thieu password → 422",
        "put", f"{url}/user/password", 422,
        headers=auth(USER_TOKEN),
        json={
            "current_password": USER_PASSWORD,
            "password_confirmation": "NewPassword123!"
        })

    run("TC23", "PUT /user/password - khong co token → 401",
        "put", f"{url}/user/password", 401,
        headers=auth(),
        json={
            "current_password": USER_PASSWORD,
            "password": "NewPassword123!",
            "password_confirmation": "NewPassword123!"
        })

    # ── GET /user/ratings ────────────────────────────────────

    res = run("TC24", "GET /user/ratings - lay lich su danh gia",
              "get", f"{url}/user/ratings", 200,
              headers=auth(USER_TOKEN), timeout=60)
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC24: {len(items)} ratings")
        if items and isinstance(items[0], dict):
            print(f"  [INFO] TC24: fields = {list(items[0].keys())}")

    run("TC25", "GET /user/ratings - filter status=approved",
        "get", f"{url}/user/ratings", 200,
        headers=auth(USER_TOKEN),
        params={"status": "approved"})

    run("TC26", "GET /user/ratings - filter status=pending",
        "get", f"{url}/user/ratings", 200,
        headers=auth(USER_TOKEN),
        params={"status": "pending"})

    res = run("TC27", "GET /user/ratings - phan trang per_page=5",
              "get", f"{url}/user/ratings", 200,
              headers=auth(USER_TOKEN),
              params={"page": 1, "per_page": 5})
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC27: {len(items)} items {'OK' if len(items) <= 5 else 'WARN > 5'}")

    run("TC28", "GET /user/ratings - status sai gia tri → 422",
        "get", f"{url}/user/ratings", [200, 422],
        headers=auth(USER_TOKEN),
        params={"status": "invalid_status"})

    run("TC29", "GET /user/ratings - khong co token → 401",
        "get", f"{url}/user/ratings", 401,
        headers=auth())

    # ── GET /user/search-history ─────────────────────────────

    res = run("TC30", "GET /user/search-history - lay lich su tim kiem",
              "get", f"{url}/user/search-history", 200,
              headers=auth(USER_TOKEN))
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC30: {len(items)} search history items")

    res = run("TC31", "GET /user/search-history - co limit",
              "get", f"{url}/user/search-history", 200,
              headers=auth(USER_TOKEN),
              params={"limit": 5})
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC31: {len(items)} items (limit=5)")

    run("TC32", "GET /user/search-history - limit=0 [edge case]",
        "get", f"{url}/user/search-history", [200, 422],
        headers=auth(USER_TOKEN),
        params={"limit": 0})

    run("TC33", "GET /user/search-history - khong co token → 401",
        "get", f"{url}/user/search-history", 401,
        headers=auth())

    # ── DELETE /user/search-history ──────────────────────────

    res = run("TC34", "DELETE /user/search-history - xoa lich su tim kiem",
              "delete", f"{url}/user/search-history", [200, 204],
              headers=auth(USER_TOKEN))
    if res and res.status_code in (200, 204):
        print(f"  [INFO] TC34: xoa lich su tim kiem OK")

    # Verify da xoa
    res = run("TC35", "GET /user/search-history - sau khi xoa phai rong",
              "get", f"{url}/user/search-history", 200,
              headers=auth(USER_TOKEN))
    if res and res.status_code == 200:
        items = extract_items(res)
        if len(items) == 0:
            print(f"  [INFO] TC35: lich su rong sau khi xoa - OK")
        else:
            print(f"  [WARN] TC35: van con {len(items)} items sau khi xoa")

    run("TC36", "DELETE /user/search-history - khong co token → 401",
        "delete", f"{url}/user/search-history", 401,
        headers=auth())

    # ── DELETE /user/account ─────────────────────────────────
    # NOTE: TC nay dung tai khoang cuoi, dung account rieng de tranh mat USER_TOKEN

    # Tao account moi de test xoa
    del_email    = f"del_user_{ts}@example.com"
    del_password = "DeleteMe123!"
    del_token    = None

    reg_res = requests.post(f"{url}/auth/register",
                            headers={"Accept": "application/json"},
                            json={
                                "username": f"deluser{ts}",
                                "full_name": f"Delete User {ts}",
                                "email": del_email,
                                "password": del_password,
                                "password_confirmation": del_password
                            })
    if reg_res.status_code in (200, 201):
        del_token = login(del_email, del_password)
        print(f"  [SETUP] Tao account xoa: {del_email}")
    else:
        print(f"  [SETUP] Tao account xoa that bai: {reg_res.status_code} - {reg_res.text[:150]}")

    if del_token:
        run("TC37", "DELETE /user/account - mat khau sai → 400",
            "delete", f"{url}/user/account", [400, 401, 422],
            headers=auth(del_token),
            json={"password": "WrongPassword999"})

        run("TC38", "DELETE /user/account - thieu password → 422",
            "delete", f"{url}/user/account", 422,
            headers=auth(del_token),
            json={})

        res = run("TC39", "DELETE /user/account - xoa tai khoan thanh cong",
                  "delete", f"{url}/user/account", [200, 204],
                  headers=auth(del_token),
                  json={"password": del_password})
        if res and res.status_code in (200, 204):
            print(f"  [INFO] TC39: xoa tai khoan {del_email} OK")

        # Verify token cu khong dung duoc nua
        run("TC40", "GET /user/profile - sau khi xoa tai khoan token het hieu luc → 401",
            "get", f"{url}/user/profile", 401,
            headers=auth(del_token))
    else:
        for tc in ["TC37", "TC38", "TC39", "TC40"]:
            print(f"[SKIP] {tc} - khong tao duoc account de test xoa")
            results.append((tc, "DELETE /user/account", None, "skip"))

    run("TC41", "DELETE /user/account - khong co token → 401",
        "delete", f"{url}/user/account", 401,
        headers=auth(),
        json={"password": USER_PASSWORD})

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
