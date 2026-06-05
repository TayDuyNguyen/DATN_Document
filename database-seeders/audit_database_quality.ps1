param(
    [string]$ApiPath = "D:\DATN\danangtrip-api"
)

$ErrorActionPreference = "Stop"

$SeederDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$AuditPhp = Join-Path $SeederDir "audit_database_quality.php"

if (-not (Test-Path -LiteralPath (Join-Path $ApiPath "artisan"))) {
    throw "Invalid Laravel API path: $ApiPath"
}

if (-not (Test-Path -LiteralPath $AuditPhp)) {
    throw "Missing audit PHP file: $AuditPhp"
}

$AuditPhpForPhp = ($AuditPhp -replace "\\", "/").Replace("'", "\\'")
$code = "require '$AuditPhpForPhp';"

Push-Location $ApiPath
try {
    php artisan tinker --execute $code
    if ($LASTEXITCODE -ne 0) {
        throw "Database audit failed."
    }
}
finally {
    Pop-Location
}
