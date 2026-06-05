# Cloudinary Upload Prep - 2026-06-04

## Current Local Asset Batch

Batch:

`2026-06-04-overpass-published-inactive`

Folder:

`D:\DATN\DATN_Tài liệu\data-center\media-assets\cloudinary-staging\locations\2026-06-04-overpass-published-inactive`

Files:

- Downloaded images: 222.
- Total size: about 85.6 MB.
- Source provider: Pexels image candidates from local crawler enrichment.
- Target DB records: `locations.status = inactive` published from Overpass crawl.

Important files:

- `originals\`: downloaded images.
- `manifest.csv`: review/upload spreadsheet.
- `manifest.json`: machine-readable upload plan.
- `summary.json`: download result summary.

## Naming Convention

Local file:

`loc-{location_id}__{location_slug}__{external_id}__p01__pexels-{photo_id}.jpg`

Cloudinary public ID:

`danangtrip/locations/{location_slug}/loc-{location_id}__{location_slug}__p01`

This means each image can always map back to:

- `locations.id`
- `locations.slug`
- `crawl_items.external_id`
- Pexels source photo ID

## Required Review Before Upload

Open:

`D:\DATN\DATN_Tài liệu\data-center\media-assets\cloudinary-staging\locations\2026-06-04-overpass-published-inactive\manifest.csv`

Review columns:

- `location_id`
- `location_slug`
- `location_name`
- `category_slug`
- `provider_page_url`
- `photographer`
- `local_file`
- `cloudinary_public_id`
- `status`

Add a manual column if needed:

- `approved_for_upload`
- `review_note`

Only upload rows approved by admin/editor.

## Upload Strategy

Recommended Cloudinary folder/public ID:

`danangtrip/locations/{location_slug}/loc-{location_id}__{location_slug}__p01`

Recommended metadata/context:

- `location_id`
- `location_slug`
- `external_id`
- `provider=pexels`
- `photo_id`
- `photographer`
- `provider_page_url`

## After Upload

After Cloudinary upload, create a result CSV with:

- `location_id`
- `location_slug`
- `local_file`
- `cloudinary_public_id`
- `secure_url`
- `asset_id`
- `version`
- `width`
- `height`
- `format`

Then generate a SQL update seed that:

- updates `locations.thumbnail` with the first approved `secure_url`.
- updates `locations.images` with approved image URLs.
- keeps `locations.status = inactive` until admin explicitly activates.

Do not update DB directly without a reviewed upload result manifest.

## Scripts

Upload local files to Cloudinary:

```powershell
cd "D:\DATN\DATN_Tài liệu\danangtrip-crawler"
.venv\Scripts\python.exe scripts\upload_cloudinary_assets.py --limit 5
```

Full upload after test:

```powershell
cd "D:\DATN\DATN_Tài liệu\danangtrip-crawler"
.venv\Scripts\python.exe scripts\upload_cloudinary_assets.py
```

Generate SQL update seed from upload results:

```powershell
cd "D:\DATN\DATN_Tài liệu\danangtrip-crawler"
.venv\Scripts\python.exe scripts\generate_location_image_update_seed.py
```

Generated SQL:

`D:\DATN\DATN_Tài liệu\database-seeders\34_update_location_images_from_cloudinary_seed.sql`
