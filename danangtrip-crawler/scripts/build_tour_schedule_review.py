from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_INPUT = DATA_DIR / "tour-staging-enriched.json"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--output-prefix", default="tour-schedule-review")
    parser.add_argument("--days", type=int, default=30)
    parser.add_argument("--schedules-per-tour", type=int, default=4)
    parser.add_argument("--start-date")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.is_absolute():
        input_path = ROOT / input_path

    start_date = date.fromisoformat(args.start_date) if args.start_date else date.today() + timedelta(days=1)
    tours = json.loads(input_path.read_text(encoding="utf-8"))
    rows = []
    for tour in tours:
        rows.extend(build_rows_for_tour(tour, start_date, args.days, args.schedules_per_tour))

    json_output = DATA_DIR / f"{args.output_prefix}.json"
    csv_output = DATA_DIR / f"{args.output_prefix}.csv"
    report_output = DATA_DIR / f"{args.output_prefix}-report.json"

    json_output.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_csv(csv_output, rows)

    report = build_report(input_path, json_output, csv_output, rows, len(tours), start_date, args.days)
    report_output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=True, indent=2))


def build_rows_for_tour(tour: dict[str, Any], start_date: date, days: int, schedules_per_tour: int) -> list[dict[str, Any]]:
    dates = select_schedule_dates(tour, start_date, days, schedules_per_tour)
    rows = []
    for index, schedule_date in enumerate(dates, start=1):
        start_time = infer_start_time(tour)
        deadline = datetime.combine(schedule_date - timedelta(days=1), time(hour=18), tzinfo=timezone.utc)
        flags = []
        if start_time["source"] != "crawl":
            flags.append("start_time_inferred")
        if tour_has_inferred_fields(tour):
            flags.append("tour_has_inferred_fields")
        if not tour.get("itinerary"):
            flags.append("missing_itinerary")
        if not tour.get("inclusions"):
            flags.append("missing_inclusions")

        rows.append(
            {
                "schedule_review_id": f"{tour.get('slug')}-SCH-{index:02d}",
                "tour_slug": tour.get("slug"),
                "tour_name": tour.get("name"),
                "review_status": "pending_review",
                "approve_for_seed": False,
                "start_date": schedule_date.isoformat(),
                "end_date": schedule_date.isoformat(),
                "max_people": int(tour.get("max_people") or 30),
                "booked_people": 0,
                "price_adult": float(tour.get("price_adult") or 0),
                "price_child": float(tour.get("price_child") or 0),
                "price_infant": float(tour.get("price_infant") or 0),
                "status": "available",
                "booking_availability": "open",
                "departure_code": build_departure_code(tour, schedule_date, index),
                "departure_place": tour.get("meeting_point") or "Da Nang / operator pickup point",
                "start_time": start_time["value"],
                "start_time_source": start_time["source"],
                "booking_deadline": deadline.isoformat(),
                "schedule_pattern": infer_schedule_pattern(tour),
                "review_flags": flags,
                "fix_notes": "",
                "source_url": (tour.get("source") or {}).get("url"),
            }
        )
    return rows


def select_schedule_dates(tour: dict[str, Any], start_date: date, days: int, limit: int) -> list[date]:
    pattern = infer_schedule_pattern(tour)
    candidates = [start_date + timedelta(days=offset) for offset in range(days)]
    if pattern == "weekend":
        candidates = [value for value in candidates if value.weekday() in (5, 6)]
    elif pattern == "weekday":
        candidates = [value for value in candidates if value.weekday() < 5]
    return candidates[:limit]


def infer_schedule_pattern(tour: dict[str, Any]) -> str:
    text = searchable_text(tour)
    if any(value in text for value in ("daily", "everyday", "every day", "daily tour")):
        return "daily"
    if any(value in text for value in ("night tour", "weekend")):
        return "weekend"
    return "daily"


def infer_start_time(tour: dict[str, Any]) -> dict[str, str]:
    existing = clean_text(tour.get("start_time"))
    if existing:
        parsed = parse_time(existing)
        if parsed:
            return {"value": parsed, "source": "crawl"}

    text = schedule_time_text(tour)
    parsed = parse_time(text)
    if parsed:
        return {"value": parsed, "source": "context"}

    if "afternoon" in text or "sunset" in text:
        return {"value": "13:30", "source": "rule"}
    if "night" in text:
        return {"value": "16:00", "source": "rule"}
    if "half day" in text:
        return {"value": "08:00", "source": "rule"}
    return {"value": "08:00", "source": "default"}


def parse_time(text: str) -> str | None:
    match = re.search(r"\b([01]?\d|2[0-3])[:h]([0-5]\d)\b", text)
    if match:
        return f"{int(match.group(1)):02d}:{match.group(2)}"
    match = re.search(r"\b([6-9]|1[0-9]|2[0-3])\s*(?:am|pm)\b", text, flags=re.IGNORECASE)
    if match:
        hour = int(match.group(1))
        if "pm" in match.group(0).lower() and hour < 12:
            hour += 12
        return f"{hour:02d}:00"
    return None


def build_departure_code(tour: dict[str, Any], schedule_date: date, index: int) -> str:
    slug = str(tour.get("slug") or "tour")
    prefix = "".join(part[:1].upper() for part in slug.split("-")[:4])[:8] or "TOUR"
    return f"{prefix}-{schedule_date.strftime('%Y%m%d')}-{index:02d}"[:50]


def searchable_text(tour: dict[str, Any]) -> str:
    parts = [
        tour.get("name") or "",
        tour.get("slug") or "",
        tour.get("duration") or "",
        tour.get("meeting_point") or "",
        " ".join(tour.get("itinerary") or []),
        " ".join(tour.get("inclusions") or []),
        (tour.get("source") or {}).get("url") or "",
    ]
    return " ".join(parts).lower()


def schedule_time_text(tour: dict[str, Any]) -> str:
    parts = [
        tour.get("name") or "",
        tour.get("duration") or "",
        tour.get("meeting_point") or "",
        (tour.get("source") or {}).get("url") or "",
    ]
    return " ".join(parts).lower()


def tour_has_inferred_fields(tour: dict[str, Any]) -> bool:
    return bool(tour.get("inferred_fields"))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames = [
        "schedule_review_id",
        "tour_slug",
        "tour_name",
        "review_status",
        "approve_for_seed",
        "start_date",
        "end_date",
        "max_people",
        "booked_people",
        "price_adult",
        "price_child",
        "price_infant",
        "status",
        "booking_availability",
        "departure_code",
        "departure_place",
        "start_time",
        "start_time_source",
        "booking_deadline",
        "schedule_pattern",
        "review_flags",
        "fix_notes",
        "source_url",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            value = dict(row)
            value["review_flags"] = "; ".join(value["review_flags"])
            writer.writerow(value)


def build_report(
    input_path: Path,
    json_output: Path,
    csv_output: Path,
    rows: list[dict[str, Any]],
    tour_count: int,
    start_date: date,
    days: int,
) -> dict[str, Any]:
    return {
        "input": str(input_path.relative_to(ROOT)).replace("\\", "/"),
        "outputs": {
            "json": str(json_output.relative_to(ROOT)).replace("\\", "/"),
            "csv": str(csv_output.relative_to(ROOT)).replace("\\", "/"),
        },
        "tourCount": tour_count,
        "scheduleRows": len(rows),
        "dateWindow": {
            "start": start_date.isoformat(),
            "days": days,
        },
        "pendingReview": sum(1 for row in rows if row["review_status"] == "pending_review"),
        "approvedForSeed": sum(1 for row in rows if row["approve_for_seed"]),
        "startTimeSources": count_by(rows, "start_time_source"),
        "schedulePatterns": count_by(rows, "schedule_pattern"),
        "rowsWithReviewFlags": sum(1 for row in rows if row["review_flags"]),
        "policy": {
            "approveForSeedDefault": False,
            "manualReviewRequired": True,
            "doesNotPublishDb": True,
        },
    }


def count_by(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    result: dict[str, int] = {}
    for row in rows:
        value = str(row[key])
        result[value] = result.get(value, 0) + 1
    return dict(sorted(result.items()))


def clean_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


if __name__ == "__main__":
    main()
