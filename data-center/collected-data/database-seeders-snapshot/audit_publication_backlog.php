<?php

$out = [
    'generated_at' => now()->toIso8601String(),
    'summary' => [
        'locations_pending_review' => DB::table('locations')->where('status', 'pending_review')->count(),
        'tours_pending_review' => DB::table('tours')->where('status', 'pending_review')->count(),
        'blog_posts_draft' => DB::table('blog_posts')->where('status', 'draft')->count(),
    ],
    'locations_pending_review' => DB::table('locations')
        ->where('status', 'pending_review')
        ->select('id', 'name', 'slug')
        ->orderBy('id')
        ->get(),
    'tours_pending_review' => DB::table('tours')
        ->where('status', 'pending_review')
        ->select('id', 'name', 'slug')
        ->orderBy('id')
        ->get(),
    'blog_posts_draft' => DB::table('blog_posts')
        ->where('status', 'draft')
        ->select('id', 'title', 'slug')
        ->orderBy('id')
        ->get(),
];

$reportDir = 'D:/DATN/DATN_Tài liệu/data-center/reports';
if (! is_dir($reportDir)) {
    mkdir($reportDir, 0777, true);
}

$reportPath = $reportDir . '/publication-backlog-' . now()->format('Y-m-d-His') . '.json';
file_put_contents($reportPath, json_encode($out, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));

echo json_encode([
    'report_path' => $reportPath,
    'summary' => $out['summary'],
], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
