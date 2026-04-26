"""
Cap nhat sort_order cua categories dua tren so luong location
- Category co nhieu location nhat → sort_order nho nhat (len dau)
- Category test (khong co location) → sort_order lon (xuong cuoi)
Run: python tests/scripts/update_category_sort_order.py
"""
import psycopg2
import requests

BASE = "http://localhost:8000/api/v1"
hp   = {"Accept": "application/json"}

DB_HOST = "aws-1-ap-northeast-1.pooler.supabase.com"
DB_PORT = "5432"
DB_USER = "postgres.bucmucgvsuawrpompyvu"
DB_PASS = "taybkdn@2004"
DB_NAME = "postgres"

def get_location_count(category_id):
    """Dem so location thuoc category."""
    r = requests.get(BASE+"/locations", headers=hp,
                     params={"category_id": category_id, "per_page": 1}, timeout=15)
    if r.status_code == 200:
        return r.json().get("data", {}).get("total", 0)
    return 0

def main():
    # 1. Lay tat ca categories
    cats = requests.get(BASE+"/categories", headers=hp, timeout=15).json()["data"]
    real_cats = [c for c in cats if c["status"] == "active"]
    print(f"Tong so categories: {len(real_cats)}")

    # 2. Dem so location cho tung category
    print("\nDang dem location cho tung category...")
    cat_counts = []
    for c in real_cats:
        count = get_location_count(c["id"])
        cat_counts.append({
            "id":         c["id"],
            "name":       c["name"],
            "count":      count,
            "is_test":    any(x in c["name"] for x in ["TC", "1775", "Seed", "Linked", "Cat "])
        })
        print(f"  id={c['id']:3d} count={count:3d} {'[TEST]' if cat_counts[-1]['is_test'] else '      '} {c['name']}")

    # 3. Sap xep: category thuc co nhieu location len dau, test xuong cuoi
    real = sorted([c for c in cat_counts if not c["is_test"] and c["count"] > 0],
                  key=lambda x: -x["count"])
    real_empty = [c for c in cat_counts if not c["is_test"] and c["count"] == 0]
    test_cats  = [c for c in cat_counts if c["is_test"]]

    ordered = real + real_empty + test_cats

    print("\nThu tu moi (sort_order se duoc cap nhat):")
    updates = []
    for i, c in enumerate(ordered):
        new_order = i + 1
        updates.append((new_order, c["id"]))
        marker = "★" if not c["is_test"] and c["count"] > 0 else ("○" if not c["is_test"] else "✗")
        print(f"  {marker} sort_order={new_order:3d}  count={c['count']:3d}  {c['name']}")

    # 4. Cap nhat DB
    print("\nCap nhat sort_order vao DB...")
    conn = psycopg2.connect(
        host=DB_HOST, port=DB_PORT,
        user=DB_USER, password=DB_PASS,
        dbname=DB_NAME, sslmode="require", connect_timeout=15
    )
    cur = conn.cursor()
    for new_order, cat_id in updates:
        cur.execute("UPDATE categories SET sort_order = %s WHERE id = %s",
                    (new_order, cat_id))
    conn.commit()
    cur.close()
    conn.close()

    print(f"\nDa cap nhat sort_order cho {len(updates)} categories.")
    print("\nTop 6 category se hien thi tren trang chu:")
    for c in ordered[:6]:
        print(f"  {c['name']} ({c['count']} locations)")

if __name__ == "__main__":
    main()
