# Vercel Deployment

## Recommended Settings

- Repository: `JFeimster/ecommerce-fee-audit.vercel.app`
- Production branch: `main`
- Root directory: `site`
- Framework preset: Other
- Build command: leave empty
- Install command: leave empty
- Output directory: leave empty

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

## Deployment Control

If `vercel.json` has Git deployments disabled, temporarily set production deployment to enabled only when intentionally deploying from `main`.

After production verification, disable preview deploys again if the project requires manual deployment control.

## QA Checklist

- Home page loads.
- Embed page loads.
- CSS and JS paths resolve.
- Mobile layout does not overflow.
- CTA links point to the intended Moonshine / Distilled Funding destination.
- No private files or test customer data are publicly served.
- Footer disclaimer is visible.
