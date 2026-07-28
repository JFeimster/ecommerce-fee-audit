# Repository Structure

```text
.
├── AGENTS.md
├── CODEX.md
├── CURSOR.md
├── JULES.md
├── POWERSHELL.md
├── PROJECT_CONTEXT.md
├── REPO_STRUCTURE.md
├── README.md
├── assets/
├── docs/
├── knowledge/
├── scripts/
├── site/
└── widget/
```

## Root Files

Root-level instruction files are for tools and humans that need global repository context.

- `AGENTS.md`: universal agent rules
- `CODEX.md`: Codex-specific workflow
- `JULES.md`: Jules-specific workflow
- `CURSOR.md`: Cursor local-edit workflow
- `POWERSHELL.md`: Windows / PowerShell local-ops workflow
- `PROJECT_CONTEXT.md`: business and product context
- `REPO_STRUCTURE.md`: source map

## site/

Public static site root for Vercel.

- `index.html`: main public page
- `styles.css`: shared styles
- `script.js`: light interaction and event hooks
- `embed.html`: iframe-friendly embed module
- `robots.txt`: crawler rules
- `sitemap.xml`: basic sitemap
- `404.html`: static not-found page
- `site.webmanifest`: lightweight app metadata

## knowledge/

Knowledge library for GPT behavior, product packaging, sales docs, and implementation guides.

Recommended subfolders:

```text
knowledge/business-models/
knowledge/products/
knowledge/sales/
knowledge/implementation/
```

## widget/

Use this for deeper embeddable calculators, scorecards, GPT companion widgets, and iframe assets that should be versioned separately from the main site page.

## docs/

Use this for implementation notes, Vercel deployment instructions, architecture records, and operational runbooks.

## scripts/

Use this for repeatable maintenance scripts. Prefer PowerShell for local Windows workflows unless another runtime is explicitly required.
