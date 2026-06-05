<?php

$tables = collect(DB::select(
    "select table_name
     from information_schema.tables
     where table_schema = current_schema()
       and table_type = 'BASE TABLE'
     order by table_name"
))->pluck('table_name');

$counts = [];
foreach ($tables as $table) {
    try {
        $counts[$table] = DB::table($table)->count();
    } catch (Throwable $exception) {
        $counts[$table] = [
            'error' => $exception->getMessage(),
        ];
    }
}

echo json_encode($counts, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
