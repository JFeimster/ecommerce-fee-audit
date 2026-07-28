# Site Assets

Place public static site assets here.

## Folder Map

```text
site/assets/
├── images/     Public-safe site images and graphics
├── icons/      Favicons, UI marks, product icons, and platform badges
├── downloads/  Public-safe PDFs, CSV templates, and lead magnets
├── css/        Optional future split CSS files
└── js/         Optional future split JavaScript files
```

## Practical Rule

- If a file needs to load from the live site, save it under `site/assets/`.
- If a file is a source/design/internal working asset, save it under root `assets/`.

## Public URL Patterns

```text
/assets/images/file-name.ext
/assets/icons/file-name.ext
/assets/downloads/file-name.ext
```

## Rules

- Do not store private client exports, raw platform data, credentials, API keys, bank data, or real financial records in this folder.
- Use fictional examples only when public sample files are needed.
- Keep production site files static-first and Vercel-friendly.
- Put the primary CSS and JavaScript at `site/styles.css` and `site/script.js` unless the site grows enough to justify splitting assets.
