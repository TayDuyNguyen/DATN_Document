<?php
// Bootstrap Laravel
require 'd:/DATN/danangtrip-api/vendor/autoload.php';
$app = require_once 'd:/DATN/danangtrip-api/bootstrap/app.php';
$kernel = $app->make(Illuminate\Contracts\Console\Kernel::class);
$kernel->bootstrap();

$v2Dir = "d:/DATN/DATN_Tài liệu/database-seeders/seeders_v2";

echo "=== DanangTrip Master Database Exporter to Seeders v2 ===\n\n";

// Helper for generic table dump
function dumpTableToSql($tableName, $query, $onConflict = '') {
    $rows = $query->get();
    if ($rows->isEmpty()) {
        return "-- No records in $tableName\n\n";
    }
    
    // Get columns
    $columns = array_keys((array)$rows->first());
    $columnsList = implode(', ', array_map(fn($c) => "\"$c\"", $columns));
    
    $sql = "INSERT INTO \"$tableName\" ($columnsList) VALUES\n";
    $valueLines = [];
    foreach ($rows as $row) {
        $values = [];
        foreach ($columns as $col) {
            $val = $row->$col;
            if ($val === null) {
                $values[] = 'NULL';
            } elseif (is_bool($val)) {
                $values[] = $val ? 'true' : 'false';
            } elseif (is_int($val) || is_float($val)) {
                $values[] = $val;
            } else {
                $isJson = false;
                if (in_array($col, ['itinerary', 'inclusions', 'exclusions', 'images', 'opening_hours', 'metadata', 'headers', 'body', 'content_hash']) &&
                    (strpos($val, '[') === 0 || strpos($val, '{') === 0)) {
                    $isJson = true;
                }
                
                $escaped = str_replace("'", "''", $val);
                if ($isJson) {
                    $values[] = "'$escaped'::jsonb";
                } else {
                    $values[] = "'$escaped'";
                }
            }
        }
        $valueLines[] = "(" . implode(', ', $values) . ")";
    }
    $sql .= implode(",\n", $valueLines);
    if ($onConflict) {
        $sql .= "\n$onConflict;\n\n";
    } else {
        $sql .= ";\n\n";
    }
    return $sql;
}

// Dedicated function to dump tours with enrichment
function dumpToursToSql($query) {
    $rows = $query->get();
    if ($rows->isEmpty()) {
        return "-- No records in tours\n\n";
    }
    
    $columns = array_keys((array)$rows->first());
    $columnsList = implode(', ', array_map(fn($c) => "\"$c\"", $columns));
    
    $enrichmentsFile = 'C:/Users/TUF/.gemini/antigravity-ide/brain/304e46c9-fc7c-4a8c-b2a9-136f350e5d65/scratch/vi_tour_enrichments.json';
    $enrichments = [];
    if (file_exists($enrichmentsFile)) {
        $enrichments = json_decode(file_get_contents($enrichmentsFile), true);
    }

    $sql = "INSERT INTO \"tours\" ($columnsList) VALUES\n";
    $valueLines = [];
    foreach ($rows as $row) {
        $values = [];
        $id = $row->id;
        $slug = $row->slug;
        
        if (isset($enrichments[$slug])) {
            $row->name = $enrichments[$slug]['name'];
            $row->short_desc = $enrichments[$slug]['short_desc'];
            $row->description = $enrichments[$slug]['description'];
            $row->itinerary = json_encode($enrichments[$slug]['itinerary'], JSON_UNESCAPED_UNICODE);
            $row->inclusions = json_encode($enrichments[$slug]['inclusions'], JSON_UNESCAPED_UNICODE);
            $row->exclusions = json_encode($enrichments[$slug]['exclusions'], JSON_UNESCAPED_UNICODE);
            $row->meeting_point = $enrichments[$slug]['meeting_point'];
            $row->start_time = $enrichments[$slug]['start_time'] ?? $row->start_time;
        }
        
        $name = $row->name;
        
        foreach ($columns as $col) {
            $val = $row->$col;
            
            // Enrich empty inclusions
            if ($col === 'inclusions') {
                $incVal = trim($val);
                if (empty($incVal) || $incVal === '[]' || $incVal === '{}' || $incVal === 'null') {
                    if (strpos(strtolower($name), 'bà nà') !== false || strpos(strtolower($name), 'ba na') !== false) {
                        $incArr = [
                            "Xe du lịch đưa đón đời mới phục vụ suốt hành trình",
                            "Vé cáp treo khứ hồi Bà Nà Hills theo quy định của Sun World",
                            "Hướng dẫn viên tiếng Việt chuyên nghiệp, tận tâm và am hiểu địa phương",
                            "Bữa ăn trưa buffet tại nhà hàng trên đỉnh Bà Nà (áp dụng theo gói chọn)",
                            "Nước uống đóng chai miễn phí trên xe (1 chai/người/ngày)",
                            "Bảo hiểm du lịch trọn gói mức bồi thường tối đa 20.000.000đ/vụ"
                        ];
                    } elseif (strpos(strtolower($name), 'cảng') !== false || strpos(strtolower($name), 'port') !== false || strpos(strtolower($name), 'shore') !== false) {
                        $incArr = [
                            "Xe du lịch đưa đón khứ hồi từ cảng biển (Tiên Sa hoặc Chân Mây) theo lịch trình tàu cập cảng",
                            "Hướng dẫn viên tiếng Việt/tiếng Anh vui vẻ, giàu kinh nghiệm, thuyết minh suốt tuyến",
                            "Vé tham quan tất cả các địa danh nổi tiếng có trong chương trình",
                            "Bữa ăn trưa đặc sản địa phương tại nhà hàng chất lượng",
                            "Nước uống đóng chai phục vụ miễn phí trên xe suốt hành trình",
                            "Bảo hiểm du lịch cơ bản suốt tuyến bảo vệ du khách"
                        ];
                    } else {
                        $incArr = [
                            "Xe du lịch vận chuyển đời mới đưa đón theo lịch trình chi tiết",
                            "Hướng dẫn viên chuyên nghiệp, am hiểu văn hóa và địa phương đồng hành suốt hành trình",
                            "Vé vào cổng các điểm tham quan theo chương trình",
                            "Nước uống đóng chai phục vụ trên xe du lịch",
                            "Bảo hiểm du lịch cơ bản"
                        ];
                    }
                    $val = json_encode($incArr, JSON_UNESCAPED_UNICODE);
                }
            }
            
            // Enrich empty exclusions
            if ($col === 'exclusions') {
                $excVal = trim($val);
                if (empty($excVal) || $excVal === '[]' || $excVal === '{}' || $excVal === 'null') {
                    $excArr = [
                        "Thuế VAT 10% (nếu du khách yêu cầu xuất hóa đơn đỏ)",
                        "Đồ uống gọi thêm trong các bữa ăn và các chi phí ăn uống phát sinh ngoài chương trình",
                        "Chi phí cá nhân: mua sắm quà lưu niệm, giặt ủi, dịch vụ khách sạn",
                        "Tiền tip cho hướng dẫn viên và tài xế (tự nguyện theo mức độ hài lòng của du khách)"
                    ];
                    $val = json_encode($excArr, JSON_UNESCAPED_UNICODE);
                }
            }
            
            // Enrich empty meeting point
            if ($col === 'meeting_point') {
                $meetVal = trim($val);
                if (empty($meetVal) || $meetVal === 'null') {
                    $nameLower = strtolower($name);
                    $slugLower = strtolower($slug);
                    if (strpos($nameLower, 'hội an') !== false || strpos($slugLower, 'hoi-an') !== false) {
                        $val = "Đón khách tại khách sạn hoặc điểm hẹn khu vực Phố cổ Hội An";
                    } elseif (strpos($nameLower, 'huế') !== false || strpos($slugLower, 'hue') !== false) {
                        $val = "Đón khách tại khách sạn hoặc điểm hẹn khu vực trung tâm TP. Huế";
                    } elseif (strpos($nameLower, 'đà nẵng') !== false || strpos($slugLower, 'da-nang') !== false || strpos($nameLower, 'bà nà') !== false || strpos($slugLower, 'ba-na') !== false || strpos($slugLower, 'tien-sa') !== false) {
                        $val = "Đón khách tại khách sạn hoặc điểm hẹn khu vực trung tâm TP. Đà Nẵng";
                    } else {
                        $val = "Đón khách tại khách sạn hoặc điểm hẹn theo yêu cầu trong khu vực trung tâm";
                    }
                }
            }
            
            if ($val === null) {
                $values[] = 'NULL';
            } elseif (is_bool($val)) {
                $values[] = $val ? 'true' : 'false';
            } elseif (is_int($val) || is_float($val)) {
                $values[] = $val;
            } else {
                $isJson = false;
                if (in_array($col, ['itinerary', 'inclusions', 'exclusions', 'images']) &&
                    (strpos($val, '[') === 0 || strpos($val, '{') === 0)) {
                    $isJson = true;
                }
                
                $escaped = str_replace("'", "''", $val);
                if ($isJson) {
                    $values[] = "'$escaped'::jsonb";
                } else {
                    $values[] = "'$escaped'";
                }
            }
        }
        $valueLines[] = "(" . implode(', ', $values) . ")";
    }
    
    $sql .= implode(",\n", $valueLines) . "\nON CONFLICT (id) DO UPDATE SET\n";
    $sql .= "    name = EXCLUDED.name,\n";
    $sql .= "    slug = EXCLUDED.slug,\n";
    $sql .= "    tour_category_id = EXCLUDED.tour_category_id,\n";
    $sql .= "    description = EXCLUDED.description,\n";
    $sql .= "    short_desc = EXCLUDED.short_desc,\n";
    $sql .= "    itinerary = EXCLUDED.itinerary,\n";
    $sql .= "    inclusions = EXCLUDED.inclusions,\n";
    $sql .= "    exclusions = EXCLUDED.exclusions,\n";
    $sql .= "    price_adult = EXCLUDED.price_adult,\n";
    $sql .= "    price_child = EXCLUDED.price_child,\n";
    $sql .= "    price_infant = EXCLUDED.price_infant,\n";
    $sql .= "    discount_percent = EXCLUDED.discount_percent,\n";
    $sql .= "    duration = EXCLUDED.duration,\n";
    $sql .= "    start_time = EXCLUDED.start_time,\n";
    $sql .= "    meeting_point = EXCLUDED.meeting_point,\n";
    $sql .= "    max_people = EXCLUDED.max_people,\n";
    $sql .= "    min_people = EXCLUDED.min_people,\n";
    $sql .= "    thumbnail = EXCLUDED.thumbnail,\n";
    $sql .= "    images = EXCLUDED.images,\n";
    $sql .= "    status = EXCLUDED.status,\n";
    $sql .= "    updated_at = NOW();\n\n";
    return $sql;
}

// Helper for dynamic schedules
function dumpTourSchedulesToSql($query) {
    $rows = $query->get();
    if ($rows->isEmpty()) {
        return "-- No records in tour_schedules\n\n";
    }
    
    $today = new DateTime('2026-06-15'); // June 15, 2026 as pivot
    
    $sql = "INSERT INTO \"tour_schedules\" (id, tour_id, start_date, end_date, max_people, booked_people, price_adult, price_child, price_infant, status, booking_availability, departure_code, departure_place, booking_deadline, created_at, updated_at) VALUES\n";
    $valueLines = [];
    foreach ($rows as $row) {
        $id = $row->id;
        $tourId = $row->tour_id;
        
        $startDate = new DateTime($row->start_date);
        $offsetDays = $today->diff($startDate)->format('%r%a');
        $startDateExpr = "CURRENT_DATE + ($offsetDays)";
        
        $endDate = new DateTime($row->end_date);
        $endOffsetDays = $today->diff($endDate)->format('%r%a');
        $endDateExpr = "CURRENT_DATE + ($endOffsetDays)";
        
        $maxP = $row->max_people !== null ? $row->max_people : 'NULL';
        $booked = $row->booked_people !== null ? $row->booked_people : 'NULL';
        $priceAdult = $row->price_adult !== null ? $row->price_adult : 'NULL';
        $priceChild = $row->price_child !== null ? $row->price_child : 'NULL';
        $priceInfant = $row->price_infant !== null ? $row->price_infant : 'NULL';
        
        $statusExpr = $row->status !== null ? "'" . str_replace("'", "''", $row->status) . "'" : "NULL";
        $availExpr = $row->booking_availability !== null ? "'" . str_replace("'", "''", $row->booking_availability) . "'" : "NULL";
        
        $depCode = $row->departure_code;
        if ($depCode && preg_match('/^(.*-)(\d{8})$/', $depCode, $m)) {
            $prefix = $m[1];
            $depCodeExpr = "'$prefix' || to_char(CURRENT_DATE + ($offsetDays), 'YYYYMMDD')";
        } else {
            $depCodeExpr = $depCode ? "'" . str_replace("'", "''", $depCode) . "'" : "NULL";
        }
        
        $meetingPointExpr = $row->departure_place !== null ? "'" . str_replace("'", "''", $row->departure_place) . "'" : "NULL";
        
        if ($row->booking_deadline) {
            $startTS = strtotime($row->start_date . ' ' . (isset($row->start_time) ? $row->start_time : '08:00:00'));
            $deadlineTS = strtotime($row->booking_deadline);
            $diffSeconds = $startTS - $deadlineTS;
            $diffHours = round($diffSeconds / 3600);
            $deadlineExpr = "(CURRENT_DATE + ($offsetDays))::timestamp - interval '$diffHours hours'";
        } else {
            $deadlineExpr = "NULL";
        }
        
        $valueLines[] = "($id, $tourId, $startDateExpr, $endDateExpr, $maxP, $booked, $priceAdult, $priceChild, $priceInfant, $statusExpr, $availExpr, $depCodeExpr, $meetingPointExpr, $deadlineExpr, NOW(), NOW())";
    }
    
    $sql .= implode(",\n", $valueLines) . "\nON CONFLICT (id) DO UPDATE SET\n";
    $sql .= "    start_date = EXCLUDED.start_date,\n";
    $sql .= "    end_date = EXCLUDED.end_date,\n";
    $sql .= "    departure_code = EXCLUDED.departure_code,\n";
    $sql .= "    booking_deadline = EXCLUDED.booking_deadline,\n";
    $sql .= "    updated_at = NOW();\n\n";
    return $sql;
}

// Dedicated function to dump blog posts with enrichment
function dumpBlogPostsToSql($query, $onConflict = '') {
    $rows = $query->get();
    if ($rows->isEmpty()) {
        return "-- No records in blog_posts\n\n";
    }
    
    $columns = array_keys((array)$rows->first());
    $columnsList = implode(', ', array_map(fn($c) => "\"$c\"", $columns));
    
    $enrichmentsFile = 'C:/Users/TUF/.gemini/antigravity-ide/brain/304e46c9-fc7c-4a8c-b2a9-136f350e5d65/scratch/vi_blog_enrichments.json';
    $enrichments = [];
    if (file_exists($enrichmentsFile)) {
        $enrichments = json_decode(file_get_contents($enrichmentsFile), true);
    }
    
    $sql = "INSERT INTO \"blog_posts\" ($columnsList) VALUES\n";
    $valueLines = [];
    foreach ($rows as $row) {
        $slug = $row->slug;
        if (isset($enrichments[$slug])) {
            $row->title = $enrichments[$slug]['title'];
            $row->excerpt = $enrichments[$slug]['excerpt'];
            $row->content = $enrichments[$slug]['content'];
            $row->status = $enrichments[$slug]['status'] ?? 'published';
        }
        
        $values = [];
        foreach ($columns as $col) {
            $val = $row->$col;
            if ($val === null) {
                $values[] = 'NULL';
            } elseif (is_bool($val)) {
                $values[] = $val ? 'true' : 'false';
            } elseif (is_int($val) || is_float($val)) {
                $values[] = $val;
            } else {
                $isJson = false;
                if (in_array($col, ['body', 'headers', 'metadata']) &&
                    (strpos($val, '[') === 0 || strpos($val, '{') === 0)) {
                    $isJson = true;
                }
                
                $escaped = str_replace("'", "''", $val);
                if ($isJson) {
                    $values[] = "'$escaped'::jsonb";
                } else {
                    $values[] = "'$escaped'";
                }
            }
        }
        $valueLines[] = "(" . implode(', ', $values) . ")";
    }
    $sql .= implode(",\n", $valueLines);
    if ($onConflict) {
        $sql .= "\n$onConflict;\n\n";
    } else {
        $sql .= ";\n\n";
    }
    return $sql;
}

// Dedicated function to dump relevant tour locations
function dumpTourLocationsToSql($tourIds) {
    if (!is_array($tourIds)) {
        $tourIds = [$tourIds];
    }
    
    // Load all locations
    $locations = DB::table('locations')->get()->keyBy('id');
    
    // Load tours in scope
    $tours = DB::table('tours')->whereIn('id', $tourIds)->get();
    
    // Load enrichments
    $enrichmentsFile = 'C:/Users/TUF/.gemini/antigravity-ide/brain/304e46c9-fc7c-4a8c-b2a9-136f350e5d65/scratch/vi_tour_enrichments.json';
    $enrichments = [];
    if (file_exists($enrichmentsFile)) {
        $enrichments = json_decode(file_get_contents($enrichmentsFile), true);
    }
    
    // Create map of tour id -> description & itinerary
    $tourDataMap = [];
    foreach ($tours as $t) {
        $name = $t->name;
        $desc = $t->description . " " . $t->short_desc . " " . $t->name;
        $itinerary = json_decode($t->itinerary, true) ?? [];
        
        if (isset($enrichments[$t->slug])) {
            $name = $enrichments[$t->slug]['name'];
            $desc = $enrichments[$t->slug]['description'] . " " . $enrichments[$t->slug]['short_desc'] . " " . $name;
            $itinerary = $enrichments[$t->slug]['itinerary'] ?? [];
        }
        
        $tourDataMap[$t->id] = [
            'name' => $name,
            'desc' => $desc,
            'itinerary' => $itinerary
        ];
    }
    
    // Fetch all tour_locations matching tourIds
    $tourLocs = DB::table('tour_locations')->whereIn('tour_id', $tourIds)->orderBy('tour_id')->orderBy('location_id')->get();
    
    if ($tourLocs->isEmpty()) {
        return "-- No records in tour_locations\n\n";
    }
    
    $keptCount = 0;
    $filteredCount = 0;
    
    $columns = array_keys((array)$tourLocs->first());
    $columnsList = implode(', ', array_map(fn($c) => "\"$c\"", $columns));
    
    $valueLines = [];
    foreach ($tourLocs as $row) {
        $tourId = $row->tour_id;
        $locId = $row->location_id;
        
        if (!isset($locations[$locId]) || !isset($tourDataMap[$tourId])) {
            $filteredCount++;
            continue;
        }
        
        $locName = $locations[$locId]->name;
        $tourInfo = $tourDataMap[$tourId];
        $tourDesc = $tourInfo['desc'];
        
        // Strip common prefixes to get the core keyword (e.g. 'Sun World Bà Nà Hills' -> 'Bà Nà Hills')
        $cleanLocName = preg_replace('/(khu du lịch|danh thắng|phố cổ|chùa|làng|đảo|bãi biển|cầu|sông|cảng|vườn quốc gia|điểm lưu trú|quán|chợ|sun world)\s+/iu', '', $locName);
        $cleanLocName = trim($cleanLocName);
        
        // Fallback
        if (mb_strlen($cleanLocName) < 3) {
            $cleanLocName = $locName;
        }
        
        $inDesc = (mb_stripos($tourDesc, $cleanLocName) !== false);
        
        $inItinerary = false;
        if (is_array($tourInfo['itinerary'])) {
            foreach ($tourInfo['itinerary'] as $item) {
                $itemText = is_array($item) ? json_encode($item, JSON_UNESCAPED_UNICODE) : $item;
                if (mb_stripos($itemText, $cleanLocName) !== false) {
                    $inItinerary = true;
                    break;
                }
            }
        }
        
        if ($inDesc || $inItinerary) {
            $values = [];
            foreach ($columns as $col) {
                $val = $row->$col;
                if ($val === null) {
                    $values[] = 'NULL';
                } elseif (is_bool($val)) {
                    $values[] = $val ? 'true' : 'false';
                } elseif (is_int($val) || is_float($val)) {
                    $values[] = $val;
                } else {
                    $values[] = "'" . str_replace("'", "''", $val) . "'";
                }
            }
            $valueLines[] = "(" . implode(', ', $values) . ")";
            $keptCount++;
        } else {
            $filteredCount++;
        }
    }
    
    echo "Tour-Location relevance filter: Kept $keptCount, Filtered $filteredCount relations for tour range.\n";
    
    if (empty($valueLines)) {
        return "-- All tour_locations filtered out as irrelevant for this range\n\n";
    }
    
    $sql = "INSERT INTO \"tour_locations\" ($columnsList) VALUES\n";
    $sql .= implode(",\n", $valueLines);
    $sql .= " ON CONFLICT (tour_id, location_id) DO NOTHING;\n\n";
    return $sql;
}


// ---------------------------------------------------------------------
// WRITE BASE SQL FILES
// ---------------------------------------------------------------------
echo "Exporting base/01_categories.sql... ";
$catSql = "BEGIN;\n" . dumpTableToSql('categories', DB::table('categories')->orderBy('id'), "ON CONFLICT (id) DO NOTHING") . "COMMIT;\n";
file_put_contents("$v2Dir/base/01_categories.sql", $catSql);
echo "Done!\n";

echo "Exporting base/02_subcategories.sql... ";
$subSql = "BEGIN;\n" . dumpTableToSql('subcategories', DB::table('subcategories')->orderBy('id'), "ON CONFLICT (id) DO NOTHING") . "COMMIT;\n";
file_put_contents("$v2Dir/base/02_subcategories.sql", $subSql);
echo "Done!\n";

echo "Exporting base/03_tags.sql... ";
$tagSql = "BEGIN;\n" . dumpTableToSql('tags', DB::table('tags')->orderBy('id'), "ON CONFLICT (id) DO NOTHING") . "COMMIT;\n";
file_put_contents("$v2Dir/base/03_tags.sql", $tagSql);
echo "Done!\n";

echo "Exporting base/04_amenities.sql... ";
$amSql = "BEGIN;\n" . dumpTableToSql('amenities', DB::table('amenities')->orderBy('id'), "ON CONFLICT (id) DO NOTHING") . "COMMIT;\n";
file_put_contents("$v2Dir/base/04_amenities.sql", $amSql);
echo "Done!\n";

echo "Exporting base/05_tour_categories.sql... ";
$tcSql = "BEGIN;\n" . dumpTableToSql('tour_categories', DB::table('tour_categories')->orderBy('id'), "ON CONFLICT (id) DO NOTHING") . "COMMIT;\n";
file_put_contents("$v2Dir/base/05_tour_categories.sql", $tcSql);
echo "Done!\n";

echo "Exporting base/06_blog_categories.sql... ";
$bcSql = "BEGIN;\n" . dumpTableToSql('blog_categories', DB::table('blog_categories')->orderBy('id'), "ON CONFLICT (id) DO NOTHING") . "COMMIT;\n";
file_put_contents("$v2Dir/base/06_blog_categories.sql", $bcSql);
echo "Done!\n";

echo "Exporting base/07_system_settings.sql... ";
$setSql = "BEGIN;\n" . dumpTableToSql('settings', DB::table('settings')->orderBy('id'), "ON CONFLICT (id) DO NOTHING") . "COMMIT;\n";
file_put_contents("$v2Dir/base/07_system_settings.sql", $setSql);
echo "Done!\n";

echo "Exporting base/08_admin_users.sql... ";
$admSql = "BEGIN;\n" . dumpTableToSql('users', DB::table('users')->whereIn('id', [1, 2])->orderBy('id'), 
    "ON CONFLICT (id) DO UPDATE SET email = EXCLUDED.email, full_name = EXCLUDED.full_name, role = EXCLUDED.role, status = EXCLUDED.status, updated_at = NOW()") . "COMMIT;\n";
file_put_contents("$v2Dir/base/08_admin_users.sql", $admSql);
echo "Done!\n";

echo "Exporting base/09_point_rules.sql... ";
$prSql = "BEGIN;\n";
$prSql .= dumpTableToSql('point_rules', DB::table('point_rules')->orderBy('id'), "ON CONFLICT (id) DO NOTHING");
$prSql .= dumpTableToSql('point_rewards', DB::table('point_rewards')->orderBy('id'), "ON CONFLICT (id) DO NOTHING");
$prSql .= "COMMIT;\n";
file_put_contents("$v2Dir/base/09_point_rules.sql", $prSql);
echo "Done!\n";

echo "Exporting base/10_landing_pages.sql... ";
$lpSql = "BEGIN;\n" . dumpTableToSql('landing_pages', DB::table('landing_pages')->orderBy('id'), "ON CONFLICT (id) DO NOTHING") . "COMMIT;\n";
file_put_contents("$v2Dir/base/10_landing_pages.sql", $lpSql);
echo "Done!\n";


// ---------------------------------------------------------------------
// WRITE DEMO SQL FILES
// ---------------------------------------------------------------------
echo "Exporting demo/01_demo_users.sql... ";
$demoUserSql = "BEGIN;\n" . dumpTableToSql('users', DB::table('users')->whereNotIn('id', [1, 2])->where('email', '!=', 'duytayx8@gmail.com')->orderBy('id'),
    "ON CONFLICT (id) DO UPDATE SET email = EXCLUDED.email, username = EXCLUDED.username, full_name = EXCLUDED.full_name, updated_at = NOW()") . "COMMIT;\n";
file_put_contents("$v2Dir/demo/01_demo_users.sql", $demoUserSql);
echo "Done!\n";

echo "Exporting demo/02_promotions.sql... ";
$promoSql = "BEGIN;\n" . dumpTableToSql('promotions', DB::table('promotions')->orderBy('id'), "ON CONFLICT (id) DO NOTHING") . "COMMIT;\n";
file_put_contents("$v2Dir/demo/02_promotions.sql", $promoSql);
echo "Done!\n";

echo "Exporting demo/03_locations.sql... ";
$locationsFile = "$v2Dir/demo/03_locations.sql";
$locSql = "BEGIN;\n";
$locSql .= "-- Disable triggers\nALTER TABLE locations DISABLE TRIGGER ALL;\n\n";
$locSql .= dumpTableToSql('locations', DB::table('locations')->where('id', '<=', 114)->orderBy('id'), 
    "ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name, slug = EXCLUDED.slug, category_id = EXCLUDED.category_id, address = EXCLUDED.address, description = EXCLUDED.description, short_description = EXCLUDED.short_description, thumbnail = EXCLUDED.thumbnail, images = EXCLUDED.images, status = EXCLUDED.status, updated_at = NOW()");
$locSql .= dumpTableToSql('location_tags', DB::table('location_tags')->where('location_id', '<=', 114)->orderBy('location_id')->orderBy('tag_id'), "ON CONFLICT (location_id, tag_id) DO NOTHING");
$locSql .= dumpTableToSql('location_amenities', DB::table('location_amenities')->where('location_id', '<=', 114)->orderBy('location_id')->orderBy('amenity_id'), "ON CONFLICT (location_id, amenity_id) DO NOTHING");
$locSql .= "-- Re-enable triggers\nALTER TABLE locations ENABLE TRIGGER ALL;\n\n";
$locSql .= "SELECT setval(pg_get_serial_sequence('locations', 'id'), GREATEST((SELECT COALESCE(MAX(id), 0) FROM locations), 1), true);\n\n";
$locSql .= "COMMIT;\n";
file_put_contents($locationsFile, $locSql);
echo "Done!\n";

echo "Exporting demo/04_tours.sql... ";
$toursFile = "$v2Dir/demo/04_tours.sql";
$tourSql = "BEGIN;\n";
$tourSql .= "-- Disable triggers\nALTER TABLE tours DISABLE TRIGGER ALL;\n\n";
$tourSql .= dumpToursToSql(DB::table('tours')->where('id', '<=', 164)->orderBy('id'));
$tourSql .= dumpTourSchedulesToSql(DB::table('tour_schedules')->where('tour_id', '<=', 164)->orderBy('id'));
$tourSql .= dumpTourLocationsToSql(range(1, 164));
$tourSql .= "-- Re-enable triggers\nALTER TABLE tours ENABLE TRIGGER ALL;\n\n";
$tourSql .= "SELECT setval(pg_get_serial_sequence('tours', 'id'), GREATEST((SELECT COALESCE(MAX(id), 0) FROM tours), 1), true);\n";
$tourSql .= "SELECT setval(pg_get_serial_sequence('tour_schedules', 'id'), GREATEST((SELECT COALESCE(MAX(id), 0) FROM tour_schedules), 1), true);\n";
$tourSql .= "SELECT setval(pg_get_serial_sequence('tour_locations', 'id'), GREATEST((SELECT COALESCE(MAX(id), 0) FROM tour_locations), 1), true);\n\n";
$tourSql .= "COMMIT;\n";
file_put_contents($toursFile, $tourSql);
echo "Done!\n";

echo "Exporting demo/05_blog_posts.sql... ";
$blogsFile = "$v2Dir/demo/05_blog_posts.sql";
$blogSql = "BEGIN;\n";
$blogSql .= "-- Disable triggers\nALTER TABLE blog_posts DISABLE TRIGGER ALL;\n\n";
$blogSql .= dumpBlogPostsToSql(DB::table('blog_posts')->where('id', '<=', 100)->orWhereBetween('id', [201, 218])->orderBy('id'),
    "ON CONFLICT (id) DO UPDATE SET title = EXCLUDED.title, slug = EXCLUDED.slug, excerpt = EXCLUDED.excerpt, content = EXCLUDED.content, featured_image = EXCLUDED.featured_image, status = EXCLUDED.status, updated_at = NOW()");
$blogSql .= dumpTableToSql('blog_post_categories', DB::table('blog_post_categories')->whereIn('post_id', function($q) {
    $q->select('id')->from('blog_posts')->where('id', '<=', 100)->orWhereBetween('id', [201, 218]);
})->orderBy('post_id')->orderBy('blog_category_id'), "ON CONFLICT (post_id, blog_category_id) DO NOTHING");
$blogSql .= "-- Re-enable triggers\nALTER TABLE blog_posts ENABLE TRIGGER ALL;\n\n";
$blogSql .= "SELECT setval(pg_get_serial_sequence('blog_posts', 'id'), GREATEST((SELECT COALESCE(MAX(id), 0) FROM blog_posts), 1), true);\n\n";
$blogSql .= "COMMIT;\n";
file_put_contents($blogsFile, $blogSql);
echo "Done!\n";

echo "Exporting demo/06_bookings.sql... ";
$bookSql = "BEGIN;\n";
// Filter out bookings relating to tour 165
$bookingSubquery = function($q) {
    $q->select('booking_id')->from('booking_items')->where('tour_id', 165);
};
$bookSql .= dumpTableToSql('bookings', DB::table('bookings')->whereNotIn('id', $bookingSubquery)->orderBy('id'),
    "ON CONFLICT (id) DO UPDATE SET booking_status = EXCLUDED.booking_status, payment_status = EXCLUDED.payment_status, updated_at = NOW()");
$bookSql .= dumpTableToSql('booking_items', DB::table('booking_items')->whereNotIn('booking_id', $bookingSubquery)->orderBy('id'), "ON CONFLICT (id) DO NOTHING");
$bookSql .= dumpTableToSql('payments', DB::table('payments')->whereNotIn('booking_id', $bookingSubquery)->orderBy('id'),
    "ON CONFLICT (id) DO UPDATE SET payment_status = EXCLUDED.payment_status, updated_at = NOW()");
$bookSql .= "SELECT setval(pg_get_serial_sequence('bookings', 'id'), GREATEST((SELECT COALESCE(MAX(id), 0) FROM bookings), 1), true);\n";
$bookSql .= "SELECT setval(pg_get_serial_sequence('booking_items', 'id'), GREATEST((SELECT COALESCE(MAX(id), 0) FROM booking_items), 1), true);\n";
$bookSql .= "SELECT setval(pg_get_serial_sequence('payments', 'id'), GREATEST((SELECT COALESCE(MAX(id), 0) FROM payments), 1), true);\n\n";
$bookSql .= "COMMIT;\n";
file_put_contents("$v2Dir/demo/06_bookings.sql", $bookSql);
echo "Done!\n";

echo "Exporting demo/07_ratings.sql... ";
$ratingSql = "BEGIN;\n";
$ratingSubquery = function($q) {
    $q->select('id')->from('ratings')->where('tour_id', 165);
};
$ratingSql .= dumpTableToSql('ratings', DB::table('ratings')->where('tour_id', '!=', 165)->orWhereNull('tour_id')->orderBy('id'), "ON CONFLICT (id) DO NOTHING");
$ratingSql .= dumpTableToSql('rating_images', DB::table('rating_images')->whereNotIn('rating_id', $ratingSubquery)->orderBy('id'), "ON CONFLICT (id) DO NOTHING");
$ratingSql .= "SELECT setval(pg_get_serial_sequence('ratings', 'id'), GREATEST((SELECT COALESCE(MAX(id), 0) FROM ratings), 1), true);\n";
$ratingSql .= "SELECT setval(pg_get_serial_sequence('rating_images', 'id'), GREATEST((SELECT COALESCE(MAX(id), 0) FROM rating_images), 1), true);\n\n";
$ratingSql .= "COMMIT;\n";
file_put_contents("$v2Dir/demo/07_ratings.sql", $ratingSql);
echo "Done!\n";

echo "Exporting demo/08_notifications_activity.sql... ";
$naSql = "BEGIN;\n";
$naSql .= dumpTableToSql('notifications', DB::table('notifications')->orderBy('id'), "ON CONFLICT (id) DO NOTHING");
$naSql .= dumpTableToSql('search_logs', DB::table('search_logs')->orderBy('id'), "ON CONFLICT (id) DO NOTHING");
$naSql .= dumpTableToSql('contacts', DB::table('contacts')->orderBy('id'), "ON CONFLICT (id) DO NOTHING");
$naSql .= dumpTableToSql('views', DB::table('views')->orderBy('id'), "ON CONFLICT (id) DO NOTHING");
$naSql .= dumpTableToSql('point_transactions', DB::table('point_transactions')->orderBy('id'), "ON CONFLICT (id) DO NOTHING");
$naSql .= dumpTableToSql('user_point_balances', DB::table('user_point_balances')->orderBy('id'), "ON CONFLICT (id) DO NOTHING");
$naSql .= dumpTableToSql('user_vouchers', DB::table('user_vouchers')->orderBy('id'), "ON CONFLICT (id) DO NOTHING");
$naSql .= "SELECT setval(pg_get_serial_sequence('notifications', 'id'), GREATEST((SELECT COALESCE(MAX(id), 0) FROM notifications), 1), true);\n";
$naSql .= "SELECT setval(pg_get_serial_sequence('search_logs', 'id'), GREATEST((SELECT COALESCE(MAX(id), 0) FROM search_logs), 1), true);\n";
$naSql .= "SELECT setval(pg_get_serial_sequence('contacts', 'id'), GREATEST((SELECT COALESCE(MAX(id), 0) FROM contacts), 1), true);\n";
$naSql .= "SELECT setval(pg_get_serial_sequence('views', 'id'), GREATEST((SELECT COALESCE(MAX(id), 0) FROM views), 1), true);\n";
$naSql .= "SELECT setval(pg_get_serial_sequence('point_transactions', 'id'), GREATEST((SELECT COALESCE(MAX(id), 0) FROM point_transactions), 1), true);\n";
$naSql .= "SELECT setval(pg_get_serial_sequence('user_point_balances', 'id'), GREATEST((SELECT COALESCE(MAX(id), 0) FROM user_point_balances), 1), true);\n";
$naSql .= "SELECT setval(pg_get_serial_sequence('user_vouchers', 'id'), GREATEST((SELECT COALESCE(MAX(id), 0) FROM user_vouchers), 1), true);\n\n";
$naSql .= "COMMIT;\n";
file_put_contents("$v2Dir/demo/08_notifications_activity.sql", $naSql);
echo "Done!\n";

echo "Exporting demo/09_chat_knowledge.sql... ";
$chatSql = "BEGIN;\n";
$chatSql .= dumpTableToSql('chat_knowledge_base', DB::table('chat_knowledge_base')->orderBy('id'), "ON CONFLICT (id) DO NOTHING");
$chatSql .= "SELECT setval(pg_get_serial_sequence('chat_knowledge_base', 'id'), GREATEST((SELECT COALESCE(MAX(id), 0) FROM chat_knowledge_base), 1), true);\n\n";
$chatSql .= "COMMIT;\n";
file_put_contents("$v2Dir/demo/09_chat_knowledge.sql", $chatSql);
echo "Done!\n";


// ---------------------------------------------------------------------
// WRITE TEST SQL FILES
// ---------------------------------------------------------------------
echo "Exporting test/01_test_cart.sql... ";
$cartSql = "BEGIN;\n" . dumpTableToSql('cart_items', DB::table('cart_items')->orderBy('id'), "ON CONFLICT (id) DO NOTHING") . "COMMIT;\n";
file_put_contents("$v2Dir/test/01_test_cart.sql", $cartSql);
echo "Done!\n";

echo "Exporting test/03_test_checkout.sql (with enrichments for tour 165)... ";
$testCheckoutFile = "$v2Dir/test/03_test_checkout.sql";
$testSql = "BEGIN;\n";
$testSql .= dumpTableToSql('users', DB::table('users')->where('email', 'duytayx8@gmail.com'),
    "ON CONFLICT (email) DO UPDATE SET username = EXCLUDED.username, full_name = EXCLUDED.full_name, phone = EXCLUDED.phone, birthdate = EXCLUDED.birthdate, gender = EXCLUDED.gender, city = EXCLUDED.city, role = EXCLUDED.role, status = EXCLUDED.status, email_verified_at = COALESCE(users.email_verified_at, EXCLUDED.email_verified_at), updated_at = NOW()");
$testSql .= dumpToursToSql(DB::table('tours')->where('id', 165));
$testSql .= dumpTourLocationsToSql([165]);
$testSql .= dumpTourSchedulesToSql(DB::table('tour_schedules')->where('tour_id', 165));

$testBookings = DB::table('bookings')->whereIn('id', function($q) {
    $q->select('booking_id')->from('booking_items')->where('tour_id', 165);
});
if ($testBookings->count() > 0) {
    $testSql .= dumpTableToSql('bookings', $testBookings, "ON CONFLICT (id) DO UPDATE SET booking_status = EXCLUDED.booking_status, payment_status = EXCLUDED.payment_status, updated_at = NOW()");
    $testSql .= dumpTableToSql('booking_items', DB::table('booking_items')->whereIn('booking_id', function($q) {
        $q->select('booking_id')->from('booking_items')->where('tour_id', 165);
    }), "ON CONFLICT (id) DO NOTHING");
    $testSql .= dumpTableToSql('payments', DB::table('payments')->whereIn('booking_id', function($q) {
        $q->select('booking_id')->from('booking_items')->where('tour_id', 165);
    }), "ON CONFLICT (id) DO UPDATE SET payment_status = EXCLUDED.payment_status, updated_at = NOW()");
}

$testRatings = DB::table('ratings')->where('tour_id', 165)->orderBy('id');
if ($testRatings->count() > 0) {
    $testSql .= dumpTableToSql('ratings', $testRatings, "ON CONFLICT (id) DO NOTHING");
    $testSql .= dumpTableToSql('rating_images', DB::table('rating_images')->whereIn('rating_id', function($q) {
        $q->select('id')->from('ratings')->where('tour_id', 165);
    })->orderBy('id'), "ON CONFLICT (id) DO NOTHING");
}

$testSql .= "SELECT setval(pg_get_serial_sequence('users', 'id'), GREATEST((SELECT MAX(id) FROM users), 1), true);\n";
$testSql .= "SELECT setval(pg_get_serial_sequence('tours', 'id'), GREATEST((SELECT MAX(id) FROM tours), 1), true);\n";
$testSql .= "SELECT setval(pg_get_serial_sequence('tour_schedules', 'id'), GREATEST((SELECT MAX(id) FROM tour_schedules), 1), true);\n";
$testSql .= "SELECT setval(pg_get_serial_sequence('bookings', 'id'), GREATEST((SELECT COALESCE(MAX(id), 1) FROM bookings), 1), true);\n";
$testSql .= "SELECT setval(pg_get_serial_sequence('booking_items', 'id'), GREATEST((SELECT COALESCE(MAX(id), 1) FROM booking_items), 1), true);\n";
$testSql .= "SELECT setval(pg_get_serial_sequence('payments', 'id'), GREATEST((SELECT COALESCE(MAX(id), 1) FROM payments), 1), true);\n";
$testSql .= "SELECT setval(pg_get_serial_sequence('ratings', 'id'), GREATEST((SELECT COALESCE(MAX(id), 1) FROM ratings), 1), true);\n";
$testSql .= "SELECT setval(pg_get_serial_sequence('rating_images', 'id'), GREATEST((SELECT COALESCE(MAX(id), 1) FROM rating_images), 1), true);\n\n";
$testSql .= "COMMIT;\n";
file_put_contents($testCheckoutFile, $testSql);
echo "Done!\n\nAll seeders exported and enriched successfully!\n";
