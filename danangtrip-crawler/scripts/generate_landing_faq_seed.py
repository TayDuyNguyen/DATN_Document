from __future__ import annotations

import csv
import json
import re
import unicodedata
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
SEED_OUTPUT = ROOT.parent / "database-seeders" / "25_landing_faq_blocks_seed.sql"
FAQ_JSON = DATA_DIR / "landing-faq-staging.json"
FAQ_CSV = DATA_DIR / "landing-faq-review.csv"
REPORT_OUTPUT = DATA_DIR / "landing-faq-report.json"


FAQ_GROUPS = {
    "du-lich-da-nang": {
        "title": "FAQ du lich Da Nang",
        "source_names": [
            "vietnam-travel-da-nang",
            "vietnam-travel-da-nang-itinerary",
            "vietnam-travel-da-nang-must-visit",
            "vietnam-travel-da-nang-insider-list",
            "vietnam-travel-airports",
        ],
        "items": [
            {
                "question": "Nen di Da Nang may ngay?",
                "answer": "Lich trinh 3 ngay phu hop de ket hop bien My Khe, cau Rong, Ngu Hanh Son, Son Tra va mot diem xa hon nhu Ba Na Hills hoac Hoi An.",
            },
            {
                "question": "Di tu san bay Da Nang vao trung tam co mat nhieu thoi gian khong?",
                "answer": "San bay Da Nang gan trung tam, thuan tien di taxi, xe cong nghe hoac xe dua don. Nen du phong thoi gian neu di vao gio cao diem.",
            },
            {
                "question": "Da Nang phu hop voi nhom khach nao?",
                "answer": "Da Nang phu hop voi gia dinh, cap doi, khach di lan dau, nguoi thich bien, am thuc, lich trinh ngan ngay va ket hop Hoi An/Hue.",
            },
            {
                "question": "Nen uu tien diem nao neu chi co mot ngay?",
                "answer": "Nen chon My Khe, cau Rong, Ngu Hanh Son hoac Son Tra. Neu muon di xa hon, Ba Na Hills thuong can gan tron ngay.",
            },
        ],
    },
    "cam-nang-du-lich-mien-trung": {
        "title": "FAQ du lich mien Trung",
        "source_names": [
            "vietnam-travel-plan-your-trip",
            "vietnam-travel-transport-within-vietnam",
            "vietnam-travel-motorbike-hoi-an-hue",
            "vietnam-travel-hoi-an",
            "vietnam-travel-hue",
        ],
        "items": [
            {
                "question": "Co nen ket hop Da Nang, Hoi An va Hue trong mot chuyen di?",
                "answer": "Co. Da Nang nam giua, co san bay va ket noi tot den Hoi An, Hue, Ba Na Hills, Ngu Hanh Son va My Son.",
            },
            {
                "question": "Nen di Hoi An hay Hue tu Da Nang bang cach nao?",
                "answer": "Hoi An phu hop di xe rieng, shuttle hoac xe cong nghe. Hue co the di xe rieng, tau hoa hoac hanh trinh qua deo Hai Van.",
            },
            {
                "question": "Di mien Trung can luu y gi ve thoi tiet?",
                "answer": "Nen kiem tra mua mua va lich trinh ngoai troi. Cac diem bien, deo va nui nen di khi thoi tiet on dinh de an toan hon.",
            },
            {
                "question": "Co nen thue xe may tu Hoi An di Hue qua Hai Van khong?",
                "answer": "Chi nen di neu co kinh nghiem lai xe duong deo va kiem tra thoi tiet. Khach di lan dau nen chon xe rieng, tour hoac tau hoa.",
            },
        ],
    },
    "tour-ba-na-hills": {
        "title": "FAQ tour Ba Na Hills",
        "source_names": [
            "vietnam-travel-ba-na-hills",
            "danangfantasticity-hai-van-pass",
            "vietnam-travel-da-nang-itinerary",
        ],
        "items": [
            {
                "question": "Tour Ba Na Hills nen di nua ngay hay tron ngay?",
                "answer": "Nen di tron ngay vi khu Ba Na Hills co cap treo, Cau Vang, lang Phap, khu vui choi va nhieu diem check-in.",
            },
            {
                "question": "Can chuan bi gi khi di Ba Na Hills?",
                "answer": "Nen mang giay di bo, ao khoac mong, nuoc uong, kem chong nang va den som de co thoi gian di cap treo, Cau Vang va Fantasy Park.",
            },
            {
                "question": "Ba Na Hills co phu hop gia dinh khong?",
                "answer": "Co. Khu nay phu hop gia dinh, cap doi va nhom ban, nhung can luu y viec di bo nhieu va thoi tiet tren nui co the thay doi nhanh.",
            },
        ],
    },
    "tour-son-tra-ngu-hanh-son": {
        "title": "FAQ tour Son Tra va Ngu Hanh Son",
        "source_names": [
            "vietnam-travel-marble-mountains",
            "danangfantasticity-son-tra-peninsula",
            "vietnam-travel-da-nang-insider-list",
        ],
        "items": [
            {
                "question": "Son Tra va Ngu Hanh Son co the di trong nua ngay khong?",
                "answer": "Co the di nua ngay neu chi chon cac diem chinh. Neu muon tham quan ky hang dong, chua va diem ngam canh, nen danh nhieu thoi gian hon.",
            },
            {
                "question": "Ngu Hanh Son co can leo nhieu khong?",
                "answer": "Co nhieu bac da va loi di trong hang dong, nen mang giay de di bo va han che lich trinh qua day neu di voi nguoi kho van dong.",
            },
            {
                "question": "Nen di Son Tra vao thoi diem nao?",
                "answer": "Nen di sang som hoac chieu muon de tranh nang, co anh sang dep va de ngam bien/thanh pho tot hon.",
            },
        ],
    },
}


def main() -> None:
    guides = load_json(DATA_DIR / "blog-guides-staging.json")
    source_url_by_name = {item["source_name"]: item["source_url"] for item in guides}
    groups = []

    for slug, config in FAQ_GROUPS.items():
        source_urls = [source_url_by_name[name] for name in config["source_names"] if name in source_url_by_name]
        items = []
        for faq in config["items"]:
            items.append(
                {
                    "question": ascii_text(faq["question"]),
                    "answer": ascii_text(faq["answer"]),
                    "status": "pending_review",
                    "source_urls": source_urls,
                }
            )
        groups.append(
            {
                "landing_slug": slug,
                "title": ascii_text(config["title"]),
                "status": "pending_review",
                "items": items,
                "source_urls": source_urls,
            }
        )

    FAQ_JSON.write_text(json.dumps(groups, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_csv(groups)
    SEED_OUTPUT.write_text(render_sql(groups), encoding="utf-8")

    report = {
        "output": str(SEED_OUTPUT),
        "jsonOutput": str(FAQ_JSON),
        "csvOutput": str(FAQ_CSV),
        "groups": len(groups),
        "faqItems": sum(len(group["items"]) for group in groups),
        "policy": "FAQ seed is generated from source-backed guide staging. It updates landing_pages.content_blocks as draft-review content.",
    }
    REPORT_OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=True, indent=2))


def write_csv(groups: list[dict[str, Any]]) -> None:
    rows = []
    for group in groups:
        for item in group["items"]:
            rows.append(
                {
                    "approve_for_seed": True,
                    "landing_slug": group["landing_slug"],
                    "question": item["question"],
                    "answer": item["answer"],
                    "source_urls": " | ".join(item["source_urls"]),
                    "status": item["status"],
                }
            )
    with FAQ_CSV.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()) if rows else [])
        if rows:
            writer.writeheader()
            writer.writerows(rows)


def render_sql(groups: list[dict[str, Any]]) -> str:
    statements = [
        "-- DanangTrip landing FAQ blocks seed",
        "-- FILE: 25_landing_faq_blocks_seed.sql",
        "-- Source: danangtrip-crawler/data/landing-faq-staging.json",
        "-- Policy: text-only FAQ blocks generated from source-backed guide staging; no images.",
        "-- Run after 18_landing_pages_seed.sql.",
        "",
        "BEGIN;",
        "",
    ]
    for group in groups:
        content_blocks = {
            "sections": [
                {
                    "type": "faq",
                    "title": group["title"],
                    "items": [
                        {
                            "question": item["question"],
                            "answer": item["answer"],
                        }
                        for item in group["items"]
                    ],
                }
            ],
            "source_notes": [
                "FAQ draft generated from source-backed guide staging.",
                "No image generation.",
                "Editor review required before public use.",
            ],
            "source_urls": group["source_urls"],
        }
        statements.extend(
            [
                f"-- FAQ update for {group['landing_slug']}",
                "UPDATE landing_pages",
                f"SET content_blocks = {sql_string(json.dumps(content_blocks, ensure_ascii=False))}::json,",
                "    updated_at = NOW()",
                f"WHERE slug = {sql_string(group['landing_slug'])};",
                "",
            ]
        )
    statements.extend(["COMMIT;", ""])
    return "\n".join(statements)


def sql_string(value: Any) -> str:
    if value is None or value == "":
        return "NULL"
    return "'" + ascii_text(str(value)).replace("'", "''") + "'"


def ascii_text(value: Any) -> str:
    text = str(value)
    replacements = {
        "Đ": "D",
        "đ": "d",
        "’": "'",
        "‘": "'",
        "“": '"',
        "”": '"',
        "–": "-",
        "—": "-",
        "…": "...",
    }
    for source, target in replacements.items():
        text = text.replace(source, target)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(char for char in text if not unicodedata.combining(char))
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
