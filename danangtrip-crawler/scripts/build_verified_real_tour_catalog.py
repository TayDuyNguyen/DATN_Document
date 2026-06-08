from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUTPUT = DATA_DIR / "verified-real-tour-catalog-20260607.json"
REPORT = DATA_DIR / "verified-real-tour-catalog-20260607-report.json"

SOURCES = (
    (
        DATA_DIR / "vmtravel-central-price-v3-enriched-20260607.json",
        DATA_DIR / "vmtravel-central-final-readiness-20260607.json",
        "source_images_verified_by_parser",
    ),
    (
        DATA_DIR / "vmtravel-old-ready-price-recheck-enriched-20260607.json",
        DATA_DIR / "vmtravel-old-ready-price-recheck-readiness-20260607.json",
        "source_images_verified_by_parser",
    ),
)

MANUALLY_APPROVED_PEXELS_URLS = {
    "https://venusvietnamtravel.com/afternoon-ba-na-hills-golden-bridge-dragon-bridge-by-night-tour",
    "https://venusvietnamtravel.com/cham-island-sightseeing-and-snorkeling-tour",
}


def main() -> None:
    catalog: dict[str, dict[str, Any]] = {}

    for data_path, gate_path, image_policy in SOURCES:
        items = load_items_by_url(data_path)
        gate = load_gate_by_url(gate_path)
        for source_url, decision in gate.items():
            if decision.get("publish_readiness") != "ready_for_manual_publish":
                continue
            item = items[source_url]
            catalog[source_url] = verified_item(item, image_policy)

    pexels_items = load_items_by_url(
        DATA_DIR / "venus-tour-pexels-enriched-20260607.json"
    )
    pexels_gate = load_gate_by_url(
        DATA_DIR / "venus-tour-pexels-readiness-20260607.json"
    )
    for source_url in MANUALLY_APPROVED_PEXELS_URLS:
        decision = pexels_gate.get(source_url) or {}
        if decision.get("publish_readiness") != "ready_for_manual_publish":
            raise SystemExit(f"Pexels tour did not pass gate: {source_url}")
        catalog[source_url] = verified_item(
            pexels_items[source_url],
            "source_primary_plus_pexels_visually_reviewed",
        )

    rows = sorted(catalog.values(), key=lambda item: item["name"])
    validate(rows)
    OUTPUT.write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    report = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "output": str(OUTPUT.relative_to(ROOT)).replace("\\", "/"),
        "total": len(rows),
        "uniqueSourceUrls": len({item["source"]["url"] for item in rows}),
        "directPrice": sum(
            1
            for item in rows
            if item.get("price_raw")
            and not str(item["price_raw"]).startswith("estimated_from_context:")
        ),
        "directDuration": sum(
            1
            for item in rows
            if not any(
                field.get("field") == "duration"
                for field in item.get("inferred_fields") or []
            )
        ),
        "withItinerary": sum(1 for item in rows if item.get("itinerary")),
        "withInclusions": sum(1 for item in rows if item.get("inclusions")),
        "withExclusions": sum(1 for item in rows if item.get("exclusions")),
        "withAtLeastTwoImages": sum(
            1 for item in rows if len(item.get("images") or []) >= 2
        ),
        "imagePolicy": count_by(
            rows,
            lambda item: item["verification"]["imagePolicy"],
        ),
        "databaseWritten": False,
        "status": "verified_staging",
    }
    REPORT.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2))


def load_items_by_url(path: Path) -> dict[str, dict[str, Any]]:
    return {
        canonical_url(str((item.get("source") or {}).get("url") or "")): item
        for item in json.loads(path.read_text(encoding="utf-8"))
        if (item.get("source") or {}).get("url")
    }


def load_gate_by_url(path: Path) -> dict[str, dict[str, Any]]:
    return {
        canonical_url(str(item.get("source_url") or "")): item
        for item in json.loads(path.read_text(encoding="utf-8"))
        if item.get("source_url")
    }


def verified_item(item: dict[str, Any], image_policy: str) -> dict[str, Any]:
    output = dict(item)
    output["verification"] = {
        "status": "verified_staging",
        "verifiedAt": datetime.now(timezone.utc).isoformat(),
        "qualityGate": "strict_tour_publish_readiness_v3",
        "sourceFacts": "direct_not_inferred",
        "imagePolicy": image_policy,
        "databaseWritten": False,
    }
    return output


def validate(rows: list[dict[str, Any]]) -> None:
    if len(rows) != 30:
        raise SystemExit(f"Expected 30 verified tours, got {len(rows)}")
    urls = [canonical_url(item["source"]["url"]) for item in rows]
    if len(urls) != len(set(urls)):
        raise SystemExit("Duplicate source URLs in verified catalog")
    inferred_core = [
        item["name"]
        for item in rows
        if any(
            field.get("field") in {"price_adult", "duration"}
            for field in item.get("inferred_fields") or []
        )
    ]
    if inferred_core:
        raise SystemExit(f"Inferred core fields remain: {inferred_core}")


def canonical_url(url: str) -> str:
    return url.split("#", 1)[0].split("?", 1)[0].rstrip("/").lower()


def count_by(
    rows: list[dict[str, Any]],
    key_fn: Any,
) -> dict[str, int]:
    result: dict[str, int] = {}
    for row in rows:
        key = str(key_fn(row))
        result[key] = result.get(key, 0) + 1
    return dict(sorted(result.items()))


if __name__ == "__main__":
    main()
