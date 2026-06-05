from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("inputs", nargs="+")
    args = parser.parse_args()

    merged: dict[str, dict[str, Any]] = {}
    for input_path in args.inputs:
        path = Path(input_path)
        if not path.is_absolute():
            path = ROOT / path
        for item in json.loads(path.read_text(encoding="utf-8")):
            key = item.get("sourceUrl") or f"{item.get('sourceName')}::{item.get('slug')}"
            if key not in merged or quality_score(item) > quality_score(merged[key]):
                merged[key] = item

    output = Path(args.output)
    if not output.is_absolute():
        output = ROOT / output
    items = sorted(merged.values(), key=lambda item: (item.get("sourceName") or "", item.get("tourName") or ""))
    output.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "count": len(items)}, ensure_ascii=True, indent=2))


def quality_score(item: dict[str, Any]) -> int:
    score = 0
    if item.get("price"):
        score += 20
    if item.get("duration"):
        score += 20
    if item.get("images"):
        score += 20
    if item.get("itinerary"):
        score += 20
    if item.get("includedServices") or item.get("excludedServices"):
        score += 10
    if item.get("destination"):
        score += 10
    return score


if __name__ == "__main__":
    main()
