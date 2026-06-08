from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PATHS = (
    ROOT / "data",
    ROOT.parent / "database-seeders",
    ROOT.parent / "data-center",
)
REPORT_DIR = ROOT.parent / "data-center" / "reports"
TEXT_EXTENSIONS = {
    ".csv",
    ".json",
    ".md",
    ".php",
    ".py",
    ".sql",
    ".txt",
    ".ts",
    ".js",
    ".mjs",
    ".yaml",
    ".yml",
}
SKIP_PARTS = {
    ".git",
    ".venv",
    "node_modules",
    "vendor",
    "media-assets",
}
SKIP_FILES = {
    "audit_mojibake.py",
    "audit_mojibake_db.php",
}
STRONG_PATTERNS = {
    "replacement_character": re.compile("\ufffd"),
    "utf8_as_latin1_vietnamese": re.compile(r"(?:Ã[\x80-\xBF]|áº|á»|Ä[\x80-\xBF]|Æ[\x80-\xBF])"),
    "broken_smart_punctuation": re.compile(r"(?:â€|â€™|â€œ|â€\x9d|â€“|â€”|â€¦)"),
    "broken_bom": re.compile(r"(?:ï»¿|ï¿½)"),
    "broken_emoji": re.compile(r"(?:ðŸ|ð\x9f)"),
    "c1_control": re.compile(r"[\u0080-\u009f]"),
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit text data for mojibake and invalid UTF-8.")
    parser.add_argument("paths", nargs="*", type=Path)
    parser.add_argument("--output-prefix", default=f"mojibake-audit-{datetime.now().date().isoformat()}")
    parser.add_argument("--max-examples", type=int, default=500)
    args = parser.parse_args()

    paths = tuple(args.paths) or DEFAULT_PATHS
    files = collect_files(paths)
    findings: list[dict[str, object]] = []
    invalid_utf8_files: list[dict[str, object]] = []
    counts: Counter[str] = Counter()

    for path in files:
        raw = path.read_bytes()
        try:
            text = raw.decode("utf-8-sig")
        except UnicodeDecodeError as error:
            invalid_utf8_files.append(
                {
                    "file": str(path),
                    "start": error.start,
                    "end": error.end,
                    "reason": error.reason,
                }
            )
            counts["invalid_utf8_files"] += 1
            text = raw.decode("utf-8-sig", errors="replace")

        for line_number, line in enumerate(text.splitlines(), start=1):
            for pattern_name, pattern in STRONG_PATTERNS.items():
                for match in pattern.finditer(line):
                    counts[pattern_name] += 1
                    if len(findings) < args.max_examples:
                        start = max(0, match.start() - 80)
                        end = min(len(line), match.end() + 120)
                        findings.append(
                            {
                                "file": str(path),
                                "line": line_number,
                                "type": pattern_name,
                                "match": match.group(0),
                                "context": line[start:end],
                            }
                        )

    files_with_findings = len({item["file"] for item in findings} | {item["file"] for item in invalid_utf8_files})
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scope": [str(path) for path in paths],
        "files_scanned": len(files),
        "files_with_findings": files_with_findings,
        "counts": dict(counts),
        "invalid_utf8_files": invalid_utf8_files,
        "examples": findings,
        "policy": {
            "strong_signals_only": True,
            "single_valid_characters_not_flagged": ["Â", "Ã"],
            "automatic_repair": False,
        },
    }

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    json_path = REPORT_DIR / f"{args.output_prefix}.json"
    csv_path = REPORT_DIR / f"{args.output_prefix}.csv"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_csv(csv_path, findings)
    print(
        json.dumps(
            {
                "filesScanned": len(files),
                "filesWithFindings": files_with_findings,
                "counts": dict(counts),
                "json": str(json_path),
                "csv": str(csv_path),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def collect_files(paths: tuple[Path, ...]) -> list[Path]:
    files: set[Path] = set()
    for target in paths:
        if target.is_file() and target.suffix.lower() in TEXT_EXTENSIONS:
            files.add(target.resolve())
            continue
        if not target.is_dir():
            continue
        for path in target.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in TEXT_EXTENSIONS:
                continue
            if path.name in SKIP_FILES:
                continue
            if path.name.startswith("mojibake-audit-"):
                continue
            if any(part in SKIP_PARTS for part in path.parts):
                continue
            files.add(path.resolve())
    return sorted(files)


def write_csv(path: Path, findings: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["file", "line", "type", "match", "context"])
        writer.writeheader()
        writer.writerows(findings)


if __name__ == "__main__":
    main()
