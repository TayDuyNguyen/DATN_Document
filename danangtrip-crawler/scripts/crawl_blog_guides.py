from __future__ import annotations

import argparse
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_SOURCE_FILE = DATA_DIR / "blog_guide_sources.json"
DEFAULT_OUTPUT_PREFIX = DATA_DIR / "blog-guides"


def main() -> None:
    parser = argparse.ArgumentParser(description="Crawl text-only travel guide sources for DanangTrip blog staging.")
    parser.add_argument("--source-file", default=str(DEFAULT_SOURCE_FILE))
    parser.add_argument("--output-prefix", default=str(DEFAULT_OUTPUT_PREFIX))
    parser.add_argument("--delay-ms", type=int, default=750)
    args = parser.parse_args()

    sources = load_json(Path(args.source_file))
    output_prefix = Path(args.output_prefix)
    crawled_at = datetime.now(timezone.utc).isoformat()

    raw_items: list[dict[str, Any]] = []
    normalized_items: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []

    headers = {
        "User-Agent": "DanangTripCrawler/0.1 contact:admin@danangtrip.local",
        "Accept": "text/html,application/xhtml+xml",
    }

    with httpx.Client(headers=headers, timeout=30.0, follow_redirects=True) as client:
        for source in sources:
            try:
                response = client.get(source["url"])
                response.raise_for_status()
                raw = extract_raw_page(source, response.text, str(response.url), crawled_at)
                normalized = normalize_blog_guide(raw)
                raw_items.append(raw)
                normalized_items.append(normalized)
            except Exception as exc:  # noqa: BLE001 - crawler keeps failure evidence.
                failures.append(
                    {
                        "source": source,
                        "error": str(exc),
                        "crawled_at": crawled_at,
                    }
                )
            time.sleep(max(args.delay_ms, 0) / 1000)

    raw_path = output_prefix.with_name(output_prefix.name + "-raw.json")
    normalized_path = output_prefix.with_name(output_prefix.name + "-normalized.json")
    report_path = output_prefix.with_name(output_prefix.name + "-report.json")

    raw_path.write_text(json.dumps(raw_items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    normalized_path.write_text(json.dumps(normalized_items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = {
        "generatedAt": crawled_at,
        "sourceFile": str(Path(args.source_file)),
        "rawOutput": str(raw_path),
        "normalizedOutput": str(normalized_path),
        "totalSources": len(sources),
        "success": len(normalized_items),
        "failures": len(failures),
        "failureDetails": failures,
        "policy": "Text-only crawl. No images generated. Content is summarized for review, source_url is retained.",
    }
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=True, indent=2))


def extract_raw_page(source: dict[str, Any], html: str, final_url: str, crawled_at: str) -> dict[str, Any]:
    soup = BeautifulSoup(html, "lxml")
    for node in soup(["script", "style", "noscript", "svg", "form"]):
        node.decompose()

    title = text_or_none(soup.find("h1")) or text_or_none(soup.find("title")) or source["name"]
    meta_description = None
    meta = soup.find("meta", attrs={"name": "description"})
    if meta and meta.get("content"):
        meta_description = clean_text(meta["content"])

    headings = [clean_text(tag.get_text(" ")) for tag in soup.find_all(["h2", "h3"])][:20]
    paragraphs = []
    for paragraph in soup.find_all("p"):
        text = clean_text(paragraph.get_text(" "))
        if len(text) >= 60:
            paragraphs.append(text)
        if len(paragraphs) >= 24:
            break

    return {
        "source_name": source["name"],
        "source_url": source["url"],
        "final_url": final_url,
        "domain": urlparse(final_url).netloc,
        "category_hint": source.get("category_hint"),
        "title": title,
        "meta_description": meta_description,
        "headings": dedupe_keep_order(headings),
        "paragraphs": paragraphs,
        "crawled_at": crawled_at,
    }


def normalize_blog_guide(raw: dict[str, Any]) -> dict[str, Any]:
    title = clean_title(raw["title"])
    headings = raw.get("headings") or []
    paragraphs = raw.get("paragraphs") or []
    facts = build_fact_bullets(headings, paragraphs)
    excerpt = build_excerpt(raw, facts)
    content_summary = build_content_summary(title, facts, raw)
    return {
        "title": title,
        "slug": slugify(title),
        "excerpt": excerpt,
        "content_summary": content_summary,
        "source_url": raw["final_url"] or raw["source_url"],
        "source_name": raw["source_name"],
        "category_hint": raw.get("category_hint"),
        "tags_hint": infer_tags(title, facts),
        "featured_image": None,
        "status": "pending_review",
        "review_flags": build_review_flags(raw, facts),
        "crawled_at": raw["crawled_at"],
    }


def build_fact_bullets(headings: list[str], paragraphs: list[str]) -> list[str]:
    candidates = []
    candidates.extend(headings[:8])
    candidates.extend(paragraphs[:10])
    facts = []
    for item in candidates:
        text = clean_text(item)
        if not text or len(text) < 20 or is_boilerplate(text):
            continue
        facts.append(shorten(text, 220))
    return dedupe_keep_order(facts)[:12]


def build_excerpt(raw: dict[str, Any], facts: list[str]) -> str:
    if raw.get("meta_description"):
        return shorten(raw["meta_description"], 480)
    if facts:
        return shorten(facts[0], 480)
    return "Bai viet cam nang du lich duoc thu thap tu nguon cong khai va can bien tap truoc khi publish."


def build_content_summary(title: str, facts: list[str], raw: dict[str, Any]) -> str:
    lines = [
        f"{title}",
        "",
        "Tom tat bien tap cho DanangTrip:",
    ]
    if facts:
        for fact in facts[:10]:
            lines.append(f"- {fact}")
    else:
        lines.append("- Can bien tap noi dung sau khi thu thap them thong tin.")
    lines.extend(
        [
            "",
            f"Nguon tham chieu: {raw['final_url'] or raw['source_url']}",
            "Trang thai: pending_review. Noi dung nay can duoc bien tap lai truoc khi publish.",
        ]
    )
    return "\n".join(lines)


def infer_tags(title: str, facts: list[str]) -> list[str]:
    text = " ".join([title, *facts]).lower()
    tags = []
    for keyword, tag in [
        ("da nang", "da-nang"),
        ("hoi an", "hoi-an"),
        ("hue", "hue"),
        ("itinerary", "lich-trinh"),
        ("hours", "lich-trinh"),
        ("food", "am-thuc"),
        ("beach", "bien"),
        ("culture", "van-hoa"),
    ]:
        if keyword in text:
            tags.append(tag)
    return dedupe_keep_order(tags)


def build_review_flags(raw: dict[str, Any], facts: list[str]) -> list[str]:
    flags = []
    if not facts:
        flags.append("missing_facts")
    if len(raw.get("paragraphs") or []) < 3:
        flags.append("low_text_volume")
    if raw.get("final_url") != raw.get("source_url"):
        flags.append("redirected_source_url")
    return flags


def clean_title(value: str) -> str:
    value = clean_text(value)
    value = re.sub(r"\s*\|\s*Vietnam Tourism.*$", "", value, flags=re.I)
    return shorten(value, 255)


def clean_text(value: str) -> str:
    value = BeautifulSoup(value or "", "lxml").get_text(" ")
    value = re.sub(r"\s+", " ", value).strip()
    return value


def is_boilerplate(value: str) -> bool:
    text = value.lower()
    blocked = [
        "copyright",
        "bản quyền",
        "ban quyen",
        "license:",
        "giấy phép",
        "giay phep",
        "welcome to the official website",
        "visit our social media",
        "the entered email",
        "newsletter",
        "oops",
        "you may also like",
        "nearby places",
        "gallery",
    ]
    return any(pattern in text for pattern in blocked)


def shorten(value: str, max_length: int) -> str:
    value = clean_text(value)
    if len(value) <= max_length:
        return value
    return value[: max_length - 1].rstrip() + "."


def slugify(value: str) -> str:
    text = value.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text[:260] or "blog-guide"


def text_or_none(node: Any) -> str | None:
    if not node:
        return None
    text = clean_text(node.get_text(" "))
    return text or None


def dedupe_keep_order(items: list[str]) -> list[str]:
    seen = set()
    result = []
    for item in items:
        key = item.lower()
        if key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
