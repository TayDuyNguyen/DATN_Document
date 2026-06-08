from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
BASE_URL = "https://vmtravel.com/"
CENTRAL_TOKENS = (
    "da-nang",
    "danang",
    "hoi-an",
    "hoian",
    "hue",
    "ba-na",
    "bana",
    "my-son",
    "cham-island",
    "marble-mountain",
    "son-tra",
    "tien-sa",
    "chan-may",
    "golden-bridge",
    "coconut",
    "basket-boat",
    "cam-thanh",
    "hot-spring",
    "monkey-mountain",
    "linh-ung",
    "ancient-town",
    "central-vietnam",
    "lang-co",
    "hai-van",
    "phong-nha",
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=80)
    parser.add_argument(
        "--output",
        default=str(DATA_DIR / "vmtravel-central-detail-sources.json"),
    )
    args = parser.parse_args()

    output = Path(args.output)
    if not output.is_absolute():
        output = ROOT / output

    known_urls = load_known_urls()
    discovered = discover_sitemap_urls()
    selected = [
        url
        for url in discovered
        if is_detail_tour(url)
        and is_central_vietnam_tour(url)
        and canonical_url(url) not in known_urls
    ][: args.limit]

    payload = {
        "sources": [
            {
                "name": f"vmtravel_central_{index:03d}",
                "url": url,
            }
            for index, url in enumerate(selected, start=1)
        ]
    }
    output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "discovered": len(discovered),
                "known": len(known_urls),
                "selected": len(selected),
                "output": str(output.relative_to(ROOT)).replace("\\", "/"),
            },
            indent=2,
        )
    )


def discover_sitemap_urls() -> list[str]:
    urls: set[str] = set()
    with httpx.Client(follow_redirects=True, timeout=30) as client:
        for root_url in (
            "https://vmtravel.com/sitemap.xml",
            "https://vmtravel.com/sitemap_index.xml",
        ):
            response = client.get(root_url)
            if response.status_code >= 400:
                continue
            sitemap_urls = parse_locs(response.text)
            for sitemap_url in sitemap_urls:
                if sitemap_url.lower().endswith(".xml"):
                    nested = client.get(sitemap_url)
                    if nested.status_code < 400:
                        urls.update(parse_locs(nested.text))
                else:
                    urls.add(sitemap_url)
    return sorted(urls)


def parse_locs(xml: str) -> list[str]:
    soup = BeautifulSoup(xml, "xml")
    return [node.get_text(strip=True) for node in soup.find_all("loc")]


def load_known_urls() -> set[str]:
    known: set[str] = set()
    paths = set(DATA_DIR.glob("*tour*.json")) | set(DATA_DIR.glob("*vmtravel*.json"))
    for path in paths:
        if path.stat().st_size > 20_000_000:
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError, UnicodeDecodeError):
            continue
        collect_urls(payload, known)
    return known


def collect_urls(value: object, output: set[str]) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if key in {"sourceUrl", "source_url", "url"} and isinstance(item, str):
                if "vmtravel.com" in item:
                    output.add(canonical_url(item))
            else:
                collect_urls(item, output)
    elif isinstance(value, list):
        for item in value:
            collect_urls(item, output)


def is_detail_tour(url: str) -> bool:
    parsed = urlparse(url)
    parts = [part for part in parsed.path.lower().split("/") if part]
    return len(parts) == 2 and parts[0] == "tours"


def is_central_vietnam_tour(url: str) -> bool:
    lower = url.lower()
    return any(token in lower for token in CENTRAL_TOKENS)


def canonical_url(url: str) -> str:
    return url.split("#", 1)[0].split("?", 1)[0].rstrip("/").lower()


if __name__ == "__main__":
    main()
