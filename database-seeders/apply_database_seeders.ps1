param(
    [ValidateSet("Full", "Incremental", "OptionalDemo", "Check")]
    [string]$Mode = "Incremental",

    [string]$ApiPath = "D:\DATN\danangtrip-api",

    [switch]$IncludeOptionalDemo
)

$ErrorActionPreference = "Stop"

$SeederDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ManifestPath = Join-Path $SeederDir "seed-manifest.json"

if (-not (Test-Path -LiteralPath $ManifestPath)) {
    throw "Missing seed manifest: $ManifestPath"
}

if (-not (Test-Path -LiteralPath (Join-Path $ApiPath "artisan"))) {
    throw "Invalid Laravel API path: $ApiPath"
}

$manifest = Get-Content -LiteralPath $ManifestPath -Raw | ConvertFrom-Json

switch ($Mode) {
    "Full" {
        $seedFiles = @($manifest.full)
        if ($IncludeOptionalDemo) {
            $seedFiles += @($manifest.optional_demo)
        }
        Write-Host "Mode Full: use only after migrate:fresh or on an empty database." -ForegroundColor Yellow
    }
    "Incremental" {
        $seedFiles = @($manifest.incremental_current_live)
        Write-Host "Mode Incremental: applies current live DB backfill seeds only." -ForegroundColor Yellow
    }
    "OptionalDemo" {
        $seedFiles = @($manifest.optional_demo)
        Write-Host "Mode OptionalDemo: applies demo/test data only." -ForegroundColor Yellow
    }
    "Check" {
        $seedFiles = @($manifest.read_only_checks)
        Write-Host "Mode Check: runs read-only coverage SQL." -ForegroundColor Yellow
    }
}

if (-not $seedFiles -or $seedFiles.Count -eq 0) {
    throw "No seed files selected for mode $Mode"
}

Push-Location $ApiPath
try {
    foreach ($fileName in $seedFiles) {
        $seedPath = Join-Path $SeederDir $fileName
        if (-not (Test-Path -LiteralPath $seedPath)) {
            throw "Missing seed file: $seedPath"
        }

        $seedPathForPhp = ($seedPath -replace "\\", "/").Replace("'", "\\'")
        $code = "DB::unprepared(file_get_contents('$seedPathForPhp')); echo 'applied: $fileName';"

        Write-Host "Applying $fileName" -ForegroundColor Cyan
        php artisan tinker --execute $code
        if ($LASTEXITCODE -ne 0) {
            throw "Failed applying seed: $fileName"
        }
        Write-Host ""
    }
}
finally {
    Pop-Location
}

Write-Host "Done: $Mode seed run completed." -ForegroundColor Green
