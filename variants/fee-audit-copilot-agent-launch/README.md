# AI Platform Fee Audit Copilot — Launch Site

Premium static launch site for **AI Platform Fee Audit Copilot**.

## Production targets

- Planned production URL: `https://platform-fee-audit.vercel.app/`
- Vercel Root Directory: `site/`
- Active Vercel config: `site/vercel.json`
- Primary CTA: AI Platform Fee Audit Copilot
- Secondary CTA: Distilled Funding finance-operations review

## File tree

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
    ├── images/
    │   └── og-platform-fee-audit.png
    ├── icons/
    │   └── favicon.svg
    └── downloads/
        └── platform-fee-audit-preflight-checklist.txt
```

## Preview locally

No package manager or build step is required.

From the repository root:

```bash
python3 -m http.server 8080 --directory site
```

Open `http://localhost:8080`.

You can also open `site/index.html` directly, but a local server gives more accurate URL and asset behavior.

## Customization

### CTA links

Search these two exact URLs across `site/`:

- `https://chatgpt.com/g/g-6a68083042408191a63f291b0c5a7d9f-ai-platform-fee-audit-copilot`
- `https://www.distilledfunding.com/apply`

### Production URL

The canonical, Open Graph URL, robots sitemap reference, and sitemap currently use:

`https://platform-fee-audit.vercel.app/`

Update all occurrences if the final production domain changes.

### Design tokens

Edit the CSS custom properties at the top of `site/styles.css`:

- `--paper`
- `--ink`
- `--yellow`
- `--orange`
- `--cyan`
- `--pink`
- `--green`
- `--purple`

The site uses system font stacks and requires no external font requests.

## Audit Radar

The home-page router lives in `site/script.js`.

Inputs:

1. Platform
2. Biggest pain
3. Urgency

Output lanes:

- Payout reconciliation
- Fee leakage review
- SKU contribution margin
- Reserve, hold, and dispute tracking

The router runs entirely in the browser. It does not upload files, calculate actual losses, identify account-specific platform errors, perform underwriting, or approve funding.

## Embed module

Public route after deployment:

`https://platform-fee-audit.vercel.app/embed`

Direct file route:

`https://platform-fee-audit.vercel.app/embed.html`

Recommended responsive iframe:

```html
<div style="width:100%;max-width:1200px;margin:0 auto;">
  <iframe
    src="https://platform-fee-audit.vercel.app/embed"
    title="AI Platform Fee Audit Radar"
    loading="lazy"
    style="width:100%;height:900px;border:0;display:block;"
    referrerpolicy="strict-origin-when-cross-origin"
  ></iframe>
</div>
```

The embed:

- Uses scoped `afa-` class names and CSS variables
- Requires no authentication
- Collects no financial files
- Includes noindex/nofollow metadata
- Links to the GPT and review form
- Fits within a 1200px maximum width
- Targets a practical height below 940px on common desktop widths

### Wix

1. Add **Embed Code**.
2. Choose **Embed a site**.
3. Paste the `/embed` URL.
4. Set width to 100% and height near 900px.
5. Check mobile height and remove surrounding page padding when possible.

### WordPress

Use a Custom HTML block and paste the iframe snippet above. Some managed hosts require an administrator role to save iframes.

### Webflow

Add an Embed element and paste the iframe snippet. Set the parent width to 100%.

### Framer

Insert an Embed component, choose URL or HTML, and use the `/embed` route. Set a responsive width and approximately 900px desktop height.

### Carrd

Use an Embed element with the iframe snippet. Iframe support may depend on the Carrd plan.

### Partner blogs or custom HTML

Paste the iframe snippet in the article or sidebar template. The module does not depend on the parent site's CSS or JavaScript.

## Vercel deployment

1. Import or open the GitHub repository in Vercel.
2. Set **Root Directory** to `site/`.
3. Leave Framework Preset as **Other**.
4. Do not add a root-level `vercel.json`.
5. No Build Command is required.
6. No Output Directory override is required.
7. Confirm the production domain is `platform-fee-audit.vercel.app`.
8. Keep automatic preview deployments disabled if that is the existing project policy.
9. Use the project's manual production deployment flow.
10. After deployment, verify `/`, `/embed`, `/404.html`, `/robots.txt`, `/sitemap.xml`, and the asset URLs.

`site/vercel.json` provides clean URLs, cache headers for assets, security headers, and noindex headers for the embed. It intentionally does not set `X-Frame-Options`, because the embed must work on approved partner sites.

## Other static hosting

### Netlify

Deploy the `site/` directory as the publish directory. Clean URLs and headers may need equivalent Netlify configuration.

### GitHub Pages

Publish the contents of `site/`. Relative links work, but the canonical and Open Graph URLs must be changed to the final GitHub Pages domain.

### Static file host

Upload the contents of `site/` while preserving the folder structure. Configure `404.html` as the not-found page where supported.

## Privacy boundary

The public site and embed do not collect raw financial exports.

Never request or expose:

- Passwords
- API keys
- Session tokens or authentication cookies
- Full card numbers or CVV codes
- Bank login credentials
- Social Security numbers
- Unredacted customer payment data

A secure, explicitly approved upload workflow would be required before file collection is added.

## Compliance boundary

The copy uses non-guaranteed language such as “designed to help,” “may help,” and “can support.” It does not promise fee recovery, dispute success, funding approval, same-day funding, tax treatment, eligibility, or terms.
