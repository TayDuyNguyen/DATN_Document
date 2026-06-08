from __future__ import annotations

import argparse
import csv
import hashlib
import json
import mimetypes
import re
import time
import urllib.request
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data" / "verified-real-tour-catalog-20260607.json"
DEFAULT_OUTPUT = (
    ROOT.parent
    / "data-center"
    / "media-assets"
    / "cloudinary-staging"
    / "tours"
    / "2026-06-07-verified-real-tours"
)
PEXELS_MANIFEST = ROOT / "data" / "venus-tour-pexels-enriched-20260607-manifest.json"
USER_AGENT = "DanangTripTourMedia/0.2 contact:admin@danangtrip.local"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--photos-per-tour", type=int, default=3)
    parser.add_argument("--delay-ms", type=int, default=300)
    parser.add_argument("--timeout", type=int, default=40)
    args = parser.parse_args()

    tours = json.loads(args.input.read_text(encoding="utf-8"))
    pexels_by_url = load_pexels_manifest()
    originals = args.output / "originals"
    originals.mkdir(parents=True, exist_ok=True)

    manifest: list[dict[str, Any]] = []
    for tour_index, tour in enumerate(tours, start=1):
        slug = ascii_slug(str(tour.get("slug") or tour.get("name") or "tour"))
        source_url = str((tour.get("source") or {}).get("url") or "")
        selected_images = select_images(tour, args.photos_per_tour)
        for photo_index, image in enumerate(selected_images, start=1):
            image_url = str(image.get("url") or "")
            provider_data = pexels_by_url.get(image_url, {})
            provider = provider_data.get("provider") or source_provider(image_url)
            external_id = (
                str(provider_data.get("photo_id") or "")
                or external_image_id(image_url)
            )
            base_name = (
                f"tour-{tour_index:03d}__{slug}__"
                f"p{photo_index:02d}__{provider}-{external_id}"
            )
            result = download_image(
                image_url,
                originals,
                base_name,
                args.timeout,
            )
            local_file = result.get("local_file") or f"{base_name}.jpg"
            public_stem = Path(local_file).stem
            manifest.append(
                {
                    "catalog_index": tour_index,
                    "tour_name": tour.get("name"),
                    "tour_slug": slug,
                    "source_url": source_url,
                    "photo_index": photo_index,
                    "is_primary": photo_index == 1,
                    "provider": provider,
                    "provider_photo_id": provider_data.get("photo_id"),
                    "provider_page_url": provider_data.get("provider_page_url"),
                    "photographer": provider_data.get("photographer"),
                    "photographer_url": provider_data.get("photographer_url"),
                    "image_url": image_url,
                    "image_alt": image.get("alt"),
                    "local_file": local_file,
                    "local_path": result.get("local_path", ""),
                    "content_type": result.get("content_type"),
                    "bytes": result.get("bytes", 0),
                    "sha256": result.get("sha256"),
                    "width": None,
                    "height": None,
                    "cloudinary_public_id": (
                        f"danangtrip/tours/{slug}/{public_stem}"
                    ),
                    "cloudinary_resource_type": "image",
                    "status": result["status"],
                    "error": result.get("error"),
                    "rights_note": (
                        "Pexels attribution metadata retained; verify final usage terms."
                        if provider == "pexels"
                        else "Downloaded from operator source page; verify reuse permission before production publication."
                    ),
                }
            )
            time.sleep(max(args.delay_ms, 0) / 1000)

    write_outputs(args.output, manifest, len(tours), args.photos_per_tour)


def select_images(tour: dict[str, Any], limit: int) -> list[dict[str, Any]]:
    images = tour.get("images") or []
    selected: list[dict[str, Any]] = []
    seen: set[str] = set()
    for image in images:
        row = image if isinstance(image, dict) else {"url": str(image), "alt": ""}
        url = str(row.get("url") or "")
        if not url or url in seen:
            continue
        selected.append(row)
        seen.add(url)
        if len(selected) >= limit:
            break
    return selected


def download_image(
    url: str,
    output_dir: Path,
    base_name: str,
    timeout: int,
) -> dict[str, Any]:
    existing_files = list(output_dir.glob(f"{base_name}.*"))
    for local_path in existing_files:
        if not local_path.is_file() or local_path.stat().st_size < 10_000:
            continue
        data = local_path.read_bytes()
        return {
            "status": "already_downloaded",
            "local_file": local_path.name,
            "local_path": str(local_path),
            "content_type": mimetypes.guess_type(local_path.name)[0],
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
        }

    last_error = ""
    for attempt in range(1, 4):
        try:
            request = urllib.request.Request(
                url,
                headers={"User-Agent": USER_AGENT, "Accept": "image/*"},
            )
            with urllib.request.urlopen(request, timeout=timeout) as response:
                content_type = response.headers.get("Content-Type", "").split(";")[0]
                data = response.read()
            if not content_type.startswith("image/"):
                raise ValueError(f"unexpected_content_type:{content_type}")
            if len(data) < 10_000:
                raise ValueError(f"image_too_small:{len(data)}")
            extension = extension_for(content_type, url)
            local_file = f"{base_name}{extension}"
            local_path = output_dir / local_file
            local_path.write_bytes(data)
            return {
                "status": "downloaded",
                "local_file": local_file,
                "local_path": str(local_path),
                "content_type": content_type,
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            }
        except Exception as exc:  # noqa: BLE001 - retry network and source errors.
            last_error = f"{type(exc).__name__}:{exc}"
            if attempt < 3:
                time.sleep(attempt * 2)
    return {
        "status": "download_failed",
        "error": last_error,
    }


def extension_for(content_type: str, url: str) -> str:
    known = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/webp": ".webp",
        "image/gif": ".gif",
    }
    if content_type in known:
        return known[content_type]
    suffix = Path(urlparse(url).path).suffix.lower()
    return suffix if suffix in {".jpg", ".jpeg", ".png", ".webp", ".gif"} else (
        mimetypes.guess_extension(content_type) or ".img"
    )


def source_provider(url: str) -> str:
    domain = urlparse(url).netloc.lower().replace("www.", "")
    if "pexels.com" in domain:
        return "pexels"
    if "vmtravel.com" in domain:
        return "vmtravel"
    if "venus" in domain:
        return "venus"
    return ascii_slug(domain.split(":")[0]) or "source"


def external_image_id(url: str) -> str:
    stem = ascii_slug(Path(urlparse(url).path).stem)
    if stem and stem != "unnamed":
        return stem[:48]
    return hashlib.sha1(url.encode("utf-8")).hexdigest()[:12]


def ascii_slug(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "unnamed"


def load_pexels_manifest() -> dict[str, dict[str, Any]]:
    if not PEXELS_MANIFEST.exists():
        return {}
    rows = json.loads(PEXELS_MANIFEST.read_text(encoding="utf-8"))
    return {
        str(row.get("image_url")): row
        for row in rows
        if row.get("status") == "manual_visual_review_required"
        and row.get("image_url")
    }


def write_outputs(
    output_dir: Path,
    rows: list[dict[str, Any]],
    tour_count: int,
    photos_per_tour: int,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    first_public_id_by_checksum: dict[str, str] = {}
    for row in rows:
        checksum = str(row.get("sha256") or "")
        if not checksum:
            row["duplicate_of_cloudinary_public_id"] = None
            continue
        if checksum in first_public_id_by_checksum:
            row["duplicate_of_cloudinary_public_id"] = first_public_id_by_checksum[
                checksum
            ]
        else:
            first_public_id_by_checksum[checksum] = row["cloudinary_public_id"]
            row["duplicate_of_cloudinary_public_id"] = None

    (output_dir / "manifest.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    fields = list(rows[0].keys()) if rows else []
    with (output_dir / "manifest.csv").open(
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    successful = [
        row
        for row in rows
        if row["status"] in {"downloaded", "already_downloaded"}
    ]
    upload_rows = [
        row
        for row in successful
        if not row.get("duplicate_of_cloudinary_public_id")
    ]
    media_map = []
    for row in rows:
        resolved_public_id = (
            row.get("duplicate_of_cloudinary_public_id")
            or row.get("cloudinary_public_id")
        )
        media_map.append(
            {
                "catalog_index": row.get("catalog_index"),
                "tour_name": row.get("tour_name"),
                "tour_slug": row.get("tour_slug"),
                "source_url": row.get("source_url"),
                "photo_index": row.get("photo_index"),
                "is_primary": row.get("is_primary"),
                "status": row.get("status"),
                "resolved_cloudinary_public_id": resolved_public_id,
                "original_cloudinary_public_id": row.get("cloudinary_public_id"),
                "duplicate_content": bool(
                    row.get("duplicate_of_cloudinary_public_id")
                ),
                "provider": row.get("provider"),
                "provider_page_url": row.get("provider_page_url"),
                "photographer": row.get("photographer"),
                "sha256": row.get("sha256"),
            }
        )

    write_json_csv(output_dir / "upload-manifest", upload_rows)
    (output_dir / "tour-media-map.json").write_text(
        json.dumps(media_map, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    successful_by_tour: dict[str, int] = {}
    for row in successful:
        slug = str(row["tour_slug"])
        successful_by_tour[slug] = successful_by_tour.get(slug, 0) + 1
    summary = {
        "tourCount": tour_count,
        "photosPerTour": photos_per_tour,
        "manifestRows": len(rows),
        "downloaded": sum(1 for row in rows if row["status"] == "downloaded"),
        "alreadyDownloaded": sum(
            1 for row in rows if row["status"] == "already_downloaded"
        ),
        "failed": len(rows) - len(successful),
        "downloadedBytes": sum(int(row.get("bytes") or 0) for row in successful),
        "uniqueChecksums": len(
            {row["sha256"] for row in successful if row.get("sha256")}
        ),
        "duplicateContentCount": len(successful)
        - len({row["sha256"] for row in successful if row.get("sha256")}),
        "uploadReadyAssets": len(upload_rows),
        "toursWithAtLeastTwoImages": sum(
            1 for count in successful_by_tour.values() if count >= 2
        ),
        "toursWithAllRequestedImages": sum(
            1 for count in successful_by_tour.values() if count >= photos_per_tour
        ),
        "cloudinaryUploaded": False,
        "databaseWritten": False,
        "output": str(output_dir),
    }
    (output_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))


def write_json_csv(path_without_suffix: Path, rows: list[dict[str, Any]]) -> None:
    path_without_suffix.with_suffix(".json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    fields = list(rows[0].keys()) if rows else []
    with path_without_suffix.with_suffix(".csv").open(
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
