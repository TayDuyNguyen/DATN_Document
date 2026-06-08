from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
INPUT = DATA_DIR / "tour-staging-enriched.json"
JSON_OUTPUT = DATA_DIR / "tour-publish-readiness.json"
CSV_OUTPUT = DATA_DIR / "tour-publish-readiness.csv"
REPORT_OUTPUT = DATA_DIR / "tour-publish-readiness-report.json"
RECRAWL_OUTPUT = DATA_DIR / "tour-recrawl-sources.json"
CRAWLER_SOURCE_OUTPUT = DATA_DIR / "tour-recrawl-source-config.json"

DAY_ROUTE_WORDS = (
    "day tour",
    "daily tour",
    "full day",
    "1 day",
    "one day",
    "shore excursion",
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(INPUT))
    parser.add_argument("--output-prefix", default="tour-publish-readiness")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.is_absolute():
        input_path = ROOT / input_path

    json_output = DATA_DIR / f"{args.output_prefix}.json"
    csv_output = DATA_DIR / f"{args.output_prefix}.csv"
    report_output = DATA_DIR / f"{args.output_prefix}-report.json"
    recrawl_output = DATA_DIR / f"{args.output_prefix}-recrawl-sources.json"
    crawler_source_output = DATA_DIR / f"{args.output_prefix}-recrawl-source-config.json"

    items = load_json(input_path)
    audited = [audit_item(item) for item in items]

    json_output.write_text(
        json.dumps(audited, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_csv(csv_output, audited)
    recrawl_sources = [
        {
            "name": item["name"],
            "source_name": item["source_name"],
            "url": item["source_url"],
            "blocking_reasons": item["blocking_reasons"],
        }
        for item in audited
        if item["publish_readiness"] == "needs_recrawl" and item["source_url"]
    ]
    recrawl_output.write_text(
        json.dumps(recrawl_sources, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    crawler_source_output.write_text(
        json.dumps(
            {
                "sources": [
                    {
                        "name": f"recrawl_{index:03d}_{item['source_name']}",
                        "url": item["url"],
                    }
                    for index, item in enumerate(recrawl_sources, start=1)
                ]
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    status_counts = Counter(item["publish_readiness"] for item in audited)
    reason_counts = Counter(
        reason
        for item in audited
        for reason in item["blocking_reasons"]
    )
    report = {
        "input": str(input_path.relative_to(ROOT)).replace("\\", "/"),
        "outputs": {
            "json": str(json_output.relative_to(ROOT)).replace("\\", "/"),
            "csv": str(csv_output.relative_to(ROOT)).replace("\\", "/"),
            "recrawlSources": str(recrawl_output.relative_to(ROOT)).replace("\\", "/"),
            "crawlerSourceConfig": str(crawler_source_output.relative_to(ROOT)).replace("\\", "/"),
        },
        "total": len(audited),
        "byStatus": dict(sorted(status_counts.items())),
        "blockingReasons": dict(reason_counts.most_common()),
        "policy": {
            "writesDatabase": False,
            "requiresManualImageReview": True,
            "inferredCoreFieldsBlocked": True,
            "sourceUrlRequired": True,
            "completeTourContentRequired": True,
        },
    }
    report_output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=True, indent=2))


def audit_item(item: dict[str, Any]) -> dict[str, Any]:
    reasons: list[str] = []
    warnings: list[str] = []
    name = str(item.get("name") or "").strip()
    duration = str(item.get("duration") or "").strip()
    source = item.get("source") or {}
    inferred_fields = item.get("inferred_fields") or []
    itinerary = item.get("itinerary") or []
    inclusions = item.get("inclusions") or []
    exclusions = item.get("exclusions") or []
    images = item.get("images") or []

    if not source.get("url"):
        reasons.append("missing_source_url")
    if not item.get("price_adult") or float(item["price_adult"]) <= 0:
        reasons.append("missing_price")
    elif price_is_suspicious(float(item["price_adult"]), duration):
        reasons.append("suspicious_price")
    if not item.get("price_raw"):
        reasons.append("missing_original_price_text")
    if any(field.get("field") in {"price_adult", "duration"} for field in inferred_fields):
        reasons.append("inferred_core_field")
    if not duration:
        reasons.append("missing_duration")
    elif duration_is_suspicious(name, duration, len(itinerary)):
        reasons.append("suspicious_duration")
    itinerary_text_length = sum(len(str(value).strip()) for value in itinerary)
    if len(itinerary) < 3 and itinerary_text_length < 350:
        reasons.append("incomplete_itinerary")
    if len(inclusions) < 2:
        reasons.append("incomplete_inclusions")
    if len(exclusions) < 1:
        reasons.append("incomplete_exclusions")
    if len(images) < 2:
        reasons.append("insufficient_images")
    if images and not image_likely_matches(images, name):
        reasons.append("irrelevant_images")
    if not item.get("meeting_point"):
        warnings.append("missing_meeting_point")

    if not reasons:
        readiness = "ready_for_manual_publish"
    elif source.get("url"):
        readiness = "needs_recrawl"
    else:
        readiness = "rejected"

    return {
        "publish_readiness": readiness,
        "blocking_reasons": reasons,
        "warnings": warnings,
        "name": name,
        "slug": item.get("slug"),
        "source_name": source.get("name"),
        "source_url": source.get("url"),
        "price_adult": item.get("price_adult"),
        "price_raw": item.get("price_raw"),
        "duration": duration,
        "itinerary_count": len(itinerary),
        "inclusions_count": len(inclusions),
        "exclusions_count": len(exclusions),
        "image_count": len(images),
        "thumbnail": item.get("thumbnail"),
    }


def duration_is_suspicious(name: str, duration: str, itinerary_count: int) -> bool:
    normalized_name = name.lower()
    normalized_duration = duration.lower()

    day_named = any(word in normalized_name for word in DAY_ROUTE_WORDS)
    hours = parse_hours(normalized_duration)
    days = parse_days(normalized_duration)

    if day_named and hours is not None and hours < 5:
        return True
    if hours is not None and hours <= 2 and itinerary_count >= 3:
        return True
    if re.search(r"from .+ port", normalized_name) and days is not None and days > 1:
        return True
    if ("afternoon" in normalized_name or "half day" in normalized_name) and days is not None:
        return True
    return False


def price_is_suspicious(price_vnd: float, duration: str) -> bool:
    days = parse_days(duration.lower())
    if days is None:
        return price_vnd > 20_000_000
    if days <= 1:
        return price_vnd > 20_000_000
    return price_vnd > 50_000_000


def parse_hours(value: str) -> float | None:
    match = re.search(r"(\d+(?:\.\d+)?)\s*(?:hour|hours|hr|hrs|gio|giờ)", value)
    return float(match.group(1)) if match else None


def parse_days(value: str) -> float | None:
    match = re.search(r"(\d+(?:\.\d+)?)\s*(?:day|days|ngay|ngày)", value)
    return float(match.group(1)) if match else None


def image_likely_matches(images: list[Any], name: str) -> bool:
    tokens = {
        token
        for token in re.findall(r"[a-z0-9]+", name.lower())
        if len(token) >= 3
        and token
        not in {
            "tour",
            "from",
            "with",
            "good",
            "price",
            "daily",
            "day",
            "trip",
            "best",
            "book",
            "now",
        }
    }
    if not tokens:
        return False

    urls = " ".join(
        (
            f"{image.get('url', '')} {image.get('alt', '')}"
            if isinstance(image, dict)
            else str(image)
        ).lower()
        for image in images
    )
    return any(token in urls for token in tokens)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames = [
        "publish_readiness",
        "blocking_reasons",
        "warnings",
        "name",
        "slug",
        "source_name",
        "source_url",
        "price_adult",
        "price_raw",
        "duration",
        "itinerary_count",
        "inclusions_count",
        "exclusions_count",
        "image_count",
        "thumbnail",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            output = dict(row)
            output["blocking_reasons"] = "; ".join(output["blocking_reasons"])
            output["warnings"] = "; ".join(output["warnings"])
            writer.writerow(output)


def load_json(path: Path) -> list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
