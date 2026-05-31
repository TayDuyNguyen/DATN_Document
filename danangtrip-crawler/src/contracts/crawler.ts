export type CrawlEntityType = "location" | "restaurant" | "hotel" | "tour" | "blog" | "faq";

export type CrawlItemStatus =
  | "raw"
  | "normalized"
  | "pending_review"
  | "approved"
  | "rejected"
  | "published"
  | "failed";

export interface RawCrawlItem {
  sourceName: string;
  sourceType: string;
  entityType: CrawlEntityType;
  externalId: string;
  sourceUrl?: string;
  rawPayload: Record<string, unknown>;
}

export interface NormalizedCrawlItem {
  sourceName: string;
  sourceType: string;
  entityType: CrawlEntityType;
  externalId: string;
  sourceUrl?: string;
  status: CrawlItemStatus;
  normalizedPayload: {
    name: string;
    slugCandidate?: string;
    categorySlug?: string;
    district?: string;
    address?: string;
    latitude?: number;
    longitude?: number;
    rating?: number;
    reviewCount?: number;
    categories: string[];
    sourceReferences?: string[];
    shortDescription?: string;
    description?: string;
    imageUrls: string[];
  };
  rawPayload: Record<string, unknown>;
  crawledAt: string;
}

export interface CrawlerSource {
  name: string;
  type: string;
  crawl(): Promise<RawCrawlItem[]>;
}
