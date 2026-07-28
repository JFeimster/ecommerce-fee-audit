# Webhook Operations Runbook

Verify signature and timestamp, deduplicate the provider event, persist a redacted audit record, acknowledge accepted payloads, and route asynchronous work to `/api/jobs`. Reject invalid signatures without logging secrets. For ambiguous delivery, verify provider status and idempotency before retry. Escalate exhausted retries to dead-letter review; rotate secrets through the approved secret manager only.
