$ErrorActionPreference='Stop'; node (Join-Path $PSScriptRoot 'check-secrets.js'); exit $LASTEXITCODE
