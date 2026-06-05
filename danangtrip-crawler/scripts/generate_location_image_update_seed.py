import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESULTS = ROOT.parent / "data-center" / "media-assets" / "cloudinary-staging" / "locations" / "2026-06-04-overpass-published-inactive" / "upload-results.csv"
DEFAULT_OUTPUT = ROOT.parent / "database-seeders" / "34_update_location_images_from_cloudinary_seed.sql"


def sql_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--status", default="inactive")
    parser.add_argument("--title", default="DanangTrip Cloudinary Location Image Update Seeder")
    args = parser.parse_args()

    rows = [row for row in read_rows(args.results) if row.get("upload_status") == "uploaded" and row.get("secure_url")]
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["location_id"])].append(row)

    lines: list[str] = [
        f"-- {args.title}",
        f"-- FILE: {args.output.name}",
        "-- Purpose:",
        f"--   Update {args.status} locations with reviewed Cloudinary image URLs.",
        "--   Generated from media asset upload results.",
        "",
        "WITH image_rows(location_id, thumbnail, images) AS (",
        "    VALUES",
    ]

    values: list[str] = []
    for location_id, items in sorted(grouped.items(), key=lambda item: int(item[0])):
        urls: list[str] = []
        seen_urls: set[str] = set()
        for item in sorted(items, key=lambda row: int(row.get("photo_index") or 1)):
            url = item["secure_url"]
            if url in seen_urls:
                continue
            seen_urls.add(url)
            urls.append(url)
        values.append(
            f"        ({int(location_id)}, {sql_quote(urls[0])}, {sql_quote(json.dumps(urls, ensure_ascii=False))}::json)"
        )

    lines.append(",\n".join(values))
    lines.extend([
        ")",
        "UPDATE locations l",
        "SET thumbnail = image_rows.thumbnail,",
        "    images = image_rows.images,",
        "    updated_at = NOW()",
        "FROM image_rows",
        "WHERE l.id = image_rows.location_id",
        f"  AND l.status = {sql_quote(args.status)};",
        "",
    ])

    args.output.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({
        "uploaded_rows": len(rows),
        "locations": len(grouped),
        "output": str(args.output),
    }, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
