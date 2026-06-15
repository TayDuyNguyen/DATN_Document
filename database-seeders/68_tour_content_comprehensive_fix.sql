-- ============================================================
-- DanangTrip Tour Content Comprehensive Fix
-- FILE: 68_tour_content_comprehensive_fix.sql
-- Purpose:
--   1. Rewrite descriptions & itineraries for tours 1-20 with full
--      Vietnamese diacritics and rich long-form content for chatbot search.
--   2. Fix start_time / duration consistency across all base tours.
--   3. Patch missing itinerary/inclusions/exclusions for tours 21-100.
--   4. Fix price_child = 0 / price_infant = 0 on verified real tours (file 49).
--   5. Set start_time on verified real tours (currently NULL).
--   6. Expand short_desc to richer copy for all active tours.
-- ============================================================

BEGIN;

-- ============================================================
-- SECTION 1: Core base tours 1-20
--   Full rewrite: description, short_desc, itinerary,
--   inclusions, exclusions, start_time, meeting_point, duration
-- ============================================================

WITH tour_core_fix(id, name, short_desc, description, itinerary, inclusions, exclusions, duration, start_time, meeting_point, max_people, min_people, price_adult, price_child, price_infant) AS (VALUES

-- ─────────────────────────────────────────────────────────────────────────────
-- Tour 1: Ba Na Hills 1 Ngày (Buffet Trưa)
-- ─────────────────────────────────────────────────────────────────────────────
(1::int,
 'Tour Bà Nà Hills 1 Ngày (Buffet Trưa)',
 'Chinh phục đỉnh núi Chúa Đà Nẵng, đặt chân lên Cầu Vàng huyền thoại, dạo bước Làng Pháp cổ kính và thưởng thức buffet trưa với hơn 100 món đa dạng. Tour trọn ngày lý tưởng cho gia đình và nhóm bạn.',
 'Bà Nà Hills là khu nghỉ dưỡng núi bốn mùa nổi tiếng bậc nhất Việt Nam, tọa lạc tại độ cao 1.487 m so với mặt biển trên đỉnh Núi Chúa, cách trung tâm Đà Nẵng khoảng 40 km về phía Tây. Nơi đây sở hữu hệ thống cáp treo giữ nhiều kỷ lục thế giới, trong đó có đường cáp treo dài nhất thế giới không trụ đỡ (5.801 m) và độ chênh cao lớn nhất (1.291 m). Điểm nhấn không thể bỏ qua là Cầu Vàng – công trình kiến trúc độc đáo mô phỏng đôi bàn tay khổng lồ nâng đỡ cây cầu ở độ cao 1.400 m, đã thu hút hàng triệu du khách toàn cầu kể từ khi khánh thành năm 2018. Ngoài ra, du khách còn được khám phá Vườn hoa Le Jardin D''Amour với chín khu vườn hoa nghệ thuật đẳng cấp châu Âu, Làng Pháp cổ kính tái hiện kiến trúc trung cổ, Công viên trò chơi Fantasy Park trong nhà lớn nhất Việt Nam, Chùa Linh Ứng trên đỉnh Núi Chúa và rất nhiều điểm check-in ấn tượng. Thời tiết tại Bà Nà luôn mát mẻ quanh năm (khoảng 18–22°C), là nơi lý tưởng để thoát khỏi cái nóng của mùa hè Đà Nẵng. Tour được phục vụ bởi đội ngũ hướng dẫn viên chuyên nghiệp, xe du lịch đời mới và bữa buffet trưa phong phú tại nhà hàng trên đỉnh núi.',
 '[{"time":"07:30","title":"Đón khách tại trung tâm Đà Nẵng","description":"Xe 45 chỗ đời mới và hướng dẫn viên đón khách tại khách sạn hoặc điểm hẹn trung tâm thành phố. HDV phát nước uống, chia sẻ lịch trình và lưu ý an toàn trong suốt hành trình."},{"time":"09:00","title":"Đến ga cáp treo Bà Nà Hills","description":"Di chuyển khoảng 40 km lên Bà Nà. Tại chân núi, HDV phát vé cáp treo và hướng dẫn làm thủ tục. Trải nghiệm cảm giác bay trên mây với đường cáp treo dài nhất thế giới không trụ đỡ, ngắm toàn cảnh rừng nguyên sinh bên dưới."},{"time":"09:45","title":"Check-in Cầu Vàng – Vườn hoa Le Jardin D''Amour","description":"Khám phá biểu tượng kiến trúc Cầu Vàng ở độ cao 1.400 m, chụp ảnh tại Đôi bàn tay khổng lồ. Tiếp tục dạo bước qua chín khu vườn hoa nghệ thuật Le Jardin D''Amour với hàng nghìn loài hoa đua nở quanh năm."},{"time":"11:00","title":"Thám hiểm Làng Pháp & Chùa Linh Ứng","description":"Đi bộ qua những con phố đá cuội lát và kiến trúc trung cổ của Làng Pháp, ghé thăm các quán cà phê view núi. Viếng Chùa Linh Ứng Bà Nà trên đỉnh Núi Chúa, thả hồn trong không gian linh thiêng giữa mây trời."},{"time":"12:00","title":"Buffet trưa hơn 100 món tại đỉnh núi","description":"Thưởng thức bữa buffet trưa phong phú với hơn 100 món bao gồm hải sản, thịt nướng, món Á, món Âu và tráng miệng tươi ngon tại nhà hàng trên đỉnh Bà Nà. Không gian thoáng mát, tầm nhìn ra thung lũng mây."},{"time":"13:30","title":"Trải nghiệm Fantasy Park & tự do khám phá","description":"Công viên trò chơi trong nhà lớn nhất Việt Nam với hơn 105 trò chơi mạo hiểm như tàu lượn, nhà ma, mô phỏng thực tế ảo... Tự do chụp ảnh tại các điểm check-in nổi tiếng trong khu resort."},{"time":"15:30","title":"Đi cáp treo xuống núi","description":"Tập hợp tại ga cáp treo, đi xuống và di chuyển về Đà Nẵng. HDV chia sẻ gợi ý nhà hàng và địa điểm vui chơi tối tại thành phố."},{"time":"17:00","title":"Trả khách tại trung tâm Đà Nẵng","description":"Xe trả khách tại khách sạn hoặc điểm hẹn ban đầu. Kết thúc tour trọn ngày Bà Nà Hills đáng nhớ."}]'::json,
 '["Xe du lịch đời mới có máy lạnh, đưa đón tận khách sạn trung tâm Đà Nẵng","Hướng dẫn viên tiếng Việt chuyên nghiệp, vui vẻ và am hiểu địa phương","Vé cáp treo khứ hồi Bà Nà Hills (bao gồm tất cả các tuyến cáp trong khu)","Vé vào cổng Sun World Ba Na Hills và Fantasy Park","Bữa buffet trưa hơn 100 món tại nhà hàng trên đỉnh núi","Nước uống trên xe (1 chai/người)","Bảo hiểm du lịch cơ bản trong suốt hành trình"]'::json,
 '["Đồ uống trong bữa ăn (bia, nước ngọt, nước ép tính phí riêng)","Chi phí cá nhân: mua sắm, trò chơi thêm phí trong Fantasy Park","Bảo tàng sáp Madame Tussauds (100.000 đ/người, tự nguyện)","Phụ thu cuối tuần và ngày lễ theo thông báo của Sun World","Tiền tip cho hướng dẫn viên và tài xế (tự nguyện, khoảng 30.000–50.000 đ/người)"]'::json,
 '1 ngày (khoảng 9,5 tiếng)', '07:30', 'Khách sạn hoặc điểm hẹn trung tâm Đà Nẵng (Hải Châu, Sơn Trà, Ngũ Hành Sơn)', 45::int, 2::int, 1250000::numeric, 950000::numeric, 250000::numeric),

-- ─────────────────────────────────────────────────────────────────────────────
-- Tour 2: Phố Cổ Hội An & Rừng Dừa Bảy Mẫu
-- ─────────────────────────────────────────────────────────────────────────────
(2,
 'Tour Phố Cổ Hội An & Rừng Dừa Bảy Mẫu',
 'Trải nghiệm chèo thuyền thúng độc đáo trong rừng dừa nước Bảy Mẫu, rồi hòa mình vào nhịp sống phố cổ Hội An về đêm với đèn lồng rực rỡ và ẩm thực trứ danh.',
 'Hội An là đô thị cổ hiếm hoi ở Đông Nam Á còn giữ gần như nguyên vẹn kiến trúc thương cảng của thế kỷ 15–19, được UNESCO công nhận là Di sản Văn hóa Thế giới năm 1999. Rừng dừa nước Bảy Mẫu (hay Rừng dừa Cẩm Thanh) cách trung tâm Hội An khoảng 3 km là hệ sinh thái đất ngập nước nhiệt đới độc đáo, nơi hàng nghìn cây dừa nước tạo thành tán xanh mướt phủ kín mặt sông. Trải nghiệm chèo thuyền thúng nan – một loại thuyền tròn truyền thống của ngư dân Việt Nam – là hoạt động được du khách khắp thế giới yêu thích, đặc biệt ấn tượng khi các nghệ nhân biểu diễn kỹ năng "xoay thúng" ngoạn mục. Phố cổ Hội An về chiều tối là thời điểm đẹp nhất trong ngày: đèn lồng thắp sáng cả con phố, hoa đăng thả trên sông Hoài phản chiếu lung linh, mùi thơm của cao lầu, mì Quảng, bánh mì Phượng và chè bắp len lỏi khắp nơi. Tour kết hợp hai trải nghiệm đặc sắc nhất của vùng đất Hội An trong một hành trình buổi chiều–tối thoải mái.',
 '[{"time":"13:30","title":"Đón khách tại Đà Nẵng hoặc Hội An","description":"Xe và HDV đón khách tại khách sạn hoặc điểm hẹn. Trên đường, HDV giới thiệu lịch sử và văn hóa Hội An, chia sẻ tips về ăn uống và mua sắm đặc sản địa phương."},{"time":"14:30","title":"Rừng dừa Bảy Mẫu – Trải nghiệm chèo thuyền thúng","description":"Đến bến thuyền làng Cẩm Thanh, mặc áo phao và lên thuyền thúng nan truyền thống. Nghệ nhân địa phương dẫn bạn len lỏi qua các con mương xanh mướt, biểu diễn kỹ năng xoay thúng ấn tượng và chia sẻ về cuộc sống của cư dân làng chài. Tự do chụp ảnh giữa thiên nhiên yên bình."},{"time":"16:00","title":"Tham quan làng nghề và mua sắm đặc sản","description":"Ghé thăm cơ sở sản xuất đèn lồng Hội An truyền thống, được tận tay trải nghiệm làm đèn (nếu chọn gói thêm). Mua sắm các đặc sản: đèn lồng, gốm Thanh Hà, yến sào, hạt tiêu Tiên Phước."},{"time":"17:00","title":"Dạo phố cổ Hội An & thưởng thức ẩm thực","description":"Bộ hành qua những con phố cổ thơ mộng – Trần Phú, Nguyễn Thái Học, Bạch Đằng. Thưởng thức bữa tối gồm các món đặc sản Hội An: cao lầu, mì Quảng, hoành thánh chiên, cơm gà Hội An và chè trôi nước tại nhà hàng truyền thống được lựa chọn kỹ càng."},{"time":"19:00","title":"Thả hoa đăng trên sông Hoài","description":"Mỗi du khách được tặng một bông hoa đăng. Cùng nhau đi bộ ra bến sông Hoài, thắp đèn và thả hoa đăng cầu may, nhìn ngắm những ngọn đèn lung linh trôi trên dòng nước. Đây là khoảnh khắc lãng mạn nhất của tour Hội An về đêm."},{"time":"20:30","title":"Trả khách – Kết thúc tour","description":"Xe đưa khách về lại Đà Nẵng hoặc điểm hẹn tại Hội An. Kết thúc hành trình đầy cảm xúc."}]'::json,
 '["Xe du lịch đưa đón tại Đà Nẵng hoặc Hội An","Hướng dẫn viên tiếng Việt am hiểu văn hóa Hội An","Vé tham quan Rừng dừa Bảy Mẫu và trải nghiệm chèo thuyền thúng nan","Bữa tối đặc sản Hội An (cao lầu, cơm gà, hoành thánh, chè)","Hoa đăng thả sông Hoài (1 cái/người)","Vé vào khu phố cổ Hội An (một lần vào)","Nước uống trên xe"]'::json,
 '["Đồ uống thêm ngoài chương trình","Khoá tình yêu tại Cầu Nhật Bản (tự nguyện)","Mua sắm cá nhân","Tip cho hướng dẫn viên và tài xế","Các lần vào khu phố cổ tiếp theo sau khi đã rời khỏi"]'::json,
 '7 giờ (buổi chiều – tối)', '13:30', 'Đà Nẵng hoặc Hội An (đón tận khách sạn)', 30::int, 2::int, 750000::numeric, 550000::numeric, 150000::numeric),

-- ─────────────────────────────────────────────────────────────────────────────
-- Tour 3: Ngũ Hành Sơn & Chùa Linh Ứng Sơn Trà
-- ─────────────────────────────────────────────────────────────────────────────
(3,
 'Tour Ngũ Hành Sơn & Chùa Linh Ứng Sơn Trà',
 'Hành trình tâm linh nửa ngày chiêm bái Phật Bà cao nhất Đông Nam Á trên bán đảo Sơn Trà và khám phá hệ thống hang động huyền bí trong lòng núi đá vôi Ngũ Hành Sơn.',
 'Ngũ Hành Sơn (Marble Mountains) là quần thể năm ngọn núi đá cẩm thạch nhô lên giữa đồng bằng ven biển, cách trung tâm Đà Nẵng khoảng 8 km về phía Nam. Mỗi ngọn núi mang tên một yếu tố trong ngũ hành: Kim, Mộc, Thủy, Hỏa, Thổ. Trong đó Thủy Sơn là ngọn lớn nhất và thu hút nhiều du khách nhất với hệ thống hang động và chùa chiền ẩn sâu trong lòng đá: Hang Âm Phủ, Động Huyền Không (có lỗ thủng trên trần để ánh sáng chiếu thẳng vào), Chùa Tam Thai, Chùa Linh Ứng Ngũ Hành Sơn và vọng đài ngắm toàn cảnh Mỹ Khê – Non Nước. Ngoài hệ thống thắng cảnh, Ngũ Hành Sơn còn là trung tâm nghề điêu khắc đá Non Nước nổi tiếng với hàng trăm cơ sở chế tác sản phẩm đá mỹ nghệ tinh xảo. Sau Ngũ Hành Sơn, tour đưa bạn đến Chùa Linh Ứng Bãi Bụt trên bán đảo Sơn Trà – ngôi chùa lớn nhất trong ba ngôi chùa Linh Ứng tại Đà Nẵng, với tượng Phật Bà Quan Thế Âm cao 67 m – cao nhất Đông Nam Á, nhìn ra biển Đông bao la.',
 '[{"time":"08:00","title":"Đón khách tại trung tâm Đà Nẵng","description":"Xe và HDV đón khách tại khách sạn hoặc điểm hẹn. HDV phát nước uống và giới thiệu tổng quan về hai điểm đến."},{"time":"08:30","title":"Tham quan Ngũ Hành Sơn – Thủy Sơn","description":"Đến Ngũ Hành Sơn, leo thang đá lên đỉnh Thủy Sơn (có thang máy cho người cao tuổi). Khám phá Động Huyền Không – kỳ quan thiên nhiên trong lòng núi với ánh sáng tự nhiên lung linh xuyên qua vòm đá. Thăm Chùa Tam Thai và Chùa Linh Ứng Ngũ Hành Sơn. Ngắm toàn cảnh thành phố Đà Nẵng và biển Mỹ Khê từ vọng đài trên đỉnh."},{"time":"09:30","title":"Tham quan làng nghề điêu khắc đá Non Nước","description":"Dạo bước qua phố nghề điêu khắc đá truyền thống, ngắm nhìn và chụp ảnh cùng các tác phẩm điêu khắc tinh xảo từ tay các nghệ nhân lành nghề. Có thể mua đồ lưu niệm bằng đá cẩm thạch chất lượng cao."},{"time":"10:00","title":"Di chuyển đến bán đảo Sơn Trà – Chùa Linh Ứng Bãi Bụt","description":"Xe đưa đoàn vào cung đường biển ven bán đảo Sơn Trà với tầm nhìn tuyệt đẹp ra Vịnh Đà Nẵng và chuỗi đảo xa. Dừng chân chụp ảnh tại các điểm view đẹp dọc đường."},{"time":"10:30","title":"Chiêm bái Chùa Linh Ứng Bãi Bụt","description":"Tham quan ngôi chùa uy nghi với tượng Phật Bà Quan Thế Âm cao 67 m, cao nhất Đông Nam Á, đứng nhìn ra Biển Đông. Dâng hương, dạo bước qua vườn chùa thanh tịnh và chụp ảnh lưu niệm. HDV chia sẻ lịch sử và ý nghĩa tâm linh của địa danh."},{"time":"12:00","title":"Trả khách – Kết thúc tour","description":"Xe đưa khách về lại điểm hẹn ban đầu tại trung tâm Đà Nẵng. Kết thúc hành trình tâm linh nửa ngày trọn vẹn."}]'::json,
 '["Xe du lịch đưa đón tận khách sạn trung tâm Đà Nẵng","Hướng dẫn viên tiếng Việt am hiểu lịch sử và tâm linh địa phương","Vé tham quan Ngũ Hành Sơn (bao gồm thang máy lên Thủy Sơn)","Vé vào Chùa Linh Ứng Sơn Trà (miễn phí)","Nước uống bổ sung trên xe","Bảo hiểm du lịch cơ bản"]'::json,
 '["Bữa ăn trưa (kết thúc tour trước 12:30, bạn tự do ăn trưa)","Chi phí cá nhân và mua sắm","Tip cho hướng dẫn viên và tài xế"]'::json,
 '4 giờ (buổi sáng)', '08:00', 'Trung tâm Đà Nẵng (đón tận khách sạn)', 20::int, 2::int, 450000::numeric, 250000::numeric, 50000::numeric),

-- ─────────────────────────────────────────────────────────────────────────────
-- Tour 4: Cù Lao Chàm – Lặn ngắm san hô
-- ─────────────────────────────────────────────────────────────────────────────
(4,
 'Tour Cù Lao Chàm – Lặn Ngắm San Hô 1 Ngày',
 'Vượt sóng bằng cano cao tốc ra Cù Lao Chàm – Khu dự trữ sinh quyển thế giới, tận hưởng làn nước trong xanh, lặn ngắm san hô đa sắc và thưởng thức hải sản tươi rói ngay trên đảo.',
 'Cù Lao Chàm là cụm đảo gồm 8 hòn đảo lớn nhỏ nằm cách cửa biển Cửa Đại (Hội An) khoảng 15 km về phía Đông. Năm 2009, UNESCO công nhận Cù Lao Chàm – Hội An là Khu dự trữ sinh quyển thế giới nhờ hệ sinh thái biển đa dạng với hơn 165 loài san hô và hơn 200 loài cá. Nước biển quanh đảo đặc biệt trong và sạch (độ trong trung bình 10–15 m), tạo điều kiện lý tưởng cho các hoạt động lặn ngắm san hô và bơi lội. Ngoài thiên nhiên, Cù Lao Chàm còn hấp dẫn du khách bởi làng chài truyền thống, Chùa Hải Tạng cổ kính, nghề nuôi yến sào và ẩm thực biển đảo độc đáo. Tour khởi hành từ bến Cửa Đại bằng cano cao tốc (chỉ 20–25 phút), phù hợp cho gia đình, nhóm bạn và những ai yêu thích thiên nhiên hoang sơ.',
 '[{"time":"07:30","title":"Đón khách tại Đà Nẵng hoặc Hội An","description":"Xe đưa đoàn đến bến Cửa Đại, Hội An. HDV phân phát áo phao, kính lặn và hướng dẫn an toàn trên biển."},{"time":"08:30","title":"Xuất phát bằng cano cao tốc ra Cù Lao Chàm","description":"Cano cao tốc lướt sóng về phía đảo Cù Lao Chàm chỉ trong 20–25 phút, ngắm bình minh trên mặt biển và dãy núi từ xa. Đến đảo Hòn Lao – đảo chính của cụm đảo."},{"time":"09:00","title":"Thăm làng chài và Chùa Hải Tạng","description":"Bộ hành qua làng Bãi Làng và Bãi Hương, tìm hiểu cuộc sống ngư dân đảo. Thăm Chùa Hải Tạng – ngôi chùa cổ nhất Cù Lao Chàm, nơi có giếng nước cổ xây dựng từ thời Champa và những gốc cây ngàn năm tuổi."},{"time":"10:00","title":"Lặn ngắm san hô – Bơi lội tự do","description":"Di chuyển bằng thuyền đến các điểm lặn đẹp nhất quanh đảo (Bãi Chồng hoặc Bãi Nần tùy điều kiện biển). Mang kính lặn và ống thở, ngắm nhìn thế giới san hô đầy màu sắc và đàn cá biển đa dạng. Hướng dẫn viên lặn hỗ trợ những ai chưa có kinh nghiệm lặn biển."},{"time":"11:30","title":"Nghỉ ngơi – Tắm biển tự do tại Bãi Chồng","description":"Tự do tắm biển tại bãi cát trắng mịn, nước biển trong vắt của Bãi Chồng. Chụp ảnh, nằm phơi nắng hoặc thuê bè nổi nghỉ ngơi trên mặt nước."},{"time":"12:00","title":"Bữa trưa hải sản tươi ngay trên đảo","description":"Thưởng thức bữa trưa hải sản tươi do ngư dân đảo chế biến: cá hấp gừng, mực nướng, tôm luộc, cua rang muối, rau xào tỏi và cơm trắng. Không khí ăn ngoài trời sát mép biển, thư giãn sau buổi sáng bơi lội."},{"time":"13:30","title":"Tự do khám phá đảo hoặc thuê xe điện","description":"Thời gian tự do: thuê xe điện (tự trả phí) khám phá đường vòng đảo, mua đặc sản yến sào, ốc vú nàng, mắm cái hoặc đơn giản là ngồi thưởng cà phê nhìn ra biển."},{"time":"14:30","title":"Trở về đất liền bằng cano","description":"Tập hợp tại bến, lên cano về Cửa Đại. Xe đưa đoàn trở lại Đà Nẵng hoặc Hội An."},{"time":"15:30","title":"Trả khách – Kết thúc tour","description":"Trả khách tại điểm đón ban đầu. Kết thúc hành trình biển đảo Cù Lao Chàm tuyệt vời."}]'::json,
 '["Xe đưa đón từ Đà Nẵng hoặc Hội An đến bến Cửa Đại","Cano cao tốc khứ hồi Cửa Đại – Cù Lao Chàm","Hướng dẫn viên và thuyền viên hỗ trợ","Bộ kính lặn và ống thở (snorkel)","Áo phao bảo hiểm","Bữa trưa hải sản tươi trên đảo (3–4 món chính)","Phí bảo vệ môi trường biển đảo","Bảo hiểm du lịch cơ bản"]'::json,
 '["Lặn bình khí (scuba diving) có thu phí riêng","Thuê xe điện trên đảo","Đồ uống và bia trong bữa trưa","Mua đặc sản yến sào và hải sản khô","Phụ thu cao điểm hè (tháng 6–8)","Tip cho hướng dẫn viên và thuyền viên"]'::json,
 '1 ngày (khoảng 8 tiếng)', '07:30', 'Đà Nẵng hoặc Hội An (đón tận khách sạn, tập hợp tại bến Cửa Đại)', 35::int, 4::int, 650000::numeric, 450000::numeric, 100000::numeric),

-- ─────────────────────────────────────────────────────────────────────────────
-- Tour 5: Cố Đô Huế 1 Ngày từ Đà Nẵng
-- ─────────────────────────────────────────────────────────────────────────────
(5,
 'Tour Cố Đô Huế 1 Ngày từ Đà Nẵng',
 'Vượt đèo Hải Vân hùng vĩ, đặt chân đến cố đô ngàn năm văn hiến, chiêm ngưỡng Đại Nội Hoàng thành, Lăng Khải Định, Chùa Thiên Mụ và thưởng thức ẩm thực cung đình Huế.',
 'Huế – cố đô của triều Nguyễn từ năm 1802 đến 1945 – là một trong những trung tâm văn hóa, lịch sử và nghệ thuật lớn nhất Việt Nam. Quần thể Di tích Cố đô Huế được UNESCO công nhận là Di sản Văn hóa Thế giới năm 1993, gồm Hoàng thành Huế (Đại Nội), các lăng tẩm vua Nguyễn, chùa chiền và hệ thống phòng thủ bao quanh. Đại Nội (Kinh thành Huế) là công trình kiến trúc cung đình đồ sộ nhất Việt Nam với hơn 100 công trình lớn nhỏ, trong đó Ngọ Môn – Điện Thái Hòa là cổng chính của Tử Cấm Thành. Lăng Khải Định là sự pha trộn độc đáo giữa kiến trúc Á – Âu với những chi tiết khảm sành sứ tinh xảo không nơi nào trên thế giới có được. Chùa Thiên Mụ là ngôi chùa cổ nhất và nổi tiếng nhất Huế, biểu tượng của cố đô bên bờ sông Hương thơ mộng. Để đến Huế từ Đà Nẵng, tour đi qua hầm Hải Vân (hoặc vượt đèo theo yêu cầu), cung đường ven biển tuyệt đẹp qua Lăng Cô.',
 '[{"time":"07:00","title":"Đón khách – Khởi hành đến Huế","description":"Xe 45 chỗ đón khách tại khách sạn Đà Nẵng. Trên đường, HDV giới thiệu lịch sử triều Nguyễn và chuẩn bị kiến thức trước khi tham quan. Xe đi qua hầm Hải Vân, dừng ngắm cảnh Lăng Cô từ xa."},{"time":"09:30","title":"Đại Nội Huế – Hoàng Thành Triều Nguyễn","description":"Tham quan quần thể Hoàng thành Huế: qua Ngọ Môn uy nghi, chiêm ngưỡng Điện Thái Hòa nơi vua thiết triều, khám phá Tử Cấm Thành và các cung điện cổ. HDV kể chuyện về 13 vị vua nhà Nguyễn và những giai thoại cung đình hấp dẫn."},{"time":"11:30","title":"Bữa trưa đặc sản Huế","description":"Thưởng thức bữa trưa tại nhà hàng chuyên phục vụ ẩm thực Huế: bún bò Huế, cơm hến, bánh bèo, bánh nậm, bánh lọc, chè Huế. Huế nổi tiếng có ẩm thực phong phú và tinh tế nhất Việt Nam."},{"time":"13:00","title":"Lăng Khải Định – Kiệt tác khảm sành sứ","description":"Tham quan lăng mộ vua Khải Định tọa lạc trên sườn núi Châu Ê. Ngạc nhiên trước kỹ thuật khảm sành sứ và thủy tinh màu tinh xảo trên toàn bộ nội thất lăng – một kiệt tác mỹ thuật trang trí độc nhất vô nhị."},{"time":"14:00","title":"Chùa Thiên Mụ – Biểu tượng cố đô","description":"Viếng thăm chùa cổ nhất Huế bên bờ sông Hương, nơi có tháp Phước Duyên 7 tầng xây dựng năm 1844. Lắng nghe sự tích huyền bí về người đàn bà mặc áo đỏ và câu chuyện chiếc xe Austin mang đến Chùa Thiên Mụ."},{"time":"15:00","title":"Phố đi bộ Nguyễn Đình Chiểu & Chợ Đông Ba","description":"Tự do dạo bộ, mua đặc sản Huế tại Chợ Đông Ba: mè xửng, kẹo gừng, nón lá Huế, tranh thêu, áo dài Huế truyền thống."},{"time":"16:00","title":"Khởi hành trở về Đà Nẵng","description":"Xe đưa đoàn về Đà Nẵng qua hầm Hải Vân. HDV chia sẻ thêm thông tin và gợi ý các tour tiếp theo."},{"time":"18:30","title":"Trả khách tại Đà Nẵng","description":"Xe trả khách tại khách sạn hoặc điểm hẹn. Kết thúc hành trình cố đô Huế đáng nhớ."}]'::json,
 '["Xe du lịch đời mới có máy lạnh, đưa đón tận khách sạn Đà Nẵng","Hướng dẫn viên tiếng Việt chuyên sâu về lịch sử cố đô","Vé vào tất cả các điểm tham quan theo lịch trình (Đại Nội, Lăng Khải Định, Chùa Thiên Mụ)","Bữa trưa đặc sản Huế tại nhà hàng uy tín","Nước uống trên xe (2 chai/người cả ngày)","Bảo hiểm du lịch cơ bản"]'::json,
 '["Chi phí cá nhân và mua sắm tại Chợ Đông Ba","Đồ uống trong bữa ăn","Tip cho hướng dẫn viên và tài xế","Phụ thu nếu yêu cầu đi qua Đèo Hải Vân thay vì hầm (phải báo trước)","Lăng Tự Đức hoặc các điểm tham quan thêm ngoài lịch trình"]'::json,
 '1 ngày (khoảng 11 tiếng)', '07:00', 'Khách sạn hoặc điểm hẹn trung tâm Đà Nẵng', 40::int, 2::int, 1050000::numeric, 750000::numeric, 200000::numeric),

-- ─────────────────────────────────────────────────────────────────────────────
-- Tour 6: Thánh Địa Mỹ Sơn nửa ngày
-- ─────────────────────────────────────────────────────────────────────────────
(6,
 'Tour Thánh Địa Mỹ Sơn – Di Sản Văn Hóa Champa',
 'Khám phá bí ẩn quần thể tháp Chàm Mỹ Sơn – Di sản Văn hóa Thế giới UNESCO, thưởng thức biểu diễn múa Apsara huyền ảo và tìm hiểu về nền văn minh Champa rực rỡ từ thế kỷ 4–13.',
 'Thánh địa Mỹ Sơn là quần thể đền tháp Hindu của người Chăm tọa lạc trong thung lũng hẹp bao quanh bởi núi rừng, cách Đà Nẵng khoảng 70 km và cách Hội An khoảng 40 km. Đây là di tích quan trọng nhất của văn minh Champa – vương quốc cổ từng hưng thịnh tại miền Trung Việt Nam trong suốt hơn 1.000 năm (từ thế kỷ 4 đến 13 SCN). Quần thể gồm hơn 70 công trình kiến trúc đá và gạch, trong đó hơn 20 tháp còn tương đối nguyên vẹn. Điều kỳ diệu nhất của Mỹ Sơn là kỹ thuật xây tháp của người Chăm hoàn toàn không dùng vữa kết dính – cho đến nay các nhà khoa học vẫn chưa giải mã được hoàn toàn bí quyết này. Năm 1999, UNESCO công nhận Mỹ Sơn là Di sản Văn hóa Thế giới. Tour kết hợp tham quan khảo cổ và thưởng thức nghệ thuật biểu diễn múa Apsara – điệu múa thiêng của người Champa.',
 '[{"time":"07:30","title":"Đón khách tại Đà Nẵng hoặc Hội An","description":"Xe đón khách và khởi hành đến Mỹ Sơn. Trên đường, HDV kể câu chuyện về vương quốc Champa và lịch sử khám phá Mỹ Sơn từ thời người Pháp cuối thế kỷ 19."},{"time":"09:00","title":"Đến Mỹ Sơn – Tham quan quần thể đền tháp","description":"Đến khu di tích, nhận vé và bắt đầu tham quan theo hướng dẫn. Khám phá nhóm tháp B-C-D (nhóm trung tâm), tháp chính Mỹ Sơn E1 và tháp A1 được phục dựng. HDV phân tích kiến trúc và điêu khắc: hình tượng Shiva, Vishnu, Ganesha và các vũ nữ Apsara trên phù điêu đá sa thạch ngàn năm."},{"time":"10:30","title":"Biểu diễn múa Apsara – Nghệ thuật Champa","description":"Xem biểu diễn múa Apsara của đoàn nghệ thuật Champa chuyên nghiệp ngay trong khung cảnh đền tháp cổ kính. Điệu múa tái hiện vũ nữ thiêng phục vụ thần linh, với trang phục và âm nhạc truyền thống của người Chăm."},{"time":"11:30","title":"Bảo tàng trưng bày – Lưu niệm","description":"Ghé thăm khu trưng bày điêu khắc và hiện vật Champa tại chỗ. Mua đồ lưu niệm thủ công mỹ nghệ mang phong cách Champa do nghệ nhân địa phương chế tác."},{"time":"12:30","title":"Trả khách tại Hội An hoặc Đà Nẵng","description":"Xe đưa đoàn về điểm xuất phát. Kết thúc hành trình khám phá văn minh Champa huyền bí."}]'::json,
 '["Xe đưa đón từ Đà Nẵng hoặc Hội An","Hướng dẫn viên tiếng Việt am hiểu lịch sử Champa","Vé vào khu di tích Mỹ Sơn","Vé xem biểu diễn múa Apsara","Nước uống trên xe"]'::json,
 '["Bữa ăn trưa (kết thúc trước 13:00, bạn tự do ăn trưa)","Đồ uống cá nhân trong khu di tích","Mua sắm đặc sản và đồ lưu niệm","Tip cho hướng dẫn viên và tài xế"]'::json,
 '5 giờ (buổi sáng)', '07:30', 'Đà Nẵng hoặc Hội An (đón tận khách sạn)', 25::int, 2::int, 550000::numeric, 400000::numeric, 100000::numeric),

-- ─────────────────────────────────────────────────────────────────────────────
-- Tour 7: Đà Nẵng City Tour – Những Cây Cầu
-- ─────────────────────────────────────────────────────────────────────────────
(7,
 'Tour Đà Nẵng City Tour – Khám Phá Những Cây Cầu & Biểu Tượng',
 'City tour nửa ngày check-in các biểu tượng hiện đại của Đà Nẵng: Bảo tàng Điêu khắc Chăm, Cầu Rồng phun lửa, Cầu Tình Yêu và chợ Hàn sầm uất.',
 'Đà Nẵng là thành phố biển phát triển năng động bậc nhất miền Trung Việt Nam, nổi tiếng với hệ thống cơ sở hạ tầng hiện đại và những cây cầu độc đáo bắc qua sông Hàn. Cầu Rồng (Dragon Bridge) là biểu tượng của Đà Nẵng, dài 666 m, có hình dáng con rồng Việt bay ra biển; cuối tuần và ngày lễ, cầu phun lửa và phun nước vào 21:00. Cầu Tình Yêu (Love Lock Bridge) là điểm hẹn hò nổi tiếng với hàng nghìn ổ khóa tình yêu gắn dọc lan can. Bảo tàng Điêu khắc Chăm là bảo tàng duy nhất ở Đông Nam Á chuyên về nghệ thuật Champa với hơn 300 hiện vật điêu khắc từ thế kỷ 7–15. Chợ Hàn là chợ truyền thống lớn nhất Đà Nẵng, nơi tập trung đặc sản địa phương: mắm nêm, bánh tráng, hải sản khô và hàng thủ công.',
 '[{"time":"08:30","title":"Đón khách tại trung tâm Đà Nẵng","description":"Xe và HDV đón khách, khởi hành tham quan thành phố với bản đồ và tài liệu giới thiệu Đà Nẵng."},{"time":"09:00","title":"Bảo tàng Điêu khắc Chăm","description":"Tham quan bảo tàng lưu giữ hơn 300 tác phẩm điêu khắc Champa từ thế kỷ 7–15, duy nhất tại Đông Nam Á. HDV giải thích ý nghĩa của các biểu tượng: Shiva – Vishnu – Ganesha, vũ nữ Apsara và hệ thống thần linh trong văn minh Champa."},{"time":"10:00","title":"Cầu Rồng – Cầu Tình Yêu – Bờ sông Hàn","description":"Tản bộ dọc bờ sông Hàn, chụp ảnh tại Cầu Rồng và Cầu Tình Yêu. HDV kể về lịch sử xây dựng những cây cầu biểu tượng của Đà Nẵng, ý nghĩa hình tượng Rồng Việt hướng ra biển Đông."},{"time":"11:00","title":"Chợ Hàn – Ẩm thực & Đặc sản địa phương","description":"Khám phá Chợ Hàn – linh hồn ẩm thực của Đà Nẵng. Thưởng thức bún chả cá, bánh xèo, nem lụi và mì Quảng tại các quán ăn ven chợ. Mua sắm đặc sản: mắm nêm Đà Nẵng, bánh tráng Túy Loan, hải sản sấy khô."},{"time":"12:00","title":"Trả khách – Kết thúc tour","description":"Xe trả khách tại khách sạn hoặc điểm hẹn. Kết thúc buổi sáng city tour Đà Nẵng."}]'::json,
 '["Xe du lịch đưa đón tận khách sạn","Hướng dẫn viên tiếng Việt","Vé vào Bảo tàng Điêu khắc Chăm","Nước uống trên xe"]'::json,
 '["Bữa ăn trưa","Đồ uống và ăn vặt tại chợ Hàn","Mua sắm cá nhân","Tip cho hướng dẫn viên"]'::json,
 '3,5 giờ (buổi sáng)', '08:30', 'Trung tâm Đà Nẵng (đón tận khách sạn)', 15::int, 2::int, 350000::numeric, 200000::numeric, 0::numeric),

-- ─────────────────────────────────────────────────────────────────────────────
-- Tour 8: Đèo Hải Vân & Vịnh Lăng Cô
-- ─────────────────────────────────────────────────────────────────────────────
(8,
 'Tour Đèo Hải Vân & Vịnh Lăng Cô – Thiên Hạ Đệ Nhất Hùng Quan',
 'Chinh phục "thiên hạ đệ nhất hùng quan" – Đèo Hải Vân hùng vĩ, ngắm nhìn bán đảo Lăng Cô thơ mộng và tắm biển tại vịnh nước xanh trong tuyệt đẹp.',
 'Đèo Hải Vân (Hải Vân Quan) là đèo núi cao và dài nhất Việt Nam nằm trên dãy Trường Sơn, phân chia ranh giới tỉnh Thừa Thiên Huế và thành phố Đà Nẵng, ở độ cao 496 m so với mặt biển. Đèo dài khoảng 21 km, có cung đường ven biển nguy hiểm nhưng thơ mộng với một bên là vách núi dựng đứng, một bên là biển xanh sâu thẳm. Tên "Hải Vân" nghĩa là "biển mây" – bởi đây là nơi thường xuyên có mây mù bao phủ, tạo ra cảnh quan kỳ ảo. Hải Vân Quan – cửa quan trên đỉnh đèo xây dựng từ thời Nguyễn là di tích lịch sử còn nhiều giá trị khảo cổ. Phía Nam đèo là Vịnh Lăng Cô – một trong những vịnh đẹp nhất thế giới theo bình chọn của World Bays Club, với bãi cát trắng dài 10 km, nước biển trong xanh và cảnh quan thiên nhiên hoang sơ chưa bị đô thị hóa. Đây là cung đường mà Jeremy Clarkson và đoàn Top Gear gọi là "một trong những cung đường đẹp nhất thế giới".',
 '[{"time":"08:00","title":"Đón khách tại Đà Nẵng","description":"Xe đón khách và khởi hành về hướng Bắc theo Quốc lộ 1A. HDV giới thiệu lịch sử và văn hóa khu vực."},{"time":"09:00","title":"Chinh phục Đèo Hải Vân","description":"Xe leo lên đèo Hải Vân theo cung đường cũ quanh co (thay vì hầm đường bộ). Dừng tại Hải Vân Quan trên đỉnh đèo, tham quan cửa quan lịch sử và chiêm ngưỡng toàn cảnh Vịnh Đà Nẵng về phía Nam, Vịnh Lăng Cô về phía Bắc. Chụp ảnh toàn cảnh từ đỉnh đèo – tầm nhìn 360 độ không gian biển–núi tuyệt đẹp."},{"time":"10:30","title":"Lăng Cô – Tắm biển và nghỉ dưỡng","description":"Xuống đèo vào Vịnh Lăng Cô. Nghỉ ngơi tại bãi biển cát trắng dài mịn màng, tắm biển nước trong xanh. HDV giới thiệu về kế hoạch phát triển du lịch Lăng Cô và chia sẻ về đời sống ngư dân địa phương."},{"time":"12:30","title":"Bữa trưa hải sản tươi Lăng Cô","description":"Thưởng thức bữa trưa hải sản tươi tại nhà hàng ven biển: tôm hùm, cua biển, cá mú hấp gừng, sò điệp nướng mỡ hành. Nước biển Lăng Cô đảm bảo hải sản luôn tươi ngon nhất."},{"time":"14:00","title":"Tham quan Lăng Cô và cầu đường sắt","description":"Dạo bộ quanh thị trấn Lăng Cô, chụp ảnh tại cây cầu đường sắt cong vắt qua đầm phá, tìm hiểu đặc sản địa phương."},{"time":"15:00","title":"Về Đà Nẵng qua hầm Hải Vân","description":"Xe di chuyển về Đà Nẵng qua hầm đường bộ Hải Vân – hầm đường bộ dài thứ hai Đông Nam Á."},{"time":"16:30","title":"Trả khách tại Đà Nẵng – Kết thúc tour","description":"Trả khách tại điểm hẹn ban đầu. Kết thúc hành trình Đèo Hải Vân – Lăng Cô trọn vẹn."}]'::json,
 '["Xe du lịch đưa đón tại Đà Nẵng","Hướng dẫn viên tiếng Việt","Bữa trưa hải sản tại Lăng Cô (3–4 món chính)","Nước uống trên xe","Bảo hiểm du lịch"]'::json,
 '["Dịch vụ biển thêm: jetski, dù bay, cano","Đồ uống trong bữa trưa","Mua sắm cá nhân","Tip cho hướng dẫn viên và tài xế"]'::json,
 '1 ngày (khoảng 8,5 tiếng)', '08:00', 'Trung tâm Đà Nẵng (đón tận khách sạn)', 20::int, 2::int, 850000::numeric, 600000::numeric, 150000::numeric),

-- ─────────────────────────────────────────────────────────────────────────────
-- Tour 9: Đêm Phố Cổ Hội An & Ăn Tối
-- ─────────────────────────────────────────────────────────────────────────────
(9,
 'Tour Đêm Phố Cổ Hội An – Đèn Lồng & Ẩm Thực',
 'Buổi chiều–tối lãng mạn tại Hội An: dạo phố đèn lồng rực rỡ, thưởng thức bữa tối đặc sản và thả hoa đăng cầu nguyện trên dòng Hoài giang.',
 'Phố cổ Hội An về đêm là một trong những trải nghiệm hút hồn nhất của du lịch Việt Nam. Khi màn đêm buông xuống, hàng nghìn chiếc đèn lồng đủ màu sắc – đặc sản thủ công độc đáo của Hội An – thắp sáng rực cả phố phường, tạo nên một bức tranh lung linh như cổ tích. Phố cổ Hội An là Di sản Văn hóa Thế giới UNESCO từ năm 1999, với hơn 1.000 công trình kiến trúc cổ còn được bảo tồn nguyên vẹn từ thế kỷ 15–19: Chùa Phúc Kiến, Nhà cổ Tấn Ký, Hội quán Triều Châu, Cầu Nhật Bản (Lai Viễn Kiều). Tại đây còn diễn ra Ngày Rằm Phố Đèn Lồng hàng tháng – đêm 14 âm lịch mọi đèn điện tắt hết, chỉ còn đèn lồng và nến, tạo không gian cổ tích đặc biệt. Bên cạnh kiến trúc, Hội An còn được biết đến là "thủ đô ẩm thực" miền Trung với vô số món ngon nổi tiếng: cao lầu, hoành thánh chiên, cơm gà Hội An, bánh mì Phượng, chè bắp, chè trôi nước.',
 '[{"time":"16:00","title":"Đón khách tại Đà Nẵng","description":"Xe đón khách và đưa đến Hội An trước giờ đèn lồng thắp sáng. Trên đường, HDV giới thiệu ẩm thực và kiến trúc đặc trưng của Hội An."},{"time":"17:00","title":"Tham quan Phố Cổ Hội An","description":"Bộ hành qua những con phố cổ đẹp nhất: Trần Phú – phố chính của Hội An với hai dãy nhà cổ sơn vàng đặc trưng. Thăm Cầu Nhật Bản (Lai Viễn Kiều) – biểu tượng của Hội An xây năm 1593. Tham quan một nhà cổ trăm năm tuổi và nghe kể về thương cảng sầm uất một thời."},{"time":"18:00","title":"Bữa tối đặc sản Hội An","description":"Thưởng thức bữa tối tại nhà hàng truyền thống: cao lầu – sợi mì vàng đặc trưng chỉ có ở Hội An, hoành thánh chiên, cơm gà Hội An, rau sống và nước mắm Nam Ô. HDV giới thiệu câu chuyện về nguồn gốc và ý nghĩa của từng món ăn."},{"time":"19:30","title":"Đèn lồng rực rỡ – Nhiếp ảnh đêm phố cổ","description":"Tận hưởng không khí phố đèn lồng khi đêm xuống: hàng nghìn chiếc đèn lồng xanh đỏ tím vàng thắp sáng các con phố. Thời điểm đẹp nhất để chụp ảnh long lanh, check-in Instagram và cảm nhận linh hồn Hội An."},{"time":"20:00","title":"Thả hoa đăng trên sông Hoài","description":"HDV tặng mỗi người một bông hoa đăng. Cùng nhau ra bến sông Hoài, thắp nến và thả hoa đăng cầu may mắn, nhìn ngắm những ngọn đèn lung linh trôi theo dòng nước. Khoảnh khắc lãng mạn khó quên nhất Hội An."},{"time":"21:00","title":"Xe đưa về Đà Nẵng","description":"Tập hợp và lên xe về Đà Nẵng. Kết thúc buổi tối đầy cảm xúc tại phố cổ Hội An."}]'::json,
 '["Xe đưa đón tại Đà Nẵng","Hướng dẫn viên tiếng Việt am hiểu văn hóa Hội An","Vé tham quan phố cổ Hội An (một lần)","Bữa tối đặc sản Hội An (4–5 món chính)","Hoa đăng thả sông Hoài (1 cái/người)","Nước uống trên xe"]'::json,
 '["Mua sắm cá nhân tại phố cổ","Đồ uống trong bữa tối","Khoá tình yêu (tự nguyện)","Tip cho hướng dẫn viên và tài xế","Thuyền đi dạo sông Hoài (tự trả phí)"]'::json,
 '5 giờ (chiều – tối)', '16:00', 'Trung tâm Đà Nẵng hoặc Hội An (đón tận khách sạn)', 25::int, 2::int, 600000::numeric, 450000::numeric, 100000::numeric),

-- ─────────────────────────────────────────────────────────────────────────────
-- Tour 10: Bà Nà Hills Đêm (Sun World Night)
-- ─────────────────────────────────────────────────────────────────────────────
(10,
 'Tour Bà Nà Hills Đêm – Sun World By Night',
 'Trải nghiệm Bà Nà Hills phiên bản huyền ảo về đêm: ánh đèn lung linh, show diễn After Glow đặc sắc, buffet tối phong phú và không khí mát mẻ dưới ánh trăng đỉnh núi.',
 'Bà Nà Hills về đêm là một trải nghiệm hoàn toàn khác biệt so với ban ngày. Khi ánh tà dương tắt dần, toàn bộ khu nghỉ dưỡng được thắp sáng bằng hàng vạn ngọn đèn LED đủ màu, tạo nên một thành phố ánh sáng lung linh trên đỉnh núi cao 1.487 m. Làng Pháp về đêm với những ngọn đèn lồng vàng ấm áp và tiếng nhạc du dương trở nên lãng mạn như khung cảnh trong truyện cổ tích châu Âu. Show diễn After Glow – chương trình nghệ thuật kết hợp ánh sáng, âm nhạc và vũ đạo hiện đại – là màn trình diễn đỉnh cao chỉ có vào buổi tối. Buffet tối tại nhà hàng Beer Plaza trên đỉnh núi phục vụ ẩm thực quốc tế phong phú kết hợp với không gian view núi mây huyền ảo. Tour chiều–tối này còn có ưu điểm là đến Bà Nà khi đường lên vắng hơn ban ngày, trải nghiệm cáp treo khứ hồi vào giờ vàng buổi chiều.',
 '[{"time":"14:30","title":"Đón khách tại Đà Nẵng","description":"Xe đón khách và khởi hành lên Bà Nà. HDV giới thiệu lịch trình buổi tối và các điểm check-in đẹp nhất về đêm."},{"time":"15:30","title":"Lên cáp treo – Đến Bà Nà Hills","description":"Lên cáp treo thế giới kỷ lục trong ánh chiều tà, ngắm cảnh rừng núi chuyển sắc khi nắng chiều nghiêng bóng. Bầu trời mây thường mở ra sau 15:00, tạo khung cảnh đẹp hơn ban sáng."},{"time":"16:00","title":"Cầu Vàng & Vườn Hoa – Golden Hour","description":"Chụp ảnh Cầu Vàng trong giờ vàng ánh chiều – khoảng thời gian nhiều nhiếp ảnh gia yêu thích nhất vì ánh sáng mềm và màu sắc ấm. Dạo qua vườn hoa Le Jardin D''Amour khi hoa rực rỡ nhất."},{"time":"18:00","title":"Buffet tối quốc tế tại Beer Plaza","description":"Thưởng thức bữa buffet tối phong phú tại nhà hàng Beer Plaza với hàng chục món Á – Âu, hải sản, thịt nướng, rượu vang và bia thủ công. Không gian ngoài trời mát mẻ với view thung lũng mây huyền ảo."},{"time":"19:30","title":"Show After Glow – Ánh Sáng Nghệ Thuật","description":"Xem chương trình nghệ thuật After Glow: màn trình diễn kết hợp ánh sáng laser, vũ đạo hiện đại và âm nhạc sống động. Đây là show diễn đặc trưng chỉ có vào buổi tối tại Bà Nà Hills."},{"time":"20:30","title":"Tự do khám phá Bà Nà về đêm","description":"Tự do dạo bước Làng Pháp lung linh ánh đèn, chụp ảnh đêm, thưởng thức cà phê hoặc giải khát tại các quán bar trên đỉnh núi."},{"time":"21:30","title":"Xuống cáp treo – Về Đà Nẵng","description":"Tập hợp và đi cáp treo xuống núi. Xe đưa đoàn về Đà Nẵng."},{"time":"22:30","title":"Trả khách – Kết thúc tour","description":"Xe trả khách tại khách sạn. Kết thúc đêm Bà Nà Hills huyền ảo đáng nhớ."}]'::json,
 '["Xe đưa đón tại Đà Nẵng","Hướng dẫn viên","Vé cáp treo khứ hồi Bà Nà Hills","Vé vào khu Sun World (bao gồm Fantasy Park và các khu vui chơi)","Bữa buffet tối tại Beer Plaza (bao gồm rượu vang và bia)","Vé xem show After Glow","Nước uống trên xe"]'::json,
 '["Đồ uống extra ngoài phần buffet","Trò chơi thêm phí trong Fantasy Park","Bảo tàng sáp Madame Tussauds","Tip cho hướng dẫn viên và tài xế","Phụ thu cuối tuần và ngày lễ"]'::json,
 '8 giờ (chiều – tối)', '14:30', 'Trung tâm Đà Nẵng (đón tận khách sạn)', 50::int, 2::int, 950000::numeric, 750000::numeric, 200000::numeric),

-- ─────────────────────────────────────────────────────────────────────────────
-- Tour 11: VinWonders Nam Hội An Full Day
-- ─────────────────────────────────────────────────────────────────────────────
(11,
 'Tour VinWonders Nam Hội An – Công Viên Giải Trí Đẳng Cấp',
 'Trọn ngày vui chơi không giới hạn tại VinWonders Nam Hội An: Safari hoang dã, công viên nước mát lạnh, Đảo Văn Hóa đa sắc tộc và vô số trò chơi mạo hiểm đỉnh cao.',
 'VinWonders Nam Hội An là tổ hợp giải trí và du lịch đẳng cấp quốc tế do Vingroup phát triển, tọa lạc tại xã Bình Minh, huyện Thăng Bình, Quảng Nam, cách Hội An khoảng 25 km về phía Nam. Khu phức hợp rộng hơn 1.300 ha gồm nhiều khu vực: VinSafari (safari tự nhiên lớn nhất Việt Nam với hơn 1.000 cá thể động vật hoang dã), VinWonders (công viên vui chơi giải trí với hơn 50 trò chơi hiện đại), công viên nước Aquatopia (hơn 20 trò chơi dưới nước), Đảo Văn Hóa tái hiện kiến trúc và văn hóa 9 quốc gia Đông Nam Á, và rất nhiều nhà hàng, cơ sở lưu trú cao cấp. Tour trọn ngày cho phép tự do khám phá tất cả các khu vực theo sở thích, phù hợp cho gia đình có trẻ nhỏ, nhóm bạn và cặp đôi.',
 '[{"time":"08:30","title":"Đón khách – Khởi hành đến VinWonders","description":"Xe buýt tham quan đón khách tại điểm hẹn hoặc khách sạn trung tâm. HDV phát vé và bản đồ khu vui chơi, hướng dẫn cách tổ chức lịch trình tự do trong ngày."},{"time":"09:30","title":"VinSafari – Vườn thú hoang dã lớn nhất VN","description":"Tham quan VinSafari bằng xe điện hoặc xe buýt safari qua các khu vực nuôi thú: Sư tử châu Phi, Hà mã, Tê giác trắng, Hổ Bengal, Gấu Bắc Cực, Voi châu Á... Xem biểu diễn thú được huấn luyện và chụp ảnh cùng các loài động vật an toàn."},{"time":"11:30","title":"Aquatopia – Công viên nước mát lạnh","description":"Thỏa sức vui chơi tại công viên nước Aquatopia với hơn 20 trò chơi dưới nước: đường trượt xoáy, suối lười nhiệt đới, hồ sóng khổng lồ, đường trượt thẳng đứng tốc độ cao và bể bơi trẻ em Kiddie Pool."},{"time":"12:30","title":"Bữa trưa set menu tại nhà hàng trong khu","description":"Thưởng thức bữa trưa set menu phong phú tại nhà hàng trong khu VinWonders với không gian rộng rãi, sạch sẽ."},{"time":"13:30","title":"VinWonders – Công viên trò chơi mạo hiểm","description":"Trải nghiệm các trò chơi cảm giác mạnh: tàu lượn siêu tốc Dragon Coaster, nhà ma kinh dị, mô phỏng thực tế ảo VR, Ferris Wheel ngắm toàn cảnh... Phù hợp từ trẻ em đến người lớn với nhiều cấp độ kịch tính khác nhau."},{"time":"15:30","title":"Đảo Văn Hóa – Kiến trúc 9 quốc gia","description":"Dạo qua Đảo Văn Hóa, khám phá kiến trúc đặc trưng của 9 quốc gia Đông Nam Á được tái hiện sinh động: Việt Nam, Thái Lan, Indonesia, Malaysia, Campuchia, Myanmar, Singapore, Philippines và Lào. Chụp ảnh check-in tại các công trình đặc sắc."},{"time":"17:00","title":"Tự do – Mua sắm đặc sản","description":"Thời gian tự do mua sắm quà lưu niệm, thưởng thức đồ ăn đường phố trong khu hoặc thư giãn trước khi lên xe về."},{"time":"17:30","title":"Lên xe – Về Đà Nẵng/Hội An","description":"Tập hợp và lên xe về Đà Nẵng hoặc Hội An."},{"time":"18:30","title":"Trả khách – Kết thúc tour","description":"Xe trả khách tại điểm hẹn. Kết thúc ngày vui trọn vẹn tại VinWonders."}]'::json,
 '["Xe bus/xe du lịch đưa đón","Hướng dẫn viên","Vé vào cổng tổng hợp VinWonders (bao gồm VinSafari, Aquatopia, VinWonders, Đảo Văn Hóa)","Bữa trưa set menu tại nhà hàng trong khu"]'::json,
 '["Mua sắm, đồ ăn vặt và đồ uống cá nhân","Chi phí dịch vụ thêm trong khu (photo studio, sticker photo...)","Tip cho hướng dẫn viên và tài xế","Phụ thu cuối tuần và ngày lễ"]'::json,
 '10 giờ (trọn ngày)', '08:30', 'Đà Nẵng hoặc Hội An (đón tận khách sạn)', 50::int, 2::int, 900000::numeric, 700000::numeric, 150000::numeric),

-- ─────────────────────────────────────────────────────────────────────────────
-- Tour 12: Suối Khoáng Nóng Núi Thần Tài Relax
-- ─────────────────────────────────────────────────────────────────────────────
(12,
 'Tour Suối Khoáng Nóng Núi Thần Tài – Tắm Bùn & Nghỉ Dưỡng',
 'Một ngày tái tạo năng lượng hoàn hảo tại Núi Thần Tài: ngâm mình trong suối khoáng nóng thiên nhiên, tắm bùn khoáng chất, trải nghiệm spa và vui chơi tại công viên nước.',
 'Khu du lịch Núi Thần Tài (Sun Spa Resort) tọa lạc tại huyện Hòa Vang, cách trung tâm Đà Nẵng khoảng 25 km về phía Tây, nằm giữa cảnh quan núi rừng xanh mướt. Nơi đây có nguồn nước khoáng nóng thiên nhiên được công nhận là có giá trị y tế cao, nhiệt độ trung bình 37–42°C, giàu khoáng chất như natri, bicarbonate, canxi và magiê – có tác dụng điều trị xương khớp, thư giãn cơ và phục hồi sức khỏe. Khu phức hợp gồm hệ thống hồ khoáng nóng ngoài trời, phòng tắm bùn khoáng nóng (đặc biệt), khu xông hơi thảo dược, spa massage cao cấp, công viên nước vui chơi và nhà hàng buffet. Tour này được thiết kế cho những ai muốn thoát khỏi nhịp sống bận rộn và tìm kiếm sự thư giãn hoàn toàn trong một ngày.',
 '[{"time":"08:00","title":"Đón khách tại Đà Nẵng","description":"Xe và HDV đón khách, khởi hành đến Núi Thần Tài. Phát khăn tắm và hướng dẫn quy định trong khu."},{"time":"08:45","title":"Check-in Núi Thần Tài – Nhận phòng thay đồ","description":"Nhận vé, đổi đồ bơi và giầy tắm tại nhà tắm công cộng rộng rãi. HDV hướng dẫn lịch trình tự do trong ngày và lưu ý các khu vực không nên bỏ qua."},{"time":"09:00","title":"Tắm bùn khoáng – Liệu pháp thư giãn","description":"Ngâm mình trong bể tắm bùn khoáng nóng giàu dưỡng chất. Tắm bùn khoáng có tác dụng làm sạch lỗ chân lông, nuôi dưỡng da, giảm đau nhức xương khớp và thư giãn cơ sâu. Đây là trải nghiệm đặc trưng không thể bỏ qua tại Núi Thần Tài."},{"time":"10:00","title":"Suối Khoáng Nóng Thiên Nhiên & Hồ Ngoài Trời","description":"Ngâm mình trong các bể khoáng nóng nhiệt độ khác nhau (37°C, 40°C, 42°C), xen kẽ giữa hồ nóng và hồ lạnh để kích thích tuần hoàn máu. Tận hưởng không gian hồ khoáng ngoài trời giữa thiên nhiên núi rừng trong lành."},{"time":"11:30","title":"Spa Massage Thư Giãn (tùy chọn)","description":"Có thể đặt thêm dịch vụ massage body truyền thống, massage đá nóng hoặc chăm sóc da mặt tại spa cao cấp trong khu (tự trả phí riêng)."},{"time":"12:00","title":"Buffet trưa phong phú","description":"Thưởng thức buffet trưa tại nhà hàng trong khu với nhiều món Á – Âu, đặc biệt là các món ăn tốt cho sức khỏe. Không gian mát mẻ với tầm nhìn vườn cây xanh mướt."},{"time":"13:30","title":"Công viên nước – Trò chơi mùa hè","description":"Vui chơi tại khu công viên nước với đường trượt, hồ sóng, suối lười và vui chơi dưới nước. Phù hợp cho trẻ em và người lớn muốn vận động sau bữa trưa."},{"time":"15:30","title":"Tự do thư giãn – Nghỉ ngơi","description":"Thời gian tự do: nằm phơi nắng, ngủ nghỉ trong khu nghỉ dưỡng, đọc sách hay đơn giản là nhâm nhi ly cà phê nhìn ra núi rừng."},{"time":"16:30","title":"Lên xe – Trở về Đà Nẵng","description":"Tập hợp và lên xe về Đà Nẵng."},{"time":"17:30","title":"Trả khách – Kết thúc tour","description":"Xe trả khách tại điểm hẹn. Kết thúc ngày nghỉ dưỡng thư giãn Núi Thần Tài."}]'::json,
 '["Xe đưa đón tại Đà Nẵng","Hướng dẫn viên","Vé vào cổng Núi Thần Tài (bao gồm tắm bùn, hồ khoáng nóng và công viên nước)","Buffet trưa tại nhà hàng trong khu","Nước uống trên xe","Bảo hiểm du lịch"]'::json,
 '["Tắm bùn sa (bùn cát – tính phí riêng)","Spa massage (tính phí riêng)","Phòng nghỉ riêng (tính phí riêng)","Đồ uống trong bữa trưa","Tip cho hướng dẫn viên và tài xế"]'::json,
 '9,5 giờ (trọn ngày)', '08:00', 'Trung tâm Đà Nẵng (đón tận khách sạn)', 30::int, 2::int, 850000::numeric, 650000::numeric, 150000::numeric),

-- ─────────────────────────────────────────────────────────────────────────────
-- Tour 13: Trekking Bán Đảo Sơn Trà
-- ─────────────────────────────────────────────────────────────────────────────
(13,
 'Tour Trekking Bán Đảo Sơn Trà – Tìm Voọc & Leo Núi Bàn Cờ',
 'Trekking rừng nguyên sinh Sơn Trà – thiên đường xanh giữa lòng thành phố biển: săn ảnh Voọc chà vá chân nâu quý hiếm, chinh phục đỉnh Bàn Cờ và ngắm toàn cảnh Đà Nẵng.',
 'Bán đảo Sơn Trà là khu bảo tồn thiên nhiên nằm ngay trong lòng thành phố Đà Nẵng, cách trung tâm chỉ 10 km. Rừng Sơn Trà là khu rừng nhiệt đới nguyên sinh hiếm hoi còn tồn tại sát khu đô thị sầm uất, với diện tích khoảng 4.400 ha. Đây là nơi cư trú của quần thể Voọc chà vá chân nâu (Red-shanked douc langur) lớn nhất thế giới – loài linh trưởng có màu sắc sặc sỡ đẹp nhất trong họ khỉ, được IUCN xếp vào danh sách Nguy cấp và là biểu tượng động vật của Đà Nẵng. Rừng Sơn Trà còn là địa bàn của hơn 287 loài thực vật quý, 287 loài động vật trong đó có nhiều loài đặc hữu. Đỉnh Bàn Cờ (693 m) là điểm cao nhất của Sơn Trà, từ đây nhìn thấy toàn cảnh thành phố Đà Nẵng, sân bay, cảng biển và dải bờ biển dài từ Non Nước đến Tiên Sa.',
 '[{"time":"05:30","title":"Tập hợp tại chân Sơn Trà – Khởi động","description":"Tập hợp tại cổng vào bán đảo Sơn Trà khi trời còn mát. HDV trekking chuyên nghiệp phát gậy trekking, bình nước và hướng dẫn kỹ thuật đi rừng an toàn, quy tắc bảo vệ thiên nhiên."},{"time":"06:00","title":"Trekking rừng nguyên sinh – Tìm kiếm Voọc Chà Vá","description":"Bắt đầu hành trình đi bộ trong rừng nguyên sinh Sơn Trà theo tuyến đường mòn chính. Đây là thời điểm vàng để quan sát Voọc chà vá chân nâu hoạt động và ăn uống. HDV hướng dẫn cách tiếp cận yên lặng và chụp ảnh Voọc mà không làm chúng hoảng sợ."},{"time":"08:00","title":"Điểm nghỉ giữa rừng – Ăn sáng nhẹ","description":"Dừng chân tại điểm nghỉ giữa rừng, thưởng thức bánh mì và hoa quả – bữa ăn sáng dã ngoại giữa thiên nhiên hoang dã. Nghe tiếng chim hót và hít thở không khí trong lành của rừng nguyên sinh."},{"time":"08:30","title":"Tiếp tục leo lên đỉnh Bàn Cờ (693 m)","description":"Chinh phục đoạn đường dốc lên đỉnh Bàn Cờ. Tại đỉnh, phóng tầm mắt ra toàn cảnh 360 độ: thành phố Đà Nẵng nhìn từ trên cao, biển Đông xanh thẳm, cảng Tiên Sa và dãy Trường Sơn xa xa."},{"time":"10:00","title":"Xuống núi – Tham quan cung đường biển Sơn Trà","description":"Xuống núi theo đường khác, đi qua các điểm view biển đẹp dọc cung đường ven bán đảo: Bãi Bắc, Bãi Rạng, Hòn Sụp... Dừng chụp ảnh tại các điểm view tự nhiên."},{"time":"11:30","title":"Kết thúc tour – Về Đà Nẵng","description":"Đoàn về lại trung tâm Đà Nẵng. HDV gợi ý nhà hàng ăn trưa phục hồi sức khỏe sau buổi trekking."}]'::json,
 '["Hướng dẫn viên trekking chuyên nghiệp am hiểu hệ sinh thái Sơn Trà","Gậy trekking (1 chiếc/người)","Bữa sáng nhẹ giữa rừng (bánh mì, hoa quả, nước uống)","Bảo hiểm du lịch trekking","Ống nhòm quan sát Voọc (dùng chung nhóm)"]'::json,
 '["Xe đưa đón (tự di chuyển đến điểm tập hợp)","Giày trekking và trang bị cá nhân (khuyên dùng giày có đế chống trơn)","Bữa ăn trưa sau tour","Tip cho hướng dẫn viên","Camera telephoto để chụp Voọc rõ nét (tự mang)"]'::json,
 '6 giờ (sáng sớm)', '05:30', 'Cổng vào bán đảo Sơn Trà (tự di chuyển hoặc đặt xe riêng)', 10::int, 2::int, 700000::numeric, 700000::numeric, 0::numeric),

-- ─────────────────────────────────────────────────────────────────────────────
-- Tour 14: Vườn Quốc Gia Bạch Mã
-- ─────────────────────────────────────────────────────────────────────────────
(14,
 'Tour Vườn Quốc Gia Bạch Mã – Chinh Phục Đỉnh Núi & Thác Đỗ Quyên',
 'Trekking rừng quốc gia Bạch Mã, chiêm ngưỡng thác Đỗ Quyên hùng vĩ và đứng trên đài vọng cảnh ngắm toàn cảnh Vịnh Lăng Cô từ đỉnh núi 1.450 m giữa rừng nguyên sinh.',
 'Vườn Quốc gia Bạch Mã nằm trên dãy Trường Sơn, ở ranh giới tỉnh Thừa Thiên Huế và tỉnh Quảng Nam, cách thành phố Huế khoảng 65 km và cách Đà Nẵng khoảng 70 km. Đây là vườn quốc gia đặc biệt nhất Việt Nam vì hội tụ đủ đặc điểm của cả hệ sinh thái rừng nhiệt đới và ôn đới, với lượng mưa cao nhất Việt Nam (8.000 mm/năm). Điểm cao nhất của Bạch Mã là đỉnh Hải Vọng Đài (1.450 m), từ đây có thể nhìn thấy toàn cảnh Vịnh Lăng Cô – một trong những vịnh đẹp nhất thế giới. Thác Đỗ Quyên – thác nước hùng vĩ cao 300 m nằm sâu trong rừng – là điểm nhấn không thể bỏ qua khi đến Bạch Mã. Vườn quốc gia là nơi trú ngụ của hàng nghìn loài động thực vật quý, trong đó có nhiều loài đặc hữu của dãy Trường Sơn.',
 '[{"time":"06:30","title":"Đón khách tại Đà Nẵng","description":"Xe đón khách sớm, di chuyển theo hướng Huế qua đèo Phú Gia và cầu Phú Lộc, vào địa phận huyện Phú Lộc để đến cổng Vườn Quốc gia Bạch Mã."},{"time":"08:30","title":"Cổng Vườn Quốc gia – Đăng ký và khởi đầu","description":"Check-in, mua vé và gặp gỡ hướng dẫn viên sinh thái chuyên tuyến Bạch Mã. HDV phổ biến quy tắc an toàn và bảo vệ thiên nhiên trong vườn quốc gia."},{"time":"09:00","title":"Trekking đến Thác Đỗ Quyên","description":"Đi bộ theo đường mòn rừng dày đặc, băng qua các suối nhỏ và cầu gỗ, len lỏi trong không gian rừng ẩm mát. Nghe tiếng chim và quan sát các loài thực vật đặc hữu. Đến thác Đỗ Quyên hùng vĩ, nghỉ ngơi và tắm mát trong làn nước suối trong lành mát lạnh."},{"time":"11:00","title":"Bữa trưa picnic giữa rừng","description":"Dừng tại điểm nghỉ giữa rừng, thưởng thức bữa trưa picnic được chuẩn bị sẵn: cơm hộp, gà luộc, rau xào và nước uống. Bữa ăn giữa thiên nhiên hoang dã của rừng quốc gia là trải nghiệm khó quên."},{"time":"12:00","title":"Leo lên Hải Vọng Đài (1.450 m)","description":"Tiếp tục leo lên đài vọng cảnh Hải Vọng Đài ở độ cao 1.450 m – điểm cao nhất có thể đến bằng đường mòn. Từ đây, tầm nhìn 360 độ bao phủ Vịnh Lăng Cô, biển Đông, đồng bằng Huế và dãy núi Trường Sơn hùng vĩ."},{"time":"13:30","title":"Xuống núi – Khám phá đường về","description":"Đi theo tuyến đường khác khi xuống núi, ngang qua các vạt rừng nguyên sinh, vườn hoa đỗ quyên (mùa xuân) và suối nước mát."},{"time":"15:00","title":"Lên xe – Trở về Đà Nẵng","description":"Lên xe trở về Đà Nẵng theo tuyến đường Huế."},{"time":"17:30","title":"Trả khách tại Đà Nẵng – Kết thúc tour","description":"Về đến điểm hẹn ban đầu. Kết thúc hành trình chinh phục Bạch Mã đáng tự hào."}]'::json,
 '["Xe du lịch đưa đón tại Đà Nẵng","Hướng dẫn viên sinh thái chuyên tuyến Bạch Mã","Vé vào cổng Vườn Quốc gia Bạch Mã","Bữa trưa picnic trong rừng","Nước uống (2 chai/người)","Bảo hiểm trekking"]'::json,
 '["Giày trekking chuyên dụng và trang bị cá nhân","Thuốc chống côn trùng và kem chống nắng","Mưa áo (rừng Bạch Mã hay có mưa bất chợt)","Tip cho hướng dẫn viên và tài xế","Vé xem bộ sưu tập mẫu vật thiên nhiên (tự nguyện)"]'::json,
 '11 giờ (trọn ngày)', '06:30', 'Trung tâm Đà Nẵng (đón tận khách sạn)', 15::int, 2::int, 1100000::numeric, 850000::numeric, 200000::numeric),

-- ─────────────────────────────────────────────────────────────────────────────
-- Tour 15: Street Food Tour Đà Nẵng bằng Xe Máy
-- ─────────────────────────────────────────────────────────────────────────────
(15,
 'Street Food Tour Đà Nẵng bằng Xe Máy – Ăn Đêm Như Người Bản Địa',
 'Ngồi sau xe máy cùng hướng dẫn viên địa phương xuyên qua các con hẻm, thưởng thức 6–7 món ăn đêm đặc sản Đà Nẵng được người dân yêu thích nhất.',
 'Street food tour xe máy là cách khám phá ẩm thực Đà Nẵng chân thực và thú vị nhất: thay vì đến nhà hàng du lịch, bạn sẽ ngồi sau xe của một người dân bản địa thực sự, cùng len lỏi vào những góc phố, hẻm nhỏ, quán vỉa hè nơi người Đà Nẵng ăn uống mỗi ngày. Tour bắt đầu lúc 18:00 khi màn đêm buông xuống và phố xá Đà Nẵng bước vào giờ cao điểm ẩm thực đường phố. Bạn sẽ được thưởng thức 6–7 món đặc sản của Đà Nẵng tại các địa điểm khác nhau: mì Quảng cá lóc, bánh xèo Đà Nẵng – to và giòn rụm khác hẳn bánh xèo Sài Gòn, nem lụi nướng trên than, bê thui Cầu Mống chấm mắm nêm Nam Ô, bánh tráng cuốn thịt heo trứ danh, chè bắp sữa dừa và kết thúc bằng cà phê trứng truyền thống hoặc bia hơi Đà Nẵng. Mỗi điểm dừng là một câu chuyện: hướng dẫn viên sẽ kể về lịch sử và văn hóa đằng sau mỗi món ăn, về cuộc sống người Đà Nẵng và phong tục địa phương.',
 '[{"time":"17:30","title":"Tập hợp tại khách sạn – Giới thiệu lái xe","description":"Hướng dẫn viên và đội lái xe xe máy đến đón tại khách sạn. Gặp gỡ người lái xe của mình (mỗi du khách 1 xe), kiểm tra mũ bảo hiểm và khởi động chuyến đi."},{"time":"18:00","title":"Mì Quảng & Bún Chả Cá – Điểm 1","description":"Điểm đầu tiên: quán mì Quảng hàng chục năm tuổi do gia đình người dân địa phương mở. Thưởng thức bát mì Quảng cá lóc với nước dùng đặc sánh, bánh tráng nướng giòn và rau thơm tươi. Hướng dẫn viên giải thích sự khác biệt của mì Quảng so với phở và bún bò."},{"time":"18:30","title":"Bánh Xèo Đà Nẵng – Điểm 2","description":"Đến quán bánh xèo nổi tiếng trong hẻm – chiếc bánh xèo Đà Nẵng cỡ lớn, vàng giòn, nhân tôm thịt và giá đỗ. Cuốn bánh cùng rau sống, chấm nước mắm pha chua ngọt. Cảnh xèo bánh trên chảo gang to và tiếng xèo xèo hấp dẫn sẽ kích thích mọi giác quan."},{"time":"19:00","title":"Nem Lụi & Bê Thui Cầu Mống – Điểm 3","description":"Điểm thứ ba: nem lụi nướng trên bếp than và bê thui Cầu Mống – hai đặc sản gắn với vùng đất Đà Nẵng và Quảng Nam. Chấm cùng mắm nêm Nam Ô – loại mắm đặc biệt chỉ có ở Đà Nẵng với hương vị đậm đà không lẫn đâu được."},{"time":"19:30","title":"Bánh Tráng Cuốn Thịt Heo – Điểm 4","description":"Thưởng thức bánh tráng cuốn thịt heo – món ăn mà người Đà Nẵng tự hào nhất: thịt heo luộc thái mỏng, cuốn cùng rau thơm đủ loại, chuối xanh, khế chua và dưa cải trong bánh tráng mỏng, chấm mắm nêm pha tỏi ớt cay. Đây là hương vị không thể quên của Đà Nẵng."},{"time":"20:00","title":"Chè Bắp & Giải Khát – Điểm 5","description":"Đến quán chè bắp sữa dừa trên đường Bạch Đằng, thư giãn nhìn sông Hàn về đêm. Chè bắp Hội An – sữa dừa thơm béo, hạt bắp ngọt mềm, ăn vào mùa hè thấy mát dịu từ trong ra ngoài."},{"time":"20:30","title":"Cà Phê Trứng & Bia Hơi – Điểm 6 (Kết thúc)","description":"Điểm kết thúc: cà phê trứng Đà Nẵng hoặc bia hơi Đà Nẵng tươi mát tại quán vỉa hè quen thuộc của người bản địa. HDV kể thêm những câu chuyện cuộc sống Đà Nẵng và hỏi bạn muốn khám phá gì thêm vào những ngày tới."},{"time":"21:00","title":"Trả về khách sạn – Kết thúc tour","description":"Lái xe đưa bạn về tận khách sạn. Kết thúc đêm ăn uống như người Đà Nẵng thực sự."}]'::json,
 '["Xe máy và lái xe địa phương am hiểu ẩm thực Đà Nẵng (1 xe/1 khách)","Mũ bảo hiểm đạt chuẩn","Tất cả các món ăn và đồ uống trong lịch trình (6–7 điểm dừng)","Hướng dẫn viên tour trưởng","Bảo hiểm du lịch cơ bản"]'::json,
 '["Đồ uống thêm ngoài chương trình (bia, cocktail)","Tip cho lái xe và hướng dẫn viên (tự nguyện, khoảng 50.000–100.000 đ/người)","Các điểm mua sắm thêm","Thuốc dạ dày nếu không quen ăn nhiều"]'::json,
 '3,5 giờ (tối)', '17:30', 'Khách sạn của bạn tại trung tâm Đà Nẵng (đón tận nơi)', 10::int, 1::int, 650000::numeric, 650000::numeric, 0::numeric),

-- ─────────────────────────────────────────────────────────────────────────────
-- Tour 16: Làm Nông Dân Làng Rau Trà Quế
-- ─────────────────────────────────────────────────────────────────────────────
(16,
 'Tour Làm Nông Dân Một Ngày – Làng Rau Trà Quế Hội An',
 'Trải nghiệm cuộc sống nông dân đích thực tại làng rau hữu cơ Trà Quế: tự tay xới đất, gieo hạt, tưới rau và chế biến bữa ăn từ rau sạch do chính mình trồng.',
 'Làng rau Trà Quế là ngôi làng nông nghiệp truyền thống nằm cách trung tâm Hội An khoảng 3 km, nổi tiếng từ hàng trăm năm nay với nghề trồng rau hữu cơ không sử dụng phân bón hóa học. Đất ở Trà Quế được cải tạo bằng phân rong biển từ sông Đế Võng, tạo nên chất đất đặc biệt giúp rau thơm ngon hơn bất kỳ nơi nào khác. Các loại rau đặc trưng của làng Trà Quế như húng quế, tía tô, bạc hà, hành lá và các loại rau thơm được dùng trong mì Quảng, cao lầu và phở chua Hội An – thiếu rau Trà Quế thì các món ăn này mất đi hương vị đặc trưng. Tour này cho phép du khách trở thành nông dân thực sự trong nửa ngày: học cách dùng cào, cuốc xới đất; trồng và tưới rau; thu hoạch rau tươi; sau đó vào bếp cùng đầu bếp địa phương chế biến bữa trưa từ chính những gì mình vừa thu hái.',
 '[{"time":"08:00","title":"Đón khách – Khởi hành đến Trà Quế","description":"Xe đưa đoàn hoặc du khách tự đến làng Trà Quế bằng xe đạp hoặc xe máy (HDV gợi ý tuyến đường đẹp). Đến nơi, mặc áo nông dân truyền thống và đội nón lá."},{"time":"08:30","title":"Học xới đất và gieo hạt","description":"Người nông dân Trà Quế hướng dẫn cách xới đất bằng cào truyền thống, làm đất tơi xốp và gieo hạt rau đúng kỹ thuật. Cảm nhận sự vất vả và niềm vui của người làm nông khi tận tay gieo những hạt mầm."},{"time":"09:30","title":"Tưới nước & Chăm sóc luống rau","description":"Học cách tưới nước đúng lượng, phát hiện sâu bệnh và nhổ cỏ dại. Người nông dân bản địa giải thích tại sao rau Trà Quế ngon và đặc biệt, cách trồng hữu cơ không dùng phân hóa học."},{"time":"10:30","title":"Thu hoạch rau và nguyên liệu nấu ăn","description":"Cùng thu hoạch rau tươi, hái lá thơm và chuẩn bị nguyên liệu cho bữa ăn trưa. Cảm giác tự tay hái rau để ăn là trải nghiệm khác hoàn toàn so với mua tại chợ."},{"time":"11:00","title":"Vào bếp – Chế biến bữa ăn từ rau Trà Quế","description":"Cùng đầu bếp địa phương học cách làm các món ăn truyền thống Hội An từ nguyên liệu vừa thu hoạch: bánh đúc rau thơm, gỏi cuốn rau sống, xào rau trứng hoặc cơm rang rau. Khám phá bí quyết pha nước chấm mắm nêm đặc trưng Hội An."},{"time":"12:00","title":"Bữa ăn gia đình – Thưởng thức thành quả","description":"Ngồi ăn cùng gia đình chủ nhà trong không gian vườn rau xanh mướt. Thưởng thức những món ăn do chính tay mình làm – ngon nhất vì có mồ hôi và tình cảm bỏ vào."},{"time":"13:00","title":"Tự do tham quan làng & Về lại Hội An","description":"Tự do dạo bộ trong làng, chụp ảnh, mua rau sạch Trà Quế mang về. Xe trả khách tại Hội An hoặc Đà Nẵng theo yêu cầu."}]'::json,
 '["Hướng dẫn viên nông nghiệp địa phương","Trang phục nông dân truyền thống (áo và nón lá)","Dụng cụ làm vườn: cào, cuốc, bình tưới","Nguyên liệu nấu ăn từ rau Trà Quế","Bữa ăn trưa gia đình tự nấu","Nước uống","Vé tham quan làng Trà Quế"]'::json,
 '["Xe đưa đón từ Đà Nẵng (báo trước để sắp xếp)","Mua rau sạch Trà Quế mang về","Tip cho người nông dân hướng dẫn","Đồ uống thêm"]'::json,
 '5 giờ (buổi sáng)', '08:00', 'Làng rau Trà Quế, Hội An (có thể đón tại trung tâm Hội An hoặc Đà Nẵng)', 12::int, 1::int, 500000::numeric, 350000::numeric, 100000::numeric),

-- ─────────────────────────────────────────────────────────────────────────────
-- Tour 17: Du Thuyền Sông Hàn & Xem Rồng Phun Lửa
-- ─────────────────────────────────────────────────────────────────────────────
(17,
 'Tour Du Thuyền Sông Hàn – Ngắm Cầu Rồng Phun Lửa Cuối Tuần',
 'Buổi tối lãng mạn trên dòng sông Hàn: ngắm nhìn Đà Nẵng về đêm từ mặt nước, xem màn trình diễn Cầu Rồng phun lửa và phun nước ngoạn mục vào mỗi thứ 7 và Chủ nhật.',
 'Sông Hàn là con sông chảy qua trung tâm thành phố Đà Nẵng, chia đôi thành phố thành hai khu vực Đông và Tây. Bờ sông Hàn về đêm là điểm tản bộ, hẹn hò và vui chơi yêu thích của cả người dân địa phương lẫn du khách. Hệ thống cầu bắc qua sông Hàn là đặc điểm nhận diện của Đà Nẵng: Cầu Rồng (Dragon Bridge – 666 m, hình con rồng Việt bay ra biển), Cầu Sông Hàn (cầu quay đầu tiên của Việt Nam), Cầu Nguyễn Văn Trỗi, Cầu Thuận Phước (cầu dây văng dài nhất Việt Nam)... Mỗi cuối tuần (thứ 7 và Chủ nhật) lúc 21:00, Cầu Rồng phun lửa và phun nước trong 15 phút – màn trình diễn ngoạn mục thu hút hàng vạn người. Du thuyền trên sông Hàn là cách tuyệt vời nhất để ngắm nhìn toàn bộ cảnh quan ánh đèn Đà Nẵng từ giữa lòng sông, với góc nhìn khác hoàn toàn so với bờ.',
 '[{"time":"19:00","title":"Tập hợp tại bến tàu Bạch Đằng","description":"Đến bến tàu du lịch Bạch Đằng, lên thuyền được bài trí đèn trang trí và có chỗ ngồi rộng rãi. HDV giới thiệu các cây cầu nổi bật và các điểm nhìn đẹp khi đi thuyền."},{"time":"19:15","title":"Khởi hành – Du thuyền ngắm Đà Nẵng về đêm","description":"Thuyền từ từ rời bến, bắt đầu hành trình trên mặt sông Hàn lung linh ánh đèn. Ngắm nhìn các cây cầu thắp sáng đẹp mắt phản chiếu xuống mặt nước: Cầu Sông Hàn xanh lam, Cầu Nguyễn Văn Trỗi cổ điển, Cầu Thuận Phước dây văng trắng muốt."},{"time":"19:45","title":"Dừng ngắm Cầu Rồng – Chụp ảnh","description":"Thuyền dừng lại ở vị trí đẹp nhất để chiêm ngưỡng Cầu Rồng được chiếu sáng. Đây là điểm chụp ảnh toàn cảnh Cầu Rồng nổi tiếng nhất, góc chụp từ mặt sông cho thấy toàn bộ hình dáng con rồng bay."},{"time":"20:00","title":"Thưởng thức nước uống – Ngắm thành phố","description":"Trên thuyền có phục vụ nước uống (bao gồm trong giá tour). Tận hưởng gió sông mát mẻ, ngắm nhìn đường chân trời Đà Nẵng lấp lánh ánh đèn từ các tòa nhà, khách sạn và resort ven sông."},{"time":"21:00","title":"Cầu Rồng Phun Lửa & Phun Nước (Cuối tuần)","description":"Vào 21:00 thứ 7 và Chủ nhật: màn trình diễn Cầu Rồng phun lửa và phun nước kéo dài 15 phút. Thuyền định vị tại vị trí đẹp nhất để du khách xem toàn bộ màn trình diễn. Đây là khoảnh khắc đỉnh cao của tour – lửa và nước bắn lên bầu trời đêm, ánh sáng phản chiếu trên mặt sông, tiếng hò reo của hàng vạn người trên bờ."},{"time":"21:20","title":"Trở về bến – Kết thúc tour","description":"Thuyền trở về bến Bạch Đằng. Kết thúc 2 giờ đêm lãng mạn trên sông Hàn."}]'::json,
 '["Vé du thuyền sông Hàn (chỗ ngồi trong thuyền, có mái che)","Nước uống trên thuyền (1 chai/người)","Hướng dẫn thông tin các cây cầu","Bảo hiểm trên sông"]'::json,
 '["Bữa ăn tối trên thuyền (có thể đặt riêng)","Đồ uống thêm (bia, cocktail)","Chương trình âm nhạc sống trên thuyền (có một số thuyền phục vụ)","Tip cho thuyền viên"]'::json,
 '2 giờ (tối)', '19:30', 'Bến tàu du lịch Bạch Đằng, Đà Nẵng', 80::int, 1::int, 200000::numeric, 150000::numeric, 50000::numeric),

-- ─────────────────────────────────────────────────────────────────────────────
-- Tour 18: Đầm Phá Tam Giang & Sunset
-- ─────────────────────────────────────────────────────────────────────────────
(18,
 'Tour Đầm Phá Tam Giang – Chèo Kayak & Hoàng Hôn Huyền Ảo',
 'Khám phá hệ sinh thái đầm phá nước lợ lớn nhất Đông Nam Á – Phá Tam Giang: chèo kayak giữa đồng lúa nước, ngắm hoàng hôn rực lửa và thưởng thức hải sản tươi đầm phá.',
 'Phá Tam Giang – Cầu Hai là hệ thống đầm phá nước lợ lớn nhất Đông Nam Á, trải dài hơn 68 km qua các huyện Phong Điền, Quảng Điền, Hương Trà và Phú Vang của tỉnh Thừa Thiên Huế, cách thành phố Huế khoảng 15 km và cách Đà Nẵng khoảng 60 km. Đây là hệ sinh thái đất ngập nước độc đáo với diện tích khoảng 22.000 ha, là nơi sinh sống của hàng trăm loài thủy sản đặc hữu và là nguồn mưu sinh chính của hàng chục nghìn hộ ngư dân ven đầm. Buổi chiều – hoàng hôn tại Phá Tam Giang là thời điểm đẹp huyền ảo: mặt trời đỏ rực chìm dần xuống sau dãy núi, ánh đỏ hồng phản chiếu trên mặt nước yên lặng của đầm phá, tiếng sóng nhẹ và tiếng chim trời xa xa tạo nên khung cảnh thiên nhiên tĩnh mịch khó quên. Tour kết hợp chèo kayak giữa đồng lúa nước, ngắm hoàng hôn và ăn tối hải sản đầm phá.',
 '[{"time":"14:00","title":"Đón khách tại Huế hoặc Đà Nẵng","description":"Xe đón khách, khởi hành đến vùng đầm phá Tam Giang – Cầu Hai. Trên đường, HDV giới thiệu về hệ sinh thái đặc biệt này và cuộc sống của ngư dân đầm phá."},{"time":"15:30","title":"Đến bến thuyền – Trải nghiệm chèo Kayak","description":"Đến bến thuyền của làng chài ven đầm phá. Mặc áo phao, nhận bài hướng dẫn chèo Kayak cơ bản và bắt đầu ra đầm. Len lỏi qua các lối nhỏ giữa đồng lúa nước, ruộng sen và bãi cỏ lau, quan sát cuộc sống ngư dân đánh cá trên đầm phá."},{"time":"17:00","title":"Ngắm hoàng hôn Phá Tam Giang","description":"Dừng kayak và đứng trên bè nổi để chờ đón hoàng hôn. Khoảng 17:30–18:00, mặt trời bắt đầu chìm xuống phía Tây, ánh hoàng hôn nhuộm đỏ cả vùng đầm phá. Đây là một trong những hoàng hôn đẹp nhất miền Trung – nơi ánh sáng cuối ngày gặp gỡ mặt nước phẳng lặng của đầm phá tạo nên bức tranh thiên nhiên tuyệt tác."},{"time":"18:30","title":"Bữa tối hải sản đầm phá – Tươi từ đầm","description":"Thưởng thức bữa tối hải sản tươi do ngư dân đầm phá đánh bắt trong ngày: tôm sú hấp, cá mú nướng, nghêu luộc sả, ốc đầm hấp gừng và rau cải xào tỏi. Ngồi ăn trên bè nổi giữa đầm phá với không khí trong lành và hương vị hải sản không thể tươi hơn."},{"time":"20:00","title":"Lên xe – Trở về","description":"Về lại bờ, lên xe trở về Huế hoặc Đà Nẵng."},{"time":"21:30","title":"Trả khách – Kết thúc tour","description":"Về đến điểm hẹn ban đầu. Kết thúc hành trình đầm phá Tam Giang huyền diệu."}]'::json,
 '["Xe đưa đón tại Huế hoặc Đà Nẵng","Hướng dẫn viên thuyền chèo địa phương","Thuyền Kayak đôi (2 người/1 thuyền) và áo phao","Thuyền tham quan đầm phá (tàu nhỏ địa phương)","Bữa tối hải sản đầm phá (5–6 món chính)","Nước uống","Bảo hiểm trên nước"]'::json,
 '["Đồ uống trong bữa tối","Chi phí cá nhân","Tip cho ngư dân và hướng dẫn viên"]'::json,
 '7,5 giờ (chiều – tối)', '14:00', 'Huế hoặc Đà Nẵng (đón tận khách sạn)', 20::int, 2::int, 750000::numeric, 550000::numeric, 150000::numeric),

-- ─────────────────────────────────────────────────────────────────────────────
-- Tour 19: Ca Huế Trên Sông Hương & Ngắm Thành Phố
-- ─────────────────────────────────────────────────────────────────────────────
(19,
 'Tour Ca Huế Trên Sông Hương – Di Sản Phi Vật Thể',
 'Ngồi trên thuyền rồng trôi dọc sông Hương thơ mộng, thưởng thức Ca Huế – di sản phi vật thể quốc gia – và thả đèn hoa đăng cầu may dưới ánh trăng cố đô.',
 'Ca Huế là loại hình âm nhạc truyền thống ra đời và phát triển tại cố đô Huế, được UNESCO công nhận là Di sản Văn hóa Phi vật thể Quốc gia Việt Nam. Ca Huế bao gồm hai dòng nhạc chính: nhạc cung đình (nhã nhạc – đã được UNESCO công nhận là Di sản Thế giới năm 2003) và nhạc dân gian (ca Huế trên sông Hương). Ca Huế thính phòng thường được biểu diễn trên những chiếc thuyền rồng êm ái trôi dọc sông Hương lúc đêm khuya, với các nhạc cụ truyền thống: đàn tranh, đàn nguyệt, đàn bầu, đàn nhị, trống và sáo trúc. Sông Hương (sông Thơm) là con sông chạy qua trung tâm Huế, được ví như "tâm hồn" của cố đô với hai bờ sông cây cối xanh mướt, kiến trúc cổ kính và không gian thanh bình hiếm thấy. Buổi tối trên sông Hương nghe Ca Huế là trải nghiệm văn hóa sâu sắc nhất mà bất kỳ ai đến Huế đều nên có.',
 '[{"time":"18:30","title":"Tập hợp tại bến Tòa Khâm – Huế","description":"Đến bến thuyền du lịch tại Toà Khâm, Huế. HDV giới thiệu lịch sử Ca Huế và các nhạc cụ truyền thống sẽ được biểu diễn trong đêm."},{"time":"19:00","title":"Lên thuyền rồng – Khởi hành trên Sông Hương","description":"Lên thuyền rồng được trang trí đèn lồng rực rỡ, bắt đầu hành trình trôi dọc sông Hương thơ mộng. Nhạc cụ truyền thống đã sẵn sàng trên thuyền."},{"time":"19:15","title":"Biểu diễn Ca Huế – Âm Nhạc Di Sản","description":"Đoàn nhạc công và ca sĩ Huế biểu diễn các làn điệu Ca Huế đặc trưng: điệu nam ai, nam bình, tứ đại cảnh, hò mái nhì... Tiếng đàn tranh réo rắt, giọng ca ngân nga và ánh đèn lồng phản chiếu trên mặt sông tạo nên không gian văn hóa huyền ảo của cố đô."},{"time":"20:00","title":"Thả đèn hoa đăng – Cầu bình an","description":"Mỗi du khách nhận một bông hoa đăng. Cùng thắp nến và thả hoa đăng xuống sông Hương, gửi gắm ước nguyện và lời cầu bình an. Trăm ngọn hoa đăng nhỏ lung linh trôi theo dòng sông Hương về phía biển."},{"time":"20:30","title":"Trở về bến – Kết thúc tour","description":"Thuyền cập bến Tòa Khâm. Kết thúc buổi tối trên sông Hương đầy cảm xúc văn hóa và nghệ thuật."}]'::json,
 '["Thuyền rồng và thuyền viên","Đoàn nhạc công và ca sĩ Ca Huế chuyên nghiệp","Hoa đăng thả sông Hương (1 cái/người)","Nước uống trên thuyền","Bảo hiểm trên sông"]'::json,
 '["Bữa ăn tối (tour kết thúc 20:30, bạn tự do ăn tối)","Đồ uống thêm","Chi phí cá nhân","Tip cho nhạc công và thuyền viên"]'::json,
 '2 giờ (tối)', '19:00', 'Bến Tòa Khâm, bờ sông Hương, Thành phố Huế', 30::int, 1::int, 150000::numeric, 100000::numeric, 0::numeric),

-- ─────────────────────────────────────────────────────────────────────────────
-- Tour 20: Snorkeling Bán Đảo Sơn Trà
-- ─────────────────────────────────────────────────────────────────────────────
(20,
 'Tour Snorkeling Sơn Trà – Lặn Ngắm San Hô Ngay Tại Đà Nẵng',
 'Đi tàu gỗ ra các hòn đảo nhỏ quanh bán đảo Sơn Trà, lặn ngắm san hô đa sắc ngay gần bờ và câu cá thưởng thức giữa vùng biển trong xanh của Đà Nẵng.',
 'Bán đảo Sơn Trà không chỉ nổi tiếng với rừng xanh và Chùa Linh Ứng mà còn có vùng biển quanh đảo cực kỳ trong sạch, với hệ sinh thái san hô còn tương đối nguyên vẹn gần bờ. Các điểm lặn ngắm san hô xung quanh bán đảo Sơn Trà như Bãi Bắc, Mũi Nghê, Hòn Sụp... cách Cảng Tiên Sa chỉ 10–20 phút đi tàu, phù hợp cho các chuyến lặn nửa ngày. Độ trong của nước biển Sơn Trà đạt 5–10 m trong điều kiện thời tiết đẹp, đủ để thấy rõ san hô và cá biển sặc sỡ mà không cần phải ra xa bờ. Tour này sử dụng tàu gỗ truyền thống của ngư dân địa phương, tạo nên không khí mộc mạc và gần gũi hơn so với tour tàu hiện đại. Trên tàu có bữa trưa hải sản tươi được nấu ngay sau khi đánh bắt – đây là điểm đặc biệt mà các tour lặn biển khác không có.',
 '[{"time":"08:00","title":"Tập hợp tại Cảng Tiên Sa","description":"Đến cảng Tiên Sa, lên tàu gỗ truyền thống được trang bị đủ thiết bị an toàn. HDV phổ biến quy tắc an toàn trên tàu và hướng dẫn sử dụng kính lặn, ống thở."},{"time":"08:30","title":"Ra khơi – Đến điểm lặn san hô","description":"Tàu rời cảng, đi dọc theo cung biển đẹp của bán đảo Sơn Trà. Khoảng 20–30 phút đến điểm lặn san hô được chọn dựa theo điều kiện sóng và thời tiết trong ngày."},{"time":"09:00","title":"Lặn ngắm san hô – Snorkeling","description":"Mang kính lặn và ống thở, nhảy xuống biển trong xanh. Ngắm nhìn thế giới đại dương phong phú: san hô cứng, san hô mềm, cá hề nemo, cá chim, cá mú, cầu gai và các loài sinh vật biển đa sắc. Hướng dẫn viên lặn hỗ trợ những người chưa có kinh nghiệm."},{"time":"10:30","title":"Câu cá thư giãn – Trải nghiệm ngư dân","description":"Trở lên tàu, thư giãn và thử câu cá cùng ngư dân địa phương. Học cách buộc mồi, thả cần và kiên nhẫn chờ đợi – một trong những trải nghiệm yên bình nhất trên mặt biển."},{"time":"11:30","title":"Nấu ăn trên tàu – Bữa trưa hải sản tươi","description":"Hải sản vừa câu được hoặc mua tươi từ ngư dân khác sẽ được nấu ngay trên tàu: cá nướng than hoa, mực xào cay, cà chua nhồi tôm và cơm trắng. Ăn giữa biển xanh với gió mát là trải nghiệm độc đáo nhất của tour này."},{"time":"13:00","title":"Tắm biển tự do – Nghỉ ngơi","description":"Tự do nhảy xuống biển tắm, thư giãn, ngồi trên boong tàu đón nắng hoặc chợp mắt trong gió biển."},{"time":"14:00","title":"Trở về Cảng Tiên Sa – Kết thúc tour","description":"Tàu quay về cảng. Xe đưa đoàn về trung tâm Đà Nẵng."},{"time":"15:00","title":"Trả khách – Kết thúc tour","description":"Về đến điểm hẹn. Kết thúc buổi lặn biển Sơn Trà đáng nhớ."}]'::json,
 '["Tàu gỗ truyền thống khứ hồi từ Cảng Tiên Sa","Hướng dẫn viên lặn và thuyền viên","Bộ kính lặn và ống thở (snorkel) cho mỗi người","Áo phao bảo hiểm","Bữa trưa hải sản tươi nấu trên tàu (4–5 món)","Dụng cụ câu cá","Nước uống","Bảo hiểm trên biển"]'::json,
 '["Dịch vụ tắm nước ngọt trên tàu (tự mang khăn tắm)","Lặn bình khí scuba (tính phí riêng)","Đồ uống bia và nước có ga","Chi phí cá nhân","Tip cho ngư dân và HDV"]'::json,
 '7 giờ (buổi sáng – chiều)', '08:00', 'Cảng Tiên Sa, bán đảo Sơn Trà, Đà Nẵng', 25::int, 4::int, 600000::numeric, 450000::numeric, 100000::numeric)

)
UPDATE tours t
SET
    name            = tcf.name,
    short_desc      = tcf.short_desc,
    description     = tcf.description,
    itinerary       = tcf.itinerary,
    inclusions      = tcf.inclusions,
    exclusions      = tcf.exclusions,
    duration        = tcf.duration,
    start_time      = tcf.start_time,
    meeting_point   = tcf.meeting_point,
    max_people      = tcf.max_people,
    min_people      = tcf.min_people,
    price_adult     = tcf.price_adult,
    price_child     = tcf.price_child,
    price_infant    = tcf.price_infant,
    updated_at      = NOW()
FROM tour_core_fix tcf
WHERE t.id = tcf.id;

-- ============================================================
-- SECTION 2: Tours 21–100 (auto-generated variants)
--   Fix: propagate itinerary, inclusions, exclusions from parent (tours 1–20)
--   Fix: also propagate start_time and meeting_point
--   Fix: add differentiated short_desc based on variant prefix
-- ============================================================

UPDATE tours t
SET
    itinerary     = COALESCE(NULLIF(t.itinerary::text, '[]'), p.itinerary::text)::json,
    inclusions    = COALESCE(NULLIF(t.inclusions::text, '[]'), p.inclusions::text)::json,
    exclusions    = COALESCE(NULLIF(t.exclusions::text, '[]'), p.exclusions::text)::json,
    start_time    = COALESCE(NULLIF(t.start_time, ''), p.start_time),
    meeting_point = COALESCE(NULLIF(t.meeting_point, ''), p.meeting_point),
    duration      = COALESCE(NULLIF(t.duration, ''), p.duration),
    description   = CASE
        WHEN t.description IS NULL OR t.description = '' THEN p.description
        WHEN t.description NOT LIKE '%Trải nghiệm%' THEN p.description
        ELSE t.description
    END,
    short_desc    = CASE
        WHEN t.name LIKE 'Tour Cao Cap%' THEN
            'Phiên bản cao cấp, dịch vụ 5 sao: ' || p.short_desc
        WHEN t.name LIKE 'Tour Tiet Kiem%' THEN
            'Gói tiết kiệm linh hoạt, phù hợp ngân sách: ' || p.short_desc
        ELSE
            'Gói khám phá chuyên sâu, hướng dẫn viên riêng: ' || p.short_desc
    END,
    updated_at    = NOW()
FROM tours p
WHERE t.id BETWEEN 21 AND 100
  AND p.id = ((t.id % 20) + 1)  -- maps 21→2, 22→3, ..., 40→1, 41→2, ...
  AND (
       t.itinerary IS NULL
    OR t.itinerary::text = '[]'
    OR t.inclusions IS NULL
    OR t.inclusions::text = '[]'
    OR t.start_time IS NULL
    OR t.start_time = ''
  );

-- ============================================================
-- SECTION 3: Verified real tours (file 49 imports)
--   Fix: price_child = 0 → 70% of adult price (rounded to nearest 50k)
--   Fix: price_infant = 0 → free (0) – standard practice in Vietnam
--   Fix: start_time = NULL → infer from tour name/category
-- ============================================================

-- 3a. Fix price_child for verified tours that currently have it = 0
UPDATE tours
SET
    price_child  = ROUND(price_adult * 0.70 / 50000) * 50000,
    updated_at   = NOW()
WHERE status IN ('active', 'pending_review')
  AND id > 100
  AND (price_child IS NULL OR price_child = 0)
  AND price_adult > 0;

-- 3b. Fix price_infant for verified tours (stay 0 – industry standard under 2 yrs)
--     But set a nominal value so it's explicit, not "missing"
UPDATE tours
SET
    price_infant = 0,
    updated_at   = NOW()
WHERE status IN ('active', 'pending_review')
  AND id > 100
  AND price_infant IS NULL;

-- 3c. Fix start_time for verified real tours based on tour category slug
UPDATE tours t
SET
    start_time = CASE
        -- Night / evening tours
        WHEN t.name ILIKE '%night%' OR t.name ILIKE '%evening%' OR t.name ILIKE '%sunset%'
            THEN '14:00'
        -- Port / cruise-ship tours (usually morning pickup at port)
        WHEN t.name ILIKE '%tien sa port%' OR t.name ILIKE '%chan may port%'
            THEN '08:00'
        -- Hoi An evening tours
        WHEN tc.slug = 'tour-hoi-an' AND t.name ILIKE '%night%'
            THEN '15:00'
        -- Train tours (departure by train time)
        WHEN tc.slug = 'tour-train-hue'
            THEN '07:00'
        -- Half-day morning tours
        WHEN t.duration ILIKE '%hour%' AND CAST(SPLIT_PART(t.duration, ' ', 1) AS NUMERIC) <= 5
            THEN '08:00'
        -- Default full-day morning departure
        ELSE '08:00'
    END,
    updated_at = NOW()
FROM tour_categories tc
WHERE t.tour_category_id = tc.id
  AND t.id > 100
  AND (t.start_time IS NULL OR t.start_time = '');

-- ============================================================
-- SECTION 4: Sync tour_schedules price_child / price_infant
--   where schedules still have 0 pricing after tour fix
-- ============================================================
UPDATE tour_schedules ts
SET
    price_child  = t.price_child,
    price_infant = t.price_infant,
    updated_at   = NOW()
FROM tours t
WHERE ts.tour_id = t.id
  AND (
       (ts.price_child IS NULL OR ts.price_child = 0)
    OR (ts.price_infant IS NULL)
  )
  AND t.price_child > 0;

-- ============================================================
-- SECTION 5: Normalize duration strings for consistency
-- ============================================================

-- Verified tour durations use English ("6 Hours", "1 Day") – normalize to Vietnamese
UPDATE tours
SET
    duration = CASE
        WHEN duration ILIKE '1 day'   THEN '1 ngày'
        WHEN duration ILIKE '2 day%'  THEN '2 ngày'
        WHEN duration ILIKE '3 day%'  THEN '3 ngày'
        WHEN duration ILIKE '0.5 day' THEN 'nửa ngày'
        WHEN duration ILIKE '4 hour%' THEN '4 giờ'
        WHEN duration ILIKE '5 hour%' THEN '5 giờ'
        WHEN duration ILIKE '6 hour%' THEN '6 giờ'
        WHEN duration ILIKE '7 hour%' THEN '7 giờ'
        WHEN duration ILIKE '7.5 hour%' THEN '7,5 giờ'
        WHEN duration ILIKE '8 hour%' THEN '8 giờ'
        WHEN duration ILIKE '8.5 hour%' THEN '8,5 giờ'
        WHEN duration ILIKE '9 hour%' THEN '9 giờ'
        WHEN duration ILIKE '10 hour%' THEN '10 giờ'
        WHEN duration ILIKE '11 hour%' THEN '11 giờ'
        WHEN duration ILIKE '12 hour%' THEN '12 giờ'
        WHEN duration ILIKE '%full day%' THEN '1 ngày'
        ELSE duration
    END,
    updated_at = NOW()
WHERE id > 100
  AND duration IS NOT NULL
  AND duration ~ '^[0-9]';

-- ============================================================
-- SECTION 6: Enrich verified tour descriptions that are still template-only
--   Template pattern: "Chương trình tham quan Da Nang, Hoi An, Hue..."
--   Append the itinerary summary as additional context for chatbot retrieval.
-- ============================================================

UPDATE tours
SET
    description = description ||
        E'\n\nLịch trình chi tiết:\n' ||
        REPLACE(
            REPLACE(
                REPLACE(itinerary::text, '[', ''),
                ']', ''
            ),
            '","', E'\n- '
        ),
    updated_at = NOW()
WHERE id > 100
  AND description ILIKE 'Chương trình tham quan%'
  AND itinerary IS NOT NULL
  AND itinerary::text <> '[]'
  AND itinerary::text <> 'null'
  AND LENGTH(description) < 800;  -- only enrich if still short

-- ============================================================
-- Safety: reset sequences to avoid PK conflicts
-- ============================================================
SELECT setval(pg_get_serial_sequence('tours', 'id'),
    GREATEST((SELECT COALESCE(MAX(id), 1) FROM tours), 1), true);
SELECT setval(pg_get_serial_sequence('tour_schedules', 'id'),
    GREATEST((SELECT COALESCE(MAX(id), 1) FROM tour_schedules), 1), true);

COMMIT;
