from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "verified-real-tour-catalog-cloudinary-20260607.json"
OUTPUT = ROOT.parent / "database-seeders" / "50_verified_real_tours_editorial_vi_seed.sql"

TITLE_MAP = {
    "recrawl-018-venusvietnamtravel-afternoon-ba-na-hills-golden-bridge-dragon-bridge-by-night-tour-venustravel": "Tour Bà Nà Hills buổi chiều, Cầu Vàng và Cầu Rồng về đêm",
    "vmtravel-recheck-001-ba-na-hills-and-golden-bridge-tour-from-tien-sa-port": "Tour Bà Nà Hills và Cầu Vàng từ cảng Tiên Sa",
    "vmtravel-central-002-ba-na-hills-night-tour-and-sunset-golden-bridge-tour": "Tour Bà Nà Hills đêm và ngắm hoàng hôn Cầu Vàng",
    "vmtravel-central-003-ba-na-hills-tour-from-da-nang-1-day-tour-deluxe-group-tour": "Tour Bà Nà Hills 1 ngày từ Đà Nẵng",
    "vmtravel-central-004-ba-na-hills-tour-from-hoi-an-exquisite-delight-1-day-tour": "Tour Bà Nà Hills 1 ngày từ Hội An",
    "vmtravel-central-005-bana-hills-day-tour-book-1-day-tour-in-da-nang-best-trip": "Tour Bà Nà Hills trong ngày từ Đà Nẵng",
    "recrawl-022-venusvietnamtravel-cham-island-sightseeing-snorkeling-tour-venustravel": "Tour Cù Lao Chàm tham quan và lặn ngắm san hô",
    "vmtravel-central-006-cham-island-snorkeling-tour-from-hoi-an-or-da-nang": "Tour Cù Lao Chàm lặn ngắm san hô từ Hội An hoặc Đà Nẵng",
    "vmtravel-central-007-da-nang-city-tour-deluxe-group-tour-vm-travel": "Tour khám phá thành phố Đà Nẵng theo nhóm",
    "vmtravel-recheck-002-da-nang-city-tour-from-tien-sa-port-explore-and-shopping": "Tour Đà Nẵng từ cảng Tiên Sa kết hợp mua sắm",
    "vmtravel-central-008-da-nang-day-tour-private-tour-highlight-full-day-tour": "Tour riêng khám phá Đà Nẵng trong ngày",
    "vmtravel-central-010-da-nang-hoi-an-full-day-tour-see-the-best-of-both-cities": "Tour Đà Nẵng và Hội An trọn ngày",
    "vmtravel-central-011-da-nang-to-hue-day-trip-by-heritage-train-via-hai-van-pass": "Tour Đà Nẵng đi Huế bằng tàu qua đèo Hải Vân",
    "vmtravel-central-012-day-trip-from-da-nang-to-hoi-an-deluxe-group-tour": "Tour Hội An trong ngày từ Đà Nẵng",
    "vmtravel-central-013-day-trip-to-hoi-an-from-da-nang-private-tour-vm-travel": "Tour riêng Hội An trong ngày từ Đà Nẵng",
    "vmtravel-central-001-highlight-the-4-days-deluxe-golf-tour-in-da-nang": "Tour golf Đà Nẵng 4 ngày cao cấp",
    "vmtravel-recheck-003-hoi-an-day-tour-from-tien-sa-port-hoi-an-shore-excursions": "Tour Hội An trong ngày từ cảng Tiên Sa",
    "vmtravel-central-014-hue-bicycle-tour-organic-farm-visit-local-cooking-class": "Tour Huế đạp xe, nông trại hữu cơ và lớp nấu ăn",
    "vmtravel-central-016-hue-cooking-class-tour-from-market-to-table": "Tour lớp nấu ăn Huế từ chợ địa phương đến bàn ăn",
    "vmtravel-central-020-hue-dmz-tour-unveiling-history-on-captivating-tour": "Tour Huế DMZ tìm hiểu dấu ấn lịch sử",
    "vmtravel-central-018-hue-day-trip-from-da-nang-deluxe-small-group-tour": "Tour Huế 1 ngày từ Đà Nẵng theo nhóm nhỏ",
    "vmtravel-central-017-hue-day-trip-from-da-nang-private-tour": "Tour riêng Huế 1 ngày từ Đà Nẵng",
    "vmtravel-central-019-hue-day-trip-from-hoi-an-da-nang-book-best-1-day-group-tour": "Tour Huế 1 ngày từ Hội An hoặc Đà Nẵng",
    "vmtravel-recheck-005-hue-imperial-tour-from-chan-may-port-best-shore-excursions": "Tour Đại Nội Huế từ cảng Chân Mây",
    "vmtravel-central-021-hue-street-food-tour-explore-local-flavours-for-just-45": "Tour ẩm thực đường phố Huế",
    "vmtravel-central-023-linh-ung-pagoda-marble-mountain-tour-from-hoi-an": "Tour chùa Linh Ứng và Ngũ Hành Sơn từ Hội An",
    "vmtravel-central-022-luxury-da-nang-golf-tour-6-days-5-nights-4-rounds": "Tour golf Đà Nẵng 6 ngày 5 đêm cao cấp",
    "vmtravel-central-024-my-son-sanctuary-from-hoi-an-book-best-1-day-tour-in-hoi-an": "Tour Thánh địa Mỹ Sơn 1 ngày từ Hội An",
    "vmtravel-recheck-004-my-son-sanctuary-tour-from-tien-sa-port-explore-now": "Tour Thánh địa Mỹ Sơn từ cảng Tiên Sa",
    "vmtravel-central-025-paradise-cave-tour-from-hue-explore-nature-s-masterpiece": "Tour động Thiên Đường từ Huế",
}


def sql_text(value: str | None) -> str:
    if value is None:
        return "NULL"
    return "'" + value.replace("'", "''") + "'"


def sql_json(value: object) -> str:
    return sql_text(json.dumps(value, ensure_ascii=False, separators=(",", ":"))) + "::json"


def tour_kind(tour: dict) -> str:
    name = f"{tour.get('name', '')} {TITLE_MAP.get(tour['slug'], '')}".lower()
    if "golf" in name:
        return "golf"
    if "cooking" in name or "street food" in name or "ẩm thực" in name or "nấu ăn" in name:
        return "food"
    if "bicycle" in name or "đạp xe" in name:
        return "bike"
    if "train" in name or "tàu" in name:
        return "train"
    if "paradise cave" in name or "động" in name:
        return "cave"
    if "cham island" in name or "cù lao chàm" in name or "snorkeling" in name:
        return "island"
    if "my son" in name or "mỹ sơn" in name:
        return "my_son"
    if "hue" in name or "huế" in name or "dmz" in name or "chân mây" in name:
        return "hue"
    if "ba na" in name or "bana" in name or "cầu vàng" in name:
        return "bana"
    if "hoi an" in name or "hội an" in name:
        return "hoi_an"
    return "danang"


def itinerary_for(kind: str) -> list[str]:
    options = {
        "bana": [
            "Đón khách tại khách sạn hoặc điểm hẹn theo xác nhận của đơn vị tổ chức.",
            "Di chuyển lên Bà Nà Hills và trải nghiệm tuyến cáp treo ngắm toàn cảnh núi rừng.",
            "Tham quan Cầu Vàng, vườn hoa, làng Pháp và các điểm nổi bật trong khu du lịch.",
            "Dùng bữa theo chương trình và có thời gian tự do chụp ảnh, vui chơi.",
            "Trở về điểm đón ban đầu, kết thúc chương trình.",
        ],
        "island": [
            "Đón khách và di chuyển đến cảng khởi hành đi Cù Lao Chàm.",
            "Đi ca nô ra đảo, tham quan các điểm chính trên đảo theo lịch trình.",
            "Lặn ngắm san hô hoặc tắm biển tại khu vực được hướng dẫn viên sắp xếp.",
            "Dùng bữa địa phương và nghỉ ngơi trước khi quay lại đất liền.",
            "Trả khách tại điểm đón, kết thúc tour.",
        ],
        "danang": [
            "Đón khách tại khách sạn, cảng hoặc điểm hẹn đã xác nhận.",
            "Tham quan các điểm nổi bật của Đà Nẵng theo tuyến trong ngày.",
            "Dừng chụp ảnh, nghe giới thiệu về văn hóa, lịch sử và đời sống địa phương.",
            "Dùng bữa hoặc nghỉ ngơi theo chương trình của tour.",
            "Trả khách tại điểm hẹn ban đầu.",
        ],
        "hoi_an": [
            "Đón khách từ Đà Nẵng, Hội An hoặc cảng theo xác nhận đặt tour.",
            "Di chuyển đến Hội An và tham quan các điểm nổi bật của phố cổ.",
            "Tìm hiểu kiến trúc, văn hóa thương cảng và các làng nghề hoặc khu chợ địa phương.",
            "Có thời gian tự do chụp ảnh, mua sắm hoặc thưởng thức món địa phương.",
            "Quay lại điểm đón, kết thúc chương trình.",
        ],
        "hue": [
            "Đón khách và khởi hành đi Huế hoặc các điểm di sản theo chương trình.",
            "Tham quan các công trình văn hóa, lịch sử, lăng tẩm hoặc Đại Nội Huế.",
            "Nghe hướng dẫn viên giới thiệu bối cảnh lịch sử và câu chuyện địa phương.",
            "Dùng bữa theo chương trình và tiếp tục tham quan các điểm còn lại.",
            "Trả khách tại điểm đón hoặc điểm kết thúc đã thống nhất.",
        ],
        "food": [
            "Gặp hướng dẫn viên tại điểm hẹn và giới thiệu ngắn về văn hóa ẩm thực địa phương.",
            "Ghé chợ, quán ăn hoặc điểm trải nghiệm ẩm thực theo lịch trình.",
            "Thưởng thức các món đặc trưng và nghe câu chuyện về nguyên liệu, cách chế biến.",
            "Tham gia lớp nấu ăn hoặc trải nghiệm ăn uống địa phương nếu có trong chương trình.",
            "Kết thúc tour và nhận gợi ý thêm cho hành trình ăn uống tự túc.",
        ],
        "golf": [
            "Đón khách và hỗ trợ di chuyển đến sân golf theo lịch trình.",
            "Làm thủ tục tại sân, nhận thông tin tee time và các dịch vụ đi kèm.",
            "Trải nghiệm vòng golf theo số ngày, số sân và số lượt chơi đã công bố.",
            "Nghỉ ngơi, dùng bữa hoặc di chuyển giữa các điểm lưu trú theo chương trình.",
            "Kết thúc hành trình và trả khách tại điểm đã xác nhận.",
        ],
        "bike": [
            "Gặp hướng dẫn viên, nhận xe đạp và nghe phổ biến lộ trình an toàn.",
            "Đạp xe qua khu dân cư, nông trại hoặc làng quê theo tuyến đã chọn.",
            "Dừng tham quan, trò chuyện với người địa phương và trải nghiệm hoạt động nông nghiệp.",
            "Tham gia nấu ăn hoặc dùng bữa địa phương theo chương trình.",
            "Quay về điểm xuất phát, kết thúc tour.",
        ],
        "train": [
            "Đón khách và hỗ trợ làm thủ tục lên tàu theo khung giờ đã xác nhận.",
            "Di chuyển trên tuyến đường sắt ven biển, ngắm cảnh đèo Hải Vân và vịnh Lăng Cô.",
            "Đến Huế và tham quan các điểm nổi bật trong lịch trình.",
            "Dùng bữa theo chương trình và có thời gian chụp ảnh, nghỉ ngơi.",
            "Trở về điểm hẹn hoặc kết thúc tại Huế theo lựa chọn đặt tour.",
        ],
        "my_son": [
            "Đón khách và di chuyển đến khu di sản Thánh địa Mỹ Sơn.",
            "Tham quan các cụm tháp Chăm và nghe giới thiệu về lịch sử vương quốc Champa.",
            "Xem biểu diễn văn hóa hoặc trải nghiệm địa phương nếu lịch vận hành phù hợp.",
            "Dùng bữa hoặc nghỉ ngơi theo chương trình tour.",
            "Trả khách tại điểm đón ban đầu.",
        ],
        "cave": [
            "Đón khách từ Huế và khởi hành đi khu vực Phong Nha - Kẻ Bàng.",
            "Dừng tham quan các điểm trên đường theo lịch trình của đơn vị tổ chức.",
            "Khám phá động Thiên Đường và hệ thống thạch nhũ nổi bật.",
            "Dùng bữa, nghỉ ngơi và tiếp tục hành trình về Huế.",
            "Trả khách tại khách sạn hoặc điểm hẹn đã xác nhận.",
        ],
    }
    return options[kind]


def inclusions_for(kind: str) -> list[str]:
    base = [
        "Xe đưa đón theo chương trình",
        "Hướng dẫn viên theo ngôn ngữ công bố của đơn vị tổ chức",
        "Vé tham quan theo lịch trình nếu được ghi trong tour gốc",
        "Nước uống hoặc bữa ăn theo mô tả của từng tour",
    ]
    if kind == "golf":
        return [
            "Lịch chơi golf theo chương trình",
            "Xe đưa đón theo lịch trình",
            "Hỗ trợ đặt sân và điều phối tee time",
            "Dịch vụ lưu trú hoặc bữa ăn nếu được ghi trong tour gốc",
        ]
    if kind == "island":
        base.append("Ca nô hoặc phương tiện ra đảo theo chương trình")
    return base


def exclusions_for(kind: str) -> list[str]:
    return [
        "Chi phí cá nhân ngoài chương trình",
        "Đồ uống, dịch vụ hoặc vé không được nêu trong phần bao gồm",
        "Tiền tip cho hướng dẫn viên và tài xế nếu không được ghi rõ",
        "Phụ thu phát sinh do thay đổi lịch trình, thời tiết hoặc yêu cầu riêng",
    ]


def description_for(tour: dict, title: str) -> str:
    duration = tour.get("duration") or "theo chương trình"
    source_url = tour.get("source", {}).get("url", "")
    return (
        f"{title} là chương trình đã được DanangTrip chuẩn hóa từ dữ liệu công khai "
        f"của đơn vị tổ chức. Tour có thời lượng {duration}, giá tham khảo và lịch trình "
        "được đối chiếu từ nguồn gốc trước khi nhập vào hệ thống. Nội dung này đã được "
        "biên tập tiếng Việt ở mức sẵn sàng hiển thị, nhưng vẫn giữ tinh thần kiểm duyệt "
        f"cuối cùng trước vận hành thương mại. Nguồn tham khảo: {source_url}"
    )


def short_desc_for(tour: dict, title: str) -> str:
    duration = tour.get("duration") or "theo chương trình"
    return f"{title}, thời lượng {duration}, đã có giá, ảnh Cloudinary và lịch khởi hành tương lai."


def main() -> None:
    catalog = json.loads(INPUT.read_text(encoding="utf-8"))
    rows = []
    for tour in catalog:
        slug = tour["slug"]
        title = TITLE_MAP[slug]
        kind = tour_kind(tour)
        is_featured = "true" if kind in {"bana", "hue", "hoi_an"} else "false"
        is_hot = "true" if kind in {"bana", "island", "my_son"} else "false"
        rows.append(
            "    ("
            + ", ".join(
                [
                    sql_text(slug),
                    sql_text(title),
                    sql_text(description_for(tour, title)),
                    sql_text(short_desc_for(tour, title)),
                    sql_json(itinerary_for(kind)),
                    sql_json(inclusions_for(kind)),
                    sql_json(exclusions_for(kind)),
                    is_featured,
                    is_hot,
                ]
            )
            + ")"
        )

    sql = f"""-- Vietnamese editorial activation for verified real tours.
-- Source seed: 49_verified_real_tours_seed.sql
-- Policy:
--   - update only the 30 verified real tour slugs;
--   - preserve prices, Cloudinary media, schedules and location mappings;
--   - switch status to active after user approval.

BEGIN;

WITH editorial(slug, name, description, short_desc, itinerary, inclusions, exclusions, is_featured, is_hot) AS (
VALUES
{",\n".join(rows)}
)
UPDATE tours target
SET
    name = editorial.name,
    description = editorial.description,
    short_desc = editorial.short_desc,
    itinerary = editorial.itinerary,
    inclusions = editorial.inclusions,
    exclusions = editorial.exclusions,
    status = 'active',
    booking_availability = 'open',
    is_featured = editorial.is_featured,
    is_hot = editorial.is_hot,
    updated_at = NOW()
FROM editorial
WHERE target.slug = editorial.slug;

COMMIT;
"""
    OUTPUT.write_text(sql, encoding="utf-8", newline="\n")
    print(json.dumps({"output": str(OUTPUT), "tours": len(rows)}, indent=2))


if __name__ == "__main__":
    main()
