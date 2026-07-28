$ErrorActionPreference='Stop'; python .github/scripts/validate_knowledge.py; & (Join-Path $PSScriptRoot 'check-static-site.ps1'); node (Join-Path $PSScriptRoot 'check-secrets.js'); exit $LASTEXITCODE
