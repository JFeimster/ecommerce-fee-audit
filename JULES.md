# JULES.md

## Role

Use Jules for focused implementation tasks, repository cleanup, issue-driven code changes, and static-site improvements.

## Preferred Scope

Good Jules tasks:

- Improve `site/` visual design.
- Refactor vanilla JavaScript safely.
- Add static sections to the landing page.
- Create embed variants.
- Add documentation pages.
- Create repeatable PowerShell scripts.
- Tighten accessibility and mobile layout.

Avoid giving Jules vague product-strategy tasks without a concrete file target.

## Repo Constraints

- Static-first architecture.
- Vercel root directory should remain `site`.
- No build process required unless explicitly approved.
- No private data, customer files, secrets, or financial exports in commits.
- Public language must stay compliance-safe.

## Recommended Jules Prompt

```text
Work in this repo:
https://github.com/JFeimster/ecommerce-fee-audit.vercel.app

Task:
[describe exact change]

Constraints:
- Keep the site static under site/.
- Use vanilla HTML/CSS/JS.
- Preserve existing file names unless a new file is clearly needed.
- Do not add dependencies.
- Do not expose private customer, finance, or credential data.
- Use compliance-safe language around funding, fees, disputes, and AI.

Deliver:
- Summary of changed files.
- Full patch or commit summary.
- Any follow-up work needed.
```

## Review Checklist

- Does the site still work without a build step?
- Do links use the correct relative paths?
- Is the embed still iframe-safe?
- Is the copy direct but not legally reckless?
- Were no secrets or private files added?
