import argparse
import csv
import json
import re
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_DB_EXPORT = ROOT.parent / "data-center" / "media-assets" / "db-published-locations.json"
DEFAULT_ENRICHED = DATA_DIR / "overpass-danang-pois-enriched.json"
DEFAULT_OUTPUT = ROOT.parent / "data-center" / "media-assets" / "cloudinary-staging" / "locations" / "2026-06-04-overpass-published-inactive"


def ascii_slug(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "unnamed"


def pexels_photo_id(url: str) -> str:
    match = re.search(r"/photos/(\d+)/", url)
    if match:
        return match.group(1)
    match = re.search(r"pexels-photo-(\d+)", url)
    if match:
        return match.group(1)
    return "unknown"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def candidate_rows(db_rows: list[dict[str, Any]], enriched_rows: list[dict[str, Any]], photos_per_location: int) -> list[dict[str, Any]]:
    by_external_id = {row.get("externalId"): row for row in enriched_rows}
    rows: list[dict[str, Any]] = []

    for db in db_rows:
        external_id = db.get("external_id") or db.get("externalId")
        enriched = by_external_id.get(external_id)
        if not enriched:
            rows.append({
                "location_id": db.get("id"),
                "location_slug": db.get("slug"),
                "location_name": db.get("name"),
                "external_id": external_id,
                "status": "missing_enriched_candidate",
            })
            continue

        normalized = enriched.get("normalizedPayload") or {}
        raw = enriched.get("rawPayload") or {}
        candidates = raw.get("imageCandidates") or normalized.get("imageCandidates") or []
        if not candidates:
            image_urls = normalized.get("imageUrls") or []
            candidates = [{"url": url, "provider": "pexels"} for url in image_urls]

        if not candidates:
            rows.append({
                "location_id": db.get("id"),
                "location_slug": db.get("slug"),
                "location_name": db.get("name"),
                "external_id": external_id,
                "status": "missing_image_candidate",
            })
            continue

        for index, candidate in enumerate(candidates[:photos_per_location], start=1):
            url = candidate.get("url") or candidate.get("imageUrl")
            if not url:
                continue
            location_id = str(db.get("id"))
            slug = ascii_slug(str(db.get("slug") or normalized.get("slugCandidate") or db.get("name") or "location"))
            photo_id = pexels_photo_id(url)
            file_name = f"loc-{location_id}__{slug}__{external_id}__p{index:02d}__pexels-{photo_id}.jpg"
            cloudinary_public_id = f"danangtrip/locations/{slug}/loc-{location_id}__{slug}__p{index:02d}"
            rows.append({
                "location_id": location_id,
                "location_slug": slug,
                "location_name": db.get("name") or normalized.get("name"),
                "location_status": db.get("status"),
                "category_slug": db.get("category_slug") or normalized.get("categorySlug"),
                "external_id": external_id,
                "source_url": db.get("source_url") or enriched.get("sourceUrl"),
                "provider": candidate.get("provider") or "pexels",
                "photo_index": index,
                "photo_id": photo_id,
                "image_url": url,
                "thumbnail_url": candidate.get("thumbnailUrl"),
                "provider_page_url": candidate.get("pageUrl"),
                "photographer": candidate.get("photographer"),
                "photographer_url": candidate.get("photographerUrl"),
                "local_file": file_name,
                "cloudinary_public_id": cloudinary_public_id,
                "status": "pending_download",
            })

    return rows


def download_file(url: str, target: Path, timeout: int) -> tuple[bool, str]:
    target.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "DanangTripMediaStaging/0.1 contact:admin@danangtrip.local",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            content_type = response.headers.get("Content-Type", "")
            data = response.read()
        if not data:
            return False, "empty_response"
        if "image" not in content_type.lower():
            return False, f"unexpected_content_type:{content_type}"
        target.write_bytes(data)
        return True, f"downloaded:{len(data)}"
    except (urllib.error.URLError, TimeoutError) as exc:
        return False, f"download_error:{exc}"


def write_manifest(rows: list[dict[str, Any]], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "manifest.json"
    csv_path = output_dir / "manifest.csv"
    json_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    fieldnames = sorted({key for row in rows for key in row.keys()})
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db-export", type=Path, default=DEFAULT_DB_EXPORT)
    parser.add_argument("--enriched", type=Path, default=DEFAULT_ENRICHED)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--photos-per-location", type=int, default=1)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--download", action="store_true")
    parser.add_argument("--delay-ms", type=int, default=250)
    parser.add_argument("--timeout", type=int, default=30)
    args = parser.parse_args()

    db_rows = load_json(args.db_export)
    enriched_rows = load_json(args.enriched)
    if args.limit > 0:
        db_rows = db_rows[: args.limit]

    rows = candidate_rows(db_rows, enriched_rows, args.photos_per_location)
    originals_dir = args.output / "originals"

    if args.download:
        for row in rows:
            if row.get("status") != "pending_download":
                continue
            target = originals_dir / str(row["local_file"])
            if target.exists() and target.stat().st_size > 0:
                row["status"] = "already_downloaded"
                row["local_path"] = str(target)
                continue
            ok, message = download_file(str(row["image_url"]), target, args.timeout)
            row["status"] = "downloaded" if ok else "download_failed"
            row["download_message"] = message
            row["local_path"] = str(target) if ok else ""
            time.sleep(max(args.delay_ms, 0) / 1000)

    write_manifest(rows, args.output)

    summary = {
        "db_rows": len(db_rows),
        "manifest_rows": len(rows),
        "downloaded": sum(1 for row in rows if row.get("status") in {"downloaded", "already_downloaded"}),
        "missing_candidate": sum(1 for row in rows if str(row.get("status", "")).startswith("missing_")),
        "download_failed": sum(1 for row in rows if row.get("status") == "download_failed"),
        "output": str(args.output),
    }
    (args.output / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
