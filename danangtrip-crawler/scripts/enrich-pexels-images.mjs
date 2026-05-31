import "dotenv/config";
import fs from "node:fs";
import path from "node:path";

const rootDir = path.resolve(".");
const inputPath = path.join(rootDir, "data", "overpass-danang-pois-clean.json");
const outputPath = path.join(rootDir, "data", "overpass-danang-pois-enriched.json");
const reportPath = path.join(rootDir, "data", "pexels-enrichment-report.json");
const sqlPath = path.resolve(rootDir, "..", "database-seeders", "14_pexels_image_enrichment_seed.sql");

const apiKey = process.env.PEXELS_API_KEY;
const apiUrl = process.env.PEXELS_API_URL || "https://api.pexels.com/v1/search";
const limit = positiveInt(process.env.PEXELS_ENRICH_LIMIT, 80);
const photosPerItem = Math.min(positiveInt(process.env.PEXELS_PHOTOS_PER_ITEM, 3), 5);
const requestDelayMs = positiveInt(process.env.PEXELS_REQUEST_DELAY_MS, 750);
const stopOnThrottle = process.env.PEXELS_STOP_ON_429 !== "false";

if (!apiKey) {
  throw new Error("Missing PEXELS_API_KEY in .env");
}

const items = JSON.parse(fs.readFileSync(inputPath, "utf8"));
const existingItems = fs.existsSync(outputPath) ? JSON.parse(fs.readFileSync(outputPath, "utf8")) : [];
const existingByExternalId = new Map(existingItems.map((item) => [item.externalId, item]));
const baselineItems = items.map((item) => mergeExistingImageData(item, existingByExternalId.get(item.externalId)));
const selectedItems = baselineItems.slice(0, limit).filter((item) => !hasPexelsImages(item));
const enriched = [];
const failures = [];
let throttled = false;

for (const [index, item] of selectedItems.entries()) {
  const query = buildSearchQuery(item);
  try {
    const photos = await searchPexels(query);
    const candidates = photos.slice(0, photosPerItem).map(toImageCandidate);
    enriched.push(applyImageCandidates(item, candidates, query));
    console.log(`[${index + 1}/${selectedItems.length}] ${item.normalizedPayload?.name} -> ${candidates.length} images`);
  } catch (error) {
    failures.push({
      externalId: item.externalId,
      name: item.normalizedPayload?.name,
      query,
      message: toAsciiText(error instanceof Error ? error.message : String(error)),
    });
    if (isThrottleError(error)) {
      throttled = true;
      console.log(`[${index + 1}/${selectedItems.length}] ${item.normalizedPayload?.name} -> throttled`);
      if (stopOnThrottle) {
        break;
      }
    } else {
      enriched.push(applyImageCandidates(item, [], query));
      console.log(`[${index + 1}/${selectedItems.length}] ${item.normalizedPayload?.name} -> failed`);
    }
  }

  await sleep(requestDelayMs);
}

const enrichedByExternalId = new Map(enriched.map((item) => [item.externalId, item]));
const output = baselineItems.map((item) => enrichedByExternalId.get(item.externalId) ?? item);
const itemsWithImages = output.filter((item) => hasPexelsImages(item));
const report = {
  generatedAt: new Date().toISOString(),
  input: {
    file: path.relative(rootDir, inputPath).replaceAll("\\", "/"),
    total: items.length,
  },
  pexels: {
    limit,
    photosPerItem,
    requestDelayMs,
    selectedMissingItems: selectedItems.length,
    newlyEnrichedItems: enriched.filter((item) => hasPexelsImages(item)).length,
    totalItemsWithImages: itemsWithImages.length,
    failures: failures.length,
    throttled,
  },
  output: {
    file: path.relative(rootDir, outputPath).replaceAll("\\", "/"),
    sqlSeed: path.relative(rootDir, sqlPath).replaceAll("\\", "/"),
  },
  failures,
};

fs.writeFileSync(outputPath, `${JSON.stringify(toAsciiValue(output), null, 2)}\n`, "utf8");
fs.writeFileSync(reportPath, `${JSON.stringify(toAsciiValue(report), null, 2)}\n`, "utf8");
fs.writeFileSync(sqlPath, buildSql(itemsWithImages, report), "utf8");

console.log(JSON.stringify(report, null, 2));
console.log(`Wrote ${outputPath}`);
console.log(`Wrote ${reportPath}`);
console.log(`Wrote ${sqlPath}`);

function buildSearchQuery(item) {
  const payload = item.normalizedPayload ?? {};
  const category = String(payload.categorySlug ?? "").replace(/-/g, " ");
  const entityWords = {
    location: "Da Nang Vietnam travel landmark",
    restaurant: "Da Nang Vietnam food restaurant",
    hotel: "Da Nang Vietnam hotel resort",
  };
  const fallback = entityWords[item.entityType] ?? "Da Nang Vietnam travel";
  return toAsciiText(`${payload.name ?? ""} ${category} ${fallback}`).slice(0, 120);
}

async function searchPexels(query) {
  const url = new URL(apiUrl);
  url.searchParams.set("query", query);
  url.searchParams.set("per_page", String(Math.max(photosPerItem, 3)));
  url.searchParams.set("orientation", "landscape");
  url.searchParams.set("locale", "en-US");

  const response = await fetch(url, {
    headers: {
      Authorization: apiKey,
      "User-Agent": "DanangTripCrawler/0.1",
    },
  });

  if (!response.ok) {
    const body = await response.text();
    throw new Error(`Pexels request failed ${response.status}: ${body.slice(0, 180)}`);
  }

  const data = await response.json();
  return Array.isArray(data.photos) ? data.photos : [];
}

function toImageCandidate(photo) {
  const src = photo.src ?? {};
  return toAsciiValue({
    provider: "pexels",
    providerId: String(photo.id ?? ""),
    url: src.large2x ?? src.large ?? src.original ?? src.medium ?? "",
    thumbnailUrl: src.medium ?? src.small ?? "",
    pageUrl: photo.url ?? "",
    photographer: photo.photographer ?? "",
    photographerUrl: photo.photographer_url ?? "",
    alt: photo.alt ?? "",
    width: photo.width,
    height: photo.height,
  });
}

function applyImageCandidates(item, candidates, query) {
  const imageUrls = candidates.map((candidate) => candidate.url).filter(Boolean);
  const normalizedPayload = {
    ...(item.normalizedPayload ?? {}),
    imageUrls,
    imageSource: "pexels",
    imageSearchQuery: query,
  };
  const rawPayload = {
    ...(item.rawPayload ?? {}),
    imageCandidates: candidates,
    imageEnrichment: {
      provider: "pexels",
      searchQuery: query,
      enrichedAt: new Date().toISOString(),
      candidateCount: candidates.length,
    },
  };

  return toAsciiValue({
    ...item,
    normalizedPayload,
    rawPayload,
  });
}

function mergeExistingImageData(item, existing) {
  if (!existing || !hasPexelsImages(existing)) {
    return item;
  }

  return toAsciiValue({
    ...item,
    normalizedPayload: {
      ...(item.normalizedPayload ?? {}),
      imageUrls: existing.normalizedPayload?.imageUrls ?? [],
      imageSource: existing.normalizedPayload?.imageSource ?? "pexels",
      imageSearchQuery: existing.normalizedPayload?.imageSearchQuery,
    },
    rawPayload: {
      ...(item.rawPayload ?? {}),
      imageCandidates: existing.rawPayload?.imageCandidates ?? [],
      imageEnrichment: existing.rawPayload?.imageEnrichment,
    },
  });
}

function hasPexelsImages(item) {
  return item?.normalizedPayload?.imageSource === "pexels" && Array.isArray(item.normalizedPayload?.imageUrls) && item.normalizedPayload.imageUrls.length > 0;
}

function buildSql(enrichedItems, report) {
  const itemsWithPayload = enrichedItems.filter((item) => item.externalId);
  const chunks = [];

  chunks.push(`-- DanangTrip Crawler Pexels Image Enrichment Seed\n`);
  chunks.push(`-- FILE: 14_pexels_image_enrichment_seed.sql\n`);
  chunks.push(`-- Generated: ${report.generatedAt}\n`);
  chunks.push(`-- Items with images: ${report.pexels.totalItemsWithImages}\n`);
  chunks.push(`-- Notes: URLs and attribution metadata come from Pexels API.\n\n`);

  for (const item of itemsWithPayload) {
    chunks.push(`UPDATE crawl_items ci\n`);
    chunks.push(`SET normalized_payload = ${sqlJson(item.normalizedPayload)}::jsonb,\n`);
    chunks.push(`    raw_payload = ${sqlJson(item.rawPayload)}::jsonb,\n`);
    chunks.push(`    updated_at = NOW()\n`);
    chunks.push(`FROM crawl_sources s\n`);
    chunks.push(`WHERE ci.source_id = s.id\n`);
    chunks.push(`  AND s.name = 'overpass-danang-pois'\n`);
    chunks.push(`  AND ci.external_id = ${sqlString(item.externalId)};\n\n`);
  }

  chunks.push(`INSERT INTO crawl_logs (job_id, level, message, context_json, created_at)\n`);
  chunks.push(`SELECT j.id, 'INFO', 'Applied Pexels image enrichment', ${sqlJson(report)}::jsonb, NOW()\n`);
  chunks.push(`FROM crawl_jobs j\n`);
  chunks.push(`JOIN crawl_sources s ON s.id = j.source_id\n`);
  chunks.push(`WHERE s.name = 'overpass-danang-pois'\n`);
  chunks.push(`ORDER BY j.id DESC\n`);
  chunks.push(`LIMIT 1;\n`);

  return chunks.join("");
}

function positiveInt(value, fallback) {
  const parsed = Number.parseInt(String(value ?? ""), 10);
  return Number.isFinite(parsed) && parsed > 0 ? parsed : fallback;
}

function toAsciiText(value) {
  return String(value)
    .replace(/[đĐ]/g, (char) => (char === "Đ" ? "D" : "d"))
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^\x00-\x7F]/g, "")
    .replace(/\s+/g, " ")
    .trim();
}

function toAsciiValue(value) {
  if (typeof value === "string") {
    return toAsciiText(value);
  }

  if (Array.isArray(value)) {
    return value.map(toAsciiValue);
  }

  if (value && typeof value === "object") {
    return Object.fromEntries(Object.entries(value).map(([key, item]) => [toAsciiText(key), toAsciiValue(item)]));
  }

  return value;
}

function sqlString(value) {
  return `'${String(value).replaceAll("'", "''")}'`;
}

function sqlJson(value) {
  return sqlString(JSON.stringify(value));
}

function isThrottleError(error) {
  return error instanceof Error && (error.message.includes("429") || error.message.toLowerCase().includes("throttle"));
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
