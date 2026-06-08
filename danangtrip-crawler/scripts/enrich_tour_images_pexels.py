from __future__ import annotations

import argparse
import json
import os
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_API_URL = "https://api.pexels.com/v1/search"
QUERY_BY_URL = {
    "https://venusvietnamtravel.com/hoi-an-boat-ride/": "Hoi An lantern river Vietnam",
    "https://venusvietnamtravel.com/3-traditional-handicraft-villages-in-1-tour/": "Hoi An pottery village Vietnam",
    "https://venusvietnamtravel.com/afternoon-ba-na-hills-golden-bridge-dragon-bridge-by-night-tour/": "Ba Na Hills Golden Bridge Da Nang Vietnam",
    "https://venusvietnamtravel.com/cham-island-sightseeing-and-snorkeling-tour/": "Cham Island Vietnam snorkeling",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-prefix", default="tour-pexels-enriched")
    parser.add_argument("--photos-per-tour", type=int, default=3)
    parser.add_argument("--delay-ms", type=int, default=750)
    parser.add_argument("--timeout", type=int, default=30)
    args = parser.parse_args()

    load_dotenv(ROOT / ".env")
    api_key = os.environ.get("PEXELS_API_KEY", "")
    api_url = os.environ.get("PEXELS_API_URL", DEFAULT_API_URL)
    if not api_key:
        raise SystemExit("Missing PEXELS_API_KEY")

    input_path = Path(args.input)
    if not input_path.is_absolute():
        input_path = ROOT / input_path
    items = json.loads(input_path.read_text(encoding="utf-8"))

    manifest: list[dict[str, Any]] = []
    enriched_count = 0
    for item in items:
        source_url = str((item.get("source") or {}).get("url") or "")
        query = QUERY_BY_URL.get(source_url)
        if not query:
            continue

        payload: dict[str, Any] = {}
        error = ""
        for attempt in range(1, 4):
            try:
                payload = pexels_search(
                    query,
                    api_key,
                    api_url,
                    args.photos_per_tour,
                    args.timeout,
                )
                break
            except Exception as exc:  # noqa: BLE001 - continue with other tours.
                error = f"{type(exc).__name__}:{exc}"
                if attempt < 3:
                    time.sleep(attempt * 2)
        photos = payload.get("photos") or []
        if not photos:
            manifest.append(
                {
                    "tour_name": item.get("name"),
                    "source_url": source_url,
                    "query": query,
                    "provider": "pexels",
                    "status": "search_failed",
                    "error": error or "no_photos",
                }
            )
            continue
        existing = {
            str(image.get("url") if isinstance(image, dict) else image)
            for image in item.get("images") or []
        }
        added = 0
        for photo in photos:
            src = photo.get("src") or {}
            image_url = src.get("large2x") or src.get("large") or src.get("original")
            if not image_url or image_url in existing:
                continue
            item.setdefault("images", []).append(
                {
                    "url": image_url,
                    "alt": f"{item.get('name', '')} - Pexels candidate for {query}",
                }
            )
            existing.add(image_url)
            added += 1
            manifest.append(
                {
                    "tour_name": item.get("name"),
                    "source_url": source_url,
                    "query": query,
                    "provider": "pexels",
                    "photo_id": photo.get("id"),
                    "image_url": image_url,
                    "thumbnail_url": src.get("medium"),
                    "provider_page_url": photo.get("url"),
                    "photographer": photo.get("photographer"),
                    "photographer_url": photo.get("photographer_url"),
                    "status": "manual_visual_review_required",
                }
            )
        if added:
            enriched_count += 1
        time.sleep(max(args.delay_ms, 0) / 1000)

    output = DATA_DIR / f"{args.output_prefix}.json"
    manifest_output = DATA_DIR / f"{args.output_prefix}-manifest.json"
    report_output = DATA_DIR / f"{args.output_prefix}-report.json"
    output.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    manifest_output.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    report = {
        "input": str(input_path.relative_to(ROOT)).replace("\\", "/"),
        "output": str(output.relative_to(ROOT)).replace("\\", "/"),
        "manifest": str(manifest_output.relative_to(ROOT)).replace("\\", "/"),
        "targetTours": len(QUERY_BY_URL),
        "enrichedTours": enriched_count,
        "imageCandidatesAdded": len(manifest),
        "policy": {
            "provider": "pexels",
            "sourceFactsChanged": False,
            "manualVisualReviewRequired": True,
        },
    }
    report_output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2))


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def pexels_search(
    query: str,
    api_key: str,
    api_url: str,
    per_page: int,
    timeout: int,
) -> dict[str, Any]:
    params = urllib.parse.urlencode(
        {
            "query": query,
            "per_page": per_page,
            "orientation": "landscape",
        }
    )
    request = urllib.request.Request(
        f"{api_url}?{params}",
        headers={
            "Authorization": api_key,
            "User-Agent": "DanangTripCrawler/0.1 contact:admin@danangtrip.local",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


if __name__ == "__main__":
    main()
