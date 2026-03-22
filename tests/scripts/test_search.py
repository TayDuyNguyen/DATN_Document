"""
Test script - SEARCH
Run: python tests/scripts/test_search.py
Yeu cau: pip install requests
"""

import requests
import time

BASE_URL = "http://localhost:8000/api/v1"
RUN_ID   = str(int(time.time()))

PASS    = "\033[92mPASS\033[0m"
FAIL    = "\033[91mFAIL\033[0m"
results = []


def auth(token=None):
    h = {"Accept": "application/json"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def run(tc, desc, method, url, expected, **kwargs):
    try:
        res   = getattr(requests, method)(url, **kwargs)
        ok    = res.status_code in expected if isinstance(expected, list) else res.status_code == expected
        label = PASS if ok else FAIL
        print(f"[{label}] {tc} - {desc} | got {res.status_code}, expected {expected}")
        results.append((tc, desc, ok, res.status_code))
        return res
    except Exception as e:
        print(f"[ERROR] {tc} - {desc} | {e}")
        results.append((tc, desc, False, "error"))
        return None


def extract_list(res):
    """Trích data list từ response, hỗ trợ nhiều cấu trúc JSON khác nhau."""
    if res is None:
        return []
    try:
        body = res.json()
    except Exception:
        return []
    data = body.get("data", [])
    # Nếu data là dict (vd: {"items": [...], "total": 10})
    if isinstance(data, dict):
        for key in ("items", "data", "results", "locations"):
            if isinstance(data.get(key), list):
                return data[key]
        return []
    if isinstance(data, list):
        return data
    return []


def extract_meta(res):
    """Trích meta từ response."""
    if res is None:
        return {}
    try:
        body = res.json()
        meta = body.get("meta", {})
        # Một số backend trả meta lồng trong data
        if not meta and isinstance(body.get("data"), dict):
            meta = body["data"].get("meta", {})
        return meta if isinstance(meta, dict) else {}
    except Exception:
        return {}


def check_sorted(data, key, reverse=True):
    """Kiểm tra list có được sắp xếp theo key không."""
    if not isinstance(data, list):
        return True  # không thể kiểm tra, bỏ qua
    values = [item[key] for item in data if isinstance(item, dict) and item.get(key) is not None]
    if len(values) < 2:
        return True
    return all(values[i] >= values[i+1] for i in range(len(values)-1)) if reverse \
        else all(values[i] <= values[i+1] for i in range(len(values)-1))


def run_tests():
    url = BASE_URL

    print("\n" + "="*55)
    print("  SEARCH — TEST SUITE")
    print("="*55 + "\n")

    # ── GET /search ──────────────────────────────────────────

    res = run("TC01", "GET /search - tu khoa hop le, co ket qua",
              "get", f"{url}/search", 200,
              headers=auth(), params={"q": "hải sản"})
    if res and res.status_code == 200:
        data = extract_list(res)
        meta = extract_meta(res)
        if not isinstance(data, list):
            print("  [WARN] TC01: data khong phai array")
        if meta.get("total", 0) == 0:
            print("  [WARN] TC01: total = 0, kiem tra seed data")

    res = run("TC02", "GET /search - tu khoa khong co ket qua",
              "get", f"{url}/search", 200,
              headers=auth(), params={"q": "xyzkhongcokq123"})
    if res and res.status_code == 200:
        meta = extract_meta(res)
        if meta.get("total", -1) != 0:
            print("  [WARN] TC02: total nen = 0")

    run("TC03", "GET /search - filter category_id=1",
        "get", f"{url}/search", 200,
        headers=auth(), params={"q": "quán", "category_id": 1})

    run("TC04", "GET /search - filter district",
        "get", f"{url}/search", 200,
        headers=auth(), params={"q": "cà phê", "district": "Hải Châu"})

    run("TC05", "GET /search - filter price_level=2",
        "get", f"{url}/search", 200,
        headers=auth(), params={"q": "nhà hàng", "price_level": 2})

    run("TC06", "GET /search - filter price_min & price_max",
        "get", f"{url}/search", 200,
        headers=auth(), params={"q": "buffet", "price_min": 100000, "price_max": 500000})

    run("TC07", "GET /search - filter rating_min=4.0",
        "get", f"{url}/search", 200,
        headers=auth(), params={"q": "resort", "rating_min": 4.0})

    res = run("TC08", "GET /search - sort avg_rating desc",
              "get", f"{url}/search", 200,
              headers=auth(), params={"q": "khách sạn", "sort": "avg_rating", "order": "desc"})
    if res and res.status_code == 200:
        data = extract_list(res)
        if not check_sorted(data, "avg_rating", reverse=True):
            print("  [WARN] TC08: ket qua chua duoc sap xep dung")

    res = run("TC09", "GET /search - sort view_count asc",
              "get", f"{url}/search", 200,
              headers=auth(), params={"q": "biển", "sort": "view_count", "order": "asc"})
    if res and res.status_code == 200:
        data = extract_list(res)
        if not check_sorted(data, "view_count", reverse=False):
            print("  [WARN] TC09: ket qua chua duoc sap xep dung")

    res = run("TC10", "GET /search - phan trang page=2 per_page=5",
              "get", f"{url}/search", 200,
              headers=auth(), params={"q": "ăn", "page": 2, "per_page": 5})
    if res and res.status_code == 200:
        meta = extract_meta(res)
        data = extract_list(res)
        if meta.get("current_page") != 2:
            print(f"  [WARN] TC10: current_page nen = 2, got {meta.get('current_page')}")
        if len(data) > 5:
            print(f"  [WARN] TC10: data co {len(data)} phan tu, nen <= 5")

    run("TC11", "GET /search - truyen session_id",
        "get", f"{url}/search", 200,
        headers=auth(), params={"q": "hải sản", "session_id": f"sess_{RUN_ID}"})

    run("TC12", "GET /search - ket hop nhieu filter",
        "get", f"{url}/search", 200,
        headers=auth(), params={
            "q": "nhà hàng", "category_id": 1, "district": "Sơn Trà",
            "price_level": 2, "sort": "avg_rating", "order": "desc",
            "page": 1, "per_page": 10
        })

    run("TC13", "GET /search - thieu q",
        "get", f"{url}/search", 422,
        headers=auth())

    run("TC14", "GET /search - q qua ngan (1 ky tu)",
        "get", f"{url}/search", 422,
        headers=auth(), params={"q": "a"})

    run("TC15", "GET /search - price_level sai gia tri",
        "get", f"{url}/search", 422,
        headers=auth(), params={"q": "nhà hàng", "price_level": 9})

    run("TC16", "GET /search - sort sai gia tri",
        "get", f"{url}/search", 422,
        headers=auth(), params={"q": "nhà hàng", "sort": "invalid_field"})

    run("TC17", "GET /search - order sai gia tri",
        "get", f"{url}/search", 422,
        headers=auth(), params={"q": "nhà hàng", "order": "random"})

    run("TC18", "GET /search - per_page vuot max (100)",
        "get", f"{url}/search", 422,
        headers=auth(), params={"q": "nhà hàng", "per_page": 200})

    run("TC19", "GET /search - rating_min ngoai khoang 0-5",
        "get", f"{url}/search", 422,
        headers=auth(), params={"q": "nhà hàng", "rating_min": 6})

    # ── GET /search/suggestions ──────────────────────────────

    res = run("TC20", "GET /search/suggestions - co goi y",
              "get", f"{url}/search/suggestions", 200,
              headers=auth(), params={"q": "nhà"})
    if res and res.status_code == 200:
        data = extract_list(res)
        if data:
            item = data[0]
            if not isinstance(item, dict):
                print(f"  [WARN] TC20: item khong phai dict, got {type(item)}")
            else:
                for field in ["id", "name", "slug", "district"]:
                    if field not in item:
                        print(f"  [WARN] TC20: thieu field '{field}' trong response")

    run("TC21", "GET /search/suggestions - khong khop dia diem nao",
        "get", f"{url}/search/suggestions", 200,
        headers=auth(), params={"q": "xyzkhongco"})

    res = run("TC22", "GET /search/suggestions - gioi han limit=3",
              "get", f"{url}/search/suggestions", 200,
              headers=auth(), params={"q": "nhà", "limit": 3})
    if res and res.status_code == 200:
        data = extract_list(res)
        if len(data) > 3:
            print(f"  [WARN] TC22: data co {len(data)} phan tu, nen <= 3")

    res = run("TC23", "GET /search/suggestions - default limit (5)",
              "get", f"{url}/search/suggestions", 200,
              headers=auth(), params={"q": "nhà"})
    if res and res.status_code == 200:
        data = extract_list(res)
        if len(data) > 5:
            print(f"  [WARN] TC23: data co {len(data)} phan tu, nen <= 5 (default)")

    # TC24: suggestions không ghi search_logs — chỉ verify response OK
    run("TC24", "GET /search/suggestions - khong ghi search_logs (verify 200)",
        "get", f"{url}/search/suggestions", 200,
        headers=auth(), params={"q": "nhà hàng"})

    run("TC25", "GET /search/suggestions - thieu q",
        "get", f"{url}/search/suggestions", 422,
        headers=auth())

    run("TC26", "GET /search/suggestions - limit vuot max (20)",
        "get", f"{url}/search/suggestions", 422,
        headers=auth(), params={"q": "nhà", "limit": 50})

    run("TC27", "GET /search/suggestions - limit khong phai so",
        "get", f"{url}/search/suggestions", 422,
        headers=auth(), params={"q": "nhà", "limit": "abc"})

    # ── GET /search/popular ──────────────────────────────────

    res = run("TC28", "GET /search/popular - lay danh sach mac dinh",
              "get", f"{url}/search/popular", 200,
              headers=auth())
    if res and res.status_code == 200:
        data = extract_list(res)
        if data:
            item = data[0]
            if not isinstance(item, dict):
                print(f"  [WARN] TC28: item khong phai dict, got {type(item)}")
            else:
                for field in ["query", "count"]:
                    if field not in item:
                        print(f"  [WARN] TC28: thieu field '{field}' trong response")

    res = run("TC29", "GET /search/popular - gioi han limit=5",
              "get", f"{url}/search/popular", 200,
              headers=auth(), params={"limit": 5})
    if res and res.status_code == 200:
        data = extract_list(res)
        if len(data) > 5:
            print(f"  [WARN] TC29: data co {len(data)} phan tu, nen <= 5")

    res = run("TC30", "GET /search/popular - loc theo days=7",
              "get", f"{url}/search/popular", 200,
              headers=auth(), params={"days": 7})
    if res and res.status_code == 200:
        meta = extract_meta(res)
        if meta.get("period_days") != 7:
            print(f"  [WARN] TC30: meta.period_days nen = 7, got {meta.get('period_days')}")

    res = run("TC31", "GET /search/popular - sap xep count giam dan",
              "get", f"{url}/search/popular", 200,
              headers=auth(), params={"limit": 10})
    if res and res.status_code == 200:
        data = extract_list(res)
        if not check_sorted(data, "count", reverse=True):
            print("  [WARN] TC31: ket qua chua duoc sap xep theo count desc")

    run("TC32", "GET /search/popular - DB trong (nen tra array rong)",
        "get", f"{url}/search/popular", 200,
        headers=auth())

    run("TC33", "GET /search/popular - limit vuot max (50)",
        "get", f"{url}/search/popular", 422,
        headers=auth(), params={"limit": 100})

    run("TC34", "GET /search/popular - days am",
        "get", f"{url}/search/popular", 422,
        headers=auth(), params={"days": -1})

    # ── SUMMARY ─────────────────────────────────────────────

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
