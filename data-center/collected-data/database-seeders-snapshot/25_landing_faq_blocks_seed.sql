-- DanangTrip landing FAQ blocks seed
-- FILE: 25_landing_faq_blocks_seed.sql
-- Source: danangtrip-crawler/data/landing-faq-staging.json
-- Policy: text-only FAQ blocks generated from source-backed guide staging; no images.
-- Run after 18_landing_pages_seed.sql.

BEGIN;

-- FAQ update for du-lich-da-nang
UPDATE landing_pages
SET content_blocks = '{"sections": [{"type": "faq", "title": "FAQ du lich Da Nang", "items": [{"question": "Nen di Da Nang may ngay?", "answer": "Lich trinh 3 ngay phu hop de ket hop bien My Khe, cau Rong, Ngu Hanh Son, Son Tra va mot diem xa hon nhu Ba Na Hills hoac Hoi An."}, {"question": "Di tu san bay Da Nang vao trung tam co mat nhieu thoi gian khong?", "answer": "San bay Da Nang gan trung tam, thuan tien di taxi, xe cong nghe hoac xe dua don. Nen du phong thoi gian neu di vao gio cao diem."}, {"question": "Da Nang phu hop voi nhom khach nao?", "answer": "Da Nang phu hop voi gia dinh, cap doi, khach di lan dau, nguoi thich bien, am thuc, lich trinh ngan ngay va ket hop Hoi An/Hue."}, {"question": "Nen uu tien diem nao neu chi co mot ngay?", "answer": "Nen chon My Khe, cau Rong, Ngu Hanh Son hoac Son Tra. Neu muon di xa hon, Ba Na Hills thuong can gan tron ngay."}]}], "source_notes": ["FAQ draft generated from source-backed guide staging.", "No image generation.", "Editor review required before public use."], "source_urls": ["https://vietnam.travel/places-to-go/central-vietnam/da-nang", "https://vietnam.travel/things-to-do/da-nang-itinerary", "https://vietnam.travel/things-to-do/must-visit-places-in-da-nang", "https://vietnam.travel/things-to-do/must-do-da-nang-an-insider-list", "https://vietnam.travel/node/887"]}'::json,
    updated_at = NOW()
WHERE slug = 'du-lich-da-nang';

-- FAQ update for cam-nang-du-lich-mien-trung
UPDATE landing_pages
SET content_blocks = '{"sections": [{"type": "faq", "title": "FAQ du lich mien Trung", "items": [{"question": "Co nen ket hop Da Nang, Hoi An va Hue trong mot chuyen di?", "answer": "Co. Da Nang nam giua, co san bay va ket noi tot den Hoi An, Hue, Ba Na Hills, Ngu Hanh Son va My Son."}, {"question": "Nen di Hoi An hay Hue tu Da Nang bang cach nao?", "answer": "Hoi An phu hop di xe rieng, shuttle hoac xe cong nghe. Hue co the di xe rieng, tau hoa hoac hanh trinh qua deo Hai Van."}, {"question": "Di mien Trung can luu y gi ve thoi tiet?", "answer": "Nen kiem tra mua mua va lich trinh ngoai troi. Cac diem bien, deo va nui nen di khi thoi tiet on dinh de an toan hon."}, {"question": "Co nen thue xe may tu Hoi An di Hue qua Hai Van khong?", "answer": "Chi nen di neu co kinh nghiem lai xe duong deo va kiem tra thoi tiet. Khach di lan dau nen chon xe rieng, tour hoac tau hoa."}]}], "source_notes": ["FAQ draft generated from source-backed guide staging.", "No image generation.", "Editor review required before public use."], "source_urls": ["https://vietnam.travel/plan-your-trip", "https://vietnam.travel/plan-your-trip/transport-within-vietnam", "https://vietnam.travel/node/705", "https://vietnam.travel/places-to-go/central-vietnam/hoi-an", "https://vietnam.travel/places-to-go/central-vietnam/hue"]}'::json,
    updated_at = NOW()
WHERE slug = 'cam-nang-du-lich-mien-trung';

-- FAQ update for tour-ba-na-hills
UPDATE landing_pages
SET content_blocks = '{"sections": [{"type": "faq", "title": "FAQ tour Ba Na Hills", "items": [{"question": "Tour Ba Na Hills nen di nua ngay hay tron ngay?", "answer": "Nen di tron ngay vi khu Ba Na Hills co cap treo, Cau Vang, lang Phap, khu vui choi va nhieu diem check-in."}, {"question": "Can chuan bi gi khi di Ba Na Hills?", "answer": "Nen mang giay di bo, ao khoac mong, nuoc uong, kem chong nang va den som de co thoi gian di cap treo, Cau Vang va Fantasy Park."}, {"question": "Ba Na Hills co phu hop gia dinh khong?", "answer": "Co. Khu nay phu hop gia dinh, cap doi va nhom ban, nhung can luu y viec di bo nhieu va thoi tiet tren nui co the thay doi nhanh."}]}], "source_notes": ["FAQ draft generated from source-backed guide staging.", "No image generation.", "Editor review required before public use."], "source_urls": ["https://vietnam.travel/things-to-do/explore-ba-na-hills", "https://danangfantasticity.com/hai-van-pass", "https://vietnam.travel/things-to-do/da-nang-itinerary"]}'::json,
    updated_at = NOW()
WHERE slug = 'tour-ba-na-hills';

-- FAQ update for tour-son-tra-ngu-hanh-son
UPDATE landing_pages
SET content_blocks = '{"sections": [{"type": "faq", "title": "FAQ tour Son Tra va Ngu Hanh Son", "items": [{"question": "Son Tra va Ngu Hanh Son co the di trong nua ngay khong?", "answer": "Co the di nua ngay neu chi chon cac diem chinh. Neu muon tham quan ky hang dong, chua va diem ngam canh, nen danh nhieu thoi gian hon."}, {"question": "Ngu Hanh Son co can leo nhieu khong?", "answer": "Co nhieu bac da va loi di trong hang dong, nen mang giay de di bo va han che lich trinh qua day neu di voi nguoi kho van dong."}, {"question": "Nen di Son Tra vao thoi diem nao?", "answer": "Nen di sang som hoac chieu muon de tranh nang, co anh sang dep va de ngam bien/thanh pho tot hon."}]}], "source_notes": ["FAQ draft generated from source-backed guide staging.", "No image generation.", "Editor review required before public use."], "source_urls": ["https://vietnam.travel/things-to-do/around-marble-mountains", "https://danangfantasticity.com/the-son-tra-peninsula", "https://vietnam.travel/things-to-do/must-do-da-nang-an-insider-list"]}'::json,
    updated_at = NOW()
WHERE slug = 'tour-son-tra-ngu-hanh-son';

COMMIT;
