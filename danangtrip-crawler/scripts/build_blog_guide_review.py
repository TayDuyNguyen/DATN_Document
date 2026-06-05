from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
INPUT = DATA_DIR / "blog-guides-staging.json"
CSV_OUTPUT = DATA_DIR / "blog-guides-review.csv"
JSON_OUTPUT = DATA_DIR / "blog-guides-review.json"
REPORT_OUTPUT = DATA_DIR / "blog-guides-review-report.json"


def main() -> None:
    items = load_json(INPUT)
    review_rows = []
    for item in items:
        review_rows.append(
            {
                "approve_for_seed": False,
                "title": item.get("title"),
                "slug": item.get("slug"),
                "category_hint": item.get("category_hint"),
                "tags_hint": ", ".join(item.get("tags_hint") or []),
                "excerpt": item.get("excerpt"),
                "source_name": item.get("source_name"),
                "source_url": item.get("source_url"),
                "review_flags": ", ".join(item.get("review_flags") or []),
                "status": item.get("status"),
            }
        )

    JSON_OUTPUT.write_text(json.dumps(review_rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with CSV_OUTPUT.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(review_rows[0].keys()) if review_rows else [])
        if review_rows:
            writer.writeheader()
            writer.writerows(review_rows)

    report = {
        "input": str(INPUT),
        "csvOutput": str(CSV_OUTPUT),
        "jsonOutput": str(JSON_OUTPUT),
        "total": len(review_rows),
        "pendingReview": sum(1 for row in review_rows if row["status"] == "pending_review"),
        "recordsWithFlags": sum(1 for row in review_rows if row["review_flags"]),
    }
    REPORT_OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=True, indent=2))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
