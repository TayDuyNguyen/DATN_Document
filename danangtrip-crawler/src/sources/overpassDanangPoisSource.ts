import { env } from "../config/env.js";
import type { CrawlEntityType, CrawlerSource, RawCrawlItem } from "../contracts/crawler.js";
import { toAsciiText } from "../utils/text.js";

interface OverpassResponse {
  elements?: OverpassElement[];
}

interface OverpassElement {
  type: "node" | "way" | "relation";
  id: number;
  lat?: number;
  lon?: number;
  center?: {
    lat?: number;
    lon?: number;
  };
  tags?: Record<string, string>;
}

const DA_NANG_BBOX = {
  south: 15.95,
  west: 107.95,
  north: 16.2,
  east: 108.35,
};

export class OverpassDanangPoisSource implements CrawlerSource {
  name = "overpass-danang-pois";
  type = "overpass_api";

  async crawl(): Promise<RawCrawlItem[]> {
    const allElements: OverpassElement[] = [];

    for (const group of queryGroups) {
      const payload = await this.fetchGroup(group);
      allElements.push(...(payload.elements ?? []));
      await sleep(1200);
    }

    const uniqueElements = dedupeElements(allElements);

    return uniqueElements
      .filter(hasUsefulName)
      .map((element) => this.toRawItem(element))
      .filter((item): item is RawCrawlItem => item !== null);
  }

  private async fetchGroup(group: QueryGroup): Promise<OverpassResponse> {
    const response = await fetch(env.OVERPASS_API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "User-Agent": env.CRAWLER_USER_AGENT,
      },
      body: new URLSearchParams({ data: buildOverpassQuery(group) }),
    });

    if (!response.ok) {
      throw new Error(`Overpass request failed with ${response.status}: ${await response.text()}`);
    }

    return (await response.json()) as OverpassResponse;
  }

  private toRawItem(element: OverpassElement): RawCrawlItem | null {
    const tags = element.tags ?? {};
    const name = toAsciiText(tags.name ?? tags["name:vi"] ?? tags["name:en"] ?? "");
    const latitude = element.lat ?? element.center?.lat;
    const longitude = element.lon ?? element.center?.lon;

    if (!name || latitude === undefined || longitude === undefined) {
      return null;
    }

    const entityType = inferEntityType(tags);
    const categorySlug = inferCategorySlug(tags);
    const categories = inferCategories(tags);

    return {
      sourceName: this.name,
      sourceType: this.type,
      entityType,
      externalId: `osm-${element.type}-${element.id}`,
      sourceUrl: `https://www.openstreetmap.org/${element.type}/${element.id}`,
      rawPayload: {
        name,
        categorySlug,
        district: toAsciiText(tags["addr:district"] ?? tags["is_in:district"] ?? ""),
        address: formatAddress(tags),
        latitude,
        longitude,
        categories,
        shortDescription: buildShortDescription(name, tags),
        description: buildDescription(name, tags),
        imageUrls: [],
        sourceReferences: ["OpenStreetMap contributors", "Overpass API"],
        osmType: element.type,
        osmId: element.id,
        osmTags: tags,
      },
    };
  }
}

interface QueryGroup {
  name: string;
  selectors: string[];
  limit: number;
}

const queryGroups: QueryGroup[] = [
  {
    name: "attractions",
    selectors: [
      '["tourism"~"attraction|museum|viewpoint|theme_park"]',
      '["historic"]',
    ],
    limit: 250,
  },
  {
    name: "restaurants",
    selectors: ['["amenity"~"restaurant|fast_food"]'],
    limit: 250,
  },
  {
    name: "cafes-bars",
    selectors: ['["amenity"~"cafe|bar|pub"]'],
    limit: 250,
  },
  {
    name: "hotels",
    selectors: ['["tourism"~"hotel|guest_house|hostel|resort"]'],
    limit: 250,
  },
  {
    name: "nature-parks",
    selectors: [
      '["leisure"~"park|water_park|nature_reserve"]',
      '["natural"~"beach|peak|bay"]',
    ],
    limit: 250,
  },
];

function buildOverpassQuery(group: QueryGroup): string {
  const { south, west, north, east } = DA_NANG_BBOX;
  const bbox = `${south},${west},${north},${east}`;
  const selectors = group.selectors
    .flatMap((selector) => [
      `node${selector}(${bbox});`,
      `way${selector}(${bbox});`,
      `relation${selector}(${bbox});`,
    ])
    .join("\n");

  return `
    [out:json][timeout:60];
    (
      ${selectors}
    );
    out center tags ${group.limit};
  `;
}

function hasUsefulName(element: OverpassElement): boolean {
  const tags = element.tags ?? {};
  return Boolean(tags.name ?? tags["name:vi"] ?? tags["name:en"]);
}

function inferEntityType(tags: Record<string, string>): CrawlEntityType {
  if (["hotel", "guest_house", "hostel", "resort"].includes(tags.tourism ?? "")) {
    return "hotel";
  }

  if (["restaurant", "cafe", "fast_food", "bar", "pub"].includes(tags.amenity ?? "")) {
    return "restaurant";
  }

  return "location";
}

function inferCategorySlug(tags: Record<string, string>): string {
  if (tags.amenity === "restaurant" || tags.amenity === "fast_food") {
    return "am-thuc-dia-phuong";
  }

  if (tags.amenity === "cafe") {
    return "ca-phe-tra-sua";
  }

  if (tags.amenity === "bar" || tags.amenity === "pub") {
    return "bar-pub";
  }

  if (["hotel", "guest_house", "hostel", "resort"].includes(tags.tourism ?? "")) {
    return "khach-san-homestay";
  }

  if (tags.tourism === "museum" || tags.historic) {
    return "bao-tang-di-tich";
  }

  if (tags.natural === "beach") {
    return "check-in-noi-tieng";
  }

  if (tags.natural === "peak" || tags.natural === "bay") {
    return "hang-dong-nui-non";
  }

  if (tags.leisure === "park" || tags.leisure === "nature_reserve") {
    return "cong-vien-vuon-hoa";
  }

  if (tags.leisure === "water_park" || tags.tourism === "theme_park") {
    return "cong-vien-nuoc";
  }

  return "check-in-noi-tieng";
}

function inferCategories(tags: Record<string, string>): string[] {
  return [
    tags.tourism,
    tags.amenity,
    tags.historic,
    tags.leisure,
    tags.natural,
    tags.cuisine,
  ].filter((value): value is string => Boolean(value));
}

function dedupeElements(elements: OverpassElement[]): OverpassElement[] {
  const seen = new Set<string>();
  const unique: OverpassElement[] = [];

  for (const element of elements) {
    const key = `${element.type}:${element.id}`;
    if (seen.has(key)) {
      continue;
    }

    seen.add(key);
    unique.push(element);
  }

  return unique;
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function formatAddress(tags: Record<string, string>): string | undefined {
  const parts = [
    tags["addr:housenumber"],
    tags["addr:street"],
    tags["addr:ward"],
    tags["addr:district"],
    tags["addr:city"] ?? "Da Nang",
  ].filter(Boolean);

  return parts.length > 0 ? toAsciiText(parts.join(", ")) : undefined;
}

function buildShortDescription(name: string, tags: Record<string, string>): string {
  const type = tags.tourism ?? tags.amenity ?? tags.historic ?? tags.leisure ?? tags.natural ?? "poi";
  return `${name} duoc thu thap tu OpenStreetMap voi nhom du lieu ${type}. Can admin kiem tra mo ta, anh va thong tin van hanh truoc khi publish.`;
}

function buildDescription(name: string, tags: Record<string, string>): string {
  const category = inferCategorySlug(tags);
  return `${name} la diem du lieu du lich/dich vu tai khu vuc Da Nang, duoc crawl tu OpenStreetMap qua Overpass API. Ban ghi dang o trang thai pending_review va can duoc bien tap noi dung, anh, gio mo cua, gia va danh muc (${category}) truoc khi dua len website DanangTrip.`;
}
