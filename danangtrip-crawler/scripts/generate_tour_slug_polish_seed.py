import argparse
import json
import re
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT.parent / "data-center" / "reports" / "generic-tour-slugs-input-2026-06-05.json"
DEFAULT_OUTPUT = ROOT.parent / "database-seeders" / "43_polish_generic_tour_slugs_seed.sql"
DEFAULT_REVIEW = ROOT.parent / "data-center" / "reports" / "generic-tour-slugs-polish-2026-06-05.json"


def sql_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def ascii_slug(value: str) -> str:
    value = unicodedata.normalize("NFD", value)
    value = "".join(char for char in value if unicodedata.category(char) != "Mn")
    value = value.replace("Đ", "D").replace("đ", "d")
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "tour"


def clean_name(name: str) -> str:
    name = re.sub(r"\s+", " ", name).strip()
    replacements = [
        ("Tour Khám Phá Tour ", "Tour Khám Phá "),
        ("Tour Cao Cấp Tour ", "Tour Cao Cấp "),
        ("Tour Tiết Kiệm Tour ", "Tour Tiết Kiệm "),
        ("Tour Khám Phá Tour Khám Phá ", "Tour Khám Phá "),
        ("Tour Khám Phá Street Food Tour ", "Tour Khám Phá Street Food "),
    ]
    for old, new in replacements:
        name = name.replace(old, new)
    return name


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--review", type=Path, default=DEFAULT_REVIEW)
    args = parser.parse_args()

    rows = json.loads(args.input.read_text(encoding="utf-8"))
    used_slugs = {
        "tour-ba-na-hills-1-ngay",
        "tour-hoi-an-rung-dua",
        "tour-ngu-hanh-son-son-tra",
        "tour-cu-lao-cham",
        "tour-hue-1-ngay",
        "tour-my-son",
        "tour-city-danang",
        "tour-hai-van-lang-co",
        "tour-dem-hoi-an",
        "tour-ba-na-night",
        "tour-vinwonders-nam-hoi-an",
        "tour-nui-than-tai",
        "tour-trekking-son-tra",
        "tour-bach-ma",
        "tour-street-food-danang",
        "tour-tra-que-farmer",
        "tour-du-thuyen-song-han",
        "tour-tam-giang-sunset",
        "tour-ca-hue-song-huong",
        "tour-snorkeling-son-tra",
    }

    updates: list[dict[str, str | int]] = []
    for row in rows:
        tour_id = int(row["id"])
        old_name = str(row["name"])
        new_name = clean_name(old_name)
        base_slug = ascii_slug(new_name)
        slug = base_slug
        if slug in used_slugs:
            slug = f"{base_slug}-goi-{tour_id}"
        used_slugs.add(slug)
        updates.append({
            "id": tour_id,
            "old_name": old_name,
            "new_name": new_name,
            "old_slug": str(row["slug"]),
            "new_slug": slug,
        })

    values = [
        f"        ({item['id']}, {sql_quote(str(item['new_name']))}, {sql_quote(str(item['new_slug']))})"
        for item in updates
    ]
    lines = [
        "-- DanangTrip polish generic tour slugs",
        "-- FILE: 43_polish_generic_tour_slugs_seed.sql",
        "-- Purpose: replace tour-real-variant-* slugs and clean repeated Tour wording.",
        "",
        "WITH tour_updates(id, name, slug) AS (",
        "    VALUES",
        ",\n".join(values),
        ")",
        "UPDATE tours t",
        "SET name = tour_updates.name,",
        "    slug = tour_updates.slug,",
        "    updated_at = NOW()",
        "FROM tour_updates",
        "WHERE t.id = tour_updates.id",
        "  AND (t.slug LIKE 'tour-real-variant-%' OR t.name LIKE '%Variant%');",
        "",
    ]
    args.output.write_text("\n".join(lines), encoding="utf-8")
    args.review.write_text(json.dumps(updates, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"updates": len(updates), "output": str(args.output), "review": str(args.review)}, indent=2))


if __name__ == "__main__":
    main()
