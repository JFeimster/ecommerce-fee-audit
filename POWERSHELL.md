# POWERSHELL.md

## Purpose

PowerShell is the default local automation layer for this Windows / OneDrive project.

Use it for:

- scaffolding files
- syncing local changes
- creating backups
- checking repository status
- pushing to GitHub
- preparing Vercel-ready static assets

## Local Project Path

```powershell
$ProjectRoot = "C:\Users\jason\OneDrive\Desktop\The Prompt Lab\AI Platform Fee Audit Copilot"
```

## GitHub Remote

```powershell
$RepoUrl = "https://github.com/JFeimster/ecommerce-fee-audit.vercel.app.git"
```

## Safe Start

```powershell
Set-Location $ProjectRoot
git status --short --branch
git remote -v
```

## Create Backup Before Big Changes

```powershell
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$BackupRoot = Join-Path (Split-Path $ProjectRoot -Parent) "_project-backups"
New-Item -ItemType Directory -Force -Path $BackupRoot | Out-Null
Compress-Archive -Path (Join-Path $ProjectRoot "*") -DestinationPath (Join-Path $BackupRoot "AI-Platform-Fee-Audit-Copilot-$Stamp.zip") -Force
```

## Commit and Push

```powershell
Set-Location $ProjectRoot
git add --all
git status --short
git commit -m "Describe the change"
git push origin main
```

## Static Site Local Check

```powershell
Start-Process (Join-Path $ProjectRoot "site\index.html")
Start-Process (Join-Path $ProjectRoot "site\embed.html")
```

## Do Not Commit

- `.env` files
- credentials
- platform API keys
- private exports
- real customer bank or payout files
- unredacted screenshots
- client data
- lender credentials

## Vercel Reminder

Set Vercel Root Directory to:

```text
site
```

If `vercel.json` disables deployments, change `main` to `true` only when intentionally allowing production deployments, then turn it back off if desired.
