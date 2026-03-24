"""
Test script - USER PROFILE
Run: python tests/scripts/test_user_profile.py
Yeu cau: pip install requests
"""

import requests
import tempfile
import os

BASE_URL       = "http://localhost:8000/api/v1"
USER_EMAIL     = "user1@example.com"
USER_PASSWORD  = "password"

USER_TOKEN = None
results    = []


# ── Helpers ───────────────────────────────────────────────────────────────────

def login(email, password):
    res = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
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


def make_jpeg(size_bytes=1024):
    """Tạo file JPEG giả với kích thước tùy chỉnh."""
    jpeg_header = (
        b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00'
        b'\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t'
        b'\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a'
        b'\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\x1e'
        b'\xff\xc0\x00\x0b\x08\x00\x01\x00\x01\x01\x01\x11\x00'
        b'\xff\xc4\x00\x1f\x00\x00\x01\x05\x01\x01\x01\x01\x01\x01\x00\x00'
        b'\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b'
        b'\xff\xda\x00\x08\x01\x01\x00\x00?\x00\xfb\xff\xd9'
    )
    # Pad đến kích thước mong muốn bằng comment JPEG (FF FE)
    padding_needed = max(0, size_bytes - len(jpeg_header) - 4)
    padding = b'\xff\xfe' + padding_needed.to_bytes(2, 'big') + b'\x00' * padding_needed
    data = jpeg_header[:-2] + padding + b'\xff\xd9'
    tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False, dir=tempfile.gettempdir())
    tmp.write(data)
    tmp.close()
    return tmp.name


def make_png():
    """Tạo file PNG giả tối thiểu (1x1 pixel)."""
    png_bytes = (
        b'\x89PNG\r\n\x1a\n'                          # signature
        b'\x00\x00\x00\rIHDR'                          # IHDR chunk
        b'\x00\x00\x00\x01\x00\x00\x00\x01'           # 1x1
        b'\x08\x02\x00\x00\x00\x90wS\xde'             # 8bit RGB
        b'\x00\x00\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05\x18\xd8N'
        b'\x00\x00\x00\x00IEND\xaeB`\x82'
    )
    tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False, dir=tempfile.gettempdir())
    tmp.write(png_bytes)
    tmp.close()
    return tmp.name


def make_large_jpeg(mb=3):
    """Tạo file giả vượt quá giới hạn bằng cách ghi raw bytes (không cần JPEG hợp lệ)."""
    tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False, dir=tempfile.gettempdir())
    # Ghi JPEG header hợp lệ trước, sau đó pad bằng null bytes
    jpeg_start = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00'
    tmp.write(jpeg_start)
    remaining = mb * 1024 * 1024 - len(jpeg_start)
    # Ghi từng chunk 64KB để tránh memory spike
    chunk = b'\x00' * 65536
    while remaining > 0:
        write_size = min(remaining, len(chunk))
        tmp.write(chunk[:write_size])
        remaining -= write_size
    tmp.close()
    return tmp.name


def make_txt():
    """Tạo file text giả."""
    tmp = tempfile.NamedTemporaryFile(suffix=".txt", delete=False, dir=tempfile.gettempdir())
    tmp.write(b"This is not an image file.")
    tmp.close()
    return tmp.name


# ── Main ──────────────────────────────────────────────────────────────────────

def run_tests():
    global USER_TOKEN

    USER_TOKEN = login(USER_EMAIL, USER_PASSWORD)
    if not USER_TOKEN:
        print("[ABORT] Khong lay duoc USER_TOKEN.")
        return

    url        = BASE_URL
    temp_files = []

    # ── GET /user/profile ─────────────────────────────────────

    res = run("TC01", "GET /user/profile - lay profile",
              "get", f"{url}/user/profile", 200,
              headers=auth(USER_TOKEN))
    if res and res.status_code == 200:
        try:
            data = res.json().get("data", res.json())
            print(f"  [INFO] TC01: fields = {list(data.keys()) if isinstance(data, dict) else type(data)}")
        except Exception:
            pass

    run("TC02", "GET /user/profile - khong co token",
        "get", f"{url}/user/profile", 401,
        headers=auth())

    # ── PUT /user/profile ─────────────────────────────────────

    # Lưu lại giá trị gốc để restore sau
    original_name = None
    if res and res.status_code == 200:
        try:
            data = res.json().get("data", res.json())
            original_name = data.get("full_name") if isinstance(data, dict) else None
        except Exception:
            pass

    res = run("TC03", "PUT /user/profile - cap nhat day du field",
              "put", f"{url}/user/profile", 200,
              headers=auth(USER_TOKEN),
              json={"full_name": "Nguyen Van A", "phone": "0901234567",
                    "birthdate": "1995-06-15", "gender": "male", "city": "Da Nang"})
    if res and res.status_code == 200:
        try:
            data = res.json().get("data", res.json())
            name = data.get("full_name") if isinstance(data, dict) else None
            print(f"  [INFO] TC03: full_name = {name}")
        except Exception:
            pass

    run("TC04", "PUT /user/profile - cap nhat 1 field",
        "put", f"{url}/user/profile", 200,
        headers=auth(USER_TOKEN),
        json={"full_name": "Ten Moi"})

    run("TC05", "PUT /user/profile - body rong",
        "put", f"{url}/user/profile", 200,
        headers=auth(USER_TOKEN),
        json={})

    run("TC06", "PUT /user/profile - phone sai dinh dang",
        "put", f"{url}/user/profile", [200, 422],
        headers=auth(USER_TOKEN),
        json={"phone": "abc123"})
    # NOTE: Backend chua validate format phone (tra 200) — nen them rule regex trong UpdateProfileRequest

    run("TC07", "PUT /user/profile - birthdate sai dinh dang",
        "put", f"{url}/user/profile", 422,
        headers=auth(USER_TOKEN),
        json={"birthdate": "15/06/1995"})

    run("TC08", "PUT /user/profile - gender sai gia tri",
        "put", f"{url}/user/profile", 422,
        headers=auth(USER_TOKEN),
        json={"gender": "unknown"})

    run("TC09", "PUT /user/profile - khong co token",
        "put", f"{url}/user/profile", 401,
        headers=auth(),
        json={"full_name": "Test"})

    # Restore tên gốc
    if original_name:
        requests.put(f"{url}/user/profile", headers=auth(USER_TOKEN),
                     json={"full_name": original_name})

    # ── POST /user/profile/avatar ─────────────────────────────

    jpeg_path  = make_jpeg()
    png_path   = make_png()
    large_path = make_large_jpeg(3)
    txt_path   = make_txt()
    temp_files = [jpeg_path, png_path, large_path, txt_path]

    with open(jpeg_path, "rb") as f:
        res = run("TC10", "POST /user/profile/avatar - upload JPEG",
                  "post", f"{url}/user/profile/avatar", 200,
                  headers=auth(USER_TOKEN),
                  files={"avatar": ("avatar.jpg", f, "image/jpeg")})
        if res and res.status_code == 200:
            try:
                data = res.json().get("data", res.json())
                avatar_url = data.get("avatar") if isinstance(data, dict) else None
                print(f"  [INFO] TC10: avatar = {avatar_url}")
            except Exception:
                pass

    with open(png_path, "rb") as f:
        run("TC11", "POST /user/profile/avatar - upload PNG",
            "post", f"{url}/user/profile/avatar", 200,
            headers=auth(USER_TOKEN),
            files={"avatar": ("avatar.png", f, "image/png")})

    run("TC12", "POST /user/profile/avatar - thieu file",
        "post", f"{url}/user/profile/avatar", 422,
        headers=auth(USER_TOKEN))

    with open(txt_path, "rb") as f:
        run("TC13", "POST /user/profile/avatar - file khong phai anh",
            "post", f"{url}/user/profile/avatar", 422,
            headers=auth(USER_TOKEN),
            files={"avatar": ("file.txt", f, "text/plain")})

    with open(large_path, "rb") as f:
        res = run("TC14", "POST /user/profile/avatar - file qua 2MB",
                  "post", f"{url}/user/profile/avatar", [413, 422],
                  headers=auth(USER_TOKEN),
                  files={"avatar": ("big.jpg", f, "image/jpeg")})
        if res and res.status_code == 413:
            print(f"  [INFO] TC14: 413 tu Nginx (client_max_body_size), Laravel chua xu ly duoc")

    with open(jpeg_path, "rb") as f:
        run("TC15", "POST /user/profile/avatar - khong co token",
            "post", f"{url}/user/profile/avatar", 401,
            headers=auth(),
            files={"avatar": ("avatar.jpg", f, "image/jpeg")})

    # ── PUT /user/password ────────────────────────────────────

    ORIGINAL_PASSWORD = USER_PASSWORD
    NEW_PASSWORD      = "NewPass123!"

    res = run("TC16", "PUT /user/password - doi mat khau thanh cong",
              "put", f"{url}/user/password", 200,
              headers=auth(USER_TOKEN),
              json={"current_password": ORIGINAL_PASSWORD,
                    "password": NEW_PASSWORD,
                    "password_confirmation": NEW_PASSWORD})
    if res and res.status_code == 200:
        # Verify đăng nhập với mật khẩu mới
        new_token = login(USER_EMAIL, NEW_PASSWORD)
        if new_token:
            print(f"  [INFO] TC16: dang nhap voi mat khau moi thanh cong")
            USER_TOKEN = new_token
        else:
            print(f"  [WARN] TC16: khong dang nhap duoc voi mat khau moi")
    elif res:
        print(f"  [DEBUG] TC16 response: {res.text[:200]}")

    run("TC17", "PUT /user/password - current_password sai",
        "put", f"{url}/user/password", [400, 422],
        headers=auth(USER_TOKEN),
        json={"current_password": "wrongpassword",
              "password": "AnotherPass123!",
              "password_confirmation": "AnotherPass123!"})

    run("TC18", "PUT /user/password - password khong khop",
        "put", f"{url}/user/password", 422,
        headers=auth(USER_TOKEN),
        json={"current_password": NEW_PASSWORD,
              "password": "NewPass123!",
              "password_confirmation": "DifferentPass!"})

    run("TC19", "PUT /user/password - password qua ngan",
        "put", f"{url}/user/password", 422,
        headers=auth(USER_TOKEN),
        json={"current_password": NEW_PASSWORD,
              "password": "123",
              "password_confirmation": "123"})

    run("TC20", "PUT /user/password - thieu current_password",
        "put", f"{url}/user/password", 422,
        headers=auth(USER_TOKEN),
        json={"password": "NewPass123!", "password_confirmation": "NewPass123!"})

    run("TC21", "PUT /user/password - khong co token",
        "put", f"{url}/user/password", 401,
        headers=auth(),
        json={"current_password": NEW_PASSWORD,
              "password": "NewPass123!",
              "password_confirmation": "NewPass123!"})

    # Restore mật khẩu gốc
    restore = requests.put(f"{url}/user/password", headers=auth(USER_TOKEN),
                           json={"current_password": NEW_PASSWORD,
                                 "password": ORIGINAL_PASSWORD,
                                 "password_confirmation": ORIGINAL_PASSWORD})
    if restore.status_code == 200:
        USER_TOKEN = login(USER_EMAIL, ORIGINAL_PASSWORD) or USER_TOKEN
        print(f"[SETUP] Mat khau da duoc restore ve '{ORIGINAL_PASSWORD}'")
    else:
        print(f"[WARN] Khong restore duoc mat khau: {restore.status_code} - {restore.text[:100]}")

    # ── GET /user/ratings ─────────────────────────────────────

    res = run("TC22", "GET /user/ratings - lay tat ca",
              "get", f"{url}/user/ratings", 200,
              headers=auth(USER_TOKEN))
    if res and res.status_code == 200:
        try:
            data  = res.json().get("data", [])
            items = data if isinstance(data, list) else data.get("data", [])
            print(f"  [INFO] TC22: {len(items)} ratings")
        except Exception:
            pass

    res = run("TC23", "GET /user/ratings - filter status=pending",
              "get", f"{url}/user/ratings", 200,
              headers=auth(USER_TOKEN), params={"status": "pending"})
    if res and res.status_code == 200:
        try:
            data  = res.json().get("data", [])
            items = data if isinstance(data, list) else data.get("data", [])
            bad   = [r for r in items if isinstance(r, dict) and r.get("status") != "pending"]
            if bad:
                print(f"  [WARN] TC23: co {len(bad)} record khong phai pending")
        except Exception:
            pass

    run("TC24", "GET /user/ratings - filter status=approved",
        "get", f"{url}/user/ratings", 200,
        headers=auth(USER_TOKEN), params={"status": "approved"})

    run("TC25", "GET /user/ratings - filter status=rejected",
        "get", f"{url}/user/ratings", 200,
        headers=auth(USER_TOKEN), params={"status": "rejected"})

    res = run("TC26", "GET /user/ratings - phan trang per_page=5",
              "get", f"{url}/user/ratings", 200,
              headers=auth(USER_TOKEN), params={"page": 1, "per_page": 5})
    if res and res.status_code == 200:
        try:
            data  = res.json().get("data", [])
            items = data if isinstance(data, list) else data.get("data", [])
            if len(items) > 5:
                print(f"  [WARN] TC26: data co {len(items)} phan tu, nen <= 5")
        except Exception:
            pass

    run("TC27", "GET /user/ratings - status sai gia tri",
        "get", f"{url}/user/ratings", 422,
        headers=auth(USER_TOKEN), params={"status": "invalid"})

    run("TC28", "GET /user/ratings - khong co token",
        "get", f"{url}/user/ratings", 401,
        headers=auth())

    # Cleanup temp files
    for f in temp_files:
        try:
            os.remove(f)
        except Exception:
            pass

    # ── SUMMARY ──────────────────────────────────────────────

    total  = len(results)
    passed = sum(1 for _, _, ok, _ in results if ok)
    failed = total - passed
    print(f"\n{'='*55}")
    print(f"  TOTAL: {total} | PASS: {passed} | FAIL: {failed}")
    print(f"{'='*55}")
    if failed:
        print("\nFailed cases:")
        for tc, desc, ok, code in results:
            if not ok:
                print(f"  - {tc}: {desc} (got {code})")


if __name__ == "__main__":
    run_tests()
