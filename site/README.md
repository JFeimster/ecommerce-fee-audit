# Site

Vercel-ready public site files belong here.

## Recommended Deployment Configuration

- Vercel Root Directory: `site`
- Framework Preset: Other
- Build Command: none
- Output Directory: none
- Install Command: none
- Vercel config file: `site/vercel.json`

## Primary Files

```text
site/
├── index.html
├── embed.html
├── styles.css
├── script.js
├── 404.html
├── robots.txt
├── sitemap.xml
├── site.webmanifest
├── vercel.json
└── assets/
    ├── downloads/
    ├── icons/
    ├── css/
    ├── js/
    └── images/
```

## Design Direction

Default site style: neo-brutalist fintech.

Use:

- Heavy black borders
- Hard shadows
- High-contrast cards
- Warm paper background
- Loud accent colors
- Plain HTML, CSS, and vanilla JavaScript
- No required build tools

## Asset Rules

Keep public site assets safe. Do not place private client data, platform exports, bank files, API keys, or raw financial records anywhere under `site/`.
