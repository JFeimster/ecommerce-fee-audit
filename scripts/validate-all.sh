#!/usr/bin/env sh
python .github/scripts/validate_knowledge.py
node scripts/check-secrets.js
*** Add File: docs/security/security-architecture.md
# Security Architecture

Controls are provisional, fail closed, and prohibit live credentials, funding/dispute submission, and financial transactions.
