from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
MEDIA_DIR = (
    ROOT.parent
    / "data-center"
    / "media-assets"
    / "cloudinary-staging"
    / "tours"
    / "2026-06-07-verified-real-tours"
)
CATALOG_INPUT = DATA_DIR / "verified-real-tour-catalog-20260607.json"
CATALOG_OUTPUT = DATA_DIR / "verified-real-tour-catalog-cloudinary-20260607.json"


def main() -> None:
    upload_results = load_results()
    full_manifest = json.loads((MEDIA_DIR / "manifest.json").read_text(encoding="utf-8"))
    media_map = json.loads((MEDIA_DIR / "tour-media-map.json").read_text(encoding="utf-8"))

    uploaded_by_original_public_id: dict[str, dict[str, Any]] = {}
    uploaded_by_local_file: dict[str, dict[str, Any]] = {}
    for result in upload_results:
        if result.get("upload_status") != "uploaded":
            continue
        original_public_id = str(result.get("cloudinary_public_id") or "")
        uploaded_by_original_public_id[original_public_id] = result
        uploaded_by_local_file[str(result.get("local_file") or "")] = result

    manifest_by_slot = {
        (int(row["catalog_index"]), int(row["photo_index"])): row
        for row in full_manifest
    }
    final_map: list[dict[str, Any]] = []
    for row in media_map:
        slot = (int(row["catalog_index"]), int(row["photo_index"]))
        manifest_row = manifest_by_slot[slot]
        resolved_original_id = str(row.get("resolved_cloudinary_public_id") or "")
        result = uploaded_by_original_public_id.get(resolved_original_id)
        if not result and not row.get("duplicate_content"):
            result = uploaded_by_local_file.get(str(manifest_row.get("local_file") or ""))

        final_map.append(
            {
                **row,
                "cloudinary_public_id": result.get("public_id") if result else None,
                "secure_url": result.get("secure_url") if result else None,
                "width": to_int(result.get("width")) if result else None,
                "height": to_int(result.get("height")) if result else None,
                "format": result.get("format") if result else None,
                "cloudinary_bytes": to_int(result.get("bytes")) if result else None,
                "upload_status": "uploaded" if result else "not_uploaded",
            }
        )

    (MEDIA_DIR / "cloudinary-tour-media-map.json").write_text(
        json.dumps(final_map, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    by_source_url: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in final_map:
        if row.get("secure_url"):
            by_source_url[canonical_url(str(row["source_url"]))].append(row)
    for rows in by_source_url.values():
        rows.sort(key=lambda value: int(value["photo_index"]))

    catalog = json.loads(CATALOG_INPUT.read_text(encoding="utf-8"))
    for tour in catalog:
        source_url = canonical_url(str((tour.get("source") or {}).get("url") or ""))
        cloudinary_rows = by_source_url.get(source_url) or []
        tour["cloudinary_media"] = [
            {
                "url": row["secure_url"],
                "public_id": row["cloudinary_public_id"],
                "is_primary": row["is_primary"],
                "photo_index": row["photo_index"],
                "width": row["width"],
                "height": row["height"],
                "format": row["format"],
                "provider": row["provider"],
                "provider_page_url": row["provider_page_url"],
                "photographer": row["photographer"],
                "sha256": row["sha256"],
            }
            for row in cloudinary_rows
        ]
        if cloudinary_rows:
            tour["thumbnail"] = cloudinary_rows[0]["secure_url"]
            tour["image_urls"] = [row["secure_url"] for row in cloudinary_rows]
        tour["verification"]["cloudinaryUploaded"] = bool(cloudinary_rows)

    CATALOG_OUTPUT.write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    counts_by_tour = {
        source_url: len(rows)
        for source_url, rows in by_source_url.items()
    }
    summary = {
        "catalogOutput": str(CATALOG_OUTPUT.relative_to(ROOT)).replace("\\", "/"),
        "mediaMap": str(
            (MEDIA_DIR / "cloudinary-tour-media-map.json").relative_to(ROOT.parent)
        ).replace("\\", "/"),
        "uniqueAssetsUploaded": len(
            {
                row["cloudinary_public_id"]
                for row in final_map
                if row.get("cloudinary_public_id")
            }
        ),
        "mappedImageSlots": sum(1 for row in final_map if row.get("secure_url")),
        "unmappedImageSlots": sum(1 for row in final_map if not row.get("secure_url")),
        "toursWithCloudinaryMedia": len(counts_by_tour),
        "toursWithAtLeastTwoCloudinaryImages": sum(
            1 for count in counts_by_tour.values() if count >= 2
        ),
        "toursWithThreeCloudinaryImages": sum(
            1 for count in counts_by_tour.values() if count >= 3
        ),
        "databaseWritten": False,
    }
    (MEDIA_DIR / "cloudinary-summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))


def load_results() -> list[dict[str, Any]]:
    rows = json.loads((MEDIA_DIR / "upload-results.json").read_text(encoding="utf-8"))
    retry_path = MEDIA_DIR / "upload-retry-results.json"
    if retry_path.exists():
        rows.extend(json.loads(retry_path.read_text(encoding="utf-8")))
    return rows


def canonical_url(url: str) -> str:
    return url.split("#", 1)[0].split("?", 1)[0].rstrip("/").lower()


def to_int(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


if __name__ == "__main__":
    main()
