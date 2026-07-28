# Wix Entitlement Sync Runbook

Accept only verified Wix webhooks at `/api/webhooks/{provider}` slot 8. Deduplicate by provider event ID, map the source event to an existing canonical event, then update entitlement, role, CRM labels, group access, and dashboard handoff. Retry through the webhook policy; retain the existing entitlement and place failures in the manual queue.
