from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


def main() -> None:
    parser = argparse.ArgumentParser(description="Merge normalized blog guide crawl batches.")
    parser.add_argument(
        "--inputs",
        nargs="+",
        default=[
            str(DATA_DIR / "blog-guides-batch3-clean-normalized.json"),
            str(DATA_DIR / "blog-guides-batch4-clean-normalized.json"),
        ],
    )
    parser.add_argument("--output", default=str(DATA_DIR / "blog-guides-staging.json"))
    args = parser.parse_args()

    merged: list[dict[str, Any]] = []
    seen_source_urls = set()
    seen_slugs = set()

    for input_path in args.inputs:
        for item in load_json(Path(input_path)):
            source_url = item.get("source_url")
            slug = item.get("slug")
            if source_url in seen_source_urls:
                continue
            if slug in seen_slugs:
                item = dict(item)
                item["slug"] = unique_slug(slug, item.get("source_name") or "source", seen_slugs)
                item["review_flags"] = sorted(set(item.get("review_flags") or []) | {"deduped_slug"})
            seen_source_urls.add(source_url)
            seen_slugs.add(item["slug"])
            merged.append(item)

    output = Path(args.output)
    output.write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = {
        "output": str(output),
        "inputs": args.inputs,
        "total": len(merged),
        "byCategoryHint": summarize(merged, "category_hint"),
        "recordsWithReviewFlags": sum(1 for item in merged if item.get("review_flags")),
        "status": "pending_review",
    }
    report_path = output.with_name(output.stem + "-report.json")
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=True, indent=2))


def unique_slug(slug: str, source_name: str, seen_slugs: set[str]) -> str:
    base = f"{slug}-{source_name}".strip("-")[:250]
    candidate = base
    index = 2
    while candidate in seen_slugs:
        candidate = f"{base}-{index}"[:260]
        index += 1
    return candidate


def summarize(items: list[dict[str, Any]], key: str) -> dict[str, int]:
    result: dict[str, int] = {}
    for item in items:
        value = item.get(key) or "unknown"
        result[value] = result.get(value, 0) + 1
    return dict(sorted(result.items()))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
