import type { CrawlerSource, RawCrawlItem } from "../contracts/crawler.js";
import { toAsciiText } from "../utils/text.js";

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
    return toAsciiText(value);
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
    name: "Cau Rong Da Nang",
    categorySlug: "check-in-noi-tieng",
    district: "Hai Chau / Son Tra",
    address: "Nguyen Van Linh - Vo Van Kiet, Da Nang",
    latitude: 16.06125,
    longitude: 108.22779,
    categories: ["bridge", "landmark", "night-view"],
    shortDescription: "Cay cau bieu tuong bac qua song Han, noi tieng voi hinh rong va show lua nuoc cuoi tuan.",
    description:
      "Cau Rong la mot trong nhung bieu tuong hien dai cua Da Nang, ket noi trung tam thanh pho voi khu vuc bien My Khe. Dia diem phu hop de ngam song Han, chup anh dem va theo doi man trinh dien lua nuoc vao cuoi tuan.",
    imageUrls: [],
    sourceUrl: "https://danangfantasticity.com/en/architecture/dragon-bridge",
    sourceReferences: ["Danang Fantasticity - Da Nang City Tourism Information Portal"],
  },
  {
    externalId: "danang-my-khe-beach",
    name: "Bai bien My Khe",
    categorySlug: "check-in-noi-tieng",
    district: "Son Tra / Ngu Hanh Son",
    address: "Vo Nguyen Giap, Da Nang",
    latitude: 16.05441,
    longitude: 108.24731,
    categories: ["beach", "nature", "sunrise", "family"],
    shortDescription: "Bai bien noi tieng cua Da Nang, phu hop tam bien, ngam binh minh va nghi duong ven bien.",
    description:
      "My Khe la khu bien trung tam cua Da Nang, duoc biet den voi bo cat dai, khong gian thoang va nhieu dich vu du lich ven bien. Day la diem nen co trong lich trinh dau tien khi khach den Da Nang.",
    imageUrls: [],
    sourceUrl: "https://www.vietnamtourism.com/en/visiting-da-nang-your-complete-travel-guide-to-vietnam-s-coastal-city",
    sourceReferences: ["Vietnam Tourism - Da Nang travel guide"],
  },
  {
    externalId: "danang-marble-mountains",
    name: "Ngu Hanh Son",
    categorySlug: "hang-dong-nui-non",
    district: "Ngu Hanh Son",
    address: "Hoa Hai, Ngu Hanh Son, Da Nang",
    latitude: 16.00358,
    longitude: 108.26492,
    categories: ["mountain", "cave", "spiritual", "heritage"],
    shortDescription: "Cum nui da voi hang dong, chua co va diem ngam canh gan bien Non Nuoc.",
    description:
      "Ngu Hanh Son la cum nui da voi nhieu hang dong, chua va diem ngam canh gan khu vuc Non Nuoc. Dia diem phu hop cho khach thich van hoa, tam linh va kham pha canh quan tu nhien.",
    imageUrls: [],
    sourceUrl: "https://vietnamtourism.gov.vn/en/post/13818",
    sourceReferences: ["Vietnam National Authority of Tourism"],
  },
  {
    externalId: "danang-linh-ung-bai-but",
    name: "Chua Linh Ung Bai But",
    categorySlug: "du-lich-tam-linh",
    district: "Son Tra",
    address: "Ban dao Son Tra, Da Nang",
    latitude: 16.10025,
    longitude: 108.27702,
    categories: ["pagoda", "spiritual", "viewpoint", "son-tra"],
    shortDescription: "Diem du lich tam linh tren ban dao Son Tra, nhin ve bien va thanh pho Da Nang.",
    description:
      "Chua Linh Ung Bai But nam tren ban dao Son Tra, la diem den tam linh ket hop ngam canh bien va thanh pho. Day la dia diem phu hop cho lich trinh Son Tra, chua Linh Ung va cac diem check-in ven nui.",
    imageUrls: [],
    sourceUrl: "https://danangfantasticity.com/en/discovery/linh-ung-pagoda-bai-but.html",
    sourceReferences: ["Danang Fantasticity - Da Nang City Tourism Information Portal"],
  },
  {
    externalId: "danang-ba-na-hills",
    name: "Ba Na Hills",
    categorySlug: "cong-vien-nuoc",
    district: "Hoa Vang",
    address: "Hoa Ninh, Hoa Vang, Da Nang",
    latitude: 15.99506,
    longitude: 107.99727,
    categories: ["theme-park", "mountain-resort", "cable-car", "family"],
    shortDescription: "Khu du lich tren nui voi cap treo, lang Phap, khu vui choi va nhieu diem check-in.",
    description:
      "Ba Na Hills la khu du lich tren nui o Hoa Vang, phu hop cho tour tron ngay tu trung tam Da Nang. Du lieu nay nen duoc duyet them ve gia ve, gio mo cua va chinh sach dich vu truoc khi publish.",
    imageUrls: [],
    sourceUrl: "https://banahills.sunworld.vn/en",
    sourceReferences: ["Sun World Ba Na Hills official website"],
  },
  {
    externalId: "danang-golden-bridge",
    name: "Cau Vang",
    categorySlug: "check-in-noi-tieng",
    district: "Hoa Vang",
    address: "Sun World Ba Na Hills, Hoa Ninh, Hoa Vang, Da Nang",
    latitude: 15.99581,
    longitude: 107.99678,
    categories: ["bridge", "viewpoint", "photo-spot", "ba-na-hills"],
    shortDescription: "Diem check-in noi bat trong khu Ba Na Hills voi thiet ke ban tay nang cay cau.",
    description:
      "Cau Vang la diem check-in noi bat trong khu Ba Na Hills, thuong duoc dua vao lich trinh tour Ba Na trong ngay. Khi publish nen gan voi location Ba Na Hills hoac tour Ba Na de tranh trung lap trai nghiem.",
    imageUrls: [],
    sourceUrl: "https://banahills.sunworld.vn/en",
    sourceReferences: ["Sun World Ba Na Hills official website"],
  },
  {
    externalId: "danang-cham-sculpture-museum",
    name: "Bao tang Dieu khac Cham Da Nang",
    categorySlug: "bao-tang-di-tich",
    district: "Hai Chau",
    address: "02 2 Thang 9, Hai Chau, Da Nang",
    latitude: 16.06055,
    longitude: 108.22302,
    categories: ["museum", "heritage", "culture", "indoor"],
    shortDescription: "Bao tang trung bay nghe thuat dieu khac Champa, phu hop lich trinh van hoa trong trung tam Da Nang.",
    description:
      "Bao tang Dieu khac Cham Da Nang luu giu va trung bay bo suu tap hien vat nghe thuat Champa. Day la diem den phu hop cho khach quan tam di san, lich su va cac hoat dong trong nha.",
    imageUrls: [],
    sourceUrl: "https://visitdanang.travel/en/da-nang-museum-of-cham-sculpture-2036",
    sourceReferences: ["Visit Da Nang"],
  },
  {
    externalId: "danang-han-market",
    name: "Cho Han",
    categorySlug: "cho-dia-phuong",
    district: "Hai Chau",
    address: "119 Tran Phu, Hai Chau, Da Nang",
    latitude: 16.06805,
    longitude: 108.22431,
    categories: ["market", "shopping", "local-food", "souvenir"],
    shortDescription: "Cho trung tam gan song Han, phu hop mua dac san, qua luu niem va trai nghiem mua sam dia phuong.",
    description:
      "Cho Han la mot diem mua sam quen thuoc o trung tam Da Nang, gan truc Bach Dang - Tran Phu. Du lieu nay nen duoc bo sung anh, gio hoat dong va cac luu y mua sam truoc khi publish.",
    imageUrls: [],
    sourceUrl: "https://danangfantasticity.com/en/where-to-shop",
    sourceReferences: ["Danang Fantasticity - Where to shop"],
  },
];
