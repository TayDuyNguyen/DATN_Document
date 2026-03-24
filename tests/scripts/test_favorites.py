"""
Test script - FAVORITES
Run: python tests/scripts/test_favorites.py
Yeu cau: pip install requests
"""

import requests

BASE_URL       = "http://localhost:8000/api/v1"
ADMIN_EMAIL    = "admin@example.com"
ADMIN_PASSWORD = "password"
USER_EMAIL     = "user1@example.com"
USER_PASSWORD  = "password"
USER2_EMAIL    = "user2@example.com"
USER2_PASSWORD = "password"

USER_TOKEN  = None
USER2_TOKEN = None
results     = []


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


def get_location_ids(n=10, token=None):
    """Lấy n location_id từ DB."""
    ids = []
    page = 1
    while len(ids) < n:
        res = requests.get(f"{BASE_URL}/locations", headers=auth(token),
                           params={"per_page": 50, "page": page})
        if res.status_code != 200:
            print(f"  [DEBUG] GET /locations status={res.status_code}, body={res.text[:200]}")
            break
        try:
            body  = res.json()
            data  = body.get("data", [])
            items = data if isinstance(data, list) else data.get("data", data.get("items", []))
            if not items:
                print(f"  [DEBUG] GET /locations: data rong, body={str(body)[:200]}")
                break
            ids += [item["id"] for item in items if isinstance(item, dict) and item.get("id")]
            meta      = body.get("meta") or (data if isinstance(data, dict) else {})
            last_page = meta.get("last_page") or meta.get("total_pages") or 1
            if page >= last_page:
                break
            page += 1
        except Exception as e:
            print(f"  [DEBUG] GET /locations parse error: {e}")
            break
    return ids[:n]


def get_current_favorites(token):
    """Lấy danh sách location_id đang trong favorites của user."""
    saved = set()
    page  = 1
    while True:
        res = requests.get(f"{BASE_URL}/user/favorites", headers=auth(token),
                           params={"per_page": 50, "page": page})
        if res.status_code != 200:
            break
        try:
            body  = res.json()
            data  = body.get("data", [])
            items = data if isinstance(data, list) else data.get("data", [])
            if not items:
                break
            for item in items:
                if isinstance(item, dict):
                    lid = item.get("location_id") or item.get("id")
                    if lid:
                        saved.add(lid)
            meta      = body.get("meta") or (data if isinstance(data, dict) else {})
            last_page = meta.get("last_page") or meta.get("total_pages") or 1
            if page >= last_page:
                break
            page += 1
        except Exception:
            break
    return saved


def add_favorite(token, location_id):
    """Thêm location vào favorites, trả về response."""
    return requests.post(f"{BASE_URL}/user/favorites", headers=auth(token),
                         json={"location_id": location_id})


def remove_favorite(token, location_id):
    """Xóa location khỏi favorites."""
    return requests.delete(f"{BASE_URL}/user/favorites/{location_id}", headers=auth(token))


def ensure_not_favorited(token, location_id):
    """Đảm bảo location chưa có trong favorites (xóa nếu có)."""
    remove_favorite(token, location_id)


def ensure_favorited(token, location_id):
    """Đảm bảo location đã có trong favorites (thêm nếu chưa có)."""
    res = add_favorite(token, location_id)
    return res.status_code in (200, 201, 409)


# ── Main ──────────────────────────────────────────────────────────────────────

def run_tests():
    global USER_TOKEN, USER2_TOKEN

    USER_TOKEN  = login(USER_EMAIL, USER_PASSWORD)
    USER2_TOKEN = login(USER2_EMAIL, USER2_PASSWORD)

    if not USER_TOKEN:
        print("[ABORT] Khong lay duoc USER_TOKEN.")
        return

    url      = BASE_URL
    all_locs = get_location_ids(10)
    print(f"[SETUP] Found {len(all_locs)} locations: {all_locs[:5]}")
    if len(all_locs) < 2:
        # Thử lại với token
        all_locs = get_location_ids(10, token=USER_TOKEN)
        print(f"[SETUP] Retry with token: {len(all_locs)} locations: {all_locs[:5]}")
    if len(all_locs) < 2:
        print("[ABORT] Can it nhat 2 locations trong DB.")
        return

    loc1 = all_locs[0]
    loc2 = all_locs[1] if len(all_locs) > 1 else all_locs[0]
    print(f"[SETUP] loc1={loc1}, loc2={loc2}")

    # ── POST /user/favorites ──────────────────────────────────

    # Đảm bảo loc1 chưa trong favorites của user1
    ensure_not_favorited(USER_TOKEN, loc1)

    res = run("TC01", "POST /user/favorites - them thanh cong",
              "post", f"{url}/user/favorites", [200, 201],
              headers=auth(USER_TOKEN),
              json={"location_id": loc1})
    if res and res.status_code in (200, 201):
        try:
            body = res.json()
            data = body.get("data", body)
            print(f"  [INFO] TC01: response data keys = {list(data.keys()) if isinstance(data, dict) else type(data)}")
        except Exception:
            pass

    # Verify favorite_count tăng sau TC01
    loc1_detail = requests.get(f"{url}/locations/{loc1}", headers=auth(USER_TOKEN))
    if loc1_detail.status_code == 200:
        try:
            d = loc1_detail.json().get("data", loc1_detail.json())
            fc = d.get("favorite_count") if isinstance(d, dict) else None
            if fc is not None:
                print(f"  [INFO] TC01: favorite_count sau khi them = {fc}")
        except Exception:
            pass

    # TC02: thêm trùng loc1 (vừa thêm ở TC01)
    run("TC02", "POST /user/favorites - them trung",
        "post", f"{url}/user/favorites", [409, 422],
        headers=auth(USER_TOKEN),
        json={"location_id": loc1})

    run("TC03", "POST /user/favorites - thieu location_id",
        "post", f"{url}/user/favorites", 422,
        headers=auth(USER_TOKEN),
        json={})

    run("TC03b", "POST /user/favorites - location_id khong phai so",
        "post", f"{url}/user/favorites", 422,
        headers=auth(USER_TOKEN),
        json={"location_id": "abc"})

    run("TC04", "POST /user/favorites - location_id khong ton tai",
        "post", f"{url}/user/favorites", [404, 422],
        headers=auth(USER_TOKEN),
        json={"location_id": 99999})

    run("TC05", "POST /user/favorites - khong co token",
        "post", f"{url}/user/favorites", 401,
        headers=auth(),
        json={"location_id": loc1})

    # ── GET /user/favorites ───────────────────────────────────

    res = run("TC06", "GET /user/favorites - lay danh sach",
              "get", f"{url}/user/favorites", 200,
              headers=auth(USER_TOKEN))
    if res and res.status_code == 200:
        try:
            body  = res.json()
            data  = body.get("data", [])
            items = data if isinstance(data, list) else data.get("data", [])
            print(f"  [INFO] TC06: {len(items)} favorites")
            if items and isinstance(items[0], dict):
                print(f"  [INFO] TC06: item keys = {list(items[0].keys())}")
                # Verify có field location và category theo spec
                has_location = "location" in items[0] or "location_id" in items[0]
                has_category = "category" in items[0] or (
                    isinstance(items[0].get("location"), dict) and
                    "category" in items[0]["location"]
                )
                if not has_location:
                    print(f"  [WARN] TC06: thieu field 'location' trong response")
                if not has_category:
                    print(f"  [WARN] TC06: thieu field 'category' trong response")
        except Exception:
            pass

    res = run("TC07", "GET /user/favorites - phan trang per_page=5",
              "get", f"{url}/user/favorites", 200,
              headers=auth(USER_TOKEN),
              params={"page": 1, "per_page": 5})
    if res and res.status_code == 200:
        try:
            data  = res.json().get("data", [])
            items = data if isinstance(data, list) else data.get("data", [])
            if len(items) > 5:
                print(f"  [WARN] TC07: data co {len(items)} phan tu, nen <= 5")
        except Exception:
            pass

    # TC08: user2 chưa lưu gì → danh sách rỗng
    if USER2_TOKEN:
        # Xóa hết favorites của user2 trước
        user2_favs = get_current_favorites(USER2_TOKEN)
        for lid in user2_favs:
            remove_favorite(USER2_TOKEN, lid)

        res = run("TC08", "GET /user/favorites - danh sach rong",
                  "get", f"{url}/user/favorites", 200,
                  headers=auth(USER2_TOKEN))
        if res and res.status_code == 200:
            try:
                data  = res.json().get("data", [])
                items = data if isinstance(data, list) else data.get("data", [])
                if items:
                    print(f"  [WARN] TC08: data co {len(items)} phan tu, nen = 0")
                else:
                    print(f"  [INFO] TC08: data rong, dung")
            except Exception:
                pass
    else:
        print("[SKIP] TC08 - khong co USER2_TOKEN")
        results.append(("TC08", "GET favorites danh sach rong", False, "skip"))

    run("TC09", "GET /user/favorites - khong co token",
        "get", f"{url}/user/favorites", 401,
        headers=auth())

    # ── DELETE /user/favorites/{location_id} ─────────────────

    # Đảm bảo loc2 đã trong favorites của user1 để test delete
    ensure_favorited(USER_TOKEN, loc2)

    # TC12: user2 xóa loc2 của user1 (user2 không có loc2 trong favorites)
    if USER2_TOKEN:
        run("TC12", "DELETE /user/favorites - xoa cua nguoi khac",
            "delete", f"{url}/user/favorites/{loc2}", [403, 404],
            headers=auth(USER2_TOKEN))
    else:
        print("[SKIP] TC12 - khong co USER2_TOKEN")
        results.append(("TC12", "DELETE favorites cua nguoi khac", False, "skip"))

    run("TC11", "DELETE /user/favorites - khong co trong favorites",
        "delete", f"{url}/user/favorites/99999", [404, 422],
        headers=auth(USER_TOKEN))

    # TC11b: location_id tồn tại trong DB nhưng user chưa lưu vào favorites
    loc_not_saved = all_locs[2] if len(all_locs) > 2 else 99998
    ensure_not_favorited(USER_TOKEN, loc_not_saved)
    run("TC11b", "DELETE /user/favorites - chua luu vao favorites",
        "delete", f"{url}/user/favorites/{loc_not_saved}", [404, 422],
        headers=auth(USER_TOKEN))

    run("TC13", "DELETE /user/favorites - khong co token",
        "delete", f"{url}/user/favorites/{loc2}", 401,
        headers=auth())

    res = run("TC10", "DELETE /user/favorites - xoa thanh cong",
              "delete", f"{url}/user/favorites/{loc2}", [200, 204],
              headers=auth(USER_TOKEN))
    if res and res.status_code in (200, 204):
        # Verify đã xóa khỏi danh sách
        check = requests.get(f"{url}/user/favorites", headers=auth(USER_TOKEN))
        if check.status_code == 200:
            try:
                data  = check.json().get("data", [])
                items = data if isinstance(data, list) else data.get("data", [])
                ids   = [i.get("location_id") or i.get("id") for i in items if isinstance(i, dict)]
                if loc2 not in ids:
                    print(f"  [INFO] TC10: loc2={loc2} da bi xoa khoi favorites")
                else:
                    print(f"  [WARN] TC10: loc2={loc2} van con trong favorites sau khi xoa")
            except Exception:
                pass
        # Verify favorite_count giảm
        loc2_detail = requests.get(f"{url}/locations/{loc2}", headers=auth(USER_TOKEN))
        if loc2_detail.status_code == 200:
            try:
                d  = loc2_detail.json().get("data", loc2_detail.json())
                fc = d.get("favorite_count") if isinstance(d, dict) else None
                if fc is not None:
                    print(f"  [INFO] TC10: favorite_count sau khi xoa = {fc}")
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
