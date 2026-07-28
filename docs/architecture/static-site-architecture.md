# Static Site Architecture

## Decision

Use a static-first architecture for the first public version of Ecommerce Fee Audit.

## Rationale

The current goal is to ship a fast landing page, embed module, and product shell without adding build complexity.

This supports:

- Vercel static deployment
- Wix and WordPress embedding
- fast iteration
- low maintenance
- easy review by AI coding agents

## Public Site Root

```text
site/
```

## Current Static Files

```text
site/index.html
site/styles.css
site/script.js
site/embed.html
site/robots.txt
site/sitemap.xml
site/404.html
site/site.webmanifest
```

## Future Expansion Paths

Add only when needed:

1. `widget/` for deeper interactive calculators or GPT companion widgets.
2. `site/data/` for static JSON configuration.
3. `api/` only when lead capture, HubSpot, Notion, n8n, or authenticated workflows require a backend.
4. Framework migration only if static files become a bottleneck.

## Guardrail

Do not migrate to a framework just because the site may grow. Migrate only when the repo needs routing, components, server-side actions, authenticated state, or CMS integration that static files cannot reasonably support.
