# AGENTS.md

## Mission

Build and maintain the **Ecommerce Fee Audit** repo as a static-site, embed, and knowledge-library system for the AI Platform Fee Audit Copilot.

The product exists to help ecommerce operators understand platform settlements, payout timing, processor fees, marketplace deductions, reserves, disputes, SKU contribution margin, and funding-readiness gaps.

## Operating Priorities

1. Preserve the reconciliation-first model.
2. Keep the public site static and Vercel-friendly.
3. Keep embed files portable for Wix, WordPress, partner pages, and simple iframes.
4. Keep knowledge files readable, versioned, and safe for Custom GPT upload.
5. Do not invent funding, lending, fee, tax, accounting, or platform-policy claims.

## Repository Map

```text
site/          Public Vercel site. Root directory for deployment.
widget/        Future embeddable audit widgets and calculators.
knowledge/     GPT knowledge files, product models, sales, and implementation docs.
docs/          Architecture, deployment, and operations documentation.
scripts/       Local maintenance and PowerShell automation.
assets/        Brand and downloadable assets.
```

## Compliance Boundaries

Do not say or imply:

- guaranteed fee recovery
- guaranteed funding approval
- guaranteed savings
- tax, legal, accounting, or underwriting advice
- Moonshine Capital is a bank
- AI replaces professional judgment

Use:

- may help
- can support
- designed to help
- eligibility varies
- terms may change
- not a guarantee
- subject to review

## Static Site Rules

- Keep `site/` deployable without npm, build tools, React, or framework assumptions unless explicitly changed.
- Use relative links where practical.
- Do not add external dependencies casually.
- Keep `site/embed.html` iframe-friendly.
- Keep CSS in `site/styles.css` and behavior in `site/script.js`.

## Data and Privacy Rules

Never commit:

- real bank exports
- real payout files
- API keys
- OAuth secrets
- customer data
- unredacted screenshots
- private financial statements
- lender credentials

Use fictional examples only.

## Recommended Agent Workflow

1. Read `PROJECT_CONTEXT.md`.
2. Read `REPO_STRUCTURE.md`.
3. Confirm whether the task affects `site/`, `knowledge/`, `widget/`, or root tooling.
4. Make the smallest coherent change.
5. Preserve existing file names and cross-references.
6. Run local static checks when possible.
7. Summarize changed files and deployment impact.
