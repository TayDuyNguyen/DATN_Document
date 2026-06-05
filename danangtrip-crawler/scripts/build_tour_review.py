from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_INPUT = DATA_DIR / "tour-staging.json"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--output-prefix", default="tour-review")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.is_absolute():
        input_path = ROOT / input_path

    items = json.loads(input_path.read_text(encoding="utf-8"))
    review_items = [build_review_item(index + 1, item) for index, item in enumerate(items)]

    json_output = DATA_DIR / f"{args.output_prefix}.json"
    csv_output = DATA_DIR / f"{args.output_prefix}.csv"
    report_output = DATA_DIR / f"{args.output_prefix}-report.json"

    json_output.write_text(json.dumps(review_items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_csv(csv_output, review_items)

    report = build_report(input_path, json_output, csv_output, review_items)
    report_output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=True, indent=2))


def build_review_item(index: int, item: dict[str, Any]) -> dict[str, Any]:
    review_flags = []
    if not item.get("price_adult"):
        review_flags.append("missing_price")
    if not item.get("duration"):
        review_flags.append("missing_duration")
    if not item.get("itinerary"):
        review_flags.append("missing_itinerary")
    if not item.get("inclusions"):
        review_flags.append("missing_inclusions")
    if not item.get("destination_names"):
        review_flags.append("missing_destinations")
    if len(item.get("images") or []) < 2:
        review_flags.append("few_images")

    source = item.get("source") or {}
    return {
        "review_id": f"TOUR-{index:03d}",
        "review_status": "pending_review",
        "approve_for_seed": False,
        "reject_reason": "",
        "fix_notes": "",
        "name": item.get("name"),
        "slug": item.get("slug"),
        "tour_category_slug": item.get("tour_category_slug"),
        "destination_names": item.get("destination_names") or [],
        "price_adult": item.get("price_adult"),
        "price_raw": item.get("price_raw"),
        "duration": item.get("duration"),
        "meeting_point": item.get("meeting_point"),
        "thumbnail": item.get("thumbnail"),
        "image_count": len(item.get("images") or []),
        "itinerary_count": len(item.get("itinerary") or []),
        "inclusions_count": len(item.get("inclusions") or []),
        "exclusions_count": len(item.get("exclusions") or []),
        "review_flags": review_flags,
        "inferred_fields": item.get("inferred_fields") or [],
        "source_name": source.get("name"),
        "source_url": source.get("url"),
    }


def write_csv(path: Path, items: list[dict[str, Any]]) -> None:
    fieldnames = [
        "review_id",
        "review_status",
        "approve_for_seed",
        "reject_reason",
        "fix_notes",
        "name",
        "slug",
        "tour_category_slug",
        "destination_names",
        "price_adult",
        "price_raw",
        "duration",
        "meeting_point",
        "thumbnail",
        "image_count",
        "itinerary_count",
        "inclusions_count",
        "exclusions_count",
        "review_flags",
        "inferred_fields",
        "source_name",
        "source_url",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for item in items:
            row = dict(item)
            row["destination_names"] = "; ".join(row["destination_names"])
            row["review_flags"] = "; ".join(row["review_flags"])
            row["inferred_fields"] = "; ".join(
                f"{field.get('field')}={field.get('value')} ({field.get('confidence')}, {field.get('method')})"
                for field in row["inferred_fields"]
            )
            writer.writerow(row)


def build_report(input_path: Path, json_output: Path, csv_output: Path, items: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "input": str(input_path.relative_to(ROOT)).replace("\\", "/"),
        "outputs": {
            "json": str(json_output.relative_to(ROOT)).replace("\\", "/"),
            "csv": str(csv_output.relative_to(ROOT)).replace("\\", "/"),
        },
        "total": len(items),
        "pendingReview": sum(1 for item in items if item["review_status"] == "pending_review"),
        "missingPrice": count_flag(items, "missing_price"),
        "missingDuration": count_flag(items, "missing_duration"),
        "missingItinerary": count_flag(items, "missing_itinerary"),
        "missingInclusions": count_flag(items, "missing_inclusions"),
        "fewImages": count_flag(items, "few_images"),
        "itemsWithInferredFields": sum(1 for item in items if item.get("inferred_fields")),
        "policy": {
            "approveForSeedDefault": False,
            "manualReviewRequired": True,
            "doesNotPublishDb": True,
        },
    }


def count_flag(items: list[dict[str, Any]], flag: str) -> int:
    return sum(1 for item in items if flag in item["review_flags"])


if __name__ == "__main__":
    main()
