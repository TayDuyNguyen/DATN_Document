param(
    [string]$ApiPath = "D:\DATN\danangtrip-api",
    [string]$SeedersPath = ""
)

$ErrorActionPreference = "Stop"

$DataCenterPath = Split-Path -Parent $PSScriptRoot
$DocsPath = Split-Path -Parent $DataCenterPath
if ([string]::IsNullOrWhiteSpace($SeedersPath)) {
    $SeedersPath = Join-Path $DocsPath "database-seeders"
}

if (-not (Test-Path -LiteralPath (Join-Path $ApiPath "artisan"))) {
    throw "Invalid API path: $ApiPath"
}

if (-not (Test-Path -LiteralPath (Join-Path $SeedersPath "apply_database_seeders.ps1"))) {
    throw "Invalid seeders path: $SeedersPath"
}

function Invoke-TinkerRequire {
    param([string]$ScriptName)

    $scriptPath = Join-Path $SeedersPath $ScriptName
    if (-not (Test-Path -LiteralPath $scriptPath)) {
        throw "Missing script: $scriptPath"
    }

    $scriptPathForPhp = ($scriptPath -replace "\\", "/").Replace("'", "\\'")
    php artisan tinker --execute="require '$scriptPathForPhp';"
    if ($LASTEXITCODE -ne 0) {
        throw "Script failed: $ScriptName"
    }
}

Push-Location $ApiPath
try {
    Write-Host "Step 1/6 - Backup current database before rebuild" -ForegroundColor Cyan
    Invoke-TinkerRequire "backup_full_database_before_reseed.php"

    Write-Host "Step 2/6 - Drop all tables and rerun migrations" -ForegroundColor Cyan
    php artisan migrate:fresh --force

    Write-Host "Step 3/6 - Apply full seed manifest" -ForegroundColor Cyan
    powershell -ExecutionPolicy Bypass -File (Join-Path $SeedersPath "apply_database_seeders.ps1") -Mode Full -ApiPath $ApiPath

    Write-Host "Step 4/6 - Sync schedule availability" -ForegroundColor Cyan
    php artisan tour-schedules:sync-availability
    if ($LASTEXITCODE -ne 0) {
        throw "Schedule availability sync failed"
    }

    Write-Host "Step 5/6 - Run data quality audits" -ForegroundColor Cyan
    Invoke-TinkerRequire "audit_database_completeness.php"
    Invoke-TinkerRequire "audit_database_coverage.php"
    Invoke-TinkerRequire "audit_public_vietnamese_content.php"
    Invoke-TinkerRequire "audit_locations_vietnamese_detailed.php"
    Invoke-TinkerRequire "audit_vietnamese_diacritics_db.php"
    Invoke-TinkerRequire "audit_mojibake_db.php"
    Invoke-TinkerRequire "audit_tour_schedule_quality.php"
    Invoke-TinkerRequire "audit_ratings_quality.php"
    Invoke-TinkerRequire "audit_operational_activity.php"

    Write-Host "Step 6/6 - Run backend schedule test" -ForegroundColor Cyan
    php artisan test tests\Unit\SyncTourScheduleAvailabilityTest.php

    Write-Host "Done - database rebuilt, seeded, audited, and tested." -ForegroundColor Green
}
finally {
    Pop-Location
}
