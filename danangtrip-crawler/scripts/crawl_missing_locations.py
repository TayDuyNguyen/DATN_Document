from __future__ import annotations

import argparse
import csv
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import httpx


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_SOURCE = DATA_DIR / "missing_location_sources.json"
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
USER_AGENT = os.getenv("CRAWLER_USER_AGENT", "DanangTripCrawler/0.1 contact:admin@danangtrip.local")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", default=str(DEFAULT_SOURCE))
    parser.add_argument("--output-prefix", default="missing-locations")
    parser.add_argument("--delay-ms", type=int, default=1200)
    args = parser.parse_args()

    source_path = Path(args.source_file)
    if not source_path.is_absolute():
        source_path = ROOT / source_path

    payload = json.loads(source_path.read_text(encoding="utf-8"))
    locations = payload["locations"]

    crawled = []
    with httpx.Client(
        headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
        follow_redirects=True,
        timeout=25,
    ) as client:
        for location in locations:
            crawled.append(crawl_location(client, location))
            time.sleep(args.delay_ms / 1000)

    review = [build_review_item(item) for item in crawled]

    crawl_output = DATA_DIR / f"{args.output_prefix}-crawl.json"
    review_json = DATA_DIR / f"{args.output_prefix}-review.json"
    review_csv = DATA_DIR / f"{args.output_prefix}-review.csv"
    report_output = DATA_DIR / f"{args.output_prefix}-report.json"

    crawl_output.write_text(json.dumps(crawled, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    review_json.write_text(json.dumps(review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_csv(review_csv, review)

    report = build_report(source_path, crawl_output, review_json, review_csv, review)
    report_output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=True, indent=2))


def crawl_location(client: httpx.Client, location: dict[str, Any]) -> dict[str, Any]:
    attempts = []
    for query in location["queries"]:
        try:
            response = client.get(
                NOMINATIM_URL,
                params={
                    "q": query,
                    "format": "jsonv2",
                    "addressdetails": 1,
                    "limit": 3,
                    "accept-language": "en,vi",
                },
            )
            response.raise_for_status()
            results = response.json()
            attempts.append({"query": query, "resultCount": len(results)})
            best = select_best_result(results)
            if best:
                return normalize_nominatim(location, best, attempts)
        except Exception as exc:  # noqa: BLE001 - crawler should continue.
            attempts.append({"query": query, "error": str(exc)})

    return normalize_fallback(location, attempts)


def select_best_result(results: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not results:
        return None
    preferred_classes = {"tourism", "historic", "leisure", "amenity", "harbour", "natural", "boundary"}
    for result in results:
        if result.get("class") in preferred_classes:
            return result
    return results[0]


def normalize_nominatim(location: dict[str, Any], result: dict[str, Any], attempts: list[dict[str, Any]]) -> dict[str, Any]:
    address = result.get("address") or {}
    display_name = result.get("display_name") or location["name"]
    district = (
        address.get("city")
        or address.get("town")
        or address.get("county")
        or address.get("district")
        or address.get("suburb")
        or ""
    )
    ward = address.get("quarter") or address.get("suburb") or address.get("village") or address.get("hamlet")
    return {
        "name": location["name"],
        "slug": location["slug"],
        "source_type": "nominatim",
        "source_references": ["OpenStreetMap contributors", "Nominatim"],
        "reference_urls": location.get("reference_urls") or [],
        "source_payload": {
            "osm_type": result.get("osm_type"),
            "osm_id": result.get("osm_id"),
            "class": result.get("class"),
            "type": result.get("type"),
            "importance": result.get("importance"),
            "display_name": display_name,
        },
        "address": display_name[:255],
        "district": clean_admin_name(district),
        "ward": clean_admin_name(ward),
        "latitude": round(float(result["lat"]), 8),
        "longitude": round(float(result["lon"]), 8),
        "short_description": build_short_description(location["name"], display_name),
        "description": build_description(location["name"], display_name, "OpenStreetMap/Nominatim"),
        "status": "pending_review",
        "is_featured": False,
        "category_slug": "dia-diem-tham-quan",
        "review_flags": review_flags_for_result(result, display_name),
        "crawl_attempts": attempts,
        "crawled_at": now_iso(),
    }


def normalize_fallback(location: dict[str, Any], attempts: list[dict[str, Any]]) -> dict[str, Any]:
    fallback = location["fallback"]
    return {
        "name": location["name"],
        "slug": location["slug"],
        "source_type": "curated_fallback",
        "source_references": ["Configured fallback context"],
        "reference_urls": location.get("reference_urls") or [],
        "source_payload": None,
        "address": fallback["address"],
        "district": fallback.get("district") or "",
        "ward": fallback.get("ward"),
        "latitude": fallback["latitude"],
        "longitude": fallback["longitude"],
        "short_description": build_short_description(location["name"], fallback["address"]),
        "description": build_description(location["name"], fallback["address"], "configured fallback context"),
        "status": "pending_review",
        "is_featured": False,
        "category_slug": "dia-diem-tham-quan",
        "review_flags": ["used_curated_fallback", "manual_coordinate_review_required"],
        "crawl_attempts": attempts,
        "crawled_at": now_iso(),
    }


def build_review_item(item: dict[str, Any]) -> dict[str, Any]:
    flags = list(item.get("review_flags") or [])
    if not item.get("latitude") or not item.get("longitude"):
        flags.append("missing_coordinates")
    if not item.get("district"):
        flags.append("missing_district")
    return {
        "location_slug": item["slug"],
        "location_name": item["name"],
        "review_status": "pending_review",
        "approve_for_location_seed": False,
        "reject_reason": "",
        "fix_notes": "",
        "category_slug": item["category_slug"],
        "address": item["address"],
        "district": item["district"],
        "ward": item.get("ward"),
        "latitude": item["latitude"],
        "longitude": item["longitude"],
        "short_description": item["short_description"],
        "description": item["description"],
        "source_type": item["source_type"],
        "source_references": "; ".join(item["source_references"]),
        "reference_urls": "; ".join(item.get("reference_urls") or []),
        "review_flags": flags,
    }


def review_flags_for_result(result: dict[str, Any], display_name: str) -> list[str]:
    flags = []
    if result.get("importance") is not None and float(result["importance"]) < 0.2:
        flags.append("low_nominatim_importance")
    if "Vietnam" not in display_name and "Việt Nam" not in display_name:
        flags.append("country_not_explicit_in_display_name")
    return flags


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames = [
        "location_slug",
        "location_name",
        "review_status",
        "approve_for_location_seed",
        "reject_reason",
        "fix_notes",
        "category_slug",
        "address",
        "district",
        "ward",
        "latitude",
        "longitude",
        "short_description",
        "description",
        "source_type",
        "source_references",
        "reference_urls",
        "review_flags",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            value = dict(row)
            value["review_flags"] = "; ".join(value["review_flags"])
            writer.writerow(value)


def build_report(
    source_path: Path,
    crawl_output: Path,
    review_json: Path,
    review_csv: Path,
    rows: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "source": str(source_path.relative_to(ROOT)).replace("\\", "/"),
        "outputs": {
            "crawl": str(crawl_output.relative_to(ROOT)).replace("\\", "/"),
            "reviewJson": str(review_json.relative_to(ROOT)).replace("\\", "/"),
            "reviewCsv": str(review_csv.relative_to(ROOT)).replace("\\", "/"),
        },
        "total": len(rows),
        "fromNominatim": sum(1 for row in rows if row["source_type"] == "nominatim"),
        "fromFallback": sum(1 for row in rows if row["source_type"] == "curated_fallback"),
        "pendingReview": sum(1 for row in rows if row["review_status"] == "pending_review"),
        "approvedForLocationSeed": sum(1 for row in rows if row["approve_for_location_seed"]),
        "withCoordinates": sum(1 for row in rows if row["latitude"] and row["longitude"]),
        "policy": {
            "imagesCollected": False,
            "manualReviewRequired": True,
            "doesNotPublishDb": True,
        },
    }


def build_short_description(name: str, address: str) -> str:
    return f"{name} la dia diem lien quan den hanh trinh tour DanangTrip, can admin duyet thong tin truoc khi seed."


def build_description(name: str, address: str, source: str) -> str:
    return (
        f"{name} duoc thu thap tu {source} voi dia chi tham chieu: {address}. "
        "Ban ghi dang o trang thai pending_review va can kiem tra lai toa do, dia chi, danh muc truoc khi dua vao database."
    )


def clean_admin_name(value: Any) -> str:
    return str(value or "").replace("District", "").replace("district", "").strip()[:50]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


if __name__ == "__main__":
    main()
