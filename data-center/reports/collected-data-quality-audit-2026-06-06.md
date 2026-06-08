# Collected Data Quality Audit - 2026-06-06

## Verdict

The collected database is sufficient for a graduation-project demo, but the public content dataset is not yet production-grade.

The strongest dataset is locations collected from OpenStreetMap/Overpass. Tours and blogs still contain substantial seed/template content and require replacement or editorial enrichment.

## Locations

### Passed

- Total: 333
- Active: 221
- Published crawl items linked to production entities: 222/222
- Missing names, addresses, districts, descriptions or coordinates: 0
- Missing or non-Cloudinary thumbnails: 0
- Empty image arrays: 0
- Invalid price ranges: 0
- Locations without tags or amenities: 0

### Needs review

- Active descriptions under 100 characters: 107
- Active short descriptions under 40 characters: 94
- Duplicate normalized name groups: 2
  - Memory Lounge: one active and one inactive duplicate
  - HanCook: three inactive branches with similar names but different addresses
- Shared coordinate groups: 7
  - Most are legitimate co-located events/attractions.
  - Starbucks Bach Dang and Novotel Han River should be manually verified.
- 13 locations are outside the narrow Da Nang bounding box.
  - These are mostly intentional regional destinations in Hoi An, Quang Nam and Hue.
  - They are not coordinate errors if DanangTrip supports Central Vietnam excursions.

## Tours

### Structural checks passed

- Total: 100
- Missing itinerary, inclusions, exclusions, images, duration, start time or meeting point: 0
- Missing schedules or location mappings: 0
- Invalid people range or zero adult price: 0

### Major quality problems

- Live tour IDs are 1-100; none of the separately crawled operator tours with IDs 101+ are present.
- Only 40 distinct names across 100 tours.
- Duplicate normalized name groups: 20.
- Duplicate description groups: 20.
- All 100 descriptions are under 150 characters.
- 80 short descriptions are under 40 characters.
- 80 prices contain random-looking fractional VND values.

Assessment: the live tour table is primarily a demo/variant seed, not a clean catalog of real operator tours.

## Blogs

### Structural checks passed

- Published: 104
- Missing excerpt, image or published timestamp: 0
- Images use Cloudinary.

### Major quality problems

- 101/104 published posts contain fewer than 500 content characters.
- Average published content length: about 280 characters.
- Published post 102 has only 8 characters: `chay quá`.
- Posts 103, 104 and 105 have identical 5,030-character content.
- Most short posts are teaser paragraphs ending with ellipses, not complete articles.

Assessment: the blog table is visually populated but is not a complete editorial dataset.

## Crawl staging

- Total: 942
- Published: 222
- Pending review: 258
- Rejected: 462
- Published rows without production entity links: 0
- Pending rows missing address: 0
- Pending rows missing coordinates: 0
- Pending rows missing image candidates: 258

The remaining pending rows should stay unpublished until images and manual verification are available.

## Priority

1. Replace or archive the 80 synthetic tour variants; import reviewed real operator tours with retained source URLs.
2. Rewrite or unpublish the 101 short blog posts, especially post 102.
3. Keep one of blog posts 103-105 and archive the two duplicated copies.
4. Enrich the 107 short active location descriptions from reliable sources.
5. Add provenance fields or a generic source-reference table for production tours, blogs and locations.
6. Manually verify the suspicious shared coordinates and the two duplicate-name groups.

## Audit scripts

- `database-seeders/audit_collected_data_quality.php`
- `database-seeders/audit_collected_data_details.php`
