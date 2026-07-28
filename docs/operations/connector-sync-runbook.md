# Connector Sync Runbook

1. Start the authorized connector flow at `/api/connectors` (slot 6); callbacks use `/api/oauth-callback` (slot 7). Store credentials only in approved server-side encrypted systems.
2. Discover eligible accounts and require explicit selection whenever more than one account, store, marketplace, organization, or ad account is available. Verify ownership before financial or commerce sync.
3. Queue `connector_sync` at `/api/jobs` (slot 9). Use a checkpoint, source-scoped idempotency key, provider cursor when available, and provider-aware pagination/rate limiting.
4. An incremental sync resumes after the checkpoint; a historical import requires explicit authorization and preserves period labels. A verified provider webhook may queue a follow-up job through `/api/webhooks/{provider}` (slot 8), never bypassing signature and idempotency controls.
5. On rate limits or outages, honor provider retry guidance and back off. On partial completion, retain a checkpoint and record the completed scope. On authorization failure, request reauthorization; on ambiguity, use review or manual upload.

No connector can guarantee data completeness, fee recovery, funding availability, a provider decision, or an underwriting outcome.
