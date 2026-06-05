from __future__ import annotations

import argparse
import json
import re
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import httpx
from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
SOURCE_CONFIG = DATA_DIR / "tour_sources.json"

USER_AGENT = "DanangTripCrawler/0.1 contact:admin@danangtrip.local"
TOUR_KEYWORDS = (
    "tour",
    "da-nang",
    "danang",
    "hoi-an",
    "hue",
    "ba-na",
    "bana",
    "my-son",
    "cu-lao-cham",
    "marble",
    "son-tra",
)
SKIP_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".pdf", ".zip", ".rar")


@dataclass
class Source:
    name: str
    url: str


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-pages-per-source", type=int, default=35)
    parser.add_argument("--delay-ms", type=int, default=750)
    parser.add_argument("--source-file", default=str(SOURCE_CONFIG))
    parser.add_argument("--output-prefix", default="tour-crawl")
    parser.add_argument("--discover-mode", choices=("sitemap", "page-links", "exact"), default="sitemap")
    args = parser.parse_args()

    source_config = Path(args.source_file)
    if not source_config.is_absolute():
        source_config = ROOT / source_config
    raw_output = DATA_DIR / f"{args.output_prefix}-raw.json"
    normalized_output = DATA_DIR / f"{args.output_prefix}-normalized.json"
    report_output = DATA_DIR / f"{args.output_prefix}-report.json"

    sources = load_sources(source_config)
    raw_items: list[dict[str, Any]] = []
    report_sources: list[dict[str, Any]] = []

    with httpx.Client(
        headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml"},
        follow_redirects=True,
        timeout=25,
    ) as client:
        for source in sources:
            started = now_iso()
            allowed = robots_allowed(client, source.url)
            if not allowed:
                report_sources.append(
                    {
                        "name": source.name,
                        "url": source.url,
                        "status": "skipped_by_robots",
                        "candidateUrls": 0,
                        "collected": 0,
                        "startedAt": started,
                        "finishedAt": now_iso(),
                    }
                )
                continue

            candidates = discover_candidate_urls(client, source, args.max_pages_per_source, args.discover_mode)
            collected = 0
            failures = 0
            for url in candidates:
                try:
                    item = crawl_tour_page(client, source, url)
                    if item:
                        raw_items.append(item)
                        collected += 1
                except Exception as exc:  # noqa: BLE001 - crawler must continue source-by-source.
                    failures += 1
                    print(f"[WARN] {source.name} {url}: {exc}")

                time.sleep(args.delay_ms / 1000)

            report_sources.append(
                {
                    "name": source.name,
                    "url": source.url,
                    "status": "completed",
                    "candidateUrls": len(candidates),
                    "collected": collected,
                    "failures": failures,
                    "startedAt": started,
                    "finishedAt": now_iso(),
                }
            )

    normalized = normalize_items(raw_items)
    write_json(raw_output, raw_items)
    write_json(normalized_output, normalized)
    write_json(
        report_output,
        {
            "generatedAt": now_iso(),
            "sources": report_sources,
            "rawCount": len(raw_items),
            "normalizedCount": len(normalized),
            "outputs": {
                "raw": str(raw_output.relative_to(ROOT)).replace("\\", "/"),
                "normalized": str(normalized_output.relative_to(ROOT)).replace("\\", "/"),
            },
            "policy": {
                "mode": "public_facts_only",
                "longDescriptions": "not_copied",
                "sourceUrlRequired": True,
                "images": "candidate_urls_only",
            },
        },
    )

    print(json.dumps({"raw": len(raw_items), "normalized": len(normalized), "sources": report_sources}, indent=2))


def load_sources(source_config: Path) -> list[Source]:
    payload = json.loads(source_config.read_text(encoding="utf-8"))
    return [Source(name=item["name"], url=item["url"]) for item in payload["sources"]]


def robots_allowed(client: httpx.Client, base_url: str) -> bool:
    parsed = urlparse(base_url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    parser = RobotFileParser()
    parser.set_url(robots_url)
    try:
        response = client.get(robots_url)
        if response.status_code >= 400:
            return True
        parser.parse(response.text.splitlines())
        return parser.can_fetch(USER_AGENT, base_url)
    except Exception:
        return True


def discover_candidate_urls(client: httpx.Client, source: Source, max_pages: int, discover_mode: str) -> list[str]:
    urls: set[str] = set()
    if discover_mode == "exact":
        return [source.url]
    if discover_mode == "sitemap":
        urls.update(fetch_sitemap_urls(client, source.url))
        urls.update(fetch_home_links(client, source.url))
    elif discover_mode == "page-links":
        urls.update(fetch_home_links(client, source.url))
    urls.add(source.url)

    filtered = [
        url
        for url in urls
        if same_domain(source.url, url)
        and not urlparse(url).path.lower().endswith(SKIP_EXTENSIONS)
        and looks_like_tour_url(url)
    ]
    return sorted(set(filtered))[:max_pages]


def fetch_sitemap_urls(client: httpx.Client, base_url: str) -> set[str]:
    parsed = urlparse(base_url)
    candidates = [
        f"{parsed.scheme}://{parsed.netloc}/sitemap.xml",
        f"{parsed.scheme}://{parsed.netloc}/sitemap_index.xml",
    ]
    urls: set[str] = set()
    for sitemap_url in candidates:
        try:
            response = client.get(sitemap_url)
            if response.status_code >= 400 or "<" not in response.text:
                continue
            soup = BeautifulSoup(response.text, "xml")
            nested = [loc.get_text(strip=True) for loc in soup.find_all("loc")]
            for loc in nested:
                if loc.endswith(".xml") and same_domain(base_url, loc):
                    try:
                        nested_response = client.get(loc)
                        nested_soup = BeautifulSoup(nested_response.text, "xml")
                        urls.update(node.get_text(strip=True) for node in nested_soup.find_all("loc"))
                    except Exception:
                        continue
                else:
                    urls.add(loc)
        except Exception:
            continue
    return urls


def fetch_home_links(client: httpx.Client, base_url: str) -> set[str]:
    try:
        response = client.get(base_url)
        response.raise_for_status()
    except Exception:
        return set()

    soup = BeautifulSoup(response.text, "lxml")
    links = set()
    for anchor in soup.find_all("a", href=True):
        links.add(urljoin(base_url, anchor["href"]).split("#")[0])
    return links


def crawl_tour_page(client: httpx.Client, source: Source, url: str) -> dict[str, Any] | None:
    response = client.get(url)
    if response.status_code >= 400 or "text/html" not in response.headers.get("content-type", ""):
        return None

    soup = BeautifulSoup(response.text, "lxml")
    title = extract_title(soup)
    text = clean_text(soup.get_text(" "))
    if not title or not is_tour_content(url, title, text):
        return None

    return {
        "sourceName": source.name,
        "sourceUrl": url,
        "crawledAt": now_iso(),
        "tourName": title,
        "slug": slugify(title),
        "destination": infer_destination(f"{title} {text[:800]}"),
        "duration": find_first(DURATION_PATTERNS, text),
        "departureLocation": find_departure(text),
        "price": find_price(text),
        "originalPrice": None,
        "itinerary": extract_section_lines(soup, ("itinerary", "schedule", "program", "lich trinh", "hanh trinh")),
        "highlights": extract_section_lines(soup, ("highlight", "overview", "why", "diem noi bat")),
        "includedServices": extract_section_lines(soup, ("include", "included", "bao gom", "inclusion")),
        "excludedServices": extract_section_lines(soup, ("exclude", "excluded", "khong bao gom", "exclusion")),
        "cancellationPolicy": extract_section_lines(soup, ("cancel", "cancellation", "policy", "chinh sach")),
        "images": extract_images(soup, url),
        "summary": rewrite_summary(title, text),
    }


DURATION_PATTERNS = (
    r"\b\d+\s*(?:day|days|hour|hours|hrs|h)\b",
    r"\b\d+\s*(?:ngay|gio)\b",
    r"\bhalf\s*day\b",
    r"\bfull\s*day\b",
)
PRICE_PATTERNS = (
    r"(?:from\s*)?\$[\s]?\d{1,4}(?:[.,]\d{1,2})?",
    r"\b\d{1,3}(?:[.,]\d{3})+\s*(?:vnd|vnđ|đ|d)\b",
    r"\b\d{1,4}\s*(?:usd|us\$)\b",
)


def extract_title(soup: BeautifulSoup) -> str:
    og_title = soup.find("meta", property="og:title")
    if og_title and og_title.get("content"):
        return clean_text(og_title["content"])
    h1 = soup.find("h1")
    if h1:
        return clean_text(h1.get_text(" "))
    if soup.title:
        return clean_text(soup.title.get_text(" "))
    return ""


def is_tour_content(url: str, title: str, text: str) -> bool:
    haystack = f"{url} {title} {text[:2000]}".lower()
    return "tour" in haystack and any(keyword in haystack for keyword in ("da nang", "danang", "hoi an", "hue", "ba na", "my son", "cu lao cham"))


def extract_section_lines(soup: BeautifulSoup, keywords: tuple[str, ...], max_items: int = 8) -> list[str]:
    lines: list[str] = []
    for heading in soup.find_all(re.compile("^h[1-6]$")):
        label = clean_text(heading.get_text(" ")).lower()
        if not any(keyword in label for keyword in keywords):
            continue
        for sibling in heading.find_all_next(["p", "li"], limit=20):
            value = clean_text(sibling.get_text(" "))
            if value and len(value) > 4 and value not in lines:
                lines.append(value[:280])
            if len(lines) >= max_items:
                return lines
    return lines


def extract_images(soup: BeautifulSoup, page_url: str, max_images: int = 8) -> list[dict[str, str]]:
    images: list[dict[str, str]] = []
    seen: set[str] = set()
    for img in soup.find_all("img"):
        src = img.get("src") or img.get("data-src") or img.get("data-lazy-src")
        if not src:
            continue
        full_url = urljoin(page_url, src)
        if full_url in seen or full_url.startswith("data:"):
            continue
        alt = clean_text(img.get("alt", ""))
        lower = full_url.lower()
        if any(token in lower for token in ("logo", "icon", "avatar", "placeholder")):
            continue
        images.append({"url": full_url, "alt": alt})
        seen.add(full_url)
        if len(images) >= max_images:
            break
    return images


def normalize_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    unique: dict[str, dict[str, Any]] = {}
    for item in items:
        key = item["sourceUrl"]
        unique[key] = item
    return sorted(unique.values(), key=lambda item: (item["sourceName"], item["tourName"]))


def find_first(patterns: tuple[str, ...], text: str) -> str | None:
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return clean_text(match.group(0))
    return None


def find_price(text: str) -> str | None:
    return find_first(PRICE_PATTERNS, text)


def find_departure(text: str) -> str | None:
    match = re.search(r"(?:departure|depart|pickup|meeting point|khoi hanh|don khach)[^\.;:]{0,80}", text, flags=re.IGNORECASE)
    return clean_text(match.group(0)) if match else None


def infer_destination(text: str) -> list[str]:
    mapping = {
        "da nang": "Da Nang",
        "danang": "Da Nang",
        "hoi an": "Hoi An",
        "hue": "Hue",
        "ba na": "Ba Na Hills",
        "bana": "Ba Na Hills",
        "my son": "My Son",
        "cu lao cham": "Cu Lao Cham",
        "marble": "Marble Mountains",
        "son tra": "Son Tra",
    }
    lower = text.lower()
    found = []
    for key, label in mapping.items():
        if key in lower and label not in found:
            found.append(label)
    return found


def rewrite_summary(title: str, text: str) -> str:
    destinations = ", ".join(infer_destination(f"{title} {text[:800]}")) or "Central Vietnam"
    duration = find_first(DURATION_PATTERNS, text)
    parts = [f"Tour {title} khai thac hanh trinh tai {destinations}."]
    if duration:
        parts.append(f"Thoi luong tham khao: {duration}.")
    parts.append("Thong tin duoc tong hop tu nguon cong khai va can duoc bien tap truoc khi su dung production.")
    return " ".join(parts)


def looks_like_tour_url(url: str) -> bool:
    lower = url.lower()
    return any(keyword in lower for keyword in TOUR_KEYWORDS)


def same_domain(base_url: str, candidate_url: str) -> bool:
    return urlparse(base_url).netloc.replace("www.", "") == urlparse(candidate_url).netloc.replace("www.", "")


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def slugify(value: str) -> str:
    text = value.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")[:220] or "tour"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
