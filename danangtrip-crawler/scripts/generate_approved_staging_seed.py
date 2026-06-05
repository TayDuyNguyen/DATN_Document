from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
SEED_OUTPUT = ROOT.parent / "database-seeders" / "20_approved_tour_staging_seed.sql"

TOUR_CATEGORY_IDS = {
    "tour-ba-na-hills": 1,
    "tour-hoi-an": 2,
    "tour-hue": 3,
    "tour-bien-dao": 4,
    "tour-thien-nhien": 5,
    "tour-am-thuc": 6,
    "tour-mao-hiem": 7,
    "tour-nghi-duong": 8,
    "tour-trong-ngay": 9,
}


def main() -> None:
    staging_tours = load_json(DATA_DIR / "tour-staging-enriched.json")
    approved_tours = load_json(DATA_DIR / "approved-tours-review.json")
    approved_locations = load_json(DATA_DIR / "approved-locations-review.json")
    approved_tour_locations = load_json(DATA_DIR / "approved-tour-locations-review.json")
    approved_schedules = load_json(DATA_DIR / "approved-tour-schedules-review.json")

    approved_tour_slugs = [item["slug"] for item in approved_tours if item.get("approve_for_seed")]
    tour_by_slug = {item["slug"]: item for item in staging_tours if item["slug"] in approved_tour_slugs}
    ordered_tours = [tour_by_slug[slug] for slug in approved_tour_slugs if slug in tour_by_slug]

    tour_id_by_slug = {tour["slug"]: 101 + index for index, tour in enumerate(ordered_tours)}
    new_location_id_by_slug = build_new_location_id_map(approved_locations)
    location_id_by_slug = build_location_id_map(approved_tour_locations, new_location_id_by_slug)

    sql = []
    sql.append("-- DanangTrip approved staging seed generated from crawler review files.")
    sql.append("-- Source: danangtrip-crawler/data/approved-*.json")
    sql.append("-- Policy: staging/demo seed only; images are candidate source URLs; schedules are review/default data.")
    sql.append("-- Run after 03_tour_blog_categories.sql and 05_locations.sql.")
    sql.append("")
    sql.append("BEGIN;")
    sql.append("")
    sql.extend(render_locations(approved_locations, new_location_id_by_slug))
    sql.append("")
    sql.extend(render_tours(ordered_tours, tour_id_by_slug))
    sql.append("")
    sql.extend(render_tour_locations(approved_tour_locations, tour_id_by_slug, location_id_by_slug))
    sql.append("")
    sql.extend(render_tour_schedules(approved_schedules, tour_id_by_slug))
    sql.append("")
    sql.append("SELECT setval(pg_get_serial_sequence('locations', 'id'), GREATEST((SELECT MAX(id) FROM locations), 1));")
    sql.append("SELECT setval(pg_get_serial_sequence('tours', 'id'), GREATEST((SELECT MAX(id) FROM tours), 1));")
    sql.append("SELECT setval(pg_get_serial_sequence('tour_schedules', 'id'), GREATEST((SELECT MAX(id) FROM tour_schedules), 1));")
    sql.append("")
    sql.append("COMMIT;")
    sql.append("")

    SEED_OUTPUT.write_text("\n".join(sql), encoding="utf-8")
    report = {
        "output": str(SEED_OUTPUT),
        "locations": len(new_location_id_by_slug),
        "tours": len(ordered_tours),
        "tourLocations": sum(1 for item in approved_tour_locations if item.get("approve_for_seed")),
        "tourSchedules": sum(1 for item in approved_schedules if item.get("approve_for_seed")),
    }
    report_path = DATA_DIR / "approved-staging-seed-report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=True, indent=2))


def build_new_location_id_map(approved_locations: list[dict[str, Any]]) -> dict[str, int]:
    slugs = [item["location_slug"] for item in approved_locations if item.get("approve_for_location_seed")]
    return {slug: 101 + index for index, slug in enumerate(slugs)}


def build_location_id_map(
    approved_tour_locations: list[dict[str, Any]],
    new_location_id_by_slug: dict[str, int],
) -> dict[str, int]:
    result = dict(new_location_id_by_slug)
    for item in approved_tour_locations:
        if item.get("location_status") == "existing_seed_location" and item.get("location_id_hint"):
            result[item["location_slug"]] = int(item["location_id_hint"])
    return result


def render_locations(
    approved_locations: list[dict[str, Any]],
    new_location_id_by_slug: dict[str, int],
) -> list[str]:
    rows = []
    for item in approved_locations:
        if not item.get("approve_for_location_seed"):
            continue
        location_id = new_location_id_by_slug[item["location_slug"]]
        rows.append(
            "("
            f"{location_id}, "
            f"{sql_string(item['location_name'])}, "
            f"{sql_string(item['location_slug'])}, "
            "1, "
            f"{sql_string(item.get('address'))}, "
            f"{sql_string(item.get('district'))}, "
            f"{sql_decimal(item.get('latitude'))}, "
            f"{sql_decimal(item.get('longitude'))}, "
            f"{sql_string(item.get('description'))}, "
            f"{sql_string(item.get('short_description'))}, "
            "'{\"mon\":\"00:00-23:59\",\"tue\":\"00:00-23:59\",\"wed\":\"00:00-23:59\",\"thu\":\"00:00-23:59\",\"fri\":\"00:00-23:59\",\"sat\":\"00:00-23:59\",\"sun\":\"00:00-23:59\"}'::json, "
            "0, 0, 'pending_review', false, NULL, NOW(), NOW()"
            ")"
        )
    if not rows:
        return ["-- No approved new locations."]
    return [
        "-- 1. Approved missing locations",
        "INSERT INTO locations (id, name, slug, category_id, address, district, latitude, longitude, description, short_description, opening_hours, price_min, price_max, status, is_featured, created_by, created_at, updated_at) VALUES",
        join_rows(rows),
        "ON CONFLICT (slug) DO NOTHING;",
    ]


def render_tours(tours: list[dict[str, Any]], tour_id_by_slug: dict[str, int]) -> list[str]:
    rows = []
    for tour in tours:
        category_id = TOUR_CATEGORY_IDS.get(tour.get("tour_category_slug"), 9)
        rows.append(
            "("
            f"{tour_id_by_slug[tour['slug']]}, "
            f"{sql_string(tour.get('name'))}, "
            f"{sql_string(tour.get('slug'))}, "
            f"{category_id}, "
            f"{sql_string(tour.get('description'))}, "
            f"{sql_string(tour.get('short_desc'))}, "
            f"{sql_json(tour.get('itinerary') or [])}, "
            f"{sql_json(tour.get('inclusions') or [])}, "
            f"{sql_json(tour.get('exclusions') or [])}, "
            f"{sql_decimal(tour.get('price_adult'))}, "
            f"{sql_decimal(tour.get('price_child') or 0)}, "
            f"{sql_decimal(tour.get('price_infant') or 0)}, "
            f"{int(tour.get('discount_percent') or 0)}, "
            f"{sql_string(tour.get('duration'))}, "
            "NULL, "
            f"{sql_string(tour.get('meeting_point'))}, "
            f"{int(tour.get('max_people') or 30)}, "
            f"{int(tour.get('min_people') or 1)}, "
            "NULL, NULL, "
            f"{sql_string(tour.get('thumbnail'))}, "
            f"{sql_json(tour.get('images') or [])}, "
            "NULL, 'pending_review', 'open', false, false, NOW(), NOW()"
            ")"
        )
    return [
        "-- 2. Approved tours",
        "INSERT INTO tours (id, name, slug, tour_category_id, description, short_desc, itinerary, inclusions, exclusions, price_adult, price_child, price_infant, discount_percent, duration, start_time, meeting_point, max_people, min_people, available_from, available_to, thumbnail, images, video_url, status, booking_availability, is_featured, is_hot, created_at, updated_at) VALUES",
        join_rows(rows),
        "ON CONFLICT (slug) DO NOTHING;",
    ]


def render_tour_locations(
    approved_tour_locations: list[dict[str, Any]],
    tour_id_by_slug: dict[str, int],
    location_id_by_slug: dict[str, int],
) -> list[str]:
    rows = []
    seen = set()
    for item in approved_tour_locations:
        if not item.get("approve_for_seed"):
            continue
        tour_id = tour_id_by_slug.get(item.get("tour_slug"))
        location_id = location_id_by_slug.get(item.get("location_slug"))
        if not tour_id or not location_id:
            continue
        key = (tour_id, location_id)
        if key in seen:
            continue
        seen.add(key)
        rows.append(f"({tour_id}, {location_id}, NOW())")
    return [
        "-- 3. Approved tour-location mappings",
        "INSERT INTO tour_locations (tour_id, location_id, created_at) VALUES",
        join_rows(rows),
        "ON CONFLICT (tour_id, location_id) DO NOTHING;",
    ]


def render_tour_schedules(
    approved_schedules: list[dict[str, Any]],
    tour_id_by_slug: dict[str, int],
) -> list[str]:
    rows = []
    schedule_id = 1001
    for item in approved_schedules:
        if not item.get("approve_for_seed"):
            continue
        tour_id = tour_id_by_slug.get(item.get("tour_slug"))
        if not tour_id:
            continue
        rows.append(
            "("
            f"{schedule_id}, "
            f"{tour_id}, "
            f"{sql_string(item.get('start_date'))}::date, "
            f"{sql_string(item.get('end_date'))}::date, "
            f"{int(item.get('max_people') or 0)}, "
            f"{int(item.get('booked_people') or 0)}, "
            f"{sql_decimal(item.get('price_adult'))}, "
            f"{sql_decimal(item.get('price_child') or 0)}, "
            f"{sql_decimal(item.get('price_infant') or 0)}, "
            f"{sql_string(item.get('status') or 'available')}, "
            f"{sql_string(item.get('booking_availability') or 'open')}, "
            f"{sql_string(item.get('departure_code'))}, "
            f"{sql_string(item.get('departure_place'))}, "
            f"{sql_string(item.get('booking_deadline'))}::timestamp, "
            "NOW(), NOW()"
            ")"
        )
        schedule_id += 1
    return [
        "-- 4. Approved tour schedules",
        "INSERT INTO tour_schedules (id, tour_id, start_date, end_date, max_people, booked_people, price_adult, price_child, price_infant, status, booking_availability, departure_code, departure_place, booking_deadline, created_at, updated_at) VALUES",
        join_rows(rows),
        "ON CONFLICT (tour_id, start_date) DO NOTHING;",
    ]


def join_rows(rows: list[str]) -> str:
    return ",\n".join(rows)


def sql_string(value: Any) -> str:
    if value is None or value == "":
        return "NULL"
    return "'" + str(value).replace("'", "''")[:5000] + "'"


def sql_decimal(value: Any) -> str:
    if value is None or value == "":
        return "NULL"
    return str(float(value))


def sql_json(value: Any) -> str:
    return sql_string(json.dumps(value, ensure_ascii=False)) + "::json"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
