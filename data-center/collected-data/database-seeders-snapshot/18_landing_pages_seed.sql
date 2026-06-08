-- DanangTrip Seed: Landing Pages
-- FILE: 18_landing_pages_seed.sql
-- Purpose: Seed text/config-only SEO landing pages.
-- Notes:
--   - No image creation.
--   - hero_image and og_image are kept NULL.
--   - content_blocks stores FAQ, CTA and body copy as structured JSON.

INSERT INTO landing_pages (
  slug,
  title,
  page_type,
  intro,
  hero_image,
  seo_title,
  seo_description,
  og_image,
  filters,
  content_blocks,
  status,
  created_at,
  updated_at
) VALUES
(
  'du-lich-da-nang',
  'Du lich Da Nang',
  'destination',
  'Tong hop tour, dia diem, bai viet va goi y lich trinh cho khach muon kham pha Da Nang.',
  NULL,
  'Du lich Da Nang - Tour, dia diem va kinh nghiem moi nhat',
  'Kham pha Da Nang voi goi y tour Ba Na Hills, Son Tra, Ngu Hanh Son, bien My Khe, am thuc va lich trinh phu hop.',
  NULL,
  '{"destination":"da-nang","tour_category_slugs":["tour-da-nang","tour-ba-na","tour-son-tra"],"sort":"featured"}'::jsonb,
  '{
    "sections": [
      {
        "type": "intro",
        "title": "Da Nang danh cho moi kieu du khach",
        "body": "Da Nang ket hop bien, nui, cau bieu tuong, am thuc dia phuong va cac diem den gan Hoi An, Hue. Trang landing nay gom noi dung de dieu huong den tour, dia diem noi bat va bai viet huong dan."
      },
      {
        "type": "highlights",
        "title": "Diem noi bat",
        "items": ["Bien My Khe", "Cau Rong", "Ban dao Son Tra", "Ngu Hanh Son", "Ba Na Hills", "Am thuc dia phuong"]
      },
      {
        "type": "faq",
        "items": [
          {"question": "Nen di Da Nang may ngay?", "answer": "Lich trinh 3 den 4 ngay phu hop de xem bien, Son Tra, Ngu Hanh Son va mot tour Ba Na Hills."},
          {"question": "Thoi diem nao phu hop?", "answer": "Mua kho tu khoang thang 3 den thang 8 phu hop cho tam bien va lich trinh ngoai troi."},
          {"question": "Co the ket hop Hoi An va Hue khong?", "answer": "Co. Da Nang la diem trung chuyen tot de di Hoi An trong ngay hoac Hue qua deo Hai Van."}
        ]
      }
    ],
    "cta": {"label": "Xem tour Da Nang", "href": "/tours?destination=da-nang"},
    "source_notes": ["Internal travel content seed", "No image generation"]
  }'::jsonb,
  'published',
  NOW(),
  NOW()
),
(
  'tour-ba-na-hills',
  'Tour Ba Na Hills va Cau Vang',
  'tour_line',
  'Landing gom cac tour va kinh nghiem can biet khi tham quan Ba Na Hills, Cau Vang va khu vui choi tren nui.',
  NULL,
  'Tour Ba Na Hills - Cau Vang, cap treo va lich trinh trong ngay',
  'Dat tour Ba Na Hills tu Da Nang, xem kinh nghiem di cap treo, Cau Vang, lang Phap, Fantasy Park va cac luu y theo mua.',
  NULL,
  '{"tour_category_slugs":["tour-ba-na"],"keywords":["ba na hills","cau vang","cap treo"],"sort":"popular"}'::jsonb,
  '{
    "sections": [
      {
        "type": "intro",
        "title": "Mot ngay tren nui Ba Na",
        "body": "Ba Na Hills phu hop cho du khach muon trai nghiem cap treo, Cau Vang, khu vui choi va khong gian khi hau mat hon trung tam Da Nang."
      },
      {
        "type": "checklist",
        "title": "Nen chuan bi",
        "items": ["Ao khoac mong", "Giay di bo", "Ve cap treo", "Lich trinh den som de tranh dong"]
      },
      {
        "type": "faq",
        "items": [
          {"question": "Tour Ba Na Hills mat bao lau?", "answer": "Thong thuong la tour tron ngay tu sang den chieu."},
          {"question": "Co phu hop gia dinh khong?", "answer": "Co. Khu vui choi va cac diem check-in phu hop nhieu nhom tuoi."}
        ]
      }
    ],
    "cta": {"label": "Xem tour Ba Na", "href": "/tours?category=tour-ba-na"},
    "source_notes": ["Internal travel content seed", "No image generation"]
  }'::jsonb,
  'published',
  NOW(),
  NOW()
),
(
  'tour-son-tra-ngu-hanh-son',
  'Tour Son Tra va Ngu Hanh Son',
  'tour_line',
  'Goi y cac hanh trinh tham quan chua Linh Ung, ban dao Son Tra, Ngu Hanh Son va cac diem ven bien.',
  NULL,
  'Tour Son Tra Ngu Hanh Son - Lich trinh nua ngay va mot ngay',
  'Kham pha Son Tra, chua Linh Ung, Ngu Hanh Son, lang da Non Nuoc va cac diem ngam canh gan bien.',
  NULL,
  '{"tour_category_slugs":["tour-son-tra","tour-ngu-hanh-son"],"keywords":["son tra","ngu hanh son","linh ung"],"sort":"featured"}'::jsonb,
  '{
    "sections": [
      {
        "type": "intro",
        "title": "Lich trinh gan trung tam",
        "body": "Son Tra va Ngu Hanh Son la hai cum diem den gan trung tam Da Nang, phu hop voi lich trinh nua ngay hoac mot ngay."
      },
      {
        "type": "highlights",
        "title": "Diem nen co",
        "items": ["Chua Linh Ung Bai But", "Ban dao Son Tra", "Dong Huyen Khong", "Lang da Non Nuoc"]
      },
      {
        "type": "faq",
        "items": [
          {"question": "Co nen di buoi sang khong?", "answer": "Nen di sang som de tranh nang va co anh sang dep khi ngam bien."},
          {"question": "Lich trinh co can leo bac khong?", "answer": "Ngu Hanh Son co nhieu bac va hang dong, nen chuan bi giay de di bo."}
        ]
      }
    ],
    "cta": {"label": "Xem tour Son Tra", "href": "/tours?keyword=son-tra"},
    "source_notes": ["Internal travel content seed", "No image generation"]
  }'::jsonb,
  'published',
  NOW(),
  NOW()
),
(
  'khuyen-mai-tour-da-nang',
  'Khuyen mai tour Da Nang',
  'promotion',
  'Tong hop cac uu dai dang ap dung cho tour Da Nang va mien Trung.',
  NULL,
  'Khuyen mai tour Da Nang - Ma giam gia va uu dai moi',
  'Cap nhat cac chuong trinh khuyen mai tour Da Nang, Ba Na Hills, Son Tra, Ngu Hanh Son va tour gia dinh.',
  NULL,
  '{"promotion_codes":["DANANG10","CENTRAL15","FAMILY200K","BANAHILLS300K"],"sort":"newest"}'::jsonb,
  '{
    "sections": [
      {
        "type": "intro",
        "title": "Uu dai dang ap dung",
        "body": "Trang nay dung de dieu huong nguoi dung den cac tour co khuyen mai va ho tro admin test landing page loai promotion."
      },
      {
        "type": "promotion_codes",
        "items": ["DANANG10", "CENTRAL15", "FAMILY200K", "BANAHILLS300K"]
      },
      {
        "type": "faq",
        "items": [
          {"question": "Ma giam gia co ap dung dong thoi khong?", "answer": "Mac dinh moi booking chi nen ap dung mot ma giam gia."},
          {"question": "Ma het han co hien thi khong?", "answer": "Chi nen hien thi ma active trong giao dien public."}
        ]
      }
    ],
    "cta": {"label": "Xem uu dai", "href": "/promotions"},
    "source_notes": ["Internal promotion content seed", "No image generation"]
  }'::jsonb,
  'published',
  NOW(),
  NOW()
),
(
  'cam-nang-du-lich-mien-trung',
  'Cam nang du lich mien Trung',
  'destination',
  'Noi dung tong quan cho khach muon ket hop Da Nang, Hoi An va Hue trong mot lich trinh.',
  NULL,
  'Cam nang du lich mien Trung - Da Nang, Hoi An, Hue',
  'Goi y lich trinh mien Trung, cach di chuyen, thoi diem phu hop va cac trai nghiem noi bat.',
  NULL,
  '{"destination":"central-vietnam","keywords":["da nang","hoi an","hue"],"sort":"recommended"}'::jsonb,
  '{
    "sections": [
      {
        "type": "intro",
        "title": "Ba diem den trong mot hanh trinh",
        "body": "Da Nang phu hop lam diem dung chinh de ket hop bien, Hoi An co khong gian pho co va Hue noi bat ve lich su."
      },
      {
        "type": "itinerary",
        "title": "Goi y lich trinh",
        "items": ["Ngay 1: Da Nang va bien My Khe", "Ngay 2: Son Tra va Ngu Hanh Son", "Ngay 3: Hoi An", "Ngay 4: Hue hoac Ba Na Hills"]
      },
      {
        "type": "faq",
        "items": [
          {"question": "Nen o dau de tien di chuyen?", "answer": "Da Nang la diem trung tam, thuan tien ra san bay va di Hoi An/Hue."},
          {"question": "Co can dat tour tron goi khong?", "answer": "Neu di gia dinh hoac lan dau den mien Trung, tour tron goi giup tiet kiem thoi gian."}
        ]
      }
    ],
    "cta": {"label": "Xem goi y tour", "href": "/tours"},
    "source_notes": ["Internal travel content seed", "No image generation"]
  }'::jsonb,
  'draft',
  NOW(),
  NOW()
)
ON CONFLICT (slug) DO UPDATE SET
  title = EXCLUDED.title,
  page_type = EXCLUDED.page_type,
  intro = EXCLUDED.intro,
  hero_image = EXCLUDED.hero_image,
  seo_title = EXCLUDED.seo_title,
  seo_description = EXCLUDED.seo_description,
  og_image = EXCLUDED.og_image,
  filters = EXCLUDED.filters,
  content_blocks = EXCLUDED.content_blocks,
  status = EXCLUDED.status,
  updated_at = NOW();
