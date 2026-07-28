# Build Notes and QA

## Positioning decisions

- The site is framed as an ecommerce finance-operations audit engine, not a chatbot, bookkeeping app, reimbursement offer, or approval funnel.
- The hero leads with the distinction between gross sales, payouts, cash, and profit.
- The workflow follows the control order: reconcile, classify, calculate, diagnose, act.
- Illustrative UI avoids fabricated customer numbers, testimonials, logos, or outcomes.
- Funding is positioned only after the margin and cash-timing audit.

## CTA verification

Verified public targets used in the build:

- GPT: `https://chatgpt.com/g/g-6a68083042408191a63f291b0c5a7d9f-ai-platform-fee-audit-copilot`
- Review: `https://www.distilledfunding.com/apply`

## Relative-link verification

Local links use relative paths:

- `./styles.css`
- `./script.js`
- `./site.webmanifest`
- `./embed.html`
- `./assets/icons/favicon.svg`
- `./assets/images/og-platform-fee-audit.png`
- `./assets/downloads/platform-fee-audit-preflight-checklist.txt`
- `./`

The canonical and Open Graph URLs are intentionally absolute.

## Responsive QA checklist

- [ ] 390px: no horizontal overflow; buttons stack; nav opens and closes; select fields fit.
- [ ] 430px: hero dashboard fits; offer ribbons do not clip; footer links wrap.
- [ ] Tablet: two-column cards align; router result remains readable.
- [ ] Laptop: sticky navigation fits without wrapping.
- [ ] Wide desktop: content remains capped at 1200px and does not become sparse.
- [ ] Embed at 320px, 390px, 430px, 768px, and 1200px.
- [ ] Reduced-motion setting disables marquee movement.
- [ ] Zoom to 200% and confirm content reflows without horizontal scrolling.

## Accessibility checklist

- [x] Semantic header, nav, main, section, form, and footer landmarks.
- [x] Skip link.
- [x] Visible keyboard focus.
- [x] Programmatic labels for all router controls.
- [x] Required form controls use native validation.
- [x] Router result uses `aria-live`.
- [x] Mobile navigation exposes `aria-expanded`.
- [x] Escape closes mobile navigation.
- [x] FAQ buttons expose expanded state.
- [x] Decorative elements are hidden where appropriate.
- [ ] Manual screen-reader pass in VoiceOver, NVDA, or JAWS.
- [ ] Manual contrast audit in browser DevTools or axe.
- [ ] Keyboard-only pass after production deployment.

## Assumptions

1. The planned Variation 2 domain, `platform-fee-audit.vercel.app`, replaces the older suggested canonical from Variation 1.
2. The Vercel project will continue using `site/` as Root Directory.
3. Automatic preview deployments remain disabled in Vercel project settings; this cannot be enforced by the static files.
4. No financial-file upload is included.
5. No analytics, CRM, form embed, secure data room, or authenticated workflow is approved yet.
6. The product ladder has no public pricing supplied, so the site presents responsibility, cadence, scope, and deliverables without invented prices.
7. Platform names are plain-text coverage labels, not implied partnerships.
8. The current public GPT and review URLs remain the approved CTA targets.

## Unresolved dependencies

- Final confirmation that `platform-fee-audit.vercel.app` is assigned to the intended Vercel project.
- Final production deployment through the connected Vercel account.
- Optional secure upload architecture, data-retention policy, consent language, and vendor review before collecting financial files.
- Optional analytics ID and consent requirements.
- Optional scheduling or CRM endpoint for DWY/DFY intake.
- Any approved brand marks or downloadable templates from the private Drive/Notion library.
- Final legal review of service terms, privacy policy, and data processing if managed services are activated.

## Connector and deployment limitation

The connected GitHub, Vercel, Notion, and Google Drive plugins were not available to the build session. Public repository, live-site, GPT, Notion, and review URLs were inspected where accessible, but:

- No GitHub commit or pull request was created.
- No Vercel project setting or deployment was changed.
- The existing `site/vercel.json` could not be retrieved byte-for-byte through the unavailable connector; the delivered file is a complete static-site configuration rebuilt from the stated requirements.
- Private or connector-gated Google Drive assets were not imported.
- Production ownership, Root Directory, manual deployment controls, and domain assignment require confirmation in the connected accounts.
