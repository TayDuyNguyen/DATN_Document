import argparse
import csv
import hashlib
import hmac
import json
import mimetypes
import os
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT.parent / "data-center" / "media-assets" / "cloudinary-staging" / "locations" / "2026-06-04-overpass-published-inactive" / "manifest.csv"
DEFAULT_RESULTS = DEFAULT_MANIFEST.parent / "upload-results.csv"
DEFAULT_RESULTS_JSON = DEFAULT_MANIFEST.parent / "upload-results.json"
API_ENV = ROOT.parents[1] / "danangtrip-api" / ".env"


def load_cloudinary_credentials() -> tuple[str, str, str]:
    load_dotenv(API_ENV)
    load_dotenv(ROOT / ".env")

    cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME", "")
    api_key = os.getenv("CLOUDINARY_KEY", "")
    api_secret = os.getenv("CLOUDINARY_SECRET", "")
    cloudinary_url = os.getenv("CLOUDINARY_URL", "")

    if cloudinary_url and (not api_key or not api_secret or not cloud_name):
        parsed = urllib.parse.urlparse(cloudinary_url)
        if parsed.scheme == "cloudinary":
            api_key = api_key or urllib.parse.unquote(parsed.username or "")
            api_secret = api_secret or urllib.parse.unquote(parsed.password or "")
            cloud_name = cloud_name or parsed.hostname or ""

    missing = [
        name
        for name, value in {
            "CLOUDINARY_CLOUD_NAME": cloud_name,
            "CLOUDINARY_KEY": api_key,
            "CLOUDINARY_SECRET": api_secret,
        }.items()
        if not value
    ]
    if missing:
        raise RuntimeError(f"Missing Cloudinary credentials: {', '.join(missing)}")
    return cloud_name, api_key, api_secret


def read_manifest(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def signature(params: dict[str, str], api_secret: str) -> str:
    source = "&".join(f"{key}={value}" for key, value in sorted(params.items()) if value)
    return hashlib.sha1((source + api_secret).encode("utf-8")).hexdigest()


def context_value(value: str) -> str:
    value = value.encode("ascii", "ignore").decode("ascii")
    value = value.replace("|", " ").replace("=", " ").strip()
    return value[:240]


def multipart_body(fields: dict[str, str], file_field: str, file_path: Path) -> tuple[bytes, str]:
    boundary = "----DanangTripCloudinaryBoundary" + hashlib.md5(str(time.time()).encode()).hexdigest()
    chunks: list[bytes] = []

    for key, value in fields.items():
        chunks.append(f"--{boundary}\r\n".encode())
        chunks.append(f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode())
        chunks.append(str(value).encode("utf-8"))
        chunks.append(b"\r\n")

    mime = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
    chunks.append(f"--{boundary}\r\n".encode())
    chunks.append(
        f'Content-Disposition: form-data; name="{file_field}"; filename="{file_path.name}"\r\n'
        f"Content-Type: {mime}\r\n\r\n".encode()
    )
    chunks.append(file_path.read_bytes())
    chunks.append(b"\r\n")
    chunks.append(f"--{boundary}--\r\n".encode())
    return b"".join(chunks), boundary


def upload_one(row: dict[str, str], cloud_name: str, api_key: str, api_secret: str, timeout: int) -> dict[str, Any]:
    local_path = Path(row.get("local_path") or "")
    if not local_path.is_file():
        return {**row, "upload_status": "missing_local_file", "upload_error": str(local_path)}

    timestamp = str(int(time.time()))
    context_parts = {
        "location_id": row.get("location_id", ""),
        "location_slug": row.get("location_slug", ""),
        "external_id": row.get("external_id", ""),
        "provider": row.get("provider", ""),
        "photo_id": row.get("photo_id", ""),
        "photographer": row.get("photographer", ""),
        "provider_page_url": row.get("provider_page_url", ""),
    }
    context = "|".join(f"{key}={context_value(value)}" for key, value in context_parts.items() if context_value(value))
    upload_params = {
        "public_id": row["cloudinary_public_id"],
        "overwrite": "true",
        "timestamp": timestamp,
    }
    if context:
        upload_params["context"] = context
    upload_params["signature"] = signature(upload_params, api_secret)
    upload_params["api_key"] = api_key

    body, boundary = multipart_body(upload_params, "file", local_path)
    request = urllib.request.Request(
        f"https://api.cloudinary.com/v1_1/{cloud_name}/image/upload",
        data=body,
        headers={
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "User-Agent": "DanangTripCloudinaryUpload/0.1",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
        return {
            **row,
            "upload_status": "uploaded",
            "asset_id": payload.get("asset_id", ""),
            "public_id": payload.get("public_id", ""),
            "version": payload.get("version", ""),
            "secure_url": payload.get("secure_url", ""),
            "width": payload.get("width", ""),
            "height": payload.get("height", ""),
            "format": payload.get("format", ""),
            "bytes": payload.get("bytes", ""),
        }
    except Exception as exc:
        return {**row, "upload_status": "upload_failed", "upload_error": str(exc)}


def write_results(rows: list[dict[str, Any]], csv_path: Path, json_path: Path) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    fieldnames = sorted({key for row in rows for key in row.keys()})
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--results", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--results-json", type=Path, default=DEFAULT_RESULTS_JSON)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--delay-ms", type=int, default=500)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--only-downloaded", action="store_true", default=True)
    args = parser.parse_args()

    cloud_name, api_key, api_secret = load_cloudinary_credentials()
    rows = read_manifest(args.manifest)
    rows = [row for row in rows if row.get("status") in {"downloaded", "already_downloaded"}]
    if args.offset > 0:
        rows = rows[args.offset :]
    if args.limit > 0:
        rows = rows[: args.limit]

    results: list[dict[str, Any]] = []
    for row in rows:
        result = upload_one(row, cloud_name, api_key, api_secret, args.timeout)
        results.append(result)
        write_results(results, args.results, args.results_json)
        print(json.dumps({
            "location_id": result.get("location_id"),
            "local_file": result.get("local_file"),
            "upload_status": result.get("upload_status"),
            "secure_url": result.get("secure_url", ""),
        }, ensure_ascii=True))
        time.sleep(max(args.delay_ms, 0) / 1000)

    write_results(results, args.results, args.results_json)
    summary = {
        "input_rows": len(rows),
        "uploaded": sum(1 for row in results if row.get("upload_status") == "uploaded"),
        "failed": sum(1 for row in results if row.get("upload_status") != "uploaded"),
        "results": str(args.results),
    }
    print(json.dumps(summary, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
