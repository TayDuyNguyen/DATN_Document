-- DanangTrip Real Data Seeder: Tours, Pivots & Schedules (100 real tours)
-- FILE: 06_tours.sql

-- 1. TOURS (Target 100)
INSERT INTO tours (id, name, slug, tour_category_id, description, short_desc, itinerary, inclusions, exclusions, price_adult, price_child, price_infant, discount_percent, duration, start_time, meeting_point, max_people, min_people, status, is_featured, is_hot, created_at, updated_at) VALUES
(1, 'Tour Ba Na Hills 1 Ngay (Buffet Trua)', 'tour-ba-na-hills-1-ngay', 1, 'Kham pha chon bong lai tien canh voi Cau Vang, Lang Phap va he thong cap treo dat nhieu ky luc the gioi.', 'Hanh trinh dua quy khach den voi dinh Nui Chua - Da Nang.', '[{"time": "08:00", "task": "Don khach tai trung tam Da Nang"}, {"time": "09:30", "task": "Check-in Cau Vang"}, {"time": "12:00", "task": "An trua Buffet"}, {"time": "15:30", "task": "Roi Ba Na"}]', '["Xe dua don doi moi", "Huong dan vien", "Ve cap treo", "Buffet trua 100 mon"]', '["Nuoc uong trong bua an", "Chi phi ca nhan", "Tip cho HDV"]', 1250000, 950000, 250000, 5, '1 ngay', '08:00', 'Van phong Da Nang / Khach san trung tam', 45, 2, 'active', true, true, NOW(), NOW()),
(2, 'Tour Pho Co Hoi An & Rung Dua Bay Mau', 'tour-hoi-an-rung-dua', 2, 'Trai nghiem cheo thung tai rung dua Bay Mau va kham pha ve dep hoai co cua pho co Hoi An ve dem.', 'Ket hop trai nghiem song nuoc va van hoa pho co.', '[{"time": "14:00", "task": "Don khach"}, {"time": "15:00", "task": "Tham quan Rung dua"}, {"time": "17:30", "task": "Dao pho co Hoi An"}, {"time": "21:00", "task": "Tro ve Da Nang"}]', '["Xe dua don", "Ve tham quan", "Cheo thung", "An toi dac san Hoi An"]', '["Do uong", "O khoa tinh yeu"]', 750000, 550000, 150000, 0, '7 gio', '14:00', 'Da Nang / Hoi An', 30, 2, 'active', true, false, NOW(), NOW()),
(3, 'Tour Ngu Hanh Son & Chua Linh Ung Son Tra', 'tour-ngu-hanh-son-son-tra', 5, 'Hanh trinh tam linh kham pha cac hang dong ky bi tai Ngu Hanh Son va chiem bai Phat Ba tai Son Tra.', 'Tour tam linh nua ngay ngam canh bien Da Nang.', '[{"time": "08:00", "task": "Tham quan Chua Linh Ung"}, {"time": "10:00", "task": "Kham pha Ngu Hanh Son"}, {"time": "12:00", "task": "Ket thuc tour"}]', '["Xe du lich", "HDV nhiet tinh", "Nuoc suoi", "Ve tham quan"]', '["An trua", "Chi phi ca nhan"]', 450000, 250000, 0, 0, '4 gio', '08:00', 'Da Nang', 20, 2, 'active', false, false, NOW(), NOW()),
(4, 'Tour Cu Lao Cham Lan Ngam San Ho', 'tour-cu-lao-cham', 3, 'Chuyen di bien dao hap dan voi cac hoat dong tam bien, lan ngam san ho va thuong thuc hai san tuoi ngon.', 'Thien duong bien dao Cu Lao Cham.', '[{"time": "08:30", "task": "Cano cao toc di dao"}, {"time": "10:00", "task": "Lan ngam san ho"}, {"time": "12:00", "task": "An trua hai san"}, {"time": "14:30", "task": "Ve lai dat lien"}]', '["Cano cao toc", "Kinh lan", "An trua", "Bao hiem du lich"]', '["Lan binh khi", "Phi moi truong quoc te"]', 650000, 450000, 100000, 10, '1 ngay', '08:00', 'Cang Cua Dai', 35, 4, 'active', true, true, NOW(), NOW()),
(5, 'Tour Co Do Hue 1 Ngay tu Da Nang', 'tour-hue-1-ngay', 5, 'Vuot deo Hai Van den voi co do Hue, tham quan Dai Noi, chua Thien Mu va cac lang tam uy nghiem.', 'Hanh trinh di san co do mien Trung.', '[{"time": "07:30", "task": "Khoi hanh qua ham Hai Van"}, {"time": "10:30", "task": "Tham quan Dai Noi"}, {"time": "12:00", "task": "An trua dac san Hue"}, {"time": "15:00", "task": "Tham quan Lang Khai Dinh"}]', '["Xe dua don", "HDV", "Ve tham quan cac diem", "An trua"]', '["Chi phi ca nhan"]', 1050000, 750000, 200000, 0, '1 ngay', '07:30', 'Da Nang', 40, 2, 'active', true, false, NOW(), NOW()),
(6, 'Tour Thanh Dia My Son nua ngay', 'tour-my-son', 5, 'Tim hieu ve van hoa Champa co dai qua quan the den thap My Son - Di san van hoa the gioi.', 'Kham pha bi an thap Cham.', '[{"time": "08:00", "task": "Khoi hanh"}, {"time": "09:30", "task": "Tham quan My Son"}, {"time": "11:00", "task": "Xem mua Apsara"}, {"time": "13:00", "task": "Ve lai Hoi An"}]', '["Xe van chuyen", "HDV", "Ve tham quan", "Xem bieu dien van nghe"]', '["An trua", "Tip"]', 550000, 400000, 100000, 0, '5 gio', '08:00', 'Da Nang / Hoi An', 25, 2, 'active', false, false, NOW(), NOW()),
(7, 'Tour Da Nang City - Nhung Cay Cau', 'tour-city-danang', 1, 'Hanh trinh check-in nhung bieu tuong hien dai cua Da Nang: Cau Rong, Cau Tinh Yeu, Bao tang Cham.', 'Tour kham pha thanh pho dang song.', '[{"time": "08:00", "task": "Bao tang Cham"}, {"time": "10:00", "task": "Cau Rong & Cau Tinh Yeu"}, {"time": "11:30", "task": "Cho Han"}]', '["Xe du lich", "HDV", "Ve bao tang", "Nuoc uong"]', '["An trua"]', 350000, 200000, 0, 0, '4 gio', '08:30', 'Da Nang', 15, 2, 'active', false, false, NOW(), NOW()),
(8, 'Tour Deo Hai Van & Lang Co - O to', 'tour-hai-van-lang-co', 3, 'Trai nghiem cung duong deo dep nhat Viet Nam va thu gian tai vinh bien Lang Co tho mong.', 'Ngam nhin "Thien ha de nhat hung quan".', '[]', '["Xe du lich", "HDV", "An trua hai san"]', '["Dich vu bien"]', 850000, 600000, 150000, 0, '1 ngay', '08:00', 'Da Nang', 20, 2, 'active', false, false, NOW(), NOW()),
(9, 'Tour Dem Pho Co Hoi An & An Toi', 'tour-dem-hoi-an', 6, 'Dao buoc pho den long, tha den hoa dang va thuong thuc cac mon an dac san noi tieng cua Hoi An.', 'Lang man pho co ve dem.', '[]', '["Xe dua don", "An toi", "Tha hoa dang"]', '["Mua sam ca nhan"]', 600000, 450000, 100000, 0, '5 gio', '16:00', 'Da Nang', 25, 2, 'active', false, true, NOW(), NOW()),
(10, 'Tour Ba Na Hills Dem (Sun World Night)', 'tour-ba-na-night', 1, 'Trai nghiem Ba Na Hills lung linh ve dem voi Buffet toi, ruou vang va cac show dien dac sac.', 'Ba Na huyen ao buoi dem.', '[]', '["Cap treo khu hoi", "An toi Buffet", "Ruou vang/Bia"]', '["Cac tro choi co phi"]', 950000, 750000, 200000, 0, '1 ngay', '15:30', 'Cap treo Ba Na', 50, 1, 'active', false, true, NOW(), NOW()),
(11, 'Tour VinWonders Nam Hoi An Full Day', 'tour-vinwonders-nam-hoi-an', 1, 'Vui choi khong gioi han tai VinWonders Nam Hoi An voi Safari, Cong vien nuoc va Dao van hoa.', 'The gioi giai tri da sac mau.', '[]', '["Xe bus don tien", "Ve vao cong", "An trua set menu"]', '["Mua sam", "Chi phi khac"]', 900000, 700000, 150000, 0, '1 ngay', '09:00', 'Da Nang / Hoi An', 50, 1, 'active', false, false, NOW(), NOW()),
(12, 'Tour Suoi Khoang Nong Than Tai Relax', 'tour-nui-than-tai', 4, 'Thu gian tuyet doi voi dich vu tam khoang, tam bun va khu vui choi nuoc giua nui rung.', 'Nghi duong va cham soc suc khoe.', '[]', '["Xe dua don", "Ve cong", "Buffet trua"]', '["Tam bun/Tam sa", "Phong nghi"]', 850000, 650000, 150000, 0, '1 ngay', '08:30', 'Da Nang', 30, 2, 'active', false, false, NOW(), NOW()),
(13, 'Tour Trekking Ban Dao Son Tra', 'tour-trekking-son-tra', 7, 'Tham hiem rung gia Son Tra, tim kiem vooc cha va chan nau va chinh phuc dinh Ban Co.', 'Thu thach thien nhien Son Tra.', '[]', '["HDV tham hiem", "Gay trekking", "An nhe", "Nuoc suoi"]', '["Van chuyen"]', 700000, 700000, 0, 0, '6 gio', '06:00', 'Son Tra', 10, 2, 'active', false, false, NOW(), NOW()),
(14, 'Tour Kham Pha Bach Ma National Park', 'tour-bach-ma', 7, 'Trekking rung quoc gia Bach Ma, ngam thac Do Quyen va ngam toan canh vinh Lang Co tu Hai Vong Dai.', 'Hanh trinh chinh phuc dinh Bach Ma.', '[]', '["Xe dua don", "HDV chuyen tuyen", "An trua picnic", "Ve cong"]', '["Dung cu ca nhan"]', 1100000, 850000, 200000, 0, '1 ngay', '07:30', 'Da Nang / Hue', 15, 2, 'active', false, false, NOW(), NOW()),
(15, 'Street Food Tour Da Nang bang Xe May', 'tour-street-food-danang', 6, 'Ngoi sau xe may cung HDV dia phuong len loi vao cac ngo ngach thuong thuc 5-7 mon an dac san.', 'Kham pha am thuc Da Nang nhu nguoi ban dia.', '[]', '["Xe may & Xang", "Tat ca do an thuc uong", "HDV dia phuong"]', '["Tip"]', 650000, 650000, 0, 0, '4 gio', '18:00', 'Khach san trung tam', 10, 1, 'active', false, true, NOW(), NOW()),
(16, 'Tour Lam Nong Dan Lang Rau Tra Que', 'tour-tra-que-farmer', 5, 'Hoc cach xoi dat, trong rau, tuoi nuoc va tu tay che bien mon an tu rau sach Tra Que.', 'Mot ngay lam nong dan Hoi An.', '[]', '["Phi tham quan", "HDV nong dan", "An trua gia dinh"]', '["Dua don"]', 500000, 350000, 100000, 0, '4 gio', '08:30', 'Lang Tra Que', 12, 1, 'active', false, false, NOW(), NOW()),
(17, 'Tour Du Thuyen Song Han & Xem Rong Phun Lua', 'tour-du-thuyen-song-han', 1, 'Ngam nhin thanh pho anh sang tu giua long song va xem Cau Rong phun lua, phun nuoc vao toi cuoi tuan.', 'Buoi toi lang man tren song Han.', '[]', '["Ve du thuyen", "Nuoc uong", "Bao hiem"]', '["An toi tren thuyen"]', 200000, 150000, 50000, 0, '2 gio', '19:30', 'Ben tau Bach Dang', 80, 1, 'active', false, false, NOW(), NOW()),
(18, 'Tour Dam Pha Tam Giang & Sunset', 'tour-tam-giang-sunset', 3, 'Kham pha he sinh thai dam pha nuoc lo, cheo thuyen Kayak va ngam hoang hon tuyet dep.', 'Hoang hon ruc ro tren pha Tam Giang.', '[]', '["Xe dua don", "Thuyen tham quan", "An toi hai san"]', '["Chi phi khac"]', 750000, 550000, 150000, 0, '6 gio', '14:30', 'Hue', 20, 2, 'active', false, false, NOW(), NOW()),
(19, 'Tour Ca Hue Tren Song Huong & Ngam Thanh Pho', 'tour-ca-hue-song-huong', 5, 'Thuong thuc loai hinh nghe thuat di san phi vat the va tha den hoa dang cau may tren song Huong.', 'Van hoa co do dac sac.', '[]', '["Thuyen rong", "Nghe nhan bieu dien", "Hoa dang"]', '["An toi"]', 150000, 100000, 0, 0, '2 gio', '19:00', 'Ben Toa Kham', 30, 1, 'active', false, false, NOW(), NOW()),
(20, 'Tour Snorkeling Ban Dao Son Tra', 'tour-snorkeling-son-tra', 7, 'Di tau go ra cac hon dao nho quanh ban dao Son Tra de lan ngam san ho va cau ca.', 'Kham pha dai duong Son Tra.', '[]', '["Tau go du lich", "Thiet bi lan", "An trua tren tau"]', '["Dich vu tam nuoc ngot"]', 600000, 450000, 100000, 0, '6 gio', '08:30', 'Cang Tien Sa', 25, 4, 'active', false, false, NOW(), NOW());

-- Generate more tours 21-100 (Variations of above with different durations/options)
INSERT INTO tours (id, name, slug, tour_category_id, description, short_desc, price_adult, price_child, price_infant, duration, max_people, min_people, status, created_at, updated_at)
SELECT 
    i, 
    'Tour ' || (CASE WHEN i % 5 = 0 THEN 'Cao Cap ' WHEN i % 5 = 1 THEN 'Tiet Kiem ' ELSE 'Kham Pha ' END) || t.name,
    'tour-real-variant-' || i,
    t.tour_category_id,
    'Trai nghiem ' || (CASE WHEN i % 5 = 0 THEN 'sang trong ' ELSE 'chuyen sau ' END) || 'hon cua ' || t.description,
    t.short_desc,
    t.price_adult * (1 + (random() * 0.2)),
    t.price_child * (1 + (random() * 0.1)),
    t.price_infant,
    t.duration,
    t.max_people,
    t.min_people,
    'active',
    NOW(),
    NOW()
FROM generate_series(21, 100) AS i
JOIN tours t ON t.id = (i % 20) + 1;

-- 2. TOUR_SCHEDULES (Target ~200)
INSERT INTO tour_schedules (id, tour_id, start_date, end_date, max_people, booked_people, price_adult, price_child, status, created_at, updated_at)
SELECT 
    i, 
    (i % 100) + 1, 
    CURRENT_DATE + (i / 100 * 7) + (i % 7) + 1, -- Avoid today
    CURRENT_DATE + (i / 100 * 7) + (i % 7) + 1, 
    20, 
    (random() * 5)::int, 
    NULL, 
    NULL, 
    'available', 
    NOW(), 
    NOW()
FROM generate_series(1, 300) AS i;

-- 3. TOUR_LOCATIONS (Pivots)
INSERT INTO tour_locations (tour_id, location_id, created_at) VALUES
(1, 23, NOW()), (1, 31, NOW()), -- Ba Na Hills, APEC Park
(2, 1, NOW()), (2, 3, NOW()), -- Ancient Town, Coconut Forest
(3, 21, NOW()), (3, 20, NOW()), -- Marble Mt, Linh Ung
(4, 13, NOW()), -- Cu Lao Cham
(7, 14, NOW()), (7, 15, NOW()), (7, 16, NOW()), -- Bridges
(12, 22, NOW()); -- Than Tai
-- Randomly link others
INSERT INTO tour_locations (tour_id, location_id, created_at)
SELECT 
    t.id, 
    (random() * 99 + 1)::int, 
    NOW()
FROM tours t
CROSS JOIN generate_series(1, 2)
WHERE t.id > 20
ON CONFLICT DO NOTHING;

