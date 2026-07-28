# Vercel Deployment

## Recommended Settings

- Repository: `JFeimster/ecommerce-fee-audit.vercel.app`
- Production branch: `main`
- Root directory: `site`
- Framework preset: Other
- Build command: leave empty
- Install command: leave empty
- Output directory: leave empty
- Vercel config file: `site/vercel.json`

## Expected URL

```text
https://ecommerce-fee-audit.vercel.app
```

## Static Files

Vercel should serve these directly from `site/`:

- `/index.html`
- `/styles.css`
- `/script.js`
- `/embed.html`
- `/robots.txt`
- `/sitemap.xml`
- `/404.html`
- `/site.webmanifest`
- `/assets/icons/`
- `/assets/downloads/`

## Deployment Control

The active Vercel configuration now lives at:

```text
site/vercel.json
```

The current configuration disables Git deployments for every branch except `main`:

```json
"deploymentEnabled": {
  "*": false,
  "main": true
}
```

Change these settings only through an intentional deployment-control decision. This repository uses `site/vercel.json`; there is no repository-root `vercel.json`.

## QA Checklist

- Home page loads.
- Embed page loads.
- CSS and JS paths resolve.
- Mobile layout does not overflow.
- CTA links point to the intended Moonshine / Distilled Funding destination.
- No private files or test customer data are publicly served.
- Footer disclaimer is visible.
- `site/assets/icons/` contains only public-safe assets.
- `site/assets/downloads/` contains only public-safe downloads.
