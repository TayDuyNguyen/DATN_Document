"""
crawl_places.py
===============
Crawl dữ liệu địa điểm Đà Nẵng từ Google Places API
và export ra file seed.sql để import vào MySQL.

Cài đặt:
    pip install requests python-slugify

Chạy thật (cần API key):
    python crawl_places.py --key YOUR_API_KEY

Chạy thử không cần API key (mock data):
    python crawl_places.py --mock
    python crawl_places.py --mock --out my_seed.sql
"""

import argparse
import json
import re
import time
import unicodedata
from datetime import datetime

import requests

# ── Cấu hình ──────────────────────────────────────────────────────────────────

BASE_URL = "https://maps.googleapis.com/maps/api"

# Map Google place type → (category_id, subcategory_id)
# Phải khớp với dữ liệu seed trong bảng categories / subcategories
CATEGORY_MAP = {
    # Ăn uống (category_id = 1)
    "restaurant":   (1, 1),   # Nhà hàng
    "cafe":         (1, 2),   # Quán cà phê
    "bar":          (1, 3),   # Bar / Pub
    "bakery":       (1, 4),   # Tiệm bánh
    "food":         (1, 1),   # Mặc định → Nhà hàng
    # Khách sạn (category_id = 2)
    "lodging":      (2, 5),   # Khách sạn
    "hotel":        (2, 5),   # Khách sạn
    "resort":       (2, 6),   # Resort
    "hostel":       (2, 7),   # Hostel / Homestay
    # Du lịch (category_id = 3)
    "tourist_attraction": (3, 8),  # Điểm tham quan
    "museum":             (3, 9),  # Bảo tàng
    "park":               (3, 10), # Công viên / Bãi biển
    "amusement_park":     (3, 11), # Vui chơi giải trí
    "natural_feature":    (3, 10), # Thiên nhiên
    "beach":              (3, 10), # Bãi biển
}

# Quận Đà Nẵng → chuẩn hóa
DISTRICT_MAP = {
    "hải châu":      "Hải Châu",
    "hai chau":      "Hải Châu",
    "sơn trà":       "Sơn Trà",
    "son tra":       "Sơn Trà",
    "ngũ hành sơn":  "Ngũ Hành Sơn",
    "ngu hanh son":  "Ngũ Hành Sơn",
    "cẩm lệ":        "Cẩm Lệ",
    "cam le":        "Cẩm Lệ",
    "thanh khê":     "Thanh Khê",
    "thanh khe":     "Thanh Khê",
    "liên chiểu":    "Liên Chiểu",
    "lien chieu":    "Liên Chiểu",
}

VALID_DISTRICTS = set(DISTRICT_MAP.values())

# Từ khóa tìm kiếm theo từng nhóm
SEARCH_QUERIES = [
    # Ăn uống
    "nhà hàng hải sản Đà Nẵng",
    "quán ăn ngon Đà Nẵng",
    "quán cà phê view đẹp Đà Nẵng",
    "nhà hàng buffet Đà Nẵng",
    "quán nhậu Đà Nẵng",
    # Khách sạn
    "khách sạn 4 sao Đà Nẵng",
    "resort biển Đà Nẵng",
    "homestay Đà Nẵng",
    "hostel Đà Nẵng",
    # Du lịch
    "điểm tham quan Đà Nẵng",
    "bãi biển Đà Nẵng",
    "vui chơi giải trí Đà Nẵng",
    "bảo tàng Đà Nẵng",
]


# ── Helpers ───────────────────────────────────────────────────────────────────

def slugify(text: str) -> str:
    """Chuyển tiếng Việt → slug ASCII."""
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    text = re.sub(r"[\s_-]+", "-", text)
    return text


def escape_sql(value: str) -> str:
    """Escape chuỗi để dùng trong SQL INSERT."""
    if value is None:
        return "NULL"
    value = str(value).replace("\\", "\\\\").replace("'", "\\'")
    return f"'{value}'"


def extract_district(address_components: list) -> str:
    """Trích quận từ address_components của Google."""
    for comp in address_components:
        name_lower = comp.get("long_name", "").lower()
        for key, district in DISTRICT_MAP.items():
            if key in name_lower:
                return district
    return "Hải Châu"  # fallback


def map_category(place_types: list) -> tuple:
    """Map Google place types → (category_id, subcategory_id)."""
    for t in place_types:
        if t in CATEGORY_MAP:
            return CATEGORY_MAP[t]
    return (1, 1)  # fallback: Ăn uống / Nhà hàng


def format_opening_hours(periods: list) -> str | None:
    """Chuyển Google opening_hours.periods → JSON string."""
    if not periods:
        return None
    days = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]
    result = {}
    for period in periods:
        open_info  = period.get("open", {})
        close_info = period.get("close", {})
        day_idx    = open_info.get("day", 0)
        day_key    = days[day_idx]
        open_time  = open_info.get("time", "0000")
        close_time = close_info.get("time", "2359")
        result[day_key] = f"{open_time[:2]}:{open_time[2:]}-{close_time[:2]}:{close_time[2:]}"
    return json.dumps(result, ensure_ascii=False)


# ── Google Places API calls ───────────────────────────────────────────────────

def text_search(query: str, api_key: str, page_token: str = None) -> dict:
    """Gọi Places Text Search API."""
    params = {
        "query":    query,
        "key":      api_key,
        "language": "vi",
        "region":   "vn",
    }
    if page_token:
        params["pagetoken"] = page_token
    resp = requests.get(f"{BASE_URL}/place/textsearch/json", params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()


def place_detail(place_id: str, api_key: str) -> dict:
    """Gọi Places Detail API để lấy thông tin đầy đủ."""
    params = {
        "place_id": place_id,
        "key":      api_key,
        "language": "vi",
        "fields":   ",".join([
            "place_id", "name", "formatted_address", "address_components",
            "geometry", "formatted_phone_number", "website",
            "opening_hours", "price_level", "rating", "types",
            "photos", "business_status", "editorial_summary",
        ]),
    }
    resp = requests.get(f"{BASE_URL}/place/details/json", params=params, timeout=10)
    resp.raise_for_status()
    return resp.json().get("result", {})


def get_photo_url(photo_reference: str, api_key: str, max_width: int = 800) -> str:
    """Tạo URL ảnh từ photo_reference."""
    return (
        f"{BASE_URL}/place/photo"
        f"?maxwidth={max_width}"
        f"&photo_reference={photo_reference}"
        f"&key={api_key}"
    )


# ── Crawl logic ───────────────────────────────────────────────────────────────

def crawl_all(api_key: str, max_per_query: int = 20) -> list[dict]:
    """Crawl tất cả queries, trả về list địa điểm đã xử lý."""
    seen_ids  = set()
    locations = []

    for query in SEARCH_QUERIES:
        print(f"\n🔍 Đang crawl: {query}")
        page_token = None
        count      = 0

        while count < max_per_query:
            data = text_search(query, api_key, page_token)

            if data.get("status") not in ("OK", "ZERO_RESULTS"):
                print(f"  ⚠️  API error: {data.get('status')} - {data.get('error_message','')}")
                break

            for result in data.get("results", []):
                place_id = result["place_id"]
                if place_id in seen_ids:
                    continue
                seen_ids.add(place_id)

                # Lấy chi tiết
                time.sleep(0.2)  # tránh rate limit
                detail = place_detail(place_id, api_key)
                if not detail:
                    continue

                # Bỏ qua nếu không ở Đà Nẵng
                address = detail.get("formatted_address", "")
                if "đà nẵng" not in address.lower() and "da nang" not in address.lower():
                    continue

                loc = process_place(detail, api_key)
                if loc:
                    locations.append(loc)
                    count += 1
                    print(f"  ✅ [{count}] {loc['name']}")

            page_token = data.get("next_page_token")
            if not page_token:
                break
            time.sleep(2)  # Google yêu cầu delay trước khi dùng next_page_token

    print(f"\n📦 Tổng cộng: {len(locations)} địa điểm")
    return locations


def process_place(detail: dict, api_key: str) -> dict | None:
    """Xử lý raw detail → dict khớp với schema locations."""
    name = detail.get("name", "").strip()
    if not name:
        return None

    address_components = detail.get("address_components", [])
    geometry           = detail.get("geometry", {}).get("location", {})
    photos             = detail.get("photos", [])
    place_types        = detail.get("types", [])
    opening            = detail.get("opening_hours", {})
    summary            = detail.get("editorial_summary", {}).get("overview", "")

    category_id, subcategory_id = map_category(place_types)
    district = extract_district(address_components)

    # Ảnh
    thumbnail = None
    extra_images = []
    for i, photo in enumerate(photos[:6]):
        ref = photo.get("photo_reference")
        if not ref:
            continue
        url = get_photo_url(ref, api_key)
        if i == 0:
            thumbnail = url
        else:
            extra_images.append(url)

    return {
        "name":             name,
        "slug":             slugify(name),
        "category_id":      category_id,
        "subcategory_id":   subcategory_id,
        "description":      summary or None,
        "short_description": summary[:200] if summary else None,
        "address":          detail.get("formatted_address", ""),
        "district":         district,
        "latitude":         geometry.get("lat"),
        "longitude":        geometry.get("lng"),
        "phone":            detail.get("formatted_phone_number"),
        "website":          detail.get("website"),
        "opening_hours":    format_opening_hours(opening.get("periods", [])),
        "price_level":      detail.get("price_level"),
        "avg_rating":       detail.get("rating", 0),
        "thumbnail":        thumbnail,
        "images":           json.dumps(extra_images) if extra_images else None,
        "status":           "active",
        "is_featured":      0,
    }


# ── Export SQL ────────────────────────────────────────────────────────────────

def export_sql(locations: list[dict], output_file: str = "seed_locations.sql"):
    """Xuất danh sách địa điểm ra file SQL INSERT."""
    slug_count: dict[str, int] = {}

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"-- Seed data: locations\n")
        f.write(f"-- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"-- Total: {len(locations)} records\n\n")
        f.write("SET NAMES utf8mb4;\n")
        f.write("SET FOREIGN_KEY_CHECKS = 0;\n\n")
        f.write("INSERT INTO locations (\n")
        f.write("  name, slug, category_id, subcategory_id,\n")
        f.write("  description, short_description,\n")
        f.write("  address, district,\n")
        f.write("  latitude, longitude,\n")
        f.write("  phone, website, opening_hours,\n")
        f.write("  price_level, avg_rating,\n")
        f.write("  thumbnail, images,\n")
        f.write("  status, is_featured, created_by\n")
        f.write(") VALUES\n")

        rows = []
        for loc in locations:
            # Đảm bảo slug duy nhất
            base_slug = loc["slug"] or slugify(loc["name"])
            slug      = base_slug
            if slug in slug_count:
                slug_count[base_slug] += 1
                slug = f"{base_slug}-{slug_count[base_slug]}"
            else:
                slug_count[base_slug] = 0

            lat = f"{loc['latitude']}" if loc["latitude"] else "NULL"
            lng = f"{loc['longitude']}" if loc["longitude"] else "NULL"
            price = str(loc["price_level"]) if loc["price_level"] else "NULL"
            rating = f"{loc['avg_rating']:.2f}" if loc["avg_rating"] else "0.00"

            row = (
                f"  ({escape_sql(loc['name'])}, {escape_sql(slug)}, "
                f"{loc['category_id']}, "
                f"{loc['subcategory_id'] if loc['subcategory_id'] else 'NULL'}, "
                f"{escape_sql(loc['description'])}, "
                f"{escape_sql(loc['short_description'])}, "
                f"{escape_sql(loc['address'])}, "
                f"{escape_sql(loc['district'])}, "
                f"{lat}, {lng}, "
                f"{escape_sql(loc['phone'])}, "
                f"{escape_sql(loc['website'])}, "
                f"{escape_sql(loc['opening_hours'])}, "
                f"{price}, {rating}, "
                f"{escape_sql(loc['thumbnail'])}, "
                f"{escape_sql(loc['images'])}, "
                f"'active', {loc['is_featured']}, 1)"
            )
            rows.append(row)

        f.write(",\n".join(rows))
        f.write(";\n\n")
        f.write("SET FOREIGN_KEY_CHECKS = 1;\n")

    print(f"\n✅ Đã xuất {len(locations)} địa điểm → {output_file}")


# ── Mock data (dùng khi không có API key) ────────────────────────────────────

MOCK_LOCATIONS = [
    {
        "name": "Nhà hàng Bé Mặn",
        "slug": "nha-hang-be-man",
        "category_id": 1, "subcategory_id": 1,
        "description": "Nhà hàng hải sản nổi tiếng tại Đà Nẵng với các món đặc sản biển tươi sống.",
        "short_description": "Hải sản tươi sống, view biển đẹp.",
        "address": "Lô 4 Trần Bạch Đằng, Mỹ An, Ngũ Hành Sơn, Đà Nẵng",
        "district": "Ngũ Hành Sơn",
        "latitude": 16.0471, "longitude": 108.2468,
        "phone": "0236 3959 888", "website": None,
        "opening_hours": '{"mon":"10:00-22:00","tue":"10:00-22:00","wed":"10:00-22:00","thu":"10:00-22:00","fri":"10:00-23:00","sat":"10:00-23:00","sun":"10:00-22:00"}',
        "price_level": 2, "avg_rating": 4.3,
        "thumbnail": None, "images": None,
        "status": "active", "is_featured": 1,
    },
    {
        "name": "Cà phê Bạch Đằng",
        "slug": "ca-phe-bach-dang",
        "category_id": 1, "subcategory_id": 2,
        "description": "Quán cà phê view sông Hàn lãng mạn, không gian thoáng đãng.",
        "short_description": "View sông Hàn, cà phê ngon.",
        "address": "Bạch Đằng, Hải Châu, Đà Nẵng",
        "district": "Hải Châu",
        "latitude": 16.0678, "longitude": 108.2208,
        "phone": None, "website": None,
        "opening_hours": '{"mon":"07:00-22:00","tue":"07:00-22:00","wed":"07:00-22:00","thu":"07:00-22:00","fri":"07:00-23:00","sat":"07:00-23:00","sun":"07:00-22:00"}',
        "price_level": 1, "avg_rating": 4.1,
        "thumbnail": None, "images": None,
        "status": "active", "is_featured": 0,
    },
    {
        "name": "Khách sạn Mường Thanh Luxury",
        "slug": "khach-san-muong-thanh-luxury",
        "category_id": 2, "subcategory_id": 5,
        "description": "Khách sạn 5 sao sang trọng tại trung tâm Đà Nẵng, view biển Mỹ Khê.",
        "short_description": "5 sao, view biển Mỹ Khê.",
        "address": "270 Võ Nguyên Giáp, Phước Mỹ, Sơn Trà, Đà Nẵng",
        "district": "Sơn Trà",
        "latitude": 16.0544, "longitude": 108.2472,
        "phone": "0236 3888 999", "website": "https://muongthanh.com",
        "opening_hours": None,
        "price_level": 4, "avg_rating": 4.6,
        "thumbnail": None, "images": None,
        "status": "active", "is_featured": 1,
    },
    {
        "name": "Bãi biển Mỹ Khê",
        "slug": "bai-bien-my-khe",
        "category_id": 3, "subcategory_id": 10,
        "description": "Một trong những bãi biển đẹp nhất hành tinh theo bình chọn của Forbes.",
        "short_description": "Bãi biển đẹp nhất Đà Nẵng.",
        "address": "Phước Mỹ, Sơn Trà, Đà Nẵng",
        "district": "Sơn Trà",
        "latitude": 16.0600, "longitude": 108.2470,
        "phone": None, "website": None,
        "opening_hours": None,
        "price_level": None, "avg_rating": 4.7,
        "thumbnail": None, "images": None,
        "status": "active", "is_featured": 1,
    },
    {
        "name": "Bảo tàng Điêu khắc Chăm",
        "slug": "bao-tang-dieu-khac-cham",
        "category_id": 3, "subcategory_id": 9,
        "description": "Bảo tàng lưu giữ bộ sưu tập điêu khắc Chăm Pa lớn nhất thế giới.",
        "short_description": "Bộ sưu tập Chăm Pa lớn nhất thế giới.",
        "address": "02 Tháng 2, Bình Hiên, Hải Châu, Đà Nẵng",
        "district": "Hải Châu",
        "latitude": 16.0680, "longitude": 108.2230,
        "phone": "0236 3572 935", "website": None,
        "opening_hours": '{"mon":"07:00-17:00","tue":"07:00-17:00","wed":"07:00-17:00","thu":"07:00-17:00","fri":"07:00-17:00","sat":"07:00-17:00","sun":"07:00-17:00"}',
        "price_level": 1, "avg_rating": 4.4,
        "thumbnail": None, "images": None,
        "status": "active", "is_featured": 1,
    },
    {
        "name": "Núi Ngũ Hành Sơn",
        "slug": "nui-ngu-hanh-son",
        "category_id": 3, "subcategory_id": 8,
        "description": "Quần thể 5 ngọn núi đá cẩm thạch với hang động, chùa chiền và tượng Phật.",
        "short_description": "5 ngọn núi đá cẩm thạch huyền bí.",
        "address": "Hòa Hải, Ngũ Hành Sơn, Đà Nẵng",
        "district": "Ngũ Hành Sơn",
        "latitude": 16.0020, "longitude": 108.2640,
        "phone": "0236 3961 114", "website": None,
        "opening_hours": '{"mon":"07:00-17:30","tue":"07:00-17:30","wed":"07:00-17:30","thu":"07:00-17:30","fri":"07:00-17:30","sat":"07:00-17:30","sun":"07:00-17:30"}',
        "price_level": 1, "avg_rating": 4.5,
        "thumbnail": None, "images": None,
        "status": "active", "is_featured": 1,
    },
    {
        "name": "Cầu Rồng Đà Nẵng",
        "slug": "cau-rong-da-nang",
        "category_id": 3, "subcategory_id": 8,
        "description": "Cây cầu hình rồng biểu tượng của Đà Nẵng, phun lửa và nước vào cuối tuần.",
        "short_description": "Biểu tượng Đà Nẵng, phun lửa cuối tuần.",
        "address": "Trần Hưng Đạo, Hải Châu, Đà Nẵng",
        "district": "Hải Châu",
        "latitude": 16.0610, "longitude": 108.2270,
        "phone": None, "website": None,
        "opening_hours": None,
        "price_level": None, "avg_rating": 4.6,
        "thumbnail": None, "images": None,
        "status": "active", "is_featured": 1,
    },
    {
        "name": "Hostel Danang Backpacker",
        "slug": "hostel-danang-backpacker",
        "category_id": 2, "subcategory_id": 7,
        "description": "Hostel giá rẻ, sạch sẽ, gần biển Mỹ Khê, phù hợp khách du lịch bụi.",
        "short_description": "Hostel giá rẻ, gần biển.",
        "address": "12 An Thượng 4, Mỹ An, Ngũ Hành Sơn, Đà Nẵng",
        "district": "Ngũ Hành Sơn",
        "latitude": 16.0490, "longitude": 108.2460,
        "phone": "0905 123 456", "website": None,
        "opening_hours": None,
        "price_level": 1, "avg_rating": 4.0,
        "thumbnail": None, "images": None,
        "status": "active", "is_featured": 0,
    },
    {
        "name": "Quán Mì Quảng Bà Mua",
        "slug": "quan-mi-quang-ba-mua",
        "category_id": 1, "subcategory_id": 1,
        "description": "Quán mì Quảng truyền thống nổi tiếng nhất Đà Nẵng, đông khách từ sáng sớm.",
        "short_description": "Mì Quảng truyền thống, đông khách.",
        "address": "19-21 Trần Bình Trọng, Hải Châu, Đà Nẵng",
        "district": "Hải Châu",
        "latitude": 16.0720, "longitude": 108.2190,
        "phone": None, "website": None,
        "opening_hours": '{"mon":"06:00-11:00","tue":"06:00-11:00","wed":"06:00-11:00","thu":"06:00-11:00","fri":"06:00-11:00","sat":"06:00-11:00","sun":"06:00-11:00"}',
        "price_level": 1, "avg_rating": 4.5,
        "thumbnail": None, "images": None,
        "status": "active", "is_featured": 0,
    },
    {
        "name": "Sky36 Bar & Lounge",
        "slug": "sky36-bar-lounge",
        "category_id": 1, "subcategory_id": 3,
        "description": "Bar trên tầng thượng cao nhất Đà Nẵng, view toàn thành phố và biển.",
        "short_description": "Bar cao nhất Đà Nẵng, view 360°.",
        "address": "Tầng 36, Novotel Đà Nẵng, 36 Bạch Đằng, Hải Châu, Đà Nẵng",
        "district": "Hải Châu",
        "latitude": 16.0690, "longitude": 108.2220,
        "phone": "0236 3929 999", "website": "https://sky36.vn",
        "opening_hours": '{"mon":"17:00-02:00","tue":"17:00-02:00","wed":"17:00-02:00","thu":"17:00-02:00","fri":"17:00-03:00","sat":"17:00-03:00","sun":"17:00-02:00"}',
        "price_level": 3, "avg_rating": 4.4,
        "thumbnail": None, "images": None,
        "status": "active", "is_featured": 1,
    },
]


def crawl_mock() -> list[dict]:
    """Trả về mock data để test không cần API key."""
    print("🧪 Chạy ở chế độ MOCK — không cần Google API key")
    print(f"📦 Tổng cộng: {len(MOCK_LOCATIONS)} địa điểm mẫu\n")
    for i, loc in enumerate(MOCK_LOCATIONS, 1):
        print(f"  ✅ [{i}] {loc['name']} ({loc['district']})")
    return MOCK_LOCATIONS




def main():
    parser = argparse.ArgumentParser(description="Crawl Google Places → seed.sql")
    parser.add_argument("--key",   required=True, help="Google Places API Key")
    parser.add_argument("--max",   type=int, default=20, help="Số địa điểm tối đa mỗi query (default: 20)")
    parser.add_argument("--out",   default="seed_locations.sql", help="Tên file output (default: seed_locations.sql)")
    args = parser.parse_args()

    locations = crawl_all(api_key=args.key, max_per_query=args.max)

    if not locations:
        print("❌ Không crawl được dữ liệu nào.")
        return

    export_sql(locations, output_file=args.out)
    print(f"\n📌 Chạy lệnh sau để import vào MySQL:")
    print(f"   mysql -u root -p danang_trip < {args.out}")


if __name__ == "__main__":
    main()
