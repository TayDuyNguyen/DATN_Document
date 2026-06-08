<?php

$accentPattern = '/[ăâđêôơưáàảãạắằẳẵặấầẩẫậéèẻẽẹếềểễệíìỉĩịóòỏõọốồổỗộớờởỡợúùủũụứừửữựýỳỷỹỵ]/iu';
$unaccentedPattern = '/\b(trai nghiem|tuyet voi|dich vu|gia ca|hop ly|chuyen di|dang nho|huong dan vien|nhiet tinh|canh quan|thien nhien|khong khi|gia dinh|chat luong|diem den|da nang)\b/iu';

$findings = [];
DB::table('ratings')
    ->select('id', 'comment')
    ->whereNotNull('comment')
    ->orderBy('id')
    ->chunk(200, function ($rows) use (&$findings, $accentPattern, $unaccentedPattern): void {
        foreach ($rows as $row) {
            $comment = trim((string) $row->comment);
            if ($comment === '') {
                continue;
            }

            if (preg_match($unaccentedPattern, $comment) === 1 && preg_match($accentPattern, $comment) !== 1) {
                $findings[] = [
                    'id' => $row->id,
                    'comment' => $comment,
                ];
            }
        }
    });

$summary = [
    'total' => DB::table('ratings')->count(),
    'approved' => DB::table('ratings')->where('status', 'approved')->count(),
    'admin_read_state' => [
        'new' => DB::table('ratings')->where('is_new', true)->count(),
        'viewed' => DB::table('ratings')->where('is_new', false)->count(),
        'new_older_than_30_days' => DB::table('ratings')
            ->where('is_new', true)
            ->where('created_at', '<', now()->subDays(30))
            ->count(),
    ],
    'overall_average' => round((float) DB::table('ratings')->avg('score'), 2),
    'by_score' => DB::table('ratings')
        ->select('score', DB::raw('count(*) as total'))
        ->groupBy('score')
        ->orderBy('score')
        ->get(),
    'location_ratings' => DB::table('ratings')->whereNotNull('location_id')->count(),
    'tour_ratings' => DB::table('ratings')->whereNotNull('tour_id')->count(),
    'booking_ratings' => DB::table('ratings')->whereNotNull('booking_id')->count(),
    'locations_with_reviews' => DB::table('ratings')
        ->whereNotNull('location_id')
        ->distinct()
        ->count('location_id'),
    'active_locations_without_reviews' => DB::table('locations as l')
        ->leftJoin('ratings as r', static function ($join): void {
            $join->on('r.location_id', '=', 'l.id')
                ->where('r.status', '=', 'approved');
        })
        ->where('l.status', 'active')
        ->whereNull('r.id')
        ->count(),
    'tours_with_reviews' => DB::table('ratings')
        ->whereNotNull('tour_id')
        ->distinct()
        ->count('tour_id'),
    'active_tours_without_reviews' => DB::table('tours as t')
        ->leftJoin('ratings as r', static function ($join): void {
            $join->on('r.tour_id', '=', 't.id')
                ->where('r.status', '=', 'approved');
        })
        ->where('t.status', 'active')
        ->whereNull('r.id')
        ->count(),
    'unaccented_comments' => count($findings),
    'duplicate_user_location_groups' => DB::table('ratings')
        ->select('user_id', 'location_id')
        ->whereNotNull('location_id')
        ->groupBy('user_id', 'location_id')
        ->havingRaw('count(*) > 1')
        ->count(),
    'duplicate_user_tour_groups' => DB::table('ratings')
        ->select('user_id', 'tour_id')
        ->whereNotNull('tour_id')
        ->groupBy('user_id', 'tour_id')
        ->havingRaw('count(*) > 1')
        ->count(),
    'location_aggregate_mismatches' => DB::table('locations as l')
        ->leftJoinSub(
            DB::table('ratings')
                ->selectRaw('location_id, count(*)::integer as rating_count, round(avg(score)::numeric, 2) as rating_avg')
                ->whereNotNull('location_id')
                ->where('status', 'approved')
                ->groupBy('location_id'),
            'r',
            'r.location_id',
            '=',
            'l.id'
        )
        ->whereRaw('l.review_count <> COALESCE(r.rating_count, 0)')
        ->orWhereRaw('l.avg_rating <> COALESCE(r.rating_avg, 0)')
        ->count(),
    'tour_aggregate_mismatches' => DB::table('tours as t')
        ->leftJoinSub(
            DB::table('ratings')
                ->selectRaw('tour_id, count(*)::integer as rating_count, round(avg(score)::numeric, 2) as rating_avg')
                ->whereNotNull('tour_id')
                ->where('status', 'approved')
                ->groupBy('tour_id'),
            'r',
            'r.tour_id',
            '=',
            't.id'
        )
        ->whereRaw('t.rating_count <> COALESCE(r.rating_count, 0)')
        ->orWhereRaw('t.rating_avg <> COALESCE(r.rating_avg, 0)')
        ->count(),
    'examples' => array_slice($findings, 0, 30),
];

echo json_encode($summary, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
