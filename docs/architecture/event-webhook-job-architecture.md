# Event, Webhook, and Job Architecture

All events remain compatible with `api/schemas/event-envelope.schema.json`. Provider ingress is multiplexed through `/api/webhooks/{provider}` on slot 8; asynchronous work is multiplexed through `/api/jobs` on slot 9. Signature verification, idempotency, durable audit logs, bounded retries, and dead-letter records apply before requeue. Funding and dispute automation may run autonomously after configured authorization and thresholds; human review occurs only on configured triggers.
