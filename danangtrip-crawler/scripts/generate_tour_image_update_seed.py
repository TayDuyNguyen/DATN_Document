import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESULTS = ROOT.parent / "data-center" / "media-assets" / "cloudinary-staging" / "tours" / "2026-06-04-tour-missing-thumbnail" / "upload-results.csv"
DEFAULT_OUTPUT = ROOT.parent / "database-seeders" / "40_update_tour_images_from_cloudinary_seed.sql"


def sql_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    with args.results.open("r", encoding="utf-8", newline="") as f:
        rows = [row for row in csv.DictReader(f) if row.get("upload_status") == "uploaded" and row.get("secure_url")]

    grouped: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        tour_id = str(row.get("tour_id") or row.get("location_id"))
        url = row["secure_url"]
        if url not in grouped[tour_id]:
            grouped[tour_id].append(url)

    values = []
    for tour_id, urls in sorted(grouped.items(), key=lambda item: int(item[0])):
        values.append(f"        ({int(tour_id)}, {sql_quote(urls[0])}, {sql_quote(json.dumps(urls, ensure_ascii=False))}::json)")

    lines = [
        "-- DanangTrip tour Cloudinary image update",
        "-- FILE: 40_update_tour_images_from_cloudinary_seed.sql",
        "-- Purpose: update tour thumbnail/images from reviewed Cloudinary upload results.",
        "",
        "WITH image_rows(tour_id, thumbnail, images) AS (",
        "    VALUES",
        ",\n".join(values),
        ")",
        "UPDATE tours t",
        "SET thumbnail = image_rows.thumbnail,",
        "    images = image_rows.images,",
        "    updated_at = NOW()",
        "FROM image_rows",
        "WHERE t.id = image_rows.tour_id;",
        "",
    ]
    args.output.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"uploaded_rows": len(rows), "tours": len(grouped), "output": str(args.output)}, indent=2))


if __name__ == "__main__":
    main()
