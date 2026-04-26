import psycopg2
from collections import Counter

DB_HOST = "aws-1-ap-northeast-1.pooler.supabase.com"
DB_PORT = "5432"
DB_USER = "postgres.bucmucgvsuawrpompyvu"
DB_PASS = "taybkdn@2004"
DB_NAME = "postgres"

conn = psycopg2.connect(
    host=DB_HOST, port=DB_PORT,
    user=DB_USER, password=DB_PASS,
    dbname=DB_NAME, sslmode="require", connect_timeout=15
)
cur = conn.cursor()

tables = [
    ("tours",          "status",         "active | inactive | sold_out"),
    ("tour_schedules", "status",         "available | full | cancelled"),
    ("locations",      "status",         "active | inactive"),
    ("categories",     "status",         "active | inactive"),
    ("bookings",       "booking_status", "pending | confirmed | cancelled | completed"),
    ("bookings",       "payment_status", "unpaid | paid | failed | refunded"),
    ("payments",       "payment_status", "pending | success | failed | refunded"),
    ("ratings",        "status",         "pending | approved | rejected"),
    ("blog_posts",     "status",         "draft | published | archived"),
    ("contacts",       "status",         "new | read | replied"),
]

print("="*65)
print(f"{'Table':<20} {'Column':<20} {'Values in DB'}")
print("="*65)

issues = []
for table, col, expected in tables:
    try:
        cur.execute(f"SELECT {col}, COUNT(*) FROM {table} GROUP BY {col} ORDER BY COUNT(*) DESC")
        rows = cur.fetchall()
        values = {r[0]: r[1] for r in rows}
        values_str = ", ".join([f"{v}({c})" for v, c in values.items()])

        # Kiem tra co gia tri ngoai expected khong
        expected_set = set(expected.split(" | "))
        actual_set   = set(values.keys())
        unexpected   = actual_set - expected_set

        flag = " ⚠️ SAIGIÁ TRỊ" if unexpected else " ✅"
        print(f"  {table:<20} {col:<20} {values_str}{flag}")
        if unexpected:
            issues.append((table, col, unexpected, expected))
    except Exception as e:
        print(f"  {table:<20} {col:<20} ERROR: {e}")

cur.close()
conn.close()

if issues:
    print("\n" + "="*65)
    print("CÁC VẤN ĐỀ CẦN SỬA:")
    for table, col, unexpected, expected in issues:
        print(f"\n  Bảng: {table}.{col}")
        print(f"  Giá trị sai: {unexpected}")
        print(f"  Giá trị đúng theo schema: {expected}")
        print(f"  → Cần UPDATE {table} SET {col}=... WHERE {col} IN {tuple(unexpected)}")
else:
    print("\n✅ Tất cả status values đều đúng theo schema!")
