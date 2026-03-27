"""
Test script - UPLOAD (Upload anh Cloudinary)
Run: python tests/scripts/test_upload.py
Yeu cau: pip install requests Pillow (Pillow optional, co fallback)
"""

import requests
import io
import os

BASE_URL      = "http://localhost:8000/api/v1"
USER_EMAIL    = "user1@example.com"
USER_PASSWORD = "password"

# Thu muc chua anh that de test
IMAGES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), "images")

# Duong dan cac file anh that
IMG_JPEG1 = os.path.join(IMAGES_DIR, "anh-dep-35.jpg")
IMG_JPEG2 = os.path.join(IMAGES_DIR, "anh-dep-35.jpg")
IMG_JPEG3 = os.path.join(IMAGES_DIR, "anh-dep-35.jpg")
IMG_PNG   = os.path.join(IMAGES_DIR, "images.png")
IMG_WEBP  = os.path.join(IMAGES_DIR, "tai-anh-phong-canh-dep-3.webp")

USER_TOKEN = None
results    = []


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
    # Them timeout mac dinh 15s de tranh treo
    kwargs.setdefault("timeout", 15)
    try:
        res   = getattr(requests, method)(url, **kwargs)
        ok    = res.status_code in expected if isinstance(expected, list) else res.status_code == expected
        label = "\033[92mPASS\033[0m" if ok else "\033[91mFAIL\033[0m"
        print(f"[{label}] {tc} - {desc} | got {res.status_code}, expected {expected}")
        if not ok:
            try:
                body = res.json()
                # Chi in message, khong in full stack trace
                print(f"  [DEBUG] {body.get('message') or body.get('code') or str(body)[:200]}")
            except Exception:
                print(f"  [DEBUG] raw = {res.text[:200]}")
        results.append((tc, desc, ok, res.status_code))
        return res
    except requests.exceptions.Timeout:
        print(f"[TIMEOUT] {tc} - {desc} | request timeout sau 15s")
        results.append((tc, desc, False, "timeout"))
        return None
    except Exception as e:
        print(f"[ERROR] {tc} - {desc} | {type(e).__name__}: {str(e)[:100]}")
        results.append((tc, desc, False, "error"))
        return None


# ── Image factories ───────────────────────────────────────────────────────────


def jpeg():
    """Doc file JPEG that tu disk, fallback ve in-memory neu khong co."""
    if os.path.exists(IMG_JPEG1):
        with open(IMG_JPEG1, "rb") as f:
            return f.read()
    try:
        from PIL import Image
        img = Image.new("RGB", (100, 100), color=(255, 100, 0))
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        return buf.getvalue()
    except ImportError:
        return (b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00"
                b"\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c"
                b"\xff\xc0\x00\x0b\x08\x00\x01\x00\x01\x01\x01\x11\x00"
                b"\xff\xc4\x00\x1f\x00\x00\x01\x05\x01\x01\x01\x01\x01\x01\x00\x00"
                b"\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b"
                b"\xff\xda\x00\x08\x01\x01\x00\x00?\x00\xf5\n\xff\xd9")

def jpeg2():
    return jpeg()

def jpeg3():
    return jpeg()

def png():
    """Doc file PNG that tu disk."""
    with open(IMG_PNG, "rb") as f:
        return f.read()

def webp():
    """Doc file WEBP that tu disk."""
    with open(IMG_WEBP, "rb") as f:
        return f.read()

def large():
    return b"X" * (6 * 1024 * 1024)  # 6MB fake


def extract_public_id(res):
    """Lay public_id tu response upload."""
    try:
        data = res.json().get("data", res.json())
        return (data.get("public_id")
                or data.get("publicId")
                or data.get("public_id"))
    except Exception:
        return None


def extract_url(res):
    """Lay url tu response upload."""
    try:
        data = res.json().get("data", res.json())
        return data.get("url") or data.get("image_url") or data.get("path") or ""
    except Exception:
        return ""


def extract_urls(res):
    """Lay danh sach urls tu response upload multiple."""
    try:
        data = res.json().get("data", res.json())
        # Backend tra ve data.items = [{url, public_id}, ...]
        if isinstance(data, dict):
            items = data.get("items") or data.get("urls") or data.get("images") or []
            if items and isinstance(items[0], dict):
                return [i.get("url") or i.get("secure_url") for i in items]
            return items
        if isinstance(data, list):
            return data
        return []
    except Exception:
        return []


# ── Main ──────────────────────────────────────────────────────────────────────

def run_tests():
    global USER_TOKEN

    USER_TOKEN = login(USER_EMAIL, USER_PASSWORD)
    if not USER_TOKEN:
        print("[ABORT] Khong lay duoc USER_TOKEN.")
        return

    # Kiem tra file anh
    for name, path in [("JPEG1", IMG_JPEG1), ("JPEG2", IMG_JPEG2), ("JPEG3", IMG_JPEG3),
                        ("PNG",   IMG_PNG),   ("WEBP",  IMG_WEBP)]:
        status = "OK" if os.path.exists(path) else "MISSING (se dung fallback)"
        print(f"[FILE] {name}: {os.path.basename(path)} — {status}")

    url_single   = f"{BASE_URL}/upload/image"
    url_multiple = f"{BASE_URL}/upload/images"
    h = auth(USER_TOKEN)

    # ── POST /upload/image ────────────────────────────────────

    res = run("TC01", "POST /upload/image - upload JPEG",
              "post", url_single, [200, 201], headers=h,
              files={"image": ("test.jpg", jpeg(), "image/jpeg")},
              timeout=60)
    if res and res.status_code in (200, 201):
        img_url = extract_url(res)
        pid     = extract_public_id(res)
        print(f"  [INFO] TC01: url={img_url[:70]}")
        print(f"  [INFO] TC01: public_id={pid}")
        if not img_url.startswith("http"):
            print(f"  [WARN] TC01: url khong hop le")

    res = run("TC02", "POST /upload/image - upload PNG",
              "post", url_single, [200, 201], headers=h,
              files={"image": ("test.png", png(), "image/png")})
    if res and res.status_code in (200, 201):
        print(f"  [INFO] TC02: url={extract_url(res)[:70]}")

    run("TC03", "POST /upload/image - upload WEBP",
        "post", url_single, [200, 201], headers=h,
        files={"image": ("test.webp", webp(), "image/webp")})

    res = run("TC04", "POST /upload/image - upload voi folder=locations",
              "post", url_single, [200, 201], headers=h,
              files={"image": ("test.jpg", jpeg(), "image/jpeg")},
              data={"folder": "locations"})
    if res and res.status_code in (200, 201):
        img_url = extract_url(res)
        if "locations" in img_url:
            print(f"  [INFO] TC04: URL chua 'locations' - OK")
        else:
            print(f"  [WARN] TC04: URL khong chua 'locations': {img_url[:80]}")

    run("TC05", "POST /upload/image - khong co folder (optional)",
        "post", url_single, [200, 201], headers=h,
        files={"image": ("test.jpg", jpeg(), "image/jpeg")})

    run("TC06", "POST /upload/image - thieu image",
        "post", url_single, 422, headers=h)

    run("TC07", "POST /upload/image - file PDF",
        "post", url_single, 422, headers=h,
        files={"image": ("test.pdf", b"%PDF-1.4 fake", "application/pdf")})

    run("TC08", "POST /upload/image - file TXT",
        "post", url_single, 422, headers=h,
        files={"image": ("test.txt", b"hello world", "text/plain")})

    run("TC09", "POST /upload/image - file > 5MB",
        "post", url_single, [422, 413], headers=h,
        files={"image": ("large.jpg", large(), "image/jpeg")})

    run("TC10", "POST /upload/image - khong co token",
        "post", url_single, 401, headers=auth(),
        files={"image": ("test.jpg", jpeg(), "image/jpeg")})

    # ── POST /upload/images ───────────────────────────────────

    res = run("TC11", "POST /upload/images - upload 2 anh",
              "post", url_multiple, [200, 201], headers=h,
              files=[("images[]", ("anh1.jpg",  jpeg(), "image/jpeg")),
                     ("images[]", ("anh2.png",  png(),  "image/png"))])
    if res and res.status_code in (200, 201):
        try:
            raw = res.json()
            print(f"  [INFO] TC11: response keys = {list(raw.keys())}")
            data = raw.get("data", raw)
            print(f"  [INFO] TC11: data type = {type(data).__name__}, value = {str(data)[:150]}")
        except Exception:
            pass
        urls = extract_urls(res)
        print(f"  [INFO] TC11: {len(urls)} urls tra ve")
        if len(urls) != 2:
            print(f"  [WARN] TC11: ky vong 2 urls, got {len(urls)}")

    res = run("TC12", "POST /upload/images - upload 1 anh",
              "post", url_multiple, [200, 201], headers=h,
              files=[("images[]", ("a.jpg", jpeg(), "image/jpeg"))])
    if res and res.status_code in (200, 201):
        urls = extract_urls(res)
        print(f"  [INFO] TC12: {len(urls)} urls tra ve")

    # TC13: 10 ảnh (max) — xoay vòng 3 file thật
    imgs = [
        ("image/jpeg", jpeg()),
        ("image/png",  png()),
        ("image/webp", webp()),
    ]
    files_10 = [("images[]", (f"img{i}.{['jpg','png','webp'][i%3]}", imgs[i%3][1], imgs[i%3][0]))
                for i in range(10)]
    res = run("TC13", "POST /upload/images - upload 10 anh (max)",
              "post", url_multiple, [200, 201], headers=h,
              files=files_10, timeout=90)
    if res and res.status_code in (200, 201):
        urls = extract_urls(res)
        if len(urls) == 10:
            print(f"  [INFO] TC13: 10 urls - OK")
        else:
            print(f"  [WARN] TC13: ky vong 10 urls, got {len(urls)}")

    res = run("TC14", "POST /upload/images - upload voi folder=ratings",
              "post", url_multiple, [200, 201], headers=h,
              files=[("images[]", ("anh1.jpg", jpeg(), "image/jpeg")),
                     ("images[]", ("anh2.png", png(),  "image/png"))],
              data={"folder": "ratings"})

    # TC15: 11 ảnh vượt max
    files_11 = [("images[]", (f"img{i}.{['jpg','png','webp'][i%3]}", imgs[i%3][1], imgs[i%3][0]))
                for i in range(11)]
    run("TC15", "POST /upload/images - 11 anh vuot max",
        "post", url_multiple, 422, headers=h,
        files=files_11)

    run("TC16", "POST /upload/images - thieu images[]",
        "post", url_multiple, 422, headers=h)

    run("TC17", "POST /upload/images - co file PDF trong batch",
        "post", url_multiple, 422, headers=h,
        files=[("images[]", ("anh1.jpg", jpeg(), "image/jpeg")),
               ("images[]", ("b.pdf",    b"%PDF-1.4 fake content", "application/pdf"))])

    run("TC18", "POST /upload/images - co file > 5MB trong batch",
        "post", url_multiple, [422, 413], headers=h,
        files=[("images[]", ("anh1.jpg", jpeg(),  "image/jpeg")),
               ("images[]", ("big.jpg",  large(), "image/jpeg"))])

    run("TC19", "POST /upload/images - khong co token",
        "post", url_multiple, 401, headers=auth(),
        files=[("images[]", ("anh1.jpg", jpeg(), "image/jpeg"))])

    # ── DELETE /upload/image ──────────────────────────────────

    # Upload 1 ảnh để lấy public_id cho TC20
    setup_res = requests.post(url_single, headers=h, timeout=30,
                              files={"image": ("del_test.jpg", jpeg(), "image/jpeg")})
    del_public_id = None
    if setup_res.status_code in (200, 201):
        del_public_id = extract_public_id(setup_res)
        print(f"[SETUP] del_public_id = {del_public_id}")
    else:
        print(f"[SETUP] Upload setup that bai: {setup_res.status_code}")

    if del_public_id:
        res = run("TC20", "DELETE /upload/image - xoa thanh cong",
                  "delete", url_single, 200, headers=h,
                  json={"public_id": del_public_id})
        if res and res.status_code == 200:
            print(f"  [INFO] TC20: xoa public_id={del_public_id} - OK")
    else:
        print("[SKIP] TC20 - khong lay duoc public_id de xoa")
        results.append(("TC20", "DELETE /upload/image - xoa thanh cong", None, "skip"))

    run("TC21", "DELETE /upload/image - public_id khong ton tai",
        "delete", url_single, [200, 404, 422], headers=h,
        json={"public_id": "danang_trip/khong_ton_tai_xyz_999"})
    # Note: Cloudinary tra 200 khi xoa ID khong ton tai (behavior cua Cloudinary API)

    run("TC22", "DELETE /upload/image - thieu public_id",
        "delete", url_single, 422, headers=h,
        json={})

    run("TC23", "DELETE /upload/image - public_id rong",
        "delete", url_single, 422, headers=h,
        json={"public_id": ""})

    run("TC24", "DELETE /upload/image - khong co token",
        "delete", url_single, 401, headers=auth(),
        json={"public_id": "danang_trip/test"})

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
