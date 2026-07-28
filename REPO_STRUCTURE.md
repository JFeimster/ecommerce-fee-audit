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
│   └── brand/
├── docs/
├── knowledge/
├── scripts/
├── site/
│   └── assets/
│       ├── images/
│       ├── icons/
│       └── downloads/
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

## assets/

Root `assets/` is for source/design/internal working assets only.

```text
assets/
└── brand/
```

Use `assets/brand/` for editable brand files, source graphics, working design exports, and non-site creative references.

Do not add duplicate root folders such as:

```text
assets/images/
assets/icons/
assets/downloads/
```

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
- `vercel.json`: Vercel config, because Vercel root is `site`

## site/assets/

Use this for files that need to load from the live site.

```text
site/assets/
├── images/     Public site images
├── icons/      Favicons, UI marks, badges, and SVG icons
└── downloads/  Public-safe PDFs, CSV templates, and lead magnets
```

Public URL examples after deployment:

```text
/assets/images/hero.png
/assets/icons/favicon.svg
/assets/downloads/platform-fee-audit-checklist.pdf
```

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
