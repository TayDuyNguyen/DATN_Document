# Crawl Results

## 2026-05-31 - Overpass Da Nang POIs

Command:

```powershell
npm.cmd run crawl:overpass
```

Output:

```text
data/overpass-danang-pois.json
```

Result summary:

| Metric | Count |
| --- | ---: |
| Total items | 942 |
| Location items | 218 |
| Restaurant/cafe items | 483 |
| Hotel/stay items | 241 |

Category summary:

| Category slug | Count |
| --- | ---: |
| `check-in-noi-tieng` | 145 |
| `hang-dong-nui-non` | 15 |
| `bao-tang-di-tich` | 24 |
| `cong-vien-nuoc` | 4 |
| `ca-phe-tra-sua` | 251 |
| `am-thuc-dia-phuong` | 233 |
| `khach-san-homestay` | 240 |
| `cong-vien-vuon-hoa` | 30 |

Data source:

- OpenStreetMap contributors
- Overpass API

Status:

- All records are normalized as `pending_review`.
- Data has not been inserted into production tables.
- Image enrichment has not run yet because `PEXELS_API_KEY` is not configured.

Recommended next step:

1. Remove low-quality names.
2. Deduplicate against existing `locations`.
3. Add Pexels image enrichment.
4. Generate SQL seed/staging insert only after review.

## 2026-05-31 - Overpass Quality Filter

Command:

```powershell
npm.cmd run filter:overpass
```

Outputs:

```text
data/overpass-danang-pois-clean.json
data/overpass-danang-pois-rejected.json
data/overpass-quality-report.json
../database-seeders/13_overpass_quality_review_seed.sql
```

Result summary:

| Metric | Count |
| --- | ---: |
| Input items | 942 |
| Unique after dedupe | 940 |
| Clean pending-review items | 580 |
| Rejected items | 360 |

Clean split:

| Entity | Count |
| --- | ---: |
| `location` | 180 |
| `restaurant` | 220 |
| `hotel` | 180 |

Clean category split:

| Category slug | Count |
| --- | ---: |
| `check-in-noi-tieng` | 116 |
| `hang-dong-nui-non` | 13 |
| `bao-tang-di-tich` | 19 |
| `cong-vien-nuoc` | 3 |
| `ca-phe-tra-sua` | 73 |
| `am-thuc-dia-phuong` | 148 |
| `khach-san-homestay` | 179 |
| `cong-vien-vuon-hoa` | 29 |

Quality rule:

- Minimum score: `58`
- Max per entity:
  - `location`: 180
  - `restaurant`: 220
  - `hotel`: 180
- Obvious generic/test names are rejected.
- Overflow items beyond target count are marked `rejected` with reason `over_entity_limit`.

