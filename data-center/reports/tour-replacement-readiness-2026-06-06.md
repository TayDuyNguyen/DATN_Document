# Tour Replacement Readiness - 2026-06-06

## Decision

Do not replace the 80 synthetic live tour variants yet.

The existing crawler review marked 34/36 tours as approved using a permissive rule. A stricter production gate found only 4 tours ready for final manual verification and 32 requiring recrawl.

## Strict gate

Required:

- Direct source URL.
- Directly parsed price and original price text.
- No inferred price or duration.
- At least three itinerary items.
- At least two inclusion and exclusion items.
- At least two image candidates.
- Plausible duration for the route and itinerary size.
- Manual image relevance review before publishing.

## Result

- Total crawled tours: 36
- Ready for manual publish: 4
- Needs recrawl: 32

Blocking reasons:

- Incomplete itinerary: 17
- Suspicious duration: 14
- Incomplete exclusions: 8
- Incomplete inclusions: 7
- Inferred core field: 4

## Ready candidates

1. Hue Tour From Da Nang - Da Nang Local Tours
2. Am Phu Cave Tour with Marble Mountain and Lady Buddha - HoiAn Day Trip
3. Ba Na Hills Afternoon Tour with Golden Hands Bridge - HoiAn Day Trip
4. Ba Na Hills Early Morning Tour to Beat the Crowds - HoiAn Day Trip

These records still require a final source-page and image relevance check before database publication.

## Outputs

- `danangtrip-crawler/data/tour-publish-readiness.json`
- `danangtrip-crawler/data/tour-publish-readiness.csv`
- `danangtrip-crawler/data/tour-publish-readiness-report.json`
- `danangtrip-crawler/scripts/audit_tour_publish_readiness.py`

## Next action

Recrawl only the 32 failed source URLs, then run the strict gate again. A replacement seed should only be generated after enough unique real tours pass the gate to preserve catalog coverage.

## Targeted recrawl result

Completed on 2026-06-06:

- URLs requested: 32
- URLs collected: 32
- Network failures: 0
- Robots exclusions: 0
- Staging rows: 32
- Rows passing the strict gate after recrawl: 0

The recrawl reproduced the same blockers:

- Incomplete itinerary: 17
- Suspicious duration: 14
- Incomplete exclusions: 8
- Incomplete inclusions: 7
- Inferred core fields: 4

Conclusion: repeated crawling will not improve this batch. The extraction parser must be updated for each operator layout, especially duration and section parsing.

Recrawl outputs:

- `danangtrip-crawler/data/tour-recrawl-20260606-raw.json`
- `danangtrip-crawler/data/tour-recrawl-20260606-normalized.json`
- `danangtrip-crawler/data/tour-recrawl-20260606-report.json`
- `danangtrip-crawler/data/tour-recrawl-staging-20260606.json`
- `danangtrip-crawler/data/tour-recrawl-enriched-20260606.json`
- `danangtrip-crawler/data/tour-recrawl-readiness-20260606.json`

## Parser v3 and image validation - 2026-06-07

The crawler now has operator-aware extraction for:

- Venus Vietnam Travel itinerary and service sections.
- VM Travel duration, itinerary, inclusion, and exclusion sections.
- Heading-bounded sections for Da Nang Local Tours.
- Open Graph primary images and title-relevant gallery images.

The image gate now rejects logos, TripAdvisor assets, menu images, unrelated
tour thumbnails, and records with fewer than two relevant image candidates.

Final strict result from the latest successful responses:

- Source URLs requested: 32
- URLs collected: 28
- Temporary DNS failures: 4
- Detail records after normalization: 27
- Ready for manual publish: 4
- Blocked: 23

Ready candidates:

1. Ba Na Hills And Golden Bridge Tour From Tien Sa Port
2. Da Nang City Tour From Tien Sa Port - Explore and Shopping
3. My Son Sanctuary Tour From Tien Sa Port - Explore Now
4. Hue Imperial Tour from Chan May Port: Best Shore Excursions

Each ready candidate has a direct price, direct duration, complete itinerary,
inclusions and exclusions, and eight source-relevant image candidates.

Remaining primary blockers:

- Insufficient images: 14
- Suspicious duration: 9
- Irrelevant images: 9
- Incomplete inclusions: 7
- Incomplete exclusions: 7
- Incomplete itinerary: 6
- Inferred core field: 4

No database write or replacement seed was performed. The live synthetic tour
catalog must remain unchanged until enough real records pass this stricter gate.

Latest outputs:

- `danangtrip-crawler/data/tour-recrawl-parser-v3-20260606-raw.json`
- `danangtrip-crawler/data/tour-recrawl-parser-v3-staging-20260606.json`
- `danangtrip-crawler/data/tour-recrawl-parser-v3-enriched-20260606.json`
- `danangtrip-crawler/data/tour-recrawl-parser-v3-readiness-20260606.json`
- `danangtrip-crawler/data/tour-recrawl-parser-v3-readiness-20260606.csv`

## Verified real tour catalog - 2026-06-07

The VM Travel sitemap was scanned and deduplicated against collected source
URLs. Twenty-six new Central Vietnam detail pages were crawled. The price
parser was corrected to read `.table-price-tour` instead of the first price
found in the page header or navigation.

Additional quality controls:

- Block VM Travel pages whose price table has no direct numeric price.
- Block implausibly high prices for the parsed duration.
- Accept a single explicit exclusion when it fully describes the source rule.
- Accept two long itinerary sections when their combined content is complete.
- Match short destination tokens such as Hue, Hoi An, and DMZ in image review.
- Retry Pexels enrichment per tour without aborting the complete batch.

Final verified staging catalog:

- Total tours: 30
- Unique source URLs: 30
- Direct prices: 30
- Direct durations: 30
- Complete itineraries: 30
- Complete inclusions: 30
- Complete exclusions: 30
- At least two relevant images: 30
- Source-image tours: 28
- Source primary image plus visually reviewed Pexels candidates: 2
- Inferred core fields: 0
- Database writes: 0

The two manually reviewed Pexels groups represent:

- Ba Na Hills Golden Bridge.
- Cham Island snorkeling and coral.

Catalog outputs:

- `danangtrip-crawler/data/verified-real-tour-catalog-20260607.json`
- `danangtrip-crawler/data/verified-real-tour-catalog-20260607-report.json`
- `danangtrip-crawler/data/venus-tour-pexels-enriched-20260607-manifest.json`

This catalog is ready for final editorial review and media download/Cloudinary
mapping. It has not replaced the live synthetic tour rows.

## Media download and Cloudinary staging - 2026-06-07

Downloaded up to three full-resolution images for each verified tour.

Result:

- Tours: 30
- Requested image slots: 90
- Downloaded files: 89
- Downloaded size: 68,012,203 bytes
- Tours with at least two local images: 30
- Tours with all three requested images: 29
- Failed source image: 1
- Unique SHA-256 checksums: 78
- Duplicate-content mappings: 11
- Upload-ready unique assets: 78
- Cloudinary uploads performed: 0
- Database writes performed: 0

The failed image belongs to the Da Nang-Hue heritage train tour. That tour
still has two successfully downloaded images and remains media-complete under
the minimum quality rule.

Duplicate files are retained in the full audit manifest but excluded from the
Cloudinary upload manifest. `tour-media-map.json` resolves duplicate image
slots to the canonical Cloudinary public ID.

Staging directory:

- `data-center/media-assets/cloudinary-staging/tours/2026-06-07-verified-real-tours/`

Important files:

- `manifest.json`: complete 90-slot audit manifest.
- `manifest.csv`: spreadsheet version of the audit manifest.
- `upload-manifest.json`: 78 unique local assets ready to upload.
- `upload-manifest.csv`: input for `upload_cloudinary_assets.py`.
- `tour-media-map.json`: tour-to-canonical-Cloudinary mapping.
- `summary.json`: download and deduplication totals.

## Cloudinary upload completed - 2026-06-07

Uploaded the deduplicated media set to the configured Cloudinary account.

Result:

- Unique assets uploaded: 78/78
- Initial upload: 75 succeeded, 3 failed due to an overlong public ID
- Retry after shortening the affected Ba Na Hills path: 3/3 succeeded
- Image slots resolved through canonical assets: 89
- Unmapped slots: 1 source image that never downloaded
- Tours with Cloudinary media: 30/30
- Tours with at least two Cloudinary images: 30/30
- Tours with all three requested Cloudinary images: 29/30
- HTTP validation: 78/78 unique secure URLs returned an image response
- Database writes: 0

Final outputs:

- `danangtrip-crawler/data/verified-real-tour-catalog-cloudinary-20260607.json`
- `data-center/media-assets/cloudinary-staging/tours/2026-06-07-verified-real-tours/cloudinary-tour-media-map.json`
- `data-center/media-assets/cloudinary-staging/tours/2026-06-07-verified-real-tours/cloudinary-summary.json`
- `data-center/media-assets/cloudinary-staging/tours/2026-06-07-verified-real-tours/upload-results.json`
- `data-center/media-assets/cloudinary-staging/tours/2026-06-07-verified-real-tours/upload-retry-results.json`

The Cloudinary-backed catalog is ready for editorial title/summary cleanup and
database replacement seed generation. No live database rows have been changed.
