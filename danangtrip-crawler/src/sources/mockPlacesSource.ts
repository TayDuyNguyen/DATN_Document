import type { CrawlerSource, RawCrawlItem } from "../contracts/crawler.js";

export class MockPlacesSource implements CrawlerSource {
  name = "mock-places";
  type = "mock";

  async crawl(): Promise<RawCrawlItem[]> {
    return [
      {
        sourceName: this.name,
        sourceType: this.type,
        entityType: "location",
        externalId: "mock-dragon-bridge",
        sourceUrl: "https://danangtrip.local/mock/dragon-bridge",
        rawPayload: {
          name: "Cau Rong Da Nang",
          address: "An Hai, Son Tra, Da Nang",
          latitude: 16.06125,
          longitude: 108.22779,
          rating: 4.7,
          reviewCount: 12500,
          categories: ["bridge", "landmark", "nightlife"],
          description: "Iconic bridge in Da Nang known for fire and water shows.",
          imageUrls: [],
        },
      },
      {
        sourceName: this.name,
        sourceType: this.type,
        entityType: "location",
        externalId: "mock-my-khe-beach",
        sourceUrl: "https://danangtrip.local/mock/my-khe-beach",
        rawPayload: {
          name: "My Khe Beach",
          address: "Vo Nguyen Giap, Da Nang",
          latitude: 16.05441,
          longitude: 108.24731,
          rating: 4.6,
          reviewCount: 9800,
          categories: ["beach", "nature", "family"],
          description: "Popular beach area with long coastline and sunrise views.",
          imageUrls: [],
        },
      },
    ];
  }
}

