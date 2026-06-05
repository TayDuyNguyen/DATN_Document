-- DanangTrip activate curated inactive locations batch 1
-- FILE: 37_activate_curated_inactive_locations_batch1.sql
-- Purpose: activate reviewed non-lodging inactive locations with complete Cloudinary media.

UPDATE locations
SET status = 'active',
    updated_at = NOW()
WHERE status = 'inactive'
  AND id IN (115, 116, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 138, 139, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 158, 159, 164, 165, 166, 167, 168, 169, 173, 174, 176, 180, 184, 186, 187, 190, 191, 199, 202, 204, 207, 209, 213, 214, 216, 219, 221, 223, 224, 225, 226, 227, 230, 231, 233, 234, 235, 269, 271, 272, 274, 275, 277, 278, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 291, 298, 304, 306, 309, 311, 312, 316, 317, 319, 320, 321, 322, 323, 324, 325, 326, 327, 329, 331, 332, 333, 334);
