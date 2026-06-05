from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"

GENERIC_TOUR_KEYWORDS = (
    "daily group tour package",
    "vietnam luxury tour",
)


def main() -> None:
    locations = load_json(DATA_DIR / "missing-locations-review.json")
    tours = load_json(DATA_DIR / "tour-review-enriched.json")
    tour_locations = load_json(DATA_DIR / "tour-location-review.json")
    schedules = load_json(DATA_DIR / "tour-schedule-review.json")

    decided_locations = decide_locations(locations)
    approved_location_slugs = {
        item["location_slug"] for item in decided_locations if item.get("approve_for_location_seed")
    }

    decided_tours = decide_tours(tours)
    approved_tour_slugs = {item["slug"] for item in decided_tours if item.get("approve_for_seed")}

    decided_tour_locations = decide_tour_locations(tour_locations, approved_tour_slugs, approved_location_slugs)
    decided_schedules = decide_schedules(schedules, approved_tour_slugs)

    write_json(DATA_DIR / "approved-locations-review.json", decided_locations)
    write_csv(DATA_DIR / "approved-locations-review.csv", decided_locations)
    write_json(DATA_DIR / "approved-tours-review.json", decided_tours)
    write_csv(DATA_DIR / "approved-tours-review.csv", decided_tours)
    write_json(DATA_DIR / "approved-tour-locations-review.json", decided_tour_locations)
    write_csv(DATA_DIR / "approved-tour-locations-review.csv", decided_tour_locations)
    write_json(DATA_DIR / "approved-tour-schedules-review.json", decided_schedules)
    write_csv(DATA_DIR / "approved-tour-schedules-review.csv", decided_schedules)

    report = {
        "locations": summarize(decided_locations, "approve_for_location_seed"),
        "tours": summarize(decided_tours, "approve_for_seed"),
        "tourLocations": summarize(decided_tour_locations, "approve_for_seed"),
        "tourSchedules": summarize(decided_schedules, "approve_for_seed"),
        "policy": {
            "doesNotPublishDb": True,
            "doesNotCreateSqlSeed": True,
            "reviewFilesOnly": True,
            "fallbackLocationsRequireManualCoordinateReview": True,
        },
    }
    write_json(DATA_DIR / "approved-review-report.json", report)
    print(json.dumps(report, ensure_ascii=True, indent=2))


def decide_locations(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    decided = []
    for item in items:
        row = dict(item)
        flags = set(row.get("review_flags") or [])
        if row.get("source_type") == "nominatim" and "missing_coordinates" not in flags:
            row["review_status"] = "approved"
            row["approve_for_location_seed"] = True
            row["fix_notes"] = append_note(row.get("fix_notes"), "Auto-approved: Nominatim/OpenStreetMap coordinates present.")
        else:
            row["review_status"] = "pending_review"
            row["approve_for_location_seed"] = False
            row["fix_notes"] = append_note(row.get("fix_notes"), "Pending: fallback coordinates require manual check.")
        decided.append(row)
    return decided


def decide_tours(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    decided = []
    for item in items:
        row = dict(item)
        name = str(row.get("name") or "").lower()
        flags = set(row.get("review_flags") or [])
        if any(keyword in name for keyword in GENERIC_TOUR_KEYWORDS):
            row["review_status"] = "rejected"
            row["approve_for_seed"] = False
            row["reject_reason"] = "generic_package_not_specific_enough_for_tour_seed"
        elif row.get("price_adult") and row.get("duration") and row.get("image_count", 0) > 0:
            row["review_status"] = "approved"
            row["approve_for_seed"] = True
            if row.get("inferred_fields"):
                row["fix_notes"] = append_note(row.get("fix_notes"), "Approved for staging seed; contains inferred fields requiring final business review.")
            elif flags:
                row["fix_notes"] = append_note(row.get("fix_notes"), "Approved for staging seed with review flags retained.")
            else:
                row["fix_notes"] = append_note(row.get("fix_notes"), "Auto-approved: has price, duration and images.")
        else:
            row["review_status"] = "pending_review"
            row["approve_for_seed"] = False
            row["fix_notes"] = append_note(row.get("fix_notes"), "Pending: missing core tour data.")
        decided.append(row)
    return decided


def decide_tour_locations(
    items: list[dict[str, Any]],
    approved_tour_slugs: set[str],
    approved_location_slugs: set[str],
) -> list[dict[str, Any]]:
    decided = []
    for item in items:
        row = dict(item)
        tour_slug = row.get("tour_slug")
        location_slug = row.get("location_slug")
        status = row.get("location_status")
        if tour_slug not in approved_tour_slugs:
            row["review_status"] = "rejected"
            row["approve_for_seed"] = False
            row["fix_notes"] = append_note(row.get("fix_notes"), "Rejected: parent tour is not approved.")
        elif status == "existing_seed_location":
            row["review_status"] = "approved"
            row["approve_for_seed"] = True
            row["fix_notes"] = append_note(row.get("fix_notes"), "Auto-approved: maps approved tour to existing location seed.")
        elif status == "missing_location_seed" and location_slug in approved_location_slugs:
            row["review_status"] = "approved"
            row["approve_for_seed"] = True
            row["fix_notes"] = append_note(row.get("fix_notes"), "Approved after creating missing location seed.")
        else:
            row["review_status"] = "pending_review"
            row["approve_for_seed"] = False
            row["fix_notes"] = append_note(row.get("fix_notes"), "Pending: location seed is not approved yet.")
        decided.append(row)
    return decided


def decide_schedules(items: list[dict[str, Any]], approved_tour_slugs: set[str]) -> list[dict[str, Any]]:
    decided = []
    for item in items:
        row = dict(item)
        if row.get("tour_slug") in approved_tour_slugs:
            row["review_status"] = "approved"
            row["approve_for_seed"] = True
            row["fix_notes"] = append_note(row.get("fix_notes"), "Auto-approved for staging schedule seed; schedule remains demo/review data.")
        else:
            row["review_status"] = "rejected"
            row["approve_for_seed"] = False
            row["fix_notes"] = append_note(row.get("fix_notes"), "Rejected: parent tour is not approved.")
        decided.append(row)
    return decided


def summarize(items: list[dict[str, Any]], approve_key: str) -> dict[str, int]:
    return {
        "total": len(items),
        "approved": sum(1 for item in items if item.get(approve_key)),
        "rejected": sum(1 for item in items if item.get("review_status") == "rejected"),
        "pending": sum(1 for item in items if item.get("review_status") == "pending_review"),
    }


def append_note(existing: Any, note: str) -> str:
    existing_text = str(existing or "").strip()
    return f"{existing_text} {note}".strip()


def load_json(path: Path) -> list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            value = dict(row)
            for key, item in list(value.items()):
                if isinstance(item, list):
                    value[key] = "; ".join(str(entry) for entry in item)
                elif isinstance(item, dict):
                    value[key] = json.dumps(item, ensure_ascii=False)
            writer.writerow(value)


if __name__ == "__main__":
    main()
