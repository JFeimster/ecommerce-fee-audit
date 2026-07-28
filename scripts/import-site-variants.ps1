#requires -Version 5.1
<#[
.SYNOPSIS
Imports the ChatGPT Sites and Agent Launch Site Builder ZIP packages into /variants.

.DESCRIPTION
- Preserves /site as the canonical production source.
- Imports ChatGPT Sites into variants/platform-fee-audit-chatgpt-site.
- Flattens the Agent Launch package's internal site/ folder into
  variants/fee-audit-copilot-agent-launch.
- Rejects common secret files and scans text for obvious live credentials.
- Optionally commits and pushes the imported files.
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [string]$ChatGptSiteZip,

    [Parameter(Mandatory)]
    [string]$AgentLaunchZip,

    [string]$RepoRoot = "C:\Users\jason\OneDrive\Desktop\The Prompt Lab\AI Platform Fee Audit Copilot",

    [switch]$CommitAndPush
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Write-Step([string]$Message) {
    Write-Host "`n==> $Message" -ForegroundColor Cyan
}

function Assert-File([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        throw "File not found: $Path"
    }
}

function Remove-UnsafeEntries([string]$Root) {
    $blockedNames = @(
        '.git', '.vercel', 'node_modules', '.env', '.env.local',
        '.env.production', '.env.development', 'credentials', 'secrets'
    )

    Get-ChildItem -LiteralPath $Root -Recurse -Force | Where-Object {
        $blockedNames -contains $_.Name
    } | Sort-Object FullName -Descending | ForEach-Object {
        Remove-Item -LiteralPath $_.FullName -Recurse -Force
    }
}

function Test-ForSecrets([string]$Root) {
    $patterns = @(
        'https://api\.vercel\.com/v1/integrations/deploy/',
        'gh[pousr]_[A-Za-z0-9_]{20,}',
        'sk-[A-Za-z0-9_-]{20,}',
        '(?im)^\s*[A-Z0-9_]*(SECRET|TOKEN|API_KEY|PASSWORD|PRIVATE_KEY)[A-Z0-9_]*\s*=\s*\S+'
    )

    $textExtensions = @('.html', '.css', '.js', '.json', '.xml', '.txt', '.md', '.svg', '.yml', '.yaml')
    $hits = @()

    Get-ChildItem -LiteralPath $Root -Recurse -File -Force | Where-Object {
        $textExtensions -contains $_.Extension.ToLowerInvariant()
    } | ForEach-Object {
        $content = Get-Content -LiteralPath $_.FullName -Raw -ErrorAction SilentlyContinue
        foreach ($pattern in $patterns) {
            if ($content -match $pattern) {
                $hits += $_.FullName
                break
            }
        }
    }

    if ($hits.Count -gt 0) {
        throw "Potential secret material detected:`n$($hits -join "`n")"
    }
}

Assert-File $ChatGptSiteZip
Assert-File $AgentLaunchZip

if (-not (Test-Path -LiteralPath $RepoRoot -PathType Container)) {
    throw "Repository root not found: $RepoRoot"
}

$variantsRoot = Join-Path $RepoRoot 'variants'
$chatTarget = Join-Path $variantsRoot 'platform-fee-audit-chatgpt-site'
$agentTarget = Join-Path $variantsRoot 'fee-audit-copilot-agent-launch'
$tempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("ecommerce-fee-audit-variants-" + [guid]::NewGuid())
$chatTemp = Join-Path $tempRoot 'chatgpt-site'
$agentTemp = Join-Path $tempRoot 'agent-launch'

try {
    Write-Step 'Extracting uploaded archives'
    New-Item -ItemType Directory -Path $chatTemp, $agentTemp -Force | Out-Null
    Expand-Archive -LiteralPath $ChatGptSiteZip -DestinationPath $chatTemp -Force
    Expand-Archive -LiteralPath $AgentLaunchZip -DestinationPath $agentTemp -Force

    Remove-UnsafeEntries $chatTemp
    Remove-UnsafeEntries $agentTemp
    Test-ForSecrets $chatTemp
    Test-ForSecrets $agentTemp

    Write-Step 'Locating package roots'
    $chatPackage = Get-ChildItem -LiteralPath $chatTemp -Directory | Select-Object -First 1
    $agentPackage = Get-ChildItem -LiteralPath $agentTemp -Directory | Select-Object -First 1

    if (-not $chatPackage) { throw 'ChatGPT Sites package root was not found.' }
    if (-not $agentPackage) { throw 'Agent Launch package root was not found.' }

    $agentSite = Join-Path $agentPackage.FullName 'site'
    if (-not (Test-Path -LiteralPath $agentSite -PathType Container)) {
        throw "Expected Agent Launch site folder not found: $agentSite"
    }

    Write-Step 'Replacing variant folders only'
    New-Item -ItemType Directory -Path $variantsRoot -Force | Out-Null
    Remove-Item -LiteralPath $chatTarget -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item -LiteralPath $agentTarget -Recurse -Force -ErrorAction SilentlyContinue
    New-Item -ItemType Directory -Path $chatTarget, $agentTarget -Force | Out-Null

    Copy-Item -Path (Join-Path $chatPackage.FullName '*') -Destination $chatTarget -Recurse -Force

    # Preserve Agent Launch documentation at the variant root.
    foreach ($doc in @('README.md', 'BUILD-NOTES.md')) {
        $source = Join-Path $agentPackage.FullName $doc
        if (Test-Path -LiteralPath $source) {
            Copy-Item -LiteralPath $source -Destination (Join-Path $agentTarget $doc) -Force
        }
    }

    # Flatten the package's site/ contents into the semantic variant root.
    Copy-Item -Path (Join-Path $agentSite '*') -Destination $agentTarget -Recurse -Force

    Test-ForSecrets $chatTarget
    Test-ForSecrets $agentTarget

    Write-Step 'Verifying required variant files'
    $required = @(
        (Join-Path $chatTarget 'index.html'),
        (Join-Path $chatTarget 'styles.css'),
        (Join-Path $chatTarget 'script.js'),
        (Join-Path $agentTarget 'index.html'),
        (Join-Path $agentTarget 'styles.css'),
        (Join-Path $agentTarget 'script.js'),
        (Join-Path $agentTarget 'embed.html')
    )

    foreach ($file in $required) {
        Assert-File $file
    }

    Write-Host "`nImported:" -ForegroundColor Green
    Write-Host "  $chatTarget"
    Write-Host "  $agentTarget"
    Write-Host "`nCanonical production folder was not modified: $(Join-Path $RepoRoot 'site')" -ForegroundColor Green

    if ($CommitAndPush) {
        Write-Step 'Committing and pushing variants'
        Push-Location $RepoRoot
        try {
            & git add -- variants scripts/import-site-variants.ps1
            & git diff --cached --quiet
            if ($LASTEXITCODE -ne 0) {
                & git commit -m 'Add ChatGPT Sites and Agent Launch site variants'
                if ($LASTEXITCODE -ne 0) { throw 'Git commit failed.' }
                & git push origin main
                if ($LASTEXITCODE -ne 0) { throw 'Git push failed.' }
            }
            else {
                Write-Host 'No variant changes were available to commit.' -ForegroundColor Yellow
            }
        }
        finally {
            Pop-Location
        }
    }
}
finally {
    Remove-Item -LiteralPath $tempRoot -Recurse -Force -ErrorAction SilentlyContinue
}
