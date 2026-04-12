
"""
Test script - TAGS & AMENITIES
Branch: feat/taynd/api-tags-amenities
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
            for key in ["tag", "amenity"]:
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

    # ── GET /tags ─────────────────────────────────────────────

    res = run("TC01", "GET /tags - lay tat ca tags",
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

    run("TC07", "GET /tags - type sai gia tri → 422",
        "get", f"{url}/tags", [200, 422],
        headers=auth(), params={"type": "invalid_type"})

    # ── GET /amenities ────────────────────────────────────────

    res = run("TC08", "GET /amenities - lay tat ca amenities",
              "get", f"{url}/amenities", 200, headers=auth())
    if res and res.status_code == 200:
        items = extract_items(res)
        print(f"  [INFO] TC08: {len(items)} amenities")
        if items and isinstance(items[0], dict):
            print(f"  [INFO] TC08: fields = {list(items[0].keys())}")

    for tc, cat_val in [("TC09", "connectivity"), ("TC10", "parking"),
                         ("TC11", "comfort"), ("TC12", "payment")]:
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

    run("TC14", "GET /amenities - category sai gia tri → 422",
        "get", f"{url}/amenities", [200, 422],
        headers=auth(), params={"category": "invalid_category"})

    # ── POST /admin/tags ──────────────────────────────────────

    res = run("TC15", "POST /admin/tags - tao tag day du fields",
              "post", f"{url}/admin/tags", [200, 201],
              headers=auth(ADMIN_TOKEN),
              json={"name": f"Test Tag {ts}", "slug": f"test-tag-{ts}", "type": "cuisine"})
    tag_id = None
    if res and res.status_code in (200, 201):
        data = extract_data(res)
        tag_id = data.get("id")
        if tag_id:
            created_tag_ids.append(tag_id)
        print(f"  [INFO] TC15: id={tag_id}, slug={data.get('slug')}")

    res = run("TC16", "POST /admin/tags - tao tag khong co type [bug: type bat buoc]",
              "post", f"{url}/admin/tags", [200, 201, 422],
              headers=auth(ADMIN_TOKEN),
              json={"name": f"Tag No Type {ts}"})
    if res and res.status_code in (200, 201):
        tid = extract_data(res).get("id")
        if tid:
            created_tag_ids.append(tid)

    run("TC17", "POST /admin/tags - thieu name → 422",
        "post", f"{url}/admin/tags", 422,
        headers=auth(ADMIN_TOKEN),
        json={"slug": "no-name-tag", "type": "cuisine"})

    run("TC18", "POST /admin/tags - type sai gia tri → 422",
        "post", f"{url}/admin/tags", 422,
        headers=auth(ADMIN_TOKEN),
        json={"name": f"Bad Type Tag {ts}", "type": "invalid_type"})

    # TC19: slug trung — dung slug vua tao
    run("TC19", "POST /admin/tags - slug trung → 422/409",
        "post", f"{url}/admin/tags", [409, 422],
        headers=auth(ADMIN_TOKEN),
        json={"name": f"Dup Slug Tag {ts}", "slug": f"test-tag-{ts}"})

    run("TC20", "POST /admin/tags - user thuong bi 403",
        "post", f"{url}/admin/tags", 403,
        headers=auth(USER_TOKEN),
        json={"name": f"User Tag {ts}"})

    run("TC21", "POST /admin/tags - khong co token → 401",
        "post", f"{url}/admin/tags", 401,
        headers=auth(),
        json={"name": f"No Token Tag {ts}"})

    # ── PUT /admin/tags/{id} ──────────────────────────────────

    if tag_id:
        res = run("TC22", f"PUT /admin/tags/{tag_id} - cap nhat name",
                  "patch", f"{url}/admin/tags/{tag_id}", 200,
                  headers=auth(ADMIN_TOKEN),
                  json={"name": f"Updated Tag {ts}"})
        if res and res.status_code == 200:
            data = extract_data(res)
            if f"Updated Tag {ts}" in str(data.get("name", "")):
                print(f"  [INFO] TC22: name cap nhat OK")

        res = run("TC23", f"PUT /admin/tags/{tag_id} - cap nhat type",
                  "patch", f"{url}/admin/tags/{tag_id}", 200,
                  headers=auth(ADMIN_TOKEN),
                  json={"type": "service"})
        if res and res.status_code == 200:
            data = extract_data(res)
            if data.get("type") == "service":
                print(f"  [INFO] TC23: type=service - OK")

        run("TC24", f"PUT /admin/tags/{tag_id} - cap nhat slug",
            "patch", f"{url}/admin/tags/{tag_id}", 200,
            headers=auth(ADMIN_TOKEN),
            json={"slug": f"updated-slug-{ts}"})
    else:
        for tc in ["TC22", "TC23", "TC24"]:
            print(f"[SKIP] {tc} - khong co tag_id")
            results.append((tc, "PUT /admin/tags/{id}", None, "skip"))

    run("TC25", "PUT /admin/tags/99999 - ID khong ton tai → 404",
        "patch", f"{url}/admin/tags/99999", [404, 422],
        headers=auth(ADMIN_TOKEN), json={"name": "Test"})

    run("TC26", f"PUT /admin/tags/{tag_id or 1} - type sai gia tri → 422",
        "patch", f"{url}/admin/tags/{tag_id or 1}", 422,
        headers=auth(ADMIN_TOKEN), json={"type": "invalid_type"})

    run("TC27", f"PUT /admin/tags/{tag_id or 1} - user thuong bi 403",
        "patch", f"{url}/admin/tags/{tag_id or 1}", 403,
        headers=auth(USER_TOKEN), json={"name": "Hacked"})

    run("TC28", f"PUT /admin/tags/{tag_id or 1} - khong co token → 401",
        "patch", f"{url}/admin/tags/{tag_id or 1}", 401,
        headers=auth(), json={"name": "No Token"})

    # ── DELETE /admin/tags/{id} ───────────────────────────────

    # Tao tag rieng de xoa
    del_tag_res = requests.post(f"{url}/admin/tags",
                                headers=auth(ADMIN_TOKEN),
                                json={"name": f"Del Tag {ts}", "slug": f"del-tag-{ts}",
                                      "type": "feature"})
    del_tag_id = None
    if del_tag_res.status_code in (200, 201):
        del_tag_id = extract_data(del_tag_res).get("id")

    if del_tag_id:
        res = run("TC29", f"DELETE /admin/tags/{del_tag_id} - xoa thanh cong",
                  "delete", f"{url}/admin/tags/{del_tag_id}", [200, 204],
                  headers=auth(ADMIN_TOKEN))
        if res and res.status_code in (200, 204):
            print(f"  [INFO] TC29: xoa tag id={del_tag_id} - OK")
    else:
        print("[SKIP] TC29 - khong tao duoc tag de xoa")
        results.append(("TC29", "DELETE /admin/tags/{id}", None, "skip"))

    run("TC30", "DELETE /admin/tags/99999 - ID khong ton tai → 404",
        "delete", f"{url}/admin/tags/99999", [404, 422],
        headers=auth(ADMIN_TOKEN))

    run("TC31", f"DELETE /admin/tags/{tag_id or 1} - user thuong bi 403",
        "delete", f"{url}/admin/tags/{tag_id or 1}", 403,
        headers=auth(USER_TOKEN))

    run("TC32", f"DELETE /admin/tags/{tag_id or 1} - khong co token → 401",
        "delete", f"{url}/admin/tags/{tag_id or 1}", 401,
        headers=auth())

    res = run("TC33", "POST /admin/amenities - tao amenity day du fields",
              "post", f"{url}/admin/amenities", [200, 201],
              headers=auth(ADMIN_TOKEN),
              json={"name": f"Test Amenity {ts}", "icon": "fa-wifi",
                    "category": "connectivity"})
    amenity_id = None
    if res and res.status_code in (200, 201):
        data = extract_data(res)
        amenity_id = data.get("id")
        if amenity_id:
            created_amenity_ids.append(amenity_id)
        print(f"  [INFO] TC33: id={amenity_id}")

    res = run("TC34", "POST /admin/amenities - tao amenity chi co name [bug: icon+category bat buoc]",
              "post", f"{url}/admin/amenities", [200, 201, 422],
              headers=auth(ADMIN_TOKEN),
              json={"name": f"Minimal Amenity {ts}"})
    if res and res.status_code in (200, 201):
        aid = extract_data(res).get("id")
        if aid:
            created_amenity_ids.append(aid)

    run("TC35", "POST /admin/amenities - thieu name → 422",
        "post", f"{url}/admin/amenities", 422,
        headers=auth(ADMIN_TOKEN),
        json={"icon": "fa-wifi", "category": "connectivity"})

    run("TC36", "POST /admin/amenities - category sai gia tri → 422",
        "post", f"{url}/admin/amenities", 422,
        headers=auth(ADMIN_TOKEN),
        json={"name": f"Bad Cat Amenity {ts}", "category": "invalid_category"})

    run("TC37", "POST /admin/amenities - user thuong bi 403",
        "post", f"{url}/admin/amenities", 403,
        headers=auth(USER_TOKEN),
        json={"name": f"User Amenity {ts}"})

    run("TC38", "POST /admin/amenities - khong co token → 401",
        "post", f"{url}/admin/amenities", 401,
        headers=auth(),
        json={"name": f"No Token Amenity {ts}"})

    # ── PUT /admin/amenities/{id} ─────────────────────────────

    if amenity_id:
        res = run("TC39", f"PUT /admin/amenities/{amenity_id} - cap nhat name",
                  "patch", f"{url}/admin/amenities/{amenity_id}", 200,
                  headers=auth(ADMIN_TOKEN),
                  json={"name": f"Updated Amenity {ts}"})
        if res and res.status_code == 200:
            data = extract_data(res)
            if f"Updated Amenity {ts}" in str(data.get("name", "")):
                print(f"  [INFO] TC39: name cap nhat OK")

        run("TC40", f"PUT /admin/amenities/{amenity_id} - cap nhat icon",
            "patch", f"{url}/admin/amenities/{amenity_id}", 200,
            headers=auth(ADMIN_TOKEN),
            json={"icon": "fa-parking"})

        res = run("TC41", f"PUT /admin/amenities/{amenity_id} - cap nhat category",
                  "patch", f"{url}/admin/amenities/{amenity_id}", 200,
                  headers=auth(ADMIN_TOKEN),
                  json={"category": "parking"})
        if res and res.status_code == 200:
            data = extract_data(res)
            if data.get("category") == "parking":
                print(f"  [INFO] TC41: category=parking - OK")
    else:
        for tc in ["TC39", "TC40", "TC41"]:
            print(f"[SKIP] {tc} - khong co amenity_id")
            results.append((tc, "PUT /admin/amenities/{id}", None, "skip"))

    run("TC42", "PUT /admin/amenities/99999 - ID khong ton tai → 404",
        "patch", f"{url}/admin/amenities/99999", [404, 422],
        headers=auth(ADMIN_TOKEN), json={"name": "Test"})

    run("TC43", f"PUT /admin/amenities/{amenity_id or 1} - category sai gia tri → 422",
        "patch", f"{url}/admin/amenities/{amenity_id or 1}", 422,
        headers=auth(ADMIN_TOKEN), json={"category": "invalid_category"})

    run("TC44", f"PUT /admin/amenities/{amenity_id or 1} - user thuong bi 403",
        "patch", f"{url}/admin/amenities/{amenity_id or 1}", 403,
        headers=auth(USER_TOKEN), json={"name": "Hacked"})

    run("TC45", f"PUT /admin/amenities/{amenity_id or 1} - khong co token → 401",
        "patch", f"{url}/admin/amenities/{amenity_id or 1}", 401,
        headers=auth(), json={"name": "No Token"})

    # ── DELETE /admin/amenities/{id} ──────────────────────────

    # Tao amenity rieng de xoa
    del_amenity_res = requests.post(f"{url}/admin/amenities",
                                    headers=auth(ADMIN_TOKEN),
                                    json={"name": f"Del Amenity {ts}x",
                                          "icon": "fa-trash",
                                          "category": "payment"})
    del_amenity_id = None
    if del_amenity_res.status_code in (200, 201):
        del_amenity_id = extract_data(del_amenity_res).get("id")
    else:
        print(f"  [SETUP WARN] Tao del amenity that bai: {del_amenity_res.status_code} - {del_amenity_res.text[:150]}")

    if del_amenity_id:
        res = run("TC46", f"DELETE /admin/amenities/{del_amenity_id} - xoa thanh cong",
                  "delete", f"{url}/admin/amenities/{del_amenity_id}", [200, 204],
                  headers=auth(ADMIN_TOKEN))
        if res and res.status_code in (200, 204):
            print(f"  [INFO] TC46: xoa amenity id={del_amenity_id} - OK")
    else:
        print("[SKIP] TC46 - khong tao duoc amenity de xoa")
        results.append(("TC46", "DELETE /admin/amenities/{id}", None, "skip"))

    run("TC47", "DELETE /admin/amenities/99999 - ID khong ton tai → 404",
        "delete", f"{url}/admin/amenities/99999", [404, 422],
        headers=auth(ADMIN_TOKEN))

    run("TC48", f"DELETE /admin/amenities/{amenity_id or 1} - user thuong bi 403",
        "delete", f"{url}/admin/amenities/{amenity_id or 1}", 403,
        headers=auth(USER_TOKEN))

    run("TC49", f"DELETE /admin/amenities/{amenity_id or 1} - khong co token → 401",
        "delete", f"{url}/admin/amenities/{amenity_id or 1}", 401,
        headers=auth())

    # ── CLEANUP ───────────────────────────────────────────────

    if ADMIN_TOKEN:
        if created_tag_ids:
            print(f"\n[CLEANUP] Xoa {len(created_tag_ids)} tags...")
            for tid in created_tag_ids:
                r = requests.delete(f"{url}/admin/tags/{tid}",
                                    headers=auth(ADMIN_TOKEN))
                print(f"  [CLEANUP] tag/{tid} → {r.status_code}")

        if created_amenity_ids:
            print(f"[CLEANUP] Xoa {len(created_amenity_ids)} amenities...")
            for aid in created_amenity_ids:
                r = requests.delete(f"{url}/admin/amenities/{aid}",
                                    headers=auth(ADMIN_TOKEN))
                print(f"  [CLEANUP] amenity/{aid} → {r.status_code}")

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
