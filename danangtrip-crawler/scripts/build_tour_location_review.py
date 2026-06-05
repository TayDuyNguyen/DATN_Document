from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_INPUT = DATA_DIR / "tour-staging-enriched.json"


LOCATION_RULES = (
    {
        "slug": "ba-na-hills",
        "name": "Ba Na Hills",
        "location_id_hint": 23,
        "keywords": ("ba na", "bana", "golden bridge", "cau vang", "french village"),
    },
    {
        "slug": "hoi-an-ancient-town",
        "name": "Hoi An Ancient Town",
        "location_id_hint": 1,
        "keywords": ("hoi an", "hoian", "ancient town", "lantern", "flower lantern", "boat ride"),
    },
    {
        "slug": "bay-mau-coconut-forest",
        "name": "Bay Mau Coconut Forest",
        "location_id_hint": 3,
        "keywords": ("basket boat", "cam thanh", "coconut", "coconut jungle", "coconut forest"),
    },
    {
        "slug": "my-son-sanctuary",
        "name": "My Son Sanctuary",
        "location_id_hint": 8,
        "keywords": ("my son", "holyland", "holy land", "sanctuary"),
    },
    {
        "slug": "cu-lao-cham",
        "name": "Cham Island (Cu Lao Cham)",
        "location_id_hint": 13,
        "keywords": ("cham island", "cu lao cham", "snorkeling"),
    },
    {
        "slug": "marble-mountains",
        "name": "Marble Mountains",
        "location_id_hint": 21,
        "keywords": ("marble mountain", "marble mountains", "am phu cave", "ngu hanh son"),
    },
    {
        "slug": "linh-ung-pagoda",
        "name": "Linh Ung Pagoda",
        "location_id_hint": 20,
        "keywords": ("linh ung", "lady buddha", "monkey mountain", "son tra"),
    },
)

MISSING_LOCATION_RULES = (
    {
        "slug": "bach-ma-national-park",
        "name": "Bach Ma National Park",
        "keywords": ("bach ma", "bạch mã"),
    },
    {
        "slug": "hoa-phu-thanh",
        "name": "Hoa Phu Thanh",
        "keywords": ("hoa phu thanh", "hòa phú thành", "waterfall sliding"),
    },
    {
        "slug": "hue-imperial-city",
        "name": "Hue Imperial City",
        "keywords": ("hue tour", "hue imperial", "imperial", "citadel", "chan may"),
    },
    {
        "slug": "tien-sa-port",
        "name": "Tien Sa Port",
        "keywords": ("tien sa port", "tien sa"),
    },
    {
        "slug": "chan-may-port",
        "name": "Chan May Port",
        "keywords": ("chan may port", "chan may"),
    },
    {
        "slug": "nui-than-tai-hot-spring-park",
        "name": "Nui Than Tai Hot Spring Park",
        "keywords": ("than tai", "hot spring"),
    },
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--output-prefix", default="tour-location-review")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.is_absolute():
        input_path = ROOT / input_path

    tours = json.loads(input_path.read_text(encoding="utf-8"))
    rows = []
    for tour in tours:
        rows.extend(build_rows_for_tour(tour))

    json_output = DATA_DIR / f"{args.output_prefix}.json"
    csv_output = DATA_DIR / f"{args.output_prefix}.csv"
    report_output = DATA_DIR / f"{args.output_prefix}-report.json"

    json_output.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_csv(csv_output, rows)

    report = build_report(input_path, json_output, csv_output, rows, len(tours))
    report_output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=True, indent=2))


def build_rows_for_tour(tour: dict[str, Any]) -> list[dict[str, Any]]:
    text = searchable_text(tour)
    matched = []
    for rule in LOCATION_RULES:
        if any(keyword in text for keyword in rule["keywords"]):
            matched.append(build_row(tour, rule, "existing_seed_location", "medium"))

    for rule in MISSING_LOCATION_RULES:
        if any(keyword in text for keyword in rule["keywords"]):
            matched.append(build_row(tour, rule, "missing_location_seed", "low"))

    if not matched:
        matched.append(
            {
                "tour_slug": tour.get("slug"),
                "tour_name": tour.get("name"),
                "review_status": "pending_review",
                "approve_for_seed": False,
                "location_status": "unmatched",
                "location_id_hint": None,
                "location_slug": "",
                "location_name": "",
                "confidence": "low",
                "mapping_method": "no_keyword_match",
                "fix_notes": "",
                "source_url": (tour.get("source") or {}).get("url"),
            }
        )
    return dedupe_rows(matched)


def build_row(tour: dict[str, Any], rule: dict[str, Any], location_status: str, confidence: str) -> dict[str, Any]:
    return {
        "tour_slug": tour.get("slug"),
        "tour_name": tour.get("name"),
        "review_status": "pending_review",
        "approve_for_seed": False,
        "location_status": location_status,
        "location_id_hint": rule.get("location_id_hint"),
        "location_slug": rule["slug"],
        "location_name": rule["name"],
        "confidence": confidence,
        "mapping_method": "keyword_context_match",
        "fix_notes": "",
        "source_url": (tour.get("source") or {}).get("url"),
    }


def searchable_text(tour: dict[str, Any]) -> str:
    source_url = (tour.get("source") or {}).get("url") or ""
    source_path = urlparse(source_url).path
    parts = [
        tour.get("name") or "",
        tour.get("meeting_point") or "",
        source_path,
    ]
    text = " ".join(parts).lower()
    company_noise = (
        "hoian day trip company",
        "hoian-day-trip-company",
        "hoi an day trip company",
        "hoi-an-day-trip-company",
        "hoiandaytrip",
        "da nang local tours",
        "da-nang-local-tours",
        "danang local tours",
        "danang-local-tours",
        "dacotours",
        "venusvietnamtravel",
        "vmtravel",
        "vietnam adventure tours",
        "vietnam-adventure-tours",
    )
    for value in company_noise:
        text = text.replace(value, " ")
    return " ".join(text.split())


def dedupe_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen = {}
    for row in rows:
        key = (row["tour_slug"], row["location_slug"], row["location_status"])
        seen[key] = row
    return list(seen.values())


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames = [
        "tour_slug",
        "tour_name",
        "review_status",
        "approve_for_seed",
        "location_status",
        "location_id_hint",
        "location_slug",
        "location_name",
        "confidence",
        "mapping_method",
        "fix_notes",
        "source_url",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_report(
    input_path: Path,
    json_output: Path,
    csv_output: Path,
    rows: list[dict[str, Any]],
    tour_count: int,
) -> dict[str, Any]:
    return {
        "input": str(input_path.relative_to(ROOT)).replace("\\", "/"),
        "outputs": {
            "json": str(json_output.relative_to(ROOT)).replace("\\", "/"),
            "csv": str(csv_output.relative_to(ROOT)).replace("\\", "/"),
        },
        "tourCount": tour_count,
        "mappingRows": len(rows),
        "existingSeedLocationRows": sum(1 for row in rows if row["location_status"] == "existing_seed_location"),
        "missingLocationSeedRows": sum(1 for row in rows if row["location_status"] == "missing_location_seed"),
        "unmatchedRows": sum(1 for row in rows if row["location_status"] == "unmatched"),
        "approvedForSeed": sum(1 for row in rows if row["approve_for_seed"]),
        "policy": {
            "approveForSeedDefault": False,
            "manualReviewRequired": True,
            "doesNotPublishDb": True,
        },
    }


if __name__ == "__main__":
    main()
