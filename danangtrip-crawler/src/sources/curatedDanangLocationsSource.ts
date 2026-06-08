import type { CrawlerSource, RawCrawlItem } from "../contracts/crawler.js";
import { normalizeDisplayText } from "../utils/text.js";

const sourceName = "curated-danang-locations";
const sourceType = "curated_official_sources";

export class CuratedDanangLocationsSource implements CrawlerSource {
  name = sourceName;
  type = sourceType;

  async crawl(): Promise<RawCrawlItem[]> {
    return curatedLocations.map((location) => ({
      sourceName: this.name,
      sourceType: this.type,
      entityType: "location",
      externalId: location.externalId,
      sourceUrl: location.sourceUrl,
      rawPayload: normalizeStrings(location),
    }));
  }
}

function normalizeStrings(value: unknown): Record<string, unknown> {
  return normalizeUnknownStrings(value) as Record<string, unknown>;
}

function normalizeUnknownStrings(value: unknown): unknown {
  if (typeof value === "string") {
    return normalizeDisplayText(value);
  }

  if (Array.isArray(value)) {
    return value.map(normalizeUnknownStrings);
  }

  if (value && typeof value === "object") {
    return Object.fromEntries(Object.entries(value).map(([key, item]) => [key, normalizeUnknownStrings(item)]));
  }

  return value;
}

const curatedLocations = [
  {
    externalId: "danang-dragon-bridge",
    name: "Cầu Rồng Đà Nẵng",
    categorySlug: "check-in-noi-tieng",
    district: "Hải Châu / Sơn Trà",
    address: "Nguyễn Văn Linh - Võ Văn Kiệt, Đà Nẵng",
    latitude: 16.06125,
    longitude: 108.22779,
    categories: ["bridge", "landmark", "night-view"],
    shortDescription: "Cây cầu biểu tượng bắc qua sông Hàn, nổi tiếng với hình rồng và màn trình diễn lửa, nước cuối tuần.",
    description:
      "Cầu Rồng là một trong những biểu tượng hiện đại của Đà Nẵng, kết nối trung tâm thành phố với khu vực biển Mỹ Khê. Địa điểm phù hợp để ngắm sông Hàn, chụp ảnh đêm và theo dõi màn trình diễn lửa, nước vào cuối tuần.",
    imageUrls: [],
    sourceUrl: "https://danangfantasticity.com/en/architecture/dragon-bridge",
    sourceReferences: ["Danang Fantasticity - Da Nang City Tourism Information Portal"],
  },
  {
    externalId: "danang-my-khe-beach",
    name: "Bãi biển Mỹ Khê",
    categorySlug: "check-in-noi-tieng",
    district: "Sơn Trà / Ngũ Hành Sơn",
    address: "Võ Nguyên Giáp, Đà Nẵng",
    latitude: 16.05441,
    longitude: 108.24731,
    categories: ["beach", "nature", "sunrise", "family"],
    shortDescription: "Bãi biển nổi tiếng của Đà Nẵng, phù hợp tắm biển, ngắm bình minh và nghỉ dưỡng ven biển.",
    description:
      "Mỹ Khê là khu biển trung tâm của Đà Nẵng, được biết đến với bờ cát dài, không gian thoáng và nhiều dịch vụ du lịch ven biển. Đây là điểm nên có trong lịch trình đầu tiên khi khách đến Đà Nẵng.",
    imageUrls: [],
    sourceUrl: "https://www.vietnamtourism.com/en/visiting-da-nang-your-complete-travel-guide-to-vietnam-s-coastal-city",
    sourceReferences: ["Vietnam Tourism - Da Nang travel guide"],
  },
  {
    externalId: "danang-marble-mountains",
    name: "Ngũ Hành Sơn",
    categorySlug: "hang-dong-nui-non",
    district: "Ngũ Hành Sơn",
    address: "Hòa Hải, Ngũ Hành Sơn, Đà Nẵng",
    latitude: 16.00358,
    longitude: 108.26492,
    categories: ["mountain", "cave", "spiritual", "heritage"],
    shortDescription: "Cụm núi đá với hang động, chùa cổ và điểm ngắm cảnh gần biển Non Nước.",
    description:
      "Ngũ Hành Sơn là cụm núi đá với nhiều hang động, chùa và điểm ngắm cảnh gần khu vực Non Nước. Địa điểm phù hợp cho khách yêu thích văn hóa, tâm linh và khám phá cảnh quan tự nhiên.",
    imageUrls: [],
    sourceUrl: "https://vietnamtourism.gov.vn/en/post/13818",
    sourceReferences: ["Vietnam National Authority of Tourism"],
  },
  {
    externalId: "danang-linh-ung-bai-but",
    name: "Chùa Linh Ứng Bãi Bụt",
    categorySlug: "du-lich-tam-linh",
    district: "Sơn Trà",
    address: "Bán đảo Sơn Trà, Đà Nẵng",
    latitude: 16.10025,
    longitude: 108.27702,
    categories: ["pagoda", "spiritual", "viewpoint", "son-tra"],
    shortDescription: "Điểm du lịch tâm linh trên bán đảo Sơn Trà, nhìn về biển và thành phố Đà Nẵng.",
    description:
      "Chùa Linh Ứng Bãi Bụt nằm trên bán đảo Sơn Trà, là điểm đến tâm linh kết hợp ngắm cảnh biển và thành phố. Đây là địa điểm phù hợp cho lịch trình Sơn Trà, chùa Linh Ứng và các điểm check-in ven núi.",
    imageUrls: [],
    sourceUrl: "https://danangfantasticity.com/en/discovery/linh-ung-pagoda-bai-but.html",
    sourceReferences: ["Danang Fantasticity - Da Nang City Tourism Information Portal"],
  },
  {
    externalId: "danang-ba-na-hills",
    name: "Bà Nà Hills",
    categorySlug: "cong-vien-nuoc",
    district: "Hòa Vang",
    address: "Hòa Ninh, Hòa Vang, Đà Nẵng",
    latitude: 15.99506,
    longitude: 107.99727,
    categories: ["theme-park", "mountain-resort", "cable-car", "family"],
    shortDescription: "Khu du lịch trên núi với cáp treo, làng Pháp, khu vui chơi và nhiều điểm check-in.",
    description:
      "Bà Nà Hills là khu du lịch trên núi ở Hòa Vang, phù hợp cho tour trọn ngày từ trung tâm Đà Nẵng. Dữ liệu này cần được duyệt thêm về giá vé, giờ mở cửa và chính sách dịch vụ trước khi xuất bản.",
    imageUrls: [],
    sourceUrl: "https://banahills.sunworld.vn/en",
    sourceReferences: ["Sun World Ba Na Hills official website"],
  },
  {
    externalId: "danang-golden-bridge",
    name: "Cầu Vàng",
    categorySlug: "check-in-noi-tieng",
    district: "Hòa Vang",
    address: "Sun World Bà Nà Hills, Hòa Ninh, Hòa Vang, Đà Nẵng",
    latitude: 15.99581,
    longitude: 107.99678,
    categories: ["bridge", "viewpoint", "photo-spot", "ba-na-hills"],
    shortDescription: "Điểm check-in nổi bật trong khu Bà Nà Hills với thiết kế bàn tay nâng cây cầu.",
    description:
      "Cầu Vàng là điểm check-in nổi bật trong khu Bà Nà Hills, thường được đưa vào lịch trình tour Bà Nà trong ngày. Khi xuất bản nên gắn với địa điểm Bà Nà Hills hoặc tour Bà Nà để tránh trùng lặp trải nghiệm.",
    imageUrls: [],
    sourceUrl: "https://banahills.sunworld.vn/en",
    sourceReferences: ["Sun World Ba Na Hills official website"],
  },
  {
    externalId: "danang-cham-sculpture-museum",
    name: "Bảo tàng Điêu khắc Chăm Đà Nẵng",
    categorySlug: "bao-tang-di-tich",
    district: "Hải Châu",
    address: "02 đường 2 Tháng 9, Hải Châu, Đà Nẵng",
    latitude: 16.06055,
    longitude: 108.22302,
    categories: ["museum", "heritage", "culture", "indoor"],
    shortDescription: "Bảo tàng trưng bày nghệ thuật điêu khắc Champa, phù hợp lịch trình văn hóa trong trung tâm Đà Nẵng.",
    description:
      "Bảo tàng Điêu khắc Chăm Đà Nẵng lưu giữ và trưng bày bộ sưu tập hiện vật nghệ thuật Champa. Đây là điểm đến phù hợp cho khách quan tâm di sản, lịch sử và các hoạt động trong nhà.",
    imageUrls: [],
    sourceUrl: "https://visitdanang.travel/en/da-nang-museum-of-cham-sculpture-2036",
    sourceReferences: ["Visit Da Nang"],
  },
  {
    externalId: "danang-han-market",
    name: "Chợ Hàn",
    categorySlug: "cho-dia-phuong",
    district: "Hải Châu",
    address: "119 Trần Phú, Hải Châu, Đà Nẵng",
    latitude: 16.06805,
    longitude: 108.22431,
    categories: ["market", "shopping", "local-food", "souvenir"],
    shortDescription: "Chợ trung tâm gần sông Hàn, phù hợp mua đặc sản, quà lưu niệm và trải nghiệm mua sắm địa phương.",
    description:
      "Chợ Hàn là một điểm mua sắm quen thuộc ở trung tâm Đà Nẵng, gần trục Bạch Đằng - Trần Phú. Dữ liệu này cần được bổ sung ảnh, giờ hoạt động và các lưu ý mua sắm trước khi xuất bản.",
    imageUrls: [],
    sourceUrl: "https://danangfantasticity.com/en/where-to-shop",
    sourceReferences: ["Danang Fantasticity - Where to shop"],
  },
];
