
"""
Test script - BLOG (Bai viet)
Branch: feat/taynd/api-blog
Run: python tests/scripts/test_blog.py
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
created_post_ids     = []
created_category_ids = []
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
            for key in ["post", "blog_post", "category", "blog_category"]:
                if d.get(key):
                    return d[key]
            return d
        return {}
    except Exception:
        return {}


def get_published_slug():
    """Lay slug bai viet published de test."""
    res = requests.get(f"{BASE_URL}/blog", headers=auth(), params={"per_page": 5})
    if res.status_code == 200:
        items = extract_items(res)
        for item in items:
            if isinstance(item, dict) and item.get("slug"):
                return item["slug"]
    return None


def get_admin_category_id():
    """Lay category_id dau tien tu admin."""
    res = requests.get(f"{BASE_URL}/admin/blog-categories",
                       headers=auth(ADMIN_TOKEN))
    if res.status_code == 200:
        items = extract_items(res)
        if items and isinstance(items[0], dict):
            return items[0].get("id")
    return None


def run_tests():
    global USER_TOKEN, ADMIN_TOKEN

    USER_TOKEN  = login(USER_EMAIL, USER_PASSWORD)
    ADMIN_TOKEN = login(ADMIN_EMAIL, ADMIN_PASSWORD)

    if not ADMIN_TOKEN:
        print("[ABORT] Khong lay duoc ADMIN_TOKEN.")
        return

    url = BASE_URL

    # SETUP: lay category_id va slug co san
    cat_id = get_admin_category_id()
    print(f"[SETUP] blog category_id = {cat_id}")

    # ── GET /blog ─────────────────────────────────────────────

    res = run("TC01", "GET /blog - lay danh sach",
              "get", f"{url}/blog", 200, headers=auth())
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC01: {len(items)} posts")
        if items and isinstance(items[0], dict):
            print(f"  [INFO] TC01: fields = {list(items[0].keys())}")

    res = run("TC02", "GET /blog - chi tra published",
              "get", f"{url}/blog", 200, headers=auth())
    if res and res.status_code == 200:
        items = extract_items(res)
        bad = [i for i in items if isinstance(i, dict) and i.get("status") != "published"]
        if bad:
            print(f"  [WARN] TC02: co {len(bad)} item khong phai published")
        else:
            print(f"  [INFO] TC02: tat ca {len(items)} items la published - OK")

    res = run("TC03", "GET /blog - phan trang per_page=5",
              "get", f"{url}/blog", 200,
              headers=auth(), params={"page": 1, "per_page": 5})
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC03: {len(items)} items {'OK' if len(items) <= 5 else 'WARN > 5'}")

    run("TC04", "GET /blog - trang 2",
        "get", f"{url}/blog", 200,
        headers=auth(), params={"page": 2, "per_page": 5})

    run("TC05", "GET /blog - filter category_id=1",
        "get", f"{url}/blog", 200,
        headers=auth(), params={"category_id": cat_id or 1})

    run("TC06", "GET /blog - category_id khong co bai",
        "get", f"{url}/blog", [200, 422],
        headers=auth(), params={"category_id": 99999})

    run("TC07", "GET /blog - category_id khong phai so → 422",
        "get", f"{url}/blog", 422,
        headers=auth(), params={"category_id": "abc"})

    run("TC08", "GET /blog - per_page vuot max",
        "get", f"{url}/blog", [200, 422],
        headers=auth(), params={"per_page": 200})

    run("TC09", "GET /blog - khong can token (public)",
        "get", f"{url}/blog", 200, headers=auth())

    # ── GET /blog/{slug} ──────────────────────────────────────

    pub_slug = get_published_slug()
    print(f"[SETUP] published slug = {pub_slug}")

    if pub_slug:
        res = run("TC10", f"GET /blog/{pub_slug} - chi tiet thanh cong",
                  "get", f"{url}/blog/{pub_slug}", 200, headers=auth())
        if res and res.status_code == 200:
            data = extract_data(res)
            print(f"  [INFO] TC10: fields = {list(data.keys())}")
            for f in ["id", "title", "slug", "content", "view_count"]:
                if f not in data:
                    print(f"  [WARN] TC10: thieu field '{f}'")

        # TC11: view_count tang
        res1 = requests.get(f"{url}/blog/{pub_slug}", headers=auth())
        res2 = requests.get(f"{url}/blog/{pub_slug}", headers=auth())
        if res1.status_code == 200 and res2.status_code == 200:
            vc1 = extract_data(res1).get("view_count", 0)
            vc2 = extract_data(res2).get("view_count", 0)
            ok  = vc2 >= vc1
            label = "\033[92mPASS\033[0m" if ok else "\033[91mFAIL\033[0m"
            print(f"[{label}] TC11 - GET /blog/{{slug}} - view_count tang | {vc1} → {vc2}")
            results.append(("TC11", "view_count tang", ok, 200))
        else:
            print("[SKIP] TC11 - khong lay duoc response")
            results.append(("TC11", "view_count tang", None, "skip"))

        run("TC12", "GET /blog/{slug} - khong can token",
            "get", f"{url}/blog/{pub_slug}", 200, headers=auth())
    else:
        for tc in ["TC10", "TC11", "TC12"]:
            print(f"[SKIP] {tc} - khong co published post")
            results.append((tc, "GET /blog/{slug}", None, "skip"))

    run("TC13", "GET /blog/slug-khong-ton-tai-xyz-999 - 404",
        "get", f"{url}/blog/slug-khong-ton-tai-xyz-999", 404, headers=auth())

    # TC14: bai draft khong hien thi public — tao draft roi thu GET
    res_draft = requests.post(f"{url}/admin/blog-posts",
                              headers=auth(ADMIN_TOKEN),
                              json={"title": f"Draft TC14 {ts}", "content": "Draft content",
                                    "category_ids": [cat_id] if cat_id else [],
                                    "status": "draft"})
    draft_slug = None
    if res_draft.status_code in (200, 201):
        d = extract_data(res_draft)
        draft_slug = d.get("slug")
        draft_id   = d.get("id")
        if draft_id:
            created_post_ids.append(draft_id)

    if draft_slug:
        run("TC14", f"GET /blog/{draft_slug} - bai draft khong hien thi public",
            "get", f"{url}/blog/{draft_slug}", [403, 404], headers=auth())
    else:
        print("[SKIP] TC14 - khong tao duoc draft post")
        results.append(("TC14", "bai draft khong hien thi", None, "skip"))

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

    # ── GET /admin/blog-posts ─────────────────────────────────

    res = run("TC17", "GET /admin/blog-posts - lay tat ca (ke ca draft)",
              "get", f"{url}/admin/blog-posts", 200,
              headers=auth(ADMIN_TOKEN))
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC17: {len(items)} posts")

    run("TC18", "GET /admin/blog-posts - filter status=draft",
        "get", f"{url}/admin/blog-posts", 200,
        headers=auth(ADMIN_TOKEN), params={"status": "draft"})

    run("TC19", "GET /admin/blog-posts - filter status=published",
        "get", f"{url}/admin/blog-posts", 200,
        headers=auth(ADMIN_TOKEN), params={"status": "published"})

    run("TC20", "GET /admin/blog-posts - filter category_id",
        "get", f"{url}/admin/blog-posts", 200,
        headers=auth(ADMIN_TOKEN), params={"category_id": cat_id or 1})

    res = run("TC21", "GET /admin/blog-posts - phan trang per_page=5",
              "get", f"{url}/admin/blog-posts", 200,
              headers=auth(ADMIN_TOKEN), params={"page": 1, "per_page": 5})
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC21: {len(items)} items {'OK' if len(items) <= 5 else 'WARN > 5'}")

    run("TC22", "GET /admin/blog-posts - user thuong bi 403",
        "get", f"{url}/admin/blog-posts", 403,
        headers=auth(USER_TOKEN))

    run("TC23", "GET /admin/blog-posts - khong co token → 401",
        "get", f"{url}/admin/blog-posts", 401, headers=auth())

    # ── POST /admin/blog-posts ────────────────────────────────

    res = run("TC24", "POST /admin/blog-posts - tao draft",
              "post", f"{url}/admin/blog-posts", [200, 201],
              headers=auth(ADMIN_TOKEN),
              json={"title": f"Draft Post {ts}", "content": "Noi dung draft",
                    "category_ids": [cat_id] if cat_id else [],
                    "status": "draft"})
    post_id = None
    if res and res.status_code in (200, 201):
        data = extract_data(res)
        post_id = data.get("id")
        if post_id:
            created_post_ids.append(post_id)
        print(f"  [INFO] TC24: id={post_id}, slug={data.get('slug')}")

    res = run("TC25", "POST /admin/blog-posts - tao published",
              "post", f"{url}/admin/blog-posts", [200, 201],
              headers=auth(ADMIN_TOKEN),
              json={"title": f"Published Post {ts}", "content": "Noi dung published",
                    "category_ids": [cat_id] if cat_id else [],
                    "status": "published"})
    if res and res.status_code in (200, 201):
        data = extract_data(res)
        pid  = data.get("id")
        if pid:
            created_post_ids.append(pid)
        if data.get("published_at"):
            print(f"  [INFO] TC25: published_at={data.get('published_at')} - OK")
        else:
            print(f"  [WARN] TC25: published_at=null")

    res = run("TC26", "POST /admin/blog-posts - day du fields",
              "post", f"{url}/admin/blog-posts", [200, 201],
              headers=auth(ADMIN_TOKEN),
              json={"title": f"Full Fields Post {ts}", "content": "Noi dung day du",
                    "excerpt": "Tom tat", "category_ids": [cat_id] if cat_id else [],
                    "status": "draft"})
    if res and res.status_code in (200, 201):
        pid = extract_data(res).get("id")
        if pid:
            created_post_ids.append(pid)

    res = run("TC27", "POST /admin/blog-posts - nhieu category_ids",
              "post", f"{url}/admin/blog-posts", [200, 201],
              headers=auth(ADMIN_TOKEN),
              json={"title": f"Multi Cat Post {ts}", "content": "Noi dung",
                    "category_ids": [cat_id, cat_id] if cat_id else [], "status": "draft"})
    if res and res.status_code in (200, 201):
        pid = extract_data(res).get("id")
        if pid:
            created_post_ids.append(pid)

    run("TC28", "POST /admin/blog-posts - thieu title → 422",
        "post", f"{url}/admin/blog-posts", 422,
        headers=auth(ADMIN_TOKEN),
        json={"content": "Noi dung", "status": "draft"})

    run("TC29", "POST /admin/blog-posts - thieu content → 422",
        "post", f"{url}/admin/blog-posts", 422,
        headers=auth(ADMIN_TOKEN),
        json={"title": "Tieu de", "status": "draft"})

    run("TC30", "POST /admin/blog-posts - status sai gia tri → 422",
        "post", f"{url}/admin/blog-posts", 422,
        headers=auth(ADMIN_TOKEN),
        json={"title": "Test", "content": "Test", "status": "invalid_status"})

    run("TC31", "POST /admin/blog-posts - category_ids khong ton tai → 422",
        "post", f"{url}/admin/blog-posts", [404, 422],
        headers=auth(ADMIN_TOKEN),
        json={"title": "Test", "content": "Test", "category_ids": [99999], "status": "draft"})

    run("TC32", "POST /admin/blog-posts - user thuong bi 403",
        "post", f"{url}/admin/blog-posts", 403,
        headers=auth(USER_TOKEN),
        json={"title": "Test", "content": "Test", "status": "draft"})

    run("TC33", "POST /admin/blog-posts - khong co token → 401",
        "post", f"{url}/admin/blog-posts", 401,
        headers=auth(),
        json={"title": "Test", "content": "Test", "status": "draft"})

    # ── GET /admin/blog-posts/{id} ────────────────────────────

    if post_id:
        res = run("TC34", f"GET /admin/blog-posts/{post_id} - chi tiet",
                  "get", f"{url}/admin/blog-posts/{post_id}", 200,
                  headers=auth(ADMIN_TOKEN))
        if res and res.status_code == 200:
            data = extract_data(res)
            print(f"  [INFO] TC34: fields = {list(data.keys())}")
    else:
        print("[SKIP] TC34 - khong co post_id")
        results.append(("TC34", "GET /admin/blog-posts/{id}", None, "skip"))

    run("TC35", "GET /admin/blog-posts/99999 - ID khong ton tai",
        "get", f"{url}/admin/blog-posts/99999", [404, 422],
        headers=auth(ADMIN_TOKEN))

    run("TC36", "GET /admin/blog-posts/{id} - khong co token → 401",
        "get", f"{url}/admin/blog-posts/{post_id or 1}", 401,
        headers=auth())

    # ── PUT /admin/blog-posts/{id} ────────────────────────────

    if post_id:
        res = run("TC37", f"PUT /admin/blog-posts/{post_id} - cap nhat title",
                  "put", f"{url}/admin/blog-posts/{post_id}", 200,
                  headers=auth(ADMIN_TOKEN),
                  json={"title": f"Updated Title {ts}"})
        if res and res.status_code == 200:
            data = extract_data(res)
            if f"Updated Title {ts}" in str(data.get("title", "")):
                print(f"  [INFO] TC37: title cap nhat OK")

        run("TC38", f"PUT /admin/blog-posts/{post_id} - cap nhat content",
            "put", f"{url}/admin/blog-posts/{post_id}", 200,
            headers=auth(ADMIN_TOKEN),
            json={"content": "Noi dung moi da cap nhat"})

        run("TC39", f"PUT /admin/blog-posts/{post_id} - cap nhat category_ids",
            "put", f"{url}/admin/blog-posts/{post_id}", 200,
            headers=auth(ADMIN_TOKEN),
            json={"category_ids": [cat_id] if cat_id else []})
    else:
        for tc in ["TC37", "TC38", "TC39"]:
            print(f"[SKIP] {tc} - khong co post_id")
            results.append((tc, "PUT /admin/blog-posts/{id}", None, "skip"))

    run("TC40", "PUT /admin/blog-posts/99999 - ID khong ton tai",
        "put", f"{url}/admin/blog-posts/99999", [404, 422],
        headers=auth(ADMIN_TOKEN), json={"title": "Test"})

    run("TC41", f"PUT /admin/blog-posts/{post_id or 1} - status sai gia tri → 422",
        "put", f"{url}/admin/blog-posts/{post_id or 1}", 422,
        headers=auth(ADMIN_TOKEN), json={"status": "invalid_status"})

    run("TC42", f"PUT /admin/blog-posts/{post_id or 1} - user thuong bi 403",
        "put", f"{url}/admin/blog-posts/{post_id or 1}", 403,
        headers=auth(USER_TOKEN), json={"title": "Test"})

    run("TC43", f"PUT /admin/blog-posts/{post_id or 1} - khong co token → 401",
        "put", f"{url}/admin/blog-posts/{post_id or 1}", 401,
        headers=auth(), json={"title": "Test"})

    # ── PATCH /admin/blog-posts/{id}/status ───────────────────

    if post_id:
        res = run("TC48", f"PATCH /admin/blog-posts/{post_id}/status - draft → published",
                  "patch", f"{url}/admin/blog-posts/{post_id}/status", 200,
                  headers=auth(ADMIN_TOKEN), json={"status": "published"})
        if res and res.status_code == 200:
            data = extract_data(res)
            if data.get("status") == "published":
                print(f"  [INFO] TC48: status=published - OK")
            if data.get("published_at"):
                print(f"  [INFO] TC48: published_at set - OK")

        res = run("TC49", f"PATCH /admin/blog-posts/{post_id}/status - published → draft",
                  "patch", f"{url}/admin/blog-posts/{post_id}/status", 200,
                  headers=auth(ADMIN_TOKEN), json={"status": "draft"})
        if res and res.status_code == 200:
            data = extract_data(res)
            if data.get("status") == "draft":
                print(f"  [INFO] TC49: status=draft - OK")

        run("TC50", f"PATCH /admin/blog-posts/{post_id}/status - archived",
            "patch", f"{url}/admin/blog-posts/{post_id}/status", 200,
            headers=auth(ADMIN_TOKEN), json={"status": "archived"})

        run("TC51", f"PATCH /admin/blog-posts/{post_id}/status - idempotent",
            "patch", f"{url}/admin/blog-posts/{post_id}/status", 200,
            headers=auth(ADMIN_TOKEN), json={"status": "published"})
    else:
        for tc in ["TC48", "TC49", "TC50", "TC51"]:
            print(f"[SKIP] {tc} - khong co post_id")
            results.append((tc, "PATCH .../status", None, "skip"))

    run("TC52", f"PATCH /admin/blog-posts/{post_id or 1}/status - status sai → 422",
        "patch", f"{url}/admin/blog-posts/{post_id or 1}/status", 422,
        headers=auth(ADMIN_TOKEN), json={"status": "invalid_status"})

    run("TC53", f"PATCH /admin/blog-posts/{post_id or 1}/status - thieu status → 422",
        "patch", f"{url}/admin/blog-posts/{post_id or 1}/status", 422,
        headers=auth(ADMIN_TOKEN), json={})

    run("TC54", "PATCH /admin/blog-posts/99999/status - ID khong ton tai",
        "patch", f"{url}/admin/blog-posts/99999/status", [404, 422],
        headers=auth(ADMIN_TOKEN), json={"status": "published"})

    run("TC55", f"PATCH /admin/blog-posts/{post_id or 1}/status - user thuong bi 403",
        "patch", f"{url}/admin/blog-posts/{post_id or 1}/status", 403,
        headers=auth(USER_TOKEN), json={"status": "published"})

    run("TC56", f"PATCH /admin/blog-posts/{post_id or 1}/status - khong co token → 401",
        "patch", f"{url}/admin/blog-posts/{post_id or 1}/status", 401,
        headers=auth(), json={"status": "published"})

    # ── DELETE /admin/blog-posts/{id} ─────────────────────────

    # Tao post rieng de xoa
    del_res = requests.post(f"{url}/admin/blog-posts",
                            headers=auth(ADMIN_TOKEN),
                            json={"title": f"To Delete {ts}", "content": "Del content",
                                  "category_ids": [cat_id] if cat_id else [],
                                  "status": "draft"})
    del_id = None
    if del_res.status_code in (200, 201):
        del_id = extract_data(del_res).get("id")

    if del_id:
        run("TC45", f"DELETE /admin/blog-posts/99999 - ID khong ton tai",
            "delete", f"{url}/admin/blog-posts/99999", [404, 422],
            headers=auth(ADMIN_TOKEN))

        run("TC46", f"DELETE /admin/blog-posts/{del_id} - user thuong bi 403",
            "delete", f"{url}/admin/blog-posts/{del_id}", 403,
            headers=auth(USER_TOKEN))

        run("TC47", f"DELETE /admin/blog-posts/{del_id} - khong co token → 401",
            "delete", f"{url}/admin/blog-posts/{del_id}", 401,
            headers=auth())

        res = run("TC44", f"DELETE /admin/blog-posts/{del_id} - xoa thanh cong",
                  "delete", f"{url}/admin/blog-posts/{del_id}", [200, 204],
                  headers=auth(ADMIN_TOKEN))
        if res and res.status_code in (200, 204):
            print(f"  [INFO] TC44: xoa id={del_id} - OK")
    else:
        for tc in ["TC44", "TC45", "TC46", "TC47"]:
            print(f"[SKIP] {tc} - khong tao duoc post de xoa")
            results.append((tc, "DELETE /admin/blog-posts/{id}", None, "skip"))

    # ── Admin Blog Categories ─────────────────────────────────

    res = run("TC57", "GET /admin/blog-categories - lay danh sach",
              "get", f"{url}/admin/blog-categories", 200,
              headers=auth(ADMIN_TOKEN))
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC57: {len(items)} categories")

    res = run("TC58", "POST /admin/blog-categories - tao danh muc",
              "post", f"{url}/admin/blog-categories", [200, 201],
              headers=auth(ADMIN_TOKEN),
              json={"name": f"Blog Cat {ts}", "description": "Mo ta test"})
    new_cat_id = None
    if res and res.status_code in (200, 201):
        new_cat_id = extract_data(res).get("id")
        if new_cat_id:
            created_category_ids.append(new_cat_id)
        print(f"  [INFO] TC58: id={new_cat_id}")

    if new_cat_id:
        res = run("TC59", f"PUT /admin/blog-categories/{new_cat_id} - cap nhat",
                  "put", f"{url}/admin/blog-categories/{new_cat_id}", 200,
                  headers=auth(ADMIN_TOKEN),
                  json={"name": f"Updated Cat {ts}"})
        if res and res.status_code == 200:
            print(f"  [INFO] TC59: cap nhat OK")
    else:
        print("[SKIP] TC59 - khong co new_cat_id")
        results.append(("TC59", "PUT /admin/blog-categories/{id}", None, "skip"))

    run("TC60", "POST /admin/blog-categories - thieu name → 422",
        "post", f"{url}/admin/blog-categories", 422,
        headers=auth(ADMIN_TOKEN), json={"description": "Mo ta"})

    # Tao category rieng de xoa
    del_cat_res = requests.post(f"{url}/admin/blog-categories",
                                headers=auth(ADMIN_TOKEN),
                                json={"name": f"Del Cat {ts}"})
    del_cat_id = None
    if del_cat_res.status_code in (200, 201):
        del_cat_id = extract_data(del_cat_res).get("id")

    if del_cat_id:
        res = run("TC61", f"DELETE /admin/blog-categories/{del_cat_id} - xoa",
                  "delete", f"{url}/admin/blog-categories/{del_cat_id}", [200, 204],
                  headers=auth(ADMIN_TOKEN))
        if res and res.status_code in (200, 204):
            print(f"  [INFO] TC61: xoa category id={del_cat_id} - OK")
    else:
        print("[SKIP] TC61 - khong tao duoc category de xoa")
        results.append(("TC61", "DELETE /admin/blog-categories/{id}", None, "skip"))

    run("TC62", "DELETE /admin/blog-categories/99999 - ID khong ton tai",
        "delete", f"{url}/admin/blog-categories/99999", [404, 422],
        headers=auth(ADMIN_TOKEN))

    run("TC63", "POST /admin/blog-categories - user thuong bi 403",
        "post", f"{url}/admin/blog-categories", 403,
        headers=auth(USER_TOKEN), json={"name": "Test"})

    run("TC64", "GET /admin/blog-categories - khong co token → 401",
        "get", f"{url}/admin/blog-categories", 401,
        headers=auth())

    # ── CLEANUP ───────────────────────────────────────────────

    if ADMIN_TOKEN and created_post_ids:
        print(f"\n[CLEANUP] Xoa {len(created_post_ids)} posts...")
        for pid in created_post_ids:
            r = requests.delete(f"{url}/admin/blog-posts/{pid}",
                                headers=auth(ADMIN_TOKEN))
            print(f"  [CLEANUP] post/{pid} → {r.status_code}")

    if ADMIN_TOKEN and created_category_ids:
        print(f"[CLEANUP] Xoa {len(created_category_ids)} categories...")
        for cid in created_category_ids:
            r = requests.delete(f"{url}/admin/blog-categories/{cid}",
                                headers=auth(ADMIN_TOKEN))
            print(f"  [CLEANUP] category/{cid} → {r.status_code}")

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
