from __future__ import annotations

import csv
import json
import re
import unicodedata
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
SEED_OUTPUT = ROOT.parent / "database-seeders" / "22_approved_blog_guides_seed.sql"

CATEGORY_HINT_TO_ID = {
    "cam-nang-da-nang": 24,
    "cam-nang-hoi-an": 22,
    "cam-nang-hue": 23,
    "lich-trinh": 5,
    "diem-den": 3,
    "bien": 64,
    "am-thuc": 2,
    "di-chuyen": 30,
    "kinh-nghiem": 1,
    "thoi-tiet": 11,
}


def main() -> None:
    items = load_json(DATA_DIR / "blog-guides-staging.json")
    approved = [item for item in items if not item.get("review_flags")]
    pending = [item for item in items if item.get("review_flags")]

    write_approval_files(approved, pending)
    SEED_OUTPUT.write_text(render_sql(approved), encoding="utf-8")

    report = {
        "output": str(SEED_OUTPUT),
        "approved": len(approved),
        "pending": len(pending),
        "policy": "Approve blog guide staging records without review_flags. Keep redirected/deduped records pending.",
        "firstId": 201,
        "categoryMap": CATEGORY_HINT_TO_ID,
    }
    report_path = DATA_DIR / "approved-blog-guides-seed-report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=True, indent=2))


def write_approval_files(approved: list[dict[str, Any]], pending: list[dict[str, Any]]) -> None:
    approved_path = DATA_DIR / "approved-blog-guides-review.json"
    pending_path = DATA_DIR / "pending-blog-guides-review.json"
    approved_csv = DATA_DIR / "approved-blog-guides-review.csv"
    pending_csv = DATA_DIR / "pending-blog-guides-review.csv"

    approved_rows = [review_row(item, True) for item in approved]
    pending_rows = [review_row(item, False) for item in pending]

    approved_path.write_text(json.dumps(approved_rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    pending_path.write_text(json.dumps(pending_rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_csv(approved_csv, approved_rows)
    write_csv(pending_csv, pending_rows)


def review_row(item: dict[str, Any], approve: bool) -> dict[str, Any]:
    return {
        "approve_for_seed": approve,
        "title": item.get("title"),
        "slug": item.get("slug"),
        "category_hint": item.get("category_hint"),
        "category_id": CATEGORY_HINT_TO_ID.get(item.get("category_hint"), 1),
        "source_name": item.get("source_name"),
        "source_url": item.get("source_url"),
        "review_flags": item.get("review_flags") or [],
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames = ["approve_for_seed", "title", "slug", "category_hint", "category_id", "source_name", "source_url", "review_flags"]
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            row = dict(row)
            row["review_flags"] = ", ".join(row.get("review_flags") or [])
            writer.writerow(row)


def render_sql(items: list[dict[str, Any]]) -> str:
    post_rows = []
    pivot_rows = []
    for index, item in enumerate(items):
        post_id = 201 + index
        category_id = CATEGORY_HINT_TO_ID.get(item.get("category_hint"), 1)
        content = normalize_content(item)
        post_rows.append(
            "("
            f"{post_id}, "
            f"{sql_string(item.get('title'))}, "
            f"{sql_string(item.get('slug'))}, "
            f"{sql_string(build_excerpt(item))}, "
            f"{sql_string(content)}, "
            "NULL, "
            "2, "
            "0, "
            "'draft', "
            "NULL, "
            "NOW(), NOW()"
            ")"
        )
        pivot_rows.append(f"({post_id}, {category_id})")

    return "\n".join(
        [
            "-- DanangTrip approved source-backed blog guide seed",
            "-- FILE: 22_approved_blog_guides_seed.sql",
            "-- Source: danangtrip-crawler/data/blog-guides-staging.json",
            "-- Policy: inserts only approved records without review flags; status remains draft.",
            "-- Run after 03_tour_blog_categories.sql and 04_users.sql.",
            "",
            "BEGIN;",
            "",
            "INSERT INTO blog_posts (id, title, slug, excerpt, content, featured_image, author_id, view_count, status, published_at, created_at, updated_at) VALUES",
            ",\n".join(post_rows),
            "ON CONFLICT (slug) DO NOTHING;",
            "",
            "INSERT INTO blog_post_categories (post_id, blog_category_id) VALUES",
            ",\n".join(pivot_rows),
            "ON CONFLICT (post_id, blog_category_id) DO NOTHING;",
            "",
            "SELECT setval(pg_get_serial_sequence('blog_posts', 'id'), GREATEST((SELECT MAX(id) FROM blog_posts), 1));",
            "",
            "COMMIT;",
            "",
        ]
    )


def normalize_content(item: dict[str, Any]) -> str:
    title = ascii_text(item.get("title") or "Travel guide")
    category = ascii_text(item.get("category_hint") or "cam-nang")
    tags = ", ".join(ascii_text(tag) for tag in (item.get("tags_hint") or []))
    source_name = ascii_text(item.get("source_name") or "")
    source_url = ascii_text(item.get("source_url") or "")
    topic = infer_topic(title, category)
    return "\n".join(
        [
            title,
            "",
            "Ban nhap source-backed cho DanangTrip.",
            "",
            "Tom tat rewrite:",
            f"- Chu de: {topic}.",
            f"- Nhom noi dung: {category}.",
            f"- Tu khoa goi y: {tags or 'du lich mien Trung'}.",
            "- Noi dung nen bien tap thanh bai cam nang ngan gon, uu tien thong tin thuc te ve diem den, lich trinh, thoi diem tham quan, di chuyen va luu y cho du khach.",
            "- Khong publish truc tiep neu chua duoc bien tap lai bang giong van DanangTrip.",
            "",
            f"Nguon tham chieu: {source_name}",
            f"Source URL: {source_url}",
            "Trang thai: draft. Can bien tap truoc khi published.",
        ]
    )


def build_excerpt(item: dict[str, Any]) -> str:
    title = ascii_text(item.get("title") or "Travel guide")
    category = ascii_text(item.get("category_hint") or "cam-nang")
    topic = infer_topic(title, category)
    return f"Ban nhap cam nang ve {topic}, duoc thu thap tu nguon cong khai va can bien tap truoc khi publish."


def infer_topic(title: str, category: str) -> str:
    lower = title.lower()
    if "da nang" in lower:
        return "cam nang va trai nghiem du lich Da Nang"
    if "hoi an" in lower:
        return "cam nang va trai nghiem du lich Hoi An"
    if "hue" in lower:
        return "cam nang va trai nghiem du lich Hue"
    if "ba na" in lower:
        return "trai nghiem Ba Na Hills va khu vuc Cau Vang"
    if "marble" in lower:
        return "tham quan Ngu Hanh Son va cac hang dong/chua"
    if "my son" in lower:
        return "tham quan Thanh dia My Son va di san Cham"
    if "hai van" in lower:
        return "tham quan deo Hai Van va hanh trinh Da Nang - Hue"
    if "son tra" in lower:
        return "tham quan ban dao Son Tra"
    if "beach" in lower:
        return "cam nang bien Da Nang"
    if "food" in lower or "pork" in lower:
        return "am thuc dia phuong Da Nang"
    return category.replace("-", " ")


def sql_string(value: Any) -> str:
    if value is None or value == "":
        return "NULL"
    return "'" + ascii_text(str(value)).replace("'", "''")[:8000] + "'"


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
