"""
Test script - NOTIFICATIONS (Thong bao)
Run: python tests/scripts/test_notifications.py
Yeu cau: pip install requests
"""

import requests

try:
    import psycopg2
    HAS_PSYCOPG2 = True
except ImportError:
    HAS_PSYCOPG2 = False

BASE_URL      = "http://localhost:8000/api/v1"
USER_EMAIL    = "user1@example.com"
USER_PASSWORD = "password"
USER2_EMAIL   = "user2@example.com"
USER2_PASSWORD = "password"

DB_HOST = "aws-1-ap-northeast-1.pooler.supabase.com"
DB_PORT = "5432"
DB_USER = "postgres.bucmucgvsuawrpompyvu"
DB_PASS = "taybkdn@2004"
DB_NAME = "postgres"

USER_TOKEN  = None
USER2_TOKEN = None
USER1_DB_ID = None
results     = []


# ── Helpers ───────────────────────────────────────────────────────────────────


def insert_unread_notification(user_db_id):
    """Tạo 1 notification chưa đọc cho user qua psycopg2."""
    if not HAS_PSYCOPG2:
        print("[SETUP] psycopg2 chua cai — chay: pip install psycopg2-binary")
        return False
    try:
        conn = psycopg2.connect(
            host=DB_HOST, port=DB_PORT,
            user=DB_USER, password=DB_PASS,
            dbname=DB_NAME, sslmode="require",
            connect_timeout=10
        )
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO notifications (user_id, type, title, content, is_read, created_at) "
            "VALUES (%s, %s, %s, %s, %s, NOW())",
            (user_db_id, "rating_approved", "Test TC08", "Noi dung test TC08/TC09", False)
        )
        conn.commit()
        cur.close()
        conn.close()
        print(f"[SETUP] Da INSERT notification chua doc cho user_id={user_db_id}")
        return True
    except Exception as e:
        print(f"[SETUP] Loi ket noi DB: {e}")
        return False

def login(email, password):
    global USER1_DB_ID
    res = requests.post(f"{BASE_URL}/auth/login",
                        json={"email": email, "password": password},
                        headers={"Accept": "application/json"})
    if res.status_code == 200:
        data  = res.json()
        token = (data.get("token")
                 or data.get("access_token")
                 or data.get("data", {}).get("token")
                 or data.get("data", {}).get("access_token"))
        # Lấy user id từ response để dùng khi insert DB
        user_data = data.get("user") or data.get("data", {}).get("user") or data.get("data", {})
        if isinstance(user_data, dict) and user_data.get("id") and email == USER_EMAIL:
            USER1_DB_ID = user_data.get("id")
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


def get_notifications(token, **params):
    """Lấy danh sách notifications, trả về list items."""
    res = requests.get(f"{BASE_URL}/user/notifications",
                       headers=auth(token), params=params)
    if res.status_code == 200:
        return extract_items(res)
    return []


def get_unread_id(token):
    """Tìm 1 notification chưa đọc (is_read=false/0)."""
    items = get_notifications(token, is_read=0, per_page=50)
    for item in items:
        if isinstance(item, dict) and not item.get("is_read"):
            return item.get("id")
    # Fallback: lấy bất kỳ
    all_items = get_notifications(token, per_page=50)
    for item in all_items:
        if isinstance(item, dict) and not item.get("is_read"):
            return item.get("id")
    return None


def get_read_id(token):
    """Tìm 1 notification đã đọc (is_read=true/1)."""
    items = get_notifications(token, is_read=1, per_page=50)
    for item in items:
        if isinstance(item, dict) and item.get("is_read"):
            return item.get("id")
    return None


def get_any_id(token):
    """Lấy bất kỳ notification ID nào."""
    items = get_notifications(token, per_page=50)
    if items and isinstance(items[0], dict):
        return items[0].get("id")
    return None


# ── Main ──────────────────────────────────────────────────────────────────────

def get_user_id(token):
    """Lay user_id tu /user/profile."""
    res = requests.get(f"{BASE_URL}/user/profile",
                       headers={"Accept": "application/json",
                                "Authorization": f"Bearer {token}"})
    if res.status_code == 200:
        d = res.json().get("data", res.json())
        if isinstance(d, dict):
            return d.get("id") or d.get("user", {}).get("id")
    return None


def send_notification_via_admin(admin_token, user_id, title="Test notification"):
    """Dung admin API tao notification cho user."""
    res = requests.post(f"{BASE_URL}/admin/notifications/send",
                        headers={"Accept": "application/json",
                                 "Authorization": f"Bearer {admin_token}"},
                        json={"user_id": user_id, "type": "system",
                              "title": title, "content": "Setup for test"})
    if res.status_code in (200, 201):
        d = res.json().get("data", res.json())
        nid = d.get("id") or (d.get("notification", {}) or {}).get("id")
        print(f"  [SETUP] Tao notification id={nid} cho user_id={user_id} - OK")
        return nid
    print(f"  [SETUP] Tao notification that bai: {res.status_code} - {res.text[:150]}")
    return None


def run_tests():
    global USER_TOKEN, USER2_TOKEN

    USER_TOKEN  = login(USER_EMAIL, USER_PASSWORD)
    USER2_TOKEN = login(USER2_EMAIL, USER2_PASSWORD)
    ADMIN_TOKEN = login("admin@example.com", "password")

    if not USER_TOKEN:
        print("[ABORT] Khong lay duoc USER_TOKEN.")
        return

    # SETUP: tao notification cho user2 de dung TC12, TC18, TC20
    user2_setup_id = None
    if ADMIN_TOKEN and USER2_TOKEN:
        user2_db_id = get_user_id(USER2_TOKEN)
        if user2_db_id:
            user2_setup_id = send_notification_via_admin(
                ADMIN_TOKEN, user2_db_id, "Notification for user2 test")
            # Tao them 1 cai de TC18 co du data
            send_notification_via_admin(
                ADMIN_TOKEN, user2_db_id, "Notification for user2 test 2")

    url = BASE_URL

    # ── GET /user/notifications ───────────────────────────────

    res = run("TC01", "GET /user/notifications - lay danh sach",
              "get", f"{url}/user/notifications", 200,
              headers=auth(USER_TOKEN))
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC01: {len(items)} notifications")
        if items and isinstance(items[0], dict):
            print(f"  [INFO] TC01: fields = {list(items[0].keys())}")
            for f in ["id", "type", "title", "is_read", "created_at"]:
                if f not in items[0]:
                    print(f"  [WARN] TC01: thieu field '{f}'")

    res = run("TC02", "GET /user/notifications - phan trang per_page=5",
              "get", f"{url}/user/notifications", 200,
              headers=auth(USER_TOKEN), params={"page": 1, "per_page": 5})
    if res and res.status_code == 200:
        items = extract_items(res)
        if len(items) > 5:
            print(f"  [WARN] TC02: tra ve {len(items)} items, nen <= 5")
        else:
            print(f"  [INFO] TC02: {len(items)} items - OK")

    run("TC03", "GET /user/notifications - trang 2",
        "get", f"{url}/user/notifications", 200,
        headers=auth(USER_TOKEN), params={"page": 2, "per_page": 5})

    # TC03b: per_page vượt max — backend có thể trả 422 (validate) hoặc 200 (tự clamp)
    res = run("TC03b", "GET /user/notifications - per_page=200 (vuot max)",
              "get", f"{url}/user/notifications", [200, 422],
              headers=auth(USER_TOKEN), params={"per_page": 200})
    if res and res.status_code == 422:
        print(f"  [INFO] TC03b: backend tra 422 khi per_page > 100 - OK (validate dung)")
    elif res and res.status_code == 200:
        items = extract_items(res)
        if len(items) <= 100:
            print(f"  [INFO] TC03b: backend tu gioi han <= 100 items - OK")
        else:
            print(f"  [WARN] TC03b: tra ve {len(items)} items, nen co gioi han")

    res = run("TC04", "GET /user/notifications - filter is_read=0",
              "get", f"{url}/user/notifications", 200,
              headers=auth(USER_TOKEN), params={"is_read": 0})
    if res and res.status_code == 200:
        items = extract_items(res)
        bad = [i for i in items if isinstance(i, dict) and i.get("is_read") not in (False, 0)]
        if bad:
            print(f"  [WARN] TC04: co {len(bad)} item co is_read != false/0")
        else:
            print(f"  [INFO] TC04: {len(items)} items, tat ca is_read=false - OK")

    res = run("TC05", "GET /user/notifications - filter is_read=1",
              "get", f"{url}/user/notifications", 200,
              headers=auth(USER_TOKEN), params={"is_read": 1})
    if res and res.status_code == 200:
        items = extract_items(res)
        bad = [i for i in items if isinstance(i, dict) and i.get("is_read") not in (True, 1)]
        if bad:
            print(f"  [WARN] TC05: co {len(bad)} item co is_read != true/1")
        else:
            print(f"  [INFO] TC05: {len(items)} items, tat ca is_read=true - OK")

    res = run("TC06", "GET /user/notifications - sap xep moi nhat len dau",
              "get", f"{url}/user/notifications", 200,
              headers=auth(USER_TOKEN))
    if res and res.status_code == 200:
        items = extract_items(res)
        if len(items) >= 2:
            first = items[0].get("created_at", "")
            last  = items[-1].get("created_at", "")
            if first >= last:
                print(f"  [INFO] TC06: thu tu DESC - OK ({first[:10]} >= {last[:10]})")
            else:
                print(f"  [WARN] TC06: thu tu khong phai DESC ({first[:10]} < {last[:10]})")
        else:
            print(f"  [INFO] TC06: chi co {len(items)} item, khong the verify thu tu")

    run("TC07", "GET /user/notifications - khong co token",
        "get", f"{url}/user/notifications", 401,
        headers=auth())

    # ── PATCH /user/notifications/{id}/read ──────────────────

    # Tìm notification chưa đọc để test TC08
    unread_id = get_unread_id(USER_TOKEN)

    # Nếu không có unread → tự INSERT vào DB
    if not unread_id:
        print(f"[SETUP] Khong co notification chua doc, thu INSERT vao DB...")
        db_id = USER1_DB_ID
        if not db_id:
            profile_res = requests.get(f"{url}/user/profile", headers=auth(USER_TOKEN))
            if profile_res.status_code == 200:
                pdata = profile_res.json().get("data", profile_res.json())
                db_id = pdata.get("id") if isinstance(pdata, dict) else None
        if db_id:
            inserted = insert_unread_notification(db_id)
            if inserted:
                unread_id = get_unread_id(USER_TOKEN)

    if unread_id:
        print(f"[SETUP] unread_id = {unread_id}")
    else:
        print("[SETUP] Khong the tao notification chua doc — TC08/TC09 se SKIP")
        print(f"[HINT] Chay SQL: INSERT INTO notifications (user_id,type,title,content,is_read,created_at,updated_at)"
              f" VALUES ({USER1_DB_ID or 'USER_ID'},'rating_approved','Test','Test',0,NOW(),NOW());")

    if unread_id:
        res = run("TC08", f"PATCH /user/notifications/{unread_id}/read - danh dau da doc",
                  "patch", f"{url}/user/notifications/{unread_id}/read", 200,
                  headers=auth(USER_TOKEN))
        if res and res.status_code == 200:
            try:
                data = res.json().get("data", res.json())
                is_read = data.get("is_read") if isinstance(data, dict) else None
                read_at = data.get("read_at") if isinstance(data, dict) else None
                if is_read in (True, 1):
                    print(f"  [INFO] TC08: is_read=true - OK")
                else:
                    print(f"  [WARN] TC08: is_read={is_read}, ky vong true")
                if read_at:
                    print(f"  [INFO] TC08: read_at={read_at} - OK")
                else:
                    print(f"  [WARN] TC08: read_at=null sau khi danh dau doc")
            except Exception:
                pass

        # TC09: đánh dấu lại (idempotent) — dùng cùng ID vừa đọc
        res = run("TC09", f"PATCH /user/notifications/{unread_id}/read - danh dau lai (idempotent)",
                  "patch", f"{url}/user/notifications/{unread_id}/read", 200,
                  headers=auth(USER_TOKEN))
        if res and res.status_code == 200:
            print(f"  [INFO] TC09: idempotent OK")
    else:
        for tc, desc in [("TC08", "danh dau da doc"), ("TC09", "idempotent")]:
            print(f"[SKIP] {tc} - PATCH .../read - {desc} | khong co unread notification")
            results.append((tc, f"PATCH .../read - {desc}", None, "skip"))

    run("TC10", "PATCH /user/notifications/99999/read - ID khong ton tai",
        "patch", f"{url}/user/notifications/99999/read", 404,
        headers=auth(USER_TOKEN))

    run("TC11", "PATCH /user/notifications/abc/read - ID khong hop le",
        "patch", f"{url}/user/notifications/abc/read", [404, 422],
        headers=auth(USER_TOKEN))

    # TC12: thông báo của user khác — dùng notification vừa tạo cho user2
    if USER2_TOKEN:
        user2_notif_id = user2_setup_id or get_any_id(USER2_TOKEN)
        if user2_notif_id:
            run("TC12", f"PATCH /user/notifications/{user2_notif_id}/read - thong bao user khac",
                "patch", f"{url}/user/notifications/{user2_notif_id}/read", [403, 404],
                headers=auth(USER_TOKEN))
        else:
            print("[SKIP] TC12 - user2 khong co notification")
            results.append(("TC12", "PATCH .../read - thong bao user khac", None, "skip"))
    else:
        print("[SKIP] TC12 - khong lay duoc USER2_TOKEN")
        results.append(("TC12", "PATCH .../read - thong bao user khac", None, "skip"))

    run("TC13", "PATCH /user/notifications/{id}/read - khong co token",
        "patch", f"{url}/user/notifications/1/read", 401,
        headers=auth())

    # ── PATCH /user/notifications/read-all ───────────────────

    res = run("TC14", "PATCH /user/notifications/read-all - danh dau tat ca da doc",
              "patch", f"{url}/user/notifications/read-all", 200,
              headers=auth(USER_TOKEN))
    if res and res.status_code == 200:
        # Verify: không còn thông báo chưa đọc
        unread_after = get_notifications(USER_TOKEN, is_read=0)
        if len(unread_after) == 0:
            print(f"  [INFO] TC14: sau read-all, is_read=0 tra ve 0 items - OK")
        else:
            print(f"  [WARN] TC14: van con {len(unread_after)} notification chua doc sau read-all")

    # TC15: gọi lại khi không còn gì chưa đọc (idempotent)
    res = run("TC15", "PATCH /user/notifications/read-all - khong co gi chua doc (idempotent)",
              "patch", f"{url}/user/notifications/read-all", 200,
              headers=auth(USER_TOKEN))
    if res and res.status_code == 200:
        print(f"  [INFO] TC15: idempotent OK")

    run("TC16", "PATCH /user/notifications/read-all - khong co token",
        "patch", f"{url}/user/notifications/read-all", 401,
        headers=auth())

    # ── DELETE /user/notifications/{id} ──────────────────────

    # Lấy notification để xóa (ưu tiên chưa đọc)
    all_items = get_notifications(USER_TOKEN, per_page=50)
    unread_items = [i for i in all_items if isinstance(i, dict) and not i.get("is_read")]
    read_items   = [i for i in all_items if isinstance(i, dict) and i.get("is_read")]

    delete_unread_id = unread_items[0].get("id") if unread_items else None
    delete_read_id   = read_items[0].get("id")   if read_items   else None

    # Nếu không có unread, lấy bất kỳ
    if not delete_unread_id and all_items:
        delete_unread_id = all_items[0].get("id") if isinstance(all_items[0], dict) else None

    if delete_unread_id:
        res = run("TC17", f"DELETE /user/notifications/{delete_unread_id} - xoa chua doc",
                  "delete", f"{url}/user/notifications/{delete_unread_id}", [200, 204],
                  headers=auth(USER_TOKEN))
        if res and res.status_code in (200, 204):
            # Verify: GET list không còn ID này
            all_after = get_notifications(USER_TOKEN, per_page=100)
            ids_after = [i.get("id") for i in all_after if isinstance(i, dict)]
            if delete_unread_id not in ids_after:
                print(f"  [INFO] TC17: ID {delete_unread_id} khong con trong list - OK")
            else:
                print(f"  [WARN] TC17: ID {delete_unread_id} van con trong list sau khi xoa")
    else:
        print("[SKIP] TC17 - khong co notification de xoa")
        results.append(("TC17", "DELETE - xoa chua doc", None, "skip"))

    if delete_read_id and delete_read_id != delete_unread_id:
        run("TC18", f"DELETE /user/notifications/{delete_read_id} - xoa da doc",
            "delete", f"{url}/user/notifications/{delete_read_id}", [200, 204],
            headers=auth(USER_TOKEN))
    else:
        # Tao them notification cho user1 de xoa
        user1_db_id = USER1_DB_ID or get_user_id(USER_TOKEN)
        extra_id = None
        if ADMIN_TOKEN and user1_db_id:
            extra_id = send_notification_via_admin(
                ADMIN_TOKEN, user1_db_id, "Extra notification for TC18")
        if extra_id:
            run("TC18", f"DELETE /user/notifications/{extra_id} - xoa da doc",
                "delete", f"{url}/user/notifications/{extra_id}", [200, 204],
                headers=auth(USER_TOKEN))
        else:
            remaining = get_notifications(USER_TOKEN, per_page=50)
            if remaining and isinstance(remaining[0], dict):
                second_id = remaining[0].get("id")
                run("TC18", f"DELETE /user/notifications/{second_id} - xoa da doc",
                    "delete", f"{url}/user/notifications/{second_id}", [200, 204],
                    headers=auth(USER_TOKEN))
            else:
                print("[SKIP] TC18 - khong con notification de xoa")
                results.append(("TC18", "DELETE - xoa da doc", None, "skip"))

    run("TC19", "DELETE /user/notifications/99999 - ID khong ton tai",
        "delete", f"{url}/user/notifications/99999", [404, 422],
        headers=auth(USER_TOKEN))

    # TC20: xóa thông báo của user khác — dùng notification vừa tạo cho user2
    if USER2_TOKEN:
        user2_notif_id = user2_setup_id or get_any_id(USER2_TOKEN)
        if user2_notif_id:
            run("TC20", f"DELETE /user/notifications/{user2_notif_id} - thong bao user khac",
                "delete", f"{url}/user/notifications/{user2_notif_id}", [403, 404],
                headers=auth(USER_TOKEN))
        else:
            print("[SKIP] TC20 - user2 khong co notification")
            results.append(("TC20", "DELETE - thong bao user khac", None, "skip"))
    else:
        print("[SKIP] TC20 - khong lay duoc USER2_TOKEN")
        results.append(("TC20", "DELETE - thong bao user khac", None, "skip"))

    run("TC21", "DELETE /user/notifications/{id} - khong co token",
        "delete", f"{url}/user/notifications/1", 401,
        headers=auth())

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
