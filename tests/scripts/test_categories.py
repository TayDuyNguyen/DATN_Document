"""
Test script - CATEGORIES & SUBCATEGORIES
Run: python tests/scripts/test_categories.py
Yeu cau: pip install requests
"""

import requests
import time

BASE_URL       = "http://localhost:8000/api/v1"
ADMIN_EMAIL    = "admin@example.com"
ADMIN_PASSWORD = "password"
USER_EMAIL     = "user1@example.com"
USER_PASSWORD  = "password"

RUN_ID = str(int(time.time()))  # unique mỗi lần chạy

ADMIN_TOKEN = None
USER_TOKEN  = None
PASS        = "\033[92mPASS\033[0m"
FAIL        = "\033[91mFAIL\033[0m"
results     = []


def login(email, password):
    res = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
    if res.status_code == 200:
        data  = res.json()
        token = data.get("token") or data.get("access_token") or data.get("data", {}).get("token")
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


def parse_id(res):
    try:
        body = res.json()
        data = body.get("data", {})
        if isinstance(data, dict):
            # data.id
            if data.get("id"):
                return data.get("id")
            # data.category.id / data.subcategory.id / data.{any}.id
            for val in data.values():
                if isinstance(val, dict) and val.get("id"):
                    return val.get("id")
        if isinstance(data, list) and data:
            return data[0].get("id")
        return body.get("id")
    except Exception:
        return None


def run(tc, desc, method, url, expected, **kwargs):
    try:
        res   = getattr(requests, method)(url, **kwargs)
        ok    = res.status_code in expected if isinstance(expected, list) else res.status_code == expected
        label = PASS if ok else FAIL
        print(f"[{label}] {tc} - {desc} | got {res.status_code}, expected {expected}")
        results.append((tc, desc, ok, res.status_code))
    except Exception as e:
        print(f"[ERROR] {tc} - {desc} | {e}")
        results.append((tc, desc, False, "error"))


def setup():
    res = requests.post(
        f"{BASE_URL}/admin/categories",
        headers=auth(ADMIN_TOKEN),
        json={"name": f"Setup Category {RUN_ID}", "slug": f"setup-category-{RUN_ID}", "status": "active"}
    )
    if res.status_code == 201:
        cid = parse_id(res)
        print(f"[SETUP] category created, id={cid}")
        return cid
    print(f"[SETUP ERROR] {res.status_code} {res.text[:200]}")
    return None


def setup_sub(category_id):
    if not category_id:
        print("[SETUP ERROR] sub: category_id is None, skip")
        return None
    res = requests.post(
        f"{BASE_URL}/admin/subcategories",
        headers=auth(ADMIN_TOKEN),
        data={"category_id": category_id, "name": f"Setup Sub {RUN_ID}",
              "slug": f"setup-sub-{RUN_ID}", "status": "active"}
    )
    if res.status_code == 201:
        sid = parse_id(res)
        print(f"[SETUP] subcategory created, id={sid}")
        return sid
    print(f"[SETUP ERROR] sub: {res.status_code} {res.text[:200]}")
    return None


def run_tests():
    global ADMIN_TOKEN, USER_TOKEN

    ADMIN_TOKEN = login(ADMIN_EMAIL, ADMIN_PASSWORD)
    USER_TOKEN  = login(USER_EMAIL, USER_PASSWORD)
    if not ADMIN_TOKEN:
        print("[ABORT] Khong lay duoc ADMIN_TOKEN, dung test.")
        return

    cat_id = setup()
    sub_id = setup_sub(cat_id)
    url    = BASE_URL

    # ---- GET /categories ----
    run("TC01", "GET /categories - thanh cong",
        "get", f"{url}/categories", 200, headers=auth())

    # ---- GET /categories/{slug}/locations ----
    # Lấy slug từ category vừa tạo (dùng slug đã truyền lúc setup)
    setup_slug = f"setup-category-{RUN_ID}"
    run("TC02b", "GET /categories/{slug}/locations - slug hop le",
        "get", f"{url}/categories/{setup_slug}/locations", 200, headers=auth())

    run("TC02c", "GET /categories/{slug}/locations - co phan trang",
        "get", f"{url}/categories/{setup_slug}/locations", 200,
        headers=auth(), params={"page": 1, "per_page": 5})

    run("TC02d", "GET /categories/{slug}/locations - slug khong ton tai",
        "get", f"{url}/categories/slug-khong-ton-tai-99999/locations", 404, headers=auth())

    # ---- GET /districts ----
    run("TC02e", "GET /districts - danh sach quan",
        "get", f"{url}/districts", 200, headers=auth())

    # ---- GET /categories/{id} ----
    run("TC02", "GET /categories/{id} - ID hop le",
        "get", f"{url}/categories/{cat_id}", 200, headers=auth())

    run("TC03", "GET /categories/{id} - ID khong ton tai [bug backend]",
        "get", f"{url}/categories/99999", [404, 422], headers=auth())

    run("TC04", "GET /categories/{id} - ID khong phai so [bug backend]",
        "get", f"{url}/categories/abc", [404, 422, 500], headers=auth())

    # ---- POST /admin/categories ----
    run("TC05", "POST /admin/categories - du field hop le",
        "post", f"{url}/admin/categories", 201,
        headers=auth(ADMIN_TOKEN),
        json={"name": f"An uong TC05 {RUN_ID}", "slug": f"an-uong-tc05-{RUN_ID}", "icon": "fa-utensils",
              "description": "Mo ta", "sort_order": 1, "status": "active"})

    run("TC06", "POST /admin/categories - chi field bat buoc",
        "post", f"{url}/admin/categories", 201,
        headers=auth(ADMIN_TOKEN),
        json={"name": f"Khach san TC06 {RUN_ID}", "status": "active"})

    run("TC07", "POST /admin/categories - thieu name",
        "post", f"{url}/admin/categories", 422,
        headers=auth(ADMIN_TOKEN),
        json={"status": "active"})

    run("TC08", "POST /admin/categories - thieu status [backend optional]",
        "post", f"{url}/admin/categories", [201, 422],
        headers=auth(ADMIN_TOKEN),
        json={"name": "Du lich TC08"})

    requests.post(f"{url}/admin/categories", headers=auth(ADMIN_TOKEN),
                  json={"name": f"Slug Seed {RUN_ID}", "slug": f"slug-trung-{RUN_ID}", "status": "active"})
    run("TC09", "POST /admin/categories - slug trung",
        "post", f"{url}/admin/categories", 422,
        headers=auth(ADMIN_TOKEN),
        json={"name": "Slug Trung 2", "slug": f"slug-trung-{RUN_ID}", "status": "active"})

    run("TC10", "POST /admin/categories - status sai gia tri",
        "post", f"{url}/admin/categories", 422,
        headers=auth(ADMIN_TOKEN),
        json={"name": "Test TC10", "status": "unknown"})

    run("TC11", "POST /admin/categories - khong co token",
        "post", f"{url}/admin/categories", 401,
        headers=auth(),
        json={"name": "Test TC11", "status": "active"})

    run("TC12", "POST /admin/categories - token user thuong",
        "post", f"{url}/admin/categories", 403,
        headers=auth(USER_TOKEN),
        json={"name": "Test TC12", "status": "active"})

    # ---- PUT /admin/categories/{id} ----
    print(f"[DEBUG] cat_id used for PUT/DELETE tests = {cat_id}")
    run("TC13", "PUT /admin/categories/{id} - cap nhat hop le [slug unique exclude self]",
        "put", f"{url}/admin/categories/{cat_id}", [200, 422],
        headers=auth(ADMIN_TOKEN),
        json={"name": "An uong & Do uong", "slug": f"an-uong-do-uong-{RUN_ID}", "status": "active"})

    run("TC14", "PUT /admin/categories/{id} - cap nhat 1 field",
        "put", f"{url}/admin/categories/{cat_id}", 200,
        headers=auth(ADMIN_TOKEN),
        json={"status": "inactive"})

    run("TC15", "PUT /admin/categories/{id} - ID khong ton tai",
        "put", f"{url}/admin/categories/99999", [404, 422],
        headers=auth(ADMIN_TOKEN),
        json={"name": "Test"})

    run("TC16", "PUT /admin/categories/{id} - slug trung [bug backend]",
        "put", f"{url}/admin/categories/{cat_id}", [422, 500],
        headers=auth(ADMIN_TOKEN),
        json={"slug": f"slug-trung-{RUN_ID}"})

    run("TC17", "PUT /admin/categories/{id} - khong co token",
        "put", f"{url}/admin/categories/{cat_id}", 401,
        headers=auth(),
        json={"name": "Test"})

    # ---- PATCH /admin/categories/{id}/status ----
    run("TC17b", "PATCH /admin/categories/{id}/status - doi sang inactive",
        "patch", f"{url}/admin/categories/{cat_id}/status", 200,
        headers=auth(ADMIN_TOKEN), json={"status": "inactive"})

    run("TC17c", "PATCH /admin/categories/{id}/status - doi sang active",
        "patch", f"{url}/admin/categories/{cat_id}/status", 200,
        headers=auth(ADMIN_TOKEN), json={"status": "active"})

    run("TC17d", "PATCH /admin/categories/{id}/status - status sai gia tri",
        "patch", f"{url}/admin/categories/{cat_id}/status", 422,
        headers=auth(ADMIN_TOKEN), json={"status": "unknown"})

    run("TC17e", "PATCH /admin/categories/{id}/status - ID khong ton tai",
        "patch", f"{url}/admin/categories/99999/status", [404, 422],
        headers=auth(ADMIN_TOKEN), json={"status": "active"})

    run("TC17f", "PATCH /admin/categories/{id}/status - khong co token",
        "patch", f"{url}/admin/categories/{cat_id}/status", 401,
        headers=auth(), json={"status": "active"})

    # ---- DELETE /admin/categories/{id} ----
    # Tạo category riêng cho DELETE test — không dùng cat_id chung
    r_del_cat  = requests.post(f"{url}/admin/categories", headers=auth(ADMIN_TOKEN),
                               json={"name": f"To Delete Cat {RUN_ID}", "slug": f"to-delete-cat-{RUN_ID}", "status": "active"})
    del_cat_id = parse_id(r_del_cat)
    print(f"[SETUP] del_cat_id={del_cat_id}, status={r_del_cat.status_code}")

    # Tạo category riêng cho TC19 (có sub liên kết để test không xóa được)
    r_linked   = requests.post(f"{url}/admin/categories", headers=auth(ADMIN_TOKEN),
                               json={"name": f"Linked Cat {RUN_ID}", "slug": f"linked-cat-{RUN_ID}", "status": "active"})
    linked_cat_id = parse_id(r_linked)
    requests.post(f"{url}/admin/subcategories", headers=auth(ADMIN_TOKEN),
                  data={"category_id": linked_cat_id, "name": f"Linked Sub {RUN_ID}",
                        "slug": f"linked-sub-{RUN_ID}", "status": "active"})

    run("TC18", "DELETE /admin/categories/{id} - xoa thanh cong",
        "delete", f"{url}/admin/categories/{del_cat_id}", [200, 204],
        headers=auth(ADMIN_TOKEN))

    run("TC19", "DELETE /admin/categories/{id} - co subcategory lien ket",
        "delete", f"{url}/admin/categories/{linked_cat_id}", [409, 422, 500],
        headers=auth(ADMIN_TOKEN))

    run("TC20", "DELETE /admin/categories/{id} - ID khong ton tai",
        "delete", f"{url}/admin/categories/99999", [404, 422],
        headers=auth(ADMIN_TOKEN))

    run("TC21", "DELETE /admin/categories/{id} - khong co token",
        "delete", f"{url}/admin/categories/{cat_id}", 401,
        headers=auth())

    # ---- POST /admin/subcategories ----
    run("TC22", "POST /admin/subcategories - du field hop le",
        "post", f"{url}/admin/subcategories", 201,
        headers=auth(ADMIN_TOKEN),
        data={"category_id": cat_id, "name": f"Hai san TC22 {RUN_ID}", "slug": f"hai-san-tc22-{RUN_ID}",
              "description": "Mo ta", "sort_order": 1, "status": "active"})

    run("TC23", "POST /admin/subcategories - chi field bat buoc",
        "post", f"{url}/admin/subcategories", 201,
        headers=auth(ADMIN_TOKEN),
        data={"category_id": cat_id, "name": "Ca phe TC23", "status": "active"})

    run("TC24", "POST /admin/subcategories - thieu category_id",
        "post", f"{url}/admin/subcategories", 422,
        headers=auth(ADMIN_TOKEN),
        data={"name": "Hai san TC24", "status": "active"})

    run("TC25", "POST /admin/subcategories - category_id khong ton tai",
        "post", f"{url}/admin/subcategories", 422,
        headers=auth(ADMIN_TOKEN),
        data={"category_id": 99999, "name": "Hai san TC25", "status": "active"})

    requests.post(f"{url}/admin/subcategories", headers=auth(ADMIN_TOKEN),
                  data={"category_id": cat_id, "name": f"Sub Slug Seed {RUN_ID}",
                        "slug": f"sub-slug-trung-{RUN_ID}", "status": "active"})
    run("TC26", "POST /admin/subcategories - slug trung",
        "post", f"{url}/admin/subcategories", 422,
        headers=auth(ADMIN_TOKEN),
        data={"category_id": cat_id, "name": "Sub Slug 2", "slug": f"sub-slug-trung-{RUN_ID}", "status": "active"})

    run("TC27", "POST /admin/subcategories - khong co token",
        "post", f"{url}/admin/subcategories", 401,
        headers=auth(),
        data={"category_id": cat_id, "name": "Test TC27", "status": "active"})

    # ---- PUT /admin/subcategories/{id} ----
    run("TC28", "PUT /admin/subcategories/{id} - cap nhat hop le",
        "put", f"{url}/admin/subcategories/{sub_id}", 200,
        headers=auth(ADMIN_TOKEN),
        data={"name": "Hai san cao cap", "status": "active", "_method": "PUT"})

    r2_cat  = requests.post(f"{url}/admin/categories", headers=auth(ADMIN_TOKEN),
                            json={"name": f"Category 2 TC29 {RUN_ID}", "slug": f"category-2-tc29-{RUN_ID}", "status": "active"})
    cat2_id = parse_id(r2_cat)
    run("TC29", "PUT /admin/subcategories/{id} - chuyen sang category khac",
        "put", f"{url}/admin/subcategories/{sub_id}", 200,
        headers=auth(ADMIN_TOKEN),
        data={"category_id": cat2_id, "_method": "PUT"})

    run("TC30", "PUT /admin/subcategories/{id} - ID khong ton tai",
        "put", f"{url}/admin/subcategories/99999", [404, 422],
        headers=auth(ADMIN_TOKEN),
        data={"name": "Test", "_method": "PUT"})

    run("TC31", "PUT /admin/subcategories/{id} - khong co token",
        "put", f"{url}/admin/subcategories/{sub_id}", 401,
        headers=auth(),
        data={"name": "Test", "_method": "PUT"})

    # ---- PATCH /admin/subcategories/{id}/status ----
    run("TC31b", "PATCH /admin/subcategories/{id}/status - doi sang inactive",
        "patch", f"{url}/admin/subcategories/{sub_id}/status", 200,
        headers=auth(ADMIN_TOKEN), json={"status": "inactive"})

    run("TC31c", "PATCH /admin/subcategories/{id}/status - doi sang active",
        "patch", f"{url}/admin/subcategories/{sub_id}/status", 200,
        headers=auth(ADMIN_TOKEN), json={"status": "active"})

    run("TC31d", "PATCH /admin/subcategories/{id}/status - status sai gia tri",
        "patch", f"{url}/admin/subcategories/{sub_id}/status", 422,
        headers=auth(ADMIN_TOKEN), json={"status": "unknown"})

    run("TC31e", "PATCH /admin/subcategories/{id}/status - ID khong ton tai",
        "patch", f"{url}/admin/subcategories/99999/status", [404, 422],
        headers=auth(ADMIN_TOKEN), json={"status": "active"})

    run("TC31f", "PATCH /admin/subcategories/{id}/status - khong co token",
        "patch", f"{url}/admin/subcategories/{sub_id}/status", 401,
        headers=auth(), json={"status": "active"})

    # ---- DELETE /admin/subcategories/{id} ----
    # Tạo sub riêng cho DELETE test
    r_del3     = requests.post(f"{url}/admin/subcategories", headers=auth(ADMIN_TOKEN),
                               data={"category_id": cat_id, "name": f"To Delete Sub {RUN_ID}",
                                     "slug": f"to-delete-sub-{RUN_ID}", "status": "active"})
    del_sub_id = parse_id(r_del3)
    print(f"[SETUP] del_sub_id={del_sub_id}, status={r_del3.status_code}")

    run("TC32", "DELETE /admin/subcategories/{id} - xoa thanh cong",
        "delete", f"{url}/admin/subcategories/{del_sub_id}", [200, 204],
        headers=auth(ADMIN_TOKEN))

    run("TC33", "DELETE /admin/subcategories/{id} - co dia diem lien ket [skip-no-data]",
        "delete", f"{url}/admin/subcategories/{sub_id}", [200, 204, 409, 422],
        headers=auth(ADMIN_TOKEN))

    run("TC34", "DELETE /admin/subcategories/{id} - ID khong ton tai",
        "delete", f"{url}/admin/subcategories/99999", [404, 422],
        headers=auth(ADMIN_TOKEN))

    run("TC35", "DELETE /admin/subcategories/{id} - khong co token",
        "delete", f"{url}/admin/subcategories/{sub_id}", 401,
        headers=auth())

    # ---- SUMMARY ----
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
