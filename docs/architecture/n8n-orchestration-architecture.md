# n8n Orchestration Architecture

n8n is an inactive, contract-only orchestration layer. Workflows call only the established shared routes and slots 2–9; provider traffic ultimately enters `/api/webhooks/{provider}` on slot 8. The registry defines execution modes, credential placeholders, idempotency, retry/dead-letter controls, funding/dispute safeguards, Wix entitlement synchronization, and CRM/Notion handoffs. No workflow is activated or credentialed.
