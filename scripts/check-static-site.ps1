#requires -Version 5.1
<#
.SYNOPSIS
Local static-site sanity check for the Ecommerce Fee Audit repo.

.DESCRIPTION
Checks that required static site files exist and that the core HTML files reference the shared CSS and JS files.
#>

[CmdletBinding()]
param(
    [string]$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
)

$ErrorActionPreference = "Stop"
$SiteRoot = Join-Path $ProjectRoot "site"

$RequiredFiles = @(
    "index.html",
    "styles.css",
    "script.js",
    "embed.html",
    "robots.txt",
    "sitemap.xml",
    "404.html",
    "site.webmanifest"
)

$BatchSevenFiles = @(
    "app/index.html", "app/styles.css", "app/app.js", "app/config.js", "app/README.md",
    "embed/platform-fee-audit-widget.html", "embed/platform-fee-audit-widget.css", "embed/platform-fee-audit-widget.js", "embed/README.md",
    "data/public-product-catalog.json", "data/public-connector-catalog.json", "data/public-fee-taxonomy.json", "data/sample-audit-summary.json",
    "pages/getting-started.html", "pages/privacy-and-safe-uploads.html", "pages/supported-data-sources.html", "pages/audit-process.html", "pages/pricing-and-access.html", "pages/dispute-workflow.html", "pages/funding-readiness.html"
)

Write-Host "Checking static site at: $SiteRoot" -ForegroundColor Cyan

foreach ($File in $RequiredFiles) {
    $Path = Join-Path $SiteRoot $File
    if (-not (Test-Path -LiteralPath $Path)) {
        throw "Missing required site file: $File"
    }
    Write-Host "OK: $File" -ForegroundColor Green
}

foreach ($File in $BatchSevenFiles) {
    $Path = Join-Path $SiteRoot $File
    if (-not (Test-Path -LiteralPath $Path)) {
        throw "Missing Batch 7 static file: $File"
    }
    Write-Host "OK: $File" -ForegroundColor Green
}

$Index = Get-Content -LiteralPath (Join-Path $SiteRoot "index.html") -Raw
$Embed = Get-Content -LiteralPath (Join-Path $SiteRoot "embed.html") -Raw

if ($Index -notmatch 'styles\.css') { throw "index.html does not reference styles.css" }
if ($Index -notmatch 'script\.js') { throw "index.html does not reference script.js" }
if ($Embed -notmatch 'styles\.css') { throw "embed.html does not reference styles.css" }
if ($Embed -notmatch 'script\.js') { throw "embed.html does not reference script.js" }

$App = Get-Content -LiteralPath (Join-Path $SiteRoot "app/index.html") -Raw
if ($App -notmatch 'styles\.css') { throw "app/index.html does not reference styles.css" }
if ($App -notmatch 'config\.js' -or $App -notmatch 'app\.js') { throw "app/index.html does not reference app JavaScript" }

foreach ($DataFile in @("public-product-catalog.json", "public-connector-catalog.json", "public-fee-taxonomy.json", "sample-audit-summary.json")) {
    try { Get-Content -LiteralPath (Join-Path $SiteRoot "data/$DataFile") -Raw | ConvertFrom-Json | Out-Null }
    catch { throw "Invalid public JSON: $DataFile" }
}

if (Test-Path -LiteralPath (Join-Path $SiteRoot "api")) { throw "Batch 7 must not create site/api routes" }

Write-Host "Static site check passed." -ForegroundColor Green
