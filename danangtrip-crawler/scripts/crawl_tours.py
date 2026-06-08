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

    itinerary = extract_itinerary(soup, url)
    included_services = extract_services(soup, url, included=True)
    excluded_services = extract_services(soup, url, included=False)
    duration = extract_duration(soup, url, title)
    price = extract_price(soup, url)

    return {
        "sourceName": source.name,
        "sourceUrl": url,
        "crawledAt": now_iso(),
        "tourName": title,
        "slug": slugify(title),
        "destination": infer_destination(f"{title} {text[:800]}"),
        "duration": duration,
        "departureLocation": find_departure(text),
        "price": price,
        "originalPrice": None,
        "itinerary": itinerary,
        "highlights": extract_section_lines(soup, ("highlight", "overview", "why", "diem noi bat")),
        "includedServices": included_services,
        "excludedServices": excluded_services,
        "cancellationPolicy": extract_section_lines(soup, ("cancel", "cancellation", "policy", "chinh sach")),
        "images": extract_images(soup, url, title),
        "summary": rewrite_summary(title, text, duration),
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
        heading_level = int(heading.name[1])
        for sibling in heading.next_elements:
            if sibling is heading:
                continue
            if getattr(sibling, "name", None) and re.fullmatch(r"h[1-6]", sibling.name):
                if int(sibling.name[1]) <= heading_level:
                    break
            if getattr(sibling, "name", None) not in {"p", "li"}:
                continue
            value = clean_text(sibling.get_text(" "))
            if value and len(value) > 4 and value not in lines:
                lines.append(value[:280])
            if len(lines) >= max_items:
                return lines
    return lines


def extract_itinerary(soup: BeautifulSoup, page_url: str, max_items: int = 10) -> list[str]:
    domain = urlparse(page_url).netloc.lower()
    if "venusvietnamtravel.com" in domain:
        return extract_selector_lines(soup, ".it-row", max_items)
    if "vmtravel.com" in domain:
        lines = extract_section_lines(soup, ("detail itinerary", "itinerary"), max_items)
        if lines:
            return lines
        return extract_selector_lines(soup, ".accordion-item", max_items)
    return extract_section_lines(
        soup,
        ("itinerary", "schedule", "program", "lich trinh", "hanh trinh"),
        max_items,
    )


def extract_services(
    soup: BeautifulSoup,
    page_url: str,
    *,
    included: bool,
    max_items: int = 10,
) -> list[str]:
    domain = urlparse(page_url).netloc.lower()
    if "venusvietnamtravel.com" in domain:
        bodies = soup.select(".spec-body")
        index = 0 if included else 1
        if len(bodies) > index:
            return extract_list_or_text_lines(bodies[index], max_items)

    keywords = (
        ("include", "included", "bao gom", "inclusion")
        if included
        else ("exclude", "excluded", "khong bao gom", "exclusion")
    )
    return extract_section_lines(soup, keywords, max_items)


def extract_selector_lines(soup: BeautifulSoup, selector: str, max_items: int) -> list[str]:
    lines: list[str] = []
    for node in soup.select(selector):
        value = clean_text(node.get_text(" "))
        if value and len(value) > 4 and value not in lines:
            lines.append(value[:280])
        if len(lines) >= max_items:
            break
    return lines


def extract_list_or_text_lines(node: Any, max_items: int) -> list[str]:
    list_items = node.find_all("li")
    if list_items:
        return unique_lines((item.get_text(" ") for item in list_items), max_items)

    text = clean_text(node.get_text(" "))
    chunks = re.split(r"\s*[.;]\s+|\s{2,}", text)
    return unique_lines(chunks, max_items)


def unique_lines(values: Any, max_items: int) -> list[str]:
    lines: list[str] = []
    for raw_value in values:
        value = clean_text(str(raw_value))
        if len(value) > 4 and value not in lines:
            lines.append(value[:280])
        if len(lines) >= max_items:
            break
    return lines


def extract_duration(soup: BeautifulSoup, page_url: str, title: str) -> str | None:
    domain = urlparse(page_url).netloc.lower()

    if "vmtravel.com" in domain:
        for feature in soup.select(".st-service-feature .item"):
            value = clean_text(feature.get_text(" "))
            match = re.search(r"\bduration\s+(.+)", value, flags=re.IGNORECASE)
            if match:
                duration = find_first(DURATION_PATTERNS, match.group(1))
                if duration:
                    return duration

    if "venusvietnamtravel.com" in domain:
        for row in soup.select(".it-row"):
            value = clean_text(row.get_text(" "))
            duration = duration_from_time_range(value)
            if duration:
                return duration

    title_duration = find_first(DURATION_PATTERNS, title)
    if title_duration:
        return title_duration

    content = clone_without_page_chrome(soup)
    content_text = clean_text(content.get_text(" "))
    candidates = find_all(DURATION_PATTERNS, content_text)
    if not candidates:
        return None

    day_named = any(
        token in title.lower()
        for token in ("day tour", "daily tour", "full day", "full-day", "day trip")
    )
    if day_named:
        day_candidate = next(
            (value for value in candidates if re.search(r"\b(?:1|one)\s*day\b|\bfull\s*-?\s*day\b", value, re.I)),
            None,
        )
        if day_candidate:
            return day_candidate
    return candidates[0]


def extract_price(soup: BeautifulSoup, page_url: str) -> str | None:
    domain = urlparse(page_url).netloc.lower()

    if "vmtravel.com" in domain:
        price_nodes = soup.select(".table-price-tour, .price-package-tour.table-price")
        for node in price_nodes:
            value = clean_text(node.get_text(" "))
            price = find_price(value)
            if price:
                return price
        if price_nodes:
            return None

    for meta in soup.find_all("meta"):
        property_name = str(meta.get("property") or meta.get("itemprop") or "").lower()
        if property_name not in {
            "product:price:amount",
            "og:price:amount",
            "price",
        }:
            continue
        content = clean_text(str(meta.get("content") or ""))
        if not content:
            continue
        currency = find_meta_currency(soup)
        return f"{content} {currency}".strip()

    content = clone_without_page_chrome(soup)
    return find_price(clean_text(content.get_text(" ")))


def find_meta_currency(soup: BeautifulSoup) -> str:
    for meta in soup.find_all("meta"):
        property_name = str(meta.get("property") or meta.get("itemprop") or "").lower()
        if property_name in {"product:price:currency", "og:price:currency", "pricecurrency"}:
            return clean_text(str(meta.get("content") or ""))
    return ""


def duration_from_time_range(value: str) -> str | None:
    match = re.search(
        r"\b(\d{1,2}):(\d{2})\s*[–—-]\s*(\d{1,2}):(\d{2})\b",
        value,
    )
    if not match:
        return None
    start = int(match.group(1)) * 60 + int(match.group(2))
    end = int(match.group(3)) * 60 + int(match.group(4))
    if end <= start:
        end += 24 * 60
    hours = (end - start) / 60
    if not 0.5 <= hours <= 24:
        return None
    return f"{hours:g} hours"


def clone_without_page_chrome(soup: BeautifulSoup) -> BeautifulSoup:
    content = BeautifulSoup(str(soup), "lxml")
    for node in content.select("nav, header, footer, script, style, form, .menu, .mega-menu, .dropdown-menu"):
        node.decompose()
    return content


def extract_images(
    soup: BeautifulSoup,
    page_url: str,
    title: str,
    max_images: int = 8,
) -> list[dict[str, str]]:
    images: list[dict[str, str]] = []
    seen: set[str] = set()
    title_tokens = relevant_image_tokens(title)

    for meta in soup.find_all("meta"):
        if meta.get("property") not in {"og:image", "og:image:secure_url"}:
            continue
        add_image_candidate(images, seen, meta.get("content"), title, page_url)

    for img in soup.find_all("img"):
        src = (
            img.get("data-large_image")
            or img.get("data-src")
            or img.get("data-lazy-src")
            or img.get("src")
        )
        if not src:
            continue
        full_url = urljoin(page_url, src)
        if full_url in seen or full_url.startswith("data:"):
            continue
        alt = clean_text(img.get("alt", ""))
        haystack = f"{full_url} {alt}".lower()
        if any(
            token in haystack
            for token in (
                "logo",
                "icon",
                "avatar",
                "placeholder",
                "tripadvisor",
                "travelers_choice",
                "branding",
            )
        ):
            continue
        if image_token_overlap(haystack, title_tokens) < 2:
            continue
        add_image_candidate(images, seen, full_url, alt or title, page_url)
        if len(images) >= max_images:
            break
    return images


def add_image_candidate(
    images: list[dict[str, str]],
    seen: set[str],
    raw_url: str | None,
    alt: str,
    page_url: str,
) -> None:
    if not raw_url:
        return
    full_url = urljoin(page_url, raw_url)
    if full_url in seen or full_url.startswith("data:"):
        return
    lower = full_url.lower()
    if any(token in lower for token in ("logo", "icon", "avatar", "placeholder", "tripadvisor", "branding")):
        return
    images.append({"url": full_url, "alt": clean_text(alt)})
    seen.add(full_url)


def relevant_image_tokens(value: str) -> set[str]:
    ignored = {
        "tour",
        "from",
        "with",
        "good",
        "price",
        "daily",
        "trip",
        "best",
        "explore",
        "city",
        "travel",
    }
    return {
        token
        for token in re.findall(r"[a-z0-9]+", value.lower())
        if len(token) >= 3 and token not in ignored
    }


def image_token_overlap(value: str, title_tokens: set[str]) -> int:
    image_tokens = set(re.findall(r"[a-z0-9]+", value.lower()))
    return len(title_tokens & image_tokens)


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


def find_all(patterns: tuple[str, ...], text: str) -> list[str]:
    values: list[str] = []
    for pattern in patterns:
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            value = clean_text(match.group(0))
            if value not in values:
                values.append(value)
    return values


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


def rewrite_summary(title: str, text: str, duration: str | None = None) -> str:
    destinations = ", ".join(infer_destination(f"{title} {text[:800]}")) or "Central Vietnam"
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
