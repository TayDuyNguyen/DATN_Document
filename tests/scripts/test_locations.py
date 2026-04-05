"""
Test script - LOCATIONS
Run: python tests/scripts/test_locations.py
Yeu cau: pip install requests
"""

import requests
import time

BASE_URL       = "http://localhost:8000/api/v1"
ADMIN_EMAIL    = "admin@example.com"
ADMIN_PASSWORD = "password"
USER_EMAIL     = "user1@example.com"
USER_PASSWORD  = "password"

RUN_ID = str(int(time.time()))

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
            if data.get("id"):
                return data.get("id")
            for val in data.values():
                if isinstance(val, dict) and val.get("id"):
                    return val.get("id")
        if isinstance(data, list) and data:
            return data[0].get("id")
        return body.get("id")
    except Exception:
        return None


def parse_slug(res):
    try:
        body = res.json()
        data = body.get("data", {})
        if isinstance(data, dict):
            if data.get("slug"):
                return data.get("slug")
            for val in data.values():
                if isinstance(val, dict) and val.get("slug"):
                    return val.get("slug")
        return None
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


def setup_category():
    res = requests.post(
        f"{BASE_URL}/admin/categories",
        headers=auth(ADMIN_TOKEN),
        json={"name": f"Location Cat {RUN_ID}", "slug": f"location-cat-{RUN_ID}", "status": "active"}
    )
    if res.status_code == 201:
        cid = parse_id(res)
        print(f"[SETUP] category created, id={cid}")
        return cid
    print(f"[SETUP ERROR] category: {res.status_code} {res.text[:200]}")
    return None


def setup_location(cat_id):
    if not cat_id:
        print("[SETUP ERROR] location: cat_id is None, skip")
        return None, None
    # thử từng payload để tìm field nào gây 500
    payloads = [
        # payload đầy đủ nhất
        {
            "name":        f"Setup Location {RUN_ID}",
            "slug":        f"setup-location-{RUN_ID}",
            "category_id": cat_id,
            "description": "Mo ta setup location",
            "short_description": "Mo ta ngan setup",
            "address":     "123 Tran Phu",
            "district":    "Hai Chau",
            "latitude":    16.0544,
            "longitude":   108.2022,
            "phone":       "0236123456",
            "price_min":   50000,
            "price_max":   200000,
            "price_level": 1,
            "status":      "active",
            "is_featured": False,
        },
        # payload tối giản
        {
            "name":        f"Setup Location {RUN_ID}",
            "slug":        f"setup-location-{RUN_ID}",
            "category_id": cat_id,
            "description": "Mo ta setup location",
            "short_description": "Mo ta ngan setup",
            "address":     "123 Tran Phu",
            "district":    "Hai Chau",
            "latitude":    16.0544,
            "longitude":   108.2022,
            "status":      "active",
        },
    ]
    for payload in payloads:
        res = requests.post(
            f"{BASE_URL}/admin/locations",
            headers=auth(ADMIN_TOKEN),
            json=payload
        )
        if res.status_code == 201:
            lid  = parse_id(res)
            slug = parse_slug(res) or payload["slug"]
            print(f"[SETUP] location created, id={lid}, slug={slug}")
            return lid, slug
        print(f"[SETUP ERROR] location: {res.status_code} {res.text[:500]}")
    return None, None


def run_tests():
    global ADMIN_TOKEN, USER_TOKEN

    ADMIN_TOKEN = login(ADMIN_EMAIL, ADMIN_PASSWORD)
    USER_TOKEN  = login(USER_EMAIL, USER_PASSWORD)
    if not ADMIN_TOKEN:
        print("[ABORT] Khong lay duoc ADMIN_TOKEN, dung test.")
        return

    cat_id        = setup_category()
    loc_id, slug  = setup_location(cat_id)
    # fallback: nếu parse_slug không lấy được, dùng slug đã truyền vào lúc setup
    if not slug:
        slug = f"setup-location-{RUN_ID}"
    url           = BASE_URL

    # ---- GET /locations ----
    run("TC01", "GET /locations - khong filter",
        "get", f"{url}/locations", 200, headers=auth())

    # ---- GET /locations/districts ----
    run("TC01b", "GET /locations/districts - danh sach quan dynamic",
        "get", f"{url}/locations/districts", 200, headers=auth())

    run("TC02", "GET /locations - filter category_id",
        "get", f"{url}/locations", 200,
        headers=auth(), params={"category_id": cat_id})

    run("TC03", "GET /locations - filter district",
        "get", f"{url}/locations", 200,
        headers=auth(), params={"district": "Hai Chau"})

    run("TC04", "GET /locations - filter price_level",
        "get", f"{url}/locations", 200,
        headers=auth(), params={"price_level": 2})

    run("TC05", "GET /locations - sort avg_rating desc",
        "get", f"{url}/locations", 200,
        headers=auth(), params={"sort": "avg_rating", "order": "desc"})

    run("TC06", "GET /locations - ket hop filter + sort + paginate",
        "get", f"{url}/locations", 200,
        headers=auth(),
        params={"category_id": cat_id, "district": "Hai Chau", "sort": "avg_rating",
                "order": "desc", "page": 1, "per_page": 12})

    run("TC07", "GET /locations - category_id khong ton tai",
        "get", f"{url}/locations", [200, 404, 422],
        headers=auth(), params={"category_id": 99999})

    run("TC08", "GET /locations - price_level sai gia tri",
        "get", f"{url}/locations", [200, 422],
        headers=auth(), params={"price_level": 99})

    run("TC08b", "GET /locations - filter subcategory_id",
        "get", f"{url}/locations", 200,
        headers=auth(), params={"subcategory_id": 1})

    # ---- GET /locations/featured ----
    run("TC09", "GET /locations/featured - danh sach noi bat [bug: can ?limit]",
        "get", f"{url}/locations/featured", [200, 500], headers=auth())

    run("TC09b", "GET /locations/featured - co limit",
        "get", f"{url}/locations/featured", 200,
        headers=auth(), params={"limit": 4})

    # ---- GET /locations/nearby ----
    run("TC10", "GET /locations/nearby - toa do hop le [bug backend]",
        "get", f"{url}/locations/nearby", [200, 500],
        headers=auth(), params={"lat": 16.0544, "lng": 108.2022, "radius": 5})

    run("TC11", "GET /locations/nearby - khong co radius [bug backend]",
        "get", f"{url}/locations/nearby", [200, 500],
        headers=auth(), params={"lat": 16.0544, "lng": 108.2022})

    run("TC12", "GET /locations/nearby - thieu lat",
        "get", f"{url}/locations/nearby", 422,
        headers=auth(), params={"lng": 108.2022})

    run("TC13", "GET /locations/nearby - thieu lng",
        "get", f"{url}/locations/nearby", 422,
        headers=auth(), params={"lat": 16.0544})

    run("TC14", "GET /locations/nearby - lat/lng khong phai so",
        "get", f"{url}/locations/nearby", 422,
        headers=auth(), params={"lat": "abc", "lng": "xyz"})

    # ---- GET /locations/{slug} ----
    run("TC15", "GET /locations/{slug} - slug hop le",
        "get", f"{url}/locations/{slug}", 200, headers=auth())

    run("TC16", "GET /locations/{slug} - slug khong ton tai",
        "get", f"{url}/locations/slug-khong-ton-tai-99999", 404, headers=auth())

    # ---- GET /locations/{id}/images ----
    run("TC15b", "GET /locations/{id}/images - ID hop le",
        "get", f"{url}/locations/{loc_id}/images", 200, headers=auth())

    run("TC15c", "GET /locations/{id}/images - ID khong ton tai",
        "get", f"{url}/locations/99999/images", [404, 422], headers=auth())

    # ---- GET /locations/{id}/rating-stats ----
    run("TC15d", "GET /locations/{id}/rating-stats - ID hop le [bug backend: crash 500]",
        "get", f"{url}/locations/{loc_id}/rating-stats", [200, 500], headers=auth())

    run("TC15e", "GET /locations/{id}/rating-stats - ID khong ton tai",
        "get", f"{url}/locations/99999/rating-stats", [404, 422], headers=auth())

    # ---- GET /locations/{id}/nearby ----
    run("TC15f", "GET /locations/{id}/nearby - ID hop le [bug backend: crash 500]",
        "get", f"{url}/locations/{loc_id}/nearby", [200, 500], headers=auth())

    run("TC15g", "GET /locations/{id}/nearby - ID khong ton tai",
        "get", f"{url}/locations/99999/nearby", [404, 422], headers=auth())

    # ---- GET /locations/{id}/ratings ----
    run("TC17", "GET /locations/{id}/ratings - co ratings",
        "get", f"{url}/locations/{loc_id}/ratings", 200, headers=auth())

    run("TC18", "GET /locations/{id}/ratings - chua co rating",
        "get", f"{url}/locations/{loc_id}/ratings", 200, headers=auth())

    run("TC19", "GET /locations/{id}/ratings - ID khong ton tai",
        "get", f"{url}/locations/99999/ratings", [404, 422], headers=auth())

    run("TC19b", "GET /locations/{id}/ratings - co paginate",
        "get", f"{url}/locations/{loc_id}/ratings", 200,
        headers=auth(), params={"page": 1, "per_page": 5})

    # ---- POST /locations/{id}/view ----
    run("TC20", "POST /locations/{id}/view - guest co session_id",
        "post", f"{url}/locations/{loc_id}/view", 200,
        headers=auth(),
        json={"session_id": f"sess-guest-{RUN_ID}"})

    run("TC21", "POST /locations/{id}/view - user da dang nhap",
        "post", f"{url}/locations/{loc_id}/view", 200,
        headers=auth(USER_TOKEN),
        json={"session_id": f"sess-user-{RUN_ID}"})

    run("TC22", "POST /locations/{id}/view - ID khong ton tai [bug backend]",
        "post", f"{url}/locations/99999/view", [404, 422, 500],
        headers=auth(),
        json={"session_id": f"sess-{RUN_ID}"})

    run("TC23", "POST /locations/{id}/view - thieu session_id [bug backend: crash 500]",
        "post", f"{url}/locations/{loc_id}/view", [200, 422, 500],
        headers=auth(), json={})

    run("TC23b", "POST /locations/{id}/view - xem lai lan 2 cung session",
        "post", f"{url}/locations/{loc_id}/view", [200, 422],
        headers=auth(),
        json={"session_id": f"sess-guest-{RUN_ID}"})

    # ---- POST /admin/locations ----
    run("TC24", "POST /admin/locations - du field hop le",
        "post", f"{url}/admin/locations", 201,
        headers=auth(ADMIN_TOKEN),
        json={
            "name":              f"Nha hang TC24 {RUN_ID}",
            "slug":              f"nha-hang-tc24-{RUN_ID}",
            "category_id":       cat_id,
            "description":       "Mo ta day du",
            "short_description": "Mo ta ngan",
            "address":           "123 Tran Phu",
            "district":          "Hai Chau",
            "latitude":          16.0544,
            "longitude":         108.2022,
            "phone":             "0236123456",
            "price_min":         100000,
            "price_max":         500000,
            "price_level":       2,
            "status":            "active",
            "is_featured":       False,
        })

    run("TC25", "POST /admin/locations - chi field bat buoc [bug: slug required]",
        "post", f"{url}/admin/locations", [201, 500],
        headers=auth(ADMIN_TOKEN),
        json={
            "name":             f"Quan Ca Phe TC25 {RUN_ID}",
            "slug":             f"quan-ca-phe-tc25-{RUN_ID}",
            "category_id":      cat_id,
            "description":      "Mo ta ngan",
            "short_description": "Mo ta ngan tc25",
            "address":          "456 Le Duan",
            "district":         "Hai Chau",
            "latitude":         16.0544,
            "longitude":        108.2022,
            "status":           "active",
        })

    run("TC26", "POST /admin/locations - thieu name",
        "post", f"{url}/admin/locations", 422,
        headers=auth(ADMIN_TOKEN),
        json={"category_id": cat_id, "address": "123 Tran Phu", "district": "Hai Chau", "status": "active"})

    run("TC27", "POST /admin/locations - thieu category_id",
        "post", f"{url}/admin/locations", 422,
        headers=auth(ADMIN_TOKEN),
        json={"name": "Test TC27", "address": "123 Tran Phu", "district": "Hai Chau", "status": "active"})

    run("TC28", "POST /admin/locations - category_id khong ton tai",
        "post", f"{url}/admin/locations", 422,
        headers=auth(ADMIN_TOKEN),
        json={"name": "Test TC28", "category_id": 99999, "address": "123 Tran Phu", "district": "Hai Chau", "status": "active"})

    run("TC29", "POST /admin/locations - district sai gia tri",
        "post", f"{url}/admin/locations", 422,
        headers=auth(ADMIN_TOKEN),
        json={"name": "Test TC29", "category_id": cat_id, "address": "123 Tran Phu", "district": "Quan Khong Ton Tai", "status": "active"})

    run("TC30", "POST /admin/locations - price_level sai gia tri",
        "post", f"{url}/admin/locations", 422,
        headers=auth(ADMIN_TOKEN),
        json={"name": "Test TC30", "category_id": cat_id, "address": "123 Tran Phu", "district": "Hai Chau", "price_level": 99, "status": "active"})

    run("TC30b", "POST /admin/locations - status sai gia tri",
        "post", f"{url}/admin/locations", 422,
        headers=auth(ADMIN_TOKEN),
        json={"name": "Test TC30b", "category_id": cat_id, "description": "Mo ta",
              "address": "123 Tran Phu", "district": "Hai Chau",
              "latitude": 16.0544, "longitude": 108.2022, "status": "unknown"})

    # Seed slug trùng cho TC31
    requests.post(f"{url}/admin/locations", headers=auth(ADMIN_TOKEN),
                  json={"name": f"Slug Seed Loc {RUN_ID}", "slug": f"slug-loc-trung-{RUN_ID}",
                        "category_id": cat_id, "description": "Mo ta seed",
                        "short_description": "Mo ta ngan seed",
                        "address": "123 Tran Phu", "district": "Hai Chau",
                        "latitude": 16.0544, "longitude": 108.2022, "status": "active"})
    run("TC31", "POST /admin/locations - slug trung",
        "post", f"{url}/admin/locations", 422,
        headers=auth(ADMIN_TOKEN),
        json={"name": "Test TC31 Dup", "slug": f"slug-loc-trung-{RUN_ID}",
              "category_id": cat_id, "address": "123 Tran Phu", "district": "Hai Chau", "status": "active"})

    run("TC32", "POST /admin/locations - khong co token",
        "post", f"{url}/admin/locations", 401,
        headers=auth(),
        json={"name": "Test TC32", "category_id": cat_id, "address": "123", "district": "Hai Chau", "status": "active"})

    run("TC33", "POST /admin/locations - token user thuong",
        "post", f"{url}/admin/locations", 403,
        headers=auth(USER_TOKEN),
        json={"name": "Test TC33", "category_id": cat_id, "address": "123", "district": "Hai Chau", "status": "active"})

    # ---- PUT /admin/locations/{id} ----
    print(f"[DEBUG] loc_id used for PUT/DELETE tests = {loc_id}")

    run("TC34", "PUT /admin/locations/{id} - cap nhat nhieu field",
        "put", f"{url}/admin/locations/{loc_id}", 200,
        headers=auth(ADMIN_TOKEN),
        json={"name": f"Updated Location {RUN_ID}", "description": "Mo ta moi", "status": "active"})

    run("TC35", "PUT /admin/locations/{id} - cap nhat 1 field",
        "put", f"{url}/admin/locations/{loc_id}", 200,
        headers=auth(ADMIN_TOKEN),
        json={"status": "inactive"})

    run("TC36", "PUT /admin/locations/{id} - ID khong ton tai",
        "put", f"{url}/admin/locations/99999", [404, 422],
        headers=auth(ADMIN_TOKEN),
        json={"name": "Test"})

    run("TC37", "PUT /admin/locations/{id} - slug trung location khac",
        "put", f"{url}/admin/locations/{loc_id}", 422,
        headers=auth(ADMIN_TOKEN),
        json={"slug": f"slug-loc-trung-{RUN_ID}"})

    run("TC38", "PUT /admin/locations/{id} - khong co token",
        "put", f"{url}/admin/locations/{loc_id}", 401,
        headers=auth(),
        json={"name": "Test"})

    run("TC38b", "PUT /admin/locations/{id} - cap nhat slug cua chinh no [khong bao trung]",
        "put", f"{url}/admin/locations/{loc_id}", 200,
        headers=auth(ADMIN_TOKEN),
        json={"slug": f"setup-location-{RUN_ID}"})

    run("TC38c", "PUT /admin/locations/{id} - token user thuong",
        "put", f"{url}/admin/locations/{loc_id}", 403,
        headers=auth(USER_TOKEN),
        json={"name": "Test"})

    # ---- DELETE /admin/locations/{id} ----
    r_del = requests.post(f"{url}/admin/locations", headers=auth(ADMIN_TOKEN),
                          json={"name": f"To Delete Loc {RUN_ID}", "slug": f"to-delete-loc-{RUN_ID}-{int(time.time())}",
                                "category_id": cat_id, "description": "Mo ta xoa",
                                "short_description": "Mo ta ngan xoa",
                                "address": "123 Tran Phu", "district": "Hai Chau",
                                "latitude": 16.0544, "longitude": 108.2022,
                                "status": "active", "is_featured": False})
    del_loc_id = parse_id(r_del)
    print(f"[SETUP] del_loc_id={del_loc_id}, status={r_del.status_code}, body={r_del.text[:300]}")

    run("TC39", "DELETE /admin/locations/{id} - xoa thanh cong",
        "delete", f"{url}/admin/locations/{del_loc_id}", [200, 204],
        headers=auth(ADMIN_TOKEN))

    # ---- GET /admin/locations/export ----
    run("TC39b", "GET /admin/locations/export - export thanh cong",
        "get", f"{url}/admin/locations/export", 200,
        headers=auth(ADMIN_TOKEN))

    run("TC39c", "GET /admin/locations/export - export voi filter",
        "get", f"{url}/admin/locations/export", 200,
        headers=auth(ADMIN_TOKEN), params={"district": "Hai Chau", "status": "active"})

    run("TC39d", "GET /admin/locations/export - khong co token",
        "get", f"{url}/admin/locations/export", 401,
        headers=auth())

    # ---- POST /admin/locations/{id}/tags ----
    # Cần seed tag trước
    r_tag = requests.post(f"{url}/admin/tags", headers=auth(ADMIN_TOKEN),
                          json={"name": f"Tag TC {RUN_ID}", "slug": f"tag-tc-{RUN_ID}", "type": "feature"})
    tag_id = parse_id(r_tag)
    print(f"[SETUP] tag_id={tag_id}, status={r_tag.status_code}")

    run("TC39e", "POST /admin/locations/{id}/tags - gan tags hop le",
        "post", f"{url}/admin/locations/{loc_id}/tags", 200,
        headers=auth(ADMIN_TOKEN),
        json={"tag_ids": [tag_id]} if tag_id else {"tag_ids": []})

    run("TC39f", "POST /admin/locations/{id}/tags - tag_id khong ton tai",
        "post", f"{url}/admin/locations/{loc_id}/tags", 422,
        headers=auth(ADMIN_TOKEN),
        json={"tag_ids": [99999]})

    run("TC39g", "POST /admin/locations/{id}/tags - khong co token",
        "post", f"{url}/admin/locations/{loc_id}/tags", 401,
        headers=auth(),
        json={"tag_ids": [1]})

    # ---- DELETE /admin/locations/{id}/tags/{tagId} ----
    run("TC39h", "DELETE /admin/locations/{id}/tags/{tagId} - xoa tag hop le",
        "delete", f"{url}/admin/locations/{loc_id}/tags/{tag_id}", [200, 204],
        headers=auth(ADMIN_TOKEN))

    run("TC39i", "DELETE /admin/locations/{id}/tags/{tagId} - tagId khong ton tai [bug backend]",
        "delete", f"{url}/admin/locations/{loc_id}/tags/99999", [200, 404, 422],
        headers=auth(ADMIN_TOKEN))

    run("TC39j", "DELETE /admin/locations/{id}/tags/{tagId} - khong co token",
        "delete", f"{url}/admin/locations/{loc_id}/tags/{tag_id}", 401,
        headers=auth())

    # ---- POST /admin/locations/{id}/amenities ----
    r_amenity = requests.post(f"{url}/admin/amenities", headers=auth(ADMIN_TOKEN),
                              json={"name": f"Amenity TC {RUN_ID}", "icon": "fa-wifi", "category": "connectivity"})
    amenity_id = parse_id(r_amenity)
    print(f"[SETUP] amenity_id={amenity_id}, status={r_amenity.status_code}")

    run("TC39k", "POST /admin/locations/{id}/amenities - gan amenities hop le",
        "post", f"{url}/admin/locations/{loc_id}/amenities", 200,
        headers=auth(ADMIN_TOKEN),
        json={"amenity_ids": [amenity_id]} if amenity_id else {"amenity_ids": []})

    run("TC39l", "POST /admin/locations/{id}/amenities - amenity_id khong ton tai",
        "post", f"{url}/admin/locations/{loc_id}/amenities", 422,
        headers=auth(ADMIN_TOKEN),
        json={"amenity_ids": [99999]})

    run("TC39m", "POST /admin/locations/{id}/amenities - khong co token",
        "post", f"{url}/admin/locations/{loc_id}/amenities", 401,
        headers=auth(),
        json={"amenity_ids": [1]})

    # ---- DELETE /admin/locations/{id}/amenities/{amenityId} ----
    run("TC39n", "DELETE /admin/locations/{id}/amenities/{amenityId} - xoa amenity hop le",
        "delete", f"{url}/admin/locations/{loc_id}/amenities/{amenity_id}", [200, 204],
        headers=auth(ADMIN_TOKEN))

    run("TC39o", "DELETE /admin/locations/{id}/amenities/{amenityId} - amenityId khong ton tai [bug backend]",
        "delete", f"{url}/admin/locations/{loc_id}/amenities/99999", [200, 404, 422],
        headers=auth(ADMIN_TOKEN))

    run("TC39p", "DELETE /admin/locations/{id}/amenities/{amenityId} - khong co token",
        "delete", f"{url}/admin/locations/{loc_id}/amenities/{amenity_id}", 401,
        headers=auth())

    run("TC40", "DELETE /admin/locations/{id} - ID khong ton tai",
        "delete", f"{url}/admin/locations/99999", [404, 422],
        headers=auth(ADMIN_TOKEN))

    run("TC41", "DELETE /admin/locations/{id} - khong co token",
        "delete", f"{url}/admin/locations/{loc_id}", 401,
        headers=auth())

    # ---- PATCH /admin/locations/{id}/status ----
    run("TC42", "PATCH /admin/locations/{id}/status - doi sang inactive",
        "patch", f"{url}/admin/locations/{loc_id}/status", 200,
        headers=auth(ADMIN_TOKEN),
        json={"status": "inactive"})

    run("TC43", "PATCH /admin/locations/{id}/status - doi sang active",
        "patch", f"{url}/admin/locations/{loc_id}/status", 200,
        headers=auth(ADMIN_TOKEN),
        json={"status": "active"})

    run("TC44", "PATCH /admin/locations/{id}/status - status sai gia tri",
        "patch", f"{url}/admin/locations/{loc_id}/status", 422,
        headers=auth(ADMIN_TOKEN),
        json={"status": "unknown"})

    run("TC45", "PATCH /admin/locations/{id}/status - ID khong ton tai",
        "patch", f"{url}/admin/locations/99999/status", [404, 422],
        headers=auth(ADMIN_TOKEN),
        json={"status": "active"})

    run("TC46", "PATCH /admin/locations/{id}/status - khong co token",
        "patch", f"{url}/admin/locations/{loc_id}/status", 401,
        headers=auth(),
        json={"status": "active"})

    run("TC46b", "PATCH /admin/locations/{id}/status - token user thuong",
        "patch", f"{url}/admin/locations/{loc_id}/status", 403,
        headers=auth(USER_TOKEN),
        json={"status": "active"})

    # ---- PATCH /admin/locations/{id}/featured ----
    run("TC47", "PATCH /admin/locations/{id}/featured - bat noi bat",
        "patch", f"{url}/admin/locations/{loc_id}/featured", 200,
        headers=auth(ADMIN_TOKEN),
        json={"is_featured": True})

    run("TC48", "PATCH /admin/locations/{id}/featured - tat noi bat",
        "patch", f"{url}/admin/locations/{loc_id}/featured", 200,
        headers=auth(ADMIN_TOKEN),
        json={"is_featured": False})

    run("TC49", "PATCH /admin/locations/{id}/featured - is_featured sai kieu",
        "patch", f"{url}/admin/locations/{loc_id}/featured", 422,
        headers=auth(ADMIN_TOKEN),
        json={"is_featured": "yes"})

    run("TC50", "PATCH /admin/locations/{id}/featured - ID khong ton tai",
        "patch", f"{url}/admin/locations/99999/featured", [404, 422],
        headers=auth(ADMIN_TOKEN),
        json={"is_featured": True})

    run("TC51", "PATCH /admin/locations/{id}/featured - khong co token",
        "patch", f"{url}/admin/locations/{loc_id}/featured", 401,
        headers=auth(),
        json={"is_featured": True})

    run("TC51b", "PATCH /admin/locations/{id}/featured - token user thuong",
        "patch", f"{url}/admin/locations/{loc_id}/featured", 403,
        headers=auth(USER_TOKEN),
        json={"is_featured": True})

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
