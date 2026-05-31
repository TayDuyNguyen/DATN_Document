import fs from "node:fs";
import path from "node:path";

const rootDir = path.resolve(".");
const inputPath = path.join(rootDir, "data", "overpass-danang-pois.json");
const cleanPath = path.join(rootDir, "data", "overpass-danang-pois-clean.json");
const rejectedPath = path.join(rootDir, "data", "overpass-danang-pois-rejected.json");
const reportPath = path.join(rootDir, "data", "overpass-quality-report.json");
const sqlPath = path.resolve(rootDir, "..", "database-seeders", "13_overpass_quality_review_seed.sql");

const MIN_SCORE = 58;
const MAX_PER_ENTITY = {
  location: 180,
  restaurant: 220,
  hotel: 180,
};

const suspiciousNamePatterns = [
  /^saturday option$/i,
  /^option$/i,
  /^test$/i,
  /^unknown$/i,
  /^no name$/i,
  /^poi$/i,
  /^viewpoint$/i,
  /^restaurant$/i,
  /^cafe$/i,
  /^hotel$/i,
  /^bar$/i,
];

const items = JSON.parse(fs.readFileSync(inputPath, "utf8"));
const scored = items.map(scoreItem);
const unique = dedupe(scored);
const passedBeforeLimit = unique.filter((item) => item.quality.pass);
const rejectedBeforeLimit = unique.filter((item) => !item.quality.pass);

const clean = [];
const overflowRejected = [];

for (const entity of Object.keys(MAX_PER_ENTITY)) {
  const limit = MAX_PER_ENTITY[entity];
  const group = passedBeforeLimit
    .filter((item) => item.entityType === entity)
    .sort((a, b) => b.quality.score - a.quality.score || a.normalizedPayload.name.localeCompare(b.normalizedPayload.name));

  clean.push(...group.slice(0, limit));
  overflowRejected.push(...group.slice(limit).map((item) => reject(item, "over_entity_limit")));
}

const entityTypesWithoutLimit = passedBeforeLimit.filter((item) => !Object.hasOwn(MAX_PER_ENTITY, item.entityType));
clean.push(...entityTypesWithoutLimit);

const rejected = [...rejectedBeforeLimit, ...overflowRejected].sort((a, b) =>
  a.normalizedPayload.name.localeCompare(b.normalizedPayload.name),
);

const cleanOutput = clean.map(toOutputItem);
const rejectedOutput = rejected.map(toOutputItem);
const report = buildReport(items, unique, cleanOutput, rejectedOutput);

fs.writeFileSync(cleanPath, `${JSON.stringify(cleanOutput, null, 2)}\n`, "utf8");
fs.writeFileSync(rejectedPath, `${JSON.stringify(rejectedOutput, null, 2)}\n`, "utf8");
fs.writeFileSync(reportPath, `${JSON.stringify(report, null, 2)}\n`, "utf8");
fs.writeFileSync(sqlPath, buildSql(cleanOutput, rejectedOutput, report), "utf8");

console.log(JSON.stringify(report, null, 2));
console.log(`Wrote ${cleanPath}`);
console.log(`Wrote ${rejectedPath}`);
console.log(`Wrote ${reportPath}`);
console.log(`Wrote ${sqlPath}`);

function scoreItem(item) {
  const normalized = item.normalizedPayload ?? {};
  const raw = item.rawPayload ?? {};
  const tags = raw.osmTags ?? {};
  const reasons = [];
  let score = 0;

  const name = String(normalized.name ?? "").trim();
  const address = String(normalized.address ?? "").trim();
  const categories = Array.isArray(normalized.categories) ? normalized.categories : [];
  const latitude = Number(normalized.latitude);
  const longitude = Number(normalized.longitude);

  if (name.length >= 3) score += 20;
  else reasons.push("name_too_short");

  if (name.length <= 80) score += 8;
  else reasons.push("name_too_long");

  if (!suspiciousNamePatterns.some((pattern) => pattern.test(name))) score += 18;
  else reasons.push("generic_or_suspicious_name");

  if (Number.isFinite(latitude) && Number.isFinite(longitude)) score += 22;
  else reasons.push("missing_coordinates");

  if (address && address.toLowerCase() !== "da nang") score += 10;
  else reasons.push("weak_address");

  if (categories.length > 0) score += 10;
  else reasons.push("missing_categories");

  if (item.entityType === "location") score += 10;
  if (item.entityType === "hotel") score += 8;
  if (item.entityType === "restaurant") score += 6;

  if (tags.wikidata || tags.wikipedia) score += 8;
  if (tags.website || tags.contact?.website || tags["contact:website"]) score += 5;
  if (tags.phone || tags["contact:phone"]) score += 4;
  if (tags.opening_hours) score += 4;
  if (tags.cuisine) score += 3;

  const hardReject = reasons.includes("name_too_short") || reasons.includes("missing_coordinates") || reasons.includes("generic_or_suspicious_name");

  return {
    ...item,
    normalizedPayload: {
      ...normalized,
      qualityScore: score,
      qualityReasons: reasons,
      reviewPriority: score >= 80 ? "high" : score >= MIN_SCORE ? "normal" : "low",
    },
    quality: {
      score,
      reasons,
      pass: !hardReject && score >= MIN_SCORE,
    },
  };
}

function dedupe(scoredItems) {
  const bestByKey = new Map();

  for (const item of scoredItems) {
    const key = dedupeKey(item);
    const current = bestByKey.get(key);

    if (!current || item.quality.score > current.quality.score) {
      bestByKey.set(key, item);
    }
  }

  return Array.from(bestByKey.values());
}

function dedupeKey(item) {
  const name = normalizeName(item.normalizedPayload?.name ?? "");
  const lat = Number(item.normalizedPayload?.latitude ?? 0).toFixed(3);
  const lng = Number(item.normalizedPayload?.longitude ?? 0).toFixed(3);
  return `${item.entityType}:${name}:${lat}:${lng}`;
}

function normalizeName(value) {
  return String(value)
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, " ")
    .trim();
}

function reject(item, reason) {
  return {
    ...item,
    normalizedPayload: {
      ...item.normalizedPayload,
      qualityReasons: [...new Set([...(item.normalizedPayload.qualityReasons ?? []), reason])],
      reviewPriority: "low",
    },
    quality: {
      ...item.quality,
      pass: false,
      reasons: [...new Set([...(item.quality.reasons ?? []), reason])],
    },
  };
}

function toOutputItem(item) {
  const { quality, ...rest } = item;
  return {
    ...rest,
    status: quality.pass ? "pending_review" : "rejected",
  };
}

function buildReport(original, uniqueItems, cleanItems, rejectedItems) {
  return {
    generatedAt: new Date().toISOString(),
    input: {
      total: original.length,
      uniqueAfterDedupe: uniqueItems.length,
    },
    output: {
      clean: cleanItems.length,
      rejected: rejectedItems.length,
    },
    cleanByEntity: countBy(cleanItems, "entityType"),
    rejectedByEntity: countBy(rejectedItems, "entityType"),
    cleanByCategory: countBy(cleanItems, (item) => item.normalizedPayload?.categorySlug ?? "unknown"),
    rejectedTopReasons: countReasons(rejectedItems),
    minScore: MIN_SCORE,
    maxPerEntity: MAX_PER_ENTITY,
  };
}

function countBy(items, keyOrFn) {
  const result = {};

  for (const item of items) {
    const key = typeof keyOrFn === "function" ? keyOrFn(item) : item[keyOrFn];
    result[key] = (result[key] ?? 0) + 1;
  }

  return result;
}

function countReasons(items) {
  const result = {};

  for (const item of items) {
    for (const reason of item.normalizedPayload?.qualityReasons ?? []) {
      result[reason] = (result[reason] ?? 0) + 1;
    }
  }

  return Object.fromEntries(Object.entries(result).sort((a, b) => b[1] - a[1]));
}

function buildSql(cleanItems, rejectedItems, report) {
  const cleanExternalIds = cleanItems.map((item) => item.externalId).filter(Boolean);
  const rejectedExternalIds = rejectedItems.map((item) => item.externalId).filter(Boolean);
  const chunks = [];

  chunks.push(`-- DanangTrip Crawler Quality Review Seed\n`);
  chunks.push(`-- FILE: 13_overpass_quality_review_seed.sql\n`);
  chunks.push(`-- Generated: ${report.generatedAt}\n`);
  chunks.push(`-- Clean: ${cleanItems.length}\n`);
  chunks.push(`-- Rejected: ${rejectedItems.length}\n\n`);

  chunks.push(buildStatusUpdate("pending_review", cleanExternalIds));
  chunks.push("\n");
  chunks.push(buildStatusUpdate("rejected", rejectedExternalIds));
  chunks.push("\n");
  chunks.push(`INSERT INTO crawl_logs (job_id, level, message, context_json, created_at)\n`);
  chunks.push(`SELECT j.id, 'INFO', 'Applied Overpass quality filter', ${sqlJson(report)}::jsonb, NOW()\n`);
  chunks.push(`FROM crawl_jobs j\n`);
  chunks.push(`JOIN crawl_sources s ON s.id = j.source_id\n`);
  chunks.push(`WHERE s.name = 'overpass-danang-pois'\n`);
  chunks.push(`ORDER BY j.id DESC\n`);
  chunks.push(`LIMIT 1;\n`);

  return chunks.join("");
}

function buildStatusUpdate(status, externalIds) {
  if (externalIds.length === 0) {
    return "";
  }

  const valueRows = externalIds.map((id) => `(${sqlString(id)})`).join(",\n");

  return `WITH source_row AS (
  SELECT id FROM crawl_sources WHERE name = 'overpass-danang-pois'
), selected_external_ids(external_id) AS (
  VALUES
${valueRows}
)
UPDATE crawl_items ci
SET status = '${status}',
    updated_at = NOW()
FROM source_row s, selected_external_ids selected
WHERE ci.source_id = s.id
  AND ci.external_id = selected.external_id
  AND ci.status NOT IN ('approved', 'published');
`;
}

function sqlString(value) {
  return `'${String(value).replaceAll("'", "''")}'`;
}

function sqlJson(value) {
  return sqlString(JSON.stringify(value));
}

