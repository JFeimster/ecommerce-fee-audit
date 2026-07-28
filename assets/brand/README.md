# Brand Assets

Use this root-level folder for source/design/internal brand assets that are not directly served by the public Vercel site.

Recommended assets:

- editable logo/source files
- Canva/Figma export notes
- brand references
- working design files
- non-site screenshots
- internal creative concepts

Path rule:

```text
assets/brand/
```

Do not use this folder for files that the live site must load. If an asset needs a public URL on the deployed site, place it under:

```text
site/assets/
```

Do not store client financial data, raw platform exports, credentials, API keys, or sensitive customer information here.
