from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
SEED_OUTPUT = ROOT.parent / "database-seeders" / "21_approve_overpass_clean_batch1.sql"
REVIEW_OUTPUT = DATA_DIR / "overpass-approval-batch1-review.csv"
REPORT_OUTPUT = DATA_DIR / "overpass-approval-batch1-report.json"


def main() -> None:
    items = load_json(DATA_DIR / "overpass-danang-pois-enriched.json")
    approved = [item for item in items if is_approval_candidate(item)]
    pending = [item for item in items if item not in approved]

    SEED_OUTPUT.write_text(render_sql(approved), encoding="utf-8")
    write_review_csv(approved)

    report = {
        "output": str(SEED_OUTPUT),
        "reviewCsv": str(REVIEW_OUTPUT),
        "sourceFile": str(DATA_DIR / "overpass-danang-pois-enriched.json"),
        "policy": "Approve only high-priority enriched Overpass items with images and no qualityReasons. Skip duplicates at SQL runtime.",
        "approved": summarize(approved),
        "pending": summarize(pending),
    }
    REPORT_OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=True, indent=2))


def is_approval_candidate(item: dict[str, Any]) -> bool:
    normalized = item.get("normalizedPayload") or {}
    return (
        item.get("sourceName") == "overpass-danang-pois"
        and item.get("status") == "pending_review"
        and item.get("entityType") in {"location", "restaurant", "hotel"}
        and normalized.get("reviewPriority") == "high"
        and bool(normalized.get("imageUrls"))
        and not normalized.get("qualityReasons")
        and bool(item.get("externalId"))
    )


def render_sql(items: list[dict[str, Any]]) -> str:
    external_ids = [item["externalId"] for item in items]
    external_id_values = ",\n".join(f"        ({sql_string(external_id)})" for external_id in external_ids)
    return "\n".join(
        [
            "-- DanangTrip Overpass clean batch approval",
            "-- FILE: 21_approve_overpass_clean_batch1.sql",
            "-- Purpose: approve only clean high-priority Overpass staging items before optional publish.",
            "-- Required before running:",
            "--   1. 11_crawl_staging_tables.sql",
            "--   2. 12_overpass_danang_pois_seed.sql",
            "--   3. 13_overpass_quality_review_seed.sql",
            "--   4. 14_pexels_image_enrichment_seed.sql",
            "--   5. 15_crawl_duplicate_matching_seed.sql",
            "-- This file does not insert into production locations. Run 16 only after this if you want to publish approved rows as inactive.",
            "",
            "WITH source_row AS (",
            "    SELECT id FROM crawl_sources WHERE name = 'overpass-danang-pois'",
            "),",
            "approved_external_ids(external_id) AS (",
            "    VALUES",
            external_id_values,
            "),",
            "updated AS (",
            "    UPDATE crawl_items ci",
            "    SET status = 'approved',",
            "        reviewed_at = NOW(),",
            "        normalized_payload = jsonb_set(",
            "            jsonb_set(",
            "                COALESCE(ci.normalized_payload, '{}'::jsonb),",
            "                '{approvalBatch}',",
            "                to_jsonb('overpass-clean-batch1'::text),",
            "                true",
            "            ),",
            "            '{approvalPolicy}',",
            "            to_jsonb('high_priority_with_images_no_quality_reasons'::text),",
            "            true",
            "        ),",
            "        updated_at = NOW()",
            "    FROM source_row s",
            "    JOIN approved_external_ids a ON a.external_id = ci.external_id",
            "    WHERE ci.source_id = s.id",
            "      AND ci.status = 'pending_review'",
            "      AND ci.duplicate_source_id IS NULL",
            "      AND ci.entity_type IN ('location', 'restaurant', 'hotel')",
            "    RETURNING ci.id, ci.entity_type",
            ")",
            "INSERT INTO crawl_logs (job_id, level, message, context_json, created_at)",
            "SELECT j.id,",
            "       'INFO',",
            "       'Approved Overpass clean batch 1',",
            "       jsonb_build_object(",
            "           'source', 'overpass-danang-pois',",
            "           'approval_batch', 'overpass-clean-batch1',",
            "           'approved_count', (SELECT count(*) FROM updated),",
            "           'location_count', (SELECT count(*) FROM updated WHERE entity_type = 'location'),",
            "           'restaurant_count', (SELECT count(*) FROM updated WHERE entity_type = 'restaurant'),",
            "           'hotel_count', (SELECT count(*) FROM updated WHERE entity_type = 'hotel'),",
            "           'note', 'Duplicates are skipped by duplicate_source_id IS NULL. Rows are still staging until publish seed 16 runs.'",
            "       ),",
            "       NOW()",
            "FROM crawl_jobs j",
            "JOIN source_row s ON s.id = j.source_id",
            "ORDER BY j.id DESC",
            "LIMIT 1;",
            "",
        ]
    )


def write_review_csv(items: list[dict[str, Any]]) -> None:
    with REVIEW_OUTPUT.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "entity_type",
                "external_id",
                "name",
                "category_slug",
                "district",
                "address",
                "latitude",
                "longitude",
                "image_count",
                "source_url",
            ],
        )
        writer.writeheader()
        for item in items:
            normalized = item.get("normalizedPayload") or {}
            writer.writerow(
                {
                    "entity_type": item.get("entityType"),
                    "external_id": item.get("externalId"),
                    "name": normalized.get("name"),
                    "category_slug": normalized.get("categorySlug"),
                    "district": normalized.get("district"),
                    "address": normalized.get("address"),
                    "latitude": normalized.get("latitude"),
                    "longitude": normalized.get("longitude"),
                    "image_count": len(normalized.get("imageUrls") or []),
                    "source_url": item.get("sourceUrl"),
                }
            )


def summarize(items: list[dict[str, Any]]) -> dict[str, Any]:
    by_entity: dict[str, int] = {}
    by_category: dict[str, int] = {}
    for item in items:
        entity = item.get("entityType") or "unknown"
        category = (item.get("normalizedPayload") or {}).get("categorySlug") or "unknown"
        by_entity[entity] = by_entity.get(entity, 0) + 1
        by_category[category] = by_category.get(category, 0) + 1
    return {
        "total": len(items),
        "byEntity": dict(sorted(by_entity.items())),
        "byCategory": dict(sorted(by_category.items())),
    }


def sql_string(value: Any) -> str:
    return "'" + str(value).replace("'", "''") + "'"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
