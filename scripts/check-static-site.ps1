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

Write-Host "Checking static site at: $SiteRoot" -ForegroundColor Cyan

foreach ($File in $RequiredFiles) {
    $Path = Join-Path $SiteRoot $File
    if (-not (Test-Path -LiteralPath $Path)) {
        throw "Missing required site file: $File"
    }
    Write-Host "OK: $File" -ForegroundColor Green
}

$Index = Get-Content -LiteralPath (Join-Path $SiteRoot "index.html") -Raw
$Embed = Get-Content -LiteralPath (Join-Path $SiteRoot "embed.html") -Raw

if ($Index -notmatch 'styles\.css') { throw "index.html does not reference styles.css" }
if ($Index -notmatch 'script\.js') { throw "index.html does not reference script.js" }
if ($Embed -notmatch 'styles\.css') { throw "embed.html does not reference styles.css" }
if ($Embed -notmatch 'script\.js') { throw "embed.html does not reference script.js" }

Write-Host "Static site check passed." -ForegroundColor Green
