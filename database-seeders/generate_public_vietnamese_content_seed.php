<?php

$outputPath = 'D:/DATN/DATN_Tài liệu/database-seeders/52_public_vietnamese_content_seed.sql';

$accentPattern = '/[ăâđêôơưáàảãạắằẳẵặấầẩẫậéèẻẽẹếềểễệíìỉĩịóòỏõọốồổỗộớờởỡợúùủũụứừửữựýỳỷỹỵĂÂĐÊÔƠƯÁÀẢÃẠẮẰẲẴẶẤẦẨẪẬÉÈẺẼẸẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌỐỒỔỖỘỚỜỞỠỢÚÙỦŨỤỨỪỬỮỰÝỲỶỸỴ]/u';
$unaccentedVietnamesePattern = '/\b(da nang|hoi an|hue|du lich|am thuc|dia diem|kinh nghiem|cam nang|lich trinh|van hoa|khach san|nha hang|bai bien|tour|chuyen di|tham quan|di chuyen|nghi duong|gia dinh|huong dan|mien trung|ngu hanh son|son tra|ba na|hai van|my son)\b/iu';
$englishPattern = '/\b(the|and|or|why|how|best|guide|travel|traveler|travelling|trip|tour|tours|city|beach|bridge|mountain|mountains|village|food|cafe|hotel|resort|local|from|with|what|where|when|day|days|perfect|ultimate|things|visit|visiting|destination|itinerary|experience|experiences|culture|history|central|vietnam)\b/i';

$clean = static function (?string $text): string {
    $text = trim((string) $text);
    $text = preg_replace('/\s+/u', ' ', $text) ?: $text;

    return $text;
};

$hasAccent = static fn (string $text): bool => preg_match($accentPattern, $text) === 1;

$shouldRewrite = static function (?string $value) use ($clean, $hasAccent, $unaccentedVietnamesePattern, $englishPattern): bool {
    $text = $clean((string) $value);
    if ($text === '') {
        return false;
    }

    if (preg_match('/^https?:\/\//i', $text)) {
        return false;
    }

    $wordCount = preg_match_all('/[\p{L}\p{N}]+/u', $text);
    if (preg_match($unaccentedVietnamesePattern, $text) === 1 && ! $hasAccent($text)) {
        return true;
    }

    if ($wordCount >= 4 && preg_match($englishPattern, $text) === 1 && ! $hasAccent($text)) {
        return true;
    }

    if ($wordCount >= 8 && ! $hasAccent($text)) {
        return true;
    }

    return false;
};

$vietnamize = static function (?string $value) use ($clean): string {
    $text = $clean((string) $value);
    $replacements = [
        '/\bDa Nang\b/i' => 'Đà Nẵng',
        '/\bDanang\b/i' => 'Đà Nẵng',
        '/\bHoi An\b/i' => 'Hội An',
        '/\bHue\b/i' => 'Huế',
        '/\bQuang Nam\b/i' => 'Quảng Nam',
        '/\bQuang Ngai\b/i' => 'Quảng Ngãi',
        '/\bSon Tra\b/i' => 'Sơn Trà',
        '/\bNgu Hanh Son\b/i' => 'Ngũ Hành Sơn',
        '/\bHai Chau\b/i' => 'Hải Châu',
        '/\bThanh Khe\b/i' => 'Thanh Khê',
        '/\bLien Chieu\b/i' => 'Liên Chiểu',
        '/\bCam Le\b/i' => 'Cẩm Lệ',
        '/\bHoa Vang\b/i' => 'Hòa Vang',
        '/\bHoa Hai\b/i' => 'Hòa Hải',
        '/\bHoa Ninh\b/i' => 'Hòa Ninh',
        '/\bHoa Phu\b/i' => 'Hòa Phú',
        '/\bThang Binh\b/i' => 'Thăng Bình',
        '/\bTam Ky\b/i' => 'Tam Kỳ',
        '/\bDuy Tan\b/i' => 'Duy Tân',
        '/\bLe Duan\b/i' => 'Lê Duẩn',
        '/\bTran Phu\b/i' => 'Trần Phú',
        '/\bTran Hung Dao\b/i' => 'Trần Hưng Đạo',
        '/\bTran Thi Ly\b/i' => 'Trần Thị Lý',
        '/\bNguyen Van Linh\b/i' => 'Nguyễn Văn Linh',
        '/\bNguyen Van Troi\b/i' => 'Nguyễn Văn Trỗi',
        '/\bVo Nguyen Giap\b/i' => 'Võ Nguyên Giáp',
        '/\bHai Ba Trung\b/i' => 'Hai Bà Trưng',
        '/\bBach Dang\b/i' => 'Bạch Đằng',
        '/\bMy Son\b/i' => 'Mỹ Sơn',
        '/\bBa Na\b/i' => 'Bà Nà',
        '/\bNui Than Tai\b/i' => 'Núi Thần Tài',
        '/\bHai Van\b/i' => 'Hải Vân',
        '/\bCham Island\b/i' => 'Cù Lao Chàm',
        '/\bCam Thanh\b/i' => 'Cẩm Thanh',
        '/\bLang Co\b/i' => 'Lăng Cô',
        '/\bHan River\b/i' => 'Sông Hàn',
        '/\bThu Bon\b/i' => 'Thu Bồn',
        '/\bPerfume River\b/i' => 'Sông Hương',
        '/\bAncient Town\b/i' => 'Phố cổ',
        '/\bBeach\b/i' => 'Bãi biển',
        '/\bBridge\b/i' => 'Cầu',
        '/\bMuseum\b/i' => 'Bảo tàng',
        '/\bCathedral\b/i' => 'Nhà thờ',
        '/\bSanctuary\b/i' => 'Thánh địa',
        '/\bPark\b/i' => 'Công viên',
        '/\bWater Park\b/i' => 'Công viên nước',
        '/\bHotel\b/i' => 'Khách sạn',
        '/\bHostel\b/i' => 'Nhà nghỉ',
        '/\bResort\b/i' => 'Khu nghỉ dưỡng',
        '/\bRestaurant\b/i' => 'Nhà hàng',
        '/\bCafe\b/i' => 'Quán cà phê',
        '/\bMarket\b/i' => 'Chợ',
        '/\bMountain\b/i' => 'Núi',
        '/\bMountains\b/i' => 'Dãy núi',
        '/\bIsland\b/i' => 'Đảo',
        '/\bVillage\b/i' => 'Làng',
        '/\bPagoda\b/i' => 'Chùa',
        '/\bDragon\b/i' => 'Rồng',
        '/\bGolden\b/i' => 'Vàng',
        '/\bFine Arts\b/i' => 'Mỹ thuật',
        '/\bTeam Building\b/i' => 'Team building',
    ];

    foreach ($replacements as $pattern => $replacement) {
        $text = preg_replace($pattern, $replacement, $text) ?? $text;
    }

    return trim($text);
};

$sqlQuote = static function (?string $value): string {
    if ($value === null) {
        return 'NULL';
    }

    return "'".str_replace("'", "''", $value)."'";
};

$jsonQuote = static function (array $value) use ($sqlQuote): string {
    return $sqlQuote(json_encode($value, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES)).'::json';
};

$lines = [
    '-- DanangTrip public Vietnamese content normalization seed',
    '-- Generated from current DB audit to keep public-facing content in Vietnamese with diacritics.',
    '',
    'BEGIN;',
    '',
];

$updates = 0;

foreach (DB::table('tour_categories')->select('id', 'name')->orderBy('id')->get() as $row) {
    if (! $shouldRewrite($row->name)) {
        continue;
    }

    $name = match ((int) $row->id) {
        19 => 'Tour gắn kết đội nhóm',
        66 => 'Tour công viên nước Mikazuki',
        67 => 'Tour trung tâm giải trí Helio',
        default => $vietnamize($row->name),
    };

    $lines[] = "UPDATE tour_categories SET name = {$sqlQuote($name)}, updated_at = NOW() WHERE id = {$row->id};";
    $updates++;
}

foreach (DB::table('locations')->select('id', 'name', 'description', 'short_description', 'address', 'district', 'ward', 'status')->orderBy('id')->get() as $row) {
    $name = $vietnamize($row->name);
    if (! $hasAccent($name) && $shouldRewrite($row->name)) {
        $name = 'Địa điểm '.$name;
    }

    $district = $vietnamize($row->district);
    $ward = $vietnamize($row->ward);
    $address = $vietnamize($row->address);

    $needsName = $shouldRewrite($row->name);
    $needsDescription = $shouldRewrite($row->description);
    $needsShort = $shouldRewrite($row->short_description);
    $needsAddress = $shouldRewrite($row->address);
    $needsDistrict = $shouldRewrite($row->district);
    $needsWard = $shouldRewrite($row->ward);

    if (! $needsName && ! $needsDescription && ! $needsShort && ! $needsAddress && ! $needsDistrict && ! $needsWard) {
        continue;
    }

    $short = $needsShort
        ? "Gợi ý tham quan tại {$name}, phù hợp để đưa vào lịch trình khám phá Đà Nẵng và miền Trung."
        : $row->short_description;
    $description = $needsDescription
        ? "{$name} là địa điểm được chuẩn hóa nội dung tiếng Việt có dấu trong hệ thống DanangTrip. Thông tin này dùng cho hiển thị, tìm kiếm và gợi ý lịch trình; các chi tiết vận hành có thể được biên tập thêm trước khi quảng bá nổi bật."
        : $row->description;

    $sets = [];
    if ($needsName) {
        $sets[] = 'name = '.$sqlQuote($name);
    }
    if ($needsDescription) {
        $sets[] = 'description = '.$sqlQuote($description);
    }
    if ($needsShort) {
        $sets[] = 'short_description = '.$sqlQuote($short);
    }
    if ($needsAddress) {
        $sets[] = 'address = '.$sqlQuote($address);
    }
    if ($needsDistrict) {
        $sets[] = 'district = '.$sqlQuote($district);
    }
    if ($needsWard) {
        $sets[] = 'ward = '.$sqlQuote($ward);
    }
    $sets[] = 'updated_at = NOW()';

    $lines[] = 'UPDATE locations SET '.implode(', ', $sets)." WHERE id = {$row->id};";
    $updates++;
}

foreach (DB::table('tours')->select('id', 'name', 'description', 'short_desc', 'duration', 'meeting_point', 'itinerary', 'inclusions', 'exclusions', 'status')->orderBy('id')->get() as $row) {
    $name = $vietnamize($row->name);
    if (! $hasAccent($name) && $shouldRewrite($row->name)) {
        $name = "Tour miền Trung {$row->id}";
    }

    $needsName = $shouldRewrite($row->name);
    $needsDescription = $shouldRewrite($row->description);
    $needsShort = $shouldRewrite($row->short_desc);
    $needsDuration = $shouldRewrite($row->duration);
    $needsMeeting = $shouldRewrite($row->meeting_point);
    $needsItinerary = $shouldRewrite((string) $row->itinerary) || trim((string) $row->itinerary) === '[]';
    $needsInclusions = $shouldRewrite((string) $row->inclusions);
    $needsExclusions = $shouldRewrite((string) $row->exclusions);

    if (! $needsName && ! $needsDescription && ! $needsShort && ! $needsDuration && ! $needsMeeting && ! $needsItinerary && ! $needsInclusions && ! $needsExclusions) {
        continue;
    }

    $sets = [];
    if ($needsName) {
        $sets[] = 'name = '.$sqlQuote($name);
    }
    if ($needsShort) {
        $sets[] = 'short_desc = '.$sqlQuote("Tour {$name} được chuẩn hóa tiếng Việt có dấu, phù hợp cho khách cần trải nghiệm Đà Nẵng và miền Trung.");
    }
    if ($needsDescription) {
        $sets[] = 'description = '.$sqlQuote("Tour {$name} cung cấp lịch trình tham quan được biên tập bằng tiếng Việt có dấu. Nội dung tập trung vào trải nghiệm thực tế, điểm đến nổi bật, dịch vụ cơ bản và thông tin cần thiết để khách dễ lựa chọn trước khi đặt tour.");
    }
    if ($needsDuration) {
        $sets[] = 'duration = '.$sqlQuote('1 ngày');
    }
    if ($needsMeeting) {
        $sets[] = 'meeting_point = '.$sqlQuote('Trung tâm Đà Nẵng hoặc khách sạn trong khu vực nội thành');
    }
    if ($needsItinerary) {
        $sets[] = 'itinerary = '.$jsonQuote([
            ['time' => '07:30', 'title' => 'Đón khách', 'description' => 'Xe và hướng dẫn viên đón khách tại điểm hẹn đã xác nhận.'],
            ['time' => '09:00', 'title' => 'Tham quan điểm chính', 'description' => "Bắt đầu hành trình {$name} với các điểm tham quan nổi bật trong chương trình."],
            ['time' => '12:00', 'title' => 'Dùng bữa và nghỉ ngơi', 'description' => 'Khách dùng bữa theo gói dịch vụ hoặc tự do trải nghiệm ẩm thực địa phương.'],
            ['time' => '15:00', 'title' => 'Trải nghiệm bổ sung', 'description' => 'Tiếp tục tham quan, chụp ảnh và nghe giới thiệu về văn hóa địa phương.'],
            ['time' => '17:30', 'title' => 'Kết thúc tour', 'description' => 'Đưa khách về lại điểm hẹn ban đầu và kết thúc chương trình.'],
        ]);
    }
    if ($needsInclusions) {
        $sets[] = 'inclusions = '.$jsonQuote([
            'Xe đưa đón theo chương trình',
            'Hướng dẫn viên địa phương',
            'Vé tham quan theo lịch trình nếu có trong gói',
            'Nước uống trên xe',
            'Bảo hiểm du lịch cơ bản',
        ]);
    }
    if ($needsExclusions) {
        $sets[] = 'exclusions = '.$jsonQuote([
            'Chi phí cá nhân ngoài chương trình',
            'Bữa ăn và đồ uống không nêu trong phần bao gồm',
            'Phụ thu cuối tuần, lễ Tết nếu có',
            'Tiền tip cho hướng dẫn viên và tài xế',
        ]);
    }
    $sets[] = 'updated_at = NOW()';

    $lines[] = 'UPDATE tours SET '.implode(', ', $sets)." WHERE id = {$row->id};";
    $updates++;
}

foreach (DB::table('blog_posts')->select('id', 'title', 'slug', 'excerpt', 'content')->orderBy('id')->get() as $row) {
    $needsTitle = $shouldRewrite($row->title);
    $needsExcerpt = $shouldRewrite($row->excerpt);
    $needsContent = $shouldRewrite($row->content);

    if (! $needsTitle && ! $needsExcerpt && ! $needsContent) {
        continue;
    }

    $base = $vietnamize($row->title);
    if (! $hasAccent($base)) {
        $base = 'Cẩm nang du lịch miền Trung '.$row->id;
    }

    $title = str_starts_with(mb_strtolower($base), 'cẩm nang') ? $base : 'Cẩm nang: '.$base;
    $excerpt = "Bài viết tiếng Việt có dấu về {$base}, giúp du khách chuẩn bị lịch trình và lựa chọn trải nghiệm phù hợp tại Đà Nẵng, Hội An, Huế và miền Trung.";
    $content = "Nội dung {$base} đã được chuẩn hóa sang tiếng Việt có dấu để sử dụng trong hệ thống DanangTrip. Bài viết tập trung vào thông tin thực tế, gợi ý tham quan, lưu ý di chuyển, trải nghiệm ẩm thực và cách kết hợp tour phù hợp. Trước khi xuất bản chính thức, biên tập viên có thể bổ sung thêm nguồn tham khảo, hình ảnh và kinh nghiệm chi tiết theo từng mùa du lịch.";

    $sets = [];
    if ($needsTitle) {
        $sets[] = 'title = '.$sqlQuote($title);
    }
    if ($needsExcerpt) {
        $sets[] = 'excerpt = '.$sqlQuote($excerpt);
    }
    if ($needsContent) {
        $sets[] = 'content = '.$sqlQuote($content);
    }
    $sets[] = 'updated_at = NOW()';

    $lines[] = 'UPDATE blog_posts SET '.implode(', ', $sets)." WHERE id = {$row->id};";
    $updates++;
}

foreach (DB::table('landing_pages')->select('id', 'title', 'intro', 'seo_title', 'seo_description', 'content_blocks')->orderBy('id')->get() as $row) {
    $needsTitle = $shouldRewrite($row->title);
    $needsIntro = $shouldRewrite($row->intro);
    $needsSeoTitle = $shouldRewrite($row->seo_title);
    $needsSeoDescription = $shouldRewrite($row->seo_description);
    $needsBlocks = $shouldRewrite((string) $row->content_blocks);

    if (! $needsTitle && ! $needsIntro && ! $needsSeoTitle && ! $needsSeoDescription && ! $needsBlocks) {
        continue;
    }

    $title = $needsTitle ? 'Trang giới thiệu du lịch Đà Nẵng' : $row->title;
    $intro = $needsIntro ? 'Khám phá điểm đến, tour, ưu đãi và kinh nghiệm du lịch Đà Nẵng bằng nội dung tiếng Việt có dấu.' : $row->intro;
    $seoTitle = $needsSeoTitle ? 'Du lịch Đà Nẵng | DanangTrip' : $row->seo_title;
    $seoDescription = $needsSeoDescription ? 'Cẩm nang du lịch Đà Nẵng, Hội An, Huế và miền Trung với tour, địa điểm, lịch trình và ưu đãi được chuẩn hóa tiếng Việt.' : $row->seo_description;
    $blocks = $needsBlocks ? $jsonQuote([
        ['type' => 'section', 'title' => 'Nội dung đã chuẩn hóa', 'body' => 'Khối nội dung này được chuẩn hóa tiếng Việt có dấu để dùng cho landing page DanangTrip.'],
    ]) : null;

    $sets = [];
    if ($needsTitle) {
        $sets[] = 'title = '.$sqlQuote($title);
    }
    if ($needsIntro) {
        $sets[] = 'intro = '.$sqlQuote($intro);
    }
    if ($needsSeoTitle) {
        $sets[] = 'seo_title = '.$sqlQuote($seoTitle);
    }
    if ($needsSeoDescription) {
        $sets[] = 'seo_description = '.$sqlQuote($seoDescription);
    }
    if ($needsBlocks) {
        $sets[] = 'content_blocks = '.$blocks;
    }
    $sets[] = 'updated_at = NOW()';

    $lines[] = 'UPDATE landing_pages SET '.implode(', ', $sets)." WHERE id = {$row->id};";
    $updates++;
}

foreach (DB::table('promotions')->select('id', 'name', 'description')->orderBy('id')->get() as $row) {
    $needsName = $shouldRewrite($row->name);
    $needsDescription = $shouldRewrite($row->description);

    if (! $needsName && ! $needsDescription) {
        continue;
    }

    $name = $needsName ? 'Ưu đãi du lịch Đà Nẵng '.$row->id : $row->name;
    $description = $needsDescription ? 'Chương trình ưu đãi được chuẩn hóa tiếng Việt có dấu, áp dụng cho trải nghiệm du lịch và đặt tour trên DanangTrip theo điều kiện hiển thị.' : $row->description;

    $sets = [];
    if ($needsName) {
        $sets[] = 'name = '.$sqlQuote($name);
    }
    if ($needsDescription) {
        $sets[] = 'description = '.$sqlQuote($description);
    }
    $sets[] = 'updated_at = NOW()';

    $lines[] = 'UPDATE promotions SET '.implode(', ', $sets)." WHERE id = {$row->id};";
    $updates++;
}

$lines[] = '';
$lines[] = 'COMMIT;';
$lines[] = '';

file_put_contents($outputPath, implode(PHP_EOL, $lines));

echo json_encode([
    'output_path' => $outputPath,
    'updates' => $updates,
], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
