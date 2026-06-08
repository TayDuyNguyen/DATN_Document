param(
    [string]$ApiPath = "D:\DATN\danangtrip-api",
    [string]$SeedersPath = ""
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath (Join-Path $ApiPath "artisan"))) {
    throw "Invalid API path: $ApiPath"
}

$DataCenterPath = Split-Path -Parent $PSScriptRoot
$DocsPath = Split-Path -Parent $DataCenterPath
if ([string]::IsNullOrWhiteSpace($SeedersPath)) {
    $SeedersPath = Join-Path $DocsPath "database-seeders"
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
    Write-Host "Sync - tour schedule availability" -ForegroundColor Cyan
    php artisan tour-schedules:sync-availability
    if ($LASTEXITCODE -ne 0) {
        throw "Schedule availability sync failed"
    }

    Write-Host "Audit - database completeness" -ForegroundColor Cyan
    Invoke-TinkerRequire "audit_database_completeness.php"

    Write-Host "Audit - database coverage" -ForegroundColor Cyan
    Invoke-TinkerRequire "audit_database_coverage.php"

    Write-Host "Audit - public Vietnamese content" -ForegroundColor Cyan
    Invoke-TinkerRequire "audit_public_vietnamese_content.php"

    Write-Host "Audit - detailed location Vietnamese content" -ForegroundColor Cyan
    Invoke-TinkerRequire "audit_locations_vietnamese_detailed.php"

    Write-Host "Audit - Vietnamese diacritics" -ForegroundColor Cyan
    Invoke-TinkerRequire "audit_vietnamese_diacritics_db.php"

    Write-Host "Audit - mojibake" -ForegroundColor Cyan
    Invoke-TinkerRequire "audit_mojibake_db.php"

    Write-Host "Audit - tour schedule quality" -ForegroundColor Cyan
    Invoke-TinkerRequire "audit_tour_schedule_quality.php"

    Write-Host "Audit - ratings quality" -ForegroundColor Cyan
    Invoke-TinkerRequire "audit_ratings_quality.php"

    Write-Host "Audit - operational activity" -ForegroundColor Cyan
    Invoke-TinkerRequire "audit_operational_activity.php"

    Write-Host "Done - audit completed." -ForegroundColor Green
}
finally {
    Pop-Location
}
