# Wix Commercial Architecture

Moonshine Capital Wix is the proposed commercial, checkout, member-access, CRM, forms, Groups, Bookings, and lifecycle layer. Vercel remains the app/dashboard layer; Notion remains internal operations only. All mappings are contract-only and must be configured draft-first.

Verified Wix events enter `/api/webhooks/{provider}` as provider `wix` on function slot 8. They create idempotent entitlement updates, roles, labels, onboarding tasks, and dashboard handoff eligibility. No public checkout grants internal roles. Groups provide education and community, never the audit database.

Pricing is inherited from the canonical Batch 1 catalog: every value is explicitly provisional, founding-member, placeholder, or not applicable until commercial approval. Managed services use application/proposal/invoice workflows, not self-service checkout.
