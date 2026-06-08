from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PATHS = (
    ROOT / "data",
    ROOT.parent / "database-seeders",
)
REPORT_DIR = ROOT.parent / "data-center" / "reports"
VIETNAMESE_DIACRITICS = re.compile(
    r"[ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠ"
    r"àáâãèéêìíòóôõùúăđĩũơ"
    r"ƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀẾỂỄỆ"
    r"ỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪỬỮỰ"
    r"ỲỴỶỸÝ"
    r"ưăạảấầẩẫậắằẳẵặẹẻẽềếểễệ"
    r"ỉịọỏốồổỗộớờởỡợụủứừửữự"
    r"ỳỵỷỹý]"
)
STRONG_ASCII_VIETNAMESE = {
    "bao",
    "ban",
    "bien",
    "bieu",
    "can",
    "cang",
    "cap",
    "chieu",
    "chi",
    "chon",
    "chuyen",
    "cong",
    "cua",
    "danh",
    "dat",
    "dich",
    "diem",
    "dieu",
    "doi",
    "don",
    "du",
    "dua",
    "duoc",
    "duong",
    "gia",
    "gio",
    "gioi",
    "gom",
    "hanh",
    "hoat",
    "huong",
    "khach",
    "kham",
    "khong",
    "khu",
    "lich",
    "lieu",
    "luu",
    "mien",
    "mo",
    "mua",
    "ngam",
    "ngay",
    "nghiem",
    "nguoi",
    "nguon",
    "noi",
    "phong",
    "quan",
    "quy",
    "san",
    "thanh",
    "tham",
    "thoi",
    "thong",
    "thu",
    "tieng",
    "tinh",
    "tong",
    "trai",
    "trinh",
    "trong",
    "tu",
    "van",
    "viet",
    "voi",
    "vu",
}
ASCII_VIETNAMESE_PHRASES = (
    "duoc thu thap",
    "duoc tong hop",
    "can duyet",
    "du lieu nay",
    "diem du lich",
    "dich vu",
    "gio mo cua",
    "huong dan",
    "kham pha",
    "khach san",
    "lich trinh",
    "mien trung",
    "nguoi dung",
    "noi dung",
    "thanh pho",
    "tham quan",
    "thong tin",
    "tieng viet",
    "trai nghiem",
)
DISPLAY_KEYS = {
    "address",
    "answer",
    "content",
    "description",
    "district",
    "duration",
    "excerpt",
    "exclusions",
    "highlights",
    "inclusions",
    "itinerary",
    "meeting_point",
    "name",
    "question",
    "short_desc",
    "shortdescription",
    "summary",
    "task",
    "title",
}
SKIP_KEYS = {
    "alt",
    "cloudinary_public_id",
    "file",
    "filename",
    "local_file",
    "local_path",
    "provider_page_url",
    "secure_url",
    "slug",
    "source_url",
    "thumbnail",
    "url",
}
SUPPORTED = {".json", ".csv", ".sql"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="*", type=Path)
    parser.add_argument("--output-prefix", default="vietnamese-diacritics-audit-2026-06-07")
    parser.add_argument("--max-examples", type=int, default=250)
    args = parser.parse_args()

    paths = args.paths or list(DEFAULT_PATHS)
    files = discover_files(paths)
    totals = Counter()
    by_file: dict[str, Counter[str]] = defaultdict(Counter)
    examples: list[dict[str, Any]] = []

    for path in files:
        try:
            if path.suffix.lower() == ".json":
                values = scan_json(path)
            elif path.suffix.lower() == ".csv":
                values = scan_csv(path)
            else:
                values = scan_sql(path)
            for field, value in values:
                classification = classify(value)
                totals[classification] += 1
                by_file[str(path)][classification] += 1
                if (
                    classification == "vietnamese_unaccented"
                    and len(examples) < args.max_examples
                ):
                    examples.append(
                        {
                            "file": str(path),
                            "field": field,
                            "value": clean(value)[:500],
                        }
                    )
        except Exception as exc:  # noqa: BLE001 - audit must continue.
            totals["file_errors"] += 1
            examples.append(
                {
                    "file": str(path),
                    "field": "__file_error__",
                    "value": f"{type(exc).__name__}: {exc}",
                }
            )

    ranked_files = [
        {
            "file": file,
            **counts,
        }
        for file, counts in sorted(
            by_file.items(),
            key=lambda item: item[1]["vietnamese_unaccented"],
            reverse=True,
        )
        if counts["vietnamese_unaccented"] > 0
    ]
    report = {
        "scope": [str(path) for path in paths],
        "filesScanned": len(files),
        "totals": dict(totals),
        "filesWithUnaccentedVietnamese": len(ranked_files),
        "topFiles": ranked_files[:100],
        "examples": examples,
        "policy": {
            "slugUrlTechnicalAsciiAllowed": True,
            "englishSourceContentAllowed": True,
            "displayVietnameseShouldUseDiacritics": True,
            "automaticMutationPerformed": False,
        },
    }

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    json_output = REPORT_DIR / f"{args.output_prefix}.json"
    csv_output = REPORT_DIR / f"{args.output_prefix}.csv"
    json_output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_csv(csv_output, ranked_files)
    print(
        json.dumps(
            {
                "filesScanned": len(files),
                "totals": dict(totals),
                "filesWithUnaccentedVietnamese": len(ranked_files),
                "json": str(json_output),
                "csv": str(csv_output),
            },
            ensure_ascii=True,
            indent=2,
        )
    )


def discover_files(paths: Iterable[Path]) -> list[Path]:
    files: set[Path] = set()
    for raw_path in paths:
        path = raw_path if raw_path.is_absolute() else ROOT / raw_path
        if path.is_file() and path.suffix.lower() in SUPPORTED:
            files.add(path)
        elif path.is_dir():
            files.update(
                child
                for child in path.rglob("*")
                if child.is_file()
                and child.suffix.lower() in SUPPORTED
                and child.stat().st_size <= 100_000_000
            )
    return sorted(files)


def scan_json(path: Path) -> Iterable[tuple[str, str]]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    yield from walk_json(payload)


def walk_json(value: Any, key: str = "") -> Iterable[tuple[str, str]]:
    normalized_key = key.lower()
    if isinstance(value, dict):
        for child_key, child_value in value.items():
            if child_key.lower() in SKIP_KEYS:
                continue
            yield from walk_json(child_value, child_key)
    elif isinstance(value, list):
        for child in value:
            yield from walk_json(child, key)
    elif isinstance(value, str):
        if normalized_key in DISPLAY_KEYS or len(value.split()) >= 4:
            yield key, value


def scan_csv(path: Path) -> Iterable[tuple[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            for key, value in row.items():
                if (
                    value
                    and key
                    and key.lower() not in SKIP_KEYS
                    and (key.lower() in DISPLAY_KEYS or len(value.split()) >= 4)
                ):
                    yield key, value


def scan_sql(path: Path) -> Iterable[tuple[str, str]]:
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    for match in re.finditer(r"'((?:''|[^'])*)'", text):
        value = match.group(1).replace("''", "'")
        if len(value.split()) >= 2:
            yield "sql_literal", value


def classify(value: str) -> str:
    value = clean(value)
    if not value:
        return "empty"
    if VIETNAMESE_DIACRITICS.search(value):
        return "vietnamese_accented"
    lower = value.lower()
    if any(phrase in lower for phrase in ASCII_VIETNAMESE_PHRASES):
        return "vietnamese_unaccented"
    tokens = re.findall(r"[a-z]+", lower)
    score = sum(token in STRONG_ASCII_VIETNAMESE for token in tokens)
    if score >= 3 and score / max(len(tokens), 1) >= 0.18:
        return "vietnamese_unaccented"
    return "other_or_english"


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields = [
        "file",
        "vietnamese_unaccented",
        "vietnamese_accented",
        "other_or_english",
        "empty",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
