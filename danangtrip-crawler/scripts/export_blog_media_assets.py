import argparse
import csv
import json
import os
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT.parent / "data-center" / "reports" / "blog-posts-missing-featured-image-2026-06-05.json"
DEFAULT_OUTPUT = ROOT.parent / "data-center" / "media-assets" / "cloudinary-staging" / "blogs" / "2026-06-05-blog-missing-featured-image"
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


def ascii_slug(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "unnamed"


def queries(row: dict[str, Any]) -> list[str]:
    title = str(row.get("title") or "")
    excerpt = str(row.get("excerpt") or "")
    text = f"{title} {excerpt}".lower()
    base: list[str] = []
    if "hoi an" in text or "hội an" in text:
        base.append("Hoi An Vietnam travel")
    if "hue" in text or "huế" in text:
        base.append("Hue Vietnam travel")
    if "ba na" in text or "bà nà" in text:
        base.append("Ba Na Hills Vietnam")
    if "son tra" in text or "sơn trà" in text:
        base.append("Son Tra Da Nang Vietnam")
    if "food" in text or "am thuc" in text or "ẩm thực" in text:
        base.append("Da Nang Vietnamese food")
    if "beach" in text or "bien" in text or "biển" in text:
        base.append("Da Nang beach Vietnam")
    base.extend([
        f"{title} Da Nang Vietnam",
        "Da Nang Vietnam travel",
    ])

    result: list[str] = []
    for query in base:
        query = re.sub(r"\s+", " ", query).strip()
        if query and query not in result:
            result.append(query)
    return result


def pexels_search(query: str, api_key: str, api_url: str, timeout: int) -> dict[str, Any]:
    params = urllib.parse.urlencode({"query": query, "per_page": 1, "orientation": "landscape"})
    req = urllib.request.Request(
        f"{api_url}?{params}",
        headers={"Authorization": api_key, "User-Agent": "DanangTripBlogMedia/0.1 contact:admin@danangtrip.local"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def download(url: str, target: Path, timeout: int) -> tuple[bool, str]:
    target.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "DanangTripBlogMedia/0.1 contact:admin@danangtrip.local"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            content_type = response.headers.get("Content-Type", "")
            data = response.read()
        if "image" not in content_type.lower():
            return False, f"unexpected_content_type:{content_type}"
        target.write_bytes(data)
        return True, f"downloaded:{len(data)}"
    except Exception as exc:
        return False, f"{type(exc).__name__}:{exc}"


def write_manifest(rows: list[dict[str, Any]], output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    (output / "manifest.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    fields = sorted({key for row in rows for key in row.keys()})
    with (output / "manifest.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--download", action="store_true")
    parser.add_argument("--delay-ms", type=int, default=750)
    parser.add_argument("--timeout", type=int, default=30)
    args = parser.parse_args()

    load_dotenv(ROOT / ".env")
    api_key = os.environ.get("PEXELS_API_KEY", "")
    api_url = os.environ.get("PEXELS_API_URL", DEFAULT_PEXELS_URL)
    if not api_key:
        raise SystemExit("Missing PEXELS_API_KEY")

    source_rows = json.loads(args.input.read_text(encoding="utf-8"))
    manifest: list[dict[str, Any]] = []
    originals = args.output / "originals"

    for row in source_rows:
        blog_id = str(row["id"])
        slug = ascii_slug(str(row.get("slug") or row.get("title") or "blog-post"))
        selected: dict[str, Any] | None = None
        selected_query = ""
        error = ""
        for query in queries(row):
            try:
                payload = pexels_search(query, api_key, api_url, args.timeout)
                photos = payload.get("photos") or []
                if photos:
                    selected = photos[0]
                    selected_query = query
                    break
            except Exception as exc:
                error = f"{type(exc).__name__}:{exc}"
            time.sleep(max(args.delay_ms, 0) / 1000)

        if not selected:
            manifest.append({**row, "blog_id": blog_id, "blog_slug": slug, "status": "missing_image_candidate", "search_error": error})
            continue

        src = selected.get("src") or {}
        image_url = src.get("large2x") or src.get("large") or src.get("original")
        photo_id = str(selected.get("id") or "unknown")
        local_file = f"blog-{blog_id}__{slug}__p01__pexels-{photo_id}.jpg"
        local_path = originals / local_file
        status = "pending_download"
        message = ""
        if args.download:
            if local_path.exists() and local_path.stat().st_size > 0:
                status = "already_downloaded"
                message = f"existing:{local_path.stat().st_size}"
            else:
                ok, message = download(str(image_url), local_path, args.timeout)
                status = "downloaded" if ok else "download_failed"

        manifest.append({
            **row,
            "blog_id": blog_id,
            "blog_slug": slug,
            "location_id": blog_id,
            "location_slug": slug,
            "provider": "pexels",
            "photo_index": 1,
            "photo_id": photo_id,
            "image_url": image_url,
            "thumbnail_url": src.get("medium"),
            "provider_page_url": selected.get("url"),
            "photographer": selected.get("photographer"),
            "photographer_url": selected.get("photographer_url"),
            "local_file": local_file,
            "local_path": str(local_path) if status in {"downloaded", "already_downloaded"} else "",
            "cloudinary_public_id": f"danangtrip/blogs/{slug}/blog-{blog_id}__{slug}__p01",
            "search_query": selected_query,
            "status": status,
            "download_message": message,
        })
        time.sleep(max(args.delay_ms, 0) / 1000)

    write_manifest(manifest, args.output)
    summary = {
        "source_rows": len(source_rows),
        "manifest_rows": len(manifest),
        "downloaded": sum(1 for row in manifest if row.get("status") in {"downloaded", "already_downloaded"}),
        "missing_candidate": sum(1 for row in manifest if row.get("status") == "missing_image_candidate"),
        "download_failed": sum(1 for row in manifest if row.get("status") == "download_failed"),
        "output": str(args.output),
    }
    (args.output / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
