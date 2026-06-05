import argparse
import csv
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB_EXPORT = ROOT.parent / "data-center" / "media-assets" / "db-active-missing-thumbnail-locations.json"
DEFAULT_OUTPUT = ROOT.parent / "data-center" / "media-assets" / "cloudinary-staging" / "locations" / "2026-06-04-active-missing-thumbnail"
DEFAULT_PEXELS_URL = "https://api.pexels.com/v1/search"


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


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


def category_query(row: dict[str, Any]) -> str:
    slug = str(row.get("category_slug") or "").lower()
    name = str(row.get("category_name") or "").lower()
    haystack = f"{slug} {name}"
    if any(token in haystack for token in ["hotel", "stay", "homestay", "accommodation"]):
        return "Da Nang hotel"
    if any(token in haystack for token in ["restaurant", "food", "cafe", "coffee", "eat"]):
        return "Vietnamese food restaurant Da Nang"
    if any(token in haystack for token in ["beach", "nature", "park", "attraction", "sight"]):
        return "Da Nang travel landmark"
    if any(token in haystack for token in ["temple", "pagoda", "culture", "museum"]):
        return "Da Nang Vietnam cultural landmark"
    return "Da Nang Vietnam travel"


def search_queries(row: dict[str, Any]) -> list[str]:
    name = str(row.get("name") or "")
    category = category_query(row)
    queries = [
        f"{name} Da Nang",
        f"{name} Vietnam",
        category,
    ]
    compact: list[str] = []
    for query in queries:
        query = re.sub(r"\s+", " ", query).strip()
        if query and query not in compact:
            compact.append(query)
    return compact


def pexels_search(query: str, api_key: str, api_url: str, timeout: int) -> dict[str, Any]:
    params = urllib.parse.urlencode({"query": query, "per_page": 1, "orientation": "landscape"})
    req = urllib.request.Request(
        f"{api_url}?{params}",
        headers={
            "Authorization": api_key,
            "User-Agent": "DanangTripMediaStaging/0.1 contact:admin@danangtrip.local",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def download_file(url: str, target: Path, timeout: int) -> tuple[bool, str]:
    target.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "DanangTripMediaStaging/0.1 contact:admin@danangtrip.local"},
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
    (output_dir / "manifest.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    fieldnames = sorted({key for row in rows for key in row.keys()})
    with (output_dir / "manifest.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db-export", type=Path, default=DEFAULT_DB_EXPORT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--download", action="store_true")
    parser.add_argument("--delay-ms", type=int, default=750)
    parser.add_argument("--timeout", type=int, default=30)
    args = parser.parse_args()

    load_dotenv(ROOT / ".env")
    api_key = os.environ.get("PEXELS_API_KEY", "")
    api_url = os.environ.get("PEXELS_API_URL", DEFAULT_PEXELS_URL)
    if not api_key:
        raise SystemExit("Missing PEXELS_API_KEY")

    db_rows = load_json(args.db_export)
    if args.limit > 0:
        db_rows = db_rows[: args.limit]

    manifest: list[dict[str, Any]] = []
    originals_dir = args.output / "originals"

    for row in db_rows:
        location_id = str(row.get("id"))
        slug = ascii_slug(str(row.get("slug") or row.get("name") or "location"))
        selected: dict[str, Any] | None = None
        selected_query = ""
        error = ""

        for query in search_queries(row):
            try:
                result = pexels_search(query, api_key, api_url, args.timeout)
                photos = result.get("photos") or []
                if photos:
                    selected = photos[0]
                    selected_query = query
                    break
            except Exception as exc:  # Keep manifest evidence for retry/review.
                error = f"{type(exc).__name__}:{exc}"
            time.sleep(max(args.delay_ms, 0) / 1000)

        if not selected:
            manifest.append({
                **row,
                "location_id": location_id,
                "location_slug": slug,
                "search_status": "missing_image_candidate",
                "search_error": error,
            })
            continue

        image_url = selected.get("src", {}).get("large2x") or selected.get("src", {}).get("large") or selected.get("src", {}).get("original")
        photo_url = selected.get("url") or ""
        photo_id = str(selected.get("id") or pexels_photo_id(photo_url) or "unknown")
        local_file = f"loc-{location_id}__{slug}__active-missing-thumbnail__p01__pexels-{photo_id}.jpg"
        local_path = originals_dir / local_file
        status = "pending_download"
        download_message = ""

        if args.download:
            if local_path.exists() and local_path.stat().st_size > 0:
                status = "already_downloaded"
                download_message = f"existing:{local_path.stat().st_size}"
            else:
                ok, download_message = download_file(str(image_url), local_path, args.timeout)
                status = "downloaded" if ok else "download_failed"

        manifest.append({
            **row,
            "location_id": location_id,
            "location_slug": slug,
            "search_query": selected_query,
            "provider": "pexels",
            "photo_index": 1,
            "photo_id": photo_id,
            "image_url": image_url,
            "thumbnail_url": selected.get("src", {}).get("medium"),
            "provider_page_url": photo_url,
            "photographer": selected.get("photographer"),
            "photographer_url": selected.get("photographer_url"),
            "local_file": local_file,
            "local_path": str(local_path) if status in {"downloaded", "already_downloaded"} else "",
            "cloudinary_public_id": f"danangtrip/locations/{slug}/loc-{location_id}__{slug}__p01",
            "search_status": "found",
            "status": status,
            "download_message": download_message,
        })

        time.sleep(max(args.delay_ms, 0) / 1000)

    write_manifest(manifest, args.output)
    summary = {
        "db_rows": len(db_rows),
        "manifest_rows": len(manifest),
        "found": sum(1 for row in manifest if row.get("search_status") == "found"),
        "downloaded": sum(1 for row in manifest if row.get("status") in {"downloaded", "already_downloaded"}),
        "missing_candidate": sum(1 for row in manifest if row.get("search_status") == "missing_image_candidate"),
        "download_failed": sum(1 for row in manifest if row.get("status") == "download_failed"),
        "output": str(args.output),
    }
    (args.output / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
