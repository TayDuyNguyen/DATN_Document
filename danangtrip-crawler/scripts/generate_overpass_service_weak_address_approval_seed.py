from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
SEED_OUTPUT = ROOT.parent / "database-seeders" / "24_approve_overpass_weak_address_services.sql"
REVIEW_OUTPUT = DATA_DIR / "overpass-approval-batch3-weak-address-services-review.csv"
REPORT_OUTPUT = DATA_DIR / "overpass-approval-batch3-weak-address-services-report.json"

SIGNAL_KEYS = ["website", "contact:website", "phone", "contact:phone", "opening_hours", "cuisine"]
GENERIC_NAMES = {"24 7", "kfc", "lotteria", "home", "hotel", "cafe", "restaurant"}


def main() -> None:
    items = load_json(DATA_DIR / "overpass-danang-pois-enriched.json")
    candidates = [item for item in items if is_candidate(item)]
    approved = [item for item in candidates if should_approve(item)]
    pending = [item for item in candidates if item not in approved]

    SEED_OUTPUT.write_text(render_sql(approved), encoding="utf-8")
    write_review_csv(approved, pending)

    report = {
        "output": str(SEED_OUTPUT),
        "reviewCsv": str(REVIEW_OUTPUT),
        "sourceFile": str(DATA_DIR / "overpass-danang-pois-enriched.json"),
        "policy": "Approve restaurant/hotel weak-address records only when they have at least two operational/source signals.",
        "candidateCount": len(candidates),
        "approved": summarize(approved),
        "pending": summarize(pending),
    }
    REPORT_OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=True, indent=2))


def is_candidate(item: dict[str, Any]) -> bool:
    normalized = item.get("normalizedPayload") or {}
    return (
        item.get("sourceName") == "overpass-danang-pois"
        and item.get("status") == "pending_review"
        and item.get("entityType") in {"restaurant", "hotel"}
        and (normalized.get("qualityReasons") or []) == ["weak_address"]
        and bool(normalized.get("imageUrls"))
        and bool(item.get("externalId"))
    )


def should_approve(item: dict[str, Any]) -> bool:
    normalized = item.get("normalizedPayload") or {}
    name = str(normalized.get("name") or "").strip().lower()
    if name in GENERIC_NAMES:
        return False
    return signal_count(item) >= 2


def signal_count(item: dict[str, Any]) -> int:
    tags = ((item.get("rawPayload") or {}).get("osmTags") or {})
    return sum(1 for key in SIGNAL_KEYS if tags.get(key))


def render_sql(items: list[dict[str, Any]]) -> str:
    external_id_values = ",\n".join(f"        ({sql_string(item['externalId'])})" for item in items)
    return "\n".join(
        [
            "-- DanangTrip Overpass weak-address service approval",
            "-- FILE: 24_approve_overpass_weak_address_services.sql",
            "-- Purpose: approve selected restaurants/hotels that only failed weak_address but have strong operational signals.",
            "-- Required before running:",
            "--   1. 11_crawl_staging_tables.sql",
            "--   2. 12_overpass_danang_pois_seed.sql",
            "--   3. 13_overpass_quality_review_seed.sql",
            "--   4. 14_pexels_image_enrichment_seed.sql",
            "--   5. 15_crawl_duplicate_matching_seed.sql",
            "-- This file only updates crawl_items to approved. Run 16 after approval if publishing is desired.",
            "",
            "WITH source_row AS (",
            "    SELECT id FROM crawl_sources WHERE name = 'overpass-danang-pois'",
            "),",
            "approved_external_ids(external_id) AS (",
            "    VALUES",
            external_id_values or "        (NULL)",
            "),",
            "updated AS (",
            "    UPDATE crawl_items ci",
            "    SET status = 'approved',",
            "        reviewed_at = NOW(),",
            "        normalized_payload = jsonb_set(",
            "            jsonb_set(",
            "                COALESCE(ci.normalized_payload, '{}'::jsonb),",
            "                '{approvalBatch}',",
            "                to_jsonb('overpass-weak-address-services'::text),",
            "                true",
            "            ),",
            "            '{approvalPolicy}',",
            "            to_jsonb('services_with_two_or_more_operational_signals'::text),",
            "            true",
            "        ),",
            "        updated_at = NOW()",
            "    FROM source_row s",
            "    JOIN approved_external_ids a ON a.external_id = ci.external_id",
            "    WHERE ci.source_id = s.id",
            "      AND ci.status = 'pending_review'",
            "      AND ci.duplicate_source_id IS NULL",
            "      AND ci.entity_type IN ('restaurant', 'hotel')",
            "    RETURNING ci.id, ci.entity_type",
            ")",
            "INSERT INTO crawl_logs (job_id, level, message, context_json, created_at)",
            "SELECT j.id,",
            "       'INFO',",
            "       'Approved Overpass weak-address service batch',",
            "       jsonb_build_object(",
            "           'source', 'overpass-danang-pois',",
            "           'approval_batch', 'overpass-weak-address-services',",
            "           'approved_count', (SELECT count(*) FROM updated),",
            "           'restaurant_count', (SELECT count(*) FROM updated WHERE entity_type = 'restaurant'),",
            "           'hotel_count', (SELECT count(*) FROM updated WHERE entity_type = 'hotel'),",
            "           'note', 'Only service records with at least two operational/source signals are approved.'",
            "       ),",
            "       NOW()",
            "FROM crawl_jobs j",
            "JOIN source_row s ON s.id = j.source_id",
            "ORDER BY j.id DESC",
            "LIMIT 1;",
            "",
        ]
    )


def write_review_csv(approved: list[dict[str, Any]], pending: list[dict[str, Any]]) -> None:
    rows = []
    for approve, items in [(True, approved), (False, pending)]:
        for item in items:
            normalized = item.get("normalizedPayload") or {}
            tags = ((item.get("rawPayload") or {}).get("osmTags") or {})
            rows.append(
                {
                    "approve_for_seed": approve,
                    "entity_type": item.get("entityType"),
                    "external_id": item.get("externalId"),
                    "name": normalized.get("name"),
                    "category_slug": normalized.get("categorySlug"),
                    "address": normalized.get("address"),
                    "latitude": normalized.get("latitude"),
                    "longitude": normalized.get("longitude"),
                    "quality_score": normalized.get("qualityScore"),
                    "signal_count": signal_count(item),
                    "signals": ", ".join(key for key in SIGNAL_KEYS if tags.get(key)),
                    "image_count": len(normalized.get("imageUrls") or []),
                    "source_url": item.get("sourceUrl"),
                }
            )
    with REVIEW_OUTPUT.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()) if rows else [])
        if rows:
            writer.writeheader()
            writer.writerows(rows)


def summarize(items: list[dict[str, Any]]) -> dict[str, Any]:
    by_entity: dict[str, int] = {}
    by_category: dict[str, int] = {}
    names = []
    for item in items:
        normalized = item.get("normalizedPayload") or {}
        entity = item.get("entityType") or "unknown"
        category = normalized.get("categorySlug") or "unknown"
        by_entity[entity] = by_entity.get(entity, 0) + 1
        by_category[category] = by_category.get(category, 0) + 1
        names.append(normalized.get("name"))
    return {
        "total": len(items),
        "byEntity": dict(sorted(by_entity.items())),
        "byCategory": dict(sorted(by_category.items())),
        "names": names,
    }


def sql_string(value: Any) -> str:
    if value is None:
        return "NULL"
    return "'" + str(value).replace("'", "''") + "'"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
