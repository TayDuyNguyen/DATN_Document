# Media Asset Naming Standard - 2026-06-04

## Local Folder

Use:

`D:\DATN\DATN_Tài liệu\data-center\media-assets\cloudinary-staging\locations\2026-06-04-overpass-published-inactive`

Subfolders:

- `originals`: downloaded source images.
- `manifest.csv`: spreadsheet mapping every image to DB and source.
- `manifest.json`: machine-readable mapping.
- `summary.json`: download status summary.

## File Name Convention

Pattern:

`loc-{location_id}__{location_slug}__{external_id}__p{photo_index}__pexels-{photo_id}.jpg`

Example:

`loc-103__hue-imperial-city__osm-node-123__p01__pexels-14021725.jpg`

Meaning:

- `loc-{location_id}` maps directly to `locations.id`.
- `{location_slug}` maps to `locations.slug`.
- `{external_id}` maps to `crawl_items.external_id`.
- `p01`, `p02`, `p03` is the image order for that location.
- `pexels-{photo_id}` keeps provider traceability.

## Cloudinary Public ID Convention

Pattern:

`danangtrip/locations/{location_slug}/loc-{location_id}__{location_slug}__p{photo_index}`

Example:

`danangtrip/locations/hue-imperial-city/loc-103__hue-imperial-city__p01`

Do not include file extension in Cloudinary public ID.

## Required Manifest Columns

- `location_id`
- `location_slug`
- `location_name`
- `location_status`
- `category_slug`
- `external_id`
- `source_url`
- `provider`
- `photo_index`
- `photo_id`
- `image_url`
- `thumbnail_url`
- `provider_page_url`
- `photographer`
- `photographer_url`
- `local_file`
- `local_path`
- `cloudinary_public_id`
- `status`

## Review Rule

Do not upload all downloaded images blindly.

Before Cloudinary upload:

1. Open `manifest.csv`.
2. Review image relevance by location.
3. Remove or mark bad rows.
4. Upload only approved files.
5. Store returned Cloudinary secure URL back to DB only after approval.

