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
        throw "Missing audit script: $scriptPath"
    }

    $scriptPathForPhp = ($scriptPath -replace "\\", "/").Replace("'", "\\'")
    php artisan tinker --execute="require '$scriptPathForPhp';"
    if ($LASTEXITCODE -ne 0) {
        throw "Audit failed: $ScriptName"
    }
}

Push-Location $ApiPath
try {
    Write-Host "Step 1/4 - Apply incremental seed manifest" -ForegroundColor Cyan
    powershell -ExecutionPolicy Bypass -File (Join-Path $SeedersPath "apply_database_seeders.ps1") -Mode Incremental -ApiPath $ApiPath

    Write-Host "Step 2/4 - Sync schedule availability" -ForegroundColor Cyan
    php artisan tour-schedules:sync-availability
    if ($LASTEXITCODE -ne 0) {
        throw "Schedule availability sync failed"
    }

    Write-Host "Step 3/4 - Run data quality audits" -ForegroundColor Cyan
    Invoke-TinkerRequire "audit_database_completeness.php"
    Invoke-TinkerRequire "audit_database_coverage.php"
    Invoke-TinkerRequire "audit_public_vietnamese_content.php"
    Invoke-TinkerRequire "audit_locations_vietnamese_detailed.php"
    Invoke-TinkerRequire "audit_vietnamese_diacritics_db.php"
    Invoke-TinkerRequire "audit_mojibake_db.php"
    Invoke-TinkerRequire "audit_tour_schedule_quality.php"
    Invoke-TinkerRequire "audit_ratings_quality.php"
    Invoke-TinkerRequire "audit_operational_activity.php"

    Write-Host "Step 4/4 - Run backend schedule test" -ForegroundColor Cyan
    php artisan test tests\Unit\SyncTourScheduleAvailabilityTest.php

    Write-Host "Done - incremental seed applied, audited, and tested." -ForegroundColor Green
}
finally {
    Pop-Location
}
