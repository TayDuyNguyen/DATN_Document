from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_INPUT = DATA_DIR / "tour-location-review.json"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--output-prefix", default="missing-location-candidates")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.is_absolute():
        input_path = ROOT / input_path

    rows = json.loads(input_path.read_text(encoding="utf-8"))
    candidates = build_candidates(rows)

    json_output = DATA_DIR / f"{args.output_prefix}.json"
    csv_output = DATA_DIR / f"{args.output_prefix}.csv"
    report_output = DATA_DIR / f"{args.output_prefix}-report.json"

    json_output.write_text(json.dumps(candidates, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_csv(csv_output, candidates)

    report = {
        "input": str(input_path.relative_to(ROOT)).replace("\\", "/"),
        "outputs": {
            "json": str(json_output.relative_to(ROOT)).replace("\\", "/"),
            "csv": str(csv_output.relative_to(ROOT)).replace("\\", "/"),
        },
        "missingLocationCandidateCount": len(candidates),
        "policy": {
            "manualReviewRequired": True,
            "doesNotPublishDb": True,
        },
    }
    report_output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=True, indent=2))


def build_candidates(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, dict[str, Any]] = {}
    for row in rows:
        if row.get("location_status") != "missing_location_seed":
            continue
        slug = row["location_slug"]
        item = grouped.setdefault(
            slug,
            {
                "location_slug": slug,
                "location_name": row["location_name"],
                "review_status": "pending_review",
                "approve_for_location_seed": False,
                "matched_tour_count": 0,
                "matched_tour_slugs": [],
                "suggested_action": "create_location_seed_before_tour_locations",
                "fix_notes": "",
            },
        )
        item["matched_tour_count"] += 1
        item["matched_tour_slugs"].append(row["tour_slug"])
    return sorted(grouped.values(), key=lambda item: item["location_slug"])


def write_csv(path: Path, candidates: list[dict[str, Any]]) -> None:
    fieldnames = [
        "location_slug",
        "location_name",
        "review_status",
        "approve_for_location_seed",
        "matched_tour_count",
        "matched_tour_slugs",
        "suggested_action",
        "fix_notes",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for candidate in candidates:
            row = dict(candidate)
            row["matched_tour_slugs"] = "; ".join(row["matched_tour_slugs"])
            writer.writerow(row)


if __name__ == "__main__":
    main()
