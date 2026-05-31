import fs from "node:fs";
import path from "node:path";

const root = path.resolve(".");
const inputPath = path.join(root, "data", "overpass-danang-pois.json");
const outputPath = path.resolve(root, "..", "database-seeders", "12_overpass_danang_pois_seed.sql");
const items = JSON.parse(fs.readFileSync(inputPath, "utf8"));

function sqlString(value) {
  if (value === undefined || value === null) return "NULL";
  return `'${String(value).replaceAll("'", "''")}'`;
}

function jsonb(value) {
  return `${sqlString(JSON.stringify(value))}::jsonb`;
}

const header = `-- DanangTrip Crawler Seed: Overpass Da Nang POIs
-- FILE: 12_overpass_danang_pois_seed.sql
-- Source: D:/DATN/DATN_Document/danangtrip-crawler/data/overpass-danang-pois.json
-- Generated: ${new Date().toISOString()}
-- Total items: ${items.length}
-- Notes:
--   Requires 11_crawl_staging_tables.sql to be applied first.
--   Records stay in crawl_items.status = 'pending_review'.
--   Admin review is required before publishing into production tables.
--   Text content is normalized to ASCII / Vietnamese without diacritics.

`;

const sourceConfig = {
  bbox: { south: 15.95, west: 107.95, north: 16.2, east: 108.35 },
  source: "OpenStreetMap contributors via Overpass API",
  output_file: "data/overpass-danang-pois.json",
  text_policy: "ascii_vietnamese_without_diacritics",
};

const sourceSql = `INSERT INTO crawl_sources (name, type, config_json, enabled, last_run_at, created_at, updated_at)
VALUES ('overpass-danang-pois', 'overpass_api', ${jsonb(sourceConfig)}, TRUE, NOW(), NOW(), NOW())
ON CONFLICT (name) DO UPDATE SET
  type = EXCLUDED.type,
  config_json = EXCLUDED.config_json,
  enabled = TRUE,
  last_run_at = NOW(),
  updated_at = NOW();

`;

const jobSql = `WITH source_row AS (
  SELECT id FROM crawl_sources WHERE name = 'overpass-danang-pois'
)
INSERT INTO crawl_jobs (source_id, status, started_at, finished_at, created_at, updated_at)
SELECT id, 'completed', NOW(), NOW(), NOW(), NOW() FROM source_row;

`;

const rows = items.map((item) => {
  const normalized = item.normalizedPayload ?? {};
  const raw = item.rawPayload ?? {};
  return `SELECT
  s.id AS source_id,
  j.id AS job_id,
  ${sqlString(item.entityType)} AS entity_type,
  ${sqlString(item.externalId)} AS external_id,
  ${sqlString(item.sourceUrl)} AS source_url,
  ${jsonb(raw)} AS raw_payload,
  ${jsonb(normalized)} AS normalized_payload,
  'pending_review' AS status
FROM source_row s
CROSS JOIN job_row j`;
});

const chunks = [];
for (let i = 0; i < rows.length; i += 100) {
  const chunk = rows.slice(i, i + 100);
  chunks.push(`WITH source_row AS (
  SELECT id FROM crawl_sources WHERE name = 'overpass-danang-pois'
), job_row AS (
  SELECT id FROM crawl_jobs
  WHERE source_id = (SELECT id FROM source_row)
  ORDER BY id DESC
  LIMIT 1
)
INSERT INTO crawl_items (
  source_id, job_id, entity_type, external_id, source_url, raw_payload, normalized_payload, status, created_at, updated_at
)
${chunk.join("\nUNION ALL\n")}
ON CONFLICT (source_id, external_id) WHERE external_id IS NOT NULL DO UPDATE SET
  job_id = EXCLUDED.job_id,
  entity_type = EXCLUDED.entity_type,
  source_url = EXCLUDED.source_url,
  raw_payload = EXCLUDED.raw_payload,
  normalized_payload = EXCLUDED.normalized_payload,
  status = CASE
    WHEN crawl_items.status IN ('approved', 'published') THEN crawl_items.status
    ELSE EXCLUDED.status
  END,
  updated_at = NOW();
`);
}

const footer = `
INSERT INTO crawl_logs (job_id, level, message, context_json, created_at)
SELECT j.id, 'INFO', 'Imported Overpass Da Nang POIs into crawl_items', ${jsonb({ total: items.length })}, NOW()
FROM crawl_jobs j
JOIN crawl_sources s ON s.id = j.source_id
WHERE s.name = 'overpass-danang-pois'
ORDER BY j.id DESC
LIMIT 1;
`;

fs.writeFileSync(outputPath, header + sourceSql + jobSql + chunks.join("\n") + footer, "utf8");
console.log(`Wrote ${outputPath} (${items.length} items)`);

