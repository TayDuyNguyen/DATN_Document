import argparse
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT.parent / "data-center" / "reports" / "tours-quality-input-2026-06-04.json"
DEFAULT_OUTPUT = ROOT.parent / "database-seeders" / "39_tour_content_quality_backfill_seed.sql"


def sql_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def json_sql(value: Any) -> str:
    return sql_quote(json.dumps(value, ensure_ascii=False)) + "::json"


def text(value: Any) -> str:
    return str(value or "").strip()


def is_empty_json(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        value = value.strip()
        if not value:
            return True
        try:
            value = json.loads(value)
        except json.JSONDecodeError:
            return False
    return isinstance(value, list) and len(value) == 0


def destination_from_name(name: str) -> str:
    lowered = name.lower()
    known = [
        ("bà nà", "Bà Nà Hills"),
        ("ba na", "Bà Nà Hills"),
        ("hội an", "Hội An"),
        ("hoi an", "Hội An"),
        ("huế", "Huế"),
        ("hue", "Huế"),
        ("sơn trà", "Sơn Trà"),
        ("son tra", "Sơn Trà"),
        ("mỹ sơn", "Mỹ Sơn"),
        ("my son", "Mỹ Sơn"),
        ("cù lao chàm", "Cù Lao Chàm"),
        ("cu lao cham", "Cù Lao Chàm"),
        ("ngũ hành sơn", "Ngũ Hành Sơn"),
        ("ngu hanh son", "Ngũ Hành Sơn"),
        ("hải vân", "Đèo Hải Vân"),
        ("hai van", "Đèo Hải Vân"),
        ("đà nẵng", "Đà Nẵng"),
        ("da nang", "Đà Nẵng"),
    ]
    for needle, destination in known:
        if needle in lowered:
            return destination
    return "Đà Nẵng"


def day_count(duration: str) -> int:
    duration = duration.lower()
    match = re.search(r"(\d+)\s*(ngày|day)", duration)
    if match:
        return max(1, int(match.group(1)))
    if "nửa" in duration or "half" in duration:
        return 1
    return 1


def itinerary_for(row: dict[str, Any]) -> list[dict[str, str]]:
    name = text(row.get("name"))
    duration = text(row.get("duration")) or "1 ngày"
    destination = destination_from_name(name)
    days = day_count(duration)
    if days >= 2:
        return [
            {
                "day": "Ngày 1",
                "title": f"Khởi hành và khám phá {destination}",
                "description": f"Đón khách tại điểm hẹn ở Đà Nẵng, di chuyển đến {destination}, tham quan các điểm nổi bật và dùng bữa theo chương trình.",
            },
            {
                "day": "Ngày 2",
                "title": "Trải nghiệm địa phương và trở về",
                "description": "Tiếp tục tham quan, mua sắm đặc sản địa phương, sau đó đưa khách về điểm hẹn ban đầu.",
            },
        ]
    return [
        {
            "time": "07:30",
            "title": "Đón khách",
            "description": "Xe và hướng dẫn viên đón khách tại điểm hẹn trung tâm Đà Nẵng.",
        },
        {
            "time": "09:00",
            "title": f"Tham quan {destination}",
            "description": f"Khám phá các điểm nổi bật của {destination}, chụp ảnh và nghe giới thiệu về văn hóa địa phương.",
        },
        {
            "time": "12:00",
            "title": "Dùng bữa và nghỉ ngơi",
            "description": "Thưởng thức bữa ăn theo chương trình hoặc tự do trải nghiệm ẩm thực địa phương tùy gói tour.",
        },
        {
            "time": "15:30",
            "title": "Trải nghiệm bổ sung",
            "description": "Tiếp tục tham quan, mua sắm đặc sản hoặc tự do khám phá theo hướng dẫn của điều phối tour.",
        },
        {
            "time": "17:30",
            "title": "Kết thúc tour",
            "description": "Đưa khách về lại điểm hẹn ban đầu tại Đà Nẵng.",
        },
    ]


def inclusions_for(row: dict[str, Any]) -> list[str]:
    return [
        "Xe đưa đón theo chương trình",
        "Hướng dẫn viên địa phương",
        "Vé tham quan theo lịch trình nếu có trong gói",
        "Nước uống trên xe",
        "Bảo hiểm du lịch cơ bản",
    ]


def exclusions_for(row: dict[str, Any]) -> list[str]:
    return [
        "Chi phí cá nhân ngoài chương trình",
        "Bữa ăn và đồ uống không nêu trong phần bao gồm",
        "Phụ thu cuối tuần, lễ Tết nếu có",
        "Tiền tip cho hướng dẫn viên và tài xế",
    ]


def default_start_time(row: dict[str, Any]) -> str:
    duration = text(row.get("duration")).lower()
    if "nửa" in duration or "half" in duration:
        return "08:00"
    return "07:30"


def default_meeting_point(row: dict[str, Any]) -> str:
    return "Trung tâm Đà Nẵng hoặc khách sạn trong khu vực nội thành"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    rows = json.loads(args.input.read_text(encoding="utf-8"))
    values: list[str] = []
    for row in rows:
        update = {
            "id": int(row["id"]),
            "itinerary": itinerary_for(row) if is_empty_json(row.get("itinerary")) else None,
            "inclusions": inclusions_for(row) if is_empty_json(row.get("inclusions")) else None,
            "exclusions": exclusions_for(row) if is_empty_json(row.get("exclusions")) else None,
            "start_time": default_start_time(row) if not text(row.get("start_time")) else None,
            "meeting_point": default_meeting_point(row) if not text(row.get("meeting_point")) else None,
            "price_infant": int(float(row.get("price_infant") or 0)) or 50000,
        }
        if not any(value is not None for key, value in update.items() if key != "id"):
            continue
        values.append(
            "        ("
            + ", ".join([
                str(update["id"]),
                "NULL" if update["itinerary"] is None else json_sql(update["itinerary"]),
                "NULL" if update["inclusions"] is None else json_sql(update["inclusions"]),
                "NULL" if update["exclusions"] is None else json_sql(update["exclusions"]),
                "NULL" if update["start_time"] is None else sql_quote(update["start_time"]),
                "NULL" if update["meeting_point"] is None else sql_quote(update["meeting_point"]),
                str(update["price_infant"]),
            ])
            + ")"
        )

    lines = [
        "-- DanangTrip tour content quality backfill",
        "-- FILE: 39_tour_content_quality_backfill_seed.sql",
        "-- Purpose: Fill missing tour itinerary, inclusions, exclusions, start time, meeting point, and infant price defaults.",
        "",
        "WITH tour_updates(id, itinerary, inclusions, exclusions, start_time, meeting_point, price_infant) AS (",
        "    VALUES",
        ",\n".join(values),
        ")",
        "UPDATE tours t",
        "SET itinerary = CASE WHEN t.itinerary IS NULL OR json_array_length(t.itinerary) = 0 THEN tour_updates.itinerary ELSE t.itinerary END,",
        "    inclusions = CASE WHEN t.inclusions IS NULL OR json_array_length(t.inclusions) = 0 THEN tour_updates.inclusions ELSE t.inclusions END,",
        "    exclusions = CASE WHEN t.exclusions IS NULL OR json_array_length(t.exclusions) = 0 THEN tour_updates.exclusions ELSE t.exclusions END,",
        "    start_time = COALESCE(NULLIF(t.start_time, ''), tour_updates.start_time),",
        "    meeting_point = COALESCE(NULLIF(t.meeting_point, ''), tour_updates.meeting_point),",
        "    price_infant = CASE WHEN t.price_infant IS NULL OR t.price_infant <= 0 THEN tour_updates.price_infant ELSE t.price_infant END,",
        "    updated_at = NOW()",
        "FROM tour_updates",
        "WHERE t.id = tour_updates.id;",
        "",
    ]
    args.output.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"updates": len(values), "output": str(args.output)}, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
