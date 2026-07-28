# GitHub Copilot Instructions

This repository supports the Ecommerce Fee Audit static site, embed layer, and AI Platform Fee Audit Copilot knowledge system.

## Default Architecture

- Public deploy root: `site/`
- Default stack: static HTML, CSS, and vanilla JavaScript
- No framework unless explicitly requested
- No external dependencies unless explicitly justified

## Product Context

The product helps ecommerce operators understand:

- platform settlements
- payout reconciliation
- processor and marketplace fees
- reserves and holds
- refunds and disputes
- SKU contribution margin
- cash-timing gaps
- funding-readiness documentation

## Copy Rules

Use direct, practical, compliance-safe language. Do not guarantee fee recovery, funding approval, savings, income, or underwriting outcomes.

## Privacy Rules

Do not suggest committing real financial exports, bank statements, customer data, API keys, credentials, or private screenshots.

## Coding Rules

- Prefer full, readable files over clever abstractions.
- Keep paths relative inside `site/`.
- Keep `embed.html` iframe-friendly.
- Keep JavaScript small and dependency-free.
- Preserve accessibility basics: semantic HTML, labels, contrast, and keyboard-friendly links/buttons.
