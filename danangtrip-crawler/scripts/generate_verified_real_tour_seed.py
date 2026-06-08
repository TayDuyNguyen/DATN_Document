from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "verified-real-tour-catalog-cloudinary-20260607.json"
OUTPUT = ROOT.parent / "database-seeders" / "49_verified_real_tours_seed.sql"

CATEGORY_RULES = [
    (("golf",), "tour-golf"),
    (("street food", "cooking class", "local cooking"), "tour-am-thuc"),
    (("bicycle",), "tour-dap-xe"),
    (("heritage train",), "tour-train-hue"),
    (("paradise cave",), "tour-hang-dong"),
    (("cham island", "snorkeling"), "tour-bien-dao"),
    (("my son",), "tour-heritage-path"),
    (("hue", "dmz"), "tour-hue"),
    (("ba na", "bana"), "tour-ba-na-hills"),
    (("hoi an",), "tour-hoi-an"),
    (("city tour", "da nang day tour"), "tour-trong-ngay"),
]

LOCATION_RULES = {
    "Da Nang": 19,
    "Ba Na Hills": 23,
    "Hoi An": 1,
    "Hue": 103,
    "Son Tra": 107,
    "Cu Lao Cham": 13,
    "My Son": 8,
    "Marble Mountains": 21,
}


def sql_text(value: str | None) -> str:
    if value is None:
        return "NULL"
    return "'" + value.replace("'", "''") + "'"


def sql_json(value: object) -> str:
    payload = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return f"{sql_text(payload)}::json"


def clean_text(value: str | None, limit: int | None = None) -> str | None:
    if value is None:
        return None
    cleaned = re.sub(r"\s+", " ", value).strip()
    return cleaned[:limit].rstrip() if limit else cleaned


def category_slug(tour: dict) -> str:
    haystack = tour.get("name", "").lower()
    for keywords, slug in CATEGORY_RULES:
        if any(keyword in haystack for keyword in keywords):
            return slug
    return tour.get("tour_category_slug") or "tour-trong-ngay"


def duration_days(value: str | None) -> int:
    if not value:
        return 1
    lowered = value.lower()
    match = re.search(r"(\d+)\s*(?:day|days|ngày)", lowered)
    if match:
        return max(1, int(match.group(1)))
    return 1


def normalized_description(tour: dict) -> str:
    source = tour.get("source", {})
    destinations = ", ".join(tour.get("destination_names", []))
    duration = clean_text(tour.get("duration")) or "theo chương trình"
    return (
        f"Chương trình tham quan {destinations} với thời lượng {duration}. "
        "Thông tin giá, lịch trình, dịch vụ bao gồm và không bao gồm được tổng hợp "
        "từ website công khai của đơn vị tổ chức, sau đó chuẩn hóa để phục vụ bước "
        "kiểm duyệt nội dung trước khi mở bán. "
        f"Nguồn tham khảo: {source.get('url', '')}"
    )


def normalized_short_description(tour: dict) -> str:
    destinations = ", ".join(tour.get("destination_names", []))
    duration = clean_text(tour.get("duration")) or "theo chương trình"
    return clean_text(
        f"Tour {destinations}, thời lượng {duration}, sử dụng giá và lịch trình "
        "được xác minh từ nguồn của đơn vị tổ chức.",
        500,
    ) or ""


def build_seed(catalog: list[dict]) -> str:
    rows = []
    mappings = []
    schedules = []

    for index, tour in enumerate(catalog, start=1):
        slug = clean_text(tour["slug"], 220)
        name = clean_text(tour["name"], 200)
        source_url = tour.get("source", {}).get("url")
        image_urls = tour.get("image_urls") or [
            item["url"] for item in tour.get("cloudinary_media", []) if item.get("url")
        ]
        thumbnail = image_urls[0] if image_urls else tour.get("thumbnail")
        category = category_slug(tour)
        days = duration_days(tour.get("duration"))

        rows.append(
            "    ("
            + ", ".join(
                [
                    sql_text(slug),
                    sql_text(name),
                    sql_text(category),
                    sql_text(normalized_description(tour)),
                    sql_text(normalized_short_description(tour)),
                    sql_json(tour.get("itinerary") or []),
                    sql_json(tour.get("inclusions") or []),
                    sql_json(tour.get("exclusions") or []),
                    str(float(tour.get("price_adult") or 0)),
                    str(float(tour.get("price_child") or 0)),
                    str(float(tour.get("price_infant") or 0)),
                    str(int(tour.get("discount_percent") or 0)),
                    sql_text(clean_text(tour.get("duration"), 50)),
                    sql_text(clean_text(tour.get("start_time"), 50)),
                    sql_text(clean_text(tour.get("meeting_point"), 255)),
                    str(max(1, int(tour.get("max_people") or 30))),
                    str(max(1, int(tour.get("min_people") or 1))),
                    sql_text(thumbnail),
                    sql_json(image_urls),
                    sql_text(source_url),
                    str(days),
                    str(index),
                ]
            )
            + ")"
        )

        name_haystack = tour.get("name", "").lower()
        location_ids = set()
        location_keywords = {
            "Da Nang": ("da nang",),
            "Ba Na Hills": ("ba na", "bana"),
            "Hoi An": ("hoi an",),
            "Hue": ("hue",),
            "Son Tra": ("son tra", "linh ung"),
            "Cu Lao Cham": ("cham island", "cu lao cham"),
            "My Son": ("my son",),
            "Marble Mountains": ("marble mountain",),
        }
        for destination, keywords in location_keywords.items():
            if any(keyword in name_haystack for keyword in keywords):
                location_ids.add(LOCATION_RULES[destination])
        if not location_ids:
            location_ids.add(LOCATION_RULES["Da Nang"])
        for location_id in sorted(location_ids):
            mappings.append(f"    ({sql_text(slug)}, {location_id})")

        schedules.append(f"    ({sql_text(slug)}, {days}, {index})")

    return f"""-- Verified real tour catalog import.
-- Source: danangtrip-crawler/data/verified-real-tour-catalog-cloudinary-20260607.json
-- Policy:
--   - upsert by slug, never delete historical tours or relations;
--   - imported tours remain inactive until editorial/admin approval;
--   - source facts remain in itinerary/inclusions/exclusions;
--   - all media URLs use the verified Cloudinary catalog;
--   - future schedules are operational data generated at seed runtime.

BEGIN;

CREATE TEMP TABLE verified_real_tour_import (
    slug varchar(220) PRIMARY KEY,
    name varchar(200) NOT NULL,
    category_slug varchar(220) NOT NULL,
    description text NOT NULL,
    short_desc varchar(500) NOT NULL,
    itinerary json NOT NULL,
    inclusions json NOT NULL,
    exclusions json NOT NULL,
    price_adult numeric(12,2) NOT NULL,
    price_child numeric(12,2) NOT NULL,
    price_infant numeric(12,2) NOT NULL,
    discount_percent integer NOT NULL,
    duration varchar(50),
    start_time varchar(50),
    meeting_point varchar(255),
    max_people integer NOT NULL,
    min_people integer NOT NULL,
    thumbnail text,
    images json NOT NULL,
    source_url text NOT NULL,
    duration_days integer NOT NULL,
    import_order integer NOT NULL
) ON COMMIT DROP;

INSERT INTO verified_real_tour_import VALUES
{",\n".join(rows)};

INSERT INTO tours (
    name, slug, tour_category_id, description, short_desc, itinerary, inclusions,
    exclusions, price_adult, price_child, price_infant, discount_percent, duration,
    start_time, meeting_point, max_people, min_people, thumbnail, images, status,
    booking_availability, is_featured, is_hot, created_at, updated_at
)
SELECT
    source.name,
    source.slug,
    category.id,
    source.description,
    source.short_desc,
    source.itinerary,
    source.inclusions,
    source.exclusions,
    source.price_adult,
    source.price_child,
    source.price_infant,
    source.discount_percent,
    source.duration,
    source.start_time,
    source.meeting_point,
    source.max_people,
    source.min_people,
    source.thumbnail,
    source.images,
    'inactive',
    'open',
    false,
    false,
    NOW(),
    NOW()
FROM verified_real_tour_import source
JOIN tour_categories category ON category.slug = source.category_slug
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    tour_category_id = EXCLUDED.tour_category_id,
    description = EXCLUDED.description,
    short_desc = EXCLUDED.short_desc,
    itinerary = EXCLUDED.itinerary,
    inclusions = EXCLUDED.inclusions,
    exclusions = EXCLUDED.exclusions,
    price_adult = EXCLUDED.price_adult,
    price_child = EXCLUDED.price_child,
    price_infant = EXCLUDED.price_infant,
    discount_percent = EXCLUDED.discount_percent,
    duration = EXCLUDED.duration,
    start_time = EXCLUDED.start_time,
    meeting_point = EXCLUDED.meeting_point,
    max_people = EXCLUDED.max_people,
    min_people = EXCLUDED.min_people,
    thumbnail = EXCLUDED.thumbnail,
    images = EXCLUDED.images,
    updated_at = NOW();

WITH mapping(slug, location_id) AS (
VALUES
{",\n".join(mappings)}
)
INSERT INTO tour_locations (tour_id, location_id, created_at)
SELECT tours.id, mapping.location_id, NOW()
FROM mapping
JOIN tours ON tours.slug = mapping.slug
JOIN locations ON locations.id = mapping.location_id
ON CONFLICT (tour_id, location_id) DO NOTHING;

WITH schedule_source(slug, duration_days, import_order) AS (
VALUES
{",\n".join(schedules)}
),
future_dates AS (
    SELECT
        schedule_source.*,
        (
            date_trunc('week', CURRENT_DATE)::date
            + 5
            + (week_index * 7)
        )::date AS start_date,
        week_index
    FROM schedule_source
    CROSS JOIN generate_series(1, 8) AS week_index
)
INSERT INTO tour_schedules (
    tour_id, start_date, end_date, max_people, booked_people, price_adult,
    price_child, price_infant, status, booking_availability, departure_code,
    departure_place, booking_deadline, created_at, updated_at
)
SELECT
    tours.id,
    future_dates.start_date,
    future_dates.start_date + (future_dates.duration_days - 1),
    tours.max_people,
    0,
    tours.price_adult,
    tours.price_child,
    tours.price_infant,
    'available',
    'open',
    'REAL-' || lpad(future_dates.import_order::text, 2, '0')
        || '-' || to_char(future_dates.start_date, 'YYYYMMDD'),
    COALESCE(NULLIF(tours.meeting_point, ''), 'Đà Nẵng / điểm đón của đơn vị tổ chức'),
    (future_dates.start_date::timestamp - interval '18 hours'),
    NOW(),
    NOW()
FROM future_dates
JOIN tours ON tours.slug = future_dates.slug
ON CONFLICT (tour_id, start_date) DO NOTHING;

SELECT setval(
    pg_get_serial_sequence('tours', 'id'),
    GREATEST((SELECT MAX(id) FROM tours), 1),
    true
);

COMMIT;
"""


def main() -> None:
    catalog = json.loads(INPUT.read_text(encoding="utf-8"))
    if len(catalog) != 30:
        raise ValueError(f"Expected 30 verified tours, found {len(catalog)}")

    invalid = [
        tour.get("slug")
        for tour in catalog
        if tour.get("verification", {}).get("status") != "verified_staging"
        or not tour.get("verification", {}).get("cloudinaryUploaded")
        or len(tour.get("image_urls") or []) < 2
    ]
    if invalid:
        raise ValueError(f"Catalog contains unverified tours: {invalid}")

    OUTPUT.write_text(build_seed(catalog), encoding="utf-8", newline="\n")
    print(
        json.dumps(
            {
                "input": str(INPUT),
                "output": str(OUTPUT),
                "tours": len(catalog),
                "status": "inactive",
                "schedules_per_tour": 8,
            },
            ensure_ascii=True,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
