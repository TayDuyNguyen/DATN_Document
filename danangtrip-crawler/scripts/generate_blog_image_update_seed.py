import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESULTS = ROOT.parent / "data-center" / "media-assets" / "cloudinary-staging" / "blogs" / "2026-06-05-blog-missing-featured-image" / "upload-results.csv"
DEFAULT_OUTPUT = ROOT.parent / "database-seeders" / "41_update_blog_featured_images_from_cloudinary_seed.sql"


def sql_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    with args.results.open("r", encoding="utf-8", newline="") as f:
        rows = [row for row in csv.DictReader(f) if row.get("upload_status") == "uploaded" and row.get("secure_url")]

    by_id: dict[str, str] = {}
    for row in rows:
        blog_id = str(row.get("blog_id") or row.get("location_id"))
        by_id[blog_id] = row["secure_url"]

    values = [
        f"        ({int(blog_id)}, {sql_quote(url)})"
        for blog_id, url in sorted(by_id.items(), key=lambda item: int(item[0]))
    ]

    lines = [
        "-- DanangTrip blog Cloudinary featured image update",
        "-- FILE: 41_update_blog_featured_images_from_cloudinary_seed.sql",
        "-- Purpose: update published blog_posts.featured_image from reviewed Cloudinary upload results.",
        "",
        "WITH image_rows(blog_id, featured_image) AS (",
        "    VALUES",
        ",\n".join(values),
        ")",
        "UPDATE blog_posts b",
        "SET featured_image = image_rows.featured_image,",
        "    updated_at = NOW()",
        "FROM image_rows",
        "WHERE b.id = image_rows.blog_id",
        "  AND b.status = 'published'",
        "  AND (b.featured_image IS NULL OR b.featured_image = '');",
        "",
    ]
    args.output.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"uploaded_rows": len(rows), "blog_posts": len(by_id), "output": str(args.output)}, indent=2))


if __name__ == "__main__":
    main()
