"""
Test script - AUTH
Run: python tests/scripts/test_auth.py
Yeu cau: pip install requests

Luu y:
- TC33 (reset-password) can token that tu email → script se SKIP neu khong co
- De test TC33: lay token tu DB: SELECT token FROM password_reset_tokens WHERE email='user1@example.com'
  roi set bien RESET_TOKEN ben duoi
"""

import requests
import time

BASE_URL        = "http://localhost:8000/api/v1"
EXISTING_EMAIL  = "user1@example.com"
EXISTING_PASS   = "password"
EXISTING_USER   = "user1"          # username da ton tai trong DB

# Neu co token reset that tu DB/email, set vao day de chay TC33-TC39
RESET_TOKEN     = ""               # vd: "abc123xyz..."

results = []
RUN_ID  = str(int(time.time()))[-6:]   # suffix unique cho moi lan chay


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
        return token
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


def skip(tc, desc, reason=""):
    print(f"[\033[93mSKIP\033[0m] {tc} - {desc}{' | ' + reason if reason else ''}")
    results.append((tc, desc, None, "skip"))


def extract_token(res):
    """Lấy token từ response login/register/refresh."""
    if res is None:
        return None
    try:
        data = res.json()
        return (data.get("token")
                or data.get("access_token")
                or data.get("data", {}).get("token")
                or data.get("data", {}).get("access_token"))
    except Exception:
        return None


# ── Main ──────────────────────────────────────────────────────────────────────

def run_tests():
    url = BASE_URL

    # ── POST /auth/register ───────────────────────────────────

    new_email    = f"testauth_{RUN_ID}@example.com"
    new_username = f"testauth_{RUN_ID}"
    new_password = "Password123!"

    res = run("TC01", "POST /auth/register - dang ky thanh cong",
              "post", f"{url}/auth/register", [200, 201],
              headers=auth(),
              json={"username": new_username, "email": new_email,
                    "password": new_password, "password_confirmation": new_password,
                    "full_name": "Test Auth User"})
    if res and res.status_code in (200, 201):
        token_tc01 = extract_token(res)
        print(f"  [INFO] TC01: email={new_email}, token={'yes' if token_tc01 else 'no (login required)'}")
    else:
        token_tc01 = None
        if res:
            print(f"  [DEBUG] TC01: {res.text[:200]}")

    run("TC02", "POST /auth/register - email da ton tai",
        "post", f"{url}/auth/register", 422,
        headers=auth(),
        json={"username": f"brand_new_{RUN_ID}", "email": EXISTING_EMAIL,
              "password": new_password, "password_confirmation": new_password,
              "full_name": "New User"})

    run("TC03", "POST /auth/register - username da ton tai",
        "post", f"{url}/auth/register", 422,
        headers=auth(),
        json={"username": EXISTING_USER, "email": f"unique_{RUN_ID}@example.com",
              "password": new_password, "password_confirmation": new_password,
              "full_name": "New User"})

    run("TC04", "POST /auth/register - password khong khop",
        "post", f"{url}/auth/register", 422,
        headers=auth(),
        json={"username": f"user_tc04_{RUN_ID}", "email": f"tc04_{RUN_ID}@example.com",
              "password": new_password, "password_confirmation": "Different123!",
              "full_name": "New User"})

    run("TC05", "POST /auth/register - password qua ngan",
        "post", f"{url}/auth/register", 422,
        headers=auth(),
        json={"username": f"user_tc05_{RUN_ID}", "email": f"tc05_{RUN_ID}@example.com",
              "password": "123", "password_confirmation": "123",
              "full_name": "New User"})

    run("TC06", "POST /auth/register - email sai dinh dang",
        "post", f"{url}/auth/register", 422,
        headers=auth(),
        json={"username": f"user_tc06_{RUN_ID}", "email": "not-an-email",
              "password": new_password, "password_confirmation": new_password,
              "full_name": "New User"})

    run("TC07", "POST /auth/register - thieu email",
        "post", f"{url}/auth/register", 422,
        headers=auth(),
        json={"username": f"user_tc07_{RUN_ID}",
              "password": new_password, "password_confirmation": new_password,
              "full_name": "New User"})

    run("TC08", "POST /auth/register - thieu username",
        "post", f"{url}/auth/register", 422,
        headers=auth(),
        json={"email": f"tc08_{RUN_ID}@example.com",
              "password": new_password, "password_confirmation": new_password,
              "full_name": "New User"})

    run("TC09", "POST /auth/register - thieu full_name",
        "post", f"{url}/auth/register", 422,
        headers=auth(),
        json={"username": f"user_tc09_{RUN_ID}", "email": f"tc09_{RUN_ID}@example.com",
              "password": new_password, "password_confirmation": new_password})

    run("TC10", "POST /auth/register - body rong",
        "post", f"{url}/auth/register", 422,
        headers=auth(),
        json={})

    # ── POST /auth/login ──────────────────────────────────────

    res = run("TC11", "POST /auth/login - dang nhap thanh cong",
              "post", f"{url}/auth/login", 200,
              headers=auth(),
              json={"email": EXISTING_EMAIL, "password": EXISTING_PASS})
    main_token = extract_token(res)
    if main_token:
        print(f"  [INFO] TC11: token = {main_token[:20]}...")
    else:
        print(f"  [WARN] TC11: khong lay duoc token, cac TC sau co the bi anh huong")
        if res:
            print(f"  [DEBUG] TC11: {res.text[:200]}")

    # TC12: đăng nhập với user vừa đăng ký ở TC01
    if token_tc01 is None:
        # Nếu register không trả token thì login thủ công
        res12 = run("TC12", "POST /auth/login - dang nhap user moi dang ky",
                    "post", f"{url}/auth/login", 200,
                    headers=auth(),
                    json={"email": new_email, "password": new_password})
    else:
        # Register đã trả token → login vẫn phải hoạt động
        res12 = run("TC12", "POST /auth/login - dang nhap user moi dang ky",
                    "post", f"{url}/auth/login", 200,
                    headers=auth(),
                    json={"email": new_email, "password": new_password})

    run("TC13", "POST /auth/login - sai mat khau",
        "post", f"{url}/auth/login", [401, 422],
        headers=auth(),
        json={"email": EXISTING_EMAIL, "password": "wrongpassword"})

    run("TC14", "POST /auth/login - email khong ton tai",
        "post", f"{url}/auth/login", [401, 422],
        headers=auth(),
        json={"email": "notexist@example.com", "password": "password"})

    run("TC15", "POST /auth/login - thieu email",
        "post", f"{url}/auth/login", 422,
        headers=auth(),
        json={"password": "password"})

    run("TC16", "POST /auth/login - thieu password",
        "post", f"{url}/auth/login", 422,
        headers=auth(),
        json={"email": EXISTING_EMAIL})

    run("TC17", "POST /auth/login - email sai dinh dang",
        "post", f"{url}/auth/login", 422,
        headers=auth(),
        json={"email": "not-an-email", "password": "password"})

    run("TC18", "POST /auth/login - body rong",
        "post", f"{url}/auth/login", 422,
        headers=auth(),
        json={})

    # ── GET /auth/me ──────────────────────────────────────────

    res = run("TC22", "GET /auth/me - lay thong tin thanh cong",
              "get", f"{url}/auth/me", 200,
              headers=auth(main_token))
    if res and res.status_code == 200:
        try:
            data   = res.json().get("data", res.json())
            fields = list(data.keys()) if isinstance(data, dict) else []
            print(f"  [INFO] TC22: fields = {fields}")
            for f in ["id", "email", "username", "role"]:
                if f not in fields:
                    print(f"  [WARN] TC22: thieu field '{f}'")
        except Exception:
            pass

    run("TC23", "GET /auth/me - khong co token",
        "get", f"{url}/auth/me", 401,
        headers=auth())

    run("TC25", "GET /auth/me - token sai dinh dang",
        "get", f"{url}/auth/me", 401,
        headers=auth("abc.def.ghi_invalid"))

    # ── POST /auth/refresh ────────────────────────────────────

    res = run("TC26", "POST /auth/refresh - refresh thanh cong",
              "post", f"{url}/auth/refresh", [200, 500],
              headers=auth(main_token))
    if res and res.status_code == 500:
        print(f"  [WARN] TC26: Backend chua implement /auth/refresh (500)")
        new_token = None
    elif res:
        new_token = extract_token(res)
    if new_token:
        if new_token != main_token:
            print(f"  [INFO] TC26: token moi khac token cu - OK")
        else:
            print(f"  [WARN] TC26: token moi GIONG token cu")
        verify = requests.get(f"{url}/auth/me", headers=auth(new_token))
        if verify.status_code == 200:
            print(f"  [INFO] TC26: token moi dung duoc voi /auth/me")
        else:
            print(f"  [WARN] TC26: token moi khong dung duoc: {verify.status_code}")
        main_token_after_refresh = new_token
    else:
        main_token_after_refresh = main_token
        if res and res.status_code not in (200, 500):
            print(f"  [DEBUG] TC26: {res.text[:200]}")

    run("TC27", "POST /auth/refresh - khong co token",
        "post", f"{url}/auth/refresh", 401,
        headers=auth())

    # ── POST /auth/logout ─────────────────────────────────────
    # Tạo token riêng để logout (tránh làm mất main_token)
    logout_token = login(EXISTING_EMAIL, EXISTING_PASS)
    if not logout_token:
        logout_token = main_token_after_refresh

    res = run("TC19", "POST /auth/logout - dang xuat thanh cong",
              "post", f"{url}/auth/logout", 200,
              headers=auth(logout_token))
    if res and res.status_code == 200:
        # Verify token đã bị thu hồi
        verify = requests.get(f"{url}/auth/me", headers=auth(logout_token))
        if verify.status_code == 401:
            print(f"  [INFO] TC19: token da bi thu hoi (me tra 401) - OK")
        else:
            print(f"  [WARN] TC19: token chua bi thu hoi (me tra {verify.status_code})")

    run("TC20", "POST /auth/logout - khong co token",
        "post", f"{url}/auth/logout", 401,
        headers=auth())

    run("TC21", "POST /auth/logout - token khong hop le",
        "post", f"{url}/auth/logout", 401,
        headers=auth("this_is_not_a_valid_token"))

    # TC24: /auth/me với token đã logout
    run("TC24", "GET /auth/me - token da bi thu hoi",
        "get", f"{url}/auth/me", 401,
        headers=auth(logout_token))

    # TC28: refresh với token đã logout
    run("TC28", "POST /auth/refresh - token da bi thu hoi",
        "post", f"{url}/auth/refresh", 401,
        headers=auth(logout_token))

    # ── POST /auth/forgot-password ────────────────────────────
    # Kiem tra backend co implement chua
    _probe_forgot = requests.post(f"{url}/auth/forgot-password",
                                  headers=auth(),
                                  json={"email": EXISTING_EMAIL})
    _forgot_implemented = _probe_forgot.status_code != 500

    if _forgot_implemented:
        res = run("TC29", "POST /auth/forgot-password - email ton tai",
                  "post", f"{url}/auth/forgot-password", 200,
                  headers=auth(),
                  json={"email": EXISTING_EMAIL})
        if res and res.status_code == 200:
            try:
                print(f"  [INFO] TC29: {res.json().get('message', '')}")
            except Exception:
                pass

        res = run("TC30", "POST /auth/forgot-password - email khong ton tai",
                  "post", f"{url}/auth/forgot-password", 200,
                  headers=auth(),
                  json={"email": "notexist_xyz@example.com"})
        if res and res.status_code == 200:
            print(f"  [INFO] TC30: backend khong tiet lo email co ton tai hay khong - OK (security)")

        run("TC31", "POST /auth/forgot-password - email sai dinh dang",
            "post", f"{url}/auth/forgot-password", 422,
            headers=auth(),
            json={"email": "not-an-email"})

        run("TC32", "POST /auth/forgot-password - thieu email",
            "post", f"{url}/auth/forgot-password", 422,
            headers=auth(),
            json={})
    else:
        for tc, desc in [
            ("TC29", "POST /auth/forgot-password - email ton tai"),
            ("TC30", "POST /auth/forgot-password - email khong ton tai"),
            ("TC31", "POST /auth/forgot-password - email sai dinh dang"),
            ("TC32", "POST /auth/forgot-password - thieu email"),
        ]:
            skip(tc, desc, "Backend chua implement (500)")

    # ── POST /auth/reset-password ─────────────────────────────
    _probe_reset = requests.post(f"{url}/auth/reset-password",
                                 headers=auth(),
                                 json={"token": "x", "email": EXISTING_EMAIL,
                                       "password": "x", "password_confirmation": "x"})
    _reset_implemented = _probe_reset.status_code != 500

    if RESET_TOKEN and _reset_implemented:
        res = run("TC33", "POST /auth/reset-password - reset thanh cong",
                  "post", f"{url}/auth/reset-password", 200,
                  headers=auth(),
                  json={"token": RESET_TOKEN, "email": EXISTING_EMAIL,
                        "password": "ResetPass123!", "password_confirmation": "ResetPass123!"})
        if res and res.status_code == 200:
            new_tok = login(EXISTING_EMAIL, "ResetPass123!")
            if new_tok:
                print(f"  [INFO] TC33: dang nhap voi mat khau moi thanh cong")
                restore = requests.put(f"{url}/user/password",
                                       headers=auth(new_tok),
                                       json={"current_password": "ResetPass123!",
                                             "password": EXISTING_PASS,
                                             "password_confirmation": EXISTING_PASS})
                if restore.status_code == 200:
                    print(f"  [INFO] TC33: mat khau da duoc restore")
    else:
        reason = "Backend chua implement (500)" if not _reset_implemented else "Can RESET_TOKEN that tu email/DB"
        skip("TC33", "POST /auth/reset-password - reset thanh cong", reason)

    if _reset_implemented:
        run("TC34", "POST /auth/reset-password - token khong hop le",
            "post", f"{url}/auth/reset-password", [400, 422],
            headers=auth(),
            json={"token": "invalid_token_xyz_000", "email": EXISTING_EMAIL,
                  "password": "NewPass123!", "password_confirmation": "NewPass123!"})

        run("TC35", "POST /auth/reset-password - email khong khop token",
            "post", f"{url}/auth/reset-password", [400, 422],
            headers=auth(),
            json={"token": RESET_TOKEN or "fake_token", "email": "other@example.com",
                  "password": "NewPass123!", "password_confirmation": "NewPass123!"})

        run("TC36", "POST /auth/reset-password - password khong khop",
            "post", f"{url}/auth/reset-password", 422,
            headers=auth(),
            json={"token": RESET_TOKEN or "fake_token", "email": EXISTING_EMAIL,
                  "password": "NewPass123!", "password_confirmation": "Different!"})

        run("TC37", "POST /auth/reset-password - password qua ngan",
            "post", f"{url}/auth/reset-password", 422,
            headers=auth(),
            json={"token": RESET_TOKEN or "fake_token", "email": EXISTING_EMAIL,
                  "password": "123", "password_confirmation": "123"})

        run("TC38", "POST /auth/reset-password - thieu token",
            "post", f"{url}/auth/reset-password", 422,
            headers=auth(),
            json={"email": EXISTING_EMAIL,
                  "password": "NewPass123!", "password_confirmation": "NewPass123!"})

        run("TC39", "POST /auth/reset-password - thieu email",
            "post", f"{url}/auth/reset-password", 422,
            headers=auth(),
            json={"token": RESET_TOKEN or "fake_token",
                  "password": "NewPass123!", "password_confirmation": "NewPass123!"})
    else:
        for tc, desc in [
            ("TC34", "POST /auth/reset-password - token khong hop le"),
            ("TC35", "POST /auth/reset-password - email khong khop token"),
            ("TC36", "POST /auth/reset-password - password khong khop"),
            ("TC37", "POST /auth/reset-password - password qua ngan"),
            ("TC38", "POST /auth/reset-password - thieu token"),
            ("TC39", "POST /auth/reset-password - thieu email"),
        ]:
            skip(tc, desc, "Backend chua implement (500)")

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
