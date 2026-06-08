import type { NormalizedCrawlItem, RawCrawlItem } from "../contracts/crawler.js";
import { normalizeDisplayText, toAsciiText } from "../utils/text.js";

export function normalizeLocationItems(rawItems: RawCrawlItem[]): NormalizedCrawlItem[] {
  return rawItems.map((item) => {
    const raw = item.rawPayload;
    const name = normalizeDisplayText(getString(raw.name));

    return {
      sourceName: item.sourceName,
      sourceType: item.sourceType,
      entityType: item.entityType,
      externalId: item.externalId,
      sourceUrl: item.sourceUrl,
      status: "pending_review",
      normalizedPayload: {
        name,
        slugCandidate: toSlug(name),
        categorySlug: getOptionalString(raw.categorySlug),
        district: getOptionalString(raw.district),
        address: getOptionalString(raw.address),
        latitude: getOptionalNumber(raw.latitude),
        longitude: getOptionalNumber(raw.longitude),
        rating: getOptionalNumber(raw.rating),
        reviewCount: getOptionalNumber(raw.reviewCount),
        categories: getStringArray(raw.categories),
        sourceReferences: getStringArray(raw.sourceReferences),
        shortDescription: getOptionalString(raw.shortDescription),
        description: getOptionalString(raw.description),
        imageUrls: getStringArray(raw.imageUrls),
      },
      rawPayload: normalizeUnknownStrings(item.rawPayload) as Record<string, unknown>,
      crawledAt: new Date().toISOString(),
    };
  });
}

function getString(value: unknown): string {
  return typeof value === "string" && value.trim() ? value.trim() : "Untitled";
}

function getOptionalString(value: unknown): string | undefined {
  return typeof value === "string" && value.trim() ? normalizeDisplayText(value) : undefined;
}

function getOptionalNumber(value: unknown): number | undefined {
  return typeof value === "number" && Number.isFinite(value) ? value : undefined;
}

function getStringArray(value: unknown): string[] {
  if (!Array.isArray(value)) {
    return [];
  }

  return value
    .filter((item): item is string => typeof item === "string" && item.trim().length > 0)
    .map((item) => normalizeDisplayText(item));
}

function toSlug(value: string): string {
  return toAsciiText(value)
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

function normalizeUnknownStrings(value: unknown): unknown {
  if (typeof value === "string") {
    return normalizeDisplayText(value);
  }

  if (Array.isArray(value)) {
    return value.map(normalizeUnknownStrings);
  }

  if (value && typeof value === "object") {
    return Object.fromEntries(
      Object.entries(value).map(([key, item]) => [key, normalizeUnknownStrings(item)]),
    );
  }

  return value;
}
