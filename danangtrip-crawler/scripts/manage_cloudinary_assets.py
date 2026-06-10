import argparse
import base64
import hashlib
import json
import os
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[1]
API_ENV = ROOT.parents[1] / "danangtrip-api" / ".env"
CLOUDINARY_URL_PATTERN = re.compile(r"https://res\.cloudinary\.com/[^\"'\s,)]+")


def load_cloudinary_credentials() -> tuple[str, str, str]:
    load_dotenv(API_ENV)
    load_dotenv(ROOT / ".env")

    cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME", "")
    api_key = os.getenv("CLOUDINARY_KEY") or os.getenv("CLOUDINARY_API_KEY", "")
    api_secret = os.getenv("CLOUDINARY_SECRET") or os.getenv("CLOUDINARY_API_SECRET", "")
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
            "CLOUDINARY_KEY/CLOUDINARY_API_KEY": api_key,
            "CLOUDINARY_SECRET/CLOUDINARY_API_SECRET": api_secret,
        }.items()
        if not value
    ]
    if missing:
        raise RuntimeError(f"Missing Cloudinary credentials: {', '.join(missing)}")

    return cloud_name, api_key, api_secret


def sign(params: dict[str, str], api_secret: str) -> str:
    source = "&".join(f"{key}={value}" for key, value in sorted(params.items()) if value)
    return hashlib.sha1((source + api_secret).encode("utf-8")).hexdigest()


def signed_api_request(
    cloud_name: str,
    api_key: str,
    api_secret: str,
    method: str,
    path: str,
    params: dict[str, str] | None = None,
) -> dict[str, Any]:
    params = dict(params or {})
    timestamp = str(int(time.time()))
    params["timestamp"] = timestamp
    params["signature"] = sign(params, api_secret)
    params["api_key"] = api_key

    data = urllib.parse.urlencode(params).encode("utf-8")
    request = urllib.request.Request(
        f"https://api.cloudinary.com/v1_1/{cloud_name}/{path}",
        data=data,
        method=method,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def admin_api_request(
    cloud_name: str,
    api_key: str,
    api_secret: str,
    method: str,
    path: str,
    params: list[tuple[str, str]] | None = None,
) -> dict[str, Any]:
    params = params or []
    query = urllib.parse.urlencode(params)
    url = f"https://api.cloudinary.com/v1_1/{cloud_name}/{path}"
    if query:
        url = f"{url}?{query}"
    token = base64.b64encode(f"{api_key}:{api_secret}".encode("utf-8")).decode("ascii")
    request = urllib.request.Request(
        url,
        method=method,
        headers={"Authorization": f"Basic {token}"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def list_resources_by_prefix(
    cloud_name: str,
    api_key: str,
    api_secret: str,
    prefix: str,
) -> list[dict[str, Any]]:
    resources: list[dict[str, Any]] = []
    next_cursor = ""
    while True:
        params = [
            ("prefix", prefix.strip("/")),
            ("max_results", "500"),
        ]
        if next_cursor:
            params.append(("next_cursor", next_cursor))

        payload = admin_api_request(cloud_name, api_key, api_secret, "GET", "resources/image/upload", params)
        resources.extend(payload.get("resources") or [])
        next_cursor = payload.get("next_cursor") or ""
        if not next_cursor:
            break
    return resources


def extract_public_id(url: str) -> str | None:
    parsed = urllib.parse.urlparse(url)
    parts = parsed.path.split("/")
    try:
        upload_index = parts.index("upload")
    except ValueError:
        return None

    public_parts = parts[upload_index + 1 :]
    if public_parts and re.fullmatch(r"v\d+", public_parts[0]):
        public_parts = public_parts[1:]
    if not public_parts:
        return None

    public_id = "/".join(public_parts)
    return re.sub(r"\.[a-zA-Z0-9]+$", "", public_id)


def collect_used_public_ids(roots: list[Path]) -> set[str]:
    used: set[str] = set()
    for root in roots:
        if not root.exists():
            continue
        files = [root] if root.is_file() else [path for path in root.rglob("*") if path.is_file()]
        for file_path in files:
            try:
                text = file_path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for match in CLOUDINARY_URL_PATTERN.findall(text):
                public_id = extract_public_id(match)
                if public_id:
                    used.add(public_id)
    return used


def audit(args: argparse.Namespace) -> None:
    cloud_name, api_key, api_secret = load_cloudinary_credentials()
    resources = list_resources_by_prefix(cloud_name, api_key, api_secret, args.prefix)
    used_ids = collect_used_public_ids([Path(path) for path in args.used_url_roots])
    rows = []
    for resource in resources:
        public_id = resource.get("public_id", "")
        rows.append(
            {
                "public_id": public_id,
                "secure_url": resource.get("secure_url", ""),
                "bytes": resource.get("bytes", 0),
                "created_at": resource.get("created_at", ""),
                "is_referenced_by_seed_or_docs": public_id in used_ids,
            }
        )

    print(json.dumps({
        "prefix": args.prefix,
        "resource_count": len(rows),
        "referenced_count": sum(1 for row in rows if row["is_referenced_by_seed_or_docs"]),
        "unreferenced_count": sum(1 for row in rows if not row["is_referenced_by_seed_or_docs"]),
        "resources": rows,
    }, ensure_ascii=False, indent=2))


def delete_prefix(args: argparse.Namespace) -> None:
    if args.confirm != args.prefix:
        raise SystemExit("Refusing delete. Pass --confirm with the exact prefix value.")

    cloud_name, api_key, api_secret = load_cloudinary_credentials()
    resources = list_resources_by_prefix(cloud_name, api_key, api_secret, args.prefix)
    public_ids = [resource["public_id"] for resource in resources if resource.get("public_id")]
    if not public_ids:
        print(json.dumps({"prefix": args.prefix, "deleted": 0}, indent=2))
        return

    deleted = []
    for index in range(0, len(public_ids), 100):
        chunk = public_ids[index : index + 100]
        payload = admin_api_request(
            cloud_name,
            api_key,
            api_secret,
            "DELETE",
            "resources/image/upload",
            [("public_ids[]", public_id) for public_id in chunk],
        )
        deleted.append(payload)

    print(json.dumps({"prefix": args.prefix, "requested_delete": len(public_ids), "responses": deleted}, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    audit_parser = subparsers.add_parser("audit")
    audit_parser.add_argument("--prefix", required=True)
    audit_parser.add_argument("--used-url-roots", nargs="+", required=True)
    audit_parser.set_defaults(func=audit)

    delete_parser = subparsers.add_parser("delete-prefix")
    delete_parser.add_argument("--prefix", required=True)
    delete_parser.add_argument("--confirm", required=True)
    delete_parser.set_defaults(func=delete_prefix)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
