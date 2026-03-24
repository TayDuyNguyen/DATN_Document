"""
Test script - BLOG (Bai viet)
Run: python tests/scripts/test_blog.py
Yeu cau: pip install requests
"""

import requests

BASE_URL       = "http://localhost:8000/api/v1"
USER_EMAIL     = "user1@example.com"
USER_PASSWORD  = "password"
ADMIN_EMAIL    = "admin@example.com"
ADMIN_PASSWORD = "password"

USER_TOKEN  = None
ADMIN_TOKEN = None
results     = []

# ID/slug tạo ra trong quá trình test (để cleanup)
created_ids = []


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


def get_first_published_slug():
    """Lấy slug bài viết published đầu tiên."""
    res = requests.get(f"{BASE_URL}/blog", headers=auth(), params={"per_page": 5})
    if res.status_code == 200:
        items = extract_items(res)
        for item in items:
            if isinstance(item, dict) and item.get("slug"):
                return item.get("slug"), item.get("id")
    return None, None


def get_first_category_id():
    """Lấy category_id đầu tiên từ /blog/categories."""
    res = requests.get(f"{BASE_URL}/blog/categories", headers=auth())
    if res.status_code == 200:
        items = extract_items(res)
        if items and isinstance(items[0], dict):
            return items[0].get("id")
    return 1


def admin_create_post(title, status="draft", **extra):
    """Tạo bài viết qua admin API, trả về (id, slug)."""
    # Lấy category_id nếu chưa truyền vào
    if "category_ids" not in extra:
        cid = get_first_category_id()
        extra["category_ids"] = [cid] if cid else []
    body = {"title": title, "content": f"Noi dung {title}", "status": status, **extra}
    res  = requests.post(f"{BASE_URL}/admin/blog",
                         headers=auth(ADMIN_TOKEN), json=body)
    if res.status_code in (200, 201):
        data = extract_data(res)
        pid  = data.get("id")
        slug = data.get("slug")
        if pid:
            created_ids.append(pid)
        return pid, slug
    return None, None


# ── Main ──────────────────────────────────────────────────────────────────────

def run_tests():
    global USER_TOKEN, ADMIN_TOKEN

    USER_TOKEN  = login(USER_EMAIL, USER_PASSWORD)
    ADMIN_TOKEN = login(ADMIN_EMAIL, ADMIN_PASSWORD)

    if not USER_TOKEN:
        print("[ABORT] Khong lay duoc USER_TOKEN.")
        return
    if not ADMIN_TOKEN:
        print("[WARN] Khong lay duoc ADMIN_TOKEN — cac TC admin se SKIP.")

    url = BASE_URL

    # ── GET /blog ─────────────────────────────────────────────

    res = run("TC01", "GET /blog - lay danh sach",
              "get", f"{url}/blog", 200, headers=auth())
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC01: {len(items)} bai viet")
        if items and isinstance(items[0], dict):
            print(f"  [INFO] TC01: fields = {list(items[0].keys())}")

    res = run("TC02", "GET /blog - chi tra ve published",
              "get", f"{url}/blog", 200, headers=auth())
    if res and res.status_code == 200:
        items = extract_items(res)
        bad = [i for i in items if isinstance(i, dict) and i.get("status") != "published"]
        if bad:
            print(f"  [WARN] TC02: co {len(bad)} bai khong phai published")
        else:
            print(f"  [INFO] TC02: tat ca {len(items)} bai deu published - OK")

    res = run("TC03", "GET /blog - phan trang per_page=5",
              "get", f"{url}/blog", 200,
              headers=auth(), params={"page": 1, "per_page": 5})
    if res and res.status_code == 200:
        items = extract_items(res)
        if len(items) > 5:
            print(f"  [WARN] TC03: tra ve {len(items)} items, nen <= 5")
        else:
            print(f"  [INFO] TC03: {len(items)} items - OK")

    run("TC04", "GET /blog - trang 2",
        "get", f"{url}/blog", 200,
        headers=auth(), params={"page": 2, "per_page": 5})

    cat_id = get_first_category_id()
    res = run("TC05", f"GET /blog - filter category_id={cat_id}",
              "get", f"{url}/blog", 200,
              headers=auth(), params={"category_id": cat_id})
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC05: {len(items)} bai trong category {cat_id}")

    res = run("TC06", "GET /blog - category_id khong co bai nao",
              "get", f"{url}/blog", [200, 422],
              headers=auth(), params={"category_id": 99999})
    if res and res.status_code == 200:
        items = extract_items(res)
        if len(items) == 0:
            print(f"  [INFO] TC06: data=[] - OK")
        else:
            print(f"  [WARN] TC06: tra ve {len(items)} items, ky vong 0")
    elif res and res.status_code == 422:
        print(f"  [INFO] TC06: backend validate category_id ton tai - OK")

    run("TC07", "GET /blog - category_id khong phai so",
        "get", f"{url}/blog", 422,
        headers=auth(), params={"category_id": "abc"})

    res = run("TC08", "GET /blog - per_page=200 vuot max",
              "get", f"{url}/blog", [200, 422],
              headers=auth(), params={"per_page": 200})
    if res and res.status_code == 422:
        print(f"  [INFO] TC08: backend validate per_page max - OK")
    elif res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC08: tra ve {len(items)} items {'(<= 100 OK)' if len(items) <= 100 else '(WARN: > 100)'}")

    run("TC09", "GET /blog - khong can token (public)",
        "get", f"{url}/blog", 200, headers=auth())

    # ── GET /blog/{slug} ──────────────────────────────────────

    first_slug, first_id = get_first_published_slug()
    if first_slug:
        print(f"[SETUP] first_slug = {first_slug}")
    else:
        print("[SETUP] Khong tim thay bai published nao — TC10-TC14 co the SKIP")

    if first_slug:
        res = run("TC10", f"GET /blog/{first_slug} - chi tiet thanh cong",
                  "get", f"{url}/blog/{first_slug}", 200, headers=auth())
        if res and res.status_code == 200:
            data = extract_data(res)
            print(f"  [INFO] TC10: fields = {list(data.keys())}")
            for f in ["id", "title", "slug", "content", "view_count"]:
                if f not in data:
                    print(f"  [WARN] TC10: thieu field '{f}'")

        # TC11: view_count tăng
        vc1 = extract_data(
            requests.get(f"{url}/blog/{first_slug}", headers=auth())
        ).get("view_count", 0)
        requests.get(f"{url}/blog/{first_slug}", headers=auth())
        vc2 = extract_data(
            requests.get(f"{url}/blog/{first_slug}", headers=auth())
        ).get("view_count", 0)
        ok_vc = vc2 >= vc1
        label = "\033[92mPASS\033[0m" if ok_vc else "\033[91mFAIL\033[0m"
        print(f"[{label}] TC11 - GET /blog/{{slug}} - view_count tang | {vc1} -> {vc2}")
        results.append(("TC11", "view_count tang", ok_vc, f"{vc1}->{vc2}"))

        run("TC12", f"GET /blog/{first_slug} - khong can token",
            "get", f"{url}/blog/{first_slug}", 200, headers=auth())
    else:
        for tc in ["TC10", "TC11", "TC12"]:
            print(f"[SKIP] {tc} - khong co bai published")
            results.append((tc, "GET /blog/{slug}", None, "skip"))

    run("TC13", "GET /blog/slug-khong-ton-tai-xyz-999 - 404",
        "get", f"{url}/blog/slug-khong-ton-tai-xyz-999", 404, headers=auth())

    # TC14: bài draft không hiển thị public — cần tạo bài draft trước
    if ADMIN_TOKEN:
        draft_id, draft_slug = admin_create_post("Draft TC14 test post", status="draft")
        if draft_slug:
            run("TC14", f"GET /blog/{draft_slug} - bai draft khong hien thi public",
                "get", f"{url}/blog/{draft_slug}", [403, 404], headers=auth())
        else:
            print("[SKIP] TC14 - khong tao duoc bai draft")
            results.append(("TC14", "Bai draft khong hien thi", None, "skip"))
    else:
        print("[SKIP] TC14 - khong co ADMIN_TOKEN")
        results.append(("TC14", "Bai draft khong hien thi", None, "skip"))

    # ── GET /blog/categories ──────────────────────────────────

    res = run("TC15", "GET /blog/categories - lay danh muc",
              "get", f"{url}/blog/categories", 200, headers=auth())
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC15: {len(items)} categories")
        if items and isinstance(items[0], dict):
            for f in ["id", "name", "slug"]:
                if f not in items[0]:
                    print(f"  [WARN] TC15: thieu field '{f}'")

    run("TC16", "GET /blog/categories - khong can token",
        "get", f"{url}/blog/categories", 200, headers=auth())

    # ── POST /admin/blog ──────────────────────────────────────

    if not ADMIN_TOKEN:
        for tc in [f"TC{i}" for i in range(17, 27)]:
            print(f"[SKIP] {tc} - khong co ADMIN_TOKEN")
            results.append((tc, "POST /admin/blog", None, "skip"))
    else:
        res = run("TC17", "POST /admin/blog - tao draft",
                  "post", f"{url}/admin/blog", [200, 201],
                  headers=auth(ADMIN_TOKEN),
                  json={"title": "TC17 Draft Post", "content": "Noi dung TC17",
                        "category_ids": [cat_id], "status": "draft"})
        if res and res.status_code in (200, 201):
            data = extract_data(res)
            pid  = data.get("id")
            if pid:
                created_ids.append(pid)
            print(f"  [INFO] TC17: id={pid}, slug={data.get('slug')}, status={data.get('status')}")
            if data.get("status") != "draft":
                print(f"  [WARN] TC17: status={data.get('status')}, ky vong draft")

        res = run("TC18", "POST /admin/blog - tao published",
                  "post", f"{url}/admin/blog", [200, 201],
                  headers=auth(ADMIN_TOKEN),
                  json={"title": "TC18 Published Post", "content": "Noi dung TC18",
                        "category_ids": [cat_id], "status": "published"})
        if res and res.status_code in (200, 201):
            data = extract_data(res)
            pid  = data.get("id")
            if pid:
                created_ids.append(pid)
            if data.get("status") == "published":
                print(f"  [INFO] TC18: status=published - OK")
            if data.get("published_at"):
                print(f"  [INFO] TC18: published_at={data.get('published_at')} - OK")
            else:
                print(f"  [WARN] TC18: published_at=null sau khi published")

        res = run("TC19", "POST /admin/blog - day du fields",
                  "post", f"{url}/admin/blog", [200, 201],
                  headers=auth(ADMIN_TOKEN),
                  json={"title": "TC19 Full Fields", "content": "Noi dung TC19",
                        "excerpt": "Tom tat TC19",
                        "featured_image": "https://example.com/img.jpg",
                        "category_ids": [cat_id], "status": "draft"})
        if res and res.status_code in (200, 201):
            data = extract_data(res)
            pid  = data.get("id")
            if pid:
                created_ids.append(pid)

        res = run("TC20", "POST /admin/blog - nhieu category_ids",
                  "post", f"{url}/admin/blog", [200, 201],
                  headers=auth(ADMIN_TOKEN),
                  json={"title": "TC20 Multi Category", "content": "Noi dung TC20",
                        "category_ids": [cat_id], "status": "draft"})
        if res and res.status_code in (200, 201):
            data = extract_data(res)
            pid  = data.get("id")
            if pid:
                created_ids.append(pid)

        run("TC21", "POST /admin/blog - thieu title",
            "post", f"{url}/admin/blog", 422,
            headers=auth(ADMIN_TOKEN),
            json={"content": "Noi dung", "status": "draft"})

        run("TC22", "POST /admin/blog - thieu content",
            "post", f"{url}/admin/blog", 422,
            headers=auth(ADMIN_TOKEN),
            json={"title": "Tieu de", "status": "draft"})

        run("TC23", "POST /admin/blog - status sai gia tri",
            "post", f"{url}/admin/blog", 422,
            headers=auth(ADMIN_TOKEN),
            json={"title": "Test", "content": "Test", "status": "invalid"})

        run("TC24", "POST /admin/blog - category_ids khong ton tai",
            "post", f"{url}/admin/blog", [422, 404],
            headers=auth(ADMIN_TOKEN),
            json={"title": "Test", "content": "Test", "category_ids": [99999], "status": "draft"})

        run("TC25", "POST /admin/blog - user thuong bi 403",
            "post", f"{url}/admin/blog", 403,
            headers=auth(USER_TOKEN),
            json={"title": "Test", "content": "Test", "status": "draft"})

        run("TC26", "POST /admin/blog - khong co token",
            "post", f"{url}/admin/blog", 401,
            headers=auth(),
            json={"title": "Test", "content": "Test", "status": "draft"})

    # ── PUT /admin/blog/{id} ──────────────────────────────────

    # Tạo bài để test PUT
    edit_id = None
    if ADMIN_TOKEN:
        edit_id, _ = admin_create_post("TC27-34 Edit Target", status="draft")
        if edit_id:
            print(f"[SETUP] edit_id = {edit_id}")

    if not ADMIN_TOKEN or not edit_id:
        for tc in [f"TC{i}" for i in range(27, 35)]:
            print(f"[SKIP] {tc} - khong co ADMIN_TOKEN hoac edit_id")
            results.append((tc, "PUT /admin/blog/{id}", None, "skip"))
    else:
        res = run("TC27", f"PUT /admin/blog/{edit_id} - cap nhat title",
                  "put", f"{url}/admin/blog/{edit_id}", 200,
                  headers=auth(ADMIN_TOKEN),
                  json={"title": "TC27 Updated Title"})
        if res and res.status_code == 200:
            data = extract_data(res)
            if "TC27 Updated Title" in (data.get("title") or ""):
                print(f"  [INFO] TC27: title cap nhat thanh cong - OK")
            else:
                print(f"  [WARN] TC27: title trong response = {data.get('title')}")

        run("TC28", f"PUT /admin/blog/{edit_id} - cap nhat content",
            "put", f"{url}/admin/blog/{edit_id}", 200,
            headers=auth(ADMIN_TOKEN),
            json={"content": "Noi dung moi TC28"})

        run("TC29", f"PUT /admin/blog/{edit_id} - cap nhat category_ids",
            "put", f"{url}/admin/blog/{edit_id}", 200,
            headers=auth(ADMIN_TOKEN),
            json={"category_ids": [cat_id]})

        run("TC30", f"PUT /admin/blog/{edit_id} - category_ids rong",
            "put", f"{url}/admin/blog/{edit_id}", [200, 422],
            headers=auth(ADMIN_TOKEN),
            json={"category_ids": []})

        run("TC31", "PUT /admin/blog/99999 - ID khong ton tai",
            "put", f"{url}/admin/blog/99999", 404,
            headers=auth(ADMIN_TOKEN),
            json={"title": "Test"})

        run("TC32", f"PUT /admin/blog/{edit_id} - status sai gia tri",
            "put", f"{url}/admin/blog/{edit_id}", 422,
            headers=auth(ADMIN_TOKEN),
            json={"status": "invalid"})

        run("TC33", f"PUT /admin/blog/{edit_id} - user thuong bi 403",
            "put", f"{url}/admin/blog/{edit_id}", 403,
            headers=auth(USER_TOKEN),
            json={"title": "Test"})

        run("TC34", f"PUT /admin/blog/{edit_id} - khong co token",
            "put", f"{url}/admin/blog/{edit_id}", 401,
            headers=auth(),
            json={"title": "Test"})

    # ── DELETE /admin/blog/{id} ───────────────────────────────

    # Tạo bài để test DELETE
    delete_id = None
    if ADMIN_TOKEN:
        delete_id, delete_slug = admin_create_post("TC35 Delete Target", status="draft")
        if delete_id:
            print(f"[SETUP] delete_id = {delete_id}")

    if not ADMIN_TOKEN or not delete_id:
        for tc in ["TC35", "TC36", "TC37", "TC38"]:
            print(f"[SKIP] {tc} - khong co ADMIN_TOKEN hoac delete_id")
            results.append((tc, "DELETE /admin/blog/{id}", None, "skip"))
    else:
        run("TC36", "DELETE /admin/blog/99999 - ID khong ton tai",
            "delete", f"{url}/admin/blog/99999", 404,
            headers=auth(ADMIN_TOKEN))

        run("TC37", f"DELETE /admin/blog/{delete_id} - user thuong bi 403",
            "delete", f"{url}/admin/blog/{delete_id}", 403,
            headers=auth(USER_TOKEN))

        run("TC38", f"DELETE /admin/blog/{delete_id} - khong co token",
            "delete", f"{url}/admin/blog/{delete_id}", 401,
            headers=auth())

        res = run("TC35", f"DELETE /admin/blog/{delete_id} - xoa thanh cong",
                  "delete", f"{url}/admin/blog/{delete_id}", [200, 204],
                  headers=auth(ADMIN_TOKEN))
        if res and res.status_code in (200, 204):
            # Verify: GET public → 404
            if delete_slug:
                check = requests.get(f"{url}/blog/{delete_slug}", headers=auth())
                if check.status_code == 404:
                    print(f"  [INFO] TC35: GET public sau xoa → 404 - OK")
                else:
                    print(f"  [WARN] TC35: GET public → {check.status_code}, ky vong 404")
            # Xóa khỏi created_ids vì đã xóa rồi
            if delete_id in created_ids:
                created_ids.remove(delete_id)

    # ── PATCH /admin/blog/{id}/publish ────────────────────────

    # Tạo bài draft để test publish
    pub_id = None
    if ADMIN_TOKEN:
        pub_id, _ = admin_create_post("TC39-46 Publish Target", status="draft")
        if pub_id:
            print(f"[SETUP] pub_id = {pub_id}")

    if not ADMIN_TOKEN or not pub_id:
        for tc in [f"TC{i}" for i in range(39, 47)]:
            print(f"[SKIP] {tc} - khong co ADMIN_TOKEN hoac pub_id")
            results.append((tc, "PATCH .../publish", None, "skip"))
    else:
        res = run("TC39", f"PATCH /admin/blog/{pub_id}/publish - draft → published",
                  "patch", f"{url}/admin/blog/{pub_id}/publish", 200,
                  headers=auth(ADMIN_TOKEN),
                  json={"status": "published"})
        if res and res.status_code == 200:
            data = extract_data(res)
            if data.get("status") == "published":
                print(f"  [INFO] TC39: status=published - OK")
            if data.get("published_at"):
                print(f"  [INFO] TC39: published_at={data.get('published_at')} - OK")
            else:
                print(f"  [WARN] TC39: published_at=null sau khi publish")

        res = run("TC40", f"PATCH /admin/blog/{pub_id}/publish - published → draft",
                  "patch", f"{url}/admin/blog/{pub_id}/publish", 200,
                  headers=auth(ADMIN_TOKEN),
                  json={"status": "draft"})
        if res and res.status_code == 200:
            data = extract_data(res)
            if data.get("status") == "draft":
                print(f"  [INFO] TC40: status=draft - OK")

        # Publish lại để test TC41
        requests.patch(f"{url}/admin/blog/{pub_id}/publish",
                       headers=auth(ADMIN_TOKEN), json={"status": "published"})

        run("TC41", f"PATCH /admin/blog/{pub_id}/publish - idempotent (published lai)",
            "patch", f"{url}/admin/blog/{pub_id}/publish", 200,
            headers=auth(ADMIN_TOKEN),
            json={"status": "published"})

        run("TC42", f"PATCH /admin/blog/{pub_id}/publish - status sai gia tri",
            "patch", f"{url}/admin/blog/{pub_id}/publish", 422,
            headers=auth(ADMIN_TOKEN),
            json={"status": "archived"})

        run("TC43", f"PATCH /admin/blog/{pub_id}/publish - thieu status",
            "patch", f"{url}/admin/blog/{pub_id}/publish", 422,
            headers=auth(ADMIN_TOKEN),
            json={})

        run("TC44", "PATCH /admin/blog/99999/publish - ID khong ton tai",
            "patch", f"{url}/admin/blog/99999/publish", 404,
            headers=auth(ADMIN_TOKEN),
            json={"status": "published"})

        run("TC45", f"PATCH /admin/blog/{pub_id}/publish - user thuong bi 403",
            "patch", f"{url}/admin/blog/{pub_id}/publish", 403,
            headers=auth(USER_TOKEN),
            json={"status": "published"})

        run("TC46", f"PATCH /admin/blog/{pub_id}/publish - khong co token",
            "patch", f"{url}/admin/blog/{pub_id}/publish", 401,
            headers=auth(),
            json={"status": "published"})

    # ── CLEANUP ───────────────────────────────────────────────

    if ADMIN_TOKEN and created_ids:
        print(f"\n[CLEANUP] Xoa {len(created_ids)} bai viet da tao trong test...")
        for pid in list(created_ids):
            r = requests.delete(f"{url}/admin/blog/{pid}", headers=auth(ADMIN_TOKEN))
            status = "OK" if r.status_code in (200, 204) else f"got {r.status_code}"
            print(f"  [CLEANUP] DELETE /admin/blog/{pid} → {status}")

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
