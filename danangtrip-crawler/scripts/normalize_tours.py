from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_INPUT = DATA_DIR / "tour-crawl-normalized.json"


CATEGORY_RULES = (
    ("tour-ba-na-hills", ("ba na", "bana", "golden bridge", "cau vang")),
    ("tour-hoi-an", ("hoi an", "hoian", "ancient town", "lantern", "basket boat", "coconut forest", "cam thanh")),
    ("tour-hue", ("hue", "imperial", "citadel", "khai dinh", "minh mang", "tu duc", "perfume river")),
    ("tour-bien-dao", ("cu lao cham", "cham island", "snorkeling", "diving", "beach", "island", "sea")),
    ("tour-am-thuc", ("food", "cuisine", "cooking", "street food", "restaurant", "dinner", "lunch")),
    ("tour-tam-linh", ("pagoda", "temple", "linh ung", "my son", "sanctuary", "marble mountains")),
    ("tour-mao-hiem", ("trek", "trekking", "adventure", "jeep", "motorbike", "kayak", "bike", "cycling")),
    ("tour-nghi-duong", ("wellness", "spa", "relax", "resort", "hot spring", "than tai")),
    ("tour-trong-ngay", ("half day", "full day", "1 day", "one day", "day trip", "daily")),
)

LOCATION_RULES = {
    "Da Nang": ("da nang", "danang", "dragon bridge", "marble mountains", "son tra", "my khe", "ba na"),
    "Hoi An": ("hoi an", "hoian", "ancient town", "cam thanh", "coconut forest", "basket boat", "lantern"),
    "Hue": ("hue", "imperial", "citadel", "khai dinh", "minh mang", "tu duc", "perfume river", "thien mu"),
    "Ba Na Hills": ("ba na", "bana", "golden bridge", "cau vang"),
    "My Son": ("my son", "sanctuary"),
    "Cu Lao Cham": ("cu lao cham", "cham island"),
    "Marble Mountains": ("marble mountains", "ngu hanh son"),
    "Son Tra": ("son tra", "monkey mountain", "linh ung"),
}

NON_TOUR_URL_KEYWORDS = (
    "/blog/",
    "/tag/",
    "/category/",
    "/categories/",
    "/tour-category/",
    "guide",
    "things-to-do",
    "best-time",
    "restaurants",
    "coffee-shops",
    "weather",
    "festival",
    "travel-guide",
    "complete-guide",
    "ultimate-guide",
)

NON_TOUR_TITLE_RE = re.compile(
    r"\b("
    r"\d+\s+best|best\s+\d+|top\s+\d+|things\s+to\s+do|must\s+know|"
    r"guide|travel\s+guide|complete\s+guide|ultimate\s+guide|"
    r"best\s+time|weather|restaurant|coffee\s+shop|festival|"
    r"where\s+is|how\s+long"
    r")\b",
    re.IGNORECASE,
)

OUT_OF_SCOPE_KEYWORDS = (
    "saigon",
    "ho chi minh",
    "cu chi",
    "mekong",
    "can tho",
    "ninh binh",
    "hanoi",
    "ha noi",
    "an giang",
    "cambodia",
    "da lat",
    "dalat",
    "north vietnam",
    "south vietnam",
    "phu quoc",
    "sapa",
)

CENTRAL_VIETNAM_KEYWORDS = (
    "da nang",
    "danang",
    "hoi an",
    "hoian",
    "hue",
    "ba na",
    "bana",
    "my son",
    "cham island",
    "cu lao cham",
    "marble",
    "son tra",
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--output-prefix", default="tour-staging")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.is_absolute():
        input_path = ROOT / input_path
    output = DATA_DIR / f"{args.output_prefix}.json"
    report_output = DATA_DIR / f"{args.output_prefix}-report.json"

    items = json.loads(input_path.read_text(encoding="utf-8"))
    staging = []
    rejected = []

    for item in items:
        normalized = normalize_item(item)
        if normalized["quality"]["usable"]:
            staging.append(normalized)
        else:
            rejected.append(normalized)

    staging = dedupe_by_slug(staging)
    report = build_report(items, staging, rejected, input_path, output)

    output.write_text(json.dumps(staging, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report_output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


def normalize_item(item: dict[str, Any]) -> dict[str, Any]:
    name = trim_name(item.get("tourName") or "")
    text = " ".join(
        [
            name,
            item.get("summary") or "",
            " ".join(item.get("destination") or []),
            " ".join(item.get("itinerary") or []),
            " ".join(item.get("highlights") or []),
            item.get("sourceUrl") or "",
        ]
    )
    images = normalize_images(item.get("images") or [])
    price = parse_price(item.get("price"))
    category_slug = infer_category(text)
    destination_names = infer_locations(text, item.get("destination") or [])
    itinerary = normalize_lines(item.get("itinerary") or [], max_items=10)
    inclusions = normalize_lines(item.get("includedServices") or [], max_items=10)
    exclusions = normalize_lines(item.get("excludedServices") or [], max_items=10)
    tour_signal_score = score_tour_detail_signals(item, text, price, itinerary, inclusions, exclusions)

    quality_reasons = []
    if len(name) < 8:
        quality_reasons.append("short_or_missing_name")
    if not item.get("sourceUrl"):
        quality_reasons.append("missing_source_url")
    if not category_slug:
        quality_reasons.append("missing_category")
    if price is None:
        quality_reasons.append("missing_or_unparsed_price")
    elif price <= 0:
        quality_reasons.append("placeholder_or_zero_price")
    if not item.get("duration"):
        quality_reasons.append("missing_duration")
    if not images:
        quality_reasons.append("missing_images")
    if not destination_names:
        quality_reasons.append("missing_destination")
    if is_probably_non_tour_page(item, name, text, tour_signal_score):
        quality_reasons.append("not_tour_detail_page")
    if is_out_of_scope_destination(name, item.get("sourceUrl") or ""):
        quality_reasons.append("out_of_scope_destination")
    if tour_signal_score < 3:
        quality_reasons.append("weak_tour_detail_signals")

    blocking_reasons = {
        "short_or_missing_name",
        "missing_source_url",
        "not_tour_detail_page",
        "out_of_scope_destination",
        "placeholder_or_zero_price",
        "weak_tour_detail_signals",
    }
    usable = not any(reason in quality_reasons for reason in blocking_reasons) and bool(category_slug)

    return {
        "name": name,
        "slug": unique_source_slug(item.get("sourceName") or "source", item.get("slug") or slugify(name)),
        "tour_category_slug": category_slug,
        "destination_names": destination_names,
        "description": rewrite_description(item, destination_names),
        "short_desc": rewrite_short_desc(item, destination_names),
        "itinerary": itinerary,
        "inclusions": inclusions,
        "exclusions": exclusions,
        "price_adult": price if price is not None else 0,
        "price_raw": item.get("price"),
        "price_child": 0,
        "price_infant": 0,
        "discount_percent": 0,
        "duration": clean_text(item.get("duration") or "")[:50] or None,
        "start_time": None,
        "meeting_point": clean_text(item.get("departureLocation") or "")[:255] or None,
        "max_people": 30,
        "min_people": 1,
        "thumbnail": images[0]["url"][:255] if images else None,
        "images": [image["url"] for image in images],
        "image_candidates": images,
        "status": "inactive",
        "booking_availability": "open",
        "is_featured": False,
        "is_hot": False,
        "source": {
            "name": item.get("sourceName"),
            "url": item.get("sourceUrl"),
            "crawledAt": item.get("crawledAt"),
        },
        "quality": {
            "usable": usable,
            "reasons": quality_reasons,
            "tourSignalScore": tour_signal_score,
        },
    }


def trim_name(value: str) -> str:
    value = clean_text(value)
    value = re.sub(r"\s*[-|]\s*(Daco|Hoi An Day Trip|VM Travel|Venus).*?$", "", value, flags=re.IGNORECASE)
    return value[:200]


def infer_category(text: str) -> str:
    lower = text.lower()
    for slug, keywords in CATEGORY_RULES:
        if any(keyword in lower for keyword in keywords):
            return slug
    return "tour-trong-ngay"


def infer_locations(text: str, existing: list[str]) -> list[str]:
    lower = text.lower()
    found = []
    for value in existing:
        if value and value not in found:
            found.append(value)
    for label, keywords in LOCATION_RULES.items():
        if any(keyword in lower for keyword in keywords) and label not in found:
            found.append(label)
    return found


def score_tour_detail_signals(
    item: dict[str, Any],
    text: str,
    price: float | None,
    itinerary: list[str],
    inclusions: list[str],
    exclusions: list[str],
) -> int:
    source_path = urlparse(item.get("sourceUrl") or "").path.lower()
    lower = text.lower()
    score = 0
    if price is not None:
        score += 2
    if item.get("duration"):
        score += 1
    if itinerary:
        score += 2
    if inclusions or exclusions:
        score += 2
    if "/tour" in source_path and "/tour-category/" not in source_path:
        score += 1
    if any(keyword in lower for keyword in ("book now", "per person", "pickup", "pick up", "tour includes", "itinerary")):
        score += 1
    return score


def is_probably_non_tour_page(item: dict[str, Any], name: str, text: str, tour_signal_score: int) -> bool:
    source_url = item.get("sourceUrl") or ""
    path = urlparse(source_url).path.lower()
    lower_name = name.lower()
    lower_text = text.lower()
    product_markers = (
        "/tour/",
        " tour",
        "tour ",
        " day trip",
        "excursion",
        "group package",
    )
    non_product_phrases = (
        "tour operator",
        "travel agency",
        "destinations",
        "ticket price",
        "summary of the best",
        "description:",
        "private transfer",
        "free entrance",
        "cheapest tourist",
        "you should choose",
        "visa extension",
        "things to see",
        "attractive destinations",
        "where to find",
        "operating hours",
    )

    if path in ("", "/"):
        return True
    if "currency=" in source_url.lower():
        return True
    if any(token in path for token in ("/categories/", "/duration/", "/destinations/", "/vacation-package-to-vietnam/")):
        return True
    if any(phrase in lower_name for phrase in non_product_phrases):
        return True
    if not any(marker in f"{path} {lower_name}" for marker in product_markers):
        return True
    if lower_name.startswith("best ") and "/tour/" not in path:
        return True
    if any(keyword in path for keyword in NON_TOUR_URL_KEYWORDS) and tour_signal_score < 7:
        return True
    if NON_TOUR_TITLE_RE.search(lower_name) and tour_signal_score < 7:
        return True
    if re.search(r"^\d+\s+(best|top)\b", lower_name):
        return True
    if any(phrase in lower_name for phrase in ("things to do", "must know", "travel guide", "complete guide", "ultimate guide")):
        return True
    if "blog" in lower_text and tour_signal_score < 7:
        return True
    return False


def is_out_of_scope_destination(name: str, text: str) -> bool:
    lower = f"{name} {text}".lower()
    has_out_of_scope = any(keyword in lower for keyword in OUT_OF_SCOPE_KEYWORDS)
    has_central = any(keyword in lower for keyword in CENTRAL_VIETNAM_KEYWORDS)
    return has_out_of_scope and not has_central


def parse_price(value: Any) -> float | None:
    if not value:
        return None
    text = str(value).lower().strip()
    if any(token in text for token in ("vnd", "vnđ", "đ")):
        grouped_vnd = re.search(r"(\d{1,3}(?:[.,]\d{3})+)", text)
        if grouped_vnd:
            return float(re.sub(r"[.,]", "", grouped_vnd.group(1)))
        plain_vnd = re.search(r"(\d{4,})", text)
        if plain_vnd:
            return float(plain_vnd.group(1))
    text = text.replace(",", "")
    usd = re.search(r"\$?\s*(\d+(?:\.\d+)?)\s*(?:usd|us\$)?", text)
    if "$" in text or "usd" in text or "us$" in text:
        if usd:
            return round(float(usd.group(1)) * 25000, 2)
    vnd = re.search(r"(\d{4,})\s*(?:vnd|vnđ|đ|d)?", text)
    if vnd:
        return float(vnd.group(1))
    return None


def normalize_images(images: list[dict[str, Any]]) -> list[dict[str, str]]:
    normalized = []
    seen = set()
    for image in images:
        url = clean_text(image.get("url") or "")
        if not url or url in seen or url.startswith("data:"):
            continue
        if len(url) > 2000:
            continue
        normalized.append({"url": url, "alt": clean_text(image.get("alt") or "")[:255]})
        seen.add(url)
        if len(normalized) >= 8:
            break
    return normalized


def normalize_lines(lines: list[str], max_items: int) -> list[str]:
    normalized = []
    for line in lines:
        value = clean_text(line)
        if len(value) < 5 or value in normalized:
            continue
        normalized.append(value[:280])
        if len(normalized) >= max_items:
            break
    return normalized


def rewrite_short_desc(item: dict[str, Any], destinations: list[str]) -> str:
    name = trim_name(item.get("tourName") or "")
    destination_text = ", ".join(destinations) or "mien Trung"
    duration = item.get("duration")
    if duration:
        return f"Tour {destination_text} trong {duration}, duoc tong hop tu nguon cong khai va can duyet noi dung truoc khi mo ban."[:500]
    return f"Tour {destination_text} duoc tong hop tu nguon cong khai va can duyet noi dung truoc khi mo ban: {name}."[:500]


def rewrite_description(item: dict[str, Any], destinations: list[str]) -> str:
    parts = [
        rewrite_short_desc(item, destinations),
        "Du lieu nay duoc chuan hoa tu website operator va giu lai source_url de doi chieu.",
    ]
    if item.get("highlights"):
        parts.append("Diem noi bat gom: " + "; ".join(normalize_lines(item["highlights"], 4)) + ".")
    return " ".join(parts)


def unique_source_slug(source: str, slug: str) -> str:
    return f"{slugify(source)}-{slugify(slug)}"[:220]


def dedupe_by_slug(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen = {}
    for item in items:
        slug = item["slug"]
        if slug not in seen:
            seen[slug] = item
            continue
        existing = seen[slug]
        if quality_score(item) > quality_score(existing):
            seen[slug] = item
    return sorted(seen.values(), key=lambda value: (value["source"]["name"] or "", value["name"]))


def quality_score(item: dict[str, Any]) -> int:
    score = 0
    if item["price_adult"] > 0:
        score += 20
    if item["duration"]:
        score += 20
    if item["images"]:
        score += 20
    if item["itinerary"]:
        score += 20
    if item["destination_names"]:
        score += 20
    return score


def build_report(
    original: list[dict[str, Any]],
    staging: list[dict[str, Any]],
    rejected: list[dict[str, Any]],
    input_path: Path,
    output_path: Path,
) -> dict[str, Any]:
    return {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "input": {
            "file": str(input_path.relative_to(ROOT)).replace("\\", "/"),
            "total": len(original),
        },
        "output": {
            "file": str(output_path.relative_to(ROOT)).replace("\\", "/"),
            "staging": len(staging),
            "rejected": len(rejected),
        },
        "coverage": {
            "withPrice": sum(1 for item in staging if item["price_adult"] > 0),
            "withDuration": sum(1 for item in staging if item["duration"]),
            "withImages": sum(1 for item in staging if item["images"]),
            "withItinerary": sum(1 for item in staging if item["itinerary"]),
            "withDestinations": sum(1 for item in staging if item["destination_names"]),
        },
        "byCategory": count_by(staging, "tour_category_slug"),
        "bySource": count_by(staging, lambda item: item["source"]["name"] or "unknown"),
        "rejectedReasons": count_reasons(rejected),
        "policy": {
            "status": "inactive",
            "images": "candidate_urls_only",
            "longDescriptions": "rewritten_summary_not_copied",
            "publish": "manual_review_required",
        },
    }


def count_by(items: list[dict[str, Any]], key_or_func: Any) -> dict[str, int]:
    result: dict[str, int] = {}
    for item in items:
        key = key_or_func(item) if callable(key_or_func) else item[key_or_func]
        result[str(key)] = result.get(str(key), 0) + 1
    return dict(sorted(result.items()))


def count_reasons(items: list[dict[str, Any]]) -> dict[str, int]:
    result: dict[str, int] = {}
    for item in items:
        for reason in item["quality"]["reasons"]:
            result[reason] = result.get(reason, 0) + 1
    return dict(sorted(result.items(), key=lambda pair: pair[1], reverse=True))


def slugify(value: str) -> str:
    text = value.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "tour"


def clean_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


if __name__ == "__main__":
    main()
