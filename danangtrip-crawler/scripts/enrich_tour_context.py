from __future__ import annotations

import argparse
import json
import statistics
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_INPUT = DATA_DIR / "tour-staging.json"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--output-prefix", default="tour-staging-enriched")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.is_absolute():
        input_path = ROOT / input_path

    items = json.loads(input_path.read_text(encoding="utf-8"))
    enriched = enrich_items(items)

    output = DATA_DIR / f"{args.output_prefix}.json"
    report_output = DATA_DIR / f"{args.output_prefix}-report.json"
    output.write_text(json.dumps(enriched, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    report = build_report(input_path, output, enriched)
    report_output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=True, indent=2))


def enrich_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    price_reference = build_price_reference(items)
    result = []
    for item in items:
        enriched = dict(item)
        enriched["inferred_fields"] = []
        enriched["enrichment"] = {
            "status": "review_required",
            "generatedAt": datetime.now(timezone.utc).isoformat(),
            "policy": "Only fill missing fields with conservative context estimates. Crawled values are never overwritten.",
        }

        if not enriched.get("price_adult"):
            estimate = infer_price(enriched, price_reference)
            if estimate:
                enriched["price_adult"] = estimate["value"]
                enriched["price_raw"] = estimate["raw"]
                add_inferred_field(enriched, "price_adult", estimate)

        if not enriched.get("duration"):
            estimate = infer_duration(enriched)
            if estimate:
                enriched["duration"] = estimate["value"]
                add_inferred_field(enriched, "duration", estimate)

        result.append(enriched)
    return result


def build_price_reference(items: list[dict[str, Any]]) -> dict[str, list[float]]:
    reference: dict[str, list[float]] = {}
    for item in items:
        price = float(item.get("price_adult") or 0)
        if price <= 0:
            continue
        keys = price_keys(item)
        for key in keys:
            reference.setdefault(key, []).append(price)
    return reference


def infer_price(item: dict[str, Any], reference: dict[str, list[float]]) -> dict[str, Any] | None:
    for key in price_keys(item):
        prices = reference.get(key) or []
        if len(prices) >= 2:
            value = round_to_vnd(statistics.median(prices))
            return {
                "value": value,
                "raw": f"estimated_from_context:{int(value)} VND",
                "confidence": "medium",
                "method": "median_similar_category_source_or_route",
                "basis": key,
            }

    fallback = fallback_price_by_name(item)
    if fallback:
        return fallback
    return None


def price_keys(item: dict[str, Any]) -> list[str]:
    name = f"{item.get('name') or ''} {item.get('slug') or ''}".lower()
    category = item.get("tour_category_slug") or "unknown"
    source = (item.get("source") or {}).get("name") or "unknown"
    keys = []
    if "ba na" in name or "bana" in name or "golden bridge" in name:
        keys.extend([f"route:ba-na:{source}", "route:ba-na"])
    if "hoi an" in name or "hoian" in name or "basket boat" in name or "cam thanh" in name:
        keys.extend([f"route:hoi-an:{source}", "route:hoi-an"])
    if "my son" in name:
        keys.extend([f"route:my-son:{source}", "route:my-son"])
    if "cham island" in name or "cu lao cham" in name:
        keys.extend([f"route:cham-island:{source}", "route:cham-island"])
    if "hue" in name:
        keys.extend([f"route:hue:{source}", "route:hue"])
    keys.extend([f"category:{category}:{source}", f"category:{category}"])
    return keys


def fallback_price_by_name(item: dict[str, Any]) -> dict[str, Any] | None:
    name = f"{item.get('name') or ''} {item.get('slug') or ''}".lower()
    fallbacks = [
        (("hoa phu thanh", "waterfall"), 1200000, "low", "fallback_named_route_hoa_phu_thanh"),
        (("bach ma",), 1450000, "low", "fallback_named_route_bach_ma"),
        (("son tra", "marble", "hoi an"), 975000, "low", "fallback_named_route_son_tra_marble_hoi_an"),
        (("cam thanh", "coconut"), 1075000, "low", "fallback_named_route_cam_thanh"),
    ]
    for keywords, value, confidence, method in fallbacks:
        if all(keyword in name for keyword in keywords):
            return {
                "value": value,
                "raw": f"estimated_from_context:{value} VND",
                "confidence": confidence,
                "method": method,
                "basis": "name_keywords",
            }
    return None


def infer_duration(item: dict[str, Any]) -> dict[str, Any] | None:
    name = f"{item.get('name') or ''} {item.get('slug') or ''}".lower()
    if "hoa phu thanh" in name or "daily tour" in name:
        return {
            "value": "1 day",
            "confidence": "low",
            "method": "fallback_named_route_or_daily_tour",
            "basis": "name_keywords",
        }
    return None


def add_inferred_field(item: dict[str, Any], field: str, estimate: dict[str, Any]) -> None:
    item["inferred_fields"].append(
        {
            "field": field,
            "value": estimate["value"],
            "confidence": estimate["confidence"],
            "method": estimate["method"],
            "basis": estimate["basis"],
            "requires_manual_review": True,
        }
    )


def round_to_vnd(value: float) -> float:
    return float(round(value / 25000) * 25000)


def build_report(input_path: Path, output: Path, items: list[dict[str, Any]]) -> dict[str, Any]:
    inferred_items = [item for item in items if item.get("inferred_fields")]
    return {
        "input": str(input_path.relative_to(ROOT)).replace("\\", "/"),
        "output": str(output.relative_to(ROOT)).replace("\\", "/"),
        "total": len(items),
        "itemsWithInferredFields": len(inferred_items),
        "inferredFieldCount": sum(len(item.get("inferred_fields") or []) for item in inferred_items),
        "missingPriceAfter": sum(1 for item in items if not item.get("price_adult")),
        "missingDurationAfter": sum(1 for item in items if not item.get("duration")),
        "policy": {
            "crawledValuesOverwritten": False,
            "manualReviewRequired": True,
            "safeForDirectProductionSeed": False,
        },
    }


if __name__ == "__main__":
    main()
