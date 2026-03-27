"""
Test script - TAGS & AMENITIES
Run: python tests/scripts/test_tags_amenities.py
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
created_tag_ids      = []
created_amenity_ids  = []


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


def run_tests():
    global USER_TOKEN, ADMIN_TOKEN

    USER_TOKEN  = login(USER_EMAIL, USER_PASSWORD)
    ADMIN_TOKEN = login(ADMIN_EMAIL, ADMIN_PASSWORD)

    if not USER_TOKEN:
        print("[ABORT] Khong lay duoc USER_TOKEN.")
        return
    if not ADMIN_TOKEN:
        print("[WARN] Khong lay duoc ADMIN_TOKEN  cac TC admin se SKIP.")

    url = BASE_URL
    ts  = int(time.time())

    #  GET /tags 

    res = run("TC01", "GET /tags - lay tat ca",
              "get", f"{url}/tags", 200, headers=auth())
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC01: {len(items)} tags")
        if items and isinstance(items[0], dict):
            print(f"  [INFO] TC01: fields = {list(items[0].keys())}")
            for f in ["id", "name", "slug", "type"]:
                if f not in items[0]:
                    print(f"  [WARN] TC01: thieu field '{f}'")

    for tc, type_val in [("TC02", "cuisine"), ("TC03", "service"),
                          ("TC04", "feature"), ("TC05", "atmosphere")]:
        res = run(tc, f"GET /tags - filter type={type_val}",
                  "get", f"{url}/tags", 200,
                  headers=auth(), params={"type": type_val})
        if res and res.status_code == 200:
            items = extract_items(res)
            bad = [i for i in items if isinstance(i, dict) and i.get("type") != type_val]
            if bad:
                print(f"  [WARN] {tc}: co {len(bad)} item khong phai type={type_val}")
            else:
                print(f"  [INFO] {tc}: {len(items)} items, tat ca type={type_val} - OK")

    run("TC06", "GET /tags - khong can token (public)",
        "get", f"{url}/tags", 200, headers=auth())

    run("TC07", "GET /tags - type sai gia tri",
        "get", f"{url}/tags", 422,
        headers=auth(), params={"type": "invalid"})

    #  GET /amenities 

    res = run("TC08", "GET /amenities - lay tat ca",
              "get", f"{url}/amenities", 200, headers=auth())
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC08: {len(items)} amenities")
        if items and isinstance(items[0], dict):
            print(f"  [INFO] TC08: fields = {list(items[0].keys())}")

    for tc, cat_val in [("TC09", "connectivity"), ("TC10", "parking"),
                         ("TC11", "comfort"),      ("TC12", "payment")]:
        res = run(tc, f"GET /amenities - filter category={cat_val}",
                  "get", f"{url}/amenities", 200,
                  headers=auth(), params={"category": cat_val})
        if res and res.status_code == 200:
            items = extract_items(res)
            bad = [i for i in items if isinstance(i, dict) and i.get("category") != cat_val]
            if bad:
                print(f"  [WARN] {tc}: co {len(bad)} item khong phai category={cat_val}")
            else:
                print(f"  [INFO] {tc}: {len(items)} items, tat ca category={cat_val} - OK")

    run("TC13", "GET /amenities - khong can token (public)",
        "get", f"{url}/amenities", 200, headers=auth())

    run("TC14", "GET /amenities - category sai gia tri",
        "get", f"{url}/amenities", 422,
        headers=auth(), params={"category": "invalid"})

    #  POST /admin/tags 

    if not ADMIN_TOKEN:
        for tc in [f"TC{i}" for i in range(15, 28)]:
            print(f"[SKIP] {tc} - khong co ADMIN_TOKEN")
            results.append((tc, "POST/DELETE /admin/tags", None, "skip"))
    else:
        tag_name = f"Test Tag {ts}"
        tag_slug = f"test-tag-{ts}"

        res = run("TC15", "POST /admin/tags - tao day du fields",
                  "post", f"{url}/admin/tags", [200, 201],
                  headers=auth(ADMIN_TOKEN),
                  json={"name": tag_name, "slug": tag_slug, "type": "cuisine"})
        if res and res.status_code in (200, 201):
            data = extract_data(res)
            tid  = data.get("id")
            if tid:
                created_tag_ids.append(tid)
            print(f"  [INFO] TC15: id={tid}, slug={data.get('slug')}, type={data.get('type')}")

        res = run("TC16", "POST /admin/tags - type la bat buoc (backend require)",
                  "post", f"{url}/admin/tags", 422,
                  headers=auth(ADMIN_TOKEN),
                  json={"name": f"Tag No Type {ts}", "slug": f"tag-no-type-{ts}"})

        run("TC17", "POST /admin/tags - thieu name",
            "post", f"{url}/admin/tags", 422,
            headers=auth(ADMIN_TOKEN),
            json={"slug": "no-name-slug"})

        run("TC18", "POST /admin/tags - thieu slug",
            "post", f"{url}/admin/tags", 422,
            headers=auth(ADMIN_TOKEN),
            json={"name": "No Slug Tag"})

        # TC19: name trùng  dùng tag_name vừa tạo
        run("TC19", "POST /admin/tags - name trung",
            "post", f"{url}/admin/tags", [422, 409],
            headers=auth(ADMIN_TOKEN),
            json={"name": tag_name, "slug": f"different-slug-{ts}"})

        # TC20: slug trùng  dùng tag_slug vừa tạo
        run("TC20", "POST /admin/tags - slug trung",
            "post", f"{url}/admin/tags", [422, 409],
            headers=auth(ADMIN_TOKEN),
            json={"name": f"Different Name {ts}", "slug": tag_slug})

        run("TC21", "POST /admin/tags - type sai gia tri",
            "post", f"{url}/admin/tags", 422,
            headers=auth(ADMIN_TOKEN),
            json={"name": f"Bad Type {ts}", "slug": f"bad-type-{ts}", "type": "invalid"})

        run("TC22", "POST /admin/tags - user thuong bi 403",
            "post", f"{url}/admin/tags", 403,
            headers=auth(USER_TOKEN),
            json={"name": "User Tag", "slug": "user-tag"})

        run("TC23", "POST /admin/tags - khong co token",
            "post", f"{url}/admin/tags", 401,
            headers=auth(),
            json={"name": "No Token Tag", "slug": "no-token-tag"})

        #  DELETE /admin/tags/{id} 

        # Tạo tag riêng để xóa
        del_res = requests.post(f"{url}/admin/tags",
                                headers=auth(ADMIN_TOKEN),
                                json={"name": f"Delete Tag {ts}", "slug": f"delete-tag-{ts}",
                                      "type": "feature"})
        del_tag_id = None
        if del_res.status_code in (200, 201):
            del_tag_id = extract_data(del_res).get("id")
            print(f"[SETUP] del_tag_id = {del_tag_id}")

        run("TC25", "DELETE /admin/tags/99999 - ID khong ton tai",
            "delete", f"{url}/admin/tags/99999", [404, 422],
            headers=auth(ADMIN_TOKEN))

        if del_tag_id:
            run("TC26", f"DELETE /admin/tags/{del_tag_id} - user thuong bi 403",
                "delete", f"{url}/admin/tags/{del_tag_id}", 403,
                headers=auth(USER_TOKEN))

            run("TC27", f"DELETE /admin/tags/{del_tag_id} - khong co token",
                "delete", f"{url}/admin/tags/{del_tag_id}", 401,
                headers=auth())

            res = run("TC24", f"DELETE /admin/tags/{del_tag_id} - xoa thanh cong",
                      "delete", f"{url}/admin/tags/{del_tag_id}", [200, 204],
                      headers=auth(ADMIN_TOKEN))
            if res and res.status_code in (200, 204):
                # Verify: không còn trong GET /tags
                all_tags = extract_items(requests.get(f"{url}/tags", headers=auth()))
                ids = [i.get("id") for i in all_tags if isinstance(i, dict)]
                if del_tag_id not in ids:
                    print(f"  [INFO] TC24: tag {del_tag_id} khong con trong list - OK")
                else:
                    print(f"  [WARN] TC24: tag {del_tag_id} van con trong list sau khi xoa")
        else:
            for tc in ["TC24", "TC26", "TC27"]:
                print(f"[SKIP] {tc} - khong tao duoc del_tag_id")
                results.append((tc, "DELETE /admin/tags/{id}", None, "skip"))

    #  POST /admin/amenities 

    if not ADMIN_TOKEN:
        for tc in [f"TC{i}" for i in range(28, 39)]:
            print(f"[SKIP] {tc} - khong co ADMIN_TOKEN")
            results.append((tc, "POST/DELETE /admin/amenities", None, "skip"))
    else:
        amenity_name = f"Test Amenity {ts}"

        res = run("TC28", "POST /admin/amenities - tao day du fields",
                  "post", f"{url}/admin/amenities", [200, 201],
                  headers=auth(ADMIN_TOKEN),
                  json={"name": amenity_name, "icon": "fa-test", "category": "connectivity"})
        if res and res.status_code in (200, 201):
            data = extract_data(res)
            aid  = data.get("id")
            if aid:
                created_amenity_ids.append(aid)
            print(f"  [INFO] TC28: id={aid}, category={data.get('category')}")

        res = run("TC29", "POST /admin/amenities - category la bat buoc (backend require)",
                  "post", f"{url}/admin/amenities", 422,
                  headers=auth(ADMIN_TOKEN),
                  json={"name": f"Amenity Minimal {ts}"})

        run("TC30", "POST /admin/amenities - thieu name",
            "post", f"{url}/admin/amenities", 422,
            headers=auth(ADMIN_TOKEN),
            json={"icon": "fa-test", "category": "connectivity"})

        # TC31: name trùng
        run("TC31", "POST /admin/amenities - name trung",
            "post", f"{url}/admin/amenities", [422, 409],
            headers=auth(ADMIN_TOKEN),
            json={"name": amenity_name})

        run("TC32", "POST /admin/amenities - category sai gia tri",
            "post", f"{url}/admin/amenities", 422,
            headers=auth(ADMIN_TOKEN),
            json={"name": f"Bad Cat {ts}", "category": "invalid"})

        run("TC33", "POST /admin/amenities - user thuong bi 403",
            "post", f"{url}/admin/amenities", 403,
            headers=auth(USER_TOKEN),
            json={"name": "User Amenity"})

        run("TC34", "POST /admin/amenities - khong co token",
            "post", f"{url}/admin/amenities", 401,
            headers=auth(),
            json={"name": "No Token Amenity"})

        #  DELETE /admin/amenities/{id} 

        del_res = requests.post(f"{url}/admin/amenities",
                                headers=auth(ADMIN_TOKEN),
                                json={"name": f"Delete Amenity {ts}", "category": "comfort",
                                      "icon": f"fa-del-{ts}"})
        del_amenity_id = None
        if del_res.status_code in (200, 201):
            del_amenity_id = extract_data(del_res).get("id")
            print(f"[SETUP] del_amenity_id = {del_amenity_id}")
        else:
            print(f"[SETUP] Tao del_amenity that bai: {del_res.status_code} - {del_res.text[:200]}")

        run("TC36", "DELETE /admin/amenities/99999 - ID khong ton tai",
            "delete", f"{url}/admin/amenities/99999", [404, 422],
            headers=auth(ADMIN_TOKEN))

        if del_amenity_id:
            run("TC37", f"DELETE /admin/amenities/{del_amenity_id} - user thuong bi 403",
                "delete", f"{url}/admin/amenities/{del_amenity_id}", 403,
                headers=auth(USER_TOKEN))

            run("TC38", f"DELETE /admin/amenities/{del_amenity_id} - khong co token",
                "delete", f"{url}/admin/amenities/{del_amenity_id}", 401,
                headers=auth())

            res = run("TC35", f"DELETE /admin/amenities/{del_amenity_id} - xoa thanh cong",
                      "delete", f"{url}/admin/amenities/{del_amenity_id}", [200, 204],
                      headers=auth(ADMIN_TOKEN))
            if res and res.status_code in (200, 204):
                all_amenities = extract_items(requests.get(f"{url}/amenities", headers=auth()))
                ids = [i.get("id") for i in all_amenities if isinstance(i, dict)]
                if del_amenity_id not in ids:
                    print(f"  [INFO] TC35: amenity {del_amenity_id} khong con trong list - OK")
                else:
                    print(f"  [WARN] TC35: amenity {del_amenity_id} van con trong list sau khi xoa")
        else:
            for tc in ["TC35", "TC37", "TC38"]:
                print(f"[SKIP] {tc} - khong tao duoc del_amenity_id")
                results.append((tc, "DELETE /admin/amenities/{id}", None, "skip"))

    #  CLEANUP 

    if ADMIN_TOKEN:
        for tid in list(created_tag_ids):
            r = requests.delete(f"{url}/admin/tags/{tid}", headers=auth(ADMIN_TOKEN))
            print(f"  [CLEANUP] DELETE /admin/tags/{tid}  {r.status_code}")
        for aid in list(created_amenity_ids):
            r = requests.delete(f"{url}/admin/amenities/{aid}", headers=auth(ADMIN_TOKEN))
            print(f"  [CLEANUP] DELETE /admin/amenities/{aid}  {r.status_code}")

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
